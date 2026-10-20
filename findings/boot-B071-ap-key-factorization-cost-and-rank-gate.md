# BOOT-B071 — Automorphism-extended GGSW compression: linear orbit and encrypted factorization gates
Date 2026-10-20. TRACK_ID BOOT; SHIP PAUSED; no writes to other tracks.
STATUS: PASS_EXACT_FACTORIZATION / FAIL_PUBLIC_LINEAR_SHORTCUT / FAIL_ONLINE_EXTERNAL_PRODUCT_BUDGET / UNCLEAR_SECURITY_AND_NATIVE.

## One primary hypothesis
Replace Bernard–Joye's selector-by-automorphism key ciphertexts encrypting -sigma(s_j)*mu_i with a smaller independent key transcript encrypting the secret images sigma(s_j) and ordinary selector gadget ciphertexts mu_i. Demand same-secret correctness, no secret-dependent public mask restrictions, and strictly lower online cost than the original AP one-product interface. Test free linear reconstruction then an encrypted factorization.

## Source and prior-art provenance
[FACT] Bernard & Joye, Bootstrapping (T)FHE Ciphertexts via Automorphisms: Closing the Gap Between Binary and Gaussian Keys, ASIACRYPT 2025, author PDF https://marcjoye.github.io/papers/BJ25autpbs.pdf , physical PDF page 14 Definitions 4.1 and 4.2; page16 Eq.(4.1) explicitly says the body GLWE^g2_s(mu_i) is SHARED across all sigma, making EACH key size (|S|*k+1) Gadget-GLWE components not |S|*(k+1). P17 Algorithm4.1 and p18 Proposition4.8 cost/noise. This existing body-row saving is NOT novel.
[PRIOR] B057 failure: publicly forced zero GGSW mask/body cross blocks may imply secret-dependent publicly visible kernels; do not employ such leakage-prone shortcuts. Full-entropy secret, separate masked encryptions needed. B070 ordinary covariant sigma transport cancels intended secret exponent weighting.

## Gate A: free public-linear reconstruction
[DERIVATION] In R=F257[X]/(X^8+1) fix primitive 16th root zeta=2. All 8 odd t mod16 give independent coordinate evaluations (sigma_t(s))(zeta)=s(zeta^t). Their values vary independently with s, so for a missing t no polynomial coefficients c_u(X) independent of s can satisfy sigma_t(s)=sum_(u!=t)c_u(X)*sigma_u(s) for all s. Evaluating at zeta contradicts independent coordinates. Since ternary secret support contains each basis monomial X^j, an F257-linear identity for all ternary s would imply it for all s. This is a restricted EXACT PUBLIC-LINEAR no-go, not a general nonlinear compression theorem, nor a security attack.
[TEST] Flattened automorphism operator matrix rank 8/8 (odd t=1,3,...,15) over F257. Eight inverse-evaluation indicator polynomials isolate each missing orbit coordinate, 8/8 PASS.

## Gate B: encrypted factorization
[DERIVATION] Put selector GGSW_s(mu_i) in ordinary BSK, and publish reusable GLWE_s(-sigma(s_j)*B^h) for every automorphism sigma, key component j, gadget digit h. On demand derive one AP mask row at h by ExtProd(GLWE_s(-sigma(s_j)*B^h),GGSW_s(mu_i)); output is valid GLWE_s(-sigma(s_j)*mu_i*B^h) up to additional external-product noise. This is a standard nonlinear encrypted multiplication, not a new primitive. Key transcript's joint KDM/circular security and reuse correlations NOT proved.
[TEST] Script verify_b071_ap_key_factorization.py SHA256 b1a40249fe3552f1c8d25daec6e065be17d7af3e2b1ea2d7822f80a034228271, R=Z65537[X]/(X^8+1), B16,d5, random ternary s, random selector monomials X^{s_i} with s_i∈{-2,-1,0,1,2}, random full GLWE masks and independent {-1,0,1} primitive noise; 60 trials*4 automorphisms*5 gadget digits=1200/1200 exact typed rows AND coefficientwise modular noise recurrences PASS. Derived row error coefficient ∞-norm median=53, observed max=129; independently directly encrypted AP rows with this primitive noise would have per-coefficient error ≤1. These are toy local errors NOT DFR.

## Concrete illustrative cost (not measured runtime)
At n465 selectors, r=|S|=4 shortcut automorphisms, k1 GLWE secret polynomial, d5 gadget digits:
- Published key per-selector (r*k+1) Gadget-GLWE components: 465*5=2325 components, each 5 regular GLWE ciphertext rows -> 11625 underlying GLWE rows.
- Factorization stores 465*(k+1)=930 ordinary selector-GGSW components =4650 rows, plus r*k*d=20 regular encrypted-secret GLWE rows -> 4670. An IDEALIZED 59.83% total **this BSK subset** byte-row reduction, excluding other evaluation keys.
- To materialize one NON-IDENTITY AP mask key for one selector needs k*d=5 EXTRA full external products, before the originally required single AP product. If all n selectors use nonidentity shortcuts: extra 2325 operations, total 2790 vs original 465 => 6x as many online full products, before public preparation and other costs. With p fraction nonidentity: n*(1+p*k*d) total; p=0 loses shortcut value. Offline precompute/caching returns stored cross-product keys (known time-memory tradeoff).
This FAILS the desired online critical-path advantage for the explicit factorization. Not a universal lower bound for arbitrary novel compression architectures.

## Security, noise, novelty qualifications
Changed transcript includes secret-dependent encryption of sigma(s) under s; circular/KDM security not formally established. Extra row noise then feeds another external product; real DFR and native runtime unknown. The source already shares common body rows. A public-dependent mask kernel may leak secret (B057 toy issue). No evidence of publishable new primitive; no attack on Bernard–Joye.
STATUS=FAIL_FREE_LINEAR_AND_ONLINE_COST; PASS_ALGEBRAIC_FACTOR.
RESULT=direct cross-automorphism key factorization correct but offline storage-vs-online-product tradeoff fails target.
NEXT_TEST B072 NOT STARTED: a genuinely FUSED multiple-input gadget multiplication interface with no explicit intermediate AP mask-row materialization, compare its decomposition counts to Bernard–Joye's one external product; stop if merely a nested external product or known tensoring. Require full security/noise/cost no-leakage gate.
STATE_UPDATE NO: findings/boot-STATE.md read_repo_file returns {} despite listing ~188KB. Preserve original; this new record append-only. SHIP unchanged.
LOCAL: BOOT_B071_handoff.zip (report, verified Python script, b071_results.json SHA256 e5efbb0c4afa712080ee8debba64fd6a4bf0a5ab760f38c93e61345e85f7b71e, run.log); ZIP SHA256 c5d8bb36f66b0bbfe661c9775e31a34f80ff99ca5defaff530d07137a11c3b63.
