---
name: repo-docs
description: Use whenever you create, update, or audit a repository's documentation surface — README.md, AGENTS.md, CLAUDE.md, docs/, CHANGELOG.md, docs/adr/, docs/backlog.md. Triggers on phrases like "set up docs", "write a CHANGELOG", "fix the README", "add an ADR", "where does X belong in the docs", "audit the docs", or any PR touching multiple top-level doc files. Apply when a repo has no documentation pass yet — the audit-and-rewrite procedure expects substantial changes by default. Prescribes index-style top-level files, current-state assertions, positive language, ADRs as the only home for trade-offs, a separate future-state backlog, and a Common-Changelog-style CHANGELOG.
---

# Repository Documentation Conventions

This skill lives in two places: `~/.claude/skills/repo-docs/` for active use by Claude Code, and `~/repos/ahara/skills/repo-docs/` for version-controlled durability. The two are kept identical; edit either and mirror.

## Procedure

### 1. Identify the task type

| Trigger | Read first | Then |
| ---- | ---- | ---- |
| New repo from scratch | [references/skeletons.md](references/skeletons.md) | Create each file from the matching skeleton; apply prohibitions below |
| Existing repo, no convention applied | [references/applying.md](references/applying.md) | Run the audit; surface violations; create scaffolds; rewrite violators |
| Single file edit | [references/skeletons.md](references/skeletons.md) §<file> + [references/principles.md](references/principles.md) | Apply prohibitions below at point of change |
| Audit a PR | [references/principles.md](references/principles.md) + [references/applying.md](references/applying.md) §1 | Quote violations by file:line |
| Add an ADR | [references/skeletons.md](references/skeletons.md) §`docs/adr/NNNN-title.md` | Run `scripts/new-adr.sh <slug>` to scaffold, then write Context/Decision/Alternatives/Consequences |

### 2. File map

| File | Purpose | Length target |
| ---- | ---- | ---- |
| `README.md` | Index + one-screen quickstart | ≤ ~150 lines |
| `AGENTS.md` | Canonical rules for every coding agent | ≤ ~200 lines |
| `CLAUDE.md` | `@AGENTS.md` import + Claude-Code-specific overrides | ≤ ~80 lines |
| `docs/README.md` | Table-of-contents into `docs/` | Index table only |
| `docs/<topic>.md` | Current-state reference for one topic | As long as needed |
| `docs/adr/NNNN-title.md` | One architectural decision with trade-offs | ≤ ~200 lines |
| `docs/adr/README.md` | ADR index (TOC + status + date) | Index table only |
| `docs/backlog.md` | Planned-but-not-built work | As long as needed |
| `CHANGELOG.md` | Version-grain shipped-behavior log | Common-Changelog style |

For full skeletons of each file, open [references/skeletons.md](references/skeletons.md). For the reasoning behind each principle, open [references/principles.md](references/principles.md).

### 3. Apply substantial changes by default on existing repos

When the task is "apply this to a repo," do not stop at additive scaffolds. The audit-and-rewrite procedure in [references/applying.md](references/applying.md) is the default scope. Expect to rewrite Non-goals sections, strip deferral status phrasing, remove historical narrative from architecture docs, and extract trade-offs to ADRs.

## Prohibitions (apply inline as you write)

**In top-level files (README, AGENTS, CLAUDE):**
- Do NOT inline content that belongs in `docs/`. The top-level files are indexes.
- Do NOT duplicate content between AGENTS.md and CLAUDE.md. CLAUDE.md is `@AGENTS.md` plus Claude-specific overrides.
- Do NOT keep broken links to legacy agent files (e.g., `CODEX.md` when `AGENTS.md` is canonical).

**In any `docs/` file:**
- Do NOT write "we used to", "previously", "this was migrated from". Version history lives in `CHANGELOG.md`.
- Do NOT write "we plan to", "next release will". Future state lives in `docs/backlog.md`.
- Do NOT write pros/cons or trade-off prose. Trade-offs live in `docs/adr/`.
- Do NOT write apologetic language ("this isn't ideal but…", "for historical reasons").

**In `docs/<feature>.md` files:**
- Do NOT write `Non-goals: Not a X / Not a Y` lists. Express scope through positive boundary statements instead.
- Do NOT write Status lines with deferral phrasing ("tracked in backlog", "DAW validation pending"). The backlog speaks for itself.
- Do NOT scatter `Limitations` content across the doc. If genuinely necessary, scope to a single subsection.

**In `CHANGELOG.md`:**
- Do NOT add entries for dependency bumps, typo fixes, CI tweaks, or formatting changes.
- Do NOT add entries for small documentation tweaks. Substantive doc reorganizations tied to a release may appear as one line per release.
- Do NOT auto-generate from `git log`. The changelog is curated; commits target a different audience.

**In `docs/adr/`:**
- Do NOT create an ADR for a decision with no real alternatives. Use a short note in `docs/<topic>.md` instead.
- Do NOT mutate accepted ADRs. Create a new one with `Status: Supersedes ADR-NNNN` and update the superseded entry's status.

**In `docs/backlog.md`:**
- Do NOT phrase items as negations ("X is not supported"). Phrase as positive future-state behavior ("Add X").
- Do NOT use GitHub Issues or Projects as the canonical backlog when the repo has AI-agent readers. Agents cannot read external systems reliably; `docs/backlog.md` is discoverable from a checkout.

## Quick reference

| Need | File | Pattern |
| ---- | ---- | ---- |
| Migration narrative | `CHANGELOG.md` | Past tense, version-grain |
| "We considered X but chose Y" | `docs/adr/NNNN-…md` | Nygard sections |
| "X will be added in v2" | `docs/backlog.md` | Positive future-state |
| "X is not implemented yet" | `docs/backlog.md` (rephrased positively) | "Add X" |
| Long architecture explanation | `docs/architecture.md` | Topic-split |
| CI / build / dev rule | `AGENTS.md` Critical Rules | Imperative bullet |
| Claude-specific instruction | `CLAUDE.md` after `@AGENTS.md` | Thin Claude-specific section |
| Trade-off justification for a baked-in rule | `docs/adr/NNNN-…md` | New ADR; link from `docs/architecture.md` |
| Generate a fresh ADR file | `scripts/new-adr.sh <slug>` | Picks next number, writes frontmatter, updates index |

## Meta-repos

A meta-repo (no shipped product, just conventions and tooling — e.g., ahara) may use a flat-root pattern: `README.md` doubles as the docs index, `AGENTS.md`/`CLAUDE.md` as above, convention files at root (e.g., `CI-WORKFLOW.md`, `INTEGRATION.md`), a `skills/` directory for version-controlled skill mirrors, no `docs/`, no `CHANGELOG.md`, no backlog. The full pattern above is for product repos.

## References

- [references/principles.md](references/principles.md) — eight core principles with reasoning.
- [references/skeletons.md](references/skeletons.md) — file skeletons for every file in the map.
- [references/applying.md](references/applying.md) — full procedure for applying to an existing repo.
- [agents.md cross-tool spec](https://agents.md/).
- [Claude Code memory docs](https://code.claude.com/docs/en/memory).
- [Common Changelog](https://common-changelog.org/).
- [Fowler — Architecture Decision Records](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html).
