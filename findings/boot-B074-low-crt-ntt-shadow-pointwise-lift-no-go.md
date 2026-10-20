# BOOT-B074 — Low CRT NTT shadow: exact cross-modulus conversion gate
Date: 2026-10-20 | TRACK_ID BOOT | SHIP PAUSED
STATUS: PASS_EXACT_CRT_NTT_TOY / FAIL_POINTWISE_NTT_LIFT / FAIL_DUAL_SHADOW_COST_AND_NOVELTY / UNCLEAR_NONLINEAR_FULL_VECTOR_CONVERSION

## One falsifiable hypothesis
H074: keep a current low-CRT accumulator in negacyclic NTT form and produce high-modulus centered CRT gadget corrections from low NTT frequencies **independently and directly**, saving inverse low NTT, forward high NTT and/or coefficient-data synchronization beyond Bernard–Joye Algorithm 3, without weakening approximation precision or changing independent BSK masks.
Cheapest killer: is each high corrected NTT frequency determined by the corresponding low NTT frequency for *all* low polynomials?

## Source provenance and prior art
[FACT] Bernard and Joye, "Approximate CRT-Based Gadget Decomposition for Fully Homomorphic Encryption", IWSEC2025, https://marcjoye.github.io/papers/BJ25gadcrt.pdf . Physical PDF p9 Equations (1),(2) and Proposition 1: centered coefficientwise low correction, high CRT gadget, ε bound. Physical p15 Algorithm 3, lines3–12: all low/high accumulator coefficient shares already maintained, low->high synchronization in decomposition, gadget digits forward NTT, product, inverse NTT to update all CRT shares. Physical p16 Eq(3),(4): key/test polynomial are already modified/pre-twisted to simplify low CRT correction. ePrint2024/909 older version; cached SHA256 5047de57cb080f2ed419c58f257a6fdf6ee1973d5ef21c02925c901ad1d1f1ff (version unverified).
[PRIOR] Li et al., "Faster Bootstrapping via Modulus Raising and Composite NTT", TCHES 2024(1), https://d-nb.info/1312413913/34 . Published composite NTT + modulus-raising hybrid for FHEW-like schemes already reduces NTT counts from 2(d_g+1)n to 2(ceil(d_g/2)+1)n in stated setting. Thus generic "less NTT through CRT gadget integration" is not novel.

## Exact mathematical gate
Use R_p=F17[X]/(X^8+1), high q∈{97,113}; CRT Q=17*97*113=186337, roots of order 16 ρ17=3, ρ97=8, ρ113=35; negacyclic NTT_j evaluates at ρ^(2j+1). The high NTT of the low CRT centered correction is T_q(a) = NTT_q(L_17(a)) where L centers EACH coefficient individually in [-8,8].

Pointwise impossibility witness: f0=0, f1=X-3. Both low j0 evaluations at X=3 equal 0 mod17, but high q97 j0 evaluation of centered f1 at X=8 equals 5 !=0. Hence NO function even nonlinear of the single input low frequency j0 can produce the high corrected frequency j0 for all polynomials. Generalize for j=0..7 with fj(X)=X-ρ17^(2j+1) mod17 and both high q: all 16 corresponding frequency witnesses PASS. This is strictly a no-go for **componentwise low-frequency to high-frequency maps**, not for a nonlinear function of the entire NTT vector.

Even using all low frequencies, fixed ADDITIVE cross-modulus conversion fails: 8+1=9=-8 (mod17), while centered Lift17(8)+Lift17(1)=9 and Lift17(8+1 mod17)=-8; they differ by 17 ≠0 modulo 97 or 113. Invertible NTT does not repair the lack of additivity. Thus no fixed group-homomorphic or linear low NTT -> high corrected NTT map works universally. A nonlinear complete-vector transform is not ruled out.

The correct baseline is iNTT_17 -> centered coefficient lift -> NTT_q. Since BJ Algorithm3 already stores and updates the coefficient CRT shares, a new low NTT shadow duplicates representation unless it demonstrably eliminates an existing actual operation.

## Independent deterministic validation
[TEST] Pure stdlib Python /mnt/data/boot_B074/verify_b074.py SHA256 c82b1fe169f5b8a123f7a002a1aa58b206efdc82cdc318646a494b274d62e795. Q186337 high CRT gadget idempotents and centered reconstruction: 4000/4000 arbitrary coefficients reconstruct within ±8. NTT17 inverse/forward roundtrip for 4000/4000 randomly sampled low polynomials PASS. Pointwise counterexample at both high primes all slots: 16/16 PASS. Naive pointwise centered lift of low frequency vs true high NTT of centered low coefficients: 31687/32000 slots MISMATCH (97: 15819/16000; 113: 15868/16000); the counterexample, not this empirical ratio, proves the no-go. All random tests seed 74020. Result JSON SHA256 69f03f10b07d60d0d486ab4b0534ac6fcf9186433086ff4ff8959fe44f198427.

## Conditional bandwidth/information note
If the low residual coefficient vector is independent uniform in F17^8 conditional on what high unit knows, the high unit's exact centered-lift NTT output is injective in that vector because p<q and high NTT invertible. Required information is at least N log2 p=32.699703 bits/polynomial (65.399405 bits for GLWE mask/body pair). Low NTT is an invertible re-expression so cannot reduce this information merely by replacing coefficients by NTT slots. This is a conditional information statement and NOT a general NTT-operation lower bound or a security theorem. Correlations across real FHE updates were not analyzed.

## Complexity, safety, novelty
Full-vector centered correction may be computed with coefficient conversion or another nonlinear transform; B074 has NOT proved the circuit complexity of all alternatives. Direct frequency-wise lift is incorrect. Adding low-NTT shadow to published coefficient-domain low CRT update has zero demonstrated saved transforms. No new BSK mask restrictions, no security claim, no real-parameter/native PBS tests, no DFR or speedup.
Decision: ARCHIVE this NTT-only simple shadow, do not prolong CRT caching B073–B074.

## End of iteration
STATUS: FAIL_POINTWISE_NTT_LIFT / PASS_MATH_FALSIFIER / FAIL_NEW_ONLINE_COST.
RESULT: explicit no-go and 16 slotwise counterexamples, exact CRT/NTT tests, and BJ/Li prior-art gate.
NEXT_TEST B075 NOT STARTED: pivot to a different crypto interface with a concrete claim of reduced online ring work; prioritize testing whether **encrypted selector preparation can be shared across a genuinely nonidentical set of AP products**, while retaining exact key labels and independent noise; screen BJ and related tensoring/hoisting prior art before pursuing. If no genuine novelty/cost advantage, kill early.
STATE_UPDATE NO: existing findings/boot-STATE.md ~187967 bytes read via GitHub Notes returns {} and cannot safely modify; new B074 finding only. SHIP unchanged.
ARTIFACTS: sandbox BOOT_B074_handoff.zip SHA256 28384678b67cf0627a58fcf27b136769fa07577e6c1566690a171571fd464c85, includes full report, reproducible Python, JSON, log, manifest.