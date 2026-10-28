# BOOT B175 Common-Lineage Gauge Accessibility Screen

Date: 2026-10-29 (Asia/Hong_Kong)  
Session: Cryptography 10.0, Research Turn 18/25  
Track: BOOT  
Active subline: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Result

- CLASSIFICATION: PASS
- SCOPE: CURRENT_B158_B175_PUBLIC_LINEAGE_ACCESSIBILITY
- EXACT_SHIFT_PUBLIC_REACHABLE: NO
- EXACT_SHIFT_SECRET_KEY_ONLY: YES
- CURRENT_LINEAGE_RERANDOMIZATION_PRESENT: NO
- CURRENT_LINEAGE_PUBLIC_KEY_PRESENT: NO
- SECRET_KEY_ZERO_ENCRYPTION_AS_PUBLIC_FHE_MECHANISM: FAIL
- COUNTERFACTUAL_PUBLIC_KEY_RERANDOMIZATION: UNCLEAR_NOT_KILLED_BY_COST
- GAUGE_DIRECTION_CURRENT_DECISION: KILLED_AS_CURRENT_PUBLIC_REDESIGN
- GAUGE_SENSITIVITY: RETAIN_AS_EXPLANATORY_PHENOMENON
- FRONTIER_A: UNCLEAR_NOT_ELIMINATED
- FRONTIER_B: UNCLEAR_NOT_ELIMINATED
- VALIDATED_REDESIGN_CANDIDATE: NONE
- PENDING_PI_DECISION: BOOT-DECISION-001
- B176: NOT_AUTHORIZED

The exact residual-preserving gauge shift established in Turn 17 is not reachable by the current public B158/B175 evaluator lineage. A secret holder can construct it, but doing so changes the trust model. The audited path contains no rerandomization and no public key. Therefore gauge selection is killed as a current fixed-`Q` public redesign mechanism while retained as an explanation of component/randomness sensitivity.

This does not prove that every noisy public-key rerandomization variant fails. Such a variant is outside the current implementation and remains an unauthorized probabilistic mechanism requiring separate correctness/DFR, cost, and novelty analysis.

No Codex task, native experiment, B175/B176 run, parameter sweep, implementation, or route selection occurred.

## B175 call-path audit

The audited B175 source contains three encryption calls, all in initial-input or initial-secret-block construction before checkpoint/basis, `GROUPED`, and `LT8` formation. It contains none of:

```text
EncryptZero
EncryptZeroNew
GenPublicKey
NewPublicKey
Rerandomize
ReRandomize
ReRand
```

Setup creates a secret key, relinearization key, Galois keys, a memory evaluation-key set, secret-key encryptor/decryptor, and evaluator. No public key is generated or passed to the B175 gate.

From completed `GROUPED` and `LT8` operands to pointwise evaluation, the path performs validation and then exactly one `MulRelinScaleInvariantNew(LT8,GROUPED)`. There is no fresh zero encryption, rerandomization, component edit, secret-dependent adjustment, rotation, key switch, refresh, rescale, or level drop between operand completion and pointwise multiplication.

The audited parent hashes remain:

```text
B175 ZIP SHA256:         1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa
B175 source/main.go SHA: a2f6ed20981e182519de044703bf50b6c1981245a5a6df67dfdf3f90b992cd20
```

## Exact gauge reachability

The exact shift is

```text
(c0,c1) -> (c0-u*s,c1+u),
```

equivalent to adding `(-u*s,u)`, whose decryption residual is exactly zero.

A public evaluator cannot form the first component for chosen `u` without the secret or an equivalent noiseless public object. The available relinearization and Galois keys are noisy gadget encryptions for specific secret relations and are not an API for arbitrary exact-zero ciphertext creation.

A secret holder can directly compute the shift with one ring multiplication and two component additions, but exposing the secret to homomorphic evaluation changes the security/trust model and is absent from the current gate.

## Secret-key zero encryption

Lattigo secret-key zero encryption samples uniform `a` and fresh error `e`, returning

```text
(e-a*s, a),
```

which decrypts to `e`, not exact integer zero. Under the default discrete-Gaussian bound, a conservative coefficient bound `||e||_inf <= 20` gives at most 22 required bits.

A degree-one L18 ciphertext carries approximately 9.50 MiB of raw `Q`-coefficient payload. Secret-key zero encryption adds sampling, one `a*s` product, component subtraction, and ciphertext addition. Its direct residual magnitude alone does not prove loss of the frontiers' three-to-four-bit final slack. It is excluded here because it requires online secret-key access, samples an uncontrolled gauge, is not a public evaluator operation, and is absent from the path.

## Public-key zero encryption

Public-key zero encryption samples a small ternary `u` and fresh errors, multiplies `u` by both public-key components in `QP`, and performs rounded `P0` mod-down. A conservative deterministic coefficient bound gives at most 16,385 residual magnitude, or at most 32 required bits.

The B175 parameters use 20 `Q` primes and four `P` primes. A degree-one public key has about 12.00 MiB raw coefficient payload, approximately 1.13% of the reported 1,114,150,880-byte relinearization-plus-Galois-key total. One rerandomization additionally requires small-secret/error sampling, basis extension, two `QP` polynomial products, inverse transforms, two rounded mod-downs, conversion, and ciphertext addition.

These bounds do not kill public-key rerandomization by noise or memory alone. Its random gauge is not selected for favorable downstream SI behavior, and a public evaluator cannot test which representative is better. Without secret-assisted selection, it creates a new probabilistic correctness/DFR question rather than a worst-case rescue guarantee.

## Scientific boundary

Current exact-gauge public redesign is statically killed. Gauge sensitivity remains a valid explanation of why identical decrypted residuals need not determine SI output.

Counterfactual noisy public-key rerandomization is `UNCLEAR_NOT_AUTHORIZED`, not a survivor candidate. Introducing it would constitute a new representation/randomization mechanism requiring PI authorization and independent correctness, DFR, cost, security, and novelty review.

Neither hybrid frontier's native status changes.

## Next no-regret task

Perform a zero-encryption rerandomization support/guarantee screen:

- prove the secret-key zero-encryption second component is uniform and characterize the full error support;
- determine whether the Turn-17 PASS and FAIL component representatives both lie in that distribution's support;
- if both do, determine whether this rules out worst-case correctness guarantees and reduces any benefit to a probabilistic DFR question;
- derive support constraints after public-key `P0` mod-down;
- identify the minimum actual operand, secret, and quantization data needed for any nontrivial success-probability bound.

This remains static and does not authorize rerandomization implementation, Codex, native execution, B176, parameter changes, or route selection.

Research-GPT-provided evidence digests:

```text
REPORT_SHA256:      84c4ebaded12106ad85a95c8077175b2dcbc8266455e4c99e8fe7ca9d6dcc0bb
BOUNDS_JSON_SHA256: 693ba25980751e8c30fd63fda1c21ee24b4b6f8d3ad064e2b820510dbef18d9b
```

The Research GPT reported that the evidence files were also saved to its Library. No separate binary artifact was added to GitHub memory in this turn.
