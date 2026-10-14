# vFHE Research State — Independent V-Series

**Checkpoint:** 2026-10-14 (Asia/Tokyo)
**LAST COMPLETED vFHE ROUND: V9. V10 NOT STARTED.**
**STATUS:** PASS globally quantified **BOUNDED-DIGIT-pair distance** across ALL no-wrap CRT primes, conditional on classical binary random-two-interleaver RAA good-distance event. Not a proof of unrestricted Fp-field code distance or the original F.2 polynomial-commitment security. Parent vFHE cross-CRT binding and zero knowledge remain OPEN / HUMAN_REVIEW; novelty NOT VERIFIED.
**Global general FHE counter FROZEN at I192.** Independent vFHE V-series: V1–V4 were accidentally called I193–I196 in older notes; preserve legacy paths, never advance global I-series for vFHE.

## Independent rounds

| Round | Core verified outcome |
|---|---|
| V1 (legacy I193) | Common bounded-integer m8 toy code nonzero distance only |
| V2 (legacy I194) | All degree-2 single-prefix encoders have O(sqrt m) distance upper bound |
| V3 (legacy I195) | Cyclic first stage plus any one more perm/prefix similarly fails constant distance |
| V4 (legacy I196) | Fp→F_(p^d) distance invariance for same prime-base code; weighted nonbinary RAA literature model mismatch |
| V5 | All source-compatible p>384m³ preserve input-support≤3 rank/distance |
| V6 | For m≤1024,p>2^48 preserve support≤4 distance via monotone parity-minor bound |
| V7 | Cauchy–Binet bound preserves support≤5 only above p>368933561632000 for m1024, near-tight example |
| V8 | Legal 49-bit p_star=353581838970881 equals an actual five-parity minor determinant; rank_Q5 vs rank_Fp4 (large-coefficient witness, NOT min distance/attack) |
| **V9** | **GLOBAL support bound for ALL admissible small integer digit pairs**, across EVERY p>m(2m+1)(beta−1), by non-wrap + primitive-integer mod2 transfer + known binary RAA distance theorem |

## Parent evidence

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025, ePrint2025/286, https://eprint.iacr.org/2025/286. 52-page GitHub-mirror primary PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, latest official equality VERSION_UNVERIFIED. §3.1 native CRT components F_(p_i^d), §6 uses 49-bit primes, Appendix F.2 physical pp50–51 Brakedown field-linear testing/evaluation.

Original structural gap [legacy I59–I60]: CRT-field componentwise digit table membership permits rectangular non-diagonal index vectors. Source-form idempotent ideal-PIOP counterexample under inspected mirror PDF, NOT authenticated current final compiled SNARK exploitation. Goal is one common, hidden bounded INTEGER digit witness across CRT primes, with a fully sound efficient shared-codeword commitment; NOT yet achieved.

## V9 — ONE hypothesis and decisive test

**HYPOTHESIS [PASS within BOUNDED digit domain]:** For fixed public integer RAA G=[I_m|P] with repeat2, TWO free interleavers and TWO positive prefix accumulators, there is a field-independent **global** positive constant relative distance among any pair of honest bounded digit messages, even if the FULL Fp code admits V8's prime-specific rank change, provided p_i satisfies a quantified no-wrap bound.

**Exact derived lemmas:**

(1) For each parity output coordinate j, column sum of the m×2m parity generator P is at most `B(m)=m(2m+1)` (achieves equality at final output), since across all unit-input messages, the first prefix gives the list 1,…,2m and the second prefix accumulates a permuted list of these. All P_ij≥0. For a,b∈[0,beta−1]^m and x=a−b, each coordinate of integer xG has magnitude≤B(m)(beta−1). Thus for ANY CRT p_i>B(m)(beta−1), reducing the common integer codeword modulo p_i (and its extension) preserves its EXACT full zero/nonzero support. This is for bounded digit DIFFERENCES, not generic native field vectors.

(2) For nonzero x∈Z^m, divide by gcd of entries to obtain primitive x' with at least one odd coordinate. Let u=x' mod2, a nonzero F2 vector. Since generator entries integral and code is systematic, any integer zero coordinate remains zero modulo2, so `wt_Z(xG)=wt_Z(x'G)≥wt_F2(u(G mod2))≥dmin(binary systematic RAA)`.

Combine:
`wt_(F_(pi^d))(E(a)−E(b))=wt_Z(E_Z(a−b))≥dmin(C_F2)`
for ALL a≠b bounded and ALL CRT prime factors obeying no-wrap, simultaneously. If independent random interleavers satisfy the known binary RAA asymptotic good-distance theorem, this restricted distance is Ω(m) over EVERY such prime. It is **not** the unrestricted Fp-linear dmin guarantee needed for a naive native-field PCS replacement.

**Primary prior art:** Guruswami & Machmouchi, *Explicit Interleavers for a Repeat Accumulate Accumulate (RAA) Code Construction*, ISIT 2008, DOI10.1109/ISIT.2008.4595333, Definition1 / Theorem1 quoting Bazzi–Mahdian–Spielman: binary repeat k≥2 with TWO uniformly random independent interleavers has dmin≥epsilon m with probability≥1−delta for large enough m. Applies to BINARY parity-only encoder, and appending external systematic x cannot decrease distance. Does NOT mean their distinct inner-systematic variant is our architecture. The result is an asymptotic ensemble guarantee, not a finite 128bit claim.

**Source-scale illustration:** m1024, beta=2^20 implies `B(m)(beta−1)=1024·2049·1048575=2200094899200 (<2^42<2^48)`. Every benchmark-style 49bit CRT prime p>2^48 satisfies for this HYPOTHETICAL code size and lookup digit range; do not identify code m with source ring N without argument. A fixed 49bit prime cannot sustain no-wrap as m→∞ with fixed beta; primes must grow as m² beta.

**Exact experiment PASS:** 3 independent seeded permutation pairs (seeds2,11,2026), m6,beta3, no-wrap threshold156, all 3×(5^6−1)=**46872 nonzero bounded digit differences** exhaustively checked. Compare integer support vs p257,p263 and 49bit source-form primes281474976829441 and353581838970881. All identical; every primitive integer input mod2 has wt≤ integer output, and binary minimum distances are seedwise [4,3,3] vs bounded-digit min [4,8,5]. Script `/mnt/data/vfhe_v9_bounded_digit_global_distance.py` SHA256 `47a53d738e23f0cfa13733e9b5faed6dcf09c7b79c5beae8122a315ac3d76936`; JSON `/mnt/data/vfhe_v9_bounded_digit_global_distance_results.json` SHA256 `2fc1fd4a19aa9126890a8e0309d0fe761f89393ad50a2fb95441f521b8dc4758`. Both local-only and rerun with identical hashes.

**KEY F.2 SOUNDNESS BLOCKER:** Original Appendix F.2 proof verifier samples arbitrary `r∈F^m` and checks `Enc(r·U_f)|Q=r·Uhat_f[:,Q]`, then for evaluation uses arbitrary native field `q1·U_f`. These are NOT legal bounded-digit differences. Thus V9's restricted distance cannot by itself justify proximity/knowledge soundness if we simply swap RS Enc to integer RAA within the original field-native Brakedown PCS. Need a NEW shared-canonical-bounded-integer commitment/extractor that first binds ALL underlying integer rows to bounded digits, otherwise using the restricted lemma is circular. Also unopened leaf range/hiding and FS remain open.

**Detailed proof/source/experiment:** `findings/vfhe-cross-crt-consistency-research.md` Section **18** (V9); legacy §17 V8, §16 V7.

## NEXT_ACTION — V10 only on PI continuation

One smallest non-circular **shared integer Merkle commitment/range binding** test, target a malicious prover who commits to apparently bounded *opened* columns but CRT-lifts inconsistent **unopened** field columns. Does checking integer leaf representation (e.g. 48bit) + current F.2 query consistency actually force the SAME bounded digit vector, or can a dishonest precommitted word evade until sampling? Specify sample order, exact success probability and zero-knowledge risks; KILL naive construction if it fails. No generic PCS build until this gate.

## Archive protocol

Global `STATE.md` remains I192 and only points here. This standalone state is sole V-series round counter. Update `findings/vfhe-cross-crt-consistency-research.md` with scientific proof/evidence. Human PI controls pivots, author contact and contribution claims; follow AGENT.md one falsifiable hypothesis/cheapest test, read before write and reread after write.
