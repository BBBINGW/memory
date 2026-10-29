# BOOT B176 Factorized Pre-LT Twist Static Ceiling

Date: 2026-10-29  
Session: 密码学 11.0, Research Turn 3/25  
B176 candidate-family substantive turn: 1/12  
TRACK_ID: BOOT  
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Primary hypothesis

`B176-H1-FACTORIZED-PRE-LT-TWIST`

Move the factorized selector to the lower-noise half-basis side before ParallelLT:

```text
P*  = SI(SI(SI(P_H,F0),F1),F2)
OUT = ParallelLT(P*)
```

The intended structural benefit was to avoid the killed high-noise `SI(LT8,GROUPED)` interface while retaining the projected 27 ct-ct full count.

## Cheapest decisive test

Use the most favorable audited required-bit trace compatible with the current B174/B175 lineage and fixed parameters, then apply the best observed ParallelLT increment. Failure occurs if the optimistic output still exceeds the positive-budget ceiling of 648 required bits.

## Result

```text
CLASSIFICATION: FAIL
RESULT: FAIL_TWISTED_BABY_BASIS_STATIC_CEILING
EVIDENCE: STATIC_ALGEBRA + TRACE_CALIBRATED_OPTIMISTIC_SCREEN
PLAINTEXT_IDENTITY: PASS
OPERATION_COUNT_CEILING: PASS
FIXED_Q_FEASIBILITY: FAIL
NATIVE_CORRECTNESS: NOT_RUN / NOT_ESTABLISHED
NOVELTY: NOT_ESTABLISHED
```

The plaintext identity is valid. Under the most favorable 29-bit observed SI increment:

```text
r(P_H)=544
r(F0,F1,F2)=541,572,604
r0=max(544,541)+29=573
r1=max(573,572)+29=602
r2=max(602,604)+29=633
```

The twisted basis therefore retains only 15 bits before ParallelLT. The best observed current-lineage ParallelLT increment is 31 bits:

```text
r_OUT = 633 + 31 = 664 > 648
```

This construction merely moves the same conditional 16-required-bit deficit to the ParallelLT output and introduces no mechanism that recovers it.

The count ceiling passes:

```text
basis ct-ct: 21
Y^2,Y^4: 2
factor twists: 3
through output: 26
projected with leading: 27
```

## Scope and decision

This kills only the fixed-parameter, current-lineage factorized pre-LT twist under current ParallelLT. It is not an impossibility theorem for every twisted representation or structured selector.

`AI_PROVISIONAL_CHOICE: PARK B176-H1; do not spend native execution on it.`

The next cheapest decisive test is `B176-DUAL-LINEAGE-TYPED-MERGE-GATE`: a Research-GPT-native typed derivation testing whether separate LT/selector RLWE lineages plus a cross-lineage tensor merge remove the input-dependent tensor/reference term or merely transfer it into the `1,s_A,s_B,s_As_B` representation and cross-key conversion.

No Codex task, native experiment, parameter change, or simple tuning rescue occurred.

