# PURE-FHE · P0-PRESCOUT-53 — Fourier-character SIMD secret shift versus negacyclic LUT extraction rank

Date: 2026-10-27 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
PREVIOUS: P0-PRESCOUT-52; findings/pure-fhe-p0-52-mpmul-two-sheet-tensor-gsw-cost-gate-2026-10-27.md; commit 1af8e9ff65038f78698dce386a75830f6e003632
LATEST_COMPLETED: P0-PRESCOUT-53
NEXT_ITERATION: P0-PRESCOUT-54 NOT_STARTED
STATUS: PASS_EXACT_CHARACTER_TWO_SHEET_SEMANTICS / FAIL_SINGLE_GALOIS_ALL_SLOT_CYCLE / FAIL_GENERIC_CHEAP_LINEAR_NEGACYCLIC_LUT_EXTRACTION / NOVELTY_NOT_ESTABLISHED / STAGNATION_HUMAN_REVIEW
NOVELTY: NOT_ESTABLISHED; Fourier decomposition, BFV batching and BFV polynomial functional bootstrapping are prior knowledge/techniques, not a new mechanism.
STATE_UPDATE: YES isolated PURE-FHE finding only; NO global STATE.md or changes to BOOT/SHIP/CGS/VFHE/EAI.
CODEX_REQUIRED: NO; no native FHE code, GPU, servers, model downloads, environment changes or experiments authorized.

## Smallest falsifiable H53

Can P0-52's faithful two-sheet semilinear hidden monomial shift avoid the Θ(nN)-dimension tensor RGSW key by evaluating original X-exponent polynomials at a primitive root ω, batching the two scalar sheets into ordinary BFV/BGV SIMD slots, and retaining BOTH (i) near-one packed controlled rotation per secret bit and (ii) cheap ordinary TFHE programmable LUT extraction to output refreshed LWE ciphertexts for ANY original source-valid negacyclic LUT?

Cheapest decisive tests:
1. Source-first original MPmul 2025/686, BFV batching Galois action and closest Liu–Wang 2023/910 batched functional bootstrapping.
2. Algebraically verify root-of-unity semilinear map at small exact field and 2-sheet periodic shift.
3. Test whether a single automorphism can perform a 2n-slot cyclic move in a fully split ordinary power-of-two BFV ring.
4. Check Fourier CHARACTER RANK needed by even the simplest valid TFHE negacyclic LUT constant-coefficient readout. This single rank gate can KILL general cheap LUT readout without inventing noise/performance measurements. Avoid launching Codex.

## [FACT] Primary sources and provenance

1. Antonio Guimarães and Hilder V. L. Pereira, *Fast Amortized Bootstrapping with Small Keys and Polynomial Noise Overhead*, CCS2025, ePrint2025/686, https://eprint.iacr.org/2025/686 . Cached original 34-page GitHub Notes mirror sha256 84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335; revision unverified. Algorithm1 §§3 pp10–12 directly read in P0-51/52: a list of n R_X-RLWE encryptions of X^{u_j}, special wrap τ(X)=X^-1, n EP per bit of encrypted v, and test-vector times X^{phase} subsequently extracted as constant coefficient. The test-vector property lets arbitrary NEGACYCLIC functions be represented with one plaintext polynomial; extracting its constant coefficient from a GLWE is a public linear ciphertext map (key-switching to the desired outgoing LWE secret may still be required). Present H53 must preserve this output type/functional scope to compare at all.
2. *Revisiting the Slot-to-Coefficient Transformation for BGV and BFV*, ePrint2024/153, https://eprint.iacr.org/2024/153 , ORIGINAL 23-page GitHub Notes mirror sha256 df89b65378023e2ae24f63f6a47778072192515c9a75a40da62c7ac8c183726f; §3.1 p8 directly read. For 2-power conductor m≥8 the group (Z/m)^×=〈5〉×〈−1〉≅C_{m/4}×C_2, not cyclic; BFV plaintext slot arrangement depends on splitting degree. Also Microsoft SEAL official code docs https://github.com/microsoft/SEAL/blob/main/native/examples/2_encoders.cpp confirms BFV/BGV fully split batch slots arranged as 2×(d/2), and evaluator rotate_rows/rotate_columns are distinct https://github.com/microsoft/SEAL/blob/main/native/src/seal/evaluator.h .
3. Liu and Wang, *Amortized Functional Bootstrapping in less than 7ms, with Õ(1) Polynomial Multiplications*, ePrint2023/910, https://eprint.iacr.org/2023/910 (indexed 29-page PDF textual lines from web; direct screenshot attempted on physical pp4/19/21 but failed 403/cache miss). The authors ALREADY use BFV batching over a prime plaintext field and BFV polynomial evaluation, support arbitrary LUT f:Z_p→Z_p and have a distinct BFV→LWE extraction/scheme-switching cost. Original indexed 2023/910 §6.1 p19 writes a full finite-field polynomial fpoly for arbitrary LUT and §4 pp12–15 discusses SlotToCoeff and BFV RLWE→LWE. This is CLOSE PRIOR ART for the general BFV/SIMD/finite-field conversion target, not a claim that their specific algorithm equals our two-sheet character shift. Their published author 6.7ms/9-bit timing is their own result, NOT ours. GitHub Notes attempts to fetch full original via eprint_id 2023/910 returned INVALID_PDF, so theorem-by-theorem review of this paper remains incomplete.
4. Other nearby packed/functional bootstrapping algorithms include 2025/686's own GPvL23 comparison, USENIX2026 BatchBoot https://www.usenix.org/conference/usenixsecurity26/presentation/li-zhihao, and TFHE coefficient extraction background https://fhetextbook.github.io/CoefficientExtraction.html . Their existence constrains novelty; no speculative claims of an original efficient scheme.

## [DERIVATION] Faithful character map and two-sheet semantics (PLAINTEXT ONLY)

Let R_X=Z_q[X]/(X^N+1) and choose a finite field F_t with L=2N | (t−1), primitive L-th root ω∈F_t, so ω^N=−1. Evaluation φ_ω:R_X (with compatible coefficient reduction mod t)→F_t sends X^u↦ω^u, faithfully respects negacyclic sign X^N=−1. For arbitrary polynomial m(X) under ω evaluation,
  φ_ω(τ(m)) = m(ω^-1), where τ:X↦X^-1.
This is NOT simply inverse of φ_ω(m) for arbitrary polynomial m, only for monomials. Important because the original plaintext might be public testvector t_j(X)*X^{phase}.

For a vector of n plaintexts m_j(X), define two-sheet scalar vector
  A_j=m_j(ω), B_j=m_j(ω^-1), j∈[0,n).
Form S=(A_0,...,A_{n−1}, B_0,...,B_{n−1}) over F_t. A cyclic right shift by v∈[0,n) gives first sheet
  S'_j =A_{j−v} if j≥v, B_{n+j−v} if j<v;
and second sheet is evaluations of τ applied to corresponding first sheet plaintexts, because τ²=id. Therefore the *algebraic MPmul semilinear wrap* is exactly representable as an ordinary 2n-cycle on scalar sheets.

This can in principle store 2n scalar values in ONE fully split BFV plaintext of degree d=2n, unlike the P0-52 tensor over R_X of degree 2n*N. Yet encrypted control of this shift, full security, FFT and output extraction are not provided by the plaintext identity alone. Original initialization sometimes uses PUBLIC LUT polynomials, but later public monomial multiplications must update each scalar sheet with ω^{±a_j}; this is plaintext SIMD multiplication with public encoded factors and must be costed.

[TOY_EXECUTED, exact finite field] t97,N8,L16,n4, ω=8 (primitive 16th root); checked ω^8=−1 mod97 and ω^16=1; 64 deterministic-seed trials with FOUR RANDOM POLYNOMIALS of degree<8 and random v∈{0,1,2,3}, verified both two-sheet cyclic shift components match φ_ω of exactly prescribed τ-wrap plaintexts: PASS64/64. No ciphertext operations/security/DFR/timing.

## [DERIVATION] First obstruction: one BFV Galois cannot produce a full 2n-slot cycle

For an ordinary fully split BFV/BGV power-of-two cyclotomic ring with ring degree d=2n≥8, conductor m=2d, its slot permutation automorphism group is (Z/m)^×≅C_2×C_{m/4}=C_2×C_n. The order of any element is ≤n; a 2n-slot single cyclic shift has order 2n. Thus no SINGLE automorphism (hence no single ordinary BFV rotate_rows) exactly implements the 2n-cycle. Explicit tiny d8,m16, units orders {1:1,3:4,5:4,7:2,9:2,11:4,13:4,15:2}, max4<n*2=8.
The desired cycle CAN be realized via public masked sums/compositions of multiple independent Galois rotations and row swaps, or by choosing a larger different ring with a row long enough. That adds multiple KSK/linear operations or slot underutilization and potentially different security parameters. The non-cyclic fact does NOT prove the packed shift itself impossible or prohibit sublinear work; it kills ONLY the naive 'one native Galois permutation across all 2n slots' shortcut.

## [DERIVATION] Second and more decisive obstruction: loss of cheap arbitrary TFHE LUT extraction

Original (T)FHE functional bootstrapping represents a NEGACYCLIC LUT by t(X) in R_X with N coefficients; the desired output for phase u∈Z_L is f_t(u)=Coeff_0(t(X) X^u). The negacyclic condition forces f_t(u+N)=−f_t(u). Coefficient extraction is linear on the ring plaintext, yet character compression m(X)→m(ω) keeps only ONE evaluation of that polynomial, generally insufficient to compute its constant coefficient linearly.
In split field F_t, every function f:Z_L→F_t has unique Fourier expansion
  f(u)=Σ_{k=0}^{L−1} fhat_k ω^{ku},
  fhat_k=(1/L)Σ_{u=0}^{L−1}f(u)ω^{-ku}.
A linear decoder from a chosen set K of character features {ω^{ku}:k∈K} can implement f FOR ALL u exactly iff supp(fhat)⊆K, by DFT independence. Thus the minimum number of character tracks needed for a linear readout is r=|supp(fhat)|. This is elementary representation/Fourier analysis; NOT a new theorem nor a lower bound for nonlinear encoding/output maps.
For VALID negacyclic f_t, fhat_k=0 for EVEN k; generic such f has all N ODD Fourier modes nonzero. Take the simplest legitimate input testvector t(X)=1:
  f_0(u)=Coeff_0(X^u)=1 if u=0, =−1 if u=N, else0 (u mod 2N).
  fhat_k=(1/L)(1−(−1)^k)=0 if k even, 1/N if k odd.
Hence its exact linear character decode requires N independent frequencies, although the input negacyclic LUT uses only ONE N-coefficient public plaintext t(X) and a cheap *coefficient extraction* in native TFHE. Scalar φ_ω cannot preserve this cheap readout. Under this exact f_0, the UNIQUE interpolating polynomial P(z) on all L roots has
  P(z)=(1/N)Σ_{j=0}^{N−1} z^{2j+1}
with degree L−1=2N−1, implying any ordinary degree-bounded arithmetic circuit computing P from ONE character scalar z via additions and binary multiplications has multiplicative depth ≥ceil(log2(2N−1)); this is not a time lower bound for all specialized FHE constructions and can be bypassed by different output representations/large keys/alternative bootstrapping.
More generally outputting arbitrary *non*-negacyclic f across L phase values can require all L characters; do not erroneously use delta_{0} alone as a source-valid original TFHE negacyclic LUT. The valid signed delta pair above gives source-relevant exact N-mode rank.

[TOY_EXECUTED, q97] With N8,L16,ω8, t(X)=1, f0=[1,0,...,0,-1,0,...,0] length16. Exact modular DFT gave fhat_k=85=1/8 mod97 for all 8 odd k, zero for 8 even k; polynomial representative has degree15. Additional spectrum examples unrestricted across L gave delta16, identity16, mod4 rank4, parity rank2, step-half9; IMPORTANT parity/mod4 as ordinary functions of phase are NOT necessarily negacyclic TFHE LUTs, so those spectra are illustrative SPECIAL FUNCTION classification only, not proof of directly substituting for source PBF.

Consequently no cheap arbitrary negacyclic LUT under the single-character SIMD representation with ONLY linear readout; a post-processing polynomial or additional characters/slots is required and will cost multiplication depth, memory, key switching and final BFV→LWE conversion. The candidate thus simply trades the MPmul EP workload for a potentially large LUT/decode workload rather than removing it.

## [PRIOR ART AND OPEN CLASS] Potential restricted-Fourier class isn't a new scheme yet

If a target function's phase dependence is itself Fourier-sparse with r≪N odd harmonics (e.g. f(u)=ω^u+ω^-u is a mathematically valid negacyclic function with 2 Fourier modes), it could be monitored in O(r) tracks with native SIMD operations and linear combination. But:
  - Such functions often have field-valued outputs rather than the desired small integer plaintext; the output LWE message format and noise robustness to source e must be established.
  - A real TFHE functional LUT f(u) typically needs to be constant over noisy decoding bins and anti-periodic, which can be Fourier dense.
  - BFV→LWE slot conversion is a nontrivial key-switch/linear transform, already tackled in Liu–Wang2023/910; no evidence this alternative route improves on their construction or BatchBoot2026 at matched security, function and DFR.
  - Native group action of 2n-slot cycle is nontrivial, added Galois keys may erode gains; source full PDF 2023/910 unavailable for independent full algorithm comparison.
Thus only an **UNPROVEN conditional specialty** may remain, not a new general FHE construction. Random more small t/FFT toys not worth it.

## End of Iteration

STATUS: PASS_SCALAR_SEMILINEAR_TWO_SHEET_EXACT / FAIL_NATIVE_SINGLE_GALOIS_2N_CYCLE / FAIL_GENERIC_CHEAP_LINEAR_LUT_READOUT / NOVELTY_NOT_ESTABLISHED / STAGNATION_HUMAN_REVIEW
RESULT: 64/64 scalar-shift small-field exact tests PASS. For degree2n split BFV power-of-two ring, automorphism order ≤n precludes a one-step 2n-cycle. Even a source-VALID negacyclic coefficient extraction LUT t(X)=1 has N nonzero ODD Fourier characters and degree2N−1 as a scalar-root interpolation; no cheap single-character *linear* extraction. Liu–Wang2023/910 has nearby BFV SIMD+arbitrary functional polynomial bootstrap prior art.
NOVELTY: NOT_ESTABLISHED; these are classic representation/Fourier facts.
NEXT_TEST: P0-PRESCOUT-54 NOT_STARTED. Park generic source MPmul via scalar BFV root; reopen only for a SOURCE-COMPLETE function class with provable o(N) Fourier support AND cheap, matched-security LWE output conversion, or a distinctly new algebraic operator, otherwise HUMAN_REVIEW/PIVOT core Pure-FHE problem. Do not silently promise full q/FFT/DFR bound.
STATE_UPDATE: YES isolated PURE-FHE finding only.
CODEX_REQUIRED: NO.