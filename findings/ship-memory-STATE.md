# SHIP Evaluation-Key Memory — Independent Research State

**Checkpoint:** 2026-10-14 (Asia/Tokyo).
**PI-selected target:** SHIP prepared evaluation-key selector memory, Cheon–Hanrot–Kim–Stehlé, EUROCRYPT 2025, ePrint 2025/784.
**LAST COMPLETED:** **I198 COMPLETED** (PI's I-series label for the independent SHIP continuation); previous SHIP-M04 completed. **No compiled Poulpy variant run.**
**STATUS:** I198 PASS narrow pinned-IFMA *conditional selector-prepared payload* and online-call-count screen; compiled CKKS accuracy, latency, process peak RAM, security and novelty remain **UNCLEAR / IMPLEMENTATION BLOCKED**; **NOVELTY NOT VERIFIED**.
**Isolation:** SHIP-M01..M04 each in own `findings/ship-memory-MNN-*.md`; global `STATE.md` is actively used by another vFHE I-series conversation. **Do not overwrite or join histories.**

## Main candidate

**Complex-paired private selector masks.** For two secret-dependent real masks `M1,M2`, store one CKKS `C=Enc(M1+iM2)`. Given complex public operand plaintexts `P1,P2`, reconstruct `M1P1+M2P2 = [C(P1−iP2)+Conj(C(conj(P1)−i conj(P2)))]/2`. Aggregate all pairs before one conjugation per leaf. Conditional selector prepared-key objects drop **4hθ→2hθ**, but ct×pt multiplication term count remains 4hθ, output accumulators double and ~h extra early conjugations for real SHIP (~2h for complex) before mux/product tree; no measured speed/RAM advantage.

**M01** `findings/ship-memory-M01-complex-paired-selector-key-gate.md`: source-shaped private mask complex packing ideal-slot identity PASS; novelty not verified.
**M02** `findings/ship-memory-M02-early-conjugation-source-modulus-gate.md`: pinned Poulpy Galois -1 key and source-level CKKS precision gate PASS; physical noise unverified.
**M03** `findings/ship-memory-M03-toy-rlwe-early-conjugation-noise.md`: an **independent N16 toy RLWE** actual encrypt/automorphism/KS/decrypt test showed baseline worst 1.96e-8 vs packed worst 3.15e-6 with a **different, unguarded low-precision eval-key**. Not a representative source-Poulpy numerical conclusion.
**M04** `findings/ship-memory-M04-source-gadget-noise-bound.md`: audited pinned `poulpy-fhe/poulpy` commit `250d4392656cd313f92ca66d96d8865702d39ddf`, `GGLWELayout`, automorphism encryption, truncated Gaussian |`e`|≤19 and guarded key `key.k=dnum*dsize*base2k+k_aux`. One conditional exact-arithmetic **source-formula** gate, illustrative `N16384,h32,θ4,base2k52,ld40,raised_k468,masked_k428,dnum9,kaux66,evk_k534`, gives additional message slot error ≤~2^-361, leaf ≤2^-362, h-fold product output ≤~2^-356 vs nominal 18.1-bit tolerance. This refutes **only** the claim that key-Gaussian + ideal k-bit normalization rounding inevitably exhaust precision. It **does not include real FFT/NTT backend error, other CKKS errors, real cost, security/novelty or actual production test**.
M04 local reproduction: `/mnt/data/ship_m04_source_noise_bound.py` SHA256 `f589cb2fe2608635a57830a87faa2f1133a16e532721c7f7abb32399883642b5`, `/mnt/data/ship_m04_source_noise_bound.json` SHA256 `506733c31ca28a4fc42c74ac7c4c364f7361f3542d94d71125a43104469c7726`.

## Main remaining obstruction

In actual Poulpy SHIP, additional ~h high-precision conjugations plus two masking-domain IDFT/normalization paths may erase the real latency win and increase transient RAM. The exact number/size of *prepared* selector operands and total RAM need a modified implementation, and actual full-message CKKS error requires backend-level confirmation. The mathematically ideal key-sampling noise is not a meaningful bottleneck under source high precision, despite the prior low-precision toy warning.

## New results after SHIP-M04: I197, I198

- `findings/ship-memory-early-galois-guard-envelope-iteration197.md`: independent ideal-key-noise envelope; superseded for the stricter source-specific bounded sampled-Gaussian screen by existing M04. No production performance assertion.
- `findings/ship-memory-prepared-ifma-cost-gate-iteration198.md`: selected pinned Poulpy IFMA backend and illustrative `N16384,h32,theta4,base2k52,raised_k468,L9`. Prepared selector left-convolution payload **512×4.5MiB=2.25GiB** baseline; candidate **256×4.5MiB=1.125GiB** (50% saving conditional on implementing the M01 packing). Ct×Pt terms **512→512**; masking per-column IDFT **64→128** (+64), plus **32 early Galois key switches**; existing final conjugation unchanged. These are source-layout / algorithm-operation counts, **not** measured Poulpy timings, accuracy or peak RAM.
- True compiled Poulpy execution remains blocked locally: `cargo`/`rustc` absent, no compiled library and no DNS fetch. Do not repeat ideal noise simulations as substitutes.

## NEXT_ACTION — only on PI continuation

Obtain a real executable pinned Poulpy Rust runner, and run **ONE** real masking-leaf paired-vs-baseline comparison at the same `N16384,h32,theta4,ld40,k_mask428`. Check prepared selector bytes, actual max decrypted slot error, time spent in masking + high-precision early Galois conjugation, and peak live memory. If such a runner cannot be obtained, report **IMPLEMENTATION BLOCKED / HUMAN_REVIEW**: PI decides PARK or seek implementation support, rather than generating more adjacent toy models. Do not change parent direction automatically.

No changes to shared `STATE.md`, prior I193/I194/I195, or original HEaaN / third-party upstream Poulpy. PI retains strategic decision.
