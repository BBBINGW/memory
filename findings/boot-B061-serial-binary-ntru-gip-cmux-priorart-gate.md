# BOOT-B061 — Serial binary NTRU GIPEval: source-shaped comparator and CMux novelty gate
DATE 2026-10-20; TRACK_ID BOOT; SHIP PAUSED.
STATUS: PASS_EXACT_ALGEBRA_AND_TOY_NOISE_COMPARATOR / FAIL_PRIMITIVE_NOVELTY / UNCLEAR_NATIVE_SECURITY_DFR.

## Primary hypothesis
The binary-selector reencoding from B059, **retaining the serial NTRU L*R gadget chain** rather than B060's failed balanced R*R tree, can remove group-local automorphisms in Dai et al. GIPEval with tolerable noise and supply a novel FHE primitive. Test source-equivalent arithmetic/noise and prior art before implementation.

## Source-grounded baseline
[FACT] Dai, Xiang, Deng, Zhang, "Accelerating MKFHE bootstrapping via parallel-friendly NTRU-based blind rotation", Cybersecurity 9:136 (2026), https://doi.org/10.1186/s42400-026-00563-w; official PDF https://link.springer.com/content/pdf/10.1186/s42400-026-00563-w.pdf, physical p9 Definition5/Lemma4, p10 Eq(4), p11 Algorithm2/Theorem3. With g=n/l and w_j=(2N/q)a_j+1, ordinary group m outputs X^(sum w_j s_j)/f, final group has extra exponent -sum_all s_j. Original g-1 vector gadget multiplications plus up to g vector automorphism/key-switches per group, original n+1 BRKs and q-1 automorphism keys.

## Candidate exact construction and final-group requirement
Use raw gadget R_f(s_j) for non-first positions, normalized L_f(s_j) at group start, shared normalized K_f=L_f(1), and original final-group correction R_f(X^(-sum_all s)).
For binary s, X^(w s)=1+(X^w-1)s, hence first weighted key = K_f+(X^w-1)L_f(s), later right weighted key = G+(X^w-1)R_f(s), with G=(1,B,...). Serial L*R chain preserves normalized type; exact last-group correction must NOT be dropped.

[TEST] b061_exhaustive_phases.py: N8,q4,l2,g2, all 4^4 public coefficient vectors and 2^4 secret bit vectors: 4096/4096 full original-theorem-equivalent and candidate outputs match, 8192/8192 group outputs match, sum of group phases = (2N/q) sum a_j s_j modulo 2N.

[TEST] b061_gip_source_shaped_pair.py: **original-formula-equivalent** GIPEval including per-vector automorphism tau_t plus exact centered gadget key-switching; matched primitive key-noise samples against candidate serial form. R=Z_Q[X]/(X^N+1), N=8 Q=2^16 B16 d4 or N16 Q=2^20 B16 d5; f in {1+X+X²,1-X+X²}; g=2,4,8; two groups; 50 trials each (600 full instances). Every automorphism residual recurrence checked exactly mod Q. Output RMS median old/new:
N8 f+: g2 18.97/14.50; g4 33.74/30.12; g8 53.73/54.87.
N8 f-: 18.29/14.17; 32.07/31.51; 52.41/54.64.
N16 f+: 32.76/26.17; 52.78/50.53; 82.48/82.19.
N16 f-: 31.28/26.99; 53.03/50.73; 80.98/80.53.
All numbers are toy empirical residual RMS (larger of the two group outputs), NOT native NTRU DFR, security or latency. Source Algorithm2 conditional control flow was reconstructed from its mathematically equivalent Theorem3 traversal, not independently patched in published OpenFHE source.

## Decisive novelty falsifier
Let C be any vector ciphertext, S any raw bit GSW/NTRU gadget vector (even noisy) and A=X^w-1. Exact decomposition h satisfies sum_j B^j h_j(C_i)=C_i. For each ciphertext limb, 
EXT(C,G+A*S)=C + A*EXT(C,S)
**exactly as ciphertext arrays modulo Q**, not just plaintexts. This is standard binary CMux. [TEST] b061_cmux_equivalence.py 1000/1000 exact equality with noisy gadget ciphertexts at N8,16.
[PRIOR ART] Li et al., "Faster NTRU-based Bootstrapping in less than 4 ms", TCHES 2024(3):418-451, https://d-nb.info/1336785470/34 ; Section3.2/Algorithm1 explicitly use NTRU CMux with binary selectors, factors X^a-1, and special NGS'(1/f) normalized initialization; also key unrolling. Therefore **this operator is not a new cryptographic primitive**. Porting it to Dai grouped MKFHE would need a separate, demonstrable new systems/algorithm contribution relative to both prior papers.

## Conditional cost, security and noise
Original GIP key vector count n+q vs candidate n+2; delta q-2 vectors, excluding other MKFHE keys. Per group original g-1 vector products plus up to g automorphism switches; candidate g-1 products plus g sparse PUBLIC polynomial operations and shared normalized unit key. Source's approximate critical path 2n/l + (3k+5)lk units would become n/l+(3k+5)lk **only under unverified assumption that public ops, parameter/noise changes, key fetches and overhead are negligible**; theoretical optimized improvement bound sqrt(2) for this simplified expression, NOT measured runtime.
Binary-selector leaf error variance can double (right) or be 3x initial (left) due to two-term public polynomial and extra unit key. Elimination of auto-key-switch noise can offset it in toy tests. Shared K_f creates inter-group correlated error; source Lemma4 noise assumptions, full MKFHE hybrid aggregation, native DFR and circular/KDM security still open. No source-native security/DFR/latency claims.

RESULT: PASS source-equivalent algebra and toy-noise comparison. FAIL new-primitive novelty; identity is pre-existing NTRU-CMux. Do not promote to publication.
NEXT_TEST B062: ONE decisive system-delta/prior-art gate: compare grouping plus CMux against existing 2024 NTRU CMux and Dai multi-key aggregation at matched security/keys; if no genuinely new group interface/proof or end-to-end speed advantage over BOTH appropriate baselines, archive this path and pivot away from binary-CMux reformulations.
STATE_UPDATE NO: the GitHub Notes read_repo_file of boot-STATE.md returned {} and so must not be overwritten; this is an append-only findings commit, SHIP unchanged.
LOCAL ARTIFACTS: BOOT_B061_handoff.zip holds full 9KB report, 3 reproducible Python scripts and JSON results.
