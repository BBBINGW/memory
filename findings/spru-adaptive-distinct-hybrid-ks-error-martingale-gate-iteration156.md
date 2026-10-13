# Iteration 156 — Adaptively generated switching digits do not alone destroy conditional orthogonality of independent centered distinct-key KS errors

Date: 2026-10-13. User “好的，请继续” followed previous source-blocked I155/I156 vFHE effort and offer to select another OPEN branch, interpreted as permission to select a different executable FHE target. Selected the existing **SPRU single-slot CKKS Trace noise** open issue, not missing-source MRFHE or archived vFHE code repairs. ONE hypothesis / ONE decisive toy + tower-property derivation. Prior I147 and I145/146 read before test. No source bug, actual CKKS precision run, official PDF validation, or performance claim.

## Source anchors

- Coron and Köstler, *Low-Latency Bootstrapping for CKKS using Roots of Unity*, ePrint 2025/651, 42-physical-page Research MCP PDF, SHA256 `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6`, source_kind github-mirror and official version **VERSION_UNVERIFIED**. §3.4/3.5 physical pp11–12: `Rot(ct,r)=KS_{rk_r}(Psi_r(ct))`; unnormalized Trace uses `log2(N/(2h))` rotations, sequential additions. Paper's Lemma 5 on p11 explicitly includes rounded switching `floor(P^-1*c1*swk)` and only bounds total KS noise, **not centering of its full rounded error**.
- `findings/spru-trace-distinct-rotation-evaluation-key-index-gate-iteration147.md`: original `coron/spru_boot/src/single_slot.cpp` 8 Trace shifts 8192,4096,...,64 at N32768,h64; distinct `5^r mod2N` automorphism key indices; 8 separately generated HYBRID key entries. **No reuse of same key map entry within one Trace**, though existing keys are frozen and can be reused across invocations.
- Tagged upstream **OpenFHE v1.4.2** `src/pke/lib/keyswitch/keyswitch-hybrid.cpp`, blob SHA `552fee8fc52c4ee12176e6b9a2ca279b079b7cbc`, independently re-read during I156: `KeySwitchGenInternal(oldPrivateKey,newPrivateKey,ekPrev)` per partition samples `DCRTPoly a(dug,...)` and independently `DCRTPoly e(dgg,...)` in the standard `ekPrev=nullptr` single-key branch; creates b including `ns*e`; public-private variant uses fresh `u,e0,e1`. `KeySwitchInPlace` invokes `KeySwitchCore`. `KeySwitchDown` calls `ApproxModDown`. Fresh e per generation is a **source-compatible ideal statistical assumption**, not an audited guarantee about conditioning on all publicly released evaluation-key bytes.
- I145 proves pre-Trace fixed-mask conditional canonical covariance under exact multiplication of independent centered PK encryption noises; I146 excludes immediate pre-Trace mod-reduction; **neither covers adaptive rotation-KS noise**. I147 leaves the joint conditional KS noise open.

## ONE primary hypothesis and falsifier

**[HYPOTHESIS]** In the **pre-ModDown linear additive switching-key-error model**, if each distinct rotation key contributes independent centered new key-generation errors conditional on fixed secret and earlier keys, and its switching digit decomposition is measurable with respect to earlier computation rather than that key's own secret encryption noise, **adaptive evolution of the input ciphertext alone does not induce nonzero cross-round Hermitian covariance** between distinct-key added error increments.

**[FALSIFIER / ONE TEST]** Check the martingale conditional-mean identity and an exhaustive finite-support **three-stage history-adaptive digit example**, where digit weights depend on previous key errors. Any nonzero offdiagonal expectation disproves the claim in that model. No actual OpenFHE measurement or full error formula is claimed.

## Derivation (new scoped result, not original paper theorem)

Fix the secret, long-lived public parameters, and allowed previous history `F_{j-1}`. Let `D_{j,k}` be the (possibly RNS/poly/slot-valued) digit weight **computed from prior ciphertext state** and `E_{j,k}` the current fresh switching-key encryption error. In exact linear arithmetic BEFORE `ApproxModDown`, put
```
 Z_j = sum_k D_{j,k} E_{j,k}.
```
Assume `D_{j,k}` is `F_{j-1}`-measurable, and `E[E_{j,k} | F_{j-1}] = 0` (conditional on common full secret and fixed baseline parameters), with finite second moments. It suffices that errors are **conditionally centered**; no independence among different k in one round is needed for the cross-round conclusion. Then
```
 E[Z_j | F_{j-1}] = sum_k D_{j,k} E[E_{j,k}|F_{j-1}] = 0.
 E[Z_i * conjugate(Z_j)] = 0 for i<j.
```
At each fixed slot, all upstream source-derived rotations are deterministic complex-linear coefficient maps; in a strictly **linear, no-rounding error propagation** model this is a martingale-difference/orthogonality argument. It does NOT imply the Z_j are independent or identically distributed, nor bound their conditional variances or maxima.

## Exactly enumerated minimal test

Sample `e1,e2,e3` independently, each uniformly from {-1,+1}, and define
```
 Z1=e1;
 Z2=(1+e1)*e2;
 Z3=(1+e1*e2)*e3.
```
Enumerating ALL 2^3=8 sign assignments in functions JavaScript gives:
```
 means (Z1,Z2,Z3)              = (0,0,0)
 E[Z1 Z2], E[Z1 Z3], E[Z2 Z3]  = (0,0,0)
 E[Z1^2], E[Z2^2], E[Z3^2]      = (1,2,2).
```
Here input weights of round 2 and 3 adapt to earlier errors; Z1 and Z2 are **not independent** (when Z1=-1, Z2 always0; when Z1=+1, Z2=±2), yet are uncorrelated. Numeric test is a model-level sanity check; general claim is proved by the tower law, not by eight samples.

## Interpretation and explicit blockers

**[PASS / MATHEMATICAL MODEL]** Input-digit adaptivity **by itself** is not sufficient to refute a probabilistic `sqrt(sum of variances)` improvement for source single-invocation Trace *fresh errors from distinct rotation-key generations*. Distinct key map entries I147 plus fresh conditional centering are plausible premises for one narrow subterm. An earlier suggestion that arbitrary ciphertext adaptivity automatically implies nonzero covariance is too strong.

**[LIMITS]**
1. **Actual source KeySwitchDown/ApproxModDown** and integer rounding can contribute noncentered/data-dependent error; key switching is executed modulo finite CRT primes, and canonical CKKS decryption error may not be a centered exact linear image of primitive `e`. This round does not check the exact conditional bias of `ApproxModDown`.
2. Public eval keys are disclosed as a whole, so a caller/adversary choosing ciphertexts based on the **current** key cannot use the history-only measurability premise; nonadaptive honest execution and adversarial chosen ciphertext are distinct models.
3. A single original fixed eval key **is reused across different bootstrap invocations**. Fresh per-key error does not mean fresh per EvalRotate call.
4. Current source-input decomposition and future stages depend on past results; variance terms remain heteroscedastic. No claim that arbitrary downstream **nonlinear** rescaling, rounding, Ct×Ct product, and SlotsToCoeffs preserve zero cross-covariance, no actual FHE precision/security/performance result, no paper error or novelty claim.
5. The algebra is standard martingale orthogonality and alone is **not publishable**; source-relevant verification must locate the exact rounded HYBRID switching error decomposition and current-key dependence.

## End of I156

**STATUS:** **PASS** for precisely conditioned **pre-ModDown, linear new-key-noise** martingale claim; **UNCLEAR** for complete SPRU HYBRID key switching/CKKS precision.
**RESULT:** Source checks eight distinct rotation key indices and fresh separately generated e for each key; adaptively chosen digits from **earlier** errors remain predictable, so independent conditional centered new-key errors can have zero cross-round Hermitian covariance. Exhaustive 8-case history-adaptive example confirms; no numerical precision bound.
**NEXT_ACTION:** If PI continues SPRU, audit **one** tagged OpenFHE v1.4.2 `KeySwitchDown→ApproxModDown` rounding term and its **conditional bias** given input digit state/previous keys in a minimal exact scalar RNS toy, to learn whether full HYBRID error is still a martingale difference (or needs an explicit bias+martingale decomposition). Do NOT rerun the I147 key index test, I145 exact pre-Trace fixed-mask covariance, or claim whole system noise `sqrt(L)` yet.
**STATE_UPDATE:** **YES** — PI-authorized research branch pivot from source-blocked P1 to SPRU, new narrow model-level result and a precise next necessary real-source gate. P1 vFHE remains OPEN/HUMAN_REVIEW/SOURCE-GATED; I152–154 integers still PARKED.
