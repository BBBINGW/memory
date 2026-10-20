# BOOT-B073 — Cross-step CRT low-correction caching: false for changing AP accumulator

Date: 2026-10-20
TRACK_ID: BOOT. SHIP paused.
STATUS: PASS_SAME_INPUT_AUTOMORPHISM_EQUIVARIANCE / FAIL_CROSS_STEP_LOW_CRT_REUSE / NO_NEW_PRIMITIVE

## Primary falsifiable hypothesis
In two consecutive Bernard–Joye automorphism-parametrized external products, retain the previous input's centered low-CRT correction and transport it by a public automorphism as a cache for the next newly computed accumulator. Intended effect: reduce low-to-high synchronization and digit re-decomposition per online Blind Rotation step with unchanged key material and approximation bound.

## Source evidence and prior-art gate
[FACT] Bernard and Joye, Approximate CRT-Based Gadget Decomposition for Fully Homomorphic Encryption, IWSEC 2025, author paper https://marcjoye.github.io/papers/BJ25gadcrt.pdf, Section 3.2 p9 Equations (1)-(2) and Proposition 1, Section 4.2 pp14-16 Algorithm 3. Earlier ePrint version https://eprint.iacr.org/2024/909, GitHub mirrored ePrint SHA256 5047de57cb080f2ed419c58f257a6fdf6ee1973d5ef21c02925c901ad1d1f1ff, VERSION_UNVERIFIED. Approximate CRT requires new low-modulus residues from current ciphertext and shares the low correction with all high CRT units. Authors already maintain low CRT accumulator shares across BR steps and pre-twist keys; those steps are prior art.
[FACT] Bernard and Joye, Bootstrapping (T)FHE Ciphertexts via Automorphisms: Closing the Gap Between Binary and Gaussian Keys, ASIACRYPT 2025, ePrint 2025/163, Section 4.1 Definition 4.2, Proposition 4.3, Algorithm 4.1: AP external product maps one *changing* GLWE accumulator through the automorphism and secret-transformed GGSW; successive inputs differ.
[PRIOR] Same-input hoisting and key decomposition decoupling are known in FHE literature; see Belorgey et al., Revisiting Key Decomposition Techniques for FHE: Simpler, Faster and More Generic, ASIACRYPT 2024. Same-input automorphism equivariance is not claimed as a new primitive.

## Exact CRT algebra
In the single-low-factor special case, q=p*Q_hi, p odd and coprime to Q_hi, let S(x)=centered(x mod p) coefficientwise. Let high factors q_j and CRT gadget idempotents w_j satisfying w_j=1 mod q_j and 0 mod other q_h and mod p. Set D_j(x)=cent_{q_j}(x-S(x)), Rec(D(x))=Σ_j w_j D_j(x). Then Rec(D(x))=x-S(x) modq and |error|<=floor(p/2).

Because negacyclic automorphism σ_t is a signed coefficient permutation, the odd-p centered correction and high digit decomposition satisfy S(σ_t(x))=σ_t(S(x)), D_j(σ_t(x))=σ_t(D_j(x)) for the *same input*. This is a positive hoisting property with no inter-step claim.

For a NEW coefficient x' and stale r, compute high residues from x'-r but retain zero in low CRT slot. Let E_low=(q/p)*( (q/p)^(-1) modp ) modq. Then exact reconstruction error is
  e_wrong ≡ r + E_low*(x'-r) (modq).
Only when r≡x' modp does this simplify to bounded centered r. If stale r differs from S(x'), the error has a nonzero CRT idempotent component: no source epsilon guarantee.

Counterexample q=17*97*113=186337, Q_hi=10961, E_low=43844, new x'=0, stale r=1: error 1-43844=-43843, while correct error is 0 and bound is 8. In this parameter case, any mismatched centered r in [-8,8] implies |e_wrong|>=10953, rather than <=8, since error equals r modulo Q_hi but has a different residue modulo17.

Independently fresh GLWE/GGSW mask rows make the next mask modulo low ring potentially uniform: if at least one digit polynomial multiplying a fresh row mask is a unit in R_p, then that mask contribution is uniform. This is conditional, not a claim about every key or a computational lower bound.

## Reproducible toy AP/CRT test
[TEST] b073_crt_reuse_gate.py, SHA256 47ed50df2fe3fdf441ae5265e70ec43b6b00808b453ff10e27d46ba290b9efa4; JSON SHA256 a558d89c2357ed17410904d2d783710a233ed41c2c3cc1b683271afe173653d1. Full BOOT_B073_handoff.zip.
R=Z_186337[X]/(X^8+1), p17, q1=97,q2=113, both high NTT-admissible (1 mod16), idempotents w=(97971,44523), GLWE k1, randomized ternary secret, uniform masks, per-row primitive errors ±1/0, source-shaped approximate-CRT AP-GGSW encryption of -σ(s)μ and μ, exact modular polynomial operations.

2500/2500 full-range exact CRT decomposition bounded by 8; 2500/2500 same-input automorphism-equivariance of digit vectors and reconstruction.
600 independently sampled AP transformations: all decryption phase and coefficientwise error recurrence checks PASS. Adjacent-step cached old correction vs actual new correction only 570/9600 coefficients match (5.9375% vs 1/17 ~5.8824%), and 0/600 entire GLWE mask/body correction vectors match. Fresh key resampling changes output mask low residue 600/600 tested draws.
12000 independent stale-correction scalar reconstructions: wrong absolute error median 43849, empirical p95 87689, while correct reconstruction max error 8; deterministic x'=0,r=1 yields -43843.

THIS IS A SMALL TOY: no 128-bit security estimate, native AP implementation, true DFR, measured runtime, or universal bound on stateful CRT schemes.

## Cost and novelty decision
FAIL direct stale-low-correction caching: source epsilon no longer holds across changing AP accumulator, even before considering security/performance. The low residue of the CURRENT output must be derived via some operation (direct low-CRT update, new communication, or a fundamentally different representation). Existing Bernard–Joye CRT-encoded accumulator already keeps low-unit residues updated. Same-input automorphism reuse is algebraically valid but existing hoisting and not demonstrated to reduce full pipeline NTT count.

STATUS FAIL_CROSS_STEP_LOW_CRT_REUSE / PASS_SAME_INPUT_AUTOMORPHISM_EQUIVARIANCE.
RESULT Exact source-special-case proof and reproducible AP-GLWE toy counterexample. No publishable new primitive.
NEXT_TEST B074 NOT STARTED: ONE new representation-level candidate, not stale caching: a securely maintained low-CRT shadow channel for each accumulator with a real reduction in NTT/external products beyond existing BJ Algorithm 3; first test exact dataflow and security with independent uniform BSK masks. Reject if just a duplicate of existing CRT maintenance or requires low-ring restricted public masks (B057 leakage concerns).
STATE_UPDATE NO: Existing findings/boot-STATE.md lists 187967 bytes, but Research GitHub Notes read_repo_file returns {}; preserve instead of overwrite. Append only B073 finding. SHIP unchanged.