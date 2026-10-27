# PURE-FHE — Post-P0-54 PairSwitch Linear-Rebasing Fusion Gate

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
LATEST_COMPLETED: P0-PRESCOUT-54
NEXT_ITERATION: P0-PRESCOUT-55 NOT_STARTED
STATUS: FAIL_LINEAR_LAZY_REBASE_FUSION / HUMAN_REVIEW / SOURCE_PARTIAL
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO
STATE_UPDATE: YES — isolated PURE-FHE finding only; root STATE.md and other tracks unchanged.

## Scope

This is NOT P0-PRESCOUT-55. It is the bounded follow-up authorized after the PairSwitch/TFB core-problem reselection. The only question tested is whether PairSwitch's public key rebasing can be made "lazy/fused" so that the server keeps only TFB-scale persistent keys, does not materialize PairSwitch's rebased product keys, but still retains PairSwitch's fast BigSwitch without paying TFB-equivalent runtime relinearization.

No native experiment, Codex, GPU/server work, or other-track write was performed.

## Current first-party facts available from the ePrint HTML abstracts

### TFB — ePrint 2026/2058
The current ePrint page (revision 2026-09-21) states:
- original GL BigSwitch is dominated by the product-secret evaluation key s_X s_Y -> s_X;
- TFB factors the trace key (1,s_X,s_Y,s_X s_Y)=(1,s_Y) tensor (1,s_X);
- the product-secret route is replaced by an s_Y -> s_X switch followed by ordinary base-ring (s^2)_X -> s_X relinearization;
- this removes evk_XY->X and saves exactly (n-1)/(2n) of coefficient-domain BigSwitch key memory;
- FRee-L accumulates K Trace products in the four-component domain and invokes BigSwitch only once per output tile, amortizing recurring relinearization/post-processing overhead as O(1/K);
- the abstract reports 768.0 -> 385.5 MiB coefficient-domain key reduction and TFB paired overhead 5.90% for K=4, 0.1933% for K=160, 0.0618% for K=512.

Full PDF remained HTTP-403 blocked in the current tool path, so theorem/algorithm numbering was NOT audited.

### PairSwitch — ePrint 2026/2373
The current ePrint page (received 2026-10-06, approved 2026-10-08) states:
- pair-merge uses n/2+1 rather than n product keys while retaining the original 2n key switches;
- no per-diagonal BigSwitch with 2n key switches holds fewer than 3n/2+1 keys in the authors' model;
- public key rebasing turns Galois keys into product keys using one relinearization key one small modulus layer above the chain;
- client publication is TFB-scale keys plus a 10.6 MiB layer key, while server resident keys are about 1.5x TFB;
- implementation reports 1.89-1.99x faster BigSwitch than TFB and 2.4 bits less noise than TFB, but 4.3 bits more noise than original BigSwitch.

The abstract points to github.com/acprk/pairswitch-gl, but the repository currently returned 404 through the GitHub connector and public web fetch in this session. The full PDF also returned HTTP 403. Therefore detailed PairSwitch KeyGen/rebasing equations remain SOURCE_BLOCKED.

## [DERIVATION] Generic linear-rebasing model

Let a standard key-switch key for source secret z into target secret s contain entries

  K_j = Enc_s(B^j z)

for gadget base B. For an input source coefficient a with gadget decomposition

  a = sum_j d_j(a) B^j,

the switching contribution is the linear accumulation

  KS_K(a) = sum_j d_j(a) K_j.

PairSwitch's abstract says public rebasing transforms a Galois key into a product key using a relinearization key. Model this transformation as a public ciphertext-linear map R from a Galois-key ciphertext to the corresponding product-key ciphertext.

Then a BigSwitch using materialized rebased keys computes

  sum_j d_j(a) R(K_j).

By linearity of R,

  sum_j d_j(a) R(K_j)
  = R( sum_j d_j(a) K_j ).

This identity is exact for any A-linear R and does not depend on gadget base or parameter values.

Therefore there are only two placements of the same rebasing functionality in this model:

1. OFFLINE/PERSISTENT:
   precompute R(K_j) for all required key entries, store them, then runtime switching uses the fast ordinary accumulation.

2. ONLINE/LAZY:
   first accumulate with the compact Galois keys, then apply R once to the accumulated ciphertext.

Entry-by-entry streaming cannot beat (2): linearity says all entrywise rebase work can be postponed until after the digit accumulation. So the cheapest no-materialization implementation inside the linear model is exactly "switch first, then rebase/relinearize once."

## [DERIVATION] Why the online endpoint is TFB-like, not a new free fusion

The TFB abstract explicitly describes the product-secret route as:
  s_Y -> s_X switch
  followed by
  base-ring (s^2)_X -> s_X relinearization.

This is structurally the ONLINE/LAZY endpoint above: use the smaller/factored switching material first, then execute the secret-multiplication/relinearization functionality at runtime.

PairSwitch's public rebasing moves that functionality to the evaluation-key side before runtime and accepts extra server-resident product keys in exchange for avoiding TFB's runtime relinearization and recovering the original 2n-switch fast path.

Hence, under the linear-rebasing model:

  "do not store rebased product keys + push rebasing through the KSK accumulation"

does NOT create a third Pareto point. It collapses to the TFB side of the existing memory/time/noise tradeoff.

The exact operation count of the collapse for PairSwitch's pair-merge schedule is NOT claimed here because the full paper is blocked. In particular, this note does not assert an exact additional n or n/2 relinearization count. The conclusion is structural: every nonresident product functionality must be realized online by R after the corresponding compact-key accumulation unless some new non-linear/shared invariant is introduced.

## [DERIVATION] Streaming/caching alone is systems work, not a Pure-FHE construction

A server could:
- materialize one rebased product key,
- consume it,
- discard it,
- or cache a subset according to workload.

This reduces peak resident key memory at the price of repeated rebasing computation. It is a legitimate systems memory/time tradeoff, but absent a new algebraic primitive it does not change the cryptographic operator graph:
  compact key -> R -> product key -> switch
or equivalently
  compact-key switch -> R.

Therefore plain lazy materialization, LRU caching, prefetching, or streaming is NOT promoted as a PURE-FHE P0-55 contribution.

## [FACT + INTERPRETATION] FRee-L further weakens the naive fusion target for blocked matrix multiplication

TFB already amortizes the recurring relinearization/post-processing by delaying BigSwitch across K Trace products. Its abstract reports only 5.90% paired overhead for K=4 and below 0.2% for K>=160.

Thus, for deep/blocked accumulation workloads, merely recovering PairSwitch-like raw BigSwitch latency while preserving TFB memory may have limited end-to-end headroom unless a new method also improves noise, output depth, or non-amortizable phases.

This does NOT make PairSwitch irrelevant: PairSwitch's abstract reports large raw BigSwitch gains and a Gram-specific path. It means a future PURE-FHE contribution needs a workload regime where the resident-memory/switch-noise frontier materially affects end-to-end cost.

## What would actually escape this gate?

A candidate must violate at least one premise of the linear placement identity. Examples of legitimate research targets, none constructed here:

1. SHARED REBASE:
   one rebasing/relinearization operation simultaneously serves multiple independent diagonal switching accumulations without first collapsing them into a single ciphertext that loses required outputs.

2. DECOMPOSITION-FUSED REBASE:
   a new gadget/key representation in which the rebase map shares the SAME decomposition/noise injection already paid by the product-source switch, rather than being a separate ciphertext-linear map after switching.

3. STRUCTURED PRODUCT-KEY REPRESENTATION:
   product-key functionality remains compressed in a representation smaller than materialized PairSwitch product keys but supports direct external/key-switch products without first reconstructing R(K_j).

4. LOWER-BOUND ESCAPE:
   move outside PairSwitch's per-diagonal 2n-switch model with a new cross-diagonal/batched operator and demonstrate a better matched key/time/noise Pareto.

Simply commuting a linear map, streaming keys, or caching them does not qualify.

## Decision

STATUS: FAIL_LINEAR_LAZY_REBASE_FUSION / HUMAN_REVIEW
LATEST_COMPLETED: P0-PRESCOUT-54
NEXT_ITERATION: P0-PRESCOUT-55 NOT_STARTED
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO

RESULT:
- The naive "fused public rebase + BigSwitch" target is killed in the linear rebasing model.
- If rebasing is not materialized offline, linearity moves it to the runtime switching result; this is structurally the TFB route already described by 2026/2058.
- PairSwitch's extra server-resident keys are therefore not an obvious redundant implementation artifact; they are the stored side of an existing memory/time/noise tradeoff.
- Full PairSwitch source is still needed before claiming this covers the authors' exact rebasing algorithm or lower-bound model.

NEXT_TEST:
Do NOT implement lazy rebasing.
Only start P0-55 if a concrete mechanism is formulated that escapes the linear-rebase placement identity, preferably by a shared cross-diagonal rebase or a decomposition-fused key representation. The first killer test must show why it is not algebraically equivalent to TFB/FRee-L and why it lies outside PairSwitch's stated per-diagonal lower-bound model.

SOURCE_SUPPORT:
Highest-priority missing source remains the full 2026/2373 PairSwitch PDF. Full 2026/2058 TFB PDF is second priority. No Codex is required.
