# Iteration 145 — SPRU conditional pre-Trace spectral covariance survives a shared public key under idealized bootstrap-key plaintext products

**Date:** 2026-10-13. PI authorized "好的，请继续" following I144. **ONE hypothesis + ONE exact source-shaped finite-field covariance/character test**. No full OpenFHE encrypted run or new security/precision theorem.

## Provenance / previous negative gates

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` after I144 (SHA `71a749720cfc8a4599f82d552857af72acb493e2`), `findings/OPEN_RESEARCH_BRANCHES.md`, and `findings/spru-ideal-trace-iid-coefficient-slot-second-moment-iteration144.md`. I143 `failures/spru-onehot-trace-noise-blockwidth-independent-bound-iteration143.md` proves ideal deterministic worst-case Trace factor L=N/(2h), reached by e(X)=1. I144 proves fixed-slot RMS √L for **one iid coefficient-error source under ideal Trace**, not genuine pre-Trace ciphertext error.

Primary Coron–Köstler, *Low-Latency Bootstrapping for CKKS using Roots of Unity*, IACR ePrint **2025/651**, https://eprint.iacr.org/2025/651; Research MCP cached 42-physical-page original mirror SHA256 `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6`, official latest binary `VERSION_UNVERIFIED`. Section **3.1 physical pp6–8**: for public-key error polynomial e_pk, the public-key encryption error is exactly `η_i=v_i e_pk+e_{0i}+s e_{1i}`; every primitive coefficient in ternary ephemeral v_i, centered χκ e0_i,e1_i is independently centered with coefficient variance τ²,σ0²,σ1² respectively (source ZO(1/2) has τ²=1/2 and χκ has σ²=κ/2). Section **3.3–3.5 physical pp9–12**: negacyclic ring R=Z[X]/(X^N+1), canonical evaluations at odd 2N-th roots, Ψ powers5 Galois orbit, unnormalized Tr_(N/2→h) with L=N/(2h). Table2 physical p24 N32768,h64,L256.

**Author source, connected GitHub verified:** `coron/spru_boot/src/single_slot.cpp` blob SHA `38d9fda8023ca0a06c5f4c9632802c83e4762c22`: `BootstrapSingleSlotKeyGen` lines ~6–37 constructs two encoded split-secret CKKS plaintexts `ptsk1,ptsk2`, independently calls `cc->Encrypt(publicKey,ptsk1)` and `cc->Encrypt(publicKey,ptsk2)` under SAME pk. `BootstrapSingleSlot` ~61–75 constructs two public complex slot-phase masks v1,v2 from ciphertext c1 and performs `cmult1=cc->EvalMult(esk1,cc->MakeCKKSPackedPlaintext(v1))`, `cmult2=cc->EvalMult(esk2,...v2)`, `cadd=cc->EvalAdd(cmult1,cmult2)` before 8 rotations/KS. `src/multiple_slot.cpp` SHA `7ffb1fff5d99dc8e0f947ae77083455d163afa64` analogous many-eprod loops. Actual OpenFHE `EvalMult` can involve scale adjustment/rescale/rounding; THIS derivation isolates exact ring multiply/add only and is not directly asserted to model `FIXEDAUTO` ciphertext behavior.

## ONE technical hypothesis and decisive test

**[HYPOTHESIS]** For source-form two bootstrap-key ciphertexts under ONE shared public key and ONE common fixed secret s, with each encryption's primitive v_i,e0_i,e1_i independently sampled centered coefficients, and **fixed public plaintext masks m1,m2 independent of these fresh encryption coins**, the **exact-ring-product + Add pre-Trace error** `E=Σ_{i=1}² m_i(v_i e_pk+e0_i+s e1_i)` retains zero offdiagonal Hermitian covariance between **distinct canonical Galois-evaluation slots**, **even conditional on the fixed shared e_pk, fixed full s, and fixed masks**. If false, reusing pk or plaintext masking destroys the I144 covariance structure before any rotation. Note: the hypothesis is NOT about entire OpenFHE EvalMult, arbitrary adversarial mask choice, key switching, or post-rescale error distribution.

**[FALSIFIER/ONE TEST]** Construct fixed shared pk-error polynomial e_pk, fixed source-compatible one-nonzero-per-B secret s, and two nonconstant ring-plaintext masks m1,m2 at N32,h2 and the paper N32768,h64; compute full conditional covariance exactly over a finite prime field supporting primitive 2N-th roots. Verify all offdiagonal Galois pairs are zero; verify diagonals equal direct three-source variance formula; if any offdiagonal nonzero, kill. This is only an algebraically exact test of the independence/spectral model, not an actual χκ sampler or experimental CKKS error.

## Conditional covariance derivation (actual source message structure)

Let ζ=e^{πi/N} primitive 2N-th root. Given fixed pk-error polynomial e_pk(X), fixed secret s(X), and fixed public plaintext masks m1(X),m2(X), set
```
 η_i(X)=v_i(X)e_pk(X)+e_{0i}(X)+s(X)e_{1i}(X)
 E(X)=m1(X)η_1(X)+m2(X)η_2(X).
```
The zero-mean elementary random coefficient polys `v_i,e0_i,e1_i` are *independent of masks, pk, secret and each other*, with uniform per-coefficient variances `τ²,σ0²,σ1²` respectively. Source's actual keygen first fixes pk and secret; the *fresh bootstrap-key encryption coins* then vary. This can be a conditional distribution over encryption coins with public key and fixed secret, **only if plaintext masks are selected independently of those coins**. Honest data-independent input masks meet that requirement; adaptively chosen masks after inspecting publicly available bootkeys might not.

For arbitrary distinct **odd** exponent evaluation coordinates a≠b mod2N, primitive term `x(X)=Σ_t x_tX^t` has exact Hermitian covariance
```
 E[x(ζ^a) overline(x(ζ^b))] =
 σ_x² Σ_{t=0}^{N−1} ζ^{(a−b)t}=0
```
because a−b is a nonzero even residue mod2N. Diagonal is Nσ_x². Conditional on fixed pk, s and masks, multiplication by e_pk,s,m_i is **per-slot multiplication**, so cross terms between independent zero-mean primitive error polys vanish; terms from the SAME public-key polynomial do NOT force nonzero covariance, because it is multiplied by fresh independent centered v_i. Thus
```
 E[E(ζ^a) overline(E(ζ^b)) | e_pk,s,m1,m2] =0 (a ≠ b).
```
And for a canonical slot z=ζ^a,
```
 Var(E(z)|e_pk,s,m1,m2)
   = N Σ_{i=1}² |m_i(z)|²
            [ τ² |e_pk(z)|² + σ0² + σ1² |s(z)|² ].
```
The expression is a real nonnegative *Hermitian second moment* (provided deterministic fixed masks, independent elementary variables). It is **not generally constant across slots**, because public masks, e_pk and s can be spectrally nonflat. Therefore the Trace output variance under **ideal additional-error-free rotations** is a **sum** of the L distinct per-input-slot variances:
```
 Var(Tr(E)(z)|...) = Σ_{j=0}^{L−1} Var(E(ζ^{5^{jh} a})|...),
  ≤ L max_j Var(E(ζ^{5^{jh} a})|...).
```
This yields RMS-out ≤√L *maximum input RMS over that orbit*, *not always exactly √L times the variance at one arbitrary input slot*. For Table2 L256 gives upper multiplier16 relative to the **maximum** input-slot RMS within this very restricted idealized model. This strictly extends I144's iid-total-error assumption to the unrounded shared-pk source Encpk + two fixed plaintext multiplications.

## One exact finite-field coefficient covariance test

Reproducible script **`/mnt/data/i145_spru_pretrace_covariance.py`**, SHA256 `fd90b760f4597f45d76e559396fc424f5659888f9c8784bc245327ff00800bad`, created and executed in current container. It uses source-compatible ring dimensions N32,h2, N256,h4, and **paper N32768,h64**, prime **q=65537** and a primitive 2N-th root from primitive q−1=65536 root 3. Choose fixed original onehot-per-B secret with signed monomials ±1 at positions kB; fixed pk error e_pk=1+X^5−X^7; fixed nonconstant plaintext masks m1=1+X^3, m2=2−X²; primitive centered source-error coefficient variances τ²=σ0²=σ1²=1/2 (mod q) and fully independent across encryption instances. Algebraic **field** covariance is computed from Σ_t ζ^{(a−b)t} with complete O(N L²) explicit character sums at N32,N256, and algebraically exact geometric-sum short form for N32768. At each orbit point check diagonal against on-slot theoretical variance, all **65280 ordered offdiagonal** tests zero at source N32768,h64.

Output:
```
N=32,h=2,L=8:          56 ordered offdiagonals zero;
                       conditional diagonal values in Fq [41957,33000,11719,57383] ... vary.
N=256,h=4,L=32:       992 ordered offdiagonals zero;
                       conditional diagonal values in Fq [29360,5636,14595,62979] ... vary.
N=32768,h=64,L=256: 65280 ordered offdiagonals zero;
                       conditional diagonal values in Fq [49254,40235,49311,51262] ... vary.
```
IMPORTANT: The F65537 residues **do not represent physical real variances, CKKS error sizes, Gaussian tails, or Table2 security/accuracy**; they are exact checks of polynomial matrix/character cancellations and conditional formula in a field model. The true complex Hermitian covariance statement follows separately from the roots-of-unity derivation above. Chosen polynomial masks are **structurally valid deterministic ring plaintext multipliers** but not extracted OpenFHE quantized m_i from a complete ciphertext; actual fresh noise distribution is source paper abstraction, not full OpenFHE test.

## Scientific limits and interpretation

- **[PASS conditional, precise]** Reused pk e_pk **alone** does not produce offdiagonal slot covariance in the *exact, before-rescale* source-form fresh PK-encryption-error model: the fresh per-bootstrap-key ephemeral and error coefficient Fourier modes remain orthogonal even with fixed shared e_pk and fixed s. The output may have NONUNIFORM per-slot variances; cannot assert literal equality √L compared with one arbitrarily chosen input slot as in iid I144.
- **[OPEN critical]** Actual code's `EvalMult(bootsk,MakeCKKSPackedPlaintext(v))` uses RNS CKKS encoding/scale adjustment and may introduce key-switch, modulus switch, rescale, componentwise rounding and nonstationary errors; author `params.cpp` uses `FIXEDAUTO`, base mod 60 bits and scale mod49 bits. These effects were NOT reproduced. In addition, the actual 8 `EvalRotate` calls introduce re-used rotation-key errors that may be correlated with source and each other. The final product tree and SlotsToCoeffs remain untested.
- **[OPEN adaptivity]** Input masks are derived from ciphertext c1; if ciphertext c1 is selected after reading bootstrap-key encryptions, the masks can depend on their fresh coins and the above *conditional independence* may fail. This source-interface hazard is not an instantiated attack and typical non-adaptive benchmarks may obey the needed independence.
- **[NOVELTY]** Polynomial Fourier diagonality under independent stationary primitive noise is elementary. This is **not publishable on its own**, not an implemented FHE improvement, and not evidence authors' empirical 14-bit correctness is wrong. A genuinely useful contribution would need to track actual OpenFHE RNS rounding and joint rotation key-switch covariance (and max-slot tail) end-to-end or propose new algorithmic improvement.

## End of iteration

**STATUS:** **PASS conditional exact-ring pre-Trace shared-pk zero offdiagonal Hermitian covariance / UNCLEAR actual FIXEDAUTO-rescaled CKKS and rotations / HUMAN_REVIEW**.
**RESULT:** The exact source Encpk error `v e_pk+e0+s e1`, under two ciphertexts encrypted with same public key, after arbitrary fixed plaintext ring masks and ciphertext Add, still has zero cross-slot Hermitian covariance conditioned on fixed pk,s,masks and independent centered bootstrap-key encryption coins. The input per-slot variances are not uniform; ideal Trace variance is their sum and ≤L·max input variance. Exact N32768,h64 finite-field covariance check of 65280 distinct ordered pairs PASS; no actual complete OpenFHE code/real precision simulated.
**NEXT_ACTION:** I146 only if PI authorizes: ONE cheapest source-specific falsifier for actual *reused rotation-key-switch error correlations and/or RNS FIXEDAUTO rounding*; pick one primary mechanism, read exact OpenFHE v1.4.2 source or build minimal differential encrypted test, and quantify whether post-Trace offdiagonal covariance or variance amplification breaks the conditional simple-sum model. If unable to access exact source or only generic iid argument remains, PARK further SPRU covariance micro-audits, prioritize higher-upside branches. Do not claim I145 yields Table2 output precision proof.
**STATE_UPDATE:** YES — resolves one concrete source-model ambiguity (shared pk alone does not break spectral diagonal covariance) and establishes the exact needed additional source-noise gate.
