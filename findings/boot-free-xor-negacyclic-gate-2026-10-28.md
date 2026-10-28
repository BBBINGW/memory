# BOOT — Free-XOR negacyclic single-PBS lower-bound gate

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

B145+B152: PARK / FAIL_NATIVE_VALUE
B158_ALGEBRA: PASS
B158_CTCT_MULT_COUNT: OPTIMAL
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B158_NATIVE_FEASIBILITY: UNRESOLVED
B162_B161_HYBRID: VALID_FAIL_AT_K1024
B163: NOT_RUN

## Fresh source

Ali Ajorian and Osman Biçer,
"Free-XOR TFHE via Lazy Bootstrapping",
arXiv:2610.29983, submitted 2026-10-21.

Primary arXiv HTML was available and inspected.

The paper:
- encodes a Boolean bit by an element of Z_4 whose parity is the logical bit;
- evaluates XOR by ciphertext addition;
- uses headroom/padding so several additions can occur before refresh;
- evaluates supported non-free symmetric binary gates using two PBS operations;
- performs lazy bootstrapping when the maximum possible value approaches headroom.

Primary source:
https://arxiv.org/abs/2610.29983

Relevant primary HTML sections:
Introduction, Sections 3.1-3.2 and 4.2-4.4.

The paper itself explicitly states that its supported non-free binary gates AND/NAND/OR/NOR require two bootstrappings, while XOR/XNOR/NOT are handled through the free-XOR representation and additions.

## Prior source

Chen et al.,
"Free-XOR Gate Bootstrapping",
ePrint 2024/1703.

This earlier construction introduced free-XOR in a single-bit plaintext setting and built an AND construction using two blind rotations. It also gives an identity-gate/bootstrap mechanism used to refresh XOR-heavy symmetric-cipher computations.

Primary source:
https://eprint.iacr.org/2024/1703.pdf

The web PDF text was readable; visual screenshot retrieval was attempted in this research turn but the remote PDF endpoint returned a cache/fetch error. Do not claim visual verification beyond the extracted text.

## Question

Can the padding/headroom requirement be removed entirely by a clever encoding so that:

1. XOR remains free under ciphertext addition; and
2. a functionally complete nonlinear binary gate such as AND is implemented by a single ordinary negacyclic PBS;
3. no unused half-domain / padding region is reserved?

If this were possible, lazy free-XOR circuits would no longer need headroom-induced refreshes merely to protect a padding bit.

## Abstract free-XOR model

Let M be an additive plaintext group supporting homomorphic addition.

Let
    pi : M -> F_2
be the logical decoding map.

For XOR to be implemented exactly by plaintext/ciphertext addition for all valid encodings, require

    pi(x+y) = pi(x) + pi(y) mod 2.

Thus pi is a group homomorphism from M to F_2.

Immediately,

    pi(-x) = -pi(x) = pi(x)

because F_2 has characteristic 2.

Therefore logical decoding is invariant under additive negation:

    pi(-x) = pi(x).              (1)

This is independent of the particular redundant representatives used for Boolean 0 and 1.

## Negacyclic PBS property

A standard FHEW/TFHE blind-rotation test polynomial implements a negacyclic LUT:

    F(t+N) = -F(t)

on paired rotation indices separated by the half-period N.

If the PBS output is interpreted using the same additive free-XOR decoding pi, then by (1)

    pi(F(t+N))
      = pi(-F(t))
      = pi(F(t)).

Therefore:

### Lemma — logical half-period invariance

Any single standard negacyclic PBS whose output stays in an additive free-XOR encoding necessarily computes a Boolean function whose logical value is identical on each negacyclic pair:

    logical_F(t+N) = logical_F(t).

Equivalently, sign changes in the plaintext representation cannot flip the Boolean value, because free-XOR homomorphic decoding is sign-invariant.

## Binary-gate impossibility without an unused half-domain

Assume four binary input pairs
    (0,0), (0,1), (1,0), (1,1)
are encoded into four distinct active LUT indices and no padding/unused half-domain is reserved.

The negacyclic involution t -> t+N partitions these four active indices into two pairs.

By the lemma, a single PBS can only output the same Boolean value on the two members of each pair.

Hence the truth table must admit a partition into two equal-output pairs.

For AND, the multiset of outputs is

    {0,0,0,1}.

No partition into two two-element pairs can make both pairs equal-valued, because the unique 1 must be paired with a 0.

Therefore:

    ONE_STANDARD_NEGACYCLIC_PBS_AND_WITH_FULL_ACTIVE_DOMAIN = IMPOSSIBLE

under the stated additive free-XOR model.

The same counting obstruction applies to any binary Boolean gate with truth-table Hamming weight 1 or 3.

Examples include AND, NAND and their input-negated/asymmetric equivalents.

## Why padding fixes the obstruction

Padding / an unused half-domain places all active gate-input indices in only one representative from each negacyclic pair.

The paired index t+N is then outside the active input set and is free to carry the forced negative plaintext value.

Thus padding is not merely an implementation convention. In this model it supplies exactly the degrees of freedom needed to evade the logical half-period-invariance obstruction.

This explains structurally why the 2026 lazy-free-XOR paper protects its padding bit and introduces headroom rather than simply allowing unrestricted wraparound.

## Relation to the 2026 construction

Ajorian–Biçer use an encoding where the Boolean bit is parity in Z_4:
- false has representatives 0 or 2;
- true has representatives 1 or 3.

This concrete encoding satisfies the abstract sign-invariance property:
    parity(-m mod 4) = parity(m).

The paper observes that non-negacyclic characteristic functions such as AND and OR require padding, and then reserves additional headroom to keep XOR additions from overwriting that padding region.

The lower-bound lemma above gives a general explanation for why a purely additive free-XOR decoding cannot use plaintext negation itself to distinguish the paired Boolean outputs of an unbalanced gate.

## Cheap observation: all 16 binary Boolean gates are algebraically generated by AND + free affine terms

Every binary Boolean function has algebraic normal form

    f(x,y) = a0 + a1*x + a2*y + a12*x*y
over F_2.

Therefore:
- if a12=0, the gate is affine and can in principle be composed from XOR/NOT/constants;
- if a12=1, it is AND plus free affine terms.

Hence a correct free-XOR AND primitive is functionally sufficient to support all 16 binary Boolean functions through free affine pre/post-composition.

The 2026 paper focuses its direct two-PBS indexed construction on symmetric gates and its implementation tables list supported symmetric gates. The ANF observation expands logical gate coverage, but by itself is too elementary to constitute a CCF-A/B contribution.

Status:
    ALL_16_GATE_COVERAGE_BY_ANF = VALID_OBSERVATION
    RESEARCH_VALUE = LOW / NOT_A_PAPER_CONTRIBUTION

## Compiler/synthesis prior art closure

A tempting next step would be to optimize whole circuits by:
- keeping XOR/affine regions in a free Boolean encoding;
- switching encoding only around nonlinear regions;
- synthesizing with XOR-AND / ESOP structure.

This broad direction is already direct prior art.

Mingfei Yu, Gabrielle De Micheli, Giovanni De Micheli,
"Making the Best Switch: Encoding Strategy Management for Efficient TFHE Circuit Evaluation",
ICCAD 2025.

The published abstract states that it:
- manages multiple plaintext encoding spaces;
- uses ESOP structure to partition Boolean functions into encoding-aligned regions;
- explicitly optimizes when/where to switch encodings;
- minimizes switch overhead;
- reports substantial evaluation-time reductions over baselines without encoding-switch management.

Sources:
https://graphsearch.epfl.ch/en/publication/d4a6ef0a-dfad-479d-93cb-d700e65ac14e
DOI: 10.1109/ICCAD66269.2025.11240699

Therefore:

    GENERIC_FREE_XOR_ESOP_ENCODING_SWITCH_COMPILER = PRIOR_ART.

## What the lower bound does and does not prove

It proves only the following model-specific statement:

If:
1. Boolean XOR is represented by an additive-group homomorphic decoder pi:M->F_2;
2. a single ordinary PBS uses a negacyclic LUT F(t+N)=-F(t);
3. all four binary input states occupy the active domain with no unused/padding half;

then a one-PBS realization cannot compute a truth table of Hamming weight 1 or 3, including AND.

It does NOT exclude:
- a different non-additive free-XOR representation;
- multiple PBS / multiple blind rotations;
- a larger domain with padding;
- a scheme whose output decoding is not a group homomorphism;
- a different accumulator ring/functionality not subject to the same negacyclic condition;
- scheme switching to another ciphertext type.

## Research decision

HEADROOM_FREE_WRAPAROUND_PLUS_ONE_STANDARD_PBS_AND:
    FAIL by negacyclic/free-XOR lower bound.

ONE_STANDARD_PBS_FUNCTIONALLY_COMPLETE_GATE_IN_THIS_MODEL:
    FAIL.

TWO_PBS_AND/SYMMETRIC_NONLINEAR_CORE:
    CONSISTENT_WITH MODEL LOWER BOUND; no optimality claim beyond the stated model.

ALL_16_BINARY_GATE_SUPPORT_VIA_AND_PLUS_AFFINE:
    VALID BUT LOW NOVELTY.

GLOBAL_ESOP / ENCODING_SWITCH COMPILATION:
    PRIOR ART (ICCAD 2025).

FREE_XOR_HEADROOM_PARAMETER_TUNING:
    OPEN ENGINEERING in 2026 paper, but not a high-priority cryptographic contribution.

NOVELTY:
    NOT_ESTABLISHED for any positive construction from this branch.

CODEX/NATIVE:
    NOT REQUIRED.

## Priority implication

Do not invest BOOT cycles in:
- trying to remove the padding bit while keeping the same additive free-XOR + standard negacyclic PBS model;
- generic XAG/ESOP encoding-switch compilation;
- expanding the direct gate table from symmetric gates to all 16 binary gates.

A future positive direction would need to break one assumption of the lower-bound model in a nontrivial way, e.g. a new accumulator functionality or ciphertext representation where the nonlinear gate is not constrained by the same negacyclic pairing.

B163 remains untouched and stays the highest native gate once Codex quota returns.
