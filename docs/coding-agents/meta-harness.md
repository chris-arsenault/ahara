# Meta-Harness and Tooling Around the Agent

[Practice index](../agentic-engineering.md)

A meta-harness is the environment around individual agent sessions: tools for
recovering context, retaining work state, supervising activity, and accessing
capabilities. Its value is continuity and dependable action across sessions,
with less context reconstruction and clearer human supervision.

These responsibilities can be served by independent tools. Use the environment
already available and add capabilities only for demonstrated gaps.

## Externalize What a Session Should Not Reconstruct

| Responsibility | Value to the work |
| --- | --- |
| Durable history and targeted retrieval | Recover an earlier request or decision with its source instead of asking the user to repeat it |
| Structural source navigation | Find the owning implementation and consumers with visible freshness and confidence |
| Shared work state | Let people and later sessions see intent, progress, blockers, and the next action |
| Capability and credential controls | Execute authorized operations without copying secrets or inventing alternate access paths |
| Activity and review surfaces | Let the user inspect and redirect work without following every tool call |
| Persistent execution environments | Preserve running work where supported; distinguish terminal survival from recoverable task state |

These responsibilities complement the agent's own reasoning and the domain
application's authoritative data. Avoid duplicating either in a second control
system. Discover tool capabilities through current help; their names and
availability vary by environment.

## Make Plans Shared and Durable

A shared plan preserves the work's intent beyond one conversation. Keep one
discoverable record of the outcome, sourced boundaries, principles, assumptions,
phases, and current state. A maintained document or task record can be enough;
choose storage and tooling according to collaboration and recovery needs.

Separate user requirements and corrections from agent proposals. Preserve their
sources and reasons so a later session can reassess an implementation choice
without mistaking it for an agreed constraint. Keep enough revision history to
understand consequential changes in direction.

Expand the next phase when its evidence is current. Keep distant phases at the
level of outcomes and dependencies. Follow the project's planning threshold;
the availability of planning tools does not make every task a substantial plan.

## Bring Boundaries Back Into Active Work

Storing a constraint does not ensure that the next session will encounter it.
Make the outcome and applicable boundaries visible when work starts, resumes,
changes phase, or receives a correction. Tool responses can supply this context;
otherwise, retrieve the current guidance at those transitions. Keep reminders
focused and link to the source when deeper context matters.

For a prerequisite that needs its own plan, retain the parent relationship,
the blocked work, and the parent's current boundaries. Local guidance adds
detail within that scope. Return to the parent when the prerequisite is
resolved and reassess the next action against the original outcome.

Apply the guidance to the next decision. Displayed reminders and source labels
support judgment; they do not enforce boundaries or establish that an attribution
is accurate. When corrected, update affected steps while retaining requirements
that still apply.

## Make Resumption and Progress Honest

Find the existing plan before creating another account of the same work. On
resume, reconcile its state with the current artifact and evidence. Preserve
blockers, unresolved decisions, and a useful next action so continuation does
not depend on replaying the conversation. Verify that state updates took effect.

Keep task progress separate from session activity. Running, waiting for input,
and disconnected describe execution; pending, blocked, and complete describe
work. Neither a live process nor a completed checklist establishes the outcome.
Close work against evidence and retain unresolved obligations explicitly.

## Connect Tools Without Loading Their Manuals

Discover the available retrieval, source navigation, execution, and access
mechanisms when the task needs them. Read their current contracts. Recover user
intent from user-authored sources, inspect retrieval coverage and freshness
when results are uncertain, and respect credential refusals.

Keep entry instructions small: capability, purpose, and route to focused help.
Maintain operational details with the tool that owns them. Improve a missing
capability when recurring friction or a required guarantee demonstrates the
need, using the smallest mechanism that satisfies it.

Evaluate the meta-harness by whether work resumes correctly, corrections remain
effective, evidence is recoverable, and the user can supervise consequential
decisions. Activity counts, token usage, and completed phase counts are useful
observations; they do not establish product quality.

For the judgment behind plan changes, use [sustained intent](sustained-intent.md).
For enforced authority, use [tooling and controls](tooling-and-controls.md).
