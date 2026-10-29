# BOOT B176 Ordinary Dual-Lineage Typed-Merge Gate

Date: 2026-10-29  
Session: 密码学 11.0, Research Turn 4/25  
B176 substantive turn: 2/12

## Hypothesis

`B176-H2-DUAL-LINEAGE-TYPED-MERGE`: keep LT8 and the selector under independent RLWE secrets/lineages, then use an ordinary tensor product and cross-secret relinearization to change the B175 tensor/reference geometry and recover at least 16 required bits at fixed Q.

## Typed derivation

For

```text
A=(a0,a1), a0+a1*sA=MA+eA
B=(b0,b1), b0+b1*sB=MB+eB
```

the ordinary cross-lineage tensor has basis `(1,sA,sB,sA*sB)` and phase

```text
(MA+eA)(MB+eB) = MA*MB + MA*eB + MB*eA + eA*eB.
```

Componentwise scale-invariant rounding adds the corresponding `(1,sA,sB,sA*sB)` rounding phase but does not remove any message-error cross term. Ordinary cross-secret evaluation keys act only after this tensor phase exists; they cannot deterministically cancel it for arbitrary runtime operands and add their own conversion error.

## Result

```text
CLASSIFICATION: FAIL
RESULT: FAIL_ORDINARY_DUAL_LINEAGE_TYPED_MERGE
EVIDENCE: STATIC_TYPED_COMPONENT_AND_PHASE_DERIVATION / OPTIMISTIC_INTERFACE_COST_SCREEN
PLAINTEXT_PRODUCT_CORRECTNESS: PASS_ALGEBRAIC
DETERMINISTIC_FIXED_Q_16_BIT_RECOVERY: FAIL_NO_MECHANISM
CT_CT_REDUCTION: NO
NATIVE_EXECUTION: NOT_RUN
NOVELTY: NOT_ESTABLISHED
```

This kills only independent RLWE lineages plus ordinary tensoring and ordinary ciphertext-independent cross-key conversion. It does not rule out a correlated tensor key with a new cancellation invariant, a different ciphertext/multiplication law, refreshed GGSW/RGSW conversion, or distribution-specific behavior.

`AI_PROVISIONAL_CHOICE: PARK B176-H2; DO_NOT_NATIVE_TEST.`

Next test: `B176-STANDARD-RLWE-TO-GGSW-PUBLIC-LIFT-GATE`.

