# Sulion lifecycle and recovery

Both skills and the executor use this procedure. Sulion tracks progress; the linked working
plan document retains the detailed contract, expansions, decisions, and evidence. A status
label is not evidence that the underlying work is complete.

## Recover context and identity

Read `sulion plan help` before the first plan command in a session. Inspect:

```sh
sulion plan current
sulion plan tree
```

If no plan is attached, use `sulion plan list --all`, then `sulion plan show <plan-id>` to
inspect the relevant records before attaching with `sulion plan attach <plan-id>`. If a plan
is attached, read its body and the linked document before deciding it is the right one. Do not
replace, detach, close, or reopen another task's plan to make the current task fit.

Use retrieval before re-deriving prior decisions or asking the user to repeat context:

```sh
sulion-retrieve search "<decision or question>"
sulion-retrieve search "<remembered user wording>" --include user --mode lexical
sulion-retrieve turn <agent-session-id> <turn-id>
```

Read the returned turn or relevant file body; search snippets only locate evidence. For file
evolution, use `sulion-retrieve file-history <repo/path>`. Read `sulion-retrieve help` for
other queries and `facets` or `index-status` before concluding material is not indexed.
If a tool fails, distinguish missing context from a tool or credential failure; report the
actual boundary rather than inventing history or a replacement tracking system.

On resume, reconcile the document with current code, working-tree changes, prior evidence,
and the Sulion tree. Reuse completed work that is still valid. Recheck a claim when its sources
changed or its evidence is insufficient; do not rerun every completed step by default.

## Create or update the root

Reuse an existing plan when it represents this work. For new work, start tracking before
multi-phase edits. A planning phase may be active while future implementation milestones stay
pending; create the latter once their scope is known. A plan published only after design is
ready uses `--all-pending`:

```sh
sulion plan start "<Feature>" --summary "<intent>; details: <plan-path>" \
  --phase "M0 — <outcome>|<acceptance summary>" \
  --phase "M1 — <outcome>|<acceptance summary>" --all-pending
```

Read `sulion plan --json current` for the root and phase IDs and record them in the document.
Add or update phases as the design
settles; do not start a duplicate root. Keep titles recognizable and mappings explicit.
Use phase IDs for later operations when available. Numbered positions are acceptable only
after checking the current tree; document milestone M0 is not automatically CLI position 0.

## Expand one milestone

Read the milestone body, its decisions and evidence, and relevant dependencies. If a matching
expansion exists, inspect and reuse it. Otherwise attach the correct parent and branch:

```sh
sulion plan branch "<milestone> — execution" --from <milestone-phase-id> \
  --summary "Expansion in <plan-path>#<section>" \
  --phase "<step>|<outcome>" --phase "<step>|<outcome>" --all-pending
```

Read `sulion plan --json current` for the expansion and step IDs and save them with the
expansion in the working document before handing off. The document
contains the actual file/outcome/change/verify detail; the Sulion summary points to it.
Planning an expansion does not mark its steps as executing.

## Execute and handle blockers

Before each status mutation, ensure the attached plan is the intended expansion or prerequisite
branch. Mark work `in_progress` when it starts, and `completed` only after its outcome and
required evidence are established. If several steps share a later check, record what is
implemented and what remains unverified; keep completion pending until that evidence exists.

A prerequisite that is itself a multi-step job gets a nested branch, not hidden extra work:

```sh
sulion plan phase set <step-id> blocked --note "<verified blocker>"
sulion plan branch "<required prerequisite>" --from <step-id> \
  --summary "<authorized scope>; details: <plan-path>#<section>" \
  --phase "<diagnose>" --phase "<resolve>"
```

Branch only into repair work already authorized by the task. An unrelated regression, external
write, destructive action, or authority change may need the user's decision first. Tracking a
blocker grants no permission to fix it. A small authorized fix can remain in the current step;
size determines tracking, not authorization. Use `sulion activity` to expose blocked or
needs-input state, following its command help.

On completion of an authorized prerequisite, update its evidence in the document and use
`sulion plan return --completed`. Returning clears the parent's blocked state; it does not
prove the parent acceptance condition. Recheck the affected outcome and resume the parent.

## Finish or hand off

At a phase boundary, update the document's changes, evidence, unresolved items, and next action.
Complete the expansion's steps, then `sulion plan return --completed` to close that branch.
Inspect the parent and mark the milestone complete only when its acceptance condition is met.
Keep future milestones pending. Close the root with `sulion plan close --completed` only when
all required work is complete; do not hide missing evidence with `--skip-remaining`.

For interruption or missing authority, retain the accurate unfinished state and a resumable
next action. Honor the user's execution scope: stop after one phase when that is what they
authorized; if they authorized the whole plan, expand the next phase just in time and continue.
