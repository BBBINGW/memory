# FHE × MPC — Postselected-T Collaborative Sampling: Share-Conversion and Prior-Art Gate

**Date:** 2026-10-26 (Asia/Singapore)
**Track:** broad FHE × MPC, prescout (not an official iteration)
**Stage:** PRESCOUT-FHE-MPC-04
**Status:** FAIL_NAIVE_DYNAMIC_T_NOVELTY / PARK_GENERIC_SHARE_CONVERSION
**Evidence:** VERIFIED_SUPPLIED_HHW_FULLTEXT + CLASSIC_PRIOR_ART_ABSTRACT/INSTITUTIONAL_RECORD + PUBLIC_2026_ABSTRACT + DERIVED_ALGEBRA, **NOT** a published new theorem or native performance test.
**GitHub parent:** findings/fhe-mpc-supplied-fulltext-standard-approx-uc-source-gate-2026-10-26.md

## Primary hypothesis and minimal decisive test

**H:** Because Hwang's t-out-of-n CKKS standard-secure approximation protocol chooses decryptor set `T` before producing the `t`-out-of-`t` collaborative bit-sharing, an implementation **must repeat the costly Discrete-CKKS BinBoot+Clean bit-sharing for every possible later-chosen T**; efficiently supporting dynamic T therefore necessarily requires a new correlated-randomness primitive.

**Result: FAIL as a necessity claim.** Linear secret-sharing conversion can take a *single correctly sampled global smudging error e per output*, with n-out-of-n additive sharing, into a t-out-of-n polynomial sharing from which any subsequently chosen T can locally derive t additive shares. It is an application of classical secret sharing, not a new cryptographic mechanism. Costs and active security are **NOT** thereby solved. Nor is this a proof that the concrete Hwang implementation supports this transformation cheaply or automatically.

## Source provenance

1. PI-supplied **Hwang et al., 2025/395**, `papers/supplied/2025-395.pdf`, Git blob `84710edb51998a1c9d50a8c306ec1970d8d389f5`. Physical p7 Definition3: semi-honest standard security. Physical p15 Fig8: `F_{n-ColSamp}` samples `e<-D`, additive `r_1,...,r_n` in `R_{q_out}`, `sum_i r_i=e`; p16 Theorem3: standard simulation only in `Fn-ColSamp` hybrid. Physical pp16–17 Fig11: actual multi-party discrete CKKS `BinBoot + Clean`, distributed decrypt + pairwise PRF zero-share masks; 2^16-bit batch partial 33.96 s, 2^18 batch partial 135.84 s, single thread, **only bootstrapping+cleaning measured**. Physical pp29–30 AppendixD Fig15/Fig17/Theorem7: post-chosen `T` of t decryptors gets a `t`-out-of-`t` sampler; security is semi-honest in `FThColSamp` hybrid.
2. Cramer–Damgård–Ishai, **Share Conversion, Pseudorandom Secret-Sharing and Applications to Secure Computation**, TCC 2005. Institutional abstract `https://ir.cwi.nl/pub/16467` identifies share conversion and noninteractive Shamir pseudorandom sharings from pre-distributed randomness. Direct ePrint/PDF byte-level algorithm details were NOT independently audited; our polynomial reshare construction below is our own elementary derivation, *not* attributed as the exact CDI algorithm.
3. **Generalized Pseudorandom Secret Sharing and ...**, ePrint 2021/1223, abstract/index `https://eprint.iacr.org/2021/1223` and PDF index snippets indicate seed-setup + local noninteractive random sharing, including malicious abort contexts. Full current text NOT audited; do not claim it is a direct implementation of Hwang's bounded uniform bit sampler.
4. **Tulva: Practical Asynchronous Threshold FHE**, arXiv 2610.20521 / ePrint 2026/2485, posted 2026-10-14, official NIST 2026-10-13 talk `https://csrc.nist.gov/presentations/2026/tcpt3-4a1`. It supports asynchronous threshold decryptor collection without pre-agreeing on the participating set, plus partial-decryption-query security. **It does NOT automatically imply standard approximate CKKS collaborative-smudging distribution or malicious UC sampler**; recent strong prior art against claiming the dynamic-decryptor property alone.
5. Brakerski et al. ePrint 2025/712, **Threshold FHE with Efficient Asynchronous Decryption** `https://eprint.iacr.org/2025/712`, prior asynchronous scheme. Publication/abstract checked, full security and interface not audited. Also `On Threshold Fully Homomorphic Encryption with Synchronized Decryptors`, de Verdière–Passelègue–Stehlé, CCS 2026/ePrint 2026/031 (identified in PI-supplied Hwang refs and author page `https://perso.ens-lyon.fr/alain.passelegue/publications.html`).

## Source-independent algebraic falsifier [DERIVATION]

Let `A=R_q` for a CKKS coefficient ring `Z_q[X]/(X^N+1)` (or any finite commutative ring), assuming there exist public nonzero interpolation points `alpha_1,...,alpha_n` in the center with every `alpha_i` and `alpha_i-alpha_j` a unit in A. This holds for e.g. each odd large RNS prime modulus greater than n with points `1,...,n`; **not** automatically true for `q=2^k` when n is large.

1. First sample fresh `e<-D` **per output**, and additive shares `s_i` distributed as Hwang's `Fn-ColSamp`, with `sum_i s_i=e` in A.
2. Each party i independently chooses degree-(t-1) `f_i(Z)=s_i+sum_{j=1}^{t-1} b_{i,j} Z^j`, with `b_{i,j}` uniform in A, sends `f_i(alpha_k)` privately to every party k. At least one honest share generator must contribute uniform coefficients; this is an **honest/private-channels** model, not malicious VSS.
3. Party k stores `S_k=sum_i f_i(alpha_k)`. Thus there is a single degree-(t-1) `F(Z)=sum_i f_i(Z)`, with `F(0)=e` and (conditional on e) uniform coefficients for degrees 1,...,t-1.
4. Once a size-t T is selected, participant k in T computes public Lagrange weight `lambda_k(T)=prod_{j in T,j!=k}(-alpha_j)/(alpha_k-alpha_j)`; let `r_k(T)=lambda_k(T)*S_k`. Then `sum_{k in T} r_k(T)=F(0)=e`.
5. For any <t share holders, their vector `(S_k)` is **uniform independent of e**, because evaluation of the uniform random (t-1) nonconstant coefficients at <t distinct points has surjective linear map (unit Vandermonde minor). Similarly the rescaled share subvector for one fixed T is independent of e when <t.
6. For each output use **fresh e and fresh sharing randomness**. Reusing the same e across independent outputs was already falsified in `findings/fhe-mpc-uc-approximate-collaborative-sampling-prescout-2026-10-26.md`.

**Technical limitations, essential:** Polynomial share conversion has O(n²) communicated ring-element evaluations in this illustrative protocol (and O(t n) local per vector depending on implementation); that may be far more expensive than Hwang's specific sampler, especially for ~2^16 bits per batch. Random shares of `e` over a field/CRT ring need modulus/lifting compatibility with Hwang's `q_out` and distributions. With corrupt dealers, parties can set inconsistent polynomial constants or equivocate and change e/bias D. Need verifiable secret sharing, secure dealer-less D sampling, corruption/abort handling, cross-output transcript analysis and concrete cost. PRSS can trade seeds/setup for online work, but naive use does not produce bit-constrained e distributed according to D. **Asynchronous collection of t shares for decryption is NOT itself sampling standard-secure CKKS e.**

## Cost and novelty result

- Claim `must rerun expensive BinBoot+Clean for every T`: **FALSE as structural claim** if one can do subset-independent share conversion at acceptable cost.
- Claim `simple additive-to-Shamir conversion is novel`: **FAIL (classical linear secret sharing/PRSS prior art)**.
- Claim `a malicious distribution-faithful CKKS sampler with postselected T is solved efficiently`: **UNVERIFIED**, not implied by our algebra or Tulva's abstract.
- Claim `this variant beats Hwang end-to-end`: **NO EVIDENCE**; simple share conversion has severe communication/verification costs.
- Additional challenge `fresh D, malicious robustness and IND-CPApD + SIM-PDEC + Rob (+IND-CIRC in uncorrupted-server setting)` is real proof obligation, but not an established open research problem without precise prior art and quantified baseline.

## Decision / next direction

**PARK this precise idea.** Avoid further iterating toy Shamir, PRSS and naive share reuse. Quality/value gate after repeated failed simple FHE×ZK and FHE×MPC composition ideas. If FHE×MPC continued, focus **only** on a concrete measured subsystem, e.g. Hwang's 2^16-bit Discrete-CKKS BinBoot+Clean, plus closest malicious threshold random-bit generators for matching corruption and distribution. If existing techniques already match full requirement cheaply, kill. Otherwise a real new non-BinBoot random-bit sampler may be high value. Relative priority: compare that fixed problem against a pure FHE high-cost algorithm/representation bottleneck before authorizing native work.

`END: STATUS=FAIL_NAIVE_DYNAMIC_T_NOVELTY; RESULT=CLSSF_SHARE_CONVERSION; NEXT_TEST=CHECK_MALICIOUS_BIT_GENERATOR_AT_MATCHED_D_AND_COST; STATE_UPDATE=THIS_NOTE_ONLY; CODEX=NOT_RUN`
