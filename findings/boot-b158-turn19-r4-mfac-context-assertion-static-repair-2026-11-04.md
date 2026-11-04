# BOOT / B158 — Research Turn 19/25
## R4 context-parameter failure: mfac exact-literal contract static repair

Date: 2026-11-04
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Candidate: rmfe-subring-envelope-single-multkey-v1
Phase: VALUE_GATE

## Authority / task isolation

GitHub Notes directory access recovered at the beginning of this turn, but read_repo_file returned empty objects for existing files and the current R4 raw artifacts are not present in the Notes repository. The latest user-supplied verified local BBBINGW/memory authority remains HEAD 9bec54259dc7686e0afc66501d2b6beff9d56c88 with authenticated remote push pending.

R4 task:
BOOT-B158-STEP2-REPAIRED-SMALL-CANARY-20261104-R4
Origin: 密码学 27.0 Turn 14
R4 is immutable / DO_NOT_RERUN.
No new native task was launched in this turn.

R4 Codex summary reported:
FIRST_FAILURE_STAGE=context_parameters
EXPECTED=m=32768,phi=16384,ord=8192,slots=2,e=5,ePrime=2,q=3126,divisor=25,effective=4,temp=625,mfac=1
OBSERVED=m=32768,phi=16384,ord=8192,slots=2,e=5,ePrime=2,q=3126,temp=625

The raw result.json/stdout/stderr/diff/canary.cpp bytes are not mounted in this environment, so the exact failing Boolean predicate remains unobserved.

## Primary hypothesis

The R4 context_parameters failure can be explained by an invalid exact-literal contract for mfac=getNormBnd(): the mathematical power-of-two norm factor is 1, but pinned HElib computes it through floating libm arithmetic and is not required to produce bit-exact 1.0.

Falsifier:
- any displayed repaired integer/profile field differs from authority; or
- pinned HElib defines mfac by exact integer/rational arithmetic guaranteeing bit-exact 1.0; or
- R4 raw source proves a different failing predicate.

## Repaired integer/profile fields

Durable repaired oracle:
m=32768
phi(m)=16384
ord_m(5)=8192
slots=2
e_H=5
ePrime_H=2
q=5^5+1=3126
divisor=5^2=25
e_eff=e_H-ePrime_H+r=5-2+1=4
temp=5^4=625

Every field actually printed in R4 OBSERVED matches this oracle. divisor and effective are direct exact derivations from the printed e/ePrime and r=1.

Thus the supplied summary contains no demonstrated repaired integer/context mismatch.

## Pinned HElib mfac implementation

Pinned HElib:
homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

src/PAlgebra.cpp blob:
b24f9de1da66d0aaac8d00a3cf10358a47553daf

Relevant source:

    static double cotan(double x) { return 1 / tan(x); }

and PAlgebra initialization:

    normBnd = 1.0;
    for (long i : range(nfactors)) {
      long u = factors[i].a;
      normBnd *= 2.0L * cotan(PI / (2.0L * u)) / u;
    }

src/NumbTh.cpp blob:
5e60bcd951152673f8cad7acadd88d4772e91bb3

PI is stored as a long-double decimal constant.

For m=32768=2^15, factorization has one distinct prime u=2. Mathematically:

    mfac* = 2*cot(pi/4)/2 = 1.

But the implementation passes PI/(4) to cotan(double), which calls tan(double). The C++/libm contract does not guarantee tan(pi/4) is exactly 1.

## Cheap Linux reproduction

A tiny C++ reproduction of the pinned expression:

    const long double PI = <same HElib literal>;
    static double cotan(double x) { return 1/std::tan(x); }
    double mfac = 2.0L*cotan(PI/(2.0L*2))/2;

on the current Linux runtime produced:

    mfac = 1.0000000000000002
    hex  = 0x1.0000000000001p+0
    mfac == 1.0 -> false

Hence:

    mfac - 1 = 2^-52
    log2(mfac) ~= 3.203426503814917e-16 bits.

This is negligible for the source raw-capacity budget but decisive for an exact equality assertion.

This local reproduction is not a byte-level execution of the R4 remote binary and does not prove the remote value. It proves that exact mfac==1 is not a portable/source-valid context contract.

## Scientific result

PASS_STATIC_MFAC_LITERAL_CONTRACT_BUG

The repaired context oracle must distinguish:
1. exact discrete/profile fields, which may be asserted by exact equality;
2. derived floating implementation diagnostics such as mfac, which must be serialized and used as their actual runtime values, not compared to a mathematical ideal with exact ==.

Recommended successor context rule:

    mfac_runtime = context.getZMStar().getNormBnd();

Record it at full precision/hexfloat. For power-of-two m, verify a tolerant property such as:

    abs(mfac_runtime - 1) <= 8*ulp(1.0)

or an equivalently explicit small tolerance, and use mfac_runtime itself in any noise/capacity threshold.

Do not replace this with a loose scientific tolerance if raw R4 canary.cpp later proves a different failure.

## R4 classification consequence

The existing independent R4 classification remains:

    UNCLEAR
    FAIL_CONTEXT_ASSERTION / FULL_DIRTY_LIFT_UNTESTED

This turn strengthens the leading harness explanation but does not claim the exact R4 Boolean predicate has been read.

No full GR(625,d) dirty-lift evidence was reached.
No correction-map equality was reached.
No /25 native witness was reached.
No pre-raw Q/prime-set witness was reached.
No source-native critical/noise diagnostics were reached.
No TOTAL centered raw-L1 evidence was reached.

## Next decisive test

Before any successor native execution, obtain the R4 raw canary source/result artifacts and identify the exact exit-code-3 predicate.

If it is the mfac exact-literal check (or another purely formatting/derived-field assertion), repair only that predicate under a NEW task/provenance ID. The successor must serialize:
- builder inputs;
- exact e/ePrime/q/divisor/effective/temp;
- mfac full precision + hexfloat;
- exact pre-raw prime set and Q;
- PRG/tie policy;
- source-native raw L-infinity / centered-mod-q / correction / critical-value diagnostics;
- TOTAL centered raw-L1 as research diagnostic;
- complete GR(625,d) dirty coefficients;
- L0..L3 correction-input equality.

Still stop before Algorithm4/security/DFR/benchmarking.

If raw R4 source shows a different genuine profile mismatch, this static mfac repair is not sufficient and the first failing interface must be reopened instead.

## Gate state

CORRECTNESS_GATE: BLOCKED
SECURITY_GATE: PENDING
VALUE_GATE: PENDING
AUDIT_GATE: PENDING
BASELINE_CORRECTNESS: BLOCKED
NOVELTY_STATUS: PREFLIGHT
PAPER_READINESS: NOT_READY
