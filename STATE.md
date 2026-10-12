# Research State — 2026-10-12

ACTIVE: **vFHE, CRT lookup soundness audit → efficient cross-CRT repair**.
PARKED: **RIG-HE**; complete prior `STATE.md` preserved verbatim at `logs/rig-state-2026-10-12-pre-vfhe-handoff.md` (NOT archived; do not discard its findings).
ARCHIVED SPECIFIC BRANCH: GL generic BigSwitch; see `failures/gl-generic-bigswitch-structure.md`. All other older research files retain their own statuses.

## CURRENT TARGET
Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint **2025/286**, especially §4.3 / Theorem 4.8 / Appendix E.2 (CRT digit lookup), §4.1–4.2 (CKKS rescale and ΠAC), and **§5 componentwise Brakedown polynomial commitments**.
Research MCP mirror: 52pp PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, mirrored 2026-04-28 after 2026-02-16 official revision; **latest official binary VERSION_UNVERIFIED**.

LAST COMPLETED ITERATION: **85 (2026-10-12)**. Corrected CRT projector; fixed c',c'' imply bounded remainder uniqueness under equal-bit active-prime hypotheses; see I85 finding.

## CURRENT QUESTION
Does a succinct verifier in source §4.2 / Appendix D.3 actually have enough publicly accessible data to reconstruct the canonical/relaxed rescale remainder h and an exact public integer aggregate A, even though the remainder is **unique conditional on BOTH c' and c'' being fixed**? If not, what is the smallest missing input or verification cost?

## PRIMARY HYPOTHESIS — NEXT, NOT YET TESTED (I86)
Although the rescale remainder is uniquely determined by a fixed complete intermediate ciphertext pair (c',c'') in the paper's same-bit setting, a succinct verifier need not possess full c': §4.2 carries intermediate states as prover oracle witnesses and Appendix D.3 only authenticates sampled evaluations. Hence directly reconstructing h/A may require the work the verifiable outsourcing was intended to avoid. Test one concrete interface and its inputs/cost, not a new proof design.

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

- [SOURCE-CORRECTION / DERIVED CONDITIONAL PASS, I85] §3.2 projector z_l includes the currently dropped p_l component; Eq(6) multiplier is [p_l^(-1)]_Q*z_l, **NOT** the projection z_(l-1) that would zero p_l. An initial supposed fixed-output ambiguity r=0 versus r=73 for N8,d2,p0=73,p1=89,B128 was wrong: with actual t=32, r=73 yields output4161 mod6497, not fixed output0. Formal conditional uniqueness lemma: for distinct equal-u-bit active CRT primes, range-legal remainders in [0,2^u) producing same fixed (c',c'') are coefficientwise unique; if ≥2 primes retained, retained modulus product already exceeds range; for last pair, inverse multiplier is nonzero at dropped prime by same-bit odd-prime argument. Thus I84's **input-only** nonuniqueness remains, but conjectured **fixed-(c',c'')** nonuniqueness FAILS. Source text extraction of Eq(6) still merits visual confirmation. See `findings/vfhe-fixed-input-output-rescale-remainder-uniqueness-iteration85.md`.

## MAIN OBSTRUCTION
[OPEN] No verified efficient cross-characteristic, knowledge-sound interface binding a certified **exact integer aggregate A** to original field PCS evaluations. Mandatory proof-ZK is not in source. For fixed full c' AND c'', equal-bit residue r is conditionally unique (I85), but full intermediate ciphertext c' is often a prover oracle witness rather than public verifier data; uniqueness does NOT imply affordable/verifier-visible reconstruction. I84's relaxed choice may still vary when only c' fixed and c'' allowed to change. Public-A client privacy with VO remains unproved.

## OPEN UNCERTAINTY
Latest official PDF SHA/version; full authors' optimized protocol/PCS/Fiat–Shamir implementation; deployed or secure-parameter effect; complete repair/soundness/privacy/cost proof; novelty relative to dual-PCS/CP-NIZK. **No authors contacted. User says DO NOT SEND EMAIL; no outreach/draft/public disclosure without explicit new permission.**

## NEXT_ACTION — ONE DECISIVE TEST (I86)
Read source §4.1–4.2 pp13–17 and Appendix D.3 pp43–44 to identify the *exact full data* visible to a succinct verifier at ONE rescaling gate (public x,y vs committed intermediate c',w_quot) and whether reconstructing r=[c']_p or an exact masked A requires processing Θ(N) coefficients / entire prover witness. Distinguish lack of explicit full c' from proof-of-unavoidability; one counterexample of identical verifier-visible data for distinct internal states or one sharply stated missing interface suffices. Do not invent new PCS/encoding variants or contact authors.

## RELEVANT FILES
- Protocol/start: `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `START_RESEARCH_SESSION.md`.
- Last I85: `findings/vfhe-fixed-input-output-rescale-remainder-uniqueness-iteration85.md`.
- I84: `findings/vfhe-rescale-remainder-public-computability-nonuniqueness-iteration84.md`.
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

STATUS: **ACTIVE vFHE repair; I85 FAIL projected-kernel counterexample, PASS conditional fixed-output remainder uniqueness; I86 verifier-visible interface audit NEXT**. Exact cross-CRT bridge and public-A privacy remain OPEN. No full SNARK forgery, no novel impossibility claim. No author contact/public disclosure authorized.
