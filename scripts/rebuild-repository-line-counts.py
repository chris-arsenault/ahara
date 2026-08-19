#!/usr/bin/env python3
"""Rebuild docs/repository-line-counts.md from repositories under ~/repos."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPOSITORIES_ROOT = PROJECT_ROOT.parent
DEFAULT_OUTPUT = PROJECT_ROOT / "docs" / "repository-line-counts.md"
MAX_FILE_BYTES = 5_000_000

LANGUAGE_EXTENSIONS = {
    "Astro": (".astro",),
    "C": (".c",),
    "C#": (".cs",),
    "C++": (".cc", ".cpp", ".cxx"),
    "C/C++ Header": (".h", ".hh", ".hpp"),
    "CMake": (".cmake",),
    "CSS": (".css",),
    "CUE": (".cue",),
    "Config": (".cfg", ".conf"),
    "Cython": (".pyx",),
    "Dart": (".dart",),
    "Dhall": (".dhall",),
    "Elixir": (".ex", ".exs"),
    "Erlang": (".erl", ".hrl"),
    "F#": (".fs", ".fsx"),
    "Go": (".go",),
    "Gradle": (".gradle",),
    "GraphQL": (".gql", ".graphql"),
    "Groovy": (".groovy",),
    "HCL": (".hcl",),
    "HTML": (".htm", ".html"),
    "INI": (".ini",),
    "JSON": (".json", ".jsonc"),
    "Java": (".java",),
    "JavaScript": (".cjs", ".js", ".jsx", ".mjs"),
    "Julia": (".jl",),
    "Kotlin": (".kt", ".kts"),
    "Less": (".less",),
    "Lua": (".lua",),
    "Make": (".mk",),
    "Move": (".move",),
    "Nim": (".nim",),
    "Nix": (".nix",),
    "Objective-C": (".m",),
    "Objective-C++": (".mm",),
    "PHP": (".php",),
    "Perl": (".pl", ".pm"),
    "Pkl": (".pkl",),
    "PowerShell": (".ps1",),
    "Properties": (".properties",),
    "Protocol Buffers": (".proto",),
    "Python": (".py", ".pyi"),
    "R": (".r",),
    "Rego": (".rego",),
    "Ruby": (".rb",),
    "Rust": (".rs",),
    "SCSS": (".scss",),
    "SQL": (".sql",),
    "SVG": (".svg",),
    "Sass": (".sass",),
    "Scala": (".scala",),
    "Shell": (".bash", ".fish", ".sh", ".zsh"),
    "Solidity": (".sol",),
    "Svelte": (".svelte",),
    "Swift": (".swift",),
    "TOML": (".toml",),
    "Terraform": (".tf", ".tfvars"),
    "TypeScript": (".ts", ".tsx"),
    "V": (".v",),
    "Visual Basic": (".vb",),
    "Vue": (".vue",),
    "XML": (".xml",),
    "XML Schema": (".xsd",),
    "XSLT": (".xsl", ".xslt"),
    "YAML": (".yaml", ".yml"),
    "Zig": (".zig",),
}

EXTENSION_LANGUAGES = {
    extension: language
    for language, extensions in LANGUAGE_EXTENSIONS.items()
    for extension in extensions
}

SPECIAL_FILENAMES = {
    "cmakelists.txt": "CMake",
    "containerfile": "Dockerfile",
    "dockerfile": "Dockerfile",
    "gemfile": "Ruby",
    "gnumakefile": "Make",
    "jenkinsfile": "Groovy",
    "justfile": "Just",
    "makefile": "Make",
    "procfile": "Procfile",
    "rakefile": "Ruby",
    "vagrantfile": "Ruby",
}

LOCKFILES = {
    ".terraform.lock.hcl",
    "bun.lock",
    "bun.lockb",
    "cargo.lock",
    "composer.lock",
    "flake.lock",
    "gemfile.lock",
    "npm-shrinkwrap.json",
    "package-lock.json",
    "pipfile.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "uv.lock",
    "yarn.lock",
}

EXCLUDED_DIRECTORIES = {
    ".mypy_cache",
    ".next",
    ".nuxt",
    ".pytest_cache",
    ".terraform",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
    "target",
    "vendor",
    "venv",
}

TEST_DIRECTORIES = {
    "__tests__",
    "acceptance",
    "cypress",
    "e2e",
    "integration-tests",
    "integration_tests",
    "spec",
    "specs",
    "test",
    "testdata",
    "testing",
    "tests",
}

MARKDOWN_EXTENSIONS = {".md", ".mdx"}
EXCLUDED_SUFFIXES = (".map", ".min.css", ".min.js", ".snap")


@dataclass
class RepositoryCounts:
    name: str
    source: Counter[str] = field(default_factory=Counter)
    tests: Counter[str] = field(default_factory=Counter)
    markdown_lines: int = 0
    markdown_files: int = 0


@dataclass(frozen=True)
class ExcludedLargeFile:
    repository: str
    path: Path
    size: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repos-root",
        type=Path,
        default=DEFAULT_REPOSITORIES_ROOT,
        help=f"directory containing repositories (default: {DEFAULT_REPOSITORIES_ROOT})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Markdown report path (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="print the report instead of writing it",
    )
    return parser.parse_args()


def discover_repositories(root: Path) -> list[Path]:
    if not root.is_dir():
        raise ValueError(f"repository root does not exist: {root}")

    return sorted(
        path for path in root.iterdir() if path.is_dir() and (path / ".git").exists()
    )


def tracked_files(repository: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(repository), "ls-files", "-z"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [Path(os.fsdecode(value)) for value in result.stdout.split(b"\0") if value]


def language_for(path: Path) -> str | None:
    filename = path.name.lower()
    return SPECIAL_FILENAMES.get(filename) or EXTENSION_LANGUAGES.get(
        path.suffix.lower()
    )


def is_excluded_path(path: Path) -> bool:
    directory_parts = {part.lower() for part in path.parts[:-1]}
    filename = path.name.lower()
    return (
        bool(directory_parts & EXCLUDED_DIRECTORIES)
        or filename in LOCKFILES
        or filename.endswith(EXCLUDED_SUFFIXES)
    )


def is_test_path(path: Path) -> bool:
    parts = [part.lower() for part in path.parts]
    filename = parts[-1]
    stem = Path(filename).stem
    return (
        any(part in TEST_DIRECTORIES for part in parts[:-1])
        or filename.startswith("test_")
        or stem.endswith("_test")
        or ".test." in filename
        or ".spec." in filename
        or filename.startswith("tests.")
    )


def count_nonblank_lines(path: Path) -> int | None:
    if path.is_symlink():
        return None

    data = path.read_bytes()
    if b"\0" in data[:8192]:
        return None

    text = data.decode("utf-8", errors="replace")
    return sum(1 for line in text.splitlines() if line.strip())


def count_repository(
    repository: Path,
    output: Path,
    excluded_large_files: list[ExcludedLargeFile],
) -> RepositoryCounts:
    counts = RepositoryCounts(name=repository.name)
    resolved_output = output.resolve()

    for relative_path in tracked_files(repository):
        full_path = repository / relative_path
        if full_path.resolve() == resolved_output or is_excluded_path(relative_path):
            continue

        try:
            size = full_path.stat().st_size
        except OSError:
            continue

        extension = relative_path.suffix.lower()
        language = language_for(relative_path)
        is_markdown = extension in MARKDOWN_EXTENSIONS
        if not is_markdown and language is None:
            continue

        if size > MAX_FILE_BYTES:
            excluded_large_files.append(
                ExcludedLargeFile(repository.name, relative_path, size)
            )
            continue

        try:
            line_count = count_nonblank_lines(full_path)
        except OSError:
            continue

        if line_count is None:
            continue

        if is_markdown:
            counts.markdown_lines += line_count
            counts.markdown_files += 1
        elif is_test_path(relative_path):
            counts.tests[language] += line_count
        else:
            counts.source[language] += line_count

    return counts


def format_counter(counter: Counter[str]) -> str:
    if not counter:
        return "—"

    ordered = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    return ", ".join(f"{language} {count:,}" for language, count in ordered)


def render_report(
    repositories_root: Path,
    repositories: list[RepositoryCounts],
    excluded_large_files: list[ExcludedLargeFile],
) -> str:
    source_totals: Counter[str] = Counter()
    test_totals: Counter[str] = Counter()
    markdown_total = 0
    markdown_file_total = 0

    for repository in repositories:
        source_totals.update(repository.source)
        test_totals.update(repository.tests)
        markdown_total += repository.markdown_lines
        markdown_file_total += repository.markdown_files

    source_total = sum(source_totals.values())
    test_total = sum(test_totals.values())
    combined_code_total = source_total + test_total
    all_text_total = combined_code_total + markdown_total
    snapshot_date = datetime.now(timezone.utc).date().isoformat()
    display_root = (
        "~/repos"
        if repositories_root == DEFAULT_REPOSITORIES_ROOT
        else str(repositories_root)
    )

    lines = [
        "# Repository Line Counts",
        "",
        f"Best-effort size snapshot of the repositories managed under `{display_root}`.",
        "",
        f"- Snapshot date: {snapshot_date}",
        f"- Repository scope: current working trees of all {len(repositories)} top-level Git repositories",
        "- Counting unit: nonblank physical lines in tracked text files",
        "",
        "## Rebuild",
        "",
        "Run `python3 scripts/rebuild-repository-line-counts.py` from the `ahara` repository root.",
        "",
        "## Totals",
        "",
        "| Category | Nonblank LoC |",
        "| --- | ---: |",
        f"| Source, configuration, and tracked data | {source_total:,} |",
        f"| Tests | {test_total:,} |",
        f"| Markdown documentation | {markdown_total:,} |",
        f"| **All included text** | **{all_text_total:,}** |",
        "",
        "## Method",
        "",
        "- Counts nonblank physical lines in files returned by `git ls-files`; comments remain in the count.",
        "- Classifies tests from common path and filename patterns such as `test/`, `tests/`, `spec/`, `e2e/`, `*_test.*`, `*.test.*`, and `*.spec.*`.",
        "- Counts `.md` and `.mdx` files only as Markdown documentation, even when they occur under a test path.",
        "- Classifies other tracked text by extension or well-known filename. JSON, YAML, SVG, XML, Terraform, and similar formats are included, so this is broader than executable source code.",
        "- Excludes the generated report itself, common dependency and build directories, lockfiles, minified files, source maps, snapshots, binary or unrecognized files, and individual files over 5 MB.",
        f"- The size rule excluded {len(excluded_large_files)} recognized text files in this snapshot.",
        "",
        "The source, test, and Markdown columns are mutually exclusive. The test classification is a path heuristic, so test fixtures stored under those paths count as tests.",
        "",
        "## Per repository",
        "",
        "| Repository | Source LoC by language | Test LoC by language | Markdown docs |",
        "| --- | ---: | ---: | ---: |",
    ]

    for repository in repositories:
        lines.append(
            f"| {repository.name} | {format_counter(repository.source)} | "
            f"{format_counter(repository.tests)} | {repository.markdown_lines:,} |"
        )

    lines.extend(
        [
            "",
            "## Language summary",
            "",
            "Markdown is omitted here because it is reported separately.",
            "",
            "| Language | Source | Tests | Combined |",
            "| --- | ---: | ---: | ---: |",
        ]
    )

    languages = sorted(
        source_totals.keys() | test_totals.keys(),
        key=lambda language: (
            -(source_totals[language] + test_totals[language]),
            language,
        ),
    )
    for language in languages:
        source = source_totals[language]
        tests = test_totals[language]
        lines.append(f"| {language} | {source:,} | {tests:,} | {source + tests:,} |")

    lines.extend(
        [
            f"| **Total** | **{source_total:,}** | **{test_total:,}** | **{combined_code_total:,}** |",
            "",
            "## Markdown documentation by repository",
            "",
            "Repositories with no Markdown are omitted from this table but remain present in the per-repository table.",
            "",
            "| Repository | Markdown LoC | Markdown files |",
            "| --- | ---: | ---: |",
        ]
    )

    repositories_with_markdown = sorted(
        (repository for repository in repositories if repository.markdown_lines),
        key=lambda repository: (-repository.markdown_lines, repository.name),
    )
    for repository in repositories_with_markdown:
        lines.append(
            f"| {repository.name} | {repository.markdown_lines:,} | "
            f"{repository.markdown_files:,} |"
        )

    lines.append(
        f"| **Total** | **{markdown_total:,}** | **{markdown_file_total:,}** |"
    )
    lines.append("")
    return "\n".join(lines)


def write_report(output: Path, report: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None

    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=output.parent,
            prefix=f".{output.name}.",
            delete=False,
        ) as temporary_file:
            temporary_file.write(report)
            temporary_path = Path(temporary_file.name)
        temporary_path.chmod(0o644)
        temporary_path.replace(output)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def main() -> int:
    args = parse_args()
    repositories_root = args.repos_root.expanduser().resolve()
    output = args.output.expanduser().resolve()

    try:
        repository_paths = discover_repositories(repositories_root)
        if not repository_paths:
            raise ValueError(f"no Git repositories found under: {repositories_root}")

        excluded_large_files: list[ExcludedLargeFile] = []
        counts = [
            count_repository(repository, output, excluded_large_files)
            for repository in repository_paths
        ]
        report = render_report(
            repositories_root,
            counts,
            excluded_large_files,
        )
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if args.stdout:
        sys.stdout.write(report)
    else:
        write_report(output, report)
        print(f"Wrote {output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
