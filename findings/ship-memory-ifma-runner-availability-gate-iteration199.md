# I199 — SHIP complex-packed selector: real IFMA runner availability gate

**Date:** 2026-10-14 (Asia/Tokyo). **Numbering:** PI's independent SHIP continuation, I199 after I198. Do not relabel or modify unrelated vFHE sessions.

## Read before write / authority

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` (SHA `db4175bdc29b0fb256a6f4d73d7722a559d749fb`), `findings/ship-memory-STATE.md` (SHA `de9b97eac83a5eccdb07c75e09df2a5779b24a16`), and `findings/ship-memory-prepared-ifma-cost-gate-iteration198.md`. Current `STATE.md` is maintained for an independent vFHE V-series and freezes the earlier global general-I counter at I192. It does not authorize replacing the separately PI-numbered SHIP I197–I199 sequence. **Do not change global STATE.md.**

Parent: Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, ePrint 2025/784; independent Poulpy implementation pinned `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf` (NOT authors' HEaaN).

Historical established facts: I198 conditional IFMA prepared selector payload: 512*4.5 MiB = 2.25 GiB baseline vs 256*4.5 MiB = 1.125 GiB complex-paired, at N16384,h32,theta4,base2k52,9 limbs. Ct×Pt terms remain 512; proposed circuit adds 64 per-column masking IDFT/normalizations and 32 early high-precision Galois key switches. This is source-layout arithmetic, not measured memory or runtime. I197 and SHIP-M04 already addressed ideal Galois key Gaussian/noise modeling; do not repeat.

## ONE PRIMARY HYPOTHESIS + ONE MINIMAL DECISIVE TEST

**H199:** This active execution environment, or an already directly executable runner accessible to this session without creating a new code-deployment workflow, is sufficient to run ONE real pinned Poulpy **baseline-vs-packed masking-leaf** check at the selected IFMA backend and parameters.

**Minimal decisive falsifier:** Check local `cargo`, `rustc`, pinned source checkout, compiled binaries, DNS access to GitHub and crates.io, and architecture/ISA. Independently inspect pinned repository backend and existing CI setup to see whether source requirements themselves are prohibitive or a usable remotely runnable test already exists. If no runnable compiled modified candidate nor a usable compiler+source/dependencies or a directly invocable CI execution mechanism exists, report **IMPLEMENTATION BLOCKED/HUMAN_REVIEW**, not a false functional PASS. Do not substitute a toy, re-run ideal error screens, or auto-build CI infrastructure.

## Evidence and precise outcome

**[FACT, local checks executed]**
- `uname -m` returned `x86_64`.
- `/proc/cpuinfo` first flags include `avx512f avx512ifma avx512vl`. Thus CPU hardware is **not** the immediate IFMA obstacle here.
- `command -v cargo` and `command -v rustc` produced no path. Targeted filesystem searches under `/usr`, `/opt`, `/home/oai`, `/home/oai/.cargo/bin`, `/usr/local/cargo/bin` found no toolchain.
- `/mnt/data` contained prior Python result files only, no compiled Poulpy executable or checkout. `git` exists; `git ls-remote --heads https://github.com/poulpy-fhe/poulpy.git` failed with `Could not resolve host: github.com`. `getent ahostsv4 github.com` and `index.crates.io` returned no addresses. `docker` was not found.
- The connected GitHub app can fetch source **text**, but its available interface contains no general `workflow_dispatch` call and cannot execute source code remotely. Read-only existing CI logs/artifacts cannot demonstrate a test of the **unimplemented candidate**. No remote modified test was invoked.
- **No Rust build, actual CKKS encryption/decryption, timing measurement, nor true peak RAM measurement was run.**

**[FACT, pinned upstream implementation requirements]**
- `poulpy-cpu-avx512/Cargo.toml` describes `NTT3x42Ifma` as needing AVX-512-IFMA and has `enable-ifma` and `enable-ckks` feature gates.
- `poulpy-cpu-avx512/src/lib.rs` requires x86_64 + AVX512F/AVX512IFMA/AVX512VL with compile-time target flags and runtime checks; prints the needed target-feature examples. The code does not guarantee CPU fallback for `NTT3x42Ifma`.
- `.github/workflows/ci.yml` pinned commit specifies `RUST_TOOLCHAIN: nightly-2026-05-14` and `avx512` job on Ubuntu 24.04; this builds with target-scoped SIMD flags and conditionally uses Intel SDE where native features are unavailable. Existing CI is for unmodified upstream, not the packed-mask candidate; SDE functional emulation is not a credible native latency benchmark.
- Exact source paths: https://github.com/poulpy-fhe/poulpy/blob/250d4392656cd313f92ca66d96d8865702d39ddf/poulpy-cpu-avx512/src/lib.rs and https://github.com/poulpy-fhe/poulpy/blob/250d4392656cd313f92ca66d96d8865702d39ddf/.github/workflows/ci.yml .

## Judgment, proposal, and restraint

**STATUS:** **FAIL H199 runner availability in this session**; **HUMAN_REVIEW / IMPLEMENTATION BLOCKED** actual CKKS matched masking-leaf benchmark. The hardware ISA passed, but compiler/source/dependency path and executable patched candidate are unavailable. This is **not** a negative result about the cryptographic algorithm's viability, memory saving, accuracy, or runtime.

**RESULT:** Identified a concrete execution barrier and an upstream-supported runner configuration: pinned Rust nightly, x86-64 + AVX512-IFMA/VL for native IFMA timing, and ability to build a *local isolated modification* of `ShipKeySet::generate/prepare` + masking accumulation before actual correctness/performance comparison. Do not conflate existing upstream CI tests with a packed variant test. No additional crypto claim, experiment or novelty outcome was obtained.

**NEXT_ACTION (requires HUMAN PI choice, one concrete decision):** Either (A) authorize/provide a reachable Rust build-and-run environment with pinned Poulpy checkout and dependencies, ideally native AVX-512IFMA Linux; perform **one** baseline-vs-packed `N=16384,h=32,theta=4` masking-leaf correctness/precision/elapsed time/prepared bytes/peak RAM test, or (B) **PARK** the SHIP complex-mask memory candidate for lack of decisive implementation evidence. Do not automatically switch research parent or repeat theoretical toy calculations.

**STATE_UPDATE:** **YES independent SHIP state** to record I199 HUMAN_REVIEW blocker. **NO global STATE.md**; no upstream repo modification.
