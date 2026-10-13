# Iteration 147 — SPRU single-slot Trace uses 8 DISTINCT rotation evaluation-key entries, not one repeatedly

**Date:** 2026-10-13. PI authorized with "好的，请继续" following I146. ONE precise source-grounded technical hypothesis / ONE exact key-index and key-map falsifier. Do NOT claim actual encrypted FHE performance, proof of independent Gaussian noises between successive rotations, or a source bug.

## Read before write / cited primary evidence
Read connected GitHub Notes `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` after I146 (SHA `05c065510f56de4223b96d344bed5840ff44a6ff`), `findings/spru-openfhe-v142-fixedauto-pretrace-mul-no-rescale-gate-iteration146.md`, and `findings/OPEN_RESEARCH_BRANCHES.md`. Current source paper Coron–Köstler, *Low-Latency Bootstrapping for CKKS using Roots of Unity*, ePrint **2025/651**, https://eprint.iacr.org/2025/651. Previously read complete 42-page Research MCP mirror (SHA256 `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6`, version vs latest official **UNVERIFIED**); source §3.5 defines Trace and Table2 N=32768,h=64. Author public OpenFHE `coron/spru_boot` uses patched **v1.4.2**. This iteration inspected actual author sources and precise upstream tagged code, not just theory.

## Primary hypothesis / decisive falsifier
[HYPOTHESIS] During the **eight** successive `EvalRotate` calls of source single-slot SPRU `Tr_{N/2→h}` with N32768,h64, the same rotation-key map entry (and thus same frozen evaluation-key encryption error polynomial) is **reused** in at least two different rounds; this reuse alone might introduce an offdiagonal inter-round KS covariance unexplained by I144/I145's ideal Trace model.

[FALSIFIER / ONE cheapest test] Extract exact `irot` sequence, exact author `EvalRotateKeyGen` indices, trace `EvalRotate(index)→FindAutomorphismIndex2nComplex(index,2N)→evalKeyMap.find(i)→KeySwitchInPlace` in OpenFHE v1.4.2, and assert whether any two trace rotations hit the SAME key-map index. Mathematical exact integer check at source N/h can kill hypothesis immediately; no Gaussian noise sampling needed if different map keys.

## Source inspection, ref-specific blobs and lines
**Author `coron/spru_boot`:**
- `src/single_slot.cpp` blob SHA `38d9fda8023ca0a06c5f4c9632802c83e4762c22`, lines79–85: `irot=N/4; nB=round(log2(B)); for k<nB-1: cadd=cadd+cc->EvalRotate(cadd,irot); irot=irot/2`. At source Table2 `B=N/h=512`, this iterates exactly eight shifts **8192,4096,2048,1024,512,256,128,64**. Lines87–92: later product loop `nh=log2(h)=6` uses next shifts **32,16,8,4,2,1**, all different; one *single* function execution uses fourteen distinct positive shift indices across these loops.
- `src/keygen.cpp` blob SHA `a367acf060fec5f85601d65974a2f1d989320f76`, lines33–43: `for (uint32_t i=1; i<=ringDim/4; i*=2) indexList.push_back(i);` and `EvalRotateKeyGen(keys.secretKey,indexList)`. At N32768 that pre-generates **14** rotation indices `{1,2,4,...,8192}` in the map.
**Exactly tagged upstream `openfheorg/openfhe-development` `ref=v1.4.2`:**
- `src/pke/include/cryptocontext.h` blob SHA `5837b5150900e3f03f5d29435713e45e712965e1`, lines2331–2334 `EvalRotate(...,index)` obtains `evalKeyMap=GetEvalAutomorphismKeyMap(ctKeyTag)` and calls `EvalAtIndex(ct,index,evalKeyMap)`; `EvalRotateKeyGen` calls `EvalAtIndexKeyGen`.
- `src/pke/lib/schemebase/base-leveledshe.cpp` SHA `c56d2a4a898adcea67e58c8a5f6056af913d2af3` lines~478–488: `EvalAtIndex` converts rotation index to automorphism index by `FindAutomorphismIndex`, calls `EvalAutomorphism`; lines~389–429: `evalKeyIterator=evalKeyMap.find(i)` and `KeySwitchInPlace(result, evalKeyIterator->second)`, then `AutomorphismTransform`; lines~365–385 `EvalAtIndexKeyGen` maps indices before `EvalAutomorphismKeyGen`, and latter uses separate `KeySwitchGen(privateKey,privateKeyPermuted)` for each distinct automorphism map index, storing in separate map entry.
- `src/pke/lib/scheme/ckksrns/ckksrns-leveledshe.cpp` SHA `237368624f41a485fcf920daffa2a5e785eb7fc7`, lines827–829: `FindAutomorphismIndex` dispatches `FindAutomorphismIndex2nComplex`.
- `src/core/lib/math/nbtheory2.cpp` SHA `5b330f45a39c2a938452d656bff0dcce32759b88`, lines243–262: for positive nonzero `index`, computes `5^index mod m`, for `m=2N=65536`.
- `src/pke/lib/keyswitch/keyswitch-hybrid.cpp` SHA `552fee8fc52c4ee12176e6b9a2ca279b079b7cbc`, lines~75–130: each single-key HYBRID `KeySwitchGenInternal` samples `DCRTPoly a(dug,...)` and `DCRTPoly e(dgg,...)` per Q partition under shared source/destination key material; evaluation-key samples are *frozen after key generation*, not newly sampled Gaussian noises per call. Existing same-secret dependencies and RNS rounding effects not modeled.

## Executed exact falsifier
```
N=32768; M=65536; h=64; B=N//h=512
trace_shifts=[N//4 >> i for i in range(log2(B)-1)]
            =[8192,4096,2048,1024,512,256,128,64]
trace_auto  =[pow(5,r,M) for r in trace_shifts]
            =[32769,49153,57345,61441,63489,31745,15873,7937]
assert len(set(trace_auto))==8
product_shifts=[32,16,8,4,2,1]
assert len(set(trace_auto+[pow(5,r,M) for r in product_shifts]))==14
assert set(trace_shifts+product_shifts)==set([1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192])
```
Local self-contained executed exact integer check `/mnt/data/i147_spru_rotation_key_mapping.py` SHA256 `2b9ad4aba694e058223a64d09cc0afba0b5c63832d4ab65d6f6f677765466cce`. **PASS:** all eight Trace keys distinct, and the six follow-on product rotation keys also distinct, matching 14 generated powers-of-two indices. No actual OpenFHE runtime/keys sampled; source call-graph and index arithmetic suffice to falsify *reuse of same map entry in one invocation*.

## Scientific boundaries / what this does and does not show

- [FAIL specific hypothesis] The **one bootstrap invocation's first eight Trace iterations DO NOT repeatedly use the same rotation-key entry**. Each shift has a distinct automorphism index and stored `EvalKey`; a hypothetical shared-key-error multiplication through exactly the same evalkey in different TRACE steps is not an accurate description.
- [PASS exact source map] Twelve? No: **8 Trace + 6 product =14 total different shifts**, all match author key generation and tagged upstream `FindAutomorphismIndex2nComplex` and `evalKeyMap.find(autoIndex)` mapping. Distinct keys at the map level does NOT imply statistically independent random variables unconditionally: all use the same source secret, potentially shared key material and evolving ciphertexts. Keygen samples `a,e` per distinct `KeySwitchGen` operation in code, but no joint covariance of actual KS error has been proved.
- [IMPORTANT] The **evaluation-key noise is fixed for each key after key generation**; `EvalRotate` does NOT freshly sample independent Gaussian noise on every call. **Across separate bootstrap executions**, a given rotation key map entry **IS reused**; our no-reuse statement concerns the first 8 (or 14 across loops) **different indices in one single-slot bootstrapping invocation**. Even in a single invocation, later ciphertext inputs depend on earlier steps, and ciphertext digit decompositions, modulus/RNS key switching and trace summations can create noise correlations. Any independent-rotation-error assumption still requires separate conditioning/argument.
- [NOT DONE] No OpenFHE ciphertext sample, secure parameters, KS error joint covariance or actual 14-bit Table2 precision analysis. No source bug/security exploit or algorithmic contribution. This is low-novelty negative source audit; do not extend it to all CKKS traces or multi-slot implementation.

## End of iteration

**STATUS:** **FAIL_SAME_EVALKEY_REUSED_ACROSS_EIGHT_TRACE_ROTATIONS / PASS_DISTINCT_AUTHOR_SOURCE_KEYMAP_INDICES / UNCLEAR_ACTUAL_KS_ERROR_COVARIANCE / HUMAN_REVIEW**.
**RESULT:** Source N32768/h64 eight Trace rotations map to eight distinct `5^r mod65536` auto keys, generated separately and addressed via map. Hence simple "same evaluation-key error reused in 8 rounds" hypothesis is false for one invocation. Fixed keys across multiple executions and dependence of successive KS inputs remain; no fresh-per-call Gaussian assumption, no measured or proven covariance/speedup.
**NEXT_ACTION:** I148 only with human PI authorization. Recommend **PARK further elementary SPRU rotation-key reuse microaudits**, as I143–I147 mostly close naive proof shortcuts and are unlikely publishable. A materially distinct next SPRU hypothesis should derive ONE source-exact **HYBRID rotation KS joint error covariance conditional on a single fixed secret** including input-digit dependence/rounding, or test real matched OpenFHE encrypted traces with a novel parameter/noise improvement, not mere key-map indexing. Otherwise prioritize unresolved vFHE CRT common-scalar lookup soundness or another high-upside backlog target, without repeating archived I95/I136–138 fixes. No outreach/background work.
**STATE_UPDATE:** YES — corrects a material false implementation premise in I146's proposed next gate; link conclusion in backlog and checkpoint.
