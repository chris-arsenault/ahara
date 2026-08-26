# What Has Worked for Me When Building Software With Coding Agents

I get the best results from coding models when I stop treating them as code
generators. I treat them as temporary product managers, designers, architects,
engineers, and reviewers. I give them outcomes and constraints, require them to
study the real system, let them choose the mechanism, and ask for evidence that
the result works.

This is a field report, not a neutral survey of AI development methods. I built
the workflow through sustained work on product software, infrastructure,
network appliances, simulations, and creative systems. Cognitive science and
the emerging agentic-engineering literature help explain parts of it. They also
identify failure modes worth testing. They do not define the method.

When published research disagrees with what I can repeatedly demonstrate in my
own environment, I keep the practice and improve the measurement. The tools and
workflows are changing too quickly for an older average result to overrule
current direct evidence. That standard cuts both ways: feeling faster is not
evidence either.

People use "vibe coding" for several incompatible practices. Simon Willison
[distinguishes unreviewed vibe coding from accountable agentic engineering](https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering/).
This essay concerns the accountable end of that range. I still care how the
system works, even when a model writes every line.

## I Own the Outcome; the Model Owns the Mechanism

My most important division of labor is simple:

| I retain | I delegate |
| --- | --- |
| Outcomes and product taste | Repository investigation |
| Priority, cost, and risk | Requirements and acceptance criteria |
| Authority to publish, spend, or deploy | Product and interaction design |
| Material product choices | Architecture, code, telemetry, and tests |
| Final acceptance | Options, recommendation, execution, and verification |

I do not ask the model to write code for a mechanism I have already designed
unless I have a specific reason to constrain it that tightly. I tell it what I
need the system to accomplish, what must remain true, and what evidence will
convince me. The model should decide whether it needs a new abstraction, a
schema change, more telemetry, or no new code at all.

This is where models become useful as product managers and designers. A model
acting as a product manager should turn an outcome into affected users,
requirements, dependencies, rollout risks, and acceptance criteria. A model
acting as a designer should reason about the complete user journey, visible
system state, recovery from failure, and the controls a person needs. Neither
role is a prelude to generating code. Sometimes the right result is a sharper
problem statement or a recommendation to leave the system alone.

Kief Morris describes a human-owned "why loop" and an agent-run "how loop" in
[Humans and Agents in Software Engineering Loops](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html).
That is close to my practice, but I give the model more of the middle than the
usual framing implies. I expect it to help define the product, not merely carry
out a specification. I still retain the outcome and the authority boundary.

The model should ask me about decisions that change the shape of the product or
system. It should not ask me to choose tunable constants, internal data
structures, logging fields, or other technical means it can evaluate itself.
Giving a model criteria and then making the human decide every mechanism throws
away most of the value.

## I Name the Work Mode Before I Name the Work

The same subject can require very different behavior. "What do you think about
this authentication design?" and "replace this authentication design" concern
the same files, but they grant different authority.

I keep these modes distinct:

| Mode | Expected result | Authority granted |
| --- | --- | --- |
| Answer | Evidence-backed answer | Read only |
| Explore | Context, tensions, directions | Read only |
| Propose | Recommended design and consequences | No implementation |
| Implement | Agreed change and verification | Scoped edits |
| Review | Findings by evidence and impact | No silent repairs |
| Publish | Reviewed external artifact | Named external action |

A question is not an instruction to start the next phase. A review is not
permission to fix everything found. A proposal written after the code changed
was never a proposal.

This boundary protects human attention as much as repository state. Sophie
Leroy's experiments on
[attention residue](https://doi.org/10.1016/j.obhdp.2009.04.002) found that
attention can remain attached to an unfinished prior task and reduce performance
on the next one. Masicampo and Baumeister found that making a specific plan for
an unfinished goal can reduce its intrusive cognitive effects in
[Consider It Done!](https://pubmed.ncbi.nlm.nih.gov/21688924/). These studies do
not prescribe an engineering process, but they explain why explicit stops,
written plans, and resumable phases help.

I also avoid letting background agents control my attention. Mitchell Hashimoto
reports the same practice in
[My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey):
the human decides when to check the agent instead of accepting a stream of
notifications. Running more agents is not useful when supervising them destroys
the attention needed to make product decisions.

## I Make the Model Research Before It Asks Me Questions

Models often ask premature questions because asking is cheaper than
investigating. I reverse that incentive. The model first reads the repository's
instructions, documentation index, architecture, decision records, current
implementation, and verification entry points. It searches prior work when a
decision may already exist. Only then should it surface choices.

The sequence I use is encoded in Ahara's
[feature-start workflow](../skills/feature-start/references/sequence.md):

1. Frame the task and load the repository's rules.
2. Survey the affected path broadly enough to find contracts, consumers,
   reusable components, and verification tools.
3. Go deep on the technically uncertain parts.
4. Classify what can be reused as-is, what must be adjusted, and what is truly
   new.
5. Ask only questions whose answers materially change the design.
6. Confirm the intended boundary before editing.
7. Record durable decisions, then make the implementation plan.

Exploration does not need to wait for permission to think. The checkpoint is
before the model locks a design or changes the system. This distinction lets the
model bring a real recommendation to the conversation instead of presenting a
blank multiple-choice form.

Breadth before depth matters. A model that opens the first plausible file and
starts editing will optimize one local mechanism before it knows who consumes
it. When recommendations begin swinging with each new comment, I stop the
implementation and ask for a consumer-by-consumer requirements map. That map
usually reveals that the apparent binary choice was an incomplete model of the
system.

## Context Engineering Is Information Architecture

The best prompt cannot compensate for an incoherent information environment.
My context system includes repository instructions, current-state docs, ADRs,
plans, code, configuration, tests, runtime evidence, transcript retrieval, and
the tools that connect them. The quality of the work depends on how those parts
represent and expose the problem.

This has a close analogue in cognitive science. Zhang and Norman's
[representational analysis](https://doi.org/10.1207/s15516709cog1801_3) treats
many tasks as systems of internal and external representations. Edwin Hutchins'
[cockpit study](https://doi.org/10.1207/s15516709cog1903_1) takes the larger
socio-technical system, rather than one person's memory, as the unit of
analysis. David Kirsh's
[work on the intelligent use of space](https://www.sciencedirect.com/science/article/pii/000437029400017U)
shows how arranging a workspace can simplify choice, perception, and internal
computation.

A repository is a symbolic workspace. File names, directory boundaries,
indexes, stable identifiers, and visible state change what both humans and
models can perceive and decide. Documentation is therefore part of the working
system, not explanatory material added after the real work.

I use this authority order when sources disagree:

1. System, organizational, and safety constraints.
2. The current request and its authorization boundary.
3. Repository-local agent instructions.
4. Current code, configuration, and observed runtime behavior.
5. Current-state architecture and operating documentation.
6. ADRs as records of rationale and accepted direction.
7. Plans and backlogs as future intent.
8. Transcript history and memory as recoverable context that still requires
   current verification.

Different information has different lifecycles. Current-state docs say what is
true now. ADRs explain why a consequential choice was made. Backlogs describe
work that has not landed. Changelogs describe shipped behavior. Mixing those
jobs creates context poisoning: the model receives several incompatible claims
without a reliable way to rank them.

My top-level files are maps, not encyclopedias. The repository's
[documentation principles](../skills/repo-docs/references/principles.md) direct
agents to progressively deeper sources. This matches the approach OpenAI
describes in
[Harness Engineering](https://openai.com/index/harness-engineering/): a short
`AGENTS.md` points into a structured, versioned knowledge base. It also matches
Anthropic's recommendation to find the smallest set of high-signal tokens and
retrieve additional material just in time in
[Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).

More context is not automatically better. The
[Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/) experiments showed
that long-context models could perform much worse when relevant information sat
in the middle of a long input. Newer models have improved, but the design lesson
still holds: indexes and targeted retrieval beat undifferentiated dumps.

Human cognitive load theory provides a related, though not identical, warning.
John Sweller's
[work on problem solving and learning](https://www.sciencedirect.com/science/article/pii/0364021388900237)
showed that a demanding means-ends search can consume capacity that would
otherwise support learning. I do not claim that human working memory and model
context windows are the same mechanism. The practical parallel is narrower:
irrelevant search and poorly structured representations consume resources that
could be used to understand the problem.

## I Let Agents Search Their Own History

I give agents direct access to prior decisions and working preferences instead
of asking people to reconstruct them from memory. A rule that says "research
before asking" only helps if the model can search what it previously did.
Without that access, every new session begins by asking the human to rebuild
context, scanning unrelated files, or guessing from the current implementation.
Compaction helps one conversation continue; searchable history lets a new
conversation recover a decision made months earlier.

I want history search to provide:

- repository scope by default, with deliberate widening when a decision spans
  projects;
- lexical search for exact identifiers and semantic search for concepts whose
  wording changed;
- source session and turn identifiers so a short result can be reopened in its
  original context;
- separate controls for reasoning, user requests, tool calls, errors, and
  low-value command mechanics;
- explicit index freshness and failure state; and
- stable machine-readable output for other tools and agents.

The searchable corpus also needs curation. Agent reasoning and concise
statements of intent are usually useful. Full command output, repeated file
reads, diffs, and image payloads are usually better recovered from the codebase
or an artifact store. Embedding everything makes similarity search noisier and
uses the context budget to reproduce mechanics rather than decisions.

History search changes the human role. I no longer need to remember where a
decision was discussed or teach the same working preference to every fresh
agent. The agent can find the prior turn, explain what it thinks was decided,
and verify that conclusion against current code and documentation. Retrieved
conversation is evidence of intent at a point in time, not proof of current
system state. If the index reports incomplete coverage, the agent can say so
instead of presenting one hit as exhaustive.

Sulion is my reference implementation. Its `sulion-retrieve` command combines
lexical and semantic search, defaults to the current repository, returns source
session and turn identifiers, and excludes routine tool mechanics by default.
It reads result text from canonical transcript tables and reports pending or
failed indexing work. During this essay's research, it found the earlier
Canonry kernel work and also reported pending semantic sources; I used the
result as a lead and checked the current project files.

The same principle applies to source navigation. An agent-facing code search
tool should expose index freshness and confidence, bound its output, and label a
syntactic fallback rather than presenting it as semantic certainty. Sulion's
`sulion-code` does that, and its patch operation produces a diff without
applying it, preserving the separate authorization boundary around file
changes.

These are context-engineering tools because they shape what evidence reaches
the model and how much uncertainty accompanies it. Anthropic makes the same
general point in
[Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents):
tools define the contract between the agent and its information or action
space, so their purpose and outputs need to be narrow and unambiguous.

## I Design Architecture Around Error Prevention and Bounded Context

Architecture determines how much of the system an agent must understand at
once, which mistakes its tools can catch, and how far a bad edit can spread. I
therefore treat architecture as part of the agent harness. The useful patterns
are not agent-only patterns; they are sound engineering practices whose value
increases when code arrives faster than people can review it.

Across the larger repositories I surveyed, the same shape keeps recurring:
clear ownership, a strict inner model, narrow adapters, small composable units,
one canonical path for each behavior, and build rules that reject invalid
structure close to the edit. The languages and frameworks differ. The method
does not.

### Start with ownership and lifecycle

I do not begin architecture with a diagram of boxes. I begin with questions:

- Who owns the behavior and the data?
- Which source is authoritative?
- What changes with a release, with machine provisioning, and at runtime?
- Which identity has permission to read or mutate each state?
- What are the upstream and downstream contracts?
- Which failures must stop the operation?
- Which optional capabilities can degrade without breaking the primary path?
- What is explicitly outside this subsystem?
- What evidence would show that the boundary works?

These questions recur throughout Ahara. The
[platform integration guide](../INTEGRATION.md) defines shared rails that
applications consume instead of recreating. The
[platform architecture](architecture.md) records construct ownership and
authoritative sources.

The peer repositories make the same method concrete:

- Gateway ADR 0016 in `ahara-vpn` separates versioned topology, machine-local
  identity, and mutable operational state because each has a different owner
  and lifecycle.
- Gateway ADR 0017 checks only what a release controls and reports external
  failures without pretending the deploy can repair them.
- Trust ADR 0002 in `ahara-trust` records a target boundary where workloads
  retrieve secrets under their own identities so a pipeline does not become a
  privileged deputy.
- Collector ADR 0006 in `ahara-collector` gives the storage schema to the system
  that stores sensor data. The collector owns protocol decoding and its native
  reading envelope.

The trust decision also shows why an ADR cannot prove current state. The shared
[TrueNAS deployment action](../.github/actions/deploy-truenas/action.yml) still
accepts deployment-time secret mappings. I treat that migration as incomplete
until the implementation and runtime path match the decision.

This style scales because it keeps adjacent responsibilities intact. When I ask
for a subsystem, I expect a coherent subsystem contract, not a patch to one node
and not a rewrite of the entire chain. The model should name what remains, what
adapts, and what disappears.

Authority deserves the same precision as data flow. A credential denial is a
hard boundary, not a debugging puzzle. The model reports the exact failure and
waits for an approved path. It does not hunt through other stores for a token or
weaken policy to make progress.

### Choose languages for the failures they reject

I do not choose a language primarily for programmer comfort or for the speed at
which a model can emit it. Models can produce plausible code in every common
language. The expensive question is what happens after generation: which
mistakes become compiler errors, which survive into review, and which reach
production.

That is why I often choose Rust for service and systems cores. I want ownership,
borrowing, thread-safety bounds, exhaustive state handling, and typed errors to
be part of the ordinary edit loop. I will accept slower compilation and a more
demanding type system when they move failures from runtime into a local,
machine-checkable result. Sulion uses Rust for the processes that own terminals,
repositories, retrieval, credentials, and node coordination. Lindelion uses it
for realtime audio, state, host adaptation, and DSP. The choice is about the
error budget, not typing speed.

Rust does not remove the need for architecture. Safe Rust still permits heap
allocation, blocking work, unbounded loops, and incorrect domain logic.
Lindelion's allocation-free audio contract says this directly, then surrounds
the realtime path with preallocation, bounded work, lock-free handoffs, and
allocation-counting tests. The language eliminates some failure classes; the
architecture and harness own the rest.

I do not force every problem into Rust. Canonry uses C# but enables current .NET
analyzers, nullable checking, warnings as errors, locked packages, and a much
stricter kernel project. Catalyst uses strict TypeScript with exact optional
property types, then adds structural and semantic decoding because TypeScript
cannot protect a JSON boundary at runtime. Harbor keeps Python for its trading
and research system, but puts decisions in pure deterministic cores with
explicit typed inputs and immutable state where the contract requires it.
Several execution modes run through those cores. The selection rule is
consistent even when the language changes: choose the language and build mode
by the defects they can exclude in this system.

### Keep the unit of work inside a bounded context

Small composable modules let an agent load the relevant contract, implementation,
and tests without carrying an entire subsystem in context. They also make
ownership visible. A focused file can have one reason to change; a focused crate
or package can expose a narrow dependency surface; a focused feature can be
reviewed without reconstructing unrelated behavior.

I encode this preference in build rules rather than asking every agent to judge
when a file has become too large. Catalyst and Scuba Sense reject TypeScript
files above 400 logical lines and functions above 75. Lindelion caps Rust files
under its crates, plugins, and automation trees at 600 lines, while Clippy flags
cognitive complexity and long functions. Sulion checks Rust files, functions,
and impl blocks separately, with one named file override rather than a general
escape.
The exact thresholds reflect each codebase. The shared policy is that an
oversized unit must either split along a real responsibility boundary or carry
a specific, reviewable reason not to.

A line cap is a tripwire, not a decomposition method. David Parnas's classic
[paper on modular decomposition](https://doi.org/10.1145/361598.361623) argues
for organizing modules around design decisions that may change rather than
merely following processing steps. That is the split I want an agent to find:
one hidden decision, one owner, and a narrow interface. Moving half of a large
file into `helpers.ts` without finding that boundary satisfies the number and
misses the architecture.

This does not mean turning every function into a file or every module into a
network service. Tiny fragments can increase navigation cost and hide the
behavioral unit. I want the smallest unit that remains coherent: enough code to
state one contract and see how it works, but not enough to mix several owners or
lifecycles. This is the code-level counterpart to the progressive context
design described earlier. The repository, not the prompt, keeps the working set
bounded.

### Keep decisions in a pure core and side effects at the edge

The most common large-repository pattern is a deterministic or pure core behind
thin adapters:

- Tsonu Music keeps playback, feature analysis, graph compilation, scheduling,
  and performance decisions in plain-data modules. The browser host gathers Web
  Audio and WebGL state, calls the core, and applies its decisions.
- Lindelion's host-neutral effect crates depend on DSP foundations rather than
  VST3 or UI code. VST3 and standalone packaging remain adapters around the
  effect contract.
- Harbor's strategy core has no network, database, clock, broker, or UI I/O.
  Live trading, paper variants, and backtests adapt external facts into the same
  decision path.
- Canonry keeps deterministic mutation in `Engine.Kernel`; host composition,
  authored domain compilation, projections, telemetry, and UI stay outside it.
- Catalyst separates its immutable game definition and runtime from browser
  lifecycle, persistence scheduling, presentation, React, and Pixi.

This boundary reduces the amount of mocking required to verify important
behavior. Tsonu's timing and graph state machines run in Node without a DOM,
audio device, or GL context. Harbor can replay the same strategy over recorded
candles. The unavoidably host-specific layer stays small enough for targeted
integration or real-device checks.

It also clarifies where an agent may introduce an effect. Code in the core
returns a decision or state transition. Code at the edge performs I/O, reads a
clock, touches a device, or translates a protocol. When those responsibilities
mix, a local change silently acquires operational consequences and the test
surface fills with imitations of the outside world.

### Compile flexible inputs into a strict runtime form

Human-friendly authoring and runtime execution need different representations.
I let authored configuration remain descriptive, named, and easy to change,
then validate and compile it once into the smallest representation the runtime
needs.

Canonry compiles domain names and gameplay concepts into stable identifiers and
primitive fixed-capacity program data before they reach its kernel. Catalyst's
dependency direction is explicit: authored content enters a compiler, which
produces a validated and deeply frozen `GameDefinition`; untrusted saves pass
through structural decoding and semantic validation before becoming
`GameState`. Tsonu's random scheduler and authored scene editor may produce
graphs differently, but both must reach the same typed graph compiler. Authored
scenes may bypass rules of taste in the scene grammar; they cannot bypass port
types, required inputs, cycle legality, or resource assignment.

This is a productive division of labor for agents. The model can work in a rich
authoring surface without teaching the hot path about prose, optional fields,
or partially valid state. The compiler becomes the arbiter. Stable IDs,
immutable definitions, typed commands, and primitive event records prevent an
agent from inventing a second interpretation inside a consumer.

### Use a small kernel and add extension seams only for real variation

A microkernel or plugin shape helps when the system has a small set of stable
invariants and many independently changing behaviors. The kernel should own
lifecycle, scheduling, type compatibility, resource bounds, and publication.
Extensions should declare what they consume and produce without gaining a
second route around those rules.

That shape bounds context as well as behavior. An agent changing one extension
needs the kernel contract and that extension, not every other implementation in
the catalog. A kernel change is visibly cross-cutting and deserves a broader
survey before editing.

Tsonu's visualizer is the clearest plugin example. A plugin definition is plain
data with typed ports, capabilities, cost, lifecycle, and scheduling metadata.
The graph compiler validates definitions without a GL context, and registering
a plugin does not require a kernel edit. Canonry uses the same division at a
different scale: the simulation kernel owns deterministic state mutation and a
primitive event stream, while projections, telemetry, UI, and future consumers
advance independently outside it.

The counterexample matters. Lindelion explicitly rejects a general-purpose
plugin framework. It owns a small host adapter and extracts shared crates when
two real consumers need the same behavior; code that merely looks generic stays
local. Its effect core is host-neutral because standalone, combined-VST, and
per-effect packaging are concrete possibilities, not because every component
must become a plugin.

I therefore do not apply “microkernel” as a default template. I use it when I
can name the invariants the kernel owns and the dimensions along which real
extensions vary. Otherwise a plugin system adds indirection, lifecycle states,
and compatibility work before it has a second consumer. Small composable
modules are a default. A generalized extension framework is an earned
boundary.

### Preserve one canonical path for each behavior

Multiple entry points are safe when they converge on one implementation of the
rule. Parallel semantic paths drift because an agent fixes the path in front of
it and may never discover the others.

The surveyed repositories repeatedly make convergence explicit. Harbor sends
backtest, paper, and broker-facing decisions through the same strategy core.
Tsonu sends generated and authored scenes through the same graph compiler.
Catalyst uses the same resolved placement decision for preview, execution, save
validation, and rendering. Agents of Glass makes its `glass` CLI the only live
state interface for agents and concentrates contract tests there; prompts do
not create an alternate mutation path.

This practice changes how I design testability. I prefer a pure core used in
production over a production implementation plus a mock-friendly duplicate. I
prefer one command or service boundary over a direct database path for “simple”
callers. If an alternate mode needs a different policy, that difference should
be an explicit input or adapter, not a forked implementation of the invariant.

### Make architectural boundaries executable and helpful

Code written by models arrives faster than human convention can correct it.
The repository therefore needs strict defaults that make the intended shape
obvious and make violations fail near the edit. OpenAI's
[Harness Engineering](https://openai.com/index/harness-engineering/) describes
the same result from an agent-first codebase: fixed dependency directions,
custom linters, structural tests, and remediation text in lint errors let the
agent move quickly inside boundaries that the build enforces.

I choose the enforcement mechanism by the property:

| Property | Preferred control | Reference implementation |
| --- | --- | --- |
| An invalid state should not exist | Type, schema, or narrow API | Typed node requests with no generic command shape |
| A dependency edge is forbidden | Project reference rule or structural lint | Sulion rejects `crate::api` imports outside the API layer; Canonry whitelists the kernel's project references |
| An API must pass through one policy point | Custom lint | Sulion's `no-direct-fetch` rule funnels HTTP through the authenticated API client |
| A runtime contract must hold | Focused unit or integration test | Reconnecting a Sulion development environment preserves its PTY inventory and output |
| A deployed behavior is claimed | Deployment and runtime evidence | Rendered configuration, deployment logs, health checks, and a user-visible path |

The failure should provide just-in-time guidance, not only rejection. Sulion's
`no-direct-fetch` error tells the agent to use `api/client.ts` and explains that
the wrapper owns base URLs, errors, and response parsing. Its inline-style rule
names the CSS path and the documented exception for truly dynamic values.
Canonry's project gate names both the forbidden reference and the two projects
the kernel may use. Catalyst's architecture check reports the file, forbidden
dependency, or cross-layer cycle. A useful control answers four questions at
the moment of violation: what rule failed, why the rule exists, which path is
allowed, and how a legitimate exception is recorded.

The severity should match the property. Direct `fetch`, forbidden dependency
edges, JavaScript source in a TypeScript application, and the wrong test
framework are errors because they bypass load-bearing policy. Large JSX prop
lists or allocations passed as props may begin as warnings because they signal
maintainability or performance debt without invalidating the system. Strictness
works when it distinguishes a broken contract from an improvement opportunity.

#### The Canonry kernel is a practical allocation-boundary proof

`the-canonry-game/src/Engine.Kernel` isolates the simulation hot path in its own
assembly. That physical boundary makes a project-wide static rule a useful
approximation of a hot-path call-graph rule.

The kernel project enforces several properties before compilation finishes:

- it may reference only `Engine.Constants` and `Engine.Eventing`;
- runtime package dependencies are rejected;
- Microsoft's banned-API analyzer reads `BannedSymbols.txt` and rejects strings,
  LINQ, heap collection types, tasks, channels, logging, profiling timers, and
  file I/O;
- a source gate catches string syntax that symbol analysis does not reliably
  catch and also rejects `stackalloc`; and
- an architecture test rejects floating-point members in the kernel assembly,
  primitive event assembly, and compiled kernel inputs; and
- warnings become build failures through the repository-wide defaults.

That is a practical proof of a named architectural property: code in the kernel
cannot use the listed APIs or dependency routes. It is stronger than a test that
runs one scenario and happens to observe zero bytes, because the build checks
every compiled kernel source path on every change.

It is not a mathematical proof that the CLR can never allocate. Array or object
construction, boxing, compiler-generated state, and a future unlisted API still
need coverage. If the claim is zero steady-state allocations in
`Simulation.AdvanceTicks()`, I would add a kernel-specific Roslyn analyzer for
those constructs and a warmed runtime allocation counter or profiler check.
The current controls justify “the known allocation-prone APIs and dependencies
are forbidden, and the runtime member boundary is fixed-point,” which is
already a strong invariant.

#### Tests protect behavior; they should not preserve yesterday's syntax

Tests drift when they mirror an implementation, authored content, or the text
of a completed migration. An agent then updates the test and implementation
together without preserving any independent fact. The extra file creates work
but little confidence.

Canonry's repository rules capture this from experience. Permanent tests must
protect durable behavior, a schema rule, or an architecture boundary. Temporary
refactor scaffolds should be deleted when the move lands. Broad source-word bans
are explicitly rejected: a past guard against `pressure` broke unrelated diving
technology. Some current architecture tests still inspect source fragments;
those are useful only where the fragment closely represents the boundary and no
stronger compiler or graph check exists.

My order of preference is:

1. Make the invalid shape unrepresentable through types, schemas, ownership, or
   a narrow command surface.
2. Enforce static boundaries in the compiler, project graph, custom analyzer,
   or lint configuration.
3. Use an architecture test for a stable repository property the build system
   cannot express directly.
4. Use behavioral tests for observable contracts and integration between real
   components.
5. Use runtime telemetry and deployed checks for performance, operations, and
   claims that only exist in the running system.

This hierarchy does not make tests secondary. It gives each fact to the layer
that can observe it without imitation. A no-import rule belongs in the build. A
reconnect contract belongs in an integration test. A latency claim belongs in
runtime evidence. Agent throughput then amplifies the controls instead of
amplifying drift.

## I Use Instructions for Judgment and Software for Guarantees

My global agent rules are part of the working system. They tell the model which
actions a question authorizes, when to publish a plan, where to retrieve prior
work, which code-navigation tool to try first, how to keep edits visible to
file-churn tracking, and when a credential or deployment failure must stop the
task. These are not preferences pasted into every prompt. They are the stable
operating contract for the environment.

I keep those rules in version control, install them into each agent's expected
location, and compare the maintained and installed copies mechanically. Sulion
is the reference implementation: its tracked templates live under
`sulion/docs/agent-instructions/`, while Claude reads the installed copy from
`~/.claude/CLAUDE.md`. The two files were byte-identical during this review.
The same check covers duplicated toolset documentation in Sulion's backend and
development-environment images. I prefer a source-to-install contract to two
files that are "kept in sync" by convention.

The rules carry the decisions that need judgment:

- answering, reviewing, proposing, editing, publishing, and deploying grant
  different authority;
- an agent retrieves prior decisions and reads the owning docs before asking me
  to reconstruct context;
- deployment failures require logs before diagnosis or remediation;
- native editor operations preserve file-churn evidence;
- credential failures stop the command and prohibit scavenging for another
  token; and
- multi-phase work publishes honest phase state in a durable plan.

Instructions also make unfamiliar tools discoverable. A model will not infer
the names of an environment's history search, code index, secret broker, or
plan publisher. Putting those names and their decision rules in the global file
makes the environment usable from the first turn. In Sulion, those tools are
`sulion-retrieve`, `sulion-code`, `with-cred`, and `sulion plan`.

I treat instruction files as behavioral guidance, not an enforcement boundary.
Any restriction that needs a guarantee also belongs in permissions, hooks,
types, build rules, or the runtime. Sulion's instruction documentation states
that division explicitly. It lets the model exercise judgment inside a
deterministic envelope. Anthropic's
[Trustworthy Agents in Practice](https://www.anthropic.com/research/trustworthy-agents)
similarly treats the model, harness, tools, and environment as separate parts
of the safety system.

## Security Comes From Capabilities, Not Promises

A secure agent environment gives the model narrow capabilities instead of
placing powerful credentials in its ambient shell and asking it to be careful.
Secret access should be explicit, time-bounded, attributable, and limited to
the process that needs it. Ambiguous merges should fail. A denial should be
machine-readable and should not reveal the value.

The behavioral rule and the mechanism do different work. The mechanism
prevents use without an active grant. The instruction tells the model not to
respond to a denial by searching files, token caches, another secret id, or a
broader cloud role. Access control blocks the direct path; the instruction
keeps a capable operator from trying to route around it.

Sulion's secrets broker is the reference implementation. It supports exactly
two credential-consumption paths: `with-cred` for an environment bundle and the
broker-backed `aws` wrapper. There is no shell-wide export and no alternate
broker execution path. `with-cred` injects values into one child process,
grants expire or can be revoked, and colliding environment keys cause a
rejection instead of an order-dependent merge. A denial exits with a distinct
status and tells the model which access was refused.

The reference implementation also documents its limit. Current Sulion PTYs
share uid 7321. One terminal can read another terminal's key path and a redeemed
child process's environment while that command lives. The grant therefore
separates locked secrets from currently unlocked secrets; it does not isolate
hostile concurrent terminals. True per-terminal isolation would require
separate identities or an inherited descriptor instead of a shared readable
path. Calling the current design "PTY-scoped isolation" would make the
documentation more reassuring and the system less safe.

The same capability pattern applies to remote execution. Prefer a closed set of
typed requests over a generic remote shell, and an allowlist of container
operations over unrestricted Docker access. Sulion's node protocol and brokered
container runner follow those rules. Its dedicated direct-Docker mode grants
host-root-equivalent authority deliberately and documents the machine as a
trusted single-user boundary. Security improves when each surface states the
authority it really provides.

## Plans Are External Working State

I plan enough to make the work resumable and inspectable, then expand details
only when the next phase is ready to execute.

A useful milestone plan records:

- the outcome and scope;
- decisions already made;
- dependencies between phases;
- a concrete exit gate for each phase;
- unresolved choices that genuinely require human input;
- what remains unverified.

The next phase can then expand into file-level steps, expected behavior, and
specific checks. Planning every edit at the beginning creates false precision
and stale instructions. Planning nothing forces the human and model to rebuild
state after every interruption.

A useful plan publisher exposes compact phase state without exposing the
agent's private reasoning or requiring someone to read its entire transcript.
Sulion is my reference implementation: the detailed plan stays with the work,
while the user sees phase names, status, notes, and history. Phase status
changes when reality changes, not in a ceremonial batch at the end.

Plans also let work stop cleanly. The Masicampo and Baumeister findings do not
prove that a Markdown plan improves software, but they support the underlying
human mechanism: a specific, credible next action helps release attention from
unfinished work. The agent benefits for a different reason. Its future context
can reload the recorded state instead of reconstructing it from a compressed
conversation.

## Verification Must Match the Claim

Generated code is cheap. Confidence is not.

I ask the model to identify the claim it is making and select evidence that can
actually support it:

- A focused unit or contract test can support a local behavior claim.
- The repository's canonical validation command can support an integration
  claim within that checkout.
- A deployment log can support a claim that the release mechanism ran.
- Runtime queries and user-visible checks can support a claim that the deployed
  system behaves correctly.

Those are not interchangeable. A green local suite does not prove deployment.
A successful deployment does not prove that the service is reachable or that
its data path works. When CI or runtime logs are unavailable, the cause remains
unverified.

Verification should be proportionate. Every meaningful change needs evidence,
but not every one-line edit deserves a permanent test. Permanent tests earn
their place by protecting a stable contract, invariant, security boundary, or
regression that would otherwise recur.

The model owns the telemetry needed to diagnose its work. If the stated outcome
cannot be measured with current instrumentation, it should add or adjust the
instrumentation rather than ask me to invent fields I will never inspect.

The strongest warning from the research is that perceived productivity can be
badly calibrated. A 2025 randomized trial by Becker, Rush, Barnes, and Rein
found that 16 experienced open-source developers working on 246 tasks with
early-2025 tools took 19 percent longer with AI, while believing they had worked
20 percent faster in the study's post-task estimate
([paper](https://arxiv.org/abs/2507.09089)).

I do not treat that result as a verdict on my current workflow. It studied older
models, a particular interface, developers with moderate AI experience, and a
different operating method. I do treat it as a verdict on intuition as a
measurement tool. The remedy is to inspect cycle time, rework, escaped defects,
operational outcomes, and the ambition of work completed. Faster typing was
never the goal.

## I Improve the Harness When a Failure Repeats

Correcting one answer fixes one answer. Changing the environment that produced
the error can fix a class of future answers.

Depending on the failure, I may improve:

- `AGENTS.md` when a stable repository rule was missing;
- an architecture document when ownership or a boundary was illegible;
- an ADR when the rationale could not be recovered;
- a skill when a recurring workflow needed a repeatable sequence;
- a test or CI check when a machine could enforce the contract;
- a retrieval index when the information existed but could not be found;
- the tool interface when the model could not act or observe precisely.

This is harness engineering in the useful sense: specifications, tools, context,
checks, and permissions shape the model's working loop. OpenAI's agent-first
repository account and Hashimoto's adoption notes both describe making these
improvements after observing real failures. Simon Willison's
[Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering/)
similarly centers tools, specification, verification, and iteration rather than
code generation alone.

The harness should stay legible. Armin Ronacher's
[agentic coding recommendations](https://lucumr.pocoo.org/2025/6/12/agentic-coding/)
emphasize simple code, useful observability, and conservative dependency
changes. I have found the same pattern. An agent can generate complexity faster
than a team can understand it. Cheap generation increases the value of clear
boundaries and small dependency surfaces.

Repository context cannot fully repair a model assigned the wrong job. A coding
agent prompted to produce proposal prose may still turn the work into a finite
defect list. A product or design task needs instructions, tools, and evaluation
criteria for that role. Treating models as designers and product managers
requires more than telling them to adopt a persona; the surrounding process
must grant the role real decisions and demand the corresponding artifacts.

## Practices I Avoid

I avoid these patterns because I have seen them fail:

- Giving the model a giant context dump and hoping relevance emerges.
- Asking it to implement before it can describe the current system and affected
  consumers.
- Making the model ask me for every technical decision after I supplied the
  criteria.
- Treating a question, review comment, or speculative thought as authorization
  to change scope.
- Fixing something and then calling the completed change a proposal.
- Letting the design swing toward the most recent comment without reconciling
  all requirements.
- Treating docs, plans, transcripts, or memory as stronger evidence than current
  code and runtime behavior.
- Equating test success with deployment success.
- Encoding an architectural property only as a prose instruction when the
  compiler, linter, or runtime can reject violations.
- Keeping tests that mirror source text or authored content after their
  migration purpose has ended.
- Spawning more agents than human attention can supervise.
- Adding permanent process or tests that cost more than the failure they prevent.
- Weakening an authority boundary to get an agent unstuck.

## The Working Loop

For substantial work, this is the loop I return to:

1. Name the mode and authorization boundary.
2. State the outcome, constraints, and evidence of success.
3. Load the repository map, retrieve relevant prior decisions, and check the
   retrieval or code index's stated freshness.
4. Survey the complete affected path with the narrowest reliable navigation
   tool before choosing a local mechanism.
5. Research the uncertain parts and verify assumptions against current sources.
6. Let the model recommend a coherent design and ask only about shape-changing
   choices.
7. Record durable decisions in the information type that owns them.
8. Publish milestone state and expand the next phase just in time.
9. Implement with the smallest correct boundary, preserve adjacent ownership,
   and encode stable constraints in the strongest deterministic layer available.
10. Verify each claim at the layer where it can actually be observed.
11. Report what remains unverified before publishing or handing off.
12. When a failure repeats, improve the harness that allowed it.

## Sources and Further Reading

### Human cognition and work

- John Sweller, 1988:
  [Cognitive Load During Problem Solving: Effects on Learning](https://www.sciencedirect.com/science/article/pii/0364021388900237)
- Jiajie Zhang and Donald Norman, 1994:
  [Representations in Distributed Cognitive Tasks](https://doi.org/10.1207/s15516709cog1801_3)
- Edwin Hutchins, 1995:
  [How a Cockpit Remembers Its Speeds](https://doi.org/10.1207/s15516709cog1903_1)
- David Kirsh, 1995:
  [The Intelligent Use of Space](https://www.sciencedirect.com/science/article/pii/000437029400017U)
- Sophie Leroy, 2009:
  [Why Is It So Hard to Do My Work? The Challenge of Attention Residue When Switching Between Work Tasks](https://doi.org/10.1016/j.obhdp.2009.04.002)
- E. J. Masicampo and Roy Baumeister, 2011:
  [Consider It Done! Plan Making Can Eliminate the Cognitive Effects of Unfulfilled Goals](https://pubmed.ncbi.nlm.nih.gov/21688924/)

### Software architecture

- David L. Parnas, 1972:
  [On the Criteria To Be Used in Decomposing Systems into Modules](https://doi.org/10.1145/361598.361623)

### Agentic engineering

- Anthropic, 2024:
  [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- Armin Ronacher, 2025:
  [Agentic Coding Recommendations](https://lucumr.pocoo.org/2025/6/12/agentic-coding/)
- Nelson Liu and collaborators, 2024:
  [Lost in the Middle: How Language Models Use Long Contexts](https://aclanthology.org/2024.tacl-1.9/)
- Anthropic, 2025:
  [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Anthropic, 2025:
  [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Simon Willison, 2025 and 2026:
  [Vibe Engineering](https://simonwillison.net/2025/Oct/7/vibe-engineering/)
  and
  [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/)
- Anthropic, 2026:
  [Trustworthy Agents in Practice](https://www.anthropic.com/research/trustworthy-agents)
- Mitchell Hashimoto, 2026:
  [My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey)
- OpenAI, 2026:
  [Harness Engineering: Leveraging Codex in an Agent-First World](https://openai.com/index/harness-engineering/)
- Kief Morris, 2026:
  [Humans and Agents in Software Engineering Loops](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html)
- Joel Becker, Nate Rush, Elizabeth Barnes, and David Rein, 2025:
  [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://arxiv.org/abs/2507.09089)
