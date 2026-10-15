# CGS-46 — Conditional variance no-go for independently centered local padding noise

Date 2026-10-15. Active PI-selected single CGS research target. CGS-45 last completed at start. ONE primary hypothesis and ONE decisive elementary moment test. This is a RESTRICTED candidate impossibility, NOT an original Okada–Takagi attack, nor a no-go against general PRSS/PCF.

## Hypothesis H-CGS46: FAIL in a precisely restricted model

Could parties replace all per-session stored Gaussian shares of Okada–Takagi Algorithm 6 / 7 by independent local, share-dependent centered Gaussian contributions using ONLY: each own random Shamir share of the FHE key, an independently assigned secret PRF seed, public sid and secret-independent public parameters, with NO shared/correlated Gaussian seed and NO extra communication? The target Gaussian should depend on the whole master FHE secret s through Bpub squared minus ||s|| squared (scalar), or Bpub squared I minus Gram covariance Sigma_s (module).

Primary falsifier: Compute the SECOND MOMENT of the sum of independent centered local contributions after averaging the random Shamir sharing slope. If each individual share is uniform independent of s, the expected local variance cannot depend on s, unlike the required target distribution.

## Original paper / previous failures [FACT]

Okada and Takagi, Low Communication Threshold FHE from Standard (Module-)LWE, ASIACRYPT2025, ePrint2025/409 https://eprint.iacr.org/2025/409, full newer 40-physical-page Research MCP original PDF SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301, VERSION_UNVERIFIED. Algorithm6 physical p26 samples fresh scalar integer Gaussian zeta per sid with width sigma0 sqrt(Bpub squared minus ||s|| squared); PartDec returns lambda_i (a^T s_i + zeta_i) + PRF_i. Algorithm7 physical p29 samples the correlated integer Gaussian with shape Bpub squared I minus Sigma_s, and requires arbitrary T-out-of-N Shamir padding shares. Algorithm3 pp19-20 has original two broadcast phases. The proposed independent centered local Gaussian is NOT in the source original.

CGS10–15 already checked published public-key PCFs and missing secret-conditioned external FHE master-key binding; CGS16–17 checked Noah's Ark real subset-shared PRSS seed count and modulus gaps; CGS18–19 interactive rounding prior art; CGS20 linear-key PRF publicly distinguishable; CGS21 naive nonlinear Shamir local rounding fails qualified-set consistency; CGS22–33 structured-covariance and flooding branches; CGS39–45 interactive Gaussian MPC is an explicitly relaxed branch recommended PARK. This iteration tests the narrower INDEPENDENT-CENTERED local output class, not those stronger mechanisms.

Relevant prior art: Ishai NIST CSRC 2020 pseudorandom correlation generators talk https://csrc.nist.gov/Presentations/2020/mpts2020-2a3 distinguishes PRSS with correlated pre-established seeds and PCGs for nonlinear correlations. True PRSS/PCF are specifically EXCLUDED by our independence assumption, hence cannot be disproved by the following moment theorem.

## General conditional-variance theorem [DERIVED]

The simplest 2-of-2 Shamir instance has secret scalar s over an odd prime field F_q, random slope a uniform F_q, and evaluation points -1 and +1. Party shares X=s-a and Y=s+a. Conditional on every fixed master secret s, both X and Y are individually UNIFORM over F_q (but jointly correlated).

Let U=F1(X,R1) and V=F2(Y,R2) be integer-valued, already Lagrange-weighted local padding contributions. R1 and R2 are independent private randomness conditional on the shares and independent of the sharing slope. For EVERY x,y, local outputs are centered E[U|X=x]=0, E[V|Y=y]=0. Let h1(x)=E[U squared|X=x], h2(y)=E[V squared|Y=y] be arbitrary nonnegative share-dependent functions. Conditional independence yields E[UV|X,Y]=0. Therefore

Var(U+V|s)
= E_a[h1(s-a)+h2(s+a)]
= (1/q)sum_{x in F_q} h1(x) + (1/q)sum_{y in F_q} h2(y),

which is EXACTLY independent of s.

This holds even if each party varies its local Gaussian variance arbitrarily as a function of its own Shamir share. A separate independent centered fixed public-noise source changes the variance by a secret-INDEPENDENT amount only. For vector Shamir shares uniform on R_q^k, the conditional covariance matrix of independent centered vector local outputs is likewise independent of the full master secret by the same averaging argument.

But the ORIGINAL intended raw integer lattice Gaussian D_Z,sigma0 sqrt(Bpub squared minus s squared) has secret-dependent exact pmf and variance. For illustrative Bpub5,sigma0=8, secret 0 gives probability at integer zero 0.0250000 while secret 1 gives 0.02551551815. So a SECRET-INDEPENDENT conditional second moment cannot produce both target Gaussian laws.

The theorem concerns RAW pre-mod-q integer output and its true variance. It is NOT a proof of an adversarial distinguisher against the original ciphertext/rounded/mod-q adaptive transcript, does not rule out nonzero local conditional means (correlation via randomized sharing), shared public or secret random coins, correlated PRSS/PCF seeds, ciphertext-dependent noise, interactive MPC, or computational rather than statistical compensation. It is not a universal lower bound or publishable novelty result.

## One exact executable test [PASS]

Reproducer /mnt/data/cgs46_independent_local_zero_mean_gate.py SHA256 30739b721910bb611c7b142e8cd1f57b3d143e726d35bcfd837c051058e90078.
JSON /mnt/data/cgs46_independent_local_zero_mean_results.json SHA256 9e6301b1fe6ff17357ab86fab7edc0c0701fa1fae51e7bfc8fe1b1e988a54980.
Enumerate ALL 257 Shamir slopes for each bounded scalar master secret s in {-1,0,+1}; use centered local symmetric random-sign outputs with deliberately SHARE-DEPENDENT amplitudes f1(x)=1+(abs(center(x)) mod3) and f2(y)=1+(center(y) squared mod3). Each is centered under independent local sign coins. For every secret, exact total second-moment numerator is 1976, denominator 257; identical conditional variance ~7.6887 despite varying local variance functions. Source target discrete Gaussian probability at zero differs 0.0250000 versus 0.0255155. Initial separate Q17 run likewise had identical 136/17=8 moments for s=-1,0,+1. At share-corner X,Y in {-1,+1}, the target variance width Bpub²−((X+Y)/2)² has mixed 2-by-2 difference -2, whereas local additive variance has zero mixed difference. Corner-only test is not a typical-KeyGen proof, since selected slopes can be negligible in probability for exponential q; full Shamir slope average theorem is primary.

## Status, source gap and next action

CGS-46 STATUS: FAIL independent local centered Gaussian-share candidate; PASS exact conditional variance theorem and q257 full-slope test; HUMAN_REVIEW original strict CGS open. This restricted theorem is elementary and not independently publication-worthy. The repeated 46-iteration exploration has not identified a source-respecting two-round, arbitrary T-out-of-N, standard MLWE, polynomial-memory on-demand secret-conditioned Gaussian primitive.

DECISION RECOMMENDATION: PARK current CGS candidate search rather than inventing more independent-noise or minor Gaussian variants, unless PI brings a NEW named noninteractive secret-conditioned correlation primitive with cryptographic setup and a credible joint-view simulator. The PI can pivot to another promising FHE paper gap, or explicitly accept additional assumptions/communication with a cost benchmark. PI retains final decision. Next CGS-47, if continued, should be one bounded GO/NO-GO prior-art+contribution review, not another loosely motivated toy design. No other FHE target states modified. STATE_UPDATE YES.