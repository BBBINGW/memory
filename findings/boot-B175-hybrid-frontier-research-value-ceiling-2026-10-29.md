# B175 Hybrid Frontier Best-Case Research-Value Ceiling

Date: 2026-10-29  
Session: Cryptography 10.0, Research Turn 21/25  
Track: BOOT  
Active subline: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Classification

- OVERALL_CLASSIFICATION: PASS
- SCOPE: BEST_CASE_RESEARCH_VALUE_CEILING_ONLY
- FRONTIER_A_INDEPENDENT_RESEARCH_VALUE: FAIL_AT_CURRENT_CLAIM_SCOPE
- FRONTIER_B_INDEPENDENT_RESEARCH_VALUE: UNCLEAR_LOW_CEILING
- NATIVE_CORRECTNESS: HYPOTHETICALLY_ASSUMED_FOR_THIS_SCREEN_ONLY
- VALIDATED_REDESIGN_CANDIDATE: NONE
- NOVELTY: NOT_ESTABLISHED

## Audited baseline

The B175 path through pointwise uses 26 ct-ct, 30 ct-pt, 30 rotations, and 30 key switches. Its full SI dependency depth is four. Adding the unexecuted leading multiplication projects 27 ct-ct. The serialized relin/Galois-key BinarySize is 1,114,150,880 bytes (1,062.54 MiB), not RSS or complete bootstrapping-key material.

## Best-case cost ceiling

Even under a hypothetical native-correctness PASS, both hybrid frontiers retain 26 ct-ct through output, 27 projected with leading, full SI depth four, 30 rotations/key switches, the same Galois/relinearization keys, and the same best-case evaluation-key size. Both increase total ct-pt from 30 to 31. Their only structural benefit is reducing the selector endpoint SI depth from three to two; this does not reduce the full depth.

Frontier A expands the lower-two-bit selector explicitly using `Y3` and `G01E`, then computes `SI(L,G01E)` and `SI(H,F2)`. It requires scale-alignment factors 256, -16, and 1 plus a custom plaintext/scale interface. Since `G01E = F0*F1`, it is a distributive expansion with no new functionality, asymptotic, count, full-depth, key, or memory advantage. Its independent-contribution ceiling is FAIL: engineering interface repair only.

Frontier B computes `ACC1=SI(F0,F1)`, `Z=SI(L,Y4)`, `A2(L)=d2*L+c2*Z`, and `OUT=SI(ACC1,A2(L))`. Its scale factors are only -1 and 1, but it couples LT8 into selector formation and breaks the modular GROUPED/LT8 interface. Since `A2(L)=L*F2`, this is multiplication reassociation/distributivity. Its independent-contribution ceiling remains UNCLEAR_LOW_CEILING: only a general, provable, prior-art-distinct BFV/BGV SI component-lift/Q-carry scheduling theorem could elevate it beyond an instance-specific engineering repair.

## Novelty boundary

Selector algebra, Paterson--Stockmeyer/block scheduling, multiplication reassociation, BSGS/hoisting/key tradeoffs, and generic noise-aware operation ordering are established categories. Neither frontier currently supplies a new plaintext identity, asymptotic, depth/count/key advantage, or native/runtime evidence. A future contribution would need a nontrivial family-level theorem showing systematic fixed-Q correctness-region improvement without increasing ct-ct count, full depth, or keys, and without secret-dependent gauge or selected randomness.

## Next no-regret test

Run a universal schedule-dominance impossibility screen. Use the Turn-17 gauge sensitivity to seek legal component representatives that reverse the relative noise ranking between the current schedule and Frontiers A/B. A ranking reversal would rule out a deterministic schedule-dominance theorem over all legal component representatives and confine any residual claim to distributional, instance-specific, native, or DFR evidence, all currently blocked by BOOT-DECISION-001 and B176 NOT_AUTHORIZED.

No Codex/native experiment, parameter sweep, B176, DFR test, implementation, or track/subline change was performed or authorized.

## Research-GPT evidence identifiers

- REPORT_SHA256: `6a7989c7cd26490b2a719fe5f2c114d932d9ad1c378bbf857d906eef779b5ac1`
- CSV_SHA256: `955767901de22dfcb4a0ac8d31c60f348765a11a1e4e5c1071a73dcb479ec942`

