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
