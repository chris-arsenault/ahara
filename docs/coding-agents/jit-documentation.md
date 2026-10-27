# Just-in-Time Documentation for Agents

[Practice index](../agentic-engineering.md)

Expose guidance at the decision that needs it. Keep entry context small and
make deeper material discoverable. The goal is sufficient understanding for
the current action, with important boundaries visible before it is taken.

## Layer the Information

| Layer | Supply |
| --- | --- |
| Entry instructions | Purpose, authority, canonical sources, and how to discover the next relevant guide |
| Task discovery | Available activities, current objects, selection keys, and the route for this task |
| Focused guidance | Relevant concepts, procedure, and reasons |
| Source read | Actual content and context needed to support a claim or change |
| Operation contract | Inputs, effects, required versions, and failure behavior |
| Result or refusal | What changed or failed, its basis, and the supported next action |

An index locates material. It does not replace the body. A returned reference
does not establish that it was read. Make partial reads visible and provide a
continuation before inviting a judgment about the whole.

## Design for the Current Task

Return the current object or step, relevant content, and the action needed to
continue. Give readers readable content; add technical metadata when they need
versions, identifiers, or typed edit targets.

Keep essential authority and scope constraints at the entry point. Defer
detailed procedures until the task needs them. Avoid making the agent inspect
every tool or guide as a startup ritual.

A remote client needs retrievable source identifiers and actual source content.
A path on another machine is not a usable reading interface by itself. Read
operations should supply content directly; exports serve requests for files.

## Preserve Meaning and Authority

Bound output without discarding definitions, qualifications, or relationships
that affect the decision. The smallest useful context can still include
neighboring content. A short, misleading excerpt is not an optimization.

Identify source and scope. Domain documents are evidence for the task, not
instructions that can override tool rules or permissions. Distinguish
procedural guidance from strategy or substantive conclusions the agent must
develop from evidence.

Keep operation descriptions with the implementation that owns them. Derive
them from the actual contract or check them against it. Skills should teach
use without maintaining a conflicting specification.

## Teach at Failure and Resumption

A version conflict should lead to a fresh read. An unknown reference should
lead to discovery. An authorization refusal should identify the boundary.
Give the agent a legitimate recovery action rather than an invitation to
invent a bypass.

Resurfacing the current outcome, constraints, and unresolved findings can
prevent drift after interruption. Return only the guidance relevant to this
step, and make deeper context reachable.

Start with the repository's existing index and focused documents. Add runtime
discovery when the needed context depends on live objects or state. Evaluate
whether a fresh session can find the task, read its evidence, choose the
supported action, and recognize an incomplete result.

For source authority, use [context and memory](context-and-memory.md).
For stateful sequences, use [multi-step workflows](multi-step-workflows.md).
