# BOOT B175 Static Noise-Attribution Audit

Date: 2026-10-29 (Asia/Hong_Kong)  
Session: Cryptography 10.0, Research Turn 9/25  
Track: BOOT  
Active subline: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Result

- PRIMARY_HYPOTHESIS_STATUS: PASS_COARSE
- FINE_GRAINED_ATTRIBUTION: UNCLEAR
- EVIDENCE: STATIC_SOURCE_AND_RAW_TRACE_AUDIT
- B175_RESULT: FAIL_B175_POINTWISE_NOISE remains unchanged
- PENDING_PI_DECISION: BOOT-DECISION-001
- B176: NOT_AUTHORIZED

The observed 31-bit required-bit increase is attributable at path level to the real Lattigo v6.2.0 scale-invariant ciphertext-ciphertext multiplication path:

```text
tensoring -> scale-invariant quantization -> relinearization
```

The evidence rules out the CASE_1 LT8 `j mod 8` layout and public expected-reference construction as the cause. It does not uniquely separate the contribution of tensor input-noise propagation, quantization rounding, and relinearization/GadgetProduct noise.

## Static evidence

The five SI ciphertext-ciphertext operations in the same B175 run all add approximately 29--31 required bits relative to their worse input:

| Operation | Required-bit increment |
| --- | ---: |
| Y -> Y2 | 31 |
| Y2 -> Y4 | 31 |
| F0,F1 -> ACC1 | 29 |
| ACC1,F2 -> GROUPED | 30 |
| LT8,GROUPED -> POINTWISE | 31 |

For the final gate:

```text
LT8 required bits      = 577
GROUPED required bits  = 633
POINTWISE required bits = 664
delta = 664 - max(577, 633) = 31
budget = 649 - 664 = -15
```

CASE_1 has `x=1`, so GROUPED expected values are all one and POINTWISE expected values equal the corresponding LT8 public block sums. LT8 and GROUPED each match all 32,768 expected slots. After pointwise multiplication, only one of 32,768 slots matches and only three decoded values lie in the set of eight public block sums. Errors are spread across every slot class rather than showing a cyclic shift or block permutation. This is incompatible with a simple LT8 slot-layout or expected-reference error.

## Source-level boundary

For two degree-one ciphertexts, the audited call dispatches through `MulRelinScaleInvariant` / `tensorScaleInvariant(..., relin=true)` and performs:

1. basis extension and NTT;
2. exact modular tensor products producing degree-two `(c0,c1,c2)`;
3. scale-invariant quantization of all three components;
4. `GadgetProduct(c2, rlk)` and addition of the relinearization correction.

The final residual has the structural form

```text
E_out = E_tensor-propagation + E_quantization + E_relinearization.
```

The current artifact stores the two valid inputs and final degree-one output, but not the internal degree-two state. These three ring-valued error terms can reinforce or cancel, so the final residual alone cannot identify which substage dominates.

## Minimum missing evidence

The smallest decisive pair for separating pre-relinearization and relinearization contributions is:

1. the complete post-quantization, pre-relinearization degree-two residual, decrypted with `(1,s,s^2)` at the final SI scale;
2. the relinearization-only residual obtained by comparing the final degree-one decryption with that degree-two decryption, together with the actual `GadgetProduct(c2, rlk)` output.

Separating tensor propagation from quantization additionally requires the encoded input plaintext coefficient polynomials, the pre-quantization degree-two components in the relevant bases, and the coefficient-wise difference between ideal rounded `T/Q` scaling and the actual quantizer output.

No new native run, Codex task, parameter sweep, B176 action, or branch change was authorized or performed for this audit.

## Necessary-condition screen

At L18, positive budget requires output required bits at most 648. If the SI path increment remains 31 bits, the worse input must have required bits at most 617. The current GROUPED input is 633, so a representation change that leaves the multiplication increment unchanged must recover at least 16 required bits. This is a conditional screen, not a universal lower bound for every possible representation.

## Next no-regret task

Derive the exact source-level error expression for the Lattigo v6.2.0 SI multiplication path, fixing scale conventions, rounding operators, and norm factors, and determine whether the existing B175 input residuals imply any sound upper or lower bound. This is read-only theory work and does not authorize implementation or experimentation.
