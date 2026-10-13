# Iteration 146 — Source-exact SPRU FIXEDAUTO fresh bootsk × plaintext-mask EvalMult does NOT immediately rescale

**Date:** 2026-10-13. **PI authorization:** “好的，请继续” after I145. **ONE falsifiable hypothesis and ONE decisive tagged-source call-path/branch test**; no OpenFHE executable CKKS/precision simulation and no claims of original-paper error.

## Read before write

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` (after I145, GitHub blob SHA `cab7864db8fe0f323078551eb910962da158306d`), `findings/spru-conditional-pretrace-pk-shared-mask-spectral-covariance-iteration145.md` and long-term `findings/OPEN_RESEARCH_BRANCHES.md`. The full original Coron–Köstler SPRU source-paper ePrint **2025/651** https://eprint.iacr.org/2025/651 had previously been read in the current branch as 42 physical pages (Research MCP mirrored PDF SHA256 `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6`, latest official VERSION_UNVERIFIED); original §3.1 encrypts bootsk and §3.5 gives Trace. I143/I144/I145 established, separately: worst-case ideal Trace factor L; iid-coefficient ideal Trace per-slot RMS √L; conditional exact two-bootsk **shared public key** covariance zero if ciphertext masks are fixed and independent of encryption coins. I145 left open whether OpenFHE FIXEDAUTO's **actual ct×plaintext operation itself** introduces an RNS modulus-drop rounding term that invalidates the pre-Trace zero-covariance argument.

## One primary hypothesis / falsifier

**[HYPOTHESIS]** In the author's actual single-slot initial pre-Trace source call
```
esk1=Encrypt(pk,ptsk1); esk2=Encrypt(pk,ptsk2);
cmult1=EvalMult(esk1,MakeCKKSPackedPlaintext(v1));
cmult2=EvalMult(esk2,MakeCKKSPackedPlaintext(v2));
cadd=EvalAdd(cmult1,cmult2);
```
OpenFHE **v1.4.2 FIXEDAUTO necessarily executes ciphertext `ModReduceInternalInPlace` / nonlinear RNS rescale during one of these two initial ct×plaintext `EvalMult` calls**, which is an immediate possible source of NONZERO offdiagonal slot covariance not covered by I145's exact-product derivation.

**[FALSIFIER / one cheapest decisive test]** Read the author's precise code and **tagged** OpenFHE v1.4.2 definitions for `Encrypt`, `MakeCKKSPackedPlaintext`, `LeveledSHERNS::EvalMult(ConstPlaintext)`, `AdjustForMultInPlace`, `LeveledSHECKKSRNS::AdjustLevelsAndDepthToOneInPlace`, `EvalMultCoreInPlace`, `ModReduceInternalInPlace`, and `EvalMult+Add` metadata. Starting from source-provided degree/level defaults, follow exactly the guards to see whether any rescale path is taken **before** the original Trace. If none, HYPOTHESIS FAIL and a rounding-based covariance counterexample at this exact stage would be an irrelevant invented mechanism.

## Source code locations and verified blobs

**Author source** `coron/spru_boot`, `src/single_slot.cpp` blob SHA `38d9fda8023ca0a06c5f4c9632802c83e4762c22`, lines ~26–37 encrypt two `MakeCKKSPackedPlaintext` encoded split-secret keys using SAME pk; lines ~65–75 compute `cc->EvalMult(esk_i,cc->MakeCKKSPackedPlaintext(vi))`, `cc->EvalAdd(cmult1,cmult2)` then first rotation. `src/params.cpp` SHA `3237e54f65039ca27752ef45759e0c50691d6d42` selects **FIXEDAUTO**, first mod size60 and scaling mod size49. The author's patch `patches/openfhe-ckksrns-protected.patch` SHA `30e1c989726fc977ae318a0cd925ad0c49ce2429` modifies **only** `src/pke/include/scheme/ckksrns/ckksrns-fhe.h` and not relevant EvalMult/leveling files in vanilla v1.4.2.

**Tagged upstream OpenFHE** `openfheorg/openfhe-development` at **ref `v1.4.2`** (not current default branch):
- `src/pke/lib/schemerns/rns-pke.cpp` SHA `4e46c873112c617713a9b5bb4f70c5fd916b17c8` lines 49–50 and 65–66: freshly encrypted ciphertext `SetNoiseScaleDeg(1)`. Fresh encryption uses level0 RNS chain (no earlier computed level-drop in author's bootstrap keygen).
- `src/pke/include/cryptocontext.h` SHA `5837b5150900e3f03f5d29435713e45e712965e1` lines 1186–1187: `MakeCKKSPackedPlaintext(value, noiseScaleDeg=1, level=0, ...)`. `src/pke/include/encoding/plaintext.h` SHA `9548bb02fb2adc3d34bc13976b809a962db141ae` defaults `noiseScaleDeg=1, level=0`.
- `src/pke/lib/schemerns/rns-leveledshe.cpp` SHA `ddcc1a9eed0524f66d67de1e1300577a9ae24da8` lines 226–242: ciphertext×plaintext `EvalMultInPlace` creates `MorphPlaintext`, then `AdjustForMultInPlace(ciphertext,ctmorphed)`, then **`EvalMultCoreInPlace(ciphertext,pt_poly)`** and increments `NoiseScaleDeg` by 1. Lines 479–485: when scheme FIXEDAUTO, `AdjustForMultInPlace` calls `AdjustLevelsAndDepthToOneInPlace`. Same file lines 474–476: auto-scaling Add calls `AdjustLevelsAndDepthInPlace` for two ciphertexts.
- `src/pke/lib/scheme/ckksrns/ckksrns-leveledshe.cpp` SHA `237368624f41a485fcf920daffa2a5e785eb7fc7` lines 612–752: `AdjustLevelsAndDepthInPlace` only acts if levels differ or noise-scale depths differ. Lines 755–765: `AdjustLevelsAndDepthToOneInPlace` first calls the adjustment above; **only if result's depth == 2 then calls `ModReduceInternalInPlace` on both operands**. Fresh (level0,degree1) for ct and encoded pt gives no level/degree adjustment and depth stays1; hence no `ModReduceInternalInPlace` and no tower drop. Lines 147–151: derived ct×plaintext wrapper delegates to base and **only updates scale metadata** `SetScalingFactor(scf²)` (FIXEDAUTO), no hidden rounding there. Lines 162–185: real `ModReduceInternalInPlace` DOES call `cv[i].DropLastElementAndScale(...)` on each ciphertext component; thus it would have introduced rounding, but source guards exclude it here.
- `src/pke/lib/schemebase/base-leveledshe.cpp` SHA `c56d2a4a898adcea67e58c8a5f6056af913d2af3` lines 749–753: `EvalMultCoreInPlace` multiplies each ciphertext RNS ring component by the already-encoded plaintext polynomial `c*=pt`, no further rescale/rounding.
- `src/pke/lib/schemerns/rns-leveledshe.cpp` lines 402–477: when two ciphertexts are added in auto mode, level/degree alignment only. The two products have identical metadata level0,degree2, so initial `EvalAdd(cmult1,cmult2)` also needs no rescale. All of this is confined to the **first pre-Trace stage**; a later ct×ct `EvalMult` and full ciphertext rescale may use ModReduce, and the eight Trace `EvalRotate` calls involve key switching.

## Exact branch-state test

Performed one fully determined metadata/call-graph guard test in functions JavaScript, mirroring the above checked source comparisons (not claiming compiled execution):
```
stage                       ct level/degree  mask level/degree   ModReduce calls    output
esk1×newly encoded v1          (0,1)               (0,1)           0              (0,2)
esk2×newly encoded v2          (0,1)               (0,1)           0              (0,2)
cadd of both products          (0,2)               (0,2)           0              (0,2)
```
The first two rows were directly executed and asserted in a branch-model JS test; the Add row follows same-level/same-depth source branch. The result is a **source-call-path correctness statement**, not an actual modified OpenFHE run. No finite-field toy covariance was necessary: the target hypothesized rounding operation is not called at this point.

## Security/noise meaning and limits

**[FAIL the proposed immediate-rescale mechanism]** The initial `EvalMult(esk_i,MakeCKKSPackedPlaintext(vi))` in author's vanilla-tagged FIXEDAUTO setup **does not execute RNS `DropLastElementAndScale`**. Its arithmetic after encoding is exact DCRT-poly modular ring multiplication; before tracing the noise remains of form `m1η1+m2η2` **with m_i the actually encoded deterministic integer plaintext**, provided masks/secret/public key fixed and plaintext masks selected independently of fresh bootkey encryption coins. Hence I145's conditional zero-offdiagonal Hermitian covariance argument remains applicable to this particular stage after accounting for deterministic encoding; do not postulate an extra rescale noise at this stage.

**[CRITICAL CAVEATS]** Encoding `MakeCKKSPackedPlaintext` DOES quantize complex masks to integer polynomial and can introduce deterministic approximation error in the semantic plaintext. That is **not fresh random ciphertext-rescale rounding**; it can affect decoded message/precision even if covariance of centered new-encryption noise stays spectral diagonal. If input ciphertext is adaptively selected based on bootkey ciphertexts, m_i may depend on bootstrap encryption coins, breaking I145's conditional independence. Later **eight EvalRotate / key switches**, ct×ct `EvalMult`, mod switching/rescale, special δ, product tree and SlotsToCoeffs may add correlated / nonlinear error; none checked here. Full Table2 Δ~2^49, empirical ~14-bit precision, tails, secrecy and per-slot max error remain UNPROVED by I146.

**[NOVELTY]** This is a simple negative source-reproduction gate: the hypothesized rounding does not occur here. It is not a performance improvement, new covariance theorem, author flaw or publishable contribution. *Do not waste next turn constructing a rounded version of a multiplication path the source does not take.*

## End

**STATUS:** **FAIL_IMMEDIATE_FIXEDAUTO_RESCALING_AT_SPRU_PRETRACE_FRESH_BOOTKEY_EVALMULT / PASS_SOURCE_TAGGED_BRANCH_AUDIT / HUMAN_REVIEW_FULL_ROTATION_KS_AND_PRECISION**.
**RESULT:** Under author source inputs fresh ct(level0,degree1), plaintext mask(level0,degree1), OpenFHE v1.4.2 FIXEDAUTO `AdjustLevelsAndDepthToOneInPlace` sees equal metadata, so no `ModReduceInternalInPlace` and product is modular ring multiplication at same level, output degree2. Original `EvalAdd` also avoids rescale because both paths match. Encoding quantization is deterministic under fixed masks; it does not itself force nonzero cross-slot covariance of centered fresh bootkey encryption noise. Real later rotation-KS/rescale effects unstudied.
**NEXT_ACTION:** I147 only with PI authorization. Recommend PARK speculative pre-Trace FIXEDAUTO rounding mechanism. If SPRU is still the target, investigate ONE **real reused rotation key-switching** error-covariance or rescaling-at-ct×ct mechanism with tagged v1.4.2 code and a source-matched falsifier; do not just continue classic Fourier identities. Else prioritize a higher-novelty target from backlog (e.g. unresolved vFHE CRT common-index proof), respecting archived repairs. No background runs/outreach.
**STATE_UPDATE:** YES — closes specific source-level noise hypothesis and narrows true next error injection point.
