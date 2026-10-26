# PURE-FHE · P0-PRESCOUT-28 — Aggregated Key-Switching (AKS) versus GCKKS Step7 unused-slot noise

Date: 2026-10-26 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: GCKKS_HIGH_PRECISION_BOOTSTRAPPING
PREVIOUS: P0-PRESCOUT-27 (findings/pure-fhe-p0-gckks2600-bsgs-fixed-noise-rotation-frontier-gate-2026-10-26.md)
STATUS: FAIL_UNMODIFIED_NOISE_PROOF_TRANSFER / PASS_FUNCTIONAL_RLWE_INTERFACE / NOT_ESTABLISHED_PUBLISHABLE_MECHANISM
NOVELTY: NOT_ESTABLISHED; general AKS-to-StC transfer explicitly acknowledged in prior art
CODEX: NOT_RUN; no GPU/native/server or large implementation
OTHER_TRACKS: UNCHANGED; no edits to global STATE.md

## Single H28 / decisive test
Hypothesis: Replacing regular masked rotations and rescaling in ePrint 2026/2600 GCKKS Step7 by Yan et al.'s AKS (ePrint 2025/1403) **automatically inherits** the published GCKKS Lemma2 / §5.3 normalized unused-slot noise upper bound, with no new source-dependent terms, and offers a previously unexploited structural mechanism.
Cheapest test: read author AKS Theorem2 and its exact Appendix C error formula plus GCKKS pp8,14–15,22–23; compare at one unused slot the order KS→PlainMult→Rescale versus the fused AKS key (evaluation-key error attenuation). Also assess first-party prior-art overlap / key count.

## [FACT] Primary-source provenance
* Yan–Zeng–Cao–Song–Wang, Faster Bootstrapping for CKKS with Less Modulus Consumption, ePrint2025/1403, cached page-aware **full PDF 51 pages** via GitHub Notes get_eprint_paper; mirror github.com/arturo-kong/IACR-eprint-mirror/blob/master/2025/1403.pdf, SHA256 784db16f5a3f7c79c68c52f0a99e03c8ca7ce3e4c06824736f5fd4dfff1f5c29. PDF VERSION_UNVERIFIED; physical pp16–22 §4, p26–27 §6.3, pp39–41 Appendix C were directly read. Its author-first-party https://ckks.org/blog/2026/less-mod-ckks/ agrees on broad claims and published June29 2026. Its §4.2 Theorem2 fuses per-diagonal plaintext multiplication, KS and Rescale via plaintext-weighted evaluation keys; sparse diagonal count ≤64 in its efficient regime. It drops BSGS and increases key storage in AKS-alone. Section6.3 **explicitly includes additional StC matrices** among places AKS may be applied with time-memory tradeoff. LCR+AKS is a different, first-CtS-after-ModRaise trick using small-lift coefficients, NOT a default extra level-saving at GCKKS Step7.
* GCKKS Ma–Liu–Wang–Wang ePrint2026/2600 supplied original PDF SHA 8db712155d087284d21e924623496bc48e36eb72; physical p8: GCKKS HomAdd/Rescale/PMult/KeySwitch use CKKS RLWE arithmetic and k-compatible rotations by rk/4 that stabilize F; p14–15 Lemma2: |Dec_F(c)(ξ)|≤K|F(ξ)| on unused slots; p22–23 §5.3: Step7 remaining partial StC has L=2N/k useful slots, plaintext diagonal κ_ij at unused ξ bounded by aξ Brnd, aξ=|F(ξ)|, and normalized BSGS map g_BSGS,r(B)=(L Brnd/r)(B+Bks)+(L/g)Bks+Bms. Thus original Step7 already includes an outer KS term independent of plaintext masks after division; do not claim ALL standard BSGS KS noise is mask-attenuated.
* Focused 2026/2531 full revised source remains unavailable and irrelevant for claiming any AKS new mechanism; no paper bug alleged.

## [DERIVATION] Functional algebraic compatibility
A k-compliant GCKKS automorphism φ fixes F and preserves the type of each slot. AKS is an identity in the underlying RLWE decryption relation replacing first KS then multiply by public plaintext m and Rescale with a modified key encrypting (P/qℓ)m s1 under switched key. Multiplying its underlying equality by the fixed F produces the same ideal GCKKS decoded useful-slot function. Therefore no generic algebraic impossibility / nonunit inverse obstruction to AKS itself was found. It does require precomputing m-dependent evaluation keys for each diagonal / level and rechecking scale, modulus and normalized unused noise.

## [FACT + DERIVATION] A source-exact mismatch in key error propagation
Yan et al. Appendix C p41 explicitly obtains underlying CKKS error:
 e_AKS = (m/qℓ)e' + (1/P) Σ_j [c1]_{Dj}(r_j+e_j) + r'_0 + r'_1 s2 + r'_2.
In particular key-encryption errors e_j enter in a term with NO multiplicative (m/qℓ) attenuation. Key-preprocessing rounding r_j may itself depend on m, but the fresh eval-key errors e_j do not.
By contrast, with a standard KeySwitch that introduces bottom-RLWE error η, then multiply by plaintext m and Rescale qℓ, its KS-introduced contribution is (m/qℓ)η (ignoring later rounding). The AKS key-related contribution is η_AKS, independent of how tiny m(ξ) may be at an unused slot.
Under F-decryption, the decoded error is multiplied by F(ξ) for both algorithms, and normalization by |F(ξ)| removes this outer F factor. So the missing plaintext-mask attenuation survives in normalized unused-slot analysis.
At a single unused embedding ξ with m(ξ)≈aξ Brnd small, standard pre-mask KS contribution has bound proportional to |m(ξ)|/qℓ; AKS requires an independent eval-key-noise term / certificate. This is a **failure of automatic transfer of the particular noise proof**, not evidence of wrong AKS correctness or certain noise blow-up: exact variances, special modulus P, correlated keys, extra rounding, and whether original BSGS's outer KS noise disappears all matter. Do not claim AKS's total variance must be worse.
Toy diagnostic (symbolic, not native): setting identical pre- and post-fusion key-error amplitudes E with m(ξ)=1 and qℓ=1024 gives ordinary contribution E/1024 vs an AKS contribution E; this only illustrates *missing structural attenuation*, not actual matched-parameter performance. m=0 in an ideal slot is also only a diagnostic, not an exact integral full-ring projector.

## [DERIVATION] Limited AKS efficiency regime and key accounting
If Step7's remaining linear transformation is treated as a single dense L-diagonal map, e.g. N=65536,k=256 => L=512, AKS-alone applies ≈L−1 weighted rotation keys (511 if every diagonal nonzero), while BSGS group g=32 needs ≈g+L/g−2=46 ordinary rotation keys as a count proxy; source 2025/1403 §4.2 compares unfavorable computation for diagonal counts ≥128, so *direct dense AKS* has no demonstrated runtime/key advantage. These are structural key *counts*, not measured byte size, peak memory, or whole bootstrap runtime, and AKS weighted keys may need multiple instances for different m/levels. Splitting the transform into ≤64-diagonal factors might restore AKS efficient scope, but introduces extra factors/levels, transform rearrangement and noise budget that must be charged end-to-end. Mere AKS on StC was already claimed in §6.3 of 2025/1403.

## [SPECULATION] Mechanisms and value gate
A new approach could potentially suppress the additional AKS key-error floor using shaped/structured eval-key error or a special representation of F, but such a proposal MUST prove key indistinguishability under a valid RLWE assumption, full correctness, security, F-invariant compatible rotations, unused-slot tail bound, key memory and RNS/modulus savings. F-shaped error is NOT automatically safe and a loss of error entropy/security may kill it. No mechanism was proposed as correct this round. Simply tuning P/K or factorization may suffice and would be existing parameter engineering, not a crypto paper.
Given repeated unsuccessful novelty scouts, park generic 'apply AKS to GCKKS Step7'. The only bounded next test worth doing before pursuing more algorithms is check whether the AKS Appendix C eval-key term, combined with the original GCKKS §5.3 outer BSGS noise and realistic parameter choices, actually creates a gap that cannot be resolved by ordinary adjustment of P, g, r, transform factorization and key storage. If ordinary retuning suffices, KILL. Do not pursue candidate without this first-pass counterfactual.

END_OF_ITERATION
STATUS: FAIL_DROP_IN_NOISE_PROOF_TRANSFER / PASS_FUNCTIONAL_ALGEBRA / NOVELTY_NOT_ESTABLISHED
RESULT: Exact AKS Appendix C error term lacks m/qℓ attenuation on evaluation-key noise; source already generalizes AKS to StC, and large dense Step7 is outside efficient sparse scope.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: Source-faithful minimal no-new-mechanism baseline: compare GCKKS original BSGS normalized outer-KS term with an AKS ≤64-diagonal factorization and check whether adjusting special modulus P / r / K is sufficient before any construction. If no nontrivial obstruction remains, KILL/PARK and prioritize other independent PURE-FHE gaps.
STATE_UPDATE: YES (single isolated PURE-FHE finding only). Global STATE.md and other tracks untouched.
CODEX_REQUIRED: NO; all native/gpu/code changes pending explicit PI authorization.
