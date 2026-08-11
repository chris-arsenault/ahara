import importlib.util
import io
import json
import os
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).with_name("report.py")
SPEC = importlib.util.spec_from_file_location("engineering_report", MODULE_PATH)
REPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REPORT)


class ReportNormalizationTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        REPORT.ARTIFACT_ROOT = self.root
        REPORT.SOURCE_ROOT = self.root
        os.environ["GITHUB_REPOSITORY"] = "chris-arsenault/example"
        os.environ["GITHUB_WORKSPACE"] = "/home/runner/work/example/example"

    def tearDown(self):
        self.tempdir.cleanup()

    def test_normalizes_job_checks_and_timing(self):
        result = REPORT.normalize_jobs(
            [
                {
                    "name": "ci",
                    "conclusion": "success",
                    "started_at": "2026-08-10T12:00:00Z",
                    "completed_at": "2026-08-10T12:00:05Z",
                    "steps": [
                        {
                            "name": "Test frontend",
                            "conclusion": "success",
                            "started_at": "2026-08-10T12:00:01Z",
                            "completed_at": "2026-08-10T12:00:04Z",
                        }
                    ],
                }
            ]
        )
        self.assertEqual(result["duration_seconds"], 5)
        self.assertTrue(result["test_passed"])
        self.assertEqual(result["checks"][0]["duration_ms"], 3000)

    def test_parses_junit_and_lcov(self):
        report_dir = self.root / "frontend" / "coverage"
        report_dir.mkdir(parents=True)
        (report_dir / "junit.xml").write_text(
            '<testsuites><testsuite name="frontend" tests="4" failures="1" '
            'errors="0" skipped="1" time="1.25"/></testsuites>'
        )
        (report_dir / "lcov.info").write_text(
            "SF:/home/runner/work/example/example/frontend/src/example.ts\n"
            "DA:1,1\nDA:2,0\nBRDA:1,0,0,1\nBRDA:2,0,1,-\n"
            "end_of_record\n"
        )

        suites = REPORT.parse_junit_reports()
        coverage = REPORT.parse_lcov_reports()
        self.assertEqual(suites[0]["passed"], 2)
        self.assertEqual(suites[0]["duration_ms"], 1250)
        self.assertEqual(coverage[0]["path"], "frontend/src/example.ts")
        self.assertEqual(coverage[0]["line_rate"], 0.5)
        self.assertEqual(coverage[0]["branch_rate"], 0.5)

    def test_normalizes_qlty_contract(self):
        quality_dir = self.root / ".ahara-ci-report" / "quality"
        quality_dir.mkdir(parents=True)
        source_dir = self.root / "src"
        source_dir.mkdir()
        (source_dir / "lib.rs").write_text("fn work() {\n    println!(\"ok\");\n}\n")
        (quality_dir / "metadata.json").write_text(
            json.dumps({"qlty_version": "0.641.0", "status": "complete"})
        )
        (quality_dir / "files.json").write_text(
            json.dumps(
                {
                    "stats": [
                        {
                            "name": "lib.rs",
                            "fullyQualifiedName": "src/lib.rs",
                            "path": "src/lib.rs",
                            "kind": "COMPONENT_TYPE_FILE",
                            "language": "LANGUAGE_RUST",
                            "files": 1,
                            "functions": 1,
                            "lines": 12,
                            "codeLines": 10,
                            "complexity": 3,
                            "cyclomatic": 4,
                        }
                    ]
                }
            )
        )
        (quality_dir / "functions.json").write_text(
            json.dumps(
                {
                    "stats": [
                        {
                            "name": "work",
                            "fullyQualifiedName": "work",
                            "path": "src/lib.rs",
                            "kind": "COMPONENT_TYPE_FUNCTION",
                            "language": "LANGUAGE_RUST",
                            "lines": 8,
                            "codeLines": 7,
                            "complexity": 3,
                            "cyclomatic": 4,
                        }
                    ]
                }
            )
        )
        (quality_dir / "findings.json").write_text(
            json.dumps(
                [
                    {
                        "tool": "qlty",
                        "driver": "duplication",
                        "ruleKey": "similar-code",
                        "message": "Similar code",
                        "level": "LEVEL_MEDIUM",
                        "language": "LANGUAGE_RUST",
                        "category": "CATEGORY_DUPLICATION",
                        "effortMinutes": 10,
                        "value": 4,
                        "location": {
                            "path": "src/lib.rs",
                            "range": {"startLine": 2, "endLine": 5},
                        },
                        "partialFingerprints": {"function.name": "work"},
                        "properties": {"structural_hash": "abc"},
                    }
                ]
            )
        )

        quality = REPORT.normalize_quality()
        self.assertEqual(quality["aggregates"]["files"], 1)
        self.assertEqual(quality["aggregates"]["functions"], 1)
        self.assertEqual(quality["aggregates"]["debt_minutes"], 10)
        self.assertEqual(quality["files"][0]["duplicated_lines"], 4)
        self.assertEqual(quality["findings"][0]["start_line"], 2)
        self.assertEqual(quality["functions"][0]["start_line"], 2)
        self.assertEqual(quality["sources"][0]["path"], "src/lib.rs")
        self.assertIn("fn work", quality["sources"][0]["content"])
        self.assertEqual(len(quality["functions"][0]["metric_key"]), 64)

    def test_post_json_reports_rejected_endpoint(self):
        os.environ["WEBHOOK_URL"] = "https://ci.services.ahara.io"
        os.environ["INGEST_TOKEN"] = "test-token"
        error = urllib.error.HTTPError(
            "https://ci.services.ahara.io/api/ci/batch",
            403,
            "Forbidden",
            {},
            io.BytesIO(b'{"error":"blocked"}'),
        )

        with mock.patch.object(
            REPORT.urllib.request, "urlopen", side_effect=error
        ) as urlopen:
            with self.assertRaisesRegex(
                RuntimeError,
                r'POST /api/ci/batch failed: HTTP 403: \{"error":"blocked"\}',
            ):
                REPORT.post_json("/api/ci/batch", {"kind": "quality_files"})

        self.assertEqual(urlopen.call_count, 3)


if __name__ == "__main__":
    unittest.main()
