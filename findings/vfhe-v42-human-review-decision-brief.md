# vFHE V42 Human Review Decision Brief — no new iteration

**2026-10-15 | SUPPLEMENT to authoritative V42, NOT V43. Global general I192 FROZEN.**

The PI again requested "continue". Before any new research, read and confirmed root `STATE.md` (SHA `3b83237bc5aba4a77479b09dc1f3ac8bccaebc7c`) and `findings/vfhe-cross-crt-state.md` (SHA `a89fdcc5b64fb1365468b8b23be5dad5f51d1299`): **V42 COMPLETE SOURCE_BLOCKED/HUMAN_REVIEW, V43 NOT STARTED** with an explicit **NO AUTO CONTINUATION** requirement unless an authentic official-current source PDF is supplied or the PI expressly chooses a source-complete FHE target pivot. Therefore NO new cryptographic protocol iteration or unapproved topic pivot is undertaken. This is a PI decision and evidence brief only, grounded in the existing source records.

## Proven / not yet proven

**[FACT provenance]** IACR official ePrint2025/286 landing reports the 2026-02-16 revision fixing a flaw in the proof of Theorem4.8. The inspected complete **52pp THIRD-PARTY GitHub-mirror** paper has 836746 bytes, PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, Git blob `a549654c5dffa3484e95e8244056f4a27c48c3e6` and `VERSION_UNVERIFIED` status. Its metadata CreationDate/ModDate corresponds to Feb16 2026, while third-party Git file history first includes its PDF Apr28 2026 (V41). This is strong revision-timing evidence, **NOT byte identity to official current IACR PDF**, whose SHA remains absent (V42). The web-only 50pp indexed copy is stale and should not substitute for the official 2026 bytes.

**[DERIVATION/EXPERIMENT mirror scope]** Mirror Appendix E.2 diagonal scalar-digit membership inference fails in composite CRT ring. Legal exact toy: N4,d2,p13,p29,q377,beta4,ellstar3,h261; h mod13=1, h mod29=0, every native CRT factor accepts local digit, but h is no globally legal 0/1/2/3 scalar digit. V17–V23 and V39 including companion built all-source-style ideal PIOP grand-product identities; 142129 possible ring constant (sigma,tau) challenge pairs passed *this ideal algebraic test* while global range was false. **NOT** an end-to-end compiled Brakedown/Fiat–Shamir exploit, verified current-edition paper erratum, or published deployment flaw.

**[IMPLEMENTATION GAP]** The independently attributed public proof-friendly CKKS GitHub snapshot supplies arithmetic/benchmark building blocks, **not** an independently verified full compiler for the source Figure1 grand product/PCS range proof. Numerous V12–V38 repair submodules work in conditional models/toy groups, but no complete, source-version-matched, full security/zero-knowledge, practical CRT digit repair was demonstrated. Cost figures for individual candidates do not establish universal lower bounds.

## Minimal decisive source gate

1. PI browser-downloads the UNMODIFIED currently served `https://eprint.iacr.org/2025/286.pdf` with exact origin URL + timestamp (NOT search-cached 50pp PDF). SHA256-pin with `shasum -a 256 2025-286.pdf` on macOS or supplied already-tested offline checker `/mnt/data/vfhe_v42_official_pdf_byte_gate.py`. Expected inspected mirror SHA is above.
2. If identical, treat original mirror-paper mathematical audit as directly relating to **that** authenticated file, but still separately check full PIOP→PCS/FS binding and actual compiler before alleging an exploit. If different, page-aware compare current Theorem4.8, Remark4.9, Appendix E.2 and F.1/F.2; SHA mismatch alone may reflect metadata differences.
3. No author contact, public claim or new V43 until PI direction and verified source. Keep `MISSING_SOURCES.md` record `MISSING_CURRENT_OFFICIAL_BINARY`.

## Explicit PI branches

**A** Supply the official PDF and resume version-diff/current theorem audit. **B** Explicitly authorize a source-complete FHE target pivot, then restore its own state before first new falsifiable iteration. **C** Park vFHE and preserve V1–V42 archive. These are choices for the PI, NOT actions taken here.

**STATUS:** SOURCE_VERSION_GATED / HUMAN_REVIEW; **RESULT:** source-specific audit and decision handoff, **no new research proof**. **NEXT_ACTION:** official current PDF or expressly approved pivot. **STATE_UPDATE:** preserve V42 completed/V43 not started and frozen I192; this is a supplemental review file only.

**Full local decision brief** `/mnt/data/VFHE_V42_PI_Human_Review_Decision_Brief_2026_10_15.md`, independently verified SHA256 `a62319905898b4381021544c0b3c509681412ef30d0d58760aba444d672df420`. **Historical sources** `findings/vfhe-v41-feb2026-mirror-pdf-timestamp-provenance-gate.md`, `findings/vfhe-v42-official-current-pdf-byte-gate.md`, `MISSING_SOURCES.md` and `findings/vfhe-cross-crt-state.md`.
