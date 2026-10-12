# Iteration 112 — Incomplete-NTT level changes require cross-register exponent mixing, not metadata-only bootstrapping-key reuse

Date: 2026-10-12. New independent full-text paper: Thales B. Paiva, Gabrielle De Micheli, Syed Mahbub Hafiz, Marcos A. Simplicio Jr., Bahattin Yildiz, *Faster amortized bootstrapping using the incomplete NTT for free*, IACR ePrint **2025/696**, primary research MCP full **24 physical pages**, GitHub mirror source URL https://github.com/arturo-kong/IACR-eprint-mirror/blob/master/2025/696.pdf, SHA256 `100140416417ad19daf56cc556713ce29d30c68780a9009d7d6234d36f68f85a`, git mirror revision `9e3c7187693fe7e51fd0e1ee969d32bb8a047773`, official latest VERSION_UNVERIFIED. Paper published at CHES/TCHES 2025/4 (author repository description). Original ePrint full contents pp1–20 read through MCP including §4 physical pp11–17.

## Read-before-write and one primary hypothesis
Read live AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md I111 and I111 source/correctness result. Prior sparse-SAB local terminal-sign erratum is already PARKED and preserved; do not reopen. Independently verified new paper entire needed §4 and pinned official author source.
[FACT] Paper §4.1 pp11–12 defines ℓ-incomplete transform with coefficients in the CRT factors of X^N+1; §4.2 physical pp13–14 derives base multiplication and ℓ≤lg N−α sufficient for no extra two-part inverse NTT arithmetic cost; §4.3 physical pp14–15 Algorithm3 requires `{Z_i}_{i=0}^{N−1}`, each a GSW encryption of `X^{−\hat{s}_i}` (sign convention may differ because code first converts to additive inverse). §4.4 physical pp16–17 uses these bootstrapping keys. Claimed 'incompleteness for free' is a **computation operation-count statement**, not a promise of free multi-level evaluation key portability; do not allege hidden author overclaim.
[FACT CODE] Public author repo `thalespaiva/incomplete_ntt_amortized_bt` pinned commit `3fd47c3215caea0a03feb8e9888cdd9831f0fba3`. `src/amortized_bootstrap_general.cpp` SHA `0368714b416df3c342e2dc8421bfc18e891f6ffe` lines 440–451 forms `s_dft` using `nc_ntt_forward(s_dft,...,rou_2nth,Q,N)` and emits one GSW ciphertext for each transformed coefficient; lines 468–489 choose root order `(2*N)>>NTT_INCOMPLETENESS` and generate the keyset; lines 454–465 similarly transform evaluation input a under current level. `src/forward_ntt.cpp` SHA `1bcb6ea869c3d941d21a8d6c4c34af72b05da5c1` uses global `NTT_INCOMPLETENESS` for stage count. This demonstrates configuration-coupled key generation, not inability to develop a conversion technique.
[HYPOTHESIS] Given full-NTT bootstrapping keys encrypting exponent values E_i=s(root_i) over fixed p, a PUBLIC PERMUTATION (even augmented by each register's public exponent scaling X→X^a and public shift X^b, i.e. affine one-input reweighting) suffices to obtain the ℓ=1 incomplete-NTT key exponent collection for the SAME p,N, without producing new GSW encryption or any cross-register homomorphic exponent combination.
[FALSIFIER] In a parameter set supporting BOTH levels, show at least one target incomplete coefficient necessarily depends on ≥2 independent full evaluation coordinates; even restricting to the paper's balanced ternary fixed-Hamming-weight key distribution, exhaustive affine one-input tests fail.

## Exact CRT conversion [DERIVATION]
Select N=4, prime p=17, root ζ=2 (ζ^4=−1 and ζ^8=1 mod17). Full ℓ0 CRT evaluation coordinates ordered as `E=(s(2),s(15),s(8),s(9))`, pairing ±roots (specific author's bit-reversal may reorder pairs; pairwise mixing invariant to permutation).
At ℓ1 the polynomial `X^4+1=(X²−4)(X²−13) mod17`. The incomplete representation is coefficient list
`C=(s0+4s2, s1+4s3, s0+13s2, s1+13s3)`.
For pair z,−z, CRT interpolation gives `c0=(s(z)+s(−z))/2`, `c1=(s(z)−s(−z))/(2z)`. Mod17:
`C=B E` with
`B=[[9,9,0,0],[13,4,0,0],[0,0,9,9],[0,0,16,1]]`.
Every row contains EXACTLY TWO nonzero values. Thus for arbitrary polynomial secrets no single input coordinate, public permutation, fixed scaling, or affine shift can yield target incomplete coefficient: B is not monomial (permutation*diagonal). This is a representation obstruction, NOT an encryption security claim.
In GSW exponent encoding `Enc(X^{−E_i})`, exponent mixing requires a homomorphic operation that forms `Enc(X^{−(uE_i+vE_j)})` from at least two encrypted monomial values, e.g. authors' homomorphic dot-product technique if applicable; simply adding two GSW ciphertexts encrypts a **sum of monomials**, not generally the desired monomial of exponent sum. Such conversion may be feasible but has cost/noise and is not provided for free by the public metadata layout.

## One exact minimal test [TEST PASS / HYPOTHESIS FAIL]
Python exact arithmetic source-compatible algebra (no cryptography). Check p17 root and all 4 basis secret polynomials. Exhaustively enumerate the N4 *balanced ternary Hamming weight 2* key distribution: one +1, one −1, 12 possibilities. All 12 satisfy `C=B E` exactly.
For each of 4 target coordinates j and 4 potential source coordinates k, exhaustively enumerate all (a,b)∈F_17² = 289 one-input affine maps `a E_k + b`, checking all 12 keys. **0/16 source-target pairs admit such a map**, even without requiring a single global permutation. Thus no source permutation + per-register affine exponent transform can derive the full ℓ1 key over the actual toy secret distribution.
Explicit s(X)=1−X: E=(16,3,10,9), C=(1,16,1,16). Polynomial-key supports the material independence proof; these are not arbitrary scalar vectors with impossible secret distribution.
The test does not assume an inaccessible full ePrint or PDF extraction correctness: CRT identities verified exactly and source paper inputs independently located. Toy parameters N4/p17 do not provide real FHE security and were chosen because the same p supports BOTH transform levels (so absence of full-NTT roots at smaller p cannot be blamed).

## Scientific assessment
**FAIL** metadata-only / single-register-affine cross-level bootstrapping-key reuse.
**PASS** exact CRT mixing explanation under fixed ring and paper-shaped secret distribution.
**NOT PROVED** key rotation levels cannot be supported under one enlarged key set, that no efficient conversion exists, that author implementation makes a mistake, or that conversion will dominate overall bootstrapping at practical parameters.
**RESEARCH RELEVANCE UNKNOWN**: operational level switching may not be needed; published experiments generate keys for each parameter setting. Most paper speed/DFR examples also CHANGE p, so even ideal same-p conversion may not apply. However published (N=1024,p=7681) supports ℓ≥2 and in principle multiple compatible ℓ values, making a fixed-p reuse scenario plausible, not demonstrated useful. Existing `homomorphic_dot_product` is prior art, so merely using it to convert exponent representations is NOT novel.

## Source-anchored possible next gate
I113 ONE minimal practical-cost gate: for SAME published (N=1024,p=7681) configuration with two supported incompleteness levels (ℓ=2 and ℓ=3), inspect pinned code and derive minimum needed extra GSW homomorphic exponent combination/key-switch work vs generating/storing two offline bootstrapping key sets. First ask if legitimate deploy scenario would vary ℓ without varying p; if no, PARK. Do not calculate 'memory saved' without concrete key bytes/parameter source and do not claim actual speed gain before noise/security and end-to-end benchmarking. This is not a generalized theorem statement about arbitrary p.

## Reproducibility and end-of-iteration
Executed Python file `/mnt/data/iteration112_ntt_keylevel_conversion.py` SHA256 `49722a330633b168d25d2e20405d8079052682e24997d53f2cd02022175c6a2c`.
JSON results `/mnt/data/iteration112_ntt_keylevel_conversion_results.json` SHA256 `f7a7406f6503d100757313f05254f439e0a365d49c0a26a1a931e51c4a4dc0a8`.
STATUS: **FAIL one-input key reindexing hypothesis; PASS precise structural obstruction; UNCLEAR nontrivial practical research impact**.
RESULT: original complete NTT keyed exponent values must be pairwise linearly mixed in exponent domain to form ℓ1 residues, not rearranged.
NEXT_TEST: I113 practical fixed-p multi-level key reuse relevance and cost gate.
STATE_UPDATE: YES. No author contact/email/outreach/public release.
