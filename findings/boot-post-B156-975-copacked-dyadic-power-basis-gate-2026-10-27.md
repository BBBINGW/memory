# BOOT post-B156 — 2026/975 co-packed dyadic power-basis gate

Date: 2026-10-27  
TRACK_ID: BOOT  
State impact: NONE. Do not modify B157 pending state.  
No Codex / GPU / remote execution was used.

## Source

Primary paper:
- ePrint 2026/975, *Functional Bootstrapping for a Single LWE Ciphertext with O~(1) Polynomial Multiplications*, Zheng–Li–Wang.
- A complete 37-page copy was available in the supplied file library and was read at algorithm/table level.

Author implementation:
- https://github.com/xiaopeng-stu/bfv-functional-bootstrapping
- pinned public revision: b113742d83d772fd0d1b353e72ac6e31f2838bea
- Lattigo v6.2.0.

The current public implementation is materially faster than the paper table, so all performance headroom below uses the current repository data rather than only the original 3.15 s figure.

## Current source-level bottleneck

For the current 9-bit, m=1 benchmark:
- N = 32768
- plaintext/LWE modulus T=q=65537
- p=512
- LWE n=2048, h=512
- current online total ~= 2.061226 s
- Step 1 ~= 0.693407 s
- polynomial evaluation ~= 1.284265 s
- BuildBasis / P ~= 1.141457 s

Thus BuildBasis is still the largest individual online substage.

The code path is Algorithm 5 with:
- r=N=32768
- lowerLen=65536=2N
- s=lowerLen/r=2

The expensive first MonomialGenExtra builds the reusable basis
(1,x,...,x^(r-1))
and separately retains x^(r/2).

For r=2^ell, ell=15, current MonomialGenExtra uses:
- ell-1 = 14 ct-ct multiplications to build x,x^2,x^4,...,x^(r/2)
- ell-1 = 14 further ct-ct multiplications to combine masked factors into the full monomial basis
- ell = 15 pt-ct masked multiplications with rescale
- total 2ell-2 = 28 ct-ct multiplications
- source planner output depth: ell+1 = 16 levels
- x^(r/2) extra is available after ell-1 = 14 levels

## Candidate: co-packed dyadic power basis (CPB)

### State

Let H=N/2 and ell=log2(N). Represent BFV/BGV slots as two rows of H slots.

For i >= 0 define:
- B_i = (1,x,...,x^(2^i-1))
- a_i = x^(2^i)

Maintain one ciphertext C_i whose plaintext is

row0 = B_i repeated H/2^i times
row1 = a_i repeated H times.

Initialization C_0 is:
- row0 = 1
- row1 = x

and can be constructed from the replicated-x input with one public 0/1 selector multiplication plus a plaintext addition; no ct-ct multiplication is needed.

### Recurrence

Let tau be the row-swap automorphism.
For i=0,...,ell-2, construct a factor F_i as follows:

- on row0, positions in the first half of every length-2^(i+1) block are 1;
- on row0, positions in the second half are a_i, taken from row0 of tau(C_i);
- on row1, every position is a_i, taken from row1 of C_i.

This factor is a public linear combination of:
- tau(C_i),
- C_i,
- fixed 0/1 slot masks,
- a fixed plaintext 1-mask.

It therefore needs one row-swap, two selector pt-ct multiplications, and additions, but no extra ct-ct multiplication.

Then

C_(i+1) = C_i * F_i

gives exactly:

row0 = B_(i+1) repeated,
row1 = a_(i+1)=a_i^2 repeated.

The proof is coordinatewise:
- first half: B_i * 1 = B_i
- second half: B_i * a_i = (x^(2^i),...,x^(2^(i+1)-1))
- row1: a_i * a_i = a_(i+1).

After ell-1 recurrences:
- row0 = (1,x,...,x^(H-1))
- row1 = x^H repeated.

A final row-swap + masked factor + one ct-ct multiplication maps this to:
- row0 = (1,...,x^(H-1))
- row1 = (x^H,...,x^(N-1))

i.e. the exact basis (1,x,...,x^(N-1)).

The same final row-swap can also be reused to materialize x^(N/2) in both rows if the downstream Algorithm-5 code requires a standalone copy.

## Exact operation-count comparison for N=32768

Baseline first MonomialGenExtra:
- 28 ct-ct mult+relin+rescale
- 15 pt-ct masked mult+rescale
- no rotations inside this substage
- output basis depth 16
- x^(N/2) depth 14

CPB:
- 15 ct-ct mult+relin+rescale
- 15 row-swap automorphisms
- about 30 public selector pt-ct multiplications, all intended to be no-rescale
- additions
- output basis depth 15
- x^(N/2) still available at depth 14

Therefore the structural saving is:
- 13 fewer ct-ct multiplications
- one less multiplicative level
- in exchange for 15 automorphism/key-switch operations and ~15 additional cheap plaintext selectors.

This is not a claim of a native speedup yet.

## Selector scale/level gate

Important implementation correction:
the author imports Lattigo `schemes/bgv` under the local alias `bfv`, and creates `NewEvaluator(..., false)`, so the current implementation uses standard BGV-style tensoring rather than BFV scale-invariant tensoring.

Nevertheless, in Lattigo v6.2.0 the standard BGV `Mul(ct, []uint64)` path:
- creates a temporary plaintext with metadata copied from the ciphertext,
- explicitly sets plaintext Scale=1,
- encodes the vector,
- uses standard tensoring.

Therefore a selector vector multiplication:
- does not drop a level by itself,
- preserves ciphertext scale (scale * 1),
- can be used without an immediate Rescale at the API/metadata level.

STATUS:
- SELECTOR_SCALE_LEVEL_GATE: PASS_SOURCE

Caveat:
API-level scale correctness is not the same as a noise proof. Coefficient-domain noise growth from repeated encoded slot masks remains unresolved.

## Depth / modulus consequence

The author's own planner gives for r=2^ell, ell>1:

monomialOutputLevel(input,r) = input - ell - 1

while the retained x^(r/2) is at:

input - (ell-1).

CPB gives:
- full basis at input-ell
- x^(r/2) at input-(ell-1).

Thus CPB structurally saves one level for the basis while preserving the downstream auxiliary-power level.

For the current 9-bit path:
- baseline input to polyeval is L18 and ctP is L2;
- CPB would make ctP naturally available at L3 while keeping x^(r/2) at L4.

It may therefore be possible to remove one Q prime and retune the downstream x^r / s=2 / BatchLT / leading-term path, but this is NOT yet proven because the downstream grouped-power and tail levels must be replanned together.

STATUS:
- ONE_Q_PRIME_REMOVAL: PLAUSIBLE_NOT_ESTABLISHED

## Rotation-key footprint

Step 1 for the current m=1,n=2048 setting uses column rotations because its inner period is 2048 < r=32768. It does not use a high-level RowRotation.

The current polynomial path already uses the RowRotation Galois element at a low level. CPB would require the same Galois element at the high polynomial-input level.

Therefore:
- CPB does NOT need 15 distinct new rotation keys;
- it needs one existing Galois element promoted/generated at a higher Q level.

From the current key-size table, this is likely a tens-of-MiB increase if parameters are otherwise unchanged, not 15x that amount.

STATUS:
- KEY_COUNT_PENALTY: ONE_HIGH_LEVEL_ROW_KEY
- EXACT_SIZE_AFTER_RETUNE: NATIVE/PARAMETER_REPLAN_REQUIRED

## Noise gate

Baseline BuildBasis contains 28 ct-ct multiplications, each followed by relinearization; CPB contains:
- 15 ct-ct/relinearizations
- 15 automorphism key switches.

Thus the number of gadget/key-switch-like events is roughly 28 versus 30, not 28 versus 15.

This is encouraging but not decisive:
- CPB rotation noise is injected before later nonlinear multiplications.
- no-rescale selector masks may increase coefficient-domain noise.
- the author deliberately rescales the current MonomialGen masked factors.

On the other hand, the current public 9-bit run shows the final RLWE-to-LWE key switch dominates the final Q'-domain noise:
- max pre-final-KS noise in the public summary: 91
- max KS-added noise: 7625
- max after-final-KS: 7632.

So a moderate increase in pre-final-KS noise could still be hidden by the existing tail KS, but intermediate decryptability must be checked separately.

STATUS:
- NOISE_HEADROOM: PLAUSIBLE
- INTERMEDIATE_DECRYPTABILITY: NOT_ESTABLISHED
- NATIVE_NOISE_GATE: REQUIRED

## Prior-art gates

### IBM root-product rotation method — US 12,562,886 / US20250293854A1

This is an important conceptual neighbor:
- duplicate x across slots,
- subtract known roots,
- multiply terms,
- repeatedly rotate and multiply,
- exploit free slots / merging.

It demonstrates that the broad idea "use spare SIMD slots + rotation to trade for fewer multiplication-tree operations" is prior art.

However it is root-product based:
P(x)=c*prod_i(x-r_i),
and explicitly relies on knowing the polynomial roots offline, with CKKS/real-complex examples.

The arbitrary LUT interpolation polynomial in 2026/975 over F_q is not guaranteed to split completely into linear factors over F_q. Moving to an extension field would change the plaintext-slot model and parameters.

Decision:
- BROAD_SPARE_SLOT_ROTATE_MULTIPLY_NOVELTY: REJECT
- EXACT_ARBITRARY_FINITE_FIELD_POWER_BASIS_COLLISION: NOT_FOUND

### Okada–Player–Pohmann, ASIACRYPT 2023 / ePrint 2023/1304

Their O(log d) route uses Frobenius/Galois structure inside a plaintext slot of extension degree d and norm/minimal-polynomial structure.

2026/975 intentionally takes q = 1 mod 2N, so the plaintext ring splits completely and each slot is rank 1 over F_q. The nontrivial within-slot Frobenius route therefore degenerates.

Decision:
- DIRECT_COLLISION: NO

### Zhao et al., CRYPTO 2026 / ePrint 2026/1089

This work extends the Okada-style high-rank-slot polynomial evaluation to non-power-of-two slot degree d and gives improved treatment when D>d.

Public abstract-level information still parameterizes the gain by slot extension degree d. In the fully split d=1 setting of 2026/975, it does not provide an O(log D) arbitrary-polynomial evaluator.

Full ePrint PDF acquisition is currently blocked, so do not claim full-paper coverage.

Decision:
- ABSTRACT_LEVEL_DIRECT_COLLISION: NO
- FULL_PRIOR_ART_GATE: SOURCE_REQUIRED

### Park et al. / Sylph-style slim polynomial evaluation (2026)

This is another close conceptual neighbor using spare slots and rotations to reduce nonlinear evaluation work, but it relies on numerical/real polynomial decompositions (e.g. sum-of-squares structure) in CKKS.

No exact arbitrary finite-field LUT power-basis collision has been established.

## Current decision

Candidate name:
CPB — Co-Packed Dyadic Power Basis for the 2026/975 m=1 sparse BFV/BGV functional bootstrap.

Status:
- CORRECTNESS_RECURSION: PASS_SYMBOLIC / PASS_ALGEBRA
- SOURCE_INTERFACE_GATE: PASS
- EXACT_OPERATION_COUNT: PASS
- DIRECT_PRIOR_ART_COLLISION: NOT_FOUND
- BROAD_IDEA_NOVELTY: NOT_NEW
- NOVELTY: UNCLEAR / MUST_BE_NARROWLY_CLAIMED
- PERFORMANCE: NOT_RUN
- NOISE: NOT_RUN / INTERMEDIATE_BOUND_REQUIRED
- CURRENT_VALUE: PROMISING_THEORY_CONDITIONAL
- CODEX_NOW: NO (quota unavailable)
- NATIVE_EXPERIMENT_LATER: YES

This candidate does not supersede B145+B152 and does not modify B157.

## Cheapest next gates

1. Derive a conservative intermediate-noise comparison for one CPB recurrence versus one baseline MonomialGen layer, paying attention to encoded 0/1 mask coefficient norms.
2. Replan the 9-bit level schedule with CPB to decide whether one 34-bit Q prime can actually be removed while preserving the s=2 grouped-power and tail path.
3. Only after 1–2 pass, prepare a minimal native patch/benchmark:
   - m=1, 9-bit only;
   - replace only the first MonomialGenExtra basis stage;
   - same function/input seeds;
   - compare correctness, per-stage noise, BuildBasis latency, total online latency, eval-key size;
   - no generalization until that gate passes.
