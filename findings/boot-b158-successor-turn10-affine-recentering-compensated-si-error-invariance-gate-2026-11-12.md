# BOOT / B158_OVERALL — Successor Research Turn 10/25
Date: 2026-11-12 Asia/Singapore
Phase: PROBLEM_SELECTION
Candidate: boot-b158-compensated-public-affine-si-recentering-v1
Status: PARKED / FAIL_IDEAL_TENSOR_ERROR_CONTRACTION / FAIL_PAPER_VALUE_PREFLIGHT
Native/Codex task: NONE; no native task launched.

## Authority and provenance
TRACK_ID BOOT; ACTIVE_SUBLINE B158_OVERALL; entering durable candidate UNKNOWN, backups NONE. Independently read GitHub repository:
- findings/boot-b158-successor-turn9-message-plateau-interpolation-leading-degree-gate-2026-11-12.md, Git blob 013eb14b560360a7ffcb8869226535655cc9cafe, PARKED;
- findings/boot-B175-hybrid-frontier-research-value-ceiling-2026-10-29.md, Git blob 8923388e3e21796a2787b5b7043e2a62bbdf3eaa, conditional hybrid value ceiling low and no native correction;
- findings/boot-B175-source-level-si-error-bounds-2026-10-29.md, Git blob c75aa60e080b28b688de7ee8859c5df4d1951c02, aggregate E_tref dominates;
- findings/boot-B175-public-mask-convolution-screen-2026-10-29.md, Git blob 98cf77cd70f589812f48fe904e0d4f8c2c86eb09, public mask ciphertext residual multiplication can add 17–18 required bits on saved healthy operands;
- findings/boot-B175-common-lineage-gauge-accessibility-2026-10-29.md, Git blob 606b4a7708e03c0f2d5169e11a40e10921e27670, exact secret-dependent gauge not public;
- B175 original native archive SHA256 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa, final pointwise required bits664 vs L18 bitlength649, mismatches32767/32768.
Lattigo v6.2.0 is pinned. This proposal differs from earlier CLOSED reciprocal public-unit preconditioners (multiplicative scaling by invertible operators), centered Q->QMul basis extension, secret-lineage gauge, modulus raising, trace projection, RNS quantizer and multi-LUT packing. The tested mechanism is an additive PUBLIC affine shift of the second operand and exact compensation, not a change to the ciphertext secret or zero rerandomization.

## Precise research pre-registration
QUESTION: For B175 A=LT8, B=GROUPED, can a public plaintext offset v, applied as B->B-v and compensated after final SI by +v*A, contract the dominant decryption-phase tensor error at fixed Q by ~16 required bits with exact arbitrary-input output semantics and paper-level value?
CURRENT_BELIEF: The ideal unrounded tensor-phase error after compensated affine recentering is IDENTICAL to the original error for all public offsets; possible effects are confined to representation-dependent centered lifts/Q-carry, exact scale conversion, rounding and their interplay. No source-backed carry-contraction or DFR mechanism currently exists.
CHEAPEST_DECISIVE_TEST: In the ideal decrypted-phase product model, expand the errors for original and recentered/compensated products, check exact equality for arbitrary messages/noises/public offsets, then score optimistic new ct-pt/ct-add costs and relation to B175 dominant residual. No native.
IF_PASS: If there is an identified nontrivial invariant/source rule that shifts or cancels the dominant tensor/reference term without reintroducing it in compensation and survives complete scale/carry correctness, admit ACTIVE for source audit then correctness/noise/DFR/whole-cost testing.
IF_FAIL: If compensation exactly restores the original ideal tensor error and the remaining representation-dependent effect has no grounded useful >=16-bit contraction nor independent novelty, PARK this affine-only candidate.
IF_UNCLEAR: If exact Lattigo SI quotient/carry interaction with offset cannot be determined from saved input residuals, explicitly retain it UNKNOWN, but do not claim a noise rescue or authorize native random offset sweeps.
WHICH_PAPER_GATE_CHANGES: full message correctness and dominant tensor/noise mechanism, then source feasibility and value.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: A compensated offset is worth implementation only if it really suppresses dominant E_tref, not if a correction term restores the identical plaintext-times-noise and noise-times-noise terms while incurring additional public linear work.

## Conditional exact plaintext and ideal noise algebra
Use commutative ring over integers before reduction/quantization; write ideal decrypted phases A=M_A+e_A and B=M_B+e_B, where M_A,M_B are exact ideal plaintext-embedding reference elements and e_A,e_B their decryption noise. Let v be ANY public ring/plaintext offset with exact compatible embedding, and consider
 C_v := A*(B-v) + v*A.
The message identity C_v=A*B holds exactly before any rounding, for arbitrary values, including all source B174 test phases and the full domain if correctly implemented. With target message M_A M_B:
 residual_orig= A*B - M_A*M_B
  = M_A*e_B + M_B*e_A + e_A*e_B.
For the recentered product alone:
 residual_shifted_product = A*(B-v) - M_A*(M_B-v)
  = M_A*e_B + (M_B-v)*e_A + e_A*e_B.
The correction v*A has residual v*e_A. Hence
 residual_compensated= residual_shifted_product + v*e_A
  = M_A*e_B + M_B*e_A + e_A*e_B
  = residual_orig.
This is an EXACT polynomial/ring identity for all v, not merely a small-noise approximation. In particular, choosing v=1 when B175 CASE1 B's target plaintext equals 1 does not remove any dominant ideal product noise in the full compensated output; it relocates the e_A term to the correction.
For public vector/plaintext mask v (non-scalar ring element), the identity still holds by distributivity in the commutative ring. It cannot produce deterministic 2^16 contraction of ideal tensor-phase error by changing only additive centering.

## What does and does not follow for stock SI
The actual Lattigo v6.2.0 BGV MulRelinScaleInvariant does QMul-centered extension, componentwise quotient/rounding by Q-related factors, reference embedding and relinearization; ciphertext operations and corrections also carry metadata scales. These are not EXACT bilinear maps of arbitrary integer ciphertext representatives. Thus the above proves NO contraction in the ideal phase multiplication plus exact compensation, but does NOT prove the actual stock SI output ciphertext is bytewise/noise-identical for all v. Offset-dependent Q-multiple aliases, quantization cells, carry of re-encoding and level/scale matching could differ; their direction and distribution are UNKNOWN without actual prequantized tensor component evidence.
Crucially B175 source-level analysis bounds its standalone E_quant (<2^46) and E_relin (<2^22) versus ~2^647 observed dominant E_tref. An affine-only proposal whose ideal tensor error exactly survives offers no credible source-backed 16-bit gain; it would need an entirely new, independently proven offset-dependent component-lift/Q-carry contraction for the actual legal B175 tensor family, NOT merely a lucky choice of v in CASE1. Such a new representation mechanism is outside the tested affine-only candidate and would require explicit reopening proof/value.
No native source code was modified or benchmark launched. The actual B175 full 32768-slot terminal error and DFR remain as audited; no assertion that any recentered native result was tested.

## Source/cost/value gate
For a source-compatible method:
1. Build a PUBLIC plaintext encoding of v at B's actual scale (GROUPED=43178 mod T in CASE1), subtract from GROUPED. Source encoding must preserve exact plaintext and metadata;
2. Call exactly one final SI(ct-ct) on A and shifted B;
3. Compute matching scale-compatible public multiplication v*A and add it to SI output, possibly with an extra plaintext scale-adjustment to align with SI output scale 30059 (as audited). Exact v*A term must use SI-specific Q-related scale metadata, not naively add unmatched scales.
Thus at least one extra ct-pt multiply or equivalent public encoding/add and extra ciphertext adds plus possible scale conversion are required, while the 26 total ct-ct through pointwise and SI depth remain unchanged. All original relin/Galois keys still required; new keys potentially not required but verified cost UNKNOWN. Public masks can enlarge coefficient-residual norm (B175 mask audit). The computation is a textbook distributivity identity and source/value advantage is unsupported. No full-benchmark, DFR, cost or novelty PASS can be claimed.
Closest prior art: elementary affine polynomial shift and compensation/linearization, conventional BGV ciphertext-plaintext operations, and archived B175 hybrid distributive selector screens. NOVELTY_STATUS=PREFLIGHT, not an independently established exact literature COLLISION. The proposal's only credible potential is source-dependent carry geometry, which is unproven and has no 16-bit/DFR certificate; not admitted ACTIVE.

## Decision and scope
KILLER GATE1: Ideal semantic equality PASS_MATH; actual complete scale/carry correctness UNKNOWN/BLOCKED, and ideal noise-invariance FAIL for claimed improvement.
KILLER GATE2: Basic ct-pt/ciphertext addition and SI operator are standard, but scale alignment for exact offset compensation is NOT source-verified; no new distinct primitive.
KILLER GATE3: FAIL optimism as a standalone publication idea: unchanged ct-ct/depth/key frontier, extra operations, ideal dominant error unchanged, no source-backed Q-carry contraction or DFR.
STATUS=PARKED, NEW_MECHANISM=NO_CREDIBLE_NEW_MECHANISM for the affine-only trick. Does NOT assert absolute impossibility of novel carry-targeting affine-assisted implementations.
REOPEN_CONDITION: Provide source-authenticated coefficient-lift/carry identity for an actual public offset that provably contracts the WHOLE B175 dominant E_tref on complete legal-input family by ~16 required bits (or useful DFR), with exact scale/whole-output compensation, verified stock compatibility and all-in cost, plus novelty beyond distributivity and fixed CASE1 tuning. Do not merely rename the offset or sweep it on one native trace.
ELIMINATED_UNCERTAINTY: Can an exact compensated public affine offset by itself lower the B175 ideal plaintext×noise/noise×noise tensor-phase error? No; the final error polynomial is identical for ALL public offsets.
DECISION_CHANGED=true; no native or Codex, research_frontier_exhausted=false; continue other BOOT/B158_OVERALL problem selection.
