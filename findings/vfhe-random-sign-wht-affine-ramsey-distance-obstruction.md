# Iteration 68 — Affine-Ramsey obstruction to constant distance of any fixed stack of randomly sign-masked Walsh–Hadamard blocks

Date: 2026-10-10
Active branch: soundness-preserving cross-CRT range lookup repair for Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, IACR ePrint 2025/286.
STATUS: **FAIL** primary hope that K=O(1) arbitrary independent ±1-diagonal masks stacked before unnormalized WHT yield positive asymptotic *minimum restricted Boolean-message Hamming distance*. **PASS** universal deterministic no-go for ALL sign-mask choices, not just Walsh characters or a few random seeds. For constant desired δ>0, this direct-stack family necessarily has K=Ω(log m) blocks asymptotically; it cannot preserve constant *symbol* expansion M/m with positive asymptotic minimum distance.
PAPER IMPACT: A scoped hypothetical repair candidate has been ruled out, NOT an attack on paper's original §4.3–§5. No efficient cross-characteristic commitment bridge built. Original 2026-02-16 official ePrint PDF version remains byte-UNVERIFIED; the Research MCP full source is a revised-looking 52pp mirror.
NOVELTY: This theorem uses standard finite-affine Ramsey theory, Gowers cube density and Fourier orthogonality and is likely a basic application; DO NOT claim a publishable new theorem without thorough specialist prior-art check.

## Protocol and source provenance
[FACT] Before the test read connected GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, unrelated parked RIG-HE STATE.md and I67 `failures/vfhe-character-modulated-hadamard-low-distance.md`, I66 `findings/vfhe-bounded-integer-code-crt-compatible-distance.md`. Original §4.3–5 physical pp24–26 rechecked via Research MCP on ePrint 2025/286 full 52pp GitHub mirror PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, VERSION_UNVERIFIED. §4.3 ring range PIOP and §5 per-CRT-field Brakedown/RS PC are from source; WHT candidate is OUR hypothetical.
[COMBINATORICS SOURCES] Affine Ramsey theorem for finite-field vector spaces, e.g. Graham–Leeb–Rothschild formulation Theorem 1.9 in https://www.math.uni-hamburg.de/home/schacht/lehre/SS14/Ramsey/Ramsey.pdf ; also Bergelson et al. Theorem2.6 https://people.math.osu.edu/bergelson.1/vb_codet23nov05.pdf . Gowers U^d cube count `E_x,h prod_(eps∈{0,1}^d)1_A(x+eps·h)≥density(A)^{2^d}` from repeated Cauchy–Schwarz / U^d≥|E f|, e.g. Green–Tao, *An inverse theorem for the Gowers U^3(G) norm*, https://www.cambridge.org/core/journals/proceedings-of-the-edinburgh-mathematical-society/article/an-inverse-theorem-for-the-gowers-u3g-norm/A8F67E92DC546D9F27F4B71797F974C4 . Fourier support of affine-subspace indicator, e.g. https://eprint.iacr.org/2004/256.pdf, Proposition 2.4. These are classical ingredients.

## One primary hypothesis / falsifier / cheapest test
[HYPOTHESIS — FAIL] For fixed K≥1 and growing m=2^r, independent random diagonal signs `D_1,...,D_K∈{±1}^{m×m}` before unnormalized WHT H may create a uniformly good restricted-message code `E(z)=concat_k H D_k z` for all `z∈{0,1}^m`, with asymptotic min relative Hamming distance δ_min≥δ0>0 and output length Km.
[FALSIFIER] Prove *for every arbitrary choice* of K diagonal sign masks a pair of Boolean messages whose codewords disagree in o(Km) coordinates as m→∞ (for fixed K), without a random-probability failure assumption. Sufficient to find an input support where ALL sign-mask vectors are constant and therefore all H transforms produce sparse Fourier support.
[CHEAPEST TEST] Recognize K masks as a fixed 2^K-coloring of F2^r and invoke affine Ramsey + Fourier orthogonality; derive quantitative dimension sufficient condition from Gowers cube count; independently check ONE seeded non-character-mask m256 K4 witness via exact FWHT, no sweeps.

## Universal deterministic no-go theorem
Let `G=F_2^r`, m=2^r, H_(a,x)=(-1)^(a·x). Let D_k diagonal ±1 functions `s_k(x)`, k∈[K], arbitrarily selected, perhaps randomly; E(z)=concat_k H D_k z for z Boolean vector length m.
Define signature coloring `c(x)=(s_1(x),...,s_K(x))∈{±1}^K`; at most C=2^K colors. By finite affine Ramsey, for every fixed K,d and large enough r, there exists a **monochromatic affine d-flat** A=x0+V⊂F2^r with dim(V)=d. Choose legal z0=0^m and z1=1_A. For each k all signs equal ε_k on A, so D_k(z1−z0)=ε_k 1_A. Fourier:
 `(H 1_A)(a)=(-1)^(a·x0)*2^d` if a∈V^perp, and 0 otherwise; |V^perp|=m/2^d.
Consequently each block has exactly m/2^d differing positions, and
 `d_H(E(z1),E(z0))/(Km)=2^(−d)`.
For every desired δ0>0 choose any fixed d with 2^(−d)<δ0; then for sufficiently large r the minimum relative distance falls below δ0. Thus **no fixed K** can give positive uniform asymptotic relative distance on the Boolean message domain, even with fully independent random signs. This is a deterministic impossibility for this *direct block stack*, not a stochastic lower-confidence bound.

## Quantitative bound / necessary number of blocks
Let a color class A have density α≥2^(−K). Gowers U^d inequality yields
 Pr_{x,h_1,..,h_d}[∀eps∈{0,1}^d: x+Σ eps_i h_i∈A] ≥ α^(2^d)≥2^(−K2^d).
Meanwhile Pr_{h_1,..,h_d}[linearly dependent] ≤ Σ_(j=0..d−1)2^(j−r)=(2^d−1)/2^r. Therefore a nondegenerate monochromatic affine d-flat is guaranteed if
 `2^r >(2^d−1)2^(K2^d)`
or `r>log2(2^d−1)+K2^d`.
For fixed K, set d≈floor(log2(r/(2K))) at sufficiently large r to get δ_min≤2^(−d)=O(K/r)=O(K/log2 m). This asymptotic bound is not optimized for moderate r.
Conversely, to guarantee δ_min≥δ0 for all m, fix any d with 2^(−d)<δ0. The above sufficient presence condition forces **necessary** `K≥(r−log2(2^d−1))/2^d=Ω(r)=Ω(log m)` as r→∞, within this direct-stack encoder family. Then M=Km=Ω(m log m): constant *symbol* rate impossible asymptotically if positive minimum distance is required. This does not prove Ω(m log²m) time for all possible optimized implementations; naive K WHT blocks take O(Km log m).
IMPORTANT FINITE PARAMETER LIMIT: For paper-inspired m=2^15, K=4, this coarse universal sufficient condition certifies only d=1, hence δ≤1/2. It does NOT refute a minimum distance 1/8 at that PARTICULAR finite size, nor give a practical attack on real instantiated commitments. The result is an asymptotic restricted-distance obstruction.

## One exact independent experiment with arbitrary non-character masks
Script `/mnt/data/iteration68_vfhe_random_sign_hadamard_affine_obstruction.py` SHA256 `4ef276e353332f8d156fd15dda1fcef6026801dc31dbcb086fa7333da0175615`.
Stdout `/mnt/data/iteration68_vfhe_random_sign_hadamard_affine_obstruction_results.txt` SHA256 `58f0db98c4aced882142cdb0e5c0c6e41a2d593bee2e5e720444495a3e34a382`. Both created and exact checks executed in current container.
Seed 20261010, m=256 (r=8), K=4, **all four masks verified NOT Walsh characters**. Signature (-1,-1,-1,-1) appears on affine 2-flat A={9,13,115,119}=9+span_F2{4,122}. Boolean z0=0 and z1=indicator_A. Exact integer butterfly H D_k(z1−z0) has 64 nonzero coordinates among256 for EVERY block (four-symbol amplitude ±4), total 256 nonzero positions among1024, δ=1/4, matching Fourier theorem. With nonnegative affine shift +m, all symbols fall within [0,2m]=[0,512], so p∈{769,773} cause no canonical modular wrap. This is an **encoding arithmetic example**, NOT actual CKKS ring parameters or a real PIOP instance.
One test only. The initial draft test erroneously assumed all nonzero Fourier signs had same sign; corrected to allow ±4 from affine shift phase (-1)^(a·x0). Final script and hashes above reflect corrected successfully passing test; general proof was not affected.

## Boundaries, comparisons, and novelty risk
- Unlike I67's character masks, this applies to **all** fixed K sign masks, including independent random diagonals. The global Boolean-message minimum distance collapses asymptotically because any finite coloring contains large monochromatic affine flats.
- It does NOT apply to multi-stage non-diagonal randomized mixing `H D H D...`, to hash/nonlinear encoders, to independently sampled dense integer matrices (I66), or to an arbitrary good field code. It also doesn't assert typical/random average input distance fails; the adversarial input depends on public masks and is worst-case.
- Affine shift ensures CRT no wrap if p_min>2m, but can't improve Hamming distance.
- Even if one escaped this code distance obstacle, one still needs a genuinely globally bound common integer digit vector and proof that every CRT component commitment encodes that SAME vector; the §5 componentwise commitments don't supply that for free.
- Affine Ramsey / Gowers / Fourier identities are classical. This scope-specific no-go is a research filter, not evidence of novelty or completed FHE+ZK contribution.

## End of iteration 68
STATUS: FAIL (arbitrary fixed K random-sign WHT-stack restricted Boolean minimum distance cannot remain constant); PASS (general proof and fixed-seed exact witness); HUMAN_REVIEW warranted due to repeated cheap encoder variants.
RESULT: Every choice of K=O(1) sign masks yields affine-monochromatic Boolean input support and δ_min→0; for target constant δ, K must grow Ω(log m) for this direct-stack form. Reproduced m256 K4 non-character mask example δ=1/4, no-wrap primes 769/773, and proved quantitative r>K2^d+log2(2^d−1) condition.
NEXT_ACTION: HUMAN_REVIEW — choose whether to stop fast-encoder variants and prioritize confidential authoritative source/author verification of the I59–61 soundness issue (requires explicit approval), OR fund a serious cross-characteristic consistent commitment protocol with external digits and published prior-art scan. No more minor mask/RS changes or toy variants.
STATE_UPDATE: NO — parked unrelated RIG-HE STATE.md unchanged.
