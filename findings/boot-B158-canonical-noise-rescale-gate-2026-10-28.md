# BOOT-B158 — canonical-mask and deferred-rescale noise gate

Date: 2026-10-28
TRACK_ID: BOOT
Parent: B158 formal recurrence / optimality finding
Status: PAPER_LEVEL_NOISE_GATE_PASS_CONDITIONAL / NATIVE_REQUIRED

No Codex, GPU, remote server, or native FHE execution was launched.

## Question

Does B158 introduce a new paper-level precision/noise blocker because its
0/1 selector plaintexts are multiplied without an immediate rescale?

Earlier prescout used coefficient l1/l2 norms only. This finding replaces that
proxy with the exact canonical-embedding norm relevant to the Zheng-Li-Wang
BGV noise lemmas.

## Exact encoder reconstruction

Pinned implementation:
- xiaopeng-stu/bfv-functional-bootstrapping
- Lattigo v6.2.0
- 9-bit case: N=32768, T=65537

The exact Lattigo batching map was reconstructed from:
- bgv/encoder.go permuteMatrix(logN)
- the negacyclic inverse NTT over T
- primitive 2N-th root convention used by Lattigo

Sanity check:
the physical first-half slot selector encodes to exactly two nonzero centered
polynomial coefficients, matching the earlier independent reconstruction:
- coefficient 0: -32768
- coefficient N/2: 128

Hence the reconstruction is source-consistent.

The centered integer polynomial lift was then evaluated at all complex
primitive 2N-th roots to obtain the canonical norm

||f||_can = max_j |f(zeta^(2j+1))|.

## Exact canonical norms

Physical half selector L (or R):
- log2 ||L||_can ~= 15.0000

Original 2026/975 Algorithm-3 masks C_i, m=1, r=32768:

selected values:
- i=1:  log2 ||C_i||_can ~= 16.788
- i=5:  ~= 18.716
- i=9:  ~= 21.164
- i=11: ~= 22.142
- i=12: ~= 22.648
- i=13: ~= 23.181
- i=14: ~= 15.000

Maximum observed original bit-mask norm:
- log2 max_i ||C_i||_can ~= 23.181

B158 regular-doubling masks M_k, which select the high k-subblock only in the
first physical half:

- k=2:    log2 ||M_k||_can ~= 15.869
- k=32:   ~= 18.321
- k=512:  ~= 20.932
- k=2048: ~= 21.667
- k=4096: ~= 22.283
- k=8192: ~= 22.733

Maximum observed B158 new-mask norm:
- log2 max_k ||M_k||_can ~= 22.733

Therefore:

max B158 selector canonical norm
<
max selector canonical norm already present in Algorithm 3.

This overturns the earlier concern based only on the loose coefficient-l1
upper bound (~2^28).

Decision:
- NEW_SELECTOR_CANONICAL_NORM_BLOCKER: NOT_FOUND
- B158 does not introduce a larger worst canonical selector than the original
  power generator already evaluates successfully.

## Secret distribution correction

The 2026/975 ParametersLiteral does not set Xs.

Pinned Lattigo v6.2.0 therefore uses:
- rlwe.DefaultXs = ring.Ternary{P: 2/3}
- i.e. uniform ternary / expected nonzero density 2/3

Do NOT substitute the final extracted LWE secret's h=512 into the BFV/RLWE
noise model.

The Zheng-Li-Wang 2023 BGV lemma used for a conservative cross-check assumes a
fixed-Hamming-weight HWT(h) secret. It therefore does not match the current
Lattigo secret exactly.

If one pessimistically substitutes h=n=32768 only as an upper-envelope sanity
check, with p=65537:

B_scale = p(sqrt(3n) + 8 sqrt(nh)/3)

has:
- log2 B_scale ~= 32.42

Using h=2n/3 as a density proxy gives:
- log2 B_scale ~= 32.13

At the top of the 9-bit polynomial chain, the same lemma gives a key-switch
term around:
- log2 B_ks ~= 23.1

The polynomial-stage primes are mainly about 34 bits.

Thus the generic theorem is extremely conservative in this parameter regime;
its rounding term is already within roughly two bits of one intermediate prime.
It is not a tight tool for distinguishing B158 from the already-working
Algorithm 3.

## Critical implementation fact: rescale really divides noise

Pinned Lattigo BGV Evaluator.Rescale explicitly documents and implements:

- divide/round by the last Q prime;
- divide the noise by that last prime;
- consume one level.

So the real B158 question is exactly the effect of delaying one
plaintext-selector normalization until the following ct-ct multiplication.

## One-prime pipeline shift

This is not fourteen independent missing rescales accumulating in series.

For the full-row r=32768 power generator with polynomial input at L18:

Original Algorithm 3:
- output power basis: L2

B158:
- output power basis: L3

At every corresponding nontrivial basis-width after the first fused step,
B158 carries one extra Q prime relative to the original accumulator path.

Thus B158 should be viewed as a one-prime pipeline shift:
- the selector factor is kept one level higher;
- the immediately following fused ct-ct multiplication performs the only
  rescale for that round;
- the one additional prime remains available throughout the pipeline.

This does not prove the same noise ratio, because multiplication cross-terms,
plaintext canonical norms of the encrypted state, and key-switch noise matter.
But it rules out the incorrect model in which B158 simply omits fourteen
independent 34-bit noise reductions while keeping the same modulus state.

## Source-level precedent for deferred normalization

The current 2026/975 implementation already contains an experimental
deferLTPostRescale policy for another Algorithm-5 product.

Its source comment states that BatchLT output can be left unnormalized and the
following ct3*ct2 ciphertext-ciphertext multiplication performs the single
rescale, provided the operands are evaluated at the same level.

This is not a correctness proof for B158, but it confirms that
"defer a plaintext/linear-stage normalization into the immediately following
ct-ct multiplication" is a supported implementation pattern in the same
Lattigo/BGV pipeline.

## Consequence for the one-Q-prime candidate

The previous one-Q-prime reduction remains algebraically/level-wise plausible,
but should NOT be the first native test.

The same-Q-chain B158 candidate uses its extra prime as the natural headroom
for the deferred selector normalization.

Removing that prime immediately would erase precisely the safety margin that
distinguishes the new schedule from the original one.

Therefore:

- SAME_Q_CHAIN_NATIVE_GATE: PRIORITY 1
- ONE_Q_PRIME_REDUCTION: SECONDARY / ONLY_AFTER_NOISE_PASS

## Paper-level decision

The strongest paper-level rejection attempt has failed:

- selector canonical norms are not worse than the original algorithm;
- B158 retains one extra prime throughout the relevant pipeline;
- the implementation framework already supports deferred-rescale patterns.

However no theorem currently proves that the fused state remains decryptable
for all 15 rounds under the current parameters.

Status:
- ALGEBRA: PASS
- CANONICAL_SELECTOR_NORM: PASS
- RESCALE/LEVEL STRUCTURE: PASS
- PAPER_LEVEL_NOISE_BLOCKER: NOT_FOUND
- NATIVE_NOISE: REQUIRED
- SAME-Q NATIVE CORRECTNESS: REQUIRED
- ONE-Q-PRIME VARIANT: HOLD

Do not infer a precision pass from this finding.
