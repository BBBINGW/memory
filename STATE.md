# FHE Research State — After Iteration 185

**I185 COMPLETED; I186 NOT STARTED.** Read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, then STATE.md. Human PI chooses final target, contribution judgment and pivots; research agent executes one falsifiable claim plus cheapest decisive test and archives evidence.

## CURRENT TARGET

Okada–Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT2025, IACR ePrint **2025/409**, full40pp Research MCP mirror PDF SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, official parity VERSION_UNVERIFIED. §1.2 leaves removal of bounded decryption count LDec open; Algorithms6/7 pre-generate fresh Shamir-shared discrete Gaussian padding per decryption, O(LDec) per-party memory. Existing PRF masks are separate and cancelled in decryption. This is an important FHE+MPC reuse target; no working solution currently.

**I184 FAIL:** independent local per-party PRF Gaussian padding fails global Shamir correlations for arbitrary active sets (T2 N3: z3=2z2-z1 modq). Real independent no-wrap equal-variance model forces negative variance v2=-V/3. Prior result `findings/threshold-fhe-independent-prf-padding-shamir-correlation-gate-iteration184.md`.

**I185 source prior art:** Cramer–Damgård–Ishai TCC2005 already non-interactively generates unlimited Shamir sharings via fixed seeds, and Benhamouda–Boyle–Gilboa–Halevi–Ishai–Nof ePrint **2021/1223** §3 extends seeded PRSS to linearly correlated uniform codewords, full59pp Research MCP mirror SHA `fa604815b3e01bd2092b9872480683218d088bbc28a4e2e9ffa9fbd938ffbe67`, official version unverified. Their generic PRSS is NOT itself a new contribution.

**I185 primary hypothesis — FAIL narrow secret-independent PRSS drop-in:** Source Algorithm7 requires Gaussian shape matrix `σ0²(Bpub²I−Σ_s)` where Σ_s is secret multiplication Gram (physical pp12–13,29–32). If PRSS setup/evaluation distribution is independent of s, reconstructed pad has same law for all s and cannot equal two distinct required laws. Exact negacyclic ring toy n2, module rank1, Bpub4, secrets sA=1 versus sB=1+X: Gram=I₂ versus2I₂; Gaussian **shape parameter matrices** 15σ0²I₂ versus14σ0²I₂. Distinct ratio P(e1)/P(0) = exp(-π/(15σ0²)) vs exp(-π/(14σ0²)). Note these are Gaussian exponent scale parameters, **not** exact sampled discrete covariance. No bound on statistical distance claimed and no source scheme attacked. Finding `findings/threshold-fhe-prss-gaussian-covariance-gate-iteration185.md` SHA `650e98c523e4667b9798378152bceb10f53ae556`, commit `b79d310dbe67b587368b8d78a7908875f7bd35e1`.

**I185 STATUS:** FAIL ordinary s-independent PRSS direct substitution, PASS original prior-art and exact source-parameter distribution mismatch, UNCLEAR privately s-conditioned Gaussian PRSS, simulation security, online interactions and costs. **STATE_UPDATE YES**.

## NEXT_ACTION — I186 NOT STARTED

One primary test only: assess an explicit **privately secret-conditioned seed setup** or distributed conditional discrete-Gaussian sampler with Shamir interpolation that hides s and Σ_s from any <T corrupted coalition, generates fresh correctly distributed padding for unbounded sessions, and preserves source simulation-security at lower total storage/online cost. First inspect original PRSS adversarial views, then choose one concrete candidate and cheapest decisive security/cost gate. Do not repeat uniform PRSS, independent PRF or a trivial covariance example. PI decides continue/park; if no concrete new mechanism, recommend PARK simple PRSS approach.

## PREVIOUS ARCHIVES

I183 GBFV few-slot invalid plain automorphism source-known PARK; I182 GBFV-CKKS output no-wrap verified and PARK; I178–181 naive dBFV-to-BGV approaches PARK; I175–176 Park C-MT binary jumps covered by LLKN23; I171–174 SHIP generic compression PARK. vFHE ePrint2025/286 P1 latest revised PDF remains SOURCE-GATED, no confirmed current-edition defect. Full historical index in `findings/OPEN_RESEARCH_BRANCHES.md`; all earlier archived files retained.
