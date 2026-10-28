# BOOT B175 Public-Mask Convolution Screen

Date: 2026-10-29 (Asia/Hong_Kong)  
Session: Cryptography 10.0, Research Turn 14/25  
Track: BOOT  
Active subline: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Result

- CLASSIFICATION: UNCLEAR
- PRIMARY_HYPOTHESIS: NOT_ESTABLISHED
- MASK_ENCODING_RECONSTRUCTION: PASS
- EXACT_CONVOLUTION_ON_SAVED_ARRAYS: PASS
- FRONTIER_A: UNCLEAR_NOT_ELIMINATED
- FRONTIER_B: UNCLEAR_NOT_ELIMINATED
- FRONTIER_ELIMINATED: NONE
- VALIDATED_REDESIGN_CANDIDATE: NONE
- PENDING_PI_DECISION: BOOT-DECISION-001
- B176: NOT_AUTHORIZED

The saved B175 residual arrays are sufficient to reconstruct the exact Lattigo public-mask encoding and to evaluate mask convolution on the saved `LT8`, `GROUPED`, and failed `POINTWISE` operands. They are not sufficient to evaluate the decisive operands in either hybrid frontier. Therefore the hypothesis that the saved arrays alone eliminate at least one frontier is not established.

No Codex task, native experiment, B175 rerun, new case, parameter sweep, B176 action, or GitHub Notes action occurred in this turn.

## Exact encoding reconstruction

For `N=32768` and `T=65537`, the masks `c2`, `d2`, and `M0..M3` were reconstructed through the Lattigo v6.2.0 `RingT` encoding convention: slot placement through `permuteMatrix`, negacyclic INTT in `Z_T[X]/(X^N+1)`, plaintext scale one, and the `T^-1 mod Q` embedding used by vector-operand multiplication.

The reconstruction passes a full 32,768-slot NTT round trip and verifies

```text
c2 + d2 = 1
M0 + M1 + M2 + M3 = 1
Mi^2 = Mi
Mi*Mj = 0 for i != j.
```

The coefficient-domain masks are dense, not sparse binary polynomials. The reported centered norms are:

| Mask | Nonzero coefficients | Centered l_inf | Centered l1 |
| --- | ---: | ---: | ---: |
| c2 | 9 | 32768 | 214538 |
| d2 | 9 | 32768 | 214538 |
| each Mi | 7 | 30721 | 79086 |

## Exact convolution on saved operands

For the three saved complete coefficient-residual vectors, the exact output required bits after applying the public masks are:

| Saved operand | Original | c2 | d2 | M0 | M1 | M2 | M3 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| LT8 | 577 | 594 | 594 | 595 | 595 | 595 | 594 |
| GROUPED | 633 | 651 | 650 | 650 | 651 | 650 | 650 |
| failed POINTWISE | 664 | 665 | 665 | 665 | 665 | 665 | 665 |

Thus healthy `LT8` and `GROUPED` operands show a 17--18 required-bit increase. The one-bit increase on the already failed `POINTWISE` residual is a centered-modulus saturation/wraparound effect and is not evidence that masks generally cost one bit. The deterministic encoding carry is only about 15--18 coefficient bits; the dominant increase on the healthy saved operands comes from the lifted mask convolved with the residual.

This is operand-specific observed evidence, not a universal lower bound.

## Frontier B

The only exactly evaluable frontier branch is `d2*LT8`:

```text
LT8 required bits                  = 577
d2*LT8 masked required bits        = 594
scale-aligned d2*LT8 required bits = 610
```

The missing high branch is `c2*SI(LT8,Y^4)`. Its coefficient residual array is absent. The known low branch does not exceed the optimistic 615-bit high-branch model, so it does not consume Frontier B's final three-bit modeled output slack by itself. Residuals from other operands cannot legally substitute for the missing branch.

Result: `FRONTIER_B=UNCLEAR_NOT_ELIMINATED`.

## Frontier A

Frontier A requires full residual vectors for `Y`, `Y^2`, and the never-constructed `Y^3`, followed by the masked branches `M1*Y`, `M2*Y^2`, and `M3*Y^3`. B175 contains only maximum-residual summaries for the available powers, not their 32,768-entry residual arrays. Scale multipliers alone cannot provide a positive lower bound because coefficientwise terms may reinforce or cancel.

Result: `FRONTIER_A=UNCLEAR_NOT_ELIMINATED`.

## Evidence boundary

Deterministic evidence established this turn includes the exact mask polynomials and identities, their coefficient norms, exact convolution on the three saved operands, and the exact masked/aligned low branch of Frontier B.

The standard bound `||A e||_inf <= ||A||_1 ||e||_inf` permits roughly an 18-bit increase but is only an upper bound. It cannot prove that an unknown operand must exceed the three-to-four-bit frontier slack. Mask convolution depends on the complete coefficient arrangement, and the final SI multiplication additionally depends on ciphertext component lifts and `Q`-carry.

The empirical 17--18-bit mask cost is a strong negative warning, but not a formal elimination of either frontier.

## Minimum missing evidence

- Frontier A: complete coefficient residuals for `Y`, `Y^2`, `Y^3`; each masked branch; and the scale-matched `G01^E` sum.
- Frontier B: complete coefficient residual for `SI(LT8,Y^4)`; the masked high branch; and the scale-matched `A2(L)` sum.
- A final correctness conclusion would still require operand component state or the actual final SI multiplication.

## Next no-regret task

Analyze the six public-mask multiplication operators at every L18 RNS prime for kernel/invertibility structure. Determine whether inverse norms, spectral zeros, or projection structure can yield any useful coefficient-norm lower bound without the missing residual vectors. This is a read-only algebraic screen and does not authorize Codex, native instrumentation, B176, or route selection.

Research-GPT-provided evidence digests:

```text
REPORT_SHA256: 35f9733cfb27ee7764bbfc49c447ab3fffa75fe4d95c7f18b7f2cc8f0bb2eb92
CSV_SHA256:    26b5eb991dc981a75177c9cf5692e63655b7ab39cb5a442972b6637d613a4125
```

These digests identify the in-conversation report/data generated during the static audit; no separate binary artifact was persisted by the Research GPT in this turn.
