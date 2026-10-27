# BOOT post-B156 fresh scout — 2026-10-27

TRACK_ID: BOOT  
State impact: NONE. Do not modify B157 pending state.  
B157 remains PENDING_CODEX_QUOTA.  
No Codex / GPU / remote execution was used.

## Scope

Fresh paper-level BOOT scouting only. Avoid repeating B145-B156 analysis.

## Scout A — ePrint 2026/2630: Exact Error Bootstrapping and Comb Bootstrapping in FHEW/TFHE

Public abstract-level facts:
- Error bootstrapping refreshes ciphertexts by recovering/lifting the encryption error rather than evaluating the message decryption function in the usual PBS manner.
- The construction is explicitly refresh-only; arbitrary function evaluation still requires programmable bootstrapping.
- Because the error takes fewer values than the ring dimension, multiple ciphertexts can be refreshed by one blind rotation (comb bootstrap).
- Reported abstract numbers: 8-bit single-thread refresh 3.5x vs TFHE-rs; comb refresh 9.1x; multiplication 6.5x; RNS multiplication for >=32-bit integers 19x.

### Algebra sanity gate: direct functional fusion

Smallest claim tested:
Can the same error-indexed blind rotation be made, at no extra message-dependent mechanism, to evaluate an arbitrary nonconstant function f(m) while refreshing?

Result: NO in the standard public-accumulator model.

Reason:
If the blind-rotation index depends only on error e, then two legal ciphertext states with the same e but different messages m0 != m1 induce the same rotation. A fixed public accumulator therefore reaches the same accumulator location for both. It cannot output f(m0) and f(m1) whenever f(m0) != f(m1) without introducing an additional message-dependent mechanism.

Decision:
- DIRECT_ERROR_BR_TO_FREE_FUNCTIONAL_PBS: FAIL_STRUCTURAL
- Do not pursue "free functional PBS fused into error bootstrap".
- Mixed refresh/PBS scheduling may still be a systems/compiler problem, but novelty is NOT established and appears weaker than a new cryptographic bootstrap primitive.

Source limitation:
Full 2026/2630 PDF could not be acquired by the configured ePrint/mirror path (HTTP 403 / mirror not yet synchronized). Do not claim full-paper coverage.

## Scout B — ePrint 2026/1730 / CRYPTO 2026: New Techniques for Fast and Shallow FHE Bootstrapping and Beyond

Public abstract / proceedings facts:
- CRYPTO 2026, pp. 428-460.
- Contribution 1: sparse small-norm LWE secret of dimension n and Hamming weight h reduces arithmetic multiplication work from ~O(n^2) to ~O(nh), with reported 4.5-7.5x practical speedup over OpenFHE for gate / functional bootstrapping.
- Contribution 2: Binary NTT RLWE + relinearization-free BV multiplication reduces sequential NTT/INTT layers to 3 versus >500 in standard FHEW/TFHE, while total 32/64-bit word-operation count remains comparable.
- Public wording only says this shallow design *suggests* lower latency on highly parallel architectures such as GPUs; no public abstract-level native GPU result for the Binary-NTT shallow construction was found.

### Fresh bottleneck

The important gap is not depth anymore; it is:
- work efficiency,
- memory traffic / key footprint,
- mapping the 3-layer DAG to real GPU resources without losing the theoretical shallow advantage.

This is a whole-bootstrap bottleneck and is more interesting than another local LUT/backend micro-optimization.

### Prior-art collision check

Do NOT pursue generic "sparse-secret GPU acceleration":
A 2026 follow-up, Compiling Sparse Keys for Bootstrapping FHEs: Algorithms, Hardware Acceleration, and Beyond, explicitly builds on Jain et al.'s sparse-secret idea in an NTRU setting and reports CPU/GPU results including RTX 4090, plus an NTT-free variant.

BOLT-FHE (TCHES/CHES 2026) also already gives a mature GPU TFHE bootstrap framework based on fused NTT/INTT/external-product/accumulator kernels and on-chip local tiling.

Therefore:
- GENERIC_SPARSE_GPU_TRANSPLANT: LOW_NOVELTY / CROWDED
- GENERIC_GPU_FUSION_OF_STANDARD_TFHE: CROWDED

The still-interesting target is specifically the Binary-NTT 3-layer construction and whether one can reduce *total work or memory movement*, not merely implement it.

### Security sanity branch

The name "Binary NTT RLWE" is not sufficient evidence that the secret is literally an arbitrary pointwise {0,1} vector in a full CRT/NTT representation. Therefore no idempotence or structured-secret attack claim is made here.

Status:
- BINARY_NTT_EXACT_DEFINITION: SOURCE_REQUIRED
- SECURITY_ATTACK_IDEA: UNCLEAR, DO NOT IMPORT FROM OTHER TRACKS WITHOUT DEFINITION

Full 2026/1730 text is currently not available through the configured ePrint/mirror path; an authorized supplied copy is needed before any algebra/security claim.

## Scout C — ePrint 2026/2616: Descent-PBS

Public abstract facts:
- Pays module rank only for first rotation, descends to ring, then continues Meta-PBS refinements.
- 16-bit negacyclic LUT: 196 ms single-thread; 128-bit security; model-predicted failure <2^-64.
- 16-bit key size reported as 1,208 MB.
- General 13-16 bit LUTs 179-368 ms, 3.8-6.6x faster than WoP-PBS in cited comparison, at about twice its memory.

Fresh bottleneck remains key/memory cost, but generic seeded compression is not novel. Any follow-up must exploit Descent-specific first-module-stage / module-to-ring structure.

Status:
- DESCENT_MEMORY_BOTTLENECK: REAL
- GENERIC_SEEDED_COMPRESSION: REJECT_AS_PRIOR_ART
- DESCENT_SPECIFIC_KEY_SHARING: UNCLEAR_SOURCE_REQUIRED

## Current fresh-research priority

P1: Obtain/read full 2026/1730 and test one narrow claim:
Can Binary-NTT's 3-layer bootstrap be made genuinely work-efficient or memory-traffic-efficient, rather than only depth-efficient?

Required order:
1. exact definition + algorithm DAG,
2. source cost table / parameters,
3. algebraic opportunities,
4. security assumptions,
5. only then implementation value.

P2: Obtain/read full 2026/2630 only to determine whether mixed refresh/PBS graph scheduling is already discussed; do not pursue direct free functional fusion.

P3: Descent-PBS memory/key bottleneck, only if a source-specific structural saving emerges.

## Source requests

Highest-value missing PDFs:
1. ePrint 2026/1730 — New Techniques for Fast and Shallow FHE Bootstrapping and Beyond.
2. ePrint 2026/2630 — Exact Error Bootstrapping and Comb Bootstrapping in FHEW/TFHE.
3. ePrint 2026/2616 — Descent-PBS, if not otherwise supplied.

## Authoritative BOOT state unchanged

LATEST_COMPLETED: B156_AUDIT  
NEXT: B157_PENDING_CODEX_QUOTA  
MAIN_POSITIVE_CANDIDATE: B145+B152  
B145_STATUS: PROMISING / NATIVE_SECURITY+PERF_UNRESOLVED  
NOVELTY: PROMISING_NOT_ESTABLISHED  
CODEX_REQUIRED: YES_FOR_B157  
CODEX_AVAILABLE: NO
