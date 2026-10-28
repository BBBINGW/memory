# BOOT — Free-XOR Lazy TFHE: cyclic one-PBS barrier
Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER / ALGEBRA LEVEL ONLY
CODEX_USED: NO
NATIVE_RUN: NO

## Source context
Fresh source: Ajorian–Biçer, "Free-XOR TFHE via Lazy Bootstrapping", arXiv:2610.29983 (2026-10-21).
The construction uses a parity encoding, free XOR by ciphertext addition, headroom H (H=16 in experiments), and two PBS operations for non-affine symmetric gates: parity extraction followed by a gate LUT.

Relevant prior:
- Bon–Pointcheval–Rivain, ePrint 2023/1589 / TCHES 2024: p-encodings map bits to sets in Z_p and evaluate multi-input Boolean functions by homomorphic linear combination followed by one PBS.
- Carpov, ePrint 2024/1204: multi-input FBS is explicitly a linear combination of LWE ciphertexts followed by one ordinary FBS; feasibility depends on image size and coefficient norm.
- Sunscreen SPF bivariate PBS source implements exactly (left * 2^p) + right and then calls univariate PBS; it is radix/product-domain packing, not a two-dimensional blind rotation.
- Extended/module/monomial-matrix/Descent PBS enlarge the scalar LUT representation but public descriptions still represent one scalar message index and pay module-rank cost in rotation.

## Lemma 1 — structure forced by stable free-XOR
Let G be a finite additive group and let nonempty disjoint sets E0,E1 subset G encode bits.
Assume exact same-encoding XOR closure:
    Eu + Ev subset E_{u xor v}
for all u,v in {0,1}.

Then E0 is a subgroup K of G and E1 is a coset g+K with g notin K and 2g in K.

Proof sketch:
E0+E0 subset E0 makes finite E0 a subgroup. Pick g in E1.
K+g subset E1, hence |E1|>=|K|.
E1+g subset K, hence |E1|<=|K|.
Thus E1=g+K; g+g in K.

## Theorem 2 — cyclic one-PBS barrier
Assume additionally G is cyclic, as for an ordinary TFHE plaintext/index group.
Take l inputs using the same stable free-XOR encoding and any integer affine pre-processing before a single ordinary PBS:
    L(x1,...,xl) = c + sum_i a_i x_i.

For bit vector b, the possible pre-PBS values form
    S_b = c + L0 + sum_i b_i a_i g,
where L0 = sum_i a_i K is a subgroup.

Each delta_i = a_i g + L0 has order at most 2 because 2g in K.
A cyclic quotient G/L0 has at most one nonzero order-2 element.
Therefore every nonzero delta_i is the same element h.

Hence S_b depends only on
    xor_{i in I} b_i
for the active indices I={i: delta_i != 0}.
The affine combination can retain at most one Boolean parity bit before the PBS.

Consequences:
- one affine combination + one ordinary univariate PBS can compute only a function constant on the two parity classes of some input subset;
- for two inputs, AND, OR, NAND, and NOR are impossible when both inputs matter;
- constants, XOR/XNOR, and unary/affine cases are not blocked.

This explains why changing coefficients or using a different radix packing cannot turn the stable free-XOR encoding into a one-PBS non-affine symmetric gate inside the standard cyclic PBS interface.

## Lemma 3 — no-wrap headroom alternative pays product-domain size
The 2026 lazy scheme does not allow arbitrary modular wrap because it reserves a padding bit and keeps representatives in [0,H).

For even H, let
    E={0,2,...,H-2}, O={1,3,...,H-1}.
Consider one affine scalar packing
    L=a m0+b m1+c
followed by one univariate LUT.
To separate the AND/OR output classes for all representatives, the minimum integer dynamic range is H^2.
It is attained by radix packing (a,b)=(H,1) or the swapped/sign variants.

For H=16 the minimum domain has 256 positions.

Interpretation:
- modular-wrap regime: cyclic-group theorem blocks non-affine one-PBS gates;
- no-wrap lazy-headroom regime: escaping the collision requires product-domain H^2 and coefficient magnitude H, destroying the linear-H headroom advantage and amplifying one input's noise before PBS.

The exact TFHE failure/noise penalty of the H^2 alternative is NOT claimed without a source-faithful noise calculation.

## Prior-art boundary
The theorem is NOT a claim that multi-input FBS is new. Multi-input FBS, p-encodings, and bivariate PBS are established prior art.
The new paper-level observation is the structural barrier created by simultaneously requiring:
1. a fixed same-encoding free-XOR closure,
2. cyclic/plain ordinary TFHE PBS,
3. one affine LWE combination,
4. one PBS for a non-affine symmetric gate.

A positive construction must break at least one assumption, e.g. use a genuinely higher-rank/non-cyclic accumulator action. Existing module PBS sources found in this scout do not immediately provide such a cheap two-phase action; they target a larger scalar LUT domain and pay module rank.

## Decision
FREE_XOR_ONE_PBS_STANDARD_CYCLIC = ALGEBRAICALLY_BLOCKED
FREE_XOR_ONE_PBS_HEADROOM_AFFINE_PACK = H^2 DOMAIN LOWER BOUND
STANDARD_BIVARIATE_PBS = PRIOR_ART / PRODUCT-DOMAIN PACKING
RANK2_ACCUMULATOR_ESCAPE = THEORETICAL / NO_LOW-COST SOURCE FOUND
POSITIVE_CANDIDATE = NONE YET

Do not spend native/Codex work on this branch.

## Authoritative BOOT state unchanged
LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE: B163_PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
B158_NATIVE_FEASIBILITY: UNRESOLVED
B163: NOT_RUN
