# BOOT-B135 — Full-source fairness audit of ePrint 2026/2119

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Paper: Ouyang et al., "CKKS Bootstrapping in less than 10ms", ePrint 2026/2119
- Supplied source: papers/supplied/2026-2119.pdf
- Git blob SHA: 5de485db8242148144f74de0c857cfcd698f0f35
- Physical pages: 35
- Status: SOURCE_GATE_RESOLVED / PASS_SCOPED_SUB10MS / PASS_MATCHED_CPU_LL13_SPEEDUP / NO_MATCHED_GPU_BASELINE
- CODEX_REQUIRED: NO
- Native reproduction: NOT YET JUSTIFIED

## 1. What the 8.2 ms / 4.6 ms claim actually measures

The sub-10ms result is the LL13 **complex-valued** configuration on an NVIDIA RTX PRO 6000 GPU.

LL13 parameters from Table 2:
- ring degree: N = 2^13 = 8192;
- log(PQ) = 218 bits;
- dnum = 8;
- q0: 25-bit prime x 1;
- KS budget: 28-bit prime x 1;
- multiplication budget: 20-bit prime x 1;
- S2C budget: 20-bit prime x 1;
- product tree: 25-bit primes x 5.

The LL configurations retain exactly **one multiplicative level** after bootstrapping.

For complex LL13, Table 3 reports measured precision 5.18 bits. Precision is defined as log2(epsilon^-1), where epsilon is the **maximum absolute error over all output slots**.

The paper states all four parameter sets satisfy its standard 128-bit security target.

GPU Table 8:
- batch 1: 8.2 ms/ciphertext;
- batch 2: 6.9 ms;
- batch 4: 6.8 ms;
- batch 8: 6.0 ms;
- batch 16: 5.8 ms;
- batch 32: 5.1 ms;
- batch 64: 4.6 ms.

Therefore the public headline is a real reported measurement, but its scope is:
**N=8192, ~5.18-bit complex output precision, one remaining multiplication level, authors' 128-bit target, RTX PRO 6000.**

It is not a generic high-precision CKKS bootstrap number.

## 2. High-precision result

LL14 uses:
- N = 2^14;
- log(PQ) = 437 bits;
- dnum = 4;
- one remaining multiplication level;
- measured complex precision 23.1 bits.

GPU Table 8:
- batch 1: 44 ms;
- batch 64: 29 ms/ciphertext.

Thus:
**HIGH_PRECISION_SUB10MS = FALSE for the reported LL14 experiment.**

The sub-10ms headline is specific to the low-precision LL13 configuration.

## 3. Security / secret interface

The implementation starts from a dense ternary application secret.

After S2C and at the lowest modulus level, it switches to a sparse secret with stated Hamming weight h=31, following SHIP / sparse-secret encapsulation.

Therefore the bootstrapping phase is not simply ordinary dense-secret CKKS under the same secret throughout. The manuscript nevertheless states that all tested parameter sets target 128-bit security.

No separate bootstrapping failure-probability table was found in this manuscript. Do not silently equate the reported precision measurement with a DFR certificate.

## 4. Hardware and parallelism

CPU platform:
- dual-socket AMD EPYC 7K62;
- base 2.6 GHz, boost 3.3 GHz;
- 1 TB DDR4-3200;
- AVX2 + OpenMP;
- SMT disabled;
- numactl controls usable cores.

GPU:
- NVIDIA RTX PRO 6000;
- custom CUDA kernels plus EasyFHE operators;
- Tensor Cores and CUDA Cores execute disjoint RNS workloads concurrently with exact integer arithmetic;
- S2C, key switching, product-tree evaluation and the remaining homomorphic stages also run on GPU;
- blind-rotation evaluation-ready keys remain resident in GPU memory.

Therefore 8.2 ms is a GPU system result combining the new algorithm with a specialized highly parallel implementation.

## 5. Matched comparison to SHIP

The strongest algorithm-level evidence is Table 3, which compares against SHIP under the same four parameter families while retaining SHIP's S2C implementation.

LL13 real:
- SHIP: 3.02 s 1-core, 239 ms 48-core, 4.45-bit precision.
- Ouyang et al.: 1.62 s 1-core, 96.0 ms 48-core, 5.18-bit precision.
- speedup: 1.86x 1-core, 2.49x 48-core.

LL13 complex:
- SHIP: 6.04 s 1-core, 430 ms 48-core, 4.45-bit precision.
- Ouyang et al.: 2.34 s 1-core, 116 ms 48-core, 5.18-bit precision.
- speedup: 2.58x 1-core, 3.71x 48-core.

This is the fair evidence that the new algorithmic/dataflow changes materially improve the low-precision SHIP regime.

The improvement is NOT uniform:
- LL14 real is slower than SHIP on both 1 core and 48 cores, although precision rises from 16.9 to 23.1 bits.
- LL14 complex is slower on 1 core and only modestly faster at 48 cores (667 ms -> 612 ms), with much higher precision.
- HT15 is slower than SHIP in the reported CPU comparisons.

Decision:
**PASS_MATCHED_CPU_LL13_SPEEDUP, but FAIL_UNIVERSAL_SPEEDUP.**

## 6. HEAAN comparison

The manuscript explicitly says direct comparison to HEAAN's reported 6.97 ms is difficult because HEAAN's algorithmic/implementation details, hardware, output precision and remaining levels are not publicly matched.

Therefore:
**do not call 8.2 ms a fair algorithmic comparison against HEAAN.**

## 7. What creates the improvement

The full source reveals four distinct effects.

### Narrow blind rotation
For the equal-block model, table-selector multiplications change from

4 g h

to

2 g (h + ceil(h/B)),

where B=floor(n/[2(g-1)]).

This saves O(N) ciphertext-plaintext products but introduces O(h) extra rotations/products.

### Complex packing of selector pairs
Pairs of real selectors are packed into the real/imaginary components of one CKKS ciphertext.

This halves the narrow evaluation-ready blind-rotation key count from

2 g (h + ceil(h/B))

to

g (h + ceil(h/B)),

but **does not halve the table-selector multiplication count**. The paper explicitly says arithmetic remains 2g(h+ceil(h/B)).

### NTT-permutation fusion
A direct head evaluation would perform 2gh forward NTTs.

The fused formulation uses only 2h base-table forward NTTs; all rotated variants are fixed NTT-domain permutations.

The dominant blind-rotation work is reorganized as structured sparse matrix-matrix multiplication, enabling GPU batching.

This is likely a major contributor to the very low GPU latency, but the manuscript does not provide a per-stage GPU latency breakdown, so its exact contribution cannot be isolated.

### Packed transmission key
The secret-dependent selector information is packed into four coefficient-encoded ciphertexts. A binary automorphism/key-switch tree reconstructs the evaluation-ready selectors once.

The evaluator then reuses the reconstructed key for subsequent bootstraps.

## 8. Important setup/memory caveat

The paper explicitly excludes blind-rotation key reconstruction from reported bootstrapping latency, treating it as one-time setup.

The evaluation-ready blind-rotation keys remain resident in GPU memory.

The paper does not report:
- reconstruction latency;
- final evaluation-ready key bytes / GPU memory footprint;
- peak GPU memory during bootstrap;
- a stage-by-stage GPU timing breakdown.

Therefore the headline latency is best interpreted as **steady-state latency after key preparation**, not end-to-end first-use latency.

This does not invalidate the latency claim for long-lived evaluation keys, but it matters for short sessions, many-user deployments and key-memory comparisons.

A previous endpoint-only Amdahl fit from 8.2 ms and 4.6 ms should remain labeled inference; the complete batch table is nonlinear and reflects GPU occupancy/batching, not a source-reported fixed+per-ciphertext decomposition.

## 9. Formal block-size notation gap

The mathematical development defines h equal blocks and writes

g = N/h

exactly, using positions j=xg+y and identities such as 2gh=2N.

The experimental section states h=31 while every reported N is a power of two (2^13, 2^14, 2^15). Hence h does not divide N.

SHIP's public presentation describes the corresponding blocks as having **approximately N/h coordinates**, consistent with a near-equal partition rather than exact divisibility.

Thus the equal-block theorem, as written in 2026/2119, does not literally instantiate the experimental h=31 parameters without a small adaptation.

### Cheapest repair

Let the real block lengths be g_x in {floor(N/h), ceil(N/h)} and let

G = max_x g_x = ceil(N/h).

Pad each shorter block with public zero selectors up to G candidates, replace xg by the actual public block start L_x, and use G in the head/tail window construction.

Then the same coefficient-window proof applies with y in [G], because padded candidates contribute zero.

For LL13:
- N=8192, h=31;
- G=ceil(8192/31)=265;
- padded candidate count hG=8215;
- only 23 dummy positions are introduced;
- overhead = 23/8192 ~= 0.28%;
- n=4096;
- 2(G-1)=528 <= n, so the tail-packing condition remains valid;
- B=floor(4096/528)=7;
- ceil(h/B)=5.

Under this padded equal-width realization:
- original table-selector count: 4*265*31 = 32860;
- narrow arithmetic count: 2*265*(31+5) = 19080, about 58.1% of the original;
- complex-packed evaluation-ready selector count: 265*(31+5) = 9540, about 29.0% of the original selector count.

Decision:
**PASS_REPAIRABLE_PARAMETERIZATION_GAP / NOT_A_CORRECTNESS_BREAK.**

The manuscript should ideally state this unequal-block/padding adaptation explicitly, but the discrepancy does not currently support a claim that the construction fails.

## 10. B135 final decision

The original source blocker is resolved.

- PASS_PUBLIC_CLAIM.
- PASS_EXACT_PARAMETER_AUDIT.
- PASS_SCOPED_SUB10MS_LL13_GPU.
- PASS_MATCHED_CPU_LL13_ALGORITHMIC_SPEEDUP.
- FAIL_CLAIM_OF_GENERIC_HIGH_PRECISION_SUB10MS.
- NO_MATCHED_GPU_SHIP_BASELINE.
- NO_FAIR_DIRECT_HEAAN_SPEEDUP CLAIM.
- SETUP_RECONSTRUCTION_EXCLUDED.
- GPU_KEY_MEMORY_BYTES_UNREPORTED.
- GPU_STAGE_BREAKDOWN_UNREPORTED.
- PASS_REPAIRABLE_EQUAL-BLOCK_NOTATION_GAP.
- NOVELTY of the paper itself: clearly substantive; novelty of any new BOOT follow-up remains NOT_ESTABLISHED.

## Recommended next research gate

The most interesting unresolved system cost exposed by the full paper is the gap between the **four-ciphertext transmission representation** and the much larger **evaluation-ready selector representation** that is reconstructed once and kept resident on GPU.

Do not implement yet.

A next algebraic/source gate should ask:

> Can the coefficient-packed indicator ciphertexts be consumed by narrow blind rotation without fully materializing all evaluation-ready selector ciphertexts, while preserving the per-block factors required by the product tree?

Cheapest test:
1. express one narrow head factor as a linear map from packed indicator coefficients to the required selector-weighted slot vector;
2. count the minimum number of output ciphertexts that must remain separate before the product tree;
3. test whether a direct packed linear transform merely replaces one-time O(N) extraction with repeated O(h sqrt(N)) / rotation-heavy work;
4. kill the idea if steady-state latency or total GPU memory traffic cannot improve.

No Codex/native work before this algebraic cost gate.
