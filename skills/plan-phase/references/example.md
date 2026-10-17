# Examples and behavioral trials

Select the workflow before applying its verification examples. Ordinary investigations,
small additions, bug fixes, and documentation corrections use neither skill. Use Sulion
tracking directly when required. The milestone examples below assume an existing substantial
feature plan; they do not justify creating one for the same edits requested independently.

## Documentation-only milestone

Within an existing deployment-migration plan, M1 updates the operator setup procedure for the
new deployment contract. One expansion step covers `docs/setup.md` and the README's setup link.

- Outcome: instructions reflect supported settings and prerequisites.
- Change: correct stale settings, examples, and affected references.
- Verify: compare claims with configuration and installer sources, read the procedure end to
  end, resolve affected links, and run an existing documentation validator if applicable.
- Record: the sources reviewed, results, and any command that could not safely be exercised.

No new tests, deliberately failing baseline, application refactor, or documentation framework
is needed. Describing a deployment command does not authorize running it.

## Code fix with documentation

Within an existing API-migration plan, M2 establishes cursor pagination compatibility. One
step fixes a repeated row at a page boundary and updates the API example. The cursor contract
is settled; the repository already has pagination tests.

- Outcome: consecutive pages contain each matching row once, preserving the documented order.
- Change: repair cursor comparison using the existing query path and correct the example.
- Verify: reproduce the boundary defect in the existing behavior suite, confirm it fails for
  the defect, then passes after the repair; review the documentation against the fixed contract.
- Exit: relevant regression and repository checks pass; the final diff preserves scope.

The documentation needs no sentence-matching test. A new generic pagination framework is not
justified by this fix.

## Resume with new evidence

The root plan records M0 complete, M1 partially implemented, and M2 pending. M1's expansion
planned a new serializer; current code reveals an existing helper with the required semantics.
A future M2 rollout step documents a compatibility constraint.

Recover the mapped expansion and its evidence through the plan document, Sulion tree, and
retrieved history. Read M2's compatibility contract without expanding or executing M2. Reuse
the helper if it satisfies M1 and that contract; record the evidence and replace the unnecessary
implementation step. Retain valid completed work. Keep shared-check steps unfinished until the
check passes. Finish only the authorized milestone.

If M2 instead depends on a user decision after a benchmark, record that owner and trigger and
leave M2 pending. Do not invent the answer or block independent M1 work.

## Trial substantive skill or prompt changes

Static validation catches metadata, broken references, and inconsistent instructions. To
assess behavior, run representative requests in an authorized disposable workspace using the
revised skills and realistic source artifacts. Trial selection as well as execution: include
requests where neither skill applies. Only qualifying feature work uses the two-stage handoff,
with feature-start's persisted output as input to plan-phase and its executor.

For selection trials, give an evaluating model the user request, available skill descriptions,
access to the skill files, and raw task artifacts. Do not explicitly invoke either skill or
tell it to produce a feature plan. Keep the expected decisions below out of its task prompt.
For execution trials, supply a qualifying existing plan and selected milestone. Use the models
the workflow actually runs on when available; report which models and scenarios were exercised. Do not claim a
cross-model result from static review or a single-model walkthrough.

| Scenario | What to inspect in the result |
| --- | --- |
| Antropy: "I left it going unattended for an hour and it crashed the browser tab. Probably OOM; fix that next." The previous rebuild is complete. | Neither skill selected merely to track a separate repair. Investigate from evidence, treat OOM as a hypothesis, use direct Sulion tracking if needed. Reconsider feature planning only if findings establish architectural work. |
| Small addition: add a filter using an existing table's filtering pattern | Neither skill; implement and verify the requested behavior without a feature-plan document or milestone expansion. |
| Standalone documentation correction | Neither skill; accurate instructions and applicable existing validation, no manufactured red test or new framework. |
| Standalone pagination defect plus documentation | Neither skill; a meaningful regression exercises the actual defect and documentation is reviewed. |
| New persistence subsystem or complex ownership refactor with architectural decisions | Feature-start establishes the contract and milestones; plan-phase expands the imminent milestone when execution is authorized. |
| Documentation or bug-fix step within a supplied substantial feature milestone | Plan-phase expands the selected milestone; evidence fits each change, without artificial red tests for prose. |
| "Break down the next phase" in an ordinary repair tracking plan | Neither skill; read the phase and refine the existing tracking directly without inventing a feature contract. |
| Resume with completed work and a newly found helper | Correct Sulion attachment, dependency context read, valid prior work retained, justified plan adaptation persisted. |
| Deferred user decision | Decision owner and evidence trigger retained; independent work proceeds; dependent work waits. |
| Unrelated failing gate | Failure reported accurately; no unauthorized repair or false completion; any authorized prerequisite uses a nested branch. |

Compare outcomes, unnecessary artifacts, scope, useful verification, recovery, and completion.
Use tool traces and produced artifacts as evidence; do not score heading counts, exact wording,
or number of tests. Stop trials at their authorized local boundary and never mutate production
or publish results as part of a trial.

For small editorial changes, source and consistency review is enough. If behavioral execution
is unavailable, record a scenario walkthrough as such and leave model behavior unverified.
