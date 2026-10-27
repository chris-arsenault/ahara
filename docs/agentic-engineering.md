# Agentic Engineering Practice

Guidance for agents working in other repositories and client environments.
Apply the destination's instructions and the user's authorized scope. These
guides help choose an approach; they do not grant access or replace local rules.

Read the guide relevant to the current decision. Follow another link only when
that subject becomes necessary. The collection is not a startup reading list.

## Select by Task

| Current need | Guide |
| --- | --- |
| Choose the simplest complete design | [Design principles](coding-agents/design-principles.md) |
| Investigate, recommend, and collaborate with the user | [Collaboration and design](coding-agents/collaboration-and-design.md) |
| Preserve intent across phases, corrections, and interruptions | [Sustained intent](coding-agents/sustained-intent.md) |
| Use tooling around the session, especially Sulion plans | [Meta-harness and tooling](coding-agents/meta-harness.md) |
| Recover context and determine which source to trust | [Context and memory](coding-agents/context-and-memory.md) |
| Design documentation or tool responses for agents | [JIT documentation](coding-agents/jit-documentation.md) |
| Let agents work in domain concepts and artifacts | [Domain-native work surfaces](coding-agents/domain-native-work.md) |
| Guide work through several connected decisions | [Multi-step workflows](coding-agents/multi-step-workflows.md) |
| Assign responsibilities within an agent system | [Agent responsibilities](coding-agents/agent-responsibilities.md) |
| Structure code to prevent errors and bound context | [Architecture for agents](coding-agents/architecture-for-agents.md) |
| Design capabilities, permissions, and useful refusals | [Tooling and controls](coding-agents/tooling-and-controls.md) |
| Verify behavior or review substantive quality | [Verification and improvement](coding-agents/verification-and-improvement.md) |
| Interpret a task or formulate a bounded assignment | [Prompt patterns](coding-agents/prompt-patterns.md) |

## Use the Collection

Start from the requested outcome and current evidence. Preserve required
behavior while choosing the smallest maintainable mechanism. Keep requirements,
assumptions, and implementation choices distinguishable. Verify the result at
the layer where the user experiences it.

Tool-specific guidance is conditional on that tool being available. In
particular, Sulion commands describe a concrete implementation, not a dependency
every client must adopt.

The [original field report](working-with-coding-agents.md) is optional human
background. It is not required context for using these guides.
[Ahara integration](../INTEGRATION.md) concerns the owner's personal platform;
use it only for work on that platform. [Repository front door](../README.md).
