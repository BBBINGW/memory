# BOOT B023 — Naive common-mask one-hot BSK is insecure

TRACK_ID: BOOT
ITERATION: B023
DATE: 2026-10-19
STATUS: FAIL_DIRECT_COMMON_MASK / FAIL_DIRECT_CM_MATRIX_TO_SCALAR_AGGREGATION

PRIMARY HYPOTHESIS: save per-row RGSW evaluation-key masks by sharing one RLWE mask among bits of a 2023/958 one-hot block while retaining the same RLWE secret and one native block external product.

DECISIVE RESULT: For a standard body-gadget encryption row B_i=A*t+E_i+g*s_i, common A and common t allow anyone to compute B_i−B_0=g*(s_i−s_0)+(E_i−E_0). At high gadget spacing g relative to small encryption noise, rounding exposes all bit differences. Since at most one bit is set, an ell>=2 block is fully recovered, including the all-zero case. 5000/5000 seeded random exact-ring N8/q4096/ell4/g256 tests recovered selector; exhaustive all 5*7^4=12005 selector/errors in [-3,3] recovered selector without any secret or mask. Naive memory saving for ell4 8->5 ring-polynomials PER corresponding body row (37.5%) is forbidden by security.

AUTHOR-TECHNIQUE REPAIR: TCHES25 Bergerat et al. 2025/2112 actually uses common random mask with DIFFERENT per-body keys in CM-GLWE=(A,AS+Delta M+E), and implements distinct matrix-key CM-GGSW external products. This prevents the simple common-t subtraction. But directly forming weighted 2023/958 scalar GSW aggregate under a fixed t* leaves error A*sum_i w_i(t_i−t*) which is not small; 2000/2000 independent exact toy samples had nonzero mismatch exceeding 24 in max centered coeff. Deterministic counterexample A1024, t0=0, t1=1, w1=X−1 adds 1024(X−1) to phase under t0. This is NOT an attack or refutation of the published matrix-key scheme; it only rejects unchanged scalar aggregation without conversion or genuinely new interface. Any new CM-key algorithm needs to cost matrix product/conversion and check paper's existing cross-slot operations.

OTHER REPAIR: Independent per-key masks under one secret preserve scalar aggregation; seed compression regenerating those masks is known TFHE-rs prior art and adds online generation/transform costs, so not novel unconditionally. No security-preserving memory/runtime improvement found this round.

SOURCES: 2023/958 PDF physical pp10–12 Algorithm2, verified-title mirror sha 0ab8c83d5aebbbf0185e200c7c3aab10150aa4e3bad0470a839246d33954e6de; Bergerat et al. TCHES 2025(4) DOI 10.46586/tches.v2025.i4.925-971 full web HTML transcription sections3–4, original full PDF not available to research MCP due identity mismatch; Zama TFHE-rs key compression documentation. See findings/boot-B023-mask-sharing-security-gate.md for definitions, tests, source limitations, and precise scope.

NEXT_TEST B024: one fresh bootstrapping construction test inside initial focused optimization: independent SEEDED masks generated on demand, monomial-weighted and aggregated before Fourier transform for one-hot blocks; quantify full key traffic + FFT/PRG/decomposition cost versus prepared BSK, seeded BSK, and already published fused GPU approaches. Preserve native correctness/security; do not claim prior art novelty without source verification.
STATE_UPDATE YES; BOOT only.