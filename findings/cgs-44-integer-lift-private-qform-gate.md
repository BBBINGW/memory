# CGS-44 — Large-prime integer lifting eliminates internal MPC truncation but not round, traffic, or cross-field costs

**Date:** 2026-10-15. Single PI-selected active CGS, authoritative prior checkpoint CGS-43. **One hypothesis, one decisive finite-field arithmetic/precision and cost gate**, followed by source-share compatibility sanity. Parent Okada–Takagi ePrint2025/409 standard-MLWE, 2-round, any-T no-O(LDec) pad storage OPEN. No secure MPC/FHE construction or source attack.

## Primary hypothesis [PARTIAL PASS / FAIL drop-in efficiency]

**H-CGS44:** Encode CGS43's secret negacyclic real spectral quadratic with b=198 fractional bits, and evaluate the entire resulting arithmetic polynomial over ONE sufficiently large prime Shamir field, *without interactive fixed-point truncation after each multiplication*. The direct implementation should retain O(n) secret multiplications and have sufficiently small statistical error, and its output could ideally be fed into source PartDec without a separate expensive share-conversion protocol.

**ONE cheapest decisive test:** Fully specify a dyadic-integer circuit, prove no modulo wrap at κ128/n1024/J224 example, bound BOTH public Fourier-constant and secret-weight approximation errors in the original Gaussian acceptance probability, independently check exact rational vs dyadic calculation, simulate threshold Beaver products, and compare arithmetic bandwidth. As subsequent correctness-interface check, test whether local reduction of a prime-field Shamir output share modulo source q remains an any-T Shamir sharing.

## Original paper/prior art [FACT]

- **Okada & Takagi**, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT2025, ePrint **2025/409**, https://eprint.iacr.org/2025/409. Re-read full original newer 40 physical-page Research MCP cached PDF SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301 (VERSION_UNVERIFIED), **Definition3.1 physical p12** R=Z[X]/(X^n+1), n power two, Gram(s); **§3.3 p13** real quadratic exponent for discrete lattice Gaussian; **Algorithm7 physical p29** true target secret-covariance-dependent integer Gaussian and R_q-Shamir shares, two online broadcast phases; **Lemma7.1 p30** additional smoothing, min-singular-value and noise assumptions still unchecked here. A 640-bit secure computation field is NOT necessarily source decryption R_q, so share-domain conversion is a genuine independent protocol obligation.
- CGS41/42/43 findings in repo established exact spherical proposal rejection law, under bounded coefficient condition constant acceptance ≥e^-1/(1+ε_Q), illustrative fixed J224, and the ideal REAL negacyclic half-spectrum quadratic expression with 3n/2 secret REAL multiplications/candidate.
- **Harth-Kitzerow, Suresh, Carle**, *SoK: Truncation Untangled*, PoPETs2025(4) 369–391, https://www.petsymposium.org/popets/2025/popets-2025-0135.php; fixed-point MPC truncation methods and offline/online communication are established, so simply avoiding per-multiplication truncation via delayed scaling is NOT inherently a new primitive. **Keller**, *Rep3 Reloaded: On the Cost of Function-Dependent Preprocessing in Semi-Honest 3PC with Honest Majority*, ePrint2025/919, https://eprint.iacr.org/2025/919, documents nontrivial multiplication preprocessing and truncation tradeoffs. Neither paper proves the actual specialized CGS sampler cost/security.

## ONE concrete no-internal-truncation arithmetic circuit [DERIVED]

For n even, omega_j=exp(pi i (2j+1)/n), define secret frequency weights w_j=gamma_j/[Bpub²(Bpub²−gamma_j)] where gamma_j=sum_i |s_i(omega_j)|². Let public dyadic scale R=2^b, b=198. Trusted KeyGen securely Shamir-shares integer W_j=round(R w_j) in the large computation field for j=0,...,n/2−1. For a PRIVATE integer Gaussian proposal z=(z_t), each active participant locally computes PUBLIC-LINEAR fixed coefficient transforms on shares:

X_j=sum_t z_t round(R cos(pi(2j+1)t/n)),
Y_j=sum_t z_t round(R sin(pi(2j+1)t/n)).

These are INTEGER linear operations in shares; NO secret multiplication and NO truncation are required. Then MPC computes

V=sum_(j<n/2) W_j (X_j²+Y_j²), and Q_tilde=2V/(nR³).

This uses exactly THREE secure multiplication gates per conjugate-frequency pair: X_j²,Y_j² in parallel (first nonlinear layer), then W_j*(X_j²+Y_j²) (second nonlinear layer). Thus ideal secure arithmetic cost is 3n/2 multiplications per candidate, J*3n/2 across a fixed-budget decryption. Crucially, the field contains integer V MOD p. Recovering its exact ordered magnitude later needs secure bit decomposition/compare, not naive modular interpretation. Using a dense direct dyadic Fourier matrix yields O(n²) local PUBLIC-constant field multiplies per candidate instead of fast FFT; this trades local CPU/field bandwidth for **zero internal secure truncation**. No public fast fixed-point FFT implementation/cost is claimed.

## Rigorous dual approximation bound [DERIVED]

Let F be the unnormalized complex negacyclic Fourier transform, ||F||op=sqrt(n), and tilde F the entrywise rounded public fixed-point matrix divided by R. Each real and imaginary coefficient incurs ≤δ_c=2^-b absolute error (conservative), hence ||tilde F−F||op ≤ sqrt(2)n δ_c. Secret weight error is ≤δ_w=2^-b. Under the source coefficient-bounded good-key condition, gamma_j≤Bpub²/2 and thus 0≤w_j≤1/Bpub²=:w_max.

By the operator norm triangle inequality, for every integer z:
|Q_tilde(z)−Q(z)| ≤ ||z||² × [δ_w(1+sqrt(2n)δ_c)² + w_max(2sqrt(2n)δ_c+2n δ_c²)].

This covers BOTH public FFT coefficient rounding and secret weight quantization; it assumes exact modular arithmetic without wrap and exact private z. On the CGS43 public truncation event ||z||²≤nH² with n1024,H72419, use kappa128,k2,Bmlwe2,Bpub2897,sigma0=4,J224,LDec2^20. Since rejection accept e^{-pi Q/sigma0²} is pi/sigma0²-Lipschitz for Q≥0, a sequential hybrid bounds the entire J LDec proposal-accept probability perturbation by (pi/sigma0²)J LDec nH² times the bracket above. For b=198 this is **6.165217003797446e−40**, below the allocated **2^-130=7.346839692639297e−40**. Within THIS conservative inequality b=197 does not pass; 198 is sufficient, NOT universally necessary. Proposal coordinate tail from CGS43 has an independent <2^-130 bound. Approximate exponent/Bernoulli, Gaussian input generation, secure comparison and output sampling errors are NOT included; budget still needs to allocate error for each of those separately before a theorem.

## Exact carry and field-size gate at source-shaped size [DERIVED+EXECUTED]

R=2^198; with |z_t|<H and each rounded cosine/sine bounded by R+1:
|X_j|,|Y_j| ≤ nH(R+1), bitlength at most 225.
0≤W_j ≤ ceil(R/Bpub²)+1, at most 175 bits.

Because there are n/2 frequency pairs and each contributes two squares,
0≤V ≤ n [ceil(R/Bpub²)+1] [nH(R+1)]² =: V_max.
For chosen public numbers, V_max has **634 bits** and 2V_max has **635 bits**. A **640-bit prime** p chosen above 2V_max is sufficient for all this integer-arithmetic V to be represented WITHOUT wrap and for centered representative tests, conditional on coefficient/sample bounds. It is a MORE THAN 640-bit bit-dynamic-range arithmetic circuit, not the original FHE q. One arbitrary 128- or 256-bit prime cannot directly represent the same V. Multi-limb/CRT may replace one huge field but requires carry/reduction circuitry and new cost/security analysis.

## ONE executed toy arithmetic, Beaver and cross-field tests [EXECUTED]

Reproducer /mnt/data/cgs44_integer_lift_mpc_gate.py SHA256 **ecf9a298266518a246f8b8739949261c0f009eb13c23c8ca0ae47cd594ae9e5d**.
JSON /mnt/data/cgs44_integer_lift_mpc_results.json SHA256 **025b66f5f80dab59a100db5b48f05fd81a1582f621d9734c3176b5d3d04f4e02**.
Executed with SymPy exact rational inverse, mpmath 130-digit trig/weight constants, secure-arithmetic *algebra simulation* of T2-out-of-N3 prime-field Shamir and ideal Beaver multiplication. No OT/PCG, malicious network, FHE/MLWE, or true Gaussian runtime proof.

- Small n8, k2, integer secrets s1=1+X,s2=1, Bpub=9, z=(2,-1,0,3,2,-2,1,1): exact Q=5228011/499374747. Direct dyadic frequency circuit abs error at b16:2.87436e−5; b32:1.67284e−10; b64:1.97901e−19; b198:1.90230e−61. Entire frequency V computed as exact integer and its field reduction is correctly reconstructed in an ideal trusted-dealer Beaver simulation from T2 parties.
- **Cross-modulus output obstruction:** Suppose the Gaussian value 7 is Shamir-shared in *computation field* F_101 with degree1 shares of polynomial P(t)=7+45t, giving shares (52,97,41). Reduce each share locally mod target F_17: (1,12,7). Then active sets {1,2},{1,3},{2,3} reconstruct mod17 **7,15,5**, respectively, NOT common target 7! This disproves naive per-share reduction F_p→F_q as a conversion, even when every pair originally reconstructs exactly 7 mod101. A genuine secure cross-field re-sharing/conversion or a proof that the final sampler can natively operate in source R_q is required; it can add rounds, random correlations and modulus overhead.
- All these results are exact integer/rational except controllably high-precision public trig approximations; no cryptographic indistinguishability or secure network implementation claimed.

## One explicit online-communication/preprocessing cost model [DERIVED; NOT benchmark]

At n1024,J224, 3n/2=1536 multiplication gates/candidate, **344064 secure multiplications per decryption**, 2 Beaver masked openings per gate => **688128 field elements opened per party/decryption**. At chosen **640-bit field** (80 bytes each) this is **55,050,240 bytes = 52.5 MiB PER party PER decryption** of opened-value payload, before Gaussian proposal generation, secret compare/exp/Bernoulli, first-success selection, authenticated channels, masks/triples generation and cross-field conversion. Across LDec2^20 calls it is **52.5 TiB PER party**. Dense dyadic transform requires **J*n²=234,881,024 local public-constant field multiplications** per decryption per participant in the unoptimized implementation (not secret multiplications). Pre-storing all Beaver multiplication triples for lifetime would need **360,777,252,864 fresh triples**; each triple has 3 large field elements, **78.75 TiB per party** at 640 bits, itself linear in LDec and vastly more than source's LDec scalar pad shares at conventional small moduli. On-demand OT/PCG can trade that off for further computation/communication, but no free noninteractive correlated randomness generation demonstrated.

This COST is a *specific 2-party Beaver-Shamir-style protocol payload model*, NOT a lower bound on all MPC technologies or a measured secure implementation. Some specialized truncation/preprocessing methods can outperform it; bit lengths 640 and source q may differ. The original source's two online rounds are already abandoned in this relaxed branch.

## Decision

**PASS:** a completely specified no-INTERNAL-truncation dyadic-integer spectrum circuit, rigorous combined weight+public FFT approximation bound at b198, source-sized integer overflow budget, exact rational and ideal Shamir/Beaver n8 controls.
**FAIL:** original CGS43/42 simplified 64/128-bit single-field low-cost interpretation; naive local reduction of output Shamir shares from F_p to F_q; treating Beaver triples pre-stored for all LDec as a memory saving.
**UNCLEAR:** true private multivariate discrete Gaussian proposal sharing, private integer-to-Bernoulli exp/compare and first-success selection, efficient source R_q re-sharing, authenticated/adaptive T-of-N robustness, source MLWE key/eval security, practical cost and contribution.
**Recommendation:** PARK the direct dense 640-bit Beaver implementation as an efficiency candidate under the original low-round/no-O(LDec) goal. Do NOT globally rule out optimized CRT/bit-decomposition or online correlation generation; they require a fresh concretely priced protocol and new security proof. The original O(LDec) under standard MLWE/two rounds remains OPEN.

**ITERATION: CGS-44. STATUS:** PASS arithmetic/quantization, FAIL direct cheap single-field/drop-in MPC protocol, HUMAN_REVIEW longer interactive rejection branch. **NEXT CGS-45 (only when PI next "继续"):** ONE smallest explicit secure *cross-field output conversion* (from large-prime sampler field to source R_q-Shamir shares) with any-T T-of-N active sets and private z, and exact added interaction/preprocessing cost. If conversion cannot be cheap, present PI option to PARK entire interactive sampler and pivot to original noninteractive secret-conditioned randomness primitive. No new automatic continuation. **STATE_UPDATE:** YES new finding, CGS parent checkpoint, sole root STATE; no unrelated files.