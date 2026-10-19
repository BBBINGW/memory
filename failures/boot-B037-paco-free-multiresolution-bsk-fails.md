# BOOT B037 failure archive — No free PaCo multi-C key reuse by slot permutation

TRACK_ID: BOOT
ITERATION: B037
DATE: 2026-10-19
STATUS: FAIL_FREE_PERMUTATION_REENCODING / PASS_PUBLIC_LINEAR_REENCODING / UNCLEAR_NATIVE_COST
STATE_UPDATE YES

Paper Coron–Seuré PaCo ePrint 2025/886 ASIACRYPT2025, cached title-verified 35pp mirror PDF sha256 ee427d006097fabdbd30a0a4dc36ed09df5ffea68df30a0511cc154b303a936a VERSION_UNVERIFIED; original author implementation se-tim/PaCo-Implementation paco_package/ckks_x.py blob ea8073682c82dadcc892ab48b29e8d8bc4ccc237 lines116–151 and author original butterfly get_E in se-tim/CKKS-in-SageMath/ckks_package/fast_dft.py blob ee6c9dfbb7393c1b78ba6f994d7b802e5800d3e8.

Primary tested hypothesis: Maximal capacity PaCo 4 encrypted BSKs for C=B=N/(4h) can serve any lower C through a FREE public slot permutation/phase relabeling, reducing key storage without any extra rotations or key noise. FAIL in a valid small structured-secret instance: N=64,h=2,B=8, C2/4/8, output 32 complex slots; actual source matrix chain for a onehot t row yields BSK plaintext at C8 with16 nonzero unit-modulus slots, at C4 with8, and at C2 with4. A global slot permutation with only complex unit phases preserves support and magnitudes, so cannot equal these other vector representations. This is not a universal impossibility bound against public diagonal masks / sums / CKKS linear transforms.

Constructive repair: For same t onehot coefficient vector d of hB16 possible locations, each sigma_t(C)=M_C d is public linear. M_8 shape32x16 full rank16; A_C=M_C pinv(M_8) public and independent of secret gives sigma_t(C)=A_C sigma_t(8), 8000/8000 source-shaped random structured onehot key tests PASS at float tolerance1e-12. But canonical pseudoinverse A_C occupies all32 cyclic-diagonal offsets and naive slot diagonal method can involve31 rotations per converted encrypted BSK, key switching/precision and possible extra scale depth. Dense canonical A does NOT prove no sparse butterfly factorization exists. One-C-at-a-time source setup gains no BSK storage reduction, on-demand multi-C use a conditional niche only; no native encrypted correctness/actual memory/DFR/benchmark; prior art generic CKKS linear transforms.

Full findings: findings/boot-B037-paco-multiresolution-bsk-linear-map-cost-gate.md. Local reproducible toy script /tmp/boot_b037_paco.py SHA256 4bf38223a4b47241c326a4015a08355a8f89587db056cf37d095beda086a6b9e, source-shaped N64 complex butterflies, not production crypto.

Next B038: cheapest factorization/online CKKS cost gate only, if no convincing whole-scheme advantage archive PaCo multi-C key representation and move to more substantive BOOT paper. SHIP PAUSED_BY_PI, no other research files accessed/written. B038 NOT STARTED.