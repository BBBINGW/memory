# Iteration 155 — Current official ePrint 2025/286 version-identity gate remains unresolved

**Date:** 2026-10-13. PI's “好的，请继续” after I154 expressly followed the agent's recommendation to park further integer-code variants and verify the **latest official revision** before assessing disclosure/real-system impact. ONE primary source-identification hypothesis and ONE minimal decisive version-identity test. No new encoder, attack, PCS design, author contact or publication claim.

## Read before write

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` (after I154 SHA `7cd0e8060695597c4f2228a0b68eafa66b9f4371`), I154 archive, I59–60 findings and `MISSING_SOURCES.md`. I152–154 fast field-independent integer encoder candidates are **PARKED** as a repair subbranch, **not** the parent P1 CRT scalar-digit question.

## One precise hypothesis

**[HYPOTHESIS / NOT VERIFIED]** The *current official ePrint PDF* (official landing page latest displayed revision 2026-02-16) is identical to the 52-physical-page Research MCP mirror PDF inspected in I59–60, or at least contains the same Appendix E.2 proof implication and same Theorem 4.8 scalar-diagonal membership relation without an omitted global CRT-index constraint.

**[DECISIVE SOURCE TEST]** Obtain original bytes of the official **current** `https://eprint.iacr.org/2025/286.pdf`; compare SHA256 with the independently cached 52-page mirror SHA `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`. If equal: official version pinned and apply I59–60 audit to it. If different: read actual official §4.3 Theorem4.8/Remark4.9, §5 and Appendix E.2; inspect the exact implication and any new constraints **before** asserting a gap. If official bytes unavailable, mark **UNCLEAR, EVIDENCE MISSING**, rather than inferring identity from title, version date or a cached excerpt.

## Results and source provenance

- **[FACT — official landing metadata, independently browsed]** `https://eprint.iacr.org/2025/286` lists 2025-02-19 received and **2026-02-16 revised**, with note **“Fixed a flaw in the proof of Theorem 4.8. Minor editorial improvements.”** It calls the item a minor revision of the CRYPTO 2025 publication. No later revision is displayed on the retrieved official landing. Metadata is **not** byte-level identification of the PDF.
- **[FACT — Research MCP mirror, source NOT OFFICIAL]** `get_eprint_paper('2025/286')` returned **cache_hit=true**, source_kind `github-mirror`, 52 physical pages, 836746 bytes, SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, `VERSION_UNVERIFIED`. `read_eprint_pages` physical p23 shows revised Theorem 4.8 `beta < p_min` and `2^ell* < p_min`; p24 has explicit **Remark 4.9** explaining an earlier proof fix; Appendix E.2 **physical p48** still says an illegal diagonal scalar-table ring witness implies at least one illegal CRT-field projection. This is the implication falsified by the exact I59–60 PIOP witness. PDF extraction has math/font/layout warnings, although the logical implication is legible.
- **[CRITICAL NEGATIVE SOURCE ACQUISITION]** Web PDF `https://eprint.iacr.org/2025/286.pdf` was delivered as an older **50-page indexed/cached** PDF, inconsistent with 52-page mirror. The official “See all versions” endpoint returned **HTTP 403** via web. A cache-busting PDF URL could not be accessed; an official PDF direct download failed; an independent container request could not resolve the official host. Attempted web PDF screenshot was unsuccessful. **There is no successfully retrieved contemporaneous official PDF binary and NO matched SHA.**
- **[NO NEW SECURITY RESULT]** I59–60 already established a concrete mathematical CRT diagonal-vs-rectangular-membership counterexample and ideal-PIOP composition audit **against the inspected 52-page mirror**. I155 neither extends the attack, nor confirms the result against a byte-verified official current revision or a compiled SNARK. Prior source-language matching revised Remark 4.9 increases plausibility only, **NOT source equality**.

## Result and required human/source action

**STATUS:** **UNCLEAR — EVIDENCE MISSING (current official PDF binary)**. Not a FAIL of the mathematical counterexample; not a PASS of the official-revision flaw hypothesis.

**RESULT:** The official landing confirms a revision as of 2026-02-16, but the accessible 50-page web cache and 52-page Research MCP mirror cannot be certified identical to today's official PDF. Appendix E.2 of the 52-page mirror retains the I59–60 disputed field-projection step. The integer-code repair subbranch I152–154 is now **PARKED by PI assent**, parent P1 **OPEN/HUMAN_REVIEW / SOURCE-GATED**.

**NEXT_ACTION:** Obtain/PI-supply exact **current official** 2025/286 PDF bytes to `papers/supplied/` via approved path; pin physical pages, compare SHA to 52-page mirror; if distinct, inspect Theorem 4.8, Remark 4.9, Appendix E.2 and §5 for any new constraint. Until then **STOP** claims about latest official version, impact, exploit and novelty; no author outreach without PI authorization.

**STATE_UPDATE:** **YES** — active subbranch parked following three failures, source-version verification now has explicit critical-source gate and latest iteration checkpoint I155.
