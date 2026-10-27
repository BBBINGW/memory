# PURE-FHE P0-PRESCOUT-62 — Focused CKKS Novelty Gate

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
ITERATION: P0-PRESCOUT-62
LATEST_COMPLETED: P0-PRESCOUT-62
NEXT_ITERATION: NOT_STARTED / SOURCE_BLOCKED
STATUS: PASS_PUBLIC_ABSTRACT_DIFFERENTIATION / PASS_PUBLIC_CODE_NEGATIVE_EVIDENCE / SOURCE_BLOCKED_FULLTEXT / NOVELTY_UNRESOLVED / HOLD_TYPED_PRECISION_LINE
CODEX_REQUIRED: NO
STATE_UPDATE: YES — isolated PURE-FHE finding only.

## 1. Question

P0-60/P0-61 produced a candidate called covariant / typed precision allocation:

- each ciphertext node carries a public cyclotomic-unit type p_v;
- exact message-preserving rebase multiplies ciphertext components by p_a p_v^{-1};
- automorphism may choose p_out=tau(p_in), making the public correction tau(p_in)p_out^{-1}=1;
- a two-stage source-shaped gate showed about 120 bits of continuous initial-modulus headroom over the best fixed unit under the same 160-bit output precision and full recovery constraint.

The largest unresolved concurrent-prior-art risk is:

Jung Hee Cheon, Junho Lee,
"High-Precision CKKS with Focal Units,"
ePrint 2026/2531, last updated 2026-10-20.

P0-62 asks whether 2531 already contains the typed/covariant construction.

## 2. Full-text acquisition status

Attempted sources:
- official ePrint PDF;
- eprint.iacr.asia mirror;
- ePrint classic mirror;
- author/title web searches;
- GitHub global search;
- public Poulpy repository search.

The official PDF endpoint returns HTTP 403 through the available ePrint acquisition path.
The eprint.iacr.asia searchable mirror exposes metadata and abstract but not a fetchable full PDF through the current tooling.
No independent author-hosted PDF, arXiv copy, Semantic-Scholar/OpenAlex-hosted full text, or public source-code implementation of Focused CKKS was found.

Therefore:

  SOURCE_BLOCKED_FULLTEXT.

This iteration MUST NOT claim that a construction is absent from 2531.

## 3. What the public abstract DOES establish

The current public abstract says Focused CKKS:

- uses cyclotomic units;
- reduces error in selected "focus slots";
- allows larger error in "background slots";
- trades unused SIMD slots for precision;
- supports focused rescaling and key-switching;
- supports different precision requirements across slots;
- gives high-precision multiplication at ordinary-multiplication cost;
- gives a Focused-CKKS bootstrapping procedure;
- during bootstrapping, uses fewer slots as precision grows.

Thus 2531 strongly overlaps with P0-60/P0-61 in:

1. cyclotomic-unit error shaping;
2. focus/high-precision slots versus low-precision/background slots;
3. rescale and key-switch shaping;
4. heterogeneous per-slot precision;
5. precision-vs-slot-count tradeoffs.

These parts cannot be novelty claims for the typed candidate.

## 4. What accessible sources do NOT currently show

Across exact-title web searches and public indexing snippets, no evidence was found for the following four specific mechanisms:

1. **Per-ciphertext changing unit type**
   A ciphertext carries a type p_v that is allowed to change at arbitrary ordinary leveled-circuit nodes.

2. **Message-preserving unit rebase**
   An explicit map
     ct_a -> (p_a p_v^{-1}) ct_a
   preserving the restored polynomial M, logical value, logical error, and scale exactly.

3. **Galois-covariant type transport**
   For an automorphism tau,
     p_out=tau(p_in),
   so the unit correction is exactly one.

4. **Circuit-wide temporal unit scheduling**
   The focus/precision profile changes according to time-varying liveness/data movement during ordinary leveled evaluation, rather than being a fixed spatial focus profile or a bootstrapping-specific split.

The public abstract language is spatial/static:
- selected focus slots;
- background slots;
- different precision requirements across slots.

It does not state changing focus sets over time.

This is only NEGATIVE EVIDENCE, not proof of absence.

## 5. Public implementation search

Global GitHub searches were run for:
- "Focused CKKS";
- "High-Precision CKKS with Focal Units";
- "FocusedRescale CKKS";
- "FocusedKeySwitch CKKS";
- "focal unit";
- focus/focused/focal searches inside poulpy-fhe/poulpy.

No implementation exposing Focused-CKKS focus-set conversion or dynamic unit-type transport was found.

The public Poulpy repository contains ordinary CKKS infrastructure and unrelated uses of the word "focused", but no identifiable implementation of the 2531 construction.

Again, absence of public code is not evidence that the paper lacks the mechanism.

## 6. Concurrent-work boundary that is already clear

Even without 2531 full text, some novelty claims are already excluded.

### Not novel: changing a decryption factor

ePrint 2026/2600, GCKKS high-precision bootstrapping, explicitly provides a generic ciphertext-conversion framework for changing decryption factors and slot counts.

Therefore "change the factor during computation" is not a contribution.

### Not novel: public coordinate shaping with cyclotomic units

ePrint 2026/2513 shaped rounding and ePrint 2026/2562 precision allocation both establish public ring/unit shaping viewpoints.

Therefore "use a public cyclotomic unit to redistribute slot error" is not a contribution.

### Potentially distinct candidate

The only remaining candidate contribution is the conjunction:

  exact message-preserving unit rebasing
  + per-ciphertext unit types
  + Galois-covariant type transport
  + circuit-wide optimization for time-varying active precision profiles.

This conjunction has not been found in accessible public evidence.

NOVELTY is still NOT ESTABLISHED because 2531 full text is unavailable.

## 7. Why P0-63 must NOT start yet

P0-61 already showed a strong source-shaped analytical effect:
about 120 bits less initial modulus than the best fixed unit on the minimal changing-active-set circuit.

But spending effort on:
- concrete NTT-prime chains;
- lattice-estimator runs;
- implementation;
- compiler scheduling;
- native benchmarks

before resolving 2531 would be backward.

The novelty gate is cheaper and potentially decisive.

Therefore:

  DO NOT start P0-63 secure-RNS closure yet.

## 8. Required missing source

The only blocking source is the full current PDF of:

  ePrint 2026/2531
  High-Precision CKKS with Focal Units
  Jung Hee Cheon, Junho Lee
  revision/current version around 2026-10-20.

Once supplied or publicly retrievable, inspect specifically:

- definitions of focal/focused ciphertext;
- whether the focal unit is fixed per parameter set, per ciphertext, or per operation;
- focused Rescale;
- focused KeySwitch / relinearization;
- rotations / Galois automorphisms;
- whether rotations require preserving a focus subgroup/pattern;
- whether focus sets can change;
- any conversion between two focal units;
- bootstrapping splitting/merging steps;
- sections on arbitrary precision vectors;
- algorithms or lemmas involving two different units on input and output;
- implementation APIs / metadata.

A direct occurrence of any equivalent to
  p_out=tau(p_in)
or
  ct -> (p_in p_out^{-1})ct
for arbitrary leveled evaluation would materially overlap P0-60.

## 9. Current evidence-weighted judgment

The accessible abstract is more naturally read as a STATIC SPATIAL precision-allocation scheme:
one selects focus slots and lets background slots absorb larger error.

P0-60/P0-61 are TEMPORAL:
the protected slot class follows the data through automorphisms and circuit stages.

So the current evidence mildly favors distinctness.

But this is not strong enough for a publication-level novelty claim.

## End of Iteration

TRACK_ID: PURE-FHE
ITERATION: P0-PRESCOUT-62

STATUS:
PASS_PUBLIC_ABSTRACT_DIFFERENTIATION /
PASS_PUBLIC_CODE_NEGATIVE_EVIDENCE /
SOURCE_BLOCKED_FULLTEXT /
NOVELTY_UNRESOLVED /
HOLD_TYPED_PRECISION_LINE /
HUMAN_REVIEW.

RESULT:
- 2531 definitely overlaps on cyclotomic-unit shaping, focused rescale/key-switch, heterogeneous per-slot precision, and slot-vs-precision tradeoffs.
- No accessible evidence shows per-ciphertext changing unit types, exact message-preserving rebasing, covariant automorphism typing, or arbitrary circuit-wide temporal focus scheduling.
- Full text is unavailable through current sources, so absence cannot be claimed.
- P0-61's ~120-bit analytical modulus separation remains alive but is not promoted.

CODEX_REQUIRED:
NO.

NEXT:
Do not start P0-63.
Acquire the full 2026/2531 PDF from an authorized source.
Once available, perform the targeted full-text audit above.
If it covers typed/covariant scheduling, KILL/PARK this line.
If it does not, immediately proceed to secure integer-RNS parameter closure.

STATE_UPDATE:
YES — this finding only.
