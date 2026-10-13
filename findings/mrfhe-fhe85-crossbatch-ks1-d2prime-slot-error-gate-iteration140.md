# Iteration 140 — FHE(8,5): a one-coefficient cross-batch KS1 error can become ≈201 slot error after D₂′ PCMM

**Date:** 2026-10-13. PI explicitly authorized I140 by “好的，请继续” after I139. Primary source: Cheon, Hong, Kang, Kim, Kim, Lee, Lee, *MRFHE: Mixed-Radix Fully Homomorphic Encryption with Better Batch Bootstrapping*, ePrint **2026/853**, https://eprint.iacr.org/2026/853.

**STATUS:** **FAIL** a tempting *constant-factor/no-W-axis-amplification noise-budget shortcut*; **PASS** source-dimensional exact W-axis algebraic witness and explicit ideal-rescale sensitivity; **UNCLEAR/HUMAN_REVIEW** real K2 complete noisy CKKS feasibility. Do **NOT** claim original paper's theorem is wrong, that actual K2 fails 128-bit security/precision, or that two genuinely noisy switching keys and Lattigo were implemented.

## Read before write and source

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, current `STATE.md` (after I139 SHA `18e037c0f59b74a637d4d088f8abaf44aafc5cb4`), `findings/OPEN_RESEARCH_BRANCHES.md`, I139 `findings/mrfhe-source-table5-multibatch-dense-ks-frontier-iteration139.md`, and I33–I35 MRFHE noise and dense second-switch archives. Original full 18-page PDF `2026-853.pdf` was fetched from the user's **ChatGPT Library**, not the Research MCP ePrint endpoint; physical pp9–12,16,18 inspected (the 2026-10-13 I139 and I140 session). Version relative to latest official ePrint PDF not byte-verified.

- §5.1 physical p9: `S^(omega)=Z[omega][W,Y,U]/(W^d−omega,Y^d−omega,U^(2n1)+1)`, `d=n2/2`.
- §5.2 **Algorithm 1 physical p10**: `star → Switch(s*→s) → d′2 circledast ct1 [PPMM] → Switch(s*→s) → Rescale(Δ)`. `star` swaps W and Y and sends monomial Y^a to W^(−a).
- **Proposition 5.7 physical p10 / Appendix D.2 pp15–16**: normalized PCMM maps the W-evaluation vector of each fixed Y-coefficient by **left multiplication with the d×d matrix D′2**, with entries `(eta_i^j)_{i,j=0,...,d-1}` and `eta_i^d=omega`; D′2 is the **unnormalized** principal Fourier-like Vandermonde block. The encoded plaintext kernel `d′2=Ψ^(omega)−1({d D′2})`, so integer scaled versions lead to a D′2 transform after output rescale.
- §5 Table5 physical p18: original source FHE(8,5) `w2=8,w3=5,n1=2^6=64,d=3^5=243,n2=486,N=62208`, logPQ=1658, dnum=5, dense source secret weight h31104 and temporary sparse h32. **Original Table4 does not benchmark K2/3 extra auxiliary packing under FHE(8,5)**. Source security estimate applies only to its original schemes/inputs, not automatically K2/3.

## ONE primary technical gate

[HYPOTHESIS / FALSIFIER] A naive completion of I139's conditional dense-KS cost model might **carry I34's small coefficient-wise first-switch error unchanged into the final CKKS evaluation-slot error budget**, because D′2 acts separately on each Y batch and exact rescale nominally restores ciphertext scale. **Falsify** this noise-no-amplification shortcut with one legitimate unit-coefficient KS1 error contributed by the *additional K2 batch* and compute the exact D′2 image in actual source d243; include second KS with zero extra error and an explicitly IDEAL exact-integer rescale to isolate the W-axis effect. This is a **necessary headroom test**, not the full I139 conjecture that *some* noise-safe source parameter chain exists.

## Valid ring-level cross-batch contribution into a target Y⁰ component

Use first source batch Y^0,...,Y^63 and second Y^64,...,Y^127. Consider a legal *additional ciphertext component* `δa=Y^64` under an unrestricted common original secret s(W,U), with `δb=−δa s(W,U)`, so **its semantic plaintext is zero**; no W-constant-secret weakening. This is a constructed (not statistically typical) RLWE ciphertext relation.

Because source `star(Y^64)=W^(−64)`, choosing one zero-level balanced gadget digit `g_0=W^(−64)` and a corresponding **small monomial switching-key error** `ε_0=W^64` gives
```
 δE1 = g_0 * ε_0 = W^(−64) W^64 = 1
```
in `W^243=omega`. In the canonical power basis `W^(−64)=omega^(−1) W^179=(-1−omega)W^179`, which has coefficients -1,-1 in the omega basis and fits a signed gadget digit at this low level. The error term `ε_0=W^64` has one coefficient1. Other key errors and original input errors are set zero **only for isolation**, not claimed to match an actual secure-key sample distribution. This is source-ring-compatible algebra and one specific allowed sparse error realization, not a typical sampled noise estimate. The K1 baseline's added component is absent.

After first switch the *incremental* decrypted error in Y⁰ is `1`. Proposition 5.7 then gives the D′2 action. Since `ψ^(omega)(1)=(1,...,1)`, 
```
 D′2 * (1,...,1)^T = (H(eta_i))_{i=0,...,242},
 H(W)=1+W+W²+...+W^242.
```
This is **exact** because the RHS `H(eta_i)=Σ_{j=0}^{242}eta_i^j` equals the row sum of `D′2`. The after-PPMM error polynomial is **dense in all 243 W power coefficients**, each coefficient equal1 (coefficient infinity norm remains1). Yet the CKKS canonical evaluation slot at `eta_0=exp(2πi/729)` has magnitude
```
 |H(eta_0)| = |1−omega|/|1−eta_0|
            = sqrt(3)/(2 sin(π/729))
            ≈ 200.9600043988338.
```
This is the claimed **slot-norm amplification** of a *single auxiliary KS1 error of coefficient norm1* and therefore invalidates equating first-switch coefficient norm with final per-slot error without W-transform accounting. It does **not** imply a real output loses 7.65 precision bits: actual scale/noise and coefficient-to-slot transforms must be included, and this adversarial error might have very low probability.

To isolate the second switching, set its fresh switching-key error to zero (its algebraic secret-switch relation still holds); the *decrypted message+error* after switch2 retains the above transformed error, independent of how dense its input is. For the rescale stage, an illustrative plaintext-kernel multiplier `Δ=2^20` yields formal coefficient difference `Δ H(W)` before rescale, and exact division of these integer coefficients by Δ yields `H(W)` again. **WARNING:** This is only an **ideal exact-divisibility check on the decrypted difference**. Actual CKKS `Rescale(ct3;Δ)` rounds the two ciphertext components separately and can add secret-weighted rounding error; the test neither simulates that nor the original modulus prime schedule, full random keys, Gaussian noise, or RNS decomposition. Do NOT label it a full encrypted Algorithm1 test.

## Exact reproducible W-axis field and numeric checks

A self-contained **41-line** Python check was executed, source `/mnt/data/i140_mrfhe_waxis_noise_gate.py` SHA256 `8ae771a6e0e9e839a7d4f2c8067774e979a6158a41582443cd28c1529e1d63e7`. It tests:
- `q=2251799815574017` verified prime, `q≡1 mod(729*256)`; supports primitive 729th W roots, primitive 256th U roots, and `omega^3=1`. A **synthetic 52-bit modulus**, not the precise Table5 chain or full CRT/RNS installation.
- `eta=2009145358644053` (order729), `omega=194173253097193`, `u=262351006200414` (order256). Exactly evaluate all 243 rows of D′2 times ones, match each to `H(eta_i)` with `eta_i=eta*(eta^3)^i`, including the geometric-sum formula, and assert all 243 field evaluations are nonzero. The first row is `556789408361591 mod q`. 
- Assert `W^(−64)W^64=1` using W^243=omega, `H(W)` has exactly 243 coefficients of1, and ideal Δ=2^20 coefficient-divisibility rescale reconstructs exactly the coefficient vector all ones without wrap (Δ≪q/2).
- Independently calculate the **complex** canonical slot0 `|H(exp(2πi/729))|=200.9600044`. These are separate finite-field *algebra* and complex *precision* views; do not interpret finite-field residue 556789408361591 as a CKKS error magnitude.

Minimal reproduction:
```python
import math, cmath, sympy as sp
d,n1,q=243,64,2251799815574017
assert sp.isprime(q) and (q-1)%(729*256)==0
g=sp.primitive_root(q); eta=pow(g,(q-1)//729,q)
omega=pow(eta,d,q); xi=pow(eta,3,q)
assert omega != 1 and pow(omega,3,q)==1
assert pow(omega,-1,q)*omega%q == 1
for i in range(d):
    r=eta*pow(xi,i,q)%q
    h=sum(pow(r,j,q) for j in range(d))%q
    assert h==(1-omega)*pow(1-r,-1,q)%q
z=cmath.exp(2j*math.pi/729)
gain=abs((1-cmath.exp(2j*math.pi/3))/(1-z))
assert abs(gain-200.9600043988338)<1e-8
scale=2**20
assert [x//scale for x in [scale]*d]==[1]*d
```

## Decision and missing full source gate

- **[PASS, precise]** W-axis cross-batch error propagation CAN be `200.96` in one complex slot while the input switching error has coefficient infinity norm1. Error polynomial after D′2 becomes dense W sum, even though the plaintext per-Y batch transform remains noninterfering. This is NOT a genuine source error: it is the ordinary DFT/Vandermonde slot-domain amplification phenomenon and the allowed cross-batch KS noise already visible in I33.
- **[FAIL]** Any attempt to transfer I34's `||E1||_coeff∞` unchanged to **CKKS evaluation-slot precision** for the complete PCMM, or to claim rescale necessarily removes the amplified noise, is unsound. A factor dependent on source `D′2` (and honest transformed source noise plus second KS/rounding) is needed.
- **[UNCLEAR / HUMAN_REVIEW]** Does **typical** source FHE(8,5) K2 error materially lower precision? We did not implement or simulate secure Gaussian gadget keys in the full 15M-rank S^(omega), the second dense *nonzero* KS2 noise, source RNS rescale, modulus-consumption/security reestimate, or conversion cost. A rare/error-designed polynomial cannot determine average performance or required modulus. The paper's 1658-bit logPQ is composite and does not specify an independently validated K2 precision tolerance; no original FHE(8,5) K2-batch benchmark.
- **[NOVELTY]** This is an elementary amplification counterexample under published DFT algebra, conceptually already known. I139's packing cost advantage remains an unverified conditional scheduling opportunity, not a new algorithm or submission.
- **[NEXT_RESEARCH_GATE]** Do not spend more iterations on isolated input support or toy DFT errors. To honestly decide source-parameter K2 viability, obtain an original Lattigo implementation/parameter transcript with real scale, switching-key error distribution, actual key-switch decomposition and rescale sequence, then perform **one comparative K1/K2 full Algorithm1 noisy measurement** of extracted coefficient and canonical-slot errors at each stage using matched common original key and switching keys. If source executable evidence unavailable, mark **MISSING IMPLEMENTATION/UNCLEAR** and consider PARK this low-novelty extension rather than fabricate fidelity.

## End of iteration

**STATUS:** PASS exact ring/evaluation sensitivity; FAIL naive coefficient-to-slot noise-isolation shortcut; **UNCLEAR** full K2 precision/latency/safety feasibility; HUMAN_REVIEW.
**RESULT:** At actual source shape FHE(8,5), a legal additional Y^64 batch input can contribute 1 to an existing batch's KS1 error; D′2 maps its all-ones evaluation vector to H(W)=ΣW^j, yielding **200.9600× max complex-slot error** despite small coefficient norm. Zero-added-noise KS2 and ideal exact-divisible rescale do not remove it. Exact q52 and complex numerical checks PASS. This is NOT a full source CKKS run.
**NEXT_ACTION:** PI decides: (a) if full source Lattigo implementation and noise/RNS details can be obtained, authorize I141 ONE matched K1/K2 complete noisy auxiliary-PCMM test and measure source precision/cost; (b) otherwise PARK this unproven and likely low-novelty multibatch scheduling branch, keep I139 conditional cost plus I140 precision obstruction in opportunity backlog. No author contact or background work.
**STATE_UPDATE:** YES — source-sized noise headroom condition changes branch risk and next test; preserves full cost window separately.
