# I197 — SHIP complex-packed selector early-Galois guarded-noise envelope

Date: 2026-10-14. Human PI instruction: resume research after historical I193, assign this result number **I197**, and do NOT continue the vFHE I194–I195 work. The original repository I193 was also vFHE; therefore the already PI-selected **independent SHIP evaluation-key-memory** thread (M01–M03, created after I193) is the non-vFHE research parent for this iteration. No rewriting of I193–I195 or any source code.

## Scope and evidence provenance

[FACT, prior GitHub Notes] Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md`, `logs/vfhe-state-2026-10-14-post-I193-pre-SHIP-M01.md`, independent `findings/ship-memory-STATE.md` and SHIP-M01/M02/M03. M01 established exact CKKS-slot pairing of TWO REAL secret-derived masks via ONE complex mask ciphertext and one aggregated conjugation per masking leaf; M02 established source-shape feasibility; M03 encrypted toy confirmed the identity but found key-switch noise ~3.15e-6 versus baseline ~1.96e-8 under its low-width toy key-switch parameters. These numbers are NOT production Poulpy results.

[FACT, pinned third-party source] Public independent implementation, **NOT author HEaaN**: `poulpy-fhe/poulpy` pinned at `250d4392656cd313f92ca66d96d8865702d39ddf`, files:
- `poulpy-ckks/src/layouts/ship/plan.rs`: `raised_k=roundup(((tree_depth+2)*ld+budget),base2k)`;
- `poulpy-ckks/src/test_suite/mod.rs`: `atk_layout` takes `dnum=ceil(k_in/(dsize*base2k))`, `k_aux=dsize*base2k+log_n`;
- `poulpy-core/src/layouts/gglwe.rs`: key width `k_key=dnum*dsize*base2k+k_aux`, and `k_aux` is a separate key noise guard;
- `poulpy-core/src/reference/encryption/glwe_automorphism_key.rs`, `.../encryption/gglwe.rs`: automorphism GGLWE key encryptions under transformed secret, with fresh encryption noise;
- `poulpy-core/src/component_noise.rs`: the fresh-key body error has stored standard deviation 3.2 **at the generation-precision coefficient grid**; metadata explicitly does **not** propagate through homomorphic operations;
- `poulpy-core/src/reference/automorphism/glwe.rs`, `.../keyswitching/glwe.rs`, `poulpy-ckks/src/reference/conjugate.rs`: conjugation performs actual GGLWE key switching, followed by automorphism, with target precision normalization;
- `poulpy-ckks/src/reference/ship/bootstrap.rs`: full implementation performs one post-tree conjugation; complex-packed candidate would additionally need one early conjugation per SHIP support/output half.

Original paper: Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint 2025/784, relevant §3.3 and §4.4. Previously cached Research MCP full source mirror 33pp, version parity not verified. No new author-version PDF claim in I197.

## ONE primary hypothesis / ONE minimal falsifier

**H197 [HYPOTHESIS, narrowly parameter-conditional]:** For the source-shaped Poulpy early-conjugation step and suitably bounded fresh Galois-key errors, **Galois-key noise alone** can remain below a pessimistic full-bootstrapping precision allocation at masked output `k=428`. Thus the strong claim that M03's toy key-switch error is intrinsically prohibitive at Poulpy source precision should fail its cheapest source-parameter gate.

**Cheapest decisive test:** Instantiate exact source key widths at the already recorded M02 illustrative plan `N=16384,h=32,base2k=52,ld=40,budget_out=104,tree_depth=6,raised_k=468`, so `k_mask=428`, `dnum=9`, `k_aux=66`, `k_key=9*52+66=534`. Derive one coefficientwise, worst-case, **exact-integer arithmetic** upper bound on added evaluation-key encryption error and one final nearest-rounding error. Compare against a conservative h-factor product tolerance. No real encryption, speed test, or second candidate.

## Conditional mathematical calculation [DERIVED, EXACT under assumptions]

Let a negacyclic input-mask polynomial be radix-decomposed into at most `D=9` digit polynomials, each with coefficients of magnitude at most `B=2^52` (deliberately loose). Each independent or dependent key-row encryption error polynomial `e_i` is **assumed** bounded coefficientwise by `|e_{i,j}|<=E=64`. This is a **conditional envelope**, not a security-probability statement for the unbounded Gaussian distribution. No cancellation/independence is used.

For the integer product `e_KS=sum_i d_i * e_i` over `Z[X]/(X^N+1)`, the triangle inequality gives
`||e_KS||_infty <= D*N*B*E`.

Key encryption is at `k_key=534` bits of torus precision. Assume exact integer arithmetic and a **single final nearest rounding to k_out=428 coefficient-grid bits**, producing at most half a coefficient unit. A slot evaluation at a unit-circle CKKS embedding point has operator norm at most `N` from coefficient infinity norm. With `ld=40`, decode a torus error by multiplying by `2^40`. Consequently
`eta_slot <= 2^40 * N * (D*N*B*E/2^534 + 2^(-429))`.

Numeric evaluation at `N=2^14,D=9,B=2^52,E=64`:
- GGLWE error term contribution: `log2 <= -404.8300749986` in decoded slot units.
- One final output rounding term: exactly `2^-375` slot units.
- Combined conditional bound: `eta <= 1.2994262220670705e-113 ≈ 2^-375`.

As a screening-only pessimistic target, set `epsilon=2^-18.1≈3.55923840155e-6`, inspired by the prior SHIP high-precision report and **not guaranteed equivalent to Poulpy h32 end-to-end accuracy**. For `h=32` ideal factors of magnitude at most 1, an extra per-leaf perturbation bounded by `eta/2` gives a final error envelope `2[(1+eta/2)^h-1]`. Solving `2[(1+eta/2)^h-1]<=epsilon` gives `eta_limit≈1.11226104327e-7≈2^-23.10`. The conditional source-shape bound is ~351.9 bits below this allocation.

**IMPORTANT LIMITATIONS:** (1) `E=64` is an explicit assumption, not a certified tail probability or exhaustive bound on the actual key samples. (2) The modeled single final nearest rounding does NOT cover backend DFT/NTT precision/normalization errors, accumulation internals, layout mismatches or numerical precision of `CnvPVecL`. (3) Real SHIP mux rotations, relinearization, product-tree errors, dependency structure, scale manipulation and final real/imaginary extraction are NOT analyzed. (4) The simplified `|factor|<=1` budget and the paper's epsilon are screening targets, not verified full source conditions. (5) One may NOT infer production numerical correctness/security, practical memory savings, or speedup from this inequality. (6) It does not compare actual runtime; ~h new early key switches and two masking transforms remain.

[EXPERIMENT] Deterministic exact-rational arithmetic calculation using only parameter/formula checks:
local `/mnt/data/ship_i197_guarded_ks_gate.py`, SHA256 `bfb71068a0c813ad6167d92e50e25b6302e6ba8c1098c431af8a622324ae5052`; local JSON `/mnt/data/ship_i197_guarded_ks_gate_results.json`, SHA256 `3e7c0358b6a964d64e4ee36129575e8fea8554656959f06ee7dc1cf1e2b78253`. These paths are local only, not GitHub-MCP-accessible.

## Conclusion and next test

**STATUS: PASS for only this ideal guarded-key-noise parameter screen; UNCLEAR real Poulpy FHE precision/runtime, security and novelty.**

**RESULT:** M03's simplistic toy-Galois error is not a source-backed reason to KILL complex-paired SHIP masks. At pinned source key widths, a conservative and explicitly bounded exact-arithmetic calculation leaves an enormous guard margin. The actually decisive remaining issue is numerical backend precision and added online cost/peak RAM, not this idealized fresh-key error component. This is **not** a new algorithm, novelty verified, or a demonstrated SHIP speedup.

**NEXT_ACTION (one executable gate, requires PI continuation):** On pinned Poulpy with its real backend, run **one** matched rank-1 masking-leaf test at `N=16384, k_mask=428, ld=40`: encrypt source-generated real mask pair; compare baseline two-mask accumulation with complex-packed U/V followed by actual pre-mux conjugation; measure per-slot max error and runtime for just the masking leaf, separating `keyswitch`, `IDFT`, and memory peak. Stop if error exceeds the preallocated leaf budget or if added online cost dominates the saved prepared selectors. Do not sweep parameters until this single gate is resolved. If runtime unavailable, report SOURCE/IMPLEMENTATION BLOCKED, do not simulate a pass.

**STATE_UPDATE: NO to global `STATE.md` (different concurrently maintained vFHE target); this atomic I197 record preserves the independent SHIP finding and next executable check.**
