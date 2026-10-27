# Just-in-Time Documentation for Agents

[Practice index](../agentic-engineering.md) · [Field report](../working-with-coding-agents.md)

Just-in-time (JIT) documentation delivers the relevant instructions and source
material when the agent reaches the work that needs them. An entry point tells
the agent where to start; discovery narrows the task; a substantive read
supplies the evidence; an operation explains how to act on it.

This is an information-design practice. A Markdown index and a few focused
documents can implement it. A domain application can go further by returning
guidance alongside current state and the next available action.

## Give Each Layer a Job

| Layer | What belongs there | When it enters context |
| --- | --- | --- |
| Entry instructions | Purpose, authority boundaries, canonical sources, and how to discover more | At orientation |
| Task index or discovery tool | Available activities, objects, identifiers, and the route for the current task | When choosing work |
| Focused guide | The relevant procedure, domain concepts, and a small example | When beginning that activity |
| Source read | Actual prose, code, evidence, or current object state | Before making a claim or change |
| Operation contract | Accepted inputs, effects, version requirements, and failure behavior | Before performing the operation |
| Result or refusal | What changed or failed, the basis for that result, and a useful next action | After the operation |

Keep the load-bearing boundaries at the entry point. Defer the detailed
operating manual. Guidance about authority must still be available before
the agent exercises that authority.

An index entry is a routing aid. A document title, search snippet, schema, or
status flag does not substitute for reading the body. A returned reference
shows that a source was offered, not that it was read.

## A Concrete Discovery Path in Bidcraft

Bidcraft is the proposal-authoring application maintained in `opm-clarity`.
Its MCP interface illustrates this layering:

1. `workspace_quickstart` returns selected proposal and edition IDs, current
   work state, and a small set of task routes.
2. `categories_describe`, `workflows_list`, or `operations_describe` exposes
   the part of the application needed for the chosen task.
3. `content_read` returns authored content. `sources_list` and `sources_read`
   discover and read the supporting material; a section read stays within the
   selected heading and its subsections.
4. An edit-target read with `include_metadata:true` supplies the versions and
   typed references needed for a write. Ordinary reading returns readable
   content without requiring the full technical envelope.
5. A guided step returns its immediate references, current question or stage,
   and the fields needed to answer. A partial source read provides a
   continuation call.

The starting guide supplies navigation and procedural instructions. The
proposal strategy comes from reading the selected evidence and doing the
domain work. Listing every tool and preloading every guidance document would
obscure that sequence.

This also makes the interface usable from a client that cannot see the
repository. A remote agent needs retrievable source identifiers and readable
content; a path on the server's filesystem alone cannot supply either.

## Put Guidance Beside the Decision

A useful response answers the agent's immediate questions: what am I working
on, what must I understand, what can I do next, and what will that action
change? For example, an illustrative drafting step might return:

```text
Current task: explain the buyer's benefit.
Read: the selected requirement and the saved approach.
Question: who benefits, and what changes in their work?
Return: an answer for the benefit field using the current run version.
Revision: update the earlier approach explicitly if this answer changes it.
```

This response leaves the argument to the agent and domain expert. The
application supplies the current state and the means to work on it.

Errors can carry documentation too. A version conflict should identify the
conflict and direct a fresh read. An unknown reference should explain how to
discover valid references. An authorization refusal should identify the
boundary. Recovery instructions must respect that boundary.

## Preserve Source and Meaning

Documentation, retrieved evidence, and instructions have different authority.
Identify the source and scope of returned material. Treat a customer document
as evidence about the task; it does not acquire authority to change tool rules
or permissions because it appears in context.

Keep operating contracts with the implementation that owns them. Where a tool
already has a schema, help text should use that schema or be checked against
it. A skill can teach how to use the tool without maintaining a second,
divergent specification of its inputs.

Bounded output must make omissions visible. Return a continuation or narrower
query when content is partial. Keep definitions, qualifications, and source
relationships that affect meaning; a short response that hides them is poor
context. The right working set is the smallest one that supports the decision.

## Apply It in an Existing Repository

Choose one task an agent repeatedly gets wrong or struggles to discover.
Give it a route from the repository index to the owning guide and source.
Move detailed instructions to that guide, keep essential boundaries at entry,
and make the first read and next action explicit. Add runtime discovery only
when the needed information depends on live objects or state.

Try the route from a fresh session. Check whether the agent can find the task,
read the relevant body, choose the supported action, and recognize an
incomplete result. If it fails, fix the missing route, ambiguous contract, or
misleading response. Loading the whole repository is rarely a useful repair.

The [context and memory guide](context-and-memory.md) covers source authority
and information lifecycles. [Multi-step workflows](multi-step-workflows.md)
extends this discovery pattern into work that spans several decisions.

## Source Example

In the Bidcraft repository (`opm-clarity`), the maintained entry points are
`tools/bidcraft-service/README.md` and
`bidcraft/lib/bidcraft/editorial/agent_guide.md`. The guided CLI's
`bidcraft/lib/bidcraft/guide/prompt.rb` assembles each question with its
references and continuation commands. These are implementation examples;
their tool names are specific to Bidcraft.
