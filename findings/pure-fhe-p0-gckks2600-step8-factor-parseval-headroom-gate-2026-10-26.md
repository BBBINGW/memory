# PURE-FHE · P0-PRESCOUT-30 — Step8 nonunit CRT re-encoding: factor-norm / modulus-headroom gate

Date: 2026-10-26 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: GCKKS_HIGH_PRECISION_BOOTSTRAPPING
PREVIOUS: P0-PRESCOUT-29, findings/pure-fhe-p0-gckks2600-aks-bsgs-rescale-relaxation-kill-gate-2026-10-26.md, commit e179566d4d6d624d957b550517442e93bb02965c.
STATUS: PASS_CONDITIONAL_PARSeVAL_HEADROOM / FAIL_FORCED_NEW_PRECISION_OVERHEAD / REAL_PARAMETERS_UNCLEAR
NOVELTY: NOT_ESTABLISHED; elementary bound and condition check, no cryptographic construction
CODEX_REQUIRED: NO; NO GPU/NATIVE/REMOTE or repo infrastructure changes
OTHER_TRACKS: UNCHANGED; global STATE.md untouched

## One primary falsifiable H30

After excluding two-level shared-power and generic AKS Step7, does the nonunit Step8 CKKS→GCKKS CRT component re-encoding *necessarily* force a new precision-growing Q/q modulus headroom, due to unaccounted coefficientwise rounding multiplied by F, thus defeating §5.5's precision-dependent O(p log k/k) cost claim?

Cheapest decisive test: use GCKKS's own restricted subring structure to express the unknown coefficient l1 norm of F in terms of canonical useful/unused magnitudes c_m and c_e; substitute into Step8's published conditional correctness criterion and evaluate a transparently **conditional** high-N parameter region. No new parameter generation, numerical BKZ, or native encryption.

## Primary sources and important existing record

[FACT] User-supplied Ma–Liu–Wang–Wang *High-precision Bootstrapping for GCKKS*, ePrint 2026/2600, papers/supplied/2026-2600.pdf SHA 8db712155d087284d21e924623496bc48e36eb72. Newly re-read original physical pp3–7,9–12,15–19,24–26:
- §2.3 p7: F in Z[X^(2N/k)]/(X^N+1); let Y=X^(2N/k), n=k/2, F in Z[Y]/(Y^n+1). One useful canonical conjugate pair with common F=c_m and remaining n/2−1 unused conjugate pairs bounded by c_e.
- §3 p10–12: for w<1 author heuristics: useful c_m=O(w^(1−4/k)), unused c_e=O(w^(−4/k)) with fixed k/BKZ quality. Heuristics are NOT worst-case rigorous factor bounds for realized F.
- §4 pp14–16: normalized unused-slot invariant and scale ρ≥r c_e.
- §5.1 p18: Step2 balances both small-q CKKS RLWE components and reinterprets at Q≫q; source asserts b+as=m+qI with ||I||inf≤15 with overwhelming probability under sparse secret encapsulation h=32. This is a special centered integral-lift path, not arbitrary input residues mod Q.
- §5.4 pp24–25 Algorithm1 / Lemma3: projected CRT lift/round input components independently and use target nonunit F factor; requires ||b+as||2+||eF||inf<Q/2. If valid, output useful error is c_m τ_useful(e) and unused error eF.
- §5.5 p25: total precision-dependent high-level modulus O(p log k/k); §6 p26 explicitly 'Implementation Not available yet'. No real F,q,Q or exact bottom-modulus and security ledger provided in this supplied source passage.
[FACT] Historical P0-PRESCOUT-21, findings/pure-fhe-p0-gckks2600-nonunit-conversion-modulus-lift-gate-2026-10-26.md SHA 9240f78fbc58f17e7dab07d0daf72169fb0a6e8c ALREADY derived:
 Q > 2 sqrt(N)(||m||inf + q K_I) + (1+||s||1)||F||1.
Its toy modulo-only counterexample is outside Lemma3 small-lift hypothesis. Do NOT present this previously derived sufficiency or failure as new.

## [DERIVATION] Exact Parseval control of coefficient norm by canonical magnitudes

For n=k/2 and F(Y)=Σ_{j=0}^{n−1} f_jY^j∈Z[Y]/(Y^n+1), n a power of two, orthogonality of the primitive 2n-th root evaluation matrix gives EXACTLY
  Σ_j |f_j|²=(1/n) Σ_{ξ primitive}|F(ξ)|²=(2/n) Σ_{i=0}^{n/2−1}|F(ζ_{2n}^{5^i})|².
There is one useful pair with magnitude c_m (common useful), and n/2−1 unused pairs each ≤ c_e. Therefore
  ||F||coeff,2² ≤(2/n)c_m²+((n−2)/n)c_e².
Since F has only n coefficients when embedded sparsely in R=Z[X]/(X^N+1), Cauchy-Schwarz gives
  ||F||coeff,1 ≤ √n ||F||coeff,2 ≤ sqrt(2 c_m² +(n−2)c_e²). [EXACT]
Combining with the P0-21 lifting certificate, for normalized ||m||inf≤ε q, ||I||inf≤K_I, and h=||s||1, the one-step sufficient bound is
  Q/q > 2√N(K_I+ε) +(1+h)*sqrt(2(cm/q)² + (k/2−2)(ce/q)²).
This is a condition, not a guarantee for the author's unreleased parameters, and depends on the actual source lift event.

## [TOY_EXACT] Check on the P0-21 nonunit factor

For N=8,k=8,n=4,Y=X², F(Y)=3+Y−Y³:
 f=(3,1,0,−1), ||f||²2=11, ||f||1=5.
 Canonical useful c_m=3+√2, unused c_e=3−√2.
 Parseval identity: (2/4)[(3+√2)²+(3−√2)²]=11, exactly.
 New l1 bound: sqrt(2cm²+2ce²)=2√11≈6.633, valid for actual ||F||1=5.
 This is an exact symbolic ring check, NOT a real GCKKS native ciphertext experiment.

## [TOY_NUMERIC] Fixed additive modulus bits in one explicitly conditional regime

Illustrative assumptions only, **not** author measurements: N=65536, k=256,n=128, ephemeral h=32, KI=15, ||m||inf≤q/16, and BOTH cm≤q and ce≤q. Then ||F||1/q≤√128, and
  Q/q > 2*256*(15+1/16)+33√128
      =7712+373.3523804664971
      =8085.3523804664971;
therefore Q/q≥8192=2^13 suffices for this individual Lemma3 lift certificate. Conditional headroom≈12.981 bits, q itself can be precision-dependent, and this is NOT the whole bootstrapping modulus cost. No claim that the actual paper's q or F satisfy cm≤q and ce≤q.

## [DERIVATION — heuristic consistency, not actual parameters]

For a fixed k and fixed r, the source's BKZ/GSA estimates when w→0 give
  cm ∝ w^(1−4/k), ce ∝ w^(−4/k), and natural ρ≈Δ≈r ce.
If the input q scales at least proportionally to Δ (a separate design assumption to be checked), then
  cm/q = O(w), ce/q=O(1).
The derived Q/q headroom bound is then p-INDEPENDENT for fixed N,k,h,ε,KI, even though q and |F| themselves grow as w→0. Meanwhile Δ/cm∝1/w is the CKKS-equivalent scale, explaining why increasing useful precision need not force extra Step8 *ratio* bits. This is conditional/heuristic, NOT a realization proof or a claim of publication-relevant improvement.

## Results, kill/keep and limits

H30's supposed NECESSARY independent precision-growing Q/q surcharge FAILS as an unconditional assertion: exact canonical Parseval gives a simple sufficient certificate depending on cm/q and ce/q, and a plausible precision-scaling regime allows fixed additive headroom. However the original 2026/2600 contains no implementation, and the specific factors and Q/q values have NOT been checked. The real implementation feasibility and security remain UNKNOWN.
This is not a new FHE construction, and it is not a flaw in source Lemma3 or §5.5. P0-21 already addressed small-lift hazards and derived nearly the same headroom bound; P0-30 adds only exact factor-norm elimination using source ring structure.
No further synthetic scans. At this point several closely related P0-23 to P0-30 GCKKS novelties have failed to produce a nontrivial mechanism. Recommendation: PARK the GCKKS line until (a) first-party 2026/2531 revised full PDF or (b) real full F,q,Q,Δ,ρ,eval key/noise/security/ciphertext ledger is available; pivot to another independent PURE-FHE candidate via source-first novelty scouting if PI continues. Any future Codex task requires explicit PI permission.

END_OF_ITERATION:
STATUS: PASS_FACTOR_NORM_EXACT / FAIL_FORCED_PRECISION_GROWING_STEP8_HEADROOM / REAL_PARAMETER_FEASIBILITY_UNCLEAR
RESULT: Exact ||F||1≤sqrt(2cm²+(k/2−2)ce²) from Parseval; combined Step8 Q/q sufficient condition; conditional N65536,k256,h32 scenario has 13-bit headroom, no unconditional actual parameter certification.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: Unless primary parameter set or revised Focused CKKS §6 becomes available, stop repetitive GCKKS prescouts and initiate independent source-first PURE-FHE gap search on PI continuation; one hypothesis per round.
STATE_UPDATE: YES, one isolated PURE-FHE finding. No global STATE.md/other research tracks modified.
CODEX_REQUIRED: NO; all native implementation/security validation work PENDING user authorization.
