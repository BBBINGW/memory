# Iteration 65 — Naive cross-characteristic Reed–Solomon codeword reductions are not compatible

Date: 2026-10-10
Active target: Cascudo, Costache, Cozzo, Fiore, Guimarães, Soria-Vazquez, *Verifiable Computation for Approximate Homomorphic Encryption Schemes* (CRYPTO 2025), IACR ePrint 2025/286, §4.3–5.
STATUS: **FAIL** for the specific coded bridge: "commit once to a shared integer digit vector as a Reed–Solomon codeword over one external finite prime field F_P; then take the canonical integer representatives of the codeword symbols mod each distinct CKKS CRT prime p_i and use those as the field-specific RS codewords." This is algebraically INCORRECT even for honest all-Boolean messages. No new efficient repair; general cross-characteristic consistency question OPEN.
Novelty: familiar characteristic/integer-lifting obstruction and field-specific RS encoding, not a new cryptographic theorem.

## Read-before-write / protocol
Before defining the hypothesis, read AGENT.md, RESEARCH_PHILOSOPHY.md, separate parked RIG-HE STATE.md, I64 `failures/vfhe-shared-integer-raw-spotcheck-not-succinct.md` and I63 `findings/vfhe-crt-diagonal-lookup-local-algebraic-no-go.md`.
One primary hypothesis, one minimal exact counterexample. This is a repair candidate for the earlier I59–I61 CRT-diagonal scalar lookup soundness counterexample; no author contact authorized or performed. STATE.md remains untouched.

## Primary paper evidence and prior art
[FACT] In 52-physical-page full-paper mirror ePrint 2025/286, PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, VERSION_UNVERIFIED, §4.3 pp.20–24 defines scalar digit table t_beta={0,...,beta−1} and range witness h with m=2^ell*N*c entries, and verifier has 25 ring-oracle queries and O(log m+log beta) PIOP verification. §5 pp.25–26 constructs a Ring-R_q polynomial commitment as a vector of independently committed F_(p_i^d) projections; suggests Brakedown/RS encodings in those individual finite fields and reports 1020 RS-coded column openings as one DISTINCT setting. The present bridge is OUR hypothetical change, not claimed in the paper.
[GENERIC SOURCE] Vitalik Buterin, *Binius: highly efficient proofs over binary fields* (2024), https://vitalik.eth.limo/general/2024/04/29/binius.html explicitly explains that integer Reed–Solomon extensions can blow up, motivating finite-field evaluation. This is general background, not provenance for our exact witness.
[COMPARATIVE SOURCE] Guo et al., *DeepFold*, USENIX Security 2025 https://www.usenix.org/conference/usenixsecurity25/presentation/guo-yanpei uses RS-code PCS within its native finite-field setting, not a verification of cross-prime reduction compatibility.

## One primary hypothesis and cheapest falsification
[HYPOTHESIS — FAIL] For a common Boolean coefficient message z∈{0,1}^m and coefficient-form RS code E_P(z) over external prime field F_P, with P distinct from each CRT p_i, the canonical representative-wise map `red_p(E_P(z))` equals `E_p(z)` for each i (same integer evaluation nodes), so a shared external codeword can be sampled to check each component's RS codeword without nonnative range/carry proofs.
[FALSIFIER] ONE honest Boolean message, ONE RS evaluation node, and distinct target primes for which `(Σ z_j a^j mod P) mod p_i ≠ Σ (z_j mod p_i) a^j mod p_i`.
[CHEAPEST TEST] Exact integer evaluation and modular reductions, no SNARK circuit construction or parameter sweep.

## Exact honest correctness counterexample
Choose a 3-symbol coefficient-form Reed–Solomon message z=(1,1,1), f(T)=1+T+T², evaluation node a=7 (one point of a valid RS evaluation set). External P=41 and CRT primes p0=29,p1=37. All primes are different and P>max(p_i).
Raw f(7)=57; external codeword symbol =57 mod41=16. Naive reductions yield (16 mod29,16 mod37)=(16,16).
But separate genuine field evaluations of SAME legal Boolean message give (f(7) mod29,f(7) mod37)=(28,20).
Hence `red_(29,37)(E_41(z))=(16,16) ≠ (28,20)=(E_29(z),E_37(z))`. This is an honest false reject; not a soundness attack or malicious cross-CRT idempotent instance. A bridge using this equality violates perfect completeness.
[EXACT GENERAL CAUSE] Writing t=Σ_j z_j a^j as an integer and t= c_P + kP with c_P∈[0,P), then under p_i the external lifted symbol gives c_P mod p_i while the honest native field symbol is (c_P+kP) mod p_i. They coincide iff p_i divides kP, and since distinct prime p_i≠P, iff p_i divides k. Usually k=1 or arbitrary nonzero, so not preserved.
[CHARACTERISTIC ARGUMENT] There cannot be a unital ring homomorphism F_P→F_(p_i^d) for different prime characteristics: 0=P·1 in domain would map to P·1≠0 in target. Ordinary canonical integer-representative reduction is not a ring homomorphism.
[REPAIR SCOPE] This does NOT preclude integer-first code symbols `c_Z=Σ z_j a^j` followed by reduction to each p_i; the exact integer-lift identity `c_Z mod p_i=E_(p_i)(z)` is true. But then the external commitment has to bind to **the full integer c_Z and its carry k**, not merely to c_P, and verify an integer relation that is not simply a native RS codeword in F_P. Absent bounded carry/limb constraints, p_i-field witnesses could separately choose k_i and recreate the CRT-locality attack. No sound, efficient integer-first encoding protocol supplied.

## Minimal cost boundary, no universal impossibility
For the coefficient-form integer RS evaluation at a=2 and m Boolean message coefficients, all ones yield `Σ_(j=0..m−1) 2^j=2^m−1`, requiring exactly m bits. Taking example m=2^15=32768 as already used for N=2^14,c=1,ell=1, an external PRIME field of characteristic P>2^32768−1 to suppress this integer wrap at node 2 would require modulus at least 32769 bits. This is a dramatic cost for THIS coefficient evaluation layout and node; NOT a lower bound for other error-correcting codes, other RS evaluation layouts, sparse generator matrices, bounded integer codes, or proof systems with efficient limbs/quotient arguments.
RS encoding can use other points/structures but must handle actual inter-prime integer lifts; external P's being larger than individual p_i does not guarantee commutation.
[PRIOR PROTOCOL COMPARISON] Original paper's encoded commitments are per finite extension field (e.g., 49-bit primes with d=2/4). The speculative external F_P+reduction bridge adds a different characteristic and needs a nonnative relation, so original Brakedown correctness/soundness do not automatically transfer. The exact protocol overhead is NOT measured.

## Reproducibility
[EXACT SCRIPT] `/mnt/data/iteration65_vfhe_cross_characteristic_rs_commutation.py` SHA256 `6a6dd871ca070ab5a7238ee647bed51e75586b3f437bff1b151e0cacd13fac5f`.
[EXACT OUTPUT] `/mnt/data/iteration65_vfhe_cross_characteristic_rs_results.txt` SHA256 `e704e172e50f057051fe785a4cef1dfa850444bc2e7c83bfc6c648396e677322`.
Exact Python asserts difference for both primes and checks integer-first equality; computes m=32768 all-ones output bit length without constructing arbitrary brute-force lookup instances. Ran successfully in current container. This is a tiny proof-level arithmetic witness, not FHE benchmark or zero-knowledge implementation.

## Research judgment
[FAIL] Attempting to repair the original diagonal-digit soundness issue by reusing a single RS commitment over F_P, directly reducing its canonical finite-field symbols to each unrelated p_i, fails even for honest valid digits. Such a codec is *not* a drop-in, zero-overhead bridge.
[OPEN] Correct candidate must either commit to externally anchored **bounded integer/limb** code symbols and prove encoding + modular reductions, or use a genuinely cross-characteristic proof system that establishes this relation. Neither mechanism is shown cheaper than rebuilding a nonnative range proof; code distance alone supplies no cross-field message binding. Do not claim a lower bound on every coded bridge.
[STRATEGY / STAGNATION] Iterations 63–65 have now rejected three adjacent obvious repair directions: pure R-algebraic Frobenius/trace (I63), uncoded spot-checking (I64), and naive external RS reduction (I65). All are simple mathematical observations; another minor variant would likely be low-value. HUMAN_REVIEW is recommended on whether to proceed to a substantial cross-characteristic coding/SNARK construction or first obtain verified latest PDF and confidential author feedback (requires PI authorization). Avoid another toy variant.
[OFFICIAL REVISION LIMIT] Latest official revised 2026-02-16 PDF byte identity remains UNVERIFIED; the mathematical problem is supported for examined 52-page revised-looking mirror, not an authenticated latest official version. No full deployed exploit and no confidential email has been sent.

## End of iteration 65
STATUS: FAIL for the naive external-field RS codeword reduction bridge.
RESULT: One honest Boolean message f=1+T+T² at T=7 yields external F41 codeword16 which reduces to (16,16) but true CRT field evaluations are (28,20); exact incompatibility is due to field characteristic and reduction order. Using integers without wrap restores algebraic compatibility but incurs large integer/carry proof cost for ordinary coefficient-form RS.
NEXT_ACTION: HUMAN_REVIEW — the PI must decide whether to invest in a genuinely nonnative cross-characteristic integer codeword consistency protocol with explicit security/cost proof, or stop repair design until the authoritative current 2026-02-16 PDF and authors' confidential technical position have been verified. No contact absent explicit authorization; do not run further adjacent trivial examples.
STATE_UPDATE: NO — parked RIG-HE STATE.md unchanged.
