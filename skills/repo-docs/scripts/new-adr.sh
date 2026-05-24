#!/usr/bin/env bash
# new-adr.sh — scaffold a new Architecture Decision Record.
#
# Usage: scripts/new-adr.sh <slug> [adr-dir]
#   <slug>     kebab-case slug for the decision, e.g. "no-plugin-framework"
#   [adr-dir]  destination directory; defaults to docs/adr/
#
# Picks the next NNNN number by scanning existing files, writes a stub
# at <adr-dir>/NNNN-<slug>.md with Nygard sections, and appends a row
# to <adr-dir>/README.md (creating it if necessary).

set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "usage: $0 <slug> [adr-dir]" >&2
    exit 64
fi

slug="$1"
adr_dir="${2:-docs/adr}"
mkdir -p "$adr_dir"

# Find the highest existing NNNN, default 0
highest=0
for f in "$adr_dir"/[0-9][0-9][0-9][0-9]-*.md; do
    [[ -e "$f" ]] || continue
    basename=$(basename "$f")
    n=${basename:0:4}
    n=${n#0}; n=${n#0}; n=${n#0}
    if [[ "$n" -gt "$highest" ]]; then
        highest="$n"
    fi
done

next=$(printf "%04d" $((highest + 1)))
target="$adr_dir/$next-$slug.md"

if [[ -e "$target" ]]; then
    echo "refusing to overwrite existing $target" >&2
    exit 73
fi

date=$(date +%Y-%m-%d)

# Generate the ADR file
cat > "$target" <<EOF
# $next — <title>

- Status: Proposed
- Date: $date

## Context

<!-- TODO: what forced the decision — one or two paragraphs of present-tense context -->

## Decision

<!-- TODO: what we chose, in one or two sentences -->

## Alternatives considered

- **Option A** — <!-- pros / cons; reason rejected -->
- **Option B** — <!-- pros / cons; reason rejected -->

## Consequences

<!-- TODO: what changes downstream as a result — positive and negative -->
EOF

# Ensure the index exists
index="$adr_dir/README.md"
if [[ ! -e "$index" ]]; then
    cat > "$index" <<EOF
# Architecture Decision Records

| # | Title | Status | Date |
| - | ----- | ------ | ---- |
EOF
fi

# Append the new row
echo "| [$next]($next-$slug.md) | <title> | Proposed | $date |" >> "$index"

echo "wrote $target"
echo "appended row to $index"
echo "next:"
echo "  1. Edit $target — replace <title>, fill Context/Decision/Alternatives/Consequences."
echo "  2. Edit $index — update <title> in the new row to match."
echo "  3. When accepted, change Status: Proposed → Accepted in both the ADR file and the index row."
