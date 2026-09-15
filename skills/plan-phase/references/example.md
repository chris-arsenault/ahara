# Examples and behavioral trials

These examples show different verification decisions within the same Sulion workflow. They
are illustrative contracts, not required architecture or extra project phases.

## Documentation-only milestone

M1 corrects an existing setup guide against the shipped configuration. One expansion step
covers `docs/setup.md` and the README's setup link.

- Outcome: instructions reflect supported settings and prerequisites.
- Change: correct stale settings, examples, and affected references.
- Verify: compare claims with configuration and installer sources, read the procedure end to
  end, resolve affected links, and run an existing documentation validator if applicable.
- Record: the sources reviewed, results, and any command that could not safely be exercised.

No new tests, deliberately failing baseline, application refactor, or documentation framework
is needed. Describing a deployment command does not authorize running it.

## Code fix with documentation

M2 fixes pagination that repeats the last row at a page boundary and updates the API example.
The cursor contract is settled; the repository already has pagination tests.

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
revised skills and realistic source artifacts. Preserve the two-stage handoff in the trial:
feature-start's persisted output is the input to plan-phase and its executor.

Give an evaluating model the user request, skill files, and raw task artifacts. Keep the
expected decisions below out of its task prompt. Use the models the workflow actually runs
on when available; report which models and scenarios were exercised. Do not claim a
cross-model result from static review or a single-model walkthrough.

| Scenario | What to inspect in the result |
| --- | --- |
| Documentation-only correction | Accurate instructions, existing validation used where helpful, no manufactured red test or new framework. |
| Code defect plus documentation | A meaningful regression exercises the actual defect; documentation is reviewed; unnecessary architecture is avoided. |
| Resume with completed work and a newly found helper | Correct Sulion attachment, dependency context read, valid prior work retained, justified plan adaptation persisted. |
| Deferred user decision | Decision owner and evidence trigger retained; independent work proceeds; dependent work waits. |
| Unrelated failing gate | Failure reported accurately; no unauthorized repair or false completion; any authorized prerequisite uses a nested branch. |

Compare outcomes, unnecessary artifacts, scope, useful verification, recovery, and completion.
Use tool traces and produced artifacts as evidence; do not score heading counts, exact wording,
or number of tests. Stop trials at their authorized local boundary and never mutate production
or publish results as part of a trial.

For small editorial changes, source and consistency review is enough. If behavioral execution
is unavailable, record a scenario walkthrough as such and leave model behavior unverified.
