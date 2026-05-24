# Core principles — reasoning

Eight principles that govern repository documentation. Each carries a one-line statement plus its reasoning, so judgment-call edge cases stay decidable.

## 1. Index, not encyclopedia

Top-level files (`README.md`, `AGENTS.md`, `CLAUDE.md`) are navigational. A one-paragraph intro plus a table of pointers into `docs/`. Anything that grows past a screen moves to `docs/`.

**Why:** `AGENTS.md` and `CLAUDE.md` load into the agent's context at session start. Anthropic's Claude Code memory docs note that longer files "consume more context and reduce adherence." Top-level files that grow encyclopedically displace conversation context and degrade the agent's responsiveness to the rules they contain.

## 2. AGENTS.md is canonical; CLAUDE.md imports it

`AGENTS.md` carries the cross-tool rules that every coding agent (Claude Code, Cursor, Aider, Codex, and others) reads. `CLAUDE.md` is thin:

```markdown
@AGENTS.md

## Claude-specific

- Skills available: ...
- Subagent guidance: ...
```

**Why:** The agents.md cross-tool spec is read by 20+ tools. Anthropic's Claude Code memory docs explicitly recommend the import pattern over keeping duplicate copies. Duplicate files always drift; one canonical file with thin tool-specific overrides does not.

## 3. Current state only

Documents describe what *is*, not what *was* or what *we're planning*. No migration narratives, no apologetics, no historical asides outside the places designed for them.

Three overflow valves:
- Version history → `CHANGELOG.md`.
- Design rationale and trade-offs → `docs/adr/`.
- Future work → `docs/backlog.md`.

If a sentence starts with "we used to", "previously", "this was migrated from", or "we plan to", it belongs in one of those three files instead.

**Why:** Agents and new humans both read docs as ground truth. Historical content trains the wrong prior — a "we used to use Redis" sentence sitting next to "we now use PostgreSQL" produces unpredictable behavior because the model picks one arbitrarily. This is "context poisoning" in the agent-tooling literature.

## 4. Positive assertions

Tell readers (and agents) what the system does and what to do. Avoid lists of what wasn't implemented or what to avoid as defaults.

**Why:** Anthropic's Claude 4 best-practices doc names this as the first technique for instruction-tuning: *"Tell Claude what to do instead of what not to do."* Positive examples beat negative ones for both prompts and files read into context. The same mechanism applies to repo docs because `AGENTS.md`/`CLAUDE.md` content is delivered to the agent as user-message context.

## 5. Limitations are scoped

When discoverability genuinely requires a negation ("Glirdir does not yet ingest streamed sidechain input"), put it in a single `Limitations` subsection inside the relevant feature doc. Never at the top of `README.md`, never in `AGENTS.md`/`CLAUDE.md`, never in `CHANGELOG.md`. Prefer rephrasing the negation as a positive backlog entry first.

**Why:** The discoverability case is real — sometimes a user does need to know X isn't supported to stop searching. The conventional resolution is to scope negations to one local subsection, not scatter them and not promote them to top-level files. This bounds the damage of negation-default thinking without losing the information.

## 6. Trade-offs live in ADRs only

Every architectural decision with real alternatives gets a single file under `docs/adr/NNNN-title.md` with the Nygard sections (Context, Decision, Alternatives Considered, Consequences). The index lives at `docs/adr/README.md`. Other docs reference ADRs by number but do not duplicate their reasoning.

**Why:** Fowler and Nygard both describe ADRs as the canonical home for "why we chose X over Y, Z." Putting pros/cons in architecture docs makes the architecture doc historical instead of current-state. If you find yourself writing pros/cons in `docs/architecture.md`, extract them to an ADR and link.

## 7. Future state lives in a backlog

`docs/backlog.md` lists planned-but-not-built work. Each item is a positive assertion of future-state behavior. Distinct from:
- ADRs — decisions made.
- Specs — designs about to begin (`docs/specs/<name>.md`).
- CHANGELOG.md — shipped behavior only.

**Why:** Mainstream OSS uses GitHub Issues for this, but GitHub Issues are not discoverable from a checkout and not reliably readable by AI agents. An in-repo file is portable and grep-able. Phrasing items as positive intent rather than as negations of current state preserves the positive-assertion principle.

## 8. CHANGELOG.md is shipped behavior at version-grain

- Version heading: `## vMAJOR.MINOR.PATCH - YYYY-MM-DD`. Pre-1.0 still uses `0.x`.
- Topic-grouped subsections.
- Each bullet is one sentence in plain language about a user-visible change. Past-tense action verbs by default.
- A `### Bug fixes` subsection per version.
- Substantive documentation reorganizations tied to a release MAY appear as a single bullet under a final "Documentation" subsection. Small doc tweaks, typos, formatting, link updates, internal refactors, dependency bumps, and CI config changes DO NOT appear.

**Why:** Common Changelog (the stricter sibling of Keep a Changelog) prescribes this exact tone. Auto-generated commit-log changelogs are noisy because commits target a different audience than the changelog. Small doc/typo/CI entries waste reader attention on changes that did not change product behavior.
