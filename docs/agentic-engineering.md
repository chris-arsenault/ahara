# Agentic Engineering Practice

[Repository front door](../README.md)

This is Chris Arsenault's collection of practices and thought pieces about
building software and domain tools with agents. It starts with hands-on work:
how to delegate technical judgment, arrange information, enforce boundaries,
and decide whether the result works. These ideas are intended for use in other
organizations, including my work across client environments.

The [field report](working-with-coding-agents.md) explains the working stance:
set outcomes and constraints, let the model investigate and recommend the
mechanism, and require evidence at the layer where the claim exists. The
guides below turn parts of that stance into practices a team can apply.

## Choose a Starting Point

| What you need | Read |
| --- | --- |
| Understand the overall approach | [What has worked for me](working-with-coding-agents.md) |
| Give an agent useful context without a giant startup prompt | [JIT documentation](coding-agents/jit-documentation.md), then [context and memory](coding-agents/context-and-memory.md) |
| Build a tool that guides an agent through substantive domain work | [Multi-step workflows](coding-agents/multi-step-workflows.md), then [agent responsibilities](coding-agents/agent-responsibilities.md) |
| Decide which part of an agent system should own a behavior | [Agent responsibilities](coding-agents/agent-responsibilities.md), then [architecture for agents](coding-agents/architecture-for-agents.md) |
| Improve an existing coding workflow | [Collaboration and design](coding-agents/collaboration-and-design.md), [tooling and controls](coding-agents/tooling-and-controls.md), and [verification](coding-agents/verification-and-improvement.md) |

## Guides and Thought Pieces

| Guide | What it develops |
| --- | --- |
| [Design principles](coding-agents/design-principles.md) | The recurring errors behind the architectural rules I give agents |
| [Design as a conversation between peers](coding-agents/collaboration-and-design.md) | Delegating investigation and mechanism while retaining product judgment |
| [Context engineering as information architecture](coding-agents/context-and-memory.md) | Source authority, documentation lifecycles, retrieval, and memory |
| [Just-in-time documentation for agents](coding-agents/jit-documentation.md) | Small entry points, task-specific discovery, substantive reads, and useful errors |
| [Multi-step workflows that carry their own context](coding-agents/multi-step-workflows.md) | Guided questions, shared progress, explicit revisions, and resumable domain work |
| [Separating responsibilities in agent systems](coding-agents/agent-responsibilities.md) | Interfaces, execution, resources, inference, domain systems, and agent working modes |
| [Architecture that helps agents stay correct](coding-agents/architecture-for-agents.md) | Ownership, bounded context, canonical paths, and enforceable contracts |
| [Tooling, capabilities, and external work state](coding-agents/tooling-and-controls.md) | Instructions, permissions, credentials, plans, and actionable failures |
| [Verification and harness improvement](coding-agents/verification-and-improvement.md) | Matching evidence to claims and improving the environment after recurring failures |
| [Reusable prompt patterns](coding-agents/prompt-patterns.md) | Adaptable ways to express intent, scope, delegated judgment, and completion |

## How the Examples Fit

The examples supply concrete mechanisms. They do not establish that every
team should adopt the same tools or that the approach has measured benefits
in every setting.

| Example | Contribution to the practice |
| --- | --- |
| Ahara | A personal platform that puts delivery rules and engineering controls outside individual prompts |
| Sulion | Tooling for retrieving prior work, navigating source, brokering credentials, and retaining plan state |
| Bidcraft, maintained in `opm-clarity` | A domain application whose shared model, targeted guidance, and guided authoring are reachable through CLI, MCP, and a review UI |
| Hephaestus | A proposed design separating developer-owned implementation, interactive project collaboration, and bounded background specialists |

The Bidcraft and Hephaestus guides explain the relevant mechanisms here and
give source locations for readers with repository access. Client proposal
content and access to those systems are unnecessary to follow the examples.

## Adapting the Practice

Start with one real piece of work. Name its outcome, the source that owns its
data, the judgment delegated to the agent, and the actions the environment
permits. Apply the relevant guide using the project's existing tools. Inspect
whether another session or colleague can understand the result and continue
the work without reconstructing the conversation.

Keep the distinction between principles and local implementations explicit:

| Reusable idea | Adaptation in another environment |
| --- | --- |
| Give documentation an index and clear ownership | Use the destination repository's documentation conventions; [repo-docs](../skills/repo-docs/SKILL.md) is one concrete implementation |
| Expand substantial work just in time | Retain outcomes, boundaries, and current phase in the team's existing planning system |
| Retrieve prior decisions with their basis | Use authorized history and source search, with visible provenance and freshness |
| Enforce consequential boundaries in software | Use the destination's identity, permissions, types, checks, and delivery controls |
| Keep domain work coherent across interfaces | Put domain rules and canonical state behind the interfaces that need them |

The checked-in [feature-start](../skills/feature-start/SKILL.md) and
[plan-phase](../skills/plan-phase/SKILL.md) skills are concrete Sulion workflows;
their command requirements need adaptation elsewhere. Reading this collection
does not install those skills or replace a project's own instructions.

Ahara's [integration guide](../INTEGRATION.md) documents my private platform.
Reuse the engineering ideas with your own infrastructure and authorization.
Where a local example depends on a particular tool, preserve the purpose and
choose the smallest existing mechanism that serves it.
