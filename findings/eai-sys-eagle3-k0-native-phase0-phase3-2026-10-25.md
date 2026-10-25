# EAI-SYS post-S54: EAGLE3 dynamic K=0 KV-only native Phase 0–3

**Date:** 2026-10-25 (Asia/Singapore)  
**Research ID:** `TRACK_ID=EAI`, `ACTIVE_SUBLINE=EAI-SYS`; `LATEST_COMPLETED=SCOUT-S54`; `NEXT_ITERATION=S55_NOT_STARTED`. Post-S54 Phase0–3 are **not** S55.
**Status:** `HUMAN_REVIEW / HOLD_WORKLOAD / PARK_ENGINEERING_RESULT` (PI accepted recommendation to park candidate and move to EAI-P evidence audit).
**Evidence provenance:** The phase results are **user-supplied Codex reports only**, not independently audited raw GPU traces. Three original ZIPs have not been read or SHA256-recomputed by the assistant. Do not promote to independent native verification.

## Primary falsifiable claim

For a fixed **one-layer Llama EAGLE3** Draft, a dynamic K=0 dedicated method retaining original normalized embedding/fused target input, full packed QKV projection, RoPE, physical KV mapping and same native cache writer can produce the same *future-readable* Draft K/V as Full Sync while skipping attention output/o_proj/MLP/final normalization/sampling. Native correctness and K>0 resume must match Full Sync; micro-cost savings must also survive a fair end-to-end workload test. This does **not** apply automatically to multi-layer, compiled, graph or alternate drafters.

**Exact pins:** vLLM `debcf228431f0b04ee8f12cfc410b0fe3c34a4f7`; Target `meta-llama/Llama-3.1-8B-Instruct@0e9e39f249a16976918f6564b8830bc894c89659`; Draft `yuhuili/EAGLE3-LLaMA3.1-Instruct-8B@ada412b672e293d682423de84a095447bf38a637`; RTX4090, Torch 2.14.0+cu126, CUDA12.6, driver565.57.01, FlashAttention2, true eager, LBNHC, BF16 KV (per Codex reports).

## Tested progression — [FACT: Codex-reported, NOT independently audited]

- **Phase0 `PASS_CUDA12_NATIVE_ENVIRONMENT`:** source-built fixed commit; native KV writer/FA2/Triton/FlashInfer smoke; no live CUDA13-only dynamic dependency.
- **Phase1 `PASS_MODEL_LOADING`:** both immutable checkpoint revisions truly loaded; Draft one-layer Llama EAGLE3. Candidate edit changes ONLY `vllm/model_executor/models/llama_eagle3.py` and `vllm/v1/worker/gpu/spec_decode/target_dependent_ar/speculator.py`, 77 added lines.
- **Phase2 `PASS_NATIVE_CORRECT` in tested scope:** QL=1/8/64 full draft cache and future-readable physical slots bitwise parity; max_abs_diff=0; one native writer call per Arm; bad RoPE/wrong shifted token/missing writer controls detected. True dynamic K schedule `[3,0,0,3,3,3,3,3,3,3]` included consecutive two K0s; 10 proposal events/26 KV updates; resumed hidden hash, proposed tokens, rejected count, target verification, KV and final tokens reported identical.
- **Phase3 `PASS_REAL_K0_SPEED_ONLY / HOLD_WORKLOAD`:** 36 paired K0 micro test groups, all positive, followed by KV bitwise regression PASS:

| QL | Full GPU ms | KV GPU ms | Percent saved / reported 95% CI | kernels |
|---|---:|---:|---|---|
| 1 | 0.6677 | 0.2161 | 67.63% [67.24,67.98] | 16→8 |
| 8 | 0.7128 | 0.2630 | 63.10% [62.74,63.43] | 15→8 |
| 64 | 0.7719 | 0.2723 | 64.72% [64.52,64.90] | 18→9 |

45 dynamic executions: three arms (Full Sync / KV-only / No-Spec) × three **SYNTHETIC SCHEDULE** scenarios × five independent fresh-process replicates. In all 15 paired Full/KV runs, K sequence, acceptance, accepted/rejected counts and complete output reported identical:

| scenario | K0 share | Full tok/s | KV tok/s | KV E2E gain / 95% CI | No-Spec tok/s |
|---|---:|---:|---:|---|---:|
| K0-dominant | 82.76% | 102.188 | 104.231 | 2.000% [1.952,2.029] | 105.185 |
| Alternating | 31.25% | 81.833 | 82.403 | 0.696% [0.627,0.769] | 74.253 |
| Low K0 | 6.45% | 67.167 | 67.228 | 0.090% [0.024,0.157] | 61.144 |

**[DERIVED] Decisive outcome:** max synthetic end-to-end benefit +2.000% is below the **predeclared ~3%** value threshold; No-Spec exceeds KV in K0-dominant scenario. Missing a representative *production* K0 distribution prevents generalization. High local 63–68% savings are real *only under reported tests*, not 63–68% model acceleration. Amdahl wall predictions and measurements broadly agree.

## Limitations and novelty

- Packed QKV computation is **not** removed. Original KV writer remains; savings mainly removed downstream Attention/o_proj/MLP work; cache writer ~0.0038–0.0041ms and MLP ~0.388–0.443ms as reported.
- Candidate `skip_sample && method=="eagle3"` branch does not have production-grade one-layer/eager/backend feature-guard and Full Sync fallback; production patch not validated.
- Prior art: [vLLM #56441 DSpark KV-only](https://github.com/vllm-project/vllm/pull/56441), [vLLM #53426 dynamic K0 skip](https://github.com/vllm-project/vllm/pull/53426), [vLLM #53416 EAGLE3 synchronization](https://github.com/vllm-project/vllm/issues/53416). KV-only primitive known. `NOVELTY: NOT_ESTABLISHED`.
- This evidence does not imply all schedules or architectures have ≤2% gains; it fails only the defined tested workload/value gate.

## Raw evidence location: POINTERS ONLY, NOT FILES STORED IN GIT

Reported ephemeral folder `/dev/shm/eai-sys-eagle3-k0-resume-20261024/` (unavailable from current ChatGPT session):

1. `EAI-SYS-EAGLE3-CUDA12-NATIVE-ENVIRONMENT-GATE-2026-10-25.zip` SHA256 reported `898ede760e00c26680dba5bd8f962f3fa78c2a7e0116fa536f5324cd8619f5b0`.
2. `EAI-SYS-EAGLE3-K0-PHASE1-PHASE2-NATIVE-GATE.zip` SHA256 reported `abbb5e436ad578e1a8468dd649e02c67a342af962f1b6d2cdbb8ef8ac7d023a1` (127860 bytes).
3. `EAI-SYS-EAGLE3-K0-PHASE3-NATIVE-PERFORMANCE.zip` SHA256 reported `9a0384b2a9c7bae21888d4216c4b82f13eaa3c7ef9bfd391c4503c5ca20ebe41` (161167 bytes).

[OPEN] Must preserve/copy original ZIPs to PI-authorized persistent storage, then upload for independent raw audit. This GitHub note is only the evidence index and research finding, not a substitute for raw logs.

## End of research checkpoint

**STATUS:** `HUMAN_REVIEW / HOLD_WORKLOAD / PARK_KV_ONLY_ENGINEERING_RESULT`.  
**RESULT:** Codex-reported Phase0 environment PASS, Phase1 model PASS, Phase2 bitwise correctness PASS; Phase3 K0 micro savings 63–68% but synthetic E2E max +2% below predeclared ~3% value gate, no established paper novelty.  
**NEXT_TEST:** `NONE_FOR_PARKED_EAGLE3` unless PI provides meaningful production trace/new mechanism.  
**NEXT_ACTION:** PI-selected `EAI-P / EAI-010 READ-ONLY RAW_EVIDENCE_AND_QUALITY_AUDIT`. Revisit exact reported native 320.145 vs conversion 254.942 tokens/s (+25.576%), and 255-position mean absolute NLL difference 0.092033 nat, verify from real artifact, establish source/kernel/quality baseline and prior art, design **one cheapest falsifiable test** before new Codex/GPU. EAI-P numbering is separate; EAI-SYS S55 remains NOT_STARTED.  
**STATE_UPDATE:** `YES` only once GitHub commit and readback are verified.
