# BOOT — RDK-CKKS bootstrap-key overhead prescout
Date: 2026-10-28
TRACK_ID: BOOT
MODE: SOURCE/PAPER LEVEL ONLY
CODEX_USED: NO

## Source
ePrint 2026/2575, Noh–Chabounia–Hanrot–Passelègue, "RDK-CKKS: A Framework for Rigorous Error Analysis for CKKS Computation."

Verified from the current abstract:
- randomization keys (RDKs) are zero-encrypting evaluation material injected at key-switching and rescaling;
- they make homomorphic errors amenable to rigorous probabilistic analysis;
- rigorous bootstrapping reports 27% communication overhead over the ordinary bootstrap keys for one evaluation and another 8% for each additional evaluation;
- most RDK material can be reused when a circuit is evaluated repeatedly;
- the rigorous binary-CKKS bootstrap parameters require only about 3% more modulus than a Gaussian-heuristic baseline.

Full 2026/2575 text could not be acquired in this session (ePrint PDF 403, fallback unavailable, fixed mirror absent). Exact reusable/non-reusable RDK classes and the proof reason for the residual 8% are therefore unknown.

## Smallest question
Why is the remaining +8% evaluation-specific?
Possible proof roles to distinguish once full source is available:
1. marginal tail bounds;
2. conditional independence inside one bootstrap;
3. independence across repeated evaluations;
4. circuit-privacy / threshold security;
5. proof convenience only.

Do not assume which one is true from the abstract.

## Conditional linear-basis no-go
Suppose a proof requires E evaluation-specific injected error objects to have a jointly non-degenerate E-dimensional randomness structure.
If all E objects are generated only by public linear combinations of r fixed independent RDK randomness objects, then conditioned on the fixed pool they lie in a span of dimension at most r.
Thus r<E cannot reproduce a proof distribution requiring full-rank E fresh randomness.

This is only conditional. If the paper needs only marginal tail bounds, stronger reuse may remain possible. The authors already state that most RDKs are reusable.

## Gates
RDK_GATE_1: recover full definitions and classify reusable vs evaluation-specific RDKs.
RDK_GATE_2: identify the exact proof dependency that forces freshness.
RDK_GATE_3: only if cross-evaluation freshness is not essential, test bootstrap-specific public rerandomization/fixed-basis reuse; do not use generic seeded compression.
RDK_GATE_4: require a material reduction of the reported +8%/evaluation without hidden online work, larger modulus, or extra key-holder interaction.

## Status
RDK_KEY_MEMORY_BOTTLENECK = HIGH_VALUE_SOURCE
RDK_FIXED_BASIS_REUSE = UNRESOLVED
RDK_LINEAR_BASIS_WITH_FULL_INDEPENDENCE = CONDITIONAL_NO_GO
NOVELTY = NOT_ESTABLISHED
CODEX_REQUIRED = NO for source/proof gates

## Authoritative state unchanged
LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE: B163_PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
B158_NATIVE_FEASIBILITY: UNRESOLVED
B163: NOT_RUN
