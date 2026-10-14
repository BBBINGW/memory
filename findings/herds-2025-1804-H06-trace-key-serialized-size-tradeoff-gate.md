# HERDS H-HERDS-06 — Table 3 TRK doubles serialized trace-key bytes versus pinned public Go implementation

**Date:** 2026-10-14 (Asia/Tokyo). **Independent HERDS round H06**, not concurrent global vFHE or independent SHIP research. Human PI requested continuation after H05. Read-before-write verified START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, read-only global STATE.md at V25 (globally frozen general I192), findings/herds-2025-1804-go-trace-gadget-history-provenance-gate.md and H04. SHIP I226 unchanged. One primary hypothesis, one smallest source-exact test.

## Primary source provenance [FACT]

- Original: Xiang et al., *HERDS: Multi-Key Fully Homomorphic Encryption with Sublinear Bootstrapping*, EUROCRYPT 2026, ePrint **2025/1804** https://eprint.iacr.org/2025/1804, 46 physical pp public Research MCP mirror SHA256 **c08a83cea17b352df1006a7051cee26c133bf92a4212860d3cf28f6b6426e7d7**, VERSION_UNVERIFIED relative to publisher. Physical p27 Table3 Set V (32 parties / claimed λ100) has n560,N2048, BRK (2^9,4), **TRK (2^5,8)**, hybrid (2^4,10), packed accumulator length8. Source Lemma5–7 p16/p18–19; paper mathematical PDF extraction not visually authenticated.
- Pinned public author Go source **SNUCP/mktfhe-parallel-go@e3b8f56d92a5bc535e9b2f0853f4b7135dcbe53a**; `mktfhe/params_list.go` blob SHA 8e18f4dea1c438109b6d6b7a7c68350796089d6f 32-party default has BRK base 2^9 length 4, accumulator base 2^5 length 8, hybrid base 2^4 length 10; `mktfhe/bootstrap_keygen.go` blob SHA 50f8832061ceadfb6ec2e4c00b6891f603847f7b `GenTraceKey()` at line73 PASSES `BlindRotateParameters()` to `GenGLWEKeySwitchKey`, NOT accumulator parameters. Each party has ceil(log2 AccumulatorParameters.Level())=3 trace Galois key objects.
- Pinned dependency **sp301415/tfhe-go@v0.6.0**, as required by author `go.mod` (blob fbf63e1d1affbde922d269b09d5fff2b732772a4). `tfhe/keyswitch_key.go` blob eb89bceb0fa9b17b75eb0ca36218e58cd3ce60c3 stores GLWE key-switch key as `InputGLWERank` **FourierGLevCiphertexts**; `tfhe/fourier_glwe.go` blob 7aef7c5cbf93b984a508b2eadfc121c61d710dd9 allocates exactly `Level` Fourier GLWE ciphertexts of `GLWERank+1` polynomials each; `tfhe/keyswitch_key_marshal.go` blob 64f5c741528caf7eadf50c93021b902db52ff4a8 gives **exact `GLWEKeySwitchKey.ByteSize()`**: `40 + inputRank*level*(outputRank+1)*polyDegree*8`. Key serialization writes a 40-byte header then coefficient data; this is **serialized bytes, not peak Go process RSS**.
- Prior H04 finding `findings/herds-2025-1804-author-go-trace-gadget-paper-code-mismatch-gate.md`: approximate Lemmas5–7 worksheet with Set V shows normalized final `6σ_out/q` **0.0359761390647** under paper TRK `(2^5,8)` versus **0.0366414781052** under source TRK `(2^9,4)`; both `<1/16`. Trace key-switch σ model about **16× smaller** with paper TRK, whereas final σ only about **1.8494%** smaller in that conditional approximate model. No actual DFR or latency benchmark.

## One primary falsifiable hypothesis and cheapest decisive test

**H-HERDS-06:** Replacing the source's (B=2^9,d=4) trace Galois gadget with the paper's (B=2^5,d=8) does **not** materially change the stored trace-key bytes for the same 32-party evaluation set: the Fourier encoding normalizes everything to the same total storage. If true, the discrepancy is effectively only about approximation precision/noise, not evaluation-key storage.

**Falsifier/test:** Read the *pinned exact tfhe-go v0.6.0* `GLWEKeySwitchKey.ByteSize()` function and `FourierGLevCiphertext` nesting and the author key-generation count. Plug in k=32, input rank=output rank=1, poly degree N=2048, number of automorphisms=ceil(log2 8)=3, and gadget levels d4 versus d8. One exact integer test suffices; no random encryption/benchmarks required. A positive material byte difference falsifies H06.

## Exact integer results [DERIVATION/COMPUTED]

For **one** GLWE trace key: `size(level)=40+1*level*(1+1)*2048*8 = 40+32768*level` bytes.

| configuration | one Galois key bytes | 96 Galois keys bytes | 96-key MiB |
|---|---:|---:|---:|
| Pinned Go trace key, radix2^9 length4 | **131112** | **12,586,752** | **12.003662109375 MiB** |
| Table3 Set V TRK, radix2^5 length8 | **262184** | **25,169,664** | **24.003662109375 MiB** |

**Exact additional serialized bytes =12,582,912=12 MiB** for 32 parties. Per-key fixed 40-byte header means exact *total serialization* ratio is slightly **under** 2 (payload ratio exactly 2); saying precisely 2× for byte-sized total including header is wrong. Other eval keys untouched. Under the same number of trace stages and same actual source API, the Galois keys require eight ciphertext gadget rows instead of four; this establishes 2× row/data quantity but **does NOT establish 2× actual runtime** for full bootstrap, key generation or process RSS.

Reproducible locally generated exact Python arithmetic (no Go dependency, code-level inspection only): `/mnt/data/herds_H06_trace_key_bytes_gate.py` SHA256 `1c5055caea111a99d7e9dadf197db4a14c966782c81f63ded0f60f2ad26196ec`; `/mnt/data/herds_H06_trace_key_bytes_results.json` SHA256 `e1169e8ef53acc1771570757e4c13fee945fb1ce9c3ee2aaf4cd7a71f213547d`.

**Runner access [FACT]:** `go version go1.23.2 linux/amd64` present in local container, but `git ls-remote https://github.com/SNUCP/mktfhe-parallel-go.git` fails DNS (`Could not resolve host: github.com`), and HTTPS to `proxy.golang.org` similarly fails DNS; required Go module not locally cached. Thus could NOT independently compile or execute author Go code, and did NOT run actual pairwise end-to-end encryption/decryption test. GitHub app supplied pinned source read; do not pass that off as a compiled run.

## Verdict

**STATUS: FAIL H-HERDS-06** 'serialized bytes unchanged'. **PASS source-faithful exact storage-size delta 12 MiB** and prior approximate noise comparison. **UNCLEAR** real runtime/DFR, exact publisher benchmark commit, code's 128-bit presets, memory allocator heap, and whether (2^5,8) was experimentally used. **NOVELTY NOT VERIFIED**.

**RESULT:** The current Go choice halves the number of trace gadget rows and reduces the 32-party 96-key serialized payload by 12 MiB relative to the manuscript TRK. According to prior approximate noise worksheet, this comes with ~16× higher local trace switching SD but ~1.85% higher overall SD for this example, still below the six-sigma heuristic. A deliberate storage/performance trade-off is plausible but NOT verified as author intention. This is a source-level **reproducibility/parameter sensitivity finding**, not a cryptographic primitive, accuracy failure or publication-worthy new optimization.

**NEXT_ACTION:** HUMAN_REVIEW/PARK this branch until (a) network/Go module runner with pinned source and tfhe-go v0.6.0 becomes available to run controlled trace gadget parameter swap and measure correct outputs, cold/warm keygen time, actual key size, peak RSS and full bootstrapping latency/DFR for k32, or (b) authors supply official benchmark commit/config and valid 128bit presets. DO NOT treat 1k no-failure trials as formal DFR security, and do not keep counting adjacent memory buffers. Any major pivot remains the human PI's decision; global vFHE STATE and independent SHIP state untouched.

**STATE_UPDATE:** YES this one HERDS finding only; NO edits to global STATE, ship-memory STATE, or upstream repositories.