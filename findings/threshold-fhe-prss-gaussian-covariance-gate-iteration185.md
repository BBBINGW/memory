# Iteration 185 — PRSS prior art versus covariance-dependent MLWE Gaussian padding

Date: 2026-10-14 JST. Human PI authorized by “好的，请继续.” Protocol read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, STATE.md SHA `25ddd209c290c95aac37cd4d882d97d8047d04f6`, I184 archive. ONE primary PRSS direct-substitution hypothesis and ONE exact two-input distribution mismatch test; no FHE implementation.

## Source provenance [FACT]

Okada–Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025, ePrint **2025/409**, https://eprint.iacr.org/2025/409. Full Research MCP 40 physical pp, github-mirror PDF SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, latest official version VERSION_UNVERIFIED. Source §1.2 p4 explicitly leaves removing bound LDec OPEN; Algorithms6/7 pp26,29 Shamir-share a fresh discrete Gaussian padding per decryption session, requiring O(LDec) stored values. Separate per-party PRF masks cancel in FinDec and are not padding. Algorithm7 p29, Lemma7.1 pp30–32 require Gaussian **shape parameter** `Σζ=σ0²(Bpub² I−Σ_s)`, where `Σ_s=Σ_i Gram(s_i)`. Definitions3.1 pp12 and 3.3 pp13 define Gram and Gaussian density: `ρ_S(x)=exp(−π x^T(SS^T)^(-1)x)`. `Σζ` is **squared-scale / Gaussian shape**, not exactly the empirical covariance of a lattice-truncated discrete Gaussian. Original statistical smoothing and MLWE correctness/security not re-proved.

Cramer–Damgård–Ishai, *Share Conversion, Pseudorandom Secret-Sharing and Applications to Secure Computation*, TCC2005. Institutional original publication https://ir.cwi.nl/pub/16467; DOI https://doi.org/10.1007/978-3-540-30576-7_19. Supports noninteractive unbounded Shamir pseudorandom sharings from pre-distributed PRF seeds; known PRIOR ART.

Benhamouda–Boyle–Gilboa–Halevi–Ishai–Nof, *Generalized Pseudorandom Secret Sharing and Efficient Straggler-Resilient Secure Computation*, ePrint **2021/1223**, https://eprint.iacr.org/2021/1223. Full Research MCP 59pp github-mirror SHA256 `fa604815b3e01bd2092b9872480683218d088bbc28a4e2e9ffa9fbd938ffbe67`, official parity VERSION_UNVERIFIED. Source §1.1 p5 and §3 pp16–18 construct seeded noninteractive, fixed linear combinations of PRF outputs, uniform correlated vectors over linear codes/finite-field spaces, optimized seed covering designs. Generalized linear correlation is ALREADY SOLVED; no original theorem directly constructing hidden-key-covariance-dependent discrete Gaussian padding.

## ONE hypothesis and falsification condition

**H:** Substitute conventional standard PRSS with its setup seeds and fixed local linear coefficients chosen independently of source FHE secret key s, without extra conditional sampling or communication, for the paper's Shamir-shared Gaussian padding. Reconstructed padding must exactly meet `D_(Z^n, σ0 sqrt(Bpub² I−Σ_s))` for every admissible s.

**Falsifier:** Two nonzero full-rank valid MLWE secrets that induce different target Gaussian shape matrices, since an s-independent PRSS setup/evaluator has the same output law at fixed sid under both, and cannot equal two distinct target laws. This is exact-distribution noncompatibility only, NOT proof of non-negligible statistical distance at all parameters.

## ONE exact ring test [DERIVATION]

Use `R=Z[X]/(X²+1)`, module rank k=1, n=2, secret coefficient bound Bmlwe=1, Bpub=4>sqrt(k n² Bmlwe²+1)=sqrt5. Two candidate secrets (each mat(s) invertible):
```
s_A=1,    S_A=[[1,0],[0,1]],      Gram=I₂,  σ_min=1.
s_B=1+X,  S_B=[[1,-1],[1,1]],     Gram=2I₂, σ_min=√2.
```
Thus source Gaussian padding shapes are
```
Σζ(A) = 15 σ0² I₂;
Σζ(B) = 14 σ0² I₂.
```
Both positive definite. Given original D_Z²,√Σ shape, the ratios of probability masses `P(e₁)/P(0)` are `exp(−π/(15 σ0²))` and `exp(−π/(14 σ0²))`, **unequal for every finite σ0>0**. Matrix products/positive definiteness checked via exact integer negacyclic multiplication; source dimension is an algebra toy not asymptotic security. A single s-independent output distribution cannot equal both targets. It is misleading to say 15I and14I are exact empirical covariance; they are PDF shape parameter matrices, proven distinct by likelihood ratio.

## Source-aware verdict

**FAIL:** Ordinary secret-key-independent-seed PRSS is NOT a direct substitute for conditional discrete Gaussian padding in Alg7, even though PRSS independently solves Shamir correlation missing in I184. Claiming generation of arbitrary random Shamir sharings by seeds as novel would rediscover CDI05 and 2021/1223.

**UNKNOWN:** A correlated conditional Gaussian sampler whose setup uses s privately (without revealing s or Σ_s to ≤T−1 corrupted participants), whose outputs match source's statistical/computational simulation, and whose online/storage cost beats pre-sharing O(LDec) noises. Also other Gaussian oversmoothing/flooding substitutions may alter q and security. This proof does NOT exclude them. No claim of original-paper error, real protocol insecurity or universal lower bound. PRSS sources apply uniform linear correlations; do not claim they proved Gaussian impossibility.

## End of Iteration 185

**STATUS:** FAIL exact drop-in s-independent PRSS hypothesis; PASS source prior-art check and two-key target Gaussian distribution mismatch; UNCLEAR secret-conditioned correlated Gaussian generation and concrete cost / security.
**RESULT:** Standard PRSS can precompute linearly correlated Shamir shares but cannot exactly supply BOTH s-dependent Gaussian targets using one s-independent random generator. Example Σζ=15σ0² I₂ versus14σ0² I₂, different likelihood ratios. Parent unbounded LDec gap remains open.
**NEXT_ACTION:** I186 NOT STARTED, human decides. Smallest next gate: can a **privately s-conditioned** correlated PRSS setup supply fresh target discrete Gaussians while coalition of ≤T−1 corrupted parties cannot infer `Σ_s`, and without O(LDec) stored Gaussian values? Check an explicit protocol/security definition before another toy calculation. If no credible private conditional sampler, PARK simple PRSS adaptation; consider other sourced targets.
**STATE_UPDATE:** YES.
