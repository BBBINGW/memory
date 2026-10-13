# FHE Research State — After Iteration 159

**Checkpoint:** 2026-10-13 · `main` · I159 completed, I160 **NOT STARTED**.
**Authority:** Compact current research recovery entry, not all history. Prior long state `logs/state-pre-session-handoff-2026-10-13-iteration151.md` (blob `7641c5eb985497ae77e9284ed9e94a5713f3222d`); backlog `findings/OPEN_RESEARCH_BRANCHES.md`. Human PI decides targets, contribution, pivots, and disclosure. Agent performs one minimal test per authorized iteration.

## CURRENT TARGET

**Current examined research direction: SPRU CKKS bootstrapping**, Coron–Köstler, *Low-Latency Bootstrapping for CKKS using Roots of Unity*, ePrint 2025/651, §3.4–3.5; 42-page Research MCP GitHub mirror SHA256 `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6`, official version still VERSION_UNVERIFIED. Original author code `coron/spru_boot` with tagged upstream OpenFHE **v1.4.2**. Prior I147 verified eight distinct Trace rotation keys at source N32768,h64. **I156–I159 source-shape rounding-bias microaudits have reached HUMAN_REVIEW/PARK recommendation (not PI-archived yet); no active hypothesis.**

**Original vFHE P1 parent remains OPEN/HUMAN_REVIEW / SOURCE-GATED**, Cascudo et al. ePrint 2025/286 CRT common scalar-digit lookup ideal-PIOP source finding from I59–60. Current official 2026-02-16 PDF bytes unverified and missing; no latest official defect or compiled exploit claim. Fast integer encoder attempted repairs I152–154 PARKED after low-distance counterexamples. See `findings/vfhe-current-official-revision-identity-gate-iteration155.md` and `MISSING_SOURCES.md`. Human PI retains final direction/pivot/park/disclosure decisions.

## LAST COMPLETED ITERATION

**I159 (2026-10-13), I160 NOT STARTED.** Completed the single requested **uniform-public-a incremental HYBRID KS rounding bias** falsifier. At one P=5,Q=17, sOld=sNew=d=1, a uniform mod P*Q=85, e=±1 independent, exact source-shaped two-component `Dec(a,e)=Down(P−a+e)+Down(a)`. Compared at the **same a** to e=0 baseline: `Delta=CenterQ(Dec(a,e)−Dec(a,0))`. Exhaustive **170** cases: conditional means −1/2 for `a modP=0`, +1/2 for residue1, 0 otherwise; unconditional mean **0**, variance **1/5**, `|Delta|≤1`. Critically, noiseless baseline total error mean `−4/5` remains **nonzero**, distinct from incremental noise. All details `findings/spru-hybrid-ks-uniform-a-incremental-drift-cancellation-iteration159.md` SHA `fdd9d99aa22274f4f9c26766af170f4d2e6c67c1`.

## CURRENT QUESTION

Does an actual **multi-prime, source-parameter** OpenFHE HYBRID KeySwitch rounding/rotation covariance bound supply a meaningful SPRU Table2 precision/efficiency gain? The cheap alternative, a generic systematic new-key-error drift after averaging over uniform a, **does not exist in the fully enumerated 1P/1Q symmetric-noise toy**; the nonzero e=0 baseline is only ordinary coefficient rounding. The branch now needs a PI decision to PARK or a materially new source-specific hypothesis, rather than additional low-novelty scalar toy cases.

## PRIMARY HYPOTHESIS

**NONE ACTIVE.** I159 [PASS exact narrow cancellation]: same old/new secret1, digit1, public a uniform in `Z_85`, independent symmetric key noise `e=±1`, `b=−a+P+e`, both components downconverted by one-P/one-Q tagged source formula and added at decryption. Incremental `Delta(a,e)=Dec(a,e)−Dec(a,0)` centered in signed `Z_17` has unconditional mean0, Var1/5, max absolute1; conditional nonzero mean in 2 of 5 a-residue classes. e0 baseline mean−4/5. Therefore I158's fixed a=P conditional −1/2 does **not** imply unconditional fresh-key-error drift. This **does not** prove real source full multi-prime key-switch noise is conditionally centered after publishing public keys, nor source precision benefit.

## CURRENT EVIDENCE

- **[I159 PASS single-parameter distribution gate; RECOMMEND PARK]** Source-shape uniform-a full two-component toy (`P=5,Q=17,a←Z_85,e=±1`) has `E[Dec(a,e)−Dec(a,0)]=0`, `Var=1/5`, `max|Delta|=1`, yet `E[Dec(a,0)−1]=−4/5`. Precise conditioned signed-residue behavior in `findings/spru-hybrid-ks-uniform-a-incremental-drift-cancellation-iteration159.md`. Conventional modular quotient identity; **not a publishable SPRU scheme improvement**.
- **[DERIVED/EXACT I158]** One-P one-Q full private-private HYBRID KS conditional bias **survives** both conversions and plus-sign decryption for chosen public a=P, with two-component output (Down(b),Down(a))=(-1 or0,1). Valid old ciphertext (0,1) under old secret1, no-noise baseline correct. Keygens have e uniformly ±1 in toy, not author's true Gaussian; a chosen P is rare. Archive `findings/spru-openfhe-two-component-hybrid-ks-rounding-drift-iteration158.md`.
- **[FACT tagged source decryption]** OpenFHE v1.4.2 `src/pke/lib/schemerns/rns-pke.cpp` blob `4e46c873112c617713a9b5bb4f70c5fd916b17c8`, `PKERNS::DecryptCore` has positive `cv0+cv1*s`; `keyswitch-hybrid.cpp` blob `552fee8fc52c4ee12176e6b9a2ca279b079b7cbc`, `EvalFastKeySwitchCoreExt` accumulates b into cTilda0 and a into cTilda1 before two source `ApproxModDown` calls; `dcrtpoly-impl.h` blob `0fec66253228c4d6f36526f6f63d62c146fe39ca` uses canonical P-residue lift.
- **[DERIVED/EXACT I157 FAIL isolated rounding-centeredness]** Tagged OpenFHE v1.4.2 ordinary `KeySwitchInPlace → KeySwitchCore → EvalFastKeySwitchCore → ApproxModDown` direct call chain. `src/pke/lib/keyswitch/keyswitch-hybrid.cpp` blob `552fee8fc52c4ee12176e6b9a2ca279b079b7cbc`, `src/core/include/lattice/hal/default/dcrtpoly-impl.h` blob `0fec66253228c4d6f36526f6f63d62c146fe39ca`. Single-P `P5`→single-Q `Q17` canonical-residue basis lift yields `down(5−1)=0` and `down(5+1)=1`, bias `−1/2` relative ideal quotient 1. Source-exact **in isolated scalar subcase**, not a demonstrated full ciphertext decryption bias. Original p11 Lemma5 is only a norm bound. Archive `findings/spru-openfhe-hybrid-approxmoddown-rounding-conditional-bias-iteration157.md`.
- **[DERIVED/EXACT I156 PASS conditional]** Tower property of conditional means yields pairwise orthogonality for centered independently generated fresh-key errors with past-measurable switch digits in strictly linear/pre-rounded arithmetic. Three-stage exact toy `Z1=e1;Z2=(1+e1)e2;Z3=(1+e1e2)e3`, independent uniform signed e variables, 8-case cross moments all zero. Details `findings/spru-adaptive-distinct-hybrid-ks-error-martingale-gate-iteration156.md`.
- **[FACT source; not entire actual noise model]** Tagged `openfheorg/openfhe-development` **v1.4.2** `src/pke/lib/keyswitch/keyswitch-hybrid.cpp`, blob `552fee8fc52c4ee12176e6b9a2ca279b079b7cbc`, `KeySwitchGenInternal` creates per-part Gaussian e for each separately called single-key keygen; `KeySwitchInPlace` uses `KeySwitchCore`; **`KeySwitchDown` calls `ApproxModDown`**. Source does not imply rounded error conditionally centered. Its alternate threshold/key-reuse path `ekPrev` exists but is not the author's single-key Trace invocation.
- **[DERIVED I147]** Author `coron/spru_boot/src/single_slot.cpp` SHA `38d9fda8023ca0a06c5f4c9632802c83e4762c22`, Trace 8 shifts (8192,4096,2048,1024,512,256,128,64), distinct `5^r mod65536` key map entries for `N32768,h64`, but public frozen key bytes may be reused across separate invocations. Archive `findings/spru-trace-distinct-rotation-evaluation-key-index-gate-iteration147.md`.
- **[DERIVED I145/146]** Exact-ring pre-Trace two fresh bootkey ciphertexts with shared pk and fixed masks can exhibit spectral cross-slot orthogonality; tagged FIXEDAUTO initial `EvalMult+Add` performs no immediate rescale. Neither covers actual rotation HYBRID KS modulo rounding. `findings/spru-conditional-pretrace-pk-shared-mask-spectral-covariance-iteration145.md`; `findings/spru-openfhe-v142-fixedauto-pretrace-mul-no-rescale-gate-iteration146.md`.
- **[FACT source-paper]** ePrint 2025/651 §3.4 p11 Lemma5 bounds rounded KS error, does NOT claim conditional zero mean for full rounding; §3.5 pp11–12 unnormalized Trace uses O(log N) KS and rotations. Original Table2 N32768,h64,L256. Do not infer complete `√L=16` full-source RMS or 14bit real precision from this ideal result.
- **[PARKED]** I143 deterministic onehot trace-operator B-independent bound failed, I144 ideal Fourier identity already known, I146 initial-rescale and I147 same-key-within-single-trace shortcuts failed. Do NOT repeat these ideas. See backlog SPRU watchlist.

## MAIN OBSTRUCTION

Cheap source-shaped scalar gates I156–159 do not yield a novel CKKS/FHE result. I156's pre-rounded martingale orthogonality is standard; I157 isolated and I158 two-component examples have exceptional **conditional** rounding drift; I159 correctly separates e0 baseline from new-key increment and proves exact unconditional increment mean0 **after uniformly averaging a** in the single-prime toy. None models real multi-prime RNS, actual Gaussian tails, source N32768/h64 and stagewise rotated/additive CKKS error, public evaluation-key adaptivity, rescaling or actual precision. Further toy examples risk stagnation. SPRU microaudit **RECOMMEND PARK/HUMAN_REVIEW**, not unilaterally closed by agent.

## OPEN UNCERTAINTY

[OPEN] Whether actual tagged OpenFHE v1.4.2 multi-prime, source-parameter HYBRID KS introduces a *quantitatively important* conditional bias/covariance and supports a novel valid Table2 precision/latency improvement. No experimental implementation, algorithmic speedup, security issue, theorem gap or novelty verified. Parent vFHE P1 source-gated, unchanged.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION

**I160 NOT STARTED. PI decision gate.** Recommend **PARK SPRU I156–159 routine HYBRID rounding noise microaudits** and delegate selection of a new source-available, high-upside FHE direction from `findings/OPEN_RESEARCH_BRANCHES.md`, OR authorize **one** distinctly source-constrained full multi-prime+multi-stage bias/tail statement with actual OpenFHE Table2 relevance before any further computation. Do **not** repeat one-P/Q toy examples or claim systematic noise drift from I158. Do not restart vFHE without official latest PDF or material new evidence; preserve its P1 status. Human PI makes final strategy choice.

## RELEVANT FILES — NEW CHAT READ ORDER

1. `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → this `STATE.md`.
2. `findings/spru-hybrid-ks-uniform-a-incremental-drift-cancellation-iteration159.md` — definitive exact 170-case distribution gate and caveats.
3. `findings/spru-openfhe-two-component-hybrid-ks-rounding-drift-iteration158.md` — conditional two-component witness, no universal cancellation.
4. `findings/spru-openfhe-hybrid-approxmoddown-rounding-conditional-bias-iteration157.md` — isolated source-rounded map.
5. `findings/spru-adaptive-distinct-hybrid-ks-error-martingale-gate-iteration156.md` — linear pre-rounded conditional martingale.
6. `findings/spru-trace-distinct-rotation-evaluation-key-index-gate-iteration147.md` — 8 distinct source keys.
7. `findings/OPEN_RESEARCH_BRANCHES.md` — long-term opportunity index if PI authorizes pivot; vFHE `MISSING_SOURCES.md` only if returning to P1.

## STATUS

**I159 CLOSED: PASS source-shape one-P/Q averaged incremental rounding-error centering (170 exact cases, mean0, variance1/5) / FAIL treating I158 exceptional fixed-public-a drift as generic systematic fresh-noise bias / e0 baseline rounding bias −4/5 separately identified / UNCLEAR full tagged multi-prime SPRU noise and precision. I160 NOT STARTED.** **SPRU HYBRID noise microaudit HUMAN_REVIEW/PARK recommended; PI decides actual parking or source-distinct follow-up.** No claimed paper flaw, novel algorithm, benchmark, or FHE performance. vFHE P1 retains OPEN/SOURCE-GATED status; I152–154 repairs PARKED.
