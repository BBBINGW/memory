# PURE-FHE · P0-PRESCOUT-12 — Restricted Slot Subalgebra / Rotation Closure Gate

- Date: 2026-10-26 (Asia/Hong_Kong)
- TRACK_ID: PURE-FHE
- Previous: P0-PRESCOUT-11, generic nonlinear-intertwining failed
- Primary hypothesis H12: a nontrivial high-capacity complex-linear CKKS slot subspace W ≤ C^n closed under slotwise multiplication and *all* cyclic slot rotations enables a genuinely new low-cost representation conversion.
- STATUS: FAIL_HIGH_CAPACITY_STRUCTURAL_NOVELTY; PASS_ALGEBRAIC_CLASSIFICATION; NATIVE_NOT_RUN.
- NOVELTY: NOT_ESTABLISHED. This is a mathematical filtering result, not a new cryptographic construction.

## [DERIVATION] Classification

For a complex-linear W≤C^n with x∘y∈W for all x,y∈W, coordinate evaluation maps φ_i:W→C are either zero or partition into equal nonzero linear functionals. Choose v∈W with distinct nonzero φ_i(v) on distinct equivalence classes. Since W is an algebra, polynomials p(v) with p(0)=0 lie in W. Lagrange interpolation constructs each class indicator χ_B∈W. Consequently W is exactly the span of mutually disjoint 0/1 indicators, i.e. vectors constant on each block and zero off the union. In particular dim(W)=number of blocks.

If W≠0 and invariant under the unit cyclic rotation on n coordinates, the support is all coordinates; shift-invariant equivalence classes are cosets of a subgroup H≤Z_n. Therefore W consists of sequences of period d=[Z_n:H], where d|n. For any proper W, d≤n/2. A proper, fully rotation-invariant, multiplication-closed complex-linear subspace necessarily loses at least 50% independent slot capacity.

Example n=8: W={(a,b,a,b,a,b,a,b)} with dimension 2; closed under slotwise product and all rotations. A length-8 ordinary DFT has support only at k=0,4, with values 4(a+b), 4(a-b). Toy DFT is not the full CKKS canonical embedding.

## [DERIVATION] Lift caveat, avoid overstated impossibility

Toy coefficient model: q=16, m=(1,2,1,2) lies in a period-2 subspace; arbitrary lift J=(1,0,0,0) gives t=m+qJ=(17,2,1,2), which is not periodic. Averaging each repeated coordinate pair produces (9,2,9,2), not congruent to m mod 16. However selecting representatives t_0,t_1, reducing each mod q, then replicating DOES recover m exactly in this toy setting. Thus failure of invariance for the lifted state alone does NOT rule out all partial-conversion algorithms. The required selection, reconstruction, noise, precision, security, and true CKKS coefficient-vs-slot mapping costs remain unresolved.

## [FACT] Prior art checks

- Coron–Seuré, PaCo: Bootstrapping for CKKS via Partial CoeffToSlot, ASIACRYPT 2025, ePrint 2025/886. The original paper describes nontrivial product algebra C[Z]/(Z^B−α)→C^B through a ring isomorphism, partial CoeffToSlot, and a special secret-key pattern, specifically Sec. 1.2 (printed pp. 4–6). This is NOT contradicted by the above theorem: multiplication in coefficient coordinates is a pulled-back convolution-like product, not unchanged Hadamard product. Source: https://eprint.iacr.org/2025/886.pdf . Connector cached mirror version VERSION_UNVERIFIED; pdf text is available but screenshot via web was 403.
- Seuré, SCORE: A SlotToCoeff Optimization for Real-Vector Encryption in CKKS, ePrint 2025/1983 (2025): real-vector specialization and up-to-2× proof-of-concept reported; our theorem concerns complex-linear W and does not exclude real-linear structures. https://eprint.iacr.org/2025/1983
- OpenFHE advanced CKKS bootstrapping example already supports sparse packing and reports typical gains, hence sparse slots alone have no novelty. https://github.com/openfheorg/openfhe-development/blob/main/src/pke/examples/advanced-ckks-bootstrapping.cpp
- CKKS standard bootstrapping and sparse packing surveyed in https://link.springer.com/article/10.1186/s42400-025-00384-3

## [DERIVATION] Systems consequence

At fixed CKKS ring degree and modulus configuration, using d<n independent slots does not by itself reduce the cost of an N-degree ciphertext multiplication. Any projected reduction in conversion cost must be offset against representative extraction, replication, key-switching, precision/noise, total evaluator memory, and lost throughput capacity. No native performance claim.

## Decision

Do not promote periodic subspace closure / generic partial conversion to a new algorithm. Do not conflate PaCo paper's scheme named SHIP with our separate SHIP evaluation-key-memory research line.

NEXT_TEST: LIFT_REPRESENTATIVE_EXTRACTION_AND_RECONSTRUCTION_GATE — establish a precise fixed-workload extraction/replication equation at the actual CKKS polynomial/slot interface, and falsify cheap savings against prior sparse bootstrapping, PaCo, SCORE. Only one primary hypothesis + one cheapest decisive test next time.

CODEX: NOT_RUN
OTHER_TRACKS: UNCHANGED
STATE_UPDATE: only this isolated PURE-FHE finding; no changes to STATE.md or other tracks.
