# BOOT — Direct dBFV rounding / bootstrap gate

Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER_LEVEL_ONLY
CODEX: NOT_USED
NATIVE: NOT_RUN

## Authoritative BOOT state

LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE_GATE: B163_CORRECTED_B160_NOSCALE_SELECTOR_GATE
B163_STATUS: PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
DO_NOT_AUTO_RUN_CODEX: YES

B158_ALGEBRA: PASS
B158_CTCT_MULT_COUNT: OPTIMAL
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B158_NATIVE_FEASIBILITY: UNRESOLVED
B163: NOT_RUN

## Primary source

Peikert–Zarchy–Zyskind,
"High-Precision Exact FHE Made Simple, General, and Fast",
ePrint 2025/2321 / CRYPTO 2026.

Research-MCP mirror SHA256:
1e41b62004aeee0bf572d0ccca8de8c5827ee9a14fb333a1d3d0f4d2ab483849
VERSION_UNVERIFIED.

Verified relevant pages:
- pp.4-9: dBFV overview, empirical d/base tradeoff, and bootstrap overview.
- pp.19-30: dBFV plaintext/ciphertext decomposition, error polynomial, ciphertext reduction.
- pp.31-35: generic BFV/dBFV/GSW bootstrap reductions.
- pp.40-43: dGSW operations and efficient multivariate implementation.

## Source-open problem

Section 5.1 bootstraps a dBFV ciphertext by:

1. lifting
      c(B,S) -> sum_{i<d} c_i(S) B^i,
   where each c_i is an ordinary mod-p BFV ciphertext under the same secret key and encrypts digit mu_i;

2. bootstrapping each c_i separately/in parallel;

3. recombining
      c'(B,S)=sum_i c'_i(S) B^i mod L.

Remark 5.1 explicitly states that lifting back to BFV form may be wasteful because:
- the plaintext digits are relatively small compared with p;
- they arise from a dBFV ciphertext whose error is similarly decomposed;
- a bootstrapping scheme specialized to dBFV could potentially implement rounding directly.

This is a primary-source future-work target, not an invented gap.

## Concrete parameter relevance

For plaintext p=2^64, Figure 1 evaluates:
- d=1, log2(b)=64;
- d=4, log2(b)=16;
- d=8, log2(b)=8;
- d=16, log2(b)=4.

The dBFV multiplication cost grows with d but is still ordinary arithmetic, whereas the generic bootstrap invokes d full high-precision BFV bootstraps.

For log2(n)=12, GPU multiplication times reported by the source are approximately:
- d=1: 0.18 ms;
- d=4: 0.74 ms;
- d=8: 1.60 ms;
- d=16: 3.68 ms.

This does NOT predict direct-bootstrap speed, but confirms that d is practically small/moderate and that representation-level B-axis arithmetic is a distinct cost regime from a full bootstrap.

## Direct-rounding semantics in the p=b^d case

For simplicity take R=Z and p=b^d.

After homomorphic decryption/lifting, write the noisy decomposition as

    y(B)=sum_{i=0}^{d-1} y_i B^i,
    y_i = mu_i + e_i,

where mu_i are integer digits from a relaxed decomposition of the plaintext and each error coefficient e_i is independently decodable modulo Z, e.g. |e_i|<1/2.

The direct bootstrap only needs the single final plaintext

    mu = sum_i b^i mu_i mod b^d,

not d separately materialized refreshed digit ciphertexts.

Equivalently, the desired nonlinear map is

    F(y_0,...,y_{d-1})
      = sum_i b^i Round(y_i) mod b^d.

Thus direct dBFV rounding is naturally a multi-input/single-output error-correction problem.

## No-go 1: generic same-ring SIMD packing cannot collapse d full digit ciphertexts to one

Suppose each digit ciphertext c_i already carries S independent application SIMD slots.

Then the d ciphertexts jointly contain dS independent plaintext digit values.

One ciphertext of the same ring/packing has only S plaintext slots.

Therefore no injective same-ring packing can losslessly encode all dS independent digit values into one S-slot ciphertext.

Consequences:
- generic "pack the d BFV ciphertexts into one ordinary packed BFV ciphertext" only works if spare slot capacity exists;
- otherwise it requires a larger ring / more slots / another carrier, which must be included in the cost;
- such spare-capacity batching is ordinary amortization, not a structural dBFV-specific contribution.

The real open problem must exploit the fact that the final output is only the recombined mu, not preserve all d refreshed digits.

## No-go 2: collapse B -> b before nonlinear correction destroys the dBFV error advantage

If we first evaluate the noisy decomposition at B=b, then

    y(b)
      = mu + E,
    E = sum_{i=0}^{d-1} b^i e_i.

If |e_i|<=delta independently, then

    |E|
      <= delta * sum_{i=0}^{d-1} b^i
      = delta * (b^d-1)/(b-1).

Any scalar nearest-integer recovery that must distinguish adjacent plaintext integers requires

    |E| < 1/2.

Hence necessarily

    delta
      < (b-1)/(2(b^d-1))
      ~= 1/(2 b^{d-1}).

By contrast, dBFV correctness only needs each coefficient error separately decodable, on the order of

    |e_i| < 1/2.

Therefore:

    COLLAPSE_TO_SCALAR_BEFORE_ROUNDING = FAIL.

It loses essentially the entire decomposition-error advantage and returns to a tiny-error regime resembling ordinary high-precision BFV.

A valid direct dBFV bootstrap must preserve the B-axis information until after the nonlinear correction.

## Stronger one-linear-projection robustness bound

The previous result used the specific evaluation weights 1,b,...,b^{d-1}. More generally, suppose one tries to compress the noisy digit vector y into one scalar

    z = sum_i a_i y_i

before applying an arbitrary one-dimensional nonlinear bootstrap/function g(z).

Assume:
- changing any one integer digit mu_i by +1 changes the desired plaintext output;
- each independent digit error satisfies |e_i|<=delta;
- the scalar decoder must be correct for every error in this box.

For a fixed integer digit vector mu, the projected uncertainty interval has radius

    R = delta * ||a||_1.

Two adjacent cells differing only in digit i have projected centers separated by |a_i|.

Their intervals must be disjoint, so for every i,

    |a_i| > 2 delta ||a||_1.

Summing over i yields the necessary condition

    1 > 2 delta d,

i.e.

    delta < 1/(2d).

Therefore:

### One-projection theorem

At full/near-full dBFV coefficientwise error tolerance (delta close to 1/2), no single linear projection of the d noisy digits followed by an arbitrary scalar nonlinear function can implement exact direct rounding when d>=2.

This is independent of the choice of base b.

It does not rule out:
- several projections;
- nonlinear preprocessing before compression;
- a genuinely vector/module bootstrap;
- or a circuit that preserves B-dimensional state until late.

## Positive lemma: diagonal moment sharing without materializing digit outputs

Although the noisy digits cannot be collapsed before nonlinear correction, some nonlinear aggregate computations can be shared in the B-polynomial representation.

Let

    Y(B)=sum_{i=0}^{d-1} y_i B^i

and for public weights w_i define

    Y*(B)=sum_{i=0}^{d-1} w_i y_i B^{d-1-i}.

Then ordinary lifted polynomial multiplication gives

    [B^{d-1}] (Y(B) * Y*(B))
       = sum_{i=0}^{d-1} w_i y_i^2.

Proof:
a product term y_i * w_j y_j lands in degree

    i + (d-1-j).

This equals d-1 iff i=j.

For direct dBFV recombination take w_i=b^i. Therefore one parent-level polynomial multiplication plus public coefficient extraction computes the weighted quadratic moment

    S_2 = sum_i b^i y_i^2

without materializing the d individual squares.

Status:
    WEIGHTED_QUADRATIC_MOMENT_SHARING = PASS.

This is an algebraic positive result, not yet a rounding algorithm.

## Why the moment lemma does not solve rounding immediately

If a scalar rounding approximant has degree D,

    P(t)=sum_{k=0}^D c_k t^k,

then

    sum_i b^i P(y_i)
      = sum_k c_k S_k,

where

    S_k=sum_i b^i y_i^k.

So a direct polynomial-rounding circuit can in principle be reduced to weighted diagonal moments.

However:
- S_2 is exceptionally easy;
- general k-way diagonal extraction is a tensor problem;
- simple Kronecker exponent encodings can isolate the diagonal but grow the B-degree rapidly (roughly d^{k-1} for a direct mixed-radix construction);
- ordinary BFV digit-removal/rounding polynomials may have substantial degree.

Chen–Han EUROCRYPT 2018 (ePrint 2018/067) uses lowest-digit-removal polynomials whose degree scales with the relevant radix/plaintext parameters; later work studies the degree limits of such polynomials.

Therefore:

    LOW_DEGREE_DIRECT_ROUNDING = NOT ESTABLISHED.

The quadratic lemma is useful only if the direct rounding/correction function has enough low-degree structure, or if several diagonal moments can be generated much more efficiently than separate digit bootstraps.

## Source implementation cost warning

Appendix B of 2321 notes:
- the B-degree is moderate/small;
- dedicated B-axis FFT/NTT may not be worthwhile;
- Kronecker substitution can combine X/G/B polynomial arithmetic;
- the overall polynomial arithmetic can be implemented quasi-linearly in the representation sizes.

Empirically, one dBFV multiplication costs roughly O(d) ordinary-BFV work in the reported regimes, sometimes with a larger constant.

Therefore a direct circuit made of many dBFV multiplications is not automatically cheaper than d separate small circuits.

The win must specifically replace expensive bootstrap/nonlinear-refresh work, not merely rewrite d independent multiplications as one B-polynomial multiplication.

## Current prior-art threats

### Generic packed/batched bootstrapping

Packing/batching multiple ciphertexts before bootstrapping is mature prior art in BFV/TFHE variants.

For example:
- GBFV explicitly uses packing to batch bootstrap multiple ciphertexts;
- BatchBoot (USENIX Security 2026) provides batched TFHE bootstrapping.

Therefore:
    "batch the d digit ciphertexts" = LOW NOVELTY / GENERIC AMORTIZATION
unless the dBFV decomposition enables a new structural reduction.

### Exact error / comb bootstrap, ePrint 2026/2630

The public abstract states that comb bootstrap can refresh several FHEW/TFHE ciphertexts with one blind rotation because the error has a small state space.

This is a dangerous current neighbor:
- 2321 can use a third-generation/FHEW-style host to bootstrap BFV digit ciphertexts;
- the d dBFV digit errors are exactly a family of small errors needing refresh.

Full 2630 text is currently unavailable, so compatibility/output details cannot be verified.

Potential implication:
    applying generic comb bootstrap to the d lifted coefficient ciphertexts may already reduce the number of blind rotations, but this would be an application of generic comb bootstrap, not a direct dBFV rounding theorem.

Do not claim novelty until 2630 is read.

## Why the problem remains high value

The primary source itself identifies the generic reduction as potentially wasteful.

Moreover, dBFV's purpose is precisely to obtain error behavior controlled by approximately p^(1/d), not p.

A successful direct bootstrap that preserves the coefficientwise error geometry while avoiding d full mod-p BFV refreshes would:
- remove a complete interface materialization;
- make bootstrapping respect the scheme's decomposed high-precision structure;
- potentially turn high-precision exact FHE into an end-to-end decomposed scheme rather than falling back to ordinary mod-p BFV at refresh time.

This is a structurally meaningful target.

## Candidate label

    DIRECT_DBFV_ROUNDING

## Gate decision

PRIMARY_SOURCE_OPEN_PROBLEM:
    PASS — Remark 5.1 explicitly leaves specialized direct rounding open.

GENERIC_d_TO_1_SIMD_PACKING:
    FAIL GENERICALLY by slot-capacity conservation; spare-capacity batching only.

COLLAPSE_B_TO_b_BEFORE_NONLINEAR_CORRECTION:
    FAIL by error amplification.

ONE_LINEAR_PROJECTION_PLUS_ONE_SCALAR_NONLINEARITY:
    FAIL at near-full coefficientwise error tolerance; necessary delta<1/(2d).

WEIGHTED_QUADRATIC_MOMENT_SHARING:
    PASS.

GENERAL_LOW_DEGREE_DIRECT_ROUNDING_CIRCUIT:
    NOT ESTABLISHED.

COMB_BOOTSTRAP_COLLISION:
    UNCLEAR / SOURCE_BLOCKED BY 2026/2630 FULL TEXT.

NOVELTY:
    PROMISING_NOT_ESTABLISHED.

END_TO_END_VALUE:
    NOT ESTABLISHED.

CCF_A_B_READINESS:
    NO.

CODEX_REQUIRED_NOW:
    NO.

## Cheapest next gate

DIRECT_DBFV_GATE_2:

1. Work first in the source's simplest p=b^d, R=Z model.
2. Formalize the exact direct rounding map on the bounded relaxed-digit/error domain.
3. Determine whether it admits a circuit using:
   - dBFV linear/reduction maps,
   - O(1) or O(log d) parent-level nonlinear operations,
   - without materializing d refreshed BFV outputs.
4. In particular, derive S_3/S_4 diagonal-moment costs and test whether a useful rounding approximant can be expressed from a small moment set.
5. Compare against:
   - d ordinary BFV bootstraps;
   - d small-domain TFHE/PBS calls;
   - current comb-bootstrap possibility once 2630 full text is available.
6. PARK if every exact/robust direct circuit needs Omega(d) independent nonlinear channels with similar per-channel cost.
7. Advance if one can prove a sub-d nonlinear-refresh count or a materially smaller host plaintext/ring requirement while preserving the dBFV error advantage.

No native experiment until a source/algebraic construction survives.

## Paper-only BOOT priority update

1. DIRECT_DBFV_ROUNDING — high-value open problem, complete primary source available, no construction yet.
2. STABILIZER_AWARE_SUBFIELD_SECRET — PROMISING_SOURCE_INCOMPLETE.
3. 2026/1779 partial-recovery interaction rank — strong theory but source-blocked.
4. 2026/2630 lossy-KS/error-bootstrap — source-blocked, also relevant prior art to dBFV.
5. RANK_PARTITION_LRMT — HOLD_NO_WORKLOAD.

B163 remains the highest native gate once Codex quota is explicitly restored by the PI.
