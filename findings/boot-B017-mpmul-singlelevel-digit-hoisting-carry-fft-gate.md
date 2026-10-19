# BOOT B017 — Per-ciphertext gadget hoisting across MPmul differences: real-source carry and FFT gate

TRACK_ID: BOOT
DATE: 2026-10-19
ITERATION: B017
STATUS: FAIL_EXACT_DIFFERENCE_HOIST / FAIL_TRANSFORM_COUNT_SAVING / STRONG_NEW_PRIOR_ART_FOUND
STATE_UPDATE: YES

## One primary technical hypothesis
For Guimarães–Pereira MPmul (2025/686) with real FBS1/FBS2 one-level approximate RGSW gadget, each stage computes one difference ciphertext d_j=c_{j-s}-c_j and its digit decomposition. Hypothesis: pre-decompose and Fourier-transform each of the n input ciphertexts just once and form Fourier-domain differences, avoiding the original n difference FFTs at negligible correction/noise cost.

This is the hypothesis tested. It does NOT assert a generic impossibility of hoisting, which is actually achieved in a different and prior-art method below.

## Read-before-write, precise provenance
[FACT] 2025/686 ePrint verified-title VERSION_UNVERIFIED 34-page mirror SHA256 84b694a59fe50dc0062ff9f24bd26f1a9cdc335. Source phys pp. 11–12, Algorithm 1: for each encrypted bit i and each output index j, CMUX(c_j, c_{j-2^i}, C_i) (or negacyclic wrapped automorphism) uses ONE GSW external product on their RLWE ciphertext difference. Section 7.1/Table 3 p.23 gives FBS1 N=2048, ell_A=1, Bgbit=23, q=2^64; FBS2 N=8192, ell_A=1, Bgbit=22, q=2^64; Table 4 is a DIFFERENT HW-reducing KSK.
[FACT; SOURCE CODE INSPECTED] Authors' public repo https://github.com/antoniocgj/Fast-Amortized-Bootstrapping, default branch viewed 2026-10-19 (no immutable commit pinned). src/sparse_amortized_bootstrap.c, lines ~215–245: CMUX computes trlwe_sub(in2,in1), calls trgsw_mul_trlwe_DFT on difference, then trlwe_from_DFT and trlwe_add. RGSW_monomial_mul uses n CMUX/NCMUX outputs per bit and overwrites stage buffers; input list changes between stages.
[FACT; SOURCE CODE INSPECTED] In src/mosfhet/src/trgsw.c, lines ~384–412, rank-one trgsw_mul_trlwe_DFT calls polynomial_decompose_i and polynomial_torus_to_DFT for EACH of two input RLWE polynomials at ell_A=1; one selector key already pre-FFT. In src/mosfhet/src/polynomial.c lines ~74–89, *optimized single-digit routine polynomial_decompose_i* includes additional low-bit rounding offset; in src/mosfhet/src/trlwe.c lines ~607–630 a DIFFERENT general trlwe_decompose omits this low-bit offset for its all-at-once routine. B017 is about the optimized single-digit routine ACTUALLY called by rank-one FBS path, not the general routine.
[FACT] Lee et al. ePrint 2023/958, p.16, already hoists/reuses a common accumulator decomposition and FFT for multiple RGSW keys inside ONE block. This does not imply distinct MPmul ciphertexts across output indices share the same decomposed operand.
[CRITICAL PRIOR ART; official full PDF VISUALLY INSPECTED] Zhihao Li et al., "BatchBoot: Fast Batched Bootstrapping for TFHE Scheme and Practical Applications", 35th USENIX Security Symposium, Aug. 2026, USENIX official paper page https://www.usenix.org/conference/usenixsecurity26/presentation/li-zhihao and freely accessible full 20-page prepublication https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_li-zhihao.pdf . Abstract p.1 and Section 4.1 PDF pp.5–6 explicitly cite 2025/686 "AmortBoot" and introduce EMPmul with multibit CMUX and *a different FFT/Decom/automorphism hoisting*. Their Eq.(8) lets automorphism X->X^-1 penetrate the Fourier/gadget stage and shares FFT work between automorphism and external products; Table 2 counts FFT vs Hadamard operations for grouping delta=1,2,3,4; authors report 2.4x improvement vs AmortBoot in their experiments. This is direct source-verified near-exact prior art, not B017 invention, and modifies interpretation of B016 and B017: algorithmic transform-saving multi-bit variants have ALREADY BEEN DEVELOPED. The authors' 2.4x is not our result.
[QUALITY] GitHub default branch was not pinned, so code may evolve; no native code execution, benchmarking, RLWE DFR/security simulation or file modifications outside BOOT. Main authors' 2025/686 paper is mirror version unverified; BatchBoot is official freely accessible PDF, pages 1,4,5 visually checked.

## Exact gadget rule in the real CMUX implementation
[DERIVATION FROM C CODE, modulo unsigned 64-bit] For one level ell_A=1 and Bgbit=b ∈{23,22}, set B=2^b, G=2^(64-b)=Q/B, H=B/2, word mask 2^64−1, offset=2^63+G/2. The optimized source's signed digit function on 64-bit torus word x is
    D_b(x) = (((x+offset mod 2^64) >> (64-b)) & (B−1)) − H,
a balanced B digit in [-H,H−1]. Its reconstruction is D_b(x)*G modulo 2^64 and centered remainder r_b(x)= x−G D_b(x) mod Q lifted to [-G/2,G/2), including a particular tie-breaking at G/2. Unlike the general trlwe_decompose, optimized polynomial_decompose_i rounds nearest using +G/2.

For any two words a,c:
    D_b(a−c) ≡ D_b(a)−D_b(c)+κ(a,c) (mod B)
where the carry κ is in {-1,0,1} and
    κ = [r_b(a)−r_b(c)−r_b(a−c)]/G
with local integer lifts. Because r_b(a), r_b(c) ∈[-G/2,G/2), the direct difference may exceed half-step and require a nonzero κ. The full equality in signed digit integers also incurs a canonical-reduction correction of ±B if D_b(a)−D_b(c) leaves centered digit range; this ±B changes the G-weighted reconstruction by ±Q=0 mod Q but still changes evaluation-key Gaussian error if multiplied by noisy GSW ciphertext.

[DETERMINISTIC COUNTEREXAMPLE] Choose a=G/4 and c=−G/4 mod Q (both legal words, no encryption noise). Then D(a)=D(c)=0, while D(a−c)=D(G/2)=1. Hence D(a−c) !=D(a)−D(c), already at one coefficient. A polynomial with the same pair at every coefficient makes κ(X) identically 1 (all N coefficients nonzero); the correction can be *completely dense*. A sparse-correction-only FFT is therefore not a generic exact method.

## Cheap decisive independent reference test
[COMPUTATION] Reproduce optimized unsigned-64-bit source C shifts and wraparound in NumPy uint64 with seed 20261019. For each b=23 (FBS1) and b=22 (FBS2), sample 2^20=1,048,576 independent uniform pairs (a,c) of 64-bit torus words; compute D(a),D(c),D(a−c), κ centered modulo B, and direct raw digit difference. The observed results:
  b=23: P(κ!=0)=0.2500810623 (262229/1048576); P(|D(a)−D(c)|>=B/2)=0.2503690720; P(D(a−c) != D(a)−D(c) in signed integers)=0.4376153946.
  b=22: P(κ!=0)=0.2494077682 (261523/1048576); P(|D(a)−D(c)|>=B/2)=0.2502336502; P(full signed integer mismatch)=0.4371547699.
All κ values are in {-1,0,1} after reduction modulo B; source-accurate residue/carry identity tested on all sampled pairs.
The mean squared modulus-normalized raw digit difference is ~2x fresh digit, as expected for independent uniform original digits; and the raw centered remainder difference has empirical variance / fresh decomposition remainder variance 2.0003233 for b=23, 2.0003740 for b=22. These are algebraically plausible *input-independent random torus word* statistics, NOT actual MPmul ciphertext distributions, security or final-DFr error.

[SIMPLE MATHEMATICAL MODEL] If centered remainder r_b(x) were independent continuous uniforms over [-G/2,G/2), then r_b(a)−r_b(c) has twice the variance of a single residual, and Pr(|r_a−r_c|>=G/2)=1/4. Source near-25% carry observations agree. For approximate GSW external product one cannot naively treat residuals as independent of the secret, key noise, or current accumulator; therefore 2x is an illustrative variance cost, not a validated DFR inflation factor for the full FHE pipeline.

## Transform-count falsifier for this precise hoisting schedule
[DERIVATION FROM SOURCE CODE] At one MPmul bit stage on n distinct ciphertexts c0,...,c_(n-1), each RLWE ciphertext has k+1=2 ring polynomials. The source constructs n distinct coefficient differences d_j, then external product uses 2n forward FFT transforms across digit polynomials; n outputs of 2 RLWE polynomials are converted back with 2n inverse transforms (GSW keys pre-transformed). Ignoring per-wrapped-output automorphism transforms, baseline count per stage = 2n forward + 2n inverse.
Proposed "predecompose every c_j" hoist still preprocesses n ciphertexts × 2 polynomials = 2n forward FFT transforms, then subtracts FFT-domain digit vectors O(nN), followed by unchanged 2n inverse transforms. No main-transform count saving even when κ is ignored and all n stored transform-domain digits are reused in the same stage. If exact difference digits are demanded, κ is dense at ~25% of random coefficients and can be fully dense on legitimate polynomial words; evaluating FFT(κ) per output costs new transforms (or equivalent dense work), cancelling the proposed shortcut further.
Every bit stage overwrites c_j through ciphertext CMUX and inverses, so precomputed digits cannot be carried to the NEXT bit stage unless one proves new update identities and accounts for noise/error; this naive hoist does not supply them.
The proposed approach might reduce a small *linear-time* coefficient torus subtraction, but requires *linear-time* Fourier-domain vector subtraction and pre-storage, so no proof of real speedup without profiling; no reduced FFT count or key size is established.

## Interpretation of the independent 2026 BatchBoot success
[FACT] BatchBoot achieves FFT reduction because (1) it groups adjacent selector bits using a multi-bit CMUX layout, trading more prepared selector rows/Hadamard work, and (2) it lets the negacyclic automorphism of an RLWE ciphertext interact with decomposition/FFT so the SAME operand transform is shared between key variants. This is NOT the same as D(a−c)=D(a)−D(c) hoisting; its source Eq.(8) and Table 2 explicitly account for FFT vs Hadamard.
[DERIVATION] Our B016 four-choice rank>=3 scalar external-product lower bound remains correct under its restricted model; BatchBoot does not contradict it because it uses multi-bit RGSW key patterns and a changed computation pipeline to reduce expensive FFTs, not a claim that generic four-way choice is one standard scalar external product. The correct comparison is FFT/Hadamard/automorphism/keys/runtimes at equal security and DFR, not merely scalar product count.

## Decision
STATUS: FAIL_EXACT_DIFFERENCE_HOIST / FAIL_TRANSFORM_COUNT_SAVING / STRONG_NEW_PRIOR_ART_FOUND
RESULT: Genuine source's optimized balanced digit is nonlinear under subtraction; ~25% frequent carry and a fully dense worst case; per-stage preprocessing one transform per original operand polynomial saves zero transforms because there are n outputs and n inputs; ignoring correction doubles an idealized residual variance and changes key-error digit norms, so cannot inherit DFR. A newer DIRECT prior-art BatchBoot published 2026 already solves much of the practical FFT bottleneck via a different multi-bit/automorphism hoist and reports 2.4x vs 2025/686. NO novel bootstrapping optimization is established here.

NEXT_TEST B018: SOURCE-READ BatchBoot official Sec.4.1 Eq.(8), Alg.2, Lemma4.1, Table2 and Section 5 parameters. One primary falsifiable question: Does its exact claimed FFT/Hadamard advantage for delta=2 persist when contrasted against 2025/686's TRUE one-level approximate gadget (d=1, Q=2^64), after accounting for all Hadamard products, FFTs, added grouped selector key storage, and actual security/DFR constraints? Begin by reproducing the source operation-count equations (cheap kill test); distinguish source's measured speedups from any new contribution. If nothing is unexplained, close this subtopic, select a NEW primitive/structural performance bottleneck from the official BatchBoot implementation (if code available) instead of re-deriving prior art. User decision on further directions.
STATE_UPDATE: YES; all changes confined to BOOT-owned files.
