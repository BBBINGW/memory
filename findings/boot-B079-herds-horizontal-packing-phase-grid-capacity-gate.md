# BOOT-B079 — HERDS horizontal packing: full-precision single-key transfer gate

Date: 2026-10-20 · TRACK_ID BOOT · SHIP PAUSED

**STATUS:** `PASS_HERDS_IDEAL_ALIGNED_DEMUX / FAIL_UNQUANTIZED_D_INDEPENDENT_LUTS / FAIL_NOVELTY_DIRECT_TRANSFER / UNCLEAR_NOISE_SECURITY_MATCHED_ALTERNATIVES`

## Primary hypothesis

The horizontal gadget packing and trace/automorphism decoding of HERDS (EUROCRYPT 2026) can be transferred to single-key TFHE to implement **d independently programmable, full-domain negacyclic LUTs via one blind rotation in the same degree-N ring**, using only a single function-dependent public test polynomial, the existing bootstrapping key, and fixed public trace/extraction keys, **without quantizing the phase to a multiple of d, increasing N, or adding independent per-output function polynomials**.

This is an intentionally strong, falsifiable interpretation of a possible cross-paper optimization. It is not HERDS's actual published claim.

## Primary source and exact provenance

[FACT] Xiang, Min, Hwang, Wang, He, Wei, Yang, Zhang, Deng, Yu, *HERDS: Multi-key Fully Homomorphic Encryption with Sublinear Bootstrapping*, EUROCRYPT 2026, IACR ePrint 2025/1804, https://eprint.iacr.org/2025/1804 ; Springer DOI https://doi.org/10.1007/978-3-032-25327-9_8.

Original PDF acquired via the connected Research GitHub Notes ePrint tool from an IACR mirror: SHA256 `c08a83cea17b352df1006a7051cee26c133bf92a4212860d3cf28f6b6426e7d7`, 46 physical pages, `VERSION_UNVERIFIED`; the official ePrint listing identifies the latest revision as 2026-03-04. Formulas in extracted plaintext could lose typography. The public Springer HTML abstract independently corroborates complexity and components.

- pp4-7 Section 1.1–1.2: serial O(kn), parallel **span** O(sqrt(kn)); d packed gadget levels constructed from one party-wise blind rotation instead of d rounds; trace decode; blockwise acceleration.
- p6 precise initial public test polynomial sum_{j=0}^{d-1} g_j X^j and received encrypted sum_j g_j X^{j+phase}. **Assumes d divides phase**; achieved by tailored modulus switching rounding input phase coefficients to multiples of d.
- pp14-18 Section 3.1, Algorithm 1, Lemma 5, Algorithms 2/3, Lemma 6: binary block key, BR for d levels in one packed phase; recursive Galois automorphism / trace extraction. For Q=2^64 noninvertible d, must modulus-switch to Q/d and raise, adding noise; no free division by d. Algorithm 2 sequential trace KS roughly 2(d-1) terms, Algorithm 3 d log2(d) KS but log-depth parallelism; both also have BSK/conversion overhead.
- pp18-21 Section 3.2 Hybrid V2M accumulation and Theorem 1: combines k RLEV under different secrets with special keys; block parallelism splits n=ω1 ω2, span ~ ω1+kω2 with optimum ω1~sqrt(kn), ω2~sqrt(n/k), but total serial gadget work remains O(kn).
- k=1: no multi-party aggregation needed for a single target GLWE accumulator; HERDS gadget-level RLEV output is not required by ordinary single-key TFHE PBS. Hence naive k=1 substitution cannot in itself reduce ordinary single-key BR serial work.

[PRIOR] Multi-value PBS is established: Carpov, Izabachène, Mollimard, *New Techniques for Multi-value Input Homomorphic Evaluation and Applications*, CT-RSA 2019, https://eprint.iacr.org/2018/622, DOI 10.1007/978-3-030-12612-4_6, computes multiple outputs from one blind rotation with output-dependent auxiliary public polynomials (different interface than our restricted single-V hypothesis). Guimarães, Borin, Aranha *Revisiting the Functional Bootstrap in TFHE* (TCHES2021) and *MOSFHET* ePrint2022/515 also study improved multi-value bootstrap. Therefore one-BR many-output is NOT a new contribution.

## Strict mathematical gate: phase alignment / capacity

Let q odd, N power of 2, d=2^r|N, R_q=F_q[X]/(X^N+1). Write ONE public test polynomial V(X)=sum_{j=0}^{d-1}sum_{u=0}^{N/d-1}v_{j,u}X^{j+du}; secret phase t is encoded by rotation F_t=X^t V in R_q.

Define sigma_a(X)=X^a for odd a mod2N. With q odd define normalized trace projector
  Proj_j(F)= (1/d) prod_{w=0}^{r-1}(I+sigma_{1+N/2^w})(X^{-j}F),
so Proj_j selects exactly exponents 0 mod d after shifting by -j. Noises/ciphertext key-switches are excluded from this PLAINTEXT projector test. For t multiple d,
  Proj_j(X^t V) = X^t sum_{u=0}^{N/d-1}v_{j,u}X^{du},
allowing exact independent channel reconstruction. The d channels each have N/d coefficients; total dimension N.

For t not divisible by d, channel labels rotate: Proj_j(X^t V) depends on coefficients of the original residue class (j-t) mod d, not solely V_{j,*}. Thus the fixed decoder does not recover j-th source message channel; unknown t mod d must be carried and dealt with securely.

A stronger public function-space proof applies to ANY fixed F_q-linear decryption-side postprocessing of one public V: the map V ∈ F_q^N -> (d arbitrary target negacyclic full-domain LUTs) ∈ F_q^{dN} has rank ≤N, so for d>1 cannot be surjective. Restrict t to d-grid: there are 2N/d phase positions (negacyclic symmetry halves independent values), hence d*(N/d)=N free target values, and the aligned trace map is an isomorphism. The proof is limited to a single function-dependent V and fixed linear decoders. It does not apply to Carpov et al.'s multiple additional function-dependent output polynomials, different evaluation keys, nonlinear conversions, higher-degree rings, etc.

Elementary sample extraction witness in full domain: F_j(t)=[X^j]X^tV satisfies F_1(t+1)=F_0(t) (for d≥2), so cannot represent simultaneously arbitrary independent functions F_0,F_1 with F_0(0)=1 and F_1(1)=0. The full-output map (F_j(t))_{t=0..N-1,j=0..d-1} has rank exactly N, and augmenting it by an arbitrary impulse target gives rank N+1.

Simple counterexample N32,d4,q257,V=1+2X+4X²+8X³ and t=1: observed normalized projected traces after shifts j=0..3 have nonzero (degree,value) positions [(4,8)],[(0,1)],[(0,2)],[(0,4)]. Intended 'same original j-channel' shifted traces would be [(1,1)],[(1,2)],[(1,4)],[(1,8)]. All four channels disagree.

## Deterministic reproducible results

[TEST] `verify_b079.py`, stdlib Python; seed79020; R=F257[X]/(X^N+1), N∈{16,32}, d∈{2,4,8}, t ranges all phases. Ideal projector uses true σ ring automorphisms (signed coefficient permutation), exact modular inverse of 2, and checks polynomial identity, support and constant extraction:

| N | d | aligned traces | off-grid fixed-channel mismatches | full target dim / rank | aligned target dim / rank |
|---|---|---:|---:|---:|---:|
|16|2|2560 PASS|2560/2560|32/16|16/16|
|16|4|2560 PASS|7680/7680|64/16|16/16|
|16|8|2560 PASS|17920/17920|128/16|16/16|
|32|2|5120 PASS|5120/5120|64/32|32/32|
|32|4|5120 PASS|15360/15360|128/32|32/32|
|32|8|5120 PASS|35840/35840|256/32|32/32|

23,040 aligned trace checks PASS; 84,480 off-grid fixed-channel mismatches in random trials (not needed for proof). All 6 exact finite-field ranks agree with capacity bound; all augmented-rank counterexamples PASS.

[TEST] d-grid nearest rounding over 2N phase positions has exactly 2N/d distinct outputs, and t=0,1 collide for d=2,4,8. In an illustrative N32,d4,h16 binary support and mask coefficients 1, actual summed phase16 rounds to0 after per-coordinate grid rounding, producing an accumulated phase error16 (mod64). This is not a realistic DFR model but proves that blindly imposing the divisibility constraint changes the phase. HERDS explicitly budgets this for low-precision binary messages; a high-precision full-phase LUT cannot inherit that guarantee.

## Why no new competitive construction

- HERDS horizontal packing is ALREADY published and correctly requires aligned phase, evaluation-key trace/KS, and (for power-of-two ciphertext modulus) modulus switch/raise. It is meaningful for d gadget *levels* required by its MKFHE V2M layer, not automatically useful for k=1 TFHE output.
- For single-key ordinary one-output PBS, d independent RLEV gadget outputs are unnecessary; generating them adds post-BR key switching. A separate multi-output PBS task can reuse BR, but prior art Carpov2019 and MOSFHET already does so through DIFFERENT (extra postprocessing) interfaces.
- Simple symbolic gadget count for n1024,d4: 'd separate BR' =4096 selector updates vs packed 1024 + trace-keyswitch overhead; this compares a hypothetical task that actually needs d outputs, NOT native TFHE original single-BR PBS; not wall-time or proof of security-matched gain.
- HERDS O(sqrt(kn)) is parallel span with O(kn) serial work. Setting k=1 and using ω2≈sqrt(n) processors gives schematic span ≈2sqrt(n) with total work ≥n; it does not yield O(sqrt(n)) total gadget work. Security/DFR may worsen due to extra keys and noise.

## End of iteration

STATUS: `PASS_ALIGNED_HERDS_DEMUX / FAIL_SINGLE_V_FULL_DOMAIN_D_OUTPUT / FAIL_DIRECT_TRANSFER_NOVELTY`.
RESULT: exact phase-grid projection and rank proof, explicit off-grid counterexample, prior-art invalidates obvious single-BR multi-value novelty. Cannot assert general multi-output PBS impossibility.
NEXT_TEST B080 (NOT STARTED): One candidate to *handle encrypted phase residue mod d* while retaining horizontal packing, via a genuine cheap non-ordinary LUT/residue interface, must beat existing multi-value PBS and HERDS at matched N/Q/security/DFR; if it requires an additional full PBS or d independent function polynomials, abandon immediately. Alternatively pivot to a different family if no cost edge. No new construction in B079.
STATE_UPDATE NO: read before write; BOOT state from current GitHub Notes read_repo_file returns {}, don't overwrite existing large state; BOOT finding append-only, SHIP unchanged.

## Source links
- https://eprint.iacr.org/2025/1804
- https://doi.org/10.1007/978-3-032-25327-9_8
- https://eprint.iacr.org/2018/622
- https://eprint.iacr.org/2022/515