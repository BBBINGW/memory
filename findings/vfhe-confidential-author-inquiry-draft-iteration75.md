# Iteration 75 — Confidential author inquiry prepared, NOT SENT

Date: 2026-10-11
STATUS: PASS (faithful, narrowly scoped, source-checked author inquiry draft); HUMAN_REVIEW (fresh explicit approval required for any actual outbound author contact).
STATE_UPDATE: NO — unrelated parked RIG-HE STATE.md unchanged.
SENT: NO. Gmail DRAFT: NO. PUBLIC DISCLOSURE: NO. ATTACHMENTS TRANSMITTED: NO.

## Read-before-write / provenance
Read AGENT.md, RESEARCH_PHILOSOPHY.md, separate parked STATE.md, I74 findings/vfhe-confidential-pi-review-package-iteration74.md, and I73 PiAC source audit. Read primary ePrint 2025/286 pp1–3 via Research MCP to establish named authors and organizational contact formats. Independently opened official IACR page https://eprint.iacr.org/2025/286 showing 2026-02-16 revision of Theorem 4.8 and contact authors. Inspected local I74 markdown review and exact math.

[HYPOTHESIS] A first private author inquiry can efficiently check current official version, omitted cross-CRT scalar consistency condition, and omitted rescale relation constraint without prematurely claiming a complete SNARK exploit.
[FALSIFIER] If its arithmetic does not reproduce Eq16 and Eq13, if it conflates the exact 52pp mirror with the current official PDF, if it claims end-to-end SNARK forgery, or if it sends/discloses before fresh authorization.
[MINIMAL TEST] Checked q=149*157*173=4046989, p173 inverse modulo 149*157 is 17849, public fake y173 and r4017060; 0-r-p*y=-q, and (-r*17849) modq=173; y173<23393, beta16<149 and 128<149. All PASS. Source-level GKR tests and local sumcheck status retained from I73, never described as serialized original PiAC.

## Exact deliverable
Container file: /mnt/data/iteration75_vfhe_confidential_author_inquiry.md
SHA256: f8be0eb535e829298a050ae5c65ffc50211ced4e1f4db001b15234979772ee6d
Length: 3268 bytes; draft includes subject, greeting, CRT diagonal-vs-rectangular inconsistency, full bounded-output CKKS witness, source constraints, three questions, caveats, placeholder human signature and NOT SENT banner.

### Proposed private inquiry — unsent

Subject: Confidential technical question on Theorem 4.8 and CKKS range checks (ePrint 2025/286)

Dear authors,

I am studying your CRYPTO 2025 paper, *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, and would appreciate your help checking a possible oversight in the revised proof of Theorem 4.8. I am using a 52-page mirror copy of ePrint 2025/286 (PDF SHA-256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19). I have seen the revision notice dated 16 February 2026, but have not independently authenticated these PDF bytes against the currently served official version.

In Appendix E.2 (physical p. 48), the argument appears to infer that if a ring-valued digit is outside the global scalar table t_beta={0,...,beta-1}, then at least one of its CRT-field projections is outside the corresponding projected table. In a product ring, however, a CRT idempotent with coordinates (0,1) is outside the diagonal table {0,1} although both projections are individually valid. This seems to leave the fieldwise protocol enforcing the rectangular closure of the scalar table, rather than the stated diagonal membership relation.

We also checked a small, algebraically admissible CKKS-rescaling example: N=8, d=4, RNS primes (149,157,173), q=4046989, with zero input ciphertexts and zero key-switch decomposition. Taking a remainder witness r=4017060 and claimed public output y=173 satisfies the Appendix E.1 Eq. (16) check, since 0-r-173*y=-q=0 (mod q). The public output is within the prescribed coefficient bound (173<23393), but the true rescaling output for zero input is zero. For the auxiliary bound B=256, c=2, beta=16, and ell*=7, the revised Theorem 4.8 inequalities hold (16<149 and 128<149); the componentwise lookup admits the noncanonical remainder.

I have checked the displayed arithmetic/wiring equations (16)–(20) and local sum-check identities, but **have not constructed a complete optimized PIOP transcript, Fiat–Shamir SNARK proof, or attack against an implementation**. Could you kindly clarify:

1. Whether the SHA-pinned 52-page PDF is the current corrected version;
2. Whether an additional cross-CRT shared-digit/index consistency check is imposed elsewhere in the intended protocol; and
3. Whether the complete CKKS verification relation includes an additional condition excluding the above zero-input, bounded-public-output witness?

I have a two-page technical note and exact reproducibility scripts and would be glad to provide them privately if helpful. I have not made any public disclosure.

Best regards,
[Your name]
[Affiliation, if desired]

### Source-boundary and file handling notes
I74 original PDF SHA256 in verified ZIP: 06c4ca4d8db38d0d91161fa61d572c95264f6bcf5da475e705225af2d464812b (49560 bytes). At I75 verification, a loose file now residing at /mnt/data/iteration74_vfhe_confidential_pi_review.pdf had **different current bytes** SHA256 8c09454c71b24c69d4bf35f258c478f0dce7ad2365dff65148512199af002be4 (74529 bytes). The I74 bundle ZIP still preserves the exact originally archived 49560-byte PDF and its SHA256SUMS. Do not attach or rely on the loose PDF as byte-identical to archived evidence. The inquiry attaches nothing. This discrepancy affects attachment provenance, not the separately verified arithmetic.
No email was sent or even drafted in a live mail service. No public issue, no mailing-list post, no report to authors.
Do not assume current official paper bytes match the mirror. The author contact identities and email formatting appear on the official landing and mirrored paper cover, but a recipient should be explicitly chosen/approved by PI for any future send.

## End of iteration 75
STATUS: PASS (draft) + HUMAN_REVIEW (outbound authorization).
RESULT: Prepared a concise, carefully qualified confidential technical inquiry containing the exact algebraic witness, source location, and three decisive questions, while preserving the no-send boundary and identifying the loose-PDF/archived-bundle checksum discrepancy.
NEXT_ACTION: PI reviews the unsent text and decides whether to authorize a private author email. If not approved, continue only with exact source-protocol step-serialization of Appendix E.1 for the fixed I72 witness, without additional toy parameter variants.
STATE_UPDATE: NO — unrelated RIG-HE STATE.md untouched.
