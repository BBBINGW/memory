# BOOT RMFE Post-Raw Partial-Fusion Static Cost Ceiling

Date: 2026-10-31
Session: 密码学 16.0
Logical Research Turn: 3/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

This turn evaluates only whether the post-raw single-bootkey fusion surviving Turn 2 has enough **optimistic structural latency headroom** to justify one later timing gate.

No native candidate implementation, Codex run, cryptographic correctness experiment, DFR test, parameter sweep, or end-to-end benchmark occurred.

Parent:
- findings/boot-RMFE-post-raw-single-bootkey-envelope-gate-2026-10-31.md

Durable negative boundary preserved:
- findings/boot-RMFE-p5w512-commutation-boundary-2026-10-29.md
- pre-raw/full-path exact fusion remains KILLED.

## Primary hypothesis

For the published p=5, w=512, k=5 correction/trace-and-merge point, the narrower post-raw fusion has enough structural headroom that it cannot be killed before measuring the already-instrumented HElib timer shares.

Falsifier:
even under optimistic assumptions, the maximum eliminable middle-path work is insufficient to cross the previously established thin-throughput frontier.

## Source provenance

### Aung et al. ePrint 2025/350

Cached source:
- ePrint 2025/350
- PDF SHA256 922c860a838fd8c9a8a5853489ac8ac7706fc3332e2083075540ad5f422bde82
- VERSION_UNVERIFIED mirror, 30 physical pages.

Published p=5, w=512, k=5 correction/TnM process breakdown:

- SlotsToCtxts: 2.284 s
- MultKey: 4.732 s
- CtxtsToSlots: 0.078 s
- DigitExtract: 4.240 s
- total: about 11.33 s
- final capacity: 101
- thin-bootstrap throughput: 107.06 capacity*slots/sec

Thus, holding final capacity at 101, matching thin throughput requires

latency < 10*101/107.06 = 9.433962264... s.

### Pinned HElib source

Paper-pinned HElib:
homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

Relevant files:
- src/recryption.cpp
- src/EvalMap.cpp
- src/matmul.cpp

The source exposes separate timers:
- AAA_slotToCoeff
- AAA_bootKeySwitch
- AAA_coeffToSlot

Thin recryption source order is:

slotToCoeff
-> canonicalization/mod-down
-> reLinearize(recryptKeyID)
-> rawModSwitch
-> newMakeDivisible
-> divide by p^{e'}
-> ctxt = recryptEkey
-> multByConstant(zzParts[1])
-> addConstant(zzParts[0])
-> coeffToSlot.

For m=32768,p=5:
- phi(m)=16384
- ord_m(5)=8192
- nslots=2.

ThinEvalMap therefore has reduced dimension 2.
Its inverse CoeffToSlots applies the D=2 matrix transform and then traceMap.

At the pinned source, traceMap uses the binary branch when d=8192 and the strategy is not the short FULL case. Since 8192=2^13, the binary recurrence executes exactly 13 Frobenius automorphisms.

The previously persisted multi-output-hoist gate established the corresponding transform-side counts:
- per thin SlotsToCoeff: about 1 nonidentity automorphism;
- per thin CoeffToSlots: about 1 D=2 automorphism + 13 trace automorphisms = 14;
- across five branches: 5 + 5*14 = 75 transform automorphisms.

## Exact latency threshold for the partial fusion

Conservatively retain all published non-MultKey stages, including the 0.078 s final CtxtsToSlots even though a successful integrated recovery may later remove it.

Fixed outside-middle latency:

2.284 + 0.078 + 4.240 = 6.602 s.

To beat the thin-throughput frontier at capacity 101:

candidate_middle < 9.433962264 - 6.602
                 = 2.831962264 s.

Baseline MultKey is 4.732 s.

Required MultKey reduction:

1 - 2.831962264/4.732
= 0.40152953.

Therefore the post-raw candidate needs at least a

**40.15% wall-clock reduction of the published MultKey block**

if final capacity remains 101 and all other stage times are conservatively unchanged.

Equivalent required absolute saving:

4.732 - 2.831962264 = 1.900037736 s.

## Structural operation-count ceiling

Baseline five-way MultKey transform side:

- 5 thin S2C automorphisms;
- 5 * 14 = 70 thin C2S automorphisms;
- total transform automorphisms ~75;
- plus five branch-local canonicalization/reLinearize/rawModSwitch/newMakeDivisible preprocessings;
- plus five recryptEkey plaintext-polynomial reconstructions.

Post-raw candidate:

- retains the five thin S2C automorphisms;
- retains all five branch-local reLinearize/rawModSwitch/newMakeDivisible preprocessings;
- replaces five recryptEkey reconstructions by one exact post-raw reconstruction;
- replaces five thin C2S paths by:
  - RM10: 10 automorphisms;
  - exact R8 C2S BSGS map: 6 automorphism/key-switch calls;
- transform-side total ~5+10+6 = 21 automorphisms before any final RMFE adapter cost.

Therefore the exact known transform support drops approximately

75 -> 21,

a reduction of 54 automorphisms, or 72%.

This is an operation-count ceiling, not a runtime claim. In particular, the retained five reLinearize/rawModSwitch/newMakeDivisible paths could dominate wall-clock time and erase the required 40.15% saving.

## Decision

RESULT:
PASS_STATIC_COST_CEILING_NOT_KILLED

Reason:
- required wall-clock MultKey reduction: >=40.15%;
- exact known transform automorphism reduction: about 72%;
- therefore a plausible latency window remains;
- static information alone cannot determine whether retained nonlinear preprocessing consumes more than the allowed 2.832 s middle budget.

This is sufficient to keep the candidate alive for exactly one timer-share gate, but **not** sufficient to authorize a full candidate implementation or claim speedup.

## Cheapest decisive next test

Use the existing pinned HElib timers on the faithful baseline only.

Proposed task identifier:

BOOT-RMFE-POSTRAW-TIMER-SHARE-20261031-R3-01

Required output for p=5,w=512,k=5 correction/TnM:
- aggregate and per-branch AAA_slotToCoeff;
- aggregate AAA_bootKeySwitch;
- aggregate AAA_coeffToSlot;
- if possible, minimally split AAA_bootKeySwitch into:
  - canonicalize/modDown/reLinearize;
  - rawModSwitch;
  - newMakeDivisible/divide;
  - recryptEkey multByConstant/addConstant;
- no candidate implementation;
- no parameter sweep;
- no full Algorithm-5 rerun beyond the faithful baseline needed to collect timers.

Decision rule:
- if the retained branch-local preprocessing plus an optimistic lower bound for RM10/R8 recovery already exceeds 2.832 s, KILL post-raw fusion on latency ceiling;
- otherwise retain it for one bounded native correctness/timing prototype.

AI_PROVISIONAL_CHOICE:
RETAIN_POST_RAW_FUSION_FOR_ONE_BASELINE_TIMER_SHARE_GATE

INDEPENDENT_RESEARCH_AVAILABLE: true
RESEARCH_FRONTIER_EXHAUSTED: false
