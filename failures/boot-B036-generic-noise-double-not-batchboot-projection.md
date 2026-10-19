# BOOT-B036 failure archive — B035 generic covariance example is not a valid BatchBoot post-repack falsifier; basic row dedup still too weak for publication

TRACK_ID BOOT
ITERATION B036
DATE 2026-10-19
STATUS FAIL_GENERIC_TWO_PATH_SUM_AS_REAL_DFR_COUNTEREXAMPLE / FAIL_NOVEL_BOOTSTRAPPING_CONSTRUCTION
STATE_UPDATE YES
SHIP PAUSED_BY_PI / NO CROSS-TRACK WRITES

Main test: Revisit B035 ordinary/parametrized radix4 RGSW SAME-message body row reuse under the ACTUAL BatchBoot Algorithm2 and Algorithm6+Homomorphic Trace, not a made-up sum of ciphertexts. The source has two alternative external products per (target output index j, selector branch r): direct OR tau_-1 inverse depending on negacyclic wrap. Original USENIX Security26 BatchBoot PDF physical p6 Table1/Eqs7–9, p7 Alg2, p18 Alg5/6 and C.2; independent TFHEpp implementation github virtualsecureplatform/TFHEpp file include/tfhe/batchboot.hpp blob db73ed7d1c5c3cf6283711e1a6640be4a513d0c8 lines 443–475 input/output mapping and 608–658 final trace/repack.

Exact linear projection in noiseless ideal ring arithmetic: n|N, all powers2, Repack(c0,...,c_(n−1)) at exponent j*N/n equals constant coefficient of c_j, and is zero in other exponents after sparse Homomorphic Trace. For each fixed selector row, at a fixed output position j there is ONE of direct and inverse usage, so the same key-row encryption error e_B cannot enter the same final output coefficient along both branches. If L_D,k and L_I,k are the source-exact linear error-influence vectors from same e_B, their inner product0 for every FINAL packed coefficient. Therefore shared/independent key row have identical FIRST-ORDER PER-COEFFICIENT variance contribution at this finalized projection, contrary to interpreting B035 generic 'add 2e_B' example as a proof of harm for true BatchBoot.

Exact tests:
 - Basis for N8/16/32, slots2/4/8/16 with slots<=N, 1552/1552 active coefficient projections pass.
 - N8 slots4, 250 random body-decomposition input arrays, 3 radix4 branches, positive/negative direction, every final output coefficient after trace, 12000/12000 cross-covariance=0.
 - After one additional ideal monomial-selection/negacyclic permutation stage, 500 random arrays, 24000/24000 final coefficient cross=0.
 - Important caution: before Homomorphic Trace, X1 coefficient with source body-decomposition inputs d0=1,d3=X² and radix4 row0 produces L_D=(0,1/4,0,1/4,0,1/4,0,-1/4), L_I=(0,1/4,0,1/4,0,-1/4,0,-1/4), thus independent var .5σ², shared .75σ² (1.5x), BUT sparse trace projects X1 to ZERO; thus B035 middle-state risk must not be mistaken for final active-slot DFR. With full packing n=N no trace, all final coefficients are unique-source projections, so the corresponding cross still zero.
Toy math excludes actual source torus rounded halves/FFT errors, approximate gadget digits depending on previous noisy ciphertexts, correlated KSK noise introduced during trace, previous key reuse and joint IND-CPA/circular security proof. Per-output marginals may match in ideal model while CROSS-OUTPUT covariance differs and could affect subsequent ciphertext computations or joint failure event. So no production DFR/cost/security claim.
The local dedup still saves theoretically three same-message body RLWE rows from 14 per radix4 digit, 21.4286% of EMP stored spectral row payload, NOT measured entire BSK/RSS/online latency, and no reduction in online external products/FFTs. Published paper already describes both halves as RLWE'_s(m), authors' original Zenodo artifact DOI 10.5281/zenodo.17936945 inaccessible, so novelty versus authors unverified. This is probably straightforward memory storage, not new cryptographic algorithm. Do not claim paper-ready contribution.
FINDINGS: findings/boot-B036-batchboot-repack-shared-row-orthogonality-audit.md
RESEARCH DECISION: Correct/archive B035 over-strong covariance concern, preserve viable ideal compact-format observation, then STOP B035/B036 key-row microbranch as not paper worthy. Next B037 source-first audit different modern bootstrapping algorithm with truly new structure and smallest decisive test; no B037 initiated. SHIP remains paused.
STATE_UPDATE YES.
