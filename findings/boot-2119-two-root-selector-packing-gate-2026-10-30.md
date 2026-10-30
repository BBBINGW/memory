# BOOT — ePrint 2026/2119 two-root narrow-selector packing gate

Date: 2026-10-30
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Session: 密码学 15.0 — Research Turn 5/25

Status:
PASS_TWO_ROOT_NARROW_SELECTOR_PACKING /
FAIL_FOUR_PACKED_SELECTOR_ROOTS_ARE_NECESSARY /
HALVE_PACKED_SELECTOR_ROOT_STORAGE /
HALVE_COEFFICIENT_DECOMPRESSION_TREES /
ONLINE_EVALUATION_READY_KEY_AND_8P2MS_PATH_UNCHANGED /
FULL_NOISE_DFR_NATIVE_NOVELTY_UNVERIFIED

## Reprioritization

Independent of the families closed/parked in Turns 1–4:
- SPRU stride=2 custom cryptanalysis;
- FHEW AKU matched-DFR repair;
- LFBS PRCA one-automorphism-per-level aggregation;
- FAB bounded-gap exact sampler/security boundary.

The selected fresh source is:
Rending Ouyang, Jian Liu, Peimin Gao, Pan Xiao, Heng Zhang, Man Ho Au,
Cong Zhang, Kui Ren, Chun Chen,
"CKKS Bootstrapping in less than 10ms", ePrint 2026/2119.

Supplied source:
papers/supplied/2026-2119.pdf
Git blob SHA: 5de485db8242148144f74de0c857cfcd698f0f35
35 physical pages.

The public ePrint source could not be freshly acquired by Research MCP (HTTP 403)
during this turn, so source-specific claims below are for this supplied PDF.
Current-version byte parity is not asserted.

## Source context

The paper builds on SHIP and introduces:
- narrow blind rotation;
- real/imag packing of positive/negative selectors;
- NTT-permutation fusion;
- coefficient packing of the persistent blind-rotation key;
- low-depth FBS.

Its GPU implementation reports 8.2 ms for one LL13 complex ciphertext and
4.6 ms amortized at batch size 64 on an RTX PRO 6000. Key reconstruction is
explicitly treated as a one-time setup cost and excluded from bootstrapping timing.

Section 6 packs the persistent blind-rotation key into four ciphertexts:
for i in [4],

    p_i(X) = sum_{j=0}^{N-1} b_{iN+j} X^j,
    ct_i <- Enc(p_i(X)).

Each ct_i is decompressed by a binary substitution tree. A tree has N-1 internal
nodes and hence N-1 substitutions/key switchings. Section 6.3 then applies public
slot masks to the replicated decrypted bits to reconstruct the head and packed-tail
selectors needed by the narrow blind rotation.

## Primary hypothesis

The four coefficient-packed selector roots of Section 6 are necessary to recover
the narrow blind-rotation selectors while preserving the same online algorithm.

Cheapest decisive falsifier:
trace the actual private selector information in Sections 3–4. If both head and
tail selectors depend only on the same two private candidate-sign indicator
families, and their differing layouts are public masks applied after decompression,
then only two packed roots are required.

## 1. The narrow selector secret information is only two bit families

Fix a secret block x and candidate offset y. Let the unique nonzero position in
the block be o_x and its sign be s_x in {+1,-1}.

Define the two private bits

    b^+_{x,y} = 1[y=o_x and s_x=+1],
    b^-_{x,y} = 1[y=o_x and s_x=-1].

Section 3.3 head computation uses exactly these two selector bits:
the positive head selector is b^+ multiplied by the public head-slot mask,
and the negative head selector is b^- multiplied by the same public mask.

Section 3.4 tail computation uses the SAME sign/candidate conditions. The only
difference is the public tail layout:
for each block the selected bit is placed into the last g-1 positions of that
block's 2(g-1)-slot packed group; the rest are public zeros.

Section 4 then complex-packs the positive and negative selector plaintexts as

    selector^complex = selector^+ + i selector^-.

Therefore the private information required after narrow-table transformation is
only the two arrays {b^+_{x,y}} and {b^-_{x,y}}.

The head/tail distinction is not private information.

## 2. Two coefficient-packed roots suffice

Index the candidate positions j=xg+y in the same public ordering used by the
current packing. Define

    P_+(X) = sum_j b^+_j X^j,
    P_-(X) = sum_j b^-_j X^j.

Key generation publishes only

    C_+ = Enc(P_+(X)),
    C_- = Enc(P_-(X)),

together with the same substitution-key set already required by Section 6.

Apply the paper's exact binary coefficient-decompression tree independently to
C_+ and C_-.

After log2 N depths, for every candidate j this yields ciphertexts encrypting the
replicated scalar bits b^+_j and b^-_j, up to the same public ordering and N
normalization already handled by the source.

Now reconstruct:

### Head
Multiply the positive and negative replicated leaves by the public head mask

    H = 1_(n-g+1) || 0_(g-1)

and complex-pack them exactly as in Section 4.

### Packed tail
For each tail pack, multiply the SAME replicated b^+_j/b^-_j leaves by the public
block-placement masks from Section 3.4/6.3, add them into the packed layout,
and complex-pack the two signs.

These are exactly the selector plaintexts consumed by the existing narrow blind
rotation.

No new secret-dependent function is introduced.

## 3. Exact equivalence argument

For every candidate j, the source narrow selector plaintexts are public-linear
functions of the pair (b^+_j,b^-_j).

Let L_H and L_T denote the public linear maps that respectively place a replicated
indicator into the head layout and into its assigned packed-tail layout.

Then

    kappa_H(j) = L_H(Enc(b^+_j)) + i L_H(Enc(b^-_j)),
    kappa_T(j) = L_T(Enc(b^+_j)) + i L_T(Enc(b^-_j)).

Because RLWE encryption, addition, plaintext multiplication/masking, and the
source decompression tree are linear at this interface, deriving both selector
layouts from the same pair of leaves preserves the intended plaintexts exactly.

The rest of Sections 3–5 is unchanged.

Hence four independent coefficient-packed roots are not required for functional
correctness of the narrow selector reconstruction.

## 4. Relation to original SHIP four masks

SHIP Lemma 1 expresses the rotated secret contribution using four public-table
branches and four secret-dependent masks. For a fixed secret position/sign,
those masks are products of:
- the positive/negative sign indicator, and
- public slot masks m_j or (1-m_j), with table-half/sign choices.

The 2026/2119 narrow construction has already moved the coefficient-window and
head/tail layout logic into public tables/masks before Section 6.

Thus carrying four original-style private mask families into coefficient packing is
strictly more private selector material than the post-narrow evaluator needs.

This is a source-specific factorization enabled by the paper's own narrow-table
reorganization; it is not a claim that original SHIP universally needs only two
mask ciphertexts without that reorganization.

## 5. Cost consequence

Current supplied source:
- four packed selector-root ciphertexts;
- one N-leaf binary decompression tree per root;
- therefore 4(N-1) substitution/key-switch invocations in the selector-root
  decompression stage, by direct application of Section 6.2.

Two-root construction:
- two packed selector-root ciphertexts;
- two decompression trees;
- 2(N-1) substitution/key-switch invocations.

Therefore:

    packed selector-root ciphertext count: 4 -> 2  (50% reduction)
    selector-root decompression substitutions: 4(N-1) -> 2(N-1) (50%)

The shared log2 N substitution-key TYPES are unchanged.

This is an exact logical-operation reduction for the one-time reconstruction
stage, not a measured wall-clock speedup.

## 6. What does NOT improve

The paper reconstructs the evaluation-ready narrow blind-rotation selectors once
and reuses them. Its GPU benchmark keeps blind-rotation keys resident in GPU
memory and explicitly excludes reconstruction from reported bootstrapping timings.

Our two-root change reconstructs the SAME evaluation-ready selector set.

Therefore it does NOT, by itself:
- reduce the steady-state evaluation-ready blind-rotation key size;
- reduce the GPU-resident key after full reconstruction;
- change the Section-5 sparse matrix payload Wx;
- change online table-selector multiplication count;
- change product-tree depth;
- improve the reported 8.2 ms single-ciphertext or 4.6 ms batch-64 latency.

Its direct benefits are:
- persistent/transmitted packed selector-root material;
- one-time reconstruction work;
- potentially setup latency and setup energy.

Total transmitted evaluation-key reduction is LESS than 2x because the shared
substitution keys remain.

## 7. Noise/security boundary

The two-root key can be chosen as a subset/re-factorization of selector indicator
encryptions already implicit in the current key:
positive and negative candidate bits are not new KDM plaintext functions.

Giving fewer secret-dependent RLWE ciphertext roots does not create an obvious
new leakage channel.

However, current four-root reconstruction may give independent encryption/key-
switch noise to selector copies that become head versus tail, whereas the two-root
construction reuses the same decompressed indicator ciphertext and obtains the two
layouts by public linear maps.

At the intended slot level, head and tail outputs have disjoint supports, and the
paper's final narrow output is their sum, so the same slot does not intentionally
sum both correlated selector copies. This is positive structural evidence only.

A full covariance/noise/DFR proof under the source CKKS approximation model has
NOT been completed, and no native experiment has been run.

Thus:
- plaintext/ciphertext-type correctness: PASS
- exact operation-count reduction: PASS
- security regression: no new obvious mechanism; NOT formally re-proved
- full output noise/DFR parity: UNVERIFIED
- native setup-time gain: UNVERIFIED

## 8. Novelty boundary

This is a narrow source-specific key-packing optimization, not a new bootstrapping
primitive. Its scientific value comes from exposing that Section 6 packs pre-narrow
four-way selector information even though the narrow evaluator only needs two
private sign/candidate families and public post-decompression layouts.

No direct prior collision was found in the inspected 2026/2119 source or SHIP
mask construction. Current ePrint byte parity beyond the supplied copy is
unverified.

Do not promote this to a publication contribution without:
1. source-author/code revision check;
2. exact noise/covariance analysis or native reconstruction parity;
3. measured setup and total key-size benefit including substitution keys;
4. novelty search against compressed-query/evaluation-key packing literature.

## Verdict

PASS_TWO_ROOT_NARROW_SELECTOR_PACKING.
FAIL_FOUR_PACKED_SELECTOR_ROOTS_ARE_NECESSARY.
PACKED_SELECTOR_ROOT_STORAGE: 4 -> 2.
DECOMPRESSION_TREE_KEYSWITCHES: 4(N-1) -> 2(N-1).
ONLINE_BOOTSTRAP_LATENCY: UNCHANGED_BY_THIS_STATIC_REWRITE.
FULL_NOISE_DFR_NATIVE_NOVELTY: UNVERIFIED.

No Codex/native task is justified yet; the next cheapest gate is a source-code /
noise-covariance audit of reusing the same decompressed indicator leaves for
disjoint head/tail masks, followed only if needed by one setup microbenchmark.

TOP_LEVEL_BOOT_FRONTIER_EXHAUSTED: false.
PENDING_CODEX_TASKS: none.
