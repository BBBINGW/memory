# Iteration 74 — Confidential two-page PI review package for vFHE CRT lookup soundness discrepancy

Date: 2026-10-11
STATUS: **PASS** — independent fixed-witness arithmetic recheck, source-pinned two-page private review report, PDF visual audit and reproducibility bundle integrity verification; **HUMAN_REVIEW** — author contact is a strategic/authorization decision, not presumed by "continue". No new attack, proof system repair or SNARK compilation claimed.
STATE_UPDATE: NO — unrelated parked RIG-HE STATE.md unchanged. No author email, public issue or external transmission.

## Read-before-write and precise iteration hypothesis
Read AGENT.md, RESEARCH_PHILOSOPHY.md, parked STATE.md, I59 `findings/vfhe-crt-lookup-cross-component-soundness.md`, I69 `findings/vfhe-theorem48-post-revision-mirror-provenance-diff.md`, I70 rectangular relation, I72 bounded-output CKKS finding, and I73 `findings/vfhe-piac-gkr-eq16-20-source-wiring-transcript-audit.md`. Read primary IACR ePrint 2025/286, revised-looking 52pp Research MCP PDF §§4.1–4.3 and Appendices E.1–E.2. Official IACR landing newly rechecked in this iteration; note dated 2026-02-16: "Fixed a flaw in the proof of Theorem 4.8". Pinned mirror PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, Git blob `a549654c5dffa3484e95e8244056f4a27c48c3e6`, post-revision mirror date 2026-04-28; latest official PDF bytes still **VERSION_UNVERIFIED**.
[HYPOTHESIS] The previously obtained mathematical evidence can be condensed into an accurate <=2-page source-anchored internal review note that contains a false CKKS computation witness, explicit range inconsistency and direct questions, without claiming a complete instantiated SNARK exploit.
[FALSIFIERS] Basic Eq13 and Eq16 do not both match the same fixed witness; archived I72/I73 reproducibility checks do not rerun; report exceeds two pages or omits limitations; or bundle hashes fail.
[TEST] Re-execute two known scripts, compute hashes, independently check Eq13 and Eq16, render PDF to images and inspect both pages, verify page count, verify every embedded bundle member against SHA256SUMS, then archive minimal information.

## Independent arithmetic and source review
With q=149*157*173=4,046,989, p=173, q_survive=23393, inverse p^-1 mod23393=17849, zero cprime, public y=173 and malicious auxiliary remainder r=4,017,060:
 `0-r-p*y = -4,046,989 = -q ≡ 0 (mod q)` — source Appendix E.1 Eq(16).
 `(-r*17849) modq = 173` — source Eq(13) inverse-side check at fixed cprime=0. Both independently recomputed, PASS.
 `y=173<23393=q_survive` and y mod173=0; both checks PASS; original true output=0 because inputs, d0,d1,d2 and legitimate key-switch witness are zero.
 `r>256` violates intended remainder range; 256>max(149,157,173) means T_256^rect=R_q; auxiliary Pi_range digit beta=16, ell*=7 -> 16<149,128<149 as required in revised Thm4.8.
Original §4.1 p15 footnote7 explicitly allows removing output range proof if public output is known to verifier. This example has truthfully bounded public y, so no bypass of an expected public range check is relied on.
Original §4.2 p17–19 Eq16–20 + Appendix E.1 pp44–46 specify quotient/remainder binding, GKR reductions and output/aux oracle routing. I73 checked those mathematical identities and local honest sumchecks; not a complete optimized protocol implementation.
Original §4.3 pp20–24 Eq21–23, Fig1, revised Thm4.8; Appendix E.2 p48 uses invalid diagonal-to-field-illegality CRT inference. The actually supported relation is rectangular CRT lookup; this supports a source-level computation relation discrepancy, subject to limitations.
Actual `python iteration72_vfhe_public_output_binding_rescale_audit.py` and `python iteration73_vfhe_pi_ac_gkr_wiring_audit.py` independently RERUN with exit=0. Their SHA256 hashes matched prior records:
- I72 script: `6c0dc008c95f7a39d0a288551d0a5e1dcd1255e7b7df2e4ec5ee2599b0bfd1e3`; JSON `441512f5bcb074cf39a087b14253860cb30d821bd75d5d6351ce5b13c2198e7e`.
- I73 script: `ade755d160cf10773c4e99f8fc6bd15bc6c2f38742e6578b5859460f2b8ceb6d`; JSON `c5589c3c9493605dae3a29314bd39c8d24630de8e439c48091d5565980c502bb`.
Known minor metadata bug: I72 JSON `degree_d:0` due reused Python variable; actual d=4, verified factorization and I73 correct metadata. This was documented in I73; code/artifacts left unaltered rather than silently changed.

## Internal-only deliverables verified in active container
1. `/mnt/data/iteration74_vfhe_confidential_pi_review.pdf`: **exactly TWO A4 pages**, 49,560 bytes, SHA256 `06c4ca4d8db38d0d91161fa61d572c95264f6bcf5da475e705225af2d464812b`. Both pages rendered to PNG and visually inspected; no clipping or overlap. Text extraction verified both pages contain selectable text, and 'CONFIDENTIAL / PI REVIEW ONLY / NOT SENT'.
2. `/mnt/data/iteration74_vfhe_confidential_pi_review.md`: 4,522 bytes, SHA256 `2b4ed971bc75d2f6a7bc5f4a957b7c350baf6a9df4cb12adb69b5886e147adf0`. Editable source with full evidence and source locations.
3. `/mnt/data/iteration74_vfhe_confidential_pi_review_bundle.zip`: 61,244 bytes, SHA256 `2a6b572592c16439e4a9b899f19188b148e541e11a14676fa773d1a30b129bb6`. Contains PDF + MD + original two Python scripts + two JSON results + SHA256SUMS.txt. All six members verified against SHA256SUMS. No copyrighted paper PDF redistributed.
The note is a PI-decision package, NOT a sent author email. It asks three narrow questions: (Q1) Is this source-PDF SHA the current corrected revision? (Q2) Is there an unstated cross-CRT diagonal-index consistency check? (Q3) Is there an unstated full CKKS relation constraint that excludes the zero-input/public y173 witness?
[INFERENCE] These exact data support a candidate *ideal-oracle/source-algebraic computation-level soundness gap* in the inspected 52pp revision, not confirmation of an actual SNARK forgery, deployed verifier break, or independent proof of novel/publishable vulnerability.
[EXTERNAL FACT] Official landing: https://eprint.iacr.org/2025/286 (latest live metadata viewed 2026-10-11), revision note "Fixed a flaw in the proof of Theorem 4.8"; strict latest official PDF bitwise identity unverified.

## End of Iteration 74
STATUS: PASS (evidence package and integrity); HUMAN_REVIEW (authorization).
RESULT: Completed readable 2pp PDF, editable Markdown and verified bundle; independently checked Eq13, Eq16, re-executed I72/I73 scripts with unchanged SHA. Clearly separated source facts, inference and unresolved latest official version / exact SNARK implementation boundaries.
NEXT_ACTION: Ask PI explicitly whether to authorize PRIVATE, narrowly scoped technical inquiry to authors (not public disclosure). If authorized, draft a concise inquiry for PI approval and only then use an available authorized outbound channel, if any; otherwise retain package privately and independently reconstruct the exact original optimized Pi_AC public-coin message schedule for this same fixed witness.
STATE_UPDATE: NO — parked RIG-HE STATE.md unchanged.
