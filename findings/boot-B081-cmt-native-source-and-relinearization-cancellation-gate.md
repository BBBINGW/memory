# BOOT-B081 — B052 CMT native-baseline availability + relin-cancellation gate

Date: 2026-10-20  
TRACK_ID: **BOOT**; SHIP paused  
**STATUS:** `PASS_EXACT_COST_CANCELLATION / BLOCKED_AUTHOR_CMT_NATIVE_SOURCE / FAIL_STANDALONE_NOVELTY / HUMAN_REVIEW`

## Primary falsifiable hypothesis

B052's 18-bit p=16 CMT non-symmetric split j=2 improves the *whole published CMT* merely by saving 3,840 ciphertext-ciphertext products relative to source j=3, without a comparable cost being transferred to MSD relinearization. First verify true published source availability; then model actual Section 7 scheduling to disprove/confirm an unqualified computational improvement, rather than making unmeasured native timing claims.

## Independently verified primary sources

1. Dumezy et al., *Evaluating Larger Lookup Tables using CKKS*, TCHES 2026(1), 559–591, ePrint2025/1301, https://eprint.iacr.org/2025/1301 ; original full 35-page PDF verified earlier, SHA256 048ba3ae4fe97eae0417138b816572b1c79b503727db54ce76576a4d38190b19 (version not verified). Physical p15 Alg.3 `KProduct`, p19 Alg.6 `CMT`, p20 Alg.7 CMT-FBT; physical p23–24 Section 7 explicitly fully relinearizes `ctKMSD` before public LUT multiplication and lazily treats last LSD products. p25 observes LUT scalar multiplication becomes bottleneck for large tables. Table3 p26 reports *author's* 18-bit original single-thread latency 1290.5 s (not our measurement). First-page footnote says author's CMT implementation available **upon request for research** and planned for OpenFHE v1.5.
2. **Original-author OpenFHE tracker:** https://github.com/openfheorg/openfhe-development/issues/1228 ; author Andreea Alexandru created July 28, 2026, title `Add the Large LUT evaluation method`; body: `Scheme CMT-FBT from https://eprint.iacr.org/2025/1301.`; observed OPEN on Oct20, 2026, milestone future 1.7.0, 0 comments. This is direct evidence it remains an outstanding upstream feature, not categorical proof all private branches lack code.
3. Official `openfheorg/openfhe-development` GitHub README version v1.6.1 released Oct9,2026. Its `src/pke/examples/functional-bootstrapping-ckks.cpp` SHA 6c8552473d927081d95d7af03c8fa23d34af39e6 and `src/pke/examples/CKKS_FUNCTIONAL_BOOTSTRAPING.md` SHA 9fd91561fe6c00a61de84e216b8c76db4cfc42b1 do NOT refer to `CMT`, `KProduct`, `Collapsed`, or the final CMT-FBT paper by code-name. The latter documents AKP and Fourier-extension FBT. Public author `jdumezy/sec-ckks` README describes early ~8-bit CKKS FBT + WIP tree, not verified paper 18-bit final CMT implementation. Official issue plus source restrict current native availability conclusion.
4. Prior art from B080: known FHE compiler data layout / weighted tensor contraction / matrix-chain scheduling including Fhelipe (2024). Rebracketing alone is not a new cryptographic primitive. The source already explicitly studies the same costs and optimized lazy relinearization.

## Minimal decisive gate: same KProduct work, reversed orientation

Source / B052 candidate (padded vectors; 5 radix-16 digits represent *logical* 18 bits; final high digit selector still physically length16; 18-bit logical LUT has 2^18 valid values; number of potential padded positions 16^5=2^20):

| Operator count | Original LSD3/MSD2 | B052 LSD2/MSD3 |
|--|--:|--:|
| LSD KProduct ct-ct multiplications | 4,352 | 256 |
| MSD KProduct ct-ct multiplications | 256 | 4,352 |
| **KProduct total** | **4,608** | **4,608** |
| Final lazy LSD-by-MSD ct-ct products | **4,096** | **256** |
| Overall counted ct-ct multiplications | **8,704** | **4,864** |
| Full relinearization of source Section7 MSD outputs | **256** | **4,096** |
| Physical complete MSD selector vector count | 256 | 4,096 |
| Public LUT scalar MulInt over 18-bit logically valid entries | 262,144 | 262,144 |
| Multiplicative depth of CMT | 3 | 3 |

Hence **saved final lazy multiplies = +3,840; additional full relin outputs = +3,840**. Both KProduct work totals are identical; no new homomorphic primitive is eliminated at that stage. Counts are exact *for this representation and source Section7 scheduling*. Note the naive physical padded LUT table would contain 2^20 positions, whereas the logical 18-bit function has 2^18 valid entries. We assume invalid public lookup coefficients can be zeros/skipped without discarding noisy encrypted selector ciphertexts; this step must be checked in the actual source. Since the number of publicly nonzero LUT entries is the same for both schedules, it cancels in this particular side-by-side comparison.

### Conditional weighted break-even

Let `c_lazy` denote a final ct-ct product's cost and `c_relin` denote the *full relinearization of one MSD selector ciphertext*, both at the actual RNS levels. Under the very strong assumption that all KProduct operations, the logical 2^18 scalar LUT operations, and all other terms have identical costs:

`C_B052 − C_original = 3840*(c_relin − c_lazy)`.

In THIS model the candidate is better only when `c_relin < c_lazy`. If `c_relin = c_lazy`, there is no gain at all from the 44.1% change of raw ct-ct count. If `c_relin > c_lazy`, candidate is worse, and some unequal RNS level or memory-specific advantage is required to rescue it. This is not an actual measured ratio: relin and lazy mul costs depend heavily on RNS limbs, NTT representation, modulus level and key switching. Source MSD depth changes 1→2, potentially affecting both RNS limb prices and available precision; before final Mul, automatic level matching/modulus dropping may also erase apparent per-MulInt differences.

The general honest cost relation is:

`ΔC = 3840*(c_relin−c_lazy) + ΔC_KProduct_RNS + 2^18*Δc_LUTscalar + ΔC_noise_rescale_memory_levels`.

ALL Δ terms except the first are unmeasured. Source paper's optimization already attempts to lower the limb count of LUT scalar work, so do not assume candidate's scalar path strictly dominates or that equal CMT multiplicative depth implies equal CKKS error.

Sensitivity toy with homogeneous per-ctct cost4 units, LUT scalar cost1 unit, zero other costs:

- relin/lazy=0.25: formal candidate speed factor 1.04032;
- relin/lazy=0.5: 1.0265;
- relin/lazy=1: 1.0000;
- relin/lazy=2: 0.95114 (candidate slower);
- relin/lazy=4: 0.86726 (candidate slower).

These are **pure cost model sensitivities, not measured performance**. None proves native speed.

## Native execution gate

The research container has no discovered OpenFHE build or author large-CMT executable, and the authoritative author implementation has not been fetched. `NATIVE_RESULTS: NOT_RUN`; `BASELINE: NOT_RUN`; `CANDIDATE: NOT_RUN`; exact number of native tests = 0. No CKKS precision, 128-bit estimator, failure probability, or end-to-end wallclock assertion is supported. Readiness BLOCKED on source. User can obtain implementation directly from authors; do not invent a substitute source nor spend long experiments on standalone modern OpenFHE AKP as a *CMT* reference.

## Independent test and reproduction

Script `b081_relinearization_cost_gate.py` deterministic, pure Python standard library: source-like Algorithm3 pair tree and Alg6 split for LUT 13–20 bits. All 17–20 full-padded cases verify same KProduct work, same depth, 3,840 saved late lazy multiplies and 3,840 extra right-side relinearizations. JSON `b081_results.json` includes source/candidate counts, logical vs padded LUT sizes, and explicit hypothetical sensitivity. No native timings.

## Decision

**FAIL unconditional "44% local multiplications saved means useful native CMT optimization" claim**: exact relinearization counts cancel the number saving under equal normalized costs. **BLOCKED final code and actual performance**. **FAIL stand-alone paper novelty** because known FHE contraction scheduling; opportunity remains as a software tuning observation only if tested against the author's actual source (which may incorporate it already).

**STOP** B052 in BOOT after B081 unless source is supplied or a distinct cryptographically substantive theorem/primitive is proposed. Do not continue B082 as speculative noise-aware DP without source/implementation. Suggested PI action if desired: request original TCHES CMT-FBT code, exact 18-bit OpenFHE parameters and revision from author; only then do one 18-bit same-security original/candidate full-FBT benchmark including FDD, CMT, SlotsToCoeffs, relin counts, levels, peak RSS and plaintext correctness. Otherwise prioritize NEW primitive search from independently credible source rather than B052 scheduling.

**STATE_UPDATE:** NO: existing `findings/boot-STATE.md` list succeeds but Notes read previously returned `{}` for 187,967-byte file. Do not overwrite. Only append B081 to isolated BOOT findings. SHIP paused.