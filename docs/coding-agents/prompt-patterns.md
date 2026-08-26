# Reusable Prompt Patterns

[Back to the guide overview](../working-with-coding-agents.md)

> Throughout this article, “I,” “me,” and “my” refer to Chris Arsenault. The
> editorial agent is named explicitly when describing its analysis of the
> prompt archive.

The editorial agent reviewed my initiating prompts across product,
infrastructure, simulation, and creative-tool repositories. It excluded status
checks, corrections that applied only to the immediate conversation, and
publication commands such as “commit and push.” The archive spans multiple
agent tools, and its older sessions are indexed unevenly, so these are
recurring structures rather than a statistical ranking.

None of the wording here is magic. The value of each prompt comes from
specifying a work contract:

| Prompt field | What it establishes |
| --- | --- |
| Mode | Whether the agent should explore, propose, review, implement, or operate |
| Outcome | What should become true for a person or system |
| Evidence | Which code, documents, history, data, or runtime path the agent must inspect |
| Constraints | What must remain true and what is out of scope |
| Judgment | Which choices the agent should make and which require me |
| Persistence | Whether to stop at a design gate, phase boundary, or completion |
| Proof | What evidence closes the work |

I rarely put every standing rule into the task prompt. Repository instructions
hold stable constraints, skills hold repeatable workflows, and the plan holds
evolving execution state. The prompt supplies the current outcome and the delta
from those defaults. That layering keeps prompts short without making them
vague.

## Start a Non-Trivial Feature

This is the main product-and-design prompt. It begins with the pain and desired
capability rather than a proposed implementation. It grants permission to
investigate and design while withholding permission to edit.

```text
I want [outcome] because [current pain or missed opportunity].

The system needs to support:
- [capability]
- [capability]

Constraints and explicit non-goals:
- [property that must remain true]
- [work that does not belong in this first design]

Start in design mode. Inspect the current implementation, repository rules,
relevant ADRs and plans, affected consumers, and prior decisions. Identify
what can be reused as-is, what needs adjustment, and what is genuinely new.
Ask me only about choices that would materially change the product or system
shape. Then produce a phased plan with decisions, dependencies, and exit
gates. Do not implement yet.
```

In a repository with a mature workflow, I state the outcome and constraints,
then ask the agent to run the feature-start workflow. The longer form matters
when the environment does not already encode the sequence in a skill. Ahara's
[feature-start sequence](../../skills/feature-start/references/sequence.md) is
the reference implementation.

## Resume a Project With a State Audit

“Pick this project up” appears simple, but the implied task is broader than
reading the README. The agent must reconcile the checkout, prior intent,
current architecture, verification state, and deployment state before it can
recommend the next move.

```text
I want to pick this project up. Do a thorough state review before changing
anything.

Inspect Git history and the worktree, current architecture and runtime paths,
durable plans and ADRs, tests and canonical validation, deployment or release
state, and relevant prior sessions. Identify contradictions, unfinished work,
and material risks. Report what is verified, what remains uncertain, and the
recommended pickup order. Do not implement fixes.
```

This prevents the agent from treating the most visible backlog item as the
current priority or trusting a stale handoff over the code.

## Review Architecture Without Repairing It

A useful review prompt defines the target, evaluation axes, and their
calibration. It also says that finding a problem does not authorize a fix.

```text
Review [system, repository, or path] as it exists now. Do not make changes.

Evaluate it for:
- [specific boundary or quality]
- [specific failure mode]
- [specific operating concern]

Calibrate the review to [system stage, threat model, team size, or cost
constraint]. Trace findings to current code, tests, configuration, or runtime
evidence. Distinguish confirmed defects from risks and preferences. Report
findings by impact, with the affected path and a proportionate direction for
repair, in [chat or named report].
```

Calibration changes the answer. “SOLID where appropriate” asks whether the
principle improves this system. “Real risk to a single-person home network”
rejects theoretical security findings whose remedy would add more operational
risk than it removes.

## Review a Change Against Its Intended Contract

I use this after a commit or branch introduces a mechanism that should become a
general pattern. Reviewing only the diff can miss unwired consumers, and a
local patch can masquerade as architecture.

```text
Review [commit, branch, or diff]. The intended contract is [general behavior
and ownership boundary].

Trace every affected producer and consumer, including UI or operational paths.
Check that the new behavior is actually connected, failure states are handled,
and tests prove the contract rather than the implementation. Identify places
where the change remains a special case instead of the intended reusable
architecture. Report findings first; do not silently fix them.
```

## Investigate Before Changing the System

For performance, trading, simulation balance, reliability, and usage questions,
the first task is often to improve the evidence rather than the code.

```text
Investigate [question or hypothesis]. Do not change the system yet.

Use [authoritative data, runtime, trace, or experiment] over assumptions.
Define the measurement window and protocol before running it. Record the
hypothesis and result, separate observations from interpretation, and identify
what evidence would distinguish the remaining explanations. Recommend the next
experiment or decision after reporting the result.
```

Naming the no-change boundary keeps a plausible diagnosis from becoming an
unmeasured repair. Recording the hypothesis also prevents the next run from
quietly changing the question after seeing the outcome.

## Turn Findings Into Action Without Giving Away Product Decisions

After a review, I often delegate work by class rather than enumerating every
edit. The model can resolve repairs that preserve the current contract. It must
surface choices that alter behavior or product shape.

```text
Act on the findings.

- Implement mechanical fixes that have one reference-correct answer under the
  current architecture and product behavior.
- Enumerate product, gameplay, workflow, schema, or architecture changes that
  require a design decision before editing them.
- Measure or backlog claims whose cause is still uncertain; do not repair a
  hypothesis as if it were a confirmed defect.

Keep durable track of deferred work. Add focused verification for each fix and
run the canonical checks. Stop only when a real decision changes the shape of
the result or when the evidence cannot determine the correct path.
```

This grants substantial agency without pretending all decisions are technical.
It gives the model a default when a review mixes defects, preferences, and
unresolved causal claims.

## Execute One Plan Phase

One-phase execution is the bounded form. The written plan owns scope; current
code and cited decisions own semantics.

```text
Work Phase [N] of the plan, and only that phase, in the listed order. Treat the
plan as the scope contract, then rederive correct behavior from current code,
repository instructions, and cited ADRs.

For each step, make the named change plus required incidental plumbing, prove
the specified check fails before the change when practical, then make it pass.
Run the phase exit gate and report the actual result. Stop at the phase
boundary. Do not start later phases or invent adjacent refactors.
```

Ahara's fuller
[plan-phase execution prompt](../../skills/plan-phase/EXECUTE-PHASE.md) adds
the exact decision and verification rules. Stopping at the boundary makes
sense when I want to inspect the result or when the next phase depends on a
product choice.

## Execute the Whole Plan Without Routine Pauses

This was one of the clearest recurring prompt families. Variants repeatedly
said to execute phases in order, commit between them, make ordinary decisions
without review, and pause only for a blocker the agent could not resolve.

```text
Publish or attach the agreed plan, then execute every phase in order.

For each phase, expand it just in time, complete its verification and exit gate,
update the plan honestly, and create a checkpoint commit. Continue without
waiting for routine review. Make implementation decisions that preserve the
agreed outcome and constraints.

Stop only if a required decision would materially change the product or system
shape, a safety or authority boundary denies the action, or the available
evidence cannot determine a correct path. Otherwise continue until every phase
is complete, then run the final checks and report the result and anything that
could not be verified.
```

“Do not pause until complete” works because the prompt defines complete, the
plan exposes progress, and the stop conditions protect real decision and
authority boundaries. Without those parts, persistence becomes permission to
wander. Whether each checkpoint is committed, pushed, or kept local remains a
separate publication choice; the prompt should state it explicitly.

## Reconcile a Design After It Starts Chasing Recent Feedback

When an agent follows the latest comment, adding another local correction
usually makes the design less coherent. I ask it to reload the complete set of
requirements and rebuild one model that accounts for them together.

```text
Stop implementation. The proposal is over-weighting my most recent comment
instead of accumulating the design.

Review the full decision history for [subject], the current system, and every
affected consumer. List the requirements and decisions that still hold, name
the contradictions, and propose one coherent design that satisfies them
together. Explain any requirement you recommend changing. Do not edit until
the reconciled design is approved.
```

New evidence may still overturn the earlier direction; the requirement is that
the agent reconcile the whole problem instead of alternating between partial
answers.

## Operate Until a Verifiable Terminal Condition

Deployment and repair prompts need an allowed mechanism, a forbidden path, and
a terminal condition. “Work through errors” does not authorize bypassing the
system that owns state.

```text
Get [deployment, migration, or service] to [observable terminal condition].
Use only [approved mechanism] for writes; do not use [forbidden direct path].

Inspect the actual plan or logs, resolve verified in-scope failures, and keep
monitoring while the approved operation is still running. Stop on a credential
denial, an unavailable failure log, a destructive replacement outside scope,
or a decision that changes the authority model. Finish by checking [runtime or
convergence evidence] and report any layer that remains unverified.
```

Short prompts still have a role. “Continue,” “what remains,” and “commit and
push” move an already-defined task through state or grant a specific external
action. They can stay short because the repository, plan, and preceding
decision record already hold the work contract.
