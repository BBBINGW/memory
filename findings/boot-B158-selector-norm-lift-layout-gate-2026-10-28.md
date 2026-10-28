# BOOT — B158 selector norm, lift, and simple-layout gate

Date: 2026-10-28
TRACK_ID: BOOT

## Inputs and exact implementation context

B163 evidence artifact:
`BOOT-B163-B158-CORRECTED-NORESCALE-SI-NATIVE-20261028.zip`
SHA-256:
`bb35766751a0439de8e92db3668082930afc84fa49b32ae44b8df093ce85bfad`

B163 fixed point:
- N = 32768
- T = 65537
- L18, logQ = 649
- selector scale = 1
- selector Rescale = 0
- fused ct-ct = `MulRelinScaleInvariantNew`

Lattigo v6.2.0 batching encoder was reconstructed exactly from
`schemes/bgv/encoder.go`:
- slot values are placed with `permuteMatrix`;
- `EncodeRingT` applies RingT INTT;
- `EmbedScale(..., scaleUp=true)` maps the RingT polynomial into Q.

The reconstructed encoder was sanity-checked: all-one slots encode to coefficient polynomial 1.

## Exact selector polynomial norms

For the left-row B158 stage selector
[
M_k(i)=1 iff i mod 2k ge k,qquad 0le i < H, H=16384,
]
with the right row zero, let (widetilde M_k) be the unique centered integer coefficient lift modulo T.

Exact values:

| k | nonzero centered coefficients | ||M_k||_1 | log2 ||M_k||_1 |
|---:|---:|---:|---:|
| 1 | 4 | 17,476 | 14.093 |
| 2 | 6 | 85,825 | 16.389 |
| 4 | 10 | 170,813 | 17.382 |
| 8 | 18 | 196,597 | 17.585 |
| 16 | 34 | 464,048 | 18.824 |
| 32 | 66 | 1,151,314 | 20.135 |
| 64 | 130 | 2,162,619 | 21.044 |
| 128 | 258 | 4,009,120 | 21.935 |
| 256 | 514 | 8,248,261 | 22.976 |
| 512 | 1,026 | 17,213,193 | 24.037 |
| 1024 | 2,050 | 33,570,588 | 25.001 |
| 2048 | 4,098 | 67,235,096 | 26.003 |
| 4096 | 8,194 | 134,115,624 | 26.999 |
| 8192 | 16,386 | 269,549,952 | 28.006 |

For k >= 32 the norm grows by approximately one bit per doubling.

The fixed right-half selector R has:
- centered nnz = 2
- centered ||R||_1 = 32,896
- log2 ||R||_1 = 15.006

## Direct match to B163 measured noise

For M_k * RowRotation(S_k), measured increases in required_logQ are:

| mask k | measured delta bits | log2 centered ||M_k||_1 |
|---:|---:|---:|
| 2 | 17 | 16.389 |
| 4 | 16 | 17.382 |
| 8 | 17 | 17.585 |
| 16 | 18 | 18.824 |
| 32 | 18 | 20.135 |
| 64 | 20 | 21.044 |
| 128 | 22 | 21.935 |
| 256 | 23 | 22.976 |
| 512 | 23 | 24.037 |
| 1024 | 26 | 25.001 |
| 2048 | 20 | 26.003 |
| 4096 | 26 | 26.999 |

Pearson correlation between measured delta and log2 centered L1 is approximately 0.87.

For the fixed R selector, every reached stage increases required_logQ by 16 or 17 bits, matching the 15.006-bit centered-L1 operator scale up to the expected slack/rounding/key-noise terms.

Therefore:
`SELECTOR_HIGH_NORM_MECHANISM = PASS`.

The public 0/1 slot masks are not small plaintext multipliers in coefficient norm. They are a major, quantitatively verified source of B163's noise growth.

## Equivalent coefficient lifts: strong negative gate

Let a = (a_i) be any integer coefficient lift of a RingT selector polynomial. Every equivalent lift is
[
a_i = widetilde a_i + T z_i,
]
where (widetilde a_iin[-(T-1)/2,(T-1)/2]) is the unique centered representative.

Coefficientwise,
[
|a_i|ge |widetilde a_i|.
]

Hence the centered lift simultaneously minimizes:
- coefficient L1 norm;
- coefficient L2 norm;
- the exact l_infinity-to-l_infinity norm of negacyclic convolution, whose row sum is ||a||_1.

Thus no equivalent coefficient lift can beat the centered selector for the worst-case coefficient-noise multiplication norm.

Lattigo's standard RingT-to-Q embedding uses the canonical RingT residue polynomial. A custom centered Q lift could reduce the canonical L1 norm, but the available theoretical headroom is small at the late masks:
- k=1024: about 1.01 bit;
- k=2048: about 1.01 bit;
- k=4096: about 1.01 bit;
and B163's measured selector growth already tracks the centered norm rather than the larger canonical norm.

Decision:
`ALTERNATIVE_COEFFICIENT_LIFT_RESCUE = FAIL_STRONG`.
Do not spend a native round on centered/alternative lifts alone.

## Automorphism / simple slot-reindex gate

A ring automorphism X -> X^g in the power-of-two cyclotomic ring permutes coefficient positions up to signs. Therefore it preserves coefficient L1 exactly.

So a Galois relabeling of an existing selector cannot reduce its convolution norm.

We also tested GF(2)-linear relabelings of the 14 physical left-row index bits. For each pivot bit j <= 10, every parity combination with that highest pivot was exhaustively checked. For j >= 11, hundreds of random lower-bit combinations were checked.

Best improvements over the standard single-bit mask:
- exact j=5: 0.229 bit;
- exact j=6: 0.237 bit;
- exact j=7: 0.049 bit;
- exact j=8: 0.071 bit;
- exact j=9: 0.108 bit;
- exact j=10: 0.060 bit;
- sampled j=11..13: below 0.04 bit in the tested sets.

The natural mask order is also already almost monotonically increasing in norm. Under a multiplicative norm bound, merely permuting the 14 coordinate masks leaves the product of selector amplification factors invariant; using the largest masks earlier only worsens prefix budgets.

Therefore:
- `SIMPLE_GALOIS_REINDEX = FAIL`
- `BIT_REVERSAL_RESCUE = FAIL`
- `GRAY_OR_GF2_LINEAR_REINDEX = LOW_VALUE / FAIL_CURRENT_GATE`

This does not rule out a genuinely different ciphertext representation or non-linear/non-coordinate slot layout.

## Consequence for B158 rescue strategy

The selector problem is now structural:
an exact linear map that applies M_k to an already-noisy ciphertext also applies the same ring multiplication operator to its existing error. Key-switch fusion alone cannot erase this inherited M_k * e term without a refreshing mechanism.

Remaining meaningful escape routes must therefore do at least one of:
1. construct the x^k-dependent factor from an independent cleaner ciphertext, so M_k does not multiply the noisy recurrent B158 state;
2. change the recurrence/state representation so the M_k projection is not required;
3. refresh/change error representation before the selector;
4. use a ring-switch/leaf representation in which the needed interaction is materially cheaper.

## New structural lead from current literature

Liang--Ding, ePrint 2026/1779 (latest public revision 2026-10-26), demonstrates BGV/BFV ring switching to smaller leaf rings and reports that smaller-ring bootstrapping can be practical. Their BGV experiments use N=2^16 -> n=2^15 and explicitly account for Split/Merge/key-switch costs.

This does not directly solve B158:
B158's top ring is already N=2^15, and blindly switching to n=2^14 at the full 649-bit modulus is likely security-constrained. Also, the co-packed B158 state does not expose x^k as a standalone constant polynomial.

However it suggests a precise next paper-level gate:
can a clean auxiliary x^(2^i) chain be kept in a lower-cost leaf representation and injected into only the late B158 factors, without restoring the original 28 full-ring multiplications and without violating leaf-ring security?

Status:
`B158_RING_SWITCH_CLEAN_FACTOR = OPEN_PAPER_GATE`.

No native experiment, Codex run, or security/parameter change was performed.
