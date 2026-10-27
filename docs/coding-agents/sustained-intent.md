# Preserve Intent Through Long-Running Work

[Practice index](../agentic-engineering.md)

Keep the requested outcome stable while adapting the mechanism to evidence.
A plan represents current intent and approach; writing a choice into it does
not make that choice a user requirement.

## Retain the Working Contract

| Element | Purpose |
| --- | --- |
| Outcome | What must become true for the user, with evidence of success |
| Requirements and agreed boundaries | Behavior and constraints the implementation must preserve |
| Corrections | Rejected approaches, misunderstood requirements, and instructions that change subsequent work |
| Principles | Reasons for choosing among valid approaches |
| Assumptions | Beliefs the approach depends on and evidence that could invalidate them |
| Phases and current state | Remaining work, dependencies, blockers, and what has actually been established |

Attribute requirements, user corrections, and agent proposals separately.
Preserve the reason for a boundary when its wording alone could be misapplied.
Keep the record concise enough to consult during work.

## Reconcile Before Continuing

At phase start, after interruption, and when evidence contradicts the approach:

1. Read current guidance and its relevant sources, including parent boundaries.
2. Compare the checkout or domain artifact with the recorded state.
3. Identify the next action and the required behavior it advances.
4. Revise stale implementation steps and their checks while preserving the
   user's outcome and agreed constraints.

When corrected, update the boundary and affected work before continuing.
An accurate acknowledgment alone leaves the old plan available to mislead the
next session. Later feedback may refine earlier intent; it does not erase it
by default.

## Keep Prerequisites Attached to the Outcome

Name the concrete behavior a prerequisite enables. If supporting machinery
keeps improving while the requested behavior remains absent, reassess the
approach. Technical consistency and passing tests of a substitute do not
establish the outcome.

Use a sub-plan for a prerequisite that is itself a multi-step job. Preserve the
parent's boundaries, record why the parent is blocked, and return when the
prerequisite is resolved. A sub-plan organizes work; it does not authorize
unrelated repairs or weaken the parent contract. Keep small incidental fixes
within the existing phase.

Bound depth without reducing coverage. An instruction to avoid minor edge
cases does not authorize skipping required states or stopping after an
arbitrary number of improvements.

## Adapt Within Authority

Change agent-derived mechanisms when evidence supports a simpler complete
solution. Explain consequential changes. Ask before changing user requirements
or explicitly agreed architectural boundaries. Ordinary implementation choices
within those boundaries need no repeated permission.

If the requirements conflict or the approach cannot satisfy them, state the
conflict and recommended resolution. Preserve useful work and accurate status;
do not redefine success around what was easiest to build.

## Close Against the Outcome

Distinguish completed behavior, supporting work, and unverified claims. A
completed phase records evidence, not effort or confidence. Retain unresolved
work explicitly rather than making it disappear through closure.

Move lasting mechanisms and decisions into their owning documentation at the
appropriate fidelity. Follow the repository's lifecycle for closed working
plans. A resumed agent should find the current system without treating an old
implementation plan as present authority.

For the tooling that makes this practical, use [meta-harness](meta-harness.md).
