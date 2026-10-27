# BOOT post-B156 — ePrint 2026/2368 × 2026/1200 character-output composition gate

Date: 2026-10-27
TRACK_ID: BOOT
State impact: NONE. Do not modify B157 pending state.
No Codex / GPU / remote execution was used.

## Sources

Target A:
- ePrint 2026/2368, Cheon–Cho–Jung–Lim,
  *Low-Latency Parallel Digit Decomposition and Sign Evaluation for CKKS*.
- Full PDF acquisition through the configured ePrint/mirror path is blocked (IACR HTTP 403; no exact arXiv; fixed mirror missing).
- Therefore all claims about 2368 below are restricted to its public abstract / indexed abstract:
  - all u radix-B digits are extracted in parallel with one bootstrapping;
  - each tentative digit differs by at most one carry from below;
  - carry look-ahead corrects all carries in O(log u) depth;
  - lookup depth O(log B);
  - slot cost Theta(u) per input;
  - reported 2.04x for ten radix-64 digits and 7.83x for sign on 1024 real input pairs at 2^-60 separation;
  - modulus consumption for p-bit separation changes from Theta(p^2) polynomial-approximation regime to Theta(p).

Target B:
- ePrint 2026/1200, Dumezy–Suvanto,
  *Character Block Encodings for Discrete CKKS: Single-Level LUTs and Low-Depth Arithmetic* (ASIACRYPT 2026).
- Public author page + companion repo jdumezy/ckks-block-encoding were available.
- Character/block encoding stores a finite-alphabet value in coordinates forming a character/function basis.
- Any LUT becomes an affine plaintext map in one multiplicative level.
- Modular reduction is native to the representation.
- Radix finite-state scans support add/sub and equality/comparison at O(log d) depth.

Prior-art C:
- ePrint 2026/1385 / ISC 2026,
  Shokri–Tsoutsos,
  *Walsh LUT Evaluation on Lazy Bits for CKKS AES Transciphering*.
- Public implementation repo TrustworthyComputing/aes-walsh-ckks.
- The implementation keeps AES state as separate lazy bit ciphertexts and evaluates Walsh S-boxes directly on that decomposed representation rather than first reconstructing ordinary byte scalars.
- It explicitly packs parity masks, batch-EvalMods them, and uses hoisted rotations.

## Observed standard -> block conversion bottleneck in 2026/1200 artifact

The 1200 artifact implements EvalSplitFromStandard as a bootstrap-like conversion:
1. SlotsToCoeffs
2. ScaleDown
3. ModUp
4. CoeffsToSlots
5. evaluate character coordinates through EvalMod-style finite maps

For reduced BRU, direct coordinates are generated in parallel; larger coordinates are completed using a power basis.

Committed single-thread LogN=15 benchmark results:

- t=4  (log2 t=2): from_standard mean ~5.16 s, 9 levels
- t=8  (log2 t=3): ~8.29 s
- t=16 (log2 t=4): ~14.62 s
- t=32: ~15.61 s
- t=64: ~16.13 s
- t=128: ~17.36 s

The amortized per packed input is sub-ms to ~1.1 ms because many slots are filled, but the invocation latency is large.

Thus, for small-batch / latency-sensitive workloads, eliminating a separate standard->block conversion bootstrap could be material.

## Conditional idea: CV-PDD

Candidate name:
CV-PDD = Character-Valued Parallel Digit Decomposition.

Desired interface:
- Input: ordinary CKKS scalar x.
- Use the 2368 one-bootstrap parallel digit-decomposition architecture.
- Instead of outputting corrected scalar digits d_i in {0,...,B-1}, directly output character/block coordinates
  chi_k(d_i) = omega^(k d_i)
  for the encoding used by 1200.

The key algebraic compatibility is carry correction.

If a tentative digit is corrected by a carry bit c in {0,1}, then

chi_k(d+c) = chi_k(d) * chi_k(c),

and

chi_k(c) = 1 + c * (omega^k - 1).

Therefore once a carry bit is known, correcting a character coordinate needs only:
- an affine function of c,
- one multiplication with the tentative character coordinate.

No scalar-digit reconstruction is algebraically necessary.

The existing 1200 representation then supports subsequent LUTs / modular arithmetic directly.

## Why the idea is only conditional

The full 2368 paper is unavailable, so we cannot verify:
- exact tentative-digit variable;
- whether its low-precision per-digit lookup can output arbitrary codomains without changing depth/noise;
- whether carry state requires the scalar digit itself or only finite generate/propagate predicates;
- whether its bootstrap layout permits replicating each digit into multiple character-coordinate slots without additional expensive transforms.

The public abstract is not enough to assert these interfaces.

STATUS:
- 2368_LOOKUP_CODOMAIN_INTERFACE: SOURCE_REQUIRED
- CV_PDD_CORRECTNESS: CONDITIONAL

## Representation expansion / packing cost

A reduced BRU encoding for a radix-B digit uses B-1 character coordinates.

2368 alone costs Theta(u) slots/input for u digits.

A packed CV-PDD output would cost roughly:

u * (B-1)

coordinates/input.

Example:
- 2368 benchmark: B=64, u=10 -> ~630 coordinates/input, versus ~10 digit slots/input.
  This is about a 63x representation expansion relative to scalar digits.
- For a 60-bit word with radix 4:
  u=30, B-1=3 -> ~90 coordinates/input.
  This is much more plausible but uses more digits and a deeper carry tree than radix 64.

The 1200 artifact itself defaults to small radix (radix 4), consistent with the fact that character-block encodings favor small alphabets.

Thus the potentially useful regime is:
- small B,
- latency-sensitive / underfilled SIMD workloads,
- many subsequent LUT/arithmetic operations after conversion.

It is not attractive as a generic high-throughput replacement for 2368's radix-64 benchmark.

## Prior-art collision

### 2026/1200

1200 already establishes:
- change representation rather than optimize each LUT;
- arbitrary LUT as a linear/affine map in character basis;
- carry/prefix arithmetic directly in block encoding.

Thus "characters make digit LUTs cheap" is prior art.

### 2026/1385

1385 establishes the broader design pattern:
- retain a decomposed/lazy representation after conversion;
- apply the next nonlinear LUT directly in that representation;
- avoid reconstructing the conventional scalar/byte representation.

Thus "fuse decomposition with a downstream alternate representation" is not a new high-level principle.

### 2026/2368

2368 already fuses digit extraction and carry processing inside one bootstrap/decomposition pipeline.

Without full text, we cannot exclude that arbitrary final digit functions / alternate output codomains are already discussed.

## Value judgment

Potential benefit:
- could remove a separate standard->block conversion invocation whose public 1200 small-batch latency is seconds on one thread;
- could create a direct bridge from ordinary CKKS values into 1200's low-depth arithmetic representation.

But:
- output representation expands by B-1 coordinates per digit;
- the useful regime shifts toward small radix;
- the broad representation-fusion principle is already present in 1200 and 1385;
- the remaining contribution looks like a natural composition unless 2368's exact carry algebra exposes a nontrivial obstacle.

Decision:
- CV_PDD_VALUE: CONDITIONAL
- CV_PDD_NOVELTY: LOW / NATURAL_COMPOSITION
- CV_PDD_SOURCE_STATUS: BLOCKED_ON_2368_FULL_TEXT
- CV_PDD_NATIVE_PRIORITY: NO
- CURRENT_ACTION: PARK

Do not spend Codex/native resources on CV-PDD before acquiring and reading 2026/2368 full text.

## Strategic implication

2368 + 1200 + 1385 jointly indicate that the CKKS nonlinear-function space is becoming saturated along three axes:
1. digitize in parallel;
2. change finite-alphabet representation so LUTs are cheap;
3. keep lazy/decomposed representations across nonlinear layers.

Future BOOT candidates should not merely combine these abstractions. A higher-value direction must change:
- the number of bootstraps,
- asymptotic modulus/depth law,
- ring/security parameters,
- or a stage that these representations still fundamentally require.
