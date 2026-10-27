# BOOT-B156-AUDIT — Independent audit of Codex FAIL_SECURITY_MODULUS

- Date: 2026-10-27
- TRACK_ID: BOOT
- Artifact: BOOT-B156-ONE-FBS-A2B-NATIVE.zip
- Artifact SHA-256: 7ae78aafe5fd4331a93f5d88653ae04473a47045669b1572ac52d1a547b3936d
- Audit status: RAW_ARTIFACT_INTEGRITY_PASS / BASELINE_PASS / CANDIDATE_PARAMETER_PROBE_VALID / FINAL_FAIL_LABEL_OVERRULED
- New decision: REOPEN_NATIVE_GATE

## Artifact integrity

MANIFEST.sha256 verifies for all files in the ZIP.

Baseline native run is internally consistent:
- source-faithful fhe-simd-alu import 0482dc2;
- N=65536;
- HEStd_128_classic;
- n=256;
- 256 words/ciphertext;
- two sequential FBTs;
- depth 28;
- Q=1450, P=240, QP=1690;
- 65536/65536 bits correct;
- max decoded bit error 0.0011852546;
- native A2B total 62.481726 s;
- native A2B excluding optional output reordering 48.994713 s;
- peak sampled memory 76.8 GiB.

The candidate parameter probe correctly computes:
- W=4096;
- 8 direct real LUTs;
- FBT depth 28;
- FBT output level 25;
- B152 tail depth 7.

## Why FAIL_SECURITY_MODULUS is not yet decisive

The artifact adds:

    outputPackingDepth = 1

and therefore tests candidate context depth 33 as the mandatory matched configuration.

This is too strong.

The original B156 instruction explicitly said:
"Pack/reorder output only as much as necessary to compare correctness. Do NOT spend significant time optimizing cosmetic output layout."

The source paper's Appendix C describes consecutive-bit output reordering as optional and implemented using plaintext masks, rotations, and additions. The baseline artifact itself separately reports:

    a2b_excluding_output_packing_seconds = 48.99471343 s

showing that correctness and A2B core output exist before this optional layout transformation.

Therefore a valid matched native comparison can use the native Boolean output layout for both arms and omit the optional repacking from both latency/depth paths.

## Depth-32 parameter point

The artifact's own exhaustive probe found:

- context depth = 32;
- Q towers = 33;
- Q = 1650 bits;
- HYBRID digits = 33;
- P = 60 bits;
- QP = 1710 bits.

The paper's reported 128-bit bound for this N/secret/error convention is approximately:

    QP <= 1746 bits.

Thus:

    1710 < 1746.

This candidate was not executed because the artifact treated changing HYBRID digits from baseline 8 to candidate 33 as non-matched.

That is not a valid security/packing reason to stop.

NumLargeDigits is a key-switch decomposition/performance parameter. Changing it:
- does not alter N;
- does not alter plaintext packing;
- does not alter the main secret distribution;
- does not weaken the security target;
- may materially affect key size, key-switch latency, and memory.

Those costs must be measured and reported. They are performance/system costs, not a reason to label the candidate cryptographically invalid.

## What remains unverified

The probe used HEStd_NotSet when enumerating depth-32 / 33-digit candidate points. It did not instantiate the exact

    depth=32,
    NumLargeDigits=33,
    N=65536,
    HEStd_128_classic

configuration.

Therefore the correct status is NOT PASS_SECURITY yet.

The next cheapest test is:
1. instantiate this exact point with OpenFHE HEStd_128_classic;
2. independently cross-check with the same LWE-estimator convention as the paper;
3. only if both pass, run the online candidate.

If OpenFHE rejects this exact 1710-bit point under the matched secret/error convention, then the security failure becomes decisive.

## Fair latency baseline

Because optional output repacking is removed from the candidate, the fair baseline for the next comparison is not 62.481726 s.

Use:

    baseline core A2B = 48.994713 s

which is the source baseline latency before optional output reordering.

Optionally report a second end-to-end number with both arms subjected to an equivalent final layout transform if a no-extra-level implementation exists.

## Scale-bit idea deferred

A possible additional repair is reducing candidate scale from 50 to 49 bits, since the packed depth-33 candidate misses the paper bound by only 14 bits.

Do NOT use this repair yet.

First test the cleaner depth-32/no-optional-repack configuration at the original 50-bit scale. Only consider 49-bit scale if the exact secure depth-32 point fails or if a packed-output variant is later required, and then re-run precision/correctness gates.

## Decision

Codex's raw parameter data are useful and the 1760-bit packed configuration genuinely fails the stated 1746-bit bound.

But the experiment's top-level STATUS: FAIL_SECURITY_MODULUS is overbroad because it elevated optional output reordering and fixed HYBRID decomposition count into mandatory matching constraints.

Canonical B156 audit status:

    FAIL_PACKED_VARIANT_SECURITY
    / UNPACKED_CORE_CANDIDATE_REMAINS_VIABLE
    / REOPEN_NATIVE_GATE

Next iteration: B157 exact secure depth-32 native falsification.
