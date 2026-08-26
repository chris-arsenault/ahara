# Design as a Conversation Between Peers

[Back to the guide overview](../working-with-coding-agents.md)

> Throughout this article, “I,” “me,” and “my” refer to Chris Arsenault.

I get better product and design work when I treat the model as a peer in the
conversation. I bring the outcome, product taste, constraints, and final
authority; the model brings investigation, synthesis, alternatives,
disagreement, and a concrete recommendation.

Peer doesn't mean equal authority. I still decide what is worth building and
whether to publish, deploy, spend money, or accept risk. It means the model
has a real intellectual job. If it only translates my proposed mechanism into
code, I lose most of what it could have contributed as a product manager,
designer, or architect.

The model can name this boundary itself when it slips. In a Canonry Game
session, after I rejected a design document, it concluded: “I treated ‘design’
as ‘write my preferred answer and ask for approval afterward.’ That is not
designing it with you.” It reopened the phase, relabeled its document as an
unaccepted straw proposal, and we worked through the actual gameplay decisions
one at a time. A peer proposes and argues; it doesn't collect rubber stamps.

## I Build the Specification Through Conversation

I rarely begin with a large design specification — usually just a short,
informal prompt that names the outcome, the current pain, and the few
constraints I already know matter. The model investigates the system and
returns a first account of the problem. I correct it, add product judgment, or
challenge an assumption. The next answer should accumulate that shared
understanding rather than replace it with whatever I said most recently.

Clark and Brennan describe conversation as a process of establishing enough
common ground for the current purpose in
[Grounding in Communication](https://doi.org/10.1037/10096-006). Donald Schön
describes design as a
[reflective conversation with the materials of a design situation](https://www.sciencedirect.com/science/article/pii/095070519290020G):
each move changes what the designer can see and therefore what should happen
next. Both help explain why a design can emerge through proposals, evidence,
corrections, and revised representations instead of arriving as a complete
document before the work begins.

The model is one participant in that loop, and the repository is part of the
conversation. Current code can contradict an assumed capability, a trace can
invalidate a performance theory, and a prototype can reveal that an
interaction that sounded fine in prose is awkward in use. I expect the model
to use those materials to change the design, not merely to defend its first
answer. My favorite version of this came out of a Glass Frontier review, where
the model returned with: “You're right to push. I had read the store and the
selector, not the game. I've now traced the actual paths. Three things I
recommended don't survive contact with them.” That is the loop working —
evidence arriving mid-conversation and overturning the recommendations it
contradicts.

All of this depends on continuity. When a proposal starts following only the
latest comment, I stop and ask for a consumer-by-consumer requirements map. The
model must reload the earlier decisions, name any contradiction, and produce
one design that accounts for the whole discussion. New evidence may overturn
an earlier choice, but it should do so explicitly.

That rule comes from a real failure. During a world-generation redesign in the
Canonry Game, the model produced two successive designs by swinging between
“preserve everything” and “preserve almost nothing,” each an over-reaction to
my latest comment. My prompt at the time was blunt: “now i think you've
pendullumed. your not thinking your just responding to whatever i say.” The
recovery was not a third design. It was a neutral handoff document recording
the implemented baseline, the verified runtime consumers, both rejected
directions, and the unresolved decisions, so the next session could derive the
contract from the whole requirements picture instead of my most recent mood.
The durable fix then landed in that repository's agent instructions: feedback
is evidence to synthesize across the conversation, never an instruction to
invert the prior proposal.

## Intent, Exemplar Research, Distillation

One loop inside these conversations recurs often enough to deserve its own
name. I state an intent and the problem behind it. The model researches how
existing systems solve that problem — real exemplars, with named mechanisms
and sources. We distill the result into a document the design can cite, one
that survives the session.

The Canonry Game's world-spine exploration is the shape I mean. The intent:
the simulation produces 20 to 30 structurally equivalent factions, which gives
the player no static thread for grokking the world at a glance. The first
round of ideas earned only “intresting ideas, but none of them carry any
weight. theyre meaningless designations” — so instead of iterating on guesses,
the work moved into a research document: the problem statement, the
mechanics grand-strategy games use for the same cognitive-load problem (EU4
great powers, Victoria 3 rank, Stellaris council seats, Civilization 6 era
score), and what each would mean for this simulation. The document is marked
“Brainstorm. Not canon.” Its one job is to give the eventual design something
concrete to reason against.

The distillation step is what makes the research pay. A pile of links proves
the model searched; a distilled survey attached to the house's problem
statement is a design material. Later sessions cite it instead of re-running
the research, and disagreement can move from taste to mechanism — from “I
don't like these categories” to “which exemplar's tradeoff fits our
simulation.”

## Familiarity Lets the Prompts Stay Short

I don't spend hours polishing individual prompts. They're often quick,
informal, and written in the language already established in the project. I
can say “design first,” “pick this up,” “run the next phase,” or “take a step
back” because the surrounding system carries the stable meaning.

That economy comes from durable context:

- repository instructions define standing authority and safety rules;
- current-state documents explain how the system works;
- ADRs preserve consequential decisions and their rationale;
- plans expose the active outcome, decisions, phases, and exit gates;
- retrieval lets a new session recover earlier discussions; and
- types, linters, permissions, tests, and deployment controls reject violations
  of the properties I care about most.

The prompt therefore carries the present delta rather than the entire operating
manual. I can move quickly because a typo, compressed sentence, or omitted
reminder does not erase the repository's architecture or disable its security
boundary.

Prompts still matter. A prompt needs a discernible outcome and authority
boundary — “review this” and “fix this” grant different work, and “do not
pause until complete” is safe only when the plan defines complete and the
environment defines which failures must stop. The point is that these
task-specific decisions can stay small because permanent concerns live in
permanent forms.

Mechanical protection also changes the tone of the relationship. There's no
need to threaten the model, repeat every prohibition, or demand ritual
compliance. The model can exercise judgment inside a boundary that software
enforces, which leaves the conversation free to focus on product intent,
tradeoffs, and evidence.

## I Own the Outcome; the Model Owns the Mechanism

My default division of labor is:

| I retain | I delegate |
| --- | --- |
| Outcomes and product taste | Repository investigation |
| Priority, cost, and risk | Requirements and acceptance criteria |
| Authority to publish, spend, or deploy | Product and interaction design |
| Material product choices | Architecture, code, telemetry, and tests |
| Final acceptance | Options, recommendation, execution, and verification |

I try not to dictate an implementation just because I can imagine one. I state
what the system must accomplish, what must remain true, and what evidence would
convince me. The model should decide whether the answer requires a schema
change, a new abstraction, more telemetry, a smaller boundary, or no code at
all.

Kief Morris's account of
[human and agent engineering loops](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html)
distinguishes a human-owned “why” loop from an agent-run “how” loop. My practice
gives the model more of the middle: I expect it to help define affected users,
requirements, failure recovery, interaction states, rollout risks, and
acceptance criteria. I retain the outcome and the consequential product
choices.

The model should ask me about decisions that change the shape of the product or
system. It should not ask me to pick a tunable constant, logging field, internal
data structure, or other technical means it can evaluate from evidence. Asking
the human to choose every mechanism after receiving clear criteria turns a peer
back into a transcription service.

## I State the Work Mode

The same subject can require different behavior. “What do you think about this
authentication design?” and “replace this authentication design” may concern
the same files, but they grant different authority.

| Mode | Expected result | Authority granted |
| --- | --- | --- |
| Answer | Evidence-backed answer | Read only |
| Explore | Context, tensions, and possible directions | Read only |
| Propose | Recommended design and consequences | No implementation |
| Implement | Agreed change and verification | Scoped edits |
| Review | Findings by evidence and impact | No silent repairs |
| Publish | Reviewed external artifact | Named external action |

A question doesn't authorize the next phase, a review doesn't authorize
repairs, and a proposal written after the code changed was never a proposal.

Explicit modes also protect attention. Sophie Leroy's experiments on
[attention residue](https://doi.org/10.1016/j.obhdp.2009.04.002) found that
attention can remain attached to an unfinished prior task and reduce
performance on the next one. Masicampo and Baumeister found that making a
specific plan for an unfinished goal can reduce its intrusive cognitive effects
in [Consider It Done!](https://pubmed.ncbi.nlm.nih.gov/21688924/). That's part
of why explicit stops, written plans, and resumable phases make collaboration
easier to supervise.

## The Model Researches Before It Questions Me

Models often ask premature questions because asking is cheaper than
investigating. I reverse that incentive. Before surfacing choices, the model
reads repository instructions, the documentation index, architecture and ADRs,
the current implementation, affected consumers, verification entry points, and
relevant history.

The failure mode is easy to recognize once it has a name. In a Catalyst
Castellum design session I asked whether a batch of clarifying questions was
actually necessary, and the model's answer was: “No—they weren't needed. I
slipped into requirements-interview recursion. You've already supplied enough
to design the MVP.” Every question it had queued was answerable from the
constraints I'd already given plus sensible defaults. Asking felt like
diligence; it was actually the cheaper substitute for investigation.

The sequence is:

1. Frame the task and load the repository rules.
2. Survey the affected path broadly enough to find contracts, consumers,
   reusable components, and verification tools.
3. Go deep on the technically uncertain parts.
4. Classify what can be reused as-is, what needs adjustment, and what is new.
5. Ask only questions whose answers materially change the design.
6. Confirm the boundary before editing.
7. Record durable decisions, then produce the implementation plan.

Exploration can proceed freely; the checkpoint comes before the model locks
the design or changes the system. What I get back is a peer with a
recommendation rather than a form asking me to design the mechanism one field
at a time.

### Reference points

- Ahara's
  [feature-start workflow](../../skills/feature-start/references/sequence.md)
  encodes the research, decision, and planning sequence.
- Mitchell Hashimoto's
  [AI adoption notes](https://mitchellh.com/writing/my-ai-adoption-journey)
  describe a compatible attention boundary: the human chooses when to inspect
  background work rather than letting notifications choose for them.
