# vFHE Research State — Independent V-Series

**Checkpoint:** 2026-10-14 (Asia/Tokyo)
**LAST COMPLETED vFHE ROUND:** V12. **NEXT:** V13 NOT STARTED.
**STATUS:** V12 FAIL for automatic common-witness inference from one unrelated-prime commitment + independent native CRT proofs. PASS necessary exact canonical-range + commitment-to-each-native-witness LINK relation (conditional binding + knowledge soundness); toy algebra checks. Whole vFHE repair, zero-knowledge joint extraction, 128-bit FS, performance and novelty STILL OPEN.
**GENERAL FHE ITERATION:** FROZEN I192. This is the independent V-series. V1–V4 were formerly called I193–I196 in legacy vFHE archival records only; do NOT advance global I-series.

## Independent vFHE series (compressed)

V1 bounded integer toy; V2 universal row-weight-two one-prefix distance no-go; V3 cyclic-first two-prefix distance no-go; V4 Fp-to-F_(p^d) distance invariance; V5 and V6 low-support cross-prime determinant/rank stability; V7 near-tight five-minor bound; V8 legitimate source CRT prime divides a legal five-minor (not full dmin attack); V9 GLOBAL **bounded digit difference** distance lower bound via binary RAA and integer no-wrap; V10 sampled full-encoded-Merkle integer-range does not deterministically bind all unopened leaves; V11 systematic-only sample misses one differing digit with exact probability 1−t/m; **V12 common commitment DOES NOT independently link native witness digits, and even explicit modulo-group openings need an injective canonical range**.

## Human-selected source target and evidence

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, IACR ePrint 2025/286, https://eprint.iacr.org/2025/286. Source inspected via Research MCP cached 52pp GitHub mirror PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`; latest official revision VERSION_UNVERIFIED. Original §3.1 p10 CRT characteristic and Appendix F.2 pp50–51 native field-linear PCS; source does NOT contain V12's hypothetical third-order common Pedersen commitment.

Parent issue [legacy I59–I60]: componentwise native CRT digit lookup is a rectangular membership relation rather than desired diagonal one-common-integer-digit membership. Source-form CRT idempotent ideal oracle audit suggests gap, NOT authenticated deployed or compiled final-version SNARK exploit. Goal: an actually sound efficient zero-knowledge shared bounded-integer witness extraction and commitment across native CRT fields. Still not constructed.

## V12 — ONE hypothesis and smallest decisive test

**[PRIMARY HYPOTHESIS FALSIFIED]** A common, perfectly/computationally binding hidden commitment over some unrelated prime-order field/group, combined with individually valid native CRT bounded-range/lookup/PCS proofs, automatically implies all CRT witness digits are the SAME bounded integers even WITHOUT knowledge-sound explicit links from native witness variables to the opening of the common commitment.

**[COUNTEREXAMPLE #1]** β9, native legal a_p=1 and a_q=8, same unrelated commitment C to digit1 with order r101>β, both native proofs pass when C is not linked. Binding of C is irrelevant: two separate witnesses never claimed to open it.

**[COUNTEREXAMPLE #2 — MODULAR ALIAS]** If commitment message group has r<β, even proving native witnesses each open SAME C modulo r need not yield integer equality. Let r7, β9, native digits1 and8, same Pedersen-form C=g^1 h^rho=g^8 h^rho in any group of order7. No cryptographic binding break; committed messages are identical MOD 7 but not over Z. The small group arithmetic toy is insecure and NOT an instantiated ZK scheme. At practical r≫β this particular alias is excluded.

**[DERIVED CONDITIONAL SUFFICIENCY]** Need one canonical range D=[0,β−1]^m, an injective binding vector commitment Com_r with β≤r and proof-binding encoding for ALL coordinates, and for each native field i a knowledge-sound link to the SAME C opening, using u_{i,j}=embed_(F_(p_i^d))(a_j) for all digits j, β≤min_i p_i. Extract two distinct linked canonical openings to C ⇒ violation of commitment message binding; thus except knowledge-sound/binding failures all native witnesses coincide. For beta power-of-two, use k=log2 β canonical bits b_{j,k} and a_j=Σ 2^k b_{j,k}, with k bits and a_j<p_i: the native digit-equality constraint needs NO quotient/carry reduction modulo p_i, but explicit cross-field BIT/LINK proof remains mandatory. Different-characteristic fields have no unital ring homomorphism; canonical integers, not free coercion, are the bridge. This is logical proof obligation, not a delivered proof system or cost claim.

**[PRECISE PRIOR ART]** Benarroch et al., *Zero-knowledge proofs for set membership: efficient, succinct, modular*, Designs Codes Cryptography 91 (2023), DOI10.1007/s10623-023-01245-1, §4.2.8 modular-equality proof and §4.3 range constraints / commit-and-prove composition. Existence of modular equality+range CP techniques is KNOWN; not new technical novelty.

**[EXACT TOY CHECK]** Local /mnt/data/vfhe_v12_cross_field_binding_gate.py SHA256 `3f8127d432f737c475a23463dd70a796fd8bd68fc4df11eba26d06c1fbfd4ed7`; JSON /mnt/data/vfhe_v12_cross_field_binding_gate_results.json SHA256 `5e7b0db8e5693dff82f2e2c81dd59d4a7ed5e6f06abca2c8b9822834517268db`. Source-form 49-bit CRT primes p=281474976829441, q=353581838970881; toy β9. No-link case r101: both native distinct witnesses satisfy independent range but no link; modular-alias case r7: both distinct integers open same order7 toy group expression with same blinding. Enumerate all 9 digits to verify r101 canonical integer residues injective (but no computational commitment proof implemented). This is algebraic verification only; any actual Pedersen binding, proof extraction and zero knowledge not tested.

**Detailed V12 source of truth:** `findings/vfhe-cross-crt-consistency-research.md` Section 21; §20 V11, §19 V10. No numbered global findings files.

## MAIN BLOCKERS / NEXT V13 (PI continuation only)

One falsifiable **amortized cross-field linking** mechanism: can many coordinatewise proofs of u_i,j=canonical digit a_j be replaced by a shared postcommit random linear-combination check that binds one hidden digit vector across μ CRT fields with a source-sized concrete soundness error? Research must specify challenge sampling timing, exact characteristic conversion of challenge coefficients, admissible no-wrap/range, ability to extract the canonical committed a, and actual error/performance tradeoff. Until proved, NOT a valid integrated cross-CRT PCS.

Remaining obligations: compatible commitment and knowledge-sound proof implementation; native Brakedown F.2 arbitrary field vectors vs bounded digit; low-entropy witness ZK/hiding; Fiat–Shamir and 128-bit accounting; cost vs original per-field RS commitments; official paper revision authentication. Human PI decides major pivots and novelty.

## Research process

Read `AGENT.md` and `RESEARCH_PHILOSOPHY.md`, one hypothesis / cheapest decisive test, read before write and reread after writes. Global `STATE.md` holds frozen I192 and pointers only; this file is independent V counter; topic file holds all details. No background autonomous runs.
