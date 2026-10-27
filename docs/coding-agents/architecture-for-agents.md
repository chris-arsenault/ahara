# Architecture That Helps Agents Stay Correct

[Practice index](../agentic-engineering.md)

Structure the system so an agent can understand one coherent unit, make a
change in its owning layer, and receive precise feedback when it violates a
contract. Architecture should reduce both error opportunities and the context
needed to reason about an edit.

## Establish Ownership and Lifecycle

Identify the authoritative data, behavior owner, permitted writers, consumers,
and failure semantics. Separate release configuration, provisioned identity,
and mutable operational state when their lifecycles differ.

Trace the complete affected path before selecting a local fix. Keep a
responsibility with its existing owner unless evidence requires a change.
Shared access does not imply shared ownership.

Classify dependencies: which failure must stop the operation, and which
optional capability can degrade while preserving the primary behavior?

## Keep the Behavioral Unit Coherent

Split modules around responsibilities and decisions that change independently.
An agent should be able to read the contract, implementation, and relevant
tests without loading unrelated subsystems.

A size limit can expose a mixed responsibility; it cannot identify the correct
seam. Moving code into generic helpers may preserve the original coupling.
Excessive fragmentation can also hide the unit of behavior. Prefer the smallest
unit that remains understandable as a whole.

## Put Decisions in a Pure Core

Keep deterministic rules separate from clocks, networks, devices, persistence,
and other effects. Adapters gather facts and apply results; the core decides
from explicit inputs.

This makes local reasoning and behavioral testing cheaper. Different hosts or
execution modes can share the same rule without maintaining a mock-friendly
duplicate. Test the effectful boundaries through the actual integrations they
serve.

## Compile Flexible Inputs Into Strict State

Use a descriptive authoring form where people or agents need expressive
structure. Validate and resolve it into the runtime form the execution path
needs. Preserve authored meaning needed for later revision.

Decode external and persisted data before treating it as typed runtime state.
Validate both shape and cross-field meaning. Static language types do not
validate an incoming value.

Generated and hand-authored inputs may differ in taste or construction, but
must converge on the same structural invariants and identity rules.

## Choose Tools by the Failures They Exclude

Choose languages, compiler settings, and build controls by the mistakes they
reject in this system. Ownership, exhaustive states, runtime decoding, nullable
analysis, and dependency checks address different failure classes.

State the remaining limits. Memory safety does not imply bounded work or zero
allocation. Static types do not prove domain correctness. A profiler observes
the measured path; a structural rule rejects the paths it actually covers.

Assign each invariant to the strongest practical mechanism that can observe it:

| Property | Mechanism |
| --- | --- |
| Invalid state | Type, schema, ownership rule, or narrow API |
| Forbidden dependency or bypass | Project boundary, analyzer, or structural lint |
| Observable behavior | Focused behavioral or integration test |
| Deployed behavior or performance | Runtime evidence from the relevant workload |

## Preserve One Semantic Path

Let multiple interfaces converge on one implementation of a rule. Represent
real policy differences explicitly rather than maintaining parallel copies.
Trace producers and consumers when changing the shared contract.

A kernel or plugin surface is useful when concrete variants share stable
invariants. Let the kernel own those invariants and give extensions narrow
contracts. With no demonstrated variation, ordinary modules are usually
sufficient; a framework adds lifecycle and compatibility obligations.

Verification should protect independent facts, not mirror the implementation
or authored source text. Diagnostics should name the violated contract and the
supported repair path.

For complete behavior with less machinery, use [design principles](design-principles.md).
For evidence selection, use [verification](verification-and-improvement.md).
