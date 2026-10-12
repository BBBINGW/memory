# Research State — 2026-10-12

ACTIVE: **vFHE, CRT lookup soundness audit → efficient cross-CRT repair**.
PARKED: **RIG-HE**; complete prior `STATE.md` preserved verbatim at `logs/rig-state-2026-10-12-pre-vfhe-handoff.md` (NOT archived; do not discard its findings).
ARCHIVED SPECIFIC BRANCH: GL generic BigSwitch; see `failures/gl-generic-bigswitch-structure.md`. All other older research files retain their own statuses.

## CURRENT TARGET
Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint **2025/286**, especially §4.3 / Theorem 4.8 / Appendix E.2 (CRT digit lookup), §4.1–4.2 (CKKS rescale and ΠAC), and **§5 componentwise Brakedown polynomial commitments**.
Research MCP mirror: 52pp PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, mirrored 2026-04-28 after 2026-02-16 official revision; **latest official binary VERSION_UNVERIFIED**.

LAST COMPLETED ITERATION: **84 (2026-10-12)**. Honest rescale remainder server-computable, but relaxed witness not input-unique; see I84 finding.

## CURRENT QUESTION
With an original vFHE CKKS rescale layer's *public pre-rescale ciphertext c'* AND *fixed claimed output c''*, do the complete §4.1 Eq(12)–(15) ring arithmetic, ideal embeddings and coefficient bounds force one unique w_rmd? If not, a publicly exposed aggregate A may encode extra witness choice even with fixed ciphertext input/output.

## PRIMARY HYPOTHESIS — NEXT, NOT YET TESTED
Two distinct permitted rescale remainders may fit the same (c',c'') at the original embedded-ring level because of zero divisors/CRT projection. Before investing in new public-A protocols, try to prove uniqueness or find a single fully valid two-opening witness satisfying all source equations, not just scalar divisibility. Source equation PDF extraction may require visual confirmation.

## CURRENT EVIDENCE
- [FACT/SOURCE + DERIVED, I59–70] Audited revised-looking proof uses an invalid diagonal-digit ⇒ illegal CRT component inference. Fieldwise lookup supports rectangular `T_B^rect`, not the claimed global coefficient range; `B≥max p_i` makes `T_B^rect=R_q`. Explicit ring/PIOP counterexamples recorded.
- [DERIVED/PASS, I71–76] Small paper-format CKKS instance `q=149·157·173=4046989`: zero inputs must output 0, but claimed bounded public output `y=173` with illegal remainder `r=4017060` satisfies `-r-173y=-q`. Eq.(16)–(20), source-equivalent adaptive six-step ideal-oracle ΠAC checks and negative oracle-tamper controls PASS. **No compiled SNARK forgery / realistic secure-parameter attack established.**
- [NEGATIVE, I63–68, I77–78] CRT-local equations, simple encoder variants, reduced commitments and post-challenge CRT aggregate patching do not enforce the global integer witness. If exact externally bound integer aggregate is certified, random Boolean linear checks have ≤1/2 false-pass probability per round for a fixed wrong component, but publicly revealing the aggregate leaks information.
- [NEGATIVE / REFINED FIX, I79] `P>T=m(β−1)` alone is insufficient for an external hidden `A=u_k+p_kc_k (mod P)` carry proof: `T=1920, P=1931, A=144, u_173=172,c_173=11` yields `2075=144+1931`. Require `P>max_k(T, p_k·floor(T/p_k)+p_k−1)` or an explicit RHS≤T range proof. **This fixes only integer no-wrap, not PCS linking.**
- [NEGATIVE / SOURCE + DERIVED, I80] ePrint 2025/286 §5/Appendix F uses per-field Merkle/code Brakedown PC and exposes native evaluation vector/value; ePrint 2024/943 §5 DualPCS links TWO compatible schemes over ONE prime field (KZG-FFT-FOURIER or Dory/Linear-Rel), not arbitrary Brakedown↔external F_P commitments. No unital field hom F_(p_k^d)→F_P for different primes. Direct off-the-shelf hidden-residue bridge FAIL. Straight full-verifier wrapping would process O(μ(t+1)√n) extension-field symbols plus hashing/non-native checks; this is NOT a universal lower bound or benchmark. See `failures/vfhe-brakedown-dualpcs-cross-characteristic-interface-iteration80.md`.

- [NEGATIVE / DERIVED + EXACT TEST, I81] Standard prime-order Pedersen/IPA native-additive map `F_(p_k^d)→G` is trivial unless group order equals p_k; with paper's ~49-bit primes, p_k-order discrete logarithm costs O(√p_k)≈2^24.5, far below ~128-bit binding. Toy BSGS recovered a subgroup generator relation and produced two openings to one commitment. Excludes this conventional shortcut, not hash-based PCS or non-native ZK. See `failures/vfhe-native-field-pedersen-ipa-49bit-group-security-iteration81.md`.

- [NEGATIVE / SOURCE + EXACT TEST, I82] Appendix F.2 native Brakedown checks can authenticate hypothetical masked w=q1(U_f+U_z) when a separate mask matrix is bound, but those equations never link the hidden original <q1U_f,q2> to an independent external canonical C_u. Toy F101/F211 satisfies both independent checks while native y=0 and external u=1. Also the original testing phase exposes v=rU_f, so evaluation-only masking cannot yield general ZK. This merely reestablishes I77–78 independent-commitment obstruction for a concrete masked interface; not an original-protocol forgery. See `failures/vfhe-masked-brakedown-evaluation-unlinked-hidden-residue-iteration82.md`.

- [POSITIVE SOURCE SCOPE / CONDITIONAL PRIVACY, I83] ePrint 2025/286 §2.2 Definition 2.4, Appendix D.1–D.2 definitions specify soundness, knowledge soundness, PCS binding, succinctness but not proof zero-knowledge. Appendix C Definition C.4 specifies IND-CPA privacy of client plaintext against server *with verification oracle access*, not arbitrary witness/model secrecy. §2.2 p9/Appendix F.2 p51 explicitly transmit polynomial evaluations and v=rU_f, v'=q1U_f. Therefore universal hiding of A/u was a stricter assumption imposed in I77–82, not a formal original requirement. Public A might be admissible if efficiently simulatable from already visible ciphertexts, with VO behavior secured separately; witness provenance unverified. This does NOT repair CRT soundness or authorize leaking server-private model u. See `findings/vfhe-original-privacy-not-proof-zk-iteration83.md`.

- [PASS NARROW + NEGATIVE STRONG / SOURCE + TOY, I84] ePrint 2025/286 §3.3 Eq(4)–(6), §3.4 p12, §4.1 Eq(12)–(15) pp14–15: *honest canonical* CKKS rescale remainder `[c']_p` is computed by server from ciphertext arithmetic, evk and public moduli with no client sk. However optimized range oracle permits `w_rmd=[c']_p+k p`, `k∈{0,±1}`, if within bound `2^u`; input-only unique bit aggregation FAILS even in scalar arithmetic (p13, B16, c'=15, r=2 vs15, different output quotient and aggregate A=0 vs1 under α=(1,0,0,0)). This **does NOT** prove both witnesses accepted for a *fixed claimed output*, or for the complete original Rq relation. Client IND-CPA/verification-oracle privacy of a new public-A repair still UNPROVEN; original cross-CRT soundness bridge still missing. See `findings/vfhe-rescale-remainder-public-computability-nonuniqueness-iteration84.md`.

## MAIN OBSTRUCTION
[OPEN] No verified efficient cross-characteristic, knowledge-sound interface binding an **externally certified exact integer aggregate** A to original field PCS evaluations. Mandatory proof ZK was not an original property. A canonical honest rescale witness is server-computable without sk, but relaxed remainder witness/aggregate may vary even for same pre-rescale c', and privacy of exposing A to other parties remains conditional. Need determine uniqueness when c'' fixed before source-faithful public-A optimization. Direct DualPCS / masked-only Brakedown reuse fails.

## OPEN UNCERTAINTY
Latest official PDF SHA/version; full authors' optimized protocol/PCS/Fiat–Shamir implementation; deployed or secure-parameter effect; complete repair/soundness/privacy/cost proof; novelty relative to dual-PCS/CP-NIZK. **No authors contacted. User says DO NOT SEND EMAIL; no outreach/draft/public disclosure without explicit new permission.**

## NEXT_ACTION — ONE DECISIVE TEST (I85)
Precisely read vFHE ePrint 2025/286 Eq(6), Eq(12)–(15), §3.2 ideal embedding plus Appendix B if needed. Fix *both* c' and claimed c'' as the public ciphertext trace, include all ring/level constraints and bounds. Determine whether there can exist two distinct allowed w_rmd (hence distinct bit aggregate A) for the same fixed pair. Seek ONE full-ring exact witness or prove uniqueness; don't infer full-ring acceptance from I84's scalar quotient toy. Only after this decide if verifier can efficiently reconstruct A or whether prover-only information must be certified. Do not start PCS/encoder variants or author outreach.

## RELEVANT FILES
- Protocol/start: `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `START_RESEARCH_SESSION.md`.
- Last I84: `findings/vfhe-rescale-remainder-public-computability-nonuniqueness-iteration84.md`.
- I83: `findings/vfhe-original-privacy-not-proof-zk-iteration83.md`.
- I82: `failures/vfhe-masked-brakedown-evaluation-unlinked-hidden-residue-iteration82.md`.
- I81: `failures/vfhe-native-field-pedersen-ipa-49bit-group-security-iteration81.md`.
- I80: `failures/vfhe-brakedown-dualpcs-cross-characteristic-interface-iteration80.md`.
- I79: `failures/vfhe-hidden-aggregate-carry-wrap-even-when-P-above-T-iteration79.md`.
- I78 and I77: `failures/vfhe-batched-crt-aggregate-without-shared-integer-opening.md`, `findings/vfhe-external-commitment-crt-full-opening-link-iteration77.md`.
- Gap: `findings/vfhe-crt-lookup-cross-component-soundness.md`, `findings/vfhe-theorem48-actually-sound-rectangular-relation.md`.
- CKKS impact: `findings/vfhe-ckks-public-output-binding-robust-rescale-counterexample.md`, `findings/vfhe-piac-adaptive-six-step-oracle-binding-audit.md`.
- Version: `findings/vfhe-theorem48-post-revision-mirror-provenance-diff.md`.
- UNSENT report/draft: `findings/vfhe-confidential-pi-review-package-iteration74.md`, `findings/vfhe-confidential-author-inquiry-draft-iteration75.md`.
- PARKED RIG: `logs/rig-state-2026-10-12-pre-vfhe-handoff.md`.

STATUS: **ACTIVE vFHE repair; I84 PASS narrow canonical witness provenance, FAIL input-only uniqueness; I85 fixed-output ring-level uniqueness check NEXT**. Exact cross-CRT bridge and full public-A privacy remain OPEN. No complete ZK repair, full SNARK forgery, or general impossibility result. No author contact/public disclosure authorized.
