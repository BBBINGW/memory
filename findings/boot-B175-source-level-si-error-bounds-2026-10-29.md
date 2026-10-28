# BOOT B175 Source-Level SI Error Bounds

Date: 2026-10-29 (Asia/Hong_Kong)  
Session: Cryptography 10.0, Research Turn 10/25  
Track: BOOT  
Active subline: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Result

- STATUS: PASS_STRONG_COARSE_ATTRIBUTION / UNCLEAR_FINE_DECOMPOSITION
- EVIDENCE: SOURCE_DERIVATION + B175_RAW_AUDITED_RESIDUALS
- B175_RESULT: FAIL_B175_POINTWISE_NOISE remains unchanged
- PENDING_PI_DECISION: BOOT-DECISION-001
- B176: NOT_AUTHORIZED

Under the audited B175 parameters, source-level bounds for scale-invariant quantization and relinearization are many orders of magnitude below the observed pointwise residual. Consequently, the observed 647-bit coefficient residual must be dominated by the aggregate tensor/reference term, not by quantization rounding or GadgetProduct/relinearization key-switch noise.

The remaining unresolved attribution is internal to the aggregate tensor/reference term: plaintext-times-input-noise, input-noise-times-input-noise, component-lift/Q-carry, and reference-encoding carry cannot be separated with the current artifact.

## Residual convention

Let `R = Z[X]/(X^N+1)`, `N=32768`, plaintext modulus `T=65537`, and ciphertext modulus `Q=Q18`. For ciphertext `C`, metadata scale `sigma`, and expected plaintext `m`, define

```text
e_C = rho_Q(Dec_s(C) - M_{sigma,Q}(m))
r(C) = bitlength(2*T*||e_C||_infinity)
B(C) = bitlength(Q) - r(C).
```

The B175 pointwise scale law closes exactly:

```text
sigma_LT8       = 43352
sigma_GROUPED   = 43178
(-Q mod T)^-1  = 44421
sigma_POINTWISE = 43352 * 43178 * 44421 mod 65537 = 30059.
```

This rules out an obvious output-scale metadata mismatch.

## Source-level decomposition

For degree-one ciphertexts `C=(c0,c1)` and `D=(d0,d1)`, the SI path forms degree-two tensor components `u0,u1,u2`, quantizes them to `v0,v1,v2`, and relinearizes `v2`. With centered reduction `rho_Q`, the final residual has the exact structural relation

```text
e_out = rho_Q(E_tref + E_quant + E_relin).
```

Here:

- `E_tref` is the aggregate tensor/reference term, including input residual propagation, reference multiplication, component-lift carry, and reference-encoding carry;
- `E_quant` is the sum of the three SI quantization-rounding errors after decryption with `(1,s,s^2)`;
- `E_relin` is the GadgetProduct/relinearization error.

For each component, centered nearest-quotient quantization gives a coefficient error strictly below `T/2`. Using the deterministic ternary-secret bounds `||s||_1 <= N` and `||s^2||_1 <= N^2` yields

```text
||E_quant||_infinity
  <= (T/2) * (1 + N + N^2)
  = 35,185,982,750,721
  < 2^46.
```

If quantization were the only error, its B175 required-bit upper bound would be 63, versus the observed pointwise required bits 664.

For the B175 L18 RNS relinearization key, the audited source parameters give five centered decomposition blocks. Using the parameter-layer evaluation-key error bound rounded up to 20, plus conservative rounded P-moddown error, gives

```text
||E_relin||_infinity < 2,637,825 < 2^22.
```

This corresponds to a required-bit upper bound of 39.

## Consequence

The observed pointwise maximum coefficient residual has bit length 647. Let

```text
B_small = B_quant + B_relin
        = 35,185,985,388,546.
```

The centered-distance triangle inequality implies

```text
||rho_Q(E_tref)||_infinity
  >= ||e_out||_infinity - B_small.
```

The resulting lower bound still has residual bit length 647 and required bits 664. Thus even removing quantization and relinearization at their conservative worst-case bounds would not change the B175 failure classification.

The practical conclusion is that a bounded representation redesign, if PI later authorizes one, must materially change tensor/reference geometry: coefficient geometry, component-lift/carry behavior, the representation of the low-headroom GROUPED operand, or where the multiplication occurs. Optimizing only decomposition, key-switch constants, quantization rounding, or a few local noise bits cannot rescue the current direct composition.

## Remaining uncertainty and minimum evidence

The current input residuals do not give a useful ex-ante upper bound for all of `E_tref`, because the artifact omits the componentwise centered lifts and associated Q-multiple carries. Fine decomposition requires at least:

1. the L18 componentwise centered lifts `c0,c1,d0,d1`, or equivalent pre-quantization `u0,u1,u2`;
2. the actual secret polynomial for exact rather than worst-case decomposition;
3. the coefficient-domain reference polynomials for both inputs and output;
4. the post-quantization, pre-relinearization degree-two state and residual;
5. the raw GadgetProduct output and its relinearization-only residual.

Items 4 and 5 suffice to separate pre-relinearization from relinearization. Items 1 and 3 are additionally required to separate tensor propagation from quantization. Obtaining them would require new native instrumentation and is not authorized.

## Next no-regret task

Perform a purely static mechanism-level prior-art and necessary-condition screen of bounded representation-layer candidates. A candidate is relevant only if it can explain how it changes tensor/reference geometry and can plausibly recover the conditional 16-required-bit deficit at fixed `Q`. No implementation or native experiment is authorized.
