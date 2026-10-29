# BOOT RMFE R8 Exact Plaintext Map Generator Gate

Date: 2026-10-29  
Session: 密码学 11.0, Research Turn 13/25  
Classification: `PASS_STATIC_RMFE_R8_EXACT_PLAINTEXT_MAP_GENERATOR`

## Scope

This was a source-fixed, algebraic gate for the reversible provisional candidate `RMFE_SUBRING_ENVELOPE_SINGLE_MULTKEY`. It did not use Codex, generate keys, run native code, execute `InnerProduct`, propagate the full fixed-`Q` capacity ledger, benchmark, or test DFR.

The orchestrator's durable `ACTIVE_SUBLINE` remains `B158_CHECKPOINT_DECOUPLED_HALF_BASIS`. RMFE remains provisional, not validated.

## Fixed interface

```text
S = Z/625Z
A = S[Y]/(Y^16 + 1)
F0 = Y^8 + 182
F1 = Y^8 + 443
T = [1, 15]
G = F0
```

The accepted convention is the power basis (`normal_basis=false`). HElib's inverse-map default `normal_basis=true` would add a basis transform and invalidate the coefficients in this gate.

Slot ordering is

```text
(s_0,0, ..., s_0,7, s_1,0, ..., s_1,7)
```

and coefficient ordering is `(c_0, ..., c_15)`.

## Exact bidirectional maps

Let `V` be coefficient-to-slot and `W = V^-1` be slot-to-coefficient. Entries are centered modulo 625; unlisted entries are zero.

| Row | `V`: coefficient to slot | `W`: slot to coefficient |
|---:|---|---|
| 0 | `0:1, 8:1` | `0:-312, 8:91` |
| 1 | `1:1, 15:-182` | `1:-312, 9:91` |
| 2 | `2:1, 14:182` | `2:-312, 10:91` |
| 3 | `3:1, 13:-182` | `3:-312, 11:91` |
| 4 | `4:1, 12:182` | `4:-312, 12:91` |
| 5 | `5:1, 11:-182` | `5:-312, 13:91` |
| 6 | `6:1, 10:182` | `6:-312, 14:91` |
| 7 | `7:1, 9:-182` | `7:-312, 15:91` |
| 8 | `0:-182, 8:182` | `0:-312, 8:-91` |
| 9 | `1:-182, 15:1` | `7:91, 15:-312` |
| 10 | `2:-182, 14:-1` | `6:-91, 14:312` |
| 11 | `3:-182, 13:1` | `5:91, 13:-312` |
| 12 | `4:-182, 12:-1` | `4:-91, 12:312` |
| 13 | `5:-182, 11:1` | `3:91, 11:-312` |
| 14 | `6:-182, 10:-1` | `2:-91, 10:312` |
| 15 | `7:-182, 9:1` | `1:91, 9:-312` |

Exact modular checks establish

```text
V * W = W * V = I_16 (mod 625)
```

All 16 basis images pass in both directions. The five retained RMFE coordinates in both slots pass `10/10`; the padding coordinates 5, 6, and 7 also pass.

## Exact automorphism-multiplier generator

The map is represented as

```text
L(f) = sum_{u in (Z/32Z)^*} a_u(Y) f(Y^u).
```

For each row below, coefficients correspond to `(Y^0,Y^2,Y^4,Y^6,Y^8,Y^10,Y^12,Y^14)`; all odd-power coefficients vanish.

```text
 u   S2C a_u                                  C2S a_u
 1  -25,  92, -92,  92, 266, 131,-131, 131   129, 184,-184, 184,-171, 262,-262, 262
 3 -131, -92, -92, -92, -92, 131, 131, 131   184, 262, 262, 262, 262,-184,-184,-184
 5   92,-131, -92, 131, 131,  92,-131, -92  -262,-262,-184, 262, 184, 184,-262,-184
 7   92,-131, -92, 131,-131, -92, 131,  92  -262, 184, 262,-184, 184, 262,-184,-262
 9  131,-131,  92, 131, -92,  92, 131, -92  -184,-262, 184, 262,-262, 184, 262,-184
11 -131,-131,  92, 131, -92, -92,-131,  92   184, 184,-262,-184, 262, 262, 184,-262
13   92,  92,  92,  92, 131, 131, 131, 131  -262, 184, 184, 184, 184, 262, 262, 262
15 -175, -92,  92, -92,-287, 131,-131, 131   272, 262,-262, 262,-128,-184, 184,-184
17  131, -92, -92, -92, -92,-131,-131,-131  -184,-184,-184,-184,-262,-262,-262,-262
19 -131,  92, -92,  92, -92,-131, 131,-131   184,-262, 262,-262, 262, 184,-184, 184
21   92, 131, -92,-131, 131, -92,-131,  92  -262, 262,-184,-262, 184,-184,-262, 184
23   92, 131, -92,-131,-131,  92, 131, -92  -262,-184, 262, 184, 184,-262,-184, 262
25  131, 131,  92,-131, -92, -92, 131,  92  -184, 262, 184,-262,-262,-184, 262, 184
27 -131, 131,  92,-131, -92,  92,-131, -92   184,-184,-262, 184, 262,-262, 184, 262
29   92, -92,  92, -92, 131,-131, 131,-131  -262,-184, 184,-184, 184,-262, 262,-262
31   92,  92,  92,  92,-131,-131,-131,-131  -262,-262,-262,-262, 184, 184, 184, 184
```

The exact outer lift is `Y^j -> X^(1024j)`. All 16 multipliers are nonzero; the source-faithful direct realization therefore requires exactly the 15 nonidentity automorphism exponents

```text
{3,5,7,9,11,13,15,17,19,21,23,25,27,29,31}.
```

An eight-exponent custom CRT flattening convention would change the source-fixed basis and is outside this gate.

## Canonical norm evidence

| Multiplier class | infinity norm | l1 norm | squared l2 norm | canonical embedding max |
|---|---:|---:|---:|---:|
| S2C, `u=1` | 266 | 960 | 148256 | 549.335671998462 |
| S2C, `u=15` | 287 | 1131 | 189869 | 512.191722764159 |
| S2C, each other `u` | 131 | 892 | 102500 | 580.204661394532 |
| C2S, `u=1` | 262 | 1638 | 353382 | 1106.707577524031 |
| C2S, `u=15` | 272 | 1738 | 397868 | 829.309015670558 |
| C2S, each other `u` | 262 | 1784 | 410000 | 1160.409322789064 |

Aggregate statistics:

```text
S2C: 128 nonzero coefficients; infinity norm 287; total l1 14579; total squared l2 1773125
C2S: 128 nonzero coefficients; infinity norm 272; total l1 28352; total squared l2 6491250
```

The outer lift preserves the canonical embedding maxima.

## Accepted boundary

Established in this static gate:

- pinned source ordering and power-basis interface;
- exact bidirectional 16-by-16 maps;
- all 16 basis images;
- five retained coordinates in both slots;
- exact outer lift;
- exact direct automorphism support and multiplier norms.

Not established:

- native execution or key generation;
- key memory or security closure;
- `InnerProduct` correctness;
- full fixed-`Q` capacity/noise propagation;
- runtime, DFR, benchmark, full B158 correctness, novelty, or paper contribution.

```text
VALIDATED_CANDIDATE: NO
RESEARCH_FRONTIER_EXHAUSTED: false
```

Next cheapest decisive test: `BOOT-RMFE-R8-EXACT-MAP-FIXED-Q-CAPACITY-LEDGER-GATE`, a static propagation of the exact 15-automorphism map costs and measured multiplier-norm envelope through the proposed single-multiplication pipeline before key generation or native execution.
