# BOOT — Descent × MVB broad-candidate closure
Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER/SOURCE LEVEL ONLY
CODEX_USED: NO

## Evidence
- TCHES 2024 multi-value bootstrapping already shares one blind rotation across multiple output functions on the same encrypted input, followed by function-specific public polynomial readouts.
- ePrint 2026/2332 explicitly studies the "rotate once, read many times" MVB setting with a function-independent shared rotation.
- An earlier public revision of Meta-PBS ePrint 2025/2284 mentioned simultaneous evaluation of multiple LUTs on one ciphertext; because the current abstract changed, record this only as prior-art risk.
- ePrint 2026/2616 Descent-PBS states publicly that module rank is paid only in the first rotation and that the accumulator is then descended into a ring by truncation plus functional key switching.
- Full 2026/2616 text could not be acquired in this session (ePrint 403, fallback unavailable, fixed mirror absent), so exact descent/FKS formulas remain unverified.

## Algebra gate
For abstract linear D and readout B, a global post-descent operator exists iff B preserves ker(D).
For the toy/model map that retains only the first M coefficients of K[X]/(X^N+1), multiplication by a public polynomial preserves that kernel iff the multiplier is constant.
This is a model-conditional no-go, NOT a theorem about the actual Descent-PBS FKS.

## Decision
The broad claim "share one expensive rotation and then read many functions" is already occupied by MVB prior art.

DESCENT_MVB_GENERIC = DEPRIORITIZE / HIGH_COLLISION_RISK
DESCENT_MVB_GLOBAL_POLY_COMMUTATION = CONDITIONAL_NO_GO
DESCENT_MVB_LARGE_DOMAIN_COMPATIBILITY = BLOCKED_SOURCE
ACTUAL_DESCENT_PBS_NO_GO = NOT_ESTABLISHED

Reopen only if the full 2026/2616 source becomes available or a concrete large-domain function family gives a cheap compatibility test.

## Authoritative state unchanged
LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE: B163_PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
B158_NATIVE_FEASIBILITY: UNRESOLVED
B163: NOT_RUN
