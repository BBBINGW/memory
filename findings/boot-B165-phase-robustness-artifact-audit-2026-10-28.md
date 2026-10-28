# BOOT — B165 phase-robustness artifact audit

Date: 2026-10-28
TRACK_ID: BOOT

## Artifact

Artifact:
\`BOOT-B165-B158-CHECKPOINT64-PHASE-ROBUSTNESS-20261028.zip\`

Reported SHA-256:
\`b731e40cdf2f3cc58db609ee150257a4e000f86e686dad0ab0074095eb840c76\`

Independent SHA-256 of the uploaded ZIP matches exactly.

All 24 entries in internal \`SHA256SUMS\` verify.

The packaged \`source/main.b164-parent.go\` SHA-256 is:
\`c639c57b6dad4fe6fe4593974bf058005527bbfb2b224b5933d2009f53d95f4a\`

This is byte-for-byte identical to the independently audited B164 source.

The two packaged copies of \`B164-to-B165.diff\` are byte-identical.

## Fixed parameters

- N=32768
- m=1
- r=32768
- degree=65536
- T=65537
- p=512
- Delta=128
- LogQ=[36,34x18,30]
- LogP=[34,34,34,34]
- LWE n=2048
- LWE h=512
- checkpoint k0=64
- last main stage=16384
- corrected RowRotation key L18
- selector scale one
- no selector/main/aux Rescale
- main and auxiliary ct×ct use MulRelinScaleInvariantNew
- no right selector after checkpoint
- no bootstrap/refresh

## Sweep construction audit

The source deterministically constructs exactly:
- category A: 7 special cases;
- category B: 12 message-center cases;
- category C: 16 error-boundary cases;
- category D: 32 unique seeded-random legal cases.

Random seed is fixed to 20261028 using Go math/rand. Duplicate (m,e) pairs and duplicates of earlier categories are rejected.

Total cases: 67.

The phase is computed as:
\[
x=(128m+e)\bmod 65537.
\]

The actual case list in \`deterministic-case-list.csv\` agrees with the source generator.

## Native result

\`STATUS = PASS_B165_PHASE_ROBUSTNESS\`

\`HEADROOM = STRONG\`

- total cases: 67
- pass: 67
- fail: 0
- every S16384/A16384/LH/PH_REP check is 0/32768 mismatches

Minimum per-case noise-budget statistics:
- min = 52 bits
- P10 = 53 bits
- median = 55 bits
- P90 = 56 bits
- max = 58 bits

Minimum final budgets across all cases:
- S16384: 53 bits
- A16384: 73 bits
- PH_REP: 52 bits

## Worst case

Worst case:
- case C007
- category C
- m=128
- e=-63
- x=16321
- k=16384
- object FINAL_PH_REP
- operation PH_REP_EQUALS_LH_PLUS_ROWSWAP_LH
- logQ=649
- required_logQ=597
- noise budget=52
- mismatches=0/32768

Late trace for C007:
- main at k=8192: required 566, budget 83
- aux at k=8192: required 544, budget 105
- M-selector for k=16384: required 565, budget 84
- fused main output k=16384: required 596, budget 53
- aux k=16384: required 575, budget 74
- final PH_REP: required 597, budget 52

Thus the 52-bit minimum is a real coefficient-noise headroom at fixed logQ=649.

## Control-flow invariance

For all 67 cases, operation counts are exactly identical:
- main fused ct×ct = 14
- auxiliary square ct×ct = 8
- total ct×ct to PH_REP = 22
- RowRotation = 14
- R selector after k64 = 0
- selector Rescale = 0
- fused Rescale = 0
- auxiliary Rescale = 0
- counts_ok = true for all 67

No plaintext-dependent branch changes the cryptographic algorithm.

## Interpretation

B164's x=1 result was not an isolated special-point artifact.

B165 gives strong empirical robustness evidence across structured special points, message centers, error boundaries, and deterministic random legal phases. The observed minimum budgets vary only modestly (52--58 bits), suggesting the checkpoint-decoupled mechanism has substantial margin at the fixed source parameter point.

This is still not an exhaustive proof over all 512*127 legal (m,e) pairs, so do not state universal input-domain correctness as a theorem. However, the evidence is strong enough to stop spending native runs on wider phase sweeps before integrating the downstream evaluator.

## State decision

- Original full co-packed B158: PARKED.
- Checkpoint-decoupled half-basis B158:
  - algebra: PASS
  - native mechanism: PASS
  - representative legal-phase robustness: PASS_STRONG
  - active status: ACTIVE_NATIVE_CANDIDATE
- Four-block half-basis ParallelLT: algebra PASS, native integration NOT_RUN.
- Full Algorithm-5 correctness: NOT_RUN.
- End-to-end speedup: NOT_RUN.
- Novelty: PROMISING_NOT_ESTABLISHED.

## Next gate

Proceed to B166: native integration of the four-block half-basis ParallelLT, while preserving the B165/B164 fixed parameters and k0=64.

B166 should first test only the lower-polynomial Algorithm-5 path through:
half basis -> 4-block ParallelLT -> grouped powers -> one pointwise ct×ct -> rotate-and-sum.

Do not add the leading x^65536 term or benchmark until this lower-path gate is correct and noise-feasible.

This isolates whether the modified Paterson--Stockmeyer geometry is natively compatible before adding the final leading-term branch.
