# PURE-FHE P0-PRESCOUT-58 — RDK-CKKS Residue-Only Refresh vs Reuse Invariant

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
ITERATION: P0-PRESCOUT-58
LATEST_COMPLETED: P0-PRESCOUT-58
NEXT_ITERATION: NOT_STARTED / HUMAN_REVIEW
STATUS: PASS_RESIDUE_ONLY_ROUNDING_LEMMA / FAIL_SHARED_RDK_REUSE_INVARIANT / KILL_SIMPLE_RESIDUE_ONLY_RDK_REPLACEMENT / PARK_FULL_SYNTHESIZED_RDK
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO
STATE_UPDATE: YES — isolated PURE-FHE finding only. Root STATE.md and all other tracks unchanged.

## 1. Problem selected after P0-57

The strongest source-defined PURE-FHE bottleneck found in the bounded reselection was RDK-CKKS:

Taeyeong Noh, Aimad Chabounia, Guillaume Hanrot, Alain Passelègue,
"RDK-CKKS: A Framework for Rigorous Error Analysis for CKKS Computation,"
ePrint 2026/2575, revision 2026-10-21.

The paper obtains rigorous CKKS rounding tails by adding secret-key-generated RLWE encryptions of zero (RDKs) immediately before Rescale and ModDown.

For its binary-bootstrap parameter set:
- N = 2^16, sigma = 3.2, h = 1024;
- total switching-key material = 6540 MB;
- shared ModDown RDKs = 1788 MB = 27.3% of SWK;
- fresh Rescale RDKs = 518 MB per additional invocation = 7.9% of SWK.

The paper proves that ModDown RDKs can be reused across sequential circuit evaluations, but Rescale RDKs must remain fresh.

This is a real asymptotic-in-number-of-evaluations key-material term, not a kernel micro-optimization.

## 2. Prior-art gate

Generic public rerandomization from encryptions of zero is NOT novel.

Ducas–Stehlé, EUROCRYPT 2016 / ePrint 2016/164, already put O(n log q) encryptions of zero in the public key and use random {-1,0,1} combinations plus a leftover-hash argument to make the LWE mask statistically close to uniform.

Bourse–Izabachène, ePrint 2022/1438, explicitly discuss this LHL route as expensive and give a computational alternative using one encryption of zero multiplied by a fresh Gaussian vector, relying on decision-RLWE.

Therefore:
- "public Enc(0) basis + random linear combination" is prior art;
- any possible contribution must come from an RDK-CKKS-specific weakening/invariant, not the generic rerandomization mechanism.

## 3. Smallest hypothesis H58

H58:

For an RDK-Rescale from modulus qQ to Q, replace the fresh full-modulus RDK by a reusable public RLWE-zero basis and fresh short ring selectors that synthesize a randomizer whose two components are statistically close to uniform only modulo the dropped prime q.

Claim to test:

This residue-only randomization is sufficient both
1. for the rigorous RDK-Rescale rounding tail, and
2. to preserve Theorem 7's reuse of the shared ModDown RDKs.

The first part is true; the second part is false.

## 4. PASS — residue-only uniformity is enough for the local Rescale tail

Theorem 2 writes the Rescale error using

  [a'/q]_1 and [b'/q]_1,

coefficient-wise.

These centered modulo-1 rounding residues depend only on

  a' mod q and b' mod q,

not on the quotient modulo Q.

The proof then applies bounded-uniform Fourier concentration separately to the a and b rounding residues and combines the terms by a union bound; mutual independence between the two terms is not required.

Hence full uniformity of a',b' over R_{qQ} is a stronger sufficient condition than the local tail proof needs.

A source-faithful weakening is:

If a' mod q and b' mod q are independently-from-input marginal distributions statistically epsilon-close to coefficient-wise uniform modulo q, then the same RDK-Rescale rounding-tail argument can be recovered with the corresponding additive statistical loss.

Call this the **residue-only rounding lemma**.

This is a derivation, not a theorem claimed by the source.

## 5. Current ring-LHL parameter gate

The relevant modern source is:

Katharina Boudgoust, Oleksandra Lapiha,
"Leftover Hash Lemma(s) Over Cyclotomic Rings,"
ePrint 2025/1080 / EUROCRYPT 2026.

For a fully splitting CKKS prime and m discrete-Gaussian ring selectors of width sigma_x, its counting-style discrete-Gaussian corollary specializes approximately to

  SD <= 1/sqrt(2) * sqrt((1 + q / sigma_x^m)^N - 1)

for one output ring element.

For N=2^16 and a target extractor distance around 2^-136, the small-term condition is roughly

  m log2(sigma_x) >= log2(q) + 287.

This corrects and kills the earlier naive idea that m=2 and sigma_x≈sqrt(q) would suffice.

Using only a noise-magnitude proxy for the synthesized zero-encryption error,

  sigma_eff ≈ sigma_e sigma_x sqrt(mN),
  alpha_eff ≈ 2sqrt(3) sigma_eff / q,

with sigma_e=3.2, the residue-only extractor is not immediately impossible.

Representative minimum m values while keeping alpha_eff approximately <=10 are:
- q≈2^23: m≈25;
- q≈2^25: m≈22;
- q≈2^40: m≈11.

These are only a magnitude gate, not a rigorous product-tail proof.

Thus ring-LHL cost alone does not kill residue-only refresh.

## 6. Decisive killer — Theorem 7 needs full output-space refresh

RDK-CKKS Theorem 7 proves that ModDown RDKs may be shared across repeated evaluations.

Its induction tracks independence from future shared keys.

The source explicitly identifies the difficult case:
after ciphertext-ciphertext multiplication, the a-part contains

  d1 = a b' + a' b.

The b-parts carry errors depending on RDKs used in previous iterations, including keys that will be reused later. Therefore the required independence is lost at this point.

The source repairs the induction by the immediately following fresh RDK-Rescale:

  the a-part of the multiplication output becomes uniform over R_Q
  and independent of everything sampled before.

That full R_Q reset is the step that allows the induction for the next shared ModDown RDK to continue.

### Scalar counterexample to residue-only reset

Take one coefficient and let the pre-rescale a-part be

  a = q K

for a structured/random variable K in Z_Q.

Let a residue-only randomizer A satisfy

  A mod q ~ Uniform(Z_q),

but carry no full-Q quotient randomness; for example choose A from a centered representative interval of one q-residue class system.

Then

  round((a+A)/q) mod Q
    = K + round(A/q) mod Q.

The second term has only a tiny constant-size support.

Therefore the output retains essentially all dependence on K and is not uniform over Z_Q.

The same argument coefficient-wise shows:

  A mod q uniform

does NOT imply

  round((a+A)/q) mod Q uniform or independent of the previous computation.

So residue-only refresh is enough for the CURRENT rounding tail but not for the NEXT reuse invariant.

## 7. Consequence

The simple construction

  "replace only the fresh Rescale RDKs by residue-only synthesized randomizers,
   while keeping the paper's shared ModDown RDKs and Theorem-7 proof"

is invalid.

STATUS:

  FAIL_SHARED_RDK_REUSE_INVARIANT.

This is a structural algebra/statistics failure, not a parameter miss.

## 8. Could full-modulus synthesized RDKs repair it?

Possibly in principle, but this is a different and much more expensive construction.

To restore the exact Theorem-7 invariant, the synthesized randomizer must make the post-rescale quotient close to uniform over R_Q, which naturally pushes the extractor target back toward the full working modulus qQ rather than only the 23/25/40-bit dropped prime.

The paper's top binary-bootstrap modulus chain totals 1667 bits. With the same fully-splitting LHL scaling, a full-modulus extractor would need roughly

  m log2(sigma_x) >= log2(qQ) + 287.

Under the same alpha_eff<=10 magnitude constraint and a 25-bit dropped prime, a 1667-bit target needs on the order of 148 ring-selector samples.

At the top level, one RDK is about 47 MB in the paper's table, so a naive full-modulus reusable basis would be on the order of several GB (about 7 GB for 148 top-level samples) before online synthesis cost.

This does not prove impossibility:
- the basis could amortize over many circuit invocations;
- tighter structured extractors might exist;
- a different proof invariant could avoid full post-rescale uniformity.

But it is no longer the cheap 518-MB-per-invocation elimination suggested by residue-only refresh.

It therefore fails the current cheapest-value gate and is PARKED rather than promoted.

## 9. Security-model boundary

RDK-CKKS itself states that its proof samples RDKs on the challenger side and does not establish security against an adversary who holds the RDKs, such as the evaluator.

Public rerandomizer synthesis does not automatically repair that issue.

Generic public rerandomization is old, and evaluator-selected rerandomization may create new correlations. A current warning is ePrint 2026/2546, "New IND-CPA-D Attacks on BFV and BGV": its public abstract includes an attack that selects an encryption of zero to skew a ciphertext mask. The full PDF was SOURCE_BLOCKED in this session, and the attack is on BFV/BGV, not CKKS, so no stronger transfer claim is made.

Therefore separate:
- Layer A: rigorous error-tail / communication optimization;
- Layer B: security against an evaluator holding or selecting randomization material.

P0-58 establishes neither Layer-B security nor a new IND-CPAD theorem.

## 10. Novelty judgment

NOVELTY: NOT_ESTABLISHED.

Not novel:
- public encryptions of zero for rerandomization;
- LHL-based statistical rerandomization;
- Gaussian-selector computational rerandomization.

Potentially reusable/new derivation:
- the RDK-Rescale local tail only consumes dropped-prime residues;
- residue-only regularity is therefore sufficient for the local rounding bound;
- but full output-space randomization is independently required by the paper's cross-iteration RDK-reuse invariant.

This separation between **local rounding regularity** and **global reuse freshness** is the main technical result of P0-58.

## End of Iteration

TRACK_ID: PURE-FHE
ITERATION: P0-PRESCOUT-58

STATUS:
PASS_RESIDUE_ONLY_ROUNDING_LEMMA /
FAIL_SHARED_RDK_REUSE_INVARIANT /
KILL_SIMPLE_RESIDUE_ONLY_RDK_REPLACEMENT /
PARK_FULL_SYNTHESIZED_RDK /
HUMAN_REVIEW.

RESULT:
- RDK-CKKS is a high-value source-defined bottleneck because per-invocation Rescale RDK material grows linearly with repeated evaluations.
- Generic public rerandomization is strong prior art.
- Dropped-prime residue uniformity is sufficient for the local Rescale tail.
- It is not sufficient to recover the full R_Q uniformity/independence reset that Theorem 7 uses to share ModDown RDKs.
- The simple 518-MB-per-invocation replacement is therefore killed.
- Full-modulus synthesized RDKs remain only a parked, much heavier possibility.
- No implementation is warranted.

CODEX_REQUIRED:
NO.

NEXT:
Do not launch a native implementation.
Do not automatically expand to a full public-rerandomizer framework.
At HUMAN_REVIEW, either:
1. reselect another PURE-FHE core bottleneck, or
2. only if explicitly prioritized, investigate whether Theorem 7 can be reproved under a weaker post-rescale invariant than full R_Q uniformity. That would be the only route that preserves the residue-only communication advantage.

STATE_UPDATE:
YES — this finding only.
