# FHE Research State — After Iteration 158

**Checkpoint:** 2026-10-13 · `main` · I158 completed, I159 **NOT STARTED**.
**Authority:** Compact current research recovery entry, not all history. Prior long state `logs/state-pre-session-handoff-2026-10-13-iteration151.md` (blob `7641c5eb985497ae77e9284ed9e94a5713f3222d`); backlog `findings/OPEN_RESEARCH_BRANCHES.md`. Human PI decides targets, contribution, pivots, and disclosure. Agent performs one minimal test per authorized iteration.

## CURRENT TARGET

**SPRU CKKS bootstrapping single-slot Trace — conditional key-switching error covariance (OPEN, no ACTIVE experiment).** Coron and Köstler, *Low-Latency Bootstrapping for CKKS using Roots of Unity*, ePrint **2025/651**, §3.4–3.5 physical pp11–12; Research MCP full 42pp GitHub mirror SHA256 `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6` (latest official VERSION_UNVERIFIED). Author code `coron/spru_boot`; relevant tagged upstream **OpenFHE v1.4.2**. I147 proved 8 distinct HYBRID rotation evaluation-key entries per invocation at source N32768,h64 (and 6 more distinct product keys). Open technical question is actual successive HYBRID KeySwitch **conditional noise covariance and rounding** in the Trace. This is NOT a verified source error, FHE speedup, or precision improvement.

**Previous parent target:** Cascudo et al. vFHE ePrint **2025/286**, CRT diagonal scalar-digit soundness, remains **OPEN/HUMAN_REVIEW / SOURCE-GATED**, **not resolved or invalidated**. The I59–60 mathematical ideal-PIOP mirror-backed evidence exists, but current official PDF bytes are missing; do NOT claim official latest defect or compiled attack. I152–154 fast integer-encoder repair branch PARKED after three distance failures. See `findings/vfhe-current-official-revision-identity-gate-iteration155.md` and `MISSING_SOURCES.md`. PI's “好的，请继续” after the explicitly offered choice to select another OPEN branch authorized choosing SPRU as the new executable research focus.

## LAST COMPLETED ITERATION

**I158 (2026-10-13), I159 NOT STARTED.** Source-consistent two-component HYBRID KS exact scalar specialization **FAILS universal post-decryption cancellation of I157's rounding drift**. For one Q17/P5, sOld=sNew=1, digit1, public a=P5, error e∈{−1,+1} equally, source private-private key equation b=−a sNew+P sOld+e=e; extended core outputs (b,a), separately ApproxModDown → (−1 or 0,1), decrypted result 0/1 (ideal1), conditional error mean −1/2. Zero-noise e0 baseline decrypts exactly1. No proof of typical source noise behavior. Archive `findings/spru-openfhe-two-component-hybrid-ks-rounding-drift-iteration158.md` blob `d812c83d12e47aa6d3d53f42c4bcf4c3b617d05b`.

## CURRENT QUESTION

**SPRU current analytic issue:** Does the *distribution over actual uniform public key a and centered source discrete Gaussian e*, together with the full two-component HYBRID `ApproxModDown`, make the **incremental decrypted rounding noise** sufficiently centered/small that a meaningful probabilistic bound can improve source Table2 parameters? I158 proves only existence of **conditional nonzero bias for a rare fixed a=P** in an insecure single-P single-Q toy, and cannot justify actual N32768 error growth. Other vFHE parent stays OPEN/SOURCE-GATED; I152–154 integer repair PARKED.

## PRIMARY HYPOTHESIS

**NONE ACTIVE.** I158 PASS exact **noncancellation witness**, FAIL proposed universal two-component cancellation: `P=5,Q=17,sOld=sNew=d=1,a=5,b=e` with centered `e±1`. `Down(-1)=-1`, `Down(1)=0`, `Down(5)=1`; after both conversions `Dec_new=Down(b)+Down(a)` takes 0 or1 with ideal1 and mean error −1/2; noiseless e0 baseline1. Source tagged OpenFHE v1.4.2 `KeySwitchGenInternal` private-private equation and `EvalFastKeySwitchCoreExt` two accumulators and `PKERNS::DecryptCore` plus sign were verified. This is **conditional on rare selected a modulo P**, artificial e law and toy parameters; full realistic statistics NOT determined.

## CURRENT EVIDENCE

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

Two clean probabilistic facts cannot yet be promoted to a SPRU efficiency/precision claim: I156's pre-rounded distinct-key martingale orthogonality does not automatically survive nonlinear RNS downconversion; I157 isolated scalar map and I158 source-consistent *complete two-component decrypted* map give nonzero conditional drift for chosen public randomness. However the I158 choice a=P has P residue0 (probability ~1/P under uniform a_P), key-error e=±1 is not the real Gaussian, and one-P/Q toy is insecure. Full uniform-a **incremental** noise mean, baseline deterministic rounding bias, multi-prime RNS, tails and actual SPRU stagewise precision remain unverified. These elementary toy observations are not publishable by themselves.

## OPEN UNCERTAINTY

[OPEN] Whether source keygen's actual a randomness **averages away** the apparent e-dependent rounding bias; proper separation of deterministic e=0 two-component rounding from incremental e contributions; whether scale/parameter budget makes any residual drift meaningful and nontrivial to bound. No real OpenFHE error/precision failure, algorithm, attack or speedup was found.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION

**I159 only if PI authorizes.** ONE cheapest distributional falsifier: for the same source-equation one-P/Q two-component toy and one fixed digit, compute the **average incremental decrypted key-error** `Δ(a,e)=Dec(a,e)−Dec(a,0)` under uniformly sampled a mod QP and centered symmetric e; distinguish conditional-on-a mean vs unconditional expectation and compare with a proven O(1) norm ceiling. If averaging removes the special a=P bias or leaves only elementary negligible rounding at realistic Δ, **PARK SPRU microaudit** rather than start more parameter-free examples. Any claim about source Table2 requires subsequent exact multi-prime OpenFHE noise budget. No reopening archived vFHE fixes.

## RELEVANT FILES — NEW CHAT READ ORDER

1. `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → `STATE.md`.
2. `findings/spru-openfhe-two-component-hybrid-ks-rounding-drift-iteration158.md` — current two-component exact witness and source sign checks.
3. `findings/spru-openfhe-hybrid-approxmoddown-rounding-conditional-bias-iteration157.md` — one-component downconversion bias.
4. `findings/spru-adaptive-distinct-hybrid-ks-error-martingale-gate-iteration156.md` — pre-ModDown martingale model.
5. `findings/spru-trace-distinct-rotation-evaluation-key-index-gate-iteration147.md` — source distinct rotation keys.
6. `findings/OPEN_RESEARCH_BRANCHES.md` long-term priorities. vFHE `MISSING_SOURCES.md` only if returning to P1.

## STATUS

**I158 CLOSED: FAIL universal two-component rounding-bias cancellation; PASS exact source-consistent 1P/1Q full plus-sign decrypt witness; UNCLEAR actual averaged source HYBRID KS noise and SPRU precision. I159 NOT STARTED.** Human PI should decide whether a single distribution-averaged rounding check merits continuation or park SPRU low-novelty noise microaudits. P1 vFHE stays OPEN/SOURCE-GATED; fast integer encoder repairs I152–154 PARKED. No confirmed source-paper error or publishable contribution.
