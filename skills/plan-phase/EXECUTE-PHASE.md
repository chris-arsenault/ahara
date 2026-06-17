# Execute Phase — canonical prompt

Paste this to run a phase that `plan-phase` has expanded. It is the revised form of the
"Work Phase N" prompt, updated to match the shared plan grammar (greenfield red→green,
plan-specified refactors, source-of-truth re-derivation, per-phase exit gate).

---

Work Phase N of the plan — only the steps in that phase, in the order listed. The plan is the
single source of truth: every location, fix, and verification is already in it. Re-derive
reference-correct behavior from the plan's Context / reuse-map section and any ADRs it cites.
Do not start other phases, do not invent work, abstractions, or tests beyond what the steps
specify, and do not refactor surrounding code except where a step is itself a plan-specified
refactor.

For each step in the phase, in order:

1. Correctness over speed. Re-derive or re-confirm the reference-correct behavior the step
   names before editing; if a step is tagged [DECISION], stop and ask me — do not change
   semantics by guessing.
2. Make the change the step describes. The named file(s) are its scope — but also make the
   incidental supporting edits that change genuinely requires to build and verify: adding a
   dependency it needs, registering a new module or workspace member, wiring a test harness.
   Those are part of the step, not new scope. Do not touch unrelated code, add unrequested
   behavior, or refactor beyond the step.
3. Add exactly the verification the step calls for. Confirm the test is red before your change
   and green after — for new code, red means the named symbol or contract does not exist yet;
   for a behavior change, red means the old behavior fails the new assertion.
4. Run the phase's stated exit gate (`make ci` unless the phase names another) and show me the
   actual output — don't claim it passes without it.

Respect each step's [depends on #X] ordering. When the phase is done, report per-step what
changed and what was verified, then stop — do not roll into the next phase.

---

## What changed from the original prompt, and why

- **Greenfield red→green (step 3).** New crates/symbols have nothing to "fail on." Red now also
  means "the symbol/contract does not exist yet," so the rule covers adding new code, not just
  modifying existing behavior.
- **Plan-specified refactors (intro).** Some steps *are* refactors (extract a module). The
  blanket "do not refactor surrounding code" now carves out refactors the plan names as steps,
  so they aren't mistaken for invented work.
- **Source-of-truth re-derivation (intro).** Points the executor at the plan's Context /
  reuse-map section and cited ADRs, so "re-derive reference behavior" uses the right canon.
- **Per-phase exit gate (step 4).** The grammar lets a phase declare its own exit command; the
  default remains `make ci`.
- **Named files are scope, not a whitelist (step 2).** The original "only touch the file(s) it
  names" blocked necessary plumbing — a step that says "verify allocation-free" but needs a
  dev-dependency to do so should add it. Named files define intent; incidental supporting edits
  the change requires are part of the step. The guard against scope creep is "no unrelated code,
  no unrequested behavior, no refactor beyond the step" — not a literal file count.
