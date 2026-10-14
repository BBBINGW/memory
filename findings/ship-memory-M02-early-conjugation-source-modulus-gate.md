# SHIP-M02 — Complex-paired SHIP masks: source-level early-conjugation modulus gate

**Date:** 2026-10-14. **Separate SHIP sequence:** SHIP-M02; **not** global I195 or vFHE I193/I194. PI explicitly authorized continuation with “好的，请继续”.
**STATUS:** **PASS narrow source-level absence-of-extra-level/extra-Galois-key obstruction**; **UNCLEAR actual CKKS correctness/noise, added latency, peak prepared memory, novelty**. No FHE benchmark or actual ciphertext was executed in this environment. No author communication.

## Read before write and concurrent state warning

Read in prescribed order: `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md`, and `findings/ship-memory-M01-complex-paired-selector-key-gate.md`.
**Important concurrency observation:** The latest GitHub `STATE.md` read at start of M02 has blob SHA `e4639c84f75b15a496d6f34dc78ff51097c3c637` and currently declares **vFHE I194 completed** / I195 not started, different from previous SHIP state snapshot. To avoid overwriting an independently advancing research conversation, DO NOT replace this active `STATE.md` in this SHIP round; persist SHIP-M02 in its own file and optional separate SHIP-specific pointer. No vFHE I193/I194 files modified.

**SHIP origin:** Cheon–Hanrot–Kim–Stehlé, `SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm`, EUROCRYPT 2025, ePrint 2025/784; original source §3.3, §4.1, §4.4 Alg.4, §5.1–5.4. Research MCP original 33pp mirror SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, official byte-parity `VERSION_UNVERIFIED`. Paper itself already explains auxiliary-P-saving column multiplication; we cannot label proposed early KS as an original technique.

**Pinned code:** independent `poulpy-fhe/poulpy` commit `250d4392656cd313f92ca66d96d8865702d39ddf`, NOT original HEaaN benchmark. Precisely fetched:
- `poulpy-ckks/src/layouts/ship/plan.rs` blob `364f4235253a3c76c70dfacf3ea24c5e69a2c3c2` — `raised_k(base2k)=roundUp(((tree_depth+2)*ld+log_budget_out),base2k)`, `tree_depth=ceil(log2(h+1))`.
- `poulpy-ckks/src/encoding/ship/coeff_enc.rs` blob `e0b5bb3e2cd5bb681a22b1798039061429ba17fe` — original public `pi` entries are **complex** CKKS plaintexts with `log_delta=ld` at `k_pi=ld+base2k`. They are built from public encrypted-bottom-mask coefficient residues; recomputing paired plaintext combinations at `ld` is allowed in principle but not coded.
- `poulpy-ckks/src/reference/ship/masking.rs` blob `91ba98e08ea7172b34c492d9fcc69ef18628820d` — masker computes `mul_pt_params_raw(acc.max_k,ld,raised_k-ld,pi.ld,pi.log_budget,pi.max_k)`, stamps scale `ld`, and sends convolution to `vec_znx_big_normalize`; consumes one DFT accumulator/IDFT per original masked sum.
- `poulpy-ckks/src/reference/mul.rs` — `mul_pt_params_raw` and `poulpy-ckks/src/error.rs` — `checked_mul_pt_log_budget=lhs_budget−rhs_log_delta`, provided sufficient budget. Thus a masking product at source inputs has **output budget `raised_k−2ld`**, output scale `ld`, effective ciphertext k `raised_k−ld`.
- `poulpy-ckks/src/reference/conjugate.rs` blob `4eb738484cb542cdea2a7ca2357182bd4295c5dd` — `ckks_conjugate_into_reference` uses GLWE automorphism and metadata `dst.log_budget=src.log_budget−offset`, where offset=0 if src.k==dst.k. It performs a key-switch, not free conjugation. API `poulpy-ckks/src/api/conjugate.rs` blob `b0b7bc6353de2e474e43bd3164d3b1e316d6afd6` explicitly states no **homomorphic capacity** loss at aligned k, not numerical noise-free.
- `poulpy-ckks/src/oep/derived/conjugate.rs` blob `5648b92b42f22471edda399821d63380879b0997`: retrieves existing Galois p=−1 key with input `src.k()` and applies automorphism.
- `poulpy-core/src/layouts/key_helpers.rs`: a bare prepared Galois key is returned **as stored** for any requested precision, with p checked; this is only a key **lookup** contract, not a formal bound on all reduced-precision numerical behavior.
- `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: source generator creates a dense-secret `gal_el=−1` automorphism key; `ShipKeySet::prepare` eagerly prepares it once; mask selectors at width `raised_k`. Original code already includes this key; selector complex packing needs no **new key identity**.
- `poulpy-ckks/src/test_suite/ship.rs` blob `a5e89638c430886e57c036e001093827293bfae0` uses `big=CKKSTestParams{k:raised_k,...}` and `conjugation_key:big.atk_layout()`; `poulpy-ckks/src/test_suite/mod.rs` blob `e59c9341591a29a0d7dcc602e2ecf4dc9f4edfdb` key `dnum_for_input(k)`, `k_aux=dsize*base2k+log_n`.
- `poulpy-ckks/src/reference/ship/bootstrap.rs` blob `edbec7d8ad60493d53aa5c11c842da1f30cff542` — masking occurs BEFORE per-support mux-rotation and product tree; original code conjugates the final root (or combined two roots) **ONCE** after tree. New scheme conjugates once **per support / output-half**, before these stages. This changes noise AND online KS cost.

## ONE primary technical hypothesis

[HYPOTHESIS] The M01 complex-pair reconstruction can be placed immediately after masking (before SHIP mux/product tree) **at the same source output scale/k** and using an **already resident Galois -1 key**, **without a new ciphertext-ciphertext multiplication level or extra source-width key object**. This is a narrow *necessary implementation-structure* hypothesis, NOT a guarantee of low latency, FHE correctness or 128-bit security.

[FALSIFIER / ONE TEST] Trace pinned implementation’s source key precision and source `masking → conjugate → mux` layout, compute exact `raised_k`, masker output k/scale/budget, existing conjugate key input coverage and `ckks_conjugate_into` metadata. A forced extra multiplication, insufficient existing key shape, or unavoidable output-k drop would FAIL this necessary gate. Avoid full benchmark or more hypotheses until this gate resolves.

## Decisive source-level test (performed)

Using the pinned `ShipPlan`, `mul_pt_params_raw`, `CKKSTestParams::atk_layout` equations with illustrative **Poulpy-compatible** values (not original paper LL14/HT15, not author-HEaaN measurements):

```
N=16384 (or N=32768), h=32, theta=4, base2k=52, ld=40,
log_budget_out=104, dsize=1, tree_depth=ceil(log2(33))=6.
raised_k = 52 * ceil((8*40+104)/52) = 468.
masked_budget = raised_k - 2*ld = 388.
masked_scale = ld = 40.
masked_effective_k = 388+40 = 428.
root_budget_after_six_muls = 388 - 6*40 = 148.
root_k = 148+40 = 188.
existing Galois key for -1: dnum=ceil(468/52)=9,
  k_aux=52+log2(N) = 66 (N16384) or 67 (N32768).
source prepared-mask CT count original per real half=4*h*theta=512;
proposed count=2*h*theta=256.
```

Thus `masked_k=428 < raised_k=468`. The same pre-existing high-width conjugation key was generated for source `raised_k=468` and already handles the original root at `k=188` via source key-lookup. There is **no obvious additional selector-key or missing Galois-element barrier** for a conjugation at `k=428`. With a result ciphertext allocated at `k=428` and same scale, `ckks_conjugate_into` uses offset 0 and stamps the same budget=388, scale=40; however the operation adds nonzero key-switch noise, not reflected by budget metadata.

The source's output after original masked sum is NOT a new independent rescale step in this torus model: the normalization and budget are handled by `ship_masking_accumulate`; a precise `RescaleP` textbook analogy should not be substituted for Poulpy's real API. Existing `pi` complex encodings can be replaced in principle with re-encodings of `P1−iP2` and `conj(P1)−i conj(P2)` at the SAME scale. This needs code changes but no extra ct-ct multiplicative level.

**Reproduction:** locally executed `/mnt/data/ship_m02_source_modulus_gate.py` (NOT accessible to GitHub Notes MCP); SHA256 `d60f80f0a33cb5b077788fec717885089e5d8fe5f0a55f475efefcaf7fc922ef`. Script prints three checked instances N16384,N32768,N256, with all inferred shape inequalities. **This is a source-formula / metadata test, NOT a live CKKS ciphertext execution or noise experiment.** Local environment has no `rustc`/`cargo` nor git network DNS, and no installed TenSEAL/OpenFHE/Pyfhel/SEAL. Claims of a passing live CKKS test would be false.

## Nontrivial noise and performance obstruction still OPEN

1. Original output conjugation at **root k≈188** (illustrative); proposed additional conjugations at **masked k≈428**, BEFORE mux product operations. Changing the stage can make key-switching much more costly or introduce errors that then propagate through (h) product factors. The key being present/shape-compatible does not mean early conjugation is fast/noiseless.
2. For ideal mask product target (F=M_1P_1+M_2P_2), using a Galois switch that adds plaintext-equivalent error (eta) to `Conj(V)` yields an **additional leaf error (eta/2)**. If all ideal factors have magnitude ≤1 and (|eta_j|lekappa), an elementary worst-case upper envelope for product error before final extraction is ( (1+kappa/2)^h-1); final 2Re extraction doubles that to (2[(1+kappa/2)^h-1]). This is a **sufficient pessimistic bound for one isolated source of extra error**, not an exact estimator and ignores mux key noise, scale/re-encode noise, phase error, and correlations.
3. For h31 and target threshold (arepsilon=2^{-18.1}) (original source HT15 paper's reported precision, **NOT** Poulpy h32 benchmark), the condition (kappale 2[(1+arepsilon/2)^{1/h}-1]approx1.15e-7) (≈2^-23.05) would keep ONLY the extra early-conj noise envelope below the **entire** output tolerance. The original pipeline consumes part of that tolerance, so a real candidate may require smaller (kappa). This is an upper-budget illustration, **not** an actual measured error or security parameter claim.
4. Original selector prepared-key count 4hθ→2hθ is conditional on modifying keygen+prepare+evaluation to accept complex-packed masks; 4hθ ct×pt convolution **terms remain** because U,V each need 2hθ terms. Two DFT accumulations/IDFTs and extra h (real) or 2h (complex) key switches may dominate latency and scratch. None benchmarked. Memory reduction in selector *object count*, not total peak RAM.

## Research decision

**STATUS:** **PASS** narrow necessary **modulus/level/key-identity** gate, **UNCLEAR** FHE end-to-end and latency/noise, **NOVELTY NOT VERIFIED**.
**RESULT:** In source-shaped Poulpy, `masked_k=raised_k−ld` and a source-built `p=−1` key covers the relevant width, so M01 need not add a new conjugation key or multiplicative level; the real structural cost is **early** ~h Galois key switches, doubled accumulator transforms and possible precision loss. No live ciphertext test was executable; no numerical viability claim.
**NEXT_ACTION (SHIP-M03 only on PI continuation):** ONE real implementation decisive gate. Modify an **isolated scratch fork** of pinned Poulpy `ship_masking_accumulate` and the keygen/preparation selector path to use two packed masks + two plaintext accumulation paths; for one test-sized SHIP plan run encrypt/decrypt comparing reconstructed masked leaf vs baseline at same `k, log_delta`, recording extra max slot error plus exact # prepared left operands and elapsed masking/conjugation time. Compare `epsilon_extra` to the derived output error budget, and reject if quality or latency is prohibitive. Do NOT modify original upstream and do NOT generalize to full vFHE. If cargo/runtime unavailable, request an implementation runner rather than invent test success.
**STATE_UPDATE:** **NO** to shared `STATE.md` due to concurrent vFHE I194 state; YES to this **independent SHIP-M02 file**. Preserve independent numbering and note here as SHIP recovery pointer.
