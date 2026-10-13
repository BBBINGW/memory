# FHE Research State — After Iteration 157

**Checkpoint:** 2026-10-13 · `main` · I157 completed, I158 **NOT STARTED**.
**Authority:** Compact current research recovery entry, not all history. Prior long state `logs/state-pre-session-handoff-2026-10-13-iteration151.md` (blob `7641c5eb985497ae77e9284ed9e94a5713f3222d`); backlog `findings/OPEN_RESEARCH_BRANCHES.md`. Human PI decides targets, contribution, pivots, and disclosure. Agent performs one minimal test per authorized iteration.

## CURRENT TARGET

**SPRU CKKS bootstrapping single-slot Trace — conditional key-switching error covariance (OPEN, no ACTIVE experiment).** Coron and Köstler, *Low-Latency Bootstrapping for CKKS using Roots of Unity*, ePrint **2025/651**, §3.4–3.5 physical pp11–12; Research MCP full 42pp GitHub mirror SHA256 `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6` (latest official VERSION_UNVERIFIED). Author code `coron/spru_boot`; relevant tagged upstream **OpenFHE v1.4.2**. I147 proved 8 distinct HYBRID rotation evaluation-key entries per invocation at source N32768,h64 (and 6 more distinct product keys). Open technical question is actual successive HYBRID KeySwitch **conditional noise covariance and rounding** in the Trace. This is NOT a verified source error, FHE speedup, or precision improvement.

**Previous parent target:** Cascudo et al. vFHE ePrint **2025/286**, CRT diagonal scalar-digit soundness, remains **OPEN/HUMAN_REVIEW / SOURCE-GATED**, **not resolved or invalidated**. The I59–60 mathematical ideal-PIOP mirror-backed evidence exists, but current official PDF bytes are missing; do NOT claim official latest defect or compiled attack. I152–154 fast integer-encoder repair branch PARKED after three distance failures. See `findings/vfhe-current-official-revision-identity-gate-iteration155.md` and `MISSING_SOURCES.md`. PI's “好的，请继续” after the explicitly offered choice to select another OPEN branch authorized choosing SPRU as the new executable research focus.

## LAST COMPLETED ITERATION

**I157 (2026-10-13), I158 NOT STARTED.** One source-specialized exact scalar HYBRID `ApproxModDown` falsifier. In OpenFHE v1.4.2 normal `KeySwitchInPlace→KeySwitchCore→EvalFastKeySwitchCore→ApproxModDown` (not `KeySwitchDown` as the direct intermediary), one-P/one-Q exact down-conversion of `P+E`, `P=5,Q=17,E=±1` symmetric centered, produces output 0/1 against ideal1, i.e. conditional mean additive error −1/2. **FAIL general zero-bias extension to isolated rounded map; UNCLEAR true two-component decrypted HYBRID KS noise**. Archive `findings/spru-openfhe-hybrid-approxmoddown-rounding-conditional-bias-iteration157.md` blob `303f86df2c56c92547c947a047e1d0c9eac1334e`.

## CURRENT QUESTION

Can the **two-component decrypted** HYBRID KeySwitch error in source SPRU Trace retain a useful centered decomposition/bounded predictable bias after `ApproxModDown`? I157 killed the unjustified assumption that the **isolated down-conversion of one scalar component** preserves centeredness. Need determine whether actual `ct0+s·ct1` combination cancels this toy's component bias under valid KeySwitch evaluation-key equations. No live OpenFHE precision, paper error or performance result established.

## PRIMARY HYPOTHESIS

**NONE ACTIVE.** I157 [FAIL source-exact scalar-specialized zero bias]: CKKS `t=0`, one-P `P=5`, one-Q `Q=17`, scalar integer `x=5+E`, `E∈{-1,+1}` independent symmetric. From tagged OpenFHE `ApproxSwitchCRTBasis` (canonical P residue) and `ApproxModDown`, `down(x)=((x mod17)-(x mod5))*7 mod17`, with outputs 0 and1, ideal1. Thus `E[down(5+E)−1]=-1/2`. Let `ξ_j` be full error, `B_j=E[ξ_j|past]` predictable drift, `M_j=ξ_j−B_j` centered; need genuine quantitative bounds, not toy assumptions. **No proof actual two-component decrypted KS bias is −1/2 or nonzero**. Original I156 pre-ModDown martingale statement remains correct **in its own conditional linear model**.

## CURRENT EVIDENCE

- **[DERIVED/EXACT I157 FAIL isolated rounding-centeredness]** Tagged OpenFHE v1.4.2 ordinary `KeySwitchInPlace → KeySwitchCore → EvalFastKeySwitchCore → ApproxModDown` direct call chain. `src/pke/lib/keyswitch/keyswitch-hybrid.cpp` blob `552fee8fc52c4ee12176e6b9a2ca279b079b7cbc`, `src/core/include/lattice/hal/default/dcrtpoly-impl.h` blob `0fec66253228c4d6f36526f6f63d62c146fe39ca`. Single-P `P5`→single-Q `Q17` canonical-residue basis lift yields `down(5−1)=0` and `down(5+1)=1`, bias `−1/2` relative ideal quotient 1. Source-exact **in isolated scalar subcase**, not a demonstrated full ciphertext decryption bias. Original p11 Lemma5 is only a norm bound. Archive `findings/spru-openfhe-hybrid-approxmoddown-rounding-conditional-bias-iteration157.md`.
- **[DERIVED/EXACT I156 PASS conditional]** Tower property of conditional means yields pairwise orthogonality for centered independently generated fresh-key errors with past-measurable switch digits in strictly linear/pre-rounded arithmetic. Three-stage exact toy `Z1=e1;Z2=(1+e1)e2;Z3=(1+e1e2)e3`, independent uniform signed e variables, 8-case cross moments all zero. Details `findings/spru-adaptive-distinct-hybrid-ks-error-martingale-gate-iteration156.md`.
- **[FACT source; not entire actual noise model]** Tagged `openfheorg/openfhe-development` **v1.4.2** `src/pke/lib/keyswitch/keyswitch-hybrid.cpp`, blob `552fee8fc52c4ee12176e6b9a2ca279b079b7cbc`, `KeySwitchGenInternal` creates per-part Gaussian e for each separately called single-key keygen; `KeySwitchInPlace` uses `KeySwitchCore`; **`KeySwitchDown` calls `ApproxModDown`**. Source does not imply rounded error conditionally centered. Its alternate threshold/key-reuse path `ekPrev` exists but is not the author's single-key Trace invocation.
- **[DERIVED I147]** Author `coron/spru_boot/src/single_slot.cpp` SHA `38d9fda8023ca0a06c5f4c9632802c83e4762c22`, Trace 8 shifts (8192,4096,2048,1024,512,256,128,64), distinct `5^r mod65536` key map entries for `N32768,h64`, but public frozen key bytes may be reused across separate invocations. Archive `findings/spru-trace-distinct-rotation-evaluation-key-index-gate-iteration147.md`.
- **[DERIVED I145/146]** Exact-ring pre-Trace two fresh bootkey ciphertexts with shared pk and fixed masks can exhibit spectral cross-slot orthogonality; tagged FIXEDAUTO initial `EvalMult+Add` performs no immediate rescale. Neither covers actual rotation HYBRID KS modulo rounding. `findings/spru-conditional-pretrace-pk-shared-mask-spectral-covariance-iteration145.md`; `findings/spru-openfhe-v142-fixedauto-pretrace-mul-no-rescale-gate-iteration146.md`.
- **[FACT source-paper]** ePrint 2025/651 §3.4 p11 Lemma5 bounds rounded KS error, does NOT claim conditional zero mean for full rounding; §3.5 pp11–12 unnormalized Trace uses O(log N) KS and rotations. Original Table2 N32768,h64,L256. Do not infer complete `√L=16` full-source RMS or 14bit real precision from this ideal result.
- **[PARKED]** I143 deterministic onehot trace-operator B-independent bound failed, I144 ideal Fourier identity already known, I146 initial-rescale and I147 same-key-within-single-trace shortcuts failed. Do NOT repeat these ideas. See backlog SPRU watchlist.

## MAIN OBSTRUCTION

There is an exact **nonlinear modular down-conversion obstacle** to extending I156's pre-ModDown zero-conditional-mean lemma automatically. The one-P toy yields nonzero predictable drift from symmetric error; however full HYBRID KeySwitch performs **two** separate `ApproxModDown` operations and decrypts their sum against secret `s`, where biases may cancel or combine. The full source key pair/secret structure, actual multi-prime RNS rounding, input digit distributions, evaluation-key public dependencies, subsequent CKKS rescaling and maximum-slot tails remain unverified. No end-to-end Table2 14-bit claim or speed gain.

## OPEN UNCERTAINTY

**[OPEN]** Whether single-component `ApproxModDown` bias survives in the actual **decrypted two-component** KeySwitch with source-consistent `EvalFastKeySwitchCoreExt` and new/old secret equation; conditional drift magnitude/second moments in true multi-prime OpenFHE; future ct×ct rescale, data-dependent key usage; novelty. Do not mistake model-level bias for original author scheme deficiency.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION

**I158 only if authorized.** Perform **ONE exact full two-component decryption falsifier**: read tagged OpenFHE v1.4.2 `EvalFastKeySwitchCoreExt`, relevant `KeySwitchGenInternal`, `EvalFastKeySwitchCore`, decryption sign convention, and construct source-consistent small `P,Q,sOld,sNew` with actual switching-key relation. Test whether `ct0+sNew·ct1` cancels or retains the isolated I157 conditional bias for fresh centered key errors. **Stop at this toy correctness/noise gate**; do not launch full parameter sweeps/benchmark or claim complete KS martingale behavior. Do not reopen vFHE encoder failures.

## RELEVANT FILES — NEW CHAT READ ORDER

1. `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → this `STATE.md`.
2. `findings/spru-openfhe-hybrid-approxmoddown-rounding-conditional-bias-iteration157.md` — latest exact single-component rounding obstruction and source paths.
3. `findings/spru-adaptive-distinct-hybrid-ks-error-martingale-gate-iteration156.md` — pre-ModDown conditional centered model.
4. `findings/spru-trace-distinct-rotation-evaluation-key-index-gate-iteration147.md` — original 8 distinct rotation keys.
5. `findings/spru-openfhe-v142-fixedauto-pretrace-mul-no-rescale-gate-iteration146.md`; `findings/spru-conditional-pretrace-pk-shared-mask-spectral-covariance-iteration145.md` — older fixed-mask model/source facts.
6. `findings/OPEN_RESEARCH_BRANCHES.md` — index only; `MISSING_SOURCES.md` if returning to prior vFHE parent.

## STATUS

**I157 CLOSED: FAIL automatic conditional-zero-mean extension through a source-specialized `ApproxModDown` map / PASS exact one-P/one-Q conditional-drift witness / UNCLEAR real two-component decrypted HYBRID KS / SPRU target OPEN / I158 NOT STARTED.** P1 vFHE OPEN SOURCE-GATED, integer-encoder repairs I152–154 PARKED. No actual SPRU error bias, precision failure, paper flaw, or performance gain demonstrated. Human PI retains continuation/novelty decisions.
