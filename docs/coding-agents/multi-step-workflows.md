# Multi-Step Workflows

[Practice index](../agentic-engineering.md)

Guide connected domain decisions while preserving the developing work.
The application supplies state, relevant evidence, and supported actions.
The agent and expert supply judgment and can revise the direction.

## Choose the Right Form

A skill can describe a procedure. A plan can coordinate an assignment.
Application-owned workflow state is useful when domain objects must stay
coherent across steps, sessions, or collaborators.

Start with the artifact and the decisions needed to produce it. Group work
by coherent judgment rather than a fixed number of questions. A single step
can be small; a stage can combine related questions without dropping coverage.

Use a saved workflow only when continuity or coordinated writes require it.
Several steps alone do not require a new service.

## Make Each Step Usable

A step should expose its identity and scope, current question or decision,
relevant source content or retrievable references, supported response shape,
and next action. Read the needed bodies before answering.

The ordinary loop is: read current state and evidence, develop the answer,
submit it with explicit revisions, inspect the saved result, and continue.
Let a later session recover that loop from the artifact and run state without
replaying the whole conversation.

## Make Recorded Judgment Affect Later Work

Retain consequential observations, reasons, uncertainties, and proposed
improvements with the content they concern. Surface unresolved items in later
steps where they matter. Reconsider dependent conclusions when their evidence
changes.

Resolve an item through a supported revision, an explained rejection, or an
explicit decision to carry it forward. Merely collecting notes in a log does
not preserve useful understanding if subsequent work never encounters them.

Avoid making filled fields, minimum note lengths, finding counts, or progress
counters stand in for judgment. Structural checks can establish required
coverage; they cannot score the quality of an argument or artifact.

## Separate Assessment From Revision

A review records a finding. An edit changes authored content. Preserve that
distinction even when both are submitted together, and show which content
actually changed.

Support revision of earlier answers when later work exposes a contradiction.
Check the assembled artifact after related edits. Finishing a sequence is not
evidence that its parts form a coherent whole.

When user instructions limit a review, retain the limitation and its reason.
Required structural checks and access controls remain independently governed;
filtering suggested reading does not change permission to access sources.

## Keep State and Writes Coherent

Retain the selected artifact and revision throughout a multi-call operation.
A moving default such as the latest edition can redirect later calls.

For shared writers, validate the revision being changed. For retryable writes,
use request identity that prevents duplicate effects. Coordinate artifact and
workflow updates when they must succeed together. Define how direct edits
interact with an open workflow so progress cannot silently overwrite them.

Choose durability, interruption recovery, and extensibility separately.
A local single-user task may need less machinery than a shared service.
Preserve the guarantees the actual work requires.

## Complete the Work, Not Just the Sequence

Read the result as its intended user. Check its claims and relationships,
inspect improvements prompted by review, and report remaining uncertainty.
Keep finished artifacts usable independently of the conversation.

For content-centered operations, use [domain-native work surfaces](domain-native-work.md).
For substantive quality, use [verification and improvement](verification-and-improvement.md).
