# FHE Research State — After Iteration 123
Checkpoint: **2026-10-12, after Iteration 123**.

## CURRENT TARGET
**None ACTIVE after I123 closure.** Most recent target: Zhang et al., *LEAF: A Low-Latency Evaluation Architecture for Feedforward Block in Privacy-Preserving Transformer Inference*, ePrint **2025/956**. I123 identified a **cross-key KDM/circular-security proof obligation** in the public packing + return ring-switch keys, but no attack, no verified insecurity and no novel remedy. Status HUMAN_REVIEW; do not equate a proof-obligation gap with an actual cryptographic break. Full 43-physical-page mirror PDF acquired, SHA256 `937fbae4dcd32f421c91f7df4ad83c3a003861b168f4bfd7798be1476a736267`, VERSION_UNVERIFIED. FAB I120–122, SPRU I119 and FEFBS I117–118 remain PARKED.

## LAST COMPLETED ITERATION
**123**. I124 NOT started.

## CURRENT QUESTION
**HUMAN_REVIEW / NO_ACTIVE_HYPOTHESIS:** Is LEAF's explicit linear/affine *two-key cycle* already covered by a precise existing KDM/2-circular theorem for the relevant BFV/RLWE parameter and embedding? PI decides whether to authorize one source-specific theorem applicability check in I124 or pivot to a different structural FHE target. Do not call the cycle a security exploit.

## PRIMARY HYPOTHESIS
**NONE ACTIVE.** Last I123 [HYPOTHESIS] that ordinary semantic security alone trivially supplies the joint security proof for LEAF's actual public packing+ring-switch keys is **not justified as stated**. [DERIVED] Graph inspection gives two secret-dependent encryptions; standard independent-message IND-CPA hybrid cannot simply remove either in the presence of the other. [OPEN] Actual KDM security, adequate alternate proof, any concrete attack, or meaningful novel repair.

## CURRENT EVIDENCE
- [FACT] I123 LEAF ePrint **2025/956**, §3.2 Algorithm 1 physical pp14–15 uses `K_pack=Enc_{s_H}(Rep(s_L))`; §3.5 p20 defines `K_switch=Enc_{ι(s_L)}(s_H)`, where degree-N `ι(s_L)(X)=s_L(X^{N/n})`; §3.6 p23 claims combination security follows easily from constituent semantic security, without separately explaining the disclosed key-dependent cycle in that paragraph. Full 43-page mirror PDF SHA256 `937fbae4dcd32f421c91f7df4ad83c3a003861b168f4bfd7798be1476a736267`. Note: `findings/leaf-cross-key-kdm-cycle-security-obligation-iteration123.md`.
- [DERIVED] I123 ONE decisive public-key-dependency test: `s_L → s_H → ι(s_L)`, an effective 2-key KDM/circular-encryption cycle. Because the auxiliary ciphertext of `s_H` is available when replacing encryption under `s_H`, a bare independent-message IND-CPA hybrid is insufficient. This is a **concrete proof obligation**, NOT a known exploit, IND-CPA counterexample against actual BFV, or publishable new technique. NOVELTY NOT VERIFIED.
- [FACT] I122 formal primary source: Brakerski–Döttling TCC2020 ePrint **2020/1185**, full **25 physical pages** through Research MCP mirror, SHA256 `8ee650d5d05d2e7fe33657e35ff5bb9c79be6d16d8a0d8604d8278eb87aa7e46`, official latest VERSION_UNVERIFIED. Theorem **6.9** physical p22 requires `νσ(S)≥n log(γ√n log n)+ω(log λ)` under DSPR+RLWE; RLWE-only variant requires `νσ(S)≥(1/2+α)n log q+O(n log n)`. The source explicitly says binary ring secrets are not covered by these entropic results (§1.1 p4); the conclusion is initially *mild search hardness*, not automatic compiled FHE IND-CPA.
- [DERIVED/NEGATIVE] I122 one theorem-to-parameters test: exact-one-per-block binary secret with n=hL has `H∞(S)=h log₂L`; L=16 yields only `n/4` bits vs ≥`32n` bits of the leading RLWE-only threshold for FAB's q=2^64. Conditional noise-lossiness cannot supply missing source entropy. Thus the theorem does NOT certify this FAB variant; no claim of actual insecurity. Archive `failures/fab-exact-block-entropic-rlwe-theorem-not-applicable-iteration122.md`.
- [FACT] I121 original primary sources: block binary at-most-one including empty blocks [LMSS23, ePrint **2023/958**, §3 physical p6, mirror SHA256 `0ab8c83d5aebbbf0185e200c7c3aab10150aa4e3bad0470a839246d33954e6de`]; exactly-one-per-block already used [SPRU, ePrint **2025/651**, §4.3 p15 and security analysis §4.5 p18]. Published block-key analyses are distribution-specific and not automatically a polynomial-hardness theorem for FAB RLWE. I121 detailed note `findings/fab-block-one-per-block-prior-art-security-gate-iteration121.md`.
- [DERIVED/NEGATIVE] I121 one structural/prior-art falsifier: n=hL, exactly one selector per block gives adjacent interior gap `j_{b+1}-j_b∈[1,2L−1]` so `B=2n/h`, O(h) direct KeyGen; however under uniform fixed-h secrets this structure occurs with probability `L^h/binom(Lh,h)=2^{−Ω(h)}` for fixed L>1 (exponent at L=16: ~1.39664h bits). Thus naive conditioning loses exponential factor and does not preserve the original distribution or establish security. NOVELTY NOT VERIFIED for any new proof.
- [FACT] I120 original ePrint **2025/686**, §6.1–6.2 pp21–22, Appendix C pp33–34: paper uses rejection sampling to enforce bounded interior sparse-key spacing, and reports finite concrete acceptance/security loss δ. It derives amortized SAB work `O(h log B)`, and discusses setting `B=O(n/h)` to reach `O(h log(n/h))` and `O(h)` in a specified linear-h regime.
- [DERIVED/NEGATIVE] I120 one mathematical test: `n=128t, h=8t=n/16, B=32=2n/h`, uniform size-h support. Conditional-Bernoulli counting yields
  `Pr[all consecutive interior gaps < B] ≤ (n+1)[(1-(15/16)^32)^(n/64)+2(15/16)^(n/4)] = poly(n)·exp(-Ω(n))`. Hence naive uniform rejection sampling needs exponential expected trials; **not** a refutation of the paper's finite measurements or FHE algebra. Detailed proof: `findings/fab-bounded-gap-uniform-sparse-rejection-asymptotic-iteration120.md`.
- [FACT] I119 SPRU ePrint 2025/651 (**42 physical pages**, mirror SHA256 `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6`, `VERSION_UNVERIFIED`; rendered arXiv 2607.27401v1 cross-check): Theorem 1 §4.1 p14 requires `Δ ≥ max(4N²κq,(20N³κ)²)` for unoptimized Eq.(8), with positive integer `κ` (§3.1 p7). Table 2 §6.1 p24 reports optimized New boot. `N=2^15, Δ≈2^49, h=64`, ~14-bit precision.
- [DERIVED/NEGATIVE] I119 ONE decisive substitution test at **κ=1**: required `Δ ≥ 400·2^90 ≈ 2^98.64`, ~49.64 bits above Table 2 scale. Thus published **sufficient** theorem bound cannot certify the reported parameters directly; this is NOT an algorithmic correctness/security/benchmark failure, and optimized noise proof may be substantially tighter. NOVELTY NOT VERIFIED.
- [FACT] I117: pinned `fourier_calculator.py` and `fourier_extension.py` use fixed **300** composite Simpson-3/8 panels for each half-period Fourier integral independent of harmonic index. Python source call chain is real.
- [DERIVED] I117 exact, source-equivalent *plaintext* test for `f(x)=x`, high-degree `n=216`, bridge smoothness `speed=2`: at harmonic 216, analytic `b_216≈+7.6806923566e−8`, 300-panel `b_216≈−2.3543473241e−5`; panel-refinement converges to analytic value. At harmonic 201, spuriously `b_201≈−0.0615958932`. Across 2,049 sample points, full Fourier reconstruction max error ≈0.125 versus ≈3.11e−6 with analytic coefficients. This is a reproducible **preprocessing numerical problem**, not a CKKS security/noise failure.
- [FACT] I118: author pin's **39 modified paths across 7 commits** provide continuous `gelu_test.cpp` **n44/speed12**, sigmoid n34, exp n29, boot n25, and corresponding shipped coefficient files. Explicit path: `gelu_test.cpp → fbs_utils.h → src/core/lib/math/fourier.cpp → fourier_calculator.py` when online; `-f` bypasses Python and loads precomputed `gelucoeff.txt` header44.
- [NEGATIVE] No public pinned dedicated **discrete LUTGeLU n216** example or coefficients found in this author's changed-file inventory. Thus **NO demonstrated effect on published Table 3 LUTGeLU n216**, no verified published precision error, no actual encrypted benchmark run, and no proof of cryptographic novelty.

## MAIN OBSTRUCTION
I123's key-dependency loop has real proof relevance to LEAF's cross-ring conversion and public evaluation keys. **Circular/KDM requirements are established prior art in FHE**, however; without a theorem-level incompatibility or novel cost/security preserving repair, the observation is not itself a contribution. Avoid wasting iterations on repetition. Previously FAB I120–122 was PARKED for low-novelty block-secret repair and stringent formal hardness problems.

## OPEN UNCERTAINTY
[OPEN] Whether existing *specific* affine-KDM/2-circular security proofs cover LEAF's paired BFV auxiliary-key encryptions when `ι(s_L)` is a deterministic ring-degree embedding. The existence of some KDM theorem alone is not enough; verify exact message class, scheme, ring, modulus, and assumptions. No attack/reduction proved here.
[OPEN, PARKED] FAB I120–122 security/efficiency frontier, SPRU I119 noise bound, FEFBS I117–118 published LUTGeLU provenance; original vFHE CRT lookup ideal-IOP finding remains archived/preserved (not compiled forgery).

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION
**PI decision before I124**: (A) authorize a single theorem-applicability hypothesis for one carefully sourced existing *affine/linear KDM or 2-circular* result, against LEAF's exact paired key material; cheapest test is comparing its security game, secret distribution and embedding to Algorithm 1/§3.5. If already settled, PARK LEAF and do not rehash KDM basics. OR (B) delegate selection of a different high-value FHE structural target. No research without authorization, author contact or public disclosure.

## RELEVANT FILES — READ IN NEW CHAT
1. `START_RESEARCH_SESSION.md`, `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, **this `STATE.md`**.
2. **I123** `findings/leaf-cross-key-kdm-cycle-security-obligation-iteration123.md`.
3. **I122** `failures/fab-exact-block-entropic-rlwe-theorem-not-applicable-iteration122.md`.
4. **I121** `findings/fab-block-one-per-block-prior-art-security-gate-iteration121.md`.
5. **I120** `findings/fab-bounded-gap-uniform-sparse-rejection-asymptotic-iteration120.md`.
6. **I119** `findings/spru-theorem1-table2-sufficient-bound-gap-iteration119.md`.
7. `findings/fefbs-fixed-simpson38-high-harmonic-aliasing-iteration117.md`
8. `findings/fefbs-lutgelu-216-coefficient-provenance-gate-iteration118.md`
9. `failures/fefbs-high-degree-quadrature-benchmark-impact-unverified-parked-iteration118.md`
10. **Exact complete prior verbose STATE**: `logs/state-pre-session-handoff-2026-10-12-iteration118.md` (preserved blob SHA `935d61d8d7e1cf23c21771223ec67dbb7d70d492`).
11. Historical state chain `logs/state-pre-iteration115-prca-handoff.md`, `logs/vfhe-state-2026-10-12-pre-paco-handoff.md`; retrieve specific findings/failures **only if** the PI selects those topics.

## BRANCH STATUS / DO NOT DELETE
**HUMAN_REVIEW:** LEAF cross-key KDM proof obligation I123 (no attack; novelty unverified). **PARKED:** FAB bounded-gap sparse-secret I120–122 (I120 rejection barrier retained, I121 trivial block-key repair known, I122 entropic RLWE theorem inapplicable). **PARKED:** SPRU Theorem-1/Table-2 proof-bound mismatch I119 (not a practical failure). **PARKED:** FEFBS I117–118; LFBS PRCA I114–116 (`failures/lfbs-prca-source-only-layout-low-novelty-parked-iteration116.md`); Paiva incomplete-NTT key portability I112–113; sparse-SAB local terminal sign I110–111; Carousel rounding I108–109; SIMD-ALU cutoff I103–107; Nested-RNS I99–102; PaCo precision I95–98; RIG. **ARCHIVED:** GL generic BigSwitch; specific vFHE bounded-public-A/direct Brakedown repair. **PRESERVED OPEN FINDING, not ACTIVE:** original vFHE CRT lookup ideal-IOP discrepancy ePrint2025/286. All historical results retained in archives and exact STATE snapshots.

## STATUS
**I123_CLOSED / HUMAN_REVIEW / NO_ACTIVE_HYPOTHESIS.** Last completed iteration 123. I124 not started. I123 finding and STATE read-back verified. No author contact, GitHub issues, PRs or external disclosure.

## RESEARCH PROTOCOL
Read before write. One smallest falsifiable hypothesis plus one cheapest decisive test per iteration. Mark [FACT]/[DERIVED]/[HYPOTHESIS]/[NEGATIVE]/[OPEN]; distinguish noiseless algebra, numeric approximation, CKKS feasibility and actual compiled tests. Preserve evidence provenance, hashes and negative results. Do not modify `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, or `START_RESEARCH_SESSION.md` as part of handoff.
