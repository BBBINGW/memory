# I192 — AKU FHEW DFR author-version source gate

Date: 2026-10-14. One authorized research iteration after I191. Reviewed START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, STATE.md (SHA 799025f2d8a95a5fd14856b9a481934f63e4e9f9), and I190–I191.

## Primary question
Can an authenticated author implementation and final published formula independently reproduce or resolve the ePrint 2025/381 Table3 Algorithm6 DFR 2^-36, as against the §5.1 source-extracted variance calculation?

## ONE cheapest decisive test
Check the official CANS2025 chapter's availability, visible §5.1 formulas and original author-pinned experimental repository/commit. Do NOT substitute current OpenFHE HEAD for the author's code.

## Evidence
- Zhang, Wang, Cheng, *Faster FHEW Bootstrapping with Adaptive Key Update*, CANS2025, Springer LNCS16351 pp292–312, DOI 10.1007/978-981-95-4434-9_14. Publisher https://link.springer.com/chapter/10.1007/978-981-95-4434-9_14 confirms published chapter and exposes only abstract/metadata; §5.1/full tables require institutional access.
- IACR https://eprint.iacr.org/2025/381.pdf readable as 27pp text. Research MCP GitHub-mirror SHA256 bbc507b8323f4a65dea806bb663c9eea8ef2954e41259cad3b9db11256a03faf, 707942 bytes, VERSION_UNVERIFIED. §5.1 p19 shows beta variance model, Gaussian n447 sigma3.19, q1024, Qks16384, final ModSwitch term (norm squared plus one)/12 and extracted DFR erfc((q/8)/(2 beta)); Table3 p21 Alg6 DFR2^-36. The web PDF screenshot for physical page19 failed; exact rendered math and publisher-version parity are NOT visually checked.
- Targeted GitHub repository and file searches (full title, authors, AKU/FHEW, 128_OURS), public search and ePrint text searches found NO authenticated author experiment source/commit or code release pointer. This is not proof the source does not exist.
- Current upstream OpenFHE was checked in I191: Gaussian key dgg(3.19), qKS-to-q per-coordinate round. Its version is NOT established as the author's 2025 implementation.

## STATUS / RESULT
STATUS: **FAIL** sufficient original author-edition evidence currently available for independent table reproduction; **PASS** exact source-access and code provenance checks; **UNCLEAR / SOURCE_VERSION_GATED** actual author's full variance calculation, printed publisher equation, real DFR and alleged error.
RESULT: The *conditional extracted ePrint-model discrepancy* from I190–I191 remains; do not assert actual FHE decryption failure or broken 128-bit security. No new numerical experiment or cryptographic claim I192.

## NEXT_ACTION / STATE_UPDATE
NEXT_ACTION: **I193 NOT STARTED. PARK the alleged correctness-error claim pending verified final full chapter §5.1 or authenticated author experiment source/parameter script.** Once obtained, one test: recompute every beta term and verify the 2^-36 table with the original DFR estimator. Otherwise pivot to a different fully sourced FHE bottleneck rather than repeat Gaussian toy tests.
STATE_UPDATE: **YES**. Record missing publication/author artifact in MISSING_SOURCES.md and checkpoint STATE.md. PI decides final research strategy.
