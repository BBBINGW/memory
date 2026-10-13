# Iteration 171 — Source-parameter raw selector-key material for SHIP CKKS half-bootstrap

**Date:** 2026-10-13. PI authorized I171 with “好的，请继续”, following recommendation to PARK I170's known BGV Hom-NTT no-free-collapse idea. ONE new concrete FHE resource hypothesis and ONE source-equation + exact integer-size arithmetic falsifier. PI retains final claim of novelty and target selection.

## Read before write / verified primary

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` after I170 SHA `6f4451596643eb5fc56bee4102ea2f5e8fbdfe47`, `findings/OPEN_RESEARCH_BRANCHES.md`, I170 finding, checked archived failure themes. Previously available complete **33 physical page** paper Jung Hee Cheon, Guillaume Hanrot, Jongmin Kim and Damien Stehlé, **SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm**, IACR ePrint **2025/784**, https://eprint.iacr.org/2025/784, Research MCP full GitHub mirror SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, **VERSION_UNVERIFIED**. Read exact source §§3.3–4.4 physical pp16–23, §5.1–5.4 pp24–27; equations legible in extraction for basic count, no screenshot visual parity verified. Some additional initially inspected papers ePrint 2025/809 (TFHE mean compensation) and 2025/784 lacked new unsupported numerical claims; only 2025/784 is the chosen target.

## ONE hypothesis and decisive test

**[HYPOTHESIS TO FALSIFY]** In the original paper's **literal uncompressed, independently stored full-RLWE selector ciphertext layout** for the high-precision `LL14` or `HT15` SHIP instantiations, the encrypted *column-selector/mask component alone* fits in under **1 GiB**, while using the paper's 32-core performance settings.

**[CHEAP FALSIFIER]** Read the actual key arity/size from source Algorithm4 and the parameter tables, carefully account for its text-vs-implementation stage-order swap, compute both (i) raw bit-packed modulus coefficient payload and (ii) uncompressed 64-bit RNS prime-limb payload. Explicitly separate **conditional literal-layout cost** from measured memory and from information-theoretic/method-independent lower bounds. If both payload figures already exceed 1 GiB in LL14 or HT15, the narrow hypothesis fails.

## Primary facts (source citations)

**[FACT §3.3 pp16–17]** Given an encrypted secret nonzero position and sign, four different encrypted masks `m_{j,1}^{(k)}`, k=1..4, are used to construct the corresponding rotated contribution. The paper notes a four-mask sum relation that can be exploited to reduce memory, so four mask ciphertexts is the **literal construction**, not an absolute minimum for every optimized alternative.

**[FACT §4.1 pp17–18]** Column-method encrypted onehot selection provides ONE packed RLWE ciphertext per candidate index i∈I. The fixed-root public-vs-private split is important: plaintext selector `1_{i=j}` is encrypted at modulus **P Q** and the blind rotation is evaluated by multiplying rotated known plaintext vector by selector ciphertexts, then once rescaling P.

**[FACT §4.4 pp21–22, Algorithm4]** Fused masks: for each sparse-secret position j, four encrypted arrays `M^{(k)}(j)` and one packed RLWE ciphertext per allowed *column* candidate i are provided. The paper **explicitly says Algorithm4 describes column on the HIGH part and mux on the LOW part, whereas actual implemented scheme uses the inverse order** (“our implementation uses the latter”). Thus the correct column selector arity in the experimental table is **θ**, not `ℓ0/θ` (which belongs to mux stage in actual implementation). Source Table2 p25 caption explicitly defines θ as **column-method size** and ℓ0/θ as **mux-method size**. No extra count of full `N/θ` selectors should be charged.

**[FACT §5.2 p24]** Authors use lowest-level sparse secret Hamming weight **h=31**, dense secret for other levels. Source §5 Table2 p25 gives `N, log_2(PQ), θ, RNS prime counts`; Table3 p26 gives precision and median 32-core latency (authors' actual benchmark, **not reproduced**). LL13 N8192, log PQ218, θ6, prime counts from displayed groups 1+1+1+5+1=**9**, average 4.45bits, 215ms. LL14 N16384, log PQ437, θ9, primes1+1+1+5+2=**10**, avg16.9bits,333ms. HT14 N16384, logPQ438, θ9, primes1+1+9+5+2=**18**, avg4.55bits,1.09s. HT15 N32768, logPQ881, θ17, primes1+1+9+5+4=**20**, avg18.1bits,1.63s. These component prime counts are read from the source reported parameter-chain groups, not independently verified against author's code.

## One exact payload calculation (executed)

For a *literal* four-mask ciphertext per column candidate / nonzero secret key index, all distinct encrypted RLWE ciphertexts at the stated PQ modulus:
```
  key_ct_count = 4 · h · θ
  dense_bit_capacity = key_ct_count · 2 · N · log2(PQ) /8 [bytes]
  RNS64_payload = key_ct_count · 2 · N · (# RNS prime limbs) · 8 [bytes].
```
RNS64 assumes two full polynomials per RLWE ciphertext and one machine uint64 for each prime and coefficient. The bit count uses ideal, independently stored **dense bit packing**, not seeded/randomness compression, sharing, pseudorandom key generation or plaintext-mask algebra.

| source set | h | N | logPQ | θ | source RNS prime limbs | raw selector ct | bit-packed GiB | 64-bit RNS raw GiB | paper precision / 32-core latency |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LL13 |31|8192|218|6|9|744|**0.3094**|**0.8174**|4.45 bits /215ms |
| LL14 |31|16384|437|9|10|1116|**1.8604**|**2.7246**|16.9 bits /333ms |
| HT14 |31|16384|438|9|18|1116|**1.8647**|**4.9043**|4.55 bits /1.09s |
| HT15 |31|32768|881|17|20|2108|**14.1689**|**20.5859**|18.1 bits /1.63s |

All arithmetic computed exactly with integer JavaScript in `functions.exec`; final GiB display rounded four decimals. The *literal source key layout* for LL14 already exceeds 1 GiB selector payload **even in ideal bit-packed dense form** (1.8604 GiB), and HT15 requires 14.1689 GiB at that form, 20.5859 GiB in one common 64-bit-RNS payload envelope. Overall SHIP bootstrapping key also includes mux rotation/evaluation keys and other material, so this is **only a component accounting**, NOT a real peak heap allocation. Actual memory may be **lower** due to source's four-mask relation, compressed/seeded RLWE first components, special levels, on-demand recomputation or streaming; **none of these are quantified here.** Source Table2's logPQ and prime sizes were used as an all-limb worst-level selector assumption; when an implementation uses a smaller per-key modulus, result must be recomputed per key before claiming a measured bound. Byte counts do not measure memory traffic or CPU time.

## Falsification and significance

**[FAIL stated small-key literal-layout hypothesis]** For source's high-precision LL14 and HT15 parameter sets, independently stored standard full RLWE masked-column selector ciphertexts cannot fit in <1GiB if they are all represented at the source's tabulated maximal PQ modulus; even mathematically ideal dense coefficient bit storage exceeds 1GiB. This is a **material, quantitative resource dimension** of original hybrid SHIP construction, but NOT proof of an overlooked bottleneck, actual source RAM cost, more latency or source error. §3.3 explicitly flags possible mask sharing/memory compression and source computes latency/throughput, so the authors are **not shown** to have overlooked memory. More extensive mask sharing/seeded ciphertext generation can reduce memory; required tradeoff untested. Raw 64-bit-RNS HT15 cost ~20.59GiB may matter for multi-tenant deployment, but source's hardware benchmark used 512GB DRAM, and author may use customized memory layout.

**[PASS exact source-shape costing]** θ must refer to real *column* stage (implementation reversal) and 4hθ selector objects, not naive 4h(ℓ0/θ) or 4hN/θ; the realistic stage-order check is essential to avoid false 10× count. This source-data derived memory trade-off goes beyond repeating known algebraic facts but **still lacks a new algorithm and source implementation proof**.

## End of Iteration 171

**STATUS:** **FAIL** sub-1GiB literal selector-masks claim at source's 16+ bit precision settings / **PASS** exact algorithm-count and conditional full-RNS payload gate / **UNCLEAR** actual author HEaaN key memory or truly new compression scheme.
**RESULT:** Source algorithm after implementation stage reversal uses 4hθ encrypted column masks; h31, LL14 θ9 gives1116 RLWE key ciphertexts, 1.8604GiB dense bitpacked or2.7246GiB with10 uint64 RNS limbs. HT15 θ17 gives2108 cts, 14.1689GiB dense bitpacked or20.5859GiB with20 RNS limbs. Authors already explicitly note mask sum storage relation; numerical figures are conditional memory envelopes, NOT measured implementation RAM, not universal minima.
**NEXT_ACTION:** I172 only on PI continue: ONE decisive **real key-layout** gate in an accessible SHIP implementation (e.g. pinned Poulpy CKKS SHIP, if verified source-compatible) or source's actual HEaaN artifact, count real stored **per-index masked selection ciphertexts, key level/limbs, seeded compression and memory footprint** to confirm/refute 4hθ raw full-PQ model. Do not claim published SHIP implementation equivalent to third-party code. Only if memory materially persists choose ONE nontrivial compression method with a quantified key-storage vs extra online KS/rotation/noise cost; otherwise PARK. No re-scan of θ/digits trivial numeric envelopes.
**STATE_UPDATE:** **YES** — new primary FHE key-storage frontier with quantitative source-level evidence. PI assent parks the I170 BGV NTT no-cost-collapse toy and previous AKS linearity remains parked; all other branches unchanged.
