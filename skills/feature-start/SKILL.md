---
name: feature-start
description: Use at the START of a non-trivial feature, port, migration, or subsystem — before any implementation — to produce an architecture-level plan. Triggers on "start a feature", "plan this", "how should we build X", "write an implementation plan", "we're going to port/add/build X", "scope this work". Runs a fixed sequence: load repo conventions, gather context (breadth), research the hard parts (depth), pause for clarifying decisions, confirm understanding, thread cross-cutting constraints, pre-create durable docs (delegating to repo-docs for ADRs/README/backlog) and CI-safe directory structure, then emit a numbered milestone plan with [DECISION] tags and a decisions table. Stops at milestone altitude; hand each phase to the plan-phase skill for step-level expansion before executing.
---

# Feature Start

Turn a vague "we're going to build/port X" into a confirmed, durably-documented, numbered
plan — without writing implementation. This is the front half of a two-skill workflow:
`feature-start` produces the architecture-level plan; **`plan-phase`** expands one phase into
execution-ready steps; the companion execution prompt runs them.

This skill lives in two places: `~/.claude/skills/feature-start/` for active use and
`~/repos/ahara/skills/feature-start/` for version-controlled durability. Keep them identical;
edit either and mirror.

## When to use

Use when work is large enough that a wrong shape is expensive: a new subsystem, a port, a
migration, a cross-cutting feature. Skip for a single localized change — just do it.

## The sequence

Run these in order. Each stage has an output; do not advance until it exists. Full detail in
[references/sequence.md](references/sequence.md).

| # | Stage | Output | Hard rule |
| - | ----- | ------ | --------- |
| S0 | Frame & load conventions | One-screen "what I'm working with" | Read the doc surface (README/AGENTS/CLAUDE/docs index/ADRs); note the canonical verify command, critical rules, code map |
| S1 | Gather context (breadth) | Context map: exists/overlaps vs gaps | **Verify against current code, not memory or docs**; fan out (Explore/Agent) |
| S2 | Research hard parts (depth) | Reuse inventory + risk list | Decide reuse-vs-build; note where **intent diverges** from existing use |
| S3 | Clarify (pause) | Recorded answers | Ask **only** shape-changing decisions as structured multiple-choice; never ask what you can verify or default. **This is a hard pause.** |
| S4 | Confirm understanding | Explicit user "yes" | Present the rough analysis; do not design until confirmed |
| S5 | Thread constraints | Each constraint woven through + re-verified | A constraint that rests on a fact (e.g. a dependency boundary) is checked against code |
| S6 | Pre-create durable docs + structure | ADRs, README/AGENTS/backlog/CHANGELOG, CI-safe dirs | Delegate doc conventions to the **repo-docs** skill; scaffolds must not break the build |
| S7 | Write the milestone plan | The plan, in the grammar | Numbered phases, each with an exit gate; `[DECISION]` tags; decisions table; context section |
| S8 | Decision register & handoff | Plan is single source of truth; published plan tracks it | Collate `[DECISION]` points; publish the root plan (`sulion plan start`, one phase per milestone); hand phases to `plan-phase` |

## The plan it emits

Milestone altitude — numbered phases, not step-level. The grammar (phases, exit gates,
`[DECISION]`, `[depends on]`, decisions table, context/reuse section) is defined in
[references/plan-grammar.md](references/plan-grammar.md); both skills key off it. Step-level
file/test detail is deliberately **deferred** to `plan-phase`, just-in-time before a phase runs,
so detail isn't written for phases that may change.

Place the plan at the repo root as a temporary working doc (e.g. `<FEATURE>-PLAN.md`) unless
the repo's conventions say otherwise. Durable trade-offs go to ADRs, future work to the
backlog, decided architecture to the architecture doc — via the repo-docs skill, never inlined
into the plan.

## Publishing it (inside a Sulion PTY)

The plan file carries the detail; a published plan carries the progress, and survives the
terminal. Publish the milestones as the **root** plan, one phase per milestone, so every phase
expansion and every mid-flight detour has something to hang off:

```sh
sulion plan start "<Feature>" --summary "<one line>" \
  --phase "M0 — Foundation|<the milestone's one-line goal>|m" \
  --phase "M1 — Oracle ladder|<…>|l"
```

Keep the phase titles identical to the plan file's milestone headings — `plan-phase` anchors its
branch to a phase by position, and the executor reads the two side by side. Size each phase
(`s|m|l`) when the milestones differ enough in weight to matter. Outside a Sulion PTY, skip this
and let the plan file stand alone.

## Prohibitions

- Do not skip S4. Designing before the user confirms understanding wastes the whole plan.
- Do not ask in S3 what you can answer by reading code, or what has a sensible default — pick
  it, state it, move on.
- Do not let S6 scaffolding break CI: reserve crate/dir homes with READMEs, but do not register
  half-built workspace members. Verify the build is untouched.
- Do not put trade-offs, pros/cons, or "we considered X" into the plan or `docs/` — those go to
  ADRs (use repo-docs).
- Do not write step-level file/test detail here. That is `plan-phase`'s job.
- Do not start implementing. This skill ends at a written, confirmed plan.

## Handoff

When the plan is written, decisions are registered, and the root plan is published, stop. To
execute, the user runs `plan-phase` on one phase to expand it into steps, then the companion
execution prompt (`~/.claude/skills/plan-phase/EXECUTE-PHASE.md`) to run them.
