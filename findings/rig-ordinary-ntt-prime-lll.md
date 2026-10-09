# RIG: one certified NTT prime outside q=a^N+1

Date: 2026-10-10
STATUS: PASS (one explicitly certified, non-a^N+1 weak NTT prime)
NOVELTY: NOT VERIFIED; underlying polynomial-evaluation/short-dual-vector bias mechanism is prior art.
HUMAN: choose continue/refine/archive; no broad security claim.

## Primary falsifiable claim
For N=n=32, t=2, sigma=1, L=4, B=14, K=8, there is at least one prime q ≡ 1 (mod 2N), q>2H_L satisfying the 2026-09-10 RIG manuscript's sufficient correctness condition, with q NOT of the special family a^N+1, such that an explicitly recoverable Fourier relation vector v has sigma ||v||/q < 1/(4*pi). This guarantees genuine-coordinate Fourier bias >=7/8 and a constant single-challenge attack.

## Reproducible experiment, exact witnesses [FACT / EXPERIMENT]
Artifact: /mnt/data/fhe_audits/rig_ordinary_prime_lll_audit.py
Certificate: /mnt/data/fhe_audits/rig_ordinary_prime_lll_certificate.json
Requires sympy 1.14.0. One prime, one LLL lattice, no multi-parameter sweep.
Candidate-selection rule: smallest ODD c>=3 with q=c*2^160+1 passing BPSW/probable-prime screening; c=141. This candidate has an independent deterministic Lucas primality certificate, so the result does NOT rely on probabilistic primality.
q=206071730863657311466719561412995905771486488559617 = 141*2^160+1, 168 bits.
q-1=2^160*3*47, with complete prime factorization. Lucas generator 5: pow(5,q-1,q)=1 and gcd(pow(5,(q-1)/ell,q)-1,q)=1 for ell=2,3,47. This implies q is prime.
Not a^32+1 since q-1=141*2^160 is not a 32nd power.
r=pow(5,(q-1)/64,q)=158556721435192136949260275366676042636942017280341.
r^32=-1 mod q and r^64=1; exact order 64. Every odd power is an NTT evaluation point.
Correctness: H0=29, H_L=32^15*29^16; 2H_L=18908088956230290401794697920047243944689401856; q/(2H_L)=10898.601722293879.
For conventional D_1 noise whose pmf is proportional to exp(-x*x/2), union bound over K*N=256 error coefficients exceeding 14 is < 7.0981e-47 < 2^-128; check that the original manuscript's D_sigma convention is the same fixed-stdev model.
Lattice Lambda_r = {v in Z^32: v_k ≡ u*r^k (mod q) for some u}. Basis rows (1,r,...,r^31), q*e_1,...,q*e_31. Deterministic Sympy DomainMatrix LLL delta=3/4.
Chosen odd-u basis output row index 0; v0=-461634738411160921844397670245711543360041869, odd. ALL 32 congruences (v_k-v0*r^k) ≡ 0 (mod q) verified. Exact squared norm saved in certificate.
||v||/q=0.05344983437809674 <1/(4*pi)=0.07957747154594767.
Under independent centered coefficient Gaussian with variance <=sigma^2, beta>=1-2*pi*pi*(sigma*||v||/q)^2=0.943607354506818.
With p=N/(N+n)=1/2, user prior proof shows randomized one-coordinate challenge guessing Psuccess=1/2+p*beta*(1+cos(pi*v0/q))/4 >=0.7359018386237834.
No secret permutation needs recovering. This is a MATHEMATICAL LOWER BOUND conditional on the manuscript's noise model, not a Monte Carlo measurement.

## Scope & novelty constraints
- q uses a tailored Proth-type family c*2^160+1 to allow deterministic certifiability, rather than a uniformly random ordinary prime. It is 'ordinary' only in the explicitly intended sense of not belonging to q=a^N+1; do not claim typical/random 168-bit NTT prime vulnerability.
- N=32 is a toy/insecure dimension even without this technique. Demonstrates logical correctness/security overlap in the original toy setting, not practical security failure of a standard FHE parameter set.
- q is enormous compared with common per-limb RNS primes. It meets the user's manuscript's conservative deep-circuit correctness bound, but is not an established recommended parameter.
- One instance DOES NOT prove infinitely many ordinary primes are vulnerable, generic/average-case insecurity, or practical advantage at deployment dimensions.
- Short-relations/dual Fourier/evaluation-based nonuniform error are related to classical PLWE/RLWE prior art; Elias–Lauter–Ozman–Stange ePrint 2015/106 and 2015/758. Specific RIG hidden-permutation attack uses an elementary mixture lift; standalone novel methodology not established.
- The original conditional theorem 'hard restricted source => IND-CPA' is not refuted by finding one weak source-parameter choice.
- The manuscript's correctness bound is sufficient, not necessary.

## End of iteration
STATUS: PASS (one certified non-a^N+1 weak instance).
RESULT: stronger existence witness, not stronger generality/novelty.
NEXT_TEST: HUMAN_REVIEW: decide whether testing random/unstructured legal NTT primes at relevant bit length or full security dimensions could materially improve novelty. Current technical evidence favors a narrow parameter-warning note, not a new standalone cryptanalytic technique.
STATE_UPDATE: YES; see STATE.md.
