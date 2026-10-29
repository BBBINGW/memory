# BOOT B176 Fused RGSW Signed-Secret Direct-Merge Gate

Date: 2026-10-29  
Session: 密码学 11.0, Research Turn 7/25  
B176 substantive turn: 5/12

## Hypothesis

`B176-H5-FUSED-RGSW-SIGNED-SECRET-DIRECT-MERGE`: avoid materializing `RGSW(GROUPED)` and use one `RGSW_s(-s)` external product to fold the raw tensor to degree one before scale-down, seeking a genuinely new multiplication law and the fixed-Q 16-bit recovery.

## Algebraic reduction

For LT8 `L=(b_L,a_L)`, GROUPED `C=(b_C,a_C)`, and `K=RGSW_s(-s)`, consider

```text
W = b_L*C + (a_L*C) boxdot K.
```

Its plaintext and scale identities hold, including the B175 scale `30059 mod 65537`. But the RGSW core reduces exactly to ordinary raw tensoring and early relinearization plus a zero-plaintext evaluation-key gauge term:

```text
W_RGSW = RelinRaw(Tensor(L,C)) + Z_K(a_L*C).
```

Thus the deterministic difference is only `SD1 o RelinRaw` versus `Relin o SD2`, not a new multiplication law. Degree-one scale-down improves the conservative quantization bound from at most 63 to at most 48 required bits, but B175 already shows that deleting quantization and relinearization bounds does not reduce the 664-required-bit aggregate tensor/reference term. The RGSW-specific residue is an uncontrolled gauge with no worst-case guarantee.

## Result

```text
CLASSIFICATION: FAIL
RESULT: FAIL_FUSED_RGSW_SPECIFIC_STRUCTURAL_RESCUE
EVIDENCE: EXACT_PHASE_AND_COMPONENT_REDUCTION / SCALE_AWARE_DEGREE_ONE_QUANTIZATION_BOUND / B175_SOURCE_LEVEL_ATTRIBUTION / PRIOR_GAUGE_GUARANTEE_FAILURE
RGSW_MULTIPLICATION_LAW_NEW: NO
DETERMINISTIC_16_BIT_MECHANISM: NOT_PRESENT
PLAINTEXT_IDENTITY: PASS
SCALE_IDENTITY: PASS
DEGREE_ONE_QUANTIZATION_BOUND: REQUIRED_BITS_LE_48
RGSW_GAUGE_GUARANTEE: FAIL
CANONICAL_EARLY_RELIN_NATIVE_BEHAVIOR: UNCLEAR_NOT_RUN
NATIVE_RGSW_FAILURE: NOT_CLAIMED
OPERATION_ADVANTAGE: NO
KEY_MEMORY_ADVANTAGE: NO
RUNTIME_ADVANTAGE: NOT_ESTABLISHED
SECURITY_CLOSURE: NOT_ESTABLISHED
STANDALONE_NOVELTY: FAIL
RESEARCH_VALUE_CEILING: ENGINEERING_REPAIR_ONLY
```

This does not prove that every canonical early-relinearize-before-rescale native schedule fails. It removes the proposed RGSW wrapper as a substantive structural B158 rescue; the remaining schedule-only possibility is an engineering repair outside the primary-innovation policy.

`AI_PROVISIONAL_CHOICE: PARK B176-H5; DO_NOT_EMIT CODEX TASK; PARK STANDARD EXTERNAL-PRODUCT REPAIR FAMILY.`

Next test: `B176-ORDER8-CRT-TRACE-INTERFACE-LINEARIZATION-GATE`.
