# Verification and Improvement

[Practice index](../agentic-engineering.md)

Name the claim, obtain evidence that can support it, and report its limits.
Separately judge whether the resulting artifact serves its intended user.
Correct mechanics and substantive quality need different kinds of attention.

## Match Evidence to the Claim

| Claim | Useful evidence |
| --- | --- |
| Local behavior is correct | Focused behavioral or contract test |
| Components integrate | The repository's relevant integration checks |
| A release operation ran | Actual CI or deployment logs |
| Deployed state matches intent | Observed configuration or runtime state |
| A user can complete the task | The actual user-visible path |
| Performance improved | Representative end-to-end workload with comparable conditions |
| A document or design is sound | Source review, consistency, and relevant domain judgment |
| An agent workflow helps | Representative work showing useful decisions and artifacts across revisions |

These rows do not substitute for one another. Local test success does not
establish deployment, and a successful deployment does not establish usability.
If failure logs are unavailable, the cause remains unverified.

Measure the user's actual workload. Distinguish local gains from the reported
problem, preserve relevant conditions, and identify remaining bottlenecks.
Report variability and missed goals. Do not change thresholds or impose new
runtime restrictions merely to make an acceptance number pass.

## Use Proportionate Verification

Protect stable contracts, material invariants, and regressions. Prefer a focused
regression test that can detect the bug when behavior changes. Existing passing
coverage may suffice for a refactor. Review documentation against its sources
and use relevant validators; do not manufacture failing tests for prose.

Tests that mirror implementation details can change with the code while
protecting nothing independent. Select evidence that could reveal a plausible
wrong implementation, including an omitted consumer or a substituted outcome.

Run the required checks for the final state. Repeat or broaden them when a
change, failure, or unresolved concern justifies it. If observability is missing,
add or propose the smallest signal needed to distinguish the hypotheses within
the authorized scope.

## Review for Improvement Across Dimensions

A defect review asks what is wrong. An improvement review also asks what would
make the work substantially better. Use the requested review mode and quality
bar; do not treat the absence of hard errors as a favorable quality judgment.

Identify the dimension that dominated drafting, then examine the other relevant
dimensions. Correctness can coexist with poor usability, a supported argument
with weak structure, or valid music with little direction. Choose lenses from
the artifact's purpose rather than imposing the same checklist everywhere.

Trace feedback to its structural cause. A local patch is appropriate when the
cause is local; otherwise revise the owning structure and inspect its effects
across the whole artifact. During a read-only review, propose that revision
without silently applying it.

When improvement is authorized, make a reasoned change and reassess the result.
Carry useful findings into subsequent work. Avoid mandatory finding counts,
word counts, or revision quotas that encourage manufactured criticism.
Further changes need a substantive reason tied to the requested quality bar;
review is not an instruction to churn indefinitely.

## Evaluate the Working Arrangement

For expert-directed work, evaluate creation, interruption, revision, and
redirection as well as the initial output. Determine whether earlier judgment
remains available and whether later work improves on it.

Cycle time, rework, escaped defects, decision quality, and operational outcomes
can inform evaluation. Token use, tool-call counts, and completed stages
describe activity; they are not substitutes for the result.

## Repair the Source of Recurring Failure

Choose the owning improvement: clearer instructions for judgment, better
navigation for missing context, a domain operation for incoherent edits, a
type or permission for invalid actions, or a test for observable regressions.

Keep the response cheaper and clearer than the recurring failure. Report what
changed, the evidence obtained, and what remains unresolved. Use
[multi-step workflows](multi-step-workflows.md) when findings must guide later
steps, and [meta-harness](meta-harness.md) when the gap spans sessions.
