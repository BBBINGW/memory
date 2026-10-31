# BOOT RMFE R4 Baseline-Timer Result Independent Audit

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 2/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

Audit only the delivered result for:

`BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01`

Origin: 密码学 16.0, Turn 5. Do not confuse its original generic/direct-recovery context with the current carry-compensated post-raw + rank-5 joint-recovery candidate.

The task was not rerun.

Current GitHub authority was read before judgment. At audit time, `BBBINGW/memory main` is
`de470943c14968efde0c657a856cf29877364a5f`, containing Turn-1 chained-Frobenius closure.

## Authority interaction

The original timer gate was defined in
`findings/boot-RMFE-post-raw-baseline-timing-decomposition-gate-2026-10-31.md`.

However, current authority
`findings/boot-RMFE-revised-static-latency-headroom-gate-2026-10-31.md`
explicitly supersedes the old Turn-4 retained-share hard-kill ratio.

Current middle-block budget at final capacity 101:

[
T_{middle}<2.909962264;s.
]

Current hard-kill reasoning must use unavoidable retained core plus minimum revised recovery, not the historical
(ho_{ret}ge0.5984704142) rule.

Therefore the Codex status
`PASS_BASELINE_RETAINED_SHARE_HEADROOM`
is a valid outcome under its original authorized gate, but is NOT itself a current-candidate latency PASS.

## Independent source audit

Pinned HElib:
`homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1`.

Independent source read confirms the stock `thinReCrypt` structure:

- `AAA_slotToCoeff`: slot-to-coefficient transform;
- `AAA_bootKeySwitch`: canonicalization/mod-down, reLinearize(recryptKeyID), rawModSwitch/divisibility handling, and boot-key reconstruction;
- reconstruction boundary occurs after division of the two raw parts and immediately before `ctxt = recryptEkey`;
- `AAA_coeffToSlot`: coefficient-to-slot transform;
- `AAA_extractDigitsThin`: later DigitExtract and excluded from the MultKey timing decomposition.

Thus the original proposed nested `AAA_preReconstruct` and `AAA_reconstruct` split is source-semantic and non-cryptographic if implemented at those boundaries.

## Delivered measurement sanity audit

Codex-reported configuration:
- fixed p=5,r=1,m=32768,w=512,k=5,bits=400;
- single-threaded;
- 5 warmups + 20 measured runs;
- no candidate implementation;
- no fresh-thin surrogate;
- no rescue/retry;
- 125 plaintext comparisons reported PASS;
- native exit 0.

Reported five-branch component medians:
- S2C = 0.03952 s
- pre = 0.16552 s
- reconstruct = 0.01899 s
- C2S = 2.86874 s
- T_MK reported = 3.09244 s

Independent arithmetic on component medians gives:

[
0.03952+0.16552+0.01899+2.86874=3.09277;s.
]

The 0.00033 s difference from the reported median T_MK is expected when the median of per-run sums differs from the sum of per-component medians; it is not an inconsistency.

Component-median proxy:

[
ho=(0.03952+0.16552)/3.09277=0.06629656,
]

consistent with the reported median over per-run ratios:

[
ho_{ret}=0.06649923.
]

Reported deterministic bootstrap CI:
[
[0.06619683,0.06678483].
]

Historical threshold:
[
2.831962/4.732=0.598470414201ldots
]

independently recomputes correctly. CI upper bound is about 8.96x below that historical threshold.

Therefore the statistical decision is internally coherent for the ORIGINAL gate.

## Current-candidate reinterpretation

Turn 13/14 changed what work is actually retained.

The old `pre` interval includes some work no longer retained five times in the current candidate (notably divisibility-lift/divide handling that was compressed via post-raw carry aggregation). Therefore

[
T_{S2C}+T_{pre}
]

is not the exact current unavoidable core.

It is instead a conservative over-inclusive proxy for the branch-local retained side.

Using component medians only as a non-rigorous sanity proxy:

- S2C share: 1.28% of decomposed T_MK;
- pre share: 5.35%;
- reconstruct share: 0.61%;
- C2S share: 92.76%.

This is scientifically useful: the baseline inverse/recovery transform dominates the measured MultKey decomposition, exactly where the current candidate applies its strongest structural reduction (post-raw recovery 70 transform terms -> 14).

At C=101, current middle budget is 2.909962264 s. Subtracting the over-inclusive median proxy S2C+pre = 0.20504 s leaves about 2.704922264 s for revised recovery/new work. This number is ONLY a median-scale sanity indicator, not a per-run bound, because the raw run arrays are not independently available in this audit.

Thus the delivered data strongly support continuing to a current-candidate recovery-cost measurement, but do not prove end-to-end latency gain.

## Artifact / SHA-256 audit boundary

The transport reports the following primary digests:

- final ZIP (two paths): `39da6c60f46373f8ec2c88324f0c90811a91ba7a390d53c3b4004e56d775d458`, 35844 bytes;
- `manifest.json`: `65719b6fe8d7bbbb094ca2e100b630cd9e159e7ae284eb97d07376d46c4d1b7f`;
- `SHA256SUMS`: `2493aef590ca43a32313ee9ca88ca86edcb604c5d655155400231d696fcdcbac`;
- `result.json`: `2b0fb96e2a7e439f23b386eb346db688107fb66f4c4618b40c6d30e2eaca4f9a`;
- `native-run.log`: `03e938ac48935c6487e193afda62e34bc84781dbfb33c1eea0576082458423d7`;
- `native-run.exit-code`: `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3ab86aa`;
- `benchmark.cpp`: `63e4d9db3ebcccc099949b6d20b1d5581ab215872056e995c72c388e3793f9d3`;
- `helib-timer.diff`: `3d43b50020939981818e1e172a0d4abd0e518c05dfe4e6b82c305361ad43056c`;
- built benchmark binary: `b884f1e81f363a1c203c4f0dc01adafcd8f246ebe9d80ac02a5450898ddc142d`;
- local built/installed `libhelib.a`: `0bf39bad5c92e267694de7e067aaa960384c14f64c5e5d9044eca9ecd77dc4b1`;
- R24 reference canary: `0f27d3ed7375fa7b9402cf3c0fd8ae7c4da242a2c552447edb9a2b2569beed95`.

All repeated digests in the transport are textually consistent.

But the ZIP and its files are not mounted in the current conversation container and are not discoverable in ChatGPT Library/conversation files. The absolute `/Users/bingwu/...` paths belong to the originating Mac runtime and are not readable here.

Therefore NO artifact digest can be honestly marked BYTE-RECOMPUTED in this audit. The remaining hundreds of transport-listed digests are likewise `REPORTED_NOT_RECOMPUTED`; the 213 digests omitted from the transport are not auditable at all from this session.

This blocks a full independent provenance PASS.

## Independent classification

```text
CLASSIFICATION:
  UNCLEAR

WHY_NOT_PASS:
  RAW ARTIFACT BYTES NOT ACCESSIBLE FOR INDEPENDENT SHA256 / SOURCE / TIMER-DIFF AUDIT
  CURRENT AUTHORITY SUPERSEDES THE OLD 0.5984704142 DECISION RULE

ORIGINAL_GATE_STATISTICS:
  INTERNALLY CONSISTENT / WOULD PASS ORIGINAL TURN-4 RULE

CURRENT_CANDIDATE_INTERPRETATION:
  STRONG POSITIVE HEADROOM SIGNAL
  BASELINE C2S DOMINATES DECOMPOSED MIDDLE COST
  NO CURRENT LATENCY KILL

CURRENT_NATIVE_LATENCY:
  NOT ESTABLISHED

CURRENT_WHOLE_PIPELINE_CAPACITY:
  NOT ESTABLISHED

DFR:
  NOT ESTABLISHED

PUBLISHABLE_NOVELTY:
  NOT ESTABLISHED

DO_NOT_RERUN_R4:
  TRUE
```

## Next cheapest decisive test

Do not benchmark the obsolete generic R8->RMFE four-output route.

The next latency test should target the CURRENT surviving recovery:

1. one common recryptEkey reconstruction;
2. RM10;
3. the Turn-1 chained rank-5 joint recovery using four direct j=1 Frobenius key switches;
4. required public multipliers/accumulations;
5. minimal aggregate/carry-side CPU work required at the post-raw boundary.

Measure this bounded recovery against the current C=101 middle budget 2.909962264 s, preferably from the same source-faithful post-raw state.

In parallel, whole-pipeline capacity still requires runtime instrumentation at the six DigitExtract y-u/divideByP boundaries established by Turns 22-23.

No new generic direct-four-output branch should be reopened.
