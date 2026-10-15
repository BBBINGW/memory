# SHIP-I255 — Native 2-adic Galois-orbit Fourier diagonalization fails; odd-prime toy works

**Date:** 2026-10-16. **TRACK_ID: SHIP ONLY**, PI directed "continue" after I254. All past files remain immutable; no pivot CGS/VFHE/EXPLORE. ONE technical hypothesis and ONE minimum algebraic test. Status of prior shared SHIP STATE read remains **SOURCE_READER_BLOCKED**: Research GitHub Notes `read_repo_file` returned `{}` repeatedly this iteration for `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `START_RESEARCH_SESSION.md`, `STATE.md`, `findings/ship-memory-STATE.md` and I254. The previous context and I254 checkpoint remain available; `list_repo_files` reliably lists repository paths and SHAs. **Do not blindly edit shared states**. This failure file is self-contained.

## Primary falsifiable hypothesis H255

Under the **native Poulpy 2^k torus arithmetic** and source SHIP source-shaped `N=16384,h=32,radices=[4,4,4,3],θ=4`, the selector-controlled automorphism operators `σ_(5^(d*weight))` can be transformed by one **invertible, scalar-coefficient Z_(2^k)-linear Fourier / simultaneous spectral basis change** into diagonal-by-coordinate operators, allowing a single encrypted spectral selector (a Hadamard multiplication) without added large modulus, general rotation keys, or expensive basis-changing linear transforms.

**Cheapest falsifier:** At the FIRST radix group weight=θ=4, analyze the invariant coefficient orbit of `σ_(5^4)` in `Z_(2^k)[X]/(X^16384+1)`. If it has a signed orbit block with `A^(2^r)=-I` but `λ^(2^r)=-1` has no solution in `Z_(2^k)`, an invertible native torus scalar spectral basis is impossible. Show an exact small n16 example in q256; contrast with odd-prime q257 where roots exist and Fourier selection works. This falsifies ONLY native scalar Fourier diagonalization, not approximate complex CKKS transforms, a noncommutative packed module, or transformed/enlarged modulus methods.

## Sources and provenance [FACT]

- Original Cheon–Hanrot–Kim–Stehlé *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT2025, ePrint **2025/784**; original authors' HEaaN parameters and security NOT identified with illustrative independent third-party backend.
- Pinned independent Poulpy `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`:
  - `poulpy-ckks/src/layouts/ship/keyset.rs`, blob **8be6ab92846168330100efeabe9fa19dbd9720e4**, lines 509–532: `weight=theta`, `rot=(d*weight)%m`, `weight*=b`, radix B keys for each digit and support; sample shape `theta=4,bases=[4,4,4,3]`.
  - `poulpy-ckks/src/reference/ship/mux.rs`, blob **e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce**, lines 65–150: source performs candidate VMP then public DFT-domain Galois output twist, not a general rotation KSK for every candidate.
  - `poulpy-ckks/src/layouts/ship/keyset.rs` around line 558 generates only `p=-1` conjugation key in original bundle; a complex-slot Fourier transformation would introduce ordinary rotation requirements not present as distinct KSKs in this key bundle.
- I254 `failures/ship-memory-I254-packed-one-product-galois-selection-no-go.md` already excludes `C(m)+V(P_beta * U(m))` with selector-INDEPENDENT invertible **monomial/Galois-only** U,V, but does NOT exclude arbitrary Fourier basis changes. I255 is the next broader spectral attempt, not repeating the I254 narrow model.
- Additional context: standard CKKS implements slot linear transforms through rotations and plaintext multiplications; this file makes NO novelty claim and no source-measured CKKS FFT cost.

## Algebraic result [DERIVED, EXACT]

Let `N=16384`, `q=2^k, k>=3`, and `ψ=σ_(5^4)=σ_625`, an odd-power Galois automorphism of `R_q=Z_q[X]/(X^N+1)`.
Direct modular exponentiation yields:
```
625^1024 ≡ 16385 ≡ N+1 (mod 2N)
625^2048 ≡ 1 (mod 2N).
```
Thus `ψ^1024(X)=-X`, `ψ^2048(X)=X`. The orbit of the unsigned *coefficient positions* hit from X has 1024 distinct indices modulo N and signs that return negative; the 1024-dimensional signed-monomial invariant subspace `W=span_{Z_q}{X^(625^j) mod N | 0<=j<1024}` carries a signed cyclic permutation `A` with `A^1024=-I`.

If an invertible scalar torus Fourier basis existed for that restricted cyclic action, `A` would be diagonal over `Z_(2^k)`; each diagonal entry λ would obey `λ^1024=-1 mod2^k`. But there is **NO** such λ:
- If λ even, λ^1024 is even, not -1.
- If λ odd and k>=3, λ² ≡1 mod8, hence λ^1024 ≡1 mod8, while -1≡7 mod8.
Contradiction. Even stronger global criterion: if the entire Galois automorphism matrix were invertibly diagonal over `Z_(2^k)`, all diagonal entries would be units and reduce to 1 mod2. Reduction of the similarity would imply its nontrivial mod2 coefficient permutation is the identity—false. This rules out **invertible coefficientwise torus spectral diagonalization** of nontrivial ψ, not other ring operations/packings.

## Minimum exact executable countercheck [EXECUTED]

A runnable standard-library script
`/mnt/data/ship_i255_fourier_orbit_gate.py`, SHA256 **b84945d0f070dcbad403d276dcb37c62844042693e8fa156a26074fd6ea81a35**;
JSON `/mnt/data/ship_i255_orbit_spectral_gate.json`, SHA256 **54ef3551db7eacf95091fb87ce3e57980c606a897baf96681c01bdbe5a4ff35e**.
Final script re-run PASS after the preliminary implementation corrected a signed orbit basis mismatch; do not attribute the preliminary assertion failure to the mathematical construction.

Toy `N=16`, `ψ=σ5`. On signed orbit basis `v_j=ψ^j(X),j=0..3`, it is a signed cycle `A^4=-I`.
- `q=256`: exhaustively **ZERO** scalar roots of `λ^4+1`; no native scalar Fourier basis.
- `q=257`: **FOUR distinct** roots of `λ^4+1`; Vandermonde basis is invertible and `M A = diag(λ_i) M`. Exact spectral selection `M^{-1}diag(λ_i^d)M v=A^d v` verified **1024/1024** independently random `d∈{0,1,2,3}`/vectors; no encryption, security or HEaaN inference.
- Source shape actual modular exponentiation checked orbit length **1024** and return sign -, with full complex CKKS slot permutation orders for public rotation weights `[4,16,64,256]`: **[2048,512,128,32]**. An ordinary radix-2 complex FFT for such cyclic orbit lengths has **[11,9,7,5]** butterfly stages per direction; naive independent fwd+inverse every one of 4 groups × 32 supports = `32*2*(11+9+7+5)=2048` nominal per-support/group butterfly **stages**, PLUS selector ciphertext multiplications and new general rotation KSK/constant twiddle material. This is an **illustrative unfused algorithm count, not a proven lower bound or real latency**.

**Important boundary:** CKKS approximate slot-level FFT over complex numbers CAN diagonalize these permutation operators; that is not contradicted by lack of roots over Z2^k. However doing so homomorphically on **encrypted** input requires explicit correct CKKS linear transforms/rotations, scale/noise/capacity, correlated key security and a fair benchmark. The 2-adic obstruction is specific to the attempted cheap exact **native torus** coefficient basis change. Likewise original authors' HEaaN RNS odd-prime moduli need separate analysis; do **not** claim a universal SHIP impossibility theorem.

## End of Iteration

**STATUS: FAIL H255 native torus spectral compression / PASS exact no-root proof and 1024/1024 odd-prime spectral tests / UNCLEAR approximate complex-slot extension cost and security.**

**RESULT:** Found decisive obstruction *before* testing encryption/noise: source SHIP first-layer Galois 5^4 has signed power-of-two coefficient orbit, so `Z_(2^k)` provides no invertible scalar Fourier eigenbasis. Odd-prime spectral one-multiply idea works algebraically but needs a costly change of arithmetic representation or homomorphic slot transform; does NOT establish a prepared-memory, key-count or online improvement at matched security.

**NEXT_TEST:** Do not continue FFT toy scans or claim native torus advantage. Only reopen with an **explicit different representation transform** (possibly complex CKKS) whose exact preprocessing KSK/rotation/scale cost is demonstrably amortized by a realistic multiple-use workload, and a bounded-noise security-compatible implementation. Otherwise recommend PARK SHIP key-memory theory line, original author h31 security audit I245 remains SOURCE_BLOCKED. PI decides pivots. **STATE_UPDATE:** self-contained failure archive written; shared root/topic STATE update BLOCKED by GitHub Notes empty read, never blind append or claim success.
