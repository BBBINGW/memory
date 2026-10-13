# FHE Research State — After Iteration 156

**Checkpoint:** 2026-10-13 · `main` · I156 completed, I157 **NOT STARTED**.
**Authority:** Compact current research recovery entry, not all history. Prior long state `logs/state-pre-session-handoff-2026-10-13-iteration151.md` (blob `7641c5eb985497ae77e9284ed9e94a5713f3222d`); backlog `findings/OPEN_RESEARCH_BRANCHES.md`. Human PI decides targets, contribution, pivots, and disclosure. Agent performs one minimal test per authorized iteration.

## CURRENT TARGET

**SPRU CKKS bootstrapping single-slot Trace — conditional key-switching error covariance (OPEN, no ACTIVE experiment).** Coron and Köstler, *Low-Latency Bootstrapping for CKKS using Roots of Unity*, ePrint **2025/651**, §3.4–3.5 physical pp11–12; Research MCP full 42pp GitHub mirror SHA256 `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6` (latest official VERSION_UNVERIFIED). Author code `coron/spru_boot`; relevant tagged upstream **OpenFHE v1.4.2**. I147 proved 8 distinct HYBRID rotation evaluation-key entries per invocation at source N32768,h64 (and 6 more distinct product keys). Open technical question is actual successive HYBRID KeySwitch **conditional noise covariance and rounding** in the Trace. This is NOT a verified source error, FHE speedup, or precision improvement.

**Previous parent target:** Cascudo et al. vFHE ePrint **2025/286**, CRT diagonal scalar-digit soundness, remains **OPEN/HUMAN_REVIEW / SOURCE-GATED**, **not resolved or invalidated**. The I59–60 mathematical ideal-PIOP mirror-backed evidence exists, but current official PDF bytes are missing; do NOT claim official latest defect or compiled attack. I152–154 fast integer-encoder repair branch PARKED after three distance failures. See `findings/vfhe-current-official-revision-identity-gate-iteration155.md` and `MISSING_SOURCES.md`. PI's “好的，请继续” after the explicitly offered choice to select another OPEN branch authorized choosing SPRU as the new executable research focus.

## LAST COMPLETED ITERATION

**I156 (2026-10-13), I157 NOT STARTED.** ONE precise hypothesis and test in `findings/spru-adaptive-distinct-hybrid-ks-error-martingale-gate-iteration156.md` (SHA `6360cc516a308865aad2f7afbfae74f5b532376a`): a **conditional, pre-ModDown, linear fresh-key error** martingale difference result despite switching-digit adaptivity to earlier noise. PASS restricted mathematical model; full OpenFHE source rounding/precision UNCLEAR.

## CURRENT QUESTION

Does the **actual** tagged OpenFHE v1.4.2 HYBRID rotation KeySwitch along SPRU Trace preserve conditional centering (or allow an explicit bounded bias+martingale decomposition) **after** `KeySwitchDown→ApproxModDown` integer/RNS rounding when each operation's input depends on earlier distinct-key computations? A source-grounded bounded conditional second moment could ultimately sharpen error analysis, but **no Table2 precision or performance improvement is established**.

## PRIMARY HYPOTHESIS

**NONE ACTIVE.** I156 [PASS conditional linear model]: fix shared secret and past keygen/computation history; for step j take `Z_j=Σ_k D_(j,k) E_(j,k)` with D predictable from earlier state and E the current centered independent key error conditional on that history, BEFORE any nonlinear `ApproxModDown`. Then `E[Z_j|F_(j-1)]=0` and all earlier-step `E[Z_i conj(Z_j)]=0` for i<j, even with adaptive digit weights. Exact exhaustive 8-case three-key sign experiment gives means and all pairwise covariances zero, variances (1,2,2). **Does not imply independence** or physical Gaussian CKKS precision; public-current-key adaptive ciphertexts need separate treatment.

## CURRENT EVIDENCE

- **[DERIVED/EXACT I156 PASS conditional]** Tower property of conditional means yields pairwise orthogonality for centered independently generated fresh-key errors with past-measurable switch digits in strictly linear/pre-rounded arithmetic. Three-stage exact toy `Z1=e1;Z2=(1+e1)e2;Z3=(1+e1e2)e3`, independent uniform signed e variables, 8-case cross moments all zero. Details `findings/spru-adaptive-distinct-hybrid-ks-error-martingale-gate-iteration156.md`.
- **[FACT source; not entire actual noise model]** Tagged `openfheorg/openfhe-development` **v1.4.2** `src/pke/lib/keyswitch/keyswitch-hybrid.cpp`, blob `552fee8fc52c4ee12176e6b9a2ca279b079b7cbc`, `KeySwitchGenInternal` creates per-part Gaussian e for each separately called single-key keygen; `KeySwitchInPlace` uses `KeySwitchCore`; **`KeySwitchDown` calls `ApproxModDown`**. Source does not imply rounded error conditionally centered. Its alternate threshold/key-reuse path `ekPrev` exists but is not the author's single-key Trace invocation.
- **[DERIVED I147]** Author `coron/spru_boot/src/single_slot.cpp` SHA `38d9fda8023ca0a06c5f4c9632802c83e4762c22`, Trace 8 shifts (8192,4096,2048,1024,512,256,128,64), distinct `5^r mod65536` key map entries for `N32768,h64`, but public frozen key bytes may be reused across separate invocations. Archive `findings/spru-trace-distinct-rotation-evaluation-key-index-gate-iteration147.md`.
- **[DERIVED I145/146]** Exact-ring pre-Trace two fresh bootkey ciphertexts with shared pk and fixed masks can exhibit spectral cross-slot orthogonality; tagged FIXEDAUTO initial `EvalMult+Add` performs no immediate rescale. Neither covers actual rotation HYBRID KS modulo rounding. `findings/spru-conditional-pretrace-pk-shared-mask-spectral-covariance-iteration145.md`; `findings/spru-openfhe-v142-fixedauto-pretrace-mul-no-rescale-gate-iteration146.md`.
- **[FACT source-paper]** ePrint 2025/651 §3.4 p11 Lemma5 bounds rounded KS error, does NOT claim conditional zero mean for full rounding; §3.5 pp11–12 unnormalized Trace uses O(log N) KS and rotations. Original Table2 N32768,h64,L256. Do not infer complete `√L=16` full-source RMS or 14bit real precision from this ideal result.
- **[PARKED]** I143 deterministic onehot trace-operator B-independent bound failed, I144 ideal Fourier identity already known, I146 initial-rescale and I147 same-key-within-single-trace shortcuts failed. Do NOT repeat these ideas. See backlog SPRU watchlist.

## MAIN OBSTRUCTION

**Full HYBRID KS after `ApproxModDown` is not a pre-rounded linear centered additive noise oracle**: RNS approximation/rounding may introduce biased, digit-dependent noise, while public evaluation-key access can violate past-measurability. Rotated errors later undergo nonlinear multiplications/rescalings and maximum-over-slots requires tails, not just second moments. Current linear martingale result is a necessary analytical layer, **NOT a sufficient CKKS error or precision proof**.

## OPEN UNCERTAINTY

Exact modular/real-value conditional mean or bias bound of one actual `ApproxModDown` rounding term; whether separate single-invocation keys' primitive noises are independent under all required conditioning; conditional variance and tails, full repeated bootstraps, actual parameters/precision; novelty and worthwhile speed/noise gain. P1 vFHE remains official-source-gated and unchanged.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION

**I157 only after user authorization.** ONE source-grounded falsifier: inspect **tagged OpenFHE v1.4.2** `KeySwitchDown→DCRTPoly::ApproxModDown` integer/RNS map (precise code path) and identify **one exact scalar toy** in the specified rounding model where a symmetric centered fresh key-error can yield nonzero conditional mean given a fixed input digit state, **or** prove the chosen exact simplified case stays centered. State what is dropped from full RNS code. If bias exists, derive `Z_j=B_j+M_j` with explicit predictable bias and centered residual before any source-grade error bound. Do not run large parameter scans or assert implementation precision without this gate; do not reopen vFHE integers.

## RELEVANT FILES — NEW CHAT READ ORDER

1. `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → this `STATE.md`.
2. `findings/spru-adaptive-distinct-hybrid-ks-error-martingale-gate-iteration156.md` — current partial probabilistic lemma.
3. `findings/spru-trace-distinct-rotation-evaluation-key-index-gate-iteration147.md` — source keys and index mapping.
4. `findings/spru-openfhe-v142-fixedauto-pretrace-mul-no-rescale-gate-iteration146.md`; `findings/spru-conditional-pretrace-pk-shared-mask-spectral-covariance-iteration145.md` — resolved pre-Trace assumptions.
5. `findings/OPEN_RESEARCH_BRANCHES.md` — remaining opportunities/history.
6. `findings/vfhe-current-official-revision-identity-gate-iteration155.md`, `MISSING_SOURCES.md` — original P1 source gate; only if returning to vFHE.
7. Earlier SPRU/failure archives only when specific facts needed.

## STATUS

**I156 CLOSED: PASS restricted conditional pre-ModDown martingale orthogonality / UNCLEAR full source HYBRID KS rounding/precision / SPRU OPEN one next I157 source gate / P1 vFHE OPEN SOURCE-GATED not dropped / I152–154 integer encoders PARKED / I157 NOT STARTED.** No full OpenFHE execution/benchmarks, official PDF revision match, performance or security claim.
