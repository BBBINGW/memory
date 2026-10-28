# BOOT B175 Zero-Rerandomization Support and Guarantee Screen

Date: 2026-10-29 (Asia/Hong_Kong)  
Session: Cryptography 10.0, Research Turn 19/25  
Track: BOOT  
Active subline: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Result

- OVERALL_CLASSIFICATION: PASS
- SCOPE: SUPPORT_LEVEL_AND_WORST_CASE_GUARANTEE_ONLY
- SK_C1_UNIFORMITY: PASS
- SK_ERROR_SUPPORT: PASS
- SK_SUPPORT_INTERSECTS_TURN17_PASS_AND_FAIL: PASS
- SK_WORST_CASE_FIXED_Q_GUARANTEE: FAIL
- SK_USEFUL_DFR_BOUND: UNCLEAR
- PK_FIXED_KEY_PASS_SUPPORT: PASS
- PK_FIXED_KEY_FAIL_SUPPORT: UNCLEAR
- PK_JOINT_KEYGEN_RERANDOMIZATION_PASS_AND_FAIL_SUPPORT: PASS
- PK_WORST_CASE_OVER_JOINT_SUPPORT: FAIL
- PK_USEFUL_DFR_BOUND: UNCLEAR
- FRONTIER_A: UNCLEAR_NOT_ELIMINATED
- FRONTIER_B: UNCLEAR_NOT_ELIMINATED
- VALIDATED_REDESIGN_CANDIDATE: NONE
- PENDING_PI_DECISION: BOOT-DECISION-001
- B176: NOT_AUTHORIZED

The mathematical support of zero-encryption rerandomization reaches both the Turn-17 PASS and FAIL gauge representatives. Therefore a single unselected rerandomization cannot provide an all-random-coins fixed-`Q` correctness guarantee. The exhibited support points have extremely small probability mass, so this result does not provide a useful DFR upper or lower bound for B175 or either hybrid frontier.

The analysis is counterfactual: the current B158/B175 path contains no rerandomization. No implementation, experiment, DFR claim, Codex task, B176 action, parameter change, or route selection occurred.

## Secret-key support

For fixed secret `s`, secret-key zero encryption samples

```text
Z_sk(a,e) = (e-a*s, a).
```

The second component is sampled coefficientwise uniformly in every RNS prime. CRT and NTT are bijections, so the resulting `a` is uniform in `R_Q`. For any specified polynomial `a*`,

```text
Pr[a=a*] = Q^-N.
```

At the B175 parameters, this is approximately `2^-21,233,683`.

The default bounded Gaussian sampler has exact integer coefficient support `{-19,...,19}`. Probability outside that support is zero. Support membership, exact implementation mass, and a theoretical rounded-Gaussian approximation must not be conflated.

For the Turn-17 baseline representative, the events

```text
PASS: a=0,  e=0
FAIL: a=u*, e=0
```

are both in support. More generally, the zero-error support contains the full exact gauge fiber. Under a rounded-truncated-normal approximation, either specified witness point has probability on the order of `2^-21,332,304`; this is only a scale estimate, not the implementation's exact PMF.

Thus the all-coins SK correctness guarantee fails, but no practically meaningful failure mass or DFR bound follows.

## Public-key support

For a fixed public key, public-key zero encryption samples ternary `u`, two bounded errors, forms two `QP` component products, and applies rounded `P0` mod-down. Its support is the image of

```text
(u,e0,e1) -> (Round_P0(u*pk0+e0), Round_P0(u*pk1+e1)).
```

The source support has at most `3^N * 39^(2N)` points, with log2 size at most about 398,320, while the full degree-one `R_Q` component space has log2 size about 42,467,366. Fixed-key support is therefore a highly correlated tiny subset of the full gauge fiber.

The exact-zero PASS point is always in fixed-key support by selecting all-zero coins. Membership of the specific Turn-17 FAIL representative depends on the actual public key; B175 generated no public key, so fixed-key FAIL support is unclear.

Over joint public-key generation and rerandomization support, any target exact gauge shift is reachable by a constructed support event using a suitable uniform key component, zero public-key error, a constant ternary multiplier, and zero fresh errors. The corresponding specified event again has negligible idealized mass, approximately `2^-22,695,618` for the B175 parameters.

Hence a worst-case guarantee over joint support fails, while practical DFR remains unknown.

## Scientific boundary

The established result is:

```text
single unselected zero rerandomization:
  FAIL as a worst-case correctness rescue

probabilistic rerandomization:
  UNCLEAR; it becomes a new DFR problem

gauge sensitivity:
  retained as explanatory phenomenon

gauge-based redesign:
  not validated, not authorized, not a contribution.
```

No evidence shows that rerandomization improves the success probability of either frontier. Their native status remains unclear.

Any useful probability bound would require the actual input ciphertext components and secret, centered lifts, `Q_Mul` tensor components, quantization cell boundaries, GadgetProduct behavior, exact sampler PMF or stated idealization, independence assumptions, and—on the public-key path—the actual public key and a clear choice between fixed-key and key-averaged probability.

## Next no-regret task

Perform a Turn-17 quantization-cell robustness/support-counting screen. Characterize discrete rerandomization coin neighborhoods that preserve the PASS or FAIL verdict, determine whether the FAIL witness is isolated or has a rigorously countable nonzero neighborhood, bound its support count or probability mass, and state why any such bound does or does not transfer to actual B175/frontier operands.

This remains static and does not authorize rerandomization, native execution, B176, DFR claims, parameter changes, or route selection.

Research-GPT-provided evidence digests:

```text
REPORT_SHA256: 50021c33c9e52453230eaa025a2e8e7031184d8c21324e3cdb6b7a03f3d72f27
DATA_SHA256:   d4448764f391adfd403933e741d3c568257a952042de1887dbf1e0b1a495ac49
```

These digests identify the in-conversation report/data generated during the static audit; no separate binary artifact was added to GitHub memory in this turn.
