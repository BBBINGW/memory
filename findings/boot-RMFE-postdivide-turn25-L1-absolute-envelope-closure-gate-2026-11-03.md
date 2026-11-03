# BOOT / B158 — Research Turn 25/25 — absolute L1 envelope closure for first post-F4 divide

**Date:** 2026-11-03 Asia/Singapore  
**TRACK_ID:** BOOT  
**ACTIVE_SUBLINE:** B158_CHECKPOINT_DECOUPLED_HALF_BASIS  
**Phase:** CORRECTNESS_GATE  
**Candidate:** legacy-484479fe4613  
**Native execution:** NONE.

## Authority / read-before-write

The turn starts from the PI-supplied verified fallback authority:

    BBBINGW/memory HEAD=origin/main=9f2a23973288e9ee8bdacb89dfc47c0ac9f0db26.

The local clone is not mounted here, so that supplied local authority is not silently replaced by connector state. GitHub Notes file reads are degraded. Repository copies of the already-completed Turn14-16 derivations were used only to recover the exact existing formulas and were independently recombined below; they do not override the PI-supplied authority state.

Target path was checked absent before write:

    findings/boot-RMFE-postdivide-turn25-L1-absolute-envelope-closure-gate-2026-11-03.md

Immediate scientific input from the current durable candidate / Turn24:
- fixed ordered ctxt-prime prefix P, q=product(P), with 183 <= log2(q) < 247;
- p=5, ptxtSpace625, Algorithm4-entry factor a=67;
- completed first F4 with factor d=a^5 q^4 mod625;
- Turn23 independent envelope
      EF4(q) < EFhat
      EFhat = 4155105766733618287140112599228004062478100413979797319;
- explicit first-boundary aligner
      h0 = a^4 q^4 mod625,
  with exact unit-residue audit |balRem(h0,625)| <= 311;
- Turn24 sufficient absolute-L1 threshold
      B1_star ~= 8.28321073366513e116
              ~= 2^388.39384909974.

No Turn14-16 scientific claim is regenerated here; this turn only reconnects their already-established absolute ledger to the Turn24 threshold, with upward-rounded arithmetic.

## Closest prior / exact delta

Closest prior remains Aung et al. Algorithm 4 plus pinned HElib BGV recryption/evaluation semantics. No novelty claim is added.

Exact delta of this turn:
- recover the candidate-specific absolute full-Q0 envelope for L1(z), not a relative stock/candidate operator factor;
- bind that envelope to Turn24's explicit-factor-aligned first subtraction;
- decide the previously isolated scalar inequality B1 < B1_star.

## One hypothesis / falsifier

Hypothesis:
The already-established shared-reconstruction -> repaired pure inverse -> 13-level selected recovery -> L1 public recombination coefficient-L1 ledger gives a provenance-complete absolute B1 below Turn24's B1_star, so the first post-F4 subtraction/divide boundary has a uniform estimator-independent envelope over the entire source-guaranteed prefix window.

Falsifier:
- the existing absolute chain does not actually reach L1;
- any needed stage uses only a relative operator ratio rather than an absolute envelope;
- or the resulting upward-rounded B1 is >= B1_star.

## 1. Absolute chain reaches L1

Existing independent coefficient-L1 chain:

1. Shared reconstruction:
       E_shared <= 6,957,728,854,835,200.

2. Repaired pure inverse + explicit exit cleanUp:
       E_root <= 1.2327282569105341e27.
   This state is on ctxtPrimes with ptxtSpace625; the subsequent unit normalization 28 changes the BGV intFactor to67 without multiplying ciphertext parts.

3. Selected recovery leaf:
   exact 13-level recurrence
       E_leaf <= 8192*E_root + 8191*(K+R).

   Existing source-sizing bounds:
       K <= 401,679,183,790,908.6,
       R <= 83,891,200,000.

4. L1 recombination:
   the exact full-ring coefficient-L1 amplification for the current rho/443 routing and finalized branch labeling is
       A1 = 49,548,
   with
       E(L1) <= A1 * E_leaf.
   No fresh cryptographic noise is introduced at this public-linear edge.

This is an absolute chain. No stock/candidate relative ratio is needed.

## 2. Integer-upward certificate

To avoid relying on decimal truncation, round every noninteger upper bound upward:

    E_root_hat = 1,232,728,256,910,534,100,000,000,000
    K_hat      = 401,679,183,790,909
    R_hat      = 83,891,200,000.

Then exactly:

    E_leaf_hat
      = 8192*E_root_hat + 8191*(K_hat + R_hat)
      = 10,098,509,880,614,386,188,547,250,535,619.

Using A1=49,548:

    B1_hat
      = 49,548 * E_leaf_hat
      = 500,360,967,564,681,606,870,139,169,538,850,212.

Hence:

    log2(B1_hat) ~= 118.59045257239751,

and in particular:

    B1 <= B1_hat < 2^119.

Turn24's sufficient threshold is:

    B1_star ~= 2^388.39384909974.

Therefore:

    log2(B1_star / B1_hat)
      ~= 269.80339652734233 bits.

So the threshold passes by an enormous deterministic margin.

## 3. Uniform first-boundary envelope

Turn24 gives, after mod-down of L1 to the fixed prefix P and explicit factor alignment:

    EN(q)
      <= 311*((q/Q0)*B1 + R) + EFhat.

Use:
    Q0 >= 2^399.5,
    q >= 2^183,
    B1 <= B1_hat.

At the worst lower endpoint for EN(q)/q:

    (q/Q0)*B1_hat
      <= 2^(183-399.5) * B1_hat
      < 4e-30.

Thus a simple strict integer-safe domination is:

    EN(q)
      < EFhat + 311*83,891,200,000 + 1
      = 4,155,105,766,733,618,287,140,112,599,228,004,062,478,126,504,142,997,320.

The exact integer certificate is:

    100*EN_hat
      = 415510576673361828714011259922800406247812650414299732000

    48*2^183
      = 588478287692501321609605258425718726509595822918503235584

and therefore:

    100*EN_hat < 48*2^183.

Hence for every source-guaranteed prefix in the Turn23 window:

    EN(q) < 0.48*q.

After the source-valid divideByP:

    E_u11(q) <= EN(q)/5 < 0.096*q.

At the lower endpoint the normalized ratio is at most approximately:

    EN/(0.48*q) <= 0.7060763079342008,

equivalent to approximately 0.5021039863 bits of margin to the 0.48q boundary.

The tiny B1 mod-down term is not the dominant contribution; Turn23's F4 envelope remains dominant.

## 4. Scientific consequence

Turn24 isolated one remaining uncertainty for the first Algorithm4 boundary: the absolute full-Q0 L1 envelope B1.

That uncertainty is now closed:

    PASS_ABSOLUTE_L1_PROVENANCE_CHAIN
    PASS_B1_BELOW_TURN24_THRESHOLD
    PASS_FIRST_POST_F4_UNIFORM_INDEPENDENT_L1_ENVELOPE.

Together with Turn24:
- exact Aung base-case 5-divisibility: PASS;
- explicit BGV factor alignment: PASS;
- prime-set / ptxtSpace625->125 / unit-factor transition: PASS;
- independent uniform L1 envelope: PASS.

Therefore the first Algorithm4 post-F4 subtraction/divide boundary is now statically closed at MATH evidence grade.

This does NOT imply:
- complete Algorithm4 correctness;
- native candidate correctness;
- baseline correctness;
- DFR/security compatibility;
- performance/value;
- novelty;
- paper readiness.

## 5. Remaining correctness frontier

The next source-order unresolved Algorithm4 boundary is outer j=1, inner i=0:

    y <- L2(z)
    u_0,2 <- F_e(u_0,1) = F_e(F_e(z))
    y <- (L2(z) - u_0,2)/5.

This is again a ptxtSpace625 boundary, but its F_e input is the already nonlinear u_0,1=F_e(z), so its factor and independent envelope must be propagated explicitly rather than inferred from the first boundary.

The later j=1,i=1 boundary then uses ptxtSpace125 and u_1,1, and remains separate.

## Verdict

PASS_ABSOLUTE_L1_PROVENANCE_CHAIN.
PASS_B1_BELOW_THRESHOLD_BY_269_803_BITS.
PASS_FIRST_POST_F4_UNIFORM_INDEPENDENT_L1_ENVELOPE.
PASS_FIRST_ALGORITHM4_SUBTRACT_DIVIDE_STATIC_CLOSURE.

OVERALL CANDIDATE CORRECTNESS:
    UNCLEAR / CORRECTNESS_GATE=BLOCKED.

NOVELTY_STATUS:
    PREFLIGHT.

SECURITY:
    PENDING.

VALUE:
    PENDING.

BASELINE:
    PENDING.

AUDIT:
    PENDING.

PAPER:
    NOT_READY.

## Next decisive test

Successor-session Paper-First correctness unit, no Native:
construct the next Algorithm4 source-order numerator

    L2(z) - F_e(F_e(z))

on the same fixed-prefix framework, derive its exact BGV intFactor alignment and an independent coefficient-L1 envelope, and prove or falsify the second 625->125 divide boundary. Reuse the current F4 state; do not regenerate the first-F4 or first-divide proofs.

The mandatory recovery-only native canary remains NOT_EXECUTED and continues to block evidence-order advancement to native parameter/interface verification.
