# Domain-Native Work Surfaces

[Practice index](../agentic-engineering.md)

Let the agent work in the concepts, artifacts, and judgments of the task.
Use software to handle storage, syntax mechanics, and structural rules when
those would otherwise compete with attention to the domain.

## Choose a Meaningful Unit of Work

Define the object a practitioner reasons about and the relationships needed
to change it coherently. A passage, argument, feature, or decision may span
several underlying records. Support that coherent unit while retaining
precision for a small edit.

Do not merely rename a database operation. A domain operation should express
the intended change, enforce its invariants and authority, and explain the
result in the same vocabulary. The interface should let the agent develop and
revise substantive work without reconstructing the storage model.

## Make the Work Readable

| Surface | Required meaning |
| --- | --- |
| Orientation | Current artifact, selected scope, relevant decisions, unfinished work, and available activities |
| Read | Actual content and the neighboring context or relationships needed to judge it |
| Edit | A supported domain change with stable identity and a clear effect |
| Review | Findings tied to content, evidence, and revision |
| Projection or export | A derived view whose authority and omissions are explicit |

Separate reading from exporting. A list of titles or a technical envelope is
not a substitute for the content. Return metadata when an operation needs it,
without making every reader process the entire API record.

Preserve domain meaning alongside resolved output. Authored relationships,
intentional omissions, and unresolved work may matter to revision even when a
renderer or runtime does not need them. Distinguish unfinished content from
an intentional empty result.

## Maintain One Canonical Artifact

Choose the authoritative representation explicitly. CLI, UI, and agent tools
should read and change the same model through the owning rules. Generated
views help inspection; they do not silently become alternative edit sources.

An improved interface need not replace the underlying language or storage.
Hide incidental mechanics first. Change the canonical representation only
when the existing one cannot satisfy a concrete authoring or execution need.

Support coordinated revisions where related changes must stay coherent. Use
version checks, atomic updates, and retry identity when shared editing or
delivery requires them. Keep those mechanisms inside the owning application
rather than making the agent simulate transactions in prose.

## Preserve Developing Understanding

Keep claims connected to evidence, decisions connected to reasons, and open
questions visible. When evidence changes, identify the conclusions that need
another look. Do not silently rewrite accepted decisions or depend on replaying
the entire conversation to understand them.

Let experts direct, challenge, and redirect work throughout. A useful domain
environment provides dependable capabilities while leaving substantive judgment
open. Continuing expert participation is compatible with finished software.

## Judge the Result in the Domain

Evaluate creation, revision, and continuation of a substantial artifact.
Check whether the agent can preserve relationships and develop the work over
time, and whether a person can inspect and redirect it.

Valid syntax, export parity, and successful tool calls establish structural
properties. They do not establish musical, editorial, analytical, or product
quality. Evaluate that quality directly, and distinguish the rationale for an
interface from evidence that it improves outcomes.

For guided steps, use [multi-step workflows](multi-step-workflows.md).
For ownership of execution and state, use [agent responsibilities](agent-responsibilities.md).
