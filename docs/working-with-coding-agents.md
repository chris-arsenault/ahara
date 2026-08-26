# What Has Worked for Me When Building Software With Coding Agents

I get the best results from coding models when I treat them as temporary
product managers, designers, architects, engineers, and reviewers rather than
code generators. I give them outcomes and constraints, require them to study
the real system, let them recommend the mechanism, and ask for evidence that
the result works.

This is a field report. I built the workflow through sustained work on product
software, infrastructure, network appliances, simulations, and creative
systems. Cognitive science and the emerging agentic-engineering literature
explain parts of it and suggest failure modes worth testing, but the method
comes from the practice.

When published research disagrees with what I can repeatedly demonstrate in my
environment, I keep the practice and improve the measurement. The tools and
workflows are changing too quickly for an older average result to overrule
current direct evidence. That standard cuts both ways: feeling faster isn't
evidence either.

People use “vibe coding” for several incompatible practices. Simon Willison
[distinguishes unreviewed vibe coding from accountable agentic engineering](https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering/).
This guide concerns the accountable end of that range. I still care how the
system works, even when a model writes every line.

## I Work at Architect Altitude

A large part of why I can build quickly is that I'm comfortable handing real
decisions to the model. I set up controls for the properties I care about, give
architecture guidance, and state the outcome. I am not doing spec-driven
development, and I am not reviewing the code line by line. For most interface
work my acceptance bar is that it looks right and is usable, not that a
particular button sits at a particular pixel.

None of that is new to me. It's what an architect role already asks for: own
the boundaries, contracts, failure behavior, and the decisions that change the
shape of a system, and leave the mechanism to the people implementing it.
Agents mostly compressed that division of labor into a much shorter cycle.

The internal shift I'm trying to make happen is getting developers to work the
same way. The conversations still stall on two objections: “how do you know
what it does if you don't review every line?” and a practice where the
specification runs several pages and most of the token budget goes to
verification. Both are reasoning at engineer altitude, where the code itself is
the object of care. That instinct built good software for decades, so it
doesn't yield to encouragement. It yields when the properties that made
line-by-line reading worthwhile are enforced somewhere a reader doesn't have to
stand — types, ownership boundaries, tests, permissions, and runtime evidence.

Underneath the objection sits a question I don't consider settled: what do
“right” and “quality” mean once a model writes most or all of the code? My
working answer is that they describe the system's observable behavior, its
boundaries, and the evidence that both hold — not any individual line, and not
whether a human read it. That definition holds up in how I work. Whether it
holds up across a team, an audit, or an incident review is the argument worth
having.

## Design Principles

These are the axioms I expect a model to hold while it designs an architecture,
proposes a mechanism, or answers a technical question — the standing judgment I
delegate along with the work. Each one exists because of a failure I have
corrected repeatedly, so each is paired with the tendency it corrects.

| Principle | The failure mode it corrects |
| --- | --- |
| **No gold plating.** Build what the outcome requires, at the bar it requires, and stop. | A model produces volume cheaply and expands to fill available space, then justifies the expansion with requirements nobody asked for. |
| **Most correct, not fastest.** Never a workaround standing in for the requested result, never a scope cut the implementer chose alone. | Closing the turn with something that runs is the path of least resistance, so the call-site patch beats the contract fix. |
| **Correctness is defined by maintainability.** A system that can't be changed safely tomorrow isn't correct, it's temporarily lucky. | A model optimizes the artifact in front of it and bears none of the cost of the next edit. |
| **Enumerate the whole set before acting.** States, consumers, call sites, and failure paths come from searching the system. | A model generates the cases that are plausible rather than the cases that exist, and returns a partial answer shaped like a complete one. |
| **One canonical implementation.** No second path, no divergent implementation, no shim beside the real thing. | Searching is expensive and writing is cheap, so a model reimplements what it failed to find, and the copy then drifts. |
| **Invalid state stops the system.** No fallback that lets a misconfiguration continue quietly. | A model reads a fallback as robustness; it converts a loud failure at the boundary into a silent wrong result downstream. |
| **A boundary the build doesn't enforce is not a boundary.** Dependency direction and policy chokepoints are checked mechanically. | Written rules don't bind a model. It reaches across a layer because that was the shortest route to working code. |
| **Hypotheses come from code and data, never from text completion.** Read the source, run the thing, get the log. | Fluent assertion is free, and a diagnosis with nothing behind it reads exactly like one with everything behind it. |

[Read the design principles in depth, with the prompts they came from.](coding-agents/design-principles.md)

## Guide

| Article | Question it answers |
| --- | --- |
| [Design Principles](coding-agents/design-principles.md) | Which axioms should a model hold while designing, and which failure mode does each one correct? |
| [Design as a Conversation Between Peers](coding-agents/collaboration-and-design.md) | How do I work with a model as a product and design peer without writing a complete specification first? |
| [Context Engineering as Information Architecture](coding-agents/context-and-memory.md) | How do documentation, retrieval, source navigation, and information lifecycles keep context useful? |
| [Architecture That Helps Agents Stay Correct](coding-agents/architecture-for-agents.md) | Which architecture and language choices reduce errors and keep work inside a bounded context? |
| [Tooling, Capabilities, and External Work State](coding-agents/tooling-and-controls.md) | How do agent rules, deterministic controls, secret brokering, and durable plans increase autonomy safely? |
| [Verification and Harness Improvement](coding-agents/verification-and-improvement.md) | How do I match evidence to claims and turn recurring failures into better infrastructure? |
| [Reusable Prompt Patterns](coding-agents/prompt-patterns.md) | Which material prompt structures recur in my work, and how can they be adapted without becoming rituals? |

## The Method in Brief

### Design Through Dialogue

I usually begin with a short, informal account of the outcome, the current
pain, and a few constraints — rarely a complete specification. The model
studies the system, proposes a design, and identifies the choices that would
change its shape. We build shared understanding through that exchange. When
the problem is genuinely open, that becomes an intent → exemplar research →
distillation loop, and the distilled survey stays behind as design material.

I expect the model to act as a peer: bring evidence, make recommendations,
question the premise when necessary, and say when the requested approach is
wrong. I keep product taste, authority over consequential choices, and final
acceptance. The model handles most of the investigation and technical
mechanism.

The prompts can stay quick because the permanent concerns live outside them.
Repository instructions, current-state documents, ADRs, plans, types, linters,
permissions, tests, and deployment controls carry the standing context and
reject violations of the properties that matter. Familiarity with the model
and the repository lets the conversation move quickly without making safety
depend on perfect wording.

[Read the collaboration and design article.](coding-agents/collaboration-and-design.md)

### Engineer the Information Environment

Context engineering is information architecture. A repository should tell the
agent which source owns each kind of truth, where to begin, and how to retrieve
more detail only when needed. Current code and runtime evidence outrank stale
plans; ADRs preserve rationale; backlogs describe intent. Transcript history
recovers prior decisions but can't prove current behavior.

I let agents search their own history so a new session can recover earlier work
without asking me to reconstruct it. Search results need source turns,
repository scope, index state, and a way to reopen the original context. Source
navigation needs the same honesty about confidence and fallback behavior.

[Sulion](https://github.com/chris-arsenault/sulion) is my reference
implementation for most of the tooling in this guide — transcript retrieval,
structural code navigation, brokered credentials, and published plan state.
The principle stands without it: agents need to find their prior work and
current evidence through inspectable interfaces.

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

Credential access is the clearest example: a secret broker limits each
credential to one granted command, and the agent rule treats a denial as a
hard stop rather than an invitation to hunt for another token. The tooling
article walks through this split in detail.

Plans are another tool boundary. They externalize the outcome, decisions,
phases, exit gates, and unresolved choices. I expand the next phase just in
time, so work stays resumable without filling the plan with stale file-level
instructions.

[Read the tooling and controls article.](coding-agents/tooling-and-controls.md)

### Verify the Claim at the Layer Where It Exists

A unit test supports a local behavior claim but proves nothing about
deployment; a deployment log shows the release mechanism ran but says nothing
about whether a user-visible path works. Performance claims need traces,
profiles, benchmarks, or runtime telemetry.

I require proportionate evidence and report what remains unverified. When the
same failure recurs, I improve the harness: clarify an instruction, restructure
documentation, add a type or linter, preserve a decision, improve a tool, or
add a test at the layer that can observe the contract.

[Read the verification and improvement article.](coding-agents/verification-and-improvement.md)

### Use Reusable Prompt Shapes

My recurring prompts specify mode, outcome, evidence, constraints, delegated
judgment, persistence, and proof — though rarely all in one prompt, because
standing repository context supplies the defaults.

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
3. Load the repository map, retrieve prior decisions, and check the freshness
   of the retrieval and code indexes.
4. Survey the complete affected path before choosing a local mechanism.
5. Research uncertain parts and verify assumptions against current sources.
6. Let the model recommend a coherent design and ask only about choices that
   change its shape.
7. Record lasting decisions in the document type responsible for them.
8. Publish milestone state and expand the next phase just in time.
9. Implement within the smallest correct boundary and preserve adjacent
   ownership.
10. Encode stable constraints in the strongest deterministic layer available.
11. Verify each claim where it can actually be observed.
12. Report what remains unverified before publishing or handing off.
13. When a failure repeats, improve the harness that allowed it.
