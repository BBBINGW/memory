# BOOT — 2026/1836 fused overflow/boundary FBT gate

Date: 2026-10-30
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Session: 密码学 15.0 — Research Turn 9/25

Status:
PASS_FUSED_OVERFLOW_BOUNDARY_FBT_STATIC_GATE /
PASS_GENERAL_PRIME_A2BCLA_BOOTSTRAP_COUNT_5_TO_4_STATIC /
PASS_CONCRETE_L29_LEVEL_BUDGET /
PASS_AUTHOR_CODE_SEPARATE_DELTA_BOUNDARY_BASELINE /
NATIVE_CORRECTNESS_PRECISION_LATENCY_UNVERIFIED /
NOVELTY_PROMISING_NOT_ESTABLISHED

## Reprioritization

Turns 1-8 branches are treated as parked/closed/source-gated and are not restarted.
This turn selects a fresh whole-bootstrap bottleneck from supplied source 2026/1836:
Yuchen Wei, Kaisheng Ma, Mingyu Gao, Hongren Zheng,
FHE for ALU over Large Prime Moduli and Application to One-Round Threshold ECDSA.

Supplied durable source:
papers/supplied/2026-1836.pdf
Git blob SHA: 71ee2d857cd59bd83fe60316120be7a5f428905a
42 physical pages.

Author public implementation inspected:
RyanWei0224/FHE-ALU-ECDSA
commit 581846bf911b8e6bc94897d6567345066af22bed.

## Primary hypothesis

In the paper's 256-bit general-prime A2BCLA path, the prime-only overflow correction SP-MV-FBT (delta-LUT) and the subsequent packed boundary symbol-LUT do not fundamentally require two separate CKKS bootstrappings.

A single slot-parallel multi-value FBT whose input jointly encodes the bounded overflow A and the already-available binary digit b_i should produce exactly the symbol information needed by the existing parallel LCtoC and final mux, reducing the total prime A2BCLA count from 5 CKKS BTS to 4.

Cheapest falsifiers:
1. type failure: A and b_i cannot be jointly represented before the FBT without another bootstrap;
2. semantic failure: the boundary symbols need information not determined by (A,b_i,slot-index);
3. level failure: the fused input alphabet makes the FBT plus carry-lookahead exceed the source L=29 concrete budget;
4. prior-art/code collision: the author implementation already performs this fusion.

## Source baseline

Paper Section 3 power-of-two A2BCLA consumes 3 CKKS bootstrappings.

Paper Sections 4.2-4.3 extend to prime q by adding two prime-only FBT stages:
1. overflow wrap-around SP-MV-FBT producing binary representations d^(k) of correction candidates A_k;
2. packed symbol-LUT on (d^(0),d^(1),[d^(2)],b) followed by parallel LCtoC and final mux.

Total prime A2BCLA count is 5 CKKS bootstrappings.

For concrete experiments:
N=2^16, log Delta about 43, L=29, log QP about 1741, sparse encapsulated secret weight 32.
At n=256, GPU A2BCLA without A2A-I is about 426-432 ms for p/u/p25519 versus about 245 ms for 2^256.

## 1. Bounded overflow gives a 5-bit common input

Paper Lemma 2 gives:
A in [C0, C0 + 2K + 1].

With concrete K=15:
A' := A-C0 in [0,31].

The author code independently encodes this as a2bBits=5.

After the first LCtoC, the binary digit stream b is already available, and the source explicitly broadcasts A to all n digit slots before the prime delta-LUT.

Therefore each slot i can form, using only public power-of-two scaling/doubling and ciphertext addition:

z_i = A' + 32*b_i in {0,...,63}.

This is a 6-bit slot value. No secret-dependent operation or bootstrap is needed to form z.

The current author code already packs Boolean bits for its boundary LUT using repeated doubling/addition plus a public scaling-factor adjustment, so this packing operation is type-compatible with the existing representation. Exact finite-precision scale alignment remains a native verification item.

## 2. The current two FBTs are functionally composable

For correction candidate k, the current delta-LUT computes the slot bit

d_i^(k) = bit_i(A_k(A')).

Here A_k is a deterministic public function of A' and q. Author code BuildReducedCorrectionLUT confirms each slot position has its own public LUT of the 5-bit overflow input.

The subsequent boundary symbol-LUT forms

s_i^(k) = b_i + d_i^(k),

with s_i^(k) in {0,1,2}, and outputs two indicator symbols:

r_i^(k) = 1[s_i^(k)=1],
t_i^(k) = 1[s_i^(k)=2].

Author code m_lutPackedSymbolCoeffs implements exactly these two functions.

Since A' = z mod 32 and b_i = floor(z/32), both indicators are deterministic slot-wise functions of z alone:

r_i^(k)(z) = 1[b(z) + bit_i(A_k(A'(z))) = 1],
t_i^(k)(z) = 1[b(z) + bit_i(A_k(A'(z))) = 2].

Thus one SP-MV-FBT over input modulus 64 can emit the exact same 2*candidateCount symbol function sets.

## 3. Candidate digit ciphertexts need no extra FBT outputs

The downstream LCtoC needs both:
- the digit stream s_i^(k), and
- its special carry symbol.

But s is linearly recoverable from the two existing boundary indicator outputs:

s_i^(k) = r_i^(k) + 2*t_i^(k).

Therefore the fused FBT need not add new LUT-output families beyond the current boundary-LUT outputs.

At the implementation level, the current full-packing FBT exposes real-symbol and imag-symbol ciphertext outputs separately before they are complex-packed, so the candidate data streams can be cloned/formed by public linear combinations and the same symbol outputs can still feed LCtoC.

Output count therefore stays equal to the current boundary FBT: 2*candidateCount LUT sets (with the full-packing component duplication already handled by the existing evaluator).

## 4. Exhaustive semantic sanity check

Exhaustively enumerated all 32 values A', both b in {0,1}, and both possible per-slot correction bits d in {0,1}: 32*2*2 = 128 cases.

For z=A'+32b, decoding A'=z&31 and b=(z>>5)&1 and applying the fused predicates reproduces exactly:
r=1[b+d=1], t=1[b+d=2].

Result: 128/128 PASS.

This sanity check is independent of the concrete prime because the prime/slot dependence is wholly inside the public deterministic bit function d_i^(k)(A').

## 5. Fused FBT depth is 15 by the author's own scheduler

Author code GetFBTDepth computes:

FBT depth = normalized LUT polynomial depth + exponentialDepth + 2 double-angle levels.

The exponential polynomial coeff_exp_16_big_complex_46 uses normalized depth 6; the source comment states six polynomial levels plus two double-angle levels.

For order-1 Sparse-THI with interpolation modulus p, GetHermiteTrigCoefficientsSparseTHI has coefficient count

((2*order+1)*p)/2 + 1,

so maximum possible degree is 3p/2.

Current source cross-checks:
- delta-LUT p=32: degree 48; raw PS depth 7, normalized 6 -> total FBT depth 6+6+2 = 14, matching paper Table 2;
- close-prime boundary-LUT p=8: degree 12; normalized depth 4 -> total 12, matching Table 2;
- generic-three-candidate boundary-LUT p=16: degree 24; normalized depth 5 -> total 13, matching Table 2.

Fused LUT:
p=64, order=1, degree <=96.

Author GetDepthByDegree maps degree 60..119 to raw depth 8, hence normalized LUT depth 7.

Therefore:

fused FBT depth = 7 + 6 + 2 = 15.

The number of MV output functions changes arithmetic work but not this multiplicative depth because the evaluator shares the same exponential/power basis across output functions.

## 6. Concrete L=29 budget passes

For n=256, source Table 2 / Section 6.1 uses L=29.

After replacing the two prime-only FBT stages by the fused one, a conservative source-table level accounting for the final prime-specific stage is:

R2C: 3 levels
fused p=64 SP-MV-FBT core: 15 levels
carry-lookahead: log2(256)+1 = 9 levels
final mux: 1 level

Total = 3+15+9+1 = 28 <= L=29.

Therefore the fusion does not require increasing the paper's concrete CKKS multiplicative-depth parameter.

This accounting is deliberately at the paper's Table-2 abstraction level. The implementation helper internalBooleanToBooleanCustomSIMDLUTsFull internally owns its transform/ModRaise path; do not add the same transforms twice in a code-level schedule.

## 7. Author-code collision gate

The author repository contains EvalArithToBoolean1Boot, but it explicitly rejects all non-legacy rings and only supports ZRING_LEGACY_POW2.

The arbitrary-prime function EvalArithToBooleanAnyPrime still executes two distinct prime-only FBTs:

1. internalBooleanToBooleanCustomSIMDLUTsFull(ctOverflow, m_lutMulDeltaQCoeffs) [delta-LUT];
2. after materializing candidates and packing symbolInput, internalBooleanToBooleanCustomSIMDLUTsFull(symbolInput, m_lutPackedMaskedSymbolCoeffs) [boundary-LUT].

Repository searches for fused delta/boundary or prime 5-to-4 paths found no implementation of this composition at the inspected commit.

Thus the existing author code does not already realize the proposed arbitrary-prime fusion.

## 8. Bootstrapping-count consequence

Existing prime A2BCLA:
3 base A2BCLA BTS + 1 delta BTS + 1 boundary-symbol BTS = 5 BTS.

Proposed fused prime A2BCLA:
3 base A2BCLA BTS + 1 fused overflow-boundary BTS = 4 BTS.

Therefore:

GENERAL-PRIME A2BCLA CKKS BOOTSTRAPS: 5 -> 4.

This is an exact static algorithm-count result conditional on the finite-precision fused FBT implementing the specified LUTs.

## 9. What is NOT established

Not established in this turn:
- native correctness under CKKS approximation/rounding;
- output precision/noise parity;
- actual CPU/GPU latency improvement;
- memory/evaluation-key impact;
- whether p=64 Sparse-THI coefficient magnitudes create a precision problem at the paper's scale;
- controlled security re-estimation after any implementation parameter change;
- full novelty against all contemporaneous unpublished/very recent work.

The fused p=64 LUT is one level deeper than the current p=32 delta-LUT, but it removes an entire second bootstrap transform/ModRaise/LUT stage. Runtime benefit is plausible but must be measured, not inferred from bootstrap count alone.

## Scientific interpretation

This is a stronger surviving mechanism than a setup-only representation cleanup because it changes the online prime canonicalization pipeline.

The structural explanation is:
the first prime-only FBT materializes correction bits d^(k), but the second FBT only consumes those bits together with b to compute a public finite-state symbol. Since d^(k) itself is a deterministic function of the same bounded 5-bit overflow A, the intermediate ciphertext materialization is a representation artifact.

Equivalently:

(A -> d^(k)) then (d^(k),b -> carry symbol)

can be composed into

(A,b -> carry symbol)

within one 6-bit SP-MV-FBT.

This exactly fits the research philosophy's desired pattern: locate why an existing bootstrap boundary exists, prove the intermediate representation is not algebraically necessary, and remove it without changing the final relation.

## Verdict

PASS_FUSED_OVERFLOW_BOUNDARY_FBT_STATIC_GATE.
PASS_GENERAL_PRIME_A2BCLA_BOOTSTRAP_COUNT_5_TO_4_STATIC.
PASS_CONCRETE_L29_LEVEL_BUDGET.
PASS_AUTHOR_CODE_SEPARATE_DELTA_BOUNDARY_BASELINE.

NATIVE_CORRECTNESS_PRECISION_LATENCY = UNVERIFIED.
NOVELTY = PROMISING_NOT_ESTABLISHED.

## Decision

KEEP as a positive BOOT candidate.

The next decisive step should be a bounded source-compatible implementation gate in the author repository:
- add a p=64 fused SP-MV LUT precompute that composes BuildReducedCorrectionLUT semantics with the current boundary symbols;
- pack A' and b into z before the FBT using the existing level/scale alignment helpers;
- reconstruct candidate digit streams linearly from the two symbol indicators;
- reuse the existing LCtoC and mux unchanged;
- compare against EvalArithToBooleanAnyPrime on one 256-bit close-prime case first;
- require exact decrypted bit parity, no worse output noise gate, and phase timing separating removed delta/boundary work.

Do not expand to full ECDSA or general-prime parameter sweeps before this minimal native gate.

TOP_LEVEL_BOOT_FRONTIER_EXHAUSTED: false.
PENDING_PI_DECISIONS: none.
PENDING_CODEX_TASKS: none.