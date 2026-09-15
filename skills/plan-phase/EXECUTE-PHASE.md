# Execute Phase

Use this prompt with the working plan path and selected milestone. It uses the installed
feature-start and plan-phase skills; no third skill is required.

---

Execute milestone <M#> in <plan-path> within the user's authorized scope.

Recover the current Sulion plan and expansion using the
[shared lifecycle](../feature-start/references/sequence.md). Read the milestone and its
persisted expansion, relevant decisions, predecessor evidence, and consumer contracts. Use
Sulion retrieval for missing history. Reconcile current sources and unfinished work before
editing. If the expansion is missing or stale, use plan-phase to prepare or refresh it first.

The [plan contract](../feature-start/references/plan-grammar.md) defines scope, decision
ownership, durable state, and adaptation. Preserve the agreed outcome, constraints, and
acceptance criteria. Change implementation details when current evidence justifies it:
reuse existing components, adjust files, combine steps, or reorder independent work. Record
material changes in the plan and reconcile the Sulion steps. Do not erase requirements or
expand authority. Stop dependent work at an unresolved user-owned decision; continue independent
authorized work when useful.

For each outcome, choose the useful baseline evidence, make the smallest complete change, and
verify it using [plan-phase's verification rules](SKILL.md#verification). A new test is not a
per-step requirement. Documentation gets source review; changed code behavior gets appropriate
behavioral checks; substantive prompt changes may need behavioral trials. Do not manufacture a
failing baseline or turn prose edits into wording tests.

Keep the plan document and Sulion statuses current as evidence becomes available. Capture
shared checks, failures, unverified claims, and the next action so another session can resume.
For a multi-step prerequisite, follow the nested-branch procedure in the shared lifecycle.
A branch tracks work; it does not authorize unrelated repairs or bypass a permission or
credential boundary. Diagnose failures from actual evidence before deciding what to repair.

Continue until the milestone's outcome and required verification are complete, not just its
first implementation. Run or reuse the applicable final checks, review the final diff against
the agreed scope, and record the results. If completion is blocked, leave an accurate blocked
state and report the exact missing decision, evidence, or access.

Finish the expansion, return to the parent, and reconcile milestone status using the lifecycle
procedure. Report the result, verification, material plan changes, and any remaining limitations.
Stop at the boundary of a single-phase request. If the user authorized the whole plan, expand
the next milestone just in time and continue; do not ask for routine reauthorization.
