# CGS-30 — p-cancellation obstructs polynomial decryption modulus in the CGS-28 flooding-only proof

**Date:** 2026-10-15. **Single active research program:** CGS, restored from root `STATE.md`, CGS-29 last completed. PI asked "continue". **ONE primary hypothesis + ONE decisive algebra/parameter test.**

## Hypothesis H-CGS30 and decisive falsifier

**H-CGS30 [FAIL for this SPECIFIC sufficiency proof]:** In CGS-28 stronger-fresh-Server-flooding proposal, we can freely enlarge original modulus split `Q=pq` by raising p, thereby reducing `σ_flood/p` and retaining original Okada–Takagi source's **polynomial-valued decryption modulus** `q=poly(κ)` while hiding **all** secret-dependent randomized-rounding error with a lattice-Gaussian translation TV bound at per-session level `≤2^(−κ)`. This gives no prestored session Gaussian ζ, original independent coefficient-sampled standard-MLWE secret and original low-response-degree interface.

**ONE decisive test:** Inspect actual randomized rounding's distribution as a FUNCTION OF p and plug the SAME p-dependent high-probability bound into the CGS-28 sufficient flooding condition. If `σ_flood/p` remains exponential in κ independent of how p is chosen, then raising p cannot rescue polynomial q under this proof technique. Supplement by one exact p-sweep, using published real BFV default Q budgets only as a boundary screen, not as a valid instantiation.

## Verified primary original-paper equations [FACT]

- **Hiroki Okada, Tsuyoshi Takagi**, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025, IACR ePrint **2025/409**, https://eprint.iacr.org/2025/409, full cached 40-physical-page mirror SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, VERSION_UNVERIFIED. **Algorithm7 physical p29** ServerDec, **Lemma7.1 physical p30 Eq(27)**:
```
r_i,j := u_i,j − p ⋅ round_(σ0)(u_i,j/p)
r_i,j  ~ D_(c_i,j + p Z, p σ0),    c_i,j := p ⋅ {u_i,j/p} ∈ Z.
```
So `r_i,j/p ∼ D_(c_i,j/p + Z, σ0)`: its normalized spread remains σ0 when p increases. Different coset centers are allowed.
- **Lemma7.1 physical p30 Eq(28)/(29)**: before final division by p and independent σ1 Gaussian rounding, the latent disturbance is `W+E`, with `W=r^T s - {Q/2}μ + e_eval + e_fresh` and Server E independent `R(D_(1/2 Z^n,σ_flood))`. Source **Lemma3.12 p14** already invokes huge-smudging for the bounded original eval noise only, `σ_flood=Ω(2^κ B_eval)`; the user's candidate extends it to ALL `r^T s` (CGS-28).
- **Theorem7.4 physical p32**: `q=σ_dec Ω(√κ)`, `Q=pq`, σ_dec has scaled-flood term `σ_flood/p`; hence `q≥c √κ σ_flood/p` for an unspecified positive source constant c under its sufficient correctness expression.
- **Table1 physical p3 and §1.1 p4**: the paper's desired *polynomial-valued small decryption modulus* `q=κ^{O(1)}` is stronger than a claim that its bit LENGTH `log₂ q` is polynomial. Element-count compactness (one field/ring element per decryption share) still remains even with large q. We are testing loss of the **small-q regime**, not an information-theoretic attack or an outright proof no polynomial-bit-length decryption share exists.
- **Algorithms2 physical p17** leaves underlying mFHE KeyGen/Eval and evaluation-key parameters ABSTRACT, with χ_mlwe sampled independently per coefficient and same paper χ used for secret/error, and only asserts an evaluation error bound B_eval.
- **Microsoft SEAL actual BFV source**, https://github.com/microsoft/SEAL/blob/main/native/examples/1_bfv_basics.cpp and https://github.com/microsoft/SEAL/blob/main/native/src/seal/util/globals.cpp, gives default 128-bit HEStd ciphertext modulus budgets **N=4096:109 bits**, **N=8192:218 bits**, **N=16384:438 bits**, **N=32768:881 bits**. This is RLWE rank-one, usually ternary secret/Gaussian error and arbitrary plaintext t, NOT source Algorithm2 k2 R2 with identical χ for secret and error; these values are used **ONLY** as outside implementation budget references. No libSEAL BFV FHE run or lattice estimator was performed.
- Prior branch CGS-28 precise source-derived *sufficient but potentially loose* TV bound: `σ_flood≥2^(κ+2)d M` for d=1 scalar, d=n ring; `M=k n B_mlwe R_r+2 B_eval+1/2`. CGS-29 showed low n1024 modulus-budget disagreement but previously chose p fixed. The NEW issue is **p cannot correct the stronger flooding-to-rounding ratio**.

## Exact cancellation theorem (conditional on CGS-28 sufficient condition) [DERIVATION]

For a high-probability rounding event `max_(i,j)|r_(i,j)|≤R_r`, any Gaussian coset tail threshold targeting negligible failure naturally scales as
```
R_r=p⋅σ0⋅t(κ,n,k)    (up to a bounded coset-center correction),
t(κ,n,k)=Θ(sqrt(κ+log(kn))) for per-session ≲2^(−κ) Gaussian tail.
```
For a fixed audited example we choose t=16 and σ0=16, using EXACT R_r=pσ0 t. This is only a *chosen cutoff*; the exact δ_r tail and smoothing are not certified for a complete cryptosystem. With source coefficient bound `|s_i,j|≤B`, k ring-secret components and n output coefficients, CGS28's coefficientwise conservative bound is
```
M=knB⋅(p σ0 t)+2B_eval+1/2,
σ_flood,new ≥ 2^(κ+2) ⋅ n ⋅ M.
```
After dividing by p:
```
σ_flood,new / p
  ≥ 2^(κ+2) ⋅ n ⋅ [knB σ0 t + (2B_eval+1/2)/p]
  ≥ 2^(κ+2) ⋅ k n² B σ0 t.
```
Thus the EXACT `p`-independent obstruction for THIS CHOSEN SUFFICIENT TV proof is
```
q ≥ c √κ ⋅ 2^(κ+2) ⋅ k n² B σ0 t,
```
where c>0 is the original correctness hidden multiplier, unspecified by the paper. Assuming public non-negligible B, σ0, t, n and k, the right side is `2^Ω(κ)`. Increasing p cannot lower it. In comparison, **original** paper's older flooding lower term `σ_flood,0≈2^κ B_eval` is independent of p, so its contribution to `σ_flood,0/p` CAN be reduced by choosing p accordingly. This explains why CGS-28's stronger full-rounding flood may lose source's small polynomial-valued q regime even if extra message size remains finite.

**PRECISION:** This is a FAIL of the CGS-28 *translation-TV sufficient proof with an explicit high-probability rounding cutoff and a small q target*, NOT a theorem that EVERY flooding-based protocol requires exponential q. The alternate statistical proof may exploit cancellation of unbiased W, smoothing plus covariance comparison, or computational hiding; those would need independent validity under adaptive Algorithm5 transcript. A relative variance TV analysis might improve `2^κ` to `2^(κ/2)` in a continuous Gaussian model (still exponential), but it is NOT established for the original discrete conditioned transcript in this iteration. No source paper bug, no break of original FHE.
 
## The ONE exact reproducible p-sweep [EXECUTED]

Self-contained `/mnt/data/cgs30_p_cancellation_gate.py`, SHA256 `64c556b341cb30d988cda2cbadfa1edbeb975d0913f1ca9c3e4ba16376df3418`. JSON `/mnt/data/cgs30_p_cancellation_gate.json`, SHA256 `aa1d925ed9cecfe93f84868419631d1ff24c081480f17b135ece1a2e06ef406f`. No libSEAL runtime, estimator or proof of source-compliant κ128 parameters.

We PRESERVE CGS28 illustration κ128, ring n1024, k2, coeff bound B1, σ0=16, t=16, B_eval=2^30; choose `ceil√κ=12` as an **illustrative normalization of original hidden Ω constant**, NOT as a source theorem universal constant. For each `p=2^e`, set `R_r=pσ0t`, `σ_new=2^(κ+2)n( knBR_r +2B_eval+1)`, `q_new=ceil(12σ_new/p)`. The original σ_base flooding lower TERM is `2^κB_eval`, not the full baseline source q. All ratios are exact big-integer calculations.

| e=log₂p | Original flooding TERM log₂(q_base) | New no-pad sufficient log₂(q_new) | New log₂(Q=pq_new) |
|---:|---:|---:|---:|
| 20 | 141.58496 | 162.59059 | 182.59059 |
| 32 | 129.58496 | 162.58496 | 194.58496 |
| 64 | 97.58496 | 162.58496 | 226.58496 |
| 96 | 65.58496 | 162.58496 | 258.58496 |
| 128 | 33.58496 | 162.58496 | 290.58496 |
| 160 | 1.58496 | 162.58496 | 322.58496 |

The p-INDEPENDENT integer `q` contribution `12·2^130·1024·2·1024·16·16` has `log₂≈162.5849625`, bit-length **163**. The +B_eval/p term vanishes at large p but the secret-dependent rounding term does not.

The public SEAL n8192 BFV Q budget ~218 bits would rule out the illustrative **p=2^64** no-pad case when `log₂Q_new≈226.585`, and n4096 BFV ~109 bits rules out even the p=2^20 value. However SEAL ring degree and secret/error/plaintext distributions DO NOT match this CGS illustration, so these are **cross-family budget warnings, not a certified BFV attack or source parameter instantiation**. If p=2^20, the Q183-bit illustration is below SEAL n8192 218-bit reference upper limit but has q163 bits, failing the target q=poly(κ) asymptotic regime; a real BFV FHE noise budget and security parameter comparison was not run.

## Constructive synthesis verdict

Correct technical pieces: original χ secret retained, fresh E noncolluding Server, no pad storage, exact smudging of all bounded disturbances, one ring-field PartDec per participant.

Joint failure for desired claim: **Keeping q small while making E mask r^T s via CGS28 worst-case TV** is incompatible under that sufficient analysis because r∝p. This tradeoff no longer fits the *same target* of original authors when q=polyκ is essential. Much of 'just 21 additional bits' in CGS28/29 is not useful if q already has ≈κ bits instead of O(log κ) bits.

**Decision: PARK the naive independent-Server additive flooding-only subbranch CGS28–30 under its current translation-TV proof.** Do not claim a universal impossibility of clever centered/noise-distribution or computational hiding, nor a completed new ThFHE construction. The original pre-shared secret-conditioned Gaussian problem remains OPEN.

## Close

- **ITERATION:** CGS-30.
- **STATUS:** FAIL H-CGS30; PASS exact source Eq27 p-dependence, cancellation proof and integer p sweep; **HUMAN_REVIEW** any qualitatively new reduced-noise/full-protocol construction.
- **RESULT:** CGS28 sufficient parameter q≥c√κ·2^(κ+2) k n² Bσ0t independent of p, so poly-q goal cannot be supported by this proof. Actual FHE BFV budget table confirms why whole Q matters, but no credible full parameter instantiation/estimator test completed.
- **NEXT_TEST CGS-31 (only upon PI next "继续"):** Return to original source's conditional Gaussian problem, or ONE tightly scoped theoretical alternative: Can treating r^T s as a CENTERED random variance perturbation, rather than adversarial fixed W, produce a **source-adaptive-transcript-compatible** tighter TV/smoothing bound with q=polyκ? Identify the exact adversarially observable conditioning (Algorithm5 p23 and Lemma7.1 p30) and a minimal 1-dim two-secret hypothesis test; if any unavoidable variance distinguishability forces non-poly q, PARK unconditional flooding and propose PI review of a new source-compatible PRSS/functional sampling construction. Do NOT endlessly rescreen arbitrary BFV parameters without a full instantiated library/proof.
- **STATE_UPDATE:** YES. Save own finding, CGS detailed topic archive, and single root STATE. Leave all other topic research files intact.
