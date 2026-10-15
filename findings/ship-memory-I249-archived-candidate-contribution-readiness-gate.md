# SHIP-I249 — Evidence-based SHIP evaluation-key memory contribution frontier and rediscovery guard

**Date** 2026-10-16. **User PI explicitly said continue. TRACK=SHIP ONLY**. Read RESEARCH_PHILOSOPHY.md, AGENT.md, START_RESEARCH_SESSION.md, STATE.md, findings/ship-memory-STATE.md, I246, I247, I248. This iteration is a **research-continuation decision gate**, not a new cryptographic primitive, key-recovery attack, or a redo of archived toy work. Other CGS/VFHE/EXPLORE tracks untouched.

## ONE primary falsifiable hypothesis and cheapest decisive test

**H249:** In the existing SHIP archive, at least ONE already source-supported crypto evaluation-key representation has a credible path to a paper-level contribution because it demonstrates either **>=5% lower named peak key buffer under FAIR same-policy streaming** or **>=10% fewer symbolic online ring products** without known correctness/security/precision regressions and without duplicating known tricks; no crucial proof or physical benchmark is missing. FALSIFIER: source-check all serious archived candidate types and find none fulfills the joint threshold AND evidence conditions. These are PI-review screening thresholds, NOT universal cryptographic optimality limits.

**ONE smallest test:** Read M18/M19 mixed-radix, source I203 baseline, I222/225 streaming, I229/231 cross-domain KSK, I234 default affine, I236 rank3, I246–248 scalar column, and I245 original-author security blocker. Compute *a single source-shaped normalized resource vector* for each; check if an allegedly new radix-window key-pruning idea was previously recorded. Do not repeat source experiments, run a redundant NTT demo, assert actual IFMA RSS, or launch a new full-paper search without technical trigger. Run and save exact arithmetic only.

## FACT provenance

- Original SHIP Cheon–Hanrot–Kim–Stehlé ePrint **2025/784**, EUROCRYPT 2025 §4.2/§5.1. Original authors' HEaaN source / original **h31 distribution-matched 128-bit security** still I245 **SOURCE_BLOCKED**; third-party illustrative Poulpy N16384,h32/denseHW192 physical key q520 is **NOT security-matched** to author experiments. Do not equate the two regimes.
- Pinned **independent third-party Poulpy** `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`: `poulpy-ckks/src/layouts/ship/plan.rs` blob `364f4235253a3c76c70dfacf3ea24c5e69a2c3c2` gives `window=256,theta=4,mux_candidates=ceil(513/4)=129`, greedy `mux_bases=[4,4,4,3]`; `keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4` generates all digit candidate GGLWEs; `mux.rs` blob `e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce` has shared input hoist and complete group VMP.
- **IMPORTANT rediscovery gate**: Prior `findings/ship-memory-M18-fixed-depth-mixed-radix-key-minimization.md` blob `dd735832c4dbb1accc6edf1f4dd40e996c159419` **already proved** [4,4,3,3] product144 >=129, minimum sum14 among four groups with each radix2..4, correct *for every* offset u0..512, i.e. 480→448 keys, 32 omitted full rank2 GGLWE. `findings/ship-memory-M19-fixed-depth-radix-group-cost-frontier.md` blob `1f1429e034614a1a3ae78b4f2b00211658f133ef` already source-audited count, guard, Galois, scratch and noted no Rust benchmark/security/noise proof, engineering low novelty. **Do not re-discover M18 as I249 novelty**.
- `findings/ship-memory-I222-hmux-groupwise-prepared-residency-gate.md` plus I225 prior art: group-streaming 2.875GiB named key-buffer baseline under original 4-key group (other2404MiB resident + raw180 + prepared360) is *not* process RSS and not a cryptographic key-memory reduction; a theoretical one-key streaming original could be even smaller with an API refactor.
- `findings/ship-memory-I229-onehot-completion-cross-keydomain-gate.md` and I231: nominal ~23.54% at-rest source-shaped key saving, but cross-secret KSKs, extra high modulus, key reconstruction >6336 KSK operations, and same-policy group-streaming named buffer ~3.642GiB >2.875; no Pareto.
- `failures/ship-memory-I234-onehot-default-gsw-rotation-frontier.md`: nominal ~24.18% at-rest prepared saving, 352 additional online ordinary ATKs, online symbolic VMP 17280→19008 (+10%); simple affine CMux prior art.
- `failures/ship-memory-I236-fused-affine-rank3-keysize-gate.md`: rank3 fused approach 352×135MiB vs baseline480×90MiB, total 48.75390625GiB (+9.47%), VMP slots19008 (+10%).
- `findings/ship-memory-I246-onehot-scalar-column-public-galois-completion.md`: at-rest 5.625GiB/12.63047% conditional saving, no new KSK, but 3168 PUBLIC GLWE automorphisms and unchanged online symbolic VMP; missing prepared scalar column must be restored and core streaming matched peak was NOT shown lower. `findings/ship-memory-I247-prepared-domain-onehot-rebuild-peak-memory-frontier.md`: even ideal extra-noise-free tile fuse max named peak gain 67.5MiB/2944MiB =2.2928% *within fixed four-key staged policy*, before online cost; stock kernel needs full group. `failures/ship-memory-I248-prepared-canonical-digit-carry-gap.md`: canonical prepared-digit arithmetic is not linear because carry/borrow; I247's generic prepared-domain equality overclaimed; only torus-mod-Q representation equivalence holds. Fair original finer candidate-streaming further limits claim. Candidate PARK.
- Security danger conditions `failures/ship-memory-I226-reused-zero-hmux-key-fingerprint-leak.md` (reuse zero key), I235 (shared encryption mask reveals β), I233 (high q raised control exposed), I237 (Galois-invariant s shrinks key entropy) block obvious variants. Author-SHIP h31 vs Poulpy h32 security unmatched; I245 author-distribution security audit source blocked.

## Exact normalized source-shaped arithmetic [DERIVATION/EXECUTED]

Standalone Python script run **now**; saved JSON at `/mnt/data/ship_i249_contribution_frontier.json` SHA256 **`3d6f561b0cf2552c548f874793cba6164b5d1b1f77dcd588c9d3db883af7bcf1`**. One arithmetic model for the illustrative pinned third-party IFMA layout only:
```
N=16384, h=32, radix original [4,4,4,3], dnum9, rank2 per key90MiB,
other prepared keys2404MiB, original HMux keys480,
original eager prepared total (480*90+2404)/1024=44.53515625GiB,
original symbolic online VMP product slots 480*9*2*2=17280,
same four-candidate group-stage peak named key buffer2404+4*(45+90)=2944MiB=2.875GiB.

M18/M19 [4,4,3,3]: 448 rank2 keys, prepared (448*90+2404)/1024
 =41.72265625GiB, at-rest prepared −6.31524%, symbolic VMP
 448*9*2*2=16128, −6.66667%, MAX group remains radix4 => current-group
 same four-key staged named buffer =2944MiB, 0% peak improvement.
 No benchmark, no concrete noise/security matched proof, simple published
 baseline mixed-radix tuning known; no asserted source originality.

I229 retained plus converter keys: 34.0517578125 GiB source-prepared,
−23.5396% stored, same group staging named ~3.642GiB (+26.68%).
Huge reconstruction KSK costs, no ready contribution.
I234 affine: ~33.768GiB −24.18% stored but VMP work +10%, group keys+ATK peak ~3.227GiB.
I236 rank3: 48.75390625GiB +9.47%, VMP+10%.
I246/248 scalar-only omission: 38.91015625GiB −12.63% stored, VMP unchanged,
 4-key staging old named peak2944MiB; hypothetical ideal I247 fusion saves
 ≤67.5MiB=2.2928% named stage buffer, not actual RSS; carry issue remains.
```

**Important interpretation:** (i) Key at rest + conditional prepared byte savings are NOT peak process RSS savings; (ii) every cited runtime/precision improvement remains **unverified** without Rust/IFMA; (iii) I229/I234 stream named peaks are previously archived *model-based approximations*, and changes in scratch/other-key lifetimes can alter denominators; (iv) reducing online VMP *symbolic slots* does not immediately prove lower elapsed time; (v) this is a *finite catalog assessment*, **NOT** a mathematical no-go theorem excluding all conceivable new SHIP optimizations.

## End of I249

**STATUS:** **FAIL H249 contribution-readiness criterion for ALL currently archived candidates**, PASS unique prior M18/M19 rediscovery check & one normalized arithmetic comparison, HUMAN_REVIEW/PARK recommended. **NO new crypto primitive or cryptanalysis** this iteration. Of extant candidates M18/M19 has only narrow engineering promise (−6.67% symbolic online products, −6.32% full eager-prepared bytes, but 0% matched group stage peak), while I246 gains 12.63% *at rest* but ≤2.293% group RAM ideal plus reconstruction/carry issues. Nothing yet meets credible novel and security-matched ≥5% FAIR RAM or ≥10% ONLINE Pareto, with actual correctness/precision measured. **Do not misrepresent I249 as new research contribution.**

**NEXT_ACTION:** Maintain SHIP main crypto eval-key resident RAM as **HUMAN_REVIEW / recommend PARK**, after 249 numbered iterations plus M18/M19 preexisting; I245 original-author security h31 remains **SOURCE_BLOCKED**. Resume only if PI supplies fresh material (authenticated SHIP author generator; actual IFMA runner, benchmark, or a truly new nontrivial primitive with source/security-matched algebra and convincing >5–10% fair Pareto), OR explicitly changes optimization objective to persisted/network storage after prior art survey. No automatic CGS/VFHE/EXPLORE pivot or background continuation. Continue as user instructs but refuse to invent incremental same-paper ideas. **STATE_UPDATE YES**, record this decision frontier to topical/root, preserve all tracks.
