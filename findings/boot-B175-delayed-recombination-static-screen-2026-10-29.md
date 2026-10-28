# BOOT B175 Delayed-Recombination Static Screen

Date: 2026-10-29 (Asia/Hong_Kong)  
Session: Cryptography 10.0, Research Turn 12/25  
Track: BOOT  
Active subline: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Result

- PRIMARY_HYPOTHESIS: FAIL_SCREEN
- ACTUAL_NATIVE_FEASIBILITY: UNCLEAR_NOT_RUN
- COST_SCREEN: FAIL
- SCALE_AWARE_SUFFICIENT_SCREEN: FAIL
- NOVELTY_SCREEN: FAIL_AS_NEW_MECHANISM
- VALIDATED_REDESIGN_CANDIDATE: NONE
- PENDING_PI_DECISION: BOOT-DECISION-001
- B176: NOT_AUTHORIZED

Explicit eight-branch delayed recombination avoids materializing the low-headroom GROUPED ciphertext before pointwise multiplication and therefore changes the multiplication-time geometry. However, it fails the optimistic fixed-`Q` scale-aware sufficient screen and increases the ciphertext-ciphertext count from 26 to at least 34. Its algebraic identity is a distributive/binary-selector expansion rather than a new primitive.

No partial products were executed. Their actual residuals remain unknown, so this is a static screen rather than a native impossibility result.

## Algebraic form

For public one-hot masks `M_i[j] = 1` when `j mod 8 = i`, the delayed form is

```text
S = sum_{i=0}^7 (M_i * L) * Y^i,
```

where `L` is LT8 and `Y` encrypts `y=x^8192`. With the existing bit masks `c_b` and complements `d_b`, the masks are the eight products choosing one of `c_b` or `d_b` for `b=0,1,2`. They are disjoint and sum to one.

The B174 factors are

```text
F0 = d0 + c0*Y
F1 = d1 + c1*Y^2
F2 = d2 + c2*Y^4,
```

and

```text
sum_i M_i*Y^i = F0*F1*F2.
```

Thus the eight-branch form is the distributive expansion of the existing factorized selector, not a new algebraic mechanism.

## Power dependency and operation count

Already available:

```text
Y^0 = 1                    public
Y^1 = Y                    existing ciphertext
Y^2 = SI(Y,Y)              one existing ct-ct
Y^4 = SI(Y^2,Y^2)          one existing ct-ct
```

One minimum graph for the missing independent powers is

```text
Y^3 = SI(Y,Y^2)
Y^5 = SI(Y,Y^4)
Y^6 = SI(Y^2,Y^4)
Y^7 = SI(Y^3,Y^4),
```

requiring four additional ciphertext-ciphertext multiplications. Seven nonconstant branch products require seven further ciphertext-ciphertext multiplications. The minimum total becomes

```text
checkpoint/basis = 21
existing Y^2,Y^4 = 2
missing Y^3,Y^5,Y^6,Y^7 = 4
branch products P1..P7 = 7
total = 34 ct-ct.
```

This is eight more than the current 26 operations through pointwise, a 30.8% increase. Including the unexecuted leading multiplication compares 35 against the current projected full skeleton of 27.

## Scale-aware optimistic screen

At L18, let `kappa=(-Q mod T)^-1=44421` and `sigma_Y=sigma_L=43352`. The derived power scales for `Y^i`, `i=1..7`, are

```text
[43352, 27275, 22359, 35478, 22185, 38262, 43178].
```

Assuming scale-one masks, branch scales for `P_0..P_7` are

```text
[43352, 27275, 22359, 35478, 22185, 38262, 43178, 30059].
```

Successive branch scales differ by the factor `-16 mod 65537`, so the simple accumulation screen `max_i(r_i)+3<=648` is inapplicable until scales are aligned.

For an optimistic ceiling, the audit grants all of the following favorable assumptions:

- every new SI multiplication adds only the smallest increment seen in B175, 29 required bits;
- one-hot masks add zero bits;
- no unmeasured partial residual is treated as native evidence.

This produces the optimistic branch vector

```text
[577,606,606,613,615,644,644,644].
```

If scales were free and already equal, the eight-term accumulation bound would be 647, leaving one bit of margin. Exact finite-field scale alignment removes that margin. The best target scales are 30059 or 35478. At target 30059, centered public alignment multipliers are

```text
[4096,-256,16,-1,-4096,256,-16,1],
```

with bit increments `[12,8,4,0,12,8,4,0]`. The aligned optimistic branch vector is

```text
[589,614,610,613,627,652,648,644].
```

Therefore

```text
max_i(r_i_aligned) + 3 = 655 > 648.
```

Even with zero mask cost, a common effective SI increment of at most 25 bits is required to pass. All five SI multiplications observed in B175 add 29--31 bits.

## Low-count endpoint

Keeping the factorized form avoids the four missing powers and seven branch products, preserving the 26-operation count, but it is the original endpoint. Under the same optimistic 29-bit recurrence:

```text
r(L*F0)       = 606
r(L*F0*F1)    = 635
r(L*F0*F1*F2) = 664.
```

Thus the low-count endpoint fails the noise screen, while the explicit eight-branch endpoint fails both count and scale-aware screens.

## Scientific boundary

Established:

- static sufficient screen: FAIL;
- operation-count screen: FAIL;
- novelty as a new algebraic mechanism: FAIL.

Not established:

- actual native partial-product residuals;
- possible cancellation;
- the Pareto frontier of hybrid groupings;
- a general representation impossibility theorem.

Obtaining native residuals would require new instrumentation and execution and is not authorized.

## Next no-regret task

Enumerate hybrid selector circuits between the three-step factorized form and eight-branch explicit form. Build the exact Pareto frontier in

```text
(ct-ct count, serial SI depth, scale-alignment burden)
```

and test whether any circuit has count below 34, serial depth below three, and does not materialize GROUPED before multiplication. This remains an algebraic static screen and does not authorize implementation or route selection.
