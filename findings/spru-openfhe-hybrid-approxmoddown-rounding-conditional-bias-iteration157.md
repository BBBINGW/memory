# Iteration 157 — Tagged OpenFHE HYBRID ApproxModDown can create nonzero conditional drift from symmetric centered input noise

**Date:** 2026-10-13. Human PI authorized continuation via “好的，请继续” after I156. ONE predeclared narrow falsifiable claim, ONE source-matched exact single-P/single-Q scalar RNS toy. Not a full CKKS execution, not a proof of actual SPRU mean bias, not an attack/error against the author's scheme, no novel theorem/benchmark.

## Read-before-write / primary provenance

Read in correct order `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` (after I156 sha `2dcc3c67a901be5bde44846186038eb69550315d`), then `findings/spru-adaptive-distinct-hybrid-ks-error-martingale-gate-iteration156.md` and I147 source mapping. Previous I156 proved conditional centeredness only for **linear pre-ModDown** additive fresh-key errors, `Z_j=ΣD_{j,k}E_{j,k}`.

Primary paper: Coron–Köstler, *Low-Latency Bootstrapping for CKKS using Roots of Unity*, ePrint **2025/651**, cached 42 physical pp GitHub-mirror SHA256 `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6`, latest official version **VERSION_UNVERIFIED**. Re-read physical p11, Lemma 5: KS includes rounded approximate division by P and proves **bounded error**, not zero-conditional-mean errors or full CKKS variance reduction.

Independently read exact source via connected GitHub at tag **`openfheorg/openfhe-development@v1.4.2`**:
- `src/pke/lib/keyswitch/keyswitch-hybrid.cpp`, blob SHA `552fee8fc52c4ee12176e6b9a2ca279b079b7cbc`: `KeySwitchInPlace → KeySwitchCore → EvalFastKeySwitchCore`, and **inside EvalFastKeySwitchCore both QP components call `DCRTPoly::ApproxModDown`** (about lines 414–430). IMPORTANT CORRECTION: although `KeySwitchDown` also calls `ApproxModDown` (about lines 256–280), standard `KeySwitchInPlace` does **NOT** have `KeySwitchDown` as its intermediate call. I156's label “KeySwitchDown→ApproxModDown” was an imprecise description of actual normal in-place call path, now corrected.
- `src/core/include/lattice/hal/default/dcrtpoly-impl.h`, blob SHA `0fec66253228c4d6f36526f6f63d62c146fe39ca`: `DCRTPolyImpl::ApproxSwitchCRTBasis` about line910 and `DCRTPolyImpl::ApproxModDown` about line988. `ApproxModDown` extracts P towers, converts P-coefficient representations into Q via `ApproxSwitchCRTBasis`, then computes `(partQ-partPswitchedQ)*PInvModq` in each remaining Q tower (with CKKS `t=0`). This is **NOT** literally a user-facing call to “round to nearest”; P basis switching uses canonical nonnegative residues in its exact **one-P-prime** subcase.

## ONE primary hypothesis / falsifier

**[HYPOTHESIS TO FALSIFY]** Symmetry/mean zero of the newly sampled `E=±1` suffices to preserve **zero conditional mean after the source's `ApproxModDown` map** when the ideal input is a fixed integer multiple of auxiliary modulus P. Hence the I156 martingale difference argument might carry through the rounded map without any separate drift term.

**[FALSIFIER / ONE TEST]** In single-P, single-Q exact scalar specialization of the original source’s `ApproxSwitchCRTBasis` and `ApproxModDown` with CKKS `t=0`, take `P=5,Q=17`, fixed desired quotient `k=1`, and independent centered `E∈{-1,+1}` equiprobable. Compute exactly the two output residues and conditional mean error after subtracting k; if nonzero, kill the unconditional zero-bias extension to this operator.

## Source-exact specialized map and exact results

For one P modulus, `PHat=P/p=1`, `PHatInvModp=1` and `PHatModq=1`; thus `ApproxSwitchCRTBasis` maps **canonical residue** `x_P∈{0,1,2,3,4}` into the Q tower without changing its chosen representative (here x_P<Q). Consequently, with `PInvModq=7` for `P=5,Q=17`, source `ApproxModDown` is:
```
 down(x) = ((x mod 17) - ((x mod 5) mod 17)) * 7 mod 17.
```
If the integer x is nonnegative and < Q, then the natural signed output coincides with the **Euclidean quotient** `floor(x/5)`, rather than the unbiased real division x/5.

Input `x=P*k+E=5+E`:
```
E  x   x mod 5  x mod 17  xP->Q  down_Q  desired k  error
-1 4       4        4        4       0       1        -1
+1 6       1        6        1       1       1         0
```
Then:
```
E[E] = 0;
E[down(5+E)-1] = (-1+0)/2 = -1/2 != 0;
Var(down(5+E)-1) = 1/4.
```
The arithmetic was executed in `functions.exec` using exact JavaScript integer modular operations and assertions, with `PInvModQ=7`; no floating approximations. Both integers 4/6 fit `[0,Q)`, so no negative-input signed-lift ambiguity is needed.

For this one toy, define `ξ=down(5+E)-1`, its predictable conditional drift `B=E[ξ|F_previous]=-1/2`, and centered residual `M=ξ-B∈{-1/2,+1/2}`. Then `E[M|F_previous]=0`; orthogonality can apply to **M**, not automatically to `ξ`. For general variables the tautological decomposition `ξ_j=B_j+M_j` with `B_j=E[ξ_j|F_{j-1}]` is always possible under integrability, but making it useful requires bounds on predictable bias and conditional second moments.

## Scope, novel fact, and strong caveats

**[FAIL precisely tested claim]** Merely centering the **input/key error** is INSUFFICIENT to guarantee that a **source-structured modular down-conversion output** has zero conditional mean. The I156 martingale argument cannot be applied to entire rounded HYBRID KS error without an additional proof or an explicit drift term. This is a basic source-specialized integer-division phenomenon, not a general theorem that actual HYBRID switching creates negative drift.

**[NOT established]** The constructed `x=Pk+E` is an **admissible scalar input to the isolated down-conversion routine**, not yet a distribution derived from the author's actual `EvalFastKeySwitchCoreExt` pairs and decryption against source secret; it has only one P and one Q prime, trivial ring coefficient, and tiny insecure toy parameters. Real OpenFHE may have multiple Q/P primes, coefficient-dependent residues, large random public a, switch decomposition, and **TWO down-converted ciphertext components whose decryption combination could cancel some biases**. We have **not** proved actual SPRU Trace 8-step noise has mean -1/2, nonzero covariance, growth linear in iterations, precision regression or parameter gain. Existing original Lemma 5 only claims norm-bound, so nothing here contradicts it. Real public evalkeys may violate I156 conditional current-key independence; no ciphertext adversary/attack was constructed.

**[NEXT NECESSARY GATE]** Reconstruct **the full two-component QP switching pair and decryption relation** of one tagged source `EvalFastKeySwitchCore` step, with valid (small) `P,Q`, secret and key-error data. ONE cheap exact test: can the isolated per-component scalar bias remain in **decrypted noise** or does the `ct0+s*ct1` combination systematically cancel it under valid key equations? If cancellation occurs, do not carry I157's isolated bias into a full-system claim. If survives, then only proceed to multi-prime source-parameter conditional bounds, no automatic `√L` claim.

## End of Iteration 157

**STATUS:** **FAIL** zero-bias-from-symmetric-error hypothesis for exact **one-P/one-Q isolated ApproxModDown**; PASS exact narrow counterexample and corrected source call path; **UNCLEAR full OpenFHE CKKS decrypted HYBRID KS noise**.
**RESULT:** `P=5,Q=17,x=5±1`: source-specialized down map outputs `0,1` with ideal quotient1, hence conditional error mean `−1/2` despite symmetric input errors. Need predictable drift `B_j` plus centered martingale `M_j` for any eventual full approximation-error analysis; full decryption bias untested.
**NEXT_ACTION:** **I158 only with PI approval:** reconstruct full `EvalFastKeySwitchCore` two-component source key equation and test whether decryption `ct0+s*ct1` cancels the isolated down-conversion bias for a valid small secret/key-error instance. Prioritize a falsifier before variance estimates or performance work.
**STATE_UPDATE:** **YES** — distinct new source-specialized obstruction to directly applying I156; archive normal in-place call path correction and define one full decryption consistency gate. P1 vFHE remains parked/source-gated, no change to author outreach policy.
