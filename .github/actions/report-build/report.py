import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ARTIFACT_ROOT = Path(".engineering-report")
SOURCE_ROOT = Path(".")
BATCH_SIZE = 200
MAX_BATCH_BYTES = 800_000
MAX_SOURCE_BYTES = 500_000


def read_json(path, default):
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def parse_time(value):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def elapsed_ms(started, completed):
    start = parse_time(started)
    end = parse_time(completed)
    if not start or not end:
        return None
    return max(0, int((end - start).total_seconds() * 1000))


def github_jobs():
    api = os.environ.get("GITHUB_API_URL", "https://api.github.com")
    repo = os.environ["GITHUB_REPOSITORY"]
    run_id = os.environ["GITHUB_RUN_ID"]
    url = f"{api}/repos/{repo}/actions/runs/{run_id}/jobs?per_page=100"
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as response:
        return json.loads(response.read()).get("jobs", [])


def check_category(name):
    lowered = name.lower()
    if lowered.startswith("lint"):
        return "lint"
    if lowered.startswith("test"):
        return "test"
    if "qlty" in lowered or "maintainability" in lowered:
        return "quality"
    if lowered.startswith(("build", "package")):
        return "build"
    if lowered.startswith(("deploy", "migrate", "terraform apply")):
        return "deploy"
    return "other"


def normalize_jobs(jobs):
    checks = []
    lint_results = []
    test_results = []
    starts = []
    ends = []
    overall = "success"
    failure_states = {"failure", "cancelled", "timed_out", "action_required"}

    for job in jobs:
        if "report" in job.get("name", "").lower():
            continue
        conclusion = job.get("conclusion") or "unknown"
        if conclusion in failure_states:
            overall = conclusion
        if job.get("started_at"):
            starts.append(parse_time(job["started_at"]))
        if job.get("completed_at"):
            ends.append(parse_time(job["completed_at"]))

        for step in job.get("steps", []):
            status = step.get("conclusion") or step.get("status") or "unknown"
            if status == "skipped":
                continue
            name = step.get("name", "")
            category = check_category(name)
            if category == "lint":
                lint_results.append(status == "success")
            elif category == "test":
                test_results.append(status == "success")
            checks.append(
                {
                    "job_name": job.get("name", ""),
                    "name": name,
                    "category": category,
                    "status": status,
                    "started_at": step.get("started_at"),
                    "completed_at": step.get("completed_at"),
                    "duration_ms": elapsed_ms(
                        step.get("started_at"), step.get("completed_at")
                    ),
                }
            )

    started = min((value for value in starts if value), default=None)
    completed = max((value for value in ends if value), default=None)
    return {
        "checks": checks,
        "overall": overall,
        "lint_passed": all(lint_results) if lint_results else None,
        "test_passed": all(test_results) if test_results else None,
        "started_at": started.isoformat() if started else None,
        "completed_at": completed.isoformat() if completed else None,
        "duration_seconds": (
            int((completed - started).total_seconds())
            if started and completed
            else None
        ),
    }


def local_name(tag):
    return tag.rsplit("}", 1)[-1]


def infer_framework(path):
    lowered = str(path).lower()
    if "nextest" in lowered:
        return "cargo-nextest"
    if "vitest" in lowered or "coverage/junit" in lowered:
        return "vitest"
    if "pytest" in lowered:
        return "pytest"
    return "junit"


def parse_junit_reports():
    suites = []
    if not ARTIFACT_ROOT.exists():
        return suites
    for path in ARTIFACT_ROOT.rglob("*.xml"):
        lowered = str(path).lower()
        if "junit" not in lowered and "test-result" not in lowered:
            continue
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError:
            continue
        for suite in root.iter():
            if local_name(suite.tag) != "testsuite":
                continue
            if any(local_name(child.tag) == "testsuite" for child in suite):
                continue
            tests = int(float(suite.attrib.get("tests", "0") or 0))
            failures = int(float(suite.attrib.get("failures", "0") or 0))
            errors = int(float(suite.attrib.get("errors", "0") or 0))
            skipped = int(
                float(
                    suite.attrib.get("skipped", suite.attrib.get("disabled", "0"))
                    or 0
                )
            )
            suites.append(
                {
                    "framework": infer_framework(path),
                    "path": str(path.relative_to(ARTIFACT_ROOT)),
                    "name": suite.attrib.get("name") or path.stem,
                    "tests": tests,
                    "passed": max(0, tests - failures - errors - skipped),
                    "failures": failures,
                    "errors": errors,
                    "skipped": skipped,
                    "duration_ms": int(
                        float(suite.attrib.get("time", "0") or 0) * 1000
                    ),
                }
            )
    return suites


def normalize_source_path(value):
    value = value.replace("\\", "/")
    workspace = os.environ.get("GITHUB_WORKSPACE", "").replace("\\", "/")
    if workspace and value.startswith(f"{workspace}/"):
        return value[len(workspace) + 1 :]
    if value.startswith("/"):
        repo_name = os.environ["GITHUB_REPOSITORY"].split("/")[-1]
        marker = f"/{repo_name}/"
        if marker in value:
            return value.rsplit(marker, 1)[-1]
    return value.removeprefix("./")


def parse_lcov_reports():
    coverage = {}
    if not ARTIFACT_ROOT.exists():
        return []
    for path in ARTIFACT_ROOT.rglob("lcov.info"):
        source = None
        lines = {}
        branches = {}

        def finish_record():
            if not source:
                return
            normalized = normalize_source_path(source)
            merged = coverage.setdefault(
                normalized, {"lines": {}, "branches": {}}
            )
            for number, hits in lines.items():
                merged["lines"][number] = max(
                    hits, merged["lines"].get(number, 0)
                )
            for key, hits in branches.items():
                merged["branches"][key] = max(
                    hits, merged["branches"].get(key, 0)
                )

        for raw_line in path.read_text(errors="replace").splitlines():
            if raw_line.startswith("SF:"):
                source = raw_line[3:]
            elif raw_line.startswith("DA:"):
                number, hits, *_ = raw_line[3:].split(",")
                lines[int(number)] = int(hits)
            elif raw_line.startswith("BRDA:"):
                parts = raw_line[5:].split(",")
                key = tuple(parts[:3])
                hits = 0 if parts[3] in ("-", "") else int(parts[3])
                branches[key] = hits
            elif raw_line == "end_of_record":
                finish_record()
                source = None
                lines = {}
                branches = {}
        finish_record()

    result = []
    for path, values in sorted(coverage.items()):
        total = len(values["lines"])
        covered = sum(hits > 0 for hits in values["lines"].values())
        branch_total = len(values["branches"])
        branch_covered = sum(hits > 0 for hits in values["branches"].values())
        result.append(
            {
                "path": path,
                "lines_total": total,
                "lines_covered": covered,
                "line_rate": covered / total if total else None,
                "branches_total": branch_total or None,
                "branches_covered": branch_covered if branch_total else None,
                "branch_rate": (
                    branch_covered / branch_total if branch_total else None
                ),
            }
        )
    return result


def clean_enum(value, prefix):
    return (value or "").removeprefix(prefix).lower()


def quality_paths():
    if not ARTIFACT_ROOT.exists():
        return None
    matches = list(ARTIFACT_ROOT.rglob("quality/metadata.json"))
    return matches[0].parent if matches else None


def normalize_quality():
    root = quality_paths()
    if not root:
        return None
    metadata = read_json(root / "metadata.json", {})
    file_document = read_json(root / "files.json", {})
    function_document = read_json(root / "functions.json", {})
    raw_findings = read_json(root / "findings.json", [])
    if not isinstance(raw_findings, list):
        raw_findings = raw_findings.get("issues", [])

    finding_totals = defaultdict(
        lambda: {"finding_count": 0, "debt_minutes": 0, "duplicated_lines": 0}
    )
    function_locations = defaultdict(list)
    findings = []
    for finding in raw_findings:
        location = finding.get("location") or {}
        path = normalize_source_path(location.get("path", ""))
        range_data = location.get("range") or {}
        partial_fingerprints = finding.get("partialFingerprints") or {}
        properties = dict(finding.get("properties") or {})
        if partial_fingerprints:
            properties["partial_fingerprints"] = partial_fingerprints
        function_name = partial_fingerprints.get("function.name")
        if function_name and range_data.get("startLine"):
            function_locations[(path, function_name)].append(
                int(range_data["startLine"])
            )
        fingerprint_source = {
            "driver": finding.get("driver"),
            "rule": finding.get("ruleKey"),
            "path": path,
            "line": range_data.get("startLine"),
            "message": finding.get("message"),
            "structural_hash": properties.get("structural_hash"),
        }
        fingerprint = hashlib.sha256(
            json.dumps(fingerprint_source, sort_keys=True).encode()
        ).hexdigest()
        category = clean_enum(finding.get("category"), "CATEGORY_")
        effort = int(finding.get("effortMinutes") or 0)
        value = finding.get("value")
        finding_totals[path]["finding_count"] += 1
        finding_totals[path]["debt_minutes"] += effort
        if category == "duplication":
            finding_totals[path]["duplicated_lines"] += int(value or 0)
        findings.append(
            {
                "fingerprint": fingerprint,
                "path": path,
                "start_line": range_data.get("startLine"),
                "end_line": range_data.get("endLine"),
                "start_byte": range_data.get("startByte"),
                "end_byte": range_data.get("endByte"),
                "tool": finding.get("tool") or "qlty",
                "driver": finding.get("driver") or "",
                "rule_key": finding.get("ruleKey") or "",
                "message": finding.get("message") or "",
                "level": clean_enum(finding.get("level"), "LEVEL_"),
                "language": clean_enum(finding.get("language"), "LANGUAGE_"),
                "category": category,
                "effort_minutes": finding.get("effortMinutes"),
                "value": value,
                "value_delta": finding.get("valueDelta"),
                "other_locations": finding.get("otherLocations") or [],
                "properties": properties,
            }
        )

    files = []
    for stat in file_document.get("stats", []):
        if stat.get("kind") != "COMPONENT_TYPE_FILE" or not stat.get("path"):
            continue
        path = normalize_source_path(stat["path"])
        totals = finding_totals[path]
        files.append(
            {
                "path": path,
                "name": stat.get("name") or Path(path).name,
                "fully_qualified_name": stat.get("fullyQualifiedName") or path,
                "language": clean_enum(stat.get("language"), "LANGUAGE_"),
                "files": int(stat.get("files") or 1),
                "classes": int(stat.get("classes") or 0),
                "functions": int(stat.get("functions") or 0),
                "fields": int(stat.get("fields") or 0),
                "lines": int(stat.get("lines") or 0),
                "code_lines": int(stat.get("codeLines") or 0),
                "comment_lines": int(stat.get("commentLines") or 0),
                "blank_lines": int(stat.get("blankLines") or 0),
                "complexity": int(stat.get("complexity") or 0),
                "cyclomatic": int(stat.get("cyclomatic") or 0),
                "lcom4": stat.get("lcom4"),
                **totals,
            }
        )

    functions = []
    function_occurrences = defaultdict(int)
    for locations in function_locations.values():
        locations.sort()
    for stat in function_document.get("stats", []):
        if stat.get("kind") != "COMPONENT_TYPE_FUNCTION" or not stat.get("path"):
            continue
        path = normalize_source_path(stat["path"])
        symbol = stat.get("fullyQualifiedName") or stat.get("name") or ""
        occurrence_key = (path, symbol)
        occurrence = function_occurrences[occurrence_key]
        function_occurrences[occurrence_key] += 1
        locations = function_locations[occurrence_key]
        metric_key = hashlib.sha256(
            f"{path}\0{symbol}\0{occurrence}".encode()
        ).hexdigest()
        functions.append(
            {
                "metric_key": metric_key,
                "path": path,
                "symbol": symbol,
                "start_line": (
                    locations[occurrence] if occurrence < len(locations) else None
                ),
                "language": clean_enum(stat.get("language"), "LANGUAGE_"),
                "lines": int(stat.get("lines") or 0),
                "code_lines": int(stat.get("codeLines") or 0),
                "complexity": int(stat.get("complexity") or 0),
                "cyclomatic": int(stat.get("cyclomatic") or 0),
                "lcom4": stat.get("lcom4"),
            }
        )

    sources = []
    source_root = SOURCE_ROOT.resolve()
    for item in files:
        relative = Path(item["path"])
        if relative.is_absolute() or ".." in relative.parts:
            continue
        source_path = (source_root / relative).resolve()
        if not source_path.is_relative_to(source_root) or not source_path.is_file():
            continue
        if source_path.stat().st_size > MAX_SOURCE_BYTES:
            continue
        content = source_path.read_text(errors="replace")
        sources.append(
            {
                "path": item["path"],
                "language": item["language"],
                "content": content,
                "content_sha256": f"sha256:{hashlib.sha256(content.encode()).hexdigest()}",
            }
        )

    return {
        "metadata": metadata,
        "files": files,
        "functions": functions,
        "sources": sources,
        "findings": findings,
        "aggregates": {
            "files": len(files),
            "functions": len(functions),
            "code_lines": sum(item["code_lines"] for item in files),
            "complexity": sum(item["complexity"] for item in files),
            "cyclomatic": sum(item["cyclomatic"] for item in files),
            "findings": len(findings),
            "debt_minutes": sum(
                int(item.get("effort_minutes") or 0) for item in findings
            ),
            "duplicated_lines": sum(
                item["duplicated_lines"] for item in files
            ),
        },
    }


def post_json(path, payload):
    url = f"{os.environ['WEBHOOK_URL'].rstrip('/')}{path}"
    body = json.dumps(payload, separators=(",", ":")).encode()
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {os.environ['INGEST_TOKEN']}",
            "Content-Type": "application/json",
        },
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                if 200 <= response.status < 300:
                    return
                raise RuntimeError(f"HTTP {response.status}")
        except (urllib.error.URLError, RuntimeError):
            if attempt == 2:
                raise
            time.sleep(2**attempt)


def post_batches(kind, parent_name, parent_id, items):
    batch = []
    for item in items:
        candidate = [*batch, item]
        payload = {
            "kind": kind,
            parent_name: parent_id,
            "items": candidate,
        }
        if batch and (
            len(candidate) > BATCH_SIZE
            or len(json.dumps(payload, separators=(",", ":")).encode())
            > MAX_BATCH_BYTES
        ):
            post_json(
                "/api/ci/batch",
                {"kind": kind, parent_name: parent_id, "items": batch},
            )
            batch = [item]
        else:
            batch = candidate
    if batch:
        post_json(
            "/api/ci/batch",
            {
                "kind": kind,
                parent_name: parent_id,
                "items": batch,
            },
        )


def main():
    job_data = normalize_jobs(github_jobs())
    suites = parse_junit_reports()
    coverage = parse_lcov_reports()
    quality = normalize_quality()

    tests_total = sum(item["tests"] for item in suites)
    tests_passed = sum(item["passed"] for item in suites)
    tests_failed = sum(item["failures"] + item["errors"] for item in suites)
    tests_skipped = sum(item["skipped"] for item in suites)
    coverage_total = sum(item["lines_total"] for item in coverage)
    coverage_covered = sum(item["lines_covered"] for item in coverage)

    repo = os.environ["GITHUB_REPOSITORY"]
    run_id = os.environ["GITHUB_RUN_ID"]
    branch = os.environ.get("GITHUB_HEAD_REF") or os.environ.get(
        "GITHUB_REF_NAME", ""
    )
    report = {
        "repo": repo,
        "workflow": os.environ.get("GITHUB_WORKFLOW", ""),
        "status": job_data["overall"],
        "branch": branch,
        "commit_sha": os.environ.get("GITHUB_SHA", ""),
        "run_id": run_id,
        "run_url": (
            f"{os.environ.get('GITHUB_SERVER_URL', '')}/{repo}/actions/runs/{run_id}"
        ),
        "event_name": os.environ.get("GITHUB_EVENT_NAME"),
        "started_at": job_data["started_at"],
        "completed_at": job_data["completed_at"],
        "duration_seconds": job_data["duration_seconds"],
        "lint_passed": job_data["lint_passed"],
        "test_passed": job_data["test_passed"],
        "tests_total": tests_total if suites else None,
        "tests_passed": tests_passed if suites else None,
        "tests_failed": tests_failed if suites else None,
        "tests_skipped": tests_skipped if suites else None,
        "coverage_lines_total": coverage_total if coverage else None,
        "coverage_lines_covered": coverage_covered if coverage else None,
        "coverage_line_rate": (
            coverage_covered / coverage_total if coverage_total else None
        ),
    }
    post_json("/api/ci/report", report)
    post_batches("checks", "run_id", run_id, job_data["checks"])
    post_batches("test_suites", "run_id", run_id, suites)
    post_batches("coverage_files", "run_id", run_id, coverage)

    if quality:
        scan_id = f"{run_id}:qlty"
        metadata = quality["metadata"]
        post_json(
            "/api/ci/quality/start",
            {
                "scan_id": scan_id,
                "run_id": run_id,
                "repo": repo,
                "branch": branch,
                "commit_sha": os.environ.get("GITHUB_SHA", ""),
                "qlty_version": metadata.get("qlty_version", "unknown"),
                "analyzer_digest": metadata.get("analyzer_digest", "unknown"),
                "config_digest": metadata.get("config_digest", "unknown"),
                "status": "pending",
                "started_at": metadata.get("started_at"),
                **quality["aggregates"],
            },
        )
        post_batches("quality_files", "scan_id", scan_id, quality["files"])
        post_batches(
            "quality_functions", "scan_id", scan_id, quality["functions"]
        )
        post_batches("quality_sources", "scan_id", scan_id, quality["sources"])
        post_batches(
            "quality_findings", "scan_id", scan_id, quality["findings"]
        )
        post_json(
            "/api/ci/quality/complete",
            {
                "scan_id": scan_id,
                "status": metadata.get("status", "failed"),
                "completed_at": datetime.now(timezone.utc).isoformat(),
            },
        )

    print(
        "Reported "
        f"{len(job_data['checks'])} checks, {len(suites)} test suites, "
        f"{len(coverage)} coverage files, and "
        f"{len(quality['files']) if quality else 0} quality files."
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"::warning::Engineering report ingestion failed: {error}")
        sys.exit(0)
