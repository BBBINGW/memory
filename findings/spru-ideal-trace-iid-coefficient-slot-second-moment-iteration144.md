# Iteration 144 — Source-shaped SPRU ideal Trace of iid coefficient error has exact per-slot RMS gain sqrt(L), not L

**Date:** 2026-10-13. Human PI authorized ONE iteration by “好的，请继续” following I143. Scope exactly one mathematically falsifiable statistical-error hypothesis and one exact Galois-character covariance test. No complete OpenFHE ciphertext benchmarking or implementation changes.

## Read before write / source

- Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` after I143 SHA `14d4886f1fe06f685816ad2ea564af91cbecf224`; the long-term `findings/OPEN_RESEARCH_BRANCHES.md`; I143 `failures/spru-onehot-trace-noise-blockwidth-independent-bound-iteration143.md`; I142 `findings/spru-optimized-depth-only-noise-recurrence-gap-iteration142.md`; I119 `findings/spru-theorem1-table2-sufficient-bound-gap-iteration119.md`.
- Source Coron–Köstler, *Low-Latency Bootstrapping for CKKS using Roots of Unity*, IACR ePrint **2025/651**, https://eprint.iacr.org/2025/651, Research MCP full 42-physical-page 2025 mirror PDF SHA256 `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6`, **VERSION_UNVERIFIED** vs latest official.
- Re-read **§3.1 physical pp6–8**: authors use independently sampled centered binomial χκ *coefficient noise*, with mean0, variance `σ²=κ/2` for an individual χκ coefficient; actual **fresh public-key encryption error is the combination `v·e_pk + e0 + s·e1`** and thus NOT simply iid ring coefficients without further proof. §3.3 physical pp9–10 canonical evaluation in odd roots of unity, §3.4 p11 automorphism `Ψ_r:f(X)↦f(X^{5^r})` gives slot rotation, §3.5 pp11–12 Trace `Tr_(N/2→h)=Σ_{j=0}^{L−1}Ψ_{jh}` (expanded factorization) with `L=N/(2h)`, and §4.3–4.4 pp15–16 optimized block-one plaintext selectors; Table2 physical p24 N2^15, h64, L256, empirical ~14-bit precision with Δ2^49.
- Author actual connected GitHub `coron/spru_boot/src/single_slot.cpp`, SHA `38d9fda8023ca0a06c5f4c9632802c83e4762c22`, loops eight `EvalRotate+EvalAdd` stages for N32768,h64; `src/multiple_slot.cpp` SHA `7ffb1fff5d99dc8e0f947ae77083455d163afa64` similar unnormalized Trace.
- I143 **exact worst-case** deterministic input e(X)=1 gives `Tr(e)=L` and sharp coefficient/slot infinity amplification L256. It does **not** imply all random noise has typical L growth. I144 is a new second-moment question, NOT relabeling that worst-case as probabilistic noise.

## ONE hypothesis and ONE cheapest falsifier

**[HYPOTHESIS]** For a single **ideal, error-free-automorphism** SPRU Trace on one additive pre-Trace ring error polynomial `e(X)=Σ_{t=0}^{N−1} e_t X^t`, with independent mean-zero variance-σ² coefficient samples (e.g. one unrecombined χκ error source), the output at a fixed canonical CKKS slot has **exact second moment L times the input slot's**. Thus its slot RMS grows **sqrt(L)**, not L, *despite all rotations applying to exactly the same polynomial*.

**[FALSIFIER]** On the actual Trace exponent orbit `a_j=5^{jh} mod 2N` at original N32768,h64 and small sanity N32,h2, compute the exact covariance `E[e(ζ^{a_j}) overline(e(ζ^{a_k}))]` by coefficient independence and root orthogonality, check whether offdiagonal covariance is zero and ondiagonal Nσ², and hence whether source-realistic ratio is L or L² for squared magnitudes. If orbit reuses the same root, or conjugate orthogonality fails, kill the conjecture. This is a symbolic finite character-sum check, not Monte Carlo or an OpenFHE security experiment.

## Exact derivation

Let `N` be a power of 2, `h|N/2` power of2, `L=N/(2h)`, `ζ=e^{πi/N}` primitive 2N-th root of unity. The cyclotomic automorphisms used by the source are `Ψ_r:e(X)↦e(X^{5^r})`, so expanded ideal Trace at ζ is
```
 Tr(e)(ζ) = Σ_{j=0}^{L−1} e(ζ^{a_j}), a_j=5^{j h} mod 2N.
```
The powers a_j are distinct odd residues because ord_(2N)(5)=N/2 and h divides N/2. With independent real random coeffs `E[e_t]=0, E[e_t e_u]=σ² 1[t=u]`,
```
 E[e(ζ^a) conj(e(ζ^b))]
  = Σ_{t,u} E[e_t e_u] ζ^{at-bu}
  = σ² Σ_{t=0}^{N−1} ζ^{(a−b)t}.
```
For distinct odd a,b, a−b is a **nonzero even residue** modulo 2N. Therefore `ω=ζ^{a−b}` is an Nth root with ω≠1 and `Σ_{t=0}^{N−1}ω^t=0`. For equal a=b the sum is N. Hence exact *zero offdiagonal **Hermitian covariance*** and no independence assumption on the **rotated slot errors**:
```
 Cov(e(ζ^{a_j}), overline(e(ζ^{a_k})))
 = Nσ² 1[j=k].
 E[|Tr(e)(ζ)|²] = L N σ²,
 E[|e(ζ)|²] = N σ².
 RMS gain = sqrt(L).
```
For source Table2 `N=32768,h=64,L=256`, ideal trace slot RMS gain **16×**, vs sharp deterministic worst-case 256× from I143. If specifically `e_t ← χκ`, `σ²=κ/2`, output second moment `256*32768*κ/2=4,194,304κ`, RMS `2048 sqrtκ` in unscaled coefficient-error units (input RMS `128 sqrtκ`). This is **per fixed canonical evaluation slot**; it is NOT a simultaneous high-probability maximum over N/2 slots and not an entire SPRU decrypted ciphertext precision estimate.

**Important non-contradiction:** Even with iid coeffs, constant coefficient of trace is `[X^0] Tr(e)=L e_0` exactly, yielding coefficient-0 variance `L²σ²`. It is possible to have that coherent coefficient yet still have **fixed-slot complex second moment LNσ²** because other Fourier coefficient covariances and cancellations matter. Distinguish coefficient domain, slot domain, deterministic sup bound and per-slot expected squared error.

## Exact reproducible test (ONE fixed claim at 3 sizes)

Wrote and executed standalone Python `/mnt/data/i144_spru_trace_covariance.py`, SHA256 `57c17fc68f33301ea21f9931ab3d7e1b86e0892c22dfebae6e69211827f2a89e`. For each N/h, explicitly construct all a_j using modular powers `pow(5, h*j, 2*N)`, assert odd/distinct, evaluate symbolic character sum exactly by residue parity/root-of-unity orthogonality for ALL pairs (no floating-point or random sampling):
```
N=32, h=2: L=8; 56 distinct ordered pairs cov0; input slot var32σ², trace slot var256σ²; RMS 2.8284×; coeff0 RMS8×
N=256,h=4: L=32; 992 distinct ordered pairs cov0; input slot var256σ², trace slot var8192σ²; RMS5.6569×; coeff0 RMS32×
N=32768,h=64: L=256; 65280 distinct ordered pairs cov0; input slot var32768σ², trace slot var8388608σ²; RMS16×; coeff0 RMS256×
```
This checks one exact character-orthogonality covariance hypothesis at three conformant dimensions, not three research directions.

## Scope: why NOT a complete SPRU Table2 proof

1. `e(X)` at the *actual Trace input* is formed by `eprod[u] = EvalMult(bootsk[u], Encode(v[u]))` then ciphertext Add across u, as verified in author `src/single_slot.cpp` and `src/multiple_slot.cpp`. It includes public-key encryption error `v e_pk + e0 + s e1`, encoded-plaintext multiplication/rescale/rounding noise, possible shared-pk correlation across bootstrapping key encryptions, and may **not** have independent identically distributed ring coefficients. Per-slot spectral diagonal covariance could potentially be proven under conditional noiseless-multiplication assumptions, but was **not verified** for the actual OpenFHE state here.
2. The **real trace applies rotations through key switching**, producing fresh key-switching error terms and possible correlations with the input ciphertext and across rotations; no joint distribution proof, conditional covariance bound or simulation provided. Its noise might change the sqrtL scaling or add separate terms; do not claim the two scenarios coincide.
3. Source final `Pr_{h→1}` multiplication, special δ normalization, imaginary extraction, rescale, and SlotToCoeff likewise affect distribution and precision. I142 old Appendix E recurrence was for a different circuit, and this isolated lemma does not close its 13.55-bit conditional scale certificate gap or certify ~14-bit precision.
4. Source standard primitive-root orthogonality is textbook Fourier algebra; this **is not novel in itself**, not a new SPRU optimization, and not a contradiction of source Theorem1/Table2. Finding may help choose whether sophisticated covariance-aware derivation is feasible rather than spending time on deterministic bounds.
5. Distinguish **zero covariance** vs independence: rotated evaluations share one set of e_t and are not generally independent for discrete χκ. A high-probability tail or max-norm bound needs further arguments. Source official PDF version still VERSION_UNVERIFIED.

## End of iteration

**STATUS:** **PASS exact iid-base-error ideal-Trace per-slot variance sqrtL / UNCLEAR actual OpenFHE trace and end-to-end precision / HUMAN_REVIEW**.
**RESULT:** For e_t independent centered coeff errors, source true Galois orbit Ψ_jh yields pairwise uncorrelated evaluation errors via character orthogonality. Hence ideal Trace fixed-slot second moment increases L and RMS sqrtL; for N32768,h64 L256, RMS16, despite deterministic possible max256 (I143). Exact 256-orbit covariance at source dimensions PASS. No actual optimized encrypted noise distribution or security/performance theorem; elementary result.
**NEXT_ACTION:** I145 only when PI explicitly authorizes: attempt **one source-specific covariance interface gate** at pre-trace input, including author's actual packed EvalMult+Add, public-key shared error and/or rotation-key-switching, to see whether offdiagonal slot covariance remains zero or acquires nontrivial correlations at Table2; cheapest source-pinned derivation or exact small-code counterexample. If must assume fresh iid ciphertext e without justification, PARK the attempted optimized precision theorem and prefer a distinct high-value branch; human decides.
**STATE_UPDATE:** YES — differs substantively from I143 by an exact statistical per-slot identity, but does not elevate research importance or declare theorem novelty.
