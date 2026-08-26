# Design as a Conversation Between Peers

[Back to the guide overview](../working-with-coding-agents.md)

> Throughout this article, “I,” “me,” and “my” refer to Chris Arsenault.

I get better product and design work when I treat the model as a peer in the
conversation, not as a servant waiting for a complete specification. I bring
the outcome, product taste, constraints, and final authority. The model should
bring investigation, synthesis, alternatives, disagreement, and a concrete
recommendation.

Peer does not mean equal authority. I still decide what is worth building and
whether to publish, deploy, spend money, or accept risk. It means the model has
a real intellectual job. If it only translates my proposed mechanism into
code, I lose most of what it can contribute as a product manager, designer, or
architect.

## I Build the Specification Through Conversation

I rarely begin with a large design specification. I usually begin with a short,
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
next. Neither work studies coding agents. Both explain why a design can emerge
through proposals, evidence, corrections, and revised representations instead
of arriving as a complete document before the work begins.

The model is one participant in that loop, and the repository is part of the
conversation. Current code can contradict an assumed capability. A trace can
invalidate a performance theory. A prototype can reveal that an interaction
which sounded coherent in prose is awkward in use. I expect the model to use
those materials to change the design, not merely to defend its first answer.

This approach requires continuity. When a proposal starts following only the
latest comment, I stop and ask for a consumer-by-consumer requirements map. The
model must reload the earlier decisions, name any contradiction, and produce
one design that accounts for the whole discussion. New evidence may overturn
an earlier choice, but it should do so explicitly.

## Familiarity Lets the Prompts Stay Short

I do not spend hours polishing individual prompts. My prompts are often quick,
informal, and written in the language already established in the project. I can
say “design first,” “pick this up,” “run the next phase,” or “take a step back”
because the surrounding system carries the stable meaning.

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

This does not make prompts irrelevant. A prompt still needs a discernible
outcome and authority boundary. “Review this” and “fix this” grant different
work. “Do not pause until complete” is safe only when the plan defines complete
and the environment defines which failures must stop. The point is that these
task-specific decisions can stay small because permanent concerns live in
permanent forms.

Mechanical protection also changes the tone of the relationship. I do not need
to threaten the model, repeat every prohibition, or demand ritual compliance.
The model can exercise judgment inside a boundary that software enforces. That
leaves the conversation free to focus on product intent, tradeoffs, and
evidence.

## I Own the Outcome; the Model Owns the Mechanism

My default division of labor is:

| I retain | I delegate |
| --- | --- |
| Outcomes and product taste | Repository investigation |
| Priority, cost, and risk | Requirements and acceptance criteria |
| Authority to publish, spend, or deploy | Product and interaction design |
| Material product choices | Architecture, code, telemetry, and tests |
| Final acceptance | Options, recommendation, execution, and verification |

I do not dictate an implementation simply because I can imagine one. I state
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

A question is not permission to start the next phase. A review is not
permission to repair everything found. A proposal written after the code
changed was never a proposal.

Explicit modes also protect attention. Sophie Leroy's experiments on
[attention residue](https://doi.org/10.1016/j.obhdp.2009.04.002) found that
attention can remain attached to an unfinished prior task and reduce
performance on the next one. Masicampo and Baumeister found that making a
specific plan for an unfinished goal can reduce its intrusive cognitive effects
in [Consider It Done!](https://pubmed.ncbi.nlm.nih.gov/21688924/). These studies
do not prescribe an agent workflow, but they help explain why explicit stops,
written plans, and resumable phases make collaboration easier to supervise.

## The Model Researches Before It Questions Me

Models often ask premature questions because asking is cheaper than
investigating. I reverse that incentive. Before surfacing choices, the model
reads repository instructions, the documentation index, architecture and ADRs,
the current implementation, affected consumers, verification entry points, and
relevant history.

The sequence is:

1. Frame the task and load the repository rules.
2. Survey the affected path broadly enough to find contracts, consumers,
   reusable components, and verification tools.
3. Go deep on the technically uncertain parts.
4. Classify what can be reused as-is, what needs adjustment, and what is new.
5. Ask only questions whose answers materially change the design.
6. Confirm the boundary before editing.
7. Record durable decisions, then produce the implementation plan.

Exploration does not need to wait for permission to think. The checkpoint comes
before the model locks the design or changes the system. This gives me a peer
with a recommendation rather than a form asking me to design the mechanism one
field at a time.

### Reference points

- Ahara's
  [feature-start workflow](../../skills/feature-start/references/sequence.md)
  encodes the research, decision, and planning sequence.
- Mitchell Hashimoto's
  [AI adoption notes](https://mitchellh.com/writing/my-ai-adoption-journey)
  describe a compatible attention boundary: the human chooses when to inspect
  background work rather than letting notifications choose for them.
