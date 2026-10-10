# Iteration 69 — Verified post-revision mirror timeline and proof-delta for vFHE Theorem 4.8

Date: 2026-10-10
Research target: Ignacio Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, IACR ePrint 2025/286 (CRYPTO 2025).
STATUS: **PASS** for independent Git commit-timeline and exact-blob evidence that the 52pp version under audit was in the mirror **after** the officially announced 2026-02-16 theorem-proof revision; **PASS** for a precise old/new theorem proof-delta; **UNCLEAR** for strict byte-wise identity of the 52pp mirror with the official currently served PDF (official newest bytes unobtainable with these tools).
ATTACK STATUS unchanged: algebraic counterexample from I59–61 targets the actual 52pp mirror with revised Remark4.9. Independent deployed-Fiat–Shamir-SNARK exploit not built. This is a stronger provenance audit, NOT a new cryptanalytic attack.
NO author contact, no public disclosure, no edits to separate parked RIG-HE STATE.md.

## Research protocol
Read connected GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, parked `STATE.md`, I68 `findings/vfhe-random-sign-wht-affine-ramsey-distance-obstruction.md` and I62 `findings/vfhe-crt-official-version-provenance-and-private-review.md` read-only. One primary source-authentication hypothesis, falsifiable by authoritative official PDF digest inconsistency or absence of expected revised proof changes. No further WHT or toy variants.

## Exact official and mirror provenance
[OFFICIAL] IACR ePrint landing `https://eprint.iacr.org/2025/286` (web current retrieval) states 'Note: Fixed a flaw in the proof of Theorem 4.8. Minor editorial improvements.' 'History: 2026-02-16 revised; 2025-02-19 received'; links paper pdf and all versions. This is authoritative metadata, not PDF byte digest.
[OLD CACHED PDF] The web-crawled `https://eprint.iacr.org/2025/286.pdf` currently returns a 50-physical-page **old crawler snapshot**, published/crawled around 1.4 years prior, not necessarily the 2026 revision; its PDF text shows on physical p21/22 Lemma4.6 directly over R_q with q>2^ell*, and Theorem4.8 WITHOUT explicit β<pmin and 2^ell*<pmin restrictions. Appendix E.2 directly invokes ring Lemma4.6. Browser's PDF screenshot attempt failed 'Cache miss', so no claim to visual verification by the web screenshot renderer; its text extraction unambiguously shows old theorem wording.
[NEWER 52PP MIRROR] Research MCP `get_eprint_paper("2025/286")` retrieved `source_kind=github-mirror`, 836746 bytes, 52 physical pages, source `https://github.com/arturo-kong/IACR-eprint-mirror/blob/master/2025/286.pdf`, exact Git blob SHA `a549654c5dffa3484e95e8244056f4a27c48c3e6`, PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, status VERSION_UNVERIFIED. Its §4.3 physical pp.22–24 changes Lemma4.6 to field-only, adds Theorem4.8 inequalities and Remark4.9 explaining prior repair, and its Appendix E.2 physical p48 contains the disputed CRT-projection implication.
[INDEPENDENT GITHUB TIMELINE NEW IN I69] Connected GitHub mirror's commit `2e6d22477cceacaa8e831cb8b13544c0a6a141b88b28e1be` NOT USED — avoid this unrelated SHA; the actual PREEXISTING mirror commit fetched was `2e6d22477cceacaa8e831cb8b13544c0a5ea499b` from 2024-01-15, and fetching `2025/286.pdf` there correctly returns 404.
  The mirror commit `03d21d9516bb8a5ae39c9882194c252fbd7c2a25`, message 'Update latest ePrint PDFs (2025 part 1)', GitHub `created_at=2026-04-28T17:20:00Z`, contains file `2025/286.pdf` when fetched by exact repository path + pinned commit ref, with Git blob SHA **exactly** `a549654c5dffa3484e95e8244056f4a27c48c3e6`. This SAME blob is present in next mirror commit `d523ed2373065723d8aed5b8f5c84f161c78332a` 'Update latest ePrint PDFs (2025 part 2)' and current MCP source. This anchors file existence after official 2026-02-16 revision and matches identical content SHA at original 2026-04-28 mirror snapshot.
  GitHub fetch_commit's changed-files API truncates large commits to first 300 entries, so a file's omission from that truncated list must NOT be interpreted as absent. The exact `fetch_file` at each pinned commit is the decisive presence/blob test.
[IMPORTANT LIMIT] Mirror timestamp > official revision date + revised Remark4.9 + same pinned PDF blob => STRONG EVIDENCE the audited paper is a post-revision artifact. It does not cryptographically authenticate the mirror bytes against **the current official** downloadable PDF, nor rule out later silent author corrections. Official 2026-02-16 page history reports only one revision at retrieval, but without current official PDF bytes no `OFFICIAL_VERSION_VERIFIED` claim is justified. Direct container HTTP download failed due unavailable DNS; official site PDF version-history link also returned internal error; PDF screenshot web cache miss.

## Exact old vs revised proof comparison
[OLD CRAWL] 50pp pdf physical p20–21:
 - Lemma4.6 `Rq`-valued h and bound `q>2^ell*`.
 - Theorem4.8 `S subset Rq exceptional` and error O((2^ell* + b/c)/|S|); no explicit p_min conditions.
 - Appendix E.2 directly applies ring Lemma4.6.
[REVISED MIRROR] 52pp physical p22–24:
 - Lemma4.6 applies over a **field F of characteristic p** with p>2^ell*.
 - Theorem4.8 adds `β=2^(b/c) < p_min` and `2^ell* < p_min`.
 - Remark4.9 explicitly states previous ring Lemma4.6 invocation was incorrect and declares the field-only restatement sufficient for Theorem4.8.
 - Appendix E.2 p48 tries to bridge from the global ring lookup relation to one invalid field projection, asserting `h notin diagonal scalar t_beta => exists k: Phi^(k)(h) notin t_beta`.
[MATHEMATICAL OBSTRUCTION] The last displayed implication is not valid for nontrivial product rings. From CRT, a non-diagonal element `e=(0,1)` lies outside the global scalar table but every projection is individually a legitimate table digit; I59 exact ring N2,d2 uses `e=56 mod77`, I61 N8,d4 uses `e=667 mod1073`, both satisfy the revised numeric restrictions and produce accepting ideal polynomial-oracle transcripts. Thus the revised field-only Lemma is not the same as proving original global diagonal relation. This is NOT alleging that the original authors' prior fix was ill-motivated; it repaired a *different* algebraic issue while a global-to-component claim remains unjustified in the audited mirror.

## Independent reproduction integrity
I69 reran fixed I60 script `/mnt/data/iteration60_vfhe_full_range_piop_audit.py` and I61 script `/mnt/data/iteration61_vfhe_d4_crt_soundness_audit.py`, both PASS against model algebra. SHA256 checked locally against pre-existing archives:
 - I60 `2bfa13a134a1b3938adf544bdc5955316e78cf6afdd6938dba2aecbb6ede856f`.
 - I61 `ba58b94194f3aa8b3c89e9260e92a6aece892dbc29d940d2c0da9f2756bb3c97`.
 - previously UNSENT private review ZIP `/mnt/data/iteration62_vfhe_private_review_bundle.zip` unchanged SHA256 `700c287e3735d4df0f03082473fa43b0adaeb30ae821c765eb75f290f5debc26`.
These are exact algebraic PIOP tests; not the real installed SNARK, no security-parameter attack demonstration.

## Research decision and next narrow test
STRATEGIC: Stop coding/encoder variants I63–68. The research's main scientific asset is the reproducible revised-looking Theorem4.8 soundness discrepancy, which is now documented in a mirror verifiably uploaded after the Feb16 revision.
STATUS: PASS for post-revision mirror provenance and old/new proof comparison; UNCLEAR strict official latest byte identity; HUMAN_REVIEW for any author disclosure. No author communication authorized or performed.
RESULT: We now have explicit commit-bound evidence the same PDF was mirrored 2026-04-28, after official fix, and an exact statement of the proof delta (ring lemma -> field lemma + p_min assumptions) which does NOT cure diagonal-vs-rectangular CRT digit coherence in the audited 52pp text.
NEXT_ACTION: The next independently executable technical check is to formulate and audit the strongest actually supported amended lookup relation `T_rect = Phi^(-1)(prod_k Phi^(k)(T_beta))` and prove the fieldwise reduction gives soundness for that RELAXED relation under revised numeric hypotheses. Identify whether its allowed messages are incompatible with paper's original coefficient-range relation. This separates 'what is actually sound' from 'what is claimed' without another toy counterexample. Obtain current official PDF bytes or PI-authorized confidential author confirmation before any external publication/disclosure.
STATE_UPDATE: NO. Parked RIG-HE `STATE.md` unchanged.
