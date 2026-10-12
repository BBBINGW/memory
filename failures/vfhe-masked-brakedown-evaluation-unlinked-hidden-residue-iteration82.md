# Iteration 82 — Masking Brakedown evaluation response does not prove hidden cross-CRT residue linkage

Date: 2026-10-12
Active target: Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint 2025/286 §4.3 / Theorem 4.8, §5 Brakedown PCS. Research direction unchanged.
**STATUS: FAIL** for adding a separately bound *native-field* additive mask to Brakedown evaluation response while treating a separately proven external canonical residue as implicitly linked. **OPEN** for more extensive protocols with an explicit ZK cross-characteristic link.
**NO CONTACT**: no authors contacted, no email/draft, no disclosure. Not a forgery of original or compiled vFHE.

## Source and read-before-write
- Read main `STATE.md` (last I81, I82 NEXT_ACTION), `AGENT.md`, I81 failure, plus I77–I78 archived warning about independent CRT/external commitments.
- [FACT] Read 52-physical-page ePrint 2025/286 mirror PDF by Research MCP: Appendix F.1–F.2 physical pp50–51, with corresponding §5 pp25–26 already verified. PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`; version `VERSION_UNVERIFIED` against current official binary. Native PCS is componentwise over F_(p_k^d).
- [FACT, Appendix F.2 p51] Original Brakedown testing publicly sends `v=r·U_f`, authenticates sampled encoded columns, and checks `Enc(v)|_Q=r·Uhat_f|_Q`. Evaluation publicly sends `v'=q1·U_f`, authenticates columns and checks `Enc(v')|_{Q'}=q1·Uhat_f|_{Q'}` and `y=<v',q2>`. The source does **not** claim its native PCS is zero-knowledge.
- This hypothetical masking architecture is OUR candidate; not claimed by the paper.

## ONE primary hypothesis; ONE decisive test
[HYPOTHESIS — FAIL] By attaching an independently committed native-field masking matrix U_z and revealing only w=q1(U_f+U_z) instead of v'=q1U_f, linear Brakedown checks can both authenticate the masked evaluation and connect its otherwise hidden aggregate y=<q1U_f,q2> to an *independent external* canonical integer commitment C_u without a new cross-domain proof (and therefore without non-native full PCS-verifier emulation).
[FALSIFIER] Two fixed, independently and correctly bound witness systems: native PCS commits U_f, native mask PCS commits U_z, external integer proof binds b,A,u satisfying every legitimate external range/mod-reduction equation. All proposed native masked checking equations and external equations accept, but native y differs from u. A failure proves masked linearity has not created the missing linking interface.
[TEST] Source-based equation derivation and one exact prime-field toy (which embeds into any extension field's prime subfield). No protocol implementation, full Brakedown soundness, or random sampling claimed.

## The exact modified equation, assuming Enc is linear
Let Uhat_f be row-wise encoded U_f and Uhat_z the separately authenticated encoding of U_z; define z=q1U_z and w=q1(U_f+U_z)=v'+z. Then the proposed native verifier can check
  `Enc(w)|_{Q'} = q1(Uhat_f + Uhat_z)|_{Q'}`
using authenticated opened columns of BOTH commitments.
This equation is mathematically true for honest matrices. It does NOT compare any witness to external commitment `C_u`. To certify the desired original value, one additionally needs
  `y = <w-z,q2>`
and `u = y mod p`, with a *sound hidden* proof that z refers to its committed matrix and that the external canonical u refers to the same native evaluation. Making z public defeats its privacy purpose, but hiding z without a dedicated subproof prevents the verifier from directly evaluating the unmasked identity. Merely adding authentication to w,z does not establish the external link.
Furthermore, the unchanged original testing phase publicly sends `v=rU_f`; masking ONLY evaluation response cannot yield a general zero-knowledge PCS. Any ZK claim would need to treat that phase and deterministic Merkle commitments as well, not just w.

## Explicit accepting false-bridge assignment
Field F101, external SNARK proof field F211. Set m=2, original field matrix
 `U_f=[[0,0],[0,0]]`, native mask matrix `U_z=[[4,7],[9,13]]`.
Let q1=q2=(1,0), native random test r=(3,5), and linear toy row code `Enc(x,y)=(x,y,x+y) mod101`.
- Native testing v=rU_f=(0,0), so `Enc(v)=r Uhat_f=(0,0,0)`.
- Original evaluation v'=q1U_f=(0,0), native real aggregate y=<v',q2>=0.
- Mask z=q1U_z=(4,7), w=v'+z=(4,7), `Enc(w)=(4,7,11)=q1(Uhat_f+Uhat_z)`. All native equations accept under ideally authenticated U_f,U_z.
- External canonical integer witness `b=(1,0)`, Boolean challenge `alpha=(1,0)`, exact aggregate `A=sum alpha_i b_i=1`, canonical u=1 mod101 and quotient c=0. P211 no-wrap suffices; all independent external integer equations hold.
- Crucially `y=0 != 1=u`. It is NOT a violation of the original source protocol (which never added the proposed external link); it falsifies the proposition that the mask *supplies* a cross-domain link. The discrepancy is exactly the pre-existing independent-commitment obstruction from I77–I78, now made explicit for the *modified Brakedown* equations, NOT a newly discovered general cryptographic attack.
- The fixed toy code only checks linear arithmetic identity. It does not model Merkle root security, PCS extraction, knowledge soundness, protocol challenge distributions, hiding, or security parameters. Assuming PERFECT separate commitment binding strengthens the counterexample to the logical interface claim, but does not prove any actual cryptographic forgery probability.

## Reproducibility
- Executed Python stdlib script `/mnt/data/iteration82_vfhe_masked_brakedown_link_test.py`; SHA256 `44df9e6abc5d6b3c706f13c58ffaa86980553491ace143aeca81a44a8ed3677b`.
- Exact JSON `/mnt/data/iteration82_vfhe_masked_brakedown_link_results.json`; SHA256 `158f01a6b0d1ccba5b20187fd5c394e8e53057e075a05342a2c13ef92530c467`.
- Assertions all PASS: native test true, native masked evaluation true, external integer proof true, cross-domain hidden equality false.
- Note that the script's SHA-256 digests are independent illustrative binding identifiers, NOT implemented Merkle authentication or a hiding commitment.

## Consequence and next action
[NEGATIVE] Masking the original Brakedown evaluation alone solves neither the explicit hidden residue equality nor (because the testing transcript remains visible) general ZK. Linear code compatibility is not cross-characteristic witness compatibility.
[OPEN] A significantly modified hiding PCS and explicit cross-domain ZK/AoK might still work. This round supplies no cost reduction, new extractor, secure-parameter proof, or novelty claim. Do not automatically build full SNARK, return to I64–68 encoding variants, or contact authors.
[PRIOR-ART/DIRECTION CONTROL] This is a scoped corollary of I77–80 interface obstruction; archive rather than presenting as standalone research contribution.
One higher-information NEXT_ACTION before continuing construction: **read vFHE §2.2 security/privacy definitions and Section 5 commitment assumptions to decide whether original verifiable CKKS relation actually demands zero knowledge/hiding of per-component evaluation values, or whether our imposed ZK requirement is stricter than the source target.** Falsifier: source explicitly requires witness hiding/ZK, or native plaintext-dependent leakage is demonstrably incompatible with privacy. This is a source/threat-model check, NOT a new encoder proposal.

## End of Iteration 82
STATUS: FAIL — evaluation-only masking is NOT a sound/ZK cross-characteristic residue bridge.
RESULT: In F101/F211 toy, two separately bound native matrices pass masked Brakedown linear checks and external integer proof; native aggregate is 0 while external canonical residue is 1. Original unmasked testing phase also openly transmits v=rU_f; ZK does not follow from hiding v' alone.
NEXT_ACTION: Inspect ePrint 2025/286 §2.2 and Section 5's original security/privacy goals and determine whether hiding the native aggregate is a REQUIRED property of the published vFHE setting before designing another ZK repair.
STATE_UPDATE: YES — closes I82 masking candidate and narrows next step to a source-backed requirement audit.
