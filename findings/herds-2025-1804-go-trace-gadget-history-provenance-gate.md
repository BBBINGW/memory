# HERDS H-HERDS-05 — Public Go history preserves trace-key/BRK gadget coupling across all four commits

**Date:** 2026-10-14 Asia/Tokyo. Standalone independent HERDS audit round 5, after HERDS H04. Human PI said continue. Read before write: START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, concurrent global STATE.md (frozen old I192, independent vFHE V25, READ ONLY), and findings/herds-2025-1804-author-go-trace-gadget-paper-code-mismatch-gate.md SHA 9e554886dc41ac750540ed7df4cf1ab81cb384a9. Original SHIP independent I226 left unchanged. No strategic change to live PI-selected vFHE workstream or publication claim.

## One primary falsifiable hypothesis / one minimal decisive test

**H-HERDS-05:** The disagreement between HERDS Table 3 (32-party, λ100 Set V TRK gadget (2^5,8)) and current Go trace-key gadget (2^9,4, sourced from BlindRotateParameters) was introduced **only in the final 'Ready for publish' commit** in December 2025; an earlier PUBLIC implementation revision generated trace keys with a dedicated (2^5,8) gadget, enabling recovery of a publication-equivalent Go trace-key implementation by checking history.

**Falsifier:** Enumerate the available public commit history of `SNUCP/mktfhe-parallel-go` (four indexed commits as of audit date); for EACH commit fetch original `mktfhe/bootstrap_keygen.go` by full SHA, verify its exact Git blob SHA, and read the `GenTraceKey`→`GenGLWEKeySwitchKey` argument. At least the Initial Commit's use of BlindRotateParameters disproves the claim 'introduced only in final release'. Also read contemporary parameters and date metadata so an earlier experimental revision is NOT falsely treated as a final paper benchmark.

## Primary source [FACT]

**Paper:** Xiang et al., *HERDS: Multi-Key Fully Homomorphic Encryption with Sublinear Bootstrapping*, EUROCRYPT 2026 / IACR ePrint 2025/1804. Full Research MCP PDF 46 physical pp, fixed mirror PDF SHA256 c08a83cea17b352df1006a7051cee26c133bf92a4212860d3cf28f6b6426e7d7, revision d68d3723d26dc2978fcb8f0506946a6314eca0c9, `VERSION_UNVERIFIED`. Physical p27 Table 3 Set V: k32,n560,N2048,beta1.2e-19, BRK `(2^9,4)`, TRK `(2^5,8)`, pk/rlk `(2^4,10)`; physically p26 says implementation at https://github.com/SNUCP/mktfhe-parallel-go. Text-extracted parameter table is legible; PDF/publisher version exact parity not independently established.

**Pinned source and GitHub-native retrieval:** repo https://github.com/SNUCP/mktfhe-parallel-go, default branch main (from get_repo); branch search using empty query returned `main` (no alternate branch observed in this response, but not evidence no private/unindexed history exists). Native GitHub search_commits with an empty repo-specific query returned four public commits as of 2026-10-14; fetched each commit's metadata and original source files using the exact commit SHA:

| Git commit | date UTC | message | `mktfhe/bootstrap_keygen.go` blob | argument to GenGLWEKeySwitchKey |
|---|---|---|---|---|
| `1170468723864cc916e1efce850064f8192821d5` | 2025-04-23 14:16:20 | Initial Commit | `50f8832061ceadfb6ec2e4c00b6891f603847f7b` | `e.Parameters.BlindRotateParameters()` |
| `04fe8c66c1c41510698b1532fe10ba791a3b2e69` | 2025-04-23 14:19:10 | fix: Fix wrong import | SAME | SAME |
| `9247b8bc2892538e02519190495e6f0d101d6eff` | 2025-04-24 02:16:46 | fix: Remove parameter restriction | SAME | SAME |
| `e3b8f56d92a5bc535e9b2f0853f4b7135dcbe53a` | 2025-12-11 02:14:26 | feat: Ready for publish | SAME | SAME |

Code first published in source is consistent across all four commits:

```go
traceKey[i] = e.SingleKeyEncryptor.GenGLWEKeySwitchKey(
    skAut, e.Parameters.BlindRotateParameters())
```

Historical public repos' `mktfhe/params_list.go` DID change across commits: earliest two have blob `06d4ddaf23d7e01316baacffaa073c2caa9c97fc` with **GLWEStdDev 4.63e-18** and only 2/4 presets active, others commented; April24 has blob `4654714ae35bc5030c88b51e56e29299d7c750aa` with same initial noise and commented upper parties; December 'Ready for publish' has blob `8e18f4dea1c438109b6d6b7a7c68350796089d6f`, enables 8/16/32 100-bit presets and sets **GLWEStdDev 1.2e-19**. Some older bootstrap-order settings also differ. **Therefore no older public 32-party publication-matched benchmark can be inferred from the historical commits**, even though the keygen call itself remained unchanged. Do NOT confuse author repository's December 2025 *commit message* with an authenticated tag of the EUROCRYPT 2026 published experiments.

**Dependency call-chain corroboration** in H04: `GenEvaluationKey` calls `GenTraceKey` and Eval's trace keys are registered/consumed by `TraceRLWEToRLevAssign`. tfhe-go@v0.6.0 `GenGLWEKeySwitchKey` uses its supplied gadget parameters. This is a real source-path setting, not a dead code option. PDF source-only parameter mismatch still persists, but is NOT a proved paper theorem error, DFR break, security deficiency, or actual published timing discrepancy.

**Tag/release limitations:** targeted external web access to official GitHub `/tags` and `/releases` returned cache-miss; no author-attested paper commit/tag or benchmark-run hash recovered. Native GitHub branch search found `main`; commit search returned four currently indexed public revisions, not an audit of *all possible* tags, private branches, local unpublished runs or removed refs. Absence of a retrieved historic dedicated TRK version must NOT be generalized into a claim none ever existed anywhere.

## One decisive result and scientific status

**STATUS: FAIL H-HERDS-05** (the mismatch did NOT first arise in the last public Ready-for-publish commit). **PASS four-version pinned read-backed identical Git blob/source-equality test.** **UNCLEAR** actual code at paper's reported experimental run, publisher-version input, intention, whether benchmark logs exist, and actual noise/runtime impact beyond approximate equations. **NOVELTY NOT VERIFIED.**

**RESULT:** The `BlindRotateParameters()`→TraceKey implementation coupling is present at the earliest public Go commit (2025-04-23) and unchanged through Dec2025; publication-prep only changed other things, including enabling 32-party preset and adjusting torus error parameters. This turns the H04 finding into a durable **paper-vs-released-public-code reproducibility discrepancy with provenance**, NOT a novel FHE algorithmic gap or published cryptographic attack.

**NEXT_ACTION:** HUMAN_REVIEW/PARK source archaeology. Further work only with (i) PI-approved correspondence or author-supplied exact publication benchmark commit and 100/128bit parameter logs, or (ii) a controlled run with `go` and pinned upstream dependency comparing `GenTraceKey` under BRK `(2^9,4)` and manuscript TRK `(2^5,8)` at identical seeds, recording key size / milliseconds / DFR over meaningful trials, and underlying published 128-bit preset if ever supplied. Bare 1,000 no-failure encryptions do not establish negligible DFR, and the approximate six-sigma noise budget remains non-rigorous. If neither evidence path is available, PARK this HERDS reproduction subbranch rather than fabricate source matches or research contributions. Human PI decides directions. Global vFHE/SHIP states untouched.

**STATE_UPDATE: YES** this finding only, no write to global STATE.md, independent SHIP state, OPEN_RESEARCH_BRANCHES.md, or source repo.