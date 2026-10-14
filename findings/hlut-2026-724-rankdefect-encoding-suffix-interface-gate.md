# HLUT-01 — Rank defect does NOT locate failed LUT equations in the final delta row indices

**Date:** 2026-10-14 Asia/Tokyo. Independent new fully sourced TFHE research pre-screen following HERDS H06 (HUMAN_REVIEW/PARK). Human PI: 'continue'. Prior shared protocol read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, frozen global I192/parallel vFHE V26 STATE.md and `findings/OPEN_RESEARCH_BRANCHES.md` to avoid previously closed candidates. Do NOT change global/vFHE/SHIP/HERDS states; do not write any upstream repo.

## ONE primary falsifiable hypothesis and ONE minimal decisive test

**H-HLUT-01:** For the rank-deficient large-LUT decomposition matrix A in the authors' §5.2, with rank = s^n−delta, choosing a Gaussian-elimination completion beta with delta unconstrained equations automatically guarantees the evaluation output ytilde=A beta agrees with the ORIGINAL lexicographically indexed LUT y in the first s^n−delta coordinates. Therefore the suffix-only input promise of Algorithm 5 may be assumed from rank defect alone, WITHOUT a row permutation or checking other entries.

**Falsifier:** Give one exact valid source Eq(1), Eq(4)/Eq(6)–(8) chain of atomic nonlinear functions Phi, D matrix and F_p finite-field LUT y, where rank(A)=s^n−delta, but a selected valid partial linear completion beta gives mismatch in the **first** row and no mismatch in last delta original-index rows. If possible, inspect released artifact's original row checking to determine whether this is manuscript exposition/interface ambiguity only or actual source-code issue.

## Primary material and provenance [FACT]

- Sonia Belaid, Nicolas Bon, Matthieu Rivain, *Decomposition of Large Look-Up Tables for Fast Homomorphic Evaluation*, TCHES 2026 vol3, IACR ePrint **2026/724**, https://eprint.iacr.org/2026/724 . The research MCP returned **READY** 32 physical-page full PDF from fixed GitHub ePrint mirror at revision **108e41a7dc5788eb2d61023f9aecbcb72889d1d9**, SHA256 **cc45b49e20958f5c3fc1e327d84d1549d7fef08bdb4ba973dac75fd3a67efeb4**, official PDF version status **VERSION_UNVERIFIED**. Original physical pp9–10 Eq(1), §4.3 p12–14 Eq(4)/(6)/(8), p20 Algorithm4, p21 Table1 s2/n4 standard shape, pp24–25 §5.2 and Algorithm5.
- Paper §5.2 p24 explains 'Rank(A)=s^n−delta' and asserts a Gaussian-elimination beta yields ytilde matching y except the 'last delta coordinates'; p25 Algorithm5 **explicitly lists input precondition** y_i=ytilde_i for all i=0,..,s^n−delta−1 and checks only the last delta positions for an output-encoding remap. Standard Gaussian elimination row operations, however, can swap rows, so a suffix of echelon rows is NOT a suffix of the original LUT ordering unless permutations are tracked.
- Released author reproduction artifact: https://github.com/CryptoExperts/artifact-HLUT-TCHES , pinned inspectable public code at repo commit **088029cb4cd3a6b33ac10e0c78ea193b1835216d** (2026-07-02). `decomposer/src/decomposer/gauss.py` blob **84d4c8b9889720cf4a8207b7bedc054cbbae6863** defines `check_rank_drop(A,b,solution,encoding,rank_defect)` which explicitly computes `b_actual=np.dot(A,solution)` and iterates **over ALL original LUT indices** in `zip(b,b_actual)`, rejects collisions of one field code shared by distinct source symbols, and augments the output encoding otherwise. It does **NOT** blindly trust a suffix-only property. `decomposer/src/decomposer/encoding.py` blob **9ab78f59f67a6b2b25bf74f84bd306b2a8d08bd7** canonical maps 0→{0}, 1→{1}. `decomposer/src/decomposer/decomposition.py` blob **ce5d25df0ec2296c56a75c24e158f6cbe15f90f1** also verifies `dec.encoding.equal_under_encoding(...)` over **all** target outputs after solution. Published artifact's production ‘D’ random source samples binary entries via `np.random.randint(0,2)`; our exact D below has only binary entries, so this constraint is satisfied. Python dependencies galois+Rust extension were NOT built locally; the structural source proof and independent exact toy checker do not claim a run of the author artifact.
- `decomposer/src/decomposer/atomic_function.py` blob **8599ee4cd39e318b68ca6be9ee03a2d7ef68fb9e** samples alpha over F_p and requires nonlinear psi when p≤5. Our chosen psi(z)=z² mod3 is nonlinear. Source `Chain` allows n4 and lambda2; these are Table1's s2/n4, gamma1 shape (t0=2).

## ONE exact source-shaped counterexample [DERIVATION and EXECUTED]

Let s2,p3,n4,lambda2,t2,L6, so A is 16×18 over F3. Input enumeration 16 Boolean vectors in lexicographic order (0000 first). Define chain

- x4=(2*x0+0*x1+2*x2+1*x3)^2 mod3,
- x5=(2*x0+2*x1+2*x2+0*x3+1*x4)^2 mod3,
- phi0=phi1:z→z², alpha0=(2,0,2,1), alpha1=(2,2,2,0,1); legal nonlinear atomic functions.
- Let D=((1,0,0,0,1,1),(1,1,1,1,1,0)) in {0,1}^{2×6}, satisfying paper F3 uniform-sampling support AND public author's binary-D implementation support. Define U row=(x0,x1,x2,x3,x4,x5), V=(UD^T|1), A=V box U (blockwise row Kronecker product) EXACT paper Eq(6).

Independent modular RREF finds rank(U)=**6**, rank(UD^T)=**2**, rank(A)=**15**, delta=1. The first original row indexed x=(0,0,0,0) is identically zero in U and hence also in A: A_0=0^{18}. Thus ANY beta has (A beta)_0=0.

Choose a legal Boolean function y=1 at zero input and y=0 on the other 15. With beta=0 the transformed output ytilde=A beta is all-zero. Hence y_i=ytilde_i for i=1..15, and particularly **the final delta=1 row agrees**, while at original index **0** y_0=1 ≠ ytilde_0=0. Therefore the suffix-equality precondition **does not follow** merely from rank deficiency; this is not repaired by picking another beta because row0 has zero support for every beta. The above is an exact source-compatible matrix witness, NOT a sampled ciphertext nor a secret/noise issue.

Naively applying the paper's **suffix-only** Algorithm5 logic to this invalid input would visit just row15, find no conflicts, and return the unchanged canonical output encoding. It would mis-decode x=0000. However, paper Algorithm5 explicitly assumes all prefix rows equal, so **this is not a counterexample to Algorithm5's stated input-conditional correctness**. Rather it is a **gap in establishing that input precondition** from the preceding informal Gaussian-elimination narrative or any caller that forgets row permutations.

## Actual artifact mitigation [FACT/DERIVATION]

The authentic released helper `check_rank_drop` checks all 16 rows regardless of delta. It observes target 1 at x0000 but the computed field value 0, while 0 is already the canonical image of plaintext 0. The encoding's `is_y_busy(0)` is True and it returns `(None,encoding)`. The higher-level decomposer then rejects and resamples. Therefore **the released author source does NOT exhibit the hypothetical unsafe suffix-only acceptance on this witness**. A robust manuscript repair is to specify row-permutation transport or explicitly perform all-index encoding compatibility validation; the source already chooses the latter. Neither is a new FHE algorithm.

## Exact reproducibility

Standalone integer finite-field checker (not author-code execution): `/mnt/data/hlut_H01_suffix_rank_gate.py`, SHA256 **f334d2f1ac173f9fccaf25af7352fd14928a19232c1ea27768cd997d82d35563**; result `/mnt/data/hlut_H01_suffix_rank_results.json`, SHA256 **eddd0f471404fe73a0e0eee00d6b994bc8403baf233c17fade4abc2bd363111f**. Both executed in container with assertions rank(U)6, rank(V_without_one)2, rank(A)15, original mismatch index0, suffix match, code-equivalent collision reject. No published implementation, key generation, ciphertext or decryption experiment was executed.

## Research verdict

**STATUS: FAIL H-HLUT-01** automatic rank-defect→original-index suffix agreement. **PASS exact native F3 source-compatible rank witness and source-code mitigation audit.** **UNCLEAR** whether current TCHES final printed version explicitly states an additional row-order convention not in the cached IACR mirror; PDF VERSION_UNVERIFIED. No demonstrated correctness bug in author code, cryptographic attack, DFR failure or efficiency improvement. **NOVELTY NOT VERIFIED**.

**RESULT:** A real mathematical interface distinction between Gaussian-elimination pivot-row order and original LUT input indexing. Manuscript's §5.2 textual shorthand could be misleading unless read together with Algorithm5's explicit prefix-input promise. Released author artifact correctly checks **every** LUT output and rejects this witness. Simple correction is prior implementation behavior, not a publishable new technique.

**NEXT_ACTION:** **PARK this source-interface microaudit** unless the human PI finds a different, source-grounded HLUT issue such as a genuinely nontrivial decomposition search guarantee/cost bound not already covered by the authors' matrix rank checks and paper §5.2, and with potential measured cryptographic impact. Do NOT allege a published proof error or reach out to authors without PI approval. A new standalone LUT target requires one fresh falsifiable H and a decisive test; otherwise choose a different FHE direction. Global V/SHIP/HERDS unchanged.

**STATE_UPDATE:** YES new independent finding only. NO updates to shared global STATE.md, vFHE files, ship-memory-STATE, HERDS H06, or OPEN_RESEARCH_BRANCHES.