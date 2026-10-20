# BOOT-B075 — Shared-selector two-accumulator AP packing: correctness vs true online ring-work

**Date:** 2026-10-20  
**TRACK_ID:** BOOT exclusively; SHIP paused  
**Status:** `PASS_TYPED_ENCRYPTED_INTERLEAVED_AP / FAIL_ONLINE_ARITHMETIC_SAVING / FAIL_DISTINCT_AP_GALOIS_GENERALITY / UNCLEAR_MATCHED_SECURITY`

## Primary falsifiable hypothesis

If two GLWE accumulators with **independent uniform masks and distinct plaintexts** share a bootstrapping selector and a ring secret, can their next automorphism-parametrized external products be performed as **one** external product on a packed ciphertext, thereby **reducing actual online ring multiplications and FFT work** compared to two standalone products, while preserving secret labels, correctness, and noise? This is NOT an assumption of already shared public masks.

## Prior-art sources and provenance

1. [FACT — full PDF visually checked] Li et al., *BatchBoot: Fast Batched Bootstrapping for TFHE scheme and Practical Applications*, USENIX Security 2026, full proceedings PDF https://www.usenix.org/system/files/usenixsecurity26-li-zhihao.pdf (physical PDF pages 2–4, esp. Sec. 1.2/3). Already develops batched TFHE, multi-bit CMux, automorphism/FFT sharing, sparse packing, batch circuit bootstrapping; reports 2.4× vs prior batching and 43.8× vs non-batched tfhe-rs **for their settings**. These figures are author reports, not our measurements.
2. [FACT — bibliographic/abstract only; full text not successfully read] Bergerat et al., *Sharing the Mask: TFHE Bootstrapping on Packed Messages*, TCHES 2025(4), pp. 925–971, DOI https://doi.org/10.46586/tches.v2025.i4.925-971 , ePrint https://eprint.iacr.org/2025/2112 . Published work on common-mask CM-(G)LWE packed TFHE; exact algorithms not audited here. ePrint MCP attempted source but rejected mirror identity.
3. [FACT] Bernard and Joye, *Bootstrapping (T)FHE Ciphertexts via Automorphisms: Closing the Gap Between Binary and Gaussian Keys*, ASIACRYPT 2025, ePrint 2025/163, PDF https://marcjoye.github.io/papers/BJ25autpbs.pdf , Defs. 4.1–4.2 and Prop. 4.3; defines AP external product on one GLWE, relevant unbatched baseline.
4. [FACT — full PDF] Ma et al., *Practical Dense-Key Bootstrapping with Subring Secret Encapsulation*, ASIACRYPT 2025, https://eprint.iacr.org/2025/1594, physical pp. 3–4. Shows useful subring-secret symmetry, but security is tied to smaller ring, not automatically full ambient dimension.
5. [PRIOR] Guimarães et al., *AmortBoot* (CCS 2025) discussed in BatchBoot Section 3. Do not treat batching, selector reuse, or key-cache amortization alone as novel.

## Capacity gate: no lossless equal-degree packing of arbitrary two messages

R_Q=Z_Q[X]/(X^N+1) contains Q^N possible plaintexts. A general ordered pair in R_Q² contains Q^(2N) possibilities. A single same-degree R_Q element cannot encode every pair with lossless universal recovery: pigeonhole principle. Need >= 2N ring coefficient capacity, an additional message/body channel (e.g. CM-GLWE), restricted message subset, or other state. This is an information/correctness capacity statement, not a lower bound for ciphertext batching in other representations.

## Positive doubled-degree ring construction (source-inspired, not new)

Let R_N=Z_Q[X]/(X^N+1), R_2N=Z_Q[Y]/(Y^(2N)+1), with X=Y². Two GLWE ciphertexts C0=(a0,b0), C1=(a1,b1), **same** secret s in R_N, distinct independently uniform a_i. Pack

  S(Y)=s(Y²),
  A(Y)=a0(Y²)+Y*a1(Y²),
  B(Y)=b0(Y²)+Y*b1(Y²).

Then B-A*S=(m0+e0)(Y²)+Y*(m1+e1)(Y²), exactly. The interleaved A remains uniformly distributed over the whole R_2N if a0,a1 are independent uniform; **no public mask zeroing or mask correlation** is needed. This property does not, however, grant full 2N-dimensional secret entropy: S has only N independent coordinates and an attacker can project even and odd ciphertext components into two R_N RLWE samples. Suitable smaller-ring security parameters must be chosen, not assumed.

One large-ring GGSW under S encrypting μ(Y²) updates both lanes with one ExtProd. For AP automorphism σ_t:Y→Y^t (odd t), after applying the AP key with secret image σ_t(S), output plaintext is μ(Y²)*σ_t(B-AS). Its even lane is μ(X)*σ_t(m0+e0), the odd lane is X^((t-1)/2)*μ(X)*σ_t(m1+e1). Thus odd lane has a **public monomial correction** X^(-(t-1)/2); this does not require a new secret-dependent key switch within this toy interface.

## Full encrypted toy verification

`/mnt/data/boot_B075/verify_b075_packing.py`, SHA256 `fa60a0b24b341cdef001d0046d70a4b0256df91d7e0a3056c4abff88b642e013`.

Parameters: N_small=8, N_packed=16, Q=65537, gadget base16, exact centered gadget length5, ternary small secret, independently uniform GLWE masks, primitive GGSW/key noise coefficientwise uniform {-1,0,1}, random monomial selectors X^a (a∈{-2,..,2}), seed 75120. Original GLWE ciphertext messages arbitrary random ring polys (not only monomials). Verify all modular ring/matrix computations and exact key-row error propagation (not simply decrypt/noise threshold). Results `b075_results.json`, SHA256 `fc5b1cd30da28f84a4f8eb20c4a3adfe2fa1f767d69e77bccb873eeaa47df05d`.

- 180/180 exact shared-secret packing/decryption checks.
- 540/540 exact ordinary external-product error-recurrence checks (packed plus two controls).
- 180/180 valid two-message packed ordinary external-product output checks.
- 300/300 exact nontrivial AP external-product error-recurrence checks (100 packed, 100 each separate).
- 200/200 nontrivial AP output lane recovery checks (two lanes per trial); secret tags under base S after AP correctly typed.
- Input packed public masks remain independent uniform when decomposed by even/odd extraction: 180/180 structural checks.
- Toy ordinary external-product output noise RMS medians: independent small outputs combined 30.117, packed large output 41.135, paired median ratio 1.379. AP noise median RMS 29.900 small versus 40.708 packed. Not DFR; toy distribution and dimensions insecure.

## Decisive online arithmetic cost gate

For ring degree N and k=1, gadget length d, a single GGSW external product takes approximately 2d forward NTTs, 2 inverse NTTs, 4d degree-N polynomial pointwise products, with GGSW coefficient storage 2d*N per ciphertext polynomial component. Compare two independent degree-N products to one degree-2N product at same d:

| Operation measure | Two R_N AP products (N=8, d=5) | One R_2N AP product (degree=16, d=5) |
|---|---:|---:|
| external-product invocations | 2 | 1 |
| forward NTT calls | 20 | 10 |
| inverse NTT calls | 4 | 2 |
| modular pointwise multiplications | 320 | 320 |
| radix-2 NTT butterfly units (forward+inverse) | 288 | 384 |
| stored GGSW row polynomial coefficients (excluding mask/body 2×) | 160 | 160 |

The ~4/3 butterfly ratio at N=8 is from N log2 N; it tends to 1+1/log2 N (≈1.10 at N=1024) for 2 lanes. There may be wall-clock savings from launch count, memory access, vectorization or hardware throughput, but NONE are measured or shown. **Raw ring arithmetic did not decrease.** When packing independent secrets via alternate CRT idempotents, canonical small-error and security distributions are a separate unsolved problem; not analyzed as an actual construction this round.

## Distinct AP secret-index request gate

Two independent LWE inputs usually request different automorphisms σ_{t0} and σ_{t1}, since their phase-coefficient histories differ. The global automorphism σ_t on the packed ciphertext induces the **same** local t mod 2N on both lanes, apart from the explicit odd-lane monomial correction. A single global σ_t cannot realize general independent requests t0!=t1 on arbitrary plaintext polys without another lane-specific transform. On monomials 1 and X, a fixed postmultiplying monomial cannot change the action exponent independently (it must fix 1, hence be 1). For N=8, among 8×8=64 pairs of odd local exponents, only 8 pairs agree with one global exponent and 56 are not representable by the direct shared-σ candidate. This gate does not rule out more expensive idempotent/slotwise operations or an entirely different batching representation.

## Conclusion / decision

STATUS `PASS_ENCRYPTED_PACKING / FAIL_ONLINE_ARITHMETIC_SAVING / FAIL_DISTINCT_AP_GENERALITY / UNCLEAR_MATCHED_SECURITY`.

We built and tested a valid **restricted** packed AP circuit with independent random public masks. Its apparent saving from 2 AP calls to 1 is an artifact of doubling the ring degree: pointwise arithmetic and key coefficients stay constant, FFT butterfly work increases, and original small-ring secret dimension persists. General independent AP exponents also don't combine in one σ. Published work already covers the high-level batching/packing objective much more effectively. **Archive this direct shared-selector doubling construction**; no new publishable BOOT primitive and no security-matched performance claim.

NEXT_TEST B076 (not started): a more promising cross-paper hypothesis is to examine whether BatchBoot's sparsity-dependent amortization can use Ma et al.'s **dense-secret subring encapsulation** (dense in N' but sparse embedded in N) without violating the smaller-ring dense-RLWE security estimate, input ciphertext conversion noise, batch ring type and throughput. Prior-art search must precede any novelty claim; cheapest decisive test is one exact RingSwitch/selector-compatibility lemma and h-vs-N' noise/security budget, not immediate native benchmarks. If already known, kill early.

STATE_UPDATE NO: existing `findings/boot-STATE.md` listed ~187967B but connector previously returned empty object. Preserve original without overwrite, append this finding only. SHIP unchanged.