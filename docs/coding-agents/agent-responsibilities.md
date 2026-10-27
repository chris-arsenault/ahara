# Separating Responsibilities in Agent Systems

[Practice index](../agentic-engineering.md)

Assign each behavior to the component that owns it. Interfaces, model
inference, execution, contextual resources, and domain state have different
jobs even when they share a process.

## System Responsibilities

| Part | Owns |
| --- | --- |
| Interaction | Starting, monitoring, and directing work through chat, developer tools, APIs, or events |
| Agent execution environment | Context assembly, model calls, permitted tool execution, and orchestration |
| Memory and skills | Relevant retained context and reusable task guidance, templates, scripts, or resources |
| Model inference | Generated text and structured requests from supplied context |
| Knowledge and domain systems | Retrieved evidence, authoritative business objects, domain rules, and authorized state changes |

The execution environment mediates model requests and tools. Actual execution
depends on available capabilities and the called system's authority checks.
A model request, remembered permission, or installed skill does not create
authority.

Active context supports the current call; history records an interaction;
persistent memory retains selected information beyond it. Refresh remembered
state when the decision depends on present reality.

## Distinguish Evidence From Actions

Retrieval supplies information for a claim. A domain action changes or requests
work under a business contract. The same protocol can carry both, but must
make their effects and authority clear.

A domain service can supply questions, save answers, and return source content
without making any model calls. Conversely, an inference service does not own
the business state merely because it proposes changes to it.

## Choose Agent Modes by Assignment

| Mode | Working relationship |
| --- | --- |
| Developer-supervised | Developer directs design and implementation in their chosen workspace |
| Interactive domain collaboration | A person investigates, develops, and directs work through domain tools |
| Background specialist | A scoped request or event supplies bounded inputs and expected outputs |

These modes do not dictate deployment topology. Interactive work can run on a
backend, and a headless process can still require human direction at a real
decision boundary.

Give each assignment explicit inputs, permissible actions, output, and
completion conditions. Keep implementation, accepting proposals, merging, and
deploying separately authorized. When a specialist is assigned analysis, its
result is findings or proposals, not implicit permission to perform those
other actions.

Keep personal coding credentials with their owner. Domain operations use the
acting user's or workload's authorized capabilities. Preserve input revisions
so late findings remain attributable and stale results can be recognized.

## Keep Product Ownership Clear

| Responsibility | Owns |
| --- | --- |
| Domain application | Shared records, rules, UI/API/tool interfaces, and authorized actions |
| Specialist execution | Job lifecycle, scoped access, progress, and attributed results |
| Delivery integration | Git/CI references, authorized releases, and actual execution outcomes |
| Project foundation | Maintained reference implementations, standards, and their adoption |

These are ownership boundaries, not a requirement for separate services.
Project foundation has a maintenance lifecycle; it need not be a runtime
component. Shared records should preserve meaningful contributions without
requiring every private conversation to be imported.

Use [domain-native work surfaces](domain-native-work.md) for application design,
and [meta-harness](meta-harness.md) for the environment around coding sessions.
