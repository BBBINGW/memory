# Iteration 127 — MOAI standard interleaved diagonal packing does not admit the cheap half-slot pairing assumed locally in I126

Date: 2026-10-12. PI authorized I127 by “好的，请继续” directly after I126. ONE primary question, cheapest decisive **stride/slot-permutation + operation-count** test on the actual input/output layouts of MOAI Algorithms 3/4. No encrypted implementation, no performance claims or author contact.

## Original source provenance
Linru Zhang et al., *MOAI: Module-Optimizing Architecture for Non-Interactive Secure Transformer Inference*, IACR ePrint 2025/991, https://eprint.iacr.org/2025/991; full 32 physical-page author-preprint via Research MCP mirror, PDF SHA256 `8c694fb9249c4ed4ed2269542c6bef424d7e8a4aa984a7eb2f310b8949b2f1fd`, VERSION_UNVERIFIED. Primary §3.2 pp6–7 **Eq.(1) and Lemma 3.2**: interleaving `B0=S/m=N/(2m)` matrices, row i occupies positions `iB0+r` with r the sample index; within-sample rotation = global `Rot_{jB0}`. §3.1 p5 Def.3.2 and Appendix B p19 Algorithm 3 produce m distinct diagonal ciphertexts, and p20 Algorithm 4 consumes the same format. §4 Algorithm1 p9, §5 p10 (8 levels for exp, 11 for Goldschmidt, 1 final), Appendix F Algorithm 9 p29. Experiment §6.1 p11 uses `N=2^16,S=N/2=32768,m=128` and amortizes 256 input samples.

A public conference page https://proceedings.iclr.cc/paper_files/paper/2026/hash/2f2b1d6bbd50865eca40e2774a057eef-Abstract-Conference.html lists this title at **ICLR 2026**; our equations are referenced against the explicitly hashed ePrint mirror version, not automatically assumed identical to proceedings.

## Primary hypothesis / ONE minimal decisive test
[HYPOTHESIS] One can insert the two-half paired-diagonal Softmax of I126 between **unchanged** MOAI Algorithm 3 and Algorithm 4 with cheap O(1) mask/rotation overhead per diagonal pair and therefore preserve the local m→m/2 nonlinear-ciphertext work reduction as a plausible low-batch end-to-end gain.

[FALSIFIER] Take even m=128,S=32768 and ONE actual input embedded as sample r=0 in the standard MOAI interleaved layout (remaining 255 sample lanes set to zero — the *most favorable* sparse setting). Check if a simple half-slot permutation/add realizes the I126 pair, and if not compute the exact per-row index permutation and the cost of a standard mask+rotate butterfly to carry it out and undo it. Compare added automorphism-key switches with saved relin operations, carefully avoiding a universal runtime claim.

## One exact slot-layout test
For a single sample, original row i resides at index `a_i=i*256` in every standalone diagonal ciphertext. Desired I126 two-half layout stores the same row i at index `b_i=i*128` in the low half (even diagonal) and at `H+i*128` in the high half (odd diagonal), with `H=S/2=16384`.

Therefore the low-lane slot permutation must send `a_i→b_i` with **row-dependent displacement**:
```
  a_i-b_i = 128*i, i=0,...,127.
```
The displacements are 128 distinct residues mod S. A single global rotation has a constant displacement and cannot achieve this, even using slot-wise masks and adds on one rotated copy. **In particular**, the naive pair `C_even+Rot_H(C_odd)` is invalid because `Rot_H` maps row i of the odd diagonal into row i+64 of the same sparse layout and causes collisions.

Small exact check: m=4,S=16, original sparse slots at {0,4,8,12}, E=(2,7,11,19), O=(3,5,13,23). Naive `C_E+Rot_8(C_O)` puts **15=2+13** at slot 0, rather than separately placing 2 (low half) and 3 (high half). Verified by exact NumPy integer rotations; NO encrypted evaluation.

## Explicit constructive butterfly / conversion count (not an optimality claim)
Take `S=2*m*L`, `L=H/m=128` for m=128. Initially the active row-i location is `2Li` (stride 256). For stages `b=0,...,log₂m−1`, select rows whose index has bit b=1, move their currently occupied slots left by `L*2^b` via **one plaintext mask, one global rotation, and two additions/subtractions**. The location after b stages is
```
 pos_b(i) = 2Li - L*(i mod 2^b).
```
At b=log₂m, `pos=Li`: row stride compressed from 2L to L and **all m rows fit into the low half**. Reverse the b stages to expand back from stride L to stride 2L. No collisions occur between moved and stationary nonzero support for a single independent diagonal, as confirmed in toy dimensions.

[DERIVED/TESTED] Complete mask+rotate+add constructive algorithm was checked with exact integer arrays at `(m,S)=(4,16),(8,64),(128,32768)`. Each compression and each expansion passes entry-by-entry; stage counts are 2,3,7. This is not a CKKS/noise test.

For all m=128 independent standard Algorithm-3 output diagonal ciphertexts:
- **Pack:** each original C_j: 7 rotations+7 plaintext masks; each odd (one per pair): 1 further rotation by H to target high half; pair addition. `128*7+64=960` rotations, `128*7=896` masks.
- **Unpack:** after paired Softmax dummy slots generally nonzero (because f(0)≠0), mask each active half of each pair; move odd half back by H (64 rotations); expand all 128 diagonals separately (7 each). `128*7+64=960` rotations, `128*7+128=1024` masks.
- **Local denominator:** `Rot_H` once = 1 more rotation.
- **Total naïve standalone conversion route:** `1921` added rotations, `1920` plaintext masks, plus additions and any rescale/key management. This is an **explicit working upper bound for a costly conversion**, NOT a proof all clever conversion circuits need this much. Each CKKS rotation normally invokes one automorphism key switch; plaintext masks may themselves consume multiplicative scale/levels, depending on implementation.

The I126 *ideal prepaired* m=128 Softmax saves 64 exponent polynomial evaluations + 64 final ciphertext products. MOAI §5 reports 8 levels for exponentiation; if instantiated as 8 repeated squarings each, the saved ciphertext×ciphertext multiplication count is `64*8+64=576`, usually each involving relinearization. Therefore the naïve standalone converter **adds far more rotations (1921) than the 576 ciphertext products it saves**, even before masks, but this comparison is NOT an empirical wall-clock lower bound: a ciphertext multiplication and a rotation differ in costs and GPU batching, and a better layout-aware circuit might share work across diagonals.

A restricted structural lower bound: for **a single isolated input diagonal**, with only slot-wise plaintext masks/linear addition and t global rotations, the number of distinct cumulative shifts obtainable along a data-dependence path is at most `2^t`; obtaining the 128 different row offsets requires `t≥7`. This lower bound is ONLY for independent per-diagonal permutation without inter-ciphertext packing, nonlinearity, or changed upstream generation; do not falsely claim a general 7m global lower bound.

## Why this does not falsify I126's local algebra
I126 computed Softmax on inputs **already in** the two-half format; its denominator algebra is correct. This I127 result falsifies the *shortcut* that unchanged Algorithm 3/4 provide or consume that format with trivial rotations. The original MOAI explicitly optimized away format conversions; reintroducing heavy shuffles defeats that design principle. The published full batch B=256 is also outside the I126 B≤128 pair capacity and has no throughput win.

[OPEN] A genuinely **native two-lane producer/consumer** for Algorithm 3/4 (or a different interleaved lane arrangement and denominator method) might reduce conversion cost; no such construction, performance analysis, security/noise proof, nor novelty argument was developed in I127. Standard SIMD shuffles/butterflies are prior techniques. Do not assert that all possible paired-diagonal optimizations are impossible.

## End
STATUS: **FAIL cheap unchanged-pipeline insertion / PASS slot-index counterexample + exact constructive conversion count / HUMAN_REVIEW**.
RESULT: MOAI standard `B0=S/m` interleaved outputs and I126 `B1=S/(2m)` two-half operands differ by an i-dependent slot permutation; naïve half-rotation mixes rows. Direct independent per-diagonal masked butterfly requires ~1921 additional rotations at m=128, against ~576 saved ct×ct multiplications in a specified 8-square exponent cost model. No proven speedup or actual benchmark.
NEXT_ACTION: Recommend **PARK I126–I127 standalone repacking**. PI decides to (A) authorize a *different primary hypothesis* for native two-lane Algorithm-3+4 matrix products, with one small plaintext correctness/cost falsifier and prior-art check before FHE implementation, or (B) select another FHE target. Do not repeat the same repacking loophole.
STATE_UPDATE: YES — materially falsifies the cheap pipeline integration suggested by I126; update STATE then stop.
