# BOOT B175 Decryption-Fiber Gauge Realizability Screen

Date: 2026-10-29 (Asia/Hong_Kong)  
Session: Cryptography 10.0, Research Turn 17/25  
Track: BOOT  
Active subline: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Result

- CLASSIFICATION: PASS
- SCOPE: SINGLE_SI_COMPONENT_ALGEBRA_REALIZABILITY
- EXACT_UNQUANTIZED_TENSOR_GAUGE_INVARIANCE: PASS
- POST_QUANTIZATION_GAUGE_INVARIANCE: FAIL
- FIXED_INPUT_COMPONENT_LEVEL_PASS_FAIL_WITNESS: PASS
- COMMON_ENCRYPTION_DISTRIBUTION_REALIZABILITY: UNCLEAR
- B158_B175_CROSS_STAGE_LINEAGE_REALIZABILITY: UNCLEAR
- FRONTIER_A: UNCLEAR_NOT_ELIMINATED
- FRONTIER_B: UNCLEAR_NOT_ELIMINATED
- VALIDATED_REDESIGN_CANDIDATE: NONE
- PENDING_PI_DECISION: BOOT-DECISION-001
- B176: NOT_AUTHORIZED

The unquantized tensor decrypt of an SI multiplication is exactly invariant under a degree-one ciphertext gauge transformation. Lattigo's componentwise centered lift and `T/Q` quantization break that invariance. At the actual L18 parameters, a fixed-secret, fixed-plaintext, fixed-input-residual, fixed-scale component-algebra witness gives one gauge representative whose SI output passes and another whose output has nonpositive budget.

This strengthens Turn 16 from residual-only completion to single-SI component-algebra realizability. It does not provide two executions from the same real B158/B175 encryption and homomorphic lineage, nor a usable representation repair.

No Codex task, native experiment, B175/B176 run, parameter sweep, implementation, or route selection occurred.

## Exact gauge action before quantization

Write two degree-one ciphertexts as

```text
C(Z) = c0 + c1*Z
D(Z) = d0 + d1*Z,
```

and decrypt by substituting `Z=s`. The gauge transformation

```text
(c0,c1) -> (c0-u*s, c1+u)
```

preserves the input decrypt, plaintext, residual, and metadata scale in `R_Q`.

After coefficientwise centered lift, integer representatives may differ by `Q`-multiple carry polynomials `a0,a1`. With `A(Z)=a0+a1*Z`, the change of the degree-two tensor components satisfies

```text
Delta(t0 + t1*s + t2*s^2) = Q*A(s)*(d0+d1*s).
```

All explicit gauge terms cancel after substituting `Z=s`; only centered-lift `Q`-multiple carries remain. If both operands are gauge transformed, the corresponding expression remains a `Q` multiple. Thus exact tensor multiplication is gauge invariant in `R_Q`.

## Componentwise quantization breaks invariance

Lattigo quantizes the three tensor components separately. With centered reduction `rho_Q` and centered quotient

```text
D_Q(z) = (z-rho_Q(z))/Q,
Q_Q(z) = T*D_Q(z),
```

the pre-relinearization decrypt is

```text
W_pre = T*D_Q(t0) + T*D_Q(t1)*s + T*D_Q(t2)*s^2.
```

For a gauge change in the first operand,

```text
Delta W_pre
  = T*A(s)*D(s)
    - (T/Q)*(R_T'(s)-R_T(s)),
```

where `R_T` is assembled from the three separately reduced tensor components. The first term is centered-lift/`Q`-carry sensitivity; the second is separate component-rounding sensitivity. These nonlinear operations occur before decryption recombination and need not cancel.

Relinearization does not restore general invariance. For the explicit witness below, both third components are zero, so GadgetProduct is identically zero and relinearization error is irrelevant.

## Fixed-input pass/fail witness

Use the actual L18 parameters:

```text
N = 32768
T = 65537
bitlength(Q) = 649
Q mod T = 35478
input scales = 43352 and 35478
output scale = 22185.
```

Fix any nonzero ternary secret and choose a signed monomial `mu` so that the constant coefficient of `mu*s` is one. Let `a=(Q-1)/2`, `x=-1`, and `u=a*mu`.

The baseline and gauge-related first operands are

```text
C_base  = (x,0)
C_gauge = (rho_Q(x-u*s),u).
```

Both decrypt to `-1`, have plaintext zero, residual `-1`, scale 43352, level L18, and required bits 18. The centered lift of the gauge representative carries one `Q` in the integer decrypt.

Let the second operand be `D=(E,0)`, with plaintext zero, scale 35478, level L18, and `E` chosen by the explicit threshold construction from the Research GPT report. It has required bits 633 and positive input budget 16.

For the baseline, the only tensor component is `-E`, whose centered quotient is zero, so the SI output is exactly zero and passes.

For the gauge representative, the quantized decrypt is `T*E + eta`, where a secret-independent bound gives `||eta||_inf <= 1,073,790,978`. The chosen `E` guarantees

```text
bitlength(2*T*(T*E-bound)) = 649,
```

so the output budget is at most zero and fails.

Therefore, with identical input plaintexts, decrypted residuals, levels, scales, and secret:

```text
C_base  * D -> PASS
C_gauge * D -> FAIL.
```

The final decrypted SI result is not gauge invariant.

## Realizability boundary

The witness is `L1.5 / COMPONENT_ALGEBRA_REALIZABLE`: legal degree-one ring components, fixed secret, identical decrypt/residual/scale/level, exact tensor/quantization equations, and an actual fixed-`Q` threshold crossing.

It is not `L2 / COMMON_ENCRYPTION_AND_HOMOMORPHIC_LINEAGE`. It does not show that both representatives can be sampled by the real encryption distribution, reached from the same B158 checkpoint lineage, converted through public evaluation operations, or identified with the actual B175/frontier operands.

Secret-key zero encryption resembles a gauge shift but adds fresh error. It does not preserve the residual exactly, incurs noise and cost, and the explicit witness uses a secret-dependent signed monomial unavailable to a public evaluator. Gauge sensitivity is real; a gauge-based B175 repair is not validated or authorized.

## Frontier impact

The result proves that identical decrypted residual summaries do not determine later SI output at the component-algebra level. It does not provide actual `Y`, `Y^2`, `Y^3`, `LT8`, or `SI(LT8,Y^4)` component pairs from a common lineage, nor their mask/alignment and final multiplication states.

Both frontiers remain `UNCLEAR_NOT_ELIMINATED`, with native correctness and novelty unestablished.

## Next no-regret task

Perform a common-lineage gauge-accessibility screen:

- inspect Lattigo secret-key and public-key zero-encryption component distributions;
- verify whether the B175 source contains fresh zero encryption, rerandomization, or secret-dependent affine adjustment between `LT8`/`GROUPED` and pointwise multiplication;
- classify an exact residual-preserving shift as public-reachable, secret-key-only, or unreachable in the current lineage;
- if only noisy zero encryption is available, bound its added error, operation cost, and key requirements.

This static screen determines whether gauge freedom only explains representation sensitivity or could support a usable mechanism. It does not authorize Codex, native execution, B176, parameter changes, or route selection.

Research-GPT-provided evidence digests:

```text
REPORT_SHA256:       c21eb62b681140f9402ab07c9c2b4d7640b3fc80291533a55474f98b0cfda55e
WITNESS_JSON_SHA256: f9ed51d79842b98b6d3ce4b30b7a83ced6056f3d2b0342c2491835569889e12d
```

These digests identify the in-conversation report/witness data generated during the static audit; no separate binary artifact was persisted by the Research GPT in this turn.
