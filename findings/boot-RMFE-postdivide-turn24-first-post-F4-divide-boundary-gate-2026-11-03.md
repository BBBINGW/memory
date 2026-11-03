# BOOT / B158 — Research Turn 24/25 — first post-F4 subtraction / divideByP boundary gate

**Date:** 2026-11-03 Asia/Singapore  
**TRACK_ID:** BOOT  
**ACTIVE_SUBLINE:** B158_CHECKPOINT_DECOUPLED_HALF_BASIS  
**Phase:** CORRECTNESS_GATE  
**Candidate:** legacy-484479fe4613  
**Native execution:** NONE.

## Scope and authority

This is exactly one Paper-First correctness unit following Turn 23. It does not repeat the first-F4 construction. The supplied verified fallback authority at turn start is local `BBBINGW/memory main@9f2a23973288e9ee8bdacb89dfc47c0ac9f0db26`. The local clone is not mounted in the current runtime. GitHub Notes reads are unhealthy; therefore no connector-only state is treated as overriding the supplied local authority. Public-source inspection is used only for source semantics.

Turn-23 prerequisite retained:
- p=5, ptxtSpace=625, a=67;
- ordered ctxt-prime prefix P, q=product(P), 183 <= log2(q) < 247;
- completed F4(x)=x^5-5x^3+5x with factor d=a^5 q^4 mod625;
- independent envelope
  EF4(q) < EFhat
  = 4155105766733618287140112599228004062478100413979797319
  < 0.48*2^183 <= 0.48*q.

## One hypothesis / falsifier

Hypothesis: the immediate Algorithm-4 boundary
  u_11 = (L1(z)-F4(z))/5
can be executed at the same prefix P without stock implicit factor harmonization, with exact 5-divisibility, correct BGV metadata transition 625->125, unchanged prime set, and a source-independent coefficient-L1 safety certificate.

Falsify if:
1. L1 and F4 cannot be explicitly factor-aligned by a public unit;
2. Aung's theorem does not guarantee divisibility for arbitrary Z625 lifts;
3. HElib divideByP changes the prime set or produces a nonunit factor;
4. or no independent envelope can be proved from the current durable bounds.

## Aung Algorithm-4 base case

Aung Algorithm 4 initializes u_00=z. At outer j=0 it sets y=L1(z), computes u_01=F_e(u_00), then performs y=(y-u_01)/p.

The source proof writes z=sum_t a_t phi(e_t), with arbitrary a_t in Z_{p^e}, and proves L1(z)-F_e(z) is divisible by p. The proof uses:
- a_t-a_t^p is p-divisible;
- mixed multinomial terms in the p-th power carry p;
- F_e(X)=X^p+pG(X).

Therefore the candidate's arbitrary recovered Z625 lifts are sufficient for this first divisibility statement. No equality with a stock higher-adic transcript is required.

## Exact BGV factor alignment

At Algorithm-4 entry the recovered scalar branches and therefore each public correction recombination L_t carry the normalized common factor a=67. The completed first F4 from Turn23 carries
  d = a^5 q^4 mod625.

Do not invoke stock add/subtract factor harmonization. Instead align only L1 with
  h0 = d * a^{-1} = a^4 q^4 mod625.

Because a and q are units mod625, h0 is a unit. Applying the internal Ctxt factor-preserving semantic operation corresponding to
  L1.mulIntFactor(h0)
keeps the plaintext L1(z), prime set P and ptxtSpace625, and changes its factor from a to d.

Then
  N = aligned(L1) - F4
has identical P, ptxtSpace625 and intFactor d on both operands. The subtraction therefore requires neither mod-up nor implicit noise-estimator-driven BGV factor harmonization.

Finite exact residue audit over all phi(625)=500 possible q-unit residues gives:
- a*h0 == d mod625 in every case;
- gcd(h0,625)=1 in every case;
- max |balRem(h0,625)| = 311.

Thus define H0(q)<=311.

This private/internal mulIntFactor access remains the same narrow implementation-contract issue as Turn23; it is not an algebraic obstruction and introduces no key or secret.

## divideByP type transition

Pinned HElib semantics for Ctxt::divideByP:
- require ptxtSpace divisible by p and greater than p;
- require encrypted plaintext zero mod p;
- multiply ciphertext parts by p^{-1} modulo Q=product(primeSet);
- divide noiseBound by p;
- divide ptxtSpace by p;
- reduce intFactor modulo the new ptxtSpace;
- leave primeSet unchanged.

Since Aung's base case proves N is zero modulo5, the semantic precondition holds. Hence after divideByP:
  ptxtSpace: 625 -> 125,
  primeSet: P -> P,
  intFactor: d -> d mod125 = a^5 q^4 mod125,
and this factor remains a unit.

The plaintext is exactly
  u_11 = (L1(z)-F4(z))/5 in Z125.

So the first post-F4 boundary has no construction failure and no p-adic algorithmic obstruction at the algebra/type level.

## Independent L1 envelope gate

Let B1 be the full-Q0 independent coefficient-L1 representative envelope for L1(z) at the current construction before reduction to P. Under the same inherited mod-down contract as Turn23:
  A1(q) = (q/Q0) B1 + R.

After explicit factor alignment and subtraction:
  EN(q)
    <= H0(q) A1(q) + EF4(q)
    <= 311*((q/Q0)B1 + R) + EFhat.

A sufficient uniform condition for the entire source-guaranteed prefix window is EN(q)<0.48q. The worst endpoint for this bound is q=2^183. Using Q0>=2^399.5 and R<=83891200000 gives

  A1(2^183) <
    ((0.48*2^183 - EFhat)/311)
    = approximately 2^171.89384909974,

equivalently the sufficient full-Q0 condition

  B1 < B1_star
     = (2^399.5/2^183) *
       (((0.48*2^183-EFhat)/311)-R)
     = approximately 8.28321073366513e116
     = approximately 2^388.39384909974.

If this condition holds, then
  EN(q) < 0.48q
throughout 183<=log2(q)<247, and after divideByP the resulting independent envelope is
  Eu11(q) <= EN(q)/5 < 0.096q.

## Critical evidence gap

The current recovered evidence establishes relative four-output recombination/operator factors, but this turn did not recover a provenance-complete absolute full-Q0 independent envelope B1 for L1(z) under the exact current PRE-TAG + POST-DIVIDE construction. Turn23's inherited E0 bound cannot be silently identified with B1, and multiplying it by an old relative L1/L0 operator ratio would add an unsupported interface assumption.

Therefore the algebra/type/divisibility portion PASSES, but the requested independent L1 noise certificate is still UNCLEAR. This is an evidence/proof-link gap, not a demonstrated construction failure or inherent Algorithm-4 obstruction.

## Verdict

PASS_FIRST_POST_F4_EXACT_DIVISIBILITY.
PASS_FIRST_POST_F4_EXPLICIT_FACTOR_ALIGNMENT.
PASS_DIVIDEBYP_625_TO_125_TYPE_TRANSITION.
UNCLEAR_FIRST_POST_F4_INDEPENDENT_L1_ENVELOPE.
OVERALL TURN24 VERDICT: UNCLEAR.

Candidate remains ACTIVE / CORRECTNESS_GATE=BLOCKED.
Novelty=PREFLIGHT.
Security=PENDING.
Value=PENDING.
Baseline=PENDING.
Audit=PENDING.
Paper=NOT_READY.

## Paper-level uncertainty reduced

Before this turn, the first post-F4 Algorithm-4 boundary jointly mixed three uncertainties: p-adic divisibility, BGV factor/prime-set typing, and independent noise safety. The first two are now statically closed. The remaining uncertainty is a single quantitative proof link: the absolute full-Q0 L1 envelope B1 for the current construction.

## Next decisive test

No Native. Recover or derive B1 directly from the current shared-reconstruction -> pure-inverse -> pruned-recovery -> L1 recombination ledger, without substituting relative operator ratios for an absolute bound. Compare it against
  B1_star ~= 2^388.39384909974.
If B1<B1_star, the first post-F4 boundary closes uniformly and the remaining correctness blocker moves to later Algorithm-4 divide boundaries plus the mandatory native canary. If the bound cannot be derived or exceeds the threshold, identify whether that is merely a loose proof envelope or an actual construction obstruction.
