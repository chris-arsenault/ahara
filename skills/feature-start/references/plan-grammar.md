# Shared plan grammar

The plan is a contract between three things: this skill (which writes it), the **plan-phase**
skill (which expands a phase into steps), and the **execution prompt** (which runs the steps).
Every element below exists because one of those consumers depends on it. Keep the vocabulary
identical across all three.

## Structure

```
# <Feature> — Implementation Plan

<one-paragraph intent: what, for whom, what's out of scope>

## Confirmed decisions
<the settled choices from the clarify stage, as assertions>

## Context / reuse map            <- the executor re-derives reference behavior from here
<what exists and is reused; what is built new; the source-of-truth files and ADRs>

## Cross-cutting constraints       <- each links to its ADR if durable
<constraints that apply to every phase>

## Milestones
<numbered phases; see below>

### Decisions needing your input
| Where | Decision you own |        <- collated [DECISION] register
```

## Phases

- Numbered `M0…Mn` (or `Phase 0…n`), each a coherent unit with a single **exit gate**.
- The exit gate is the repo's canonical verify command (e.g. `make ci`) plus the phase's own
  pass condition ("all Tier-1 effects pass both batteries").
- Phases may carry `[depends on M#]` when ordering is not strictly sequential.
- A phase that is conditional on an earlier result says so in its heading (e.g. `CONTINGENT on
  M2 gate`).

## `[DECISION]` tags

Tag any phase or step whose **semantics** need the user's call — a choice the plan cannot
settle from code or defaults. The execution prompt stops on these. Collect every one into the
`Decisions needing your input` table so the user sees them at a glance.

Do **not** tag mechanical choices the executor can make correctly alone — only genuine forks
(tuning by taste, promoting work into shared infra, accepting a license, picking a model).

## What this skill fills vs. what plan-phase fills

| Field | feature-start (milestone altitude) | plan-phase (step altitude) |
| ----- | --------------------------------- | -------------------------- |
| Phase number + title + exit gate | ✅ | inherits |
| Phase intent / scope | ✅ | inherits |
| `[DECISION]` at phase level | ✅ | refines to step level |
| `[depends on]` between phases | ✅ | adds between steps |
| Context / reuse map | ✅ | cites it |
| Per-step file list | — | ✅ |
| Per-step reference-correct behavior | — | ✅ |
| Per-step minimal change | — | ✅ |
| Per-step red→green verification | — | ✅ |

feature-start stops at the left column. Writing step-level detail up front for a phase that may
change (a contingency, a phase gated on a benchmark) is waste — `plan-phase` fills the right
column just-in-time, right before that phase runs.

## Milestone skeleton (what S7 emits per phase)

```
### M<n> — <title>
<one-line intent>
- <work item at milestone altitude>
- <work item>
- **[DECISION]** <fork the user owns, if any>
- Exit: <canonical verify command> green; <phase-specific pass condition>.
```
