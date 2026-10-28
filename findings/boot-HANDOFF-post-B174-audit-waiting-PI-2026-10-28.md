# BOOT handoff — B174 audited; wait for PI on B175 candidate

Date: 2026-10-28
Research session: Cryptography 10.0, Research Turn 2/25

## Authoritative state

    TRACK_ID: BOOT
    ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
    LATEST_COMPLETED: B174_AUDIT
    NEXT_ITERATION: B175_CANDIDATE_PI_REVIEW; B175_NOT_STARTED
    CURRENT_STATUS: B174_AUDITED / WAIT_PI
    ACTIVE_GEOMETRY: H=8192, s=8
    ACTIVE_CHECKPOINT: k0=32
    RESULT: PASS_B174_SCALE_INVARIANT_GROUPED
    HEADROOM: MARGINAL
    EVIDENCE: RAW_AUDITED
    NOVELTY: PROMISING_NOT_ESTABLISHED
    FULL_ALGORITHM5_CORRECTNESS: NOT_ESTABLISHED
    END_TO_END_SPEEDUP: NOT_ESTABLISHED

Full audit:
findings/boot-B174-audit-si-grouped-marginal-and-pointwise-gate-2026-10-28.md

This dated handoff supersedes the prior B174_RUNNING / RESULT_NOT_YET_RECEIVED checkpoint. The prior B173 audit and running handoff remain historical evidence. No Codex/native task or B175 experiment was launched in Research Turn 2.

## Artifact and provenance

B174 ZIP SHA-256:
9232a9b3e57fe08adb0daf84c2bfe3183e4fb49a7de4695396720d96decfe4d8

29/29 internal manifest entries pass, with no missing/extra payload members or ZIP structural/CRC errors.

B173 parent independently anchored to the original ZIP:
1bff68640c185038868c34181c6d0d11bc057659cbde4b1c98cf90a204c4498c

B173 source and B174 parent bytes are identical:
f8f994f443f708be4de954f1d005d1cfe4f14404254ea352ae8860dd9c0d6125

B174 source:
769cd351b91b17e0843e32738459b27d1df459fbbe388f61f7233b3d5bcd2d89

Actual diff verified: 17 hunks, +349/-10; no hidden parameter, mask, comparator, secret, dependency, Rescale or DropLevel change in the grouped path. Original Step1 L19->L18 normalization remains outside grouped.

## Established result and limits

All three fixed cases pass all 12 grouped-stage probes: 36 unique records, 0/32768 decoded mismatches each, all at L18/logQ649. All 119 rows across 11 CSVs match raw logs and recomputed summaries/noise arithmetic.

GROUPED budgets: 15,14,15.
Minimum factors: 44.
Minimum ACC1: 47.
Max mask delta: 17.
Max accumulator SI delta: 30.
Final scale mod65537: 43178, independently reconstructed from Q_L18 modT=35478 and SI factor44421.

References, public masks, factors and accumulators were independently checked. Both nonzero test cases have y^4=1; no order-eight y / y^4=-1 is covered. There is no new general phase-robustness or DFR claim.

Actual ct-ct to grouped: 21 basis + 4 grouped =25.
Grouped ct-pt=3; grouped Rescale=0.
27 is projected 25+pointwise+leading, not an executed whole algorithm.

Eval-key BinarySize sum: 1011911360 bytes =965.0338745 MiB.
Galois levels: L14:5,L18:1,L19:11.
The stale L14 LT key plan is adequate only for the isolated endpoint. Before any all-L18 LT8 test, check/promote relevant keys; do not repeat B168's missing high-level-key diagnostic error. This is not the final complete-workload memory cost or RSS.

## Fixed source and security parameters

Upstream xiaopeng-stu/bfv-functional-bootstrapping, commit b113742d83d772fd0d1b353e72ac6e31f2838bea.
Lattigo v6.2.0 (local bfv alias actually imports schemes/bgv).
N=32768; m=1; degree=65536; T=65537; p=512.
LogQ=[36,34x18,30]; LogP=[34,34,34,34].
LWE n=2048; h=512.
No Q/N/T/p/secret/security relaxation is authorized.

## Pending PI decision: one B175 candidate only

Hypothesis: same-run checkpoint32 LT8 and B174 GROUPED can pass one exact L18 SI pointwise multiplication with positive headroom.

Cheapest gate if authorized: one existing CASE_1 (m=0,e=1,x=1); validate required LT keys at >=L18, build both inputs in the same context, multiply once, compare independent exact block-polynomial-times-power references, record scale/noise, and stop before later stages.

The 14-bit current headroom versus observed approximately30-bit SI increments makes failure a concrete risk; estimated 14-30=-16 is not a B175 result. No benchmark, leading/aggregation/extraction stage, phase sweep, k0=16, parameter rescue or pivot is authorized.

CURRENT ACTION: WAIT FOR PI. B175 NOT_STARTED.
