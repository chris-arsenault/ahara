# What Has Worked for Me When Building Software With Coding Agents

> Throughout this guide and its linked articles, “I,” “me,” and “my” refer to
> Chris Arsenault. Work performed while assembling or reviewing the guide is
> attributed to “the editorial agent.”

I get the best results from coding models when I stop treating them as code
generators. I treat them as temporary product managers, designers, architects,
engineers, and reviewers. I give them outcomes and constraints, require them to
study the real system, let them recommend the mechanism, and ask for evidence
that the result works.

This is a field report, not a neutral survey of AI development methods. I built
the workflow through sustained work on product software, infrastructure,
network appliances, simulations, and creative systems. Cognitive science and
the emerging agentic-engineering literature explain parts of it and suggest
failure modes worth testing. They do not define the method.

When published research disagrees with what I can repeatedly demonstrate in my
environment, I keep the practice and improve the measurement. The tools and
workflows are changing too quickly for an older average result to overrule
current direct evidence. That standard cuts both ways: feeling faster is not
evidence either.

People use “vibe coding” for several incompatible practices. Simon Willison
[distinguishes unreviewed vibe coding from accountable agentic engineering](https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering/).
This guide concerns the accountable end of that range. I still care how the
system works, even when a model writes every line.

## Guide

| Article | Question it answers |
| --- | --- |
| [Design as a Conversation Between Peers](coding-agents/collaboration-and-design.md) | How do I work with a model as a product and design peer without writing a complete specification first? |
| [Context Engineering as Information Architecture](coding-agents/context-and-memory.md) | How do documentation, retrieval, source navigation, and information lifecycles keep context useful? |
| [Architecture That Helps Agents Stay Correct](coding-agents/architecture-for-agents.md) | Which architecture and language choices reduce errors and keep work inside a bounded context? |
| [Tooling, Capabilities, and External Work State](coding-agents/tooling-and-controls.md) | How do agent rules, deterministic controls, secret brokering, and durable plans increase autonomy safely? |
| [Verification and Harness Improvement](coding-agents/verification-and-improvement.md) | How do I match evidence to claims and turn recurring failures into better infrastructure? |
| [Reusable Prompt Patterns](coding-agents/prompt-patterns.md) | Which material prompt structures recur in my work, and how can they be adapted without becoming rituals? |

## The Method in Brief

### Design Through Dialogue

I do not hand the model a complete product specification and ask it to fill in
code. I usually begin with a short, informal account of the outcome, current
pain, and a few constraints. The model studies the system, proposes a design,
and identifies the choices that would change its shape. We build shared
understanding through that exchange.

I expect the model to act as a peer: bring evidence, make recommendations,
question the premise when necessary, and say when the requested approach is
wrong. I retain product taste, consequential authority, and final acceptance.
The model owns most of the investigation and technical mechanism.

The prompts can stay quick because the permanent concerns do not live in each
prompt. Repository instructions, current-state documents, ADRs, plans, types,
linters, permissions, tests, and deployment controls preserve the context and
reject important violations. Familiarity with the model and the repository
lets the conversation move quickly without making safety depend on perfect
wording.

[Read the collaboration and design article.](coding-agents/collaboration-and-design.md)

### Engineer the Information Environment

Context engineering is information architecture. A repository should tell the
agent which source owns each kind of truth, where to begin, and how to retrieve
more detail only when needed. Current code and runtime evidence outrank stale
plans. ADRs preserve rationale. Backlogs describe intent. Transcript history
recovers prior decisions but does not prove current behavior.

I let agents search their own history so a new session can recover earlier work
without asking me to reconstruct it. Search results need source turns,
repository scope, index state, and a way to reopen the original context. Source
navigation needs the same honesty about confidence and fallback behavior.

[Sulion](https://github.com/chris-arsenault/sulion) is my reference
implementation for transcript retrieval and structural code navigation, but
the principle is tool-independent: agents should be able to find their prior
work and current source evidence through bounded, inspectable interfaces.

[Read the context and memory article.](coding-agents/context-and-memory.md)

### Architect for Error Prevention and Bounded Context

I choose architecture by the mistakes it can prevent and the amount of the
system an agent must understand at once. Clear ownership, small coherent
modules, pure decision cores, strict runtime forms, one canonical path for each
behavior, and narrow extension seams all reduce the cost of a wrong edit.

Language choice follows the same rule. I use Rust when ownership, exhaustive
state handling, and concurrency constraints should become ordinary compiler
feedback. I use other languages when their ecosystem and build controls better
fit the system. Programmer comfort and model generation speed are secondary to
the failures the toolchain can exclude.

Stable architectural properties belong in types, project references, custom
linters, analyzers, or permissions whenever possible. Tests protect observable
behavior and integration. Runtime evidence protects claims that exist only in
the deployed system.

[Read the architecture article.](coding-agents/architecture-for-agents.md)

### Put Judgment in Instructions and Guarantees in Software

Agent rules define modes, authority, research expectations, publication
boundaries, and the points where judgment must return to me. Deterministic
controls enforce the properties that cannot depend on interpretation.

Credential access illustrates the difference. A secret broker can limit a
credential to one granted command. The agent rule says that a denial is a hard
stop and prohibits searching for another token. The mechanism blocks ambient
access; the instruction keeps a capable operator from trying to bypass the
boundary.

Plans are another tool boundary. They externalize the outcome, decisions,
phases, exit gates, and unresolved choices. I expand the next phase just in
time, so work stays resumable without filling the plan with stale file-level
instructions.

[Sulion](https://github.com/chris-arsenault/sulion) is my reference
implementation for agent instructions, brokered credentials, and published
plan state. The linked article describes the general contracts before the
implementation.

[Read the tooling and controls article.](coding-agents/tooling-and-controls.md)

### Verify the Claim at the Layer Where It Exists

A unit test can support a local behavior claim. It cannot prove deployment. A
deployment log can show that the release mechanism ran. It cannot prove that a
user-visible path works. Performance claims need traces, profiles, benchmarks,
or runtime telemetry.

I require proportionate evidence and report what remains unverified. When the
same failure recurs, I improve the harness: clarify an instruction, restructure
documentation, add a type or linter, preserve a decision, improve a tool, or
add a test at the layer that can observe the contract.

[Read the verification and improvement article.](coding-agents/verification-and-improvement.md)

### Use Prompt Shapes, Not Magic Phrases

My recurring prompts specify a mode, outcome, evidence, constraints, delegated
judgment, persistence rule, and proof. Not every prompt names every field.
Durable repository context supplies the defaults.

The most useful families cover feature design, project resumption,
architecture review, evidence-first investigation, decision triage, one-phase
execution, full-plan execution, design reconciliation, and bounded operations.
“Do not pause until complete” works when complete and the legitimate stop
conditions are already defined. Without those boundaries, persistence becomes
permission to wander.

[Read the prompt-pattern article.](coding-agents/prompt-patterns.md)

## The Working Loop

For substantial work, this is the loop I return to:

1. Name the mode and authorization boundary.
2. State the outcome, constraints, and evidence of success.
3. Load the repository map, retrieve prior decisions, and check the retrieval
   or code index's freshness.
4. Survey the complete affected path before choosing a local mechanism.
5. Research uncertain parts and verify assumptions against current sources.
6. Let the model recommend a coherent design and ask only about choices that
   change its shape.
7. Record durable decisions in the information type that owns them.
8. Publish milestone state and expand the next phase just in time.
9. Implement within the smallest correct boundary and preserve adjacent
   ownership.
10. Encode stable constraints in the strongest deterministic layer available.
11. Verify each claim where it can actually be observed.
12. Report what remains unverified before publishing or handing off.
13. When a failure repeats, improve the harness that allowed it.
