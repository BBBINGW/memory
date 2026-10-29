# BOOT B176 Materialized Keyed RLWE-to-RGSW Whole-Cost Gate

Date: 2026-10-29  
Session: 密码学 11.0, Research Turn 6/25  
B176 substantive turn: 4/12

## Hypothesis

`B176-H4-MATERIALIZED-KEYED-RLWE-TO-RGSW`: use a dedicated `RGSW_s(-s)` conversion key to materialize `RGSW(GROUPED)`, then external-product it with LT8, seeking at least 16 required bits of fixed-Q recovery at acceptable whole cost.

## Static recurrence

Granting the scale bridge for free, let `phi_s(c)=mu+e_G`, `c_j=g_j*c`, and let `eta_j` aggregate conversion-key row, decomposition, and rounding error. The converted upper rows satisfy

```text
phi_s(U_j) = -g_j*mu*s - g_j*e_G*s + eta_j.
```

For LT8 phase `M_L+e_L`, the final external-product error is

```text
E_out = mu*e_L + M_L*e_G + e_L*e_G + sum_j(q_j*eta_j) + E_dec/scale.
```

The conversion preserves all ordinary product cross terms and adds conversion-key error. It does not refresh or contract the existing GROUPED residual. Since GROUPED is already at required bits 633 and the positive output threshold is 648, no deterministic 16-bit recovery invariant is available.

## Whole-cost lower bound

For gadget length `l`, the materialized route needs a `2l`-row `RGSW_s(-s)` key, a transient `2l`-row selector, `l` full external products to build its upper rows, one further external product to use it, and idealized `2l(l+1)` row accumulations, before scale conversion and bookkeeping. Streaming removes transient storage but not the internal external products.

## Result

```text
CLASSIFICATION: FAIL
RESULT: FAIL_STANDARD_MATERIALIZED_KEYED_CONVERSION_WHOLE_COST
EVIDENCE: EXACT_PHASE_ERROR_RECURRENCE / OPTIMISTIC_SCALE_GRANT / STRUCTURAL_WHOLE_COST_LOWER_BOUND / PRIMARY_LITERATURE_BOUNDARY
SCALE_BRIDGE: NOT_FREE / GRANTED_FREE_FOR_SCREEN
DETERMINISTIC_16_BIT_RECOVERY: FAIL_NO_INVARIANT
MATERIALIZED_ONLINE_COST: FAIL
KEY_MEMORY_ADVANTAGE: NO
RUNTIME: NOT_MEASURED
NATIVE_FIXED_CASE_BEHAVIOR: UNCLEAR_NOT_RUN
DFR: NOT_ESTABLISHED
SECURITY_CLOSURE: NOT_ESTABLISHED
NOVELTY: FAIL_AS_STANDARD_MECHANISM
RESEARCH_VALUE_CEILING: ENGINEERING_REPAIR_ONLY
```

This parks only the standard materialized conversion route. Fused direct merge, refreshed conversion, a new contraction law, instance-specific behavior, and a new provable key/noise/operation tradeoff remain outside this result.

`AI_PROVISIONAL_CHOICE: PARK STANDARD MATERIALIZED KEYED CONVERSION; DO_NOT_NATIVE_TEST.`

Next test: `B176-FUSED-RGSW-MINUS-S-DIRECT-MERGE-SCALE-AWARE-GATE`.
