# SHIP-I245 — Final public-source gate for original SHIP h=31 security audit; HUMAN_REVIEW/SOURCE_BLOCKED

Date: 2026-10-16 (PI explicitly continued SHIP). TRACK: **SHIP ONLY**. Root `STATE.md`, topical `findings/ship-memory-STATE.md`, I244, `AGENT.md`, `RESEARCH_PHILOSOPHY.md` and session restoration instructions were re-read before this action. No other research lines modified.

## One primary falsifiable hypothesis and one minimal decisive test

**H245:** With the public primary-source archive currently accessible, SHIP author (h=31) window-secret sampling and/or attacker-optimized `zeta/k, h_g, beta, d` for original `(logN,h,logq)=(13,31,55),(14,31,100)` are recoverable **without rerunning Sage**, enough to perform a source-distribution-matched attack hit test. **Falsifier:** no authenticated author's sample law and no full optimized dimensions in the entire actual attacker revised estimator repository, linked public attack executable's artifacts, original SHIP paper or attack preprint appendices. This tests **source evidence availability**, not the mathematical feasibility of future attacks.

**One cheapest test:** confirm local executable/dependency availability; inspect *original attack ePrint footnote* to find correct first-party revised estimator; enumerate its **complete Git tree** to rule out overlooked logs, locate exact parameter scripts, saved CSV, README and appendix; cross-read original SHIP §3.2 and §5.1/5.2 (where location constraint is a correctness/design assumption), inspect related public third-party sampler and a small source-focused web query. Do not create infrastructure, retest old toy bounds, or invent optimum parameters.

## Source-audit results [FACT]

1. **Authors' SHIP security claim.** Cheon–Hanrot–Kim–Stehlé, ePrint **2025/784**, original §5.1, physical p24, restricts nonzero secret indexes `i_k∈[kN/h−w,kN/h+w)` modulo N with `w=max(175,N/(2h))`; its discussion proposes a May21 sparse-key exhaustive-attack bound, and §5.2 states `h=31` with example lattice-estimator input `(logN,log(Pq0))∈{(13,55),(14,100),(15,105)}`, claiming targeted 128-bit security for the authors' chosen parameters. This is a *textually specified support restriction*, not a verifiable source of the actual nonzero-location sampler distribution, exact key sign distribution or implemented rejection conditions. §3.2 p15 motivates order statistics on uniform indices but does **not** authenticate h31 per-window sampler in executable HEaaN code. I243 confirmed the independent Poulpy code cannot instantiate author h31 because `ShipPlan::new` enforces `h|N`; original dimensions 8192/16384/32768 are powers of 2, not divisible by 31.
2. **Source-verified attack implementation & results.** Hou–Jiang ePrint **2026/366**, original revised preprint footnote p2 `https://github.com/identitymapping/enhanced_lattice-estimator`; `FHE_paper_estimate.py` blob **ef845580494722aff5d4ed3382e11460117d5b6b**, `estimator/lwe_primal.py` blob **08c7b0bb1c301f4b14ff85cb5cb8da16f5718410**, `estimator/nd.py` blob **c244ad2e32094be8dc64561ffbf7a9d92e5f1a88**, `FHE_paper_estimate_results.csv` blob **e7e5d1da0b85599a50a136996f510e5dba4930f8**. Source exact attack input: `SparseTernary(p=15,m=16)` over **unrestricted positions** and untruncated `DiscreteGaussian(stddev=3.19)`, `red_cost_model=RC.MATZOV`, `mitm=True,babai=True,deg_ring=n,structure_leverage=True`. Original CSV saved classical `ehg=117.65` for `ec25_q_13` and `ehg=122.30` for `ec25_q_14` (ordinary HG=122.20,126.41). CSV's wall seconds are runs of **the estimator**, NOT measured attacks.
3. **NEW exhaustive discovery limit:** Used connected GitHub `fetch` of **GET /repos/identitymapping/enhanced_lattice-estimator/git/trees/master?recursive=1**; JSON `truncated=false`, **108 total tree entries**. The full tree includes the above author `FHE_paper_estimate.py` and `FHE_paper_estimate_results.csv`; only summary estimates are saved as CSV. The README mentions `.xlsx` but the complete tree does NOT contain an `FHE_paper_estimate_results.xlsx`. No separate original h31 optimized-detail dump or `ec25` attack log was present in 108 listed files. `FHE_paper_estimate.py` **prints** the full `res_ehg` Cost object while evaluating but stores **only scalar estimates** in its `result` dict/CSV. Consequently published files cannot uniquely recover `zeta, h_g, beta, d` from the 117.65/122.30 scalars. These parameters would require rerunning code and capturing stdout or obtaining author saved prints.
4. **Local runtime:** Checked `command -v sage`, `command -v conda`, `command -v docker`: unavailable; `importlib.util.find_spec('sage')` and `find_spec('fpylll')` false; Python numpy/scipy present. The previously written I244 `/mnt/data/ship_i244_reproduce_author_hybrid.py` is in workspace, but its real `LWE.primal_hybrid` entry cannot execute without Sage and the enhanced fork. Merely calling NumPy sampling cannot substitute for the optimized attack.
5. **Attack preprint Appendix check:** Read ePrint2026/366 physical pp54–58. Table E.3 reports other security triples and Table G.1 reports **quantum** estimates for the two SHIP tuples; neither gives source-window sampler or specific optimized `zeta,h_g,beta,d`. Public `identitymapping/enhanced_hybrid_attack` is primarily benchmark/GPU implementation with saved small-dimension (n256/1024) cases, not source of the original SHIP parameter details. Targeted public author-code searches including HEaaN/SHIP found no **authenticated h31 source** in inspected evidence. This does not prove such an implementation is not obtainable by other means.

## Decisive implication [DERIVED]

```
Verified:
  Original SHIP `N,h,q` source values numerically match attack-author input;
  Attack-author saved model work numbers (117.65 / 122.30 bits) are REAL ESTIMATOR OUTPUT;
  Attack-author Xs=SparseTernary(15,16) means unrestricted balanced-sign locations;
  Original SHIP imposes structured ordered support-window positions;
  Full author estimator repo contains NO saved optimum Cost object for these rows.
Not verified:
  Exact distribution of author h31 implementation, including ordered support and signs;
  Optimized attack zeta,k,h_g,beta,d on those rows;
  Conditional rotated-primal hit probability *at the optimized attack regime*;
  New log2 attack work against actual SHIP or real recovered secret.
```

I242 already checked that a legitimate *unusual* center-of-window secret refutes independence, while a *natural conditional-uniform* per-window source yields approximately the original independence heuristic at one arbitrary nonoptimal `k=4096,h_g=0`. Hence the **secret prior mismatch alone cannot be used to certify original SHIP security or invalidate published attack estimate**. Cited `(117.65,122.30)` are security-mismatch WARNINGS under published assumptions; not security guarantees nor practical key recovery.

## HUMAN_REVIEW evidence request — only necessary new external input

1. **To original SHIP implementers:** For LL13, LL14/HT14 and HT15 (`h=31`), please provide `sparse secret key support + signs` sampling rule/source (e.g., whether `i_k` independent uniform over original windows, rejection conditions, window endpoint rounding and sign counts) and exact security estimator command/commit used for §5.2. A clear `keygen` extract or a mathematically specified conditional distribution suffices; source need not be public.
2. **To attack-estimator authors:** For `ec25_q_13`, `ec25_q_14` `FHE_paper_estimate.py` results please provide the printed full `res_ehg` Cost objects `beta,zeta,h_g,d`, plus estimator commit/hash, relevant reducer/shape assumptions, whether any runs modeled SHIP's regularly-spaced secret prior. `FHE_paper_estimate_results.csv` lacks these fields.
3. **If both source and Sage runtime become available:** Take the actual h31 distribution and actual attacker-optimized `k,h_g`, compute conditional random-J rotated-event hit probabilities with exact or statistically controlled sampling, independently assess correlations, then rerun matched attack cost before any reparameterization claims. Do NOT subtract the ~40.88-bit support prior event exponent from attack costs.

## End of Iteration

**STATUS:** **SOURCE_BLOCKED/HUMAN_REVIEW** for exact SHIP-author attack cost; PASS full primary-repo inventory / appendix source audit / environment availability gate; FAIL H245 that currently published artifacts suffice without Sage or author input. No new experimental cryptanalysis; no claim attack invalid or original SHIP broken. Honest stopping rule: one should NOT launch I246 as yet another shallow same-paper source search, source-free toy variant, or estimated-bit extrapolation.

**RESULT:** Completed first-party first-level provenance at I244 and exhaustive follow-up at I245. Resolved exact origin of attack numbers; demonstrated remaining `optimal Cost stdout` and `author secret sampler` are truly absent from inspected published artifacts. Blocking inputs explicitly specified so PI can request them. Keep SHIP cryptographic HMux-memory branch provisional PARK; THIS security-audit subline SOURCE_BLOCKED pending data. PI owns final PARK/pivot decision, no unrelated track mutations.

**NEXT_TEST:** Trigger only when exact h31 sampling source or attacks' full `Cost` outputs plus runnable Sage environment emerge. If no such new input, maintain HUMAN_REVIEW / PARK recommendation. No background work or automatic pivot.
**STATE_UPDATE:** YES topical/root checkpoints only, preserve other tracks and prior research.
