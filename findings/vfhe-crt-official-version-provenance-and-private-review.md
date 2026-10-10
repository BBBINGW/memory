# Iteration 62 — Latest official version provenance remains unverified; confidential author-review package prepared

Date: 2026-10-10
Target: Cascudo, Costache, Cozzo, Fiore, Guimarães and Soria-Vazquez, *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, ePrint 2025/286, CRYPTO 2025.
Primary STATUS: UNCLEAR — could not authenticate the authoritative official **latest revised PDF** byte-for-byte against the 52-page fixed mirror used in I59–I61. No weakening of the independently verified mathematical soundness counterexample in that inspected mirror.
Supporting checks: PASS — reran original exact I60 Pi_range and I61 d4 scripts with hashes matched; prepared an UNSENT minimal confidential technical review report and reproducibility ZIP. Not a new technical attack or a confirmed fix. No human authorization to contact authors was presumed; no email/issue/public posting.

## Read-before-write / source provenance
[FACT] First reread AGENT.md, RESEARCH_PHILOSOPHY.md, separate parked RIG-HE STATE.md, I59/I60/I61 source-grounded finding records. No file other than this new archive was edited; parked STATE.md remains unchanged.
[FACT / OFFICIAL LANDING] https://eprint.iacr.org/2025/286 lists 2026-02-16 revision and says Theorem 4.8 proof flaw fixed, page note. Official landing HTML was opened fresh via web search in this iteration.
[FACT / AVAILABLE OLD WEB PDF] The web-search PDF renderer for https://eprint.iacr.org/2025/286.pdf still yields a **50-physical-page PDF** with crawl age >1 year, evidently not the 2026-02-16 52-page corrected-looking mirror. PDF screenshot attempt failed cache-miss; do not cite or assert visual inspection of web PDF.
[ATTEMPTS FAILED] Official landing version-history link returned internal error. Cache-busted official PDF links and alternative version URLs were inaccessible via web. Container requests could not resolve external DNS; container.download official link failed; no official PDF bytes saved. The Research MCP's get_eprint_paper of 2025/286 continues to return 52 pages, source_kind github-mirror, **VERSION_UNVERIFIED**, rather than claiming official source.
[PINNED MIRROR] https://github.com/arturo-kong/IACR-eprint-mirror/blob/master/2025/286.pdf at Git blob revision a549654c5dffa3484e95e8244056f4a27c48c3e6, 836746 bytes, 52 physical pages, PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`. §4.3 pp.20–24 contains revised Theorem4.8 and Remark4.9; Appendix E.2 p.48 still has false implication `h notin diagonal T_beta => exists field projection k with Phi_k(h) notin scalar table`. It is a **revised-looking version** but not yet byte-authenticated as official latest.
[SUPPLEMENTARY] CRYPTO 2025 Springer venue chapter exists with DOI 10.1007/978-3-032-01907-3_21, but it predates the February 2026 ePrint revision and therefore cannot resolve latest version issue.

## One primary hypothesis / cheapest decisive test
[PRIMARY HYPOTHESIS — NOT VERIFIED] The **current official 2026-02-16 revised PDF** is byte-identical to the fixed 52-page mirror containing the invalid CRT cross-component proof implication, and so the mathematical counterexample is certified against that latest official version.
[FALSIFIER/DECISION] Fresh official PDF SHA differs materially or its Theorem 4.8 / Appendix E.2 includes an explicit scalar-cross-component consistency check. If exact official PDF is unavailable, report UNCLEAR rather than replacing with stale cached PDF. Only source authentication is the primary iteration test.
[RESULT — UNCLEAR] Neither a fresh official byte sequence nor an authenticated author-provided latest PDF was acquired. The 52-page mirrored source and proof issue remain unaltered and publicly source-locatable, but the stronger claim about official byte identity is unsupported.

## Reproducibility integrity checks
[EXACT / PASS] Current-container SHA256 checks confirmed unmodified originals:
 - I59 `iteration59_vfhe_crt_lookup_soundness_audit.py`: `8b7f3a03d5fb6e23b896af494d03fe95081171ffe10355fce6408935cebe4826`.
 - I60 `iteration60_vfhe_full_range_piop_audit.py`: `2bfa13a134a1b3938adf544bdc5955316e78cf6afdd6938dba2aecbb6ede856f`.
 - I61 `iteration61_vfhe_d4_crt_soundness_audit.py`: `ba58b94194f3aa8b3c89e9260e92a6aece892dbc29d940d2c0da9f2756bb3c97`.
[EXECUTION] Reran I60: Pi_decomp exact oracle sumcheck all 49x49 ring points PASS; Pi_beta_range grand product/gates and virtual sumcheck PASS; public v=[56,56] not in intended coefficient-range table. Reran I61: legal N=8,d=4 ring, false public v=[667,667], product 18 factors/65 monomials symbolically identical, field factors irreducible and large exceptional set 707281 PASS. Only minor unrelated sympy deprecation warning.
[NO NEW ATTACK] The previous mathematical result remains an **ideal-oracle Ring-Rq Pi_range PIOP** false-statement acceptance construction in the inspected 52pp mirror. Full shipped compiler/Fiat–Shamir SNARK exploit was NOT implemented and version remains unresolved.

## UNSENT confidential author-review materials produced
1. `/mnt/data/iteration62_vfhe_private_author_review.md` (SHA256 `da49c1c8c405842700127d15cddb3379db0ed9f41be61fdd551f1c5337ab4abf`). Independently useful English confidential technical report: version pin, proof-position, two exact witnesses, CRT-glued memory counters, algebraic identity, checked PIOP/commitment scope, and three precise questions. Not an email or public post.
2. `/mnt/data/iteration62_vfhe_private_review_bundle.zip` (SHA256 `700c287e3735d4df0f03082473fa43b0adaeb30ae821c765eb75f290f5debc26`). Includes the review md, exact I59/I60/I61 Python code + result logs, and SHA256SUMS.txt. ZIP created and verified via current container; no paper PDF redistribution.
[NO DISCLOSURE] Not sent to any author, not placed in public repository, not posted as issue. The GitHub Notes research archive is private research state as configured, but avoid reproducing author contact info unnecessarily.
[AUTHOR QUERY] Request authoritative PDF SHA/version; determine whether there exists an externally imposed diagonal scalar-index consistency restriction not described in §4.3–§5; and ask whether Theorem4.8 range PIOP requires correction. Author response could falsify the applicability or novelty claim; do not presume.

## Research conclusion and decision
[INDEPENDENTLY ESTABLISHED] For the fixed 52-page revised-looking mirror, Theorem4.8's diagonal membership implication fails and I59–I61 exact PIOP counterexamples still stand. Commitments alone cannot fix a semantically weak relation.
[NOT ESTABLISHED] Official newest byte identity, revised official fix status, absence of unpublished repair, deployed verifier exploit, technical novelty of the error, efficient concrete repair.
[RESEARCH PRIORITY] Stop adjacent CRT toy tests: two independent legal ring dimensions (N2,d2 and N8,d4) and full Pi_range relations already checked. Remain on this branch only to verify authoritative version/author response or to devise a **new** cross-component index proof if PI decides.
[ANTI-OVERCLAIM] 2026-02-16 official note proves *a* revision exists, not that the complete 52-page mirror equals it. Authors already mention a Theorem4.8 proof correction in their Remark4.9; do not claim this issue was never independently noticed without author confirmation.

## End of Iteration 62
STATUS: UNCLEAR (exact latest official PDF provenance); PASS (independent rerun of previously found PIOP counterexamples); HUMAN_REVIEW (author verification and disclosure decision).
RESULT: Official landing current as of 2026-10-10 documents February 16 proof fix but accessible official PDF cache is old; fresh official bytes could not be obtained. Reproduced prior algebraic evidence, produced confidential self-contained author-review report and reproducibility bundle, neither sent.
NEXT_ACTION: HUMAN_REVIEW one decision: may the PI authorize a confidential, narrowly scoped version-and-proof inquiry to the corresponding author using the prepared packet? If not, obtain an independently authenticated official/current PDF with a reliable channel (author-provided or IACR version download) and reconcile Appendix E.2 before expanding any further research. Do not send without authorization.
STATE_UPDATE: NO — separate parked RIG-HE STATE.md preserved.
