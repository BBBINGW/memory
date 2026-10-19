# BOOT-B010 — MPmul selector reuse versus heterogeneous gadget weights

TRACK_ID: BOOT
DATE: 2026-10-19
ITERATION: B010
STATUS: FAIL_AUTOMORPHISM_FREQUENCY_WEIGHT / PASS_EXACT_TOY / UNCLEAR_INPUT_CONDITIONED_COVARIANCE
STATE_UPDATE: YES

## Primary hypothesis
[HYPOTHESIS] In Guimarães–Pereira's amortized bootstrapping MPmul, each GSW selector C_i (encrypting exponent bit v_i) is only effectively used at the fraction 2^i/n of coordinates that need X -> X^{-1} automorphism, so a noise weight proportional to 2^i/n can be used when importing Hong–Lee 2025/1892 heterogeneous/approximate gadget choices.

## Sources and provenance
[FACT] Guimarães–Pereira, "Fast amortized bootstrapping with small keys and polynomial noise overhead", ePrint 2025/686, 34 physical pages, version UNVERIFIED mirrored PDF SHA256 84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335. Phys. pp. 10–12 Section 2.1, Algorithm 1 MPmul and Lemma 3.1, pp. 13–14 Algorithm 2 and Lemma 4.1. The ACM CCS 2025 publication is DOI 10.1145/3719027.3765181; author's repository https://github.com/antoniocgj/Fast-Amortized-Bootstrapping .
[FACT] Hong–Lee, ePrint 2025/1892, physical pp. 11–13, Theorems 3.1–3.2 and note that usage frequency of each GSW/bootstrapping key matters. Mirror PDF SHA256 508a5a0b3914e23e8d71198476a50879c471a6f192e6f65bcd68314b89622018, VERSION_UNVERIFIED. Their theorem is derived for CGGI-like blind rotation with different *keys*, each typically used once, not MPmul where a selector is reused across n outputs.

## Decisive source-level kill test
[FACT] MPmul Algorithm 1, bit index i, shift s=2^i:
for EACH j=0,...,n-1:
    candidate a_{i,j}= Automorphism(c_{n-s+j}, X->X^-1) if j<s,
                     = c_{j-s} if j>=s;
    c'_j = (a_{i,j}-c_j) boxdot C_i + c_j.
Same GSW key C_i is reused for all n CMUX external products. The automorphism KSK is a single key for X->X^-1, also reused. Thus each stage has EXACTLY n ExtProd calls and s automorphism calls in this pseudocode, irrespective of bit index or bit value. The source's Algorithm 1 line 5 text extraction is garbled at its upper limit; mathematical range j>=s up to n-1 follows from the source's stated signed rotation and correctness, and was tested by independent reference arithmetic. Operation counts (n=8): i=0 -> (8 ExtProd,1 autom), i=1 -> (8,2), i=2 -> (8,4).
[RESULT] Weight 2^i/n measures only the *fraction of outputs needing automorphism*. It is NOT the GSW key usage frequency, number of external products, or per-output key-noise weight. That original hypothesis is FALSE before tuning any gadget parameters.

## Stronger exact finite-ring toy falsifier: all outputs may have same GSW-key noise norm
[DERIVATION] Work with n=8 coefficient-rotation ring Z[Y]/(Y^8+1) and RLWE exponent ring R=Z[X]/(X^16+1), ignoring encryption/random noise for the correctness input. For s in {1,2,4}, let m=n/s (always even) and choose encrypted exponent messages
    u_j=(m-2)/2 - floor(j/s), 0<=j<8.
Then for non-wrapped j>=s, u_{j-s}=u_j+1; for wrapped j<s, -u_{n-s+j}=u_j+1.
Hence for ALL output j, a_{i,j} encrypts X^{u_j+1}, c_j encrypts X^{u_j}, so plaintext candidate difference is
    Delta_{i,j}=X^{u_j}(X-1).
Under negacyclic coefficient embedding in R, ||Delta_{i,j}||_2^2=2 for every i and j. Independent integer reference calculation checked all 24 of 24 (three i's × eight j's), with n=8 and N=16. For an idealized single reused GSW error polynomial e_i with independent coefficient Gaussian variance sigma_i^2, the extracted scalar y_{i,j}=[Delta_{i,j} e_i]_0 satisfies Var(y_{i,j})=2 sigma_i^2 for every j and i, independent of s/n. Thus the source-valid branch choices admit identical per-output selector-error sensitivity even though automorphism counts 1,2,4.
[TOY CAVEAT] A single shared Gaussian error polynomial and one linearized external-product row are not the full randomized GSW external-product computation. This falsifies a proposed universal 2^i/n scaling law, not a full source DFR theorem.

## Key-reuse covariance counterexample
[DERIVATION] The same selector key C_i is used in all n CMUXs, so its underlying encryption-error polynomials are shared across j. Conditional on predictable gadget digits d_{i,j}, linearized key-error terms are of the form xi_{i,j}=L(d_{i,j}) e_i, and the output covariance across coordinates is
    Cov(xi_{i,j},xi_{i,k} | d)=sigma_i^2 L(d_{i,j}) L(d_{i,k})^T,
not generally zero.
For the above exact integer monomial toy and a single shared Gaussian coefficient error vector e in R of degree 16, the 8x8 covariance matrix (normalized by sigma_i^2) is the Gram matrix of the coefficient-0 linear maps of Delta_{i,j} e. Independent Python integer negacyclic convolution and exact SymPy matrix ranks yielded:
    i=0 (s=1): diagonal entries all 2; covariance matrix rank 8.
    i=1 (s=2): diagonal entries all 2; rank 4; Cov(y_0,y_1)=2 sigma².
    i=2 (s=4): diagonal entries all 2; rank 2; Cov(y_0,y_1)=2 sigma², i.e. perfect positive correlation for these two equal-variance coordinate errors.
Consequently Var(sum_j y_{i,j}) /sigma² is 2,8,32 for i=0,1,2, respectively, whereas incorrectly assuming cross-output independence would always yield 16. The sum is a *diagnostic* algebraic statistic, NOT a homomorphic aggregation explicitly performed by MPmul. The exact toy covariance is not claimed for the full real ciphertext distribution.
[FACT] Source Lemma 3.1 gives stage-uniform per-output upper bound for the key-error and automorphism-key-switching effects; it does not prove per-stage selector variance shrinks by fraction s/n. It is a worst-case/pessimistic bound on each output coefficient.
[CAUTION] Repeated use of the same evaluation key is legal under standard evaluation-key assumptions, but across-output GSW *key errors are not fresh independent samples*. Conditional independence across different selector keys/rows is a separate question. Never use independent-GSW-per-output variance or (1-(1-p)^n) joint-DFR formula without proof. A union bound is safe but may be loose. Nor does key reuse by itself imply a cheaper bootstrap.

## Does a salvage exist?
[UNCLEAR] Gadget-digit norms for operands a_{i,j}-c_j, and the effect of the X->X^-1 automorphism KSK on the *input* error, may depend on i, j, message distributions and prior stages; this could allow nonuniform empirical or robust per-bit precision with a new certified bound. The current source Lemma 3.1 does not expose such differentiating weights. Heterogeneous GSW keys by stage are type-compatible but 2025/1892 already proposes per-key heterogeneity: no demonstrated novelty from a naive MCKP port.
[UNCLEAR] Real opportunity could instead be a covariance-aware simultaneous-output DFR analysis exploiting shared selector keys, if it permits a lower-key-size/latency configuration under a rigorously proven joint failure probability. This is speculative; toy rank deficiency does not prove real gains, and adaptive ciphertext gadget digits, key switching, cross-query reuse and security all need audit.
[DECISION] Kill/park ONLY the 2^i/n selector-noise weighting hypothesis. Do not assert all heterogeneous-gadget optimization of MPmul is impossible. Avoid futile parameter tuning from unsupported weights.

## Reproducible reference summary
n=8,N=16, i=0: u=[3,2,1,0,-1,-2,-3,-4]; i=1:u=[1,1,0,0,-1,-1,-2,-2]; i=2:u=[0,0,0,0,-1,-1,-1,-1].
Evaluate v_i=0/1 via MPmul signed coefficient rotation in Z[Y]/(Y^8+1) for all eight v=0..7; 8/8 complete binary rotations matched direct negacyclic monomial multiplication for a distinct sample input [-3,5,-2,4,7,0,6,1]. In the separately constructed 3x8 exponent-difference family, 24/24 gap identities and ||Delta||²=2 passed. Covariance matrices computed with integer negacyclic ring multiplication, exact SymPy ranks 8,4,2. No native FHE benchmark or end-to-end DFR proof was performed.

## End of iteration
STATUS: FAIL_AUTOMORPHISM_FREQUENCY_WEIGHT / PASS_EXACT_TOY / UNCLEAR_COVARIANCE_OPPORTUNITY
RESULT: Each MPmul bit key is used n times, despite varying 2^i automorphisms; key noise can be equally sensitive across bit stages and correlated across outputs; no 2^i/n-based heterogeneous-gadget noise schedule is justified.
NEXT_TEST B011: Choose ONE hypothesis — can a source-faithful multi-output correlated-error model produce a **nontrivial, uniform-over-admissible-inputs** joint-DFR upper bound better than straightforward union bound at unchanged key distribution? Start with two-output/one-selector symbolic covariance and attempt to destroy input-independent correlation; only after this passes consider parameters or implementation. If covariance cannot be guaranteed uniformly, archive this correlation-to-size direction and choose another structural target in BOOT.
STATE_UPDATE: YES; BOOT files only.
