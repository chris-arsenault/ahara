# Tooling, Capabilities, and External Work State

[Back to the guide overview](../working-with-coding-agents.md)

> Throughout this article, “I,” “me,” and “my” refer to Chris Arsenault.

Agents become more useful when they can search, edit, test, retrieve secrets,
operate deployments, and preserve plans without asking a human to translate
every action. Those capabilities also increase the cost of ambiguity. I pair
behavioral instructions with deterministic controls so the model can exercise
judgment without relying on perfect obedience for safety.

## Instructions Govern Judgment; Software Enforces Invariants

Global and repository-local instructions define the operating contract. They
tell the model:

- which actions an answer, review, proposal, implementation, or publication
  request authorizes;
- when to retrieve prior work and inspect owning documentation;
- how to navigate code and edit files without losing audit evidence;
- when multi-phase work needs a published plan;
- which deployment evidence is required before diagnosing a failure;
- when a credential failure must stop the task; and
- what working climate to expect: good faith, candor, and direct bad news
  over performed agreeableness.

These decisions require interpretation. A permission system can't infer
whether “what do you think?” authorizes an edit, and a linter can't decide
when a product choice should come back to me. Instructions give the model the
policy and the reasons behind it.

I keep those rules in version control and install them into each agent's
expected location. The maintained and installed copies are compared
mechanically. A source-to-install check is stronger than two files that are
“kept in sync” by convention, and it keeps an agent's live behavior connected
to reviewable repository history.

Instructions also make unfamiliar tools discoverable. A model won't guess the
name of a local transcript search, structural code index, credential broker,
or plan publisher on its own. The global file names the tool, when to reach
for it, and the boundary around its use, while the full manual stays with the
tool's own documentation.

Instructions alone can't enforce anything, though. A restriction that must
hold also belongs in permissions, hooks, types, schemas, build rules, or
runtime authorization. Anthropic's
[Trustworthy Agents in Practice](https://www.anthropic.com/research/trustworthy-agents)
similarly treats the model, harness, tools, and environment as distinct parts
of the safety system.

### Reference points

- Sulion's
  [tracked agent instructions](https://github.com/chris-arsenault/sulion/tree/main/docs/agent-instructions)
  are installed into the live Claude and Codex locations and checked for
  drift.
- The same instructions make `sulion-retrieve`, `sulion-code`, `with-cred`, and
  `sulion plan` available by name while leaving their detailed contracts with
  each tool's own documentation.

## Secure Agents With Narrow Capabilities

A secure agent environment should grant narrow capabilities instead of placing
powerful credentials in an ambient shell and asking the model to be careful.
Secret access should be explicit, time-bounded, attributable, and limited to
the child process that needs it. When two grants would collide on the same
variable name, the broker should fail the request rather than silently pick
one, and a denial should be machine-readable without revealing the value.

The mechanism and the instruction do different work here: the broker prevents
use without an active grant, while the instruction tells the model that a
denial means stop — without going on to search files, token caches, another
secret ID, or a broader cloud role.

The same principle applies to remote execution. Prefer typed requests over a
generic remote shell, and allowlisted container operations over unrestricted
Docker access. If a direct-Docker mode grants host-root-equivalent authority,
the interface should say so and reserve it for a machine whose trust model
allows that power.

Controls should state their real limit. A broker that injects credentials into
one child process protects them from ambient shell history and unrelated
commands. It does not necessarily isolate hostile same-user processes that can
inspect one another. Calling process-scoped access “terminal isolation” would
make the description more reassuring and the system less safe.

Narrow capabilities increase power as well as safety. When an agent can request
the exact credential bundle, deployment operation, or container action it
needs, it can continue routine work autonomously. The human handles grants and
material authority changes rather than copying secrets or relaying commands.

### Reference points

- [Sulion's secret-broker design](https://github.com/chris-arsenault/sulion/blob/main/docs/secrets.md)
  documents command-scoped environment injection, revocable grants, collision
  rejection, and the boundary between locked secrets and currently redeemed
  processes.
- [Sulion](https://github.com/chris-arsenault/sulion) exposes brokered node and
  container operations separately from its explicitly high-authority direct
  Docker mode.

## Make Plans External Working State

I plan enough to make work resumable and inspectable, then expand detail only
when the next phase is ready to execute.

A milestone plan records:

- the outcome and scope;
- decisions already made;
- dependencies between phases;
- a concrete exit gate for each phase;
- unresolved choices that require human input; and
- what remains unverified.

The next phase can expand into file-level steps, reference-correct behavior,
and exact checks. Expanding every phase at the beginning creates false
precision and stale instructions. Planning nothing forces the human and model
to reconstruct state after each interruption.

A plan publisher should expose compact phase state without exposing the
agent's private reasoning or requiring someone to read an entire transcript.
Phase status changes when reality changes, not in a ceremonial batch after the
work is already over.

Plans also let work stop cleanly. Masicampo and Baumeister's
[plan-making experiments](https://pubmed.ncbi.nlm.nih.gov/21688924/) found
that a specific, credible next action can release attention from an unfinished
goal. The model benefits too: a later context can reload the recorded state
instead of reconstructing it from compressed conversation.

Just-in-time phase expansion protects the plan from drift. The milestone says
what the phase must accomplish and how it exits. Current code, cited ADRs, and
the approved design still determine exact behavior when implementation begins.

### Reference points

- [Sulion's plan publisher](https://github.com/chris-arsenault/sulion)
  exposes phase names, status, notes, and history while the detailed execution
  plan remains with the working agent.
- Ahara's [plan-phase prompt](../../skills/plan-phase/EXECUTE-PHASE.md) treats
  the plan as the scope contract, rederives semantics from current sources, and
  stops at the named phase boundary.

## Reject Errors With a Useful Next Step

A deterministic control should teach at the moment of failure. A useful error
states:

1. what rule failed;
2. why the rule exists;
3. which path is allowed; and
4. how a legitimate exception is recorded.

This is just-in-time documentation. It keeps the durable explanation next to
the machine-enforced boundary without loading every rule into the model's
opening context. It also prevents a strict default from becoming a maze of
opaque failures and ad hoc bypasses.

The severity should match the property. A forbidden dependency, credential
route, or policy bypass should fail. A maintainability signal can warn while
the team learns whether it predicts real defects. Strict defaults remain
credible when they distinguish invalid systems from possible improvements.
