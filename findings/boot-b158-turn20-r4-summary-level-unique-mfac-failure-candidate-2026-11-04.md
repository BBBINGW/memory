# BOOT / B158 — Research Turn 20/25
## R4 summary-level unique mfac failure candidate

Date: 2026-11-04
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Candidate: rmfe-subring-envelope-single-multkey-v1
Phase: VALUE_GATE

## Authority and task isolation

Primary GitHub Notes directory/list access is available, but read_repo_file currently returns empty objects for existing files. Turn 19 durable finding was nevertheless verified present by repository listing:
findings/boot-b158-turn19-r4-mfac-context-assertion-static-repair-2026-11-04.md
blob 0330b0094289bb9c70a320b8d4d87ef78f4f90e1.

Current Research Orchestrator browser status:
- local research authority HEALTHY at BBBINGW/memory HEAD 9bec54259dc7686e0afc66501d2b6beff9d56c88;
- R4 task ID still BOOT-B158-STEP2-REPAIRED-SMALL-CANARY-20261104-R4;
- Codex/native status IDLE;
- R4 native stdout path exists locally but its contents are not exposed through the available read-only browser connector.

R4 is immutable / DO_NOT_RERUN.
No new native task was launched this turn.

## Primary hypothesis

Among the fields actually represented in the supplied R4 EXPECTED/OBSERVED context summary, mfac is the only field capable of explaining FIRST_FAILURE_STAGE=context_parameters without contradicting an already displayed observed value.

This is a summary-level uniqueness result, not a claim that the raw R4 Boolean predicate has been observed.

## R4 supplied context summary

EXPECTED:
m=32768
phi=16384
ord=8192
slots=2
e=5
ePrime=2
q=3126
divisor=25
effective=4
temp=625
mfac=1

OBSERVED:
m=32768
phi=16384
ord=8192
slots=2
e=5
ePrime=2
q=3126
temp=625

Every displayed OBSERVED value equals EXPECTED exactly.

## Derived-field elimination

Pinned p=5,r=1.

From observed ePrime=2:

    divisor = p^ePrime = 5^2 = 25.

From observed e=5,ePrime=2,r=1:

    effective = e-ePrime+r = 5-2+1 = 4.

Then:

    temp = p^effective = 5^4 = 625,

which is itself observed.

Therefore divisor/effective cannot constitute an independent repaired-profile mismatch if the canary derives them from the observed context as required by the pinned HElib contract.

All remaining discrete fields are already shown matching.

Thus, among the explicitly summarized contract fields, only:

    mfac

remains as a candidate mismatch.

## mfac source semantics

Pinned HElib:
homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1.

src/PAlgebra.cpp blob:
b24f9de1da66d0aaac8d00a3cf10358a47553daf.

PAlgebra computes:

    normBnd = 1.0;
    for each distinct prime factor u of m:
        normBnd *= 2*cotan(PI/(2*u))/u;

and:

    cotan(double x) = 1/tan(x).

For m=32768=2^15, mathematical normBnd is exactly 1, but the implementation is floating and does not guarantee bit-exact 1.0.

Turn 19 same-expression Linux reproduction:
    1.0000000000000002
    0x1.0000000000001p+0
    difference = 2^-52.

Hence exact mfac==1 is an invalid portable runtime assertion while having negligible scientific capacity effect.

## Evidence boundary

PASS_SUMMARY_LEVEL_UNIQUE_MFAC_FAILURE_CANDIDATE

The following stronger claim is NOT established:

    R4_EXIT_PREDICATE == (mfac != 1.0).

Why not:
- raw R4 canary.cpp/result.json/native stdout are not available through GitHub Notes, Library, prior conversation retrieval, connected GitHub search, or the read-only Browser context;
- the canary could contain hidden context conjuncts omitted from its compact EXPECTED/OBSERVED diagnostic.

Therefore exact R4 root cause remains unverified.

## Successor admission contract

A new native successor is NOT scientifically admissible merely from this summary-level inference.

Before EXECUTE, require one of:

A. RAW_PREDICATE_VERIFIED
- materialize/read immutable R4 canary.cpp/result.json/stdout;
- identify exit-code-3 Boolean predicate;
- verify it is mfac exact-literal or another harness-only derived-field assertion.

or, if raw R4 artifacts become permanently unrecoverable:

B. SOURCE-DERIVED REPLACEMENT WITH EXPLICIT PROVENANCE LOSS
- construct a new canary from the repaired authoritative contract rather than claiming it is a minimal R4 patch;
- use a new task ID and clearly state that exact R4 source-diff lineage could not be verified;
- treat the new canary as a fresh Step-2 implementation, not as a rerun or patch of R4;
- independently audit its source before interpreting native results.

Preferred route is A.

## Minimal valid mfac rule if route A confirms the issue

Record:
- decimal with max_digits10;
- std::hexfloat value;
- actual getNormBnd() runtime result.

For power-of-two m, compare to mathematical 1 using a frozen ULP/tolerance rule, e.g. <=8 ulp at 1.0, and use the runtime value itself in all capacity/noise calculations.

Do not assert exact ==1.0.

## Scientific consequence

R4 remains:
UNCLEAR
FAIL_CONTEXT_ASSERTION / FULL_DIRTY_LIFT_UNTESTED.

Candidate remains ACTIVE.
CORRECTNESS_GATE remains BLOCKED.
VALUE conclusions remain conditional.
No security/DFR/benchmarking may advance.

## Next decisive test

Recover exact R4 raw predicate if possible. If unavailable after all connected-source routes, the next admissible move is a fresh-provenance Step-2 canary implementation from the repaired contract, explicitly not represented as R4 minimal patch lineage.

No native task is launched by this finding.
