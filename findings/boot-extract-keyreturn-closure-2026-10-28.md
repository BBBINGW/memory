# BOOT — SampleExtract / key-return fusion closure

Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER_LEVEL_ONLY
CODEX: NOT_USED
NATIVE: NOT_RUN

## Authoritative BOOT state

LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE_GATE: B163_CORRECTED_B160_NOSCALE_SELECTOR_GATE
B163_STATUS: PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
DO_NOT_AUTO_RUN_CODEX: YES

B158_ALGEBRA: PASS
B158_CTCT_MULT_COUNT: OPTIMAL
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B158_NATIVE_FEASIBILITY: UNRESOLVED
B163: NOT_RUN

## Question

Can the standard FHEW/TFHE tail

    RLWE accumulator
      -> SampleExtract
      -> modulus switch
      -> LWE key switch

be structurally shortened by absorbing SampleExtract into the key-return operation?

## Observation 1 — SampleExtract itself is only a public linear reindexing

For an RLWE ciphertext (a(X),b(X)) under ring secret t(X), extracting coefficient 0 gives an LWE ciphertext under the coefficient vector of t.

At the message/noise level SampleExtract introduces no new cryptographic operation; it is a deterministic public coefficient permutation/sign pattern.

Therefore merely "fusing the loops" of SampleExtract and LWE key switching does not remove the expensive part:
- gadget decomposition of the extracted mask coefficients;
- multiplication/addition with the key-switching material.

It changes dataflow, not asymptotic cryptographic work.

## Observation 2 — TFHE functional key switching already absorbs public linear morphisms

Chillotti–Gama–Georgieva–Izabachène,
"TFHE: Fast Fully Homomorphic Encryption over the Torus",
ePrint 2018/421.

Section 4.1 explicitly generalizes key switching beyond key replacement:
- it switches between scalar and polynomial message spaces;
- it evaluates public or private Z-module linear morphisms during the key switch;
- public functional key switching can implement projections/permutations/packing-style linear maps.

Research MCP source:
ePrint 2018/421, physical pp.19-24,
mirror PDF SHA256
23fa887ff217f14a47763d6711d8c9304a392954751bee11799a223499d393cd
(version status VERSION_UNVERIFIED).

Hence the conceptual idea
    "do extraction's public linear map inside key switching"
is already within the original TFHE functional-key-switch framework.

## Observation 3 — moving key return BEFORE extraction is also prior art

Wang–Xiang–Zhang–Deng–Feng 2025,
"Improved FHE Bootstrapping and Its Applications in Discretized Neural Networks",
performs the key-return operation while the ciphertext is still in the NTRU/ring layer and extracts afterwards.

The construction aligns the target ring-secret coefficient vector with the original LWE secret padded with zeros, performs an NTRU-domain key switch to that target, and then sample-extracts.

This is stronger than an implementation-level fusion:
the expensive key return is reordered across extraction and moved into the ring domain.

Therefore:

    RING_KEY_RETURN_THEN_EXTRACT = PRIOR ART.

## Commutation viewpoint

Let E denote constant-coefficient SampleExtract at the plaintext/ciphertext-linear level.

Let KS_R denote a ring-domain key switch from t(X) to a target ring secret t'(X), and suppose the coefficient vector of t' is chosen so that its relevant extracted coordinates correspond to the desired LWE secret s.

Then the prior-art strategy realizes the commuting intent

    E after KS_R
instead of
    KS_L after E.

The precise ciphertext-noise distributions differ by construction, but the high-level stage-reordering goal is already established.

## Why no hidden asymptotic gain remains from "fusion"

Any direct fused Extract+LWE-KS using the same ordinary LWE KSK must still process the N extracted mask coefficients (or their gadget digits). SampleExtract contributes essentially no expensive secret-dependent computation to remove.

To obtain a real asymptotic/key-size gain one must change something deeper:
- secret structure,
- ring-domain key return,
- decomposition method,
- or the target ciphertext representation.

Those directions are already covered by existing work audited elsewhere in BOOT.

## Decision

SAMPLEEXTRACT_PLUS_LWE_KS_LOOP_FUSION:
    IMPLEMENTATION-LEVEL ONLY / LOW VALUE.

PUBLIC_LINEAR_EXTRACTION_INSIDE_FUNCTIONAL_KS:
    PRIOR ART (TFHE).

RING_KEY_RETURN_BEFORE_EXTRACTION:
    PRIOR ART (Wang et al. 2025).

GENERIC_EXTRACT_KEYRETURN_STAGE_FUSION:
    PARK.

NOVELTY:
    FAIL for the generic idea.

CODEX/NATIVE:
    NOT REQUIRED.

## Next structural scout

Move to the *input* side of blind rotation.

The remaining generic front-end stage is the modulus-switch / phase-to-rotation-index conversion:
    high-modulus LWE
      -> rounded rotation-domain LWE
      -> blind rotation.

Question:
Can the explicit rounding/modulus-switch stage be absorbed into a different rotation representation or accumulator geometry so that:
- no separate modulus-switch error is introduced;
- the blind rotation still uses a compact ring;
- and cost does not simply reappear as a larger ring or larger LUT?

This is only a scouting question; no positive claim is made.

B163 remains the highest native gate once Codex quota returns.
