# BOOT — Multi-Output Hoisted Linear-Transform Gate

**Date:** 2026-10-30
**TRACK_ID:** BOOT
**ACTIVE_SUBLINE:** B158_CHECKPOINT_DECOUPLED_HALF_BASIS
**Logical turn:** Research Turn 25/25 retry; same turn, not a new turn
**Result:** FAIL_STOCK_CROSS_BRANCH_HOIST / CUSTOM_COMMON_SOURCE_WEIGHTED_TRACE_NOT_COST_EFFECTIVE_AT_K5

## Hypothesis

For the five independently projected RMFE thin branches, HElib's repeated thin SlotsToCoeff/CoeffToSlots transforms may admit a multi-output hoisting optimization that shares expensive automorphism/key-switch decomposition work across branches, without merging ciphertexts and without changing the secret/evaluation-key assumption.

Falsifier:
if HElib hoisting is intrinsically per-ciphertext and the current m=32768 geometry leaves only tiny D=2 transforms shareable while the dominant inverse trace remains branch-specific, then this family does not provide the desired k-fold linear-phase saving.

## Pinned source provenance

HElib:
homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

Relevant pinned source:
- src/EvalMap.cpp
- src/matmul.cpp
- src/recryption.cpp

### Hoisting semantics

src/matmul.cpp documents BasicAutomorphPrecon as:

"Pre-computation to speed many automorphism on the same ciphertext."

Its constructor canonicalizes one Ctxt and executes

ctxt.parts[1].breakIntoDigits(polyDigits)

then stores those gadget digits.
Each subsequent automorph rotates the stored digits and calls keySwitchDigits.

Thus the expensive decomposition being hoisted is data-dependent on one ciphertext's part[1]. It is not a key-only cache and cannot be reused exactly for another branch ciphertext.

The radix/gadget decomposition has carries; it is not a linear map from a common source that lets the exact digit vectors of arbitrary projected branches be reconstructed from one source decomposition.

Therefore stock HElib cross-branch hoisting is source-level unavailable.

## Exact thin-transform geometry

Current pinned parameters:
m=32768,
p=5,
phi(m)=16384,
ord_m(5)=8192,
nslots=2.

For the current power-of-two m, the bootstrap mvec has one nontrivial factor:
mvec=[32768].

ThinEvalMap then has:
nfactors=1,
phivec[0]=16384,
dvec[0]=8192,
reduced dimension D=phivec[0]/dvec[0]=2.

Hence the explicit MatMul1D part of either thin map is only a two-slot transform.

### SlotsToCoeff

ThinRecryptData constructs

slotToCoeff = ThinEvalMap(context.getEA(), ..., invert=false).

With nfactors=1 and D=2, this is one 2x2 public linear transform.
Its ciphertext cost contains at most one nontrivial slot automorphism.

Across five branches, an ideal common-source implementation can therefore remove at most four such automorphisms. This is a small constant saving, not a 5x middle-phase collapse.

### CoeffToSlots

ThinRecryptData constructs

coeffToSlot = ThinEvalMap(*ea, ..., invert=true).

ThinEvalMap::apply for invert=true executes:
1. the same D=2 MatMul1D transform;
2. traceMap(ctxt).

The D=2 transform can again contribute at most one nontrivial slot automorphism per branch.

The dominant extra stage is traceMap.

## Exact traceMap schedule for d=8192

src/matmul.cpp::traceMap sets

d = context.getOrdP() = 8192.

HELIB_TRACE_THRESH=50.
For d=8192, the FULL-short-table branch is not used.
For the non-MIN path, traceMap uses binary doubling.

Since

8192 = 2^13,

the loop has exactly 13 iterations and therefore exactly 13 Frobenius automorphism calls:
at accumulated exponents 1,2,4,...,4096.

Each automorphism is applied to the current branch-local trace accumulator, whose ciphertext changes after every step.

Thus baseline inverse-map trace work across five branches is

5 * 13 = 65

branch-specific Frobenius automorphisms.

Because the five accumulators differ, each requires its own gadget decomposition/key-switching work. A BasicAutomorphPrecon for branch i cannot be used for branch j.

## Can the common recryptEkey rescue the inverse side?

After independent rawModSwitch/newMakeDivisible, branch i has the form

u_i = z0_i + z1_i * E_s,

where E_s is the same encrypted boot secret and z0_i,z1_i are public branch-specific full-ring polynomials.

For the D=2 map, one automorphism of E_s can in principle be shared:

sigma(u_i)
 = sigma(z0_i) + sigma(z1_i) sigma(E_s).

Hence the one nontrivial D=2 automorphism can be reduced from five copies to one, saving four automorphisms.

But for the trace,

Tr(u_i)
 = Tr(z0_i)
 + sum_{j=0}^{8191} sigma^j(z1_i) sigma^j(E_s).

The weights sigma^j(z1_i) are branch-specific and arbitrary after the nonlinear raw-mod-switch/divisibility boundary.

The 13-step trace algorithm is cheap exactly because it repeatedly automorphs the evolving product z1_i*E_s and doubles an all-ones trace interval. Once one insists on a common source E_s, the weights are no longer all ones and the logarithmic recurrence is lost.

The problem becomes a generic weighted linear transform over the full 8192-element Frobenius orbit of E_s.

## Cost falsifier for a custom common-source transform

For a generic D-term cyclic linear transform, the standard baby-step/giant-step automorphism count is approximately

g + ceil(D/g),

minimized near g=sqrt(D).

For D=8192:

min_g [g + ceil(8192/g)] is about 2*sqrt(8192) ~= 181.

This common-source transform could feed all five outputs with different public multipliers, but its automorphism count is still about 181.

Baseline branch-local traces need only

5*13 = 65

automorphisms.

Therefore, at k=5, replacing the five structured short traces by one generic common-source multi-output transform is strictly worse even before accounting for the larger number of plaintext multiplications and accumulators.

This closes the only plausible route to large cross-branch inverse-map hoisting.

## Total transform-side ceiling

Ignoring public ct-pt multiplications and additions, the relevant automorphism counts are approximately:

Baseline:
- SlotsToCoeff D=2: 5
- CoeffToSlots D=2: 5
- CoeffToSlots trace: 65
- total: 75

Best cheap common sharing that preserves the short trace:
- shared SlotsToCoeff D=2 automorphism: 1
- shared CoeffToSlots D=2 automorphism of common E_s: 1
- branch-local traces remain: 65
- total: 67

Maximum structural reduction:
75 -> 67,
only 8 automorphisms, about 10.7%.

This is an optimistic ceiling; source plumbing and branch-specific constants can reduce the realized gain further.

It is nowhere near a k-fold collapse of the middle phase.

## Projection-side note

The five RMFE projections themselves are public trace maps of one common source ciphertext and share automorphism support.

A generic common-source multi-output implementation could hoist the source decomposition, but each degree-512 projection has a logarithmic 9-step trace when materialized branchwise. Five branches therefore use 45 structured trace automorphisms.

A generic common-source BSGS transform over 512 orbit positions needs about

2*sqrt(512) ~= 45

automorphisms before branch-specific output accumulation.

Thus even there, automorphism count does not improve at k=5; only decomposition scheduling changes. This is not a new large-gain candidate.

## Result matrix

- Stock BasicAutomorphPrecon across different branches: FAIL
- Share public transform constants: already available / low value
- Share D=2 SlotsToCoeff automorphism: possible, saves at most 4 calls
- Share D=2 CoeffToSlots automorphism of common recryptEkey: possible, saves at most 4 calls
- Share 13-step branch-local traces with stock hoisting: FAIL
- Replace five traces by one generic common-source weighted transform: cost-negative at k=5 (~181 vs 65 automorphisms)
- Projection-side common-source transform: no automorphism-count gain at k=5 (~45 vs 45)
- Native/Codex experiment justified: NO

## Scientific disposition

The candidate

five separate branches
-> cross-branch hoist ThinEvalMap automorphism/key-switch decomposition
-> retain exact branch semantics
-> obtain substantial middle-phase savings

is KILLED as a high-value path.

The reason is structural:

HElib hoisting amortizes gadget decomposition across many automorphisms of the same ciphertext. The current repeated transforms act on different branch ciphertext states. In the pinned m=32768 geometry, the only cheaply shareable pieces are the tiny D=2 transforms; the dominant inverse trace remains branch-local. Converting it to a common-source weighted transform destroys the 13-step logarithmic trace recurrence and is more expensive at k=5.

Small engineering reuse of the two D=2 automorphisms may remain, but it does not move the cryptographic/performance frontier.

## Portfolio impact

- S2 conditioning rescue: PARK
- Dense exotic basis search: PARK
- Stock cross-branch ThinEvalMap hoisting: KILL as high-value research path
- Generic common-source weighted trace at k=5: KILL on operation count
- High-level one-linear-phase objective remains prior-disclosed by Aung et al.
- No native experiment should be launched for this hoisting branch.

After this turn, the next session should reprioritize to a genuinely different BOOT mechanism/bottleneck rather than continue local RMFE linear-phase refactoring.
