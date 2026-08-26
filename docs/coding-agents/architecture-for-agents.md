# Architecture That Helps Agents Stay Correct

[Back to the guide overview](../working-with-coding-agents.md)

> Throughout this article, “I,” “me,” and “my” refer to Chris Arsenault.

Architecture determines how much of a system an agent must understand at once,
which errors its tools can reject, and how far a bad edit can spread. I treat
architecture as part of the agent harness for that reason.

These are not agent-only patterns. Clear ownership, narrow interfaces, pure
cores, strict inputs, and executable dependency rules have always helped human
teams. Their value rises when code can arrive faster than a person can review
it.

## Start With Ownership and Lifecycle

I begin an architecture with ownership questions rather than a diagram of
boxes:

- Who owns the behavior and the data?
- Which source is authoritative?
- What changes with a release, machine provisioning, or runtime operation?
- Which identity may read or mutate each state?
- What are the upstream and downstream contracts?
- Which failures stop the operation?
- Which optional capabilities may degrade without breaking the primary path?
- What remains outside this subsystem?
- What evidence would demonstrate that the boundary works?

These questions prevent two common errors. A local patch may solve one node
while leaving the subsystem incoherent. A broad rewrite may absorb
responsibilities that already have a correct owner. The useful middle is a
complete subsystem contract that says what remains, what adapts, and what
disappears.

Data flow and authority need the same precision. A credential denial is a hard
boundary, not a debugging puzzle. An optional telemetry failure may degrade
cleanly. A schema migration may require the storage owner even when another
service produces the data. Architecture should state those differences before
an agent encounters them during implementation.

### Reference points

- Ahara's [integration guide](../../INTEGRATION.md) and
  [platform architecture](../architecture.md) assign shared rails and
  infrastructure constructs to named owners.
- [Ahara VPN ADR 0016](https://github.com/chris-arsenault/ahara-vpn/blob/main/docs/adr/0016-separate-topology-machine-values-and-operational-state.md)
  separates versioned topology, machine identity, and mutable operational
  state by lifecycle. Its
  [ADR 0017](https://github.com/chris-arsenault/ahara-vpn/blob/main/docs/adr/0017-the-gate-covers-only-what-the-release-controls.md)
  limits a release gate to conditions the release controls.
- [Ahara Trust ADR 0002](https://github.com/chris-arsenault/ahara-trust/blob/main/docs/adr/0002-secrets-reach-workloads-by-identity.md)
  assigns secret retrieval to workload identities, while
  [Ahara Collector ADR 0006](https://github.com/chris-arsenault/ahara-collector/blob/main/docs/adr/0006-house-sensors-owns-the-data-schema.md)
  leaves the storage schema with the system that stores the readings.

## Choose Languages for the Failures They Reject

I do not choose a language primarily for programmer comfort or for the speed at
which a model can emit it. The expensive question comes after generation:
which mistakes become local compiler errors, which survive review, and which
reach production?

I often choose Rust for service and systems cores because ownership, borrowing,
thread-safety bounds, exhaustive state handling, and typed errors become part
of the ordinary edit loop. Slower compilation and a demanding type system are
reasonable costs when they move failures out of runtime.

Language safety does not replace architecture. Safe Rust still permits heap
allocation, blocking work, unbounded loops, and incorrect domain behavior. A
realtime path still needs preallocation, bounded work, and tests or profilers
that observe allocation. The language removes some failure classes; the
architecture and build own the rest.

I do not force every system into Rust. C# with nullable analysis, warnings as
errors, analyzers, and strict project references can protect a simulation
kernel. Strict TypeScript plus runtime decoding can protect a browser
application's internal model without pretending static types validate JSON.
Python can support research and trading work when deterministic decisions sit
behind typed inputs and effect-free boundaries.

The selection rule stays constant when the language changes: choose the
language and build mode by the defects they can exclude in the target system,
not by typing speed.

### Reference points

- [Sulion](https://github.com/chris-arsenault/sulion) uses Rust for terminal,
  repository, retrieval, credential, and node-coordination processes.
- [Lindelion](https://github.com/chris-arsenault/lindelion) uses Rust for audio,
  host adaptation, and DSP; its
  [allocation-free audio ADR](https://github.com/chris-arsenault/lindelion/blob/main/docs/adr/0001-allocation-free-audio-thread.md)
  adds the realtime constraints that memory safety alone cannot supply.
- [The Canonry Game](https://github.com/chris-arsenault/the-canonry-game),
  [Catalyst Castellum](https://github.com/chris-arsenault/catalyst-castellum),
  and [Harbor](https://github.com/chris-arsenault/harbor) apply the same
  error-rejection rule through C#, TypeScript, and Python respectively.

## Keep the Unit of Work Inside a Bounded Context

Small composable modules let an agent load a contract, implementation, and
tests without carrying an entire subsystem in context. A focused file can have
one reason to change. A focused crate or package can expose a narrow dependency
surface. A focused feature can be reviewed without reconstructing unrelated
behavior.

David Parnas's classic
[paper on modular decomposition](https://doi.org/10.1145/361598.361623) argues
for organizing modules around design decisions that may change rather than
around the sequence of processing steps. That is the split I want an agent to
find: one hidden decision, one owner, and a narrow interface.

Size limits can tell me that a unit probably contains too much, but they cannot
find the correct seam. Moving half of a large file into `helpers.ts` satisfies
the number while preserving the muddled ownership. The response to a size
failure should be either a split along a real responsibility boundary or a
specific, reviewable reason the unit must remain whole.

Tiny fragments create the opposite problem. They increase navigation cost and
hide the behavioral unit. I want the smallest unit that remains coherent:
enough code to state one contract and see how it works, but not enough to mix
owners or lifecycles. The repository then bounds context before the prompt has
to explain the subsystem.

### Reference points

- [Catalyst Castellum](https://github.com/chris-arsenault/catalyst-castellum)
  and [Scuba Sense](https://github.com/scuba-sense-inc/scuba-sense) reject
  TypeScript files above 400 logical lines and functions above 75.
- [Lindelion](https://github.com/chris-arsenault/lindelion) and
  [Sulion](https://github.com/chris-arsenault/sulion) apply separate Rust file,
  function, complexity, and implementation-block checks rather than one vague
  “keep it small” instruction.

## Keep Decisions in a Pure Core and Effects at the Edge

A deterministic core receives facts and returns a decision or state
transition. Adapters read clocks, touch devices, call networks, translate
protocols, and apply the result. This boundary reduces mocking and exposes the
operational consequences of an edit.

The core should run with plain inputs in a fast local test. The host-specific
edge may still need integration tests, a real device, or deployed evidence, but
it remains small. If effectful code enters the decision path, a local change can
silently acquire network, timing, persistence, or thread consequences. Tests
then fill with imitations of the outside world.

Pure cores also support multiple execution modes without duplicating the rule.
A backtest, paper simulation, and live process can adapt different external
facts into one strategy. A browser and a headless test can call the same timing
or graph transition. Host packaging can vary without forking the DSP behavior.

### Reference points

- [Harbor ADR 0003](https://github.com/chris-arsenault/harbor/blob/main/docs/adr/0003-pure-closed-candle-strategy-core.md)
  keeps network, database, clock, broker, and UI effects outside its strategy
  decision.
- [Tsonu Music](https://github.com/chris-arsenault/tsonu-music) keeps timing and
  graph decisions in plain-data modules that can run without browser audio or
  graphics hosts.
- [Lindelion](https://github.com/chris-arsenault/lindelion) keeps effect crates
  host-neutral and treats VST3 and standalone packaging as adapters.

## Compile Flexible Inputs Into a Strict Runtime Form

Human-friendly authoring and runtime execution need different representations.
Authored configuration should remain descriptive and easy to change. A
compiler or validator should translate it once into the smallest form the
runtime needs.

This boundary lets an agent work in a rich authoring model without teaching the
hot path about prose, optional fields, unresolved names, or partially valid
state. Stable identifiers, immutable definitions, typed commands, and primitive
event records prevent consumers from inventing their own interpretations.

Untrusted persisted or network data needs the same treatment. Static types do
not validate a value that crossed a JSON boundary. Structural decoding should
establish its shape, semantic validation should establish cross-field
invariants, and only then should it become runtime state.

Multiple authoring modes remain safe when they converge on the same compiler.
Generated and hand-authored content may follow different rules of taste. They
should not bypass port compatibility, required inputs, cycle checks, resource
bounds, or identity resolution.

### Reference points

- [The Canonry Game](https://github.com/chris-arsenault/the-canonry-game)
  compiles names and gameplay concepts into stable identifiers and fixed-form
  kernel data before simulation.
- [Catalyst Castellum](https://github.com/chris-arsenault/catalyst-castellum)
  compiles authored content into an immutable definition and separately decodes
  and validates saved runtime state.
- [Tsonu Music](https://github.com/chris-arsenault/tsonu-music) routes generated
  and authored scenes through one typed graph compiler.

## Use a Small Kernel Only When Variation Is Real

A microkernel or plugin shape helps when a system has a small set of stable
invariants and many independently changing behaviors. The kernel owns
lifecycle, scheduling, type compatibility, resource bounds, and publication.
Extensions declare what they consume and produce without gaining a second path
around those rules.

This shape bounds context as well as behavior. An agent changing one extension
needs the kernel contract and that extension, not every implementation in the
catalog. A kernel edit is visibly cross-cutting and therefore triggers a wider
survey.

Plugin architecture is not a default. If the system has one consumer and no
identified axis of variation, the framework adds indirection, lifecycle state,
and compatibility work before it has a job. Small composable modules are a
default. A generalized extension surface must be earned by real variants.

### Reference points

- [Tsonu Music's visualizer plugins](https://github.com/chris-arsenault/tsonu-music/tree/main/frontend/src/visualizer/plugins)
  declare typed ports, capabilities, cost, lifecycle, and scheduling metadata;
  registration does not require a kernel edit.
- [Lindelion](https://github.com/chris-arsenault/lindelion) is the useful
  counterexample: it keeps a small host adapter and extracts shared crates only
  when concrete consumers need them, rather than introducing a general plugin
  framework.

## Preserve One Canonical Path for Each Behavior

Multiple entry points are safe when they converge on one implementation of the
rule. Parallel semantic paths drift because an agent fixes the path in front of
it and may never discover the others.

I prefer a pure implementation used in production over a production path plus
a mock-friendly duplicate. I prefer one command or service boundary over a
direct database path for “simple” callers. If another mode needs different
policy, that difference should be an explicit input or adapter rather than a
fork of the invariant.

### Reference points

- [Harbor](https://github.com/chris-arsenault/harbor) sends backtest, paper, and
  broker-facing decisions through the same strategy core.
- [Agents of Glass](https://github.com/chris-arsenault/agents-of-glass) makes
  its `glass` CLI the live state interface for agents, so prompts do not create
  alternate mutation routes.
- [Catalyst Castellum](https://github.com/chris-arsenault/catalyst-castellum)
  reuses one resolved placement decision across preview, execution, save
  validation, and rendering.

## Make Architectural Boundaries Executable and Helpful

Code written by models arrives faster than human convention can correct it.
The repository needs strict defaults that make the intended shape obvious and
reject violations close to the edit. OpenAI's
[Harness Engineering](https://openai.com/index/harness-engineering/) describes
fixed dependency directions, custom linters, structural tests, and remediation
text in failures as core parts of an agent-first repository.

I assign each property to the strongest mechanism that can observe it:

| Property | Preferred control |
| --- | --- |
| An invalid state should not exist | Type, schema, ownership rule, or narrow API |
| A dependency edge is forbidden | Project reference rule or structural lint |
| An API must pass through one policy point | Custom lint |
| A runtime contract must hold | Focused unit or integration test |
| A deployed behavior is claimed | Deployment and runtime evidence |

A failure should provide just-in-time help, not only rejection. It should state
what failed, why the rule exists, which path is allowed, and how to record a
legitimate exception. The severity should match the property. Bypassing a
security or dependency boundary is an error. A maintainability signal may begin
as a warning.

### An Allocation Boundary as Architectural Proof

An architecture test or analyzer becomes valuable when a physical project
boundary closely approximates the property being protected. A simulation
kernel in its own assembly can reject dependency edges, package references,
allocation-prone APIs, strings, LINQ, tasks, logging, file I/O, and floating
point before a scenario runs.

That result is stronger than executing one scenario and observing zero bytes:
the build checks every compiled source path against the named prohibitions. It
is still not a mathematical proof that the runtime can never allocate. Object
construction, boxing, compiler-generated state, and future unlisted APIs may
need a custom analyzer and a warmed runtime allocation counter.

The claim must match the mechanism. A banned-API and dependency gate proves
that listed routes are absent. A call-graph-aware analyzer can prove more. A
profiler can observe one runtime path. None should be described as proving the
others.

### Tests Should Protect Behavior, Not Yesterday's Syntax

Tests drift when they mirror an implementation, authored content, or the text
of a completed migration. An agent can then update test and implementation
together without preserving an independent fact. The extra file creates work
but little confidence.

My order of preference is:

1. Make the invalid shape unrepresentable through types, schemas, ownership, or
   a narrow command surface.
2. Enforce static boundaries in the compiler, project graph, analyzer, or lint
   configuration.
3. Use an architecture test for a stable property the build cannot express.
4. Use behavioral tests for observable contracts and integration between real
   components.
5. Use runtime telemetry and deployed checks for claims that exist only in the
   running system.

This hierarchy gives each fact to the layer that can observe it without
imitation. A no-import rule belongs in the build. A reconnect contract belongs
in an integration test. A latency claim belongs in runtime evidence.

### Reference points

- [Sulion](https://github.com/chris-arsenault/sulion) uses custom rules to
  prohibit direct authenticated `fetch` calls and forbidden layer imports; its
  diagnostics name the approved path.
- [Catalyst Castellum's architecture check](https://github.com/chris-arsenault/catalyst-castellum/blob/main/tooling/checkArchitecture.ts)
  reports forbidden dependencies and cross-layer cycles.
- [The Canonry Game kernel](https://github.com/chris-arsenault/the-canonry-game/tree/main/src/Engine.Kernel)
  combines project-reference restrictions,
  [banned symbols](https://github.com/chris-arsenault/the-canonry-game/blob/main/src/Engine.Kernel/BannedSymbols.txt),
  source gates, and architecture tests to protect its deterministic fixed-form
  hot path.
