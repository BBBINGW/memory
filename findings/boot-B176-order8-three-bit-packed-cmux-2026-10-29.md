# BOOT B176 Order-8 Three-Bit Packed-CMux Whole-Cost Gate

Date: 2026-10-29  
Session: 密码学 11.0, Research Turn 9/25  
B176 substantive turn: 7/12

## Hypothesis

`B176-H7-ORDER8-THREE-BIT-PACKED-CMUX`: represent the dynamic root index as three RGSW bits and use a packed CMux tree to select CRT coordinates at acceptable whole cost, replacing GROUPED plus pointwise multiplication.

The screen gives the candidate free CRT/DFT branch values, root-index extraction, three replicated RGSW index bits, an RGSW zero flag, and all RLWE-to-RGSW/CBS conversion. This isolates the most favorable downstream selection cost.

## Packed count

A three-bit eight-way tree has seven logical CMux nodes and depth three. Since every node on a layer uses the same selector bit, an optimistic interleaved SIMD layout batches each layer into one external product. The nonzero-root path therefore needs three packed external products; supporting the zero case adds one final CMux.

```text
LOGICAL_CMUX_NODES: 7
PACKED_EXTERNAL_PRODUCTS_NONZERO_ROOTS: 3
ZERO_FLAG_FINAL_CMUX: 1
PACKED_EXTERNAL_PRODUCTS_FULL_DOMAIN: 4
FULL_DOMAIN_DEPTH: 4
```

Compared with the current 26 encrypted multiplications through the B175 output, the full-domain optimistic path has 21 basis operations plus four external products, an abstract reduction of one operation. This is a real count signal, but an SI ct-ct and an RGSW external product are not equal runtime units.

## Whole-cost and noise boundary

Four full external products require at least `8l` gadget-row accumulations. The four dynamic RGSW selectors themselves contain another `8l` RLWE rows, versus one RLWE GROUPED ciphertext. No operation, key/ciphertext-memory, or runtime advantage follows.

The four-layer selected-path error has the form

```text
e_final = e_selected + sum_{t=1}^4 eta_t + e_linear.
```

If CRT branches remain near LT8 required bits 577, the 71-bit margin to the positive threshold 648 makes downstream fixed-Q correctness plausible but unestablished. The missing dominant cost is conversion of encrypted `y in {0} union mu_8` into three binary RGSW bits plus a zero flag, requiring standard circuit/multi-bit functional bootstrapping and BSK/KSK/PFKSK-equivalent material. Oracle-provided selectors would only revalidate standard CMux functionality and do not warrant native work.

## Result

```text
CLASSIFICATION: FAIL
RESULT: FAIL_ORDER8_THREE_BIT_CMUX_WHOLE_COST_AND_NOVELTY
EVIDENCE: OPTIMISTIC_PACKED_CMUX_COUNT / GADGET_ROW_AND_SELECTOR_MATERIAL_LOWER_BOUND / STANDARD_SCHEME_SWITCH_PRIOR_ART
PACKED_LEVEL_BATCHING: PASS
PACKED_EXTERNAL_PRODUCTS_FULL_DOMAIN: 4
ABSTRACT_COUNT_SIGNAL: PASS_MINUS_ONE_OPERATION
FIXED_Q_DOWNSTREAM: UNCLEAR_PLAUSIBLE_NOT_RUN
DETERMINISTIC_16_BIT_CERTIFICATE: NOT_ESTABLISHED
OPERATION_ADVANTAGE: NOT_ESTABLISHED
KEY/CIPHERTEXT_MEMORY_ADVANTAGE: NO
RUNTIME: NOT_MEASURED
REAL_CONVERSION_COST: DOMINANT_AND_NOT_FREE
NATIVE_EXECUTION: NOT_WARRANTED
STANDALONE_NOVELTY: FAIL
RESEARCH_VALUE_CEILING: ENGINEERING_REPAIR_ONLY
```

This parks only standard root-index bits plus packed CMux and standard scheme switching as the B158 redesign. A new multi-output conversion, compressed selector representation, or new provable key/noise/operation tradeoff remains outside the result.

`AI_PROVISIONAL_CHOICE: PARK B176-H7; PARK STANDARD ORDER8 CMUX/SCHEME-SWITCH FAMILY.`

Next test: `B176-SOFT-BUDGET-8-VALUE-OF-INFORMATION-AND-REPRIORITIZATION-GATE`.
