# BOOT / Turn 10/25 — full-text theorem/interface gate for n=2 focal-window parallel sign

Date: 2026-11-09, Asia/Singapore
TRACK_ID: BOOT
RESEARCH_TURN: 10/25 (same logical turn after failed chat surface; count once)
PHASE: PROBLEM_SELECTION
POLICY: paper-first-runtime-v3
CANDIDATE_ID: focal-window-parallel-sign-n2-p42-v1
RANK: 1
PRE_TEST_STATUS: ACTIVE
POST_TEST_DECISION: FAIL_FIXED_PILOT_PROOF_GATE / PARK_N2_P42_V1
EVIDENCE_LEVEL: SOURCE_FULL_TEXT_AUDITED + STATIC_DERIVATION (NOT a native execution, NOT a probabilistic experiment)
NATIVE: pending Codex task / UNKNOWN / BACKGROUND_ONLY / DO_NOT_RERUN / UNTOUCHED
R7: BOUNDED_NO_GO / TERMINAL / NOT_REOPENED
DECISION_CHANGED: true
ELIMINATED_UNCERTAINTY: Whether the 2531 focal framework contains an operator-rounding theorem, and whether its k=2 scale-constrained guarantee certifies the specified 26-bit/47.033-bit fixed pilot without conversion.

## Pre-test decision contract

QUESTION: Does the formal focal-unit encoding/precision theorem of ePrint 2026/2531 bound plaintext S2C/diagonal/multiplication operator quantization below 2^-47.0332028 for N=2^15, Delta=2^26, k=n=2, while preserving all 2368 operations without an unaccounted focus conversion?

CURRENT_BELIEF: Full text not previously verified; the abstract's k-fold precision slogan is insufficient; hard risks are plaintext-operator quantization, coefficient/slot boundary, and padded window layout.

CHEAPEST_DECISIVE_TEST: Read both public full texts, specialize 2531's formal rounding norm, Corollary 1 and Lemmas 7–8 and S2C layout to k=2/Delta=2^26; compare 2368 Algorithm 1 FormWindows and prefix scan/slot layout. No implementation/native task.

IF_PASS: Continue source-faithful composition to exact correctness gate.
IF_FAIL: PARK this exact n=2/p=42 fixed pilot; do not benchmark.
IF_UNCLEAR: Record a precisely missing theorem/parameter premise; no PASS or inferred result.
WHICH_PAPER_GATE_CHANGES: PROBLEM_SELECTION viability; candidate CORRECTNESS_GATE remains not passed, other gates pending.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: It determines whether another proof/implementation of this paper thesis has expected value or merely reproduces a known precision/scale obstruction.

## Primary evidence and locations — verified 2026-11-09

A. Jung Hee Cheon, Junho Lee, *High-Precision CKKS with Focal Units*, ePrint 2026/2531, 42-page public PDF:
https://eprint.iacr.asia/2026/2531.pdf
- physical page 8 (PDF index 7): Lemma 1, coefficient rounding: hard canonical error bound N/2; under independent uniform fractional coefficients high-probability Ernd=6 sqrt(N/12).
- physical page 3 (index 2): overview's two constraints Delta >= ||u||can_inf E and focus decoded error |sigma_F(u)| E / Delta; unit norm and 1/k focus fraction imply ideal p=k p0 with p0=log2 Delta-log2 E.
- physical page 16 (index 15): Table 1 concrete k=2 unit gain/overhead pairs; indicates actual integral-unit overhead not magically zero.
- physical pages 17–18 (indices 16–17): Definition 6 Ecd^[u](m;Delta)=u * round(u^-1 Delta m), Proposition 4, Proposition 6 and Corollary 1. Plaintext encoding errors ARE focused, contrary to a blanket statement that the theorem excludes them.
- physical page 22 (index 21): Lemma 7 *Focused linear transformation in each coset*, with plaintext diagonals Ecd^[u] and fresh rounding term. Its displayed high-probability error norm is bounded by
  ||e'||can_inf <= d (alpha + ||u||can_inf Ernd/Delta)(||e||can_inf+E_KS) + d ||v||inf Ernd + E_RS,
  where d=N/(2k). The syntax in source typesetting places parentheses around (||e||+E_KS).
- physical page 23 (index 22): Lemma 8 focused polynomial evaluation, using Delta >= ||u||can_inf E_fresh, plus input magnitude and circuit-dependent constant.
- physical pages 24–28 (indices 23–27): focused bootstrapping, focus/coset rotation restriction; Section 5.3 Interleave/Deinterleave converts shaped-error focus into all-slots ordinary error at *different* scale u_F^-1 Delta; Section 5.4 states S2C goes focused Delta -> coefficient-encoded ordinary error at u_F^-1 Delta. Lemma 9 and Section 5.5 implement the conversion through dedicated interfaces. Therefore "unchanged 2368 operator with no hidden conversion" is not proved by Lemma 7.
- physical pages 34–39: Section 6 optional discrete-CKKS focused cleaning-based bootstrapping also has conversions/extra work and is a different algorithm.

B. *Low-Latency Parallel Digit Decomposition and Sign Evaluation for CKKS*, ePrint 2026/2368, 22-page public PDF:
https://eprint.iacr.asia/2026/2368.pdf
- physical pages 6–7 (indices 5–6): Section 3.1 uses Lambda=2^ceil(log2(u+1)) positions per logical input (digit slots + **padding**), and M=N/(2 Lambda) ordinary layout; Algorithm 1 FormWindows is StC -> coefficient-domain F(X)*ct+S(X) -> rescale -> coefficient-wise Disc and key switch. These are not just slotwise focal polynomials.
- physical pages 9–12: Root_(B^2), lookup and prefix-scan rotations operate across padded window positions. Rotations preserve focal units only if the relocated index pattern respects 2531's coset stabilizer.

C. Internal earlier source/provenance, **not** newly executed:
BBBINGW/memory@main findings/boot-2368-b64-window-probabilistic-correctness-gate-2026-10-30.md, git blob c76c54464874689499e943d951d5a30561131711. It distinguishes deterministic B64/hwt32 failure from conditional 2^-56.906 source heuristic; not a correctness PASS for this new pilot.
Root STATE.md when inspected has old B158/RMFE content and no matching 2026/2531 focal candidate; treat it as stale for this PI-supplied continuation. Do not overwrite it without reconcile. The failed chat surface contributes zero evidence/turn counts.

## Calculation, k=2 and N=2^15

[FACT] For Lemma 1's high-probability IID-uniform rounding model:
N=32768;
E_rnd = 6 sqrt(N/12) = 313.53468707624677;
log2(E_rnd) = 8.292481250360577.

[DERIVED, under the fixed pilot interpretation that the ordinary "26-bit S2C plaintext diagonal quantization" means plaintext encoding Delta=2^26] Let p0=log2(Delta/E_rnd)=17.707518749639423. A k=2 focal unit with equal-size single focus and background cosets has |u_F|*|u_B|=1 by the norm-one condition and equal multiplicity. Writing H=log2||u||can_inf= -log2|u_F| in this two-coset setting, the source's scale stability constraint Delta>=||u||can_inf E_rnd implies H<=p0. Therefore the *optimistic single-stage* focus precision certificate is no more than
-log2(|u_F| E_rnd/Delta) = p0+H <= 2p0 = 35.415037499278846 bits.
This is an optimistic theorem-envelope bound, **not** a lower bound on actual rounding noise, not a black-box impossibility of CKKS, and not a claim about special coefficients with exact representations. Importantly, the full Lemma 7 d*||v||*E_rnd and key switching/rescale costs are nonnegative and normally worsen this envelope, not improve it.

[DERIVED] Target p_target=47.0332028 bits is 11.618165300721152 bits above this optimistic certificate. The earlier 21.6885-bit S2C deficit also exceeds the permitted focal attenuation H<=17.7075187496 by 3.98098125036058 bits. Even for an isolated focused scalar error, log2 Delta would need at least
p_target/2 + log2 E_rnd = 31.809082650360576,
*before* including actual linear transform dimension, input norm and key switching. For attenuation of the claimed 21.6885-bit deficit alone, the scale feasibility condition would require log2 Delta >= 29.98098125036058.

[OPEN/CONDITION] If "26-bit S2C" meant only *measured effective precision* at a different physical Delta, rather than Delta=2^26, the numeric bound above must be recalculated with the actual Delta and error norms. No evidence from the original user packet authorizes claiming otherwise. Independently of this ambiguity, the direct drop-in composition lacks a theorem for preserving focused representation through 2368's coefficient domain without the explicit S2C conversion, and the slot-count argument below is unconditional on Delta.

## Physical capacity reconciliation

[FACT] 2368 Section 3.1: Lambda = 2^ceil(log2(u+1)).
[DERIVED] u=8 -> Lambda=16, **not 8**. At N=2^15, ordinary available CKKS slots are N/2=16384. 2531 k=2 makes at most 8192 focus slots. Without a separately proved padding-elimination/layout redesign, source-faithful 2368 needs 16 focus slots per logical input:
M_focused <= 8192/16 = **512**.
The previous 1024 target used (N/2)/(k*u) and ignored 2368's 8 extra padding positions. This is a correction of the pilot capacity claim, not evidence that 512 is useless.

## Interface/novelty boundary

[FACT] 2531 already gives focused plaintext encoding and focused *coset-local* linear transformations, as well as a tailored focused bootstrap. These are prior art and cannot be claimed as new. Section 5 states focus does not directly give coefficient accuracy, necessitating S2C/Interleave. 2368 Algorithm 1 applies StC first, then an integer coefficient fanout polynomial amplified by powers up to B^7=2^42, then its discretizer. Focused slotwise closure alone is not a proof that the coefficient branch inherits <2^-47.0332028 error.

[OPEN] No exact 2531+2368 sign composition verified in the bounded audit; NOVELTY_STATUS stays PREFLIGHT, not PASS and not an asserted collision. The 2531 paper's existing generic focused S2C and focused-polynomial technology consumes much of the generic delta.

## Final Turn 10 assessment / decision

VERDICT = FAIL_FIXED_PILOT_PROOF_GATE / PARK_N2_P42_V1.
ELIMINATED_UNCERTAINTY = OPERATOR_ROUNDING_SOURCE_SCOPE_AND_N2_SCALE_CAPACITY_BOUND.
DECISION_CHANGED = true: source verification answered a genuine paper-level feasibility question and corrected physical capacity (1024 -> 512). Do not run native canary or benchmark for n2/Delta=2^26. The default next BOOT turn is **PROBLEM_SELECTION**, starting from an actually viable source-backed mechanism/parameter regime, with exactly one chosen ACTIVE candidate only after preflight; do not fabricate a new viable candidate from this negative result.
CORRECTNESS_GATE = PENDING (pilot not certified, negative feasibility gate only)
SECURITY_GATE = PENDING
VALUE_GATE = PENDING
AUDIT_GATE = PENDING
BASELINE_CORRECTNESS = PENDING
NOVELTY_STATUS = PREFLIGHT
PAPER_READINESS = NOT_READY
PERFORMANCE_CLAIM = false
REOPEN_CONDITION = A separately specified actual Delta/operator coefficient bound and source-faithful coefficient-domain conversion/quantization proof that beats 2^-47.0332028, plus a corrected Lambda=16 capacity/value case. Changing scale alone is not an original algorithmic contribution.
NEXT_DECISIVE_TEST = **DO NOT** repeat this n2 fixed pilot; select at most one different BOOT paper candidate only after an upfront paper-level baseline/value and closest-prior-art comparison. Do not reopen R7 or touch native task.
EVIDENCE_REFS = ["https://eprint.iacr.asia/2026/2531.pdf#page=3", "https://eprint.iacr.asia/2026/2531.pdf#page=8", "https://eprint.iacr.asia/2026/2531.pdf#page=22", "https://eprint.iacr.asia/2026/2531.pdf#page=26", "https://eprint.iacr.asia/2026/2368.pdf#page=6", "https://eprint.iacr.asia/2026/2368.pdf#page=7", "BBBINGW/memory/findings/boot-2368-b64-window-probabilistic-correctness-gate-2026-10-30.md@c76c54464874689499e943d951d5a30561131711"]

No information from background task inferred. R7 BOUNDED_NO_GO remains terminal. Current research turn 10 counts once on verification of this durable result.
