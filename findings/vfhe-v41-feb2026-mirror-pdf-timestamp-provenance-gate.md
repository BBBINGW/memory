# vFHE V41 — Feb-2026 PDF internal timestamp + public Git mirror lineage strongly corroborate revision identity, official SHA still unavailable

**Date 2026-10-15 (Asia/Tokyo). ONE primary hypothesis/test; independent vFHE V41 after V40 SOURCE_BLOCKED; global general I192 FROZEN.** This is a provenance audit of the existing Theorem4.8 mirror. No new paper attack, no author contact, no code changes to upstream.

## H-V41 and decisive experiment [FACT / DERIVATION]

**H-V41:** The inspectable 52pp ePrint2025/286 GitHub mirror is actually demonstrably **older** than the official 2026-02-16 proof-revision date and therefore categorically cannot correspond to that revision. **FAIL that old-binary interpretation, PASS strong indirect same-day evidence.** Original LIVE official IACR landing `https://eprint.iacr.org/2025/286` reports **2026-02-16: revised**, notes a correction to Theorem4.8 proof. The corresponding UNTRUSTED third-party repository `arturo-kong/IACR-eprint-mirror` was audited using the GitHub CONNECTOR, not a mere snippet.

- GitHub path-specific commit history `GET /repos/arturo-kong/IACR-eprint-mirror/commits?path=2025%2F286.pdf&per_page=5` identifies addition at commit `03d21d9516bb8a5ae39c9882194c252fbd7c2a25`, timestamp **2026-04-28T17:20:00Z**, message `Update latest ePrint PDFs (2025 part 1)`. Exact `fetch_file` at predecessor `7f265e6383b958537af0a5f89dc42497a795db43` gives 404 for path; thus path was **not there before** that snapshot.
- Exact `mcp__GitHub__fetch_file({repository_full_name:"arturo-kong/IACR-eprint-mirror", path:"2025/286.pdf", ref:"03d21d9516bb8a5ae39c9882194c252fbd7c2a25", encoding:"base64"})` returned base64 of a PDF-1.7. Decoded in-memory raw binary length **836,746 bytes**, GitHub content-addressed blob SHA-1 `a549654c5dffa3484e95e8244056f4a27c48c3e6`. Direct byte-string inspection found PDF Info:
  - `/Producer (pdfTeX-1.40.27)`
  - `/Creator(LaTeX with hyperref)`
  - `/CreationDate (D:20260216103027+01'00')`
  - `/ModDate (D:20260216103027+01'00')`
  Both dates match OFFICIAL 2026-02-16 revision CALENDAR DAY, not an older PDF build date.
- Research MCP's `get_eprint_paper("2025/286")` previously returned **the identical source Git blob SHA** `a549654c5dffa3484e95e8244056f4a27c48c3e6`, exact same **836,746 bytes**, 52pp, PDF SHA-256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, source_kind `github-mirror`, version_status `VERSION_UNVERIFIED`. Git blob SHA matching across two independent connector interfaces tightly connects the full parsed 52pp paper to that 2026-04-28 GitHub file. **This is NOT a download of IACR OFFICIAL 2026 PDF and NOT an official SHA attestation.**

**CRITICAL PROVENANCE LIMIT:** PDF Info CreationDate/ModDate are user-writable fields, and a later mirror commit can copy arbitrary older/source-modified content. Neither matching dates nor correct Git blob source ID logically proves equal PDF bytes to official IACR on 2026-02-16. Container raw.github* and eprint.iacr.org DNS both fail; indexed official PDF cache gives **older 50pp snapshot**, screenshot fails 403; no direct current IACR PDF SHA obtained. Therefore status remains **OFFICIAL_SHA_UNVERIFIED**; published current-proof flaw or exploit remains UNCONFIRMED.

## Direct source text [read_eprint_pages physical pp23–24, 47–49]

- Mirror physical **p23** Theorem4.8 now includes `beta<pmin` and `2^ellstar<pmin`.
- Mirror physical **p24** Remark4.9 itself says a PREVIOUS version's Lemma4.6 was wrongly invoked over a ring and has been restricted to FIELD; these are the SAME subject as official landing's correction note. Together with PDF Info this is stronger revision-correspondence evidence but not conclusive official-byte authentication.
- Mirror **p48** AppendixE.2 nonetheless asserts an invalid implication: a globally illegal canonical ring digit forces at least one CRT field projection not to belong to scalar digit table. **THIS 52pp MIRROR implication is false.** No statement here about the current, byte-unverified official edition.

## Already-known CRT fact: independent simple exact census

Source-compatible `N=4,d=2,p13=1+4·3,p29=1+4·7,q377,beta4,ellstar3`; both `beta4<13` and `2^ellstar8<13` satisfy the amended mirror Theorem4.8's extra bounds. For scalar CRT residue values independently chosen in local `{0,1,2,3}` for the two distinct primes, exactly `beta²=16` pairs are locally valid at all four native degree-2 factors but only `beta=4` pairs are diagonally equal to ONE global legal scalar ring digit. **12/16 are globally illegal while locally legal**, especially `h=261` with `h mod13=1`, `h mod29=0` and factor tuple `(1,1,0,0)`. Prior V17–V23/V39 already prove this and develop source-ideal PIOP transcripts; **V41 does NOT claim this is a novel attack**.

## STATUS / DECISION

**STATUS:** PASS strong independent corroboration of same-day **PDF BUILD** and postrevision mirror addition; FAIL presumption mirror was definitely pre-Feb2026; **SOURCE_VERSION_GATED/HUMAN_REVIEW** for official PDF SHA, original theorem status and any responsible disclosure.

**RESULT:** Significantly improves V40 provenance classification from 'undated GitHub mirror' to 'public GitHub 2026-04-28 addition of a PDF built 2026-02-16, exact same source blob as 52pp parsed Research MCP copy'. The mirrored p48 inference remains refuted; cannot claim original live version is conclusively identical without official byte check.

**NEXT_ACTION V42 (only PI continuation):** FIRST compare current official ePrint PDF binary to mirror SHA-256, or have PI upload official same-day/current PDF bytes. If exact equal, then assess whether revised Theorem4.8 and full compiled range protocol need further scrutiny, using original current source and documented proof obligations. If unequal, make page-aware diff. No speculative new massive BP++ proof implementations or author contact until source identity resolved.

**STATE_UPDATE:** YES V41; global general I192 FROZEN; do not mark `MISSING_SOURCES.md` entry SUPPLIED.

**Local artifacts (generated and verified)**:
- `/mnt/data/VFHE_V41_Feb2026_PDF_Internal_Date_Provenance_Gate_2026_10_15.md` SHA256 `4e6cf30196ed03097d9c183b89ff9d05b34af1a4e042a323da091b33954fc767`.
- `/mnt/data/vfhe_v41_revision_provenance_gate.py` SHA256 `d7e3a8153d9be24975fb56c1f11c3049c612b15250d18be4cc7f47788c79dc87`; includes optional user-supplied PDF SHA-256/Info checker and ALL 16 CRT cases.
- `/mnt/data/vfhe_v41_revision_provenance_gate_results.json` SHA256 `29f7e25d0f4058592b8e27f554c4066bcb78ed5744a1e3b01f1c50f6e38cd859`.
