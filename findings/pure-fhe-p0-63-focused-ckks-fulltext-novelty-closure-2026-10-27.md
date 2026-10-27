# PURE-FHE P0-PRESCOUT-63 — Focused CKKS Full-Text Novelty Closure

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
ITERATION: P0-PRESCOUT-63
LATEST_COMPLETED: P0-PRESCOUT-63
NEXT_ITERATION: NOT_STARTED / HUMAN_REVIEW
STATUS: FAIL_STRONG_CONSTRUCTION_NOVELTY / PASS_SCHEDULING-ANALYSIS_DISTINCTNESS / PARK_TYPED_PRECISION_LINE / NO_IMPLEMENTATION
NOVELTY: NOT SUFFICIENT FOR A NEW PURE-FHE CONSTRUCTION
CODEX_REQUIRED: NO
STATE_UPDATE: YES — isolated PURE-FHE finding only.

## 1. Source resolved

The previous blocker was the full text of:

Jung Hee Cheon, Junho Lee,
"High-Precision CKKS with Focal Units,"
ePrint 2026/2531, revision 2026-10-20.

The PDF is now available in:

  papers/supplied/2026-2531.pdf

GitHub blob SHA:

  ca85d988bc85d7a242bf3f07b55df4687556b567

The full 42-page paper was audited page-aware from the supplied PDF.

## 2. Prior P0-60/P0-61 candidate

The candidate was:

- attach a public cyclotomic-unit type p_v to each ciphertext/node;
- exact message-preserving rebase using p_a p_v^{-1};
- under automorphism tau choose p_out=tau(p_in);
- optimize the unit schedule according to time-varying active/focus slots;
- exploit the fact that past logical error is preserved while fresh primitive error is shaped by the current output type.

P0-61 derived a source-shaped example:
  square -> swap rotation -> square
with approximately 120 bits less continuous initial modulus than the best fixed unit at the same 160-bit output precision, after full recovery accounting.

## 3. Full-text overlap: exact unit conversions are already explicit

Section 1.2 gives two equivalent views:

  b+a sk = Delta m + u e,

and

  u^{-1}b + u^{-1}a sk = u^{-1}Delta m + e.

The paper states that because u is a unit, multiplying the ciphertext by u or u^{-1} converts between these forms exactly and introduces no error.

Focused rescaling and key switching are defined by:

  RS_q^[u](ct) = u * RS_q(u^{-1} ct),

  KS^[u](ct) = u * KS(u^{-1} ct).

Thus "use a public unit to change coordinates exactly while shaping only newly introduced operation error" is already central prior art.

## 4. Full-text overlap: covariant automorphism is already Proposition 12

This is the decisive overlap.

Proposition 12 states:

If ct encrypts Delta m with error u e, then applying automorphism kappa followed by focused key switching produces a ciphertext encrypting Delta kappa(m) with error

  kappa(u) * (kappa(e)+e_KS).

Therefore the focal/error-shaping unit transforms covariantly:

  u_out = kappa(u_in).

This is precisely the algebraic behavior highlighted in P0-60 as

  p_out = tau(p_in).

The paper then says that **in practice** it restricts to automorphisms satisfying kappa(u)=u so the focused-error form stays under one fixed unit and rotations remain inside the focus pattern.

But the general covariant case itself is already formally stated and proved.

Hence:

  "covariant unit transport under automorphisms"

is NOT novel.

## 5. Full-text overlap: the P0-61 decisive toy is already expressible

The P0-61 toy was:

  square -> swap rotation -> square.

Focused CKKS already supports exactly this sequence:

1. First square:
   use Proposition 11 Mult^[u].

2. Swap automorphism:
   use Proposition 12, which changes the focal unit from u to kappa(u).

3. Second square:
   use Proposition 11 again with focal unit kappa(u).

Therefore the key temporal behavior used by the P0-61 modulus separation does not require a new cryptographic primitive.

The 120-bit calculation can remain useful as an ANALYSIS of a use case not emphasized by the source, but it no longer establishes a new construction.

## 6. Full-text overlap: changing focal units over time is already explicit

Section 6.1 says:

  "each iteration with its own focal unit and scale."

The iterated cleaning uses:

  Clean* = Clean^[u_{T-1}] o ... o Clean^[u_0].

So operation-by-operation focal-unit changes are explicit.

Further, tree-like cleaning changes the focus set itself over time:
- each layer halves the focus slots;
- each layer chooses a new focal unit u_{ell+1};
- rotations move one half of the currently relevant slots onto the next focus set;
- the next cleaning is performed with the new unit.

Thus even:

  "change unit dynamically"
and
  "change focus set dynamically"

are already source prior art.

## 7. General arbitrary precision profiles are also source prior art

Section 3.2, Theorem 1, constructs a close cyclotomic unit for an arbitrary target logarithmic precision profile delta subject to the unit-norm balance constraint.

So the source already has:
- arbitrary spatial precision profiles;
- public cyclotomic-unit synthesis;
- operation-level unit changes;
- focus-set changes;
- covariant automorphism behavior.

These substantially cover the mathematical ingredients behind the typed-precision idea.

## 8. What remains distinct

The following is not explicitly packaged in 2531 as a general framework:

1. Treating the unit as first-class ciphertext type metadata for arbitrary leveled circuits.
2. A compiler/global optimizer choosing a unit independently at every general circuit node based on liveness and future data movement.
3. An explicit arbitrary-unit message-preserving rebase API written as p_a p_v^{-1} between two arbitrary type labels.
4. Joint optimization of unit schedule, scale, modulus, and branch joins outside the paper's focused bootstrapping/cleaning settings.
5. The P0-61 quantitative observation that a moving active set can make a dynamic schedule beat the best fixed unit by ~120 modulus bits in the specific source-shaped two-stage example.

However, after the full-text audit these are best viewed as:
- a generalization / scheduling abstraction over existing Focused-CKKS mechanisms;
- a compiler/parameter-optimization problem;
- not a sufficiently distinct PURE-FHE cryptographic construction by itself.

## 9. Why not proceed to secure-RNS/native implementation

Before full-text audit, the plan was:
- if 2531 does not cover dynamic/covariant units, instantiate an RNS chain and run a >=128-bit estimator.

That condition is not satisfied.

2531 already covers the core cryptographic mechanisms needed for the P0-61 toy.

Running:
- lattice estimator;
- concrete prime search;
- native implementation;
- compiler prototype

would now validate an optimization layer on top of strong concurrent prior art, not establish the missing cryptographic novelty.

Under the project's research philosophy this is insufficient to justify implementation.

## 10. Relation to 2026/2513

The supplied directory currently contains 2026-2531.pdf but no 2026-2513.pdf at the time of this audit.

2531 itself cites 2026/2513 (Jules Dumezy, "Fully Homomorphic Encryption for Small Batches of Complex Numbers") as concurrent work, and states that 2513 uses polynomial scaling and shaped rounding/rescaling/key-switching, with subring units suppressing errors on data slots and background slots absorbing larger error.

Thus 2513 is additional strong neighboring prior art, but P0-63 does not depend on its full text: 2531 alone is sufficient to defeat strong novelty of the current typed-precision construction.

## 11. Final decision

STATUS:

  FAIL_STRONG_CONSTRUCTION_NOVELTY /
  PASS_SCHEDULING-ANALYSIS_DISTINCTNESS /
  PARK_TYPED_PRECISION_LINE /
  HUMAN_REVIEW.

Interpretation:

- The algebra and P0-61 modulus separation are not mathematically invalid.
- The ~120-bit separation remains an interesting quantitative result.
- But the required cryptographic ingredients are already present in Focused CKKS:
  - focused units;
  - arbitrary precision profiles;
  - exact public unit coordinate conversion;
  - focused rescale/key switching/multiplication;
  - automorphism sending u -> kappa(u);
  - changing focal units and focus sets over time.
- The residual novelty is primarily scheduling/optimization abstraction, not a new PURE-FHE construction.

## End of Iteration

TRACK_ID: PURE-FHE
ITERATION: P0-PRESCOUT-63

RESULT:
Full-text 2531 resolves the P0-62 blocker and materially overlaps P0-60/P0-61. The decisive square->swap->square example is already supported by Propositions 11 and 12. Dynamic focal units and dynamic focus sets are explicitly used in Section 6.

NEXT:
Do not continue this line into secure parameter closure or native implementation.
Return to problem-level PURE-FHE reselection.
Keep the 120-bit result archived as a potentially useful optimization/compiler observation, but do not promote it as a cryptographic paper idea unless a separate, clearly novel optimization theorem/system contribution emerges.

CODEX_REQUIRED:
NO.

STATE_UPDATE:
YES — this finding only.
