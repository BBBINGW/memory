# Iteration 77 — External shared Boolean commitment versus CRT-reduced digest: minimum soundness bridge

Date: 2026-10-12
Parent: Cascudo, Costache, Cozzo, Fiore, Guimarães, Soria-Vazquez, *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint 2025/286, §4.3 / Eq(21)-(23), revised Theorem 4.8 and Appendix E.2 physical p48.
STATUS: **PASS** (concrete deterministic CRT attack against a naive 'single commitment' repair; conditional binding-soundness reduction for true external shared bit commitment). **UNCLEAR / NOT YET A REPAIR** (hiding, efficiency, bulk linkage to polynomial commitments, end-to-end zero knowledge and proof costs).
NO CONTACT: User explicitly said not to send emails. No author email, messages, draft-in-mailbox or public disclosure.
STATE_UPDATE: NO — unrelated parked RIG-HE STATE.md unchanged.

## Read before write
Read AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md read-only; I76 finding `findings/vfhe-piac-adaptive-six-step-oracle-binding-audit.md`, I70 relaxed-range finding; original revised-looking Research MCP ePrint 2025/286 physical pp20-22, 47-48. PDF mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, source version is VERSION_UNVERIFIED against latest official PDF bytes. §4.3 Eq22-23 requires h digit globally in t_beta, but Appendix E.2 wrongly infers global-outside-table implies a field-outside-table, allowing CRT-rectangular membership.
Supplementary prior art checked by public web:
 - Schneider et al. (2023), *Zero-knowledge proofs for set membership: efficient, succinct, modular*, Designs, Codes and Cryptography, https://doi.org/10.1007/s10623-023-01245-1 §2.4–2.5 presents type-based commitments and commit-and-prove NIZKs for multiple domain types. This generic architecture is NOT new; exact applicability/cost to vFHE not evaluated.
 - Lycklama et al., *Artemis: Efficient Commit-and-Prove SNARKs for zkML*, arXiv 2409.12055, illustrates modern efficient commitment linking but does not establish efficient cross-characteristic vFHE digit repair.
 - Yang et al., *Rarus: A Succinct and Efficient Range Proof for Polynomial-based Vector Commitment*, USENIX Security 2026, https://www.usenix.org/conference/usenixsecurity26/presentation/yang-xinyang, asymptotically efficient vector commitment range checks; no established direct cross-CRT same-integer proof from this paper.
No novelty or efficiency claim from listing related primitives.

## One primary hypothesis and cheapest falsifier
[HYPOTHESIS] A globally shared external Boolean commitment C, linked individually to two CRT field-digit witnesses through knowledge-sound proofs of **the same full opening**, ensures the global digit is diagonal, whereas a 'shared commitment' checked only after CRT-field reduction can be independently patched even with collision-resistant H.
[FALSIFIER] Find two distinct bit openings (0,r0),(1,r1) of ONE binding external commitment C or verify that independently reduced-hash equations cannot be CRT-glued; either result would refute one direction.
[CHEAPEST TEST] One deterministic SHA256 preimage pair and one two-prime CRT calculation; no parameter sweeps; prove the binding implication symbolically. SHA256 toy transparent opening used only to demonstrate equality checks, NOT to prove cryptographic binding or ZK.

## Naive scheme is structurally UNSOUND
Let distinct primes p=149 and p'=157, q=23393 and R≈F149×F157; take global illegal mixed-bit element `e=CRT(0,1)=14602`, so e mod149=0 and e mod157=1, but e≠0,1 in Z_q.
Suppose prover supposedly uses 'one commitment' `C∈Z_q` or one ring element and field verifier k checks merely `C mod p_k = H(b_k,r_k) mod p_k`, where H is interpreted as a 256-bit integer.
Prover computes arbitrary digest values H0=SHA256(domain||0||nonce0) and H1=SHA256(domain||1||nonce1), then sets
 `C=CRT(H0 mod149,H1 mod157)=19980`.
BOTH projected digest checks pass for bit0 and bit1 simultaneously. H0≠H1 (verified); no collision has been found or required. This is exactly the old CRT patching attack transferred from digit membership to a superficially shared ring 'commitment'.
Similarly, a 256-bit publicly formatted C but whose branch verifiers check ONLY residues `C modp_k` is insufficient; a canonical byte string is necessary but not sufficient if verification merely compares its residues.

## Exact external full commitment + linked branch proofs: CONDITIONAL soundness
Let `Com_ext(m;r)` be a computationally message-binding commitment to integer bit b, with ONE shared canonical external commitment object C (parsed outside product ring). For each k, require a knowledge-sound ZK/commit-and-prove proof of relation
 `R_k(C, Ch_k) : exists b_k in {0,1}, r_k, h_k, open_k such that C=Com_ext(b_k;r_k) AND VerOpen_k(Ch_k,h_k,open_k)=1 AND h_k=b_k*1_(F_k)`,
where `Ch_k` is the committed field-specific polynomial digit or an honestly bound evaluation thereof. Equality to the external *full C* must be proved, not just reduction modulo p_k; branch bits b_k must be range-constrained as integers so p_k>1 keeps 0/1 distinct. For beta>2, range 0≤b_k<beta and beta<pmin ensures faithful representation in each field.
If all branch proofs verify, knowledge extractors yield valid openings (b_k,r_k) of the SAME C and correctly bound field values h_k=b_k. Suppose non-diagonal digit (some b_i≠b_j); then extracted openings of C to distinct messages break Com_ext's computational binding. Thus, with `mu` branch proof knowledge errors eps_i, field PC opening-binding error eps_pc, and external commitment binding error eps_bind:
 `Pr[accept non-diagonal] ≤ sum_i eps_i + eps_pc + eps_bind`
(up to extractor simulation and composition details). This is a **conditional generic construction at ONE digit**, NOT a full protocol. It needs hiding commitment and zero knowledge to hide digit. The toy code publishes b,r for checking transparency and DOES NOT preserve privacy.
Simple positive control: same b=1 and same full SHA256 digest H1 accepted by both field links; mixed b0=0,b1=1 fails exact second full-digest check when C=H0.

## Exact test artifacts
- `/mnt/data/iteration77_vfhe_shared_commitment_crt_link_test.py` SHA256 `c323ddc0830c4747b233a4547619801a21632ee535f55311037b5fee13882e74`.
- `/mnt/data/iteration77_vfhe_shared_commitment_crt_link_results.json` SHA256 `66f3b58000876c640df2456355f8cc2f269034e0dcefd6d385ba4d21ffd97bd6`.
Reran in current container PASS; p149,p157, q23393, e14602, 'ring commitment' C19980, both residues pass, H0!=H1, exact external C=H0 accepts first proof but not second, both agree b1 positive control passes. Code is an arithmetic falsification of the naive scheme, not an experimental 256-bit collision-security proof.

## Cost/novelty boundary and next cheapest question
For m digit positions and mu field factors, direct generic solution needs m external commitments plus at least m*mu link relations/proofs if instantiated per-digit/per-factor; proof aggregation could improve proof size, but prover would still have significant constraints unless a new shared-witness arithmetic technique or native compatibility is found. DO NOT present m*mu as a universal lower bound on all possible batching.
The paper's §5 factor-wise PCs do not, by themselves, supply this external binding object; nor can one identify an arbitrary ring-valued commitment with the byte-string full opening. Need an explicit bridge to bound original h oracle at Boolean points, then securely maintain its joint opening for every field.
Existing CP-NIZK with type-based commitments shows basic ability to bind heterogeneous witness domains is prior art; the possible contribution would require dramatically more efficient bulk cross-characteristic consistency inside vFHE than this naive per-digit construction, and full proof.

End of iteration:
STATUS: PASS for falsifying reduced-hash 'shared commitment' and for conditional full-external-opening soundness; UNCLEAR practical repair.
RESULT: A single Rq-valued or only component-residue-checked commitment remains CRT-separable (mixed 0/1 passes with C=19980). For a truly external canonical C whose opening is proven exactly in every branch, mixed 0/1 implies breaking computational binding, provided branch knowledge/extraction and field opening binding. No privacy/efficiency result yet.
NEXT_ACTION: Study ONE batch-cross-field link for m shared bits with a single external hiding vector commitment and field-PC commitments: write a concrete relation/API that binds each of the mu field-oracle evaluations to that SAME bit-vector commitment; falsify the tempting shortcut 'equality of random linear combinations in different characteristics' via an explicit characteristic mismatch before assigning implementation cost. Compare to type-based CP-NIZK prior art; do not start encoder variants. No author contact.
STATE_UPDATE: NO — RIG-HE STATE.md untouched.
