# BOOT — B169 audit and noise-aware Paterson–Stockmeyer aspect-ratio insight

Date: 2026-10-28
TRACK_ID: BOOT

## B169 artifact audit

Artifact:
\`BOOT-B169-B158-LT-NOISE-ATTRIBUTION-KEYFIX-20261028.zip\`

Reported and independently recomputed SHA-256:
\`a2d259d79fe30ea2c1185fa39eaefdae7199fdd71b6cf272c7e5d1157ef154cf\`

Internal SHA256SUMS:
- 26/26 listed entries PASS
- no mismatches

The packaged B168 parent source and B168 artifact hash are internally consistent.
The B168->B169 diff shows:
- raw-L18 LT key promotion now applies to attribution mode;
- every required LT Galois key is asserted to have LevelQ >=18;
- B167-equivalence control is executed first;
- attribution arithmetic is a single uninterrupted LT pass;
- instrumentation on the live path is limited to \`CopyNew()\`;
- intermediate noise probes happen only after FINAL_LT exact correctness is established.

Thus B169 is accepted as a valid noise-attribution experiment.

## Native result

\`STATUS = PASS_B169_LT_NOISE_ATTRIBUTION\`

All 15 required LT Galois elements have LevelQ >=18.

B167-equivalence control and single-pass attribution final output are byte-level behaviorally consistent in all three cases:
- exact final slots, 0/32768 mismatches;
- L18;
- identical required-logQ and budget in control vs attribution.

Budgets:
- CASE_0: 19
- CASE_1: 16
- CASE_2: 16

## LT noise attribution

Required-logQ deltas:

| Case | Total LT | Dense ct×pt masks | First-stage rot/add | Sum-columns | Final row |
|---|---:|---:|---:|---:|---:|
| CASE_0 | 34 | 22 | 1 | 11 | 0 |
| CASE_1 | 34 | 21 | 1 | 12 | 0 |
| CASE_2 | 35 | 22 | 1 | 11 | 1 |

CASE_2:
- PH_REP required=598, budget=51
- max LT term required=620, budget=29
- first-stage accumulator required=621, budget=28
- pre-row-swap required=632, budget=17
- final LT required=633, budget=16

Each of the 12 sum-column rotate/add steps adds at most 1 required bit; mean delta is 0.916667 bits.

Therefore:
\`DOMINANT_NOISE_SOURCE = DENSE_CTPT_MASKS\`.

The final row duplication is essentially free in noise.

## Why splitting the same dense masks is unlikely to help

The LT first stage is a fixed public linear map applied to the already-noisy baby-basis ciphertext. Decomposing an exact plaintext mask \(M=M_1+\cdots+M_t\) and summing
\[
M_1 C+\cdots+M_t C = MC
\]
does not remove the inherited linear error transformation \(M e\). Without an intervening refreshing/nonlinear noise-changing primitive, simple digit splitting/factorization of the same exact public linear map does not provide a principled reduction of the final inherited error.

Therefore the next priority should not be an ad hoc mask decomposition.

## New structural degree of freedom: PS aspect ratio

Let:
- polynomial degree bound \(D=2^d\);
- checkpoint \(K=2^c\);
- chosen baby-basis length \(H=2^h\);
- number of PS blocks \(s=D/H=2^{d-h}\).

For the checkpoint-decoupled construction:

1. main fused chain to \(S_H\): \(h\) ct×ct;
2. auxiliary chain from \(K\) to \(H\): \(h-c\) ct×ct;
3. author's MonomialGen-style grouped-power basis of length \(s\):
   \[
   2(\log_2 s-1)=2(d-h-1)
   \]
   ct×ct.

Total before the Algorithm-5 pointwise multiplication is therefore:
\[
h+(h-c)+2(d-h-1)=2d-c-2,
\]
which is **independent of the baby-basis exponent \(h\)**.

Adding:
- one Algorithm-5 pointwise ct×ct;
- one final leading-power square;

gives:
\[
2d-c
\]
ct×ct for the full power/evaluation skeleton, again independent of \(h\).

For the current case \(D=65536=2^{16}\), \(K=64=2^6\):
- pre-pointwise total = 24 ct×ct;
- full skeleton total = 26 ct×ct,

for any supported power-of-two baby basis \(H\) between checkpoint and the ring-layout limit.

This recovers the previously counted H=16384 result:
- basis/checkpoint path: 22 ct×ct;
- grouped-power generation for s=4: 2 ct×ct;
- pointwise: 1;
- leading square: 1;
- total: 26.

But it also predicts the same 26 ct×ct for:
- H=8192, s=8;
- H=4096, s=16;
- and other supported aspect ratios.

## Why smaller H is attractive

The current H=16384 basis enters LT with only about 50–53 bits in the hard cases, and the four-block LT costs 34–35 bits, leaving only 16–19 bits.

Stopping the checkpoint recurrence earlier gives a much cleaner basis:
B164 traces at x=1 had roughly:
- main k=8192 budget 89;
- aux k=8192 budget 109;
- main k=4096 budget 119;
- aux k=4096 budget 140.

Thus H=8192 or H=4096 can potentially buy tens of bits of LT input headroom **without increasing the total ct×ct count**.

The tradeoff is public-linear work:
- H=16384, s=4: 4 LT ct×pt, about 15 rotations;
- H=8192, s=8: 8 LT ct×pt, expected about 16 rotations under default BSGS;
- H=4096, s=16: 16 LT ct×pt, expected about 17 rotations.

Grouped-power generation grows as H shrinks, but exactly compensates the saved main/aux ct×ct count.

This gives a noise/performance tuning dimension unavailable in the original fixed H=16384 B158 design.

## Recommended next gate

B170 should be an aspect-ratio native screen, not another mask experiment.

Keep:
- k0=64;
- all cryptographic/security parameters;
- raw-L18 LT policy;
- corrected L18 Galois-key planning;
- same three fixed cases.

Test:
1. H=8192, s=8;
2. optionally in the same diagnostic binary, H=4096, s=16.

For each geometry:
- stop main/aux recurrence at H;
- construct repeated P_H via \(L_H=S_H-A_H\) and row duplication;
- run exact raw-L18 ParallelLT with s blocks;
- verify exact output;
- measure PH_REP and LT budgets;
- record ct×pt/rotation counts.

Do not yet build grouped powers or pointwise multiply.

Decision:
- prefer H=8192 if worst-case raw-LT budget is comfortably above ~30 bits;
- test H=4096 only if H=8192 is still marginal or if the linear-work increase appears acceptable.

## State

- B165 checkpoint robustness: PASS_STRONG
- B167 four-block LT: PASS_MARGINAL
- B168: INVALID_HARNESS_KEYPLAN
- B169 LT attribution: PASS
- dominant LT noise source: DENSE_CTPT_MASKS
- checkpoint-decoupled candidate: ACTIVE_NATIVE_CANDIDATE
- new subcandidate: NOISE_AWARE_PS_ASPECT_RATIO
- novelty: PROMISING_NOT_ESTABLISHED
