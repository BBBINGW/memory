# BOOT RMFE R8 Native Source-Sufficiency Audit

Date: 2026-10-29  
Session: 密码学 11.0, Research Turn 15/25  
Codex task: `BOOT-RMFE-R8-BSGS-MIDDLE-FIXEDQ-NATIVE-20261029-R14-01`  
Classification: `FAIL_PINNED_SOURCE_SUFFICIENCY`

## Scoped verdict

```text
CODEX_TASK_STATUS: SOURCE_BLOCKED / PREREQUISITE_FAILED / NO_NATIVE_SCIENTIFIC_EXECUTION
INDEPENDENT_AUDIT: PASS_SOURCE_AUDIT
SCOPED_RESULT: FAIL_PINNED_SOURCE_SUFFICIENCY
RMFE_MECHANISM_RESULT: UNCLEAR
RMFE_CANDIDATE_KILLED: NO
```

The Codex `SOURCE_BLOCKED` result is accepted for the pinned source lineage. This is not a correctness, capacity, or noise failure of the RMFE mechanism.

## Independently confirmed source boundary

- Pinned HElib's `ThinEvalMap` contract assumes constant-valued slots. A nonconstant slot polynomial uses the full `EvalMap`; it cannot be substituted directly as an R8 extension-valued adapter.
- `msh086/subring_bts@290c716507110001abb6f747443a8bf8d0cd4a56` implements subring-secret encapsulation but does not contain the required RMFE encoder, five projections, `tau_i`, or R8 envelope interface.
- The candidate patch's `src/keys.cpp` old blob matches HElib commit `3e337a6`, not the pinned HElib commit `acdb264e1a991eaee35fd8b3c31bebe9528c49a1`; the native lineage is incompatible.
- The RMFE paper defines the abstract maps, projections, and SlotsToCtxts/CtxtsToSlots workflow, but its public materials do not specify a reproducible p=5, width-512 instance with evaluation points, defining polynomial/generator, basis embedding, projection matrices, and HElib integration.
- The published workflow applies `MultKey` to five thin ciphertexts separately. A direct single `MultKey` on an RMFE-packed R8 envelope is a BOOT redesign, not an upstream interface that can be assumed to exist.

The task correctly refused to substitute a fresh-encryption surrogate.

## Codex evidence boundary

Codex completed the source-independent preflight and reported:

```text
four specified hashes: PASS
S2C grouped-vs-direct basis images: 16/16 PASS
C2S grouped-vs-direct basis images: 16/16 PASS
expected per-map counters: 6 automorphisms, 16 ct-pt, 15 additions, 0 ct-ct
224^-1 mod 625: 399
preflight exit: 0
source audit exit: 0
patch check exit: 1
native executions: 0
serialized-key BinarySize: not generated
```

Artifact transport integrity was checked by the orchestrator host:

```text
artifact: BOOT-RMFE-R8-BSGS-MIDDLE-FIXEDQ-NATIVE-20261029-R14-01.zip
bytes: 174077
SHA-256: 469a07c41f1a89bd838e4bf7ef57ab105673ca66561344955d8f9ab228fef0fc
ZIP integrity: PASS
```

Research GPT did not receive the ZIP bytes and therefore did not claim a raw-artifact scientific audit. Its source-sufficiency verdict was independently established from the pinned sources and public interface descriptions.

## Preserved results

```text
PASS_STATIC_EXACT_MAPS: PRESERVED
PASS_STATIC_6KS_BSGS_SCHEDULE: PRESERVED
OPTIMISTIC_MAP_TAX: 27.315171823128 bits
NATIVE_CORRECTNESS: NOT_ESTABLISHED
WHOLE_PIPELINE_CAPACITY: UNCLEAR
DFR / RUNTIME / MEMORY_ADVANTAGE: NOT_ESTABLISHED
```

## Next cheapest decisive test

```text
RMFE_P5_W512_CONCRETE_INSTANCE_AND_ADAPTER_CLOSURE_GATE
CODEX_REQUIRED: NO — static algebra/source gate first
```

Define a new paper-consistent instance without presenting it as the authors' unreleased instance:

```text
G  = Z/625Z
G' = GR(625,512)
E  = GR(625,8192)
k  = 5
eta = 5^(4-1) = 125
```

The gate must explicitly specify the five evaluation points, the defining polynomial and generator for `G'`, the HElib slot-basis embedding, the five projection maps' Moore coefficients, the adapter from five projections to the `Y=X^1024` R8 envelope, and whether that adapter commutes exactly with boot-key `InnerProduct`, RM10 selection, and reverse unpacking.

If the commuting closure fails, kill the current single-MultKey envelope. If it passes, select a compatible HElib lineage before any new native task. Do not retry the incompatible patch or use a fresh-encryption surrogate.

```text
AI_PROVISIONAL_CHOICE: PARK_EXACT_AUNG_IMPLEMENTATION_REPLAY
AI_PROVISIONAL_CHOICE: RETAIN_RMFE_STRUCTURAL_CANDIDATE_CONDITIONALLY
INDEPENDENT_RESEARCH_AVAILABLE: true
RESEARCH_FRONTIER_EXHAUSTED: false
```
