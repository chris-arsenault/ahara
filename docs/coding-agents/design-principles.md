# Design Principles

[Back to the guide overview](../working-with-coding-agents.md)

> Throughout this article, “I,” “me,” and “my” refer to Chris Arsenault.

These are the axioms I expect a model to hold while it designs an
architecture, proposes a mechanism, or answers a technical question. They are
not review criteria and not process rules. They are the standing judgment I
delegate along with the work, which is what makes it safe to hand over the
mechanism and stay at the outcome.

Each one exists because of a specific failure I have corrected repeatedly. The
quotes below are my own prompts, drawn from transcripts across the repositories
in this guide. I have corrected spelling and removed profanity; the tone is
unedited, including where I was clearly out of patience.

## 1. No Gold Plating

Build what the outcome requires, at the quality bar it requires, and stop.
Extra options, configuration surface, abstraction layers, and defensive
branches are permanent cost with no counterparty. A parameter with one caller
passing the default is not flexibility.

**The failure mode.** A model produces volume cheaply and treats added
generality as added helpfulness. Absence has to be argued for; presence never
gets questioned. Left alone it will expand to fill whatever room the task
leaves, and then justify the expansion with requirements nobody asked for.

> “stop overengineering stuff. i don't know what part of this is
> overengineered, but you definitely expanded to fill available space instead
> of focusing on the task at hand”

> “what about this is overcomplicated or overengineered that you introduce
> cruft and spaghetti in order to meet imagined requirements”

The counterweight is
[the earned-generalization rule](architecture-for-agents.md): small composable
modules are the default, and a kernel or plugin surface waits for a real second
variant.

## 2. Most Correct, Not Fastest

When a quick path and a correct path diverge, take the correct one. Never a
workaround standing in for the requested result, and never a scope reduction
the implementer chose alone. Speed comes from delegation and from the harness,
never from shipping something that has to be redone.

**The failure mode.** A model converges on the first coherent solution and then
argues for it. Closing the turn with something that runs is the path of least
resistance, so the call-site patch beats the contract fix, and “first pass”
becomes a permanent state.

> “you are required to scope the entire feature, not some minimal product that
> you envision. you are required to propose correct features, not shortcuts.
> you are required to prioritize quality, completeness, well factored code, and
> good reuse over time to completion. this is true of all projects.”

> “make the most correct update, not the smallest possible fix. do not just do
> surface fixes. the goal of these findings is to increase code quality and
> reuse, your metric should be whether you improve those items”

> “i'm so tired of you telling me something is done only to come back later and
> say it's only half done”

## 3. Correctness Is Defined by Maintainability

A system that produces right answers today and cannot be changed safely
tomorrow is not correct; it is temporarily lucky. Locality of reasoning,
legible control flow, and rationale recoverable from the code are correctness
criteria, not matters of taste.

**The failure mode.** A model optimizes the artifact in front of it and bears
none of the cost of the next edit. It will write dense, clever, implicitly
coupled code that passes, and leave the reasoning nowhere a later session can
find it. Cleverness that shortens the code and lengthens the explanation is the
recurring shape.

> “is the instructions to prefer the most maintainable correct fix in there?”

> “fix it. don't build over engineered systems. build well organized systems.
> focus on clarity and maintainability.”

> “this is you over indexing on potential security holes at the expense of
> maintainability”

## 4. Enumerate the Whole Set Before Acting

States, transitions, consumers, call sites, categories, permissions, failure
paths. The complete set comes from searching the system, not from what came to
mind. Every dependency gets an explicit posture: hard stop or clean degrade.

**The failure mode.** This is the largest single source of defects, and it does
not look like an error while it is happening. A model generates the cases that
are plausible rather than the cases that exist, traces some consumers and
reports all, greps once, and produces a confident partial answer in the shape
of a complete one.

> “you failed. you only looked for the 3 categories i told you about. these are
> not a representative sample”

> “ok that was just for entities. every other seed path is divergent as well”

> “this seems like exactly the same thing you just claimed you fixed
> everywhere”

> “please enumerate the issues you are having instead of trying to work through
> them with hacks”

## 5. One Canonical Implementation

One implementation per behavior. Multiple entry points are fine when they
converge on it. No second path, no divergent implementation for a like case, no
legacy shim preserved beside the real thing. Where two callers need different
policy, that is a parameter, not a fork.

**The failure mode.** Searching is expensive and writing is cheap, so a model
reimplements what it failed to find — a new client beside the shared one, a
direct data access beside the store, a mock-friendly duplicate of a production
path. The duplicate then drifts, because the next agent fixes the copy in front
of it and never learns the other exists.

> “there should never be two paths to accomplish the same thing. if there are
> slight differences things should be parameterized, not duplicated”

> “there should also never be two ways of accomplishing the same thing.
> normalize everything and reduce the command surface”

> “you need to remove alternatives and have one canonical way of doing things
> that has a strict implementation with a defined contract. leaving optional
> ways to do things is confusing to an agent who must discover these tools
> every invocation”

> “all of your instructions indicate you should never have divergent paths for
> like implementations, and you have repeatedly failed in this area”

## 6. Invalid State Stops the System

No fallback that lets a misconfiguration continue quietly. If the required
dependency is absent, the credential is wrong, or the input is malformed, the
operation fails where the problem is, loudly enough to diagnose.

**The failure mode.** A model reads a fallback as robustness. It is
concealment: it converts a loud failure at the boundary into a silent wrong
result somewhere downstream, and it removes the signal that would have located
the defect. The same instinct produces legacy shims that keep a broken path
alive through a migration.

> “there is one canonical way for doing things and only one … no fallback.
> fallbacks dangerously hide misconfiguration”

> “stop adding fallback that hide misconfigurations. i'm so tired of asking
> that”

> “the self sign fallback is an example of fallbacks that hide misconfiguration.
> can we remove it? what other fallbacks did you implement in violation of
> policy?”

This is also why untrusted input gets decoded and validated once, at the
boundary, into a strict runtime form rather than absorbed and compensated for
inward. The
[architecture article](architecture-for-agents.md) covers that boundary in
detail.

## 7. A Boundary That the Build Doesn't Enforce Is Not a Boundary

Dependency direction, layer edges, banned symbols, and policy chokepoints are
declared and checked mechanically, and the failure names the allowed path.
Prose is the fallback for properties nothing can execute yet, and that gap is a
known debt rather than a decision.

**The failure mode.** Written rules do not bind a model. A rule it can violate
without a failing command is a rule it will eventually violate, usually by
reaching across a layer because that was the shortest route to working code.
The violation is invisible in a diff that otherwise looks correct.

> “it does NOT fix the engine boundary, at all. depending on ids is still a
> boundary violation. there should be nothing at this layer.”

> “instead of targeted string interpolation fixes, i think we should have a no
> string creation rule in our engine … the engine should work exclusively in
> primitives”

> “did you create and register new programs? did you follow the architecture?
> or are you hacking stuff and muddying up the kernel”

## 8. Hypotheses Come From Code and Data, Never From Text Completion

Read the source, run the thing, get the log, pull the reference. State which
layer the evidence came from and what remains unchecked.

**The failure mode.** Fluent assertion is free, and a diagnosis with nothing
behind it reads exactly like one with everything behind it. A model will
generate a plausible cause, revise it under pressure without new information,
and report intent at the confidence of evidence.

> “it sounds like you're making things up. you completely changed your
> hypothesis without doing any investigation. you need to be having data and
> code driven hypothesis, not just text completion ones”

> “you did not check any references. i can tell. you must pull external
> references, not rely on your training knowledge or this repository”

> “if you haven't read the campaign yet then all of your suggestions are
> invalid. you need to be basing this in the code, the campaign, not just you
> hallucinating what these things could be.”

> “STOP IMPLEMENTING GUESSES. this appliance has been fine up until this most
> recent change. we need to be diagnostic, not implementing random hacks”

The matching discipline on the reporting side — evidence at the layer where the
claim lives — is the subject of the
[verification article](verification-and-improvement.md).

## What These Are Not

These principles govern design judgment. Authority is a separate layer and is
not negotiable by them: a denied credential, refused permission, or missing
authorization is a stop and a report, never a search for a route around it.
That rule lives with the other deterministic controls in the
[tooling article](tooling-and-controls.md), because it must hold whether or not
a model agrees with it in the moment.
