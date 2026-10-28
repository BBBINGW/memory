# BOOT — DESCENT_MVB_GATE_3: prior-art closure and CCF-A/B novelty decision

Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER_LEVEL_ONLY
CODEX: NOT_USED
NATIVE: NOT_RUN

## Authoritative BOOT state (native status unchanged)

LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE_GATE: B163_CORRECTED_B160_NOSCALE_SELECTOR_GATE
B163_STATUS: PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
DO_NOT_AUTO_RUN_CODEX: YES

B145+B152: PARK / FAIL_NATIVE_VALUE
B158_ALGEBRA: PASS
B158_CTCT_MULT_COUNT: OPTIMAL
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B158_NATIVE_FEASIBILITY: UNRESOLVED
B162_B161_HYBRID: VALID_FAIL_AT_K1024
B163: NOT_RUN

## Question

After DESCENT_MVB_GATE_2 corrected the composition target from "commute function-specific multiplier through descent" to "find the latest function-independent prefix and branch to multiple outputs", this gate asks:

Is "large-domain / high-precision PBS + shared function-independent prefix + multiple output functions" itself a sufficiently novel research contribution?

Decision standard: user targets CCF-A/B; a routine combination or engineering port is not enough.

## Primary prior art recovered

### 1. Carpov–Izabachène–Mollimard (CT-RSA 2019 / ePrint 2018/622)

Established the baseline MVB pattern:
- same encrypted input;
- test-polynomial factorization;
- one shared expensive first phase / blind rotation;
- function-specific second-phase multiplication and extraction repeated per output.

Therefore "rotate once, read many" is old prior art, not a new contribution.

Source: https://eprint.iacr.org/2018/622.pdf

### 2. Kluczniak–Schild FDFB2 (ePrint 2024/1376)

This is decisive prior art against the broad candidate.

The paper explicitly states that it generalizes full-domain functional bootstrapping to multiple functions at the cost of only a single bootstrapping. In its multi-value Algorithm 4:
- two function-independent accumulators acc- and acc+ are computed;
- once they are available, the paper states that the calculation can be repeated for arbitrarily many functions/polynomials;
- per-function work is public polynomial arithmetic plus sample extraction.

The introduction explicitly says prior full-domain methods needed one full-domain bootstrap per output digit, while their method computes all outputs with one full-domain functional bootstrap; they give digit decomposition as a motivating workload.

This means:
  FULL_DOMAIN_FBS + MULTI_OUTPUT_SHARED_PREFIX = PRIOR_ART.

Source: https://eprint.iacr.org/2024/1376.pdf
Relevant extracted text: physical pp.3, 11-12 in the retrieved PDF. Web visual screenshot was attempted but the upstream PDF endpoint rejected screenshot retrieval; text extraction was readable.

### 3. Li et al. LFBS (ePrint 2025/022)

This is even closer to the proposed "high-precision + late branch" pattern.

The paper targets multi-input and large-precision LUTs. Its LWE-to-RGSW ciphertext conversion produces an encoding XEncode(m) independent of the LUT/test polynomial. The paper explicitly says:
- the conversion output and multiple test polynomials enable multi-valued functional bootstrapping;
- the new multi-valued conversion requires only one blind rotation;
- in LFBS, conversion is not contingent on the LUT encoding, enabling multi-valued FBS between all sub-LUTs and the shared RGSW(XEncode(m_k));
- Algorithm 6 returns l' outputs of f(m_0,...,m_{l-1});
- horizontal packing supports multiple LUT outputs.

So:
  HIGH_PRECISION / LARGE-LUT FBS + LUT-INDEPENDENT SHARED CONVERSION + MULTIPLE OUTPUTS = PRIOR_ART.

This does not use Descent-PBS, but it destroys novelty of the generic structural pattern.

Source: https://eprint.iacr.org/2025/022.pdf
Relevant extracted text: physical pp.3-4, 16-19. Screenshot verification was attempted but the IACR endpoint returned HTTP 403; extracted PDF text was readable.

### 4. Chartier–Koskas–Lemou ePrint 2026/2332

Public abstract (full PDF not acquired) explicitly studies:
- Single-Value Mode: one rotation per function;
- Multi-Value Mode: one function-independent rotation shared by all;
- factorization of each test polynomial into a function-specific dual factor and shared rotated factor;
- exact output-noise amplification under centered accumulator error with arbitrary covariance G.

Therefore:
  EXACT MVB OUTPUT-NOISE ANALYSIS FOR SHARED ROTATION = ACTIVE PRIOR ART.

Source metadata/abstract mirror:
https://menghao303.github.io/eprint-venue/
https://eprint-classic.github.io/2026.html

Do not claim theorem details beyond the public abstract until the PDF is supplied.

### 5. Bernard–Carouge–Joye–Orfila–Tap ePrint 2026/2310

Primary PDF remains unavailable and is already recorded in MISSING_SOURCES.md.
The title itself establishes direct activity on:
  LOW-NOISE MVB via LOG-UNIT LATTICE SEARCH + LUT SHIFTING.

A current secondary index reports that it reduces MVB noise while sharing one expensive homomorphic operation across several functions and reports up to 1.59x performance in 256-bit homomorphic multiplication. Because the primary PDF was not recovered, treat this performance description as secondary evidence only.

Sources:
https://eprint-classic.github.io/2026.html
https://www.bigpicture.cl/temas/cripto.html

Therefore noise-factor optimization alone is also crowded.

## Combined prior-art map

Claim / pattern | Prior art status
--- | ---
One blind rotation, many output functions | OLD: CIM19
Full-domain functional bootstrap, many functions with shared expensive prefix | DIRECT: FDFB2
Large-precision / multi-input LUT evaluation with LUT-independent converted state reused across multiple outputs | DIRECT/VERY CLOSE: LFBS
Exact noise amplification of MVM shared rotation | DIRECT: 2026/2332 abstract
Low-noise factor/search/LUT-shift optimization for MVB | DIRECT TOPIC: 2026/2310
Descent-PBS-specific maximal shared prefix across module descent + Meta-PBS refinements | NOT VERIFIED / MAY REMAIN OPEN

## CCF-A/B novelty decision

The broad LATE-BRANCH candidate is NOT strong enough:

  "Take a large-domain/high-precision PBS, share its function-independent prefix, then branch into multiple functions"

is now PRIOR_ART_CROWDED.

FDFB2 already does this for full-domain FBS.
LFBS already does this for large-precision/multi-input LUTs with a LUT-independent converted ciphertext reused across multi-valued evaluation.
2026/2332 and 2026/2310 make generic MVB noise optimization especially crowded.

A paper whose contribution is only "apply MVB to Descent-PBS" would most likely be an engineering combination rather than a CCF-A/B-level algorithmic contribution.

## Only surviving narrow Descent-specific question

Reopen this line ONLY if the exact 2026/2616 construction yields a genuinely Descent-specific theorem or asymptotic gain, for example one of:

1. a non-obvious maximal shared prefix spanning the module blind rotation, descent FKS, and one or more Meta-PBS refinements that prior MVB/full-domain/LFBS techniques cannot share;
2. a proof that multiple >ring-dimension LUTs can share an expensive module stage with asymptotically less module-rank work/key material than independent Descent-PBS;
3. a new representability/factorization theorem for a useful function family that exploits Descent's module-to-ring structure, not generic MVB;
4. a substantial evaluation-key memory reduction or latency reduction caused specifically by avoiding repeated module stages, with a construction-level explanation rather than only implementation batching.

If the 2026/2616 full text shows that LUT dependence begins before or at the expensive module/descent stage, or if the only shareable portion is the generic function-independent carrier already mirrored by FDFB2/LFBS, PARK permanently.

## Gate decision

GENERIC_DESCENT_PLUS_MVB: PARK / PRIOR_ART_CROWDED
GENERIC_LATE_BRANCH_NOVELTY: FAIL
GENERIC_MVB_NOISE_OPTIMIZATION: DEPRIORITIZE / CROWDED
DESCENT_SPECIFIC_MAXIMAL_SHARED_PREFIX: PENDING_SOURCE_ONLY
NOVELTY: NOT_ESTABLISHED
CCF_A_B_READINESS: NO
CODEX_REQUIRED_NOW: NO

The source-critical blocker remains ePrint 2026/2616 full text.

## Research priority

Do NOT spend more paper-level cycles inventing generic MVB variants around Descent-PBS while 2026/2616 is missing.

Priority within BOOT while Codex is unavailable:
1. preserve B163 as highest native gate once quota returns;
2. park generic Descent-MVB;
3. continue fresh structural BOOT scouting for ideas that eliminate a bootstrap stage, sequential dependency, or large evaluation-key traffic and are not simply multi-output amortization;
4. reopen Descent-MVB only after 2026/2616 PDF is supplied and only for the narrow Descent-specific gate above.
