# Missing critical sources

This is persistent research memory, not a bibliography. Add only technically
important missing primary sources whose required content could not be retrieved. See `papers/README.md`.

Copy the following entry when needed (this template is not an actual request):

```text
## <exact paper title>
Status: MISSING / SUPPLIED / RESOLVED / NO_LONGER_NEEDED
Authors:
Venue / Year:
Identifier: DOI / ePrint / arXiv / URL
Needed For: active question or hypothesis
Missing Evidence: exact theorem / proof / appendix / experiment / section
Why Public Retrieval Failed: sources/versions checked and missing parts
Impact: can independent work continue? what is blocked?
Human Action: exact full text or supplement to obtain
Repository Path: papers/supplied/<actual-file>.pdf (fill after receipt)
Readability Verification: date, version/SHA, MCP read_repo_pdf page range, required evidence legibility
```

Use MISSING until the supplied source is verified readable, then SUPPLIED.
Use RESOLVED after the dependent question is resolved, or NO_LONGER_NEEDED with a
brief reason. Keep useful history; a filename alone is not readability verification.

Use `read_repo_pdf` on Repository Path to check the needed pages before marking
SUPPLIED. No-text or garbled extraction is not successful evidence recovery.

## Aikata–Roy rectangular D&C implementation artifact — MatMul-0568
Status: **MISSING** (supplementary **source code**, not a missing paper PDF)
Authors: Aikata Aikata; Sujoy Sinha Roy
Venue / Year: INDOCRYPT 2024, ePrint 2024/1730
Identifier: https://anonymous.4open.science/r/MatMul-0568 (paper §5 physical p19)
Needed For: I135 source-interface falsifier after I134 rectangular output-block capacity lower bound
Missing Evidence: actual rectangular divide-and-conquer source code, output ciphertext representation, number of Ct×Ct operations/ciphertexts when l t > k p²; one case (l,d,t)=(8,2,8)
Why Public Retrieval Failed: paper full text was obtained/read; the exact supplemental URL returned inaccessible through web tool on 2026-10-13. Related public FHERMA winning-code archive and an independent AR24 implementation were inspected but only support **square** implementations, so they do not replace the paper's own rectangular artifact.
Impact: cannot verify whether authors' algorithm already accounts for output-block factor; no proven error. Narrow I134–135 paper-claim audit PARKED pending source.
Human Action: obtain a snapshot/zip of the exact MatMul-0568 repo (or author-identified updated equivalent implementing §4.2), ideally a README, exact rectangular function and tests. Do **not** contact authors without PI authorization.
Repository Path: **N/A — supplementary code**, not `papers/supplied/*.pdf`; store original code as separately approved repo/text evidence if later supplied
Readability Verification: **PENDING**; never treat found filename or unrelated repo as original-implementation verification.

## MRFHE v5.0.2 mixed-radix Lattigo source and FHE(8,5) experiment harness
Status: **MISSING_CRITICAL_IMPLEMENTATION** (not missing original paper PDF)
Authors: Jung Hee Cheon, Seungwan Hong, Minsik Kang, Jonghyun Kim, Taeseong Kim, Changmin Lee, Junho Lee
Venue / Year: IACR ePrint 2026/853, 2026
Identifier: https://eprint.iacr.org/2026/853; cites vanilla dependency Lattigo v5.0.2 https://github.com/tuneinsight/lattigo
Needed For: **I141 source-equivalent full noisy FHE(8,5) K1 vs K2 auxiliary PCMM** (I139 nominal dense-KS amortization; I140 slot-domain KS1 cross-batch error sensitivity)
Missing Evidence: **original authors' mixed-radix fork/patch** implementing nonpower-of-two N62208 RNS ring, S^(i) and S^(omega), ring conversion and two genuine PCMM key switchings; executable K1/K2 tests and full FHE(8,5) Q/P primes, scale/rescale, error/secret distributions, security and stagewise coefficient/canonical-slot error records.
Why Public Retrieval Failed: paper's 18pp Library PDF searched for source/GitHub/implementation; only cites upstream Lattigo v5.0.2 reference [26], not a discoverable custom code release. GitHub repository and code searches using exact MRFHE/title/FHE(8,5), publicly listed repo inventory of coauthor Seungwan Hong, and public web search did not surface verified authors' MRFHE adaptation (as of 2026-10-13). Crucially vanilla upstream tag v5.0.2 `ring/ring.go` SHA `b9e2c58a2ee7fdfd2f68591758a91e4da4eb1668` checks `(N&(N-1))!=0` and REJECTS N62208 (bitmask 61952), so stock Lattigo cannot substitute. This **does not prove authors' custom code does not exist**.
Impact: Unable to perform **real full two nonzero KS + D′₂ PPMM + actual componentwise rescale K1/K2** noise/precision or benchmark for source FHE(8,5). Paper's stated N/logPQ/dnum do not suffice to faithfully reproduce their custom framework. Do not infer speedup, noise safety/failure, or security impact from I139/I140 toy tests.
Human Action: obtain **author-identified MRFHE Go source or a tarball/patch against exact Lattigo v5.0.2, reproducible FHE(8,5) K1 baseline and K2 test invocation, complete RNS and scale parameters**, security estimate and seed/benchmark protocol. **No author outreach unless PI explicitly approves.**
Repository Path: **N/A — needed full original code and experiment manifest**, not `papers/supplied/*.pdf`. Promote verified source references once received; no invented paths.
Readability Verification: **PENDING**, original mixed-radix source never fetched or executed. Supporting *upstream vanilla* code/source inspection verified 2026-10-13 in I141 finding `findings/mrfhe-v502-nonpowertwo-original-implementation-source-gate-iteration141.md`.


## Cascudo et al. ePrint 2025/286 — current official February 2026 PDF
Status: **MISSING_CURRENT_OFFICIAL_BINARY** (the 52-page full text is available from a GitHub mirror, but current official revision identity is **VERSION_UNVERIFIED**)
Authors: Ignacio Cascudo; Anamaria Costache; Daniele Cozzo; Dario Fiore; Antonio Guimarães; Eduardo Soria-Vazquez
Venue / Year: CRYPTO 2025; IACR ePrint 2025/286; official landing shows **2026-02-16 revision**
Identifier: https://eprint.iacr.org/2025/286 and https://eprint.iacr.org/2025/286.pdf
Needed For: I155 official-revision identity gate on I59–60 CRT scalar-diagonal membership soundness audit
Missing Evidence: the **exact CURRENT OFFICIAL 2026-revised PDF bytes**, Appendix E.2 Theorem 4.8 proof step and any matching current §4.3/§5 verification relation; byte-level SHA matching to available 52-page GitHub mirror
Why Public Retrieval Failed: 2026-10-13 official landing reports 2026-02-16 revised theorem proof, but web PDF index yields an OLD **50-page** snapshot, while Research MCP GitHub mirror is **52 pages**, 836746 bytes, SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, source_kind github-mirror, VERSION_UNVERIFIED. The official “See all versions” endpoint gave HTTP 403, direct official PDF download failed; local network official DNS unavailable. No official SHA was obtained. An older searchable PDF must NOT be treated as the current binary.
Impact: I59–60 exact ideal PIOP counterexample applies to the inspected mirror text but **has not been verified against current official PDF** or a compiled end-to-end proof system. Parent P1 retained OPEN/HUMAN_REVIEW / SOURCE-GATED; code-replacement repair I152–154 PARKED.
Human Action: obtain today's official ePrint `2025/286.pdf` using a normal browser, retain original bytes (not a 50-page search-index copy), and supply as a PDF file with its download date; after receipt SHA256-pin and read verified pages 23–24 and Appendix E.2, plus §5 if changed; do not contact authors without PI authorization.
Repository Path: **PENDING** — propose `papers/supplied/eprint-2025-286-official-2026-revision.pdf` only after receiving actual raw file; no path is asserted to exist.
Readability Verification: **PENDING** for actual official PDF; available MCP mirror physical pp23–24 and 47–49 legible for the critical logical implication despite extraction warnings, but not official version-verified.
Evidence: `findings/vfhe-current-official-revision-identity-gate-iteration155.md`.


**2026-10-15 V42 retrieval follow-up (still MISSING):** Live official landing https://eprint.iacr.org/2025/286 explicitly says proof of Theorem 4.8 fixed and revision 2026-02-16. Fresh `web` access to official PDF returned only a STALE 50-page cached snapshot (not raw current PDF bytes); `See all versions` https://eprint.iacr.org/archive/versions/2025/286 returned HTTP 403; cache-busting PDF URL was not accessible. Independent direct container `requests.get` to official PDF, cache-busted variants and versions path each failed due DNS NameResolutionError. Authors' PICOCRYPT publication page https://software.imdea.org/picocrypt/results/ links back to SAME IACR source, not an independently version-pinned PDF. Springer official 2025-08 publisher chapter https://link.springer.com/chapter/10.1007/978-3-032-01907-3_21 exposes preview only (subscription required), and predates 2026-02 revision, so it cannot certify CURRENT latest revision. Official current raw bytes/SHA remain UNOBTAINED. The 52-page mirror build date aligns with 2026-02-16 as established in V41, but exact official/mirror byte parity remains UNKNOWN; no newly verified mathematical attack or currently published erratum. **Decision:** maintain SOURCE_VERSION_GATED/HUMAN_REVIEW; do not initiate speculative next crypto-proof iteration solely from mirror until exact official bytes or explicit PI-chosen source-complete pivot. Evidence sources: live official HTML and original authors' institutional publication links; external web 50pp PDF rendered/screenshot failed. No change to supplied path/verification status.

## Min–Lee–Song ePrint 2025/429 — Table 4 (r=5, degrees 53/25) original polynomial coefficients and Lattigo artifact

Status: **MISSING_AUTHOR_ARTIFACT** (the complete 19-page paper text is available; missing the specific published implementation/coefficient generation, not the paper PDF)
Authors: Seonhong Min; Joon-Woo Lee; Yongsoo Song
Venue / Year: ACM ASIACCS 2025, ePrint 2025/429
Identifier: https://eprint.iacr.org/2025/429 ; DOI https://doi.org/10.1145/3708821.3710824
Needed For: I163 source-realism gate following I160–I162 discovery of a derivative-weighted degree43 *ideal-outer* approximation improvement. Need equal degrees (53,25), exact author's p2 and p1 code/coefficients to quantify real source-grade p2∘p1 effect and its precision/level cost.
Missing Evidence: coefficient vectors for polynomial p1 degree53, p2 degree25; the exact multi-interval Remez fitting routine and scaling/interval conventions; original author Lattigo fork/commit and Table4 Set I r5 benchmark scripts, parameter files and seeds. Also current official PDF binary parity with the GitHub mirror is VERSION_UNVERIFIED, although the PDF text of critical sections is legible.
Why Public Retrieval Failed: Full Research MCP 19-page mirror PDF SHA256 `150b337c0b11bc284b1f5d129c7ef1455451de0fe7cbbfd19ba8cb21e7e8dd4d` has all §3 and §5 text, Table4 Set I r5=(53,25), precision27.12bits, time24.9s but no polynomial coefficient arrays or paper-specific repo/commit. `search_eprint_text` finds no GitHub/source-code/supplement link. Inspected official landing (last ePrint revision 2025-09-11), first author's homepage and SNU Crypto & Privacy Lab publications (no explicit paper-specific code), public web and GitHub title/author/repository/code searches, including minshinfo and SNUCP repository names. No verified author-matched artifact found. The search is NOT an exhaustive proof that private/unindexed code does not exist; one user-name scoping query returned API 422.
Impact: **No original-code reproduction or actual Table4 CKKS precision/latency claim can be made.** I162 2.14188× improvement is a source-domain, degree43, exact ideal f2 toy; the authors' real r5 uses p1-degree53 and approximate p2-degree25 and substantial ciphertext noise. Conceptual/math exploration can continue independently ONLY if explicitly separated from author-code replication.
Human Action: Supply author's exact Table4 Set I r5 fitting script and polynomial coefficients (plus reproducible environment/ref), **or** explicitly authorize a clean-room independent reimplementation from the public paper/Lattigo code with all deviations documented. No author contact without PI approval.
Repository Path: **PENDING/NONE** (missing original code/artifact, not a PDF to fabricate under papers/supplied/). Once provided, record actual verified repo or uploaded archive path, hash, library commit and reproduction command; do not predeclare a file path.
Readability Verification: **PENDING for source and coefficient artifact**. Original 19-page PDF is already legible via Research MCP pp6–10, 15–17; author's code and exact coefficient vectors NOT accessed/verified.
Evidence: `findings/ckks-generalized-composite-source-artifact-gate-iteration163.md`.

## Zhang–Wang–Cheng AKU DFR author-edition source (I192)

Status: **MISSING** (final rendered proof/experiment artifact, NOT the publicly readable ePrint text)
Authors: Qi Zhang, Mingqiang Wang, Xiaopeng Cheng
Venue / Year: CANS 2025, LNCS 16351, pp292–312, Springer online publication 2025-11-13
Identifier: IACR ePrint 2025/381; https://doi.org/10.1007/978-981-95-4434-9_14
Needed For: I190–I192 Gaussian-parameter model/Table3 DFR self-consistency audit and independent original experiment reproduction
Missing Evidence: **(a)** official rendered CANS §5.1 formulas, Table2/Table3 and version comparison to ePrint, **or (b)** exact author AKU OpenFHE fork/commit, Gaussian LWE key parameter initializer, end ModSwitch code and complete DFR estimator/noise worksheet for Algorithm6 (n447, σ3.19, q1024, Qks2^14, reported DFR2^-36).
Why Public Retrieval Failed: Springer publisher page https://link.springer.com/chapter/10.1007/978-981-95-4434-9_14 exposes abstract/metadata but requires institution login for full text; ePrint original 27pp parses with formulas but mandatory visual PDF screenshot on physical p19 fails cache miss and author-edition PDF parity remains VERSION_UNVERIFIED. EPrint MCP GitHub mirror SHA256 bbc507b8323f4a65dea806bb663c9eea8ef2954e41259cad3b9db11256a03faf, 707942 bytes, 27pp, is AVAILABLE text but not a publisher-version/code substitute. Targeted web and connected GitHub title/author/AKU/128_OURS repo/code searches found no verified author AKU source; not a proof private code is nonexistent. OpenFHE HEAD is not known to be the paper's tested commit.
Impact: I190–I191 extracted-model result remains: its final ModSwitch term alone implies modeled DFR around 2^-18.19 versus printed Table3 2^-36; **actual** author DFR, publisher-equation identity, 128-bit security and reported runtime advantage NOT independently adjudicated. Label SOURCE_VERSION_GATED and PARK specific correctness-error allegation, not a confirmed paper flaw.
Human Action: If authorized, obtain relevant Springer chapter pp292–312 via institution and/or authenticated author AKU experiment repository or archive and exact DFR estimator; user/PI decides any contact. No unverified file path assumed.
Repository Path: **PENDING/NONE** (ePrint paper text available from MCP cache; missing source is publisher chapter or exact author experiment artifacts).
Readability Verification: **PENDING** for publisher §5.1 and author code. ePrint original PDF was parsed/read by Research MCP and web text, not visually verified rendered p19. Once supplied, read exact required source, verify SHA/commit and record method.
Evidence: `findings/fhew-aku-gaussian-dfr-consistency-iteration190.md`; `findings/fhew-aku-ms2-rounding-code-gate-iteration191.md`; `findings/fhew-aku-author-repro-source-gate-iteration192.md`.


## Crockett–Gentry–Kim–Lee–Lee GL matrix-arithmetic bootstrapping full text (new pivot source gate, 2026-10-14)

Status: **MISSING** (primary full PDF; abstract/DOI metadata accessible)
Authors: Eric Crockett; Craig Gentry; Hyojun Kim; Yeongmin Lee; Yongwoo Lee
Venue / Year: CRYPTO 2026 Part II pp492–524; ePrint 2026/956
Identifier: https://eprint.iacr.org/2026/956 ; DOI https://doi.org/10.1007/978-3-032-35374-0_16
Needed For: Proposed independent post-CGS matrix-FHE source audit, specifically non-power-of-two generalized trace commuting with decryption and ciphertext-plaintext CtS/StC key-switch accounting; choose exactly ONE theorem/lemma after full text is available. NOT an initiated claim that a theorem is wrong.
Missing Evidence: full original constructions, trace definition, theorem hypotheses, proof of decryption commutation, algorithm and cost/evaluation key details; abstract and bibliography do not establish these.
Why Public Retrieval Failed: Research MCP get_eprint_paper("2026/956") returned RETRIEVAL_BLOCKED: original PDF HTTP403; arXiv exact-title fallback no matching result; fixed arturo-kong GitHub mirror lacks 2026/956.pdf. Web Springer chapter fetch cache-miss, alternate ePrint mirror direct PDF inaccessible. Secondary Scribd textual repost is NOT verified equivalent to original PDF or a sufficient primary source.
Impact: technical correctness/noise/security/cost audit MUST NOT begin with the abstract. Can still research other fully accessible targets without claiming this one verified.
Human Action: If available with authorization, supply the full ePrint PDF or CRYPTO 2026 chapter PDF and, if claiming measured performance, original implementation; no author contact/disclosure without PI permission.
Repository Path: **PENDING/NONE** — only after an actual authorized upload.
Readability Verification: **PENDING**; when received, verify file identity/version/PDF hash, read original relevant pages and visually check equations where extraction is unclear.
Evidence: post-CGS17 source acquisition gate, 2026-10-14.

## Bernard–Carouge–Joye–Orfila–Tap low-noise multi-value TFHE bootstrapping (new pivot source gate, 2026-10-14)

Status: **MISSING** (primary full PDF; publication abstract accessible)
Authors: Olivier Bernard; Nolan Carouge; Marc Joye; Jean-Baptiste Orfila; Samuel Tap
Venue / Year: IACR ePrint 2026/2310, posted 2026-10-02
Identifier: https://eprint.iacr.org/2026/2310
Needed For: Possible independent source-specific audit of log-unit lattice search and LUT shifting as they affect encrypted-domain truth-table equivalence/noise. Select ONE technical claim if primary text is recovered.
Missing Evidence: construction and definitions of unit lattice, shift equivalence, noise analysis, theorem scope, reported benchmarks and parameterization.
Why Public Retrieval Failed: Research MCP get_eprint_paper("2026/2310") returned RETRIEVAL_BLOCKED: IACR PDF HTTP403, no exact-title author-matched arXiv fallback, fixed arturo-kong GitHub mirror does not contain 2026/2310.pdf. Alternative eprint mirror direct PDF inaccessible in web tool. A published abstract and author homepage are metadata only.
Impact: cannot assert a correctness flaw, improvement idea, or perform paper-formula calculations without original source.
Human Action: Supply authorized exact PDF or source code/reference artifact; no author contact unless PI approves.
Repository Path: **PENDING/NONE**.
Readability Verification: **PENDING**; recover version/hash and inspect relevant original theorem/equations on receipt.
Evidence: post-CGS17 source acquisition gate, 2026-10-14.


## Li–Xiang–Yang Levis plain-model MKFHE Cofactor Compatibility full text (2026-10-14)

Status: **MISSING** (authenticated full PDF/source; public abstract available)
Authors: Baoyu Li; Binwu Xiang; Kang Yang
Venue / Year: IACR ePrint 2026/2263, publicly listed 2026-09-29; preprint, final peer-reviewed status not verified.
Identifier: https://eprint.iacr.org/2026/2263 ; public abstract mirrored at https://eprint.iacr.asia/2026?offset=100
Needed For: independently compare Levis-fast/Levis-small against Min–Park–Song CRYPTO 2026 / ePrint 2026/322, especially Cofactor Compatibility, extension-free evaluation, initial ciphertext communication, lifting/key costs and underlying security/noise assumptions.
Missing Evidence: formal Cofactor Compatibility definition and proof; Levis-fast and Levis-small KeyGen/Enc/Eval/Dec algorithms; relative ciphertext/evaluation-key dimensions; reduction and security assumptions; noise/error growth and benchmark matched parameter tables; optional pinned source/code.
Why Public Retrieval Failed: Research MCP get_eprint_paper("2026/2263") returned RETRIEVAL_BLOCKED (official ePrint PDF HTTP403, fixed Github mirror no PDF, no exact-title author-matched arXiv paper). Web PDF URLs under eprint.iacr.org and eprint.iacr.asia inaccessible; author publication site and targeted search display abstract/download label but did not provide accessible reliable full text. Search of public repositories for title/Levis/Cofactor Compatibility did not find an independently verifiable release. Do not infer private artifacts do not exist.
Impact: published abstract explicitly claims MPS's O(dk²) per-input extension eliminated by Levis-fast and O(d) fresh ciphertext communication under Levis-small; this suffices as prior-art/novelty warning **only**. No theorem-level verification of technique, joint-key security, noise or performance. Novel new MKFHE extension-removal mechanism must be differentiated from Levis; do not invent differences without source.
Human Action: If authorized, supply the exact full PDF or stable author manuscript and (for performance review) code/parameters; no unsolicited author contact.
Repository Path: **PENDING/NONE**; once supplied, put an authorized copy in papers/supplied/ if repository protocol allows.
Readability Verification: **PENDING**. After supply, verify PDF SHA/version, read pages defining Cofactor Compatibility and concrete algorithms and visually verify hard mathematical identities.
Evidence: findings/mkfhe-levis-2026-2263-extension-free-novelty-source-gate.md (2026-10-14).

### 2026-10-15 vFHE V39 official-source retrieval retry (no new numbered V40)

**STATUS: STILL MISSING_CURRENT_OFFICIAL_BINARY; SOURCE_VERSION_GATED / HUMAN_REVIEW.** This is a retrieval provenance addendum only, **NOT V40**. Read the original source record above, authoritative `findings/vfhe-cross-crt-state.md` (V39 COMPLETE/V40 NOT STARTED), and root `STATE.md`; do not advance counters from a public slide deck.

- Official live landing https://eprint.iacr.org/2025/286 still lists 2026-02-16 revision and explicitly states 'Fixed a flaw in the proof of Theorem 4.8. Minor editorial improvements.' It does NOT expose official current PDF SHA through the publicly indexed HTML. The direct linked PDF was delivered through web indexing as **50 pages, crawled ~1.4 years ago**, and thus is an old cached snapshot, not a verified 2026 binary. Its PDF screenshot also failed web cache; we did not inspect its purported correction.
- `https://eprint.iacr.org/archive/versions/2025/286` (the official 'See all versions' destination) returns **HTTP 403** to the available research browser; attempts to fetch direct official PDF in the local tool container fail DNS for eprint.iacr.org, as before.
- A newly located independent mirror `https://eprint.iacr.asia/2025` provides a current index of 2025 titles, but direct candidate `https://eprint.iacr.asia/2025/286` and `.pdf` cannot be retrieved by the available web tools (cache miss / inaccessible). A mirror's freshness alone **does not certify the requested official bytes**; no SHA/version match is obtainable.
- New source *context*, NOT a substitute for revised Theorem 4.8: the **same authors** presented `Batch, Pack, and Prove: More Efficient Verifiable Computation for CKKS` at FHE.org 2026; public 88-slide PDF https://fhe.org/conferences/conference-2026/resources/slides/1440_Guimaraes.pdf . Slides physical ~pp33–43 explain packing small `Z_B` values into `R_q` and virtual `Z_B` oracles for range checks, and pp46–64 describe Batched Ring Basefold. This is an independent **follow-up optimization presentation** and does not state whether or how the **current official 2026 revision's Appendix E.2** establishes *globally canonical integer digit* membership across distinct CRT primes. Do not equate `Z_B` marketing diagram with a cryptographic proof.
- Author code https://github.com/vfhe/proof-friendly-CKKS identified from web search, but its README links back to ePrint2025/286; it is not an attested official revision PDF or a source for Appendix E.2 semantics.

**Precise remaining required input:** human PI obtains the current PDF bytes by manually using a normal browser on https://eprint.iacr.org/2025/286 (PDF button) on 2026-10-15 or later and supplies the **downloaded file itself**. On receipt record SHA256, physical-page count, version page/history markers, compare exact Remark 4.9/Theorem4.8 and Appendix E.2 lemma statement/proof to the known 52pp mirror SHA `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`; revalidate the exact CRT 261 counterexample ONLY if the current statement still demands global canonical digits. Without the bytes, keep V40 NOT STARTED and do not make current-official vulnerability or repair claims. No authors contacted.


### 2026-10-15 V41 February-2026 PDF Info and mirror Git-provenance — IMPORTANT, OFFICIAL FILE STILL MISSING

**STATUS REMAINS MISSING_CURRENT_OFFICIAL_BINARY / SOURCE_VERSION_GATED.** Actual public GitHub mirror file `arturo-kong/IACR-eprint-mirror/2025/286.pdf`, blob SHA-1 `a549654c5dffa3484e95e8244056f4a27c48c3e6`, decoded 836746 bytes, PDF-1.7, has decoded PDF Info `/CreationDate (D:20260216103027+01'00')` AND `/ModDate (D:20260216103027+01'00')`. Live official landing records 2026-02-16 revision fixing proof Theorem4.8, the SAME calendar date. GitHub file history shows first addition commit `03d21d9516bb8a5ae39c9882194c252fbd7c2a25` on 2026-04-28T17:20:00Z; parent file fetch at immediate prior commit 7f265e6383b958537af0a5f89dc42497a795db43 returned 404. That Git blob matches Research MCP source_revision of parsed 52pp mirror, PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`. Mirror p24 contains correction Remark4.9 and p48 still contains disputed CRT global-to-local implication. **Strong INDIRECT edition corroboration, NOT official byte identity:** PDF Info may be edited, third-party repo is not IACR; current IACR PDF bytes/SHA remain inaccessible. Do not mark supplied or claim official author exploit. Source `findings/vfhe-v41-feb2026-mirror-pdf-timestamp-provenance-gate.md`; full report `/mnt/data/VFHE_V41_Feb2026_PDF_Internal_Date_Provenance_Gate_2026_10_15.md`. **Required human action unchanged:** provide actual current official download for SHA comparison. GLOBAL I192 frozen.
