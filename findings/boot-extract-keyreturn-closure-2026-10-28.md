# BOOT — SampleExtract / key-return fusion closure

Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER_LEVEL_ONLY
CODEX: NOT_USED
NATIVE: NOT_RUN

## Authoritative native state

LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE_GATE: B163_CORRECTED_B160_NOSCALE_SELECTOR_GATE
B163_STATUS: PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
DO_NOT_AUTO_RUN_CODEX: YES

B158_ALGEBRA: PASS
B158_CTCT_MULT_COUNT: OPTIMAL
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B158_NATIVE_FEASIBILITY: UNRESOLVED
B163: NOT_RUN

## Candidate

Consider the standard FHEW/TFHE tail

    ring accumulator
      -> SampleExtract
      -> modulus/key return
      -> output LWE ciphertext.

Question: can SampleExtract and key return be fused into a new structural primitive that materially reduces work/key material, rather than merely reordering an existing linear transform?

## Source closure 1 — TFHE functional key switching already absorbs linear morphisms

TFHE (ePrint 2018/421) explicitly revisits key switching as a more general functional key-switching primitive.

The paper states that key switching can:
- switch between scalar and polynomial message spaces;
- homomorphically evaluate a public or private Z-linear morphism while switching keys;
- perform projections/permutations/repacking via functional key switching.

It also treats SampleExtract as a noiseless linear operation.

Research MCP source:
ePrint 2018/421, physical pp.19-24 and Table 1 around p.49,
mirror PDF SHA256:
23fa887ff217f14a47763d6711d8c9304a392954751bee11799a223499d393cd
(version status VERSION_UNVERIFIED).

Therefore "absorb a public linear extraction/rearrangement into key switching" is not a new cryptographic primitive.

## Source closure 2 — ring-domain key return before extraction is already prior art

The 2025 improved NTRU-based bootstrapping baseline audited elsewhere in BOOT moves the key return into the NTRU/ring domain before extraction, targeting a zero-padded form of the output LWE secret.

Thus the natural ordering

    ring ciphertext
      -> ring/NTRU key return
      -> SampleExtract

is already an explicit modern construction.

This also shrinks the final KSK to a negligible tail in the reported baseline, making a new extraction/KSK fusion even less valuable.

See:
    findings/boot-KSK-linear-embedding-gate-2026-10-28.md

## Algebraic cost observation

SampleExtract is a public linear rearrangement/sign pattern on the ring ciphertext coefficients.

Moving or fusing this linear map with a key switch does not by itself remove the secret-dependent decomposition work:
- the output mask still depends on the ring-secret coefficients;
- ordinary key switching still requires gadget decomposition / encrypted secret-dependent material unless a stronger secret relation or different cryptographic representation is introduced.

Hence a loop-level implementation can fuse indexing/rearrangement with decomposition, but this is an implementation fusion, not a structural reduction in asymptotic secret-dependent work.

## Decision

SAMPLEEXTRACT_PLUS_KEYSWITCH_AS_NEW_LINEAR_FUSION:
    PRIOR_ART / NOT NOVEL.

RING_DOMAIN_KEY_RETURN_BEFORE_EXTRACTION:
    PRIOR_ART.

EXPECTED_KEY_MATERIAL_REDUCTION_FROM_LINEAR_REORDERING:
    NONE.

EXPECTED_ASYMPTOTIC_DECOMPOSITION_REDUCTION:
    NONE.

CCF_A_B_VALUE:
    FAIL for the generic idea.

CODEX/NATIVE:
    NOT REQUIRED.

## What would be needed to reopen

Only reopen if a new mechanism removes secret-dependent decomposition itself, e.g.:
- a new secret relation with a justified security model;
- a new ciphertext representation that exposes the desired output secret publicly;
- or a cross-stage theorem showing that an entire key family disappears.

Do not spend BOOT cycles on ordinary SampleExtract/key-switch loop fusion.

## Next structural axis

Move to bootstrap-entry or cross-stage questions rather than tail fusion:
- whether input modulus switching can be structurally absorbed;
- whether a later refresh can absorb intentionally coarser earlier approximations;
- or other stage-elimination mechanisms.

B163 remains the highest native priority once Codex quota is explicitly restored.
