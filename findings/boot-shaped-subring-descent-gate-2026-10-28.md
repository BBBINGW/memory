# BOOT — Shaped small-batch CKKS subring-descent gate

Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER/SOURCE-CODE LEVEL ONLY
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

## Source target

Jules Dumezy,
"Fully Homomorphic Encryption for Small Batches of Complex Numbers",
IACR ePrint 2026/2513, updated 2026-10-21.

The current full PDF was not acquired by the Research MCP in this BOOT turn, but the author's public implementation repository
    jdumezy/eprint-2026-2513
was recovered and audited directly. Its README states that it implements the constructions and benchmarks of the paper.

Author public source:
https://jdumezy.com/publications/new-scheme/

Implementation:
https://github.com/jdumezy/eprint-2026-2513

The current repository source, not an inferred reconstruction, is used for the implementation claims below.

## What 2513 already does

Let:
- N be the ambient ring degree;
- k be the number of values in the batch;
- R be the replication factor set by the shaping unit;
- kR <= N/2.

The replicated layout stores value j on slot Rj, repeats the period kR across the N/2 CKKS slots, and treats all non-data positions in each period as guards.

The implementation defines:
    d = N / (2 k R).

Its layout documentation explicitly states that a period-kR slot vector is a sparse CKKS packing and that the corresponding plaintext polynomial is in X^d.

The native bootstrap pipeline is:
1. normalized trace onto period kR;
2. fiber-aware SlotsToCoeffs that reads data slots only;
3. ModUp under an ephemeral sparse secret;
4. normalized trace onto period k;
5. fiber-aware CoeffsToSlots that writes data slots and zero guards;
6. EvalMod;
7. recombination/final shaped rescale.

Source files:
- src/layout.rs
- src/bootstrapping/fiber.rs
- src/bootstrapping/transform.rs
- src/bootstrapping/mod.rs
- src/unit.rs
- src/security.rs

## Active-slot transform is ALREADY the paper's structure

The read-side fiber transform uses exactly k diagonal offsets:
    -t + R u,  t<R, u<k/R.

The source tests explicitly check:
    read_side_uses_k_offsets_and_ignores_the_guards.

The write side has at most k diagonals and writes zeros on guards.

The transform compiler then applies direct evaluation for <=2 diagonals or BSGS with default giant step near sqrt(k).

Thus:
    ACTIVE_SLOT_AWARE_CTS_STC = PRIOR ART / NATIVE 2513 DESIGN.

It is not a new BOOT contribution to say that CtS/StC work can be organized around k active values rather than N/2 ambient slots.

## New algebraic observation — shaping is exactly compatible with the guard-preserving subring

Let

    d = N / (2 k R),
    Z = X^d.

Then

    Z^(2 k R) = X^N = -1,

so the map

    Z -> X^d

embeds the negacyclic ring of degree 2kR,

    R_small = Z[Z] / (Z^(2kR)+1),

into the ambient ring

    R_N = Z[X] / (X^N+1).

Because the replicated plaintext after the period-kR trace is a polynomial in X^d, its exact message lies in this subring.

The shaping polynomial of 2513 is

    g(X) = U(X^(N/(2R))),

where U is a unit of a cyclotomic ring of degree 2R.

Since

    N/(2R) = d k,

we have

    g(X) = U((X^d)^k) = U(Z^k).

Therefore:

### Shaping-subring compatibility theorem

The 2513 shaping polynomial lies in the same degree-2kR subring as the period-kR replicated plaintext.

Moreover, let zeta_N = exp(i pi/N) and zeta_small = exp(i pi/(2kR)).
For the corresponding CKKS embeddings,

    g(zeta_N^(5^t))
      = U(exp(i pi 5^t/(2R)))

and

    U((zeta_small^(5^t))^k)
      = U(exp(i pi 5^t/(2R))).

Thus the data/guard magnitude profile of g is preserved exactly under the natural subring representation.

Status:
    SHAPING_SUBRING_COMPATIBILITY = PASS.

This is stronger than merely observing that U is "small": it identifies the exact minimum guard-preserving cyclotomic ring.

## Minimum guard-preserving physical degree

To retain k values with R slot classes per value, the target CKKS ring needs at least kR complex slots.

Hence the minimum standard-ring degree that preserves the complete data+guard layout is

    N_min = 2 k R.

For the principal small-batch case
    N=2^15, k=16, R=16,

this algebraic minimum is

    N_min = 512.

This is an algebraic/layout minimum only, NOT a security-valid parameter.

## Why the public glwe_switch_degree primitive is NOT sufficient

Current poulpy contains GLWESwitchDegree, which changes the polynomial degree of each GLWE column by coefficient insertion/selection when degrees divide each other.

Its API does not claim that a generic ciphertext under an arbitrary degree-N secret becomes a valid ciphertext under an independent smaller-ring secret.

By contrast, the conjugate-invariant conversion API explicitly distinguishes:
- raw degree switching of columns;
- secret embedding;
- cryptographic switching keys between different secrets/rings.

Therefore a real physical descent of the 2513 ciphertext requires a proper ring-switch / functional key-switch construction and a security analysis. One must not treat glwe_switch_degree as a cryptographic ring switch for a generic secret.

Status:
    RAW_DEGREE_REINDEXING_AS_CRYPTOGRAPHIC_DESCENT = INVALID.

## Security gate

The artifact checks every evaluation key against sparse-key-estimate 128-bit caps at its full modulus QP.

For ternary secret Hamming weight 1024, src/security.rs gives:

    ring degree 2^12 : cap 105 bits
    ring degree 2^13 : cap 211 bits
    ring degree 2^14 : cap 424 bits
    ring degree 2^15 : cap 851 bits
    ring degree 2^16 : cap 1707 bits.

The paper artifact's main N=2^15 high-depth configurations use key moduli near this 851-bit ceiling; the public README states the main secure bootstrapping restores up to 21 levels at N=2^15.

Therefore the appealing algebraic descent all the way to N_min=512 is not remotely justified by the current security table at the bootstrap modulus.

The repository also includes an n14 experiment:
    N=2^14, base2k=22, levels in {1,2},
described as a setting where two levels fit the caps.

This is important:
- security does NOT forbid every degree reduction;
- but it makes the admissible descent depth depend on the modulus/radix/gadget layout;
- deep 16–21-level bootstrapping cannot simply inherit the algebraic 64x degree reduction.

## Correct security/value gate

For each candidate target degree N':

1. recover the modulus width required at the exact point of descent;
2. include the auxiliary modulus P of every automorphism/tensor/ring-switch key under the target secret;
3. require
       log2(QP) <= SecurityCap(N', h);
4. choose the smallest secure gadget radix/digit layout;
5. compare the saved O(N log N)-style ring work against:
       - extra gadget digits;
       - ring-switch key size/work;
       - descent/lift cost;
       - any lost packing/parallelism.

Only a net end-to-end reduction counts.

## Prior-art/value warning from ePrint 2026/1779

The public abstract of
"Bootstrapping via Ring Switching without Slot Recovery"
(ePrint 2026/1779)
already establishes the broad idea of moving CKKS/BGV bootstrap computation to smaller rings and evaluating directly in the leaves without conventional slot recovery.

Its public benchmark for CKKS reports:
- parent N=2^17;
- leaf n=2^16;
- 1.13x serial speedup;
- about 2.03x–2.18x speedup when two leaves are evaluated in parallel.

Thus:
    GENERIC_RING_SWITCH_BOOTSTRAPPING = DIRECT PRIOR ART.

This also gives a practical warning: ring switching by a factor of two does not automatically yield a 2x serial gain because conversion/transform/key costs remain.

## Value judgment for 2513 + generic ring switching

2513's primary workload is low-latency small-batch arithmetic. Its strongest reported configurations already use N=2^15 because that degree is needed for the high bootstrap modulus/security budget.

If a ring-switch construction must enlarge the parent to N=2^16 merely to obtain a secure leaf at n=2^15, then the leaf arithmetic is only back at the ring degree of the existing direct 2513 bootstrap, while paying extra descent/lift overhead.

That would be negative for the single-ciphertext latency goal.

For shallow configurations, N=2^14 is already explored directly by the artifact with smaller limbs. In that regime a ring-switch detour must beat simply instantiating the whole shaped scheme at the smaller secure degree.

Therefore:

    GENERIC_2513_PLUS_RING_SWITCH = HIGH PRIOR-ART RISK / WEAK VALUE.

## What could still survive

Only a substantially narrower result would be worth reopening:

A. PRE-MODUP_ONLY_DESCENT
   Descend during the low-modulus forward-transform stage, run fiber SlotsToCoeffs in a smaller secure ring, then return to the large ring before high-modulus ModUp/EvalMod.

   This could avoid the high-modulus small-ring security barrier, but must beat the two ring conversions plus the already-k-aware BSGS transform.

B. SHAPING-PRESERVING_RING_SWITCH_THEOREM
   A scheme-level proof that the ring-switch map preserves the shaped-error ideal/profile and allows a strictly cheaper descent/lift than generic 1779 for the guard-band representation.

   The algebraic theorem above is only the plaintext/unit part; ciphertext noise/key switching is not established.

C. MULTI-LEAF_THROUGHPUT
   If multiple shaped small-batch leaves arise naturally from one parent ciphertext, 1779-style parallelism may improve throughput.
   This is misaligned with the main low-latency single-small-batch objective unless a real workload needs the leaves.

## Gate decision

ACTIVE_SLOT_AWARE_TRANSFORMS:
    ALREADY 2513.

SHAPING_SUBRING_COMPATIBILITY:
    PASS (new algebraic observation).

MINIMUM_GUARD_PRESERVING_DEGREE:
    2 k R (layout/algebra only).

CRYPTOGRAPHIC_RING_DESCENT:
    NOT ESTABLISHED.

HIGH_MODULUS_DEEP_DESCENT:
    STRONGLY SECURITY-LIMITED.

GENERIC_2513_PLUS_1779:
    PARK / PRIOR_ART-RISK / VALUE WEAK.

PRE_MODUP_ONLY_DESCENT:
    UNCLEAR, LOW-MEDIUM PRIORITY.

NOVELTY:
    NOT ESTABLISHED.

CODEX/NATIVE:
    NOT REQUIRED NOW.

## Priority

Do not spend native/Codex cycles on this candidate while:
- 1779 full text is missing;
- no end-to-end modulus/security table shows a target degree reduction;
- and no stage profile shows the pre-ModUp fiber transform dominates enough to repay ring switching.

The stronger current BOOT paper-only candidate remains the 1779 partial-recovery interaction-rank direction, pending its exact source.

B163 remains the highest native gate once Codex quota returns.
