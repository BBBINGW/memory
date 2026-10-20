# BOOT-B077 — Dense-secret phase compression versus monomial exponent lift
DATE 2026-10-20 | TRACK_ID BOOT | SHIP PAUSED
STATUS PASS_ENCRYPTED_DENSE_PHASE_GLEV / FAIL_TORUS_POLYNOMIAL_PHASE_LIFT / FAIL_LOW_DEPTH_PRIME_FIELD_INTERPOLATION / NO_NEW_PRIMITIVE

## One primary hypothesis
A single encrypted dense-secret polynomial multiplication can replace h sparse-secret monomial operations, AND an inexpensive arithmetic phase-to-monomial conversion can then produce encrypted X^(b-a*s), yielding a genuinely less costly batched blind rotation. Test phase computation and the cheapest exponent-lift algebraic feasibility gate.

## Sources and prior art
[FACT] Guimarães–Pereira, Fast Amortized Bootstrapping with Small Keys and Polynomial Noise Overhead, CCS2025, DOI 10.1145/3719027.3765181, IACR ePrint2025/686; cached full PDF SHA256 84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335 (version unverified). Physical pp3-6: MPmul computes sparse-by-dense RLWE polynomial action IN THE EXPONENT with cost O(h N log(N/h)) GSW external-product work for N messages, avoids regular GSW multiplication and difficult deep encrypted exponent summation; signed sparse secret already considered. This does NOT offer a generic low-cost dense scalar-phase->monomial interface.
[FACT] Li et al., BatchBoot, USENIX Security 2026, https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_li-zhihao.pdf , PDF physical p4 Section3 Eq1 and p7 Section4.2: sparse binary secret with h+1 EMPmul full packed, h+k for sparse packed.
[FACT] Bernard–Joye, Approximate CRT-Based Gadget Decomposition and Application to TFHE Blind Rotation, ePrint2024/909, physical p7 Section2.2.2 defines the public-polynomial-times-GLev scalar product already. Thus positive B077 phase reduction is NOT a new primitive.
[BACKGROUND NOT FULL-TEXT VERIFIED] Liu–Wang, Amortized Functional Bootstrapping in less than 7ms, ASIACRYPT2023, ePrint2023/910; Research MCP INVALID_PDF. Do not claim full source read.

## Correct encrypted dense phase from one GLev multiplication
Let R_Q=Z_Q[X]/(X^N+1), original RLWE secret s and independent bootstrap secret z. Generate GLev_z(s) rows K_j=GLWE_z(B^j*s), each with uniformly random mask and small error e_j. For a PUBLIC polynomial a with exact gadget decomposition a=Σ a_j B^j modQ, evaluate C_as=Σ a_j*K_j, a single standard gadget scalar product; Dec_z(C_as)=a*s+Σ a_j*e_j. For original input b=a*s+m+e, Dec_z(b-C_as)=m+e−Σ a_j*e_j. This produces ENCRYPTED DECRYPTION PHASE polynomial, NOT monomials X^(coefficient) or refreshed ciphertexts. Key-circularity/KDM security and matched real noise not analyzed.
[TEST] Python verify_b077_phase_lift.py, N8 q65537 B16 d5, dense ternary s, independently random ternary z, random full masks, independent primitive errors in {-1,0,1}; 800/800 ciphertext gadget product and exact error recurrences PASS, 6400/6400 phase coefficient checks. Derived gadget noise max abs89, RMS21.34. Toy only.

## Strict torus obstruction for arithmetic-only encrypted phase lift
With Q=2^w, Delta=2^(w-b), b>=2 and N>=4, suppose ordinary R_Q arithmetic (add, subtract, multiply, public constants and plaintext-preserving relinearization/key switches) evaluates public polynomial P(x) on scalar plaintext x=Delta*t, and for all t∈Z_(2N) returns target Delta*X^t in R_Q. Exclude digit extraction, modulus-scale rounding, PBS, lookup evaluation keys that already encode nonlinearity, different plaintext representations.
For any commutative-ring polynomial P, P(x2)−P(x0) is in ideal (x2−x0)R_Q. Choose t0=0,t2=2. Input difference=2Delta, while required target difference=Delta*(X²−1) whose constant coefficient -Delta is NOT divisible by 2Delta mod 2^w for b>=2. Therefore no such arithmetic-only circuit of ANY multiplicative depth exists with this encoding. This is NOT an impossibility for all homomorphic algorithms.
[TEST] Exact ideal arithmetic 16/16 cases N4,8,16,32 × (w,b)=(16,4),(32,8),(64,8),(64,16) PASS no-go witness.

## Prime q: polynomial degree/depth gate
Over prime q>2N, a polynomial F(t)∈R_q[t] representing X^t on t=0,...,2N−1 has constant coefficient f(t) with f(0)=1, f(N)=−1 and zero at the remaining 2N−2 distinct field elements. So deg f≥2N−2, and any binary-multiplication arithmetic circuit requiring degree growth only via multiplication has multiplicative depth≥ceil(log2(2N−2)). This is a restricted statement, NOT a general PBS hardware lower bound.
[TEST] q65537, N4,8,16,32,128,1024: finite difference / exact field interpolation yields degree 2N−1, including N1024 degree2047, min multiplicative depth11.

## Decision
PASS standard gadget phase computation / FAIL free ordinary-arithmetic monomial lift. Moving dense decryption into one multiplication does NOT eliminate nonlinear exponent representation step. A new PBS/digit/lookup step would be required and its key/noise/runtime must beat existing AmortBoot and BatchBoot, not merely rename PBS. No new primitive, security proof, native runtime or DFR.
STATUS PASS_PHASE_GLEV / FAIL_ARITHMETIC_ONLY_PHASE_TO_MONOMIAL.
RESULT Exact positive toy+negative proofs, prior art confirms standard phase step.
NEXT_TEST B078 NOT STARTED: inspect Li et al. Decoupled TFHE-type Functional Bootstrapping (CCS2026) and any secure non-polynomial phase-to-exponent conversion; choose one concrete interface with actual key/noise/cost advantage vs AmortBoot, BatchBoot and AP. Stop if it is another ordinary PBS.
STATE_UPDATE NO. Original findings/boot-STATE.md cannot be safely read with current Research Notes interface, preserve original ~188KB; only append new finding. SHIP unchanged.
LOCAL BOOT_B077_handoff.zip SHA256 d85b2dcb277d49ad038387a5a7bdb37b708655f65881b65ba69a6554925f7290 has detailed 9KB report, exact script, JSON results, logs and manifest.