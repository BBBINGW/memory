# Iteration 163 — ePrint 2025/429 Table 4 (r=5; polynomial degrees 53,25) source artifact / coefficient availability gate

**Date:** 2026-10-13. Human PI approved I163 via “好的，请继续” after I162. ONE primary source-availability hypothesis and ONE targeted retrieval/check gate. Do not assert a universal nonexistence of unpublished/restricted artifacts.

## Read before write

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` after I162 SHA `914e6687c69bd43dd97dc5310c113ddcd3c8b55e`, `findings/ckks-generalized-composite-fixed-degree-weighted-minimax-test-iteration162.md`. Inspected existing `MISSING_SOURCES.md` blob `57e7580a352b7d5911c66bc7c0ec2544926bfc30`; no existing 2025/429 entry.

## Source and unique objective

Original Seonhong Min, Joon-Woo Lee, Yongsoo Song, *Enhanced CKKS Bootstrapping with Generalized Polynomial Composites Approximation*, ASIACCS 2025, IACR ePrint **2025/429**, DOI 10.1145/3708821.3710824. Full **19 physical-page** Research MCP PDF mirror, SHA256 `150b337c0b11bc284b1f5d129c7ef1455451de0fe7cbbfd19ba8cb21e7e8dd4d`, version `VERSION_UNVERIFIED`. Official ePrint landing `https://eprint.iacr.org/2025/429` reports **2025-09-11: last of 2 revisions**, though bytes of current official PDF have **not** been compared to the mirror. Primary PDF §3.1 pp6–7 and §5.1 p16 describe two-stage odd-r generalized sine/inverse-sine composition and fitting with **multi-interval Remez** (referencing earlier [20]); §5.2 pp15–17 reports **Lattigo** implementation.

**[HYPOTHESIS / single falsifier]** A publicly identifiable *author-matched, pinned* code release, fitting script, polynomial coefficient table or supplemental artifact exists for the paper's **Table4 Set I, r=5, degree set (53,25)** such that I162's derivative-weighted p1 can be compared fairly to actual original p1/p2 (at unchanged outer p2 and unchanged evaluation cost), without inventing original coefficients. Locate a concrete verifiable artifact/repo/ref and coefficient instructions or record MISSING CRITICAL SOURCE.

## Exact primary facts

Source §5.2 physical p17 Table4 Set I “Ours”: **r=5**, “Degree Set” **(53,25)**, log PQ **1547**, Level **11**, average BTS precision **27.12** bits, `# relin=20`, BTS time **24.9 s**. These are **published source results**, NOT experiments executed this iteration. §5.1 p16 says stage polynomial approximations use multi-interval Remez with precision-target and level heuristics. Original paper **does not enumerate p1/p2 coefficients or identify a project-specific source repository, tag, commit, coefficient file or exact fitting script** in the inspected full 19pp. MCP `search_eprint_text(2025/429, github)`, `source code`, `supplement` found zero relevant matches, `Remez` and `Lattigo` lead to general method paragraphs and references, and `53, 25` to Table4.

## External artifact discovery attempted (source vs inference)

- **[FACT primary author websites]** Seonhong Min's public publications listing `https://minsh.info/pages/publications` and SNU Crypto & Privacy Lab listing `https://crypto.snu.ac.kr/publications` both list the target publication and link to its ePrint; **no publication-specific code artifact** is linked on the inspected entries.
- **[FACT official ePrint]** `https://eprint.iacr.org/2025/429` lists title, authors, latest revision date, published DOI, PDF; **no source-code artifact on visible landing**.
- **[SEARCH OBSERVATION]** Queried public web for exact paper name + GitHub/Lattigo/code, Seonhong Min / Joon-Woo Lee / Yongsoo Song names, title and ePrint ID. Public GitHub repository-name searches for “Generalized Polynomial Composites”, “enhanced ckks bootstrapping”, etc. returned no matching implementation repo. GitHub code search for exact title surfaced academic metadata/bibliographies/author publication markdown but no matching source code. Search for `"53, 25" "ckks"` yielded unrelated false positives. SNUCP organization repository searches for `bootstrapping, polynomial, evalmod, lattigo, remez` returned unrelated projects (e.g. blockkey-tfhe or jindo), no target software. Author `minshinfo` public repo list included `HIENAA.jl`, `fhe-org.github.io`, `snu-lukemin.github.io`; no identified ePrint 2025/429 software. `YongsooSong` public repos included `HybridHE`, `tfhe`, `FHEW`, `yongsoosong.github.io` but no matching project-specific artifact. A `user:snu-lukemin` repository-name query returned an API 422 account visibility/name error, so **do not claim all of that user's public repositories were exhaustively checked**.
- **[CRITICAL DISTINCTION]** General public Lattigo implementations are NOT equivalent to the author-specific 2025/429 polynomial fitting, special r-angle inverse sine, and chosen (53,25) coefficient arrays. Re-implementing from prose may be feasible as **independent reproduction**, but cannot substitute for a confirmed original polynomial/benchmark implementation.

## Decision and limits

**STATUS = UNCLEAR / MISSING_CRITICAL_SOURCE** on ability to verify a *source-matched* Table4 (53,25) weighted-vs-original p1 precision/cost improvement. This is a gate, NOT a positive numerical result. Under current sources no pinned author p1 coefficient vector, p2 vector, Remez generator, Lattigo tag/commit or random seed can be read. No actual CKKS computations or end-to-end precision/latency comparison performed in I163, no further degree43 toy. A public artifact may exist outside the indexed/accessible repositories, so **not found != proven unavailable**. Original full-paper math §3.1, §5 is accessible and I160–I162 conditional findings still stand, but **the source-grade comparison demanded by NEXT_ACTION is blocked**.

**PI action options:** supply author source archive/commit or the exact two polynomial coefficient vectors and fitting/config parameters with benchmark recipe; or explicitly authorize a new **independent reproduction** methodology from public paper + pinned open Lattigo/multi-interval Remez library with uncertainties reported. No contacting authors without explicit PI approval; do NOT invent a supplied file path.

## End of Iteration 163

**STATUS:** **UNCLEAR / MISSING_CRITICAL_SOURCE** (source-realism gate unsuccessful; nonexistence not proven).
**RESULT:** Original Table4 r5 (53,25), full Lattigo usage and multi-interval Remez method verified. No matching released author source, coefficient vectors, fitting scripts or pinned versions found through source/PDF, author listings, public web and GitHub search. Earlier I162 2.14188× ideal d43 result cannot be upgraded to actual 27.12-bit CKKS result.
**NEXT_ACTION:** **SOURCE-GATED / HUMAN_REVIEW.** Receive **author-matched** Table4 r5 polynomial coefficients and matching code/config; OR authorize a clearly labeled **independent reimplementation** using public specification and pinned library versions, then perform ONE matched (53,25) p2-aware numerical test with no source-equivalence assertion. No repeat of arbitrary-degree exact-outer toys.
**STATE_UPDATE:** **YES** — pause source-dependent I164 until new material, add `MISSING_SOURCES.md` entry and checkpoint `STATE.md`; SPRU remains PARKED, vFHE P1 source-gated.
