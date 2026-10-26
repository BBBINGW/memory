# PURE FHE P0 — Seeded Linear Ciphertext Lineage vs BXT's Uncompressed Output Barrier

**Date:** 2026-10-26 Asia/Singapore | **STAGE:** `PURE-FHE-P0-PRESCOUT-10` | **scope:** broad new pure-FHE structural prescout, NOT restarted BOOT/SHIP/CGS or formal I-series. User is PI, authorizations for no Codex/remote GPU/native deployment. State update THIS FINDING ONLY.

**STATUS: PASS_EXACT_LINEAR_LINEAGE_TOY / FAIL_FREE_SINGLE_SEED_RECOMPRESSION / UNCLEAR_REAL_GPU_BREAK_EVEN / NOVELTY_UNVERIFIED**.
**Priority:** `CANDIDATE_CONDITIONAL_ENGINEERING`, not a proven cryptographic primitive or speedup. Next cheapest gate: accurate BXT vs lineage-GPU memory/PRG cost from original data; no unapproved Codex.

## Source provenance, author claims vs inference

[FACT SOURCE] Yudha, Wahyudi, Rajagede, Lou, Solihin, **Memory-Efficient Designs for Word-Wise Universal Fully Homomorphic Encryption**, arXiv **2609.04769v1**, 2026-09-04, ICCD 2026. **Full HTML article text** read 2026-10-26 at https://arxiv.org/abs/2609.04769 (web ref `turn942298view2` in originating session, and `turn573094view0` etc); arxiv metadata and §III–VII available, not extracted from a PDF; no PDF-screenshot gate needed. This is not an authenticated independent reproduction.
- §III-A source ciphertext convention `C=(A,B), B=-A*S+p*E+mu` in BGV `R_Q`. A is generated from a seed at ciphertext creation.
- §V-A author BXT-C regenerates `A` with public PRNG, BXT-CS packs RNS coeffs in bit arrays (e.g. 36 vs 64 bits, unpacks L2→L1), BXT-CSO defers data generation and aggregates PADD/PMULT/HADD.
- **Crucial §V-B source explicitly:** “After each operation, the output ciphertext is stored in an uncompressed form because the seed representation cannot be directly propagated through these operations.” Author distinguishes read-only seeded input from output.
- §VI simulation uses **Accel-Sim**, NVIDIA RTX A6000-inspired 84 SM at 1410MHz, 936.2 GB/s DRAM, one 40-cycle PRNG/SM and 2-cycle bit unpacker, assumed N=2^16, log2 Q=1728, L=23 levels, dnum3; not an actual GPU silicon deployment of added warp-level hardware. §VII source reports BXT-C average 1.3x, BXT-CS 2.5x, BXT-CSO2.9x per operations over 100x GPU baseline (simulated); 3.8x at 50%-precision comparison on MNIST with <1% CNN accuracy loss **relaxes exact comparison and uses fault-aware plaintext training**, not a cryptographic exact-inference speedup. §V-B HADD time breakdown 67% load,29% store,4% other (their simulated environment). Complex HMULT/HROTATE not benefitting from BXT-CSO.
- [PRIOR] seeded LWE/GLWE types plus decompression already supported by Concrete Core since v1.0 https://www.zama.org/post/announcing-concrete-core-v1-0 . The original BXT §II refers to CraterLake/ARK's on-the-fly key material and prior communication compression. Public HEIR notes https://heir.dev/docs/design/relinearization_ilp/ discuss symbolic ciphertext key-basis graph scheduling (different from the candidate), so symbolic metadata DAG generality not an assumed new concept. No exhaustive patent/cross-library provenance audit: novelty is UNVERIFIED.

## ONE PRIMARY HYPOTHESIS and minimal test

**H_LAZY_EXACT:** Under a fixed secret s, ring R_Q and modulus Q, a ciphertext produced by *only* HADD/HNEG and public **scalar** multiplication of k independently seeded RLWE ciphertexts has an exact representation as `(B, {(seed_i, w_i)}_{i=1..k})` with the A-component reconstructed lazily as `Σ w_i G(seed_i)`, while preserving exactly the same decryption phase and error as conventional eager evaluation; no secret-dependent KeySwitch is needed **until a downstream nonclosed operation**. For public plaintext **polynomial** multiplication the coefficient weights become full polynomials and metadata/cost cannot be assumed O(k); that extension is deliberately OUT OF SCOPE.

[DERIVATION] For inputs `(A_i,B_i)` with `B_i+A_i*s = mu_i + e_i` modulo Q, source BGV convention absorbs p into e, let output `B=Σw_i B_i`, `A=Σw_i G(seed_i)`. Then `B+A*s=Σw_i(mu_i+e_i)`; this is byte-for-byte algebraic equivalence to eager HADD / constant PMULT and does not resample noise, alter the RLWE assumption, promise circuit privacy, or change reuse correlation. The public coefficients and lineage references must not expose otherwise secret model data; server must preserve same key identifier, modulus-level, scale, NTT/RNS format and full linear operation DAG.

[CHEAP TEST EXECUTED] Using self-contained deterministic test PRG (LCG, **NOT** secure), `R=Z_257[X]/(X^8+1)`, fixed ternary secret `s=(1,0,-1,1,0,0,1,0)`, four distinct seeded uniform-appearing mask vectors `A_i=PRG(seed_i)`, weights `w=(1,3,5,7)`, varying nonzero error and message per input; **1024/1024** independent seeded input test cases matched exact polynomial coefficientwise decryption phase and eager arithmetic with zero failures. Example t=0 seeds 17,18,19,20 yielded reconstructed `A=(179,253,26,227,120,76,128,155)`, output phase `(2,13,15,31,0,0,5,0)`, matches eager reference all eight coefficients. No CSPRNG, no native HE runtime, no security parameter and no benchmark; tests do not certify real BGV numerical correctness.

**RESULT:** `PASS_EXACT_LINEAR_LINEAGE_TOY`, algebra trivial linearity. Does not verify nontrivial performance or new cryptosystem.

## Repair / impossible-free-singleseed boundary

It is **not** legal to freely replace `A=Σ w_i G(seed_i)` by `A'=G(new_seed)` and retain old `B`: new phase is `mu+e+(A'-A)s`. A fresh mask requires `B'=B+(A-A')s`, an s-dependent correction not generally available as free public ring arithmetic; a suitable public-key encryption-of-zero/re-randomization/keyswitch can alter ciphertext/related noise at *nonzero cost*, but literal uniform fresh-seed choice + unchanged B fails.

Explicit exact toy: Q257 N8, old A=(4,8,12,16,20,24,28,32), new A'=(9,14,22,34,55,89,144,233), same s, correct old phase=(8,0,0,0,0,0,0,0) but wrong unchanged-B new phase=(54,73,26,209,172,113,104,177). This is an **ancillary repair check**, not second primary proposal. Standard rank obstruction: any *public additive-homomorphic linear* generator G:Fq^t→Fq^N with t<N has image dimension≤t; a public left-kernel linear functional distinguishes it exactly from uniform, so there is no free short **linearly seed-updatable** PRG maintaining full-dimensional uniform-output distribution under that definition. **Do not extrapolate** to arbitrary nonlinear PRGs, computational PRGs without public add-homomorphism, or encryption re-randomization.

Positive engineering escape: bounded **seed-expression/DAG** keeps independent original public seed references (not a compressed single seed); materialize `A` at a selected cut node before HROTATE/KeySwitch, nontrivial ciphertext×plaintext polynomial, HMULT, incompatible modulus, or when PRNG recomputation exceeds HBM savings. Combine duplicate seed IDs and coefficients in the DAG; track zero coefficients and public linear kernels. BXT already does delayed seed generation/operation fusion, so any novelty would have to be a **materially different costed cross-kernel persistent lineage strategy**, not ordinary hoisting or deferral.

## Whole-system cost necessary gate, source-derived params vs derived proxy

BXT source config `N=65536, L=23` limb-polynomials, each RNS word assumed 64-bit; a **single raw mask polynomial component** has `N·L·8 = 12,058,624 bytes = 11.5 MiB`. If source bit-pack uses 36 bits per coefficient, analogous ideal serialized mask `N·L·36/8=6.46875 MiB` (source numbers are max limb width/hardware choice, not assertion all levels always have exactly same active limbs). A seed-lineage pair `(16-byte seed, 8-byte scalar)` costs `24k` bytes excluding DAG refs, ids, alignment, security metadata and potentially materialized cache.
- k=4: 96 bytes metadata, 6,029,312 PRG-generated word elements and 4,521,984 mask adds if *fully reconstructed*.
- k=16: 384 bytes metadata, 24,117,248 PRG-word elements and 22,609,920 mask adds.
- k=64: 1536 bytes metadata, 96,468,992 PRG-word elements and 94,961,664 mask adds.
- k=784: 18,816 bytes metadata but **1.1817 billion** generated coefficient words and almost as many adds, per one full-RNS materialization, almost certainly unsuitable without costed fusion or early materialization; NO native cost/time asserted.

Storage can save half a two-component ciphertext but PRG, coefficient combination and eventual key-switch materialization can dominate. Public scalar repeated and cached branch structure may reduce effective k; *per intermediate* materialization cost differs from DAG-wide CSE. SIMD formatting (NTT vs coefficient domain), GPU PRNG throughput and 64-bit modular addition throughput are necessary to predict speed. Baseline BXT accelerations assume new custom hardware; distinguish software-only GPU kernels from their simulated PRNG and bit-unpacker. A source-aware model must include GB transmitted to HBM, L1/L2 misses, PRNG-generated words, additive/compression operations, DAG metadata, write/read counts, and fraction of path under linear gates. The source model's PMULT is by **arbitrary plaintext values**, not necessarily ring-wide scalar; our H intentionally excludes those PMULTs.

**NEXT CHEAPEST DECISIVE COST TEST, if PI continues P0:** Take one **author-source exact** HADD tree / scalar-only linear segment with explicit roots, output fanout and crossing to an unavoidable HROTATE/HMULT, and compare:
(A) source BXT-CSO: compressed read-only inputs, eager uncompressed intermediate ciphertexts plus existing cross-kernel fusion,
(B) k-limited seed lineage with chosen materialization threshold K.
Compute source-like bytes read+written and PRNG-word costs **including existing BXT fusion**. Reject candidate if (B) cannot offer a favorable break-even region under conservative GPU PRNG/GBps parameters or cannot support common non-scalar PMULT workloads. No Codex while those necessary gates and prior-art uniqueness remain unverified. If benefit confined to a narrow special workload, retain purely as engineering idea, not a new crypto algorithm.

**STATUS:** `PASS_EXACT_LINEAR_LINEAGE / FAIL_FREE_SINGLE_RESEED / UNCLEAR_NATIVE_SPEED`.
**NOVELTY:** `UNVERIFIED_PRIOR_ART`, textbook linearity; no new security theorem.
**RESULT:** `ENGINEERING_CANDIDATE_CONDITIONAL` plus exact correctness.
**NEXT_TEST:** `BXT_PAIRED_HADD_TREE_COST_WITH_EAGER_FUSION`.
**STATE_UPDATE:** `THIS_FINDING_ONLY`; previous parked engineering candidates unaffected.
**CODEX:** `NOT_RUN`.
