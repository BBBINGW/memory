# EAI-SYNTH B3 negative: naive bounded Wasserstein metric-interface gap fails
2026-10-25 | EAI-SYNTH only. No model/GPU/Codex.

[HYPOTHESIS] A W1-accurate continual DP synthetic reference cannot yield any nontrivial W2/Wp distance-value comparison bound on a common bounded metric space.
[ONE DECISIVE TEST / DERIVATION] For diameter D, Wp(P,R)^p<=D^(p-1)W1(P,R) from a W1-optimal coupling. Therefore for any candidate S, |Wp(S,P)-Wp(S,R)|<=D^(1-1/p)W1(P,R)^(1/p). True two-candidate distance margin >2 times this bound preserves the ranking; expected W1 accuracy implies expected Wp bound only. If W1 is L-infinity and W2 Euclidean on [0,1]^d, W2<=sqrt(d W1), so the dimensional penalty is real.
Two-time witness: P1=delta0, P2=delta1; proxy R1=delta_a,R2=delta_(1-a), 0<a<1/2; candidates delta0 and delta1. Winning candidate switches and proxy value gap is 1-2a>0. Purely illustrative, NOT a constructed DP release.

[FACT / prior art] Gu et al. (2025/2026) 'Differentially Private Wasserstein Barycenters', arXiv 2510.03021 §4 Proposition 4.1/Lemma 4.3, https://arxiv.org/abs/2510.03021 , already gives private coreset to barycenter objective interfaces. He et al. (2024), https://arxiv.org/abs/2402.08012 Theorem 1.1 already gives epsilon-DP infinite-append-stream synthetic data with expected cumulative W1 error. Bun et al. 2024, https://arxiv.org/html/2306.07884v2 , protects finite longitudinal user histories for specified query classes. Qiao et al. ICML2026, https://arxiv.org/html/2606.13732v2 §§4/App C.6 already study multi-silo geometry and DPOT. These adjacent guarantees are not identical and do not automatically prove feedback-adaptive, malicious-secure or rare-support preservation.

[NEGATIVE] No nontrivial new metric-level incompatibility discovered; elementary transfer and explicit closest prior art kill narrow novelty.
[UNCLEAR] Per-example Kantorovich potential scores, adaptive stream privacy under generator feedback, fresh-window P_t rather than cumulative empirical data, recurrent users/multiple silos, unknown drift, rare-support utility and recursive learning remain distinct unproved questions; NO new gap claimed.

STATUS: FAIL_B3_NAIVE_METRIC_INTERFACE_GAP
RESULT: VALUE-level W1-to-Wp interface has a standard conditional guarantee and existing DP barycenter prior art.
NOVELTY: FAIL for tested premise; broader topic NOT_ESTABLISHED.
NEXT_TEST: conditional PI-authorized single two-round feedback-adaptive transcript proof check against He's Definition 2.2 and Bun–Gaboardi–Wagaman FORC2026 adaptive separation.
STATE_UPDATE: pending root STATE append/readback.
