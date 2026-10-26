# PURE-FHE · P0-PRESCOUT-24 — Integer mask resultant / old-guard budget

Date: 2026-10-26 (Asia/Singapore)
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: GCKKS_HIGH_PRECISION_BOOTSTRAPPING
PREVIOUS: P0-PRESCOUT-23 (isolated finding: pure-fhe-p0-gckks2600-shared-power-two-level-mask-rounding-gate-2026-10-26.md)
STATUS: PASS_CONDITIONAL_CYCLOTOMIC_NORM_OBSTRUCTION / FAIL_UNIVERSAL_NOGO_INFERENCE / UNCLEAR_TWO_LEVEL_EXISTENCE
NOVELTY: NOT_ESTABLISHED
CODEX: NOT_RUN; NO GPU/NATIVE
OTHER_TRACKS: UNCHANGED

## Source / prior-art provenance

[FACT] papers/supplied/2026-2600.pdf SHA 8db712155d087284d21e924623496bc48e36eb72, original physical pp14–17,19–21: shared h1(x)=3x²−2x³ powers under F², branch masks encoded as F² round(L'_i), factor change F²→F', final divisor Δ³ (source baseline three scale-dependent layers). Source §4.1–4.3 demands bound |d_out(ξ)|/|F'(ξ)|≤K at unused slots and lower bound ρ≥max(1,r c_e). Newly discarded useful slots have different input magnitude from already-unused slots.
[FACT] Original Focused CKKS revision ePrint2026/2531 by Cheon–Junho Lee dated Oct20 2026 appears in current public index, but full PDF NOT PRESENT under papers/supplied and publicly requested file inaccessible. ePrint abstract confirms focused cyclotomic-unit arithmetic and tailored bootstrapping, NOT full §6. The 2-level split-first characterization comes only from 2600 p5–6 (SECONDARY). Dumezy 2026/2513's first-party author blog discusses shaping rounding errors into guard slots; its exact PDF remains not independently audited. Novelty is BLOCKED without these sources.

## Single minimal hypothesis H24

Within P0-23's specific template (shared power combination under F², then **one** integral polynomial branch mask M followed by F²→F' reinterpretation and one additional Δ-sized rescale), can an M with retained amplitude A=O(1) and pre-existing unused-slot amplitudes B_i=O(1) achieve new-discarded amplitude δ=O(1/Δ) at growing Δ?

## [DERIVATION] Exact cyclotomic integer norm obstruction

Take ring R=Z[X]/(X^8+1), ζ=exp(πi/8), canonical conjugate-pair representatives {1,9,5,13}. Let one retained old useful slot be ζ^1, the newly discarded old useful slot ζ^9, and two old unused slots ζ^5,ζ^13. For integer M∈R nonzero let
  A=|M(ζ^1)|, δ=|M(ζ^9)|, B1=|M(ζ^5)|, B2=|M(ζ^13)|.
Because X^8+1=Φ16 is irreducible over Q and M is a nonzero residue, Res(Φ16,M) is a nonzero integer, and conjugate pairing yields exactly
  |Res(Φ16,M)|=(A δ B1 B2)^2 >=1.
Therefore δ >=1/(A B1 B2), and if B1,B2<=B then δ>=1/(A B²).
In particular a **nonzero** integral selector cannot vanish at one primitive slot while retaining nonzero value at another. With fixed A and B, δ cannot shrink like 1/Δ.

[DERIVATION] From P0-23, the specified one-mask rewrite has factor-normalized new-unused contamination Δ² δ/ρ when bit input=1 and no other HE error; preserving K requires δ<=Kρ/Δ². For ρ=cΔ and A bounded, norm bound implies
  B >= sqrt(Δ/(A K c)).
Thus **if B=O(1)** is an imposed interface constraint as Δ grows, the two-level single-mask rewrite is impossible. This does NOT rule out masks that deliberately shift much larger amplitude into old unused slots, nor masks with precision-dependent A or multicomponent cancellations.

## [TOY_NUMERIC + EXACT] Reaudit previous P0-23 projector

For the previous rounded selector M=1+X+X²−X^6−X^7, an exact symbolic resultant computation (sympy resultant) gives
  Res(X^8+1,M)=1.
Direct canonical evaluations at exponents 1,9,5,13 give, up to negligible imaginary floating error:
  A=4.26197262739566856
  δ=0.56645449735052154
  B1=1.17958042710327459
  B2=0.35115330235708449.
Their product A*δ*B1*B2=1 (up to sign), so the prior example *saturates* this norm inequality: the leakage is not explained by a numerical implementation mistake.

Illustration ONLY (not real GCKKS parameters): let Δ=1024, ρ=3Δ, K=1, A<=5 and BOTH B_i<=2. Norm gives δ>=1/20=0.05 while required δ<=3/1024≈0.0029296875, impossible. Conversely the norm would merely require at least one old guard amplitude B>=sqrt(1024/(5*3))≈8.2624 when both are bounded equally; this is a necessary tradeoff, NOT evidence an integer mask achieving it exists.

## [DERIVATION] Why this is NOT a universal no-go; guard budget may scale

An already-unused slot ξ enters shared-power Y with factor F² and noisy normalized underlying value u_Y(ξ), while a newly discarded old-useful slot enters Y with message Δ². If |u_Y(ξ)|<=T_ξ and a_ξ=|F(ξ)|, after multiplication with F² M, reinterpretation as F', and divisor ρ, its post-conversion factor-normalized old-unused contribution is bounded by
  T_ξ a_ξ² |M(ξ)| / ρ
(ignoring other HE errors). A SUFFICIENT per-old-unused design envelope is
  |M(ξ)| <= Kρ/(T_ξ a_ξ²)
if T_ξ>0 and the full K budget is allocated to this contribution.
At ρ=Θ(Δ), that envelope may itself grow with Δ, permitting guard-amplitude growth necessary from the resultant inequality. Thus the algebraic norm gate DOES NOT rule out all 2-level masks; the mask could redirect error into old unused slots (a known conceptual principle in concurrent focused/shaped schemes). Actual amplitude/noise/parameter availability is unresolved, and the needed high-precision masking polynomial may incur enormous coefficients, modulus, RNS and key-switching/rotation cost.
No security, correctness or noise-proof PASS for a new scheme is established.

## Novelty / decision

Result is a mathematically exact *conditional* interface obstruction and sharper explanation of why naive rounded single-mask P0-23 failed. Not a new cryptographic construction or any author paper flaw. Its guard-amplitude escape is closely related to prior shaped/focused-slot tradeoffs; without 2026/2531 §6 do NOT claim originality.
Do not spawn more nearby synthetic toy masks. Next evidence gate requires primary 2531 revised Section 6 or explicit PI value/pivot; when accessible compare actual branch mask noise, scale, and whether F²→F' GCKKS nonunit case admits a new technique with end-to-end advantage.

END_OF_ITERATION:
STATUS: PASS_CONDITIONAL_NORM_BOUND / UNCLEAR_GENERAL_TWO_LEVEL_SOURCE_BLOCKED
RESULT: nonzero integer cyclotomic mask necessarily A δ B1 B2>=1; guard tradeoff B>=sqrt(Δ/(A K c)) under ρ=cΔ; exact prior projector unit norm confirmed; unrestricted two-level existence not falsified.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: Read the original revised ePrint 2026/2531 §6; determine whether its split-first cleaning already exploits growing old-unused guard budgets and whether any F²→F' compatible, two-level **new mechanism** remains. If PDF remains blocked, request supplied original / PI value review, NOT more ungrounded masks.
STATE_UPDATE: YES isolated PURE-FHE finding only, no shared STATE.md.
CODEX_REQUIRED: NO (PENDING only after a PI-approved real mechanism / implementation gate).
