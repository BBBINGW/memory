# BOOT / B158_OVERALL — Turn 14/25 — Single-limb gateway source-interface gate

Date: 2026-11-11. Candidate: boot-b158-single-limb-sparse-gateway-composite-v1. Phase: CORRECTNESS_GATE. This is a SOURCE-INTERFACE audit, NOT a native correctness result. This finding is supplementary and does NOT supersede the verified local Git authority at 3ed0c0ab5907b7c8d4e5fa1501064428ce7d462f, which was not mounted in this runtime.

## Pre-registration
QUESTION: Does unmodified OpenFHE source support the proposed q0-only h32 sparse switch and post-lift raise switch, or must candidate-native interfaces be explicitly implemented and validated before a full-LUT correctness claim?
CURRENT_BELIEF: The public baseline sparse switch uses the full composite bottom basis and is not directly a q0-only gateway.
CHEAPEST_DECISIVE_TEST: inspect public source's modulus-raise and sparse-key-switch entry points and assert the concrete bottom-basis sizing and key edges. No native build available here.
IF_PASS: if q0-only keys/params and post-lift switch are fully implemented, advance to native full-packed candidate canary with q0/q1/tower/scale instrumentation.
IF_FAIL: if a candidate implementation simply calls the baseline two-limb sparse switch at q0, mark SOURCE_INTERFACE_FAIL and park unless one bounded explicit source-interface repair exists.
IF_UNCLEAR: keep candidate ACTIVE, CORRECTNESS_PENDING, without claiming compilation or success; require exact-tree source and binary access before interpreting a full-LUT test.
WHICH_PAPER_GATE_CHANGES: source feasibility prerequisite of CORRECTNESS_GATE.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: removes any justification to treat baseline UnitTestSparseKS as validation of the candidate gateway's Ql={q0} key edge; requires explicit one-limb params/key and raise switch validation.

## Evidence and finding
Public OpenFHE 1.6.0 ckksrns-fhe.cpp program listing (https://openfhe-development.readthedocs.io/en/latest/api/program_listing_file_pke_lib_scheme_ckksrns_ckksrns-fhe.cpp.html), lines 4236-4267: baseline ModRaiseInPlace calls KeySwitchSparse before raising and uses exact composite basis extension for degree>1; then calls KeySwitchInPlace after raising. Lines 4275-4303: ExtendSparseKSToP switches single-limb via SwitchModulus only when sizeQl==1; otherwise uses exact multi-limb SwitchCRTBasis. Lines 4352-4389: sparse key generated on params Ql*P' with sizeQl=GetSparseKSParamsQ size. Lines 4392-4450: KeySwitchSparse clones precisely sizeQl bottom towers and switches QlP' -> Ql. Thus, a degree-2 baseline parameter context cannot be presumed to have a dedicated Ql={q0} q0-only sparse switching key merely because the same source has a one-limb branch. The candidate needs a distinct source-backed parameter/key edge in the degree-2 context and a separate raised-key edge; baseline UnitTestSparseKS validates only its own supplied parameters.

Public COMPOSITE_SCALING.md / CKKS_FUNCTIONAL_BOOTSTRAPING.md explicitly describe baseline >60-bit first-modulus using h=64,K=28 vs <=60-bit using h=32,K=16. This verifies the target regime but NOT its attainability under the proposed gateway.

OpenFHE candidate source/binary, configured server and exact PR #1381 test artifacts were not accessible in this runtime. A filesystem inspection found no mounted candidate OpenFHE tree or verified local BBBINGW/memory clone. The user-supplied verified local HEAD is an authority excerpt, not a current runtime Git verification. No native correctness or noise measurements were performed; epsilon_L/H, q1-restored period, ApproxModDown/R normalization, final 8-bit LUT errors, full construction and security remain UNKNOWN/PENDING.

## Decision
Verdict: SOURCE_INTERFACE_DEPENDENCY_CONFIRMED / CANDIDATE_NATIVE_CORRECTNESS_UNCLEAR. Keep only this candidate ACTIVE/PENDING. NEXT: obtain exact PR #1381 candidate source + runnable binary, first verify degree-2 context contains explicit q0-only Ql/P' tables, low key edge and post-lift raise key edge, then run pre-registered full-packed canary with tower/metadata/epsilon logging. If these edges absent, a single bounded repair is allowed by protocol; no repeated local patches. No performance claim, no novelty CLEAR.

ELIMINATED_UNCERTAINTY: whether stock degree-2 sparse encapsulation's one-limb code path alone establishes the candidate low switch: NO. DECISION_CHANGED: YES — baseline one-limb regression is calibration only; candidate-native source/interface checks are mandatory before consuming any full-LUT result.
