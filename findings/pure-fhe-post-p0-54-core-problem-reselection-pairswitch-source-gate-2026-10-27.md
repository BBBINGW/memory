# PURE-FHE — Post-P0-54 Core-Problem Reselection: PairSwitch / Current-Source Gate

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
LATEST_COMPLETED: P0-PRESCOUT-54
NEXT_ITERATION: P0-PRESCOUT-55 NOT_STARTED
STATUS: HUMAN_REVIEW / PROBLEM_RESELECTION / SOURCE_GATED
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO
STATE_UPDATE: YES — isolated PURE-FHE HUMAN_REVIEW finding only. Root STATE.md and all BOOT/SHIP/CGS/VFHE/EAI files unchanged.

## Scope

This is NOT P0-PRESCOUT-55. It is the bounded problem-level reselection authorized after P0-54 closed the one-shot Fourier/scalar hidden-MPmul route. The goal was to identify a different Pure-FHE core bottleneck with plausible main-complexity, evaluation-key, or noise/DFR impact, while reusing old-track negative lessons read-only and avoiding paper roulette.

No native experiment, Codex, GPU/server work, or other-track write occurred.

## 1. MPmul branch remains closed after P0-54

P0-54 established a model-specific operator-rank obstruction for one-shot scalar-controller hidden cyclic shifts and an exact native q=2^64 Fourier obstruction. No new non-one-hot/non-tensor hidden-action representation emerged. Therefore this reselection did not reopen MPmul.

## 2. Sorted-Bootstrapping/CMS candidate was rejected by cross-track deduplication

A fresh source audit of Bergerat–Orfila–Roux-Langlois–Tap, ePrint 2025/2214 / ASIACRYPT 2025, found a superficially promising problem:
- SBS external-product count depends on the 2-adic/congruence class of modulus-switched public LWE mask coefficients.
- CMS flips the rounding of a selected subset d of first-layer mask coefficients to move them into better classes.
- the published proof permits arbitrary d positions; the source artifact branch
  zama-ai/tfhe-rs@e1f5d36224ca88991b49e38fa6791ab18a9f63d1
  implements the actual selection by first classifying the adjacent altered modulus-switch value and then consuming shortcut candidates from highest congruence class to lowest:
  shortcut_destinations.iter().enumerate().rev().
So merely choosing the highest-valuation d positions is author implementation prior art.

More importantly, READ-ONLY cross-track reuse showed this entire residual-aware selection branch was already investigated in BOOT:
- boot-B032-sorted-cms-public-body-bias-centering-gate.md
- boot-B033-cms-input-adaptive-knapsack-noise-tail-gate.md
- boot-B034-body-aware-cms-robust-and-honest-tail-certificate.md

Those records already derive exact per-coordinate residual costs, formulate input-adaptive CMS selection/knapsack, exhibit local CMUX Pareto improvements, falsify naive full-LWE tail monotonicity with exact valid-LWE enumeration, and derive worst-case / honest-key certificates. B034 explicitly decides to STOP the CMS selection microbranch absent a genuinely new source-benchmark-beating end-to-end mechanism.

Therefore PURE-FHE MUST NOT relabel residual-aware CMS, body-aware CMS, or adaptive rounding knapsack as P0-55. BOOT remains untouched.

## 3. Current CKKS/BGV candidates are source-gated

The latest direct competitors that could materially change prior P0 portfolio conclusions were queried through the ePrint acquisition path:

- 2026/2513, "Fully Homomorphic Encryption for Small Batches of Complex Numbers" — full PDF RETRIEVAL_BLOCKED (HTTP 403, no verified mirror).
- 2026/2531, "High-Precision CKKS with Focal Units" — full PDF RETRIEVAL_BLOCKED.
- 2026/2618, "Efficient (Functional) Bootstrapping for CKKS over the Conjugate-Invariant Ring" — full PDF RETRIEVAL_BLOCKED.
- 2026/2076, "Symmetry-Graded Digit Extraction Framework for Faster BGV Bootstrapping" — full PDF RETRIEVAL_BLOCKED.
- 2024/115 large-p BGV null-polynomial source also failed verified PDF identity in the current acquisition path.

These are too close to CKKS precision/bootstrapping and BGV digit-extraction bottlenecks to invent a detailed P0-55 mechanism from abstracts. Those sublines remain SOURCE_GATED rather than falsely "open".

## 4. Highest-value newly selected core problem: matrix-native GL BigSwitch key/noise Pareto

The strongest current problem is the evaluation-key bottleneck in Gentry–Lee matrix-native FHE.

### [FACT: current prior-art abstracts]

2026/2058, Park et al., "Trace-Factored BigSwitch for Matrix-Friendly FHE" (TFB):
- GL Trace multiplication creates a four-component ciphertext.
- original BigSwitch requires large extended-ring evaluation keys, including the product-secret switch s_X s_Y -> s_X.
- TFB removes that product-secret key by factoring the rank-one trace secret and routing through an s_Y -> s_X switch plus base-ring s_X^2 -> s_X relinearization.
- author abstract reports about 50% coefficient-domain BigSwitch-key reduction, with FRee-L amortizing recurring post-processing across blocked accumulation.

2026/2373, Xiong–Wang–Wang, "PairSwitch: Efficient Galois-Paired Key Switching for Gentry–Lee Matrix FHE", last updated 2026-10-06:
- identifies original BigSwitch vs TFB as a key/time/noise Pareto.
- pair-merge BigSwitch borrows a product key from the inverse Galois diagonal and uses n/2+1 product keys while retaining the original 2n key-switch count.
- abstract states a lower bound: no per-diagonal BigSwitch with 2n key switches holds fewer than 3n/2+1 total keys under their model.
- public key rebasing lets the CLIENT publish only TFB-scale keys plus a small layer relinearization key, but SERVER resident keys become about 1.5x TFB.
- author measurements at n=256 report BigSwitch 1.89–1.99x faster than TFB and 1.28–1.38x faster than original, with 2.4 bits less noise than TFB but 4.3 bits more noise than original.
- Gram inputs admit an additional Hermitian hop reduction.

This is exactly the kind of main evaluation-key / switching-noise frontier that PURE-FHE seeks.

### [DERIVATION: precise unresolved interface, not yet a construction]

A potentially valuable post-PairSwitch question is:

Can the rebased product-key functionality be consumed without permanently materializing PairSwitch's extra server-resident product keys, while preserving approximately the 2n-switch fast path and not reintroducing TFB's extra online relinearization / whole switching-error-by-secret penalty?

This is structurally meaningful because:
- keeping all rebased keys gives PairSwitch speed but ~1.5x TFB server-resident keys;
- deriving/factoring them online naively risks collapsing back toward TFB's extra switch/noise path;
- simple lazy caching/streaming would be a systems memory-time tradeoff, NOT by itself a new cryptographic construction;
- a publication-grade candidate would need a NEW fused rebase-and-switch invariant/operator that applies the rebasing map during a BigSwitch without materializing the transformed key and without adding an equivalent full key switch.

However, this is NOT yet H55. PairSwitch's full proof/model is required before attempting to escape its per-diagonal lower bound or claiming that a fused transform is not already present.

## 5. Source gate

Full verified PDFs for the critical latest sources could not be acquired through the current GitHub Notes ePrint path:
- ePrint 2026/2058 TFB: RETRIEVAL_BLOCKED (HTTP 403; no fixed mirror copy).
- ePrint 2026/2373 PairSwitch: RETRIEVAL_BLOCKED.
- ePrint 2026/956 GL bootstrapping: RETRIEVAL_BLOCKED.

Public current abstracts and publication indices were sufficient only for problem selection, NOT theorem/algorithm-level novelty.

Therefore the next legitimate technical step is source acquisition, not an invented P0-55.

## Decision

STATUS: HUMAN_REVIEW / PASS_PROBLEM_RESELECTION / SOURCE_GATED
LATEST_COMPLETED: P0-PRESCOUT-54
NEXT_ITERATION: P0-PRESCOUT-55 NOT_STARTED
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO

RANKED NEXT SOURCE PRIORITY:
1. ePrint 2026/2373 PairSwitch — highest priority; need full Algorithm/KeyGen, pair-merge lower-bound model, public rebasing equations, exact resident/client key ledger, noise theorem.
2. ePrint 2026/2058 TFB — need exact factorization, FRee-L accumulation semantics, noise and key ledger.
3. ePrint 2026/956 Efficient Bootstrapping for GL — needed for whole-system/Amdahl relevance of BigSwitch.
4. ePrint 2026/2618 current CKKS bootstrap or 2026/2076 current BGV digit extraction only if the GL source gate fails or PI chooses another core problem.

PROVISIONAL H55 GATE — NOT STARTED:
Under PairSwitch's exact GL ciphertext/key types, can a fused public-rebase-and-key-switch operator consume TFB-scale published material with O(1) transient rebased-key state, retain the 2n general-input switch count, and avoid TFB-equivalent additional switching noise?

CHEAPEST FALSIFIER once source is supplied:
Trace one PairSwitch rebased product-key equation through one diagonal key switch. If eliminating the stored rebased key algebraically requires applying the layer relinearization/key-switch map separately to every runtime input decomposition (or an equivalent full extra switch/noise term), KILL the fusion immediately. Also KILL if PairSwitch already contains lazy/fused rebasing or its lower-bound theorem covers this operator class.

PI_SUPPORT_NEEDED:
If available, place 2026/2373 and 2026/2058 PDFs under papers/supplied/. No Codex is needed.
