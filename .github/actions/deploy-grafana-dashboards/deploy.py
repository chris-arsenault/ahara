#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

FUNCTION_NAME_PARAMETER = "/ahara/observability/grafana-dashboard-deployer/function-name"
MAX_PAYLOAD_BYTES = 5_500_000


def main() -> int:
    project = required_env("PROJECT")
    dashboards_path = Path(required_env("DASHBOARDS_PATH"))
    folder_uid = required_env("FOLDER_UID")
    folder_title = required_env("FOLDER_TITLE")
    prune = parse_bool(os.environ.get("PRUNE", "true"))
    region = os.environ.get("REGION", "us-east-1")

    dashboards = load_dashboards(dashboards_path)
    payload = {
        "project": project,
        "folder_uid": folder_uid,
        "folder_title": folder_title,
        "prune": prune,
        "dashboards": dashboards,
    }
    ensure_payload_size(payload)
    response = invoke_deployer(payload, region)
    print_summary(response)
    return 0


def required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        fail(f"{name} is required")
    return value


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    fail(f"PRUNE must be true or false, got {value!r}")


def load_dashboards(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        fail(f"dashboard path does not exist: {path}")
    if not path.is_dir():
        fail(f"dashboard path must be a directory: {path}")

    dashboards = []
    for dashboard_path in sorted(path.rglob("*.json")):
        dashboard = load_dashboard_json(dashboard_path)
        dashboards.append(
            {
                "path": dashboard_path.as_posix(),
                "dashboard": dashboard,
            }
        )

    if not dashboards:
        fail(f"no dashboard JSON files found in {path}")
    return dashboards


def load_dashboard_json(path: Path) -> dict[str, object]:
    try:
        dashboard = json.loads(path.read_text())
    except json.JSONDecodeError as error:
        fail(f"{path}: invalid JSON: {error}")

    if not isinstance(dashboard, dict):
        fail(f"{path}: dashboard JSON must be an object")
    for field in ("uid", "title"):
        value = dashboard.get(field)
        if not isinstance(value, str) or not value.strip():
            fail(f"{path}: dashboard.{field} is required")
    return dashboard


def ensure_payload_size(payload: dict[str, object]) -> None:
    size = len(json.dumps(payload, separators=(",", ":")).encode())
    if size > MAX_PAYLOAD_BYTES:
        fail(
            "dashboard deploy payload is too large for direct Lambda invoke "
            f"({size} bytes > {MAX_PAYLOAD_BYTES} bytes)"
        )


def invoke_deployer(payload: dict[str, object], region: str) -> dict[str, object]:
    function_name = aws_text(
        [
            "aws",
            "ssm",
            "get-parameter",
            "--name",
            FUNCTION_NAME_PARAMETER,
            "--query",
            "Parameter.Value",
            "--output",
            "text",
            "--region",
            region,
        ]
    )

    with tempfile.NamedTemporaryFile("w", delete=False) as payload_file:
        json.dump(payload, payload_file, separators=(",", ":"))
        payload_path = payload_file.name
    result_path = tempfile.NamedTemporaryFile(delete=False).name

    try:
        metadata = aws_json(
            [
                "aws",
                "lambda",
                "invoke",
                "--function-name",
                function_name,
                "--payload",
                f"file://{payload_path}",
                "--cli-binary-format",
                "raw-in-base64-out",
                "--region",
                region,
                result_path,
            ]
        )
        response = json.loads(Path(result_path).read_text())
    finally:
        Path(payload_path).unlink(missing_ok=True)
        Path(result_path).unlink(missing_ok=True)

    if metadata.get("FunctionError"):
        fail(f"dashboard deploy Lambda failed: {json.dumps(response, indent=2)}")
    if isinstance(response, dict) and response.get("errorMessage"):
        fail(f"dashboard deploy Lambda error: {response['errorMessage']}")
    if not isinstance(response, dict):
        fail(f"dashboard deploy Lambda returned unexpected response: {response!r}")
    return response


def aws_text(args: list[str]) -> str:
    result = run(args)
    return result.stdout.strip()


def aws_json(args: list[str]) -> dict[str, object]:
    output = aws_text(args)
    try:
        value = json.loads(output)
    except json.JSONDecodeError as error:
        fail(f"AWS CLI returned invalid JSON: {error}: {output}")
    if not isinstance(value, dict):
        fail(f"AWS CLI returned unexpected JSON: {value!r}")
    return value


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        fail(
            "command failed: "
            + " ".join(args)
            + f"\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def print_summary(response: dict[str, object]) -> None:
    upserted = response.get("upserted") or []
    pruned = response.get("pruned") or []
    print(f"Deployed {len(upserted)} Grafana dashboard(s).")
    for dashboard in upserted:
        print(
            "- "
            f"{dashboard.get('action', 'upserted')}: "
            f"{dashboard.get('uid')} "
            f"({dashboard.get('title')})"
        )
    if pruned:
        print(f"Pruned {len(pruned)} stale dashboard(s).")
        for dashboard in pruned:
            print(f"- deleted: {dashboard.get('uid')} ({dashboard.get('title')})")


def fail(message: str) -> None:
    print(f"::error::{message}", file=sys.stderr)
    raise SystemExit(1)


if __name__ == "__main__":
    raise SystemExit(main())
