# BOOT Research Handoff — post B135

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- LATEST_COMPLETED: B135
- NEXT_RESERVED: B136 — NOT STARTED
- STATUS: ACTIVE RESEARCH / SESSION HANDOFF
- NOVELTY: NOT ESTABLISHED
- CODEX_REQUIRED: NO
- NATIVE_BENCHMARK: NOT JUSTIFIED

## Research protocol

Continue the BOOT track only. Keep SHIP, PURE-FHE, CGS, VFHE, EXPLORE and EAI isolated. Read-only comparison across tracks is allowed, but do not inherit their NEXT_ACTION or write their state.

Use the fixed research rule:
smallest falsifiable claim -> cheapest decisive test -> algebra/correctness -> assumptions/security -> noise/DFR -> matched native benchmark only if justified.

Do not launch Codex, GPU/server work, large downloads, native implementation, or cross-track repository writes merely because a candidate is interesting. First clear source/prior-art/correctness/value gates.

## Historical recovery before this session

B117-B122 Sorted Bootstrapping / group-aware CMS is frozen. B121 had a user-reported native functional PASS on a crafted mask, but honest random-mask combinatorics made differences essentially unreachable at legal small K; B122 showed no source-justified DFR-certified high-K regime. Do not repeat K=8/K=45 experiments.

B123 automorphism traversal DP was archived low value: symbolic KS savings existed but modeled online gain was <1% and novelty was weak.

## B124 — Descent-PBS input-KSK / HomDivRem fusion gate

Target: ePrint 2026/2616, Descent-PBS.

Primary observation: the 16-bit construction exposes a large persistent-key / input-KSK memory tension. The tempting linear fusion
KS_{z->s} -> HomDivRem
by pre-digitizing KSK entries fails because HomDivRem contains rounding and does not commute with KSK accumulation.

Minimal counterexample for Q_u(x)=round(x/u):
u=4, x=y=1,
Q_4(1)+Q_4(1)=0 but Q_4(2)=1.

Decision:
FAIL_NAIVE_KS_HOMDIVREM_FUSION.

Do not claim impossibility of all fusion methods.

## B125 — digit-first low-modulus KS noise gate

Candidate reorder:
HomDivRem under source secret z first, then key-switch each low-modulus digit to the block-one-hot secret s.

Key reason for failure: original ordering first moves to low-Hamming-weight s, then performs HomDivRem. Moving HomDivRem earlier exposes rounding to the dense/binary coefficient secret z.

Using the paper's variance formulas:
V_MS(dense) = N/24 + 1/12,
V_MS(onehot) = (h+1)/12.

At the 16-bit regime with N=2048, h=72:
V_dense ~= 85.4167,
V_onehot ~= 6.0833,
variance ratio ~=14.04,
stddev ratio ~=3.75.

Under the paper-style window/failure model, the first windows deteriorate from roughly 2^-73 / 2^-79 scale to about 2^-7 scale. Mean compensation still leaves failure around 2^-12 to 2^-13 scale.

Decision:
FAIL_PRE_KS_HOMDIVREM_NOISE_FRONTIER.

## B126 — structured z->s ring-KSK compression gate

Observation: z=coeff(S) gives a valid ring provenance. Embedding the LWE mask/secret into a ring, doing RLWE key switching, then sample-extracting the constant coefficient can compress asymptotic flat LWE->LWE key-switch storage.

But this is direct prior art: Chen-Dai-Kim-Song, ePrint 2020/015 / ACNS 2021, gives essentially this LWE->LWE via ring embedding / RLWE KS / sample extraction construction.

Applying it to Descent-PBS also changes the security interface toward RLWE with the structured block-one-hot/sparse target ring secret. That exact parameter security is not automatically inherited.

Decision:
FAIL_NOVELTY_DIRECT_CDKS_PRIOR_ART.
SECURITY_NOT_TRANSFERABLE.
Do not claim the exact block-one-hot RLWE parameter set is insecure.

## B127 — seeded flat-KSK rank gate

After standard seeded masks are removed, consider a flat LWE linear key-switch model with r stored secret-dependent linear forms h_k(z)=<u_k,z>. To support arbitrary public mask a and recover <a,z> by public linear combination for every z, the u_k must span the full N-dimensional source space.

Hence model-specific lower bound:
r >= N.

This only lower-bounds source-coordinate rank. It does NOT prove an N*l information-theoretic lower bound because gadget levels are scalar multiples of the same source coordinate and represent a standard digit-size/noise tradeoff.

Decision:
PASS_MODEL_SPECIFIC_RANK_LOWER_BOUND.
FAIL_NEW_FLAT_KSK_COMPRESSION.
Descent-PBS input-KSK local branch PARK.

## B128 — ePrint 2026/537 phase-decomposition source/bottleneck gate

Target: Schild-Abidin-Preneel, On Phase Decompositions with Applications to Digit Decomposition.

Main source result: the new construction obtains one blind rotation per digit, with exact HomTruncTrace between digits. The truncation overhead is modeled as only a small fraction of a blind rotation (roughly single-digit percent in the paper's example), so truncation is not the dominant target.

The real open bottleneck is the per-digit blind rotation on pseudo-LWE inputs whose public coefficients lie in a small alphabet and whose binary secret is sparse.

Paper currently has theoretical/work-count evidence rather than a mature native timing baseline suitable for our own optimization claims.

Decision:
PASS_SOURCE_AND_BOTTLENECK_IDENTIFICATION.

## B129 — bounded-coefficient blind-rotation compression gate

Histogram rewrite:
E = sum_i a_i s_i = sum_v v k_v,
k_v = sum_{i:a_i=v} s_i.

Algebraic histogram compression is correct, but GGSW(k_v) supports multiplication by k_v, not exponentiation by X^{v k_v}.

Stronger model-specific obstruction:
for a group of g unrestricted binary secret bits, functions
F_a(s)=X^{sum_i a_i s_i}
already have full 2^g linear function-space rank even restricting a_i to {0,1}. Thus small coefficient alphabet alone does not make one-linear-combination + one-external-product grouped evaluation compact.

For a globally h-sparse secret, legal local secret states still have dimension at least sum_{r<=min(h,g)} binom(g,r); block-one-hot secrets escape because each block has only g+1 legal states, which is existing prior art.

Also, with only affine/linear secret-dependent multipliers, exact product
prod_i(1+s_i(X^{a_i}-1))
has multilinear secret degree h, implying h multiplicative stages in that restricted model.

Decision:
FAIL_SMALL_ALPHABET_STANDALONE_COMPRESSION.
2026/537 local bounded-coefficient BR branch PARK.
Do not present these model-specific rank/degree statements as universal blind-rotation lower bounds.

## B130-B133 — ePrint 2026/2618 CI-ring CKKS functional bootstrap

Target: Efficient (Functional) Bootstrapping for CKKS over the Conjugate-Invariant Ring.

B130:
Native/source profiling identified CtS as the dominant stage in the fastest cited configuration (about 8.31 s of 12.60 s, roughly 66%); StC and EvalMod were much smaller.
PASS_SOURCE_AND_DOMINANT_BOTTLENECK.

B131:
Attempt to move CtS factors before ModRaise fails structurally. ModRaise injects a fresh arbitrary integer coefficient overflow vector I after any pre-transform. EvalMod needs the corresponding integer slot offsets, so the post-ModRaise path must still transport this fresh I into slots. Simple CtS/ModRaise reordering therefore cannot delete the full post-MR CtS function.
FAIL_PRE_CTS_SCHEDULING_FRESH_OVERFLOW.

This is compatible with older PURE-FHE pretrace/ModRaise commutator negative results; do not reopen simple pre-transform scheduling.

B132:
Single-cosine phase shift can increase minimum node spacing, with spacing-optimal phase satisfying approximately tan(phi*)=(1/3)tan(pi/p), asymptotically giving ~4/3 larger minimum spacing. However high-precision Hermite interpolation conditioning worsens substantially. Low-degree cubic node warps can increase spacing further but worsen interpolation conditioning even more.
FAIL_PHASE_SHIFT_SPACING_OPTIMIZATION.
FAIL_LOW_DEGREE_NODE_WARP.

B133:
Nonuniform Hermite multiplicity gate. Keeping the original Chebyshev nodes and baseline multiplicity n+1, any additional degree-k correction that preserves all baseline Hermite constraints has form
H = H0 + T_p^(n+1) G,
deg G <= k-1.

For p=256 AES S-box, n=3, even a relaxed minimax problem allowing arbitrary such G gives very small worst-error improvement: up to k=64 extra degree, log2(K/K') is only about 0.19 bit, corresponding to <~0.05 bit optimistic noise-capacity gain under the paper-style model. Real selective-node multiplicity is no better and k>=2 crosses degree 1024, implying at least one more generic multiplication level absent special structure.

Decision:
FAIL_SELECTIVE_MULTIPLICITY_VALUE.
2026/2618 local optimization branch PARK.

## B134 — ePrint 2026/1264 low-rank FBS source/value gate

Target: The Power of Low Rank: Fast CKKS Functional Bootstrapping for High-Precision Lookup Tables.

The low-rank object is the reshaped LUT matrix. LRMT-FBT uses exact/numerical SVD structure and reduces LUT-matrix work from O(P) to O(r sqrt(P)).

From the public reported speedups:
Step: LUT 196.9x, total FBT 5.3x.
ReLU: LUT 99.6x, total FBT 5.1x.

Amdahl inversion implies the original LUT stage occupied about 81% of runtime, but after LRMT it is only about 2.2% (Step) to 4.2% (ReLU). Even deleting the optimized LUT cost entirely would improve total runtime only roughly 1.02-1.04x.

Step already has rank r=1.

Decision:
PASS_LOW_RANK_FBS.
FAIL_FURTHER_RANK_HEADROOM.
2026/1264 local-rank branch PARK.

Full PDF was not available through the current ePrint connector; the source/value gate above relies only on publicly verifiable paper metadata/summary numbers. Do not invent stage-level internals.

## B135 — ePrint 2026/2119 sub-10ms CKKS fairness gate

Target: Ouyang et al., CKKS Bootstrapping in less than 10ms.

Publicly verifiable author claim:
8.2 ms for one complex-valued ciphertext;
4.6 ms/ciphertext at batch 64;
method is built on SHIP and claims reduced communication/computational overhead plus efficient parallel execution.

Current blocker: full PDF unavailable to our ePrint connector (403 / no verified mirror). The public abstract does NOT expose the matched ring dimension, modulus chain, precision, security parameters, hardware/thread count, key sizes, or stage breakdown.

Therefore:
PASS_PUBLIC_CLAIM.
FAIL_FAIRNESS_VERIFICATION.
SOURCE_GATED.
NO CODEX / NO REPRODUCTION YET.

Do not compare 8.2 ms directly to SHIP 215 ms, conventional CKKS seconds, or HEAAN GPU numbers as algorithmic speedups without matched parameters.

Conditional Amdahl model only:
Assuming T(B)=A+B*C and taking the two public latency points literally,
A+C=8.2,
(A+64C)/64=4.6,
giving C~=4.543 ms and A~=3.657 ms.
Under this simplified model, batch=64 is already within about 1.2% of the infinite-batch per-ciphertext limit. Treat this as inference, not source-reported stage profiling.

## Missing source that now matters

Need an authorized copy of:
ePrint 2026/2119, CKKS Bootstrapping in less than 10ms.

If supplied under papers/supplied/, resume B135 before making claims about parameters/stages/fair speedup.

## Next active candidate — B136 NOT STARTED

Target:
Liang-Ding, ePrint 2026/1779,
Bootstrapping via Ring Switching without Slot Recovery: Independent Leaf Evaluation for SIMD-Packed Ciphertexts.
Version 5 was publicly updated 2026-10-26 and public metadata reports code/native evidence.

Known public mechanism:
after ring switching, leaves can be evaluated independently and recombined without conventional slot recovery. For unrestricted real CKKS inputs, their theorem states continuous slotwise functions support independent leaf evaluation iff the function is affine.

B136 cheapest question:
Does this affine-only theorem cease to block useful non-affine functions when the plaintext domain is finite/discrete, e.g.
D={0,...,p-1},
so that a non-affine LUT can be leaf-evaluated independently after ring switching and recombined correctly without traditional slot recovery?

First test must be algebraic, not native:
1. recover exact theorem/interface from source;
2. write the leaf observation/recombination map on a finite plaintext set;
3. solve the induced functional equation for small p;
4. construct either an explicit non-affine counterexample/solution or prove finite-domain affine closure under the actual recombination map;
5. only if PASS, check prior art and cost.

Do not assume finite domain automatically escapes the theorem; this is the point to falsify.

## Priority / stopping rules

P0: B136 discrete-domain escape from ePrint 2026/1779.
P1 conditional: resume B135 immediately if 2026/2119 full PDF is supplied.
P2: only after a mathematical PASS, inspect the 1779 code/native path.

PARK:
- B121/B122 Sorted CMS
- B123 automorphism DP
- Descent-PBS input-KSK local compression B124-B127
- 2026/537 bounded-alphabet BR B128-B129
- 2026/2618 local CI-Hermite/CtS variants B130-B133
- 2026/1264 further rank optimization B134

Do not:
- rerun old B121 K=8/K=45 tests;
- claim universal lower bounds from model-specific rank/degree gates;
- benchmark 2119 without its exact parameters;
- launch Codex before B136 algebra/source gate passes;
- silently switch into SHIP or PURE-FHE state.

## Resume state

LATEST_COMPLETED: B135
NEXT: B136_DISCRETE_LEAF_NONAFFINE_GATE — NOT STARTED
CODEX_REQUIRED: NO
SOURCE_NEEDED: ePrint 2026/2119 full PDF
