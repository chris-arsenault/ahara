"""Detect the browser-test capability without installing frontend dependencies."""

import json
import os
from pathlib import Path

import yaml


ENGINES = ["chromium", "firefox", "webkit"]


def source_directory(root, manifest):
    override = manifest.get("typescript_dir")
    if override:
        directory = Path(override)
        if directory.is_absolute() or ".." in directory.parts:
            raise ValueError("typescript_dir must stay within the repository")
        return directory.as_posix()
    candidates = []
    for directory, dirs, files in os.walk(root):
        dirs[:] = sorted(
            d for d in dirs if d not in {"node_modules", "backend", ".git"}
        )
        if "package.json" in files:
            candidates.append(Path(directory).relative_to(root))
    return (
        min(candidates, key=lambda p: (len(p.parts), p.as_posix())).as_posix()
        if candidates
        else "frontend"
    )


def detect(root):
    manifest = yaml.safe_load((root / "platform.yml").read_text())
    settings = manifest.get("browser_tests")
    disabled = {"enabled": False, "engines": [], "artifacts": []}
    if settings is False:
        return disabled
    if settings is not None and settings is not True and not isinstance(settings, dict):
        raise ValueError("browser_tests must be a boolean or mapping")
    if "typescript" not in manifest.get("stack", []):
        if settings is not None:
            raise ValueError("browser_tests requires the typescript stack")
        return disabled
    directory = source_directory(root, manifest)
    package_path = root / directory / "package.json"
    if not package_path.is_file():
        raise ValueError(f"Missing TypeScript package: {package_path}")
    if not package_path.resolve().is_relative_to(root.resolve()):
        raise ValueError("TypeScript package must stay within the repository")
    package = json.loads(package_path.read_text())
    scripts = package.get("scripts", {})
    if not scripts.get("test:browser"):
        if settings is not None:
            raise ValueError("browser_tests requires a test:browser package script")
        return disabled
    settings = settings if isinstance(settings, dict) else {}
    unknown = settings.keys() - {"engines", "artifacts"}
    if unknown:
        raise ValueError(
            f"Unknown browser_tests setting(s): {', '.join(sorted(unknown))}"
        )
    engines = settings.get("engines", ENGINES)
    if (
        not isinstance(engines, list)
        or not engines
        or any(engine not in ENGINES for engine in engines)
        or len(set(engines)) != len(engines)
    ):
        raise ValueError(
            "browser_tests.engines must contain distinct chromium/firefox/webkit entries"
        )
    artifacts = settings.get(
        "artifacts", [f"{directory}/test-results/", f"{directory}/playwright-report/"]
    )
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError(
            "browser_tests.artifacts must be a non-empty list of repository-relative paths"
        )
    for path in artifacts:
        if (
            not isinstance(path, str)
            or not path.strip()
            or "\n" in path
            or "\r" in path
            or Path(path).is_absolute()
            or ".." in Path(path).parts
            or path.startswith("!")
        ):
            raise ValueError("browser_tests.artifacts must stay within the repository")
    return {
        "enabled": True,
        "directory": directory,
        "engines": engines,
        "verify": bool(scripts.get("test:browser:verify")),
        "release": bool(scripts.get("test:release")),
        "artifacts": artifacts,
        "artifact_paths": "\n".join(artifacts),
    }


def main():
    config = detect(Path.cwd())
    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        output.write(f"enabled={str(config['enabled']).lower()}\n")
        output.write(f"config={json.dumps(config, separators=(',', ':'))}\n")


if __name__ == "__main__":
    main()
