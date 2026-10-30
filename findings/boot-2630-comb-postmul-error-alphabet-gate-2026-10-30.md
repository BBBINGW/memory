# BOOT — ePrint 2026/2630 post-multiplication comb-error alphabet gate

Date: 2026-10-30
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Session: 密码学 15.0 — Research Turn 8/25

Status:
FAIL_GENERIC_COMB_AMORTIZATION_CLOSURE_UNDER_MULTIPLICATION /
PASS_FULL_ERROR_ALPHABET_COUNTEREXAMPLE /
ADDITIVE_COMPOSITION_REMAINS_PLAUSIBLE /
PAPER_CORRECTNESS_NOT_CHALLENGED /
FULL_SOURCE_VERSION_GATE_PENDING

## Scope and provenance

Fresh BOOT source:
Philippe Chartier and Mohammed Lemou,
"Exact Error Bootstrapping and Comb Bootstrapping in FHEW/TFHE",
IACR ePrint 2026/2630, listed 2026-10-24.

Public ePrint mirrors/search indexing currently expose the abstract. The full PDF could not be acquired through the available web path during this turn, so this finding deliberately audits only the algebraic composition claim that is implied by the abstract-level interface.

Abstract-level source claims used:
- bootstrapping the error rather than full decryption;
- rounding at a resolution aligned with the message modulus preserves the message;
- reduction modulo a small integer isolates a noise-free encryption of the error;
- a blind rotation lifts and subtracts the error;
- because the error has many fewer possible values than ring rotation positions, one blind rotation can refresh several ciphertexts ("comb bootstrap");
- between refreshes, one ciphertext supports modular additions and multiplications without programmable bootstrapping;
- reported 8-bit single-thread refresh speedups: 3.5x ordinary exact-error refresh and 9.1x comb refresh; multiplication 6.5x faster than TFHE-rs.

This turn does NOT claim that the paper states comb amortization is preserved after multiplication.

## Primary hypothesis

The small-error-alphabet property that enables comb bootstrapping is generically stable under the paper's advertised ciphertext-ciphertext multiplication interface.

Cheapest falsifier:
ignore implementation noise and analyze only the unavoidable plaintext/error cross terms in the decryption phase. If one multiplication can expand the possible error values from a small set E to all of Z_p, then generic post-multiplication comb amortization is not closed under multiplication even before adding relinearization/rounding noise.

## Minimal phase model

Use the exact-integer normalized phase interface

    D(c) = m + e mod p,

where:
- m in Z_p is the encrypted message;
- e belongs to a small integer error set E.

This is the minimal abstract interface required by exact-error bootstrapping: the refresh mechanism distinguishes/removes e while preserving m modulo p.

A multiplicative homomorphic operation implementing multiplication modulo p must, before any implementation-specific correction terms, represent the product phase

    (m1 + e1)(m2 + e2)
      = m1 m2
        + m1 e2
        + m2 e1
        + e1 e2
        mod p.

Thus the intrinsic post-multiplication error is

    e_x = m1 e2 + m2 e1 + e1 e2 mod p.

Any extra multiplication/key-switch/rounding error can only enlarge the set that a correctness screen must handle; it is not needed for the counterexample.

## Full-alphabet lemma

Assume the refreshed error support E contains 0 and a unit u in Z_p.

Then the set of possible post-multiplication errors over arbitrary messages is all of Z_p.

Proof:
choose e1=u and e2=0. Then

    e_x = m2 u mod p.

Because u is a unit, multiplication by u is a permutation of Z_p. As m2 ranges over Z_p,

    {e_x} = Z_p.

Therefore:

    |E_x| = p.

The simplest common case is E containing {0,1}, giving e_x=m2.

This is exact finite-ring algebra, not a Gaussian approximation.

## Comb-capacity consequence

A negacyclic blind-rotation accumulator of degree N has at most 2N signed rotation positions.

If one comb bootstrap simultaneously refreshes k independent ciphertexts by assigning disjoint rotation positions to their possible errors, a necessary injectivity/counting condition is

    k * |E| <= 2N.

Before multiplication, if |E|=r << p,

    k_pre <= floor(2N/r).

After one generic multiplication under the lemma,

    |E_x| = p,

so

    k_post <= floor(2N/p).

Thus the small-error-alphabet amortization can collapse from an r-controlled batch factor to a message-modulus-controlled batch factor after one multiplication.

This is an information/correctness capacity bound for the simple comb mechanism; it does not assume any particular FFT implementation.

## Interval sanity bound

If centered messages satisfy |m_i| <= M and errors |e_i| <= B before reduction modulo p, then

    |e_x| <= 2 M B + B^2

before implementation-specific multiplication noise.

Hence even without the exact full-alphabet argument, the error interval grows by approximately a factor 2M for small B.

For centered 8-bit arithmetic M=127:
- B=1 gives pre-wrap bound B_x=255;
- B=2 gives B_x=512.

Illustratively, at N=1024:
- if B=1, interval counting gives at most floor(2048/511)=4 comb lanes;
- if B=2, at most floor(2048/1025)=1 lane before considering modular support saturation.

These N=1024 numbers are illustrative only, NOT claimed to be the source's ePrint parameters.

## Addition behaves differently

For addition,

    (m1+e1)+(m2+e2)
      = (m1+m2) + (e1+e2).

So the post-addition error set is the Minkowski sum

    E_+ = E + E.

For an interval E=[-B,B],

    |E_+| <= 4B+1,

only linear growth.

Therefore comb amortization is structurally much more compatible with additive chains than with unrestricted multiplication chains.

## What this proves

PASS:
- generic multiplication does not preserve a small message-independent error alphabet;
- if E contains 0 and any unit, post-multiplication error support over arbitrary messages equals all Z_p;
- a comb design whose batching capacity depends on small |E| must therefore re-evaluate capacity after multiplication;
- addition and multiplication have qualitatively different comb-amortization behavior.

FAIL:
- "comb amortization is generically closed under multiplication."

## What this does NOT prove

This does NOT show:
- any error/correctness bug in ePrint 2026/2630;
- the paper's 9.1x comb benchmark is wrong;
- the paper claims comb is used directly after arbitrary multiplication;
- the multiplication primitive is slower than reported;
- exact-error bootstrapping fails;
- a tailored multiplication cannot deliberately normalize/compress error before comb refresh.

The full paper may already schedule ordinary exact-error refresh after multiplication, restrict messages, use a special multiplication representation, or explicitly account for the expanded error alphabet. Full-source confirmation is pending.

## Research significance

The composition boundary localizes a potentially publishable direction more precisely than "make comb faster":

Existing exact-error comb refresh gains amortization from a small error alphabet.
Generic multiplication destroys that invariant through message-error cross terms.

A nontrivial continuation would require a representation or multiplication rule R such that

    small E
      -> multiply
      -> small message-independent E'

without inserting a full programmable bootstrap.

That would preserve comb width across arithmetic multiplication chains and could change a meaningful latency/throughput frontier.

Do not treat this as established novelty until the full 2026/2630 source and adjacent prior work are checked.

## Decision

PARK as a source-gated positive research question, not as a paper flaw.

Next high-information gate if the full source becomes available:
inspect the exact multiplication algorithm and refresh schedule in 2026/2630 and test whether the implementation already performs error normalization / ordinary error refresh before comb batching.

If it does, this finding becomes a boundary explanation rather than a new gap.
If it does not and comb is intended directly after generic multiplication, the full-alphabet lemma becomes a concrete design bottleneck requiring resolution.

TOP_LEVEL_BOOT_FRONTIER_EXHAUSTED: false.
PENDING_PI_DECISIONS: none.
PENDING_CODEX_TASKS: none.
