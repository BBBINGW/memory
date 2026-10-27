# BOOT-B137 — Direct consumption of the coefficient-packed 2026/2119 blind-rotation key

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Parent: BOOT-B135 full-source audit of ePrint 2026/2119
- Status: COMPLETE
- Decision: FAIL_LINEAR_DIRECT_CONSUMPTION / FAIL_PARTIAL_EXPANSION_CACHE / NONLINEAR_ESCAPE_IS_PRIOR_ART_FAMILY
- CODEX_REQUIRED: NO
- Native benchmark: NOT JUSTIFIED
- Novelty: NOT_ESTABLISHED

## Question

ePrint 2026/2119 compresses the secret-dependent blind-rotation key to four coefficient-packed RLWE ciphertexts for transmission, then performs one-time homomorphic expansion/reconstruction and keeps the much larger evaluation-ready selector key resident on GPU.

Can narrow blind rotation consume the four packed ciphertexts directly, avoiding materialization of all evaluation-ready selectors while preserving low steady-state latency?

## Source interface

For a head block x, after the paper's complex packing, the narrow factor is computed from g encrypted candidate selectors and two transformed public tables. Abstracting one real selector family, one output coordinate has the form

[
F_i(b,z)=sum_{y=0}^{g-1} b_y z_{ho_y(i)},
]

where:
- (b_y) is the encrypted one-hot selector coordinate for candidate y;
- (z_{ho_y(i)}) is the public table entry obtained from the corresponding rotation;
- for fixed i, the g table locations are distinct in the legal candidate window.

The coefficient-packed key instead stores all (b_y)'s as coefficients of a small number of RLWE ciphertexts.

## Gate 1: bilinear-rank obstruction for linear direct consumption

Consider any online construction that:
1. applies arbitrary public linear transforms to the packed encrypted selector;
2. applies arbitrary public linear transforms to the public table;
3. lets selector-dependent and table-dependent quantities interact only through R ciphertext-plaintext multiplicative channels;
4. linearly combines their outputs.

At a fixed output coordinate i, each such channel contributes one separable bilinear term

[
ell_r(b),m_r(z).
]

Therefore the resulting bilinear form has matrix rank at most R.

But the target map

[
F_i(b,z)=sum_{y=0}^{g-1} b_y z_{ho_y(i)}
]

has a g-by-n coefficient matrix containing g independent unit columns, hence rank exactly g.

Therefore

[
Rge g.
]

Correctness only needs to hold on one-hot selectors, but this does not invalidate the argument for a construction linear in b: correctness on the basis vectors (e_y) uniquely fixes its linear extension to all b.

### Two-sign case

Before complex selector packing, the positive and negative selector families are independent and require the corresponding signed/conjugated public tables. Over the natural real-linear model the same argument gives two g-dimensional selector families. This is consistent with 2026/2119's explicit observation that complex real/imag key packing halves the key ciphertext count but **does not halve the 2g table-selector multiplication count**.

### Scope

This is a model-specific lower bound:
- it kills a purely linear "four packed ciphertexts -> a few selector/table products" shortcut;
- it is NOT a universal FHE lower bound;
- ciphertext-ciphertext multiplication, encrypted binary index circuits, Mux/CMux, or other nonlinear selector processing can escape it.

## Gate 2: streaming / partial expansion tradeoff

The paper's packed-key expansion is a complete binary substitution tree. For one packed polynomial with N indicator coefficients:
- full expansion has N leaves;
- there are N-1 internal nodes;
- each internal node requires a substitution plus key switching.

Suppose setup stores all nodes at depth d instead of all leaves. Let

[
M=2^d
]

cached ciphertexts remain resident.

To finish expansion online, the M subtrees together still contain N leaves and therefore have

[
N-M
]

internal nodes.

Thus, for the same expansion algorithm,

[
	ext{online KS/substitution cost}=N-M.
]

Equivalently, if the resident-memory fraction is

[
r=M/N,
]

the remaining expansion fraction is exactly

[
1-r.
]

This is an endpoint-like tradeoff:
- save 90% of expansion-tree resident states -> still pay 90% of full expansion every bootstrap;
- reduce online expansion to 1% -> cache 99% of the leaf-equivalent states.

Because every candidate selector is used by some block, aggregate narrow blind rotation does not leave a large subset of leaves unused.

Decision:
**FAIL_PARTIAL_EXPANSION_CACHE** for the paper's existing binary expansion tree as a low-latency memory solution.

## Gate 3: nonlinear compact-selector escape

A nonlinear representation can beat the linear rank gate by encoding a secret index with (O(log g)) encrypted bits and evaluating a secret rotation through Mux operations.

This is not new:
- SHIP already gives a Mux blind-rotation whose cost is logarithmic in the encrypted-index range but uses more expensive sequential key-switching;
- SHIP explicitly combines the column and Mux methods in a baby-step/giant-step style hybrid;
- SHIP's experiments report that the hybrid is faster than either pure endpoint for its CPU cost model.

Therefore "replace one-hot column selectors by compact encrypted index bits / factor the selector range and use Mux" falls directly into the SHIP prior-art family.

The 2026/2119 paper deliberately moves back toward the column-style linear selector representation because cheap parallel plaintext-ciphertext products and the sparse-matrix GPU formulation beat the more sequential Mux path in their target system.

Decision:
**NONLINEAR_ESCAPE_EXISTS_BUT_PRIOR_ART_FAMILY.**

## Implication

The four-ciphertext packed representation is a good transmission/setup representation, but under the current algorithm it is not also a free steady-state evaluation representation.

There is a structural reason for the paper's design:
- low storage representation hides g independent selector coordinates;
- the fast online column-style blind rotation needs those g independent channels;
- materializing them once moves the unavoidable linear separation work out of the latency-critical path.

## B137 decision

- Purely linear direct consumption: **FAIL** by a rank-g bilinear obstruction.
- Partial cached expansion of the same binary tree: **FAIL VALUE**; memory saved and online expansion cost trade almost one-for-one.
- Compact nonlinear secret-index representation: **already the SHIP Mux/hybrid design space**.
- CODEX/native: **NO**.
- Branch: **PARK**.

## Next candidate

Move away from packed-key direct consumption.

Highest-value new local question in 2026/2119:

> The NTT-fusion section still performs 2h forward NTTs, one for each block-specific base table and sign transform. But all block-specific tables are derived from shifted windows of the same public ciphertext polynomial a. Can the block index x be represented as an NTT-domain permutation / phase / fixed linear correction so that the 2h base-table NTTs collapse to O(1) or O(log h) transforms without restoring the full SHIP table width?

This should be tested algebraically before any implementation.
