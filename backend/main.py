from __future__ import annotations

import asyncio
import ipaddress
import os
import re
import socket
from io import BytesIO
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, RedirectResponse
from pydantic import BaseModel, Field, HttpUrl
from pypdf import PdfReader

import database as db
import catalog
from engine import analyze_case, default_requirements

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(Path(__file__).parent / ".env")
db.init_db()

app = FastAPI(title="Shinchan's Clue Club API", version="1.1.0", description="Evidence-first mystery research case API")
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
app.add_middleware(CORSMiddleware, allow_origins=[frontend_origin, "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["GET", "POST", "PATCH", "DELETE"], allow_headers=["*"])


class CaseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    question: str = Field(min_length=8, max_length=2000)
    context: str = Field(default="", max_length=3000)
    jurisdiction: str = Field(default="", max_length=200)
    decision_date: str = ""
    requirements: list[dict] = Field(default_factory=list)


class SourceText(BaseModel):
    title: str = Field(min_length=1, max_length=240)
    text: str = Field(min_length=20, max_length=250000)
    url: str = ""
    publisher: str = ""
    published_date: str = ""


class URLSource(BaseModel):
    url: str = Field(min_length=8, max_length=2000)
    title: str = ""
    publisher: str = ""
    published_date: str = ""


class TaskUpdate(BaseModel):
    status: str | None = None
    notes: str | None = None
    title: str | None = None
    description: str | None = None
    priority: str | None = None
    sort_order: int | None = None


class ChallengeAnswer(BaseModel):
    answer_id: str = Field(min_length=1, max_length=120)


class ChallengeHintRequest(BaseModel):
    level: int = Field(default=0, ge=0, le=2)


class CaseUpdate(BaseModel):
    title: str | None = None
    question: str | None = None
    context: str | None = None
    jurisdiction: str | None = None
    decision_date: str | None = None
    status: str | None = None
    requirements: list[dict] | None = None


def require_case(case_id: str) -> dict:
    case = db.get_case(case_id)
    if not case:
        raise HTTPException(404, "Research case not found")
    return case


def _public_source(source: dict) -> dict:
    return source


@app.get("/api/health")
def health():
    return {"ok": True, "service": "Shinchan's Clue Club API", "ai_configured": bool(os.getenv("OPENAI_API_KEY"))}


@app.get("/", include_in_schema=False)
def clubhouse():
    return RedirectResponse(url=frontend_origin)


@app.get("/api/cases")
def cases():
    return db.list_cases()


@app.get("/api/library")
def sample_library():
    return catalog.public_index()


@app.post("/api/library/{slug}")
def open_library_case(slug: str):
    item = catalog.find_case(slug)
    if not item:
        raise HTTPException(404, "Sample investigation not found")
    case = db.create_case({
        "title": item["title"], "question": item["question"], "context": item["context"],
        "jurisdiction": item["jurisdiction"], "decision_date": item["decision_date"],
        "requirements": item["requirements"],
        "play_mode": item.get("play_mode", "guided"),
        "challenge": item.get("challenge"),
        "status": "unsolved" if item.get("play_mode") == "challenge" else "active",
    })
    for source in item["sources"]:
        db.add_source(case["id"], {
            **source,
            "source_type": source.get("source_type", "curated fictional sample"),
        })
    case = db.get_case(case["id"])
    if item.get("play_mode") != "challenge":
        result = analyze_case(case, case["sources"])
        db.add_analysis(case["id"], result, result["method"])
    return db.get_case(case["id"])


@app.post("/api/cases/{case_id}/challenge/answer")
def submit_challenge_answer(case_id: str, body: ChallengeAnswer):
    case = require_case(case_id)
    if case.get("play_mode") != "challenge" or not case.get("challenge"):
        raise HTTPException(400, "This case does not have a final verdict challenge")
    if not case.get("analysis_runs"):
        raise HTTPException(409, "Run the clue patrol before submitting your final verdict")
    result = db.answer_challenge(case_id, body.answer_id)
    if result is None:
        raise HTTPException(404, "Challenge case not found")
    return {**result, "case": db.get_case(case_id)}


@app.post("/api/cases/{case_id}/challenge/hint")
def reveal_challenge_hint(case_id: str, body: ChallengeHintRequest):
    result = db.challenge_hint(case_id, body.level)
    if result is None:
        raise HTTPException(404, "Challenge case not found")
    return result


@app.post("/api/cases")
def create_case(body: CaseCreate):
    data = body.model_dump()
    if not data["requirements"]:
        data["requirements"] = default_requirements(data["question"])
    return db.create_case(data)


@app.get("/api/cases/{case_id}")
def case_detail(case_id: str):
    return require_case(case_id)


@app.patch("/api/cases/{case_id}")
def patch_case(case_id: str, body: CaseUpdate):
    result = db.update_case(case_id, body.model_dump(exclude_none=True))
    if result is None:
        raise HTTPException(404, "Research case not found")
    return result


@app.delete("/api/cases/{case_id}")
def remove_case(case_id: str):
    if not db.delete_case(case_id):
        raise HTTPException(404, "Research case not found")
    return {"deleted": True}


@app.post("/api/cases/{case_id}/sources/text")
def add_text_source(case_id: str, body: SourceText):
    require_case(case_id)
    source = db.add_source(case_id, {**body.model_dump(), "source_type": "pasted excerpt"})
    return source


def _validate_public_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise HTTPException(400, "Use a complete http or https URL")
    if parsed.username or parsed.password:
        raise HTTPException(400, "URLs with embedded credentials are not allowed")
    if parsed.port and parsed.port not in (80, 443):
        raise HTTPException(400, "Only standard web ports are allowed")
    host = parsed.hostname.rstrip(".").lower()
    if host in ("localhost", "localhost.localdomain") or host.endswith(".local"):
        raise HTTPException(400, "Local network URLs are not allowed")
    try:
        addresses = socket.getaddrinfo(host, parsed.port or (443 if parsed.scheme == "https" else 80), type=socket.SOCK_STREAM)
    except socket.gaierror:
        raise HTTPException(400, "The host name could not be resolved")
    for item in addresses:
        ip = ipaddress.ip_address(item[4][0])
        if not ip.is_global:
            raise HTTPException(400, "Private or reserved network addresses are not allowed")


async def _fetch_source(url: str) -> tuple[str, str, str]:
    current = url
    timeout = httpx.Timeout(12.0, connect=5.0)
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=False, headers={"User-Agent": "ShinchanClueClub/1.1 (research source preview)"}) as client:
        for _ in range(5):
            _validate_public_url(current)
            try:
                async with client.stream("GET", current) as response:
                    if response.status_code in (301, 302, 303, 307, 308):
                        location = response.headers.get("location")
                        if not location:
                            raise HTTPException(400, "The source redirected without a destination")
                        current = urljoin(current, location)
                        continue
                    if response.status_code >= 400:
                        raise HTTPException(400, f"The source returned HTTP {response.status_code}")
                    content_type = response.headers.get("content-type", "").split(";")[0].lower()
                    if content_type not in ("text/html", "text/plain", "application/pdf", "application/xhtml+xml"):
                        raise HTTPException(415, f"Unsupported source type: {content_type or 'unknown'}")
                    chunks, size = [], 0
                    async for chunk in response.aiter_bytes():
                        size += len(chunk)
                        if size > 7_000_000:
                            raise HTTPException(413, "Source is larger than the 7 MB import limit")
                        chunks.append(chunk)
                    content = b"".join(chunks)
                    if content_type == "application/pdf" or content.startswith(b"%PDF"):
                        reader = PdfReader(BytesIO(content))
                        text = "\n\n".join(f"[Page {i+1}] {page.extract_text() or ''}" for i, page in enumerate(reader.pages))
                        title = Path(urlparse(current).path).name or "PDF source"
                    elif content_type in ("text/html", "application/xhtml+xml"):
                        soup = BeautifulSoup(content, "html.parser")
                        title = (soup.title.string.strip() if soup.title and soup.title.string else "")
                        for node in soup(["script", "style", "nav", "footer", "header", "noscript", "svg"]):
                            node.decompose()
                        main = soup.find("main") or soup.find("article") or soup.body or soup
                        text = "\n".join(line.strip() for line in main.get_text("\n").splitlines() if line.strip())
                    else:
                        title, text = Path(urlparse(current).path).name or "Text source", content.decode("utf-8", errors="replace")
                    text = text.strip()[:250000]
                    if len(text) < 20:
                        raise HTTPException(422, "The source did not contain enough extractable text")
                    return current, title, text
            except httpx.TimeoutException:
                raise HTTPException(504, "Timed out while fetching the source")
            except httpx.HTTPError as exc:
                raise HTTPException(502, f"Could not fetch source: {str(exc)[:160]}")
        raise HTTPException(400, "Too many redirects")


@app.post("/api/cases/{case_id}/sources/url")
async def add_url_source(case_id: str, body: URLSource):
    require_case(case_id)
    final_url, fetched_title, text = await _fetch_source(body.url)
    title = body.title.strip() or fetched_title
    publisher = body.publisher.strip() or urlparse(final_url).hostname or ""
    source = db.add_source(case_id, {"title": title, "url": final_url, "publisher": publisher, "published_date": body.published_date, "text": text, "source_type": "fetched webpage"})
    return source


def _extract_docx(content: bytes) -> str:
    import xml.etree.ElementTree as ET
    from zipfile import ZipFile
    with ZipFile(BytesIO(content)) as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    return "\n".join("".join(t.text or "" for t in p.findall(".//w:t", ns)) for p in root.findall(".//w:p", ns))


@app.post("/api/cases/{case_id}/sources/upload")
async def upload_source(case_id: str, file: UploadFile = File(...), title: str = "", publisher: str = "", published_date: str = ""):
    require_case(case_id)
    filename = Path(file.filename or "source").name
    ext = Path(filename).suffix.lower()
    if ext not in (".pdf", ".txt", ".md", ".docx"):
        raise HTTPException(415, "Upload a PDF, DOCX, TXT, or Markdown file")
    content = await file.read(8_000_001)
    if len(content) > 8_000_000:
        raise HTTPException(413, "File is larger than the 8 MB upload limit")
    inferred_title = inferred_publisher = inferred_date = ""
    try:
        if ext == ".pdf":
            reader = PdfReader(BytesIO(content))
            text = "\n\n".join(f"[Page {i+1}] {p.extract_text() or ''}" for i, p in enumerate(reader.pages))
        elif ext == ".docx":
            text = _extract_docx(content)
        else:
            text = content.decode("utf-8", errors="replace")
            if ext == ".md":
                frontmatter = re.match(r"\A---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)", text, re.S)
                if frontmatter:
                    metadata = {}
                    for line in frontmatter.group(1).splitlines():
                        key, separator, value = line.partition(":")
                        if separator:
                            metadata[key.strip().lower()] = value.strip().strip("\"'")
                    inferred_title = metadata.get("title", "")
                    inferred_publisher = metadata.get("publisher", "")
                    inferred_date = metadata.get("published_date", "")
                    text = text[frontmatter.end():]
    except Exception as exc:
        raise HTTPException(422, f"Could not extract text: {str(exc)[:180]}")
    if len(text.strip()) < 20:
        raise HTTPException(422, "No readable text was found in this file")
    return db.add_source(case_id, {"title": title.strip() or inferred_title or filename, "publisher": publisher.strip() or inferred_publisher, "published_date": published_date.strip() or inferred_date, "text": text[:250000], "source_type": f"uploaded {ext[1:]}", "original_filename": filename})


@app.delete("/api/cases/{case_id}/sources/{source_id}")
def remove_source(case_id: str, source_id: str):
    require_case(case_id)
    if not db.delete_source(case_id, source_id):
        raise HTTPException(404, "Source not found")
    return {"deleted": True}


@app.post("/api/cases/{case_id}/analyze")
def run_analysis(case_id: str):
    case = require_case(case_id)
    sources = db.get_sources(case_id)
    if not sources:
        raise HTTPException(400, "Add at least one source before running the patrol")
    required_file = (case.get("challenge") or {}).get("bonus_source", {}).get("filename")
    if case.get("play_mode") == "challenge" and required_file and not any(source.get("original_filename") == required_file for source in sources):
        raise HTTPException(409, f"Import {required_file} from Source Locker before running this challenge patrol")
    result = analyze_case(case, sources)
    run = db.add_analysis(case_id, result, result["method"])
    return {"run": run, "case": db.get_case(case_id)}


@app.patch("/api/tasks/{task_id}")
def patch_task(task_id: str, body: TaskUpdate):
    patch = body.model_dump(exclude_none=True)
    if "status" in patch and patch["status"] not in ("open", "in-progress", "verified", "dismissed"):
        raise HTTPException(422, "Invalid task status")
    result = db.update_task(task_id, patch)
    if not result:
        raise HTTPException(404, "Verification task not found")
    return result


@app.get("/api/cases/{case_id}/report.md", response_class=PlainTextResponse)
def report(case_id: str):
    case = require_case(case_id)
    if not case["analysis_runs"]:
        raise HTTPException(400, "Run an analysis before exporting a briefing")
    result = case["analysis_runs"][0]["result"]
    lines = [f"# Shinchan's Clue Club — {case['title']}", "", f"**Research question:** {case['question']}", f"**Analysis method:** {result.get('method', 'Unknown')}", f"**Generated:** {result.get('generated_at', '')}", "", f"> {result.get('ai_notice', 'Analysis method and limitations should be reviewed.')}", "", "## Source snapshot"]
    for item in result.get("summary", []):
        source = next((candidate for candidate in case["sources"] if candidate["id"] == item["source_id"]), {})
        lines += [f"### {item['title']}", f"Date: {item.get('published_date') or 'not listed'} · Publisher: {item.get('publisher') or 'not listed'}", f"Source: {source.get('url') or source.get('original_filename') or 'local/pasted record'} · Retrieved {source.get('retrieved_at', 'unknown')}", item["summary"], ""]
    lines.append("## Requirement coverage")
    for item in result.get("coverage", []):
        lines += [f"### [{item.get('status', 'not-reviewed').upper()}] {item['requirement'].get('label', item['requirement'].get('category', 'Requirement'))}", item.get("reason", ""), f"**Next step:** {item.get('next_step', 'Review the source records.')}"]
        for evidence in item.get("evidence", []):
            lines += [f"> {evidence['quote']}", f"> — {evidence['source_title']} ({evidence.get('published_date') or 'date not listed'})"]
        lines.append("")
    lines.append("## Findings")
    for finding in result.get("findings", []):
        lines += [f"### [{finding['type'].upper()}] {finding['title']}", finding["explanation"], ""]
        for evidence in finding.get("evidence", []):
            lines.append(f"> {evidence['quote']}")
            lines.append(f"> — {evidence['source_title']} ({evidence.get('published_date') or 'date not listed'}) {evidence.get('url', '')}")
        task = finding.get("task")
        if task:
            lines += ["", f"**Verify next:** {task['title']}"]
        lines.append("")
    lines += ["## Limitations", "Signals describe the sources in this case. ‘Not found’ does not prove information does not exist. Confirm important details with the current official source."]
    if case.get("challenge"):
        lines += ["", "## Player verdict", f"Status: {'solved' if case.get('status') == 'solved' else 'unsolved'} · Attempts: {case.get('challenge_attempts', 0)}"]
        if case.get("status") == "solved":
            lines += ["", case["challenge"].get("resolution", "The player solved this case.")]
        unresolved = [item for item in result.get("coverage", []) if item.get("status") in ("not-found", "partial")]
        if unresolved:
            lines.append("\n### Still needs confirmation")
            for item in unresolved:
                lines.append(f"- **{item['requirement'].get('label', item['requirement'].get('category'))}:** {item.get('next_step', 'Confirm with a current authoritative source.')}")
    return "\n".join(lines)


@app.post("/api/demo")
def load_demo():
    case = db.create_case({
        "title": "Shinchan's Scholarship Puzzle · sample file",
        "question": "What should I verify before applying for this scholarship?",
        "context": "A fictional scholarship program used to demonstrate document, deadline, and renewal checks.",
        "jurisdiction": "Sample only",
        "decision_date": "",
        "requirements": default_requirements("What should I verify before applying for this scholarship?"),
    })
    db.add_source(case["id"], {"title": "Round notice · fictional sample", "publisher": "Sample program office", "published_date": "2025-02-01", "text": "SAMPLE — NOT REAL SCHOLARSHIP RULES. Applicants must submit proof of enrollment and household income. Applications close March 15. This notice describes eligibility for the sample award. It does not establish the current application round.", "source_type": "synthetic demo source"})
    db.add_source(case["id"], {"title": "Scholarship FAQ · fictional sample", "publisher": "Sample program office", "published_date": "2026-01-10", "text": "SAMPLE — NOT REAL SCHOLARSHIP RULES. To apply, submit proof of enrollment, income documentation, and one reference letter. Applicants can contact the program office for further information. This sample FAQ does not include a current application deadline or renewal conditions.", "source_type": "synthetic demo source"})
    case = db.get_case(case["id"])
    result = analyze_case(case, case["sources"])
    db.add_analysis(case["id"], result, result["method"])
    return db.get_case(case["id"])
