# BOOT fresh candidate — co-packed EvalPower for ePrint 2026/975

Date: 2026-10-28
TRACK_ID: BOOT
Status: PARK_VALUE_MARGINAL
No Codex / GPU / remote run used.

## Source

Full PDF for ePrint 2026/975 was available in the user's file library and audited.
Author implementation:
xiaopeng-stu/bfv-functional-bootstrapping

The paper's single-ciphertext 9-bit functional bootstrap has:
- N=32768, m=1
- paper online total 3.149 s
- paper EvalPower 1.625 s
- paper Step 1 1.365 s

The current author repository is materially faster:
- average online total 2.061226016 s
- Step 1 = 0.693407006 s
- poly eval total = 1.284264686 s
- BuildBasis / P = 1.141456575 s
- ParallelLT = 0.097897990 s
- final key switch = 0.079953212 s

Thus BuildBasis remains the dominant individual online stage even after later engineering.

## Candidate idea

For m=1, exploit the repeated-slot representation to co-pack:
- the current generated power block, and
- the next auxiliary power x^(2^i)

inside one ciphertext.

A recurrence can be written using a row swap tau and public selector masks:
F_i = M_grow * tau(S_i) + M_aux * S_i + M_keep,
S_{i+1} = S_i * F_i.

At plaintext level, this lets the same ciphertext-ciphertext multiplication both:
1. extend the power block, and
2. square the auxiliary power for the next layer.

Exact symbolic/small-parameter checks found no algebraic counterexample.

## Precision / level gate

PASS at the API/semantics level.

Lattigo v6.2 BFV uses the scale-invariant BGV evaluator. For []uint64 plaintext-vector operands:
- plaintext scale is explicitly set to 1,
- MulScaleInvariant on a degree-0 plaintext uses tensorStandard,
- ciphertext level is preserved,
- no rescale is required merely for the 0/1 selector mask.

Therefore the selector masks do not automatically double multiplicative depth.

Important correction:
A correct recurrence requires two masked ciphertext contributions per layer (grow and aux), plus a public keep-1 region. The earlier verbal one-mask simplification is too optimistic.

## Value gate

FAIL / marginal headroom.

Author implementation structure:
- original BuildBasis for s=32768 has ell=15
- approximately 28 ciphertext-ciphertext multiplications plus 15 plaintext-ciphertext multiplications
- runtime = 1.141456575 s

Candidate would save roughly 13-14 ciphertext-ciphertext multiplications but add roughly 14 row rotations plus two scale-neutral selector-mask multiplications per layer.

The author's Step 1 for m=1 is a useful native cost proxy:
- exactly one plaintext-ciphertext multiply plus log2(min(r,n)) = 11 high-level rotations
- runtime = 0.693407006 s

Thus high-level rotations are already tens of milliseconds each and are the same order as the ciphertext multiplications being removed.

Accounting for falling modulus levels makes later candidate rotations cheaper, but a Q-limb-scaled estimate still places the added rotation cost at roughly 0.4-0.55 s. This is comparable to the optimistic savings from removing 13-14 ciphertext multiplications, before adding:
- two selector-mask ct-pt operations per layer,
- additions,
- extra rotation keys / key memory,
- implementation overhead.

Decision:
- ALGEBRA: PROMISING / NO COUNTEREXAMPLE FOUND
- LEVEL/PRECISION API GATE: PASS
- NATIVE VALUE HEADROOM: MARGINAL
- IMPLEMENTATION: NOT WARRANTED
- STATUS: PARK_VALUE_MARGINAL

Do not spend Codex/native quota unless a new way removes the added rotations or shares them with an already mandatory stage.
