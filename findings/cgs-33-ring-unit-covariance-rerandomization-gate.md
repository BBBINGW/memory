# CGS-33 — Exactly distribution-preserving ring-unit self-reductions cannot decorrelate secret Gram covariance

**Date:** 2026-10-15. **PI active research:** CGS (single root STATE). Prior CGS-32 left a fixed/persistent dummy covariance `Σ_{S'}` as an unproved computational simulator option. **ONE primary technical hypothesis, ONE cheapest decisive algebraic/enumeration test.**

## Primary hypothesis [FAIL for the named transformation class]

**H-CGS33:** Existing standard (Module-)LWE self-randomization by multiplying the unknown ring secret by an independently sampled invertible ring unit `u` and compensating in the public uniform multiplier can change/couple the actual Gram covariance enough to justify a persistent independent dummy covariance without assuming known-covariance MLWE, WHILE keeping the original independent identically distributed small-secret law and LWE error unchanged.

**Test/falsifier:** Select the valid bounded iid **uniform ternary** source secret law `χ=U({−1,0,1})`, and examine every invertible *integer ring-linear* transformation that exactly preserves `χ^n` as a distribution. Determine whether **any** such transformation changes `Gram(s)` for an input s. If not, the particular public-key self-randomization cannot erase key-covariance correlation. k=2 module case analogously includes signed-monomial component permutations.

**STATUS:** FAIL for this explicit measure-preserving ring-unit route; PASS general theorem + exact toy. This does **NOT** refute all computational reductions or dummy covariance hybrids under standard (M)LWE. No original FHE attack or publishable new primitive.

## Original and latest source provenance [FACT]

- **Okada–Takagi**, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025, ePrint **2025/409**, https://eprint.iacr.org/2025/409. Retrieved full 40-physical-page original text via Research MCP, PDF SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, VERSION_UNVERIFIED. **§2.2 physical p8** explicitly says the *known-norm scalar LWE* hardness reduction is known, whereas known-covariance Ring-LWE lacks a standard-RLWE reduction. **Algorithm2 p17**: native module secret `s∈R_q^k` sampled independent coefficientwise `χ_mlwe`, public matrix uniform and error from source χ. **Algorithm5 p23** adversarial oracle releases entire active (ctdec, all pdi), KeyGen secret fixed across sids. **Lemma7.1 Eq25 p30**, secret-induced ring covariance `Σ_s=Σ_i Gram(s_i)`. This iteration's χ uniform ternary is a CONCRETE instance of a full-cube iid small-secret law, not a claim that every allowable source distribution is uniform ternary or satisfies all original smoothing parameter bounds automatically.
- **Micciancio–Suhl**, *Simulation-Secure Threshold PKE from LWE with Polynomial Modulus*, ePrint **2023/1728**, https://eprint.iacr.org/2023/1728. **Freshly read ORIGINAL full text** via Research MCP, version status VERSION_UNVERIFIED (GitHub PDF mirror). **§3.2 p10, Definition 10 + Lemma 9**: actual scalar known-norm LWE leaks **`||s||²+||e||²`**, NOT merely `||s||²`. Reduction to ordinary small-secret LWE uses GUESSING the polynomial-sized norm for the **search** problem; for decisional follows a specialized leakage-aware search-to-decision reduction given in Appendix B, NOT ring-unit covariance self-randomization. **§5.3.2 p16, Definition 12**: the *separate* known-covariance RLWE assumption leaks `s s* + Σ_i e_i e_i*` and authors explicitly say ordinary ring hardness equivalence is left open. Their actual auxiliary covariance includes public-key errors, whereas the CGS dummy target `Σ_s` is secret-only. Do not silently equate definitions.
- **Okada–Takagi**, ePrint **2024/239**, https://eprint.iacr.org/2024/239, authors' earlier error-sharing construction from standard RLWE, **WITHDRAWN 2025-03-04** as shown in ePrint metadata. Not used as a security theorem here. It illustrates that new pre-shared secret/error-conditioned randomness—not trivial unit self-randomization—was an already published technique.
- Search in Oct 2026 also finds *Careful with the Ring! Concrete Hardness Gaps Between LWE and MLWE*, CRYPTO 2026, https://doi.org/10.1007/978-3-032-35377-1_15, on security-estimator gaps. It does not establish the specific known-covariance reduction or any impossibility relevant here.

## Exact self-randomization and covariance gate [DERIVATION]

Work with `R=Z[X]/(X^n+1)`, `R_q` for odd q, and secret distribution `χ^n` where each coefficient is **uniform** in {−1,0,1}. Given `(A,b=A s+e mod q)`, for a unit `u∈R`, put
```
s' = u s,    A' = A u^{-1},    b'=b;
A' s' + e = A u^{-1}u s+e = As+e.
```
For any fixed public invertible `u mod q`, `A'` is uniform whenever `A` is uniform. The actual question is whether `s'` still has EXACT original `χ^n` law and `Gram(s')` differs from `Gram(s)`.

### General lemma: all exactly uniform-ternary-preserving integer ring multipliers are signed monomials

Let M∈GL_n(Z) be the integer coefficient matrix of multiplication by u. Exact pushforward of uniform `χ^n` to itself implies the SUPPORT cube `S_n={−1,0,1}^n` is mapped bijectively onto itself. Hence `M S_n=S_n`, so for each integer row r of M,
```
max_{x∈S_n} |r x| = sum_j |r_j| <= 1.
```
Because M is invertible, no row is zero; therefore every row has EXACTLY ONE entry ±1, others zero. Invertibility forces these nonzero entries to occupy distinct columns. Therefore M is a **signed permutation matrix**.

For a ring multiplier, its first column is `vec(u)`; as M is signed permutation, `vec(u)=±e_j` for some j. Thus `u=±X^j`. Conversely, multiplication by these signed monomials is a signed negacyclic permutation and preserves uniform ternary χ exactly.

Since multiplication by a signed monomial u has `u u^*=1`, with involution `a^*(X)=a(X^{-1})`,
```
Gram(us)=mat(us)mat(us)^T
        =mat(u)mat(s)mat(s)^T mat(u)^T
        =mat(s)mat(s)^T
        =Gram(s).
```
The equality uses commutativity of ring multiplication and orthogonality of signed-monomial mat(u), or the ring identity `(us)(us)^*=u u^* s s^*=s s^*`. **Entire actual covariance is an exact invariant**, not just approximately correlated.

**Module rank k≥1 extension:** Suppose U∈GL_k(R) and its integer coefficient representation sends the FULL uniform ternary cube `S_{kn}` bijectively to itself. It too must be a signed permutation matrix. Ring R-linearity forces U's nonzero blocks to be signed monomial ring matrices and each input/output secret component to be permuted with one signed monomial factor (wreath-product structure). Hence `s'_i=±X^{t_i}s_{π(i)}`, and
```
Σ_{s'}=Σ_i Gram(s'_i)=Σ_i Gram(s_i)=Σ_s
```
EXACTLY. The corresponding uniform public vector transforms by inverse transpose U, preserving MLWE inner-product `A^T s`, and error remains unchanged. This covers a meaningful k=2 version directly matching source §7.

**Where the proof stops:** It applies to *linear coefficient-integral ring/module automorphisms individually preserving uniform iid ternary χ exactly*. It does not address nonuniform or dependent χ, transformations that alter χ with a new reduction, general public-key rerandomization that regenerates enc/evk, computationally hidden randomized secret shifts, noisy approximate invariance, high-error large-mod-q transforms, or impossibility under generic standard MLWE. For a mod-q-only transform the integer cube-support argument needs a no-wrap condition and is not claimed here. The source's full parameter and evaluation-key requirements are NOT inherited merely from public algebraic sample preservation.

## ONE small parameter exhaustive validation [EXECUTED]

Script `/mnt/data/cgs33_ring_unit_covariance_gate.py`, SHA256 `a68f3bf68e55db74fc94541a960903d2aa0d408478c805b7ebf7f8bf7be8478a`, JSON `/mnt/data/cgs33_ring_unit_covariance_gate.json`, SHA256 `b2913b48066fb4af4d67b49575b35637aef4d0b48681cec22d056b4ee9bf8fe2`. Tested the COMPLETE set of candidate ternary multiplier coefficient columns at n2 and n4 and all possible ternary secrets, requiring the induced map be BIJECTIVE on the full support (a zero multiplier mapping into support is NOT a valid rerandomization; filtered out).

| n | tested candidate multiplier vectors 3^n | preserving maps | exactly ±X^j count 2n | do preserving maps change Gram? |
|--:|--:|--:|--:|:--|
| 2 | 9 | 4 | 4 | NEVER |
| 4 | 81 | 8 | 8 | NEVER |

Toy n4 shows covariance genuinely changes across different secret choices: s0=1 -> Gram(s0)=I4, while s1=1+X -> Gram(s1) has diagonal 2 and nonzero off-diagonal entries, explicitly output in JSON. For q=257, tested fixed `u=X`, inverse `u^-1=−X^3`, and `(A',s')`; exact `A' s'+e=A s+e mod257`, `Gram(s')=Gram(s)`. Also tested k2 source-module example with `(s'_0,s'_1)=(X s_1,−s_0)`, matching inverse-transpose public vector; all decryption equations and summed covariance conserved.

This is a controlled algebraic toy + an unconditional restricted-class proof, NOT an algorithm solving or attacking RLWE, nor a zero-knowledge proof or FHE implementation. No empirical lattice estimator necessary to refute this algebraic bridge.

## Auxiliary-input computational reduction gap, distinguished from our local failure

The native target
```
(PK(S),Σ_S) ≈c (PK(S),Σ_{S'})
```
could follow for native PK from **known-covariance MLWE** `(A,AS+e,Σ_S)≈(A,U,Σ_S)`; this is a STRONGER assumption than normal MLWE `(A,AS+e)≈(A,U)`. Known-norm scalar LWE has a specialized proof path (Micciancio–Suhl Lemma9) involving guessing norm and search-to-decision; the ring covariance contains many coefficients and this exact proof is not ported by ring multiplication. A signed monomial merely relabels secret coefficients; because Σ is invariant it CANNOT manufacture `Σ_{S'}` independent of `PK(S)`.

Even if a clever non-unit transformation could prove the native PK-only computational hybrid, original §7 exposes evaluation keys and multiple adaptive ODec transcripts, so further proofs would remain. Do not treat the restricted self-randomization obstruction as global separation between regular MLWE and known-covariance MLWE.

## End of iteration

- `ITERATION: CGS-33`.
- `STATUS: FAIL` straightforward distribution-preserving ring-unit/GL_k(R) self-randomization to decorrelate Σ; `PASS` exact signed-permutation/no-Gram-change lemma and complete toys; `UNCLEAR/HUMAN_REVIEW` any other computational reduction or full dummy-covariance simulator.
- `RESULT:` Any exact ternary-cube-preserving integer module linear key transformation is component signed-monomial permutation; covariance **never changes**, despite correct uniform public multiplier and sample equation. Scalar known-norm LWE positive-control Lemma9 uses another reduction strategy; source ring known-covariance gap survives.
- `RECOMMENDATION:` PARK persistent dummy covariance as a direct standard-MLWE-based replacement, without claiming global no-go. Return to the original secret-conditioned hidden Gaussian pad-sharing problem; new ideas should preserve source χ and prove a **joint native PK+evk+multi-session simulator** with actual correlation generated on demand. Don't spend more turns enumerating covariance families or relabeling unknown secrets.
- `NEXT_TEST CGS-34 (only upon PI next “继续”):` Choose ONE explicit scheme with **publicly determined Gaussian target but secret-conditioned hidden threshold-share output generated on demand**, perhaps a trusted/noncolluding Server-assisted conditional-noise dealer versus setup O(LDec) tradeoff. Quantify whether the Server's knowledge is sufficient (it knows masks, not FHE secret), and attack confidentiality if s-dependent statistic must be sent to Server. Alternative actual conditional sampler from literature, not a generic PCF promise. One smallest joint leakage/set consistency test; if no feasible mechanism, PI HUMAN_REVIEW instead of repeating failures.
- `STATE_UPDATE: YES` new finding, current CGS archive and root STATE only. No unrelated topic state modified.
