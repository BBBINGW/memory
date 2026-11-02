# BOOT / B158 — Research Turn 18/25 RETRY — native Step2 infrastructure recovery gate

Date: 2026-11-03 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1
Frozen recovery canary blob: 6ae4bc7e48e0390f8dec97429f4ddb89565928c0

## Logical-turn accounting

This file is the authoritative result of the SAME logical Research Turn 18/25 retry requested after continuation recovery.

The earlier file:

    findings/boot-RMFE-postdivide-turn18-public-artifact-reproducibility-gate-2026-11-03.md

at commit e21d683aebeaf12bf9a3b42e6e5d1b0f7bb12554 is retained as historical partial work but is superseded for Turn18 progression and does NOT count as an additional substantive turn.

## Read-before-write

GitHub Notes read remains degraded. Direct durable fetch recovered:
- Turn17 authoritative scientific state at commit 34a4eb3ba825f8dc377e94aace27984cd416519d;
- frozen canary source with blob 6ae4bc7e48e0390f8dec97429f4ddb89565928c0.

Repository main before this retry write was e21d683aebeaf12bf9a3b42e6e5d1b0f7bb12554.

## Primary hypothesis

The current execution environment still has at least one bounded route to execute the frozen Step2 recovery-only canary unchanged against the exact pinned HElib commit with HELIB_DEBUG=ON.

## Falsifier

FAIL current-runtime reachability if all bounded execution surfaces are unavailable:
- no local HElib/NTL;
- no package/network route to obtain them;
- no reusable pinned CI artifact;
- no workflow dispatch/create surface;
- no binary/source archive materialization route;
- and the only remaining option would be a large manual reconstruction of entire dependency source trees through per-file API fetches.

This falsifier is operational only. It is NOT a candidate-correctness falsifier.

## Attempt matrix

### A. Local build inventory

Present:
- cmake;
- g++;
- make;
- ninja;
- git;
- GMP development/runtime support.

Absent after bounded filesystem/package inspection:
- NTL headers/libraries;
- HElib headers/libraries;
- cached NTL/HElib source archives;
- cached relevant Debian packages;
- Docker;
- conda/mamba/micromamba environments containing these dependencies.

Therefore the canary cannot be compiled from the current filesystem state.

### B. Native package/network recovery

APT metadata/package recovery cannot reach configured Debian mirrors.

git ls-remote to github.com fails because the container has no usable external network path.

Direct-IP/host-resolution bypass tests also failed to establish a usable external connection, so this is not merely a DNS-resolution issue.

Mirror-direct archive attempts likewise could not create a reachable download path.

### C. Built-in proxy/browser surfaces

The environment variables mentioning NEKO/mitmproxy do not expose a usable HTTP CONNECT proxy to the container.

The local services on the discovered ports are internal tool/Jupyter/container services, not generic outbound HTTP proxies.

Headless browser execution did not provide a file-transfer route into the build container.

### D. GitHub connector archive path

The connector can read repository text files, trees, commits, workflow metadata, logs and workflow artifacts when an artifact already exists.

It cannot materialize a generic repository tarball/zipball into the container.

GitHub release source archives are generated tarball/zipball URLs, not release assets, and binary archive fetch is outside the text fetch surface.

The external download helper requires a successfully viewable source URL first; binary GitHub/mirror archive URLs could not satisfy that gate.

### E. Existing GitHub Actions path

Neither BBBINGW/memory nor BBBINGW/research-mcp currently contains a reusable .github/workflows entry.

The available GitHub connector exposes workflow read/rerun functions but no workflow-dispatch or workflow-create action.

The pinned HElib commit has no reusable workflow artifact exposed by the available commit-run interface.

Therefore no existing CI surface can execute the canary without creating new workflow infrastructure, which the current connector cannot do.

### F. Release-neighbor reconstruction check

The nearest easy public release after the pinned commit is HElib v2.2.2 at d7be6f0dca6fa6cad2b2a0923d024ac27ce2e445.

GitHub compare shows it is five commits ahead of the pinned commit. The visible delta is small and concentrated in CI/PSI/eqtesting/documentation-related files, so an exact rollback from a v2.2.2 source archive would be feasible in principle.

However the release has no binary/source asset object beyond GitHub-generated tarball/zipball URLs, and those archives cannot be materialized into this container through the available binary-transfer surfaces.

NTL 11.5.1 archives can be located on public mirrors in web indices, but the same binary materialization barrier applies. Recovering NTL alone would not solve the missing pinned HElib tree.

### G. Manual per-file reconstruction

Reconstructing the complete pinned HElib tree and complete NTL dependency by hundreds of individual text/blob fetches is theoretically possible but is not a bounded minimal decisive test. It would be infrastructure engineering orders of magnitude larger than the frozen scientific canary and would violate the paper-first cheapest-test discipline.

Therefore this route is explicitly rejected for this turn.

## Result

All bounded current-runtime execution surfaces have been exhausted.

Verdict:

    FAIL_STEP2_EXECUTION_REACHABILITY_CURRENT_RUNTIME
    RECOVERY_CANARY = NOT_EXECUTED

This means only:

    the frozen native Step2 cannot be executed in the CURRENT tool/runtime environment.

It does NOT mean:

    FAIL_HELIB_RECOVERY_ONLY_EXACT_Z625_CANARY

and it does not change any mathematical/static candidate result.

## Scientific state after retry

Turn17 remains the latest scientific correctness result:
- estimator-independent coefficient-L1 chain reaches L0-L3 / Algorithm4 entry;
- first Fe square is runtime-prime-set conditioned;
- native Step2 remains the mandatory evidence-order prerequisite.

No new theorem, correctness PASS/FAIL, security claim, value claim, novelty claim or performance claim is produced by this infrastructure retry.

Therefore:
    CORRECTNESS_GATE = BLOCKED
    BASELINE_CORRECTNESS = PENDING
    SECURITY_GATE = PENDING
    VALUE_GATE = PENDING
    AUDIT_GATE = PENDING
    PAPER_READINESS = NOT_READY.

## Reopen condition

Immediately retry the frozen canary unchanged if ANY of the following becomes available:
- a container/runtime with pinned HElib and NTL already installed;
- outbound package/source download access;
- a materializable pinned HElib/NTL archive;
- a reusable GitHub Actions workflow/artifact;
- a workflow-dispatch/create execution surface;
- or another native execution connector capable of compiling and running C++.

Do not repeat the same infrastructure probes unless one of those capabilities materially changes.

## Next decisive scientific test

Execute the frozen revised recovery-only canary unchanged against:

    homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

with:

    HELIB_DEBUG=ON.

Require exact stdout:

    PASS_HELIB_RECOVERY_ONLY_EXACT_Z625_CANARY
    calls=17
    pruned_coord_order=0,2048,6144,1024,7168
    pruned_branch_order=2,1,4,0,3
    branch_reorder_indices=3,1,0,4,2
    scalar_unit_28=PASS
    selected_dirty_lifts=PASS
    L0_L3_exact=PASS.

Only after this PASS may Step3 exact parameter/interface verification proceed.