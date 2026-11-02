# BOOT / B158 — Research Turn 9/25 — Aung bits=400 / w=512 parameter-binding gate

Date: 2026-11-03 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613 / PRE-TAG + POST-DIVIDE late aggregation
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1
Primary paper: Aung et al., IACR ePrint 2025/350 / PKC 2025

## Read-before-write / provenance

GitHub Notes read remains degraded for existing findings. Current durable state was recovered from
BBBINGW/memory at verified HEAD:

    9d5da380bfe82d0e4fa4c91b9a937702043fe2f8

Immediate relevant findings:
- Turn8 exact-L1 guard local-capacity floor:
  findings/boot-RMFE-postdivide-turn8-exact-l1-guard-capacity-floor-gate-2026-11-02.md
  blob 8d9d0ea97adabebe80e4bc0b3e7f93b1477c6d98
- R4 native baseline-timer independent audit:
  findings/boot-RMFE-R4-baseline-timer-result-independent-audit-2026-11-01.md
  blob 06a07b1a2d13c7c9d3cd0825e0b4f068049c913f
- historical p=5,w=512 commutation-boundary gate:
  findings/boot-RMFE-p5w512-commutation-boundary-2026-10-29.md
  blob de94070931e50d1a35404686c4b6e70046f05a94

The target path was absent before write.

## Why this turn is necessary

Turn8 derived:

    shared-reconstruction capacity >= 354.9156 bits

under a HElib context with:

    bits=400.

The current paper candidate is described by the paper-facing parameters:

    m=32768
    p=5
    w=512
    k=5.

A hidden parameter-binding error would invalidate Turn8 if:
- paper parameter w=512 were actually HElib secret-key Hamming weight;
- the p=5,w=512 Table-2 experiment used a different modulus-chain bits value;
- or bits=400 were merely a historical local harness setting rather than the published baseline.

This turn audits only that binding.

## Closest prior art / exact delta

Closest prior is Aung et al.'s published implementation description and Table 2.

No novelty claim is added.

Exact delta:
bind the Turn8 HElib-specific parameter bits=400 to the primary source-faithful Aung row and disambiguate
Aung's w from HElib secret-key-weight notation.

## Primary hypothesis

Aung's published p=5,m=32768,w=512,k=5 Corr./TnM experiment is initialized under the paper-wide:

    HElib bits = 400

configuration.

Furthermore:

    w = 512

in the paper denotes RMFE extension dimension, not HElib secret-key Hamming weight.

Therefore Turn8's bits=400 reconstruction-capacity floor is genuinely attached to the primary paper
baseline rather than to a local-only timer harness.

## Falsifier

FAIL if the primary source shows any of:
1. Table 2 uses a bits value different from 400;
2. bits=400 is scoped only to another experiment family;
3. w=512 is a secret-key weight or modulus-chain parameter;
4. the p=5,w=512 Corr./TnM row is not part of the same initialization described in §6.1.

## Minimal decisive test

Read the primary source's:
- §5.3 definition and use of w;
- §6.1 Implementation Details / Initialisation;
- Table 1 parameter labels;
- Table 2 caption and target Corr./TnM row.

No implementation benchmark or native execution is needed for this parameter-binding question.

## 1. Primary source explicitly fixes bits=400 for the experiments

Aung §6.1 "Implementation Details", subsection "Initialisation", states that:
- Phi_32768(X)=X^16384+1 is used with varying p;
- the encryption scheme is initialized using HElib;
- bits=400;
- the resulting maximum ciphertext bit-width is approximately 538–541 bits.

This statement precedes and governs the experimental workflow definitions and tables.

There is no separate bits value introduced for the p=5,w=512 row.

Therefore the published target experiment belongs to a HElib buildModChain setting whose requested
ciphertext-prime budget is:

    bits_HElib = 400.

## 2. Aung w is RMFE dimension, not secret-key Hamming weight

Aung §5.3 explicitly chooses w as an independent RMFE parameter.

The source describes:

    G' = GR(p^e, s w)

and discusses the cost of evaluating the recode map as depending on w.

Example 1 constructs RMFEs "of dimension w".

Table 1 labels the column/list explicitly as:

    RMFE Dimension, w

with choices:

    128, 256, 512, 1024.

Therefore:

    w_Aung = RMFE extension/dimension parameter.

It is NOT:
- HElib Context::skHwt;
- an HElib modulus-chain bit count;
- a ciphertext-prime width.

This resolves a potentially dangerous notation collision.

## 3. The target paper row is exactly m=32768,p=5,w=512

Aung Table 2 caption states:

    m=32768, p=5, w=512.

Its correction trace-and-merge column is:

    Corr. (TnM), k=5, #rec=1.

The reported stage capacities include:

    Initial       391.1
    SlotsToCtxts  369.2
    MultKey       346.5
    CtxtsToSlots  333.8
    DigitExtract  101.0
    Final         101.0

and the final latency is approximately:

    11.33 s.

Thus the exact primary candidate comparator row is unambiguously inside the bits=400 initialization.

## 4. Historical native R4 configuration matches the paper parameter binding

The durable R4 independent audit reports its native timer configuration as:

    p=5
    r=1
    m=32768
    w=512
    k=5
    bits=400.

Before Turn9, that configuration alone did not prove the paper itself used bits=400.

The primary-source audit now confirms that the relevant bits value was not an arbitrary local harness
choice.

Therefore:

    R4 bits=400
    ==
    Aung published experimental bits=400

at the parameter-name level.

This does NOT turn the unavailable R4 raw artifact into an independently verified benchmark; it only
closes parameter binding.

## 5. Turn8 capacity floor can be attached to the primary paper row

Turn8's source theorem was conditional on:

    bits_HElib = 400.

This condition is now satisfied by the primary source-faithful Aung row.

Hence its local reconstruction statement may be written as:

For the Aung Table-2 p=5,m=32768,w_RMFE=512,k=5 initialization, assuming the current candidate uses
the same pinned-HElib bits=400 context contract and the Turn5-7 exact-L1 hard bounds,

    capacity immediately after guarded shared reconstruction
    >= 354.9156 bits.

The phrase "source-faithful" is now justified for the bits parameter.

## 6. Important notation freeze

Future findings/specifications should distinguish:

    w_RMFE = 512

from HElib secret-key weight:

    skHwt

and from HElib modulus-chain target:

    bits_HElib = 400.

Do not write merely:

    w=512

inside a HElib-specific source/API formula when the symbol could be mistaken for secret-key Hamming
weight.

Recommended fixed parameter line:

    m=32768, p=5, r=1, w_RMFE=512, k=5, bits_HElib=400.

The bootstrapping secret-key Hamming weight should remain whatever the matched HElib/Aung
initialization actually selects and must not be silently identified with 512.

## 7. PDF provenance boundary

Primary source inspected:

    https://eprint.iacr.org/2025/350.pdf

Relevant extracted text:
- §5.3 around physical pp22–23 defines w as the RMFE dimension/independent variable;
- §6.1 around physical p23 says HElib initialized with bits=400;
- Table 1 labels "RMFE Dimension, w";
- Table 2 identifies m=32768,p=5,w=512 and Corr.(TnM),k=5.

A required PDF screenshot was attempted through the available web PDF screenshot backend but failed
with HTTP 403 from the ePrint PDF host. Text extraction from the same primary PDF succeeded.

Accordingly no visual-layout-only claim is made.

## Verdict

PASS_AUNG_BITS400_PRIMARY_SOURCE_BINDING
PASS_AUNG_W512_IS_RMFE_DIMENSION
PASS_TARGET_TABLE2_ROW_BITS400_SCOPE
PASS_TURN8_CAPACITY_FLOOR_PAPER_ROW_APPLICABILITY

REFINE_PARAMETER_NOTATION:
  w_RMFE=512
  bits_HElib=400
  skHwt=SEPARATE_PARAMETER

RECOVERY_CANARY:
  NOT_EXECUTED

NATIVE_EXECUTION:
  NOT_OBTAINED

CORRECTNESS_GATE:
  BLOCKED

BASELINE_CORRECTNESS:
  PENDING

NOVELTY_STATUS:
  PREFLIGHT

SECURITY_GATE:
  PENDING

VALUE_GATE:
  PENDING

AUDIT_GATE:
  PENDING

PAPER_READINESS:
  NOT_READY

## Scope boundary

This turn proves parameter binding only.

It does NOT prove:
- the exact native ctxt-prime product of Aung's machine beyond the pinned HElib buildModChain lower
  bound used in Turn8;
- native recovery correctness;
- source-faithful baseline end-to-end correctness;
- candidate native correctness;
- final capacity;
- DFR;
- matched value.

## Next decisive test

Mandatory evidence order remains blocked at Step2:

execute the frozen revised recovery-only canary unchanged against
homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1 with HELIB_DEBUG=ON.

After Step2 PASS, Step3 should pin and print the parameter tuple:

    m=32768
    p=5
    r=1
    w_RMFE=512
    k=5
    bits_HElib=400
    rcData.mvec=[32768]
    phi(m)=16384
    ord_m(p)=8192

before applying the Turns4-9 interface assertions.

No timing/performance inference is authorized.
