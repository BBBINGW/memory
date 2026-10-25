# EAI-P / EAI-010 — raw evidence recovery checkpoint (2026-10-25)

**Scope:** EAI-P prior native q8K/q4V FlashAttention result; continuation of the current PI-selected read-only audit. This is **not** a new EAI-P numbered experiment and not EAI-SYS SCOUT-S55.

## Hypothesis / minimal decisive test

H: Existing remote EAI-010 and EAI-009R evidence contains the raw paired measurements and scoring table necessary to check the reported 32K decode throughput and explain the conflated NLL statistics *without rerunning GPU experiments*.

**Cheapest test already delegated to Codex:** inspect original remote manifests/paths read-only, verify existing hashes, parse pre-existing raw CSV and scoring records, check provenance, and produce a portable sanitized ZIP. The user provided the Codex completion report; the current GPT session does **not** have bytes of the Mac-local ZIP.

## Result and provenance

**[FACT — user-provided Codex report, not independently inspected]**
- `STATUS: PASS_EVIDENCE_RECOVERED`; EAI-010 manifest **143/143**, EAI-009R **129/129** pass remote checks; pinned `ggml-org/llama.cpp@f849095365d5ac1f560886a4e6574531d559e96f`; source tree reported clean, model SHA256 reported verified.
- Paired native-vs-conversion 32K throughput from existing raw runs: Native `320.145267516 tokens/s`, Conversion `254.941605844 tokens/s`, reported gain `25.575920202%`. No new GPU benchmark/quality run/build/download/source modification.
- Full paired 255 Token/Target/Prefix positions across Native/Conversion/F16 reported aligned.
- `mean(abs(NLL_native-NLL_conversion))=0.092033067989` nat, vs `abs(mean(NLL_native)-mean(NLL_conversion))=0.002821804440` nat. Original conflation is confirmed by Codex's recovered CSV computation, **not yet independently checked from the actual CSV by GPT**.
- Two nvidia-smi logs bearing remote-runtime tokens excluded from sanitized package, while original hashes/remote-check results retained.
- Result ZIP reportedly `EAI-010-RAW-EVIDENCE-AUDIT-2026-10-25.zip` size **44,599,217 bytes**; reported SHA256 `4f695731ad080f65c8903b75fe79a82ab33555d15ad7ef82c9ef1884f4bdf6ac`, `unzip -t PASS`. It resides on the user's **Mac local filesystem** at `/Users/bingwu/Downloads/论文/AI科研/`, **not automatically accessible to GPT**. This report is **NOT** independent ZIP, hash or original sample verification.

**[DERIVED — assistant independently recomputed arithmetic from user-supplied aggregates]** `(320.145267516/254.941605844-1)*100=25.575920201859258%`; per-token `1000/native=3.1235820ms` vs `1000/conversion=3.9224669ms`, ≈0.7988848ms savings/token under this fixed benchmark's aggregate throughput numbers. Arithmetic consistency is verified; experimental methodology remains unaudited.

## Prior art constraint

**[FACT — inspected GitHub issue metadata/body]** [ggml-org/llama.cpp Issue #30001](https://github.com/ggml-org/llama.cpp/issues/30001), created **2026-10-05**, independently proposes enabling selective native `q8_0-q4_0` FlashAttention instead of fallback F16 conversion, with RTX4090 / Qwen2.5-7B / context32K result **88.07→110.98 tok/s (+26.0%)** and build-size tradeoffs. This is highly pertinent prior art for *selective native-kernel enablement*. It is not evidence that the complete source patch/quality characteristics are identical; compare exact mechanisms before final novelty verdict. Current verdict `NOVELTY_NOT_ESTABLISHED / STRONG_PRIOR_ART_OVERLAP`.

## Limitations / next gate

- 255-position NLL difference **is not** downstream quality degradation proof; 32K task quality untested. Pointwise |delta NLL| and |difference of means| are distinct, and the small latter value can hide cancellations.
- The GPT current working environment **cannot access** the user's `/Users/bingwu/...` Mac local path and does not contain the new 44.6MB ZIP; cannot truthfully report `INDEPENDENT_AUDIT_PASS`. The file needs to be uploaded into this chat or another GPT-accessible user-approved source.
- The old EAI-009R research report already raised this exact NLL-statistic discrepancy; recovery confirms the earlier suspected confusion rather than establishing a new algorithm.
- No new GPU experiment, remote write or kernel/code change is authorized by this note.

**STATUS:** `PASS_EVIDENCE_RECOVERED_CODEX_REPORTED / GPT_RAW_AUDIT_PENDING`.
**RESULT:** Existing raw experiment bundles recovered and remote manifest validated; report-level paired speed and NLL measurements numerically coherent; independent source/raw inspection pending; no paper novelty proven.
**NEXT_TEST:** Upload the exact ZIP to the conversation, verify SHA256/manifest and recompute 3 paired run metrics and 255-row NLL distribution from original files; identify precise numeric path and quality gate. First check files **without new Codex/GPU**.
**NEXT_ACTION:** `USER_UPLOAD_EAI010_2026-10-25_RAW_ZIP_FOR_INDEPENDENT_GPT_AUDIT`.
**STATE_UPDATE:** `YES` for this note only after GitHub commit + readback; no source experiment rerun.
