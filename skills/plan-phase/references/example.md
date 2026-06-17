# Worked example

A feature-start plan had this milestone:

> ### M0 — Foundation
> - `lindelion-effect` trait crate: effect trait, params, state, latency, allocation-free
>   `process`; host-agnostic (pure-DSP deps only).
> - Shared fidelity-harness crate: general-signal battery.
> - Shared gap-fillers: envelope follower, saturation shaper, extracted STFT.
> - Validate end-to-end against Gain.
> - Exit: `make ci` green; Gain passes the general battery.

`plan-phase` expands it into steps. Note the greenfield red→green, the explicit files, the
plan-specified extraction step, and the `[depends on]` chain.

```
1. Create the lindelion-effect trait crate skeleton.
   - File(s): crates/lindelion-effect/Cargo.toml, crates/lindelion-effect/src/lib.rs,
     Cargo.toml (workspace members)
   - Reference behavior: host-agnostic effect contract per ADR-0013 — depends only on the
     pure-DSP crates; neutral primitives (sample-block process, indexed float params,
     byte-blob state, latency-samples).
   - Change: define the `Effect` trait and param/state types; register the crate as a
     workspace member. No effect implementations yet.
   - Verify: `cargo test -p lindelion-effect` compiles and a trait-object smoke test runs.
     Red before: crate/trait do not exist (does not resolve). Green after.

2. Add the allocation-free contract test for process.  [depends on #1]
   - File(s): crates/lindelion-effect/src/lib.rs (tests)
   - Reference behavior: ADR-0001 — no allocation on the audio thread.
   - Change: none to production code; add a test using `assert_no_allocations!` around a
     no-op effect's `process`.
   - Verify: the no-alloc test passes for a trivial effect; red before means the test/helper
     wiring doesn't exist yet.

3. Extract the allocation-free STFT out of lindelion-pitch-shift into a reusable module.
   - File(s): crates/lindelion-dsp-utils/src/stft.rs, crates/lindelion-pitch-shift/src/... (call sites)
   - Reference behavior: behavior-preserving extraction — the pitch-shift analyzer's existing
     STFT math is unchanged; only its home moves.
   - Change: lift the STFT into dsp-utils with preallocated scratch; point pitch-shift at it.
   - Verify: the existing pitch-shift fidelity/quality tests pass unchanged before and after
     (characterization). This is a plan-specified refactor, not new behavior.

4. Add the shared peak/RMS envelope follower.  [depends on #1]
   - File(s): crates/lindelion-dsp-utils/src/envelope_follower.rs
   - Reference behavior: attack/release follower (distinct from the synth ADSR already in
     envelope.rs); speech-tuned defaults are M1's [DECISION], so leave the timing constants
     as plain parameters here.
   - Change: implement the follower with no allocation in its hot path.
   - Verify: a step-input test shows the output reaches ~63% of target in one time constant;
     red before means the symbol doesn't exist.

5. Implement the Gain effect and run it through the general battery.  [depends on #1, #2]
   - File(s): speech/gain/Cargo.toml, speech/gain/src/lib.rs, Cargo.toml (members)
   - Reference behavior: linear gain with smoothed parameter; bypass == identity.
   - Change: implement `Effect` for Gain reusing dsp-utils smoothing.
   - Verify: the lindelion-fidelity general battery passes for Gain (finite, no-clicks,
     bypass-identity, latency-accurate, allocation-free).

Exit gate: `make ci` green; Gain passes the general battery.
```

The executor then runs the companion prompt ([../EXECUTE-PHASE.md](../EXECUTE-PHASE.md)) on
"Phase M0," doing only these five steps, in order, with red→green verification per step.
