---
name: plan-phase
description: Expand or refresh one milestone of a Sulion feature plan into durable execution steps immediately before implementation. Use for requests such as "plan phase N" or "break down the next phase."
---

# Plan a Phase

Expand one milestone from feature-start. Save the expansion in the working plan document,
publish its Sulion branch, and hand it to [EXECUTE-PHASE.md](EXECUTE-PHASE.md). Do not expand
future milestones speculatively.

The maintained source is `~/repos/ahara/skills/`. Keep both complete skill directories
synchronized in `~/.claude/skills/`, `~/.codex/skills/`, and repository-vendored copies.

## Prepare the expansion

Use the shared [Sulion lifecycle](../feature-start/references/sequence.md) to recover the
correct plan, retrieve prior decisions, and reuse an existing expansion. Read the
[plan contract](../feature-start/references/plan-grammar.md) for the document fields and
adaptation rules.

Read the selected milestone, relevant decisions, predecessor results, and downstream consumer
contracts. Other phases are valid context; expanding or implementing them remains outside a
single-phase request. Verify current sources rather than assuming the old plan is still exact.

Decompose into coherent, reviewable outcomes. Keep implementation, wiring, documentation, and
verification together when they establish one outcome. Split for a real dependency, decision,
or review boundary. Preserve required architecture and durability; do not add abstractions or
test harnesses to fill template fields.

Resolve routine implementation choices from evidence. Carry unresolved user decisions to the
step they affect, with the evidence trigger and owner. Persist the steps and useful verification
in the existing plan document, then create or reconcile the matching Sulion expansion with
unstarted steps pending. Report the document section and expansion identity.

Planning alone ends here. If execution is already authorized, load the companion prompt and
continue within that authorization.

## Verification

This section governs verification for planning and execution. Match evidence to the claim,
risk, and actual consumer rather than to file extension or a per-step test requirement.

| Change | Useful evidence |
| --- | --- |
| Code behavior or bug fix | Prefer a focused regression test that fails for the relevant behavior before the fix and passes afterward. Reuse existing coverage when sufficient. |
| New code | Exercise its real contract and material failure cases. An initial missing symbol can explain a compile failure; the completed test must detect incorrect behavior. |
| Behavior-preserving refactor | Existing tests pass before and after. Add characterization coverage only for a material gap. |
| Documentation or plans | Review accuracy, completeness, examples, and affected links against their sources. Use applicable existing validators. No artificial red gate or tests that merely assert wording, headings, or file existence. |
| Skills or prompts | Check structure and consistency. For substantive behavioral changes, trial representative tasks on the models used when available and authorized; inspect their decisions and artifacts. A metadata validator does not establish agent behavior. |
| Configuration, schemas, executable examples, or generated output | Use checks for the actual consumer: validation, builds, behavior checks, or a safe dry run as appropriate. Add regression coverage for a meaningful contract. |

For mixed work, test changed behavior and review the prose. A filesystem or text assertion is
useful when it protects a real consumed contract, not merely because an instruction was edited.
Do not test a dummy substitute for production behavior or mirror implementation details.

Choose useful baseline checks before editing. Existing passing checks can protect behavior;
never deliberately break work to manufacture red. Shared verification is valid: identify the
steps it covers and do not mark them complete before the shared evidence exists. Replace an
older plan's inappropriate verification with proportionate evidence, recording the reason while
preserving acceptance criteria.

Run the phase exit checks after its work, including checks required by repository instructions.
Reuse an already-run check if it still covers the final state; repeat only after relevant
changes, failures, or unresolved concerns. Review the final diff and outcome for omitted
requirements or accidental scope. Record actual evidence and limitations, not just "green."

See [examples and behavioral trials](references/example.md) when choosing evidence for a
substantive workflow change. Trials should evaluate useful behavior, not exact prose.
