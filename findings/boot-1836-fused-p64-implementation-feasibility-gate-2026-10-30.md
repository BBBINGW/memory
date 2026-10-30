# BOOT — 2026/1836 fused p64 implementation-feasibility gate

Date: 2026-10-30
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Session: 密码学 15.0 — Research Turn 11/25

Status:
PASS_CODE_LEVEL_FUSED_INPUT_CONSTRUCTION /
PASS_SPARSE_THI_P64_DISPATCH /
PASS_EXACT_CODE_LEVEL_FINAL_LEVEL_28 /
NO_IMPLEMENTATION_TYPE_OR_LEVEL_BLOCKER /
NATIVE_PATCH_REQUIRED_NEXT

## Parent durable state

Turn 9:
findings/boot-1836-fused-overflow-boundary-fbt-gate-2026-10-30.md
commit 5d0da2c41f8f4fd7e05347e9eac6f4dd9576bb95

Turn 10:
findings/boot-1836-fused-p64-numerical-conditioning-gate-2026-10-30.md
commit 1e6247f9225ceea52d3f7c55cfeb4399adc966eb

Parent result:
- prime A2BCLA static bootstrap count 5 -> 4;
- fused p=64 order-1 Sparse-THI depth 15;
- paper-level total 28 <= L=29;
- fused LUT coefficient/sensitivity conditioning comparable to current source LUTs;
- remaining uncertainty was whether the real author code can form and consume z=A'+32b without extra nonlinear work or level failure.

## Primary hypothesis

In the actual author implementation, the 6-bit fused input

z_i = A' + 32 b_i

can be constructed from the existing arbitrary-prime A2B dataflow with only level alignment, additions/doublings and scaling-factor metadata changes, and the resulting fused p=64 FBT outputs can be converted back into the exact candidate/symbol interface expected by current LCtoC and mux logic while staying inside L=29.

Cheapest falsifiers:
1. bitSum and ctOverflow live in incompatible layouts or cannot be aligned without an extra bootstrap;
2. scale alignment requires a real multiplication/rescale depth not accounted for;
3. Sparse-THI dispatch misidentifies the p=64 coefficient shape;
4. candidate digits cannot be reconstructed from fused symbol outputs without another nonlinear stage;
5. code-level final level exceeds L=29.

## Source provenance

Author repository:
RyanWei0224/FHE-ALU-ECDSA
commit 581846bf911b8e6bc94897d6567345066af22bed.

Relevant source files:
- src/pke/lib/scheme/ckksrns/z-fhe.cpp
- src/pke/lib/scheme/ckksrns/z-fhe-keygen.cpp
- src/pke/lib/scheme/ckksrns/z-leveledshe.cpp
- src/core/lib/math/hermite.cpp.

## 1. Exact baseline dataflow before prime tail

Inside EvalArithToBooleanAnyPrime for the close-prime secp256k1-p case:

- after the first decomposition/row-reduction and base LCtoC:
  bitSum is the canonical binary digit stream;
- source comments place bitSum at level 24 for the two-candidate close-prime path;
- ctOverflow contains the accumulated arithmetic overflow plus carry;
- source comments place ctOverflow at level 27.

The current code then:
1. broadcasts ctOverflow across the zN=256 word;
2. rotates it back to its original position;
3. subtracts a2bA0;
4. multiplies only the scaling-factor metadata by 2^a2bBits = 32;
5. runs the p=32 delta FBT.

Thus immediately before the current delta FBT, the plaintext in ctOverflow is exactly the bounded A' required by the fused construction.

## 2. bitSum and ctOverflow layouts are compatible

Both objects are CiphertextGroup pairs produced inside the same full-packing A2B pipeline.

The current code later aligns every delta-FBT candidate group to bitSum and adds them directly, so the implementation already relies on these two groups having the same logical full-packing word layout.

For secp256k1-p:
degree=zN=256, hence shiftedLayout=false.

Therefore no Curve25519-style one-slot layout correction is involved in the minimal target gate.

## 3. Level alignment is supported by existing helpers

LeveledZImpl::AdjustCiphertextToLevel permits moving a ciphertext only toward a larger consumed level.

bitSum: level 24
ctOverflow: level 27

so the legal direction is exactly what the fusion needs:

bitSum -> AdjustCiphertextToLevel(bitSum, 27).

AdjustCiphertextToLevel:
- drops the required towers;
- applies the scale-adjust scalar;
- performs the final mod-reduction;
- resets the ciphertext scaling factor to cryptoParams->GetScalingFactorBFP(targetLevel).

ctOverflow at level 27 was itself produced by the same Z-level arithmetic and EvalAddWithAdjustInPlace path, so after adjusting bitSum to level 27 the groups use the source target scale convention.

No modulus raise or bootstrap is needed for this alignment.

## 4. Constructing 32*b costs zero multiplicative levels

The current AnyPrime code already packs several Boolean ciphertext bits into one LUT input by repeated ciphertext doubling:

x <- x+x

followed by ciphertext addition, and only afterwards changes scaling-factor metadata by the target input modulus.

The exact same pattern can construct:

bit32 = 32 * bitSum

using five doublings.

These are additions only and do not consume a CKKS multiplicative level.

Then:

fusedInput = ctOverflow + bit32

gives the raw integer slot value:

A' + 32*b.

Finally:

fusedInput.scale <- fusedInput.scale * 64

uses the same metadata-normalization convention as:
- the source p=32 delta input;
- the current packed boundary input, which multiplies scaling-factor metadata by 2^(candidateCount+1).

So the fused FBT sees the intended input domain Z_64 without an extra ciphertext multiplication.

## 5. No scale-adjust obstruction

EvalAddWithAdjustInPlace already handles cross-level addition by adjusting the lower-level ciphertext to the higher consumed level.

At equal levels it requires almostEqual scaling factors.

The proposed safe implementation order is therefore:
1. clone bitSum;
2. AdjustCiphertextToLevel(bitSumClone, ctOverflow.level=27);
3. form 32*bitSumClone by repeated doubling;
4. add to ctOverflow before applying the new x64 input-modulus scale metadata.

This avoids attempting to add a p=64-normalized ciphertext to a p=2-normalized ciphertext.

## 6. Sparse-THI helper-format gate passes

GetHermiteTrigCoefficientsSparseTHI with p=64, order=1 creates

coefficientCount = ((2*1+1)*64)/2 + 1 = 97.

InferSparseTHIShape computes:
numerator = 97-1 = 96;
halfP = lowbit(96) = 32;
oddSpan = 96/32 = 3;
p = 2*32 = 64;
order = (3-1)/2 = 1.

The source generator places zero coefficients in every prohibited gap degree with degree mod 64 > 32, satisfying the dispatcher's structural check.

Therefore the existing SIMD Sparse-THI evaluator recognizes the fused coefficient sets natively as:

(p,order) = (64,1).

No evaluator API extension is needed.

## 7. Reconstructing candidates from fused outputs is linear

For each correction candidate k and slot i, fused FBT outputs the same two symbol indicators used by the current boundary LUT:

r_i^(k) = 1[s_i^(k)=1],
t_i^(k) = 1[s_i^(k)=2].

Current full-packing SIMD evaluation returns two ciphertext components per LUT function.

Before the existing code multiplies the t outputs by the imaginary unit for carry-symbol packing, form:

candidate_k[0] = r_k[0] + 2*t_k[0],
candidate_k[1] = r_k[1] + 2*t_k[1].

Since s in {0,1,2}:

s = r + 2t.

This uses only doubling and addition.

Then preserve the current symbol path:

symbol_k = r_k + i*t_k.

Thus one set of fused FBT outputs supplies BOTH:
- candidate digit ciphertexts consumed as ct_res by LCtoC;
- complex carry symbols consumed as y by LCtoC.

No extra LUT or multiplication depth is introduced.

## 8. Exact code-level output level

Concrete source parameter:
L=29, so numTowers=L+1=30.

For fused p=64 order-1:
GetFBTDepth = 15 from Turn 9/10.

Full FBT output level follows the same scheduler used by the current boundary FBT:

outputLevel = encTransformLevels + FBTDepth
            = 3 + 15
            = 18.

This reproduces the current source comment for the existing p=8 boundary FBT:
3 + 12 = level 15.

Now run internalMaskedLCtoCInplace for zN=256:

- internalCarryPropSubprocInplace performs log2(256)=8 multiply+ModReduce scan rounds:
  level 18 -> 26;
- merge/overflow public-mask multiplication plus ModReduce consumes one more level:
  level 26 -> 27;
- EvalAddWithAdjustInPlace adjusts candidate_k from level 18 to the level-27 carry correction.

Thus after parallel LCtoC:

candidates: level 27
carries:    level 27.

internalATBNewSwapFull performs one public-mask multiplication plus ModReduce:

result base: level 28.

Each final mux delta*carry product is formed from level-27 inputs and ModReduce'd once:

mux product: level 28.

They therefore add directly to the level-28 result.

Final fused AnyPrime result:

LEVEL 28.

Since L=29:

28 <= 29.

The implementation leaves one level of concrete CKKS headroom.

## 9. Comparison to current code path

Current close-prime path:
- base A2B portion;
- p=32 delta FBT;
- materialize candidate digit ciphertexts;
- pack candidate bits with bitSum;
- p=8 boundary FBT;
- LCtoC;
- mux.

Fused path:
- identical base A2B portion;
- align bitSum level 24 -> 27;
- form z=A'+32b;
- one p=64 fused FBT;
- linearly derive candidate digits and carry symbols;
- identical LCtoC;
- identical mux.

The removed intermediate representation is:

d^(k) ciphertexts materialized solely to be repacked with b and immediately bootstrapped again.

## 10. Verdict

PASS_CODE_LEVEL_FUSED_INPUT_CONSTRUCTION.
PASS_SPARSE_THI_P64_DISPATCH.
PASS_LINEAR_CANDIDATE_RECONSTRUCTION.
PASS_EXACT_CODE_LEVEL_FINAL_LEVEL_28.
NO_IMPLEMENTATION_TYPE_OR_LEVEL_BLOCKER.

Still unverified:
- actual compile/run correctness of the patch;
- finite-precision scale/noise behavior after bitSum level adjustment;
- decrypted bit parity;
- output logMaxNoise;
- CPU/GPU phase latency;
- evaluation-key delta;
- full novelty.

## Decision

KEEP as highest-priority BOOT survivor.

The static/source-level preconditions are now exhausted. The next useful test must be native; further paper-only manipulation of this exact fusion has sharply diminishing value.

Prepared native task:
TASK_ID: BOOT-1836-FUSED-P64-SECP256K1P-NATIVE-20261030-R12-01

Minimal native scope:
- base repo RyanWei0224/FHE-ALU-ECDSA at 581846bf911b8e6bc94897d6567345066af22bed;
- CPU first; do not run ECDSA;
- add a separate fused AnyPrime path behind a compile/runtime flag, preserving baseline;
- only A2B-P / secp256k1-p, zN=256, source L=29 parameters;
- generate p=64 fused LUTs by composing current correction-bit and packed-symbol semantics;
- construct z=A'+32b at level 27 as above;
- derive candidate_k=r+2t before complex symbol packing;
- reuse existing internalMaskedLCtoCInplace and final mux;
- run baseline and fused on the same deterministic/random input batch;
- require exact decrypted bit parity for every tested word;
- report output logMaxNoise baseline vs fused;
- enable DECOMP_TIME and report baseline delta-LUT + boundary-LUT versus fused-LUT time, carry-prop and mux separately;
- report end-to-end A2B-P latency;
- record compile revision, parameters, pass/fail counts and artifact hashes.

Predeclared interpretation:
- correctness mismatch => FAIL_NATIVE_CORRECTNESS and park;
- parity PASS but noise worsens by enough to threaten the source correctness margin => PARK_NOISE;
- parity/noise PASS but no meaningful latency reduction => PARK_VALUE;
- parity/noise PASS and material A2B-P latency reduction => PASS_NATIVE_VALUE, then perform novelty/prior-art gate before any expansion.

TOP_LEVEL_BOOT_FRONTIER_EXHAUSTED: false.
PENDING_PI_DECISIONS: none.
PENDING_CODEX_TASKS:
- BOOT-1836-FUSED-P64-SECP256K1P-NATIVE-20261030-R12-01.