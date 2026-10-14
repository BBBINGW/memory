# PVFHE-P04 — ONE inversion on canonical reconstructed y forces every bit scalar, but needs non-Ring-R1CS proof

**Date:** 2026-10-14 Asia/Tokyo. **Independent PVFHE-P04 COMPLETED, P05 NOT STARTED.**
**STATUS:** **PASS exact algebraic repair for the source's two-CRT-field parameters**; **UNCLEAR** whether the added Galois relation can be efficiently, soundly integrated into the original Ring-SNARG/PCS. NO compiled SNARG forgery or repaired IND-SA theorem.

## Read before write, source provenance, isolation

Read START_RESEARCH_SESSION.md SHA 6235e9d376a8b143719a40178132f02a6a41d4f3, RESEARCH_PHILOSOPHY.md SHA 49da3f7fa3e75f5025258cf525482ce4a7ab6867, AGENT.md SHA b3e73b2c7f852c05aa674dd97b632e9f99ac5f22, separate global STATE.md SHA 9aefdece0df0a4c1de22d10a31908e68abf31eca (parallel vFHE V23), P03 findings/pvfhe-P03-ring-r1cs-scalar-bit-canonical-repair-gate.md SHA e0d6bd682b1dea5f1a9b15a5276a2220bf57261b, P02 SHA 9b09262066c61778ce581abbba4dbd5098ee5483. P04 did not exist. NO changes to vFHE/SHIP/other state, P01–P03, or backlog.

Original Huang–Li–Mao–Zhang, *Fully Homomorphic Encryption with Efficient Public Verification*, IACR ePrint 2024/1764 https://eprint.iacr.org/2024/1764.pdf. Read full Research MCP 29pp GitHub mirror PDF SHA256 7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089 (VERSION_UNVERIFIED), esp. physical pp15–17 bit decomposition, Ring-R1CS and Theorem4.12; physical p26 Appendix B concrete Q,N; p27 Appendix C.3 intended proof. Web independently opened public original PDF and citations support source identity; attempts to visually screenshot p15/p16/p26 failed cache miss. Source extraction shows math glyph warnings. Official version/erratum parity remains unverified.

## ONE primary falsifiable hypothesis and ONE minimum decisive test

**[HYPOTHESIS P04]** For source actual prime Q=2^53+5, N=2048, an *unanchored* reconstructed BitDecomp y=sum(j=0..53)2^j*x_j is a **unique canonical integer encoding in scalar bits** if: (i) every x_j^2=x_j; (ii) source-specific canonical range predicates h*H=0 and h*x_2*(x_0+x_1-x_0*x_1)=0 (h=x_53; H=sum(j=3..52)2^j*x_j); and (iii) ONE extra Galois-inversion equality **sigma_{-1}(y)=y**. (Not 54 separate inversion checks on the bit variables.) Distinguish mathematical correctness from availability of a sound native Ring-R1CS constraint for sigma.

**[DECISIVE FALSIFIER]** Verify Q prime, actual number and sizes of irreducible CRT factors for X^N+1, whether sigma_{-1} swaps all components and fixes scalar coefficients, and whether the 3 predicates admit ANY non-scalar idempotent-bit assignment. Test exact source idempotents and exhaustive small analogous ring all 4^6 assignments. If inversion fixes a nontrivial idempotent, or canonical distinct component bit strings can have same reconstructed y, FAIL.

## Exact source-shaped theorem [DERIVATION, PASS]

Q=9007199254740997 is prime and Q ≡ 5 (mod4096). ord_{4096}(Q)=1024. Phi_{4096}(X)=X^2048+1 has exactly phi(4096)/1024=2 irreducible factors of degree 1024. Thus R_Q = F_Q[X]/(X^2048+1) is isomorphic to F_{Q^1024} × F_{Q^1024}. All idempotents are componentwise pairs (0,0),(1,1),(1,0),(0,1). The inverse polynomial automorphism sigma_{-1}(f)=f(X^-1) swaps the two field factors: -1 (3 mod4) does not lie in subgroup <Q> (all 1 mod4), so reciprocal roots belong to opposite Frobenius orbits.

Every x_j²=x_j hence gives b_{j,+},b_{j,-} ∈{0,1}. The P03 canonicality equations act separately in the two field factors, where they are correct for literal Boolean bits: in each factor the integer sum S_± lies in [0,Q-1] and y's component is S_± embedded as a BASE-FIELD value. Sigma_{-1}(y)=y swaps the two components with an F_Q-fixing field isomorphism, so S_+=S_- modQ. Since both are canonical representatives, equality holds AS INTEGERS, so their binary expansions are identical. Hence for every j: b_{j,+}=b_{j,-}; x_j is scalar 0 or1. Conversely genuine canonical scalar bits satisfy all 3 predicates. This is a full semantic IFF in this parameterized extended circuit.

**ONE inversion on reconstructed y suffices.** Neither canonical comparator alone (P03 failure) nor inversion on y alone (different integer representatives a and a+Q per component) suffices. Testing sigma on each x_j separately is unnecessary.

## Actually executed mathematical gate

- Runnable exact Python: /mnt/data/pvfhe_p04_inversion_scalar_bit_gate.py, SHA256 e39129721da8b352426a1e5a34fa6fd4a89bfd936d3bdfead490a4b5c58c37ea.
- JSON /mnt/data/pvfhe_p04_inversion_scalar_bit_results.json, SHA256 bac0dfa45ca817e1b4b070ba5fd2e5f4a1d3aace7cdc3f67841a1f5ce905c76e.
- Detailed user Markdown /mnt/data/PVFHE_P04_Galois_Inversion_Scalar_Bit_Repair.md, SHA256 e88d7d8d4a1038ea38f2e9838a8941bcbc1ec0aea1c2254cfb178e110217066b.

Source: exact primality and multiplicative order verified; verified all four possible source idempotents as 0,1,e,1-e (e from P01 with e=(1+i*X^1024)/2 and i²=-1) are indeed idempotent; sigma_{-1}(e)=1-e, so exactly 0,1 pass. Built-in dense but sparse-optimized negacyclic multiplication over source N2048; not a simulated FHE proof.

Toy F37[X]/(X^4+1) (also 2 irreducible factors), six bit variables each any of four idempotents: exhaust all 4^6=4096 assignments. Canonical comparator passes 1369. Requiring ONE inversion equality on y leaves exactly 37, every one has all scalar bits, **ZERO false accepts**; previous 1332 non-scalar reconstructions eliminated. The toy merely illustrates proof; no attempted exhaustive test 4^54 on huge R_Q.

## Hard cost / proof integration boundary

Computing sigma_{-1} on coefficients is a signed index-reversal: if a(X)=a_0+sum_{j=1}^{N-1}a_j X^j then sigma(a)=a_0-sum_{j=1}^{N-1}a_j X^{N-j}. This is O(N) field operations/data movement. Equality sigma(y)=y is equivalent to y_{N/2}=0 and y_j=-y_{N-j} for j1..N/2−1: **N/2=1024 linearly independent F_Q coefficient equations per decomposed reconstructed value**, versus 54×1024=55,296 if each bit separately constrained. Algebraically this adds ONE non-R-native automorphism predicate per BitDecomp plus P03 cheap canonical comparator.

**CRUCIAL BLOCKER:** Source Lemma4.4 / Theorem4.12 accepts only native R-polynomial +,* equations. sigma_{-1} is a cross-CRT-field permutation, NOT representable by adding more such equations on a free witness (P03 idempotent-gluing no-go). Setting u as a maliciously chosen “sigma(y)” hint and using a normal equality u=y without proving its automorphism relation is INVALID. The published Ring-SNARG and polynomial commitments do not automatically attest to coefficient permutation. A coefficientwise field R1CS fallback needs O(N) scalar linear checks per BitDecomp and O(N²) across N decompositions at one KeySwitch, which may destroy the target ring-native advantage; that is a cost *envelope*, NOT a compiled runtime nor generic lower bound for enriched proofs. A native automorphism-aware PCS/proof with soundness and realistic total work is still MISSING. No claim of efficient full repair, secure proof transcript, end-to-end correctness, attack probability, or novelty against prior art.

## End of iteration

**STATUS:** PASS conditional theorem for canonical+idempotence+one inversion per full decomposition; **HUMAN_REVIEW/UNCLEAR** source-compatible proof-system enforcement/cost, actual security, novelty.
**RESULT:** Narrow gap repair mathematically feasible using ONE cross-component operation per reconstructed y at exact source parameters; unavailable as an ordinary Ring-R1CS add/mul equality. Scope is an extended relation, not authors' published construction.
**NEXT_ACTION (PVFHE-P05 ONLY on PI continuation):** ONE minimum commitment-level verification gate: can source ring PCS / sum-check enforce `sigma_{-1}(y)=y` with subquadratic prover work per KeySwitch and a sound argument, or is coefficientwise field proof the unavoidable practical route? Require source algorithm/lemma evidence and quantified overhead; if none, PARK as an algebraic repair rather than claim publication novelty. No author contact/erratum allegation without PI direction.
**STATE_UPDATE:** YES standalone P04 ONLY; NO modifications to shared global/SHIP/vFHE state or previous findings.
