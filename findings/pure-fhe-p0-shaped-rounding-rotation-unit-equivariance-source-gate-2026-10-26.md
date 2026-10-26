# PURE FHE P0 — Shaped-Rounding Rotation Unit Equivariance and Headroom Gate

**Date:** 2026-10-26 (Asia/Singapore) | **Stage:** `PURE-FHE-P0-PRESCOUT-05` (independent source-first prescout, not BOOT/SHIP/CGS official series).
**Decision:** `PARK_FREE_ROTATION_AND_NAIVE_UNIT_SWITCH_NOVELTY / SOURCE_BLOCKED_FINAL_COMPARISON`.
**Evidence:** DIRECT_AUTHOR_TECH_BLOG + PRIMARY_AUTHOR_ABSTRACT + independently derived elementary exact algebra; **NOT** complete verified 2026/2513, 2531, or 2562 PDF theorems; no native benchmark or novel construction.
**CODEX:** `NOT_RUN`. Prior `findings/pure-fhe-p0-guard-slot-precision-rotation-orbit-novelty-gate-2026-10-26.md` records the subgroup-invariant protected-slot obstruction.

## G0 full-source status

PI-supplied `papers/supplied/` checked via GitHub Notes as of this iteration: only `2025-1594.pdf`, `2025-1760.pdf`, `2025-1845.pdf`, `2025-395.pdf`, `eprint-2025-286-official-2026-revision.pdf`, README; **no** 2026/2513, /2531, /2562. Research ePrint PDF acquisition was previously BLOCKED (HTTP403; author/version mirror not authenticated), and none was silently treated as read.

High-authority author source: Jules Dumezy, **Shaped Rounding: Trading Empty Slots for Precision**, Oct 19, 2026, `https://jdumezy.com/blog/shaped-rounding/`, authored companion to ePrint `2026/2513`: `https://jdumezy.com/publications/new-scheme/`. Author gives **actual algebra**, admissible rotations, bounds, bootstrapping implementation and benchmark, and comparison to independently published Focal Units / GCKKS. Read and indexed from publicly accessible author site; no full submitted PDF article fetched.

Author publication abstract / mirror for Cheon–Lee, **High-Precision CKKS with Focal Units**, `https://eprint.iacr.org/2026/2531` and `https://eprint.iacr.asia/2026`, states cyclotomic-unit focused rescaling/key switching, lower modulus costs at reduced active slots and bootstrapping. Full text not audited.
Author abstract/index for GCKKS `2026/2524` and high-precision bootstrap `2026/2600` indicates a **decryption-factor/ciphertext conversion framework** not requiring that factors be units, and joint error-cleaning of two outputs; do not independently reinvent factor conversion as novelty. `2026/2562` precision allocation also competing. All full latest source still source-gated.

## ONE primary hypothesis and test

`H_FREE_STATIC_UNIT`: Given CKKS shaped rounding with a fixed public ring unit g selected to make errors small on data slots, any desired slot rotation `tau` can preserve the *same* shaped-error distribution for the *same fixed selected slots* without changing unit, reindexing, converting, or modifying other algorithm interfaces.

**Decisive symbolic test:** write shaped rounding exactly as `R_g(x) = g · RoundCoeff(g^{-1} x)`. On the power-of-two cyclotomic ring `Z[X]/(X^N+1)`, a Galois automorphism maps a monomial basis coefficient vector through a signed permutation. Assuming signed-equivariant ties in nearest-integer rounding (or no ties),
```
tau(R_g(x))
 = tau(g) · tau(RoundCoeff(g^{-1}x))
 = tau(g) · RoundCoeff(tau(g)^{-1} tau(x))
 = R_{tau(g)}(tau(x)).
```
This **exact equivariance is with the transported unit tau(g), NOT necessarily the original g**. Source's replicated subring unit is fixed by or magnitude-aligned with its *admissible* rotations; author explicitly warns rotation by +1 can move guard errors to data. A sufficient free-unit condition is `tau(g)=g` (more generally the same rounding parallelepiped can arise from basis symmetries e.g. signed monomial factors; exact equality is not claimed necessary). In general `R_{tau(g)} != R_g` at fixed positions, so `H_FREE_STATIC_UNIT` fails without admissibility / representation update.

Quantify distortion for *conditional* public-unit embedding magnitudes `h_i=|sigma_i(g)|>0`, data slots `S`. The relative envelope amplification when a rotation k is interpreted with the original g is
```
kappa_k(S,g) = max_{i in S} h_{i-k}/h_i
```
for a consistently chosen +k slot convention. Taking max over **all** cyclic shifts gives
```
max_k kappa_k(S,g) = (max_j h_j) / (min_{i in S} h_i).
```
This follows by choosing one shift that maps a globally largest-magnitude guard slot into the smallest-magnitude target data slot. It is an envelope ratio for the same base coefficient-rounding error bound, **not a measured actual-noise amplification nor a loss of that many precision bits on every input**. In particular author reports one-data-per-R=16 unit suppressing data slot magnitudes by about 46 bits, no guard slot amplified by more than about 4.6 bits, and unit-product volume `prod_i h_i = 1`. Since all data slots are suppressed and product one, some guard must have `h_j>=1`; hence one **permitted arbitrary shift** would entail an envelope factor of at least about `2^46` against a protected data slot, *under the stated ideal repeated shape and no conversion assumptions*. Authors disallow this as free operation. Do not imply that +1 specifically reaches the worst guard or that g itself has a security flaw.

**Important escape route/novelty check:** Dynamically tracking `tau(g)` or transporting the protected set is mathematically natural. But it changes which slots are protected, output/scale semantics and potentially subsequent rescale, multiplication and bootstrapping. Multiplication by public unit `h=g/tau(g)` makes shaped error compatible with g but also multiplies the **message**: from `mu'=Delta tau(m)+tau(g)e'`, one obtains `h mu'=Delta h tau(m)+g e'`; to preserve `tau(m)` under *fixed scalar scale* needs a compensating representation/scale action, not an automatically free fix. These operations are already broadly anticipated by the author's **bidirectional CKKS conversions with shared keys**, and concurrent GCKKS conversion framework, so generic 'coordinate conversion' is not new.

## Source-headroom sanity check

Author blog concrete single-thread **16 values** / restore **16 levels**:
- Sparse CKKS N=2^16, precision 19.9 bits, **3.77 s**.
- Shaped rounding N=2^15, precision 22.9 bits, **0.75 s**.
- Same shaped N=2^15, restore 21 levels 22.8 bits, **0.86 s**.
Thus original reported **~5.03× single-thread** for 16 levels and an optimistic **3.02 seconds absolute per-bootstrapping latency budget** before the advantage disappears in an otherwise-identical matched workload. The author reports **3.6–3.7×** on **18 cores**. Prior FHERMA third-party card's 3.6× **single-thread** is inconsistent with these author numbers; do not repeat it. These are author-reported comparisons at unequal ring degrees and slightly different precision, **not independently measured nor evidence of uncounted general rotations being cheap**. If a target circuit requires q conversions each with latency `Tconv`, and other overhead `DeltaT`, a *necessary benchmark break-even* (under the same experiment and other work) is `q Tconv + DeltaT < 3.02 s`; no conversion timing/accuracy measured, no such performance is asserted.

## Research decision

`PASS`: source-authored structural comparison and exact `tau R_g=R_tau(g) tau` derivation.
`FAIL`: no-cost reuse of unchanged focusing unit g under unrestricted rotations in static data layout.
`FAIL_NAIVE_NOVELTY`: 'use a unit, shape error toward guard', same public coordinate change between Focal CKKS/GCKKS and shaped rounding in unit case, and generic conversion to/from CKKS — author publicly states the equivalences and conversions.
`UNCLEAR`: dynamic generalized shaping-unit metadata for arbitrary nonlinear circuits, whether concurrent focal/precision-allocation/full GCKKS papers already cover it, real converter/bootstrapping key storage and end-to-end cost.

**Decision:** `PARK_GENERIC_ROTATION_AWARE_UNIT_SWITCH_CONSTRUCTION` until 2026/2513, 2531, 2562 *complete source* verified. Do not launch a fourth adjacent algebra toy; this is NOT a high-value novel mechanism yet. User can provide current PDFs under `papers/supplied/` if desired. Continue the broad PURE-FHE P0 by searching another **source-complete** cost-defined structural primitive, reusing prior SHIP/BOOT failures as screening, without overriding their official series. If a new provable complexity feature from missing articles is confirmed, reopen one smallest claim and one decisive test.

**End:** `STATUS=FAIL_FREE_STATIC_G_UNDER_ALL_ROTATIONS / SOURCE_GATE`; `RESULT=SHAPED_ROUNDING_AUTOMORPHISM_EQUIVARIANCE + AUTHOR_HEADROOM`; `NOVELTY=NOT_ESTABLISHED`; `NEXT_TEST=COMPLETE_SOURCE_2026_2513_2531_2562_OR_PIVOT_COMPLETE_SOURCE_PURE_FHE`; `CODEX=NOT_RUN`; `STATE_UPDATE=THIS_NOTE_ONLY`.
