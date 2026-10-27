# PURE-FHE — Post-P0-54 Cross-Diagonal Shared Rebase = TFB Gate

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
LATEST_COMPLETED: P0-PRESCOUT-54
NEXT_ITERATION: P0-PRESCOUT-55 NOT_STARTED
STATUS: FAIL_SHARED_CROSS_DIAGONAL_REBASE_NOVELTY / PASS_ALGEBRAIC_EQUIVALENCE_TO_TFB_NOISE_FORM / HUMAN_REVIEW
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO
STATE_UPDATE: YES — isolated PURE-FHE finding only. Root STATE.md and all other tracks unchanged.

## Scope

This is NOT P0-PRESCOUT-55.

It tests only the bounded question left after the previous PairSwitch linear-rebasing gate:

Can several Galois-split BigSwitch diagonals share one rebase/relinearization, so that the product-secret functionality s*g(s) is recovered with one global rebase instead of materialized PairSwitch product keys, while preserving the fast path and avoiding TFB's noise penalty?

No native implementation, Codex, GPU/server work, or cross-track write was performed.

## Source facts

### [FACT] Original GL matrix-FHE BigSwitch structure
Gentry–Lee, "Fully Homomorphic Encryption for Matrix Arithmetic", ePrint 2025/1935, cached title-verified mirror PDF SHA256
985173da6bc45f1c89c86769d5b6b16bfcdd98bf07e91476cd424778b8d9ec84
VERSION_UNVERIFIED.

Physical pp.15–16 give the exact 4-component product:
  ct(u) tensor ct(v) = (d0,d1,d2,d3)
with decryption secret tuple
  (1, s(X,W), s(Y^-1,W^-1), s(X,W)s(Y^-1,W^-1)).

Relinearization outputs:
  (d0,d1)
  + Switchbig(d2, K_{s(Y^-1,W^-1) -> s})
  + Switchbig(d3, K_{s(X,W)s(Y^-1,W^-1) -> s}).

Thus the entire product-secret contribution is one linear Switchbig term added into one final ordinary ciphertext.

Physical p.10 defines Switchbig as an ordinary linear gadget/key-switch operation over the extended ring.

### [FACT] PairSwitch current public abstract
ePrint 2026/2373, last-updated 2026-10-06.

The current public abstract states:
- Galois splitting decomposes BigSwitch into base-ring diagonals.
- pair-merge uses n/2+1 product keys while retaining the original 2n key switches.
- the diagonal target admits
    x*g(s) + y*s*g(s)
      = g( g^-1(x)*s + g^-1(y)*s*g^-1(s) ),
  allowing a diagonal to borrow its inverse partner's product key at one Galois step.
- TFB halves keys but pays 50% more key switches and "a whole switching error multiplied by the secret".
- PairSwitch public rebasing turns Galois keys into product keys using one relinearization key, trading TFB-scale client publication for about 1.5x TFB server-resident keys.

Full PairSwitch PDF remains SOURCE_BLOCKED in the current acquisition path.

## [DERIVATION] Shared cross-diagonal rebase is algebraically possible

Let G be the set of Galois-split diagonals contributing to the product-secret BigSwitch term.

For each g in G, let the runtime data-dependent coefficient/operator contribution before multiplying by the destination secret be y_g, and let a compact Galois-key switch produce a ciphertext whose phase is

  m_g = y_g * g(s) + e_g,

where e_g is the switching error contributed by this compact switch.

Because all diagonal contributions ultimately add into the SINGLE product-secret Switchbig contribution of the original GL BigSwitch, one may sum them before rebasing:

  C = sum_g C_g

with phase

  M = sum_g y_g g(s) + E,
  E = sum_g e_g.

Now apply one shared public rebase/relinearization R_s whose plaintext functionality is multiplication by s followed by ordinary relinearization back to secret s.

By ciphertext linearity,

  R_s(C)

has target phase

  s * sum_g y_g g(s)

and noise contribution

  s * E + e_R,

where e_R is the relinearization/rebase noise.

Therefore a single shared cross-diagonal rebase is TYPE-CORRECT. Output independence is not the blocker: the diagonals are not required to remain separately decryptable, because BigSwitch sums them into one ordinary ciphertext anyway.

This corrects the initial speculative concern that Galois labels alone might forbid sharing.

## [DERIVATION] But the shared construction is exactly the TFB noise placement

The crucial term is

  s * E.

All compact-key switching errors are accumulated FIRST, and only then multiplied by the secret by the shared rebase.

This is precisely the noise placement described by the PairSwitch abstract for TFB:
  "a whole switching error multiplied by the secret."

The structural comparison is:

### Pre-rebased/product-key route (Original / PairSwitch side)

For each diagonal, use a key whose plaintext source already contains s*g(s):

  C'_g = Enc_s( y_g s g(s) + e'_g ).

Summing gives

  sum_g y_g s g(s) + sum_g e'_g.

The switch error is injected AFTER the secret multiplication has been baked into the key plaintext. There is no global secret multiplication of the accumulated switching error.

### Shared-lazy route (TFB side)

First switch the g(s) contributions:

  sum_g y_g g(s) + E,

then multiply/relinearize once:

  s * sum_g y_g g(s) + sE + e_R.

The exact target is the same, but the entire prior switching error E is multiplied by s.

Hence cross-diagonal sharing does not create a new point between TFB and PairSwitch. It lands on the TFB side of the same memory/time/noise trade-off.

## [DERIVATION] Why "one global shared rebase" does not rescue novelty

One might hope that PairSwitch's rebasing is per diagonal while a single global rebase is new.

However the original GL BigSwitch formula already shows that all product-secret diagonal pieces are merely a decomposition of one linear Switchbig(d3, K_product) contribution. Once the product secret is factored as "compact source first, multiply by s later", all of those pieces can indeed be accumulated before the later multiplication/relinearization.

That is exactly the rank-one/factored design space that TFB occupies.

Therefore:
- YES, the rebase can be shared across diagonals;
- NO, this sharing is not a new mechanism;
- its noise signature s*E is the defining TFB penalty that PairSwitch explicitly sets out to avoid by precomputing/rebasing product keys.

## Relation to FRee-L

The TFB public abstract further states that FRee-L delays recurring post-processing across K Trace products and invokes the expensive cleanup only once per output tile, making the TFB side even more explicitly an amortized "accumulate first, relinearize later" design.

Thus a PURE-FHE proposal whose only contribution is "share one relinearization across many diagonal/product contributions" is even closer to known TFB/FRee-L structure.

No exact FRee-L theorem/algorithm is claimed here because the 2026/2058 full PDF remains blocked.

## What remains outside this gate?

A genuinely new candidate must avoid the s*E penalty WITHOUT simply storing the fully rebased product keys.

That requires at least one of:

1. ERROR-AFTER-MULTIPLICATION FUSION
   A gadget/key representation where the secret multiplication by s is incorporated before fresh switch noise is injected, but without materializing the full product KSK.

2. SHARED DECOMPOSITION WITH PRODUCT-TYPED OUTPUT
   One decomposition of the runtime diagonal data drives a product-secret switch directly, while the stored key remains asymptotically closer to Galois-key material than PairSwitch product-key material.

3. STRUCTURED LOW-RANK PRODUCT KSK
   Compress the family {K_{s g(s)}}_g in a representation that supports direct switching and injects fresh error only after reconstructing the product-secret action, with a security/noise proof.

4. A NEW CROSS-DIAGONAL OPERATOR OUTSIDE THE PAIRSWITCH LOWER-BOUND MODEL
   Not merely per-diagonal 2n switching with fewer stored keys.

Plain shared relinearization, delayed relinearization, lazy rebasing, streaming, or cache eviction are closed by this gate.

## End of bounded probe

STATUS: FAIL_SHARED_CROSS_DIAGONAL_REBASE_NOVELTY / PASS_EXACT_TARGET / PASS_TFB_NOISE_EQUIVALENCE / HUMAN_REVIEW
LATEST_COMPLETED: P0-PRESCOUT-54
NEXT_ITERATION: P0-PRESCOUT-55 NOT_STARTED
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO

RESULT:
- Cross-diagonal shared rebase is algebraically valid.
- Because the original GL product-secret BigSwitch contribution is one final linear sum, all Galois-split diagonal contributions can be accumulated before one rebase.
- The resulting error is s*E + e_R, matching the TFB noise form explicitly described by PairSwitch.
- Therefore the proposed shared-rebase mechanism is not a post-PairSwitch new construction; it collapses to the existing TFB side of the Pareto frontier.

NEXT_TEST:
Do NOT start P0-55 from shared rebasing.
The only technically meaningful GL follow-up is now a decomposition-fused/product-typed key representation that injects switching error after the s*g(s) action WITHOUT storing PairSwitch-scale product keys.
Before formulating H55, the first mathematical gate must state an explicit KSK plaintext relation and show that its stored representation is asymptotically/ concretely smaller than PairSwitch resident product material while not algebraically reducing to TFB's "switch then multiply by s".

SOURCE_SUPPORT:
Full 2026/2373 PairSwitch and 2026/2058 TFB PDFs remain highest-value missing sources. No Codex required.
