# FHE Research State — After Iteration 190

**I190 COMPLETED; I191 NOT STARTED.** Read START_RESEARCH_SESSION.md → RESEARCH_PHILOSOPHY.md → AGENT.md → STATE.md; ONE primary hypothesis + ONE cheapest decisive test. Human PI decides research direction/importance/contribution/pivot; assistant executes source audits/derivations/verification/archive.

## CURRENT TARGET — HIGH-PRIORITY TECHNICAL AUDIT

**Zhang–Wang–Cheng, *Faster FHEW Bootstrapping with Adaptive Key Update*, ePrint 2025/381** https://eprint.iacr.org/2025/381. Original full 27 physical-page Research MCP github-mirror PDF SHA256 `bbc507b8323f4a65dea806bb663c9eea8ef2954e41259cad3b9db11256a03faf`, latest official binary VERSION_UNVERIFIED; independently read official PDF text at `https://eprint.iacr.org/2025/381.pdf` (§5.1 physical p19; Table3 physical p21). PDF SCREENSHOT p19 attempted through web, failed cache miss; **formula glyphs not visually verified**. No code run, no measured decryption failure attack. Authors report 20.7% bootstrap speed improvement at greater key storage.

**I190 ONE hypothesis:** Source's §5.1 Gaussian norm `||s||₂=√(nσ²)`, Table2 `n=447,σ=3.19,q=1024`, variance equation `β²=(q²/Qks²)(Qks²/Q²·σacc²+σms1²+σks²)+σms2²`, final modulus-switch variance `σms2²=(||s||₂²+1)/12`, and source DFR model `P=1−erf((q/8)/(2β))` consistently give Table3 Algorithm6 **2^-36** and DFR target **<2^-32**. **FAIL under extracted equations.**

**ONE decisive necessary lower-bound test:** Drop all nonnegative errors except final MS2. Then `||s||₂²=nσ²=447·3.19²=4548.7167`, `σms2²=379.1430583333`, `β≥19.47159619`. For q1024, `P_fail_model≥erfc(128/(2·19.47159619))=3.346946255e-6≈2^-18.1887`, **230,000× larger** than Table3 Algorithm6 2^-36 and **14,375× larger** than target 2^-32. Similarly below-limit for Algorithm5 reported 2^-37 impossible under same model. Even hypothetical alternate `erfc(128/(√2β))` gives floor `4.90874e-11≈2^-34.25`, still larger than both algorithm Table3 predictions (but would not violate <2^-32). This proves a **necessary algebraic/numerical inconsistency within the paper's extracted Gaussian model**, NOT actual FHE implementation failure or invalid 128-bit LWE hardness claim. Source uses a typical Gaussian key norm, NOT a high-probability per-key norm; stronger DFR requires independent tail analysis after checking exact conventions.

**Potential resolutions not yet checked:** PDF sqrt/erf typography, OpenFHE Gaussian σ=3.19 parameter interpretation, final post-keyswitch LWE secret distribution, ModSwitch normalization, independent covariance approximation and correct full-β worksheet; source version may have changed. No correctness/security bug alleged as confirmed until visual/implementation reproduction. Archive `findings/fhew-aku-gaussian-dfr-consistency-iteration190.md` SHA `d07cec0b01c77764f4e9620bd811d2de94b585e0`, commit `2cef862901c6fa4f9b16d82071fd8c6254fa85a3`.

**STATUS I190:** FAIL exact model-Table3 consistency, PASS source-specific variance floor and erfc computation, UNCLEAR actual code/formula version/security significance. **STATE_UPDATE YES**.

## NEXT_ACTION — I191 NOT STARTED

**HUMAN_REVIEW — recommend CONTINUE ONE source/code replication gate**, not generic toy mathematics. Verify visual §5.1 formula, secret std interpretation, final LWE key and mod-switch variance in original OpenFHE implementation or author's code, fully recompute β and Table3 DFR for n447/q1024/σ3.19. If inconsistency remains after fixing potential factor errors, recompute realistic DFR safe parameters at matched cryptographic security, evaluation key memory and latency; assess whether 20.7% speed advantage survives. If a missing scale or sigma convention reconciles source, archive correction, no unsupported defect claim. PI decides contact to authors/paper contribution. Do not repeatedly rediscover same lower bound without source fidelity.

## PREVIOUS ARCHIVES / DO NOT REPEAT

I188–189 LFBS PRCA B−1 logical key switches and ordinary hoisting with distinct operands PARK; I184–187 simple PRF/PRSS/Gaussian MPC ThFHE attempts PARK, parent ePrint2025/409 unbounded LDec OPEN; I183 GBFV few-slot ordinary automorphism invalid condition source-known; I182 GBFV-CKKS integer no-wrap safe; I178–181 naïve dBFV-to-BGV adaptations PARK; I175–176 Park C-MT binary jump already LLKN23; I171–174 SHIP small compression ideas PARK. vFHE2025/286 latest updated edition SOURCE-GATED. Full historical index `findings/OPEN_RESEARCH_BRANCHES.md`.
