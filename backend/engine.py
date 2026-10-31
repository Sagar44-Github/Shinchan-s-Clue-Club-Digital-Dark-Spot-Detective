from __future__ import annotations

import re
from datetime import date, datetime, timezone
from typing import Any

from ai import AIAnalysis, analyze_with_openai, available

CATEGORIES: dict[str, dict[str, Any]] = {
    "deadline": {"label": "Current deadline", "terms": ["deadline", "close", "due", "application period", "last date", "submit by"]},
    "eligibility": {"label": "Eligibility and exclusions", "terms": ["eligible", "eligibility", "applicant must", "reside", "citizen", "enrolled", "minimum gpa"]},
    "documents": {"label": "Required documents", "terms": ["document", "submit", "proof", "letter", "transcript", "income", "certificate", "id card"]},
    "renewal": {"label": "Renewal and retention rules", "terms": ["renew", "renewal", "retain", "continuation", "gpa requirement"]},
    "submission": {"label": "Application route", "terms": ["apply", "application link", "portal", "submit online", "submission"]},
    "fees": {"label": "Fees and costs", "terms": ["fee", "cost", "tuition", "stipend", "amount", "award"]},
    "contact": {"label": "Official contact route", "terms": ["contact", "email", "office", "phone", "help desk"]},
}
DATE_RE = re.compile(r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:,?\s+20\d{2})?\b|\b20\d{2}-\d{2}-\d{2}\b", re.I)
DOC_TERMS = {
    "enrollment proof": ["proof of enrollment", "enrollment certificate", "student status"],
    "income proof": ["household income", "income documentation", "income proof", "tax return"],
    "reference letter": ["reference letter", "recommendation letter"],
    "transcript": ["transcript", "grade report"],
    "identity proof": ["identity card", "id card", "proof of identity"],
}


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]


def _doc_set(text: str) -> set[str]:
    lower = text.lower()
    return {name for name, terms in DOC_TERMS.items() if any(term in lower for term in terms)}


def _source_age(source: dict) -> int | None:
    raw = source.get("published_date") or ""
    if not raw:
        return None
    try:
        published = date.fromisoformat(raw[:10])
        return (date.today() - published).days
    except ValueError:
        return None


def _evidence(source: dict, quote: str, relation: str = "checked") -> dict:
    return {"source_id": source["id"], "source_title": source["title"], "url": source.get("url", ""), "published_date": source.get("published_date", ""), "quote": quote, "relation": relation}


def default_requirements(question: str) -> list[dict]:
    lower = question.lower()
    requested = ["deadline", "eligibility", "documents", "renewal", "submission", "fees", "contact"]
    if any(w in lower for w in ["scholarship", "grant", "apply", "application"]):
        requested = ["deadline", "eligibility", "documents", "renewal", "submission", "fees", "contact"]
    return [{"id": f"req-{key}", "category": key, "label": CATEGORIES[key]["label"], "importance": "high" if key in ["deadline", "eligibility", "documents"] else "normal", "origin": "suggested"} for key in requested]


def _find_claims(sources: list[dict], requirements: list[dict] | None = None) -> list[dict]:
    claims = []
    requirements = requirements or []
    for source in sources:
        for sentence in _sentences(source.get("text", "")):
            lower = sentence.lower()
            categories = [key for key, cfg in CATEGORIES.items() if any(term in lower for term in cfg["terms"])]
            for req in requirements:
                terms = req.get("terms") or []
                if any(str(term).lower() in lower for term in terms):
                    categories.append(req.get("category", "general"))
            if not categories:
                categories = ["general"]
            dates = DATE_RE.findall(sentence)
            claims.append({"id": f"clm-{source['id']}-{len(claims)}", "source_id": source["id"], "source_title": source["title"], "quote": sentence, "categories": list(dict.fromkeys(categories)), "date_or_value": ", ".join(dates), "origin": "source text", "url": source.get("url", ""), "published_date": source.get("published_date", "")})
    return claims


def _fact_values(text: str) -> dict[str, set[str]]:
    """Extract comparable facts without treating every number as a contradiction."""
    times = set(re.findall(r"\b\d{1,2}(?::\d{2})?\s*(?:AM|PM)\b|\bmidnight\s+UTC\b", text, re.I))
    money = set(re.findall(r"(?:¥|\$)\s?\d[\d,]*(?:\.\d+)?", text, re.I))
    dates = set(DATE_RE.findall(text))
    durations = set(re.findall(r"\b\d+\s*(?:hours?|days?|weeks?|months?|years?)\b", text, re.I))
    def clean(items: set[str]) -> set[str]:
        return {re.sub(r"\s+", " ", item.lower()).strip() for item in items}
    return {"time": clean(times), "money": clean(money), "date": clean(dates), "duration": clean(durations)}


def _custom_requirement_conflicts(req: dict, sources: list[dict]) -> list[dict] | None:
    terms = [str(term).lower() for term in req.get("terms", []) if str(term).strip()]
    if not terms:
        return None
    passages: list[tuple[dict, str, dict[str, set[str]]]] = []
    for source in sources:
        matched = [sentence for sentence in _sentences(source.get("text", "")) if any(term in sentence.lower() for term in terms)]
        if matched:
            excerpt = " ".join(matched[:3])[:700]
            passages.append((source, excerpt, _fact_values(excerpt)))
    for i, (left, left_text, left_facts) in enumerate(passages):
        for right, right_text, right_facts in passages[i + 1:]:
            for kind in ("time", "money", "date", "duration"):
                a, b = left_facts[kind], right_facts[kind]
                if a and b and a != b and bool(a - b) and bool(b - a):
                    label = req.get("label", req.get("category", "detail"))
                    return _finding(
                        f"conflict-{req.get('category', 'detail')}-{left['id']}-{right['id']}",
                        "conflict",
                        f"Sources differ on {label.lower()}",
                        f"The reviewed passages report different {kind} details for this check. Confirm that the sources cover the same version, location, and date before relying on either one.",
                        "high",
                        [_evidence(left, left_text, "first source value"), _evidence(right, right_text, "different source value")],
                        f"Compare the current authoritative record for {label.lower()}.",
                    )
    return None


def _comparison_value(kind: str, text: str) -> str | None:
    """Extract a value only in its requirement context, avoiding unrelated times."""
    patterns = {
        "gate": r"(?:family\s+)?(?:check[ -]?in|meet(?:ing)?|arrival)(?:\s+(?:is|moves|will be|should be))?\s+(?:at\s+)?(?:the\s+)?([a-z][a-z -]*?\bgate)\b",
        "checkin": r"(?:family\s+)?check[ -]?in(?:\s+(?:is|begins|starts))?(?:\s+at)?(?:\s+(?:the\s+)?[a-z][a-z -]*?\bgate)?\s+(?:is\s+)?(?:at\s+)?(\d{1,2}(?::\d{2})?\s*(?:am|pm))\b",
        "wristband": r"\b(yellow\s+badge|blue\s+wristband|green\s+name\s+tag)\b",
    }
    pattern = patterns.get(kind)
    match = re.search(pattern, text, re.I) if pattern else None
    return re.sub(r"\s+", " ", match.group(1)).strip().title() if match else None


def _positive_support(req: dict, sentence: str) -> bool:
    lowered = sentence.casefold()
    for raw in req.get("support_patterns", []):
        pattern = str(raw).casefold().strip()
        index = lowered.find(pattern)
        if not pattern or index < 0:
            continue
        clause_start = max(lowered.rfind(mark, 0, index) for mark in (".", ";", "!", "?")) + 1
        prefix = lowered[max(clause_start, index - 90):index]
        if not re.search(r"\b(?:no|not|never|doesn't|does not|isn't|is not|cannot|can't|unconfirmed|unknown|without)\b", prefix):
            return True
    return False


def _structured_requirement_conflicts(req: dict, sources: list[dict]) -> list[dict]:
    kind = req.get("compare_kind")
    if not kind:
        return []
    records = []
    terms = [str(term).lower() for term in req.get("terms", []) if str(term).strip()]
    for source in sources:
        matches = [sentence for sentence in _sentences(source.get("text", "")) if any(term in sentence.lower() for term in terms)]
        for sentence in matches:
            value = _comparison_value(kind, sentence)
            if value:
                records.append((source, sentence, value))
    if len(records) < 2:
        return []
    preferred_pattern = str(req.get("preferred_source_pattern", "")).casefold()
    preferred = next((record for record in records if preferred_pattern and preferred_pattern in f"{record[0].get('title', '')} {record[0].get('publisher', '')}".casefold()), None)
    dated = [record for record in records if record[0].get("published_date")]
    anchor = preferred or (max(dated, key=lambda record: record[0].get("published_date", "")) if dated else None)
    if anchor is None:
        return []
    others = [record for record in records if record is not anchor and record[2].casefold() != anchor[2].casefold()]
    if not others:
        return []
    label = req.get("label", "this detail")
    findings = []
    for other_index, other in enumerate(others):
        other_date = other[0].get("published_date") or "undated"
        anchor_date = anchor[0].get("published_date") or "date not listed"
        finding = _finding(
            f"conflict-{req.get('category', 'detail')}-{other[0]['id']}-{anchor[0]['id']}",
            "conflict",
            f"Records differ on {label.lower()}",
            f"The reviewed records give different {label.lower()} values: {other[2]} in {other[0]['title']} ({other_date}) and {anchor[2]} in {anchor[0]['title']} ({anchor_date}). The organizer record may replace earlier guidance; the undated claim remains unverified. Confirm that the organizer notice applies to this event and scope.",
            "high",
            [_evidence(other[0], other[1], f"{other_date} record says {other[2]}"), _evidence(anchor[0], anchor[1], f"dated organizer record says {anchor[2]}")],
            f"Confirm the current {label.lower()} using the dated organizer record.",
            requirement_category=req.get("category"),
        )
        # Several records can disagree about the same requirement. Preserve
        # each comparison signal, but create one mission action for that
        # requirement instead of repeating the same task for every pair.
        if other_index > 0:
            finding.pop("task", None)
        findings.append(finding)
    return findings


def _superseded_source_findings(sources: list[dict]) -> list[dict]:
    findings = []
    dated = [source for source in sources if source.get("published_date")]
    for newer in dated:
        if not re.search(r"\b(?:replaces|supersedes|revised bulletin|revised update|superseded)\b", newer.get("text", ""), re.I):
            continue
        sentence = next((part for part in _sentences(newer.get("text", "")) if re.search(r"\b(?:replaces|supersedes|superseded)\b", part, re.I)), "")
        if not sentence:
            continue
        for older in dated:
            if older is newer or older.get("published_date", "") >= newer.get("published_date", ""):
                continue
            findings.append(_finding(
                f"superseded-{older['id']}-{newer['id']}", "freshness",
                f"A later record says it replaces {older['title']}",
                f"{newer['title']} explicitly says it replaces an earlier record. Treat the older record as historical context and check that the later notice applies to the same event and scope.",
                "high",
                [_evidence(older, _best_excerpt(older["text"], ["check-in", "meet", "gate"]), "earlier dated record"), _evidence(newer, sentence, "later record explicitly says it replaces earlier guidance")],
                f"Use the current organizer record to confirm any remaining details from {older['title']}.",
            ))
    return findings


def analyze_case(case: dict, sources: list[dict]) -> dict:
    requirements = case.get("requirements") or default_requirements(case["question"])
    findings: list[dict] = []
    claims = _find_claims(sources, requirements)
    method = "Rule-based evidence review"
    ai_data: AIAnalysis | None = None
    ai_notice = "AI is not configured; local evidence rules are active."
    if available() and sources:
        try:
            ai_data = analyze_with_openai(case["question"], requirements, sources)
            method = "AI-assisted + deterministic checks"
            ai_notice = "AI extraction is advisory; every accepted quote is validated against the source text."
            for item in ai_data.claims:
                source = next((s for s in sources if s["id"] == item.source_id), None)
                if source and item.quote.strip() and item.quote.strip() in source["text"]:
                    claims.append({"id": f"ai-{source['id']}-{len(claims)}", "source_id": source["id"], "source_title": source["title"], "quote": item.quote.strip(), "claim": item.claim, "categories": [item.category], "date_or_value": item.date_or_value, "scope": item.scope, "caveat": item.caveat, "origin": "AI-extracted, quote verified", "url": source.get("url", ""), "published_date": source.get("published_date", "")})
        except Exception as exc:
            ai_notice = f"AI review failed; deterministic checks completed. {type(exc).__name__}: {str(exc)[:180]}"

    for req in requirements:
        key = req.get("category", "general")
        cfg = CATEGORIES.get(key, {"label": req.get("label", key), "terms": req.get("terms") or [req.get("label", key).lower()]})
        relevant = [s for s in sources if any(term in s["text"].lower() for term in cfg["terms"])]
        if key == "deadline":
            current_dates = [s for s in sources if _source_age(s) is not None and _source_age(s) <= 365 and DATE_RE.search(s["text"])]
            if not current_dates:
                evidence = [_evidence(s, _best_excerpt(s["text"], cfg["terms"]), "checked; no current dated deadline established") for s in sources]
                findings.append(_finding("gap-deadline", "gap", "Current deadline is not established", "No current dated deadline was found in the reviewed sources. An old application date does not establish the active round.", "urgent", evidence, "Find the active official notice and confirm the deadline and time zone.", requirement_category=key))
        elif key == "renewal":
            policy = [s for s in relevant if re.search(r"renew\w*.{0,80}(?:requires|must|minimum|gpa|credit|criteria|maintain)|(?:requires|must|minimum|gpa|credit|criteria|maintain).{0,80}renew\w*", s["text"], re.I)]
            if not policy:
                evidence = [_evidence(s, s["text"][:300], "checked; renewal conditions not found in this excerpt") for s in sources]
                findings.append(_finding("gap-renewal", "gap", "Renewal conditions are not covered", "The excerpts do not establish whether the award renews or what recipients must do to retain it. This is a gap in this source set, not proof that no policy exists.", "high", evidence, "Locate the official renewal policy or ask the program office for the current retention conditions.", requirement_category=key))
        elif req.get("support_patterns"):
            support_patterns = [str(term).casefold() for term in req.get("support_patterns", []) if str(term).strip()]
            positive = [sentence for source in sources for sentence in _sentences(source.get("text", "")) if _positive_support(req, sentence)]
            if not positive:
                evidence = []
                search_terms = [str(term).casefold() for term in req.get("terms", []) if str(term).strip()]
                for source in sources:
                    relevant_sentences = [sentence for sentence in _sentences(source.get("text", "")) if any(term in sentence.casefold() for term in search_terms)]
                    if relevant_sentences:
                        evidence.extend(_evidence(source, sentence, "checked; mentions the detail but does not confirm an arrangement") for sentence in relevant_sentences[:2])
                    else:
                        evidence.append(_evidence(source, source.get("text", "")[:250], "source checked; no positive confirmation found"))
                findings.append(_finding(
                    f"gap-{key}", "gap", f"{cfg['label']} not confirmed in reviewed sources",
                    f"The reviewed records mention this detail but provide no positive confirmation matching the requested arrangement. This means it was not found in this case's source set; it does not prove that no arrangement exists.",
                    "high", evidence, req.get("next_action") or f"Confirm {cfg['label'].lower()} with a current authoritative source.", requirement_category=key,
                ))
        elif not relevant:
            evidence = [_evidence(s, s["text"][:260], "checked; no matching passage found") for s in sources]
            findings.append(_finding(f"gap-{key}", "gap", f"{cfg['label']} not found in reviewed sources", f"No passage matching {cfg['label'].lower()} was found in this case's source set.", "normal", evidence, f"Find an authoritative source covering {cfg['label'].lower()}.", requirement_category=key))
        elif key not in CATEGORIES:
            structured_conflicts = _structured_requirement_conflicts(req, sources)
            if structured_conflicts:
                findings.extend(structured_conflicts)
            else:
                custom_conflict = _custom_requirement_conflicts(req, sources)
                if custom_conflict:
                    custom_conflict["requirement_category"] = key
                    findings.append(custom_conflict)

    if len(sources) > 1:
        doc_sources = [(s, _doc_set(s["text"])) for s in sources]
        doc_sources = [(s, docs) for s, docs in doc_sources if docs]
        for i, (a, a_docs) in enumerate(doc_sources):
            for b, b_docs in doc_sources[i + 1:]:
                diff = a_docs.symmetric_difference(b_docs)
                if diff:
                    detail = ", ".join(sorted(diff))
                    evidence = [_evidence(a, _document_excerpt(a["text"]), "document list in this source"), _evidence(b, _document_excerpt(b["text"]), "document list in this source")]
                    findings.append(_finding(f"conflict-docs-{a['id']}-{b['id']}", "conflict", "Required document lists differ", f"These excerpts differ on: {detail}. Confirm they cover the same application round and whether either list is complete.", "high", evidence, f"Check the current official checklist for {detail}."))
                    break
            else:
                continue
            break

    for source in sources:
        age = _source_age(source)
        if age is None:
            findings.append(_finding(f"date-unknown-{source['id']}", "freshness", f"Publication date not found: {source['title']}", "The source has no publication date in its metadata. Its currentness cannot be established from the date field.", "normal", [_evidence(source, source["text"][:220], "source checked")], "Look for a visible updated date or compare this page with the latest official notice."))
        elif age > 365:
            findings.append(_finding(f"stale-{source['id']}", "freshness", f"Older source may describe an earlier round: {source['title']}", f"Published {source.get('published_date')}; about {age} days old. Age is a reason to verify, not evidence that the source is false.", "high", [_evidence(source, _best_excerpt(source["text"], ["deadline", "close", "round"]), "dated source")], "Replace or corroborate this with the current official notice."))

    findings.extend(_superseded_source_findings(sources))

    if not findings:
        findings.append(_finding("review-complete", "clear", "No major gap signal detected", "The current checks found no clear gap, mismatch, or age warning. Manually inspect the official sources before deciding.", "normal", [_evidence(s, s["text"][:250]) for s in sources], "Review the source excerpts and confirm details with the official source."))

    summary = []
    for source in sources:
        sentences = _sentences(source["text"])
        summary.append({"source_id": source["id"], "title": source["title"], "publisher": source.get("publisher", ""), "url": source.get("url", ""), "published_date": source.get("published_date", ""), "summary": " ".join(sentences[:3])[:650], "evidence": [_evidence(source, s) for s in sentences[:3]]})

    coverage = []
    for req in requirements:
        key = req.get("category", "general")
        matching = [c for c in claims if key in c.get("categories", [])]
        matching_findings = [f for f in findings if f.get("requirement_category") == key or f.get("id", "").startswith(f"gap-{key}") or (key == "documents" and f["type"] == "conflict")]
        status = "conflicting" if any(f["type"] == "conflict" for f in matching_findings) else "not-found" if not matching else "covered"
        required_phrases = [str(term).lower() for term in req.get("must_mention", [])]
        present_phrases = [term for term in required_phrases if any(term in claim["quote"].lower() for claim in matching)]
        if status == "covered" and required_phrases and len(present_phrases) < len(required_phrases):
            status = "partial"
        if req.get("support_patterns") and any(f.get("id") == f"gap-{key}" for f in matching_findings):
            status = "not-found"
        if key in ("deadline", "renewal") and any(f["id"] == f"gap-{key}" or f["id"].startswith(f"gap-{key}") for f in findings):
            status = "not-found"
        evidence = []
        for claim in matching:
            source = next((item for item in sources if item["id"] == claim["source_id"]), None)
            if source:
                evidence.append(_evidence(source, claim["quote"], "matched passage"))
        if req.get("support_patterns") and status == "not-found" and not any(_positive_support(req, item["quote"]) for item in evidence):
            evidence = []
            for finding in matching_findings:
                if finding.get("type") == "gap":
                    evidence.extend(finding.get("evidence", []))
        related = next((finding for finding in matching_findings if finding.get("task")), None)
        reason = {
            "conflicting": "The reviewed source passages report different values; check dates and scope.",
            "not-found": "No matching passage was found in the source records reviewed for this case.",
            "partial": "Some required detail appears, but one or more requested sub-details are not covered.",
            "covered": "One or more source passages match this requirement. Review the cited source before relying on it.",
        }.get(status, "This requirement has not been reviewed.")
        next_step = related["task"]["title"] if related else (f"Confirm {req.get('label', key)} with a current authoritative source." if status != "covered" else "Inspect the linked passage and confirm it applies to this event.")
        coverage.append({"requirement": req, "status": status, "claim_ids": [c["id"] for c in matching], "evidence": evidence, "finding_ids": [f["id"] for f in matching_findings], "reason": reason, "next_step": next_step})

    unanswered = list(ai_data.unanswered_questions if ai_data else [])
    for item in coverage:
        if item["status"] in ("not-found", "partial"):
            question = f"What current official record can confirm {item['requirement'].get('label', item['requirement']['category']).lower()}?"
            if question not in unanswered:
                unanswered.append(question)
    return {"question": case["question"], "method": method, "ai_notice": ai_notice, "source_ids": [s["id"] for s in sources], "summary": summary, "claims": claims, "findings": findings, "coverage": coverage, "unanswered_questions": unanswered, "generated_at": datetime.now(timezone.utc).isoformat()}


def _finding(fid: str, kind: str, title: str, explanation: str, priority: str, evidence: list[dict], action: str, requirement_category: str | None = None) -> dict:
    finding = {"id": fid, "type": kind, "title": title, "explanation": explanation, "priority": priority, "evidence": evidence, "origin": "deterministic signal", "task": {"title": action, "description": explanation, "priority": priority}}
    if requirement_category:
        finding["requirement_category"] = requirement_category
    return finding


def _best_excerpt(text: str, terms: list[str]) -> str:
    for sentence in _sentences(text):
        if any(term.lower() in sentence.lower() for term in terms):
            return sentence[:600]
    return text[:350]


def _document_excerpt(text: str) -> str:
    sentences = [s for s in _sentences(text) if any(term in s.lower() for term in ["submit", "document", "letter", "proof", "transcript", "income", "certificate"]) ]
    return " ".join(sentences[:3])[:650] or text[:300]
