# BOOT B015 — Reduced-T selector compatibility gate

TRACK_ID: BOOT
ITERATION: B015
DATE: 2026-10-19
STATUS: FAIL_BASELINE_NOISE_RATIO / FAIL_DIRECT_COST_ADVANTAGE / RECALIBRATED_SECURITY_UNCLEAR
STATE_UPDATE: YES

## Primary hypothesis
Can the rank-one squared Mat-MGSW of ePrint 2025/1711 replace ePrint 2025/686's concrete one-level GSW selectors, using Q<T<=Q², while preserving the original relative key-noise rate, low decryption failure, and lower transform/key-storage cost?

## Verified sources
[FACT] ePrint 2025/686, PDF physical p.23 Table 3: FBS1 N=2048, h=512, Q=2^64, single-level approximate gadget beta=2^23, q/sigma=2^50; FBS2 N=8192, h=512, beta=2^22, q/sigma=2^51. Table 4's larger gadget levels refer to a DIFFERENT key-switching key. Appendix B, p.33 Eq.(6), gives CMUX variance proxy.
[FACT] ePrint 2025/1711, PDF pp.11-15, scale Mat-MGSW bit-message signal approximately T/Q, external-product error identity of Lemma 3.4, and stronger sufficient condition Delta Q²<T in Cor.3.5. Section 3.3 provides transform/product counts. Both research-MCP PDF mirrors identity checked; versions unverified.

## Minimum information-theoretic falsifier
[DERIVATION; independent discrete Gaussian coefficient model] For rank-one squared Mat-MGSW encrypting selector b∈{0,1}, conditioned on sparse ternary secret S and uniform mask A, the signal-bearing top row has distribution E+b*r(1,S) modulo T, with integer r=round(T/Q), independently sampled integer discrete-Gaussian coefficients E of width s. Write sigma_T=s/sqrt(2*pi). With h=||S||²=512, the two conditional distributions differ by integer vector mu=r(1,S), with ||mu||=r*sqrt(513).
Integer discrete Gaussian translated by mu has exact KL divergence pi*||mu||²/s². Modular reduction cannot increase KL or total variation. Pinsker yields TV<=r*sqrt(513)/(2*sigma_T). With alpha_T=sigma_T/T and T>Q, r<=T/Q+1/2, so TV<=1.5*sqrt(513)/(2*Q*alpha_T).
At the original relative noise ratio alpha_T=2^-50 (FBS1), TV<=0.001036812. At 2^-51 (FBS2), TV<=0.002073624. Even when the secret is known to the distinguisher, the bit is nearly statistically indistinguishable. A reliable fixed-input CMUX producing two distinct, decodable outputs according to b would distinguish b with advantage approaching 1, contradicting these bounds by data processing. Thus **retaining original relative noise is not compatible with reliable selector CMUX under this explicit Gaussian model** for any T>Q. This does not refute all smaller-alpha schemes or arbitrary alternative encryption distributions.

A reference integer-Gaussian KL calculation at width s=3, shift 1 gives 0.3490658503988659, exactly pi/9. This is arithmetic validation, not native FHE.

## Independent numerical/noise proxy gate
[DERIVATION] The key-error term of squared external product is (Q/T)*E_C*c. Source Lemma3.4 averaged coefficient bound is approximately sigma_key <= Q²*alpha_T*sqrt(N) for rank-one. Original 686 Appendix B Eq.(6), omitting prior input noise, provides V_GSW≈2*N*(beta/2)^2*sigma_Q^2+((1+h)/12)*(Q/beta)^2 for ell=1,k=1.
FBS1: log2(sqrt(V_GSW))=43.77344723; log2(sigma_squared,alpha=2^-50)=83.5; difference 39.72655 bits. To have even the squared key-error bound below original GSW's proxy needs alpha_T ≲2^-89.72655.
FBS2: corresponding logs are 44.71313238 versus 83.5, difference 38.78687; alpha_T ≲2^-89.78687.
These source-derived quantities are conservative sufficient-proxy calculations, not exact real DFR or actual measured variances. If one CHOOSES sigma_T≈8 absolute, such alpha requires T around 93 bits, which lies in (Q,Q²) but has much smaller relative error than original and cannot inherit the original lattice security estimate. No estimator run: DO NOT claim it secure or insecure.

## Fixed-shape cost gate
[FACT/DERIVATION] Both 686's genuine ell=1 GSW selector and 1711's k=r=1 squared Mat-MGSW have four ring-polynomial coefficients per key, four transforms and four pointwise ring products per external product. Squared also performs coefficientwise Q/T scaling and rounding. At the same ring N, ANY T>Q needs >64-bit coefficient representation vs Q=2^64; 64-bit limb storage requires at least two limbs for T, versus one for Q. No direct operation-count or uncompressed key-bit saving exists, although custom kernels, compression or entirely redesigned parameters might alter actual execution cost. No matched benchmark, joint security estimate or end-to-end DFR.

## Decision and next test
RESULT: Original relative-noise Reduced-T proposal fails by exact statistical-distance reasoning in the standard independent discrete-Gaussian model; changing T alone cannot repair it. The original single-level key is already minimal in gadget rows; same-shape squared variant offers no direct raw cost savings. Lower alpha and altered moduli are separate, security-unverified proposals rather than a validated optimization.
DECISION: PARK this squared-MPmul direct-substitution branch, without declaring all new constructions impossible.
NEXT_TEST B016: Examine 2025/686 MPmul and 2023/958 block-binary key idea. One primary hypothesis: can two consecutive encrypted exponent bits be combined into one-hot block selection to save an entire n-output CMUX round? Cheapest falsifier: expand the two-bit controlled negacyclic rotation and check whether a nonzero b0*b1 cross-term forces at least three selector-dependent products in the original GSW primitive. Check source and prior art before claims.
STATE_UPDATE: YES. BOOT only.