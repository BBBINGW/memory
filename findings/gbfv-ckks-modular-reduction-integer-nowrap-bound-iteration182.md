# Iteration 182 — Kim 2025/888 GBFV→CKKS approximate modular reduction: no integer-wrap counterexample under stated degree/size margin

**Date:** 2026-10-14 (JST). PI authorized new iteration with “好的，请继续”, following I181 recommendation to PARK naïve dBFV→BGV. Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` I181 blob `20b2507d180d0d89687b46c2a644bc1672a0ea2a`, `findings/OPEN_RESEARCH_BRANCHES.md`, I181 archive; selected a **different** source-accessible GBFV↔CKKS conversion correctness boundary. One hypothesis and one decisive integer-lift/no-wrap test including source algebra and numerical falsification attempts, not a new FHE scheme or performance benchmark.

## Primary sources and provenance

1. **[FACT]** Jaehyung Kim, *Bootstrapping GBFV with CKKS*, IACR ePrint **2025/888**, https://eprint.iacr.org/2025/888. Full **22 physical-page** Research MCP `github-mirror` PDF SHA256 `604a22c3abe24fe0c91f1fccf9b09c0599156b6d9e759a9f352f03262e14a8e3`, revision `a8676e14ed4f6205a6e0423020b547c50e9eeea4`, **VERSION_UNVERIFIED**. Original §4.1 Lemma1, Theorems 5–8 physical pp10–14 show `Flatten(m)+tI` message after GBFV-to-CKKS, ∞-norm `3(|b|+1)/2` and degree bound under `|m|≤|b|^ell`, `ell<N/k`, small error. §4.2 Lemma3–4, Algorithm3, Theorem9 physical pp15–18 study approximate modular reduction via replacing digit weights b^j by centered residues [b^j]_u then CKKS→GBFV, with `u<|b|^ell` and `ell<N/k−4`. Lemma3 ensures integer `Σ phi_j [b^j]_u ≡ Σphi_j b^j (mod u)`. Theorem9 claims result represents integer congruent mod u, with explicit smallness/degree hypotheses. Paper's own proof uses input no-wrap Lemma4 and gives a loose bound of order `(ell+2)*u` on output coefficients, but does not lay out the **geometric signed residue bound** below. No proof/claim of paper error or novel cryptography.
2. **[FACT context]** Robin Geelen & Frederik Vercauteren, *Better GBFV Bootstrapping and Faster Encrypted Edit Distance Computation*, ePrint **2025/1104**, https://eprint.iacr.org/2025/1104, full **22 physical-page** Research MCP GitHub mirror SHA256 `2128d7f5e568b6d66f71f6ad5f913baf34847103ef694246348d27d89ca0956f`, official latest VERSION_UNVERIFIED, source §3.2 source hybrid GBFV/BFV slot conversion, Table2–4 real baseline in different precision regime. Explicit code/regime limitation `ell < n'/n''` invalid GBFV automorphism and temporary BFV fallback is **already acknowledged in source** and not pursued as new research. Kim §5 pp19–20 already establishes the CKKS high-precision branch is ~18.4s at N2^16 while original GBFV BFV-based method is far faster at 16-bit plaintext (different ring/security denoising), so no unsupported broad claim “CKKS dominates GBFV”.

## ONE primary hypothesis and falsifier

**[HYPOTHESIS to falsify]** Even under Kim Theorem9's `ell < N/k−4`, `u<|b|^ell` and source's `||Phi||∞≤3(|b|+1)/2`, `deg Phi ≤ k(ell+2)−1`, the actual integer result of approximate modular reduction `Phi→Phi'→ev_{X^k=b}(Phi')` can exceed the centered GBFV plaintext interval `(−p/2,p/2)`, where `p=|b|^{N/k}+1`. If true, wrapping modulo p could alter the intended congruence modulo unrelated u, revealing a missing correctness condition.

**[FALSIFIER]** Starting from exact source coefficient/degree constraints, try all valid messages/target moduli at a genuine power-two cyclotomic toy; include permitted `tI` modular wrap components; then derive a *uniform algebraic upper bound* using centered remainders `r_j=[b^j]_u`. If uniform bound is strictly below p/2 for all B=|b|≥2, then proposed missing no-wrap condition FAILS.

## Exact source-based no-wrap proof — most useful durable result

Set `B=|b|≥2`, `n=N/k`, `p=B^n+1` (n is a relevant power of two so if b negative, b^n positive), `u<B^ell`, `ell<n−4`. Let `Phi(X)=Flatten(m)+t I`, as in source, and write coefficients `phi_{kj+i}` with j≤ell+1, i<k, all bounded by `A=3(B+1)/2` in absolute value (Corollary3/Theorem6). The map `LinTrans` of §4.2 replaces every weight `b^j` by a centered residue `r_j=[b^j]_u`. Because `r_j` is the centered representative of `b^j`, `|r_j|≤min(B^j,u/2)`. For any fixed coefficient of the low-degree `X^k−b`-evaluated integer output:
```
 y_i = Σ_{j=0}^{ell+1} phi_{kj+i} r_j,
 |y_i| ≤ A * S, S=Σ_{j=0}^{ell+1} |r_j|.
```
For ell≥2, split the **last four indices** j=ell−2,...,ell+1 (each |r_j|≤u/2<B^ell/2) from earlier j=0,...,ell−3 (each |r_j|≤B^j):
```
 S ≤ (B^(ell−2)−1)/(B−1) + 4u/2
   < (2+1/(B²(B−1))) B^ell.
```
For ell=0 or1, all 2 or3 residues individually obey |r_j|≤u/2<B^ell/2, so the same relaxed bound holds. Thus
```
 |y_i| < [3(B+1)/2]*(2+1/(B²(B−1)))*B^ell.
```
For ALL integers B≥2,
```
 3(B+1)*(2+1/(B²(B−1))) < B^5.
```
Proof: `2+1/(B²(B−1))≤9/4`, and `(27/4)(B+1)<B^5` for B≥2 (strict at B2:20.25<32 and increasing advantage for larger B). Since ell<n−4 with integer n, n−ell≥5, so p/2>(B^(ell+5))/2. Therefore the output integer `|y_i|<p/2`: **no centered plaintext-modulus p wrap** can invalidate the desired mod-u congruence at this stage.

This proves only an **integer output range property** under the source's norm/degree hypotheses and source-defined centered digit residues. It does NOT independently establish correctness of CKKS bootstrapping, precision, linear-transform approximation error, security, or ciphertext noise throughout transformations; Theorem7–8's precision and scaling assumptions must separately hold. It does NOT prove the original theorem flawed; it adds a clean missing-in-presentation range inequality and may be merely a proof clarification.

## One exhaustive integer toy check and admissible-I envelope

Parameters `N=16,k=1,b=2,n=16,ell=11,p=65537`, satisfying ell<n−4 and u<2^ell. For I=0, computed exact balanced `Flatten(m)` via `(X−2)^{-1}` on `Z[X]/(X^16+1)`, over ALL `m∈[−2048,2048]∩Z`, `u∈[2,2047]∩Z`, **8,382,462 cases**. For every case tested:
- actual translated integer `Σ phi_j [2^j]_u` is congruent to m modulo u;
- no |output|>p/2, maximum |output|=**1536**.
- To account for paper conversion term `tI`, computed per-coordinate possible I_j=±1, 0 conditional on a CKKS input coefficient's fraction `f_j` being beyond ±1/4 under source `|e_j|/q<1/4`; for each m and u optimized sign-compatible subset of I components to find worst possible integer output without enumerating exponentially many subsets. Maximum absolute output **3633**, again <p/2=32768.5; no wrap found. This is a generous envelope over per-coordinate input error choices near threshold and is NOT a complete CKKS ciphertext correctness test.

Independent deterministic algebra sanity checks on theoretical factor:
```
B=2: 3(B+1)(2+1/(B²(B−1)))=20.25 < 32=B^5
B=3: 24.6667 < 243
B=4: 30.3125 < 1024
B=8: 54.0603 < 32768.
```
For numeric toy the relaxed uniform result `|y_i|<4.5*2.25*2048=20736<32768.5`; actual admissible envelope 3633.

## Research verdict and novelty screen

**STATUS: FAIL** hypothesized hidden overflow correctness boundary: input conditions already ensure the relevant integer output fits uniquely in GBFV centered plaintext space. **PASS** a uniform geometric-series bound clarifying why `ell<n−4` suffices, plus exhaustive source-shaped small-parameter check and constrained I envelope. **UNCLEAR** all other aspects of original Theorem9 (CKKS approximation/security/noise/availability of effective u conversion) or novelty; no counterexample, not an FHE contribution.

**NEXT_ACTION:** **HUMAN_REVIEW / PARK simple Theorem9 overflow audit**. New research cannot stop at proving a published theorem's sufficient size margin. On PI continuation, pivot to a new source-verified nontrivial FHE challenge; candidates: GBFV very-high-precision CKKS-bootstrap conversion `2025/888` versus low-precision fast GBFV `2025/1104` under fair matched security/latency, or a genuinely novel CKKS/TFHE correctness/security mechanism, but do not claim parameter crossover or source flaws without matched implementation/evidence. Unavailable new 2026 papers `2026/2310` and `2026/1604` remain SOURCE-GATED; do not treat their abstracts as original PDFs.
**STATE_UPDATE:** **YES** — one new source-backed potential theorem-boundary gate resolved with a complete conditional no-wrap argument, source SHA, exact falsification test; closes simple concern without asserting a paper defect.
