---
name: feature-start
description: Plan a substantial feature, subsystem, port, or migration in Sulion. Establish scope, decisions, and milestones before implementation. Use for feature-planning requests; skip localized changes.
---

# Feature Start

Produce the feature contract and milestone plan. **plan-phase** expands one milestone just
before execution; its **EXECUTE-PHASE.md** prompt carries out that expansion. Keep these two
skills separate.

This workflow uses Sulion plans and retrieval. The maintained source is
`~/repos/ahara/skills/`; synchronize both complete skill directories to `~/.claude/skills/`,
`~/.codex/skills/`, and repository-vendored copies when updating them.

## Establish the plan

Read [sequence.md](references/sequence.md) for the shared Sulion lifecycle and recovery rules,
and [plan-grammar.md](references/plan-grammar.md) for the durable plan format.

1. Recover relevant prior decisions and existing plan state before starting another plan.
   Read applicable repository instructions, then the sources needed for the requested work.
   Identify affected producers, consumers, reusable components, and material gaps.
2. Recommend the smallest complete design that satisfies the requested behavior, durability,
   safety, and ownership boundaries. New abstractions, dependencies, or harnesses need a
   concrete requirement or consumer. Explain meaningful alternatives and trade-offs in the
   proposal; do not create scaffolds to make the plan look complete.
3. Record settled decisions, provisional assumptions, and deferred decisions separately.
   Ask only about user-owned choices that block the work being planned. A later choice can
   remain open when its owner, evidence trigger, and affected milestone are explicit. Use
   prior answers; do not require a ceremonial confirmation of a clear request.
4. Write coherent milestones with acceptance conditions and proportionate evidence. Include
   enough scope and interface detail to assess the design, but defer step-level expansion.
   Put the plan and subsequent expansions in one existing working document, or create
   `<FEATURE>-PLAN.md` at the repository's conventional location.
5. Publish or reconcile the matching Sulion plan with future implementation phases pending.
   Record its IDs in the document and the document path in the Sulion summary. Hand the
   selected milestone to plan-phase.

Document durable architectural decisions in existing records or ADRs when warranted by their
consequences and repository conventions. Alternatives can remain in the working proposal
before a decision is settled. A planning request authorizes the requested plan artifact, not
unrelated documentation edits or implementation.

## Completion

The plan is ready when the outcome, constraints, source evidence, milestone acceptance
conditions, and decision ownership are clear enough for the next phase. Unresolved future
decisions need not block independent work. Report the plan path, Sulion identity, next phase,
and any question that actually blocks it.

Stop after planning unless the user has already authorized execution. With that authorization,
continue through plan-phase rather than asking the user to invoke the next skill manually.
