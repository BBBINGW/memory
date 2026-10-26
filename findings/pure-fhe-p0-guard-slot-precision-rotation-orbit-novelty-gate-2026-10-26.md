# PURE FHE P0 — Small-Batch Precision Shaping × Rotation-Orbit Novelty Gate

**Date:** 2026-10-26 (Asia/Singapore)
**Stage:** `PURE-FHE-P0-PRESCOUT-04`; a new topic selection after parking Sparse LCR+AKS. **No BOOT/SHIP/CGS/I-series status change**.
**STATUS:** `FAIL_FREE_ARBITRARY_ROTATION / PRIOR_ART_SATURATED / SOURCE_BLOCKED_FOR_NEW_CONSTRUCTION`.
**EVIDENCE:** fresh 2026 *author abstracts & blog* + ePrint listings; independent mathematical orbit lemma verified with exact JS enumerations. NOT primary full-PDF algorithm proof or FHE native benchmark.
**CODEX:** `NOT_RUN`.

## Objective / single smallest falsifiable claim

Screen whether a new pure-FHE representation can reserve otherwise-unused complex CKKS slots as a **static error guard band** at no communication/computation cost and still allow an *arbitrary rotation-heavy CKKS circuit* without forfeiting protected-slot precision or changing the ciphertext representation.

`H_FREE_ROTATIONS`: There exists a fixed proper nonempty subset `S⊊Z_n` of 'data slots' which remains unchanged by *every* rotation from the intended circuit, including rotate(+1), hence an unmodified fixed-guard/no-conversion pipeline can use all those rotations and keep data/noise slots separated.

## New immediate strongest prior art (explicit current web sources)

1. **Jules Dumezy**, **Fully Homomorphic Encryption for Small Batches of Complex Numbers**, ePrint `2026/2513` (October 2026), author abstract `https://jdumezy.com/publications/new-scheme/`, author explainer `https://jdumezy.com/blog/shaped-rounding/` (2026-10-19). Public ring unit `g`, shaped rounding error directed into unused guard slots, generalized scaling `g^{-1}Δ`, small cyclotomic subring replication preserving **admissible** rotations and traces, native bootstrapping reading data slots only, CKKS conversion with shared keys, 128-bit-target poulpy implementation. Author reports ring N=2^15 and batches 16/64 retaining 21 levels and ≥22.6 bits minimum precision over 21 sequential products; for 16 restored levels about 5× faster **against sparse-CKKS needing N=2^16**. Different ring dimensions mean raw ratio is for matched functional/specified security targets, NOT a microbenchmark isolating the shaped rounding kernel. An independent FHERMA Radar editorial lists **3.6×**, differs from author site reported ~5×; figures may be source-version/measurement-scope dependent. DO NOT recompute or assert exact consensus without full source and aligned table: https://www.fherma.io/radar/jules-dumezy-proposes-ckks-bootstrapping-with-guard-band-precision .
2. **Cheon and Lee**, **High-Precision CKKS with Focal Units**, ePrint `2026/2531` (2026-10-20). Cyclotomic-unit-based focused rescaling/key-switching, 1/k useful slots -> ~k times more precision bits at equal scale, supports heterogeneous slot precision and tailored bootstrapping, per public ePrint abstract. Already covers simple 'spend unused slots to protect selected slots', focus rather than blanket all-SIMD precision.
3. **Liang, Liu, Fang, Ding**, **A New Approach to Reducing Modulus Requirements in Homomorphic Computation: Precision Allocation in CKKS**, ePrint `2026/2562` (2026-10-22). Vary precision budgets across independent values while preserving standard CKKS ciphertext form; reports six squarings/256 messages, 67% initial logQ reduction and 4× reduced ring dimension at a high-precision workload, per public abstract. Cannot claim differential precision-allocation is novel without examining full theorem/cost.
4. **Ma, Liu, Wang, Wang**, **Homomorphic Encryption for High-precision Arithmetic of Approximate Numbers**, ePrint `2026/2524` (2026-10-22), and **High-Precision Bootstrapping for GCKKS**, `2026/2600` (2026-10-22). GCKKS uses fewer slots for high precision and new ciphertext-conversion/precision-doubling bootstrapping; newer paper already claims single polynomial cleaning of two outputs. DO NOT suggest 'one cleaning for two outputs' as new.
5. **Liu, Ma, Wang, Wang**, **Efficient (Functional) Bootstrapping for CKKS over the Conjugate-Invariant Ring**, ePrint `2026/2618` (2026-10-25). Native real FFT over conjugate-invariant ring and native functional bootstrapping; author abstract reports 1.46–1.80× for native single CI-CKKS bootstrap over CI↔standard conversion, no direct full-PDF verification.
6. **Existing archived lines**: `findings/pure-fhe-p0-sparse-lcr-aks-one-evalmod-repack-compatibility-gate-2026-10-26.md` PARK, `findings/ckks-lcr-aks-sparse-subsum-fourier-projection.md` proven algebra/negative system cost, SHIP and BOOT source findings untouched.

## Exact cheapest test — rotation-subgroup orbit obstruction [DERIVATION]

Idealized logical slot positions form cyclic group `Z_n`, with rotation `R_k(j)=j+k (mod n)`. An implementation promising that a single *unchanged* protected-slot set `S` survives ALL requested rotations `K={k_1,...,k_r}` without reindexing/re-encoding must obey `S+k=S` for each k∈K. Let `d=gcd(n,k_1,...,k_r)`. Subgroup H generated by the rotations is `d Z_n`, has size `n/d`, and partitions Z_n into `d` disjoint cosets. For `S` to be invariant, it must be a union of cosets; hence a nonempty such S has cardinality `|S|≥n/d`. If `K` includes rotate(1), `d=1`, so the only invariant sets are empty and all n slots: `S=Z_n`. For nontrivial fixed guard bands, a *free arbitrary rotation* guarantee is impossible **under this invariant-set model**.

**Exact enumeration / examples**:
- `n=32768, K={1}`: d=1; smallest nonempty rotation-invariant S=32768 (no guard slots).
- `K={2}`: d=2; min S=16384 (at most 2-way focus).
- `K={4,8}`: d=4; min S=8192 (at most 4-way focus).
- `K={8,16}`: d=8; min S=4096 (at most 8-way focus).
- `K={512,1024}`: d=512; min S=64 (at most 512-way focus).
All subgroup closures independently enumerated for n=16 in four controls: [1],[2],[4,8],[2,8], sizes equal n/d.

This is elementary additive-group theory, NOT a new cryptographic lemma and NOT a claim about full Galois action ordering, rotated embedding coefficients, RLWE noise or source-specific selected public unit `g`.

**Shaped-error algebra illustration, conditional on constant public unit**: If ideal canonical-embedding error has form `e=g·u` and automorphism τ permutes slots, its new factor is `τ(g)`. Protecting fixed data slots S uniformly requires bounding `κ_τ(g,S)=max_{i∈S}|τ(g)_i|/|g_i|`. If τ transports large-magnitude guard components into data positions, κ can be large, leading to reduced guaranteed precision. Correctly updating the decryption factor or performing a representation conversion might maintain semantics but is NOT a free unchanged-representation rotation. Source 2026/2513 explicitly restricts protection to admissible rotations, consistent with this concern.

**LIMITATION:** If application allows dynamic data-slot labeling, free logical rotation by permuting the tracked focus metadata, or encodes replicated values so the protected set is not the same mathematical S, H_FREE_ROTATIONS does not describe it. The formal paper may already provide a re-encoding/rotation mechanism; absent original text one cannot assert an unaddressed open problem or any security flaw. No physical FHE runtime, no cipher noise estimates, no encryption security tests.

## Novelty/value gate and next single target

- `FAIL` ordinary static guard/focus + free unrestricted rotations (invariance necessary condition).
- `FAIL_PRIOR_ART` merely use free slots for extra precision, heterogeneous precision, native CI CKKS and GCKKS 'single cleaning two outputs'.
- `SOURCE_BLOCKED`: GitHub Notes Research MCP `get_eprint_paper` failed to obtain current readable full PDF for 2026/2513, 2531, 2562, 2524, 2600, 2618 (official ePrint pdf HTTP403 and no exact arXiv/mirror for tests). Author blog/abstract are partial descriptions only.

**DECISION:** `PARK_STATIC_GUARD_ANY_ROTATION`. ONE conditional candidate to re-evaluate upon full sources: **rotation-aware shaped-noise / heterogeneous-precision representation conversion** for actual rotation-heavy applications, with explicit conversion/key switching/guard amplification + online rounding costs. This is not a new construction, and may be fully handled by the latest Focused CKKS or Precision Allocation papers; benchmark must match n,N, security, encoding precision, required rotation set K, CKKS RNS levels, memory, and full iterative circuit latency.

**Source priority for next gate:**
P0a. PI-supply/read `2026/2513` and `2026/2531` full PDFs, examine precise admissible automorphism theorem, normalization/conversion, key preservation and costs;
P0b. `2026/2562` PDF to rule out dynamic or heterogeneous precision allocation prior art;
P1. `2026/2524`, `2026/2600`, `2026/2618` full texts for close complementary headroom, only if a specific hypothesis survives.
Do not run further toy tests in this small-batch precision line without a source-supported novel invariant and a credible end-to-end win.

**End of iteration:** `STATUS=FAIL_FREE_STATIC_ROTATION / CURRENT_PAPERS_SOURCE_BLOCKED`; `RESULT=GROUP_ORBIT_NECESSITY_AND_STRONG_2026_PRIOR_ART`; `NOVELTY=NOT_ESTABLISHED`; `NEXT_TEST=AUTHOR_FULL_TEXT_ROTATION_COMPOSITION_GATE`; `CODEX=NOT_RUN`; `STATE_UPDATE=THIS_FINDING_ONLY`.
