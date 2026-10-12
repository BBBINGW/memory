# Research State — 2026-10-12

ACTIVE: **vFHE, CRT lookup soundness audit → efficient cross-CRT repair**.
PARKED: **RIG-HE**; complete prior `STATE.md` preserved verbatim at `logs/rig-state-2026-10-12-pre-vfhe-handoff.md` (NOT archived; do not discard its findings).
ARCHIVED SPECIFIC BRANCH: GL generic BigSwitch; see `failures/gl-generic-bigswitch-structure.md`. All other older research files retain their own statuses.

## CURRENT TARGET
Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint **2025/286**, especially §4.3 / Theorem 4.8 / Appendix E.2 (CRT digit lookup), §4.1–4.2 (CKKS rescale and ΠAC), and **§5 componentwise Brakedown polynomial commitments**.
Research MCP mirror: 52pp PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, mirrored 2026-04-28 after 2026-02-16 official revision; **latest official binary VERSION_UNVERIFIED**.

LAST COMPLETED ITERATION: **82 (2026-10-12)**. Evaluation-only masked Brakedown opening FAIL hidden cross-domain link; see I82 archive.

## CURRENT QUESTION
Does the original vFHE security model actually require zero-knowledge/hiding of each native Brakedown evaluation and CRT aggregate, or is that a stricter constraint introduced in our proposed repair? Clarify before investing in extensive ZK PCS redesign.

## PRIMARY HYPOTHESIS — NEXT, NOT YET TESTED
Source §2.2 / §5 may define only commitment binding / knowledge soundness and public polynomial evaluations rather than zero knowledge. If the *intended application privacy* still requires keeping witness-dependent CRT digit aggregates hidden, merely dropping ZK is not a valid workaround. The next iteration is one source-backed security-goal audit, NOT a new repair proposal.

## CURRENT EVIDENCE
- [FACT/SOURCE + DERIVED, I59–70] Audited revised-looking proof uses an invalid diagonal-digit ⇒ illegal CRT component inference. Fieldwise lookup supports rectangular `T_B^rect`, not the claimed global coefficient range; `B≥max p_i` makes `T_B^rect=R_q`. Explicit ring/PIOP counterexamples recorded.
- [DERIVED/PASS, I71–76] Small paper-format CKKS instance `q=149·157·173=4046989`: zero inputs must output 0, but claimed bounded public output `y=173` with illegal remainder `r=4017060` satisfies `-r-173y=-q`. Eq.(16)–(20), source-equivalent adaptive six-step ideal-oracle ΠAC checks and negative oracle-tamper controls PASS. **No compiled SNARK forgery / realistic secure-parameter attack established.**
- [NEGATIVE, I63–68, I77–78] CRT-local equations, simple encoder variants, reduced commitments and post-challenge CRT aggregate patching do not enforce the global integer witness. If exact externally bound integer aggregate is certified, random Boolean linear checks have ≤1/2 false-pass probability per round for a fixed wrong component, but publicly revealing the aggregate leaks information.
- [NEGATIVE / REFINED FIX, I79] `P>T=m(β−1)` alone is insufficient for an external hidden `A=u_k+p_kc_k (mod P)` carry proof: `T=1920, P=1931, A=144, u_173=172,c_173=11` yields `2075=144+1931`. Require `P>max_k(T, p_k·floor(T/p_k)+p_k−1)` or an explicit RHS≤T range proof. **This fixes only integer no-wrap, not PCS linking.**
- [NEGATIVE / SOURCE + DERIVED, I80] ePrint 2025/286 §5/Appendix F uses per-field Merkle/code Brakedown PC and exposes native evaluation vector/value; ePrint 2024/943 §5 DualPCS links TWO compatible schemes over ONE prime field (KZG-FFT-FOURIER or Dory/Linear-Rel), not arbitrary Brakedown↔external F_P commitments. No unital field hom F_(p_k^d)→F_P for different primes. Direct off-the-shelf hidden-residue bridge FAIL. Straight full-verifier wrapping would process O(μ(t+1)√n) extension-field symbols plus hashing/non-native checks; this is NOT a universal lower bound or benchmark. See `failures/vfhe-brakedown-dualpcs-cross-characteristic-interface-iteration80.md`.

- [NEGATIVE / DERIVED + EXACT TEST, I81] Standard prime-order Pedersen/IPA native-additive map `F_(p_k^d)→G` is trivial unless group order equals p_k; with paper's ~49-bit primes, p_k-order discrete logarithm costs O(√p_k)≈2^24.5, far below ~128-bit binding. Toy BSGS recovered a subgroup generator relation and produced two openings to one commitment. Excludes this conventional shortcut, not hash-based PCS or non-native ZK. See `failures/vfhe-native-field-pedersen-ipa-49bit-group-security-iteration81.md`.

- [NEGATIVE / SOURCE + EXACT TEST, I82] Appendix F.2 native Brakedown checks can authenticate hypothetical masked w=q1(U_f+U_z) when a separate mask matrix is bound, but those equations never link the hidden original <q1U_f,q2> to an independent external canonical C_u. Toy F101/F211 satisfies both independent checks while native y=0 and external u=1. Also the original testing phase exposes v=rU_f, so evaluation-only masking cannot yield general ZK. This merely reestablishes I77–78 independent-commitment obstruction for a concrete masked interface; not an original-protocol forgery. See `failures/vfhe-masked-brakedown-evaluation-unlinked-hidden-residue-iteration82.md`.

## MAIN OBSTRUCTION
[OPEN] No verified efficient cross-characteristic, knowledge-sound interface `C_{u_k} ↔ field PCS(Σα_i h_{k,i})`. Direct DualPCS and masked-only Brakedown reuse both fail to create the link; current proposed additional hiding/ZK requirement must first be checked against source/application security model. Non-native full verifier emulation may negate efficiency.

## OPEN UNCERTAINTY
Latest official PDF SHA/version; full authors' optimized protocol/PCS/Fiat–Shamir implementation; deployed or secure-parameter effect; complete repair/soundness/privacy/cost proof; novelty relative to dual-PCS/CP-NIZK. **No authors contacted. User says DO NOT SEND EMAIL; no outreach/draft/public disclosure without explicit new permission.**

## NEXT_ACTION — ONE DECISIVE TEST (I83)
Read ePrint 2025/286 §2.2 and §5 / Appendix F source requirements. Identify whether published vFHE promises ZK/hiding of native evaluation and what data is public; compare with application-level ciphertext privacy. Decide whether hiding A/u is genuinely necessary for a faithful soundness repair or an optional stronger requirement. Do not assume that absence of formal ZK implies safe disclosure of plaintext-dependent witness data. Report precise source passages and threat-model boundary before any more PCS constructions.

## RELEVANT FILES
- Protocol/start: `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `START_RESEARCH_SESSION.md`.
- Last I82: `failures/vfhe-masked-brakedown-evaluation-unlinked-hidden-residue-iteration82.md`.
- I81: `failures/vfhe-native-field-pedersen-ipa-49bit-group-security-iteration81.md`.
- I80: `failures/vfhe-brakedown-dualpcs-cross-characteristic-interface-iteration80.md`.
- I79: `failures/vfhe-hidden-aggregate-carry-wrap-even-when-P-above-T-iteration79.md`.
- I78 and I77: `failures/vfhe-batched-crt-aggregate-without-shared-integer-opening.md`, `findings/vfhe-external-commitment-crt-full-opening-link-iteration77.md`.
- Gap: `findings/vfhe-crt-lookup-cross-component-soundness.md`, `findings/vfhe-theorem48-actually-sound-rectangular-relation.md`.
- CKKS impact: `findings/vfhe-ckks-public-output-binding-robust-rescale-counterexample.md`, `findings/vfhe-piac-adaptive-six-step-oracle-binding-audit.md`.
- Version: `findings/vfhe-theorem48-post-revision-mirror-provenance-diff.md`.
- UNSENT report/draft: `findings/vfhe-confidential-pi-review-package-iteration74.md`, `findings/vfhe-confidential-author-inquiry-draft-iteration75.md`.
- PARKED RIG: `logs/rig-state-2026-10-12-pre-vfhe-handoff.md`.

STATUS: **ACTIVE vFHE repair; I82 FAIL evaluation-only masked Brakedown link; I83 source privacy/security-goal audit NEXT**. No complete ZK repair, full SNARK forgery, or general impossibility result. No author contact/public disclosure authorized.
