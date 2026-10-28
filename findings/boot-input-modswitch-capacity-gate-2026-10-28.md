# BOOT — Input modulus-switch / rotation-capacity gate

Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER_LEVEL_ONLY
CODEX: NOT_USED
NATIVE: NOT_RUN

## Authoritative BOOT state

LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE_GATE: B163_CORRECTED_B160_NOSCALE_SELECTOR_GATE
B163_STATUS: PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
DO_NOT_AUTO_RUN_CODEX: YES

B158_ALGEBRA: PASS
B158_CTCT_MULT_COUNT: OPTIMAL
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B158_NATIVE_FEASIBILITY: UNRESOLVED
B163: NOT_RUN

## Question

Can the standard input-side modulus switch

    LWE mod q
      -> phase/index mod 2N
      -> blind rotation in R_Q = Z_Q[X]/(X^N+1)

be removed entirely, with no equivalent quantization/reduction elsewhere, while:
- keeping a single N-degree negacyclic accumulator;
- keeping one monomial blind-rotation state X^r;
- and supporting an arbitrary high-resolution phase domain q > 2N?

## Ring-rotation capacity theorem

In R_Q = Z_Q[X]/(X^N+1),

    X^N = -1,
    X^(2N) = 1.

Therefore the monomial orbit
    {X^r : r in Z}
contains at most 2N distinct signed rotation states, indexed by r mod 2N.

Suppose a one-accumulator blind-rotation procedure represents an input phase z in some domain D solely through a monomial rotation state

    X^{rho(z)}

for a public/deterministic index map
    rho : D -> Z_{2N}.

Then every function evaluated solely by reading the resulting rotated accumulator necessarily factors through rho:

    F(z) = G(rho(z))

for some accumulator-defined readout G.

Therefore:

### Factor-through theorem

If |D| > 2N, rho cannot be injective.

Hence there exist z != z' such that
    rho(z)=rho(z').

Any target function F with
    F(z) != F(z')
cannot be evaluated exactly by this one-ring one-rotation representation.

Equivalently, a single N-degree negacyclic monomial accumulator can distinguish at most 2N phase classes before additional structure/refinement is introduced.

This is a pure state-capacity statement, independent of the particular CMUX/external-product implementation.

## Consequence for removing input ModSwitch

Standard FHEW/TFHE modulus switching maps the large LWE phase space into the 2N rotation-index space, accepting a controlled rounding error.

If q > 2N, any proposal that claims to:
- retain one N-degree ring accumulator;
- retain ordinary monomial blind rotation;
- support arbitrary phase-dependent LUT behavior;
- and remove all phase compression/quantization,

must contradict the 2N-state capacity bound.

Therefore:

    EXACT_GENERIC_NO_MODSWITCH_WITH_SAME_RING_STATE_SPACE = FAIL.

A scheme can avoid an *explicit* ModSwitch call only by changing one of the premises:
1. enlarge the state space;
2. use a module/multiple accumulators;
3. iterate/refine the rotation;
4. restrict the target function/message-error domain so collapsed phases are equivalent;
5. encode a different object than the full message phase.

## Prior-art consistency

### Standard FHEW/TFHE

Standard bootstrapping explicitly modulus-switches the LWE ciphertext to the rotation domain before blind rotation. This is the canonical realization of the factor-through map.

### Kang et al. / ePrint 2022/198

"Efficient FHEW Bootstrapping with Small Evaluation Keys" modifies the rounding ("round-to-odd") and observes that its modulus-reduction error is equivalent to switching to a smaller rotation modulus. It optimizes the quantization but does not remove the finite rotation-state map.

Source:
https://eprint.iacr.org/2022/198.pdf

### Descent-PBS / ePrint 2026/2616

Its public abstract explicitly states the same structural barrier from the LUT side:
a t-entry negacyclic table must fit, with redundancy, into the 2N signed rotation positions of a ring accumulator.

Module bootstrapping enlarges state capacity via module rank; Meta-PBS iterates ring rotations; Descent-PBS pays module rank only in the first rotation and then descends.

This is directly consistent with the capacity theorem.

Public source:
https://eprint.iacr.asia/2026

### Exact Error Bootstrapping / ePrint 2026/2630

This work does not contradict the theorem because it changes the object being represented:
- it rounds at a resolution aligned with the message modulus so the message is preserved;
- it then bootstraps the much smaller error domain.

Thus it avoids needing one ring rotation state for every full high-modulus message phase.

Public source:
https://eprint.iacr.asia/2026

## Important scope

The theorem does NOT say:
- ordinary ModSwitch is the only possible implementation;
- no high-precision bootstrap can exceed 2N message values;
- no full-domain or large-domain functional bootstrap exists.

It says only:

A single ordinary N-degree negacyclic monomial accumulator has at most 2N distinguishable rotation states. Exact arbitrary phase behavior beyond that must add state capacity, iteration, structure, or restrictions.

## Research implication

The generic idea

    "remove input ModSwitch but keep the same ring/blind-rotation geometry"

is not a viable BOOT research direction.

The only potentially meaningful directions are those that change what is represented, e.g.:
- error-only bootstrapping;
- quotient/remainder decomposition with separate low-cardinality states;
- module/rank extension with cheaper descent;
- a non-monomial accumulator state space.

But each of the first three is already active/recent prior art (2630, high-precision/full-domain methods, 2616).

Thus this branch is primarily a useful negative closure rather than a positive candidate.

## Decision

GENERIC_INPUT_MODSWITCH_REMOVAL:
    PARK.

SAME_RING_EXACT_HIGH_PHASE_RESOLUTION:
    FAIL by 2N rotation-state capacity.

ROUNDING_OPTIMIZATION:
    PRIOR ART / CROWDED.

LARGE-DOMAIN_ESCAPE:
    ACTIVE PRIOR ART (module / Meta-PBS / Descent-PBS).

ERROR-DOMAIN_ESCAPE:
    ACTIVE PRIOR ART (2026/2630).

NOVELTY:
    NO positive contribution established.

CODEX/NATIVE:
    NOT REQUIRED.

## Next scout

Continue outside the standard FHEW/TFHE front-tail pipeline.

The next useful BOOT search should target:
- a representation where bootstrapping refreshes only a sufficient statistic, but not merely the 2630 error;
- or a CKKS/BGV stage whose expensive linear transform has low algebraic rank/structure and can be partially skipped for restricted workloads.

B163 remains the highest native gate once Codex quota returns.
