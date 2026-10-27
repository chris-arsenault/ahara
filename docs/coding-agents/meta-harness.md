# Meta-Harness and Tooling Around the Agent

[Practice index](../agentic-engineering.md)

A meta-harness is the environment around individual agent sessions: tools for
recovering context, retaining work state, supervising activity, and accessing
capabilities. Its value is continuity and dependable action across sessions,
not a larger prompt or another model deciding everything.

Use the environment already available. Sulion is a concrete implementation;
the responsibilities also apply to other clients and toolsets.

## Externalize What a Session Should Not Reconstruct

| Responsibility | Value to the work |
| --- | --- |
| Durable history and targeted retrieval | Recover an earlier request or decision with its source instead of asking the user to repeat it |
| Structural source navigation | Find the owning implementation and consumers with visible freshness and confidence |
| Published work state | Let people and later sessions see intent, progress, blockers, and the next action |
| Capability and credential controls | Execute authorized operations without copying secrets or inventing alternate access paths |
| Activity and review surfaces | Let the user inspect and redirect work without following every tool call |
| Persistent execution environments | Preserve running work where supported; distinguish terminal survival from recoverable task state |

These responsibilities complement the agent's own reasoning and the domain
application's authoritative data. Avoid duplicating either in a second control
system. Discover tool capabilities through current help; their names and
availability vary by environment.

## Why Published Plans Matter

A private task list helps the current agent. A published plan makes the work
legible outside that conversation. Sulion plans are durable, repository-scoped
phase summaries that survive terminal exit and can be attached to other
sessions. They are a compact shared account of the work, not a transcript of
reasoning or proof of completion.

The useful content is the outcome, sourced boundaries, principles, assumptions,
and honest phase state. Expand the next phase when its evidence is current.
Avoid detailed speculative steps for distant phases.

Sulion returns the applicable outcome and boundaries with every plan command.
This restores important context during ordinary progress updates instead of
depending on the agent to remember an earlier instruction. Branch plans retain
live ancestor guidance, so a prerequisite cannot quietly escape the parent
scope. History preserves changes to guidance and progress.

Read and apply these reminders. Displaying a boundary does not enforce it.
Source labels distinguish user requirements, corrections, and agent proposals;
the service does not certify that the attribution is true.

## Use Sulion Plans When Available

Read `sulion plan help` before the first plan command in a session. Follow the
repository's planning threshold; simple tasks do not need an elaborate feature
plan merely because the tool exists.

| Situation | Action |
| --- | --- |
| Start or resume work | Read `sulion plan current`; if unattached, inspect `sulion plan list --all` and `attach` the relevant plan before creating a duplicate |
| New substantial work | Use `start` with an outcome, sourced boundaries, and coherent phases |
| Evidence or direction changes | Update guidance and affected phases; retain still-applicable boundaries |
| Phase progresses | Use `phase set` with the actual status and a useful note |
| A multi-step prerequisite blocks a phase | Mark it blocked, `branch` from that phase, resolve the authorized work, then `return --completed` |
| Need to recover context | Use `current` for full guidance, `tree` for ancestry, and `history` for changes |
| Outcome is established | Use `close --completed` after required work and evidence are complete |

Guidance updates replace supplied lists. When adding a correction, retain
existing applicable entries. Read `current` at phase start, after interruption,
and when evidence challenges the approach. Verify that the command succeeded;
an attempted status change is not the resulting state.

Published phase status and current activity answer different questions.
`sulion name` identifies the task; `sulion activity` communicates that the
session is working, blocked, or needs input. A busy terminal can still be
working on a blocked prerequisite; a quiet terminal can have unfinished work.

## Connect Tools Without Loading Their Manuals

In Sulion, `sulion-retrieve` recovers history, `sulion-code` navigates source,
and `with-cred --` supplies granted credentials to a command. Read each tool's
help when needed. Include user messages when recovering user intent, inspect
index freshness when results are uncertain, and respect credential refusals.

In another environment, map these responsibilities to its existing tools.
Do not introduce a platform migration merely to follow this guide. Improve a
missing capability only when a recurring failure demonstrates the need.

Evaluate the meta-harness by whether work resumes correctly, corrections remain
effective, evidence is recoverable, and the user can supervise consequential
decisions. Activity counts, token usage, and completed phase counts are useful
observations; they do not establish product quality.

For the judgment behind plan changes, use [sustained intent](sustained-intent.md).
For enforced authority, use [tooling and controls](tooling-and-controls.md).
