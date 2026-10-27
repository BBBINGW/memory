# PURE-FHE — Post-P0-54 Product-Typed KSK Inversion-Orbit Lower-Bound Gate

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
LATEST_COMPLETED: P0-PRESCOUT-54
NEXT_ITERATION: P0-PRESCOUT-55 NOT_STARTED
STATUS: FAIL_LINEAR_PRODUCT_TYPED_KSK_COMPRESSION / PASS_MODEL_SPECIFIC_INVERSION_ORBIT_LOWER_BOUND / GL_BIGSWITCH_PARK
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO
STATE_UPDATE: YES — isolated PURE-FHE finding only. Root STATE.md and all other tracks unchanged.

## Scope

This is NOT P0-PRESCOUT-55.

It tests the last high-value GL candidate left after the PairSwitch lazy-rebase and shared-cross-diagonal gates:

Can a decomposition-fused/product-typed compressed key representation directly inject fresh switching error AFTER the product-secret action s*g(s), while storing asymptotically or concretely fewer product-key objects than PairSwitch and retaining the original 2n-switch general-input path?

No native implementation, Codex, GPU/server work, or cross-track write was performed.

## Primary-source facts

### Original GL BigSwitch
Gentry–Lee, ePrint 2025/1935, cached mirror PDF SHA256
985173da6bc45f1c89c86769d5b6b16bfcdd98bf07e91476cd424778b8d9ec84
VERSION_UNVERIFIED.

Physical pp.15–16:
- a Trace product yields (d0,d1,d2,d3);
- the d3 term is under the product secret s(X,W)s(Y^-1,W^-1);
- relinearization contains one linear Switchbig(d3,K_product) contribution;
- p.10 defines Switchbig as standard gadget/key-switch accumulation over the extended ring.

### PairSwitch current public ePrint abstract
ePrint 2026/2373, approved 2026-10-08:
- Galois splitting decomposes BigSwitch into base-ring diagonals indexed by an inversion-closed coset;
- pair-merge uses n/2+1 product keys while retaining the original 2n key switches;
- a diagonal can borrow its inverse partner's product key through
    x*g(s)+y*s*g(s)
    = g(g^-1(x)*s + g^-1(y)*s*g^-1(s));
- the authors state that no per-diagonal BigSwitch with 2n key switches holds fewer than 3n/2+1 total keys.

Full PDF remains HTTP-403 blocked, so the authors' formal lower-bound theorem is NOT claimed to have been reproduced.

## Candidate model

Let H be the cyclic Galois subgroup indexing n split diagonals. Write

  q_g(s) := s * g(s).

A direct product-typed switching key for diagonal g contains ciphertext material whose plaintext source is q_g(s), so that runtime gadget digits multiply a key that ALREADY encodes the product-secret function. Thus fresh KSK error is injected after the product action:

  y_g q_g(s) + e_g,

rather than TFB's

  s( y_g g(s) + e_g )
  = y_g q_g(s) + s e_g.

This is exactly the noise placement we want.

Assume the fast-path model:
1. the product-typed stage is linear in runtime public gadget digits;
2. stored product-typed key plaintexts are fixed secret-dependent functions;
3. public ring/Galois automorphisms may be applied;
4. no ciphertext-ciphertext multiplication or runtime secret multiplication is used before fresh KSK error injection;
5. each diagonal gets at most one product-typed switching contribution, preserving the original/PairSwitch 2n total-switch structure.

This is intentionally model-specific.

## [DERIVATION] Formal conjugate model

Introduce formal secret conjugates

  X_h := h(s),  h in H.

Then the product-secret function for diagonal g is the quadratic monomial

  q_g = X_e X_g.

Applying a public Galois automorphism h maps it to

  h(q_g) = X_h X_{hg}.

Because multiplication is commutative, the monomial is identified with the unordered pair

  {h, hg}.

Question: when can q_{g'} = X_e X_{g'} be obtained from q_g by ONE public Galois automorphism?

We need

  {h, hg} = {e, g'}.

There are only two cases:

Case 1:
  h=e, hg=g
so
  g'=g.

Case 2:
  hg=e and h=g'
so
  h=g^-1
and
  g'=g^-1.

Therefore

  q_{g'} lies in the public-Galois orbit of q_g
  iff
  g' in {g, g^-1}.

So a directly stored product-secret key for g can serve exactly its inversion partner g^-1, and no other diagonal, under one automorphism.

This is the algebra behind PairSwitch's pair merge.

## [DERIVATION] Inversion-orbit lower bound

The product-secret labels H partition into inversion orbits

  [g] = {g,g^-1}.

Let f be the number of self-inverse elements of H. Then the number of inversion orbits is

  (n+f)/2.

For a cyclic group of even order n, the self-inverse elements are identity and the unique order-two element, so f=2 and

  #orbits = n/2 + 1.

For n=256 this gives

  129

product-secret orbits, exactly matching PairSwitch's public abstract count n/2+1.

Now impose the one-product-switch-per-diagonal fast-path budget.

A stored product-typed key whose plaintext is not proportional/equivalent to q_g (up to public automorphism) cannot, in a SINGLE linear switching contribution, output arbitrary y_g q_g for that diagonal: any other product-class components in the key plaintext remain present for arbitrary y_g and cannot be cancelled without additional independent key contributions.

Thus one stored direct product-typed key can cover at most one inversion orbit.

Therefore any direct, one-product-switch-per-diagonal, fresh-error-after-product construction requires at least

  (n+f)/2

stored product-typed key classes; for cyclic even H,

  r_product >= n/2 + 1.

PairSwitch attains this count.

## Why arbitrary mixed basis keys do not beat the bound under the same switch budget

Suppose instead one stores

  P_k = Enc_s(h_k(s))

where h_k is a public linear combination of several distinct product classes q_g.

Using only ONE such key contribution for diagonal g gives plaintext proportional to h_k(s), not pure q_g(s). Public Galois automorphisms preserve the ratio/inversion class of each quadratic monomial component; they do not convert a component from class [g1] into [g2].

To isolate q_g from a mixture requires combining multiple independent key contributions so unwanted classes cancel. That consumes additional product-typed switches.

Hence mixed bases can trade storage for more online switch contributions, but cannot improve storage while preserving the PairSwitch/original 2n-switch endpoint.

This is analogous to previous action-basis tradeoffs:
  fewer stored basis elements -> online composition/extra applications;
  one-stage direct action -> enough stored basis rank.

## Relation to PairSwitch's stated lower bound

The public PairSwitch abstract states a stronger whole-key result:
  no per-diagonal BigSwitch with 2n key switches holds fewer than 3n/2+1 total keys.

The derivation here does NOT claim to reproduce that theorem. It establishes only the product-secret half:
  r_product >= n/2+1
inside the explicit direct product-typed model above.

Adding the separate Galois/source keys plausibly yields the abstract's total-key count, but without the full PDF we do not state the exact theorem assumptions.

The exact numerical coincidence is strong consistency evidence, not a novelty claim.

## [NEGATIVE] The desired decomposition-fused candidate collapses

The hoped-for candidate required all three:
1. direct product-secret action before fresh switching error;
2. fewer than PairSwitch product-key resident classes;
3. original/PairSwitch 2n-switch online structure.

In the linear direct-switch model these are incompatible:
- (1)+(3) imply one direct product-typed key action per diagonal;
- public automorphism reuse groups q_g only by inversion;
- therefore (2) cannot beat n/2+1 product classes.

Escapes:
- combine multiple mixed keys per diagonal -> >2n switches;
- switch compact source then multiply by s -> TFB and s*E;
- materialize/rebase product keys -> PairSwitch resident-memory side;
- nonlinear/tensor operator -> outside this model and must be costed separately.

No concrete fourth mechanism remains.

## GL BigSwitch branch decision

GL BigSwitch has now been screened through the natural post-PairSwitch possibilities:

1. Lazy/public rebase without resident product keys
   -> linearity moves rebase online -> TFB-like runtime relinearization.

2. One global cross-diagonal shared rebase
   -> algebraically valid, but accumulates switching error first and produces s*E -> exactly TFB noise placement.

3. Direct decomposition-fused/product-typed compressed KSK
   -> under one-product-switch-per-diagonal linear model, public Galois reuse only covers inversion pairs; requires >=n/2+1 product-key classes, attained by PairSwitch.

Therefore the GL BigSwitch subline is PARKED for PURE-FHE.

This is not a universal impossibility theorem. Reopen only if one of the following appears:
- a genuinely nonlinear compact operator with a typed security/noise analysis;
- a cross-diagonal operator outside the authors' per-diagonal 2n-switch model;
- new source evidence revealing an unexploited structure not represented by q_g=s*g(s);
- a materially different workload/objective where the present lower-bound model is irrelevant.

Do NOT reopen for caching, streaming, lazy materialization, shared linear rebase, or mixed linear product-key bases.

## End of bounded probe

TRACK_ID: PURE-FHE
STATUS: FAIL_LINEAR_PRODUCT_TYPED_KSK_COMPRESSION / PASS_MODEL_SPECIFIC_INVERSION_ORBIT_LOWER_BOUND / GL_BIGSWITCH_PARK
LATEST_COMPLETED: P0-PRESCOUT-54
NEXT_ITERATION: P0-PRESCOUT-55 NOT_STARTED
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO

RESULT:
- Fresh-error-after-product direct switching forces product-secret key plaintexts q_g=s*g(s).
- Public Galois action maps q_g only within inversion pair {g,g^-1}.
- With one direct product-key contribution per diagonal, at least one stored product key per inversion orbit is required.
- For cyclic even H this is n/2+1, exactly PairSwitch's public product-key count.
- The last natural GL compression candidate therefore fails in the intended 2n-switch model.

NEXT:
Pivot away from GL BigSwitch. The next PURE-FHE problem selection should prioritize a different main-complexity operator, not another evaluation-key caching/compression variant.
