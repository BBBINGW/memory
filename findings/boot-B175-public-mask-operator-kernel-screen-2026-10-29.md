# BOOT B175 Public-Mask Operator Kernel Screen

Date: 2026-10-29 (Asia/Hong_Kong)  
Session: Cryptography 10.0, Research Turn 15/25  
Track: BOOT  
Active subline: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Result

- OVERALL_CLASSIFICATION: FAIL
- PRIMARY_HYPOTHESIS: FAIL_SCREEN
- RINGT_PROJECTION_ANALYSIS: PASS
- L18_RNS_KERNEL_RANK_ANALYSIS: PASS
- USEFUL_UNIVERSAL_COEFFICIENT_LINF_LOWER_BOUND: FAIL
- FRONTIER_A: UNCLEAR_NOT_ELIMINATED
- FRONTIER_B: UNCLEAR_NOT_ELIMINATED
- FRONTIER_ELIMINATED: NONE
- VALIDATED_REDESIGN_CANDIDATE: NONE
- PENDING_PI_DECISION: BOOT-DECISION-001
- B176: NOT_AUTHORIZED

The six public-mask operators' kernel, invertibility, spectral-zero, and inverse-norm structure cannot yield a universal coefficient-infinity-norm lower bound strong enough to consume Frontier A's four-bit or Frontier B's three-bit modeled slack when the decisive residual vectors are unknown. This statically falsifies the operator-only lower-bound screen. It does not validate either frontier.

No Codex task, native experiment, B175 rerun, parameter sweep, B176 action, or route selection occurred.

## Three distinct algebraic objects

The plaintext ring is

```text
R_T = F_T[X]/(X^N+1), T=65537, N=32768.
```

Because `2N` divides `T-1`, the plaintext NTT identifies `R_T` with `F_T^N`. In this ring, `c2` and `d2` are complementary rank-16384 projections, while each `Mi` is a rank-8192 projection. Their kernel dimensions are 16384 and 24576, respectively, and their idempotence and orthogonality identities hold.

This projection structure does not transfer to the raw-lift residual operator over an L18 prime `q_j`. The Lattigo scale-one vector plaintext path lifts the `R_T` coefficients through `T^-1 mod q_j`, and ciphertext-plaintext tensoring multiplies back by `T`. This coefficient lift is not a ring homomorphism from characteristic `T` to characteristic `q_j`.

The complete masked residual is also not merely `A*e`; it is

```text
e_mask = rho_Q(A*e + C_A(m)),
```

where `C_A(m)` is the reference encoding/lifting carry. Plaintext projection, lifted residual multiplication, and the complete residual-with-carry must not be conflated.

## L18 RNS reconstruction

The complete 19-prime L18 chain was reconstructed from Lattigo v6.2.0's alternating NTT-prime generation rules. It verifies

```text
bitlength(Q_L18) = 649
Q_L18 mod 65537  = 35478.
```

For every one of the 19 primes, exact integer modular evaluation at all 32,768 odd NTT roots gives the same result for all six raw-lift masks:

```text
zero eigenvalues = 0
kernel dimension = 0
rank             = 32768
invertible        = yes.
```

Thus `c2`, `d2`, and every `Mi` are units over every `R_qj`. Their pairwise products are units rather than zero, and the plaintext-ring orthogonal-projection geometry has disappeared at the residual-operator layer.

## Why invertibility gives no useful lower bound

For centered coefficient norm over one prime and `B=A^-1`, the valid inequality direction is

```text
||A e||_(inf,q) >= ||e||_(inf,q) / ||A^-1||_1.
```

The exact inverse-polynomial `log2(l1)` ranges are:

| Mask | log2 inverse l1 across L18 primes |
| --- | ---: |
| c2, d2 | 35.34--38.08 |
| M0 | 34.58--37.27 |
| M1 | 34.32--37.20 |
| M2 | 34.24--36.34 |
| M3 | 33.80--37.07 |

This can guarantee only a loss of roughly 34--38 bits, whereas frontier elimination would require a guaranteed growth of at least three or four bits.

The explicit counterexample is `e=A^-1`, for which `A*e=1` despite inverse coefficients of approximately 32--35 bits. Finite-field centered eigenvalue magnitude is not a real singular value and cannot repair this direction.

Including the carry rules out even a positive absolute lower bound. Because the aggregate operator is invertible over the CRT ring, for any fixed carry one may take

```text
e = -A_Q^-1 C_A(m),
```

which gives `e_mask=0`. This is an algebraic counterexample to any operator-only universal positive output-norm bound.

## Conditional integer result

Under three additional assumptions—no modulo-`Q` wrap, no encoding carry, and no cancellation across aligned branches—the raw integer convolution inverse gives a much stronger conditional minimum gain:

| Mask | Conditional no-wrap minimum gain |
| --- | ---: |
| c2, d2 | 14.26 bits |
| M0 | 15.23 bits |
| M1 | 15.15 bits |
| M2 | 15.46 bits |
| M3 | 15.32 bits |

This explains the 17--18-bit empirical growth on the saved healthy operands from Turn 14. It cannot eliminate either frontier because the decisive operands have no no-wrap proof, carry is present, aligned branches may cancel, and final SI behavior depends on ciphertext component lifts and `Q`-carry.

## Frontier impact

Frontier A still lacks full residual vectors for `Y`, `Y^2`, and `Y^3`, all three masked/aligned nonconstant branches, and the complete `G01^E` residual. Plaintext projection ranks do not constrain these CRT residuals, and the general inverse bound is too weak.

Frontier B still lacks `SI(LT8,Y^4)`, its `c2`-masked high branch, and the scale-matched `A2(L)` residual. The known low branch is insufficient, and operator invertibility neither guarantees high-branch growth nor rules out branch cancellation.

Both remain `UNCLEAR_NOT_ELIMINATED`; there is no native correctness result or validated redesign.

## Next no-regret task

Construct two algebraic completions of the missing residual data, both satisfying all currently persisted maxima, scales, and public-mask constraints, with one satisfying and one violating each frontier's static correctness bound. If both completions exist, the current summaries are information-theoretically insufficient and `UNCLEAR` is unavoidable. If not, the obstruction identifies an additional constraint stronger than the kernel/invertibility screen.

This remains pure algebraic work and does not authorize Codex, native instrumentation, B176, parameter changes, or route selection.

Research-GPT-provided evidence digests:

```text
REPORT_SHA256: 4f179661c74e1f1c22764d1f3528508ffdd429b7f7eb376612b651bb86a32b29
CSV_SHA256:    a3dafda2b6563b714613e15c811989bd8e557192f557f60ed0e0b9fe0d612124
```

These digests identify the in-conversation report/data generated during the static audit; no separate binary artifact was persisted by the Research GPT in this turn.
