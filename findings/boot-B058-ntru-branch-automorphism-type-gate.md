# BOOT-B058 — NTRU grouped blind rotation right-branch automorphism gate
DATE: 2026-10-20
TRACK_ID: BOOT
STATUS: FAIL_NAIVE_RIGHT_BRANCH_AUTOMORPHISM_CLOSURE / PASS_IDEAL_PRODUCT_REASSOCIATION / UNCLEAR_NEW_PRIMITIVE
SHIP: PAUSED. No other research track writes.

## Primary hypothesis
Using only Dai et al.'s GIPKeyGen and AutoKeyGen evaluation material, independently apply per-coordinate public automorphisms to unnormalized NTRU right-subtree factors and compose them in a balanced tree, instead of the n/l serial group-internal product chain. Claimed target: ideal depth g-1 -> ceil(log2 g), g=n/l; no new keys.

## Source provenance
[FACT] Dai, Xiang, Deng and Zhang, Accelerating MKFHE bootstrapping via parallel-friendly NTRU-based blind rotation, Cybersecurity 9:136 (2026), https://doi.org/10.1186/s42400-026-00563-w . Definition 5 takes NTRU'_f(u/f) on the left and NTRU'_f(v) on the right to output NTRU'_f(uv/f). GIPKeyGen makes one normalized first key per group and otherwise unnormalized keys. AutoKeyGen(t,f) publishes an encryption of f(X^t)/f(X). Within-group processing remains a sequential recurrence.
[FACT] Bernard and Joye, Bootstrapping (T)FHE Ciphertexts via Automorphisms, ASIACRYPT 2025, ePrint 2025/163; pp. 3-4, 14-16. Their automorphism-parametrized external product is GLWE-based, not an already valid NTRU right-operand type transform. Mirror PDF version unverified.

## Minimal algebraic falsifier
[DERIVATION] In noiseless ring notation define normalized L_f(u)=u/f, unnormalized R_f(v)=v, tau_t(X)=X^t and the formal existing AutoKey correction K_t=tau_t(f)/f. Then
tau_t(L_f(u))*K_t = tau_t(u)/f = L_f(tau_t(u))
but
tau_t(R_f(v))*K_t = tau_t(v)*tau_t(f)/f != R_f(tau_t(v))
for general f and t. Thus this same-key correction is not closed on independently transformed right branches.

[TOY] R=F_257[X]/(X^8+1), f=1+X invertible, t=3, v=X: expected R body X^3, transformed body X^5-X^4+X^3. Multiplying by f gives expected numerator X^4+X^3 versus transformed X^6+X^3. No ciphertext encryption or noise was simulated.
[TEST] Script b058_ntru_type_closure.py, SHA256 bd8272764084db6f6be40b1442795fcd530ffe25a01d9ea13cebb1852c58655e. Across 8 odd t in 1..15 and X^j, 0<=j<8: L closure 64/64 PASS; R closure under naive shared correction 8/64 PASS, 56/64 FAIL. Formal unweighted products L(u)*R(v)=L(uv), R(u)*R(v)=R(uv) work, so obstruction is per-factor automorphism/normalization, not plain polynomial multiplication associativity.

## Result and next test
This is a restricted no-go for the direct existing-key balanced-tree transform, not an impossibility theorem for all NTRU techniques. No security/noise/DFR/native-latency claim. Ideal group depths (g=4:3->2, g=8:7->3, g=16:15->4, g=32:31->5) are conditional, NOT accomplished circuits.
NEXT_TEST B059: propose ONE explicit same-f unnormalized right-operand automorphism primitive; check algebraic correctness, secret-key auxiliary material, security assumptions, extra noise and whether normalization consumes the entire product savings. Reject if no cost edge.
STATE_UPDATE NO: existing findings/boot-STATE.md read interface returns {}, so preserve instead of overwriting. B058 is recorded as new append-only findings file.
