"""Tests for user-provided rubric validation and arithmetic."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.rubric_score import score_review  # noqa: E402


def criterion(identifier, weight, score, **extra):
    row = {"id": identifier, "label": identifier.replace("-", " ").title(),
           "weight": weight, "score": score}
    if score is not None:
        row["evidence"] = "Section 2, paragraph 1"
        row["rationale"] = "The cited passage supports this user-assigned rating."
    row.update(extra)
    return row


def rubric(criteria=None, scale=None):
    return {"title": "Example review", "scale": scale or {"min": 0, "max": 5},
            "criteria": criteria or [criterion("methods", 2, 4)]}


class RubricScoreTests(unittest.TestCase):
    def test_partial_summary_excludes_unscored_weight_from_mean(self):
        report = score_review(rubric([
            criterion("methods", 3, 4),
            criterion("transparency", 1, 2),
            criterion("reproducibility", 2, None, not_assessed_reason="Materials were not supplied."),
        ]))
        summary = report["summary"]
        self.assertEqual(summary["status"], "partial")
        self.assertEqual(summary["weighted_mean_of_scored_criteria"], 3.5)
        self.assertEqual(summary["scale_position_percent_of_scored_criteria"], 70.0)
        self.assertEqual(summary["weight_coverage_percent"], 66.666667)
        self.assertIsNone(summary["complete_weighted_mean"])
        self.assertEqual([row["id"] for row in report["not_assessed"]], ["reproducibility"])

    def test_complete_summary_calculates_weighted_mean_and_scale_position(self):
        report = score_review(rubric([
            criterion("question", 1, 2), criterion("evidence", 3, 4),
        ], {"min": 1, "max": 5}))
        summary = report["summary"]
        self.assertEqual(summary["status"], "complete")
        self.assertEqual(summary["weighted_mean_of_scored_criteria"], 3.5)
        self.assertEqual(summary["complete_weighted_mean"], 3.5)
        self.assertEqual(summary["complete_scale_position_percent"], 62.5)
        self.assertEqual(summary["weight_coverage_percent"], 100.0)

    def test_no_scores_has_no_mean_and_zero_coverage(self):
        report = score_review(rubric([
            criterion("question", 2, None), criterion("methods", 1, None),
        ]))
        self.assertEqual(report["summary"]["status"], "not_scored")
        self.assertEqual(report["summary"]["weight_coverage_percent"], 0.0)
        self.assertIsNone(report["summary"]["weighted_mean_of_scored_criteria"])
        self.assertIsNone(report["summary"]["complete_weighted_mean"])

    def test_assigned_score_requires_evidence_and_rationale(self):
        for omitted in ("evidence", "rationale"):
            row = criterion("quality", 1, 3)
            row.pop(omitted)
            with self.subTest(omitted=omitted), self.assertRaisesRegex(ValueError, omitted):
                score_review(rubric([row]))

    def test_rejects_booleans_duplicates_and_unknown_fields(self):
        for data in (
            rubric([criterion("quality", True, 3)]),
            rubric([criterion("quality", 1, True)]),
            rubric([criterion("same", 1, 3), criterion("same", 2, 2)]),
            {**rubric(), "generated_score": 4},
        ):
            with self.subTest(data=data), self.assertRaises(ValueError):
                score_review(data)

    def test_rejects_invalid_scale_weights_and_scores(self):
        invalid = (
            rubric(scale={"min": 5, "max": 5}),
            rubric(scale={"min": float("nan"), "max": 5}),
            rubric([criterion("quality", 0, 3)]),
            rubric([criterion("quality", 1, 6)]),
        )
        for data in invalid:
            with self.subTest(data=data), self.assertRaises(ValueError):
                score_review(data)

    def test_rejects_precision_that_would_be_lost_in_the_report(self):
        with self.assertRaisesRegex(ValueError, "at most 6 fractional"):
            score_review(rubric([criterion("quality", 0.0000001, 3)]))

    def test_cli_writes_new_report_and_refuses_overwrite(self):
        tool = ROOT / "tools" / "rubric_score.py"
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as directory:
            root = Path(directory)
            source = root / "input.json"
            source.write_text(json.dumps(rubric()), encoding="utf-8")
            output = root / "report.json"
            result = subprocess.run([sys.executable, "-B", str(tool), str(source), "--output", str(output)],
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["summary"]["status"], "complete")
            output.write_text("keep", encoding="utf-8")
            result = subprocess.run([sys.executable, "-B", str(tool), str(source), "--output", str(output)],
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(output.read_text(encoding="utf-8"), "keep")

    def test_invalid_json_returns_concise_error(self):
        tool = ROOT / "tools" / "rubric_score.py"
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as directory:
            source = Path(directory) / "broken.json"
            source.write_text('{"title":', encoding="utf-8")
            result = subprocess.run([sys.executable, "-B", str(tool), str(source)],
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 2)
            self.assertIn("Invalid JSON", result.stderr)
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
