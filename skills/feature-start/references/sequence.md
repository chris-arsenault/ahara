# The sequence, in detail

The eight stages of a feature-start. Each names what it produces and the rule that keeps it
honest. The order is load-bearing: research before questions (so you ask the right ones),
questions before design (so you don't design the wrong thing), design before docs (so docs
record a real decision), docs before the plan (so the plan can cite them).

## S0 — Frame & load conventions

Identify the target repo and any reference/source material (another repo, a spec, a C#
codebase being ported). Read the documentation surface first — README, AGENTS.md, CLAUDE.md,
the docs index, the ADR index. Extract and write down:

- the **canonical verification command** (e.g. `make ci`) — every phase exit gate references it;
- the **critical rules** (allocation contracts, size limits, branch policy, "don't add X");
- the **code map** — where shared code vs product code lives;
- naming and layering conventions.

*Output:* a one-screen "what I'm working with."

## S1 — Gather context (breadth)

Fan out. Use Explore or parallel Agents to sweep the relevant subsystems rather than reading
one file at a time. You are looking for: the contracts/interfaces the new work plugs into, the
reusable primitives that already exist, the test/verification harness, and the fixtures. For a
port or migration, map the source side too.

**The rule: verify against current code, not memory, not docs, not a recalled fact.** Docs
drift; memories are point-in-time. If a doc says a helper exists, open it.

*Output:* a context map that separates what already exists / overlaps from what is a gap.

## S2 — Research the hard parts (depth)

For the genuinely hard pieces (algorithms, dependency boundaries, realtime/perf constraints),
go deep. Decide, per piece, **reuse vs build-new**, and — critically — note where the intended
use **diverges** from how an existing primitive is used today (a filter reused in a new
context still needs new tuning). Surface the realtime/allocation/licensing risks now.

*Output:* a reuse inventory (reuse-as-is / reuse-but-retune / build-new) and a risk list.

## S3 — Clarify (pause for input)

Surface **only** the decisions that change the shape of the work. For each, give 2–4 concrete
options with trade-offs, as a structured multiple-choice question. Do **not** ask about things
you can verify yourself or that have a clear default — decide those and say so.

This is iterative: an answer can reshape the design and spawn the next question. Keep going
until no shape-changing decision is open. **This is a hard pause — do not proceed past an
unresolved fork by guessing.**

*Output:* recorded answers, each tied to the design choice it settles.

## S4 — Confirm understanding

Before designing, present the rough analysis: what you understand the goal to be, the scope,
the tiers/components, the approach. Get an explicit "yes, that's right." This is the cheapest
place to catch a misread.

*Output:* user confirmation.

## S5 — Thread cross-cutting constraints

Constraints often arrive one at a time, after the first sketch ("it must also stay
packaging-neutral", "tune for speech not music"). Each one is woven through the **whole**
design, not bolted onto one section. When a constraint rests on a fact — "the core must not
depend on the host layer" depends on what the host layer pulls in — re-verify that fact against
code. Constraints that will outlive the plan become durable rules (ADR / AGENTS critical rule),
not plan prose.

*Output:* each constraint reflected everywhere it applies, and re-verified where factual.

## S6 — Pre-create durable docs + structure

Once decisions are settled, make them durable and reserve the structure:

- **ADRs** for genuine trade-offs (a decision with real, rejected alternatives). One per
  decision, Context/Decision/Alternatives/Consequences.
- **Doc surface** updates — README, AGENTS code-map/critical-rules, docs index, backlog
  (future work as positive future-state), CHANGELOG (one curated line).
- **Directory structure** — reserve crate/module homes with READMEs describing intent.

Delegate all documentation-convention questions to the **repo-docs** skill; do not re-derive
them here. **CI-safety is mandatory:** a reserved home is a directory with a README, not a
half-built workspace member — confirm the build still passes (the dirs are not yet registered).

*Output:* ADRs, updated indexes, scaffolded dirs, a build that still goes green.

## S7 — Write the milestone plan

Emit the plan in the grammar from [plan-grammar.md](plan-grammar.md): numbered phases each with
an exit gate, a decisions summary table, `[DECISION]` tags, `[depends on]` markers where phases
order, and a Context / reuse-map section the executor re-derives from. Keep it at milestone
altitude — step-level file/test detail is `plan-phase`'s job.

*Output:* the written plan at the repo root.

## S8 — Decision register & handoff

Collate every `[DECISION]` into the summary table so the user can see, at a glance, what they
own and when. State that the plan is the single source of truth.

Inside a Sulion PTY, publish the milestones as the root plan (`sulion plan start`, one phase per
milestone, titles matching the plan file's headings). That plan outlives this terminal and is
what `plan-phase` branches from; the plan file stays the source of truth for detail. Outside a
Sulion PTY, skip it.

Stop. Execution begins when the user runs `plan-phase` on a phase.

*Output:* the decision register; a published root plan; a clean stop.
