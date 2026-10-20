# BOOT-B060 — Noisy NTRU gadget tree vs serial chain

DATE 2026-10-20; TRACK_ID BOOT; SHIP PAUSED.
STATUS FAIL_MATCHED_TOY_NOISE_GATE_FOR_BALANCED_TREE / PASS_EXACT_NOISY_RING_RECURRENCE / HOLD_REAL_FHE_AND_NOVELTY.
B059 was completed; do not overwrite its result.

## One primary hypothesis
Reassociate B059's bit-reencoded group product into balanced R*R subtrees, reducing online product critical-path depth g-1 to ceil(log2 g), without prohibitive noise growth using the **same** leaves and same number g-1 of gadget products.

## Direct source and scope
[FACT] Yiran Dai et al., "Accelerating MKFHE bootstrapping via parallel-friendly NTRU-based blind rotation", Cybersecurity 9:136 (2026), https://doi.org/10.1186/s42400-026-00563-w . Definition 5 / Lemma 4 and Appendix Proof of Lemma 4 define the vector NTRU decomposition product L_f(u)*R_f(v)->L_f(uv); for monomial v their noise recurrence has form Var(g_out) <= Var(g_left)+gamma Var(g_right), under its specified statistical assumptions. The paper discusses centered base-B digits in (-B/2,B/2]. R*R is **our candidate extrapolation** and does not inherit the published theorem without checking its hypotheses.

## Reproducible paired test (toy, not secure parameters)
[TEST] Exact negacyclic Z_Q[X]/(X^N+1) arithmetic with centered gadget decomposition h; B=16, two deterministic short unit keys f=1+X+X^2 and f=1-X+X^2, fresh per-limb independent coefficient errors sampled uniformly from {-1,0,1}, and public weights w=1+(2N/q)a with q=8|N. N=8,Q=2^20,d=5 (160 paired trials per g/f); N=16,Q=2^24,d=6 (40 paired trials per g/f). Normalized first leaf = Enc_f(s/f) with an additional separately noisy Enc_f(1/f); all other right leaves are raw Enc_f(s). Public leaf multiplier X^w-1. In **each paired trial** serial chain and balanced tree use exactly the same leaf ciphertexts and number g-1 of EXT multiplications.

[CHECK] For every noisy internal node (both L*R and candidate R*R) verified modulo Q the exact identity e_out,i = v e_left,i + sum_j h(C_left,i)_j e_right,j. Message tags also match X^(sum_j w_j s_j). No silent algebraic mismatch; errors are genuine accumulated residuals measured across all d*N output coefficients.

Results, serial/tree output noise RMS medians and median PAIRED tree/serial RMS ratios:
N8,f=1+X+X²: g4 26.40/88.33, ratio3.15; g8 47.98/1391.02, ratio29.44; g16 77.71/26484.12, ratio346.35.
N8,f=1-X+X²: g4 25.84/78.46, ratio3.00; g8 48.93/1461.71, ratio31.87; g16 77.04/35054.25, ratio431.79.
N16,f=1+X+X²: g4 44.53/382.84, ratio9.18; g8 76.79/8130.78, ratio101.56; g16 114.10/359364.61, ratio2970.83.
N16,f=1-X+X²: g4 43.22/301.36, ratio7.43; g8 74.66/11532.97, ratio149.41; g16 109.72/301844.39, ratio2679.27.
For g2, schedules coincide exactly (ratio1). At g16 a synthetic output residual max threshold Q/8 was crossed 34/160,41/160 (N8) and 5/40,4/40 (N16) balanced trials; 0 serial in the four suites. THIS THRESHOLD IS NOT A REAL NTRU DECRYPTION FAILURE OR DFR.

## Structural conditional explanation
[DERIVATION] In an idealized monotone independent-node noise surrogate V(T) <= V(T_left)+gamma V(T_right), a leaf contributes its own variance times gamma^(number of right edges on its root path). In ordered binary trees with normalized leftmost leaf and all others raw R, each R leaf has >=1 right edge. The left comb (serial order) has **exactly one** right edge for each R leaf. Any non-left-comb necessarily has an internal right subtree and hence a leaf with at least two right edges. For gamma>1 and positive leaf noise this strictly worsens the SURROGATE BOUND, regardless of its smaller depth. This is NOT a lower bound on actual noise, and all real correlated-noise assumptions remain unproven. A separate dynamic program illustrates the Pareto frontier: gamma50,g8 optimal depth3 upper-bound surrogate ratio to serial 377x, depth4 21.9x, depth7 serial 1x.

## Scope limits
These fixed toy keys/parameters do not meet NTRU security requirements, use deterministic centered digits rather than the paper's ideal randomized Gaussian decomposition theorem, lack source Algorithm2 automorphism keys/evaluations, omit last-group correction/hybrid product, key transcript IND-CPA/KDM proof, native implementation, and real PBS DFR. Centered mod-Q residual may understate unreduced error after wrapping. This is a **paired source-shaped operation experiment**, not an original-source end-to-end benchmark.

## Research conclusion
FAIL this direct balanced-tree scheduling under tested toy noise regimes; do NOT treat this as no-go against all low-noise multi-operand primitives or all FHE trees.
CRITICAL SURVIVOR: B059's binary-selector **serial** L*R chain avoids R*R intermediate noise and may remove the original g group automorphism steps, subject to source-faithful correctness, key/noise/security/novelty/cost audits. Avoid killing this surviving branch based on the failed tree.

NEXT_TEST B061: one decisive full-original-GIPEval versus serialized binary-selector gate, including automorphism/last-group correction and key material cost. Do not assert novel FHE before independent prior-art/security verification.
STATE_UPDATE NO: GitHub Notes read_repo_file for existing boot-STATE.md returned {}, preserve its 188KB content; append-only BOOT B060 finding.

Local reproducible files: b060_noisy_type_tree.py SHA256 78dc744533c884f29a520618fb48afa5fd38f59b8e65b56017b301140f082f20; b060_noisy_type_tree_results.json SHA256 92a31fddda378792238cf9e06daa16d168601f2df89d04d1c7792fb3b31fcab3; b060_depth_frontier.py and JSON; BOOT_B060_handoff.zip.
