# Design Principles

[Practice index](../agentic-engineering.md)

Choose the simplest maintainable implementation that satisfies the whole
requested outcome and its actual constraints. Simplicity concerns the mechanism;
completeness concerns the behavior. Preserve both.

## Principles for Choosing a Mechanism

| Principle | Apply it by |
| --- | --- |
| Build what the outcome requires | Require a concrete consumer or failure before adding generality, recovery machinery, configuration, or another service |
| Prefer correct, complete behavior | Repair the owning contract and its affected consumers; reject shortcuts that leave part of the requested behavior unfinished |
| Make future changes understandable | Use clear ownership, ordinary control flow, and recoverable reasons for consequential decisions |
| Enumerate the real affected set | Find states, consumers, entry points, and failure paths in the system; supplied examples do not define the whole set |
| Keep one canonical implementation | Route equivalent behaviors through the same rule; represent genuine policy differences explicitly |
| Expose invalid state at its boundary | Validate required inputs and dependencies; make failures diagnosable instead of hiding misconfiguration |
| Enforce stable constraints mechanically | Use types, schemas, dependency rules, permissions, or tests where they can observe the property |
| Derive hypotheses from evidence | Read the source, inspect the data, and obtain the log before choosing a repair |

## Simplify Without Cutting the Product

Before removing a mechanism, identify the user behavior or guarantee it serves.
Keep that behavior through a simpler implementation, or obtain direction to
change the requirement. A request to simplify does not authorize reduced
coverage, weaker durability, or loss of normal behavior.

Treat these as separate choices:

- **Durability:** which authored data and decisions must survive?
- **Recovery:** what must happen after interruption or partial failure?
- **Extensibility:** which current variations must the design accommodate?

Necessary persistence may be simpler than reconstructing prior state.
Durability alone does not require exact execution replay. Several domain
variants do not automatically require a general plugin framework.

Start with the existing platform and reference design. Explain the current
requirement that makes an additional mechanism necessary. Remove redundant
state, parallel paths, and speculative controls before weakening a required
contract.

## Calibrate the Boundary

Classify required and optional dependencies explicitly. A required credential
or malformed input must fail clearly; an optional telemetry service may degrade
without breaking the primary operation. An explicit degraded mode is different
from silently accepting invalid state.

Match controls to the system's actual risk. A performance goal calls for
measurement and optimization. It does not authorize runtime caps, hard budgets,
or forced user workflows unless those are requirements.

Bound investigative depth without inventing a smaller deliverable. If the
approach cannot meet the requested outcome, explain the conflict and reconsider
the mechanism before doing more of the same work.

For structural choices, use [architecture for agents](architecture-for-agents.md).
For adapting a plan, use [sustained intent](sustained-intent.md).
