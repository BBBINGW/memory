# PURE-FHE · P0-PRESCOUT-43 — GCKKS vs shaped rounding: free representation-fusion commutator gate

Date: 2026-10-27 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: INDEPENDENT_PURE_FHE_CORE_CONSTRUCTION_SOURCE_GATE
PREVIOUS: P0-PRESCOUT-42, findings/pure-fhe-p0-42-descent-pbs-priorart-and-eval-lut-dominance-stagnation-gate-2026-10-27.md, commit 3bffed7d1f7078145928c227e2d6cf0ff5eb28c6
LATEST_COMPLETED: P0-PRESCOUT-43
NEXT_ITERATION: P0-PRESCOUT-44 NOT_STARTED; active STAGNATION/HUMAN_REVIEW
STATUS: FAIL_FREE_SHAPED_GCKKS_ENCODING_COMMUTATION / PASS_EXACT_UNIT_FACTOR_COUNTEREXAMPLE / NO_NEW_MECHANISM
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO. No GPU/native/remote/model downloads or infra actions.
STATE_UPDATE: YES, isolated PURE-FHE findings document only; root STATE.md and other tracks unchanged.

## One smallest falsifiable H43

After P0-42 declared STAGNATION and the Oct 2026 release of two related but different approximate FHE representations, can a public factor basis conversion achieve "the best of both worlds" for free—specifically, does shaped-rounding-first encoding equal GCKKS inverse-factor-first encoding for every input when F is a unit, so that a compiler can reorder encoding/rescaling/representation changes without new precision/noise cost?

Cheapest decisive test: source-first analyze exact conversion formulas, then produce a minimal exact cyclotomic-unit counterexample to the two published encoder maps. The test is not a new scheme or general FHE no-go. Source retrieval of the revised 2026/2513 author PDF via GitHub Notes is still blocked, so the source-specific comparison is grounded in the explicit first-party discussion within *2026/2524* supplied original pages rather than invented details of inaccessible 2513.

## [FACT] Primary-source evidence and provenance
Full user-supplied `papers/supplied/2026-2524.pdf`, *Homomorphic Encryption for High-precision Arithmetic of Approximate Numbers*, physical pp7–10 particularly §1.4 "Parallel and Follow-up Work", reread directly 2026-10-27:
- Original §1.4 p8 explicitly relates Jules Dumezy 2026/2513 shaped-rounding scheme to GCKKS by g=F,R=k/4, and says stored Dumezy components absorb F, while GCKKS applies F at decryption;
- For a factor F invertible modulo all relevant moduli, ciphertext formats map via multiplication by F on both components. Shaped rescaling is `Round_{F,r}(u)=(u-F*[F^{-1}u]_r)/r` as defined by source, and author gives a conjugacy identity `Round_{F,r}(F*u)=F*round(u/r)` with appropriate source rounding notation. For shaped cipher, key-switching may require shaped error or a larger P, or conversion to GCKKS and back; the latter ALREADY MENTIONED BY ORIGINAL AUTHORS p9, so it is neither a fresh fusion idea nor a novel algorithm here.
- §1.4 p9 notes shaped rescaling adds four F/F^-1 coefficient-domain polynomial multiplications per two-component ciphertext (paper's stated operation count 2kN word-size ops), while GCKKS multiplication costs a correction with F (3*l*N word products for l RNS primes), and GCKKS conjugation can cost additional correction for non-unit F. Existing work trades costs between operations, not free aggregation.
- Crucially p10 explicitly writes different plaintext encoder pipelines for same noiseless m0 and unit F:
  E_shape(m)=F*round( F^-1*round(r*m)/r ),
  E_GCKKS(m)=F*round(F^-1*m).
  The authors say the two are equal only when the inner rounding error does not flip an outer rounding. This directly establishes PRIOR ART for the non-commutation issue: this record offers a concrete, independently checked algebraic witness, NOT a new discovery or source flaw.
- Dumezy *Fully Homomorphic Encryption for Small Batches of Complex Numbers*, 2026/2513, first-party publication and blog available as text at https://jdumezy.com/publications/new-scheme/ and https://jdumezy.com/blog/shaped-rounding/ ; public author summary reports guard-domain shaped rounding, unit in small cyclotomic subring, native bootstrap, CKKS conversion and 128bit-target poulpy implementation. FULL PDF remains RETRIEVAL_BLOCKED via GitHub Notes official 403/arXiv/mirror; do not assert unreviewed theorems or algorithms beyond author's abstract. Live author's 2026/2513 summary may update numeric claims, so do not cross-infer here.
- Related 2026/2600 GCKKS full supplied source has high-precision bootstrap; user P0-21..30 already audited its local novelty. No new claims of GCKKS bootstrap novelty.

## [DERIVATION] Exact unit ring and two different encoders

Let R=Z[X]/(X^8+1). Choose the previously known toy cyclotomic unit F=1+X^2−X^6 and inverse F^-1=−1+X^2−X^6; direct multiplication reduces to FF^-1=1 (mod X^8+1). Thus invertible modulo every positive integer, meeting shaped-rounding unit premise. Work in R⊗Q with coefficient-wise nearest integer rounding, none of the relevant coordinates equal half-integers.

Let r=3 and m=−6/7−(3/7)X^2. Set:
 E_A(m)=F*[ F^-1*[r*m]/r ] with bracket meaning coefficient-wise nearest-integer rounding at BOTH inner and outer brackets.
 E_B(m)=F*[F^-1*m], with one coefficient-wise nearest-integer rounding.
Caution source notation `[ ]` for residue is context-dependent; formula above uses only nearest-integer coefficient rounding, written explicitly in the final narrative.

Compute:
  F^-1*m=(3/7)−(3/7)X²−(3/7)X⁴+(6/7)X⁶.
  round(F^-1*m)=X^6.
  E_B(m)=F X^6=−1+X^4+X^6 in R.
  round(r*m)=−3−X².
  (F^-1*round(r*m))/r=(2/3)−(2/3)X²−(1/3)X⁴+X⁶.
  round(...) =1−X²+X⁶.
  E_A(m)=F(1−X²+X⁶)=−1.
Thus E_A≠E_B and their output difference is −X⁴−X⁶. This is an exact rational and integer-ring computation, no floating point or FFT approximation. Private symbolic Python arithmetic of length-8 cyclic-negacyclic convolution confirmed all intermediates and the inverse identity. The chosen fractions do not trigger any tie-breaking convention. Both E_A and E_B are mathematically well-defined idealizations under this unit factor; no ciphertext security/precision theorem is inferred.

## [DERIVATION] Why this does not yield a positive "hybrid" scheme
At a fixed representation, rescaling conjugacy can be exact as authors show when one takes an ALREADY F-shaped polynomial F*u:
  RoundF,r(F*u)=F*round(u/r).
This algebraic identity is very different from freely moving *pre-encoding* rounding across F^-1. The counterexample separates those two operations.
Converting an actual two-component ciphertext from one representation to another requires applying F or F^-1 to components, and if non-unit F lacks inverse mod some RNS prime conversion is not even defined in the naive form. A conversion may be public but not FREE: depending on ciphertext representation and domain, FFT/NTT, modular multiplication, RNS handling, key tags and independent rounding error can add latency and noise; original source §1.4 p9 explicitly offers this alternative for key-switching. No verified high-value new algebraic trick changes main complexity. Comparing measured throughput is invalid without source-matched parameter sets and complete keys/precision/security benchmarks.
Do NOT claim strong general non-commutativity: specially aligned m,r,unit factors can make the two outputs equal, as source already says; the claim fails ONLY as universal equality or zero-cost compiler rewrite.

## End decision and stagnation handling
H43 FAILS. Closest-original papers already (i) compare schemes, (ii) mention conversion-as-keyswitch bridge, and (iii) explicitly identify noncommuting encoder rounds. The toy witness establishes source's stated caveat, not a novel crypto mechanism. Do NOT promote "adaptive representation scheduling" as an independent Pure-FHE paper without a precise new security/noise-compatible conversion and quantitative dominance over author methods.

After 43 independent P0 screens, repeated adjacent variants remain research-program STAGNATION. Recommendation HUMAN_REVIEW of Pure-FHE research objective and novelty threshold, and treat lack of inaccessible 2026/2513,2531,2616,2618 full sources as separate FIRST-PARTY SOURCE gaps; user may supply if wishing to audit those exact lines. No automatic pivot to SHIP/BOOT/EAI. No Codex tasks justified.

END_OF_ITERATION
STATUS: FAIL_FREE_ENCODER_REORDER / PASS_EXACT_NONCOMMUTATION_COUNTEREXAMPLE / STAGNATION_HUMAN_REVIEW
RESULT: ideal coefficient rounding before vs after applying a public invertible F can give provably different encodings even with F unit, r=3 and small rational m; original source already says so. No original construction.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: Await PI guidance on whether to (a) seek source-complete independent FHE scheme core or (b) change Pure-FHE publication objective to a defined security/verification/system task, or (c) audit accessible full new authors' sources. No P0-44 automatic launch.
STATE_UPDATE: YES isolated finding only; shared STATE.md and other research tracks unchanged.
CODEX_REQUIRED: NO.