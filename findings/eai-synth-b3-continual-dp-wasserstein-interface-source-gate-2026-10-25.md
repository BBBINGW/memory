# EAI-SYNTH B3 — Source-first continual DP / Wasserstein interface gate
2026-10-25. TRACK_ID EAI / EAI-SYNTH only. B1/B2 unchanged. No Codex/GPU/models/remote experiments.

## One falsifiable hypothesis
H-B3: On a bounded common feature domain, a W1-accurate continual private reference intrinsically cannot yield useful W2/Wp distance-value comparison guarantees for Qiao-style selection.

## Sources [FACT]
1. Bun, Gaboardi, Neunhoeffer, Zhang, Proc. ACM Manag. Data 2(2), Article 94 (May 2024), DOI 10.1145/3651595, arXiv 2306.07884v2 2024-05-24; original https://arxiv.org/html/2306.07884v2 §§2–3 Algorithm 1, Theorem 2.1: finite T; persistent users contribute at each step; protect user's ENTIRE longitudinal trajectory under fixed nonadaptive adjacent streams; fixed-window and cumulative queries, not arbitrary Wasserstein utility.
2. He, Vershynin, Zhu, Online Differentially Private Synthetic Data Generation, 2024, original https://arxiv.org/abs/2402.08012 §2 Definitions 2.1–2.2, Theorem 1.1, Algorithm 1: infinite append-only stream, one event-level coordinate change; entire released sequence epsilon-DP; E W1 to cumulative empirical data <= O(epsilon^-1 log(t)t^(-1/d)) for d>=2; d=1 O((epsilon t)^-1 log^4.5(t)); ground norm L-infinity on [0,1]^d; runtime O(dt+t log t). Not an arbitrary fresh-window/whole-user guarantee.
3. Gu, Kunapuli, Bun, Chien, Greenewald, Differentially Private Wasserstein Barycenters, arXiv 2510.03021 original https://arxiv.org/abs/2510.03021 §4 Proposition 4.1, Lemma 4.3, Theorem 4.5: private Wasserstein coresets and barycenter objective guarantee. Direct prior art against generic interface novelty; static central individual-record DP, no longitudinal proof.
4. Qiao et al., ICML2026 arXiv 2606.13732v2 (2026-07-02), full https://arxiv.org/html/2606.13732v2 §3 Theorem 3 under Assumption 2; §§4.2–4.4 Theorems 4–5, Eq.19/23/25; App C.6 already DP optimal transport and collaborative Wasserstein barycenter. Not shown as continually private under feedback.
5. Asiaee–Aryan, UAI2026 arXiv 2607.08122v2 full https://arxiv.org/html/2607.08122v2: adaptive DP causal-workload, reusable calibrated synthetic release; not W2 continual.
6. Bun–Gaboardi–Wagaman FORC2026 https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.FORC.2026.22 : specific-task oblivious-vs-adaptive continual DP separation; NOT a general synthetic-data impossibility.
7. He, arXiv 2609.17624 https://arxiv.org/abs/2609.17624: offline intrinsic-dimensional W1 DP, not continual.
Input/privacy/output interface differences: Bun repeated users/finite T/user-level trajectory/window statistics; He fresh appended events/infinite horizon/cumulative W1; Gu static central record-level private coreset+barycenter; Qiao fixed cross-silo OT proxies, DPOT per-release; Causal-AIM static reusable causal workload. No automatic privacy equivalence across these models; cross-silo trust, communication, recursive generator accuracy not supplied by a metric bound.

## ONE cheapest decisive derivation [DERIVATION]
If diameter(Omega,d)=D, Wp(P,Q)^p <= D^(p-1)*W1(P,Q) by d(x,y)^p<=D^(p-1)d(x,y) under a W1-optimal coupling. Then
abs(Wp(S,P)-Wp(S,Q)) <= Wp(P,Q) <= D^(1-1/p)*W1(P,Q)^(1/p).
Two candidate DISTANCE-VALUE rankings are stable if true margin >2 D^(1-1/p) a^(1/p) whenever a realized proxy satisfies W1(P,Q)<=a. An expected W1 theorem yields only expected Wp via Jensen, NOT a deterministic margin certificate. On [0,1]^d, if He uses L-infinity W1 and Qiao Euclidean W2, W2,Euclidean<=sqrt(d*W1,L-infinity), a potentially costly dimensional factor.
Minimal two-time illustration: P1=delta_0, P2=delta_1, proxies Q1=delta_a,Q2=delta_(1-a), 0<a<1/2; candidates S_A=delta_0,S_B=delta_1. Genuine winner changes across t, margin 1; each proxy still selects correct candidate with margin 1-2a. These proxies are illustrative realized distributions, NOT asserted outputs of a private algorithm.
[NEGATIVE] H-B3 false in narrow Wp distance-value interface. Elementary bound and Gu §4 prior art prevent novelty.
[UNCLEAR] Pointwise OT dual potentials/scores, tight high-dimensional accuracy, semantic rare-mode support, user-level adaptive feedback privacy, sliding-window changing P_t, malicious-secure federated communication, recursive training convergence remain unproved here.

STATUS: FAIL_B3_NAIVE_METRIC_INTERFACE_GAP
RESULT: Existing continual DP synthetic releases plus private Wasserstein barycenters; metric-level value gap falsified.
NOVELTY: FAIL for metric-interface premise; NOT_ESTABLISHED for broader feedback-adaptive multi-silo topic.
NEXT_TEST: only on PI authorization, inspect He §2 and FORC2026 exact adaptive privacy definitions and test ONE 2-round feedback-driven private reference stream against original neighboring-transcript privacy definition.
STATE_UPDATE: pending GitHub write/readback and STATE pointer confirmation.
