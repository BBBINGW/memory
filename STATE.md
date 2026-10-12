# Research State — 2026-10-12

ACTIVE: **vFHE, CRT lookup soundness audit → efficient cross-CRT repair**.
PARKED: **RIG-HE**; complete prior `STATE.md` preserved verbatim at `logs/rig-state-2026-10-12-pre-vfhe-handoff.md` (NOT archived; do not discard its findings).
ARCHIVED SPECIFIC BRANCH: GL generic BigSwitch; see `failures/gl-generic-bigswitch-structure.md`. All other older research files retain their own statuses.

## CURRENT TARGET
Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint **2025/286**, especially §4.3 / Theorem 4.8 / Appendix E.2 (CRT digit lookup), §4.1–4.2 (CKKS rescale and ΠAC), and **§5 componentwise Brakedown polynomial commitments**.
Research MCP mirror: 52pp PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, mirrored 2026-04-28 after 2026-02-16 official revision; **latest official binary VERSION_UNVERIFIED**.

LAST COMPLETED ITERATION: **80 (2026-10-12)**. Direct DualPCS–Brakedown bridge FAIL; see I80 archive.

## CURRENT QUESTION
The original vFHE Brakedown PCS has no off-the-shelf hidden cross-characteristic link to an external integer commitment. Is an architecture-changing ZK CRT repair worth pursuing, or should the repair-optimization branch pause after the source-level soundness audit?

## PRIMARY HYPOTHESIS — I80 RESOLVED; HUMAN DECISION PENDING
**FAIL** for direct Ganesh–Nair–Sharma CCS 2024 DualPCS linking of the original Brakedown field PCS aggregate to a hidden canonical external residue. No new technical hypothesis is authorized until the PI decides whether changing/co-designing the commitment architecture is acceptable.

## CURRENT EVIDENCE
- [FACT/SOURCE + DERIVED, I59–70] Audited revised-looking proof uses an invalid diagonal-digit ⇒ illegal CRT component inference. Fieldwise lookup supports rectangular `T_B^rect`, not the claimed global coefficient range; `B≥max p_i` makes `T_B^rect=R_q`. Explicit ring/PIOP counterexamples recorded.
- [DERIVED/PASS, I71–76] Small paper-format CKKS instance `q=149·157·173=4046989`: zero inputs must output 0, but claimed bounded public output `y=173` with illegal remainder `r=4017060` satisfies `-r-173y=-q`. Eq.(16)–(20), source-equivalent adaptive six-step ideal-oracle ΠAC checks and negative oracle-tamper controls PASS. **No compiled SNARK forgery / realistic secure-parameter attack established.**
- [NEGATIVE, I63–68, I77–78] CRT-local equations, simple encoder variants, reduced commitments and post-challenge CRT aggregate patching do not enforce the global integer witness. If exact externally bound integer aggregate is certified, random Boolean linear checks have ≤1/2 false-pass probability per round for a fixed wrong component, but publicly revealing the aggregate leaks information.
- [NEGATIVE / REFINED FIX, I79] `P>T=m(β−1)` alone is insufficient for an external hidden `A=u_k+p_kc_k (mod P)` carry proof: `T=1920, P=1931, A=144, u_173=172,c_173=11` yields `2075=144+1931`. Require `P>max_k(T, p_k·floor(T/p_k)+p_k−1)` or an explicit RHS≤T range proof. **This fixes only integer no-wrap, not PCS linking.**
- [NEGATIVE / SOURCE + DERIVED, I80] ePrint 2025/286 §5/Appendix F uses per-field Merkle/code Brakedown PC and exposes native evaluation vector/value; ePrint 2024/943 §5 DualPCS links TWO compatible schemes over ONE prime field (KZG-FFT-FOURIER or Dory/Linear-Rel), not arbitrary Brakedown↔external F_P commitments. No unital field hom F_(p_k^d)→F_P for different primes. Direct off-the-shelf hidden-residue bridge FAIL. Straight full-verifier wrapping would process O(μ(t+1)√n) extension-field symbols plus hashing/non-native checks; this is NOT a universal lower bound or benchmark. See `failures/vfhe-brakedown-dualpcs-cross-characteristic-interface-iteration80.md`.

## MAIN OBSTRUCTION
[OPEN] No verified efficient *hiding, knowledge-sound* interface `C_{u_k} ↔ field PCS(Σα_i h_{k,i})` across different characteristics. Direct DualPCS reuse fails due to PCS/type/characteristic mismatch and public Brakedown openings; wrapping its verifier non-natively may negate efficiency.

## OPEN UNCERTAINTY
Latest official PDF SHA/version; full authors' optimized protocol/PCS/Fiat–Shamir implementation; deployed or secure-parameter effect; complete repair/soundness/privacy/cost proof; novelty relative to dual-PCS/CP-NIZK. **No authors contacted. User says DO NOT SEND EMAIL; no outreach/draft/public disclosure without explicit new permission.**

## NEXT_ACTION — HUMAN_REVIEW (ONE DECISION)
PI decide whether replacing/co-designing the existing vFHE Brakedown PCS interface to pursue a dedicated hiding cross-characteristic CRT witness link is an acceptable architectural investment. If not, pause the repair-optimization branch and retain the proven source-level CRT lookup soundness gap as the active audit result. Do not automatically develop adjacent repair variants or contact authors.

## RELEVANT FILES
- Protocol/start: `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `START_RESEARCH_SESSION.md`.
- Last I80: `failures/vfhe-brakedown-dualpcs-cross-characteristic-interface-iteration80.md`.
- I79: `failures/vfhe-hidden-aggregate-carry-wrap-even-when-P-above-T-iteration79.md`.
- I78 and I77: `failures/vfhe-batched-crt-aggregate-without-shared-integer-opening.md`, `findings/vfhe-external-commitment-crt-full-opening-link-iteration77.md`.
- Gap: `findings/vfhe-crt-lookup-cross-component-soundness.md`, `findings/vfhe-theorem48-actually-sound-rectangular-relation.md`.
- CKKS impact: `findings/vfhe-ckks-public-output-binding-robust-rescale-counterexample.md`, `findings/vfhe-piac-adaptive-six-step-oracle-binding-audit.md`.
- Version: `findings/vfhe-theorem48-post-revision-mirror-provenance-diff.md`.
- UNSENT report/draft: `findings/vfhe-confidential-pi-review-package-iteration74.md`, `findings/vfhe-confidential-author-inquiry-draft-iteration75.md`.
- PARKED RIG: `logs/rig-state-2026-10-12-pre-vfhe-handoff.md`.

STATUS: **ACTIVE vFHE audit; I80 FAIL direct DualPCS–Brakedown linking; HUMAN_REVIEW on repair architecture**. No general cross-characteristic impossibility, full SNARK forgery, or complete ZK repair established.
