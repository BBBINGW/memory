# PURE-FHE P0-PRESCOUT-21 — Nonunit GCKKS CKKS->GCKKS conversion modulo-lift gate

- Date: 2026-10-26 Asia/Hong_Kong
- TRACK_ID: PURE-FHE
- PREVIOUS: P0-PRESCOUT-20
- PRIMARY_HYPOTHESIS H21: A valid ciphertext modulo Q is *by itself* sufficient for Algorithm 1 (ePrint 2026/2600) to convert its two RLWE components separately into GCKKS with nonunit factor F, preserving useful-slot values and resetting unused slots to bounded rounding noise.
- MINIMAL_TEST: N=8 exact negacyclic algebra and independent high-precision CRT re-encoding, comparing a satisfying instance and a modularly valid but non-small integer-lift instance.
- STATUS: FAIL_UNCONDITIONAL_MOD_Q_CONVERSION; PASS_PAPER_LEMMA3_CONDITIONAL
- NOVELTY: NOT_ESTABLISHED; NOT_A_VERIFIED_BUG_IN_PAPER
- CODEX: NOT_RUN
- OTHER_TRACKS: UNCHANGED

## [FACT] Source and statement

User-supplied primary PDF papers/supplied/2026-2600.pdf SHA 8db712155d087284d21e924623496bc48e36eb72. Ma, Liu, Wang, Wang, *High-precision Bootstrapping for GCKKS*, draft October 22, 2026. Physical PDF p18 §5.1 stage 2 explicitly balances components modulo small q and lifts them to Q >> q; decrypts as m+qI, ||I||∞≤15 with overwhelming probability under encapsulated sparse-key h=32. Stage 8 re-encodes the mod-raised components into GCKKS. Physical pp24–25 §5.4 Algorithm1/Lemma3 give CRT useful-slot projection, multiplication by c_m^-1, rounding each RLWE component and using F as target decryption factor. Lemma condition is ||b+as||_2+||eF||∞ < Q/2, and concludes at useful slots new-old = c_m τ_useful(e), unused slots new = τ_unused(eF). The printed proof relies on the *unreduced* polynomial (B'+A's)F agreeing with the chosen input lift on useful slots and being zero on unused. p26 says Implementation: Not available yet. These are primary document claims, not native validation.
The norm convention needs to distinguish an unreduced integer lift of b+as from its centered reduction in R_Q. Counterexample to unconditional applicability does not refute conditional Lemma3.

## [DERIVATION] Exact N=8 nonunit toy

R=Z[X]/(X^8+1), k=8, ζ=e^(π i/8), canonical slots exponents 1,5,9,13. Useful exponents 1,9; unused 5,13. F=3+X²−X⁶, F_useful=c_m=3+sqrt(2), F_unused=3−sqrt(2). Ring norm (c_m(3−sqrt2))^4=7^4=2401, so F is NOT a unit.

For a real polynomial U, ideal CRT projection and scale before rounding can be written E U/c_m modulo X^8+1, where
E=(1 + (X²−X⁶)/sqrt(2))/2.
It has embedding 1 on useful and 0 on unused. Let b*=round_coefficient(E b/c_m), a*=round_coefficient(E a/c_m), e=(b*−E b/c_m)+(a*−E a/c_m)s. This exactly models Alg1 (negacyclic algebra over R, real CRT and nearest integer rounding).

PASS instance: Q=257, s=1+X, b=8−3X+5X², a=−5+6X+2X².
Source b+as=3−2X+13X²+2X³, norm sqrt(186)=13.638181696986.
Rounded outputs b*=1+X²−X⁶, a*=X.
D*=(b*+a*s)F=6+3X+7X²+X³+X⁴−4X⁶−X⁷.
Exact symbolic evaluation: at useful embeddings D*−(b+as)=c_m e; unused embeddings D*=F e.
||eF||∞≈3.59619408; sqrt(186)+3.5962<257/2. Conditional theorem verified in this toy. Independent symbolic coefficients and numerical embeddings agree to ~1e-14.

FAIL unconditional modular-only assertion: Q=1009, s=1+X, a=400+400X, b=−400+209X−400X². Then unreduced b+as=1009X but valid centered decryption is 0 mod Q. Same conversion produces
 D*=(b*+a*s)F=504X+357X³−357X⁷,
which already has all coefficients in [−Q/2,Q/2]; at each useful embedding magnitude ≈1008.874..., NOT close to zero. Rounding contribution ||eF||∞=0.5, so the large discrepancy is the deleted QX lift after non-Z_Q-linear CRT projection, not approximation error. This demonstrates that ordinary modular decryption correctness alone does not imply Alg1's useful-slot semantics. Here ||b+as||_2=1009>Q/2, so the printed sufficient hypothesis FAILS. It is therefore NOT a counterexample to the printed conditional lemma. If the lemma's norm is instead interpreted solely on the centered modular decryption residue (zero), then this reveals a necessary clarification/ambiguity in the norm/lift semantics, but do not claim a verified flaw without explicit author clarification/implementation audit.

## [DERIVATION] Why author-specific ModRaise can pass and a conservative margin

Paper p18 stage2 reduces b,a to balanced representatives modulo small q, then lifts to Q >> q and gets b+as=m+qI with |I_i|≤K_I (typically K_I=15 with high probability under paper model). For this chosen small integer lift:
||b+as||_2 ≤ sqrt(N)(||m||∞+q K_I).
Rounding errors of each CRT-lifted component are coefficientwise ≤1/2. For s∈R, F∈R, negacyclic product norm inequality gives ||eF||∞ ≤ (1/2)(1+||s||_1)||F||_1.
Consequently a sufficient (conservative) easy-to-audit certificate for Lemma3 is
  Q > 2 sqrt(N)(||m||∞+q K_I) + (1+||s||_1)||F||_1.
This bound is not in the original Lemma as written and is a straightforward new derivation from it, NOT a new FHE mechanism/security result; tighter actual parameters may pass with smaller Q.
Illustration only: N=2^16, K_I=15, ||m||∞≤q/16 and ||s||_1≤32 yields
 Q/q > 7712 + 33||F||_1/q, where log2(7712)≈12.91.
This is a *sufficient* headroom condition under stated bounds, not a measured GCKKS cost or an author parameter quote. Noise tails and actual F norm must be supplied for a meaningful parameter certificate.

## [FACT] Contemporary competing work

Dumezy, ePrint 2026/2513, shaped rounding for small batches with native poulpy bootstrapping and shared-key CKKS conversions (author page https://jdumezy.com/publications/new-scheme/ ; retrieved abstract, NOT original full-text).
Cheon–Lee, ePrint 2026/2531, Focused CKKS using focal cyclotomic units and tailored bootstrap (ePrint index, only abstract verified); https://eprint.iacr.org/2026/2531.
These overlap slot sacrifice / precision focusing and limit novelty of proposing public factor F / slot-aware conversion generically. Do not claim either solves every GCKKS nonunit conversion case.

## Result and next test

H21 FAIL unconditionally but published conditional theorem passes. The counterexample is an input-lift/scope gate, NOT a flaw demonstrated for the p18 small-q ModRaise workflow. Need test author's ACTUAL parameter path: bound Q/q and ||F||_1, secret norm, ||I||∞/noise probability; ensure headroom in both high-precision and sparse/large-F regimes. Also inspect whether source p26 no implementation means favorable big-O costs may hide peak ciphertext/evaluation-key cost; prior author Dumezy has native compared on some workloads.

END_ITERATION:
STATUS: PASS_CONDITIONAL_ALGEBRA_AND_FAIL_UNCONDITIONAL_LIFT
RESULT: no paper contradiction under its stated assumption; explicit toy, conservative modulus-headroom inequality
NEXT_TEST: GCKKS_2600_STAGE2_PARAMETER_HEADROOM_AND_PEAK_CIPHERTEXT_GATE
STATE_UPDATE: YES single isolated finding only; no global STATE.md change.
