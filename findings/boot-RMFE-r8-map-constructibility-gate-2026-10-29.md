# BOOT RMFE R8 Source-Lineage and Map-Constructibility Gate

Date: 2026-10-29  
Session: 密码学 11.0, Research Turn 12/25  
Controller note: the Research GPT response self-labelled this turn as 13/25 after an adapter recovery. The controller normalized it to the next unconsumed turn, 12/25, and accepted it exactly once.

## Scope

This turn tested one provisional BOOT successor question after parking B158/B176 at its soft budget:

`RMFE_R8_SOURCE_LINEAGE_AND_MAP_CONSTRUCTIBILITY_GATE`

No Codex task, native experiment, key generation, full capacity propagation, benchmark, or parameter sweep was executed. The orchestrator's durable `ACTIVE_SUBLINE` remains `B158_CHECKPOINT_DECOUPLED_HALF_BASIS`; RMFE remains a reversible provisional candidate within the authorized BOOT objective.

## Result

```text
CLASSIFICATION: FAIL
RESULT: FAIL_DIRECT_MA_PATCH_DROPIN

SOURCE_LINEAGE_MECHANICAL_PORTABILITY:
PASS_BOUNDED_NOT_BUILD_TESTED

CUSTOM_R8_MAP_CONSTRUCTIBILITY:
PASS_STATIC

WHOLE_PIPELINE_CAPACITY:
UNCLEAR
```

The direct reuse route is killed because the existing Ma `ThinPo2IFFT` path derives its clearing depth and partition from the outer HElib context. In the fixed Aung context this produces the outer parameters (`m=32768`, `ordP=8192`, 13 clearing stages), while the provisional candidate needs an embedded degree-8 construction (`m_r=32`, `r=8`, `Y=X^1024`, 10 RM stages). The existing constructor does not expose the embedded parameters, so the stock `EvalMap`, `ThinEvalMap`, or Ma path is not a drop-in generator for the required map.

This falsifies only the direct patch/drop-in route. It does not falsify the RMFE candidate.

## Static constructive result

Let

```text
S = Z/625Z
A = S[Y]/(Y^16 + 1) subset S[X]/(X^16384 + 1)
Y = X^1024
G = (Z/32Z)^* = {1,3,5,...,31}
```

Because `5` does not divide `16`, the embedded algebra is a rank-16 Galois algebra. Any required `S`-linear basis map has an automorphism-multiplier expression

```text
L(z) = sum_{u in G} a_u(Y) * sigma_u(z),
sigma_u(Y) = Y^u.
```

After embedding, the available HElib primitives

```text
smartAutomorph(u)
multByConstant(a_u(X^1024))
ciphertext additions
```

are sufficient to express a custom map without changing the outer `ordP=8192`. A direct representation uses at most 15 nonidentity automorphism keys; a smaller decomposition is possible in principle but not established.

The ten RM exponents are:

```text
16385, 8193, 4097, 2049, 1025,
513, 257, 129, 65, 33
```

The normalization constant is `(2^10)^(-1) mod 625 = 224`. In the inspected HElib scalar-multiplication path, multiplication by a plaintext-modulus unit updates `intFactor` without increasing the ciphertext parts or the library noise ledger. This yields a local static advantage over the 13-stage route, but exact key-switch terms and whole-pipeline capacity remain unestablished.

## Accepted boundary

```text
DROPIN_EXISTING_EVALMAP: FAIL
CUSTOM_AUTOMORPHISM_MULTIPLIER_MAP: EXISTS
OUTER_ORDP_CHANGE_REQUIRED: NO
RM10_NORMALIZATION_NOISE: ZERO_IN_HELIB_LEDGER
RM10_VS_RM13: THREE_FEWER_CLEARING_STAGES
WHOLE_PIPELINE_CAPACITY_NOISE: UNCLEAR_PENDING_EXACT_CONSTANTS
VALIDATED_CANDIDATE: NO
NOVELTY: NOT_ESTABLISHED
RESEARCH_FRONTIER_EXHAUSTED: false
```

## Next cheapest decisive test

`RMFE_R8_EXACT_PLAINTEXT_MAP_GENERATOR_GATE`

The gate must stop after:

1. solving the target 16-by-16 map for the exact coefficients `a_u(Y)`;
2. lifting `Y^j` to `X^(1024j)`;
3. verifying all 16 basis images and the five retained RMFE coordinates;
4. reporting canonical coefficient norms and automorphism exponents.

It must not perform key generation, `InnerProduct`, full capacity/noise propagation, or benchmarking. Only after this gate passes would key-switch/noise-ledger execution have adequate value of information.

```text
AI_PROVISIONAL_CHOICE:
  RETAIN_RMFE_PROVISIONAL_CANDIDATE
  KILL_DIRECT_MA_PATCH_DROPIN
  REPLACE_IMPLEMENTATION_ROUTE_WITH_CUSTOM_R8_MAP_GENERATOR
```
