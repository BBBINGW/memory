# BOOT B052 — Shorter-axis CMT contraction does not establish a new bootstrapping primitive

TRACK_ID: BOOT
ITERATION: B052
DATE: 2026-10-20
STATUS: FAIL_NOVEL_SCHEME_OR_CERTIFIED_E2E_GAIN / PASS_EXACT_CONTRACTION_AND_OPERATION_COUNTS
STATE_UPDATE: YES upon GitHub Notes state append. SHIP PAUSED.

Original paper: Dumezy et al., "Evaluating Larger Lookup Tables using CKKS", TCHES 2026(1), ePrint2025/1301 (original text mirror full35pp sha256 048ba3ae4fe97eae0417138b816572b1c79b503727db54ce76576a4d38190b19, version unverified), Algorithms 2,3,6,7 physical pp13,15–16,19–20; benchmark pp26–27. Original authored implementation is available upon request according to original manuscript, NOT fetched or tested; no assertion about actual OpenFHE code.

One primary claim: for CMT-FBT with digit widths p_i=2^w and a possibly short final digit, Algorithm6 groups ceil(nd/2) LSB digits into indicator vector U of length A and the remaining MSB digits into V of length B. Its literal loop always performs one last CTCT multiplication per U_i, i.e. A products, even when A≫B. Identity f=U^T Y V=(U^T Y)V=U^T(Y V) allows public LUT transpose and outer contraction over min(A,B), with same P=A*B MulInt, same KProduct ciphertexts, same abstract depth. All equations hold for arbitrary U,V and LUT over any commutative ring.

Exact operation table:
k13 w4, A256 B32, source544 vs transpose320 total CMT CTCT;
k14 w4 A256 B64 source576 vs384;
k16 w4 A256 B256 source768 vs768;
k18 w4 A4096 B64 source8512 vs4480;
k20 w4 A4096 B256 source8704 vs4864;
k18 w5 A1024 B256 source2304 vs1536;
k20 w5 A1024 B1024 source3072 vs3072.
These include original Algorithm3 Kronecker subtree CTCTs plus final orientation, not CMT's expensive P public constant multiplications nor functional digit decomposition/cleaning. Original 20bit,w4 final A4096→256 means -93.75% of FINAL CTCTs but -44.12% only of CMT CTCTs, NOT whole bootstrap runtime. Paper CMT at 20bit has 1,048,576 MulInt and significant FDD; cannot infer 44% full acceleration. Actual CKKS levels of U and V may differ; swapping scalar multiplication to the other subtree may change rescale/key-switch noise, precision and CPU cost. No native secure measurement, DFR or memory proof.

Exact Python plain integer tests: 50,600 legal one-hot LUT selections across 8 k/w configurations, including exhaustive x for k<=14, all exact matches source vs transpose; 600 arbitrary perturbed indicator-integer-vector tests for 3 size pairs also exact; additional independent 1024 nested contraction comparisons pass. These are commutative-algebra proofs, NOT encrypted FHE results.

PRIMARY FAILURE: Matrix transpose and choosing cheaper inner/outer contraction order is elementary prior art for tensor contraction and matrix-vector evaluation; source authors already explicitly optimize # CTCT products. The current cached paper Algorithm6 literal code is asymmetrical, but absent the native author source no claim that their actual implementation failed to optimize this; no novel crypto technique/security/noise bound or verified end-to-end benefit. Current result may support a modest engineering PR after source inspection, not standalone publication. Do not confuse with already archived B040 lowrank CMT contraction or B045–B047 noise cleaning/LUT synthesis; do not generate more trivial transpose tweaks.

FULL FINDING: findings/boot-B052-cmt-short-axis-lut-contraction-orientation-gate.md
NEXT B053: return to a genuinely new bottleneck in BOOT whole-algorithm computation, not basic CMT transpose. One smallest falsifiable claim/test, original technical source and author code if available. SHIP remains PAUSED_BY_PI and no other track modified. B053 NOT_STARTED.
