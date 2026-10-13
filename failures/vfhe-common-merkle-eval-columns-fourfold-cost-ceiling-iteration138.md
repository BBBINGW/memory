# Iteration 138 — Reusing Brakedown evaluation Merkle columns: conditional binding, <4x source-format cost ceiling

Date: 2026-10-13. PI authorized I138 by “好的，请继续” after I137. Exactly ONE primary hypothesis and ONE cheap source-anchored communication/security-order falsifier. No new compiled PCS/SNARK implementation or benchmark; do not conflate optimized protocol with original paper, and do not claim original vFHE security is broken by this modification.

## Read-before-write / primary source

- Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, then current `STATE.md` last I137 sha `1bbac414dda94c08a5ecb03d6893296dcd4f6897`; read long-term `findings/OPEN_RESEARCH_BRANCHES.md` and failure archives I136 and I137, plus I94 soundness/cost.
- Cascudo, Costache, Cozzo, Fiore, Guimarães and Soria-Vazquez, *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, IACR ePrint **2025/286** https://eprint.iacr.org/2025/286. Research MCP 52 physical page mirrored PDF sha256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`; latest official binary **VERSION_UNVERIFIED**. Re-read F.1 physical p50 and **Appendix F.2 physical p51**, plus source §5 original definition pp25–26 from previous I137: Ring PCS is product of μ field PCS; `U_f ∈ F^{m_B × m_B}` and `f(a)=q1(a)^T U_f q2(a)`. Each source F.2 EVALUATION phase runs:
  1. prover sends `v'=q1(a)^T U_f` (m_B native-field elements);
  2. verifier independently samples uniformly `Q' ⊆[M]`, |Q'|=t;
  3. prover opens the t **columns of SAME committed encoded matrix Uhat_f** at Q', sends each m_B-symbol column and Merkle authentication;
  4. verifier tests `Enc(v')|Q'=q1(a)^T Uhat_f[:,Q']` and `y=⟨v',q2(a)⟩`.
  Source explicitly permits reuse of the TESTING phase for different evaluation points, but NOT reuse of one F.2 EVALUATION transcript across multiple a. In this note common-column sampling is OUR proposed modification, not paper algorithm/prior-art novelty.

## ONE hypothesis and cheapest falsifier

[HYPOTHESIS] A 4-point Brakedown opening for the FOUR fully independent vFHE I94 sumcheck terminal queries can preserve their independence and per-opening binding by sharing **only the evaluation Merkle-column set Q'**, while saving **at least 10× total communication** over four original F.2 EVALUATION phases, without a newly designed PCS proof interface.

[FALSIFIER/ONE TEST] Establish the right interactive ordering and a marginal per-evaluation binding/union-bound analysis; then derive and exactly evaluate the tightest best-case SOURCE F.2 field-symbol and Merkle-column communication ratio assuming every repeated column opening and authentication path is sent only ONCE, while all four `v'_j` remain mandatory by I137 rank-4 test. If even the perfect-reuse ratio <10, the speed/communication hypothesis is dead regardless of actual library optimization. This is a protocol-interface gate; not a security reduction for a new full SNARK.

## Common-column batch ordering / scoped soundness argument

Given **one pre-existing, tested committed encoded matrix Uhat_f per CRT component**, all four I94 Sumcheck repetitions sample their rho_j and **all terminal challenge coordinates r^(j) independently**; no q1/q2 equality and no shared Sumcheck randomness.

Prover sends all four `v'_j=q1(a_j)^T U_f` (or claimed v'_j) and claimed evaluation results y_j **before** the verifier samples shared fresh uniform `Q'`. Then one shared Q' is sampled, encoded columns of Uhat_f at Q' are opened once, and each j independently checks
```
 Enc(v'_j)|Q' ?= q1(a_j)^T Uhat_f[:,Q']
 y_j ?= ⟨v'_j, q2(a_j)⟩.
```
Every j marginally sees a post-v'_j *uniform fresh* Q' of the same size/distribution as single F.2; **conditional on original source testing-phase soundness and fixed malicious v'_j before Q'**, a single false opening retains original per-opening evaluation rejection bound `ε_eval` (Proposition5.1 source p26 gives a bound in terms of code distance and t). Events for different j MAY be correlated because same Q', but for *some false PCS opening* the union bound `Pr[any bad opening passes]≤4 ε_eval` remains valid; across μ components, a simple upper-bound budget `≤4 μ ε_field` subject to the original testing phase, commitment binding, full transcript extraction, and exact parameter proof. This does NOT give fourth-power PCS soundness; I94's fourfold exponent concerns the independently sampled sumcheck checks conditional on correct oracle openings. Fiat–Shamir/challenge domain separation, committed-oracle extraction and modular error budget for complete vFHE remain UNPROVED here.

CRITICAL ORDER: If first `Q'` is revealed before all `v'_j` are fixed, later alleged evaluation vectors can adapt to the revealed positions; the standard one-evaluation post-v' sampling reasoning no longer applies. The proposal requires a **batch barrier**, which changes source F.2 scheduling and is not a drop-in transcript rewrite. Also each μ CRT component has its own different committed matrix and Merkle tree; the SAME column DATA/path cannot be reused across distinct field component trees, only across four openings of each SAME tree.

## Source F.2 cost accounting (field symbols, no compression)

Let m_B=2^(ell/2) (matrix side), μ=number of CRT field components, t=sampled evaluation columns, b_F=field-symbol bytes (for the paper F_(p^4) with 49-bit p, **at least 25 bytes** in fixed-length encoding). Exclude identical testing-phase and fixed commitment costs, which are already amortized by source; exclude nonnegative Merkle path/hash bytes first. For FOUR original independent F.2 evaluation phases, ignoring accidental intersections of Q'_j:
```
 V_4 = 4 μ m_B b_F                        (mandatory four v'_j)
 C_4 = 4 μ t m_B b_F                      (four column opening matrices)
 T_4 = 4 μ m_B (1+t) b_F.
```
For proposed perfectly shared `Q'` and column/authentication data:
```
 V_shared = 4 μ m_B b_F
 C_shared = μ t m_B b_F
 T_shared = μ m_B (4+t) b_F.
```
Thus the exact best-case source-field-symbol speedup ceiling
```
  T_4 / T_shared = 4 (1+t)/(4+t) < 4   for every finite t≥1.
```
If adding Merkle paths at t leaves per tree, they are likewise reused at most FOUR copies→ONE while all other messages stay; the maximum overall communication gain from reusing duplicated evaluation-opened data/paths is **≤4×** across the four evaluations, never ≥10×. If an actual implementation already deduplicates common opened columns or uses Merkle multiproofs, actual gain can be smaller. This ceiling does NOT apply to a NEW PCS protocol replacing the 4 vectors or compressing high-rank functionals, which is a different nontrivial idea.

Concrete exact calculations (MiB, 2^20 bytes; **illustrative t=32, NOT original security-approved t value**):
```
μ    m_B    V_4      original field-symbol total   shared field-symbol total   ratio
6144 256    150 MiB          4,950 MiB                1,350 MiB                3.66667×
8192 1024   800 MiB         26,400 MiB                7,200 MiB                3.66667×
```
For illustrative t=1,4,8,32,128,1020, ratios respectively `1.6,2.5,3.0,3.666667,3.909091,3.988281`; exact rational arithmetic, monotonic <4 as t→∞. Example t=1020 appears in source p26 only for a particular RS-code parameter case; do not mix with arbitrary μ,m_B to claim a real selected complete parameter set. Real PC field security, Merkle hash overhead, resulting bandwidth and κ-bit extension encoding are not benchmarked.

## Scientific judgment

[PASS CONDITIONAL SECURITY GATE] A shared Merkle *column sample* need not invalidate individual field PCS opening checking, **provided** all 4 vectors and y claims are fixed before one fresh uniform shared Q', and the source's field PCS binding/commitment testing assumptions hold. This is not a new proven full protocol, nor does it imply independent PCS failure probabilities.

[FAIL TARGET] Even perfect reuse saves strictly <4× field-symbol bytes (and ≤4× all communication from only deduplicating 4 copies). It is **structurally impossible for this limited edit to give 10×**, even without counting unavoidable Sumcheck messages, 4 v' vectors, commitments, field-component multiplicity and full protocol overhead. No novelty: reusing openings for same committed data is straightforward.

[OPEN] A genuinely different multi-point PCS that handles general rank-four linear functionals, keeps independent Sumcheck challenges, and proves compact commitment opening with a big source-level gain remains unconstructed. Original vFHE CRT diagonal-table issue I59–60 remains **OPEN/HUMAN_REVIEW**, not an unpatched shipped exploit.

## End of iteration

STATUS: **FAIL 10x source-Brakedown Merkle-only sharing / PASS conditional per-opening correctness and ≤4x cost ceiling / HUMAN_REVIEW**.
RESULT: Sharing Q' for four independent terminal points is conditionally compatible with per-evaluation source F.2 binding if prover first fixes all v'_j, but perfect amortization has source message cost ratio 4(1+t)/(4+t)<4. Therefore this simple source-compatible PCS micro-optimization misses the 10x communication target even before other costs. Do not conflate fourth-power independent sumcheck soundness with union-bounded shared-Q' PCS error.
NEXT_ACTION: I139 ONLY if PI authorizes. Recommend **PARK further unchanged-Brakedown I136–138 micro-optimizations**; choose an actually NEW PCS/CRT-index-consistency mechanism with ≥10× cost and proof falsifier or pivot to higher-yield **MRFHE complete two-key-switch/noise PCMM** from opportunity backlog. Do not repurpose current paper as established vulnerability; official revised PDF version still not byte-verified.
STATE_UPDATE: YES — this closes third specific economical PCS batching shortcut, yields material priority shift; keep underlying vFHE CRT problem OPEN/HUMAN_REVIEW and preserve I95 separate repair archive.
