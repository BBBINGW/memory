# PURE FHE P0 — RBOOT×Orbit: Level/Scale/Range Functional-Bootstrap Placement Gate

**Date:** 2026-10-26 Asia/Singapore
**Stage:** `PURE-FHE-P0-PRESCOUT-10`, independent broad-source prescout; **NOT** BOOT/SHIP/CGS/EAI official iteration.
**Status:** `FAIL_LEVEL_SCALE_ONLY_FBOOT_ELIGIBILITY / PASS_NEW_NECESSARY_RANGE_CONSTRAINT / NOVELTY_SYSTEMS_UNVERIFIED / PARK_AS_NEW_CRYPTO_PRIMITIVE`.
**EVIDENCE:** verified publicly readable author/paper mirrored texts, pinned GitHub source code, exact analytic and Python math checks; **NO FHE_NATIVE**, no model benchmark, no Codex/GPU. Existing engineering candidates (FHE×MPC random-bit-sharing; FHE×ZK KS witness reuse) untouched.

## Source and provenance G0

1. Yang, Niu, Wei, Huang, Hong, Wei, *RBOOT: Accelerating Homomorphic Neural Network Inference by Fusing ReLU within Bootstrapping*, USENIX Security 2026, published USENIX https://www.usenix.org/conference/usenixsecurity26/presentation/yang-zhaomin ; ePrint 2025/1534 https://eprint.iacr.org/2025/1534 ; author/paper **35 physical pages**, SHA256 `d187c655f3ecc88d6925c76f6608ce7fdcb8715ec09c7433b088c5a19dcc0a42`, github mirror `VERSION_UNVERIFIED` (publisher PDF bytes not independently matched). Text source **physical pp16–22**, esp. §4.1 p17 `−q0/4<M<q0/4` as **assumption** for inexpensive `arcsin∘sin` functional bootstrap; p20 Alg6 odd/even ReLU RBOOT identity `ReLU(x mod q0)=arcsin(sin(2πx))/(4π)−arcsin(cos(4πx))/(8π)+1/16` for normalized x∈(−1/4,1/4)+Z. It is **NOT** claimed valid over whole [−1/2,1/2]. The full-domain Fourier alternative is mentioned p16–17, cannot infer all functional bootstrap methods have same range limit. Author p23 Table3 example `N=2^16`: full-sparse 103.2s normal bootstrap+ReLU vs 48.7s fused; 1/8-sparse 72.6s vs33.1s. p24 Table5 ResNet20/32/44/56 average2.77x inference speed, under source parameters/precision/architecture. These are already published FHE contributions, not ours.
2. Zhou, Seo, Chen, Ozdemir, Brown, Zheng, *Orbit: Optimizing Rescale and Bootstrap Placement with Integer Linear Programming Techniques for Secure Inference*, USENIX Security 2026, official https://www.usenix.org/conference/usenixsecurity26/presentation/zhou and ePrint 2026/213 https://eprint.iacr.org/2026/213 . Full PDF 26 physical pages SHA256 `dbfe4c681867ea4b38169ebadc0c0eecd9e7d5fd022e54e8fc16431fec0f309d` mirrored `VERSION_UNVERIFIED`; §3–4 pp3–6 level/scale and placement ILP; Table2 defines `bootstrap` refresh level and scale but no explicit target-function input-value-range eligibility. Authors report geometric-mean1.19x vs DaCapo,1.73x vs Orion,1.52x vs ReSBM **on different workloads/hardware from RBOOT**; never multiply speedups or compare directly.
3. Pin source **cmu-cryptosystems/Orbit** current default GitHub: `scripts/optimizer/orbit/ilp_core.py` blob `c3a1580ff3b26b9b2d5b377680d1eeabf7da17ec`, `scripts/optimizer/orbit/ilp_gurobi.py` blob `8a33708da25bd2630aeeed59cddfadb138c6a306`, `scripts/tdag/tdag.py` blob `516d41538ac19ef9f0083d108439dc364e7b897f`. The reviewed ILP variables are **level/scale/bootstrap/rescale** and code has no explicit `functional_bootstrap`, `rboot`, value `interval`, or `magnitude_bound` variable. **Only reviewed these three files**; do not assert arbitrary Orbit downstream subsystems never track input ranges.
4. Closest obvious counter-prior-art **HEIR 2026**: Jeremy Kun's maintainer update 2026-09-04 https://www.jeremykun.com/2026/09/04/updates-on-heir-homomorphic-encryption/ expressly says HEIR workflows currently require manual annotation of **bounds on the input ranges to each activation** (planned automated validation-set estimates). So annotation/range analysis for FHE activations is ALREADY KNOWN, not novel. HEIR HE compiler design https://heir.dev/docs/design/layout/ discusses compiler layout optimization. RBOOT + Orbit + HEIR together already cover most natural components. No direct proof of unoccupied integration or good matched latency.
5. Additional USENIX 2026 RBOOT paper explicitly combines activation with bootstrap and argues minimal extra computational depth. Classic nonlinear polynomial circuit scheduling and compiler techniques predates Orbit. No copyright text repeated in full.

## ONE smallest falsifiable technical claim

**H_LEVEL_SCALE_SUFFICIENT:** If two CKKS ciphertexts have the same level and scale and an identity bootstrap is legal, a static scheduler can blindly replace the identity bootstrap followed by ReLU with the cheaper RBOOT functional bootstrap **without any additional pre-activation magnitude bound** and preserve `ReLU` semantics.

**Exact analytical counterexample from source p20 Alg6 ideal function** (not a FHE noise attack):
Let normalized preactivation `x=m/q0` and
```
F(x) = arcsin(sin(2πx))/(4π) − arcsin(cos(4πx))/(8π) + 1/16.
```
For source-assumed `x=1/8∈(−1/4,1/4)`:
`arcsin(sin π/4)=π/4`, `arcsin(cos π/2)=0`, so `F(1/8)=1/16+1/16=1/8=ReLU(1/8)`.
For outside admissible bound but still within centered CKKS representative `x=3/8∈(−1/2,1/2)`:
`arcsin(sin 3π/4)=π/4`, `arcsin(cos 3π/2)=0`, so `F(3/8)=1/8 ≠3/8=ReLU(3/8)`.
**Absolute normalized semantic difference=1/4**, far larger than typical CKKS noise. Both messages may be encrypted using the **same keys, same ciphertext level, same scale, same q0** and otherwise legal identity bootstrapping. The source target-function/range precondition is not derivable from level/scale metadata.
Independently evaluated Python `asin(sin())` and `asin(cos())` at x∈{−1/8,0,1/8,3/8}; observed F values [0,0,1/8,1/8] with ~1e−17 floating error. This checks elementary trig only, NOT CKKS program execution.

**Interpretation:** FAIL LEVEL_SCALE_ONLY. Correctness of the cheap RBOOT mode **demands a typed range guarantee**, or a different general-domain functional-bootstrapping construction with updated algorithm/cost. This is **already stated in the RBOOT original source**; our contribution is only the cross-paper compiler interface necessary-condition argument, NOT an independent new crypto theorem or attack.

## Positive direction — conditional, not new publication claim

One possible compiler/algorithm research problem: simultaneous scheduling of 3 classes of encrypted nodes with **level, scale, certified range, usable output precision, and branching/liveness**:
- identity bootstrap (B_id): existing type, refresh level, preserve approximate m;
- RBOOT (B_relu): can be used only where producer's input value domain `I(v)⊂(−q0/4+epsilon,q0/4−epsilon)`, with epsilon accounting for scale/noise, and output approximation error and post-bootstrap level/scale verified under same parameter set;
- no bootstrap / ordinary polynomial ReLU: different depth, cost and output error tradeoffs.
- for residual connections, fusing RBOOT changes the node's value; cannot replace an identity bootstrap shared by a branch still requiring **raw pre-ReLU** m without a copy/duplicate branch path; this must be typed.
- range can be analyzed via public weights and input bounds, interval or affine arithmetic, precision error intervals and optional runtime fallback if provable. If range is unknown, **must not assert correctness of cheap mode**. Common HEIR range annotation already anticipated, so novelty must be **joint placement+fused functional cost with a distinct optimization algorithm and real native end-to-end win beyond source**, not "we track intervals".
- Source baseline RBOOT N=2^16, Orbit base typically N=2^17; cost model and keys need SAME N, modulus/scale, bootstrap level, CKKS security, cryptographic precision, and nonlinearity approximation. Proven compiler optimality under some bounded model or meaningful measured native speedup, plus nearest competitor HEIR/Fhelipe/RBOOT/Orbit, is necessary before any claim.

**DECISION:** Do NOT initiate a dedicated pure-FHE cryptographic-primitive research line from this. Conditional `PARK_ORBIT_RBOOT_RANGE_AWARE_COMPILER_INTEGRATION` as **applied FHE systems** research idea, lower priority than an original cryptographic dataflow mechanism unless PI explicitly authorizes a source-matched systems benchmark. No Codex task generated. The supposed idea "range analysis" is already prior art (HEIR). Given repeated P0 01–10 gates with no surviving original primitive, **trigger STAGNATION/HUMAN_REVIEW rather than keep writing superficial source+toy rounds**. Next P0 action should be a genuinely different *problem-first* source-based mechanism or broader portfolio review, not another small composition.

## End of iteration

`STATUS: FAIL_LEVEL_SCALE_ONLY / PARK_APPLIED_COMPILER`
`RESULT: RBOOT_RANGE_NECESSITY + RBOOT/ORBIT/HEIR_PRIOR_ART_TRIANGULATION`
`NOVELTY: NOT_ESTABLISHED / NO_NEW_FHE_SCHEME`
`NEXT_TEST: HUMAN_REVIEW_P0_STAGNATION_AND_NEW_PROBLEM_FIRST_CANDIDATE`
`CODEX: NOT_RUN`
`STATE_UPDATE: THIS_FINDING_ONLY; OFFICIAL_ROOT_STATE_NOT_OVERRIDDEN`.
