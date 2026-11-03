# BOOT — PI policy: prefer the configured server for future feasible native experiments

Date: 2026-11-03

TRACK_ID: BOOT

ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Explicit PI instruction

The PI explicitly instructed that future experiments which can safely and reproducibly run on the configured server should run there whenever possible.

This is a durable execution-policy override, not a scientific result and not authorization to duplicate, restart, or migrate a live task.

## Effective policy

- Codex remains the local ChatGPT-authenticated, zero-API-billing coordinator.
- New HElib/NTL builds, long native computations, multi-seed/DFR trials, and matched benchmarks prefer SSH host alias `hash0x0_polyser` after a bounded read-only preflight.
- The preferred container is `boot-b157-ubuntu2204:latest`.
- Every remote task uses a unique task-private directory below the relative remote root `.research-orchestrator/native`.
- At most one heavy native execution may run on the remote host.
- Source/dependency hashes, compiler/container provenance, logs, result JSON, source/test diff, and artifact SHA256s must be repatriated before completion is claimed.
- Local fallback is allowed only when remote infeasibility is recorded with concrete evidence.
- Benchmark timing excludes transfer, setup, container startup, and progress I/O.
- API, paid-credit, and billing fallbacks remain forbidden.

## Non-retroactivity

`BOOT-T11-R8-SMALL-CANARY-20261103-R2` was already live on the local host when this instruction was issued. It retains its original launch provenance and must not be cancelled, restarted, resubmitted, or migrated solely to adopt the new policy.

## Verified server preflight

The configured server was verified reachable through BatchMode SSH. It provides an x86_64 Linux host with 32 physical cores / 64 threads, 251 GiB memory, Docker access, and the preferred BOOT container image. At policy adoption time the server had approximately 9.9 GiB free disk, above the configured 6 GiB admission floor. The container exposes CMake, GNU Make, G++, Git, Python, NTL headers, and GMP headers; pinned HElib remains task-scoped and must be built from the exact authorized source.

## Implementation and audit contract

The orchestrator configuration records the PI source, injects the remote-native contract only into newly created Codex tasks, exposes the selected backend in the Dashboard, and requires a final `NATIVE_EXECUTION_HOST` provenance line. The doctor command verifies SSH, Docker image availability, and the configured free-disk floor. Missing or local-fallback provenance remains subject to Research GPT audit.

## Validation

- TypeScript typecheck: PASS.
- Production build: PASS.
- Full test suite: 159/159 PASS.
- Live remote-native doctor preflight: PASS.

