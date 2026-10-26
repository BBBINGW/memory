# PURE-FHE · P0-PRESCOUT-23 — Shared-power two-level split: rounded-mask gate

Date: 2026-10-26 (Asia/Singapore)
TRACK_ID: PURE-FHE
PREVIOUS: P0-PRESCOUT-22 (handoff logs/pure-fhe-session-handoff-post-p0-prescout-22-2026-10-26.md)
SOURCE: papers/supplied/2026-2600.pdf, blob 8db712155d087284d21e924623496bc48e36eb72, pp5-6,13-17,19-21,24-25.
STATUS: FAIL_NAIVE_TWO_LEVEL_REALIGN_THEN_MASK / UNCLEAR_GENERAL_H23
NOVELTY: NOT_ESTABLISHED
EXPERIMENT: symbolic analysis + local elementary CRT-projector numerical check ONLY; no native FHE/Codex/GPU.

## [FACT] Source
Paper §5.2 pp19–21 shares c2 (factor F²) and c3 (factor F²) before splitting; h1(x)=3x²−2x³; it then multiplies by branch masks L2=F² round(L2') and L3=F² round(L3'), reinterprets F²→F', and rescales by Δ³. Paper explicitly counts 3 Δ-related levels. Lemma2 (§4.1, pp14–15) requires unused |Dec_F(c)(ξ)|≤K|F(ξ)|; valid divisors obey ρ≥max(1,r c_e), including post-conversion with c'_e. §4.3 p17 explains useful-to-unused slots must be zeroed by a rounded encoded mask before factor conversion. §4.2 p16 permits auxiliary H/extra HomPMult when the target useful scale falls beneath the unused-slot minimum divisor.
Paper p5–6 characterizes revised Focused CKKS (Cheon–Lee, ePrint 2026/2531, 2026-10-20) as split-first, child-wise cleaning, 2 levels, but this is SECONDARY, not verified from 2531 original full text. Authors p26 say native Implementation Not available yet.

## [DERIVATION] One-round two-useful/unused symbolic gate
Take two old useful slots u0,u1 both carrying bit 1, plus initially unused slot z carrying 0. Output branch 0 must keep u0, discard u1 (which becomes newly unused); branch 1 vice versa.
Proposed apparent 2-level rewrite: shared powers produce C2 with decoded Δ²x² and C3 with decoded Δ³x³, each under factor F²; first Rescale(C3,Δ), then Y=3C2−2 Rescale(C3,Δ) with decoded useful Δ²h1(x). For each branch e, multiply by integer mask F² round(λP_e) where P_e ideal CRT selection (1 retained; 0 discarded/unused), reinterpret factor F²→F', then rescale by ρ≈one Δ-sized divisor. Let r_e=round(λP_e)−λP_e, computed coefficientwise, and F'(retained)=c'_m. Desired Δ'h1 output requires
  λ = ρ Δ'/(Δ² c'_m).
At retained bit1, normalized useful error (ignoring all HE errors for the cheapest best-case test) is |r_e(retained)|/|λ|.
At newly discarded bit1, P_e(discarded)=0; the factor-normalized contamination is EXACTLY
  |dout(discarded)|/|F'(discarded)| = (Δ²/ρ)|r_e(discarded)|.
Thus constant K unused bound requires |r_e(discarded)|≤ Kρ/Δ². If ρ=Θ(Δ), the ordinary O(1) CRT integer-rounding envelope is insufficient; need selector embedding accuracy O(K/Δ) at discarded slots. Changing F²→F' alone cannot help because F' cancels in the normalized requirement. Enlarging ρ to Θ(Δ²) permits O(1) error under this best-case model, but then 1 prior Δ rescale plus 2 later Δ-levels = 3 levels, i.e. no saved level. This is a cost obstruction for the specified rounded-mask template, not a general impossibility theorem.

## [DERIVATION / TOY_NUMERIC] Exact 8-degree CRT projector counterexample
R=Z[X]/(X^8+1), ξ=e^(πi/8). Canonical representatives exponents 1,9,5,13; old useful=1,9; old unused=5,13. Branch0 retains1 and discards9. The *ideal* real projector P0 with values 1,0,0,0 on these pairs has coefficients p_j=(1/4)cos(jπ/8), j=0..7. Coefficientwise round(λP0) is the ZERO polynomial at λ=1 and 2, even destroying the retained useful bit.
At λ=3:
  Q0=round(3P0)=1+X+X²−X^6−X^7.
Direct evaluations:
  Q0(ξ^1)=4.261972627395668 (retained);
  Q0(ξ^9)=0.5664544973505213 (newly discarded);
  Q0(ξ^5)=−1.1795804271032746 (old unused);
  Q0(ξ^13)=0.3511533023570824 (old unused).
Diagnostic unit-factor special case F=F'=1, Δ=Δ'=1024, ρ=3072 (so λ=3): relative retained signal error |4.2619726274/3−1|=0.4206575425, and new-unused normalized leakage 1024*0.5664544974/3=193.3498018. Violates useful correctness and any fixed K<193.35 even when tensor/relin/keyswitch/rescale noises are set to zero. This is *not* an actual secure or high-precision GCKKS parameter set, and F=F'=1 does not establish real F²→F' high-precision feasibility or infeasibility. The preceding factor-normalized algebra gives the general interface issue.

## [FACT] Source gap
Public ePrint mirror index confirms 2026/2531 title/authors and Oct20 revision but original PDF is still SOURCE_BLOCKED (GitHub Notes eprint downloader: HTTP403; arXiv exact title and fixed GitHub mirror not found; web PDF inaccessible). 2026/2513 original full PDF likewise not independently verified. Do NOT claim independent knowledge of Focused §6 masks/noise or novelty.

## Decision
One tested rewrite (cubic Δ rescale + shared h1 + coefficientwise-rounded mask + one Δ-scale final rescale) FAILS the minimal algebra/rounding gate. Broad existential claim of a different 2-level shared-power-before-split construction remains UNCLEAR; no publishable contribution established. Do not claim a universal no-go or a flaw in 2026/2600. Do not run Codex.

END_OF_ITERATION:
STATUS: FAIL_NAIVE_TWO_LEVEL_MASK / UNCLEAR_GENERAL_H23_SOURCE_BLOCKED
RESULT: specific algebraic constraint and two-useful/unused explicit counterexample
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: obtain Cheon–Lee ePrint 2026/2531 dated 2026-10-20, read §6 original tree split, masks, scale and noise proof; then compare exactly to F²→F' GCKKS.
STATE_UPDATE: YES, isolated P0 finding only; global STATE.md untouched.
CODEX_REQUIRED: NO; eventual native work PENDING explicit PI approval.
