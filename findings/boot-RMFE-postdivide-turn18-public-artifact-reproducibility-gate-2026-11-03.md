# BOOT / B158 — Research Turn 18/25 — public artifact / reproducibility gate

Date: 2026-11-03 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613 / PRE-TAG + POST-DIVIDE late aggregation
Primary paper: Aung et al., Bootstrapping with RMFE for Fully Homomorphic Encryption, ePrint 2025/350 / PKC 2025

## Read-before-write / durable authority

GitHub Notes reads remain degraded and return empty objects. Durable state was recovered by direct GitHub fetch from BBBINGW/memory main at:

    34a4eb3ba825f8dc377e94aace27984cd416519d

Immediate prerequisite:
- Turn17 freezes estimator-independent source-only L1 propagation at Algorithm4 entry until native prime-set state is known.

The target finding path was checked absent before write.

## Why this turn is paper-level

The mandatory native evidence order is blocked at Step2 recovery-canary execution, while several later correctness claims additionally need exact baseline provenance:
- Aung exact skHwt;
- key-switch digit/column configuration;
- mvec / bootstrappable build state;
- actual RMFE constants / generated files;
- command-line or source-level workflow configuration.

If the authors' implementation or artifact is public, recovering it is higher-information-gain than another source microaudit because it can directly bind the source-faithful baseline and the exact candidate Step3 context.

## Primary hypothesis

A current public implementation artifact for Aung et al. 2025/350 can be located and used to recover the exact experimental HElib context needed for baseline/candidate correctness.

## Falsifier

FAIL the bounded public-artifact route if all currently inspectable primary and resource sources expose only the paper/slides/results and pinned upstream HElib commit, while no author implementation repository, supplementary archive, exact workflow source, or parameter/configuration artifact can be located.

## Search scope

Current search date: 2026-11-03.

Sources inspected:
1. ePrint 2025/350 full text / metadata and all implementation-related text searches;
2. PKC 2025 official IACR slide deck, including visual inspection of the implementation slide;
3. Springer/PKC bibliographic landing surfaces and DOI-oriented supplementary-material searches;
4. Ask Cryptography resource topic for 2025/350;
5. current general web exact-title searches for source code / artifact / supplementary material;
6. GitHub global code search for the exact paper title and candidate-specific identifiers CtxtsToSlots / SlotsToCtxts;
7. GitHub repository search for RMFE bootstrapping / Aung RMFE / HElib combinations;
8. current author/publication-profile searches for implementation links.

This is a bounded public-web/GitHub search. It does NOT prove that no private, unindexed, deleted, institutional, or author-held artifact exists.

## 1. What the primary paper actually publishes

The paper explicitly publishes:
- HElib as the implementation library;
- pinned upstream HElib commit prefix acdb264;
- bits=400;
- m=32768 for the benchmark family;
- target p / w / k values through tables;
- CPU/RAM and single-threaded benchmark environment;
- benchmark capacities and timings;
- Magma as the RMFE-generation system.

For the current target row, prior durable audits already bind:
    p=5
    m=32768
    w_RMFE=512
    k=5
    bits_HElib=400.

## 2. Missing exact context parameters are still missing

Full-text searches found no published occurrence for:
    skHwt
    Hwt
    hamming weight
    mvec
    stdev
    scale=
    key-switching matrices
    key-switch columns.

The paper discusses the secret key only generically as part of BGV/bootstrap semantics; it does not disclose the experimental secret-key Hamming weight or the concrete HElib builder/key-switch parameters.

Therefore:
    AUNG_EXACT_SKHWT = UNKNOWN
remains mandatory and must not be replaced with HElib's default merely because the source version is pinned.

## 3. PKC slides confirm implementation but do not publish code

The official PKC slide deck visually states:

    Implemented 4 RMFE bootstrapping workflows in C++ with HElib.

It lists:
- naive vs correction digit-extraction styles;
- BSGS vs trace-and-merge recode optimisations;
- sample results.

The deck contains no visible repository URL, code URL, artifact URL or supplementary-material pointer. Text search for github/code/artifact also returns no matching link.

Thus the slides confirm implementation existence at publication time, but do not make the raw implementation recoverable.

## 4. Paper itself links only the upstream HElib repository

The only GitHub reference located in the paper relevant to this implementation is the upstream HElib citation:

    github.com/homenc/HElib
    commit acdb264.

No author repository or fork is cited for the RMFE bootstrapping modifications.

This distinction is crucial:
    pinned upstream HElib source != Aung experimental implementation source.

## 5. Current GitHub search result

Global GitHub code search for:
    exact paper title
    CtxtsToSlots RMFE
    SlotsToCtxts RMFE
    2025/350 RMFE
did not locate the authors' workflow implementation.

Repository search for:
    RMFE bootstrapping
    Bootstrapping RMFE HElib
    CtxtsToSlots
    SlotsToCtxts
    Aung RMFE
returned no matching implementation repository.

Unrelated bibliography/index copies of the paper were excluded.

## 6. Current general-web/resource result

Exact-title searches for:
    supplementary material
    source code
    artifact
    HElib code
did not surface a downloadable author implementation.

Springer/DBLP/MaRDI/ORCID surfaces point back to the chapter/ePrint metadata rather than a code artifact.

The current Ask Cryptography resource topic contains only the initial system-generated paper resource post; no implementation/GitHub resource is visible.

A January 2026 SGCrypt talk page confirms a later talk on the same work, but does not expose implementation source.

## 7. Reproducibility consequence

The public evidence is sufficient to reconstruct a SOURCE-FAITHFUL approximation around pinned HElib, but not to claim byte/source-level reproduction of the authors' experiment.

In particular, public evidence currently cannot certify:
- exact context.getHwt()/rcData.skHwt;
- exact key-switch column/digit count if authors overrode defaults;
- custom stdev/scale if any;
- exact bootstrappable context setup;
- exact mvec/gens/ords call sequence;
- exact RMFE Magma-generated constants/files;
- exact BSGS/TnM implementation choices beyond the paper-level description;
- exact compiler/build flags and command-line invocation.

Therefore a future baseline run built from the paper must be labelled:

    SOURCE-FAITHFUL RECONSTRUCTION

unless an author artifact is later recovered. It must not be labelled:

    AUTHOR-ARTIFACT REPRODUCTION.

## 8. Effect on current blockers

This bounded search does NOT change:
    CORRECTNESS_GATE = BLOCKED
    BASELINE_CORRECTNESS = PENDING.

It does change the exact route to clearing them:

1. Step2 candidate recovery canary still must be executed independently.
2. Step3 must print and persist every exact runtime parameter needed by Turns4-17 rather than infer unpublished Aung settings.
3. Baseline correctness must be established on an explicitly documented source-faithful reconstruction unless an author implementation later appears.
4. Comparisons with Table2 must state the residual provenance mismatch.

## 9. Audit consequence

The absence of a locatable raw author artifact in the bounded current search means an independent raw audit of the published implementation cannot presently be performed.

This is a reproducibility obstruction, not evidence that the paper's reported benchmark or correctness is false.

For the paper-candidate workflow, AUDIT_GATE should be treated as BLOCKED until either:
- author/source artifact becomes available, or
- our own source-faithful baseline/candidate implementation is frozen with complete provenance and independently audited as such.

## Verdict

FAIL_CURRENT_PUBLIC_AUTHOR_ARTIFACT_RECOVERY
PASS_PUBLIC_HELIB_COMMIT_AND_BITS400_PROVENANCE
PASS_REPRODUCIBILITY_GAP_IDENTIFICATION

AUNG_AUTHOR_IMPLEMENTATION:
    NOT_LOCATED_IN_BOUNDED_CURRENT_SEARCH

AUNG_EXACT_SKHWT:
    UNKNOWN

AUNG_EXACT_KS_COLUMNS:
    UNKNOWN

AUNG_EXACT_BUILD_CONFIGURATION:
    UNKNOWN

BASELINE_REPRODUCTION_CLASS:
    SOURCE_FAITHFUL_RECONSTRUCTION_ONLY

NATIVE_STEP2:
    NOT_EXECUTED

CORRECTNESS_GATE:
    BLOCKED

BASELINE_CORRECTNESS:
    PENDING

AUDIT_GATE:
    BLOCKED

NOVELTY_STATUS:
    PREFLIGHT

SECURITY_GATE:
    PENDING

VALUE_GATE:
    PENDING

PAPER_READINESS:
    NOT_READY

## Reopen condition

Reopen this finding immediately if any author repository, institutional archive, supplementary package, source tarball, artifact-evaluation bundle, or direct author-provided code becomes available.

Do not convert the bounded-search result into the universal claim that no implementation exists.

## Next decisive test

The mandatory evidence-order action remains Step2 execution of the frozen revised recovery-only canary against pinned HElib with HELIB_DEBUG=ON.

After Step2 PASS, Step3 must record every exact runtime parameter instead of borrowing unpublished baseline assumptions. Baseline correctness should then use a fully documented source-faithful reconstruction and explicitly distinguish it from author-artifact reproduction.