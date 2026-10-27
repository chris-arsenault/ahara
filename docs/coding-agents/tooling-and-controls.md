# Tooling and Controls

[Practice index](../agentic-engineering.md)

Use instructions for judgment and software for enforceable boundaries.
Capabilities should let an agent complete authorized work without asking the
user to translate routine actions or relying on perfect obedience for safety.

## Assign the Rule to Its Owner

| Concern | Owning mechanism |
| --- | --- |
| Interpreting intent, choosing an approach, asking a consequential question | Agent instructions and judgment |
| Permission to access a resource or perform an action | Identity and runtime authorization |
| Valid inputs and state transitions | Types, schemas, and domain operations |
| Allowed dependency direction or API path | Build rules, analyzers, or lint |
| Resumable work and visible progress | Published plans and domain work state |
| Evidence that a result works | Tests, observations, and review at the relevant layer |

Make unfamiliar tools discoverable in the entry instructions: name the tool,
when to use it, and how to get help. Keep its detailed contract with the tool.
Where instructions are installed in several clients, maintain one owning
source and check installed copies for drift.

## Grant Narrow Capabilities

Prefer an operation that expresses the authorized work over unrestricted
access to its underlying storage, shell, or host. Match files, commands,
network access, credentials, and identity to the assignment.

Use the prescribed credential path from the first attempt. A missing, denied,
expired, or invalid credential is a boundary: report the attempted path and
the exact failure without exposing the secret. Do not search for another
token, assume a broader role, or change permissions to get around it.

When a broker grants command-scoped credentials, consume them only through
that mechanism. Other environments may use ordinary environment variables or
workload identity; follow their established contract.

Describe protection accurately. Restricting credential injection to one child
process does not necessarily isolate hostile same-user processes. A container
with direct host control has different authority from a restricted command
broker. Instructions cannot erase that difference.

## Make Failure Useful

A refusal should identify the failed rule, its relevant cause, and the
supported next action. Provide an exception path only when the owning policy
actually defines one.

Keep authorization refusals distinct from retryable failures. A version conflict
may require a fresh read; a denied credential requires the authorized access
path to be resolved. A generic retry loop must not blur those boundaries.

Match severity to the property. Enforce security and required architectural
invariants. Treat an uncertain maintainability signal as advice until evidence
or policy warrants a hard gate.

## Keep Controls Proportionate

Add a permanent control for a concrete recurring failure or required guarantee.
Fix incorrect use of an existing platform mechanism before inventing another.
A control should reduce the failure and its operational cost without obscuring
normal behavior.

Use published plans for intent and progress; keep business data in its owning
domain system. For the surrounding environment and Sulion usage, read
[meta-harness and tooling](meta-harness.md).
