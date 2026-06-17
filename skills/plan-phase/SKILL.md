---
name: plan-phase
description: Use just before executing one phase of an existing feature-start plan, to expand that single milestone into execution-ready numbered steps. Triggers on "plan phase N", "expand phase N into steps", "make phase N executable", "break down the next phase", "detail M2 before I run it". Takes one phase from the milestone plan and writes ordered steps, each naming its file(s), the reference-correct behavior to re-derive, the minimal change, and a red→green verification, with [DECISION] tags and [depends on #X] markers. Pairs with the companion execution prompt (EXECUTE-PHASE.md) that runs the steps. Expand one phase at a time, just-in-time — never the whole plan up front.
---

# Plan a Phase

Turn one milestone from a `feature-start` plan into steps an executor can run mechanically. This
is the back half of the workflow: `feature-start` wrote the milestone plan; this skill expands
**one** phase into step-level detail; the companion prompt
([EXECUTE-PHASE.md](EXECUTE-PHASE.md)) runs it.

This skill lives in two places: `~/.claude/skills/plan-phase/` for active use and
`~/repos/ahara/skills/plan-phase/` for version-controlled durability. Keep them identical; edit
either and mirror.

## When to use

Just before executing a phase — not before. Expanding step-level detail for a phase that may
still change (a contingency, a phase gated on an earlier benchmark) is waste. Expand the phase
you are about to run, run it, then expand the next. One phase at a time.

## The per-step template

Each step strongly should carry these fields (strong guidance, not a hard gate — omit a field
only when the step genuinely has no use for it, and say why):

```
N. <imperative title>  [depends on #M]  [DECISION]
   - File(s): <the path(s) the step centers on — plus the incidental plumbing the change
     requires (a new dependency, module/workspace-member registration, test wiring); these are
     part of the step, not new scope>
   - Reference behavior: <the correct semantics to re-derive before editing; cite the plan's
     Context/reuse-map section or an ADR>
   - Change: <the minimal edit; no abstraction or refactor beyond what's named>
   - Verify: <the exact test, written red→green>
```

- **Number** every step; they run in listed order.
- **`[depends on #M]`** when a step needs an earlier step's result and order alone doesn't make
  it obvious.
- **`[DECISION]`** when the step's semantics need the user's call — the executor stops here.

## The red→green rule (including greenfield)

Every step's verification is a test that is **red before the change, green after.**

- **Modifying existing behavior:** red means the old behavior fails the new assertion.
- **New code (greenfield):** red means the symbol, crate, or contract does not exist yet — the
  test fails to compile or resolve. That still counts as red→green; say so in the step so the
  executor doesn't expect a behavioral failure.

Do not specify a test that passes before the change — it proves nothing.

## Plan-specified refactors are legitimate

If the phase calls for a refactor (extract a module, lift a shared helper), write it as its own
numbered step with its file list and a verification (behavior-preserving: the same tests pass
before and after, or a characterization test). This keeps it from looking like "invented work"
or "refactoring surrounding code" to the executor.

## Procedure

1. Read the named phase from the plan, plus the plan's Context / reuse-map section and any ADRs
   it cites. Do not read ahead into other phases.
2. Decompose the phase into the smallest ordered steps that each touch as few files as possible.
3. Fill the template per step. Re-derive reference behavior from the cited source-of-truth, not
   memory.
4. Mark `[depends on]` and `[DECISION]` where they apply. Lift any phase-level `[DECISION]` down
   to the specific step that owns it.
5. Hand off: the user runs the companion execution prompt on this phase.

## Prohibitions

- Do not expand more than the requested phase.
- Do not invent steps, abstractions, or tests beyond what the milestone specifies. If the phase
  is underspecified, surface that as a `[DECISION]` rather than inventing scope.
- Do not specify cross-file sweeping edits in one step; split them so each is reviewable.
- Do not change the plan's grammar or rename its `[DECISION]` / `[depends on]` tags — the
  execution prompt keys off them verbatim.
