# Durable plan contract

The working plan document is the detailed handoff between feature-start, plan-phase, and the
executor. Sulion provides the corresponding progress tree. Keep one detailed record rather
than separate chat-only expansions or duplicate reports.

## Feature-level record

Include what the work needs; omit empty sections.

- **Outcome and scope:** intended user or system result, non-goals, required durability,
  safety, ownership boundaries, and what execution or publication the user has authorized.
- **Context / reuse map:** source-of-truth paths, relevant producers and consumers, reuse
  choices, and evidence supporting material assumptions. Retrieved history records intent;
  current sources establish implementation facts.
- **Decisions:** settled choices with their basis; provisional assumptions with how they
  will be checked; deferred choices with an owner, evidence trigger, and affected milestone.
  Include the rationale and alternatives needed to review a proposal. Link durable ADRs
  when they exist; do not create one for every routine choice.
- **Milestones:** numbered M0…Mn, each with scope, dependencies, an acceptance condition, and
  evidence that will establish it. Conditional milestones name the condition.
- **Sulion mapping:** root plan ID, milestone phase IDs, and expansion/step IDs once created.
- **Current state:** completed work, remaining work, blockers, and the next action.

Use `[depends on M#]` between milestones and `[depends on #N]` between expansion steps when
a dependency matters. Use `[DECISION]` for unresolved user-owned choices. Record when each
choice becomes blocking; its presence in a later milestone does not halt independent work.
Technical unknowns that can be resolved by authorized investigation are investigation work,
not automatically questions for the user.

## Phase expansion

Plan-phase adds an expansion under the selected milestone in the same document:

```text
### M<n> — <outcome>
Scope: <what this milestone establishes>
Depends on: <milestones and required results, if any>
Acceptance: <observable result and constraints>
Evidence: <checks or review establishing acceptance>
Sulion: <milestone phase ID>; expansion <plan ID>

#### Execution steps
1. <coherent outcome> [depends on #N] [DECISION, only if applicable]
   - File(s): <primary files and required supporting edits>
   - Reference / outcome: <contract, invariant, or claim and its source>
   - Change: <smallest complete implementation>
   - Verify: <evidence, pass condition, and useful baseline or shared-check timing>
   - State / evidence: <step ID, progress, actual result or unverified remainder>

#### Changes and resume
<material plan changes and their evidence; unresolved decisions; next action>
```

Fields guide judgment; they are not a quota of artifacts or tests. Related steps may share a
check. Acceptance can be established by source review, behavior tests, measurements, or other
appropriate evidence; an artificial failing baseline is not required.

## Adaptation and provenance

The user request and settled constraints govern scope. Current evidence may invalidate a
planned implementation. The executor may reuse a newly discovered helper, change file locations,
reorder independent work, combine related edits, or skip an already-satisfied step without
reapproval when the outcome and acceptance criteria remain intact. Record the reason and
evidence, update dependencies and Sulion mappings, and preserve the history of completed steps.

Do not silently weaken acceptance, erase a requirement, change user-owned behavior, or expand
authority. Surface such changes for a decision. Preserve pending user decisions through resume;
do not treat assumptions, status labels, or elapsed time as approval.

Evidence records identify the check or reviewed source, its actual result, and relevant limits.
For runtime checks, include the target or revision when it matters. Before a handoff, record
enough state for a new executor to resume without guessing from the latest chat message.
