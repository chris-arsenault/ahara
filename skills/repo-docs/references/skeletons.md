# File skeletons

Use the matching skeleton when creating each file in the convention.

## README.md

```markdown
# <project-name>

<one-sentence description: what it is + who it's for>

<status / version / license badges>

## Quickstart

<the minimum commands a new contributor runs to see it work>

## Documentation

| Topic | Link |
| ---- | ---- |
| Architecture | [docs/architecture.md](docs/architecture.md) |
| Development | [docs/development.md](docs/development.md) |
| Performance | [docs/performance.md](docs/performance.md) |
| Architecture decisions | [docs/adr/README.md](docs/adr/README.md) |
| Backlog | [docs/backlog.md](docs/backlog.md) |
| Changelog | [CHANGELOG.md](CHANGELOG.md) |
| Agent guide | [AGENTS.md](AGENTS.md) |
| ... | ... |

## License

<one line + link>
```

## AGENTS.md

```markdown
# Agent Guide

<one-line repo description>

## Read first

| Topic | Link |
| ---- | ---- |
| Workspace overview | [README.md](README.md) |
| Documentation index | [docs/README.md](docs/README.md) |
| Architecture | [docs/architecture.md](docs/architecture.md) |
| Architecture decisions | [docs/adr/README.md](docs/adr/README.md) |
| Backlog | [docs/backlog.md](docs/backlog.md) |
| Changelog | [CHANGELOG.md](CHANGELOG.md) |
| ... | ... |

## Critical rules

- <positive assertion of what to do, load-bearing>
- <positive assertion of what to do, load-bearing>

## Code map

| Path | Purpose |
| ---- | ---- |
| ... | ... |

## Commands

| Command | Purpose |
| ---- | ---- |
| ... | ... |
```

## CLAUDE.md

```markdown
@AGENTS.md

## Claude-specific

- Skills available: <list of `.claude/skills/` skills relevant to this repo>
- Subagent guidance: <when to use which agent>
- Slash commands: <repo-specific commands, if any>
```

## docs/README.md

```markdown
# Documentation

| Topic | Link |
| ---- | ---- |
| Architecture | [architecture.md](architecture.md) |
| Development | [development.md](development.md) |
| Performance | [performance.md](performance.md) |
| ADRs | [adr/README.md](adr/README.md) |
| Backlog | [backlog.md](backlog.md) |
| ... | ... |
```

## docs/adr/NNNN-title.md

```markdown
# NNNN — <title>

- Status: Accepted | Proposed | Superseded by ADR-NNNN
- Date: YYYY-MM-DD

## Context

<what forced the decision — one or two paragraphs>

## Decision

<what we chose, in one or two sentences>

## Alternatives considered

- **Option A** — pros / cons; reason rejected.
- **Option B** — pros / cons; reason rejected.

## Consequences

<what changes downstream as a result — positive and negative>
```

Scaffold a new ADR file with `scripts/new-adr.sh <slug>`. It picks the next number, writes the frontmatter, and updates `docs/adr/README.md`.

## docs/adr/README.md

```markdown
# Architecture Decision Records

| # | Title | Status | Date |
| - | ----- | ------ | ---- |
| [0001](0001-<slug>.md) | <title> | Accepted | YYYY-MM-DD |
| [0002](0002-<slug>.md) | <title> | Superseded by ADR-0005 | YYYY-MM-DD |
```

## docs/backlog.md

```markdown
# Backlog

Planned-but-not-built work. Each item is a positive assertion of future-state behavior.

## <topic group>

- <item phrased as future-state behavior>
- <item phrased as future-state behavior>
```

## CHANGELOG.md

```markdown
# Changelog

All notable user-visible changes are recorded here.

## v0.4.0 - YYYY-MM-DD

### <feature group>

- <user-visible change in plain language>
- <user-visible change in plain language>

### <another feature group>

- ...

### Bug fixes

- Fixed <thing> so <correct behavior happens now>.

### Documentation

- Updated <areas> for <release-aligned reason>.  (only when substantive)
```
