# FHE Research Opportunity Backlog

**Reviewed:** 2026-10-13, after I139; I140 not yet begun.  
**Location:** `findings/OPEN_RESEARCH_BRANCHES.md` (the Research MCP presently disallows creating new root-file names).  
**Authority:** `STATE.md` remains the only authoritative *current iteration / NEXT_ACTION* entry point; this file is a **long-term opportunity index**, never an instruction to launch multiple research hypotheses. PI decides research direction, reopening, contribution and disclosure.

**Status definitions:** `OPEN/HUMAN_REVIEW` = evidence-backed question without verified full fix; `PARKED/REOPEN_IF` = stop repeating known unsuccessful proposals, only revisit with a new material premise; `ARCHIVED_SPECIFIC_REPAIR` = particular attempted solution unsuitable, **not necessarily** entire research problem. Evidence levels: [FACT] primary source, [DERIVED] exact implication, [NEGATIVE] failed claim, [OPEN] unanswered. No publication, performance or security claim without independent verification.

## P1 — vFHE: soundness-preserving, efficient CRT scalar lookup (OPEN/HUMAN_REVIEW)

**Paper:** Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint **2025/286**, §4.3 Theorem 4.8 and Fig.1, §5 / Appendix F.2. Inspected mirror is a **52-page revised-looking version, official latest binary VERSION_UNVERIFIED**.

**[DERIVED/TESTED] Hole:** independent CRT field digit membership does not force a **common scalar/diagonal table index** in the product ring. I59 constructs an ideal lookup false-statement accepted transcript; I60 checks composed `Π_range` and fieldwise PCS and finds no automatic cross-component scalar-coherence enforcement. **Not a compiled end-to-end SNARK forgery, deployed compromise or confirmed latest-edition defect**.

**[NEGATIVE] Already tested:** direct native Brakedown, bounded-public-A aggregates, same-h masked sumchecks, scalar repeated challenges. Conditional ideal soundness can be strengthened, but original source PCS opens thousands of constituent field evaluations and costs are not demonstrated practical. I95 archives **only** the bounded-public-A/direct-Brakedown repair, **not the underlying CRT finding**. **I136 NEGATIVE (new distinct PCS batching shortcut):** enforcing a common Brakedown `q2` suffix to combine four terminal openings forces shared Sumcheck suffix challenge(s), destroying the fourth-power independent-soundness argument; explicit 4-variable false-sum Sumcheck prover over scalar S=F29 succeeds for all four repetitions on shared last challenge 1 with probability **1/29**, not **1/29^4**, even when each mixing ρ and other r-coordinates are sampled independently. This does NOT rule out a newly designed multi-point PCS preserving independent query coordinates. **I137 NEGATIVE, independent coordinates retained:** The §5/F.2 multilinear matrix evaluation is rank-one `q1(a)^T U q2(a)`. Four distinct independently eligible terminal query points can yield rank-four aggregate coefficient `M=Σλ_j q1(a_j)q2(a_j)^T` (explicit F29 four-variable test det(M)=6). Therefore a 4-in-1 **single unchanged F.2 vector** linear fold is algebraically impossible in general; conditional raw 4-eval vector costs persist (I94 scenarios 150–800 MiB). This is a scoped classical rank bound, not universal batched-PCS impossibility, source flaw or new theorem. **I138 FAIL cheaper Merkle-only batching:** sharing Q' sampled AFTER all four evaluation vectors are committed/sent can preserve each source F.2 per-opening check conditionally without sharing any Sumcheck challenge (PCS false-opening union bound ≤4ε_field per CRT component, NOT fourth-power PCS soundness). But mandatory 4 source v' vectors and only one reused set of t encoded columns imply four-independent-vs-shared field-symbol cost ratio `4(1+t)/(4+t)<4` (Merkle-only reuse also saves at most 4 copies), so this limited edit cannot meet 10× communication goals. The source actually explicitly amortizes TESTING phase, not EVALUATION. A full new PCS remains unknown; do not continue cosmetic Brakedown tweaks.

**[OPEN] Need:** a new low-cost *same-index across components* proof/lookup/PCS relation with soundness, Fiat–Shamir compilation, privacy and credible communication/verification savings. Novelty uncertain.

**Next gate on explicit PI authorization:** **PARK the three direct F.2 micro-batching tweaks (I136 shared q2, I137 single-vector rank1 fold, I138 same-Q' Merkle column reuse)**. A new vFHE effort must instead specify a genuinely different arbitrary-rank multi-point PCS or a different cross-CRT integer-index proof, preserve independent Sumcheck terminal challenges, and present a falsifiable ≥10× source-comparable communication/binding advantage. Otherwise prioritize a different FHE target such as MRFHE dense second-switch PCMM. Confirm latest official version before any source flaw/public disclosure claim. Confirm official edition. **No author contact/public disclosure/email without PI approval.**

**Evidence:** `failures/vfhe-common-merkle-eval-columns-fourfold-cost-ceiling-iteration138.md`; `failures/vfhe-independent-multipoint-brakedown-rank-four-eval-folding-iteration137.md`; `failures/vfhe-shared-brakedown-q2-challenge-fourfold-soundness-iteration136.md`; `findings/vfhe-crt-lookup-cross-component-soundness.md`; `findings/vfhe-crt-full-range-piop-and-commitment-audit.md`; `findings/vfhe-fourfold-scalar-sumcheck-amplification-cost-iteration94.md`; `failures/vfhe-bounded-public-A-direct-brakedown-repair-archived-iteration95.md`; `findings/vfhe-confidential-pi-review-package-iteration74.md`; `logs/vfhe-state-2026-10-12-pre-paco-handoff.md`.

## P2 — MRFHE auxiliary-Y cross-batch packing (PARKED / REOPEN_IF)

**Paper:** Cheon et al., MRFHE, ePrint **2026/853**, §5.1–5.2; supplied 18-page full PDF previously read.

**[DERIVED] Candidate:** I32 shows algebraically independent batch packing into spare Y coefficients and favorable conditional PCMM amortization. I34 bounds isolated one-switch toy noise. **No full actual FHE speedup proven.**

**[NEGATIVE] Prior tests:** second key switch generally destroys hoped-for sparse Y support after PCMM (I35); simple W-independent keys undermine security dimension; CKL no-conversion substitutions fail.

**[OPEN] Need:** complete two-switch PCMM+rescale noise, digit decomposition and matched security/latency costs. **[PASS symbolic source parameter gate I139]:** source Table5 FHE(8,5), n1=64,d=243, has K=2/3 entire original 64-ciphertext cohorts fitting ONE auxiliary Y block. Under I32's general count including fully **dense second KS** `C_K=3+4d ceil(Kn1/d)/(Kn1)`, C1=18.1875, C2=10.59375, C3=8.0625 => theoretical R-ring KS-equivalent gain 1.7168× / 2.2558×. K4 requires two blocks and regresses. Other Table5 shapes only 0–11.7% in K2/K3. Compared with independent K1, added joint conversion/memory/modulus overhead must stay below 972 (K2) or 1944 (K3) base-switch equivalents per cohort. **NO source FHE(8,5) batch benchmark, full noise/precision/security proof or new algorithm.** I33/I35 negative noise/density facts unchanged; novelty against existing CKL/MRFHE batch schemes uncertain.

**Next gate (I140 only if PI authorizes):** for source FHE(8,5), K1 vs K2 with unchanged full original secret/switching key, quantify **first KS → actual D′2 PPMM → second KS → rescale** noise, precision, remaining modulus/security budget, and nonamortizable repacking; kill if consumes the 972 switch-equivalent margin. Do not retry I35 sparse-Y support tests.

**Evidence:** `findings/mrfhe-source-table5-multibatch-dense-ks-frontier-iteration139.md`; `findings/mrfhe-aux-ring-cross-batch-coefficient-packing.md`; `findings/mrfhe-joint-packing-lifted-ks-noise.md`; `failures/mrfhe-joint-packing-second-switch-sparsity.md`; `failures/mrfhe-joint-packing-noise-isolation.md`.

## P3 — Rectangular encrypted matrix multiplication and output-block costs (PARKED / SOURCE BLOCKED)

**Paper:** Aikata & Roy, *Secure and Efficient Outsourced Matrix Multiplication with Homomorphic Encryption*, INDOCRYPT 2024, ePrint **2024/1730**, §4.2 pp18–19. Original author-associated artifact address printed in §5: `https://anonymous.4open.science/r/MatMul-0568`.

**[DERIVED] Constraint (I134):** source packing formula `S=k p²`, k=max(l,d,t), p=min(l,d,t), can be smaller than the number of explicit output entries `l t`. In standard separately linear-preprocessed, componentwise Ct×Ct and linearly-postprocessed SIMD matmul, `#CtCt≥ceil(l t/S)`. Example (8×2) by (2×8): S=32, 64 linearly independent bilinear coordinates, ≥2 product calls. This **does not show** source implementation incorrectly omitted output blocks; row representation and “no increase” baseline are ambiguous. Related conventional output factor already audited in CKL I38.

**[OPEN] Need:** first resolve **MISSING_CRITICAL_SOURCE**: paper's exact anonymous artifact `https://anonymous.4open.science/r/MatMul-0568` returned inaccessible. I135 verified that author's separately released FHERMA challenge explanation and an independent `MatrixMult_AR24` reproduction cover **square** inputs/outputs only; neither verifies paper §4.2's rectangular routines. No published source-code bug was found. See `MISSING_SOURCES.md` for source recovery. Only then contemplate a genuinely new repaired layout; rank counting alone is classical, not a contribution.

**Next gate (I135):** inspect actual published artifact's rectangular branch and output interface, or source algorithm if unavailable. If ≥2 output products already accounted for, PARK this issue promptly.

**Evidence:** `findings/aikata-roy-rectangular-output-bilinear-capacity-gate-iteration134.md`; `failures/ckl-rectangular-cpmm-missing-output-block-factor.md`.

## P4 — FAB bounded-gap sparse-key security/KeyGen (PARKED / REOPEN_IF)

**Paper:** Guimarães & Pereira, *Fast amortized bootstrapping with small keys and polynomial noise overhead*, CCS 2025, ePrint **2025/686**.

**[DERIVED] Obstruction:** sampling uniformly fixed-weight sparse binary ring keys then rejecting until bounded inter-support gaps can have exponentially low acceptance (I120). **[NEGATIVE]** exactly-one-nonzero-per-block is old, changes distribution, and the examined entropic Ring-LWE theorem does not justify its target binary secret without new assumptions (I121–122). Not an attack.

**[OPEN] Need:** nontrivial efficient generator *and* suitable hardness reduction, parameter/security/key-noise-cost gain. Do not repeat block-key prior art.

**Evidence:** `findings/fab-bounded-gap-uniform-sparse-rejection-asymptotic-iteration120.md`; `findings/fab-block-one-per-block-prior-art-security-gate-iteration121.md`; `failures/fab-exact-block-entropic-rlwe-theorem-not-applicable-iteration122.md`.

## P5 — Online TFHE ψ-automorphism × dynamic GGSW (PARKED / REOPEN_IF)

**Paper:** Bernard–Joye, ASIACRYPT 2025, ePrint **2025/163**, §4.1.

**[NEGATIVE]** I125 ordinary online GGSW cannot be dropped into ψ-fused external product: extra `μbar·ψ(a)(ψ(s)-s)` term; ψ-specific helper key is *already source-defined*. Not a paper flaw.

**[OPEN] Need:** new online ψ-compatible key representation/gadget fusion lowering total noise, evaluation-key storage and online cost; no specific solution found.

**Evidence:** `failures/bj-automorphism-extended-external-product-ordinary-online-gadget-iteration125.md`.

## Watchlist (not currently executable priority)

- **MOAI paired BSGS I126–133: PARKED**. An exact *candidate algorithm exists* in I128/I130, so not “no scheme”. CKKS half-wise mask precision/scale, rescale modulus, output error and half-batch throughput obstruct claimed implementation benefit. I133 canonical N65536 mask can induce 0.01782 error for a rank-one attention stress case against **researcher-chosen**, not paper-required, max-0.01 stage screen; not universal infeasibility or BERT accuracy finding. `findings/moai-native-paired-bsgs-halfwise-rotation-cost-iteration130.md`; `failures/moai-n65536-low-scale-paired-mask-precision-gate-iteration133.md`.
- **CKKS sparse CtS/StC and LCR+AKS I40–45: PARKED**. Ideal Fourier/SubSum relation, no validated end-to-end savings; direct recent prior art Zheng ePrint 2026/1023. `findings/ckks-lcr-aks-sparse-subsum-fourier-projection.md`; `failures/ckks-sparse-transform-novelty-2026-1023.md`.
- **LEAF cross-key KDM I123–124: PARKED proof obligation**. Explicit helper-key cycle but no BFV attack or new security proof; general multiuser KDM prior art. `findings/leaf-cross-key-kdm-cycle-security-obligation-iteration123.md`; `failures/leaf-bv11-multikey-kdm-theorem-not-directly-applicable-iteration124.md`.
- **RIG-HE: PARKED not archived**. Exact weak-modulus Fourier candidate, literature already overlaps; novelty not verified. `findings/rig-fourier-state-snapshot.md`; `logs/rig-state-2026-10-12-pre-vfhe-handoff.md`.
- **SPRU noise theorem vs table I119: PARKED**, plausible tighter proof missing but no actual failure. `findings/spru-theorem1-table2-sufficient-bound-gap-iteration119.md`.
- **FEFBS Fourier preprocessing I117–118: PARKED**, high-harmonic aliasing synthetic, no actual benchmark source impact; known numerical repair. `findings/fefbs-fixed-simpson38-high-harmonic-aliasing-iteration117.md`; `failures/fefbs-high-degree-quadrature-benchmark-impact-unverified-parked-iteration118.md`.
- **Prior explicitly closed/parked microaudits** include CKL left/right MRFHE shortcuts, GL generic BigSwitch, Paiva cross-level BK, Nested-RNS CRT small-weights, LFBS PRCA, SIMD-ALU cutoff, PaCo, Grafting, Carousel and threshold-CKKS tuning. Their individual `failures/` and historical `logs/` contain exact closure reasons; don't resurrect a failed assertion without new evidence.

## Update rules

1. Resume with `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → `STATE.md`. This file supplements, never supersedes, STATE.
2. Consult backlog **only** when PI requests opportunity review or delegates selecting a target. Every new iteration takes exactly one primary falsifiable claim plus one minimal decisive test, not five parallel tracks.
3. Update backlog **only when a branch's research status, best evidence, or reopening conditions materially change**; update STATE whenever latest round/NEXT_ACTION changes.
4. Preserve provenance and negative results, distinguish paper statements from our conjectures and empirical simulations from actual CKKS security/precision/performance; don't claim novelty from mere absence of prior search hits.
5. PI approves archive/continue/pivot, external author contact and public disclosure. No automatic background research.
