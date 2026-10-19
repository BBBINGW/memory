# BOOT B007 — Heterogeneous T_i for squared Mat-MGSW: symmetry/convexity falsifier

TRACK_ID: BOOT
ITERATION: B007
DATE: 2026-10-19
PRIMARY HYPOTHESIS: At fixed Q, N, k, r, n, source-homogeneous bootstrapping-key noise, and a common per-ciphertext security level, varying squared-gadget Mat-MGSW key modulus T_i across blind-rotation steps yields a structurally better latency/key-size/noise frontier than one uniform T.
STATUS: FAIL_STRUCTURAL_ADVANTAGE_IN_CONTINUOUS_MODEL / PASS_SOURCE_ADMISSIBLE_NOISELESS_INTERFACE / PARK_P2
RESULT: Jensen/AM-GM shows no gain over continuous uniform T at equal total log-key storage under equal noise weights; any gain from integer bit lengths is a small discrete interpolation, and within one 64-bit machine limb it disappears from uncompressed native memory and operation counts. Real security/DFR unproven.
NEXT_TEST: B008: move within BOOT to P3, 2025/1753 free-module bootstrapping vs 2025/1892 heterogeneous/approximate gadget. First exact interface correctness counterexample, not broad implementation.
STATE_UPDATE: YES

## Provenance
[FACT] Wang, Luo, Xia, Wang, Hou, ePrint 2025/1711, 29-page VERSION_UNVERIFIED mirror PDF SHA256 0f003b5e91dfb6acd4bb48103e03127e0da94394544aa24eda1b636676ca57ff. Source physical pp. 11–15 (Sec 3.1, Lemma 3.4, Cor 3.5), p. 17–18 (GINX Algorithm 1, Thm 4.1), pp. 20–22 (STD128 configurations, benchmarking/storage complexity). Text extracted via research eprint reader; visually-sensitive math should be rechecked with a directly rendered PDF when available. IACR primary PDF attempted but returned HTTP 403. Mirror version is NOT independently verified.
[FACT] 2025/1711 external product uses square Mat-MGSW C_i in R_{T_i}^{(k+r)x(k+r)} and canonical centered lift of c in R_Q^(k+r), computes c_{i+1}=Round[(Q/T_i)*(C_i c_i mod T_i)] mod Q. The source uses T sufficiently larger than Q and condition Delta*Q^2 < T, where Delta is an integer lower-bound scale parameter; in Section 5.1 T must be NTT-friendly and Q is a power of 2.
[FACT] Source Thm 4.1 bounds GINX blind rotation under homogeneous secret/BK noise; the additive squared subgaussian parameter equals n[(k+r)N sigma^2/Delta^2 + pi(3+2kN+12 Delta^2+8kN Delta^2)/(72 Delta^2)] + sigma_0^2. Source Table 1 STD128 r=1,N=512,k=3,n=512, log2 Q=18, log2 T=41, but no heterogeneous-T benchmark.

## One cheapest decisive mathematical test: convexity
[DERIVATION, ideal continuous-modulus relaxation] Define x_i=log(T_i/Q^2). Treat Delta_i=T_i/Q^2 as a real number, an idealized relaxation of source's integer sufficient-condition Delta_i*Q^2<T_i. With all other parameters equal, per-step variance proxy is v_i=A exp(-2x_i)+B, where
    A=(k+r)N sigma^2 + pi(3+2kN)/72 >0,
    B=pi(12+8kN)/72 >0.
and V_total = sigma_0^2 + sum_i v_i.
Source raw BK size formula for r=1 and noncompressed keys: 2n(k+1)^2 N log2(T) bits at uniform T, generalizing linearly to C_size sum_i log2 T_i with C_size=2(k+r)^2 N. For fixed total log storage, sum_i x_i is fixed.
Since f(x)=exp(-2x) is strictly convex, Jensen gives
    sum_i A exp(-2x_i) >= n A exp[-2 (sum_i x_i)/n],
equality iff all x_i equal. Consequently a *continuous* uniform T_geo = exp[(1/n)sum_i log T_i] has no worse noise and exactly the same modeled total logarithmic BK size. The 2(k+r) forward+inverse transforms and (k+r)^2 pointwise products per external product in Section 3.3 are independent of T's numeric value within the same arithmetic implementation. Thus NO intrinsic arithmetic-count or continuous key-size/noise Pareto advantage comes from unequal T_i under source's equal per-step noise assumptions.

[QUALIFICATION] This is a surrogate-model result, not a theorem that prime-modulus heterogeneous schemes are forbidden. The source requires integer Delta and NTT-friendly T, so Jensen only applies exactly to a continuous relaxation, or to integer Delta with budget specified in sum log Delta. The source's security and noise model may change across moduli. If per-step coefficients A_i were unequal, a continuous optimum could allocate Delta_i proportional to sqrt(A_i); such unequal A_i were NOT shown for GINX/2025/1711. Their BK noise source uses equal sigma and structurally symmetric n stages.

## Source-compatible actual-prime discrete screen
[DERIVATION] Use STD128 *shape* n=512, Q=2^18, N=512, module rank k=3, batch r=1. These shapes come from p. 20 Table 1, but the moduli below are independently constructed toy candidates NOT claimed secure/recommended source parameters. Fix sigma = sqrt(2pi)*3.19 following paper Sec 5.1 and compute A~131079.8556512, B~536.6887450.
[INDEPENDENT COMPUTATION] Choose two prime NTT-friendly candidate moduli, each 1 modulo 2N=1024:
    T40 = 1099511592961 (40-bit), Delta40 = floor(T40/Q^2)=15, v40=A/15^2+B=1119.2658812.
    T41 = 2199023254529 (41-bit), Delta41 = floor(T41/Q^2)=31, v41=A/31^2+B=673.0881785.
Both primes, both satisfy Delta_i Q² < T_i; note choosing a prime just below a power of two changes floor Delta to 15 and 31, not 16/32.
With 128 low-modulus and 384 high-modulus stages, v_mix=(128v40+384v41)/512=784.6326042 versus all-high v41=673.0881785 and all-low v40=1119.2658812. For an explicitly *artificial* per-stage budget v_bar<=850, mixed and uniform-41 pass whereas uniform-40 fails. This is only a noise proxy, NOT a real DFR constraint.
Packed-BK bit lower-bound calculation uses 2(k+r)^2N = 16384 ring coefficients per blind-rotation index and 512 indices:
    all 41-bit: 42,991,616 bytes (~41 MiB);
    mixed 128x40bit+384x41bit: 42,729,472 bytes (~40.75 MiB);
    theoretical saving: 262,144 bytes=256 KiB, or 0.6098%.
For direct 64-bit-per-coefficient in-memory representation, both consume 67,108,864 bytes=64 MiB: zero saving. Transform count at each index remains 2(k+r)=8, pointwise multiplications (k+r)^2=16. Actual FFT/NTT speed, preparation, switching moduli, memory packing and key serialization not benchmarked, and heterogeneous T may incur overhead.
The continuous Jensen comparator for this mixture with Delta_i floor values has geometric Delta_g =15^(1/4)*31^(3/4)=25.85497 and noise proxy v_g =A/Delta_g^2+B=732.77529 (< v_mix). But Delta_g is not a selectable integer with exactly fractional average bit cost and does not define a NTT-friendly modulus; this is analytical only.

## Source-admissible noiseless algebra toy (repairs prior B006 test domain)
[DERIVATION] B006 illustrated T=128,256 with Q=16. That was outside 2025/1711's intended Delta Q²<T domain for every positive integer Delta; it was only a bare scaling counterexample, not a valid source-feasible parameter choice. This is an explicit correction.
Here use N=4, Q=16, two *prime* NTT-friendly moduli T1=769 and T2=1153 with T_i=1 mod 8, positive integer Delta1=3, Delta2=4 satisfying Delta_i Q²<T_i. Take k=r=1, zero secret S=0 and zero MLWE key noise, plaintext monomial selector matrices with square top-left entry Round(T_i/Q)*X^a. Initial ciphertext has top-component 4 X^j (message 2 mod t=8), bottom component zero. Iterate the source operation with canonical centered mod-T lift, mod-T multiplication, then coefficient-wise Round(Q/T_i) and canonical centered mod-Q storage. Exhaustively enumerate j,a1,a2 in {0..7}; 512/512 two-step combinations output exactly 4 X^(j+a1+a2) in R_Q = Z_16[X]/(X^4+1). Also 96/96 scalar centered-input choices m in {-1,0,1}, c in [-8,7] across two stages passed modulo 16. Tests are independent Python integer reference arithmetic, NOT native C++/OpenFHE and NOT secure encryption. This establishes a basic no-noise matrix/representation interface satisfying the source scale-domain lower bound, not full correct noisy FHE operation.

## Security and correctness limitations
- The above prime choices are NOT vetted for 128-bit security; no lattice estimator run and no joint multi-modulus key-distribution security proof. The public keys share a secret across two different ring moduli and may require joint rather than individual security assessment.
- The source Corollary 3.5 average-noise proof assumes specific uniform/ciphertext-distribution behavior and independence. Retaining its same A,B when different T_i are interleaved is a modeling assumption; not a proved multistep heterogeneous-modulus theorem.
- Different primes could require incompatible precomputed FFT/NTT key representations or cross-modulus conversions. Source uniform-T implementation cannot be assigned identical real runtime without a benchmark.
- Quantized prime choices can yield modest interpolation gains versus the feasible uniform set; it cannot defeat continuous Jensen, and when moduli share the same machine word size there is no basic raw-key byte saving.

## Decision and pivot
[RESULT] FAIL original P2 hypothesis as a *structural* latency/key-size/noise optimization under homogeneous noise; only marginal bit-packing interpolation appears in a toy budget and no real gain was established.
[DECISION] PARK P2 (2025/1711 + 2025/1892 through heterogeneous squared-gadget T_i) unless demonstrated nonuniform weights or hardware-specific packing gains with matched security/DFR and actual benchmarks. Source hetero gadget itself already existing in 2025/1892; do not claim novelty.
[NEXT_TEST] BOOT B008 P3 = 2025/1753 free-module bootstrapping and 2025/1892 heterogeneous approximate gadget: identify exact ring/module gadget/selector shape and seek smallest compatibility/correctness falsifier. Single primary hypothesis, one cheapest decisive test, independent source-page verification, then assess novelty and costs. No changes to other tracks.
