# Verification and Harness Improvement

[Back to the guide overview](../working-with-coding-agents.md)

> Throughout this article, “I,” “me,” and “my” refer to Chris Arsenault.

Generated code is cheap. Confidence is not. I ask the model to name the claim
it is making and choose evidence that can actually support that claim.

## Match the Evidence to the Claim

Different checks observe different layers:

| Claim | Evidence that can support it |
| --- | --- |
| A local behavior is correct | Focused unit or contract test |
| Components integrate in this checkout | Canonical repository validation |
| The release mechanism ran | CI or deployment log |
| Deployed configuration matches intent | Rendered plan, state, or configuration |
| A service is reachable and useful | Runtime query and user-visible path |
| A performance property holds | Trace, profile, benchmark, or production telemetry |

Those checks are not interchangeable. A green local suite does not prove a
deployment. A successful deployment does not prove that a service is reachable
or that its data path works. When CI or runtime logs are unavailable, the cause
of a failure remains unverified.

Verification should be proportionate. Every meaningful change needs evidence,
but not every one-line edit deserves a permanent test. A permanent test earns
its place by protecting a stable contract, invariant, security boundary, or
regression that would otherwise recur.

The model owns the telemetry needed to diagnose its work. If the stated outcome
cannot be measured with current instrumentation, it should propose or add the
smallest useful signal instead of asking me to invent fields I will never
inspect.

## Measure the Workflow, Not the Feeling

A 2025 randomized trial by Becker, Rush, Barnes, and Rein found that 16
experienced open-source developers working on 246 tasks with early-2025 tools
took 19 percent longer with AI while estimating afterward that they had worked
20 percent faster
([paper](https://arxiv.org/abs/2507.09089)).

That result does not define my current workflow. It studied earlier models, a
particular interface, developers with moderate AI experience, and a different
operating method. It does show that perceived speed is a poor measurement tool.
I look instead at cycle time, rework, escaped defects, operational outcomes,
and the ambition of work completed. Faster typing was never the outcome.

The same discipline applies inside a task. A plausible diagnosis is not a
finding. A test added after the implementation and observed only while green
does not prove it would catch the regression. A deploy that returned success
does not prove the requested route serves traffic. The agent should report the
evidence it actually obtained and the layer that remains unchecked.

## Improve the Harness When a Failure Repeats

Correcting one answer fixes one answer. Changing the environment that produced
the error can fix a class of future answers.

Depending on the failure, I may improve:

- `AGENTS.md` when a stable repository rule was missing;
- a current-state document when ownership or a boundary was hard to recover;
- an ADR when consequential rationale disappeared between sessions;
- a skill when a recurring workflow needed a repeatable sequence;
- a type, linter, or permission when an invalid action must be impossible;
- a test or CI check when a machine can observe the contract;
- a retrieval index when the information existed but could not be found; or
- a tool interface when the model could not act or observe precisely.

OpenAI's
[Harness Engineering](https://openai.com/index/harness-engineering/), Simon
Willison's
[Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering/),
and Armin Ronacher's
[agentic coding recommendations](https://lucumr.pocoo.org/2025/6/12/agentic-coding/)
all emphasize the surrounding specifications, tools, observability, and
verification rather than code generation alone.

The harness should remain legible. An agent can generate complexity faster
than a person can understand it. Cheap generation increases the value of clear
boundaries and small dependency surfaces. A permanent control should cost less
than the recurring failure it prevents.

Repository context cannot repair a model assigned the wrong job. A proposal
task needs product and design criteria. A review needs findings and evidence,
not silent repairs. A deployment task needs authority and runtime proof. The
harness should make those modes easy to state and hard to confuse.

## Failure Patterns I Avoid

I avoid these patterns because I have seen them produce weak work:

- giving the model a large context dump and hoping relevance emerges;
- asking it to implement before it can describe the current system and affected
  consumers;
- making it ask me for every technical decision after I supplied the criteria;
- treating a question, review comment, or speculation as authorization to edit;
- fixing something and then calling the completed change a proposal;
- letting the design follow the latest comment without reconciling earlier
  requirements;
- treating documents, plans, transcripts, or memory as stronger evidence than
  current code and runtime behavior;
- equating test success with deployment success;
- encoding an architectural property only in prose when the compiler, linter,
  permission system, or runtime can reject violations;
- keeping tests that mirror source syntax or completed migration scaffolding;
- running more agents than human attention can supervise;
- adding permanent process that costs more than the failure it prevents; and
- weakening an authority boundary to get an agent unstuck.

### Reference points

- [The Canonry Game](https://github.com/chris-arsenault/the-canonry-game)
  separates compile-time kernel restrictions, behavioral simulation tests, and
  runtime performance evidence instead of asking one suite to prove all three.
- [Sulion](https://github.com/chris-arsenault/sulion) combines transcript
  retrieval, structural navigation, plan state, brokered capabilities, and
  repository checks so repeated failures can move into the harness layer that
  owns them.
