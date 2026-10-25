# EAI-P / EAI-010 — Independent Original-ZIP & Numerical Audit (2026-10-25)

**Target:** EAI-P / historical EAI-010. Not a new EAI iteration or EAI-SYS S55. **Scope:** read only user-uploaded original Codex evidence ZIP; no GPU/model tests, source modification or background task. PI decides park/pivot. Protocol: one smallest falsifiable claim plus cheapest decisive test.

## H and evidence gate

**H:** Existing pinned EAI-010/EAI-009R raw artifacts suffice to independently recalculate selective native q8_0-K/q4_0-V FlashAttention throughput, pointwise NLL discrepancies and actual CUDA dispatch; determine whether the basic optimization is new.

**Test:** independently parse raw `runs.csv`, six JSONs and 6×128 latency CSVs, 255-row `paired_scores.csv` joined against all three separate quality score CSVs and 512-token input, plus source/build metadata, GPU kernel traces and original hash manifests. Direct prior-art check. **No rerun.**

## Uploaded raw artifact and verified integrity

**[FACT — independently read original uploaded bytes]** `EAI-010-RAW-EVIDENCE-AUDIT-2026-10-25.zip`, size **44,599,217 bytes**, SHA-256 independently computed **`4f695731ad080f65c8903b75fe79a82ab33555d15ad7ef82c9ef1884f4bdf6ac`**. ZIP CRC test PASS. Package `SHA256SUMS.txt` **281/281** file hashes match. EAI-009R embedded original manifest **129/129 present+match**. EAI-010 embedded original manifest **141/143 present+match**, **2 absent** `logs/nvidia-smi-before.txt`, `logs/nvidia-smi-after.txt` intentionally excluded because Codex reported sensitive runtime tokens. Their remote-original 143/143 PASS cannot be independently reproduced *from this upload*. No secrets or model GGUF were transferred as audit objects.

**Source/provenance limitation:** archived source/CMake/runtime traces show pinned `ggml-org/llama.cpp@f849095365d5ac1f560886a4e6574531d559e96f`, model Qwen2.5-1.5B-Instruct Q4_0 GGUF SHA **`a5ab77ebbd1d6d70250ff415339935bebac619b7acc508f71545f08231369dc1`**, RTX4090/CUDA12.6. This is *retained source/remote-hash evidence*; user ZIP does not contain model GGUF and our session **did not independently execute native GPU code or rehash the remote model**.

## Speed: PASS within a fixed 32K decode-only benchmark

**[FACT — offline independently recalculated from six raw data sets]** Each arm: 32,512-token prefill, then **128 serial query-length-one teacher-forced decode steps** at positions 32512–32639. Raw JSON and CSV agree with `128 / decode_seconds` and each latency CSV has 128 records.

| Pair | Conversion tok/s | Native tok/s | paired gain |
|---|---:|---:|---:|
| 1 | 254.778572162 | 320.068970062 | 25.626330090% |
| 2 | 254.983993838 | 320.324187297 | 25.625213754% |
| 3 | 254.941605844 | 320.145267516 | 25.575920202% |

Median conversion/native **254.941605844 / 320.145267516 tok/s**, **ratio of medians +25.575920202%**. Median *of paired percentage gains* is instead **25.625213754%**; do not confuse estimators. Three process pairs are reproducible in the archive but not enough to claim broad significance or hardware generalization.

**[FACT / DERIVED — scope caveat]** The 32,640-token fixed benchmark stream is **exactly the 512-token EAI-009R source list repeated cyclically**; verified all 32,640 positions. It is a synthetic workload, not natural long-context text. The +25.6% is *decode throughput after prefill*; if accounting for ~1.45s prefill and 128 generated tokens, the measured end-to-end wall-time reduction is only **5.14–5.68%** across the same three pairs (for generated-128-token total request time, equivalent to 5.42–6.02% throughput gains). No all-task result claimed.

## Numerical scores — POINTWISE PARITY FAIL as strict equality; task quality unresolved

**[FACT — independently recalculated, all 255 positions/source token IDs matched]** positions scored 0–254 target positions 257–511, source 512-token stream valid at every row, per-arm native/conversion/f16 scores aligned:

| Metric | Value |
|---|---:|
| mean native / conversion / F16 NLL | 1.906878674223 / 1.909700478663 / 1.892691352501 nat |
| `mean(abs(native_nll - conversion_nll))` | **0.092033067989 nat** |
| `abs(mean(native_nll)-mean(conversion_nll))` | **0.002821804440 nat** |
| median / p95 / p99 absolute difference | 0.027382098948 / 0.350013684870 / 0.731671377291 nat |
| max absolute pointwise difference | **2.143831005921 nat** |
| positions with abs difference >0.1 / >1.0 nat | **64/255 / 1/255** |
| positions with native NLL higher / lower | 124 / 131 |
| mean abs(native−F16) / mean abs(conversion−F16) | 0.087536589921 / 0.106109182913 nat |
| native closer / conversion closer to F16 per position | 121 / 134 |

Largest outlier index36 target position293/token47450: native3.087105952 / conversion0.943274946 / F16 2.575310147. There is **no** numerical pointwise equivalence. Aggregate near-cancellation does **not** establish task-level quality preservation or impairment. Only one 512-token teacher-forced short context was scored; 32K *quality* NOT_TESTED. Raw activation blocks, per-block scales and full logits needed to attribute a numerical root cause are absent; no rigorous mechanism-level error causal diagnosis from NLL alone. The 255 sequential positions are correlated.

## Kernel mechanism / novelty

**[FACT — independently inspected retained Nsight CSV with NVTX labels]** Build delta: Native includes `q8_0-q4_0` in `GGML_CUDA_FA_QUANTS`; Conversion does not. At actual 32K probe decode position32512 Native has **28** `flash_attn_ext_vec<(int)128,(int)1,(ggml_type)8,(ggml_type)2>` q8/q4 calls; Conversion has **28** f16/f16 vector attention calls and **28** each q8→f16 and q4→f16 conversion kernels in the decode NVTX range. In EAI-009R full 255 scored positions the analogous specialized native count is 7140. Thus the actual recorded native/conversion dataflow differs as claimed; this is not a code-executed independent CUDA rerun. Note Nsight traces were untimed probes; timed performance used regular CUDA Graph settings.

**[FACT — public GitHub original issue]** [llama.cpp #30001](https://github.com/ggml-org/llama.cpp/issues/30001), posted 2026-10-05, explicitly proposes selective native `q8_0-q4_0` FlashAttention and reports **RTX4090, Qwen2.5-7B, 32K 88.07→110.98 tok/s (+26.0%)** vs conversion fallback. Different model and setup, but basic optimization mechanism is **already described by prior art**. This EAI-010 run is a meaningful controlled engineering *baseline confirmation*, not an independently new attention algorithm. `NOVELTY_NOT_ESTABLISHED`.

## End-of-iteration fields and PI decision boundary

**STATUS:** `PASS_RAW_ARCHIVE_INTEGRITY / PASS_OFFLINE_SPEED_RECOMPUTE / PASS_POINTWISE_NLL_RECOMPUTE / PASS_TRACE_DISPATCH_CONSISTENCY / FAIL_STRICT_POINTWISE_PARITY / LONG_CONTEXT_TASK_QUALITY_UNCLEAR / HUMAN_REVIEW`.

**RESULT:** Native decode-only +25.5759% in fixed synthetic long-context load independently confirmed from original CSV/JSON, not a general serving result. Pointwise NLL deviations substantial despite nearly cancelling signed mean; average effect vs F16 is small on a single short sample, but long-context quality unverified. Selective existing kernel already prior-art-visible; no publishable new mechanism established.

**AGENT_RECOMMENDATION:** `PARK EAI-010 AS ENGINEERING BASELINE`; do **not** authorize additional broad GPU sweep. If real deployed quality is a separate PI goal, consider exactly one small native attention-output numerical-causality control with fixed quantized K/V and both fused/dequant paths, only by fresh PI authorization. For publishable research first demand a novel numerical/error mechanism beyond public selective-kernel enabling.

**NEXT_TEST:** `NONE_WHILE_PARK_RECOMMENDATION_PENDING_HUMAN_REVIEW`. **NEXT_ACTION:** `PI_DECIDE_PARK_EAI_P_EAI010_AND_SELECT_NEXT_RESEARCH_TARGET`; do not auto-switch to FHE or start new numbered EAI/P research.

**STATE_UPDATE:** `YES` after this GitHub notes commit and explicit readback. The uploaded raw ZIP remains in ChatGPT conversation attachment, not in this Git repository; file checksum above allows later cross-verification.
