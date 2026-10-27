# PURE-FHE P0-PRESCOUT-59 — Projected RDK Admissibility and Reset Lower Bound

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
ITERATION: P0-PRESCOUT-59
LATEST_COMPLETED: P0-PRESCOUT-59
NEXT_ITERATION: NOT_STARTED / HUMAN_REVIEW
STATUS: PASS_WEAK_LOCAL_KEYSWITCH_ADMISSIBILITY / PASS_PROJECTED_RESET_LOWER_BOUND / FAIL_CHEAP_THEOREM7_REPROOF / RDK_LINE_PARK
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO
STATE_UPDATE: YES — isolated PURE-FHE finding only. Root STATE.md and all other tracks unchanged.

## Scope

P0-58 established:
- a local RDK-Rescale tail only needs dropped-prime residue regularity;
- but that residue-only refresh does not recover the full post-Rescale freshness used by RDK-CKKS Theorem 7 to reuse ModDown RDKs.

P0-59 asks one narrow question:

Can Theorem 7 be reproved under a substantially weaker post-Rescale freshness invariant, weak enough that a 23/25/40-bit residue refresh retains the communication advantage?

Answer:
- YES, the operation-local KeySwitch condition can be weakened substantially;
- NO, the generic cross-iteration reset still needs randomness at the future ModDown projection scale, which in the source parameters is about 488 bits per coefficient.

Thus the cheap residue-only route remains closed.

## Primary source

Taeyeong Noh, Aimad Chabounia, Guillaume Hanrot, Alain Passelègue,
"RDK-CKKS: A Framework for Rigorous Error Analysis for CKKS Computation,"
ePrint 2026/2575, revision 2026-10-21.

Verified full PDF through the current eprint.iacr.asia mirror.

Important source facts:

1. Definition 2:
   - Rescale admissibility requires rdk independent of (b,a).
   - KeySwitch admissibility requires rdk independent of (a,swk).

2. Theorem 3:
   For KeySwitch, after defining
     A' = A_rdk + C_A,
     B' = B_rdk + C_B,
   the proof uses:
   - A',B' uniform over R_{PQ};
   - rounding residues [A'/P]_1,[B'/P]_1 for the two probabilistic rounding terms;
   - a separate Gaussian tail for E_rdk;
   - deterministic worst-case bounds on decomposition digits a_i;
   - a union bound, not independence between the A' and B' rounding terms.

3. Theorem 7:
   After multiplication, d1=ab'+a'b moves dependence from historical b-parts into the a-part.
   A fresh RDK-Rescale is then used to make the output a-part uniform and independent of everything sampled before.

4. Concrete source parameters:
   N=2^16.
   Table 2:
     Base 35,
     StC 23 x3,
     Mult 30 x20,
     EvalMod 40 x10,
     CtS 25 x3,
     P 61 x8,
     Total 1667.
   Therefore the auxiliary KeySwitch modulus has
     log2 P approximately 8*61 = 488 bits.

5. Table 3:
   shared ModDown RDK size =1788 MB;
   fresh per-invocation Rescale RDK size =518 MB.

## 1. Local KeySwitch admissibility can be weakened

Write one RDK as

  rdk=(B_0,A_0),
  B_0=-A_0 s + E_0    mod PQ,

and write the deterministic/current-state KeySwitch accumulations as

  C_A = sum_i a_i A_swk^(i),
  C_B = sum_i a_i B_swk^(i).

Then

  A' = A_0 + C_A,
  B' = B_0 + C_B.

Theorem 3's local rounding terms depend only on

  [A'/P]_1 and [B'/P]_1,

i.e. only on the coefficient residues of A',B' modulo P.

### [DERIVATION] Residue-mask sufficient condition

Let

  R := A_0 mod P.

Suppose, conditioned on the current KeySwitch state,
  R is coefficient-wise uniform over R_P
and is independent of

  (C_A mod P, C_B mod P, E_0 mod P).

No condition is imposed on the quotient part of A_0 modulo Q.

Then:

  A' mod P = R + C_A mod P

is uniform coefficient-wise.

Also

  B' mod P
    = -R s + E_0 + C_B mod P.

Since s is invertible modulo P, for every fixed (E_0,C_B), the map

  R -> -R s + E_0 + C_B

is a bijection of R_P.

Hence B' mod P is also coefficient-wise uniform.

A' and B' need NOT be mutually independent: Theorem 3 bounds their two rounding terms separately and combines them by union bound.

Therefore full uniformity of A',B' over R_{PQ} is stronger than what the LOCAL rounding tail requires.

## 2. The RDK error term need not be freshly independent for every reuse

Theorem 3 treats DFT(E_rdk) as a separate Gaussian-tail event.

For a reused RDK, one can instead define at key generation a global good event

  G_E := {|DFT(E_rdk)_k| <= T_E for all required slots/keys}.

Condition on G_E thereafter.

Then the RDK-error contribution is bounded deterministically for every reuse of that same key.

This avoids requiring a fresh conditional Gaussian law after the computation has become correlated with E_rdk.

Likewise the source already treats the decomposition digits a_i by deterministic worst-case bounds, so no fresh independence from switching-key errors is needed for those weights.

Hence a weaker operation-local theorem is plausible:

**Projected / rounding admissibility.**
A reused KeySwitch RDK is locally tail-admissible if its low-P mask residue remains uniform relative to the current pre-ModDown accumulation residues, while its fixed error polynomial satisfies one globally budgeted good event.

This is strictly weaker than Definition 2.

## 3. Why this does not yet reprove Theorem 7

Theorem 7 is not only a local-tail theorem. It is a propagation theorem guaranteeing that later reused keys remain admissible.

Across iterations:
- a fresh input mask resets the input a-part;
- the b-part still carries historical computation error;
- that historical error contains previous RDK rounding residues;
- at a ciphertext-ciphertext multiplication,
    d1=ab'+a'b
  moves this dependence into the new a-part.

Thus before a future reuse of rdk_j, the current KeySwitch accumulation may be correlated with the low-P state of rdk_j.

The weaker local theorem therefore changes the required reset target:

one no longer needs to erase dependence on the whole future RDK,
but one MUST erase dependence relevant to the future pre-ModDown residues modulo P.

This is the **projected freshness invariant**.

## 4. Generic projected reset lower bound

Let H be any finite abelian group representing a future projection of the ciphertext state, and let Z denote hidden/shared-key information.

Suppose X=f(Z) can be an arbitrary H-valued dependence.

Let U be an independent additive refresh and define

  Y=X+U.

Claim:

If Y is independent of Z for every distribution of Z and every function f, then U must be uniform over H.

### Proof

Choose any h in H and let Z be uniform over {0,1}, with

  X=0 if Z=0,
  X=h if Z=1.

Independence Y ⟂ Z implies

  Law(U)=Law(h+U).

Since h is arbitrary, the law of U is invariant under all translations of H.

The unique translation-invariant probability distribution on a finite group is uniform.

QED.

### Interpretation

Full R_Q uniformity is NOT universally necessary.

But for whatever projected state H one decides to protect, a black-box additive reset against arbitrary hidden dependence must contain a uniform one-time pad over H.

To beat this lower bound one must prove that the actual CKKS multiplication-induced dependence is restricted to a much smaller structured subset; a generic weaker-invariant argument is insufficient.

## 5. What is the natural H for RDK-CKKS reuse?

For a future RDK-KeySwitch, the rigorous rounding terms are

  [A'/P]_1,
  [B'/P]_1.

Therefore the natural protected projection is at least the pre-ModDown residue space modulo the auxiliary modulus P.

In the source binary-bootstrap parameters,

  P = product of eight approximately 61-bit primes,

so

  log2 P approximately 488 bits.

Thus the first meaningful weakening of Theorem 7 is not:

  full Q freshness -> current dropped q freshness (23/25/40 bits),

but rather:

  full Q freshness -> future ModDown P-projected freshness (~488 bits).

This destroys the main attraction of P0-58's residue-only idea.

## 6. Entropy / synthesis sanity gate

Suppose one tries to realize the projected refresh using public RLWE encryptions of zero plus fresh short ring selectors.

A necessary information-theoretic condition for statistical closeness to uniform over one R_P ring element is that the selector randomness carry roughly

  N log2 P approximately 488 N

bits of entropy before the security slack.

Using the same P0-58 synthesized-error proxy

  sigma_eff approximately sigma_e sigma_x sqrt(mN),
  alpha_eff approximately 2 sqrt(3) sigma_eff / q,

with:
  sigma_e=3.2,
  N=2^16,

and requiring alpha_eff <=10 as only a permissive magnitude gate:

- at q about 2^23, the bare entropy floor requires roughly >=41 selector polynomials;
- at q about 2^25, roughly >=35;
- at q about 2^40, roughly >=17.

These are BARE entropy floors only, not sufficient ring-LHL parameters.

The current EUROCRYPT-2026 cyclotomic LHL shows that fully-splitting rings require additional statistical slack. Extrapolating the same 2^-128-scale fully-splitting slack used in P0-58 raises representative counts to roughly:
- ~66 at 23-bit rescale levels,
- ~56 at 25-bit levels,
- ~27 at 40-bit levels,

under the same permissive alpha_eff<=10 proxy.

Because the theorem in ePrint 2025/1080 is stated cleanly for prime moduli, these composite-P numbers are a sanity extrapolation, NOT a formal instantiation.

## 7. Cost implication

Table 3's largest fresh Rescale RDK is about 47 MB.

A projected-refresh public basis needing even the bare 35-sample floor would correspond to about

  35 * 47 MB ~=1.65 GB

of top-level RLWE-zero material if instantiated naively at that level.

A 50-60 sample statistical extractor would be several GB.

Such a basis could in principle be amortized across many invocations and perhaps reduced/truncated across levels, so this is not an impossibility theorem.

However online synthesis would also require dozens of ring multiplications per fresh Rescale, and the attractive source problem was only 518 MB of fresh Rescale RDK material per additional invocation.

Thus the projected-refresh route no longer passes the cheap value gate.

## 8. What this round actually proves

### Positive

The source's KeySwitch Definition-2 admissibility condition is not locally minimal.

For the local Theorem-3 error tail, it is enough to guarantee:
- low-P residue regularity of the RDK mask relative to the current accumulation;
- a globally budgeted bound on the fixed RDK error.

Full R_{PQ} independence is primarily useful for clean propagation/reuse proofs.

### Negative

Theorem 7 cannot generically be rescued by replacing full post-Rescale freshness with only the current 23/25/40-bit dropped-prime residue freshness.

The minimal source-visible projection relevant to future reused ModDown keys is already P-scale, about 488 bits per coefficient in the concrete parameter set.

A generic additive reset on that projection must be uniform there.

Therefore the cheap residue-only communication advantage is lost before implementation.

## 9. Remaining escape hatch

The only technically meaningful way to reopen the RDK line is to prove a CIRCUIT-SPECIFIC structure theorem:

After multiplication in the concrete binary-bootstrap circuit, the dependence of the next KeySwitch accumulations on previously reused RDKs lies in a subgroup, submodule, low-rank image, or bounded-entropy set H_small with

  log |H_small| << N log P.

Only then could a projected refresh substantially smaller than 488 bits/coeff defeat the generic reset lower bound.

No such structure has been identified in this round.

Do NOT reopen for:
- generic public Enc(0) rerandomization;
- current-q residue-only refresh;
- full-modulus LHL synthesis;
- cache/streaming tricks;
- parameter micro-tuning.

## Novelty

NOVELTY: NOT_ESTABLISHED.

Potentially reusable derivations:
1. separation of local KeySwitch rounding admissibility from global propagation freshness;
2. a mask-residue sufficient condition for Theorem-3-style local tails;
3. projected one-time-pad lower bound showing the cost of a generic weaker Theorem-7 reset.

These are not claimed as new literature results without a broader proof/prior-art audit.

## End of Iteration

TRACK_ID: PURE-FHE
ITERATION: P0-PRESCOUT-59

STATUS:
PASS_WEAK_LOCAL_KEYSWITCH_ADMISSIBILITY /
PASS_PROJECTED_RESET_LOWER_BOUND /
FAIL_CHEAP_THEOREM7_REPROOF /
RDK_LINE_PARK /
HUMAN_REVIEW.

RESULT:
- Theorem 3 local tail can be supported under weaker, residue-level conditions than Definition 2.
- This does not preserve the P0-58 cheap-residue idea across repeated evaluations.
- Generic cross-iteration refresh must target at least the future ModDown P-projection.
- In the source parameters P is about 488 bits/coeff, making public projected synthesis a multi-GB / dozens-of-ring-products route rather than a cheap replacement.
- No native implementation is warranted.

CODEX_REQUIRED:
NO.

NEXT:
Do not automatically launch P0-60 on RDK.
PARK the RDK line.
Return to problem-level PURE-FHE reselection.
Only reopen RDK if a concrete circuit-specific low-rank/submodule dependence after multiplication is found from primary source or a new derivation.

STATE_UPDATE:
YES — this finding only.
