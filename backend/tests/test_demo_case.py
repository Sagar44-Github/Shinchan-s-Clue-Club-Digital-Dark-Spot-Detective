"""API regression tests for the playable School-Fair Switcheroo demo."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
ROOT = BACKEND.parent
sys.path.insert(0, str(BACKEND))

_TEMP_DATABASE = tempfile.TemporaryDirectory(prefix="shinchan-clue-club-tests-")
os.environ["DATABASE_PATH"] = str(Path(_TEMP_DATABASE.name) / "cases.sqlite3")
os.environ["OPENAI_API_KEY"] = ""
os.environ["FRONTEND_ORIGIN"] = "http://testserver"

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402

CLIENT = TestClient(app)
CASE_SLUG = "shinchan-school-fair-switcheroo"
BONUS_FILE = ROOT / "frontend" / "public" / "sample-files" / "fair-access-update.md"


def open_case() -> dict:
    response = CLIENT.post(f"/api/library/{CASE_SLUG}")
    if response.status_code != 200:
        raise AssertionError(response.text)
    return response.json()


def import_bonus(case_id: str) -> dict:
    response = CLIENT.post(
        f"/api/cases/{case_id}/sources/upload",
        files={"file": (BONUS_FILE.name, BONUS_FILE.read_bytes(), "text/markdown")},
    )
    if response.status_code != 200:
        raise AssertionError(response.text)
    return response.json()


class SchoolFairDemoTests(unittest.TestCase):
    def test_library_hides_solution_and_case_starts_unsolved(self) -> None:
        item = next(case for case in CLIENT.get("/api/library").json() if case["slug"] == CASE_SLUG)
        for secret in ("answer_id", "resolution", "hints", "hint"):
            self.assertNotIn(secret, item["challenge"])

        case = open_case()
        self.assertEqual(case["status"], "unsolved")
        self.assertEqual(len(case["sources"]), 3)
        self.assertEqual(case["analysis_runs"], [])
        for secret in ("answer_id", "resolution", "hints", "hint"):
            self.assertNotIn(secret, case["challenge"])
        self.assertEqual(CLIENT.post(f"/api/cases/{case['id']}/analyze").status_code, 409)
        self.assertEqual(
            CLIENT.post(f"/api/cases/{case['id']}/challenge/answer", json={"answer_id": "evidence-plan"}).status_code,
            409,
        )

    def test_bonus_upload_analysis_coverage_and_exact_citations(self) -> None:
        case = open_case()
        source = import_bonus(case["id"])
        self.assertEqual(source["title"], "Futaba Science Fair — Step-Free Access Update")
        self.assertEqual(source["publisher"], "Futaba Kindergarten Site Team (fictional)")
        self.assertEqual(source["published_date"], "2026-11-06")
        self.assertEqual(source["source_type"], "uploaded md")
        self.assertEqual(source["original_filename"], BONUS_FILE.name)
        self.assertNotIn("---", source["text"])

        response = CLIENT.post(f"/api/cases/{case['id']}/analyze")
        self.assertEqual(response.status_code, 200, response.text)
        result = response.json()["run"]["result"]
        coverage = {item["requirement"]["category"]: item for item in result["coverage"]}
        self.assertEqual(coverage["fair-gate"]["status"], "conflicting")
        self.assertEqual(coverage["fair-checkin"]["status"], "conflicting")
        self.assertEqual(coverage["fair-departure"]["status"], "covered")
        self.assertEqual(coverage["fair-wristband"]["status"], "conflicting")
        self.assertEqual(coverage["fair-access-route"]["status"], "covered")
        self.assertEqual(coverage["fair-accessible-dropoff"]["status"], "not-found")
        for category in ("fair-gate", "fair-checkin", "fair-wristband"):
            pairs = [item for item in result["findings"] if item.get("requirement_category") == category and item["type"] == "conflict"]
            self.assertGreaterEqual(len(pairs), 2)
        self.assertTrue(any(item["type"] == "freshness" and "Undated" in item["title"] for item in result["findings"]))

        stored = {item["id"]: item for item in response.json()["case"]["sources"]}
        for finding in result["findings"]:
            for evidence in finding.get("evidence", []):
                self.assertIn(evidence["quote"], stored[evidence["source_id"]]["text"])
        gap_tasks = [task for task in response.json()["case"]["tasks"] if "parking" in task["title"].lower()]
        self.assertTrue(gap_tasks)
        self.assertTrue(all(task["status"] == "open" for task in gap_tasks))

    def test_hints_verdict_resolution_and_unresolved_briefing(self) -> None:
        case = open_case()
        first = CLIENT.post(f"/api/cases/{case['id']}/challenge/hint", json={"level": 0}).json()
        final = CLIENT.post(f"/api/cases/{case['id']}/challenge/hint", json={"level": 2}).json()
        self.assertEqual(first["level"], 1)
        self.assertEqual(final["level"], 3)
        self.assertFalse(final["has_more"])
        self.assertNotIn("answer_id", first)
        self.assertNotIn("resolution", final)

        import_bonus(case["id"])
        self.assertEqual(CLIENT.post(f"/api/cases/{case['id']}/analyze").status_code, 200)
        wrong = CLIENT.post(f"/api/cases/{case['id']}/challenge/answer", json={"answer_id": "old-flyer-plan"}).json()
        self.assertFalse(wrong["correct"])
        self.assertTrue(wrong.get("hint"))
        self.assertNotIn("resolution", wrong)
        self.assertEqual(CLIENT.get(f"/api/cases/{case['id']}").json()["status"], "unsolved")

        solved = CLIENT.post(f"/api/cases/{case['id']}/challenge/answer", json={"answer_id": "evidence-plan"}).json()
        self.assertTrue(solved["correct"])
        self.assertIn("November 5", solved["resolution"])
        self.assertIn("none of the reviewed records confirms", solved["resolution"].lower())
        report = CLIENT.get(f"/api/cases/{case['id']}/report.md")
        self.assertEqual(report.status_code, 200)
        self.assertIn("Still needs confirmation", report.text)
        self.assertIn("accessible parking or drop-off", report.text.lower())
        self.assertIn("Ask the fictional event desk", report.text)

        fresh = open_case()
        self.assertEqual(fresh["status"], "unsolved")
        self.assertEqual(len(fresh["sources"]), 3)
        self.assertEqual(fresh["analysis_runs"], [])
        self.assertNotIn("answer_id", fresh["challenge"])


def tearDownModule() -> None:
    CLIENT.close()
    _TEMP_DATABASE.cleanup()


if __name__ == "__main__":
    unittest.main()
