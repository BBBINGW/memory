# FHE Research State — After Iteration 122
Checkpoint: **2026-10-12, after Iteration 122**.

## CURRENT TARGET
**None ACTIVE.** FAB bounded-gap sparse-key branch I120–122 is now **PARKED**: I120 proved exponential uniform-secret rejection-sampling in a valid asymptotic family; I121 showed trivial exact-one-per-block sampler is existing prior art and changes the security distribution; I122 formally ruled out direct use of known Brakerski–Döttling entropic Ring-LWE Theorem 6.9 to certify this binary block-secret under RLWE-only assumptions. Neither actual FAB ciphertext correctness nor published finite benchmarks were broken. Previously SPRU proof-bound I119 and FEFBS numerical-provenance I117–118 remain PARKED.

## LAST COMPLETED ITERATION
**122**. I123 NOT started.

## CURRENT QUESTION
**HUMAN_REVIEW / NO_ACTIVE_HYPOTHESIS:** PI must authorize a different FHE paper + structural hypothesis (or explicitly authorize agent paper selection). No open primary claim remains in the FAB keygen branch. Reopen FAB only for an independently sourced nontrivial security-reduction technique, not repeated block-key or entropy calculations.

## PRIMARY HYPOTHESIS
**NONE ACTIVE.** Last closed [HYPOTHESIS] I122: TCC2020 entropic Ring-LWE Theorem 6.9 already directly proves suitable exact-one-per-block binary RLWE security under FAB's weak-assumption parameter setting. [NEGATIVE] Fails explicit noise-lossiness/entropy precondition. Known theorem is not an FHE security attack or a novel gap.

## CURRENT EVIDENCE
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
I120 proved exponential rejection cost for uniform fixed-weight bounded-gap keys; I121's simple exact-one-per-block fix is already known and changes distribution; I122 ruled out applying the known general TCC2020 entropic RLWE theorem because of a huge secret-entropy prerequisite mismatch. A genuine new reduction for short structured RLWE is a deep separate problem, without demonstrated FHE frontier gain. **PARK FAB I120–122, do not continue source-only microaudits.**

## OPEN UNCERTAINTY
[OPEN, PARKED] Whether a nontrivial novel polynomial-hardness security proof for exact-one-block *RLWE* exists or can be designed under FAB's parameters, and if it can alter a real FHE frontier. No such proof found or developed; never claim all literature is exhaustively excluded.
[OPEN, PARKED] I119 optimized SPRU noise; I117–118 LUTGeLU n216 coefficient provenance. Historical vFHE CRT lookup ideal-IOP finding preserved, NOT a compiled forgery.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION
**PI decision gate for I123:** Only launch if PI explicitly selects one new structural FHE paper/technical claim OR delegates selecting a new non-recycled research target. Then one smallest falsifiable hypothesis + one cheapest decisive test. Current FAB I120–122 branch PARKED; no immediate technical test remains. No repeated low-novelty audits or author outreach.

## RELEVANT FILES — READ IN NEW CHAT
1. `START_RESEARCH_SESSION.md`, `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, **this `STATE.md`**.
2. **I122** `failures/fab-exact-block-entropic-rlwe-theorem-not-applicable-iteration122.md`.
3. **I121** `findings/fab-block-one-per-block-prior-art-security-gate-iteration121.md`.
4. **I120** `findings/fab-bounded-gap-uniform-sparse-rejection-asymptotic-iteration120.md`.
5. **I119** `findings/spru-theorem1-table2-sufficient-bound-gap-iteration119.md`.
6. `findings/fefbs-fixed-simpson38-high-harmonic-aliasing-iteration117.md`
7. `findings/fefbs-lutgelu-216-coefficient-provenance-gate-iteration118.md`
8. `failures/fefbs-high-degree-quadrature-benchmark-impact-unverified-parked-iteration118.md`
9. **Exact complete prior verbose STATE**: `logs/state-pre-session-handoff-2026-10-12-iteration118.md` (preserved blob SHA `935d61d8d7e1cf23c21771223ec67dbb7d70d492`).
10. Historical state chain `logs/state-pre-iteration115-prca-handoff.md`, `logs/vfhe-state-2026-10-12-pre-paco-handoff.md`; retrieve specific findings/failures **only if** the PI selects those topics.

## BRANCH STATUS / DO NOT DELETE
**PARKED:** FAB bounded-gap sparse-secret I120–122 (I120 rejection barrier retained, I121 trivial block-key repair known, I122 entropic RLWE theorem inapplicable). **PARKED:** SPRU Theorem-1/Table-2 proof-bound mismatch I119 (not a practical failure). **PARKED:** FEFBS I117–118; LFBS PRCA I114–116 (`failures/lfbs-prca-source-only-layout-low-novelty-parked-iteration116.md`); Paiva incomplete-NTT key portability I112–113; sparse-SAB local terminal sign I110–111; Carousel rounding I108–109; SIMD-ALU cutoff I103–107; Nested-RNS I99–102; PaCo precision I95–98; RIG. **ARCHIVED:** GL generic BigSwitch; specific vFHE bounded-public-A/direct Brakedown repair. **PRESERVED OPEN FINDING, not ACTIVE:** original vFHE CRT lookup ideal-IOP discrepancy ePrint2025/286. All historical results retained in archives and exact STATE snapshots.

## STATUS
**I122_CLOSED / HUMAN_REVIEW / NO_ACTIVE_HYPOTHESIS.** Last Iteration 122 completed and negative result read back. I123 not started. No author contact, issues, PRs, or public disclosure. PI decides future direction.

## RESEARCH PROTOCOL
Read before write. One smallest falsifiable hypothesis plus one cheapest decisive test per iteration. Mark [FACT]/[DERIVED]/[HYPOTHESIS]/[NEGATIVE]/[OPEN]; distinguish noiseless algebra, numeric approximation, CKKS feasibility and actual compiled tests. Preserve evidence provenance, hashes and negative results. Do not modify `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, or `START_RESEARCH_SESSION.md` as part of handoff.
