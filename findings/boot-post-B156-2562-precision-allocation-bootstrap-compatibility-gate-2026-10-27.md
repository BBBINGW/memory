# BOOT post-B156 — 2026/2562 precision allocation × bootstrap compatibility gate

Date: 2026-10-27
TRACK_ID: BOOT
State impact: NONE. Do not modify B157 pending state.
No Codex / GPU / remote execution was used.

## Source status

Target:
- ePrint 2026/2562, Zhaoyang Liang, Runkun Liu, Jingwei Fang, Dan Ding,
  *A New Approach to Reducing Modulus Requirements in Homomorphic Computation: Precision Allocation in CKKS*.

Full PDF is currently unavailable through the configured source chain:
- IACR PDF path: blocked / HTTP 403;
- exact-title arXiv: not found;
- fixed GitHub ePrint mirror: not synchronized;
- Library search: no verified full copy found;
- GitHub search: no author implementation/slides found.

Therefore this finding does NOT claim full-paper coverage.

Public abstract facts:
- modulus budget is made to depend on average rather than maximum precision requirements;
- arbitrary output precision can be allocated among independent packed values subject to decryption correctness;
- standard CKKS ciphertext format is preserved;
- no extra cryptographic assumption beyond CKKS IND-CPA;
- with 64-bit average precision requirement, the authors report transferring 75 bits without lowering depth and up to 735 bits while preserving initial recovery, with target-value precision as high as 2269 bits;
- for six squarings of 256 messages targeting 224-bit precision, the reported initial modulus bit length is reduced by 67%, allowing a 4x smaller ring dimension.

This is a high-value parameter-law result, not a kernel constant-factor optimization.

## Question

Can heterogeneous / average precision allocation be used directly to reduce the modulus consumed by a conventional CKKS bootstrap?

We deliberately do NOT assume that dense CtS/StC linear mixing alone kills the idea. A unitary transform preserves L2 error energy, so average-error reasoning may remain meaningful through linear transforms.

The critical gate is the nonlinear EvalMod / cleaning stage.

## Simplified standard-bootstrap model

Consider the core map

F(x) = A^{-1} g(Ax),

where:
- A is a dense Fourier/CtS-type linear transform;
- g is the coordinatewise nonlinear modular-reduction / cleaning map;
- A^{-1} models the inverse/StC-side recombination.

Let e be a small slot-domain perturbation induced by heterogeneous CKKS approximation error.

Linearizing at x gives

delta F ~= J(x)e,

with

J(x) = A^{-1} diag(g'(Ax)) A.

### Fourier consequence

For a Fourier A, A^{-1} diag(d) A is circulant, where d_j = g'((Ax)_j).

This matrix is diagonal for all coordinates iff d is constant, i.e. all internal coordinates have the same derivative.

For a genuinely nonlinear g and arbitrary packed inputs, g'((Ax)_j) is generically not constant.

Therefore J generically has nonzero off-diagonal entries.

Consequence:
a low-precision donor slot's error contributes at first order to a different high-precision target slot after nonlinear bootstrap.

This is stronger and more precise than the informal statement "DFT mixes the slots":
- pure linear mixing can preserve an average/L2 budget;
- the problem is that nonlinear coordinatewise processing breaks the cancellation/isolation needed to recover heterogeneous per-slot precisions.

## Two-slot sanity model

Take the Hadamard transform

A = 1/sqrt(2) [[1,1],[1,-1]].

Then z_+ = (x+y)/sqrt(2), z_-=(x-y)/sqrt(2).

The local error transfer is

J = A^T diag(g'(z_+),g'(z_-)) A

  = 1/2 [[g'_+ + g'_-, g'_+ - g'_-],
         [g'_+ - g'_-, g'_+ + g'_-]].

Thus donor y contaminates target x with coefficient

(g'_+ - g'_-)/2.

It vanishes only when the two internal derivatives agree.

For arbitrary x,y under nonlinear EvalMod, that equality cannot be guaranteed.

Hence a high-precision target cannot in general be protected from an arbitrarily low-precision donor merely by assigning different input precisions and then running the standard nonlinear bootstrap unchanged.

## Necessary condition for bootstrap-aware precision allocation

To reduce bootstrap's own modulus under heterogeneous precision requirements, a construction needs at least one of:

1. Precision isolation:
   nonlinear internal coordinates used for a high-precision target do not depend on low-precision donor slots.

2. Precision reset:
   low-precision/background coordinates are re-encoded / cleaned / reset before they can contaminate the target nonlinear path.

3. Structured equal-derivative regime:
   the internal nonlinear map acts with effectively identical derivative on all coordinates that mix into a target.
   This is fragile and generally incompatible with arbitrary inputs / modular branches.

4. Special encoding / transform:
   the physical transform is redesigned so precision classes are block-local or guarded.

Therefore:
- STANDARD_BOOTSTRAP_DIRECT_PRECISION_ALLOCATION: FAIL_GENERIC_FIRST_ORDER_ISOLATION
- LINEAR_CTS_STC_ALONE: NOT_A_NO_GO
- NONLINEAR_EVALMOD_MIXING: THE_DECISIVE_OBSTRUCTION

## Prior-art boundary

### 2026/2531 — High-Precision CKKS with Focal Units

Public abstract:
- Focused CKKS trades unused SIMD slots for precision using cyclotomic/focal units;
- using only 1/k of slots gives about k times as many precision bits at the same scaling factor/parameters;
- different precision requirements across slots are supported;
- a dedicated bootstrapping procedure is constructed;
- only the base modulus needs to grow with target precision, while the rest of bootstrap keeps approximately constant modulus consumption by using fewer slots;
- discrete-CKKS cleaning in Focused CKKS further reduces the base modulus by about the same factor k.

This is a direct prior-art collision with the broad idea:
"heterogeneous slot precision + a special bootstrap."

Any follow-up must beat its slot-capacity tradeoff or target a materially different precision profile.

### 2026/2600 — High-Precision Bootstrapping for GCKKS

Public abstract:
- slot-count/decryption-factor conversion;
- slot-aware bounds on unused slots;
- CKKS->GCKKS conversion that resets unused slots;
- precision-dependent bootstrap stages use O(k) operations and O((p/k) log k) modulus bits for 2N/k useful slots.

This is direct prior art for precision reset and slot-aware bootstrap conversion.

### 2026/2513 — shaped rounding / guard-domain CKKS variant

Public author material states:
- unused slots serve as guard domain;
- bootstrap forward transforms read only data slots;
- guard slots are written back as zeros / not imported into data;
- security remains RLWE with CKKS-like parameters.

This is direct prior art for transform-level precision isolation using background/guard slots.

## Novel extension space after prior art

A generic "precision-aware bootstrap" is already crowded.

The only fresh-looking question left from 2562 is much narrower:

Can arbitrary or fine-grained precision classes be bootstrapped while:
- retaining standard CKKS format,
- avoiding the roughly 1/k useful-slot loss of Focused CKKS / GCKKS-style methods,
- and preventing nonlinear EvalMod cross-contamination?

Call this tentative question:
CAPACITY-PRESERVING HETEROGENEOUS-PRECISION BOOTSTRAP.

Current status:
- mathematical obstruction for unchanged dense bootstrap: PASS / NO-GO;
- known guard/focus/slot-trade methods: strong prior art;
- capacity-preserving construction: NOT_FOUND;
- 2562 full text: SOURCE_REQUIRED;
- novelty: NOT_ESTABLISHED.

Do not promote this to a main candidate without 2562 full text and a construction that avoids the existing slot-capacity tradeoff.

## Decision

2026/2562 itself remains HIGH_VALUE_SOURCE_REQUIRED because its reported modulus/ring-dimension savings are unusually large.

But as a BOOT extension:
- DIRECT_STANDARD_BOOTSTRAP_APPLICATION: FAIL
- GENERIC_PRECISION-AWARE_BOOTSTRAP: PRIOR_ART_CROWDED
- CAPACITY-PRESERVING_FINE-GRAIN_PRECISION_BOOTSTRAP: OPEN / SPECULATIVE
- NATIVE_PRIORITY: NO until source + construction
- CURRENT_ACTION: PARK_SOURCE_REQUIRED

This finding does not change B145+B152 or B157.
