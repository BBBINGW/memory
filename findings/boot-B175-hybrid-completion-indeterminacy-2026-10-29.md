# BOOT B175 Hybrid-Completion Indeterminacy Screen

Date: 2026-10-29 (Asia/Hong_Kong)  
Session: Cryptography 10.0, Research Turn 16/25  
Track: BOOT  
Active subline: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Result

- CLASSIFICATION: PASS
- SCOPE: SUMMARY_AND_DECRYPTION_RESIDUAL_LEVEL_ONLY
- SUMMARY_LEVEL_NONIDENTIFIABILITY: PASS
- PUBLIC_MASK_SCALE_ALIGNMENT_ADDITION_COMPATIBILITY: PASS
- SOURCE_RESIDUAL_EQUATION_CONSISTENCY: PASS_FORMAL
- COMMON_CIPHERTEXT_COMPONENT_LINEAGE_REALIZABILITY: UNCLEAR
- FRONTIER_A_NATIVE_STATUS: UNCLEAR_NOT_ELIMINATED
- FRONTIER_B_NATIVE_STATUS: UNCLEAR_NOT_ELIMINATED
- VALIDATED_REDESIGN_CANDIDATE: NONE
- PENDING_PI_DECISION: BOOT-DECISION-001
- B176: NOT_AUTHORIZED

For each hybrid frontier, the currently persisted maxima, scales, exact saved residual arrays, public masks, and public affine operations admit one residual-level algebraic completion that passes the fixed-`Q` static bound and another that fails it. Therefore the current summaries are information-theoretically insufficient at the summary/decryption-residual abstraction level.

This result does not establish two complete realizable Lattigo executions with opposite native outcomes. Common secret, component lineage, quantization states, evaluation-key errors, and `Q`-carry remain missing.

No Codex task, native experiment, B175 rerun, parameter sweep, B176 action, or route selection occurred.

## Completion levels

Let `R_Q=Z_Q[X]/(X^N+1)`, with `N=32768`, `T=65537`, `bitlength(Q)=649`, and `Q mod T=35478`. For a centered residual `e`, use the B175 convention

```text
r(e) = bitlength(2*T*||e||_inf).
```

The fixed-`Q` positive-budget condition is `r(e) <= 648`.

Three completion levels are distinguished:

1. `L0 summary-compatible`: exact saved arrays remain fixed; maximum-only stages retain the saved maximum; level, scale, expected plaintext, and centered-representative conventions remain fixed. No homomorphic realizability is required.
2. `L1 decryption-residual/public-affine-compatible`: in addition to L0, public-mask encoding, deterministic carry, scale alignment, addition, and centered reduction follow the exact Lattigo equations. Any single residual may be embedded in a degree-one ciphertext under the decryption map, but cross-stage lineage and encryption-distribution support are not required.
3. `L2 real component lineage`: all stages must share an actual sparse-ternary secret, ciphertext components, evaluation-key errors, centered component lifts, `Q_Mul` states, quantization/relinearization outputs, and a common operation lineage.

This turn establishes opposite completions at L0/L1 only. L2 remains unclear.

## Frontier A witnesses

Frontier A is

```text
Y3   = SI(Y,Y2)
G01E = M0 + M1*Y + M2*Y2 + M3*Y3
H    = SI(LT8,G01E)
OUT  = SI(H,F2).
```

For the saved maxima of `Y` and `Y2`, use monomial residuals with exactly the required maximum, giving required bits 524 and 555. Exact public-mask and scale alignment to scale 22359 gives

```text
r(aligned M1*Y)  = 548
r(aligned M2*Y2) = 587.
```

Pass completion: choose `e_Y3=0`. Deterministic carry remains, giving

```text
r(M3*Y3) = 32
r(G01E)   = 587
r(H)      = 616
r(OUT)    = 645 <= 648.
```

Fail completion: use the saved healthy LT8 residual vector as an L1 ring-residual witness for `Y3` without claiming ciphertext reuse. Then

```text
r(e_Y3)   = 577
r(M3*Y3)  = 594
r(G01E)   = 594
r(H)      = 623
r(OUT)    = 652 > 648.
```

The modeled SI steps use the explicitly scoped optimistic 29-bit envelope. Every pre-final witness remains within the positive-budget region.

## Frontier B witnesses

Frontier B is

```text
ACC1  = SI(F0,F1)
Z     = SI(LT8,Y4)
A2(L) = d2*LT8 + c2*Z
OUT   = SI(ACC1,A2(L)).
```

The fixed low branch is the exact Turn-14 value

```text
r(aligned d2*LT8) = 610.
```

Pass completion: choose `e_Z=0`. Exact `c2` carry gives required bits 34, so

```text
r(A2(L)) = 610
r(OUT)   = 639 <= 648.
```

Fail completion: choose a centered monomial residual with `r(e_Z)=605`. Exact `c2` masking and public addition give

```text
r(c2*Z)  = 620
r(A2(L)) = 620
r(OUT)   = 649 > 648.
```

Again, every pre-final intermediate retains positive budget; the failure occurs only at the modeled final SI output.

## What is proved

Let the persisted observation contain the exact saved `LT8`, `GROUPED`, and `POINTWISE` arrays; all other saved maxima; scale metadata; expected plaintext; public masks; public scale multipliers; and exact affine residual rules. At L0/L1, both frontiers admit observations-identical pass and fail witnesses. Consequently no decision rule using only that observation can determine the frontier's fixed-`Q` static result.

This proves

```text
SUMMARY_LEVEL_UNCLEAR = INFORMATION_THEORETICALLY_UNAVOIDABLE.
```

It does not prove native-execution nonidentifiability. L2 additionally requires a common Hamming-weight-512 secret, actual `(c0,c1)` components, componentwise lifts, `Q`-multiple carries, `Q_Mul` and quantization states, relinearization-key error, cross-stage SI lineage, and encryption/error-distribution support. The real L2 fiber could contain pass and fail executions, only one verdict, or no execution matching one of the L1 witnesses.

## Next no-regret task

Analyze the decryption fiber's gauge freedom. The transformation

```text
(c0,c1) -> (c0-u*s, c1+u)
```

preserves `c0+c1*s` and hence the input decrypted residual, while SI multiplication quantizes the tensor components separately. Determine whether, at fixed input decryption residual and scale, gauge-related component pairs can algebraically produce outputs on opposite sides of the pass/fail threshold, or whether the gauge effect cancels after final decryption.

This is a static component-algebra screen and does not authorize Codex, native execution, B176, parameter changes, or route selection.

Research-GPT-provided evidence digests:

```text
REPORT_SHA256:       b3b19522daa985736a98aebe2e32362b53b88d647332b48123994f9c78e481d0
WITNESS_JSON_SHA256: 1c8f910a3ec5baa4411970af7fb5bd5146eac4af25105d2756b0f13d2fc6dbda
```

These digests identify the in-conversation report/witness data generated during the static audit; no separate binary artifact was persisted by the Research GPT in this turn.
