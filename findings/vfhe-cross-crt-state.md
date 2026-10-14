# vFHE Research State — Independent V-Series

**Checkpoint date:** 2026-10-14 (Asia/Tokyo).
**LAST COMPLETED vFHE ROUND:** **V10**. **NEXT:** V11 NOT STARTED.
**V10 STATUS:** FAIL naive deterministic shared-Merkle-root + sample-only integer range binding. PASS exact two-source-CRT-component lift counterexample, complete Merkle openings, and quantified missed-bad-column probability; CONDITIONAL positive sampling lemma if each native field is already soundly bound/extracted to a bounded digit codeword. **OPEN** actual cross-CRT native PCS binding/extraction, ZK, 128-bit FS/soundness and end-to-end cost. NOVELTY NOT VERIFIED.
**Global general FHE iteration counter FROZEN at I192**. vFHE has its own V-series. Legacy labels I193–I196 in old vFHE archives are V1–V4; do NOT advance the general I-series.

## vFHE research sequence

| Independent V | Result |
|---|---|
| V1 (legacy I193) | Small bounded-integer m8 shared-code toy |
| V2 (legacy I194) | Row-weight-2 single positive-prefix codes: asymptotically vanishing relative distance |
| V3 (legacy I195) | Cyclic first row-weight-2 plus arbitrary second permutation/prefix: similarly vanishing relative distance |
| V4 (legacy I196) | Fixed prime p to extension F_(p^d) distance invariant; weighted nonbinary RAA theorem mismatch |
| V5 | Support≤3 rank/distance invariant across sufficiently large CRT primes |
| V6 | Support≤4 invariant at m≤1024,p>2^48 by monotone parity-minor lemma |
| V7 | Cauchy–Binet five-minor bound nearly tight; upper-49-bit sufficient threshold |
| V8 | Actual legal 49bit prime p_star divides nonzero five-parity minor, gives submatrix rank drop (not global dmin) |
| V9 | All **bounded-digit integer differences** inherit binary RAA global distance over every no-wrap CRT prime; unrestricted native-field PCS distance unproved |
| **V10** | **One shared Merkle root with only sampled integer leaf-range openings DOES NOT deterministically force one global bounded integer witness**; exact CRT-lifted a≠b counterexample, postcommit detection is probabilistic |

## Human-selected parent target / source

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025, IACR ePrint 2025/286 (https://eprint.iacr.org/2025/286). Full 52-page Research-MCP GitHub mirror PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`; official latest parity VERSION_UNVERIFIED. Appendix F.2, physical pp50–51: per-field field-linear matrix commitment / Merkle columns, verifier samples random r and subsequent Q, checking Enc(rU_f)|Q = rUhat_f|Q. No shared-integer Merkle interface is claimed in the original paper.

Original cross-CRT gap from legacy general I59–I60: per-component table membership covers rectangular CRT tuple, not intended diagonal common integer digit. Source-form ideal-oracle CRT idempotent toy exists, but no validated compiled latest-version SNARK exploit.

## V10 — ONE primary hypothesis / decisive minimal test

**Question:** If the proposed repair shares ONE Merkle root of canonical integer CRT lifts, and checks integer leaf range ONLY for Q randomly opened columns, does that alone globally bind all unopened columns to one bounded digit witness while original F.2 per-field linear tests pass?

**[DERIVED/EXPERIMENT FAIL deterministic claim]** True integer unweighted repeat2/two independently seeded permutations/two positive-prefix code, m8,beta2,M24, seed20261014, H=m(2m+1)(beta−1)=136. Two native source-form 49-bit CRT primes p=281474976829441, q=353581838970881, both p mod8192=4097 valid for original ring N8192,d4. Distinct valid Boolean input witnesses a=e6, b=e2 have integer codeword E(a),E(b) differing in EXACTLY 5 positions D={2,6,15,22,23}, found by exhaustive 3^8−1=6560 nonzero digit differences.

CRT lift Y_j in [0,pq) uniquely satisfies Y_j≡E(a)_j(mod p) and Y_j≡E(b)_j(mod q). A single SHA256 Merkle commitment to ALL 24 Y_j has root
`84c67c4c77a932477f449d5faaa838e9ab447707d9be1f6a5bcac94a78553e80`,
with individually verified proofs for ALL 24 leaves; modified leaves fail. Both native component messages and their field-linear combinations are exactly valid at ALL coordinates. Because honest integer codewords lie in [0,H] and H<min(p,q), Y_j∈[0,H] iff E(a)_j=E(b)_j; exactly 5 invalid leaves. Sampled valid leaves reveal no inconsistency.

For postcommit Q drawn uniformly without replacement, |Q|=t, with range checks on opened columns, exact bad-commit acceptance probability:

    Pr[accept] = comb(24−5,t)/comb(24,t).

At t4: 3876/10626=36.4766%, exhaustively verified ALL 10626 subsets. At t8: 75582/735471=10.2767%; t12 ≈1.86335%; t20=0.

**[POSITIVE CONDITIONAL LEMMA, not full PCS proof]** If for each CRT native field a SEPARATE sound mechanism first proves/extracts an EXACT codeword Enc(a_i) for a_i∈[0,beta−1]^m, and Y is fixed before Q, then if two extracted a_i differ, V9 no-wrap and bounded digit distance d0 imply at least d0 out-of-range shared integer leaves. Hence

    Pr[pass] ≤ comb(M−d0,t)/comb(M,t) ≤(1−d0/M)^t,

with source-seed concrete d0 required for target 128-bit accounting. ORIGINAL F.2 has arbitrary native-field random r and q1, so its testing cannot be justified merely from V9's *bounded* digit distance. No non-circular exact native-codeword extractor or shared integer witness extractor has been constructed. This is only a conditional proximity intuition. A range check after revealing Q is ineffective if root not bound before Q.

**Reproducible local-only artifacts:** `/mnt/data/vfhe_v10_shared_merkle_crt_lift_gate.py` SHA256 `fc7de6805b5ad9ff5adecaa02aa02bfa6e7522a06161d0c105d76ff114cea9e7`; results JSON `/mnt/data/vfhe_v10_shared_merkle_crt_lift_gate_results.json` SHA256 `19848a3da4bcba881d6b671f499ab767554c80dab06285768c2244e0413383fa`. Locally created/tested; not Git repository files. Scope: toy proposed repair, not original or deployed vFHE SNARK.

**Full provenance + technical derivation:** `findings/vfhe-cross-crt-consistency-research.md` Section **19** for V10 (previous V9 §18, V8 §17). Do not create new numbered global findings files.

## Main OPEN and NEXT_ACTION — V11 only when PI continues

**Next single falsifier:** can an F.2 native-field codeword commitment plus Merkle authentication of systematic positions NON-CIRCULARLY extract one COMMON bounded integer digit vector across different CRT primes? Test a CRT-idempotent tuple of distinct bounded digit messages that each pass their own exact field-linear encoding and systematic leaves but has NO common bounded integer lift. If no global link, KILL the naive fieldwise extraction→shared-witness implication and identify what *one new proof mechanism* must provide. Don't conflate sampled detection probability with a complete FS/PCS security proof.

**Missing:** full native field-codeword extraction/knowledge soundness; Merkle binding of hidden unopened leaves; integer range/diagonal consistency; hiding/ZK of low-entropy digit leaves; Fiat–Shamir + 128-bit errors; performance and novelty.

## Repository boundary

Global `STATE.md` is a pointer and freezes I192; this file holds independent vFHE progress; detailed verified results go into `findings/vfhe-cross-crt-consistency-research.md`. Research follows AGENT.md read-before-write and 1 primary hypothesis/1 decisive test; human PI controls strategic pivots, author disclosure and final contribution judgment.
