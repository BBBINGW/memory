# Resume Independent FHE Bootstrapping Research — Post Structural Scout / B163 Pending Codex

Date: 2026-10-28
TRACK_ID: BOOT

## Research role and isolation

The user is PI and makes final decisions on research direction, novelty, experiments, and publication value.
The assistant acts as a cryptography research student.

This is a continuation of an existing BOOT research line, not a new project.

Strictly isolate BOOT from SHIP, PURE-FHE, CGS, VFHE, EXPLORE, EAI, and all other tracks.
Other tracks may be read only for technical background; do not modify them.

The user's research philosophy is:
    smallest falsifiable claim
      -> cheapest decisive test
      -> minimal verification.

The user only considers CCF-A/B publication targets. Routine engineering combinations, weak constant-factor tweaks, or already-crowded variants should be killed early.

## Authoritative native status

TRACK_ID: BOOT
LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE_GATE: B163_CORRECTED_B160_NOSCALE_SELECTOR_GATE
B163_STATUS: PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
DO_NOT_AUTO_RUN_CODEX: YES

CURRENT_MODE:
    PAPER_LEVEL / SOURCE_LEVEL RESEARCH ONLY

MAIN_EXISTING_NATIVE_CANDIDATE:
    B158

B158_NATIVE_FEASIBILITY:
    UNRESOLVED

B158_NOVELTY:
    PROMISING_NOT_ESTABLISHED

Do not launch Codex, native experiments, server jobs, parameter changes, environment changes, or code modifications until the PI explicitly says Codex quota is back / authorizes the experiment.

When Codex quota returns, B163 is the highest native priority.

## Native history that must remain fixed

### B145 + B152

Adjacent-window pre-bootstrap overflow cancellation:
- ALGEBRA: VALID
- NOVELTY: POTENTIALLY_NOVEL at the idea level
- native value gate: FAIL / PARK
- do not reopen casually.

### B157

Source-faithful sparse-BFV functional bootstrap, security-valid depth32 point:
- N = 65,536
- Q depth = 32
- Q ~= 1650 bits
- P = 60 bits
- QP ~= 1710 bits
- HEStd_128_classic security passes
- native precision/performance fails
- candidate latency about 288.337 s
- matched baseline about 48.995 s
- shared powers + 8 LUTs about 259.09 s
- requires about 13.1x improvement merely to break even
- no local tuning.

### B158

ePrint 2026/975 sparse-BFV functional bootstrap candidate:
- co-pack growing power basis and current binary power into two hypercube halves
- target r=32768=2^15
- 15 ct×ct multiplications
- 14 RowRotations
- authors' baseline requires 28 multiplications for the relevant basis construction

Proof result:
- highest degree r-1 requires multiplicative depth ceil(log2(r-1)) = 15
- therefore B158 multiplication count is optimal under the ordinary arithmetic SIMD model

Status:
- algebra/proof/drop-in/special-output checks: PASS
- novelty: PROMISING_NOT_ESTABLISHED
- close conceptual prior art exists around rotate-multiply / IBM patent-style ideas
- native feasibility unresolved.

### B159-B161

Old k4 native failures are INVALID because RowRotation Galois key was underleveled:
- old row key L2
- actual first use L17.

### B162

Fixed row key:
- B158_ROW_KEY_LEVEL: L18
- FIRST_B158_ROW_USE_LEVEL: L17
- S2_MISMATCHES: 0/32768
- ROWROT_S2_MISMATCHES: 0/32768
- S2_NOISE_BUDGET: 560
- ROWROT_S2_NOISE_BUDGET: 560
- all tested RowRotations exact
- key-level bug is fixed

But hybrid selector schedule genuinely fails from noise:
- selector: Mul + Rescale
- fused step: MulRelinScaleInvariantNew
- no fused Rescale
- FIRST_FAILING_K: 1024
- FINAL_BASIS_CORRECT: no
- CTCT_COUNT: 10/15
- ROWROTATION_COUNT: 9/14
- failure explained by approximately 30-bit required-logQ growth plus approximately 34 bits Q lost per doubling

Decision:
    FAIL_NATIVE_NOISE_AFTER_KEY_FIX.

### B163

B163 is the corrected B160-style schedule:
- fixed L18 RowRotation key
- selector scale-one
- NO selector Rescale
- fused MulRelinScaleInvariantNew
- NO fused Rescale
- fixed source parameters/security point

STATUS:
    NOT RUN
    PENDING_CODEX_QUOTA

Do not infer B163 result from B162.

## Current paper-only priority

### Priority 1 — Ring-switch partial recovery / interaction-rank candidate

Finding:
    findings/boot-ring-switch-partial-recovery-gate-2026-10-28.md

Primary source target:
    Liang–Ding, ePrint 2026/1779
    "Bootstrapping via Ring Switching without Slot Recovery:
     Independent Leaf Evaluation for SIMD-Packed Ciphertexts"

Public abstract establishes:
- ring switching without conventional slot recovery
- CKKS and BGV/BFV independent leaf evaluation
- for unrestricted real CKKS inputs, continuous slotwise independent leaf evaluation iff affine

Full text is currently missing and is registered in MISSING_SOURCES.md.

New model-level theorem derived in BOOT:

For a two-leaf nondegenerate linear mix
    x = alpha*u + beta*v
and polynomial p of degree d>=2 over characteristic 0 or >d,

after removing all purely local u-only and v-only terms, the mixed polynomial has exact separation/interactions rank

    r_int = d - 1.

The proof identifies the mixed coefficient matrix
    C_{i,j}
      = c_{i+j} binom(i+j,i) alpha^i beta^j
and shows, after column reversal, a triangular matrix with nonzero diagonal induced by the leading degree-d term.

Consequences:
- affine d=1: 0 cross channels
- quadratic: exactly 1 cross statistic, uv
- cubic: exactly 2
- degree d: exactly d-1 in this two-leaf polynomial model

Research hypothesis:
instead of full slot recovery after ring switching, exchange only the minimum cross-leaf sufficient statistics required by a low-interaction-rank nonlinearity.

Cheapest decisive scheme gate:
1. obtain 2026/1779 full text;
2. recover exact leaf linear map and conventional recovery operation;
3. instantiate p(x)=x^2 first;
4. compare:
       full slot recovery + x^2
   vs
       leaf-local u^2/v^2 + one uv cross statistic;
5. PARK immediately if one uv channel costs essentially the same as full recovery or requires restoring the full parent representation;
6. continue only if one cross statistic stays materially cheaper in smaller rings.

Status:
    MODEL_THEOREM: PASS
    SCHEME_COMPATIBILITY: UNKNOWN
    VALUE: UNKNOWN
    NOVELTY: NOT_ESTABLISHED
    CURRENT_PAPER_PRIORITY: HIGHEST

### Priority 2 — Lossy key switching before exact error bootstrap

Finding:
    findings/boot-error-bootstrap-lossy-ks-gate-2026-10-28.md

Primary source target:
    Chartier–Lemou, ePrint 2026/2630
    "Exact Error Bootstrapping and Comb Bootstrapping in FHEW/TFHE"

Public abstract:
- bootstraps error instead of message
- exact error removal
- comb refresh for several ciphertexts
- modular additions/multiplications can happen between refreshes
- arbitrary functional PBS is NOT free / still needs programmable bootstrapping

Full text is missing and registered in MISSING_SOURCES.md.

Scheme-independent residual bound:

If approximate key switching leaves coefficient residual
    |rho_i| <= eps
and the source secret has at most h nonzero coordinates with |s_i|<=S,

then
    |e_res| <= h S eps.

For base-B, l-digit centered truncation,
    eps approximately <= q/(2 B^l)

so
    |e_res| approximately <= h S q/(2 B^l).

Ordinary post-KS decryptability roughly requires
    B^l > h S p

for plaintext modulus p.

If error bootstrap tolerates pre-refresh error E_boot, candidate condition becomes
    B^l > h S q/(2 E_boot).

Research hypothesis:
deliberately use fewer KS gadget digits / coarser KS and let the following exact error bootstrap absorb the larger residual.

Decisive value test:
    key bytes/work saved by l -> l-1 or l-2
        versus
    larger ring/error-domain cost required by the bigger recoverable error support.

PARK if cost is merely moved downstream.

Status:
    RESIDUAL_BOUND: PASS
    2630_COMPATIBILITY: UNKNOWN
    END_TO_END_GAIN: UNKNOWN
    NOVELTY: NOT_ESTABLISHED
    PRIORITY: LOW-MEDIUM / below 1779

## Important lines closed / parked in this session

### Generic Descent-PBS × MVB

Findings:
- findings/boot-post-B162-structural-scout-descent-mvm-2026-10-28.md
- findings/boot-post-B162-descent-mvb-gate1-coefficient-projection-no-go-2026-10-28.md
- findings/boot-post-B162-descent-mvb-gate2-carrier-rank-correction-2026-10-28.md
- findings/boot-post-B162-descent-mvb-gate3-prior-art-closure-2026-10-28.md

Important corrections/results:
- the original DB_f = B~_f D commutation gate was too strong as the main composition question
- MVB already shares a function-independent blind rotation before function-specific public multipliers
- one descended N-dimensional ring carrier followed only by public multiplication + fixed linear extraction spans at most an N-dimensional function space
- arbitrary t-entry LUTs with t>N cannot be represented by that direct carrier
- generic multi-output / shared-prefix FBS is heavily covered by CIM19 MVB, FDFB2, LFBS, and 2026 MVB works

Decision:
    GENERIC_DESCENT_PLUS_MVB: PARK / PRIOR_ART_CROWDED.

Only reopen if exact 2026/2616 reveals a genuinely Descent-specific maximal shared prefix / asymptotic module-stage or key-memory win.

ePrint 2026/2616 full text is missing and registered.

### Fast/shallow / Binary-NTT generic continuation

Finding:
    findings/boot-post-B162-fast-shallow-1730-residual-gates-2026-10-28.md

CRYPTO 2026 / ePrint 2026/1730 already reports:
- sparse-secret bootstrapping work reduction
- Binary NTT RLWE
- only 3 sequential NTT/INTT layers
- comparable total word operations to standard FHEW/TFHE

Generic "remove more sequential NTT depth" is closed.

Sparse + shallow/NTT-free is also crowded by later sparse-key compiler work.

Only potential source-gated residuals:
- Binary-NTT-specific sparse composition if nontrivial
- Binary-NTT-specific key-traffic bottleneck

Priority:
    LOW / SOURCE_GATED.
ePrint 2026/1730 full text is missing and registered.

### Final KSK elimination via secret relation

Finding:
    findings/boot-KSK-linear-embedding-gate-2026-10-28.md

Algebraic lemma:
if ring-secret coefficient vector t = T s for public T and sample extraction gives LWE mask a under t, then public mask projection
    a' = T^T a
returns the ciphertext under s with no KSK/no added noise.

But:
- T=I same-secret omission is old (Micciancio–Sorrell 2018)
- zero-padded target secret is explicit prior art
- modern 2025 NTRU baseline already reduces final KSK to about 5.25 KB vs BRK about 3.45 MB
- deleting the KSK saves only about 0.15% key bytes
- setting blind-rotation secret itself to T s creates harder related-secret / low-dimensional secret security issues

Decision:
    ALGEBRA PASS
    VALUE FAIL
    PARK.

### Dense blind-rotation key family reduction

Finding:
    findings/boot-BRK-family-gate-2026-10-28.md

Model-level no-go:
for dense binary block s_i, exact blind-rotation block multiplier
    product_i (1+s_i(X^{a_i}-1))
contains higher-order products s_i s_j, ...
A single selector obtained by public affine combination of per-coordinate EVKs cannot reproduce those terms.

Boolean second finite difference:
    Delta_i Delta_j F(0)
      = (X^{a_i}-1)(X^{a_j}-1)
is generally nonzero,
whereas every affine selector has zero second difference.

Existing escape routes are all prior art:
- block-binary keys: cross terms vanish by secret support restriction
- sparse/partial/shared-randomness keys
- Bootstrapping Key Unrolling: enumerate block states
- LFHE packing/reconstruction: compress transmitted unrolled keys
- NTRU-specific BKU
- ePrint 2025/2311: NTRU block binary/ternary + unrolling, external products down to n/l or n/(2l)

Decision:
    GENERIC_DENSE_BRF_FAMILY_REDUCTION: PARK.

### Free-XOR / headroom removal

Finding:
    findings/boot-free-xor-negacyclic-gate-2026-10-28.md

New lower bound:

For additive free-XOR logical decoding
    pi:M -> F_2,
pi is a group homomorphism and therefore
    pi(-m)=pi(m).

Standard negacyclic PBS satisfies
    F(t+N)=-F(t),

hence logical outputs obey
    pi(F(t+N))=pi(F(t)).

If all four binary input states occupy active LUT indices with no unused/padding half-domain, each negacyclic pair must have the same Boolean output.

AND has output multiset {0,0,0,1}, so no such pairing exists.

Decision:
    free-XOR + no padding + one standard PBS AND: IMPOSSIBLE in this model.

Generic ESOP/XAG encoding-switch circuit optimization is also prior art (ICCAD 2025 Encoding Strategy Management for TFHE).

Do not spend cycles on:
- removing padding while keeping the same additive free-XOR + standard negacyclic PBS model
- generic ESOP/free-XOR compiler work
- merely extending the direct symmetric gate table to all 16 binary gates.

### SampleExtract / key-return fusion

Finding:
    findings/boot-extract-keyreturn-closure-2026-10-28.md

TFHE functional key switching already evaluates arbitrary public/private linear morphisms while switching keys and can move between scalar/polynomial message spaces.

Modern NTRU bootstrapping also already moves key return into the ring/NTRU domain before SampleExtract.

SampleExtract itself is a public linear rearrangement and fusing it with the KS loop does not remove the secret-dependent gadget decomposition.

Decision:
    SAMPLEEXTRACT_PLUS_KEYSWITCH_FUSION:
        PRIOR_ART / IMPLEMENTATION-ONLY
        PARK.

## Other fresh closures / warnings

### CI-CKKS representation conversion

ePrint 2026/2618 directly addresses native conjugate-invariant CKKS bootstrapping without converting to standard CKKS.

Therefore broad
    CI -> standard -> bootstrap -> CI
conversion-elimination is already current prior art.

Do not pursue generic "absorb CI conversion into bootstrap" as a new idea.

### O(1) / ALU bootstrap fusion

2026 already has multiple active ALU / O(1)-bootstrapping directions, including REFHE and ePrint 2026/1840 / 1869.

Generic "fuse many ALU refreshes into O(1) bootstraps" is crowded.

Do not elevate without a very specific unexplored structural theorem.

### CKKS <10ms / ePrint 2026/2119

Potentially relevant to stage-fusion principles, but current full text could not be acquired through the research pipeline.

Not high enough priority to add as an active missing-source blocker.

## Missing critical sources

MISSING_SOURCES.md now contains at least the following BOOT-relevant blockers:

1. ePrint 2026/1779 — ring switching without slot recovery
   Highest current paper priority.

2. ePrint 2026/2630 — exact error bootstrapping
   Second current paper candidate.

3. ePrint 2026/2616 — Descent-PBS
   Needed only if Descent-specific multi-output line is reopened.

4. ePrint 2026/1730 — CRYPTO 2026 fast/shallow bootstrapping
   Needed only for Binary-NTT-specific residual gates.

5. ePrint 2026/2332 — Rotate Once, Read Many Times / MVB noise
   Needed only for theorem-level comparison if MVB line is reopened.

Do not pretend to have read these full papers until the research MCP says READY or the PI supplies PDFs.

## Immediate next research policy while Codex remains unavailable

Do NOT:
- run B163;
- launch any native experiment;
- reopen generic BRK compression/unrolling;
- reopen generic MVB;
- do free-XOR compiler tuning;
- do generic NTT micro-optimization;
- invent results from missing PDFs.

Preferred order:

1. If PI supplies ePrint 2026/1779:
   run RING_SWITCH_PARTIAL_RECOVERY_GATE_2 immediately.

2. Else if PI supplies ePrint 2026/2630:
   run lossy-KS / exact-error-bootstrap symbolic cost gate.

3. Otherwise:
   continue fresh BOOT structural scouting only for ideas that:
   - remove an entire stage,
   - merge stages in a way that removes secret-dependent work/key material,
   - or change representation/object so a previously mandatory bootstrap operation disappears.

Kill early if:
- only a constant-factor implementation fusion,
- already standard functional KS,
- only compression/transmission saving,
- only sparse/block secret variation,
- only MVB/multi-output amortization,
- or already covered by 2025-2026 direct prior art.

## GitHub workflow

Repository:
    BBBINGW/memory

Use the GitHub Notes connector that has verified read/write access.

Always:
1. read the latest BOOT handoff and relevant findings before new work;
2. do source/prior-art/algebra gate;
3. save substantive results under findings/boot-*.md;
4. write conservative labels:
       PASS / FAIL / PARK / UNCLEAR /
       PROMISING_NOT_ESTABLISHED /
       SOURCE_GATED
5. read back / verify the new file after write;
6. update a handoff when the conversation approaches its limit.

Do not modify other research tracks.

## First files to read in a new conversation

Read these first:

1. findings/boot-HANDOFF-post-structural-scout-2026-10-28.md
2. findings/boot-HANDOFF-post-B162-B163-pending-2026-10-28.md
3. findings/boot-ring-switch-partial-recovery-gate-2026-10-28.md
4. findings/boot-error-bootstrap-lossy-ks-gate-2026-10-28.md
5. findings/boot-B158-formal-recurrence-optimality-prior-art-2026-10-28.md
6. findings/boot-B162-native-artifact-audit-2026-10-28.md
7. MISSING_SOURCES.md

Then continue BOOT only.

## Resume sentence

"Resume BOOT from post-structural-scout handoff. B162 is the latest completed native audit; B163 is NOT RUN and pending Codex quota. While Codex remains unavailable, prioritize the 2026/1779 partial-recovery interaction-rank source gate, then the 2026/2630 lossy-KS/error-bootstrap gate, and otherwise continue only high-bar structural BOOT scouting. Read GitHub before writing and persist every substantive conclusion."
