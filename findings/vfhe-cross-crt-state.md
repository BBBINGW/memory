# vFHE Research State — Independent V-Series

**Checkpoint:** 2026-10-14 (Asia/Tokyo)
**LAST COMPLETED vFHE ROUND: V8. V9 NOT STARTED.**
**Status:** V8 PASS exact *legal source-form 49-bit CRT prime* causing one rank-changing 5×5 parity minor for the integer double-accumulator code. This refutes FULL 5-minor rank invariance across all allowed CRT primes, **NOT** global code distance, bounded-digit safety, or vFHE SNARK soundness. Parent target OPEN/HUMAN_REVIEW, NOVELTY NOT VERIFIED.
**Global FHE research counter remains frozen at I192**. This independent vFHE V-series does not increment or overwrite the original FHE I-series.

## Numbering / historical map

V1 (legacy I193): bounded-integer shared codeword m8 toy; V2 (legacy I194): any binary row-weight-2 single prefix has vanishing relative distance; V3 (legacy I195): cyclic first expansion plus any second prefix/perm similarly fails; V4 (legacy I196): same-prime extension-field minimum distance invariance, weighted RAA proof mismatch; V5: supports≤3 cross-prime minor preservation; V6: supports≤4 cross-prime minor preservation at m≤1024,p>2^48; V7: sharper five-minor Cauchy–Binet sufficient threshold; **V8: actual allowable prime-divisible five-minor with rank change**. Legacy filenames retained as evidence and not renumbered.

## Parent task and original evidence

Paper: Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint 2025/286, https://eprint.iacr.org/2025/286; 52-physical-page research-MCP mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, exact official revision VERSION_UNVERIFIED. §3.1 physical p10 defines CRT primes p=1+2aN/d, odd a; §6 pp27–29 uses 49-bit native RNS primes. Old source-form ideal PIOP CRT-idempotent counterexample shows **rectangular vs diagonal digit-table membership** discrepancy; NOT an authenticated deployed compiled-SNARK exploit.

Objective: a **one-common-bounded-integer-digit cross-CRT binding/hiding verification** integrated with native field PCS, correct soundness/ZK/Fiat–Shamir and useful performance. Still no full repair.

## V8 — ONE decisive test, exact verified outcome

**Question:** Is the V7 lower-49-bit uncovered five-minor rank region only an artifact of sufficient size bounds, or does any actually permissible CRT prime DIVIDE a nonzero minor from a legal true two-permutation unweighted repeat2 double-positive-prefix integer generator?

**[DERIVED+EXACT, PASS non-invariance]** Set code message m1024, accumulators n2048, source ring N8192,d4. A legal five-selected-input first interleaver has stage-block lengths L=[357,400,421,373,497]. Each first-stage block contains a unit odd transition from first copy of selected row and L_i−1 prefix-plateau positions; 2038 nonselected repeat labels fill remainder. Second permutation is a separate **legal but deliberately tuned** permutation, grouping each plateau into block j, and routing odd transition i to block σ(i) for σ=[4,1,0,2,3]. Sample second-prefix parity columns J=[356,756,1177,1550,2047], selected message rows S=[0,1,2,3,4]. Exact 5×5 parity minor:

    M=
    [[714,1514,2356,3102,4095],
     [2,801,1643,2389,3381],
     [1,1,843,1589,2581],
     [0,0,1,747,1739],
     [0,0,0,1,993]].

Two independent exact determinant methods find

    det(M)=p_star=353581838970881,
    p_star=1+4096·86323691155, 86323691155 odd,
    2^48<p_star<2^49, isprime(p_star)=True,
    p_star mod8192=4097.

Thus rank_Q(M)=5, rank_Fp_star(M)=4; at other source-form 49-bit prime p_other=281474976829441, rank_Fp_other(M)=5. M was independently regenerated from complete length-2048 permutations and two prefix arrays (not an invented matrix). The full G=[I_m|P] remains full rank over each field.

Explicit mod-p_star LEFT null coefficient vector on S:

    x=(248360433806974,147393490404705,227528283364297,265412092786493,1).

Its five selected parity entries are zero mod p_star but NONZERO as integers. On the entire codeword of length3m3072 from the SAME lifted integer x: weight over Q2053; over p_star2048; over p_other2053. These codewords have LARGE weight, and the null coefficients are NOT admissible {0,1} or β=2^20 bounded digit differences. **No actual min-distance drop, no bounded digit attack, no vFHE exploit demonstrated.**

[REPRODUCTION] Targeted deterministic seed1826 search explored 165987 structured length/permutation candidate proposals, of which 35 determinants were source-congruent 49-bit numbers before finding this prime. This is a SELECTED witness; π1/π2 are *not* independently drawn random samples, even though every generated permutation is individually legal. No ensemble probability/typical security claim. Script `/mnt/data/vfhe_v8_prime_divisible_minor.py` SHA256 `7ef42c152a386db4cafa5a526f1c047f17eb69e7d4ed928d75993cb983a85355`; results `/mnt/data/vfhe_v8_prime_divisible_minor_results.json` SHA256 `6d66f63e957a1686af7376d8f18f0f87a50ea63abd948b2b1016efb0d65492c4`. Reran twice with identical hashes. LOCAL artifacts, not present in Git.

**Interpretation:** V6 all-support≤4 preservation for m1024,p>2^48 still holds; V8 demonstrates V7's high-49-bit sufficient threshold is meaningful: below it there can be real rank-changing five-minors. But rank preservation of EVERY SMALL submatrix is **NOT necessary** for a constant relative minimum distance. Cannot kill integer shared-code architecture on this basis.

## Current priority and NEXT_ACTION (V9 only if PI continues)

**STOP narrow t=5/6/7 prime divisibility search.** One globally decisive hypothesis: for true unweighted, independently sampled/explicitly defined two-interleaver repeat2 double-positive-prefix integer code, can we prove or falsify positive constant **unrestricted** Hamming relative distance on large native prime fields? Examine actual matching random-ensemble vs deterministic structure (and no-wrap), rather than import weighted nonbinary RAA theorem with different hypotheses. Start with a cheapest single global obstruction or a proof lemma, not an implementation. If mathematically UNCLEAR, recommend PI HUMAN_REVIEW to redirect toward direct cross-CRT PCS binding/extraction design instead of coding micro-lemmas.

The overall shared integer column commitment's binding/proximity, digit privacy/ZK, Fiat–Shamir security, 128-bit failure bound and true end-to-end cost remain unresolved.

## Source of truth

Full technical narrative including exact legal permutation construction and caveats: `findings/vfhe-cross-crt-consistency-research.md` Section **17** (V8); previous V7 §16, V6 §15, V5 §14. General `STATE.md` points here and keeps I192 frozen. AGENT.md: read-before-write, one hypothesis+decisive test, report PASS/FAIL/UNCLEAR, precise provenance, verify after writing. PI retains all research pivots/contribution/disclosure decisions.
