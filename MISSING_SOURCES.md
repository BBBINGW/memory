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
