# Applying to an existing repo

Procedure for applying the convention to a repo that was written without it. The default scope is substantial: audit every doc, create the missing scaffolds, AND rewrite the violators. Stopping at "create scaffolds" leaves the repo half-converted.

Work in this order so destructive edits come last and review is easy.

## 1. Inventory and audit

Read every `.md` in the repo. Produce a structured list of violations with file:line quotes. Look for:

- **Historical narrative** outside `CHANGELOG.md` or an ADR. Phrases: "we used to", "previously", "migrated from".
- **Apologetic language.** Phrases: "this isn't ideal but", "for historical reasons", "TODO/FIXME prose".
- **Negation-list defaults.** Sections titled "Non-goals" with "Not a X / Not a Y" bullets, where surrounding positive content already covers the scope.
- **Future-state content inline.** Phrases: "we plan to", "next release will". Roadmap-ish bullets in architecture docs.
- **Pros/cons or trade-off prose** outside `docs/adr/`.
- **Top-level files containing prose** that belongs in `docs/`. Especially `README.md`, `AGENTS.md`, `CLAUDE.md` with sections exceeding a screen.
- **Status fields with deferral phrasing.** Phrases: "tracked in backlog", "DAW validation pending", "still a scaffold".
- **Broken links to legacy agent files** (e.g., `CODEX.md` referenced after `AGENTS.md` became canonical).
- **AGENTS.md / CLAUDE.md duplicated identically.** Should be canonical-plus-import.

For each violation, record: file path, line number(s), quoted text, which principle it violates.

## 2. Create the missing scaffolds (additive, low-risk)

These are net-new files; they don't conflict with existing content. Do them in parallel:

- **`CHANGELOG.md`** from `git log` (curated, not auto-generated). Common-Changelog tone. Version-grain. Tag the current Cargo/package version as the top section.
- **`docs/adr/README.md`** index plus ADRs extracted from decisions baked into the codebase but not currently documented as decisions. Look for: realtime safety rules, dependency choices ("no plugin framework"), platform constraints ("macOS-only build"), workflow rules ("synthetic-only test fixtures"), architecture patterns ("parameter registry as single source of truth"). Each becomes one ADR with Nygard sections.
- **`docs/backlog.md`** workspace-level rollup. Pull planned-but-not-built work from per-feature backlogs, roadmap mentions in architecture docs, and `*-implementation-plan.md` files.
- **`CLAUDE.md`** as `@AGENTS.md` import plus a Claude-specific section. If `AGENTS.md` doesn't exist yet, the current `CLAUDE.md` content is what `AGENTS.md` should contain — promote it.

## 3. Rewrite existing docs (higher-risk; surface diffs)

These edits change existing content; review carefully:

- **Convert `Non-goals` sections** to positive Scope statements, or delete them entirely when surrounding positive boundaries already cover the same ground.
- **Strip deferral phrasing from Status lines.** Replace "X is tracked in [backlog]" with the current state alone. The backlog speaks for itself; the changelog speaks for itself.
- **Remove historical narrative from architecture docs.** The decision rationale lives in ADRs. Lines like "These principles came out of the X work" become straightforward present-tense claims, with a link to the relevant ADR.
- **Push pros/cons prose out of feature docs into ADRs.** Each extracted block becomes an ADR with Context, Decision, Alternatives Considered, Consequences.

## 4. Update the indexes

- Add `CHANGELOG.md`, `docs/adr/README.md`, `docs/backlog.md` to `docs/README.md` and `AGENTS.md` `Read first` tables.
- Remove broken links to legacy agent files (e.g., `CODEX.md` when `AGENTS.md` is canonical).
- Update plugin/feature doc index tables to drop deferral phrasing.

## 5. Verify

- Open `AGENTS.md` and `CLAUDE.md` and re-read them as if you were a new agent — they should be terse, index-style, and free of historical narrative.
- Run the repo's CI (e.g., `make ci`) to confirm no doc-related lint or link-check broke.
- Spot-check three random `.md` files for the prohibitions in the skill's main body.

## Anti-patterns specific to the existing-repo application

- **"Scaffold and go."** Creating `CHANGELOG.md`, `docs/adr/`, and `docs/backlog.md` but leaving the violating content elsewhere. The repo ends half-converted.
- **Unilaterally deleting root-level plan files.** Some `*-implementation-plan.md` files are intentional. Move only when the user agrees, or surface the candidates and let the user decide.
- **Rewriting the spec doc.** Plugin-specific spec docs (`docs/plugins/<product>.md`) sometimes reference a planned-but-not-moved implementation plan deliberately. Confirm the move before rewriting the spec to point elsewhere.
- **Treating `AGENTS.md` as authoritative content rather than as an index.** AGENTS.md is for rules, code map, and commands at the top level. Long explanations move to `docs/`.
- **Forgetting the deferral-status sweep.** It's tempting to skip status-line fixes because they're small. Sweep them — they are the most common surface of negation-default thinking.
