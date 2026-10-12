# Iteration 84 — Canonical rescale remainder is server-computable; relaxed witness digits are not input-unique

Date: 2026-10-12
Active target: Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint 2025/286, CRT digit-range soundness repair.
STATUS: **PASS (narrow honest-canonical provenance)** and **FAIL (strong input-only uniqueness of every relaxed allowed remainder)**; **UNCLEAR** on full public-A disclosure/privacy and uniqueness given fixed output and the complete embedded-ring relations.
No author outreach/email/draft/public disclosure. No new PCS construction or claim of an original vFHE forgery.

## Read-before-write / primary-source provenance
- Read connected GitHub Notes `AGENT.md`, `STATE.md` (last I83; I84 ONE NEXT ACTION), and `findings/vfhe-original-privacy-not-proof-zk-iteration83.md`.
- Read full primary 52-page PDF through Research MCP, ePrint 2025/286, mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, source `https://github.com/arturo-kong/IACR-eprint-mirror/blob/master/2025/286.pdf`, **VERSION_UNVERIFIED** vs latest official binary. Source-pinned main passages: §3.2–3.3 physical pp11–12, §3.4 p12; §4.1 pp13–15 and §4.2 pp16–17; Appendix C pp39–41 / Def. C.4, previously examined I83. **Extraction caution:** PDF has font and equation layout artifacts, especially parenthesized rescale formula Eq(6) and the embedding ideal; scalar toy below does NOT assert a complete implementation of Eq(6)/(13) in the paper's ring. Relevant plaintext prose around relaxed witnesses is readable.
- Official ePrint PDF direct browser fetching returned 403; primary full text remains Research MCP's cached mirror, not verified to match latest ePrint PDF.

## ONE primary hypothesis / decisive test
[HYPOTHESIS] A concrete CKKS rescaling rounding/range-check witness `w_rmd` and its digit aggregate `A` are constructible from public ciphertext computation inputs and public modulus/evaluation keys, with no client secret-key use; in particular, the verifier can treat arbitrary allowed A as a uniquely determined public input function.
[FALSIFIER] Find a prover-allowed relaxed remainder differing from the canonical modular reduction while satisfying the *scalar range and modular coherence checks* for an identical public pre-rescale coefficient, so the same input admits different digit aggregates; distinguish that from server-computability of an HONEST canonical choice.
[MINIMAL TEST] Trace the paper's one rescaling remainder, Eq(6),(12)–(15), its approximate relaxations §3.4 and §4.1, and run one deterministic scalar divisibility/range/digit test. Do not construct a full SNARK, CRT PCS bridge, or extra witness families.

## Primary source dataflow facts
[FACT §3.3 p12 Eq(4)–(6)] PreMult and KeySwitch compute `d0,d1,d2` from ciphertexts using public `evk`, then `c'_b = d_b + <CRT^{-1}(d2),evk_{j,b}>`; the `Rescale` step uses `[c'_b]_{p_l}` and a public ring-level inverse/embedding constant. Neither source algorithm calls `Dec(sk,...)` inside the server's rescaling operation. They list decryption as a separate algorithm.
[FACT §4.1 pp13–14 Eq(8),(12)–(15)] The proof arithmetization introduces nondeterministic witness `w_rmd,b`, `w_quot,b` for rescaling, uses an algebraic consistency relation and range constraints, including a `w_rmd` bound.
[FACT §3.4 p12; §4.1 p14–15] Authors explicitly allow a relaxed `w_rmd=[c']_{p_l}+k p_l`, `k∈{0,±1}`, under an optimized power-of-two bound `2^u` where `2^{u-1}<p_l<2^u`. This is approximate rescaling / proof-witness relaxation, not an arbitrary commitment equivocation. It can lead to a small output/noise shift. A proof must still enforce the paper's complete equations and output bounds.
[FACT §4.1 p15] Their batched `w_{2^u}` range oracle includes both base-decomposition values and `w_rmd`. The bit/digit vector for lookup is a proof witness built from that ring element; a *proposed* public Boolean-mask aggregate `A=Σα_i h_i` is OUR repair concept, not a published author's equation.
[FACT §4.2 p16] Prover nondeterministic inputs include intermediate ciphertexts and claimed output ciphertexts, and the public HE input ciphertexts are in the circuit. Some intermediate ciphertexts are prover-witness oracles and may not be directly public in their entirety.
[FACT Appendix C pp39–41] VC privacy Definition C.4 is client-input IND-CPA *against server*, permitting acceptance-bit verification oracle; a server's own witness/auxiliary data are not a priori hidden from that server. This is not proof ZK or a formal confidentiality claim for the server's private model against the client.

## Exact scalar minimization (NOT full Ring-Rq acceptance)
Take p=13 and optimized bound B=16, satisfying 8<p<16, and one pre-rescale integer coefficient c'=15. The canonical remainder r0=c' mod p=2; a relaxed remainder r1=r0+p=15 also satisfies 0≤r1<B and r0≡r1 mod13.
Scalar quotient identities:
  `15 = 13*1 + 2 = 13*0 + 15`.
Thus the underlying scalar divisibility/checking data allow *two different* (remainder, quotient) pairs for the SAME public input c'. They imply **different output quotient values**, so this does **NOT** exhibit two accepting witnesses for a FIXED public output ciphertext or a complete Rq protocol; the need to test that remains open.
Use β=2, length4 digit vectors (LSB first):
  r0=2→h0=(0,1,0,0);
  r1=15→h1=(1,1,1,1).
For public Boolean mask α=(1,0,0,0):
  A0=Σα_i h0_i=0, A1=Σα_i h1_i=1.
Hence the *strong* claim that any admissible relaxed A is uniquely determined by **pre-rescale c' alone** fails at the scalar range/divisibility level. This is a scope clarification, not a new weakness in the original PIOP or SNARK.
Reproducible executed stdlib Python:
 - `/mnt/data/iteration84_vfhe_rescale_remainder_provenance.py` SHA256 `b5a458c11da39dfe254d0486c008e5094911dd6637be2927c6970a9d48befae7`.
 - `/mnt/data/iteration84_vfhe_rescale_remainder_provenance.json` SHA256 `b612a39615965aa0f22bc0eb4d71db565eca76e1d5f5d218ea5517a5d54a90a0`.
All exact arithmetic assertions PASS. No cryptographic security, Merkle binding, RS soundness or valid full paper ring parameters simulated.

## Scope-corrected privacy/soundness conclusion
[PASS CONDITIONAL] The *canonical honest* rescale remainder is a PPT function of data in the **server's evaluation view** (ciphertext components / intermediate server-computed values, evaluation keys, moduli). This does not require `sk` or decrypting plaintext. The server can also compute its own h and A with α public. If a modified protocol merely transmits that prover-generated A back to the verifier, the adversarial server itself gains no information it did not already have from A it generated.
[FAIL STRONGER ASSERTION] `A` need not be an unambiguous function of **the initial public ciphertext alone** under the relaxed witness relation; intermediate ciphertexts and the choice of relaxed witness/claimed output matter. If an honest verifier or third party does not already know those values, A may be NEW information to them. The scalar example does not prove nonuniqueness after fixing all outputs and full paper constraints.
[OPEN PRIVACY] A security reduction for Appendix C's **verification-oracle IND-CPA** with a NEW public-A proof requires considering whether verification/acceptance interacts with `sk`, and whether the added messages are efficiently generated from the adversarial server's existing view. Server-private model privacy toward client is beyond the cited client-input IND-CPA notion. Full proof missing.
[OPEN SOUNDNESS] As in I77–82, public A alone can be CRT-patched or invented; it must be **soundly certified as Σα_i h_i over exact integers for witness fixed BEFORE α**, and linked to original native ring PC openings. Removing mandatory ZK does NOT remove that structural obstacle.

## End of Iteration 84
STATUS: **PASS** for honest-canonical server-side public-data computability; **FAIL** for unconditional input-only uniqueness of relaxed remainder/digit aggregate; **UNCLEAR** safety and soundness of any complete public-A repair.
RESULT: Original source computes canonical [c']_p entirely with server-known public HE arithmetic, while permitting k=±1 relaxed remainder under 2^u bound. In scalar test p13, c'=15 allows r2 or r15 with different quotient and bit-aggregate A; does not establish both pass under fixed claimed output. No proof of client IND-CPA/VO preservation under a new verifier.
NEXT_ACTION: One decisive full-paper algebraic check: with BOTH input c' and claimed rescaled output c'' fixed, and with all §4.1 eq(12)–(15) bounds and ideal embeddings, is w_rmd unique within the allowed range, or can two different h/A fit the same fixed public ciphertext transcript? If a strict ring-level counterexample exists, public A truly carries new witness dependence even after fixing output. If uniqueness holds, inspect efficient reconstructibility from that fixed trace. Check source formulas carefully; PDF extraction caveat. No fresh PCS proposals until answered.
STATE_UPDATE: YES — source-faithful repair constraint is client IND-CPA with VO, not mandatory proof ZK; public canonical A is server-computable but arbitrary accepted relaxed A is not input-only deterministic.
