# BOOT B175 Quantization-Cell Robustness and Support Counting

Date: 2026-10-29 (Asia/Hong_Kong)  
Session: Cryptography 10.0, Research Turn 20/25  
Track: BOOT  
Active subline: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Result

- CLASSIFICATION: PASS
- SCOPE: TURN17_SYNTHETIC_WITNESS_AND_SK_RERANDOMIZATION_SUPPORT
- FAIL_WITNESS_ISOLATED: NO
- EXACT_FAIL_QUANTIZATION_CELL: PASS
- EXACT_PASS_QUANTIZATION_CELL: PASS
- NONTRIVIAL_SUPPORT_COUNT: PASS
- PRACTICALLY_MEANINGFUL_FAILURE_MASS: FAIL
- B175_OR_FRONTIER_DFR_CONCLUSION: UNCLEAR_NOT_TRANSFERABLE
- STATIC_RERANDOMIZATION_SUBLINE: SATURATED_WITHOUT_ACTUAL_COMPONENTS
- FRONTIER_A: UNCLEAR_NOT_ELIMINATED
- FRONTIER_B: UNCLEAR_NOT_ELIMINATED
- VALIDATED_REDESIGN_CANDIDATE: NONE
- PENDING_PI_DECISION: BOOT-DECISION-001
- B176: NOT_AUTHORIZED

The Turn-17 FAIL witness is not an isolated point in discrete rerandomization coin space. There is an exactly countable error-polynomial cell in which every componentwise centered quotient is unchanged and the final SI output remains the same FAIL. A larger exact PASS cell also exists. Both cells still require the uniform second component to hit one of very few prescribed ring polynomials, so their probability is dominated by `Q^-N` and is astronomically negligible.

This strengthens the worst-case negative result but does not yield a practical DFR statement for B175 or either frontier. No Codex task, native experiment, rerandomization, B176 action, parameter change, implementation, or route selection occurred.

## Fixed witness and sampler

The analysis fixes the Turn-17 synthetic witness, the actual L18 modulus, `N=32768`, `T=65537`, and a nonzero ternary secret. Secret-key zero encryption samples

```text
Z(a,e) = (e-a*s, a),
```

with uniform `a` in `R_Q` and each error coefficient in `{-19,...,19}`. The uniformity statement is exact under the ideal random-byte model; the error set is a hard implementation support bound, not a Gaussian tail event.

## Exact PASS cell

For every signed-monomial multiple

```text
a = k*mu, k in {-19,...,19},
```

and every supported error polynomial, both tensor components stay inside the zero centered-quotient cell. The SI output is exactly zero and passes.

The certified support count is

```text
C_PASS = 39^(N+1),
log2(C_PASS) approximately 173197.34.
```

Because only 39 uniform ring polynomials are accepted, its probability is exactly `39*Q^-N`, approximately `2^-21,233,677.84` in log2 scale.

## Exact FAIL cells

Let `A=(Q-1)/2`. For each `k` from 0 through 19, set the uniform component to a prescribed signed-monomial polynomial `(A-k)*mu` and restrict supported error coefficients according to the sign pattern of the shifted secret. These inequalities keep every tensor component in exactly the same centered-quotient cell as the Turn-17 FAIL representative.

Consequently the tensor quotients, relinearization input, final decrypted SI output, and FAIL verdict are exactly unchanged throughout each cell.

For secret Hamming weight `h`, the exact certified support count is

```text
C_FAIL(h)
  = 39^(N-h) * sum_{k=0}^{19} (20-k)*(20+k)^(h-1).
```

The single `k=19` cell alone has `39^(N-1)` points, with log2 count approximately 173186.77. Thus the FAIL witness is decisively non-isolated.

In terms of the implementation coefficient masses `p_j`, the exact probability expression for the certified FAIL union is

```text
Q^-N * sum_{k=0}^{19} G_k * F_k^(h-1),
```

where `G_k=Pr[e<=-k]` and `F_k=Pr[e<=k]`. The full exact Ziggurat PMF was not reconstructed, so no textbook Gaussian PMF is substituted for the implementation.

Under a clearly labeled rounded-truncated-normal approximation and typical dense-ternary secret weight, the certified FAIL union remains on the order of `2^-21,233,696.10`. This is a synthetic-witness scale estimate, not B175 or frontier DFR.

## Scientific boundary

Both PASS and FAIL verdicts occupy large combinatorial cells, but each cell is pinned to a negligible set of uniform ring elements. Non-isolation therefore does not imply meaningful probability mass.

The witness uses a deliberately constructed scalar second operand, a secret-dependent signed monomial, known centered boundaries, and a zero degree-two component. Actual B175/frontier component states, secret, tensor lifts, quantization margins, GadgetProduct behavior, and randomness dependencies are absent. The result cannot be transferred to `LT8`, `GROUPED`, `G01E`, or `A2(L)`.

The static rerandomization subline is now saturated without actual component states. Further counting around this synthetic witness would not materially change the active candidate assessment. Gauge/rerandomization remains explanatory evidence, not a rescue candidate, paper contribution, or DFR result.

## Next no-regret task

Return to the two surviving hybrid selector frontiers and compute a best-case research-value ceiling assuming future native correctness. Compare ciphertext-ciphertext count, full SI depth, public-linear work, rotation keys, key memory, scale-alignment burden, interface changes, and equivalence to distributive/binary-selector/Paterson-Stockmeyer scheduling. Determine whether either frontier could offer independent research value beyond repairing a failed interface even in the best correctness case.

This remains read-only and does not authorize B176, implementation, native execution, route selection, or a contribution claim.

Research-GPT-provided evidence digests:

```text
REPORT_SHA256: 8d07f5b1992e6abe1fe6c4e7b63bdbf95cb54a69d20be1a65fcd12c205240860
DATA_SHA256:   4337142b802b424a9b8dcf3b21b4d67ab4dc53d0f1582719737e0545c5282319
```

These digests identify the in-conversation report/data generated during the static audit; no separate binary artifact was added to GitHub memory in this turn.
