# BOOT B005 — Unbiased truncated gadget and prior-art gate

TRACK_ID: BOOT
ITERATION: B005
DATE: 2026-10-19
STATUS: PASS_ALGEBRA / UNCLEAR_FULL_DFR / PARK_P1_LOW_NOVELTY
RESULT: Randomized truncation at the existing d=3, B=128 balanced-digit shape is algebraically feasible. No demonstrated performance improvement over existing d=3 baseline.

## Hypothesis
Replacing the low-bit truncation with independent Bernoulli rounding preserves all gadget rows and may produce a useful subgaussian tail improvement that leads to genuinely cheaper block-binary TFHE.

## Evidence
Read 2023/958 Algorithm 2 and Lemma 1 (p.11), and pinned SNUCP/blockkey-tfhe source (tgsw.cpp and tgsw-functions.cpp) for signed digit layout. Read 2025/1892 Theorems 3.1-3.2 (pp.12-13). Read 2023/535 pp.1-5: practical randomized subgaussian gadget decomposition already established. FINAL 2022/074 Section 4.3 also uses randomized gadget decomposition. Search for 2022/1438 shows randomized external product, but full-text was not acquired, and is not treated as fully verified prior art.

## Minimal algebra
For a 32-bit torus word u=2048z+r (0<=r<2048), choose C=1 with probability r/2048, else C=0; set u'=2048(z+C) modulo 2^32. Use unchanged centered 3-digit base-128 gadget to represent u'. The lifted normalized error E=(u-u')/2^32 is r/2^32 or (r-2048)/2^32, with conditional mean zero and conditional variance r(2048-r)/2^64 <=2^-44. Hoeffding variance proxy also <=2^-44. Circular carry is represented by the same 3 gadget digits, each in [-64,63], without new TRGSW rows.
Exhaustive reference-integer checks for 4 distinct high-word configurations and all 2048 remainders: 8192/8192 candidates PASS for both rounding outcomes, digit range, modular reconstruction, zero weighted integer mean and variance bound. This is NOT native code execution.

## Conditional block noise
For fixed nonadaptive input, public exponents, and secret, independent fresh rounding coins for every accumulator coefficient yield block phase residual eps_j = E_b -t*E_a, with Hamming weight w<=k+N-n. Each block selector is zero or X^a-1. Hoeffding and signed permutation geometry give a conditional subgaussian variance proxy per extracted coefficient <=4(1+w)2^-44 for each block, hence V_round <=4k(1+w)2^-44 for k fresh independent blocks.
Using the separate favorable independent Gaussian key-error model V_key=8(2^-25)^2 n d N 64^2 with d=3,N=1024, a component-only bound P <=2exp(-(.125)^2/(2(V_key+V_round))) gives log2 upper bounds ell 2..6: [-198.92,-182.41,-158.94,-141.42,-127.89]. Only ell 2..5 reach below 2^-128 in this simplified one-shot model. This is NOT a proof of full FHE DFR, correct security, adaptive reuse, or actual measured tail: key switching, modulus switching, FFT errors and full adversarial model are excluded.

## Performance falsifier
Test d=2 with B=2^b, b=2..16, and same variance proxy V_round=4k(1+w)2^(-4b); V_key=8 beta^2 n*2*N*2^(2b-2). Best b=8 gives log2 Chernoff upper bounds about [-30.44,-38.59,-41.13,-41.81,-41.52] for ell=2..6, not enough to certify 2^-128. This does NOT establish a lower bound on true error; only the sufficient test fails. d=3,b=6 improves modeled noise but does not save levels or transforms. For ell=2 source n=630,k=315, this 32-bit stochastic decomposition consumes 2Nk=645120 independent 11-bit random draws per bootstrap, about 0.887 MB of random bits; no timing or security evaluation for RNG overhead.

## Prior-art and decision
Randomized subgaussian decomposition and its variance accounting appear in 2023/535, FINAL, and prior work; randomized external products are at least suggested by 2022/1438 search. Neither stochastic rounding nor a blockwise variance bound is established as a novel performant bootstrapping primitive here. PARK P1 (2023/958+2025/1892); no more iterations without clear real latency/key-size leverage.

NEXT_TEST: B006 — compare squared-gadget Mat-MGSW of 2025/1711 against heterogeneous approximate gadget of 2025/1892; one exact algebraic representation/interface falsifier before noise, cost, and security.
STATE_UPDATE: YES
