# I186 — Public/common Gaussian innovation breaks conditional privacy of a seeded threshold-padding candidate

**Date:** 2026-10-14. Human authorized continuation after I185. Read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, STATE.md (blob `28eff7f00755442290319027b28231f91382edae`), I185 archive and PRSS index. One primary falsifiable candidate and one joint-transcript test (formula, simulation, algebra sanity).

## Primary source and evidence

**[FACT]** Okada–Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ePrint **2025/409**, full40pp Research MCP GitHub mirror SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, official VERSION_UNVERIFIED. §2.4 physical pp10–11: `ζ` is hidden Gaussian padding with scalar scale `η(s)=σ0 sqrt(Bpub²−||s||²)`. Algorithm5 physical p23 and Definition5.4 p24: adversary corrupting fewer than threshold receives (ctdec, *all* pdi), and can query known µ, hence observe a reconstructed decryption residual. §5.1 p20 explicitly states parties broadcast partial decryption shares to participants; noncolluding Server sees none. Algorithm6 p26 sets `pdi=λ(a⋅s_i+ζ_i)+m_i`; its theorem proof p28 simulates distribution of revealed *residual* using independent, hidden ζ. Algorithm7 p29 has MLWE covariance `σ0²(Bpub²I−Σ_s)`.
**[PRIOR ART]** Benhamouda–Boyle–Gilboa–Halevi–Ishai–Nof, ePrint **2021/1223**, full59pp Research MCP GitHub mirror SHA `fa604815b3e01bd2092b9872480683218d088bbc28a4e2e9ffa9fbd938ffbe67`, official VERSION_UNVERIFIED, §3: noninteractive **uniform linear-space** PRSS; no conditional-Gaussian claim. Prior I184 independent PRF and I185 unconditioned PRSS gates archived.

## ONE hypothesis and decisive falsifier

**[H]** In a conditioned setup, Shamir-share the scale `η(s)` rather than O(LDec) Gaussian samples. For each session j take a common **public** Gaussian factor G_j, and participant i locally creates padding share `z_ij=η_i G_j`. Any qualified active set reconstructs `ζ_j=Σ λ_i z_ij=η G_j`. The ideal **continuous** Gaussian marginal is correct for scalar padding, so the source simulation proof supposedly carries over.

**[FALSIFIER — original simulator joint view]** Source Algorithm5 gives adversary ciphertext+all partial decryptions for known µ. Using the source Algorithm6 signs, the residual after subtracting the publicly known encoded plaintext is `Y=[b−Σpdi−floor(q/2)µ]_q=[E−ζ]_q`; source occasionally writes E+ζ *in marginal distribution* because fresh hidden symmetric ζ makes sign irrelevant. In ideal real/no-wrap continuous model, with `G∼N(0,1)`, `E⊥G` and E mean0, one has `Y=E−ηG`, so:
```
 E[Y|G=g]=−η g,     Cov(Y,G)=−η,
 η_hat=−Σ_j Y_j G_j / Σ_j G_j².
```
This exposes η to a joint-transcript observer when E is not overwhelming, **even if** Var(Y) is perfectly independent of s. Thus one cannot import a simulator proving only s-independent **marginal** residual. Asymptotic PPT advantage under source's high flooding variance and finite modq/discrete Gaussians remains **UNCLEAR**, so this is NOT a proved attack on original ThFHE or all candidate distributions.

**[Analytic concrete model]** With n2, coefficients bounded3, s_A=(1,0), s_B=(1,3), Bpub5 (Bpub²25>n Blwe²+1=19), σ0=1, let key-independent base-noise variance add F=1: `Var(E_A)=1+1=2`, `Var(E_B)=10+1=11`; `η_A=√24≈4.89898`, `η_B=√15≈3.87298`. Both outputs `Y` have identical ideal marginal normal law `N(0,26)`, but their joint covariance `Cov(Y,G)` differs. Seeded JS xorshift32 `0x8A12BC34`, Box-Muller, 4096 independent sessions gives `η_hat(A)=4.8930721`, `η_hat(B)=3.9100290`, empirical Y second moments25.9185263 vs26.0438407. This is illustrative CONTINUOUS arithmetic, not FHE simulation/security claim, and σ0=1 is not asserted to meet the original asymptotic smoothing requirements.

**[Same mechanism even if G is not broadcast]** In this **particular multiplicative local protocol**, corrupt party i knows both η_i and locally computed z_i=η_iG. For η_i≠0 in field Fq, it can compute `G=z_i/η_i` and then apply the same joint-transcript logic. Exact F101 2-of-3 witness: η7, Shamir sharing polynomial `f(X)=7+31X`, G13, shares η_i=(38,69,100), padding z_i=(90,89,88), any 2 reconstruct ζ91=(7*13)%101; corrupt party1 knows η1=38,z1=90 and computes `38^-1=8`, `G=90*8=13 mod101`. This tests only linear Shamir algebra; *not* exact discrete Gaussian shape (real multiplication not automatically valid in finite field).

## Interpretation and end of iteration

**STATUS:** FAIL direct claim that public (or locally recoverable) common-normal-factor conditional scale sharing preserves source simulator's secret-independent joint transcript; PASS conditional covariance derivation and exact field share checks; UNCLEAR actual source parameters, statistical/computational attack, source-compatible discrete Gaussian generation, overhead/security of sophisticated private correlated samplers.

**RESULT:** Correct Shamir reconstruction and ideal Gaussian *marginal* shape is insufficient. Jointly observing G and residue Y gives a key-norm-sensitive regression signal; even withholding a broadcast of G fails to hide it in the naive local product form from a corrupted party. No original paper flaw, no established novelty. Also source covariance in MLWE is a Gaussian *shape parameter*, not exact empirical discrete covariance.

**NEXT_ACTION:** I187 NOT STARTED; recommend PARK naive multiplicative conditioned-PRSS scale-share design. Parent standard-(M)LWE unbounded-LDec problem remains OPEN. Next human-approved smallest test should require an **explicit hidden-innovation correlated sampling functionality** where <T corrupted parties cannot reconstruct per-session Gaussian factor from their own local views, a source-compatible discrete covariance sampler and sim-security/cost proof; otherwise PARK seed-only line/pivot. **STATE_UPDATE:** YES.
