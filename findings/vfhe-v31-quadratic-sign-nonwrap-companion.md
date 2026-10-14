# vFHE V31 COMPANION — No-wrap four-wise sign fingerprints + one-gamma source ring sumcheck

**Date 2026-10-15. NOT a second V31 or V32.** This finding is an independent companion to the authoritative, already completed V31 `findings/vfhe-v31-transitive-representative-link.md`. Leave main V31/V32 pointer and GLOBAL general I192 FROZEN.

## Primary falsifiable hypothesis

**OUR CANDIDATE:** Given already knowledge-sound fieldwise digit-table membership for each original F.1 native CRT field component, can many short-seed four-wise independent ±1 integer sketches, compared through canonical centered integer lifts across different CRT characteristics, prove common digit-vector equality WITHOUT first committing to a shared canonical integer vector? And can original F.1/F.2 serve this as a low-cost PRIVATE/ZK proof?

**STATUS:** PASS mathematically on fixed, fieldwise bounded committed native digit data; PASS one-gamma ring sumcheck batch algebra; FAIL a *cheap/hiding/drop-in* full repair: public signed sketches identify a hidden one-hot support index, naive provers process billions of integer contributions, and source F.2 byte cost stays substantial. This is our attempted modification, NOT a flaw or originally claimed proof technique of source authors.

## Source provenance [FACT]

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, ePrint2025/286, source via Research MCP inspected 52 physical-page GitHub mirror PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, VERSION_UNVERIFIED vs 2026-02-16 official revision. §2.2 physical pp8–9: ring sumcheck, PIOP→polynomial-commitment compilation; §3.1 p10: odd-a primes p_i=1+2N/d*a_i and extension field factors; §4.3 pp20–23: small digit table t_beta, original Figure1; Appendix F.1 p50 ring PCS is CRT-native field PCS tuple; F.2 physical p51: one native multilinear evaluation opens v'=q1 U_f of length m=2^(ell/2) plus RS/Merkle checks. The proposed SIGN SKETCHES are **NOT** in the paper.

[PREEXISTING MATH] Random four-wise signed sketches are familiar from Alon/Matias/Szegedy second-frequency-moment estimation; quadratic binary Reed–Muller RM(2,ell) has dual distance eight and thus uniformly random evaluations are seven-wise independent for ell≥3. Public references include https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2010.2449 and https://www.mpi-inf.mpg.de/fileadmin/inf/d1/teaching/summer20/sublinear/lec03annotated.pdf. No novelty claimed in hashing or moment analysis.

## Algebraic construction and sharp proof [DERIVATION]

Let H=2^ell, t_beta={0,...,beta−1}; assume precommitted h has **honest per-native-field table membership**, so each CRT factor j has Boolean digit vector h_j(b)∈t_beta. For each independent public short seed θ_t, prover claims one **ring value** Y_t = Σ_{b∈{0,1}^ell} w_θt(b)h(b) ∈ R_q, with signs w_θ(b) ∈{±1}. Verifier projects every Y_t to all native CRT fields, rejects unless each value belongs to its base F_p, centers the integer representative in (−p/2,p/2], and compares the **ordinary INTEGER lifts** across all native field factors. This comparison is explicitly noncomponentwise and outside V23's product-ring gate no-go.

**Bounded no-wrap lemma:** If (beta−1)H<p_min/2, each honest native signed sum S_j=Σ_b w(b)h_j(b) obeys |S_j|≤(beta−1)H and its centered field representative is exactly the signed integer sum. If arrays differ, selecting any two offending CRT components gives δ_b=h_j(b)−h_k(b)∈[−(beta−1),beta−1], not all zero; their signed sums compare equal iff Z=Σ_b δ_b w(b)=0 as an INTEGER.

**Compact honest short-seed signs:** Uniformly sample binary quadratic polynomial Q_θ(b)=⊕_{|A|≤2} a_A ∏_{i∈A}b_i with independent Boolean a_A, and set w_θ(b)=(-1)^{Q_θ(b)}. Seed length 1+ell+binom(ell,2)=301 bits when ell=24. For ell≥3, RM(2,ell) dual distance8 implies at least 4-wise independent unbiased ±1 signs over any distinct Boolean indices. Let V=Σ_b δ_b²>0. Then E Z²=V and E Z⁴=3V²−2Σ_b δ_b⁴≤3V². Cauchy–Schwarz on Z²*1_{Z≠0} gives Pr[Z≠0] ≥ (E Z²)²/E Z⁴ ≥1/3. For T independent seeds after the h commitment, conditional Pr[all **true** sketches miss an invalid common digit vector]≤(2/3)^T. T=219 gives ≤2^(-128), while 218 does not meet this **worst-case proved bound**. No union factor count is needed: take any one offending component pair.

**Cheap evaluation function:** Over any odd native prime, publicly define
`W_θ(X)=(-1)^{a_empty} ×∏_(i:a_i=1)(1−2X_i) ×∏_(i<j:a_ij=1)(1−2X_i X_j)`.
At Boolean b, W_θ(b)=w_θ(b); at arbitrary ring challenge the verifier evaluates O(ell²) known arithmetic factors without storing a length-H public MLE. Its degree in any variable is ≤ell, so virtual polynomial h(X)W_θ(X) has degree ≤ell+1 per variable (rather than original lookup sumchecks' degree3).

### ONE source-style sumcheck and ONE F.2 MLE opening for all T sketches

Naively 219 independent source sumchecks and 219 final h(z) F.2 MLE openings cost T×native opening. **Batching is sound and decisive:** Prover first binds all T claimed ring Y_t, then verifier selects **one** independent fresh gamma in a source-valid full-extension CRT ring exceptional set AFTER those claims. Define public Y_gamma=Σ_(t=0)^(T−1)gamma^tY_t and public efficiently evaluable W_gamma(X)=Σ_(t=0)^(T−1)gamma^t W_θt(X). Verify ONE ring sumcheck
`Y_gamma ?= Σ_{b∈{0,1}^ell} h(b) W_gamma(b)`,
with ONE terminal source F.1/F.2 evaluation h(z), and verifier-side evaluation W_gamma(z) from public seeds and gamma.

If any Y_t differs from its true fixed polynomial sum in some CRT factor, its error vector defines a nonzero polynomial E(gamma) of degree≤T−1 over that factor; probability E(gamma)=0 ≤(T−1)/|S|. A forged batch sumcheck adds ≤ell(ell+1)/|S| under source Theorem2.6's ring exceptional-set projection assumptions, plus real lookup/PCS errors. Hence
`eps_conditional ≤(2/3)^T+(T−1+ell(ell+1))/|S|+eps_native_field_lookup+eps_native_PCS`.
This **does not** presuppose a pre-existing common integer witness commitment, but assumes each native field's small-digit lookup is already sound and h is committed BEFORE seeds. Native ring challenge gamma must have full extension-field entropy; a 49-bit base-prime-only gamma is NOT a justified 128-bit batch combiner (V13). To keep algebraic soundness, all claimed Y_t must be fixed before gamma; otherwise the prover may select claims depending on the combiner.

### One decisive witness-privacy falsifier [FAIL]

A hidden one-hot Boolean digit vector h(b*)=1 and h(b)=0 at all other indices is a legitimate common bounded digit witness. Every PUBLIC honest summary is then **Y_t=w_θt(b*)∈{±1}**, revealing sign codeword at b*. For any other b'≠b*, pairwise independence implies per seed Pr[w(b)=w(b')]=1/2; across independent T219 seeds, and union bound over H−1 alternative indices,
`Pr[any alternative b' matches all 219 PUBLIC signs]≤(H−1)*2^(-219)<2^(-195)`
for H=2^24. The verifier (or observer) can uniquely reconstruct the one-hot location by comparing public masks; no ZK privacy is supplied. This falsifies this *proposed private range proof*, not a promised zero-knowledge property of original paper and not a valid distinguishing attack if other original public statement already reveals that location. A hiding proof of these Y_t would again need a new binding/hiding ZK interface.

## Exact independently reproducible toy [EXPERIMENT]

Standalone Python script enumerates all 128 binary quadratic seed choices for ell3,H8 (7 seed bits), verifies EVERY 4-index marginal is uniform (16 sign patterns each appearing 8 times), and checks the exact second/fourth moments of several integer delta patterns. Zero-sketch counts: one bad index 0/128; two positive indexes 64/128; all eight +1 indexes **70/128**; alternating ±1 indexes 70/128. Crucial: 70/128>1/2, so cannot silently use fully independent-sign 1/2 soundness with quadratic limited-independence weights.

For legal toy source-format N4,d2 primes p53=1+4*13 and p61=1+4*15, beta4,H8, bound24 <p53/2. Honest common vector all3 has identical centered integer summaries under all 128 seeds. For incorrect public summary errors E0=8,E1=4 in F61, exhaust 61² postclaim independent linear-combination weights: exactly61/3721 erroneous batch accepts =1/61. With ONE gamma power combiner E(gamma)=8+4gamma, exact only root gamma=59 mod61, 1/61 acceptance. These are algebraic toy tests of batching, NOT a complete published Brakedown implementation.

For 219 deterministic independently sampled toy seeds, a one-hot hidden location b*=(1,0,1) was reconstructed UNIQUELY among all 8 Boolean indices from honest public ±1 sketch results. Source finite-field PCS not simulated; full-H collision bound is mathematical above.

## Cost and scope [ESTIMATE — NOT empirical performance]

Set N16384,d4,L2,ellstar24,H2^24,beta4, two valid 49bit source-format primes p1=281474976768001,p2=281474976980993, T219. (beta−1)H=50,331,648<pmin/2.
- Honest direct T×H sign-contributions = **3,674,210,304** basic integer summands, *before* seed phase computation, native ring h table layout, and degree-25 sumcheck operations. No universal Ω(T H) lower bound is claimed: batching, FFT/chirp techniques may change costs.
- Public sign seeds =219×301=65,919 bits (~8 KiB).
- One source F.1 ring PCS evaluation opens μ=L N/d=8192 native field factors; original F.2 evaluation exposes m=4096 field elements/factor. Compact d×49 bit extension values require 25bytes each, total **838,860,800 bytes =800MiB** just the F.2 evaluation vectors, before Merkle openings.
- 219 public Y_t canonical q-coefficient encodings, naively each ring element 13bytes×N16384=212,992bytes, total 46,645,248bytes (~44.48 MiB). Honest Y_t may be scalar compressed; this is direct uncompressed format not a lower bound.
- ONE ring sumcheck degree≤25 in each of ell24 rounds sends ≤624 ring coefficients, 132,907,008bytes (~126.75MiB) of naive q-coefficient encoding. One full-ring gamma ~212,992bytes; total naïve non-Merkle payload ~971.44 MiB including native F.2. PCS bandwidth, interactive rounds and privacy remain considerable.
- Without postclaim batching, T219 extra full ring F.2 evaluations would imply 171.09375GiB raw v' vectors, but **this naive multiplication is NOT the best implementation** and is not used in the final cost recommendation.
- Source paper real 2026 revision exact PDF not authenticated; no full compiler, no source code performance benchmark, no deployed 128bit SNARK exploit, no cost-competitive or hiding ZK system.

## End

**STATUS:** PASS conditional no-wrap+4wise sign equality soundness and single-gamma batch sumcheck; FAIL cheap PRIVATE generic common-digit proof via one-hot index leakage, large unoptimized prover/PCS burden; overall HUMAN_REVIEW for value/practicality.
**RESULT:** Without shared integer vector commit, publicly revealed **bounded** signed summaries can genuinely link cross-prime canonical digit vectors, but not with zero knowledge and not for free within F.1/F.2.
**NEXT_ACTION:** Preserve the authoritative V31 separately (its V32 target: real representative native-to-integer CP or PI pivot). If PI wants V32 to explore this companion, test ONE actual knowledge-sound **hiding** equality of CRT integer fingerprints and its amortized cost, or PARK; no more conditional fingerprint probability rounds.
**STATE_UPDATE:** COMPANION ONLY, main V31 remains completed / V32 NOT STARTED, GENERAL I192 FROZEN.

**Local full note:** `/mnt/data/VFHE_V31_Quadratic_Sign_NoWrap_Batched_Companion_2026_10_15.md`, SHA256 `f67a0e62e90aaf03df996d5bce1d984a286effa1cbb078d3f250aa3f911f47b1`.
**Script:** `/mnt/data/vfhe_v31_quadratic_sign_no_wrap_gate.py`, SHA256 `6d2b51c5179f9d9bd7e5b09588980b829a05be5ec4a43c7b3013d31436dfd888`.
**Results:** `/mnt/data/vfhe_v31_quadratic_sign_results.json`, SHA256 `db24ec2a872e048ac9a494dcaaa67496a5968c12142db4ea3c66da574a9e4793`.
