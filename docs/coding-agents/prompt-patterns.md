# Prompt Patterns and Task Contracts

[Practice index](../agentic-engineering.md)

Interpret the user's request together with standing instructions and prior
authorization. Use these shapes to clarify your own work or write a bounded
assignment; do not require the user to fill out a template.

## Recover the Contract

| Element | Establish |
| --- | --- |
| Mode | Investigate, propose, review, implement, or operate |
| Outcome | What should become true for a person or system |
| Evidence | The sources and observations needed to decide or verify |
| Boundaries | Required behavior, excluded scope, and authority |
| Delegated judgment | Choices you can resolve and choices the user retains |
| Persistence | The authorized stopping point and legitimate blockers |
| Completion | Evidence that the requested result exists |

State only what the task needs. Standing context supplies stable defaults.
A short continuation usually carries the established contract forward.

## Apply the Relevant Shape

| Task | Working direction |
| --- | --- |
| Design a substantial feature | Investigate the system and consumers; recommend a complete design with clear decisions, dependencies, and acceptance |
| Resume work | Reconcile intent, current artifacts, worktree ownership, plan state, and verification before choosing the next action |
| Review architecture | Trace the actual paths against named boundaries and the system's real risk; distinguish defects, risks, and preferences |
| Review a change | Follow the intended contract through affected producers and consumers, including user and operational paths |
| Diagnose | State the symptom, inspect code and observations, test differentiating hypotheses, and report what remains unresolved |
| Act on findings | Fix authorized defects; surface changes to product or agreed architecture; keep uncertain causes as hypotheses |
| Execute one phase | Complete its authorized behavior and required plumbing, verify it, and stop at that boundary |
| Execute a full plan | Continue through authorized phases; stop for genuine blockers or decisions outside authority |
| Reconcile a drifting design | Recover the whole requirement and decision history; resolve contradictions before extending the mechanism |
| Operate or deploy | Use the permitted write path, inspect real failures, and continue to an observable terminal condition |

Planning depth follows architectural uncertainty and consequences. An ordinary
repair or documentation edit can proceed directly with appropriate tracking;
it does not need a feature-design ceremony.

## Ask at the Actual Decision Boundary

Use available context before asking for missing information. Ask when the
answer materially changes the outcome, risk, or an agreed boundary. Make
routine technical decisions and explain consequential adaptations.

Authorization persists across the task. Continuing an approved plan does not
need a new approval at every phase. A request to review or answer does not by
itself authorize repairs. Commit, push, deploy, and other external writes
remain governed by the user's authorization and destination policy.

For an experiment, hold the stated conditions fixed unless changing them is
part of the authorized test. Report the hypothesis and observed result
separately; do not change the question after seeing the answer.

## Finish Honestly

Complete the requested coverage and required checks. Update work state when
reality changes. A prerequisite sub-plan preserves the parent contract; it does
not create new scope.

When blocked, state the exact unmet condition, what evidence establishes it,
and the next action needed. Preserve independent progress and report the
unverified layer. Do not turn persistence into a permission bypass or use
scope discipline to justify incomplete work.

For plan adaptation, use [sustained intent](sustained-intent.md).
For evidence selection, use [verification](verification-and-improvement.md).
