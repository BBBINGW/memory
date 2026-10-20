# BOOT-B078 — Does decoupled / external-product-tree conversion make packed dense phases cheap?

**Date:** 2026-10-20. **TRACK_ID:** BOOT. **SHIP:** PAUSED.

**Iteration status:** `PASS_RESTRICTED_RANK_FALSIFIER / FAIL_ONE_SCALAR_LUT_FOR_M_INDEPENDENT_FULL_FIELD_PHASES / PASS_BOUNDED_DOMAIN_ESCAPE / HUMAN_REVIEW_CCS2026_FULLTEXT`.

## 1. Primary hypothesis

Given B077's GLWE encryption of a polynomial containing M independent decryption-phase coefficients, can a nonadaptive public linear preprocessing compress those M phases into fewer than M scalar functional-lookup channels, followed by arbitrary *public linear* output recombination, while evaluating every desired per-coefficient nonlinear function? First use the target \(f(x)=x^2\) on the **full prime field domain** to test an explicit gate.

The pipeline under examination is precisely
\[
 x\in\mathbb F_p^M\xrightarrow{\text{public linear/affine forms}}
 (a_j^T x+b_j)_{j=1}^r \xrightarrow{\text{one arbitrary scalar LUT per form}}
 (g_j(a_j^T x+b_j))_{j=1}^r \xrightarrow{\text{public affine output}}
 \{f(x_i)\}_{i=1}^M.
\]
LUTs are nonadaptive (cannot compose their outputs into other LUT inputs), and no homomorphic multiplications among LUT outputs are allowed. The number \(r\) counts **independent scalar-lookup channels**, *not physical GGSW ciphertexts*: one packed GGSW may contain many scalar selectors.

## 2. Sources read and limitations

[FACT] CCS 2026 program lists *Decoupled TFHE-type Functional Bootstrapping*, by Li, Shen, Lu, Wang, Zhao, Wang, scheduled Nov 17, 2026: https://www.sigsac.org/ccs/CCS2026/program/schedule.html . Author page https://zhiweiwang.github.io/publications/decouple/ lists title/authors/venue but no full technical PDF. **Its exact algorithm, noise proof, data structure and runtime were NOT read.** We do not attribute any specific algorithm to this work.

[FACT] Same group's **distinct, earlier** paper *Leveled Functional Bootstrapping via External Product Tree*, ePrint2025/022 https://eprint.iacr.org/2025/022 has verifiable public abstract claiming multi-input external-product-tree functional bootstrapping, OpenFHE implementation, 12/16-bit large-precision examples and BFV-to-LFBS scheme switching using digital extraction. A searchable PDF header was found but PDF full retrieval returned 403 and Research Notes had a source-normalization problem. **Only public metadata/abstract are used**, not internal algorithms. Neither one-to-one nor version continuity is assumed with CCS2026.

[FACT] Existing circuit-bootstrapping `circuit_bootstrap_via_trace_and_scheme_switch` https://docs.rs/sunscreen_tfhe/latest/sunscreen_tfhe/ops/bootstrapping/fn.circuit_bootstrap_via_trace_and_scheme_switch.html explicitly performs programmable bootstrapping on one LWE input then trace and scheme switch to output GGSW; documentation reports >90% of its running time comes from the PBS step in its implementation. This is one positive **nonlinear** scalar-to-GGSW interface, not free.

[FACT] OpenFHE developer discussion https://openfhe.discourse.group/t/the-complexity-of-scheme-switching/1369 confirms key switching, slot-to-coeff encoding and digit extraction vary substantially by source/target scheme. No bound on arbitrary scheme-switching is claimed here.

[PRIOR] B077 showed one GLev multiply can produce **encrypted dense phase coefficients**, but not their encrypted monomial exponent representation. B078 tests whether the latter can be amortized simply by scalar lookup sharing, and does NOT re-prove the broader arithmetic-only no-go.

## 3. Decisive algebraic statement

Let p be odd. Every full-domain function \(g_j:\mathbb F_p\to\mathbb F_p\) has a unique polynomial representative of degree \(<p\). Assume output arbitrary public linear combinations of
\[g_j(a_j^Tx+b_j),\qquad j=1,\ldots,r,\]
and public affine functions of x. If this produces all individual squares \(x_1^2,\ldots,x_M^2\), it also produces their public sum
\[F(x)=\sum_{i=1}^M x_i^2.\]
The Hessian \(\nabla^2 F=2 I_M\) has rank M. Each composed scalar lookup gives
\[\nabla^2 g_j(a_j^Tx+b_j)=g_j''(a_j^Tx+b_j) a_j a_j^T,\]
rank at most 1. The affine terms' Hessian is zero. Hence pointwise
\[ M=\operatorname{rank}(2 I_M) \le \sum_{j=1}^r \operatorname{rank}(a_ja_j^T)\le r.\]
**Thus \(r\ge M\) is necessary in this specific nonadaptive scalar-LUT-plus-linear-reconstruction interface.** Even a single encrypted polynomial storing all M coefficients cannot make one scalar LUT channel compute all M independent full-field square functions.

**Not a general FHE lower bound.** Does not apply if intermediate ciphertexts undergo nonlinear multiplication, adaptive circuit/LUT trees, ring-packed/vector-valued non-scalar lookup primitives, domain restriction, growing plaintext alphabet, or a different encoding/scheme. The statement is semantic over plaintexts, not a security proof.

## 4. Independent finite-field checks

Script `b078_unary_lut_rank_gate.py`, stdlib Python, modulus p=257, exact modular Gaussian elimination. For M=2,4,8,16 and r∈{1,max(1,floor(M/2)),M−1}, draw 150 random linear-sketch sets/weights each; 1,800 randomized Hessian calculations, all ranks ≤r (0 counterexamples). 360 independent arbitrary univariate polynomial degree≤5 Hessian chain-rule trials pass. For each M, M identity sketches and g(t)=t² give target Hessian rank M, verifying tightness.

Second proof without derivatives: for all 24 nonzero directions (a,b) in F5², solve a 25-equation finite-field system allowing **any arbitrary 5-value scalar lookup table** g(a*x+b*y), plus arbitrary public affine linear correction. Exactly 24/24 systems inconsistent with target x²+y² on all F5². Two independent square lookups reconstruct all 25/25 inputs.

## 5. Important escape route: enlarge scalar lookup domain

If each original input has only B options, one may injectively encode M independent values in scalar modulus q when q≥B^M by
\[z=\sum_{i=0}^{M-1} B^i x_i.\]
Then one arbitrary LUT indexed by z can return all M squares (as a vector or packed output). This is precisely outside the full-field constant-alphabet theorem. Toy B=4,M=3,q=257: all 64/64 distinct encodings correctly decode, compare 64-table entries vs three 4-entry unary tables =12 entries. Wide toy B=16,M=4,q=65537: 10,000/10,000 random input vectors encode/decode exactly, with domain size 65,536 versus 4·16=64 separate table entries, 1024x naive table length. **This is a LUT description size comparison, NOT a key-size, homomorphic multiplication or measured latency lower bound.** Efficient external-product trees (Li et al. 2025) may implement large domains more efficiently than a flat table.

## 6. Research decision

H078 as a free linear-combination sharing primitive is **FAIL**. Its full-field formula cannot replace M genuinely independent scalar nonlinear lookup channels with r<M while preserving all square functions. Domain widening is mathematically possible but is *already the established large-precision LUT problem*, with no sourced gain in online GSW/NTT/key size from B077's single GLev phase evaluation. A circuit-bootstrap digit preparation has real PBS/trace/scheme-switch cost and consumes key material; it cannot simply be assumed available.

No native FHE run, no 128-bit matched security, noise growth, DFR or speedup demonstration. Paper CCS2026 cannot be claimed verified beyond acceptance and authorship. Avoid publication claim.

**STATUS** `PASS_RANK_GATE / FAIL_NONADAPTIVE_SCALAR_LUT_COMPRESSION / UNCLEAR_ALTERNATIVE_PACKED_NONLINEAR_INTERFACE`.

**RESULT:** restricted no-go with exhaustive/all-function toy and bounded-domain counterexample to overgeneralizing it.

**NEXT_TEST B079 (NOT STARTED):** Do not continue the B077–B078 trivial phase-to-exponent interface loop. Study the *actual* newer multi-key sublinear-bootstrapping primitive in **HERDS** (EUROCRYPT 2026) and extract exactly one candidate transfer to single-key or packed TFHE, only after primary PDF/algorithm/Theorem reading and full prior art. If no transfer preserves novel complexity/security, archive. If full primary text unavailable, record missing source and pivot rather than guess.

**STATE_UPDATE NO:** Existing `findings/boot-STATE.md` could not safely be read in GitHub Notes in recent turns despite being listed at ~188KB. Preserve it and append only new B078 finding. SHIP remains paused.

## 7. Reproducibility

- `b078_unary_lut_rank_gate.py` SHA256 `af508a06ecb8e7056c4c1a2b9c9959de3cfa7848827fe42701b68d1ca82c8893`
- `b078_results.json` SHA256 `eec6a8626a77e690e775174a232ba5bdd35d701dc4246f0246e827eaa4391c04`
- Seed 78020, stdlib Python only.