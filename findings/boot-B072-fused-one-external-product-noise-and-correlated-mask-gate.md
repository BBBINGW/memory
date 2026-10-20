# BOOT-B072 — Can an encrypted-secret/selector pair replace a coupled AP-GGSW in one external product?

**Date:** 2026-10-20  
**Track:** BOOT exclusively; SHIP paused  
**Primary hypothesis:** Given separately stored `GLWE_s(u)` with `u=ψ(s)` and `GGSW_s(μ)`, one ordinary external product plus public polynomial operations will implement Bernard–Joye's `GLWE_s(m) ⊛_ψ AP-GGSW_s(μ) -> GLWE_s(ψ(m)μ)` with useful noise and online cost, without pre-encrypting the `uμ` cross keys.

**STATUS:** `PASS_EXACT_FUSED_ALGEBRA / FAIL_MASK_NOISE_GATE / FAIL_NAIVE_CORRELATED_MASK_SECURITY / FAIL_ONLINE_WORK_REDUCTION / NO_NEW_PRIMITIVE`

## Primary source and novelty

Bernard and Joye, *Bootstrapping (T)FHE Ciphertexts via Automorphisms: Closing the Gap Between Binary and Gaussian Keys*, ASIACRYPT 2025, [author PDF](https://marcjoye.github.io/papers/BJ25autpbs.pdf), Section 4.1, Definitions 4.1–4.2 and Proposition 4.3 (PDF physical pages 14–15). They already construct a **single external product** with coupled rows encrypting `-ψ(s_j)μ` and `μ`, and share the `μ` body rows across automorphisms (§4.2/Equation 4.1, physical p.16). Thus, reducing three operations (automorphism + KS + product) to one product is **already their contribution**. The question here is whether one can *uncouple the key transcript* without sacrificing cost or noise. GGSW external-product asymmetric noise amplification and tensoring limitations are standard (CGGI 2020/TFHE ePrint 2018/421, §§3.10–3.12), not novel.

## Constructive algebraic one-product candidate

Fix k=1 and decryption `Dec_s(a,b)=b-a*s`. Input `C=(a,b)` has `b-a*s=m+e_in`; let `u=ψ(s)`, `A=ψ(a)`, `B=ψ(b)`.

Public key transcript (distinct encryptions under `s`):

* `K_u=GLWE_s(u)` shared over selectors for a fixed ψ;
* `S_μ=GGSW_s(μ)` per selector, with its existing body gadget row `E_μ=GLWE_s(μ)`;
* no directly stored `GLWE_s(uμ)` AP rows.

Compute **one** `V=ExtProd(K_u,S_μ)` encrypting `uμ`, then output ciphertext

`C' = B * E_μ - A * V`, using *public polynomial by GLWE* multiplication, with all products taking place under the same secret `s`.

Noiseless decrypt: `Dec_s(C') = Bμ - A(uμ) = μψ(m)`.

This is algebraically a viable one-product online compilation of the desired functionality, not a proof of efficient FHE. Compared with a standard k=1 AP-ExtProd with 2D GLWE rows and two GLWE components per row, it uses the SAME `2D*2=4D` ring multiplications inside its product PLUS four ring multiplications to apply `A` and `B` to the two GLWE components. With D=4, illustrative 16 vs 20 ring multiplications, excluding precomputation/FFT/decomposition overhead. Its *candidate* stored BSK subset for n selectors and r automorphisms would be `2dn+r` GLWE rows rather than `(r+1)dn`; this is storage-vs-noise, not a true same-security native saving.

## Exact noise obstruction — decisive theorem for this candidate

Write `Dec_s(E_μ)=μ+e_μ`, `Dec_s(V)=uμ+e_V`; then, including input error,

`e_out = μψ(e_in) + B*e_μ - A*e_V`

`      = μψ(e_in) + ψ(m+e_in)*e_μ + A*(u*e_μ-e_V)`.

Define `D=u*e_μ-e_V`, which depends on **evaluation keys**, independent of a fresh uniformly random accumulator mask `A`. If `D` is a **unit** in `R_Q`, then `A*D` is uniform in `R_Q`. For `R_(2^w)=Z_(2^w)[X]/(X^N+1)` with power-of-two N, `D` is invertible precisely when `D(1)` is odd, because reduction mod2 yields `F_2[X]/((X+1)^N)`. Thus, even coefficient errors of size 1 can result in uniform-modulus output error, making an ordinary small-noise correctness argument impossible in this regime. This is a mathematically exact *conditional* obstruction to the proposed fused formula, NOT to all multilinear FHE circuits or all possible correlated evaluation-key distributions.

### Reproducible finite-ring experiment

`verify_b072_fused_noise.py`: N=8, Q=65536, B=16, d=4; exact centered gadget digits and reconstruction (suitable signed modular representative), random ternary GLWE secret, independent {-1,0,1} noise, randomized masks, ψ_t for odd t mod16. 600 independent matched-input trials; compare to a directly generated, independently noise-sampled Bernard–Joye style AP-GGSW implementation. Exact ciphertext-level identity including all noise terms checked in **600/600**.

| Metric | Published-style AP direct | One-product uncoupled candidate |
|---|---:|---:|
| median output coefficient RMS | 28.843 | 18,719.371 |
| ratio of medians | 1 | 649.0 |
| trials with any coefficient residual >= Q/8 | 0/600 | 600/600 |

In 303/600 trials `D(1)` was odd, proving an **exact uniform-mask term** arises conditional on the sampled key errors; other cases also had very large noise. **Q/8 here is a synthetic numerical threshold, not a certified cryptographic DFR**. Input plaintexts and masks were paired, but original and candidate key samples were not distribution-identically coupled. Toy ring and modulus are insecure; there is no real parameter/security/latency claim.

## Rescue gate: perfect error cancellation can leak secret if masks are naively correlated

An evaluator would like `e_V = u e_μ`, eliminating `A D` exactly. As a counterexample to a naive correlated-mask implementation, suppose the secret-key holder generates `E_μ=(p,p*s+μ+e)` and `V=u E_μ` componentwise, exposing public masks `p` and `u p`. Then `Dec_s(V)=uμ+ue` and the dangerous error cancels. But whenever `p` is a unit, an observer immediately recovers `u=(up)p^{-1}`. A standalone toy script (`verify_b072_correlated_noise_leak.py`) constructs a negacyclic inverse modulo 2^16 via Hensel/Newton lifting: 100/100 purposely unit-mask cases recover the entire hidden `u` exactly; 100/100 small-output-noise checks pass, median RMS 2.062. This is a **toy attack on that explicitly insecure mask-correlation pattern only**, not on Bernard–Joye, standard GLWE or other secret-key-generated correlated-noise transcripts. Correlating *noise alone* with otherwise independent random masks does not automatically imply leakage, but it may require directly generated cross-selector AP key material or a new construction and security proof.

## Decision, boundary, and next test

* PASS: one-ExtProd algebraic functionality, exact noisy recurrence and type checks.
* FAIL: standard independent encrypted-factor transcript has unacceptable output noise, including mathematically uniform mask noise for a large observed subset.
* FAIL: the obvious exact-noise cancellation by scaling public masks leaks `u`.
* FAIL: even ignoring noise, the candidate does not reduce per-selector ring multiplication count vs original AP external product (16 vs 20 in the illustrative D4/k1 model).
* UNCLEAR: some genuinely new correlated-randomness, tensor-key or special-gadget architecture could overcome this, but none was constructed, secured or benchmarked. No impossibility or novelty claim about such architectures.

**Research decision:** archive this direct fused key-factorization branch, rather than running expensive native PBS benchmarks. B071's full AP per-digit ciphertext storage vs computation dilemma persists.

**NEXT_TEST B073 (not started):** pivot away from simply factoring `-ψ(s)μ`. Find ONE different bootstrapping primitive with an explicitly source-derived bottleneck, ideally a batch/trace or approximate decomposition interface that reduces online digit processing while preserving all masks and the security game. Check earlier B025/B035/B040 and Bernand–Joye CRT gadget decomposition (ePrint 2024/909) before proposing novelty.

**STATE_UPDATE NO:** GitHub Notes cannot return `findings/boot-STATE.md` contents (empty response); preserve existing state. Only append one BOOT B072 finding, SHIP paused.