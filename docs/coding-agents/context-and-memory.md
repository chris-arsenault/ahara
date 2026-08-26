# Context Engineering as Information Architecture

[Back to the guide overview](../working-with-coding-agents.md)

> Throughout this article, “I,” “me,” and “my” refer to Chris Arsenault.

The best prompt cannot compensate for an incoherent information environment.
My context system includes repository instructions, current-state documents,
ADRs, plans, code, configuration, tests, runtime evidence, transcript history,
and the tools that connect them. The quality of the work depends on how those
parts represent the problem and expose the next relevant fact.

This has a close analogue in cognitive science. Zhang and Norman's
[representational analysis](https://doi.org/10.1207/s15516709cog1801_3) treats
many tasks as systems of internal and external representations. Edwin Hutchins'
[cockpit study](https://doi.org/10.1207/s15516709cog1903_1) takes the larger
socio-technical system, rather than one person's memory, as the unit of
analysis. David Kirsh's
[work on the intelligent use of space](https://www.sciencedirect.com/science/article/pii/000437029400017U)
shows how arranging a workspace can simplify perception, choice, and internal
computation.

A repository is a symbolic workspace. File names, directory boundaries,
indexes, stable identifiers, and visible state change what both people and
models can perceive and decide. Documentation is part of the working system,
not explanatory material added after the real work.

## Give Every Kind of Information One Job

I use this authority order when sources disagree:

1. System, organizational, and safety constraints.
2. The current request and its authorization boundary.
3. Repository-local agent instructions.
4. Current code, configuration, and observed runtime behavior.
5. Current-state architecture and operating documentation.
6. ADRs as records of rationale and accepted direction.
7. Plans and backlogs as future intent.
8. Transcript history and memory as recoverable context that still requires
   current verification.

Different information also has different lifecycles. Current-state documents
say what is true now. ADRs explain why a consequential choice was made. Plans
and backlogs describe work that has not landed. Changelogs describe shipped
behavior. Tests protect executable contracts. Combining these jobs in one
ever-growing document creates incompatible claims without a reliable way to
rank them.

My top-level instruction and documentation files are maps, not encyclopedias.
They name the repository, its major boundaries, the canonical validation path,
and the next documents to load. An agent follows links into more specific
material only when the task needs it.

OpenAI describes this form of progressive disclosure in
[Harness Engineering](https://openai.com/index/harness-engineering/): a short
`AGENTS.md` points into a structured, versioned knowledge base. Anthropic makes
a related recommendation in
[Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents):
find the smallest set of high-signal tokens and retrieve additional context
just in time.

## More Context Is Not Automatically Better

The
[Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/) experiments showed
that long-context models could perform much worse when relevant information sat
in the middle of a long input. Models have improved since those experiments,
but the design lesson remains useful: targeted retrieval and strong indexes are
safer than undifferentiated context dumps.

Human cognitive load theory supplies a related warning through a different
mechanism. John Sweller's
[work on problem solving and learning](https://www.sciencedirect.com/science/article/pii/0364021388900237)
showed that demanding means-ends search can consume capacity that would
otherwise support learning. Human working memory and model context windows are
not equivalent. The narrower parallel is enough: irrelevant search and poor
representations consume resources that could be used to understand the task.

This is why architecture, documentation, and search tools should bound the
working set before the prompt tries to describe it. The repository can expose a
small coherent subsystem. A documentation index can send the model to the
owning source. A structural search can find a definition and its consumers
without loading every file that contains the same word.

## Let Agents Search Their Own History

I give agents direct access to prior decisions and working preferences instead
of asking people to reconstruct them from memory. A rule that says “research
before asking” only helps if the model can search what happened in earlier
sessions. Without that access, each new conversation begins by asking the human
to rebuild context, scanning unrelated files, or guessing from the current
implementation.

Compaction and history search solve different problems. Compaction lets one
conversation continue. Search lets a new conversation recover a decision made
months earlier, or discover that a similar failure already produced a durable
rule.

I want history search to provide:

- repository scope by default, with deliberate widening across projects;
- lexical search for identifiers and semantic search for concepts whose
  wording changed;
- source session and turn identifiers so a result can be reopened in context;
- separate controls for user requests, reasoning, tool calls, errors, and
  low-value mechanics;
- explicit index freshness and failure state; and
- stable machine-readable output that other tools can consume.

The corpus needs curation. Decisions, concise reasoning, and statements of
intent are usually useful. Repeated file reads, raw diffs, command output, and
image payloads are usually better recovered from the repository or an artifact
store. Indexing everything makes similarity search noisier and spends context
replaying mechanics rather than decisions.

History changes the human role. I no longer need to remember where a decision
was discussed or restate the same preference to every fresh agent. The agent
can find the prior turn, explain what it thinks was decided, and verify that
conclusion against current code and documentation.

Retrieved conversation remains evidence of intent at a point in time, not proof
of current behavior. A useful search result names its source and uncertainty.
If the index has incomplete coverage, the agent should say so instead of
presenting one result as exhaustive.

## Code Navigation Needs the Same Epistemic Controls

An agent-facing source search should expose index freshness and confidence,
bound its output, and label a syntactic fallback instead of presenting it as a
semantic result. A symbol definition, its callers, and its dependency edges are
usually better context than every textual match for its name.

Search and editing should also retain separate authority. A tool may propose a
structural patch and show the diff without applying it. That preserves the
boundary between understanding a change and receiving permission to make it.

Tools are context engineering because they determine what evidence reaches the
model, in what representation, and with what uncertainty. Their interfaces
should be narrow enough that the agent can tell what a result proves.

### Reference points

- Ahara's
  [documentation principles](../../skills/repo-docs/references/principles.md)
  define progressive disclosure and assign distinct jobs to current-state
  documentation, ADRs, plans, and changelogs.
- [Sulion](https://github.com/chris-arsenault/sulion) is my reference
  implementation. `sulion-retrieve` combines lexical and semantic transcript
  search, returns source turns, scopes to the current repository by default,
  and reports indexing state. `sulion-code` provides bounded structural source
  navigation with confidence and fallback labels.
- [Sulion's agent instructions](https://github.com/chris-arsenault/sulion/tree/main/docs/agent-instructions)
  make both tools discoverable without embedding their operating manuals in
  each task prompt.
