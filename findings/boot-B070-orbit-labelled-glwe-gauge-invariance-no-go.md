# BOOT-B070 — Orbit-labelled GLWE/GGSW with deferred key switching: gauge-invariance falsifier

Date: 2026-10-20
TRACK_ID: BOOT. SHIP PAUSED. No writes to SHIP/CGS/VFHE/EXPLORE.
STATUS: PASS_TYPED_ORBIT_TRANSPORT / FAIL_WEIGHTED_BLIND_ROTATION_WITH_COVARIANT_KEYS / NO_NEW_PRIMITIVE.

## One primary hypothesis
H070: For arbitrary (e.g., Gaussian) LWE secret digits s_i and varying public weights a_i, retain a GLWE ciphertext on orbit-labelled secrets sigma_t(s), publicly carry one ordinary base GGSW encryption of X^(s_i) to the matching label with sigma_t, perform external products without intermediate key-switching and undo the total automorphism at the end. Can this compute target exponent e0+sum a_i*s_i with only n ordinary bootstrapping keys and no extra weighted keys? Cheapest decisive test: exact typed GLWE/GGSW arithmetic and phase recurrence.

## Prior art checked against primary full paper
[FACT] Olivier Bernard and Marc Joye, "Bootstrapping (T)FHE Ciphertexts via Automorphisms: Closing the Gap Between Binary and Gaussian Keys", ASIACRYPT 2025, https://marcjoye.github.io/papers/BJ25autpbs.pdf / ePrint 2025/163. Original PDF physical page 8 Eq(2.3): bskAUT[i]=GGSW_s(X^(s_i)); Figure2.1 telescoping traversals apply HomAut (with KS), then ordinary external product; p14 Defs4.1/4.2 instead define GGSW^{*,sigma}_s(μ) with rows encrypting -sigma(s_j)*μ and μ under the ORIGINAL key s, yielding in one parameterized ext product a GLWE under s encrypting sigma(m)*μ; p15 Prop4.3 noise, p16-18 S-parametrized traversal Algorithm4.1. This non-equivariant mixed-key GGSW is **already a published solution** to fuse an automorphism and key switch into external product. Ordinary transported GGSW is NOT that object.
[FACT] LMK+ (EUROCRYPT 2023), existing automorphism-based BR, see Bernard-Joye Section2. Source estimates AP generic n(m-1) weighted GGSWs vs automorphism approach n ordinary selector GGSWs plus automorphism switching keys; selecting larger shortcut sets S raises BSK memory. Do not invent independent novel mechanism.

## Exact mathematical gate
Use R=Z_Q[X]/(X^N+1), N=8,Q=257, automorphism sigma_t(X)=X^t (odd unit t mod2N). GLWE decryption is b-a*s=m+e. Standard GGSW_s(μ) has mask rows encrypting -s μ B^j under s, body rows encrypting μ B^j under s. Applying sigma_t to all rows makes a valid GGSW under sigma_t(s) encrypting sigma_t(μ); this uses no independently generated keys but row transforms are not free and samples are correlated.

Let t0=1, current accumulator key label sigma_(t_(i-1))(s) and plaintext exponent e_(i-1). Apply automorphism sigma_(u_i) to accumulator; t_i=t_(i-1)*u_i mod2N. Apply sigma_(t_i) to base GGSW_s(X^(s_i)) (plaintext X^(t_i*s_i)); external product is well-typed under sigma_(t_i)(s). Then
  e_i = u_i*e_(i-1) + t_i*s_i (mod2N).
Since every t_i is invertible, e_i/t_i = e_(i-1)/t_(i-1) + s_i (mod2N). Inductively, undo final sigma_(t_n)^(-1) to return under s, and output exponent EXACTLY e0+sum_i s_i, independent of all orbit-label transitions. Desired blind rotation target e0+sum_i a_i*s_i is generally different.
This is naturality/gauge cancellation for **covariantly transported** bootstrapping keys only. It is NOT an impossibility for arbitrary non-equivariant gadgets, extra keys, nonlinearity or changed ciphertext representations.

## Full toy ciphertext verification
[TEST] Python stdlib verify_b070_orbit_labels.py, SHA256 5a08c02803940fa782d1c682ae6eba056901b113ba9f77f4caa2440cd3227a34. Exact negacyclic modulo257, N8, base B2,d9 (exact digit reconstruction since 2^9>=257); randomized ternary RLWE secret polynomial, random GLWE masks, exact full 2*9-row noisy-free GGSW encryptions, 4 LWE secret values s_i∈{-2,-1,0,1,2}, odd public weight a_i and automorphism u_i, 160 trials. Verify EACH intermediate under sigma_(t_i)(s) and final under s.
- Transported ordinary bskAUT preserves type and after final inverse equals ordinary UNWEIGHTED external-product result: 160/160 PASS.
- Yet weighted target phase achieved coincidentally in only 24/160, 136/160 FAIL.
- An otherwise identical path with **pre-encrypted AP-style weighted** GGSW_s(X^(a_i*s_i)) is correct 80/80, demonstrating extra key material restores target, NOT a new primitive.
- Independent phase enumeration: s∈{-2,-1,0,1,2}^3 and a∈{1,3,5,7}^3, 8000 comparisons, 1340 accidental matches and 6660 mismatches. First s=(-2,-2,-2), a=(1,1,3), unweighted exponent10 vs desired6 mod16.
[TEST] One proposed affine public plaintext correction A+B*X^s=X^(a*s) can fit s0 and s1 but must fail at s2 for generic a. In Z257[X]/(X8+1), a3: B=1+X+X², A=1-B, s2 output -X+X³+X⁴ != X^6. Code verify_b070_affine.py SHA256 6ce9a25b869a3825b4dfa2fdaaf74eec00a852e2591e3edb6d88ddf5aea4d8ae checks a=3,5,7,9,11,13,15: 7/7 FAIL for s2. For binary s∈{0,1} the affine trick works, and is known NTRU/TFHE CMux (archived B059-B062). This check excludes this narrow affine repair only, not general ciphertext computation.

## Why Bernard-Joye works but naive orbit does not
Naive ordinary sigma_t(GGSW_s(μ)) encrypts -sigma_t(s)*sigma_t(μ),sigma_t(μ) under sigma_t(s). Its selector message transforms along with key; after undoing the entire orbit the weight cancels.
Published automorphism-extended GGSW^{*,sigma}_s(μ) encrypts -sigma_t(s)*μ and μ under BASE s, so selector μ is not covariantly transformed. A cross-secret external-product is possible at cost of one external product, with B-J key-generation/noise tradeoff. This is already prior art.
Generic AP would need a table indexed by a_i, n(m-1) entries, or other secret-dependent reweighting/cross-key gadget. With only public σ transforms of one base key per selector, weighted functionality fails. No new cryptographic construction, real DFR, security proof or latency claim.

## End
STATUS=FAIL_WEIGHTED_BR_FROM_PUBLIC_ORBIT_LABEL_TRANSPORT.
RESULT=PASS underlying type consistency, FAIL required weighted function, prior-art non-equivariant remedy located and audited.
NEXT_TEST=B071 not started. Form ONE concrete compression/decomposition-sharing claim for the non-equivariant Bernard-Joye GGSW ciphertext (rows encrypting -sigma(s)*μ under s) using fewer safe encrypted basis secret terms; audit B057 secret-dependent mask leakage and independent key/noise cost. Reject immediately if merely a repackaging of automorphism-parametrized product or full indexed key table.
STATE_UPDATE=NO: existing findings/boot-STATE.md listed 187967 bytes but read_repo_file returned {}, so do not overwrite canonical state. Append-only B070 new findings. SHIP untouched.
LOCAL REPRODUCIBILITY: BOOT_B070_handoff.zip includes full report, two Python scripts, results JSON, logs. JSON SHA256 ac11445c5d897b227316cdd9b6998cffcb40e3d942f0729490c09fab2d0deb1b.
