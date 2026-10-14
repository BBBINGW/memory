# vFHE V42 — Official current 2025/286 PDF SHA-256 acquisition GATE: SOURCE_BLOCKED / HUMAN_REVIEW

**2026-10-15, independent vFHE V42; general I192 FROZEN.** Human PI said continue. Read first START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, STATE.md and authoritative V41 and V40 source-gated findings, plus MISSING_SOURCES.md. No new generic BP, IPA, sketch or range-lookup repair branch.

## One primary H-V42 and decisive gate

**H-V42:** Current available official website, official PDF/history API, direct byte fetch or independent mirror can supply exact fresh **OFFICIAL-Origin** IACR ePrint2025/286.pdf bytes, so we can SHA256 compare to known 52pp Feb2026-looking GitHub mirror. **STATUS SOURCE_BLOCKED (test FAIL IN THIS ENVIRONMENT)**: current official bytes were NOT obtained. This is an acquisition/access result, **not a refutation or validation of current paper**. V40 already failed same key retrieval through simpler access; V42 adds tried newly located independent eprint.iacr.asia and provides an offline deterministic file-authentication workflow, not a claim of new exploit.

## Precise source evidence [FACT]

- Official HTML `https://eprint.iacr.org/2025/286` was re-opened LIVE by web; history states **2026-02-16: revised**, note `Fixed a flaw in the proof of Theorem 4.8. Minor editorial improvements.` Thus the paper underwent formal revision. HTML metadata **does not publish SHA256 of current PDF**.
- `https://eprint.iacr.org/2025/286.pdf` opens through web only as **stale cached 50-physical-page index**, crawled ~1.4 years earlier, hence cannot be current by itself. Link clicked from current landing returns same indexed edition. PDF screenshot via web tool failed Internal Error; official `See all versions` click failed Internal Error. Browser attempts at fresh query variants and history paths failed tool access (not independently verified server 404).
- Independent container `requests.get` to exact official PDF encountered DNS NameResolutionError; `container.download` to exact official PDF reported `download failed`. Hence no downloadable PDF bytes / SHA for official current origin. OAI query was inaccessible.
- Independently discovered public third-party mirror `https://eprint.iacr.asia/` has apparently maintained index, but its paper-specific `/2025/286` was a web Cache miss and `/2025/286.pdf` was not accessible from tool. No new hash obtained.
- Current Research MCP `get_eprint_paper("2025/286")` returns **cache_hit=true**, same GitHub mirror: `source_kind=github-mirror`, `source_revision=a549654c5dffa3484e95e8244056f4a27c48c3e6`, 836746 bytes, 52pp, SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, `VERSION_UNVERIFIED`. See authoritative V41 for source PDF internal **2026-02-16** build timestamp + GitHub path addition **2026-04-28**. These are strong provenance indicators but **do not cryptographically establish byte-identical present-day IACR PDF**.

## Decisive test and reproducibility

Created offline byte checker `vfhe_v42_official_pdf_byte_gate.py`. It hashes an optional user-supplied REAL official PDF and compares to pinned mirror SHA (checks bytes, PDF header and, if fitz available, physical pages, PDF metadata and theorem text marker presence). It explicitly warns that supplied file **provenance is not verifiable from pathname/metadata alone**; official-origin browser download from original URL must be preserved. Without actual official file it emits `SOURCE_BLOCKED_NO_OFFICIAL_PDF` (actual executed test). Synthetic 1-page PDF input deliberately yields `BYTES_DIFFER_FROM_PINNED_MIRROR` with exit code 2, confirming mismatch branch; synthetic bytes never treated as authentic evidence. Neither run produces a fabricated official SHA.

**Local deliverables created and verified exactly:**
- Full report: `/mnt/data/VFHE_V42_Official_Current_PDF_Byte_Authentication_Gate_2026_10_15.md`, SHA256 `d26ee1c429a014c81a8cf30c595f11d4a9d5620a8f89700eb9088d66d51d28de`.
- Offline verifier: `/mnt/data/vfhe_v42_official_pdf_byte_gate.py`, SHA256 `d04659966c47e98eaaec13065adf9e7e64885d40ba58895ae5790e912e66a8e0`.
- JSON blocked-state record: `/mnt/data/vfhe_v42_source_authentication_results.json`, SHA256 `71ae03a19581fffce9ca6822fd398dc4db28e91cf4583ebcb6975ee617dc25db`.

## Scientific boundaries and human next action

The original **mirror** p48 AppendixE.2 diagonal scalar-digit inference has a proven source-legal CRT counterexample in V17–V23 and V39; V41 already demonstrated mirror build dates match revised-day metadata. **Nothing in V42 proves whether current official Theorem4.8's text repeats that flaw, nor a compiled source end-to-end exploit**. Do not contact authors without PI authorization; do not publish a current-official vulnerability claim or modify original repo. MISSING_SOURCES.md official current PDF entry remains **MISSING_CURRENT_OFFICIAL_BINARY**, not SUPPLIED/RESOLVED.

**NEXT_ACTION (HUMAN_REVIEW, no V43 automatically):** The PI can download `https://eprint.iacr.org/2025/286.pdf` in a browser and supply original unmodified file with URL/date, then use offline checker; if SHA matches mirror, byte identity is established *relative to that authenticated download*; if differs, compare full Theorem4.8, Remark4.9, AppendixE.2 and native F.2 relation before any claim. Alternatively PI explicitly authorizes switch to a source-complete FHE project target. No generic repair branches until this source gate clears.

**STATUS:** SOURCE_BLOCKED / HUMAN_REVIEW; **RESULT:** official current PDF SHA unavailable, executable SHA gate prepared, strong V41 indirect provenance retained; **NEXT_TEST:** authenticated official PDF comparison or PI source-complete pivot; **STATE_UPDATE:** YES V42 complete source-gated, V43 NOT STARTED/NO AUTO continuation. Global I192 frozen, unrelated SHIP I226 untouched.
