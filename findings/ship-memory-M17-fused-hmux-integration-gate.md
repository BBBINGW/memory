# SHIP-M17 — Fused HMux compiled integration gate: IMPLEMENTATION_BLOCKED, no synthetic substitute

**Date:** 2026-10-14 Asia/Tokyo. **Independent SHIP M-series:** M17 COMPLETED as an execution-readiness gate; M18 NOT STARTED and the β-helper fusion engineering branch is **PARKED until a Rust-capable runner exists or the PI redirects research**. User/PI authorized M17 with “好的，请继续” after M16.
**Research target:** Evaluation-key memory for SHIP (Cheon, Hanrot, Kim, Stehlé, EUROCRYPT 2025; ePrint 2025/784). Audit of **independent Poulpy**, not authors' HEaaN. No original-paper flaw claimed.
**STATUS:** **IMPLEMENTATION_BLOCKED / HUMAN_REVIEW**. The actual fused IFMA kernel was **NOT** implemented, compiled, or tested; no encrypted CKKS bootstrapping parity, wall-clock speed, or peak-RSS results exist. This is not a scientific FAIL of the proposed algorithm, only a negative environment/execution gate. Do not relabel M16's exact-ring toy PASS as a Rust integration PASS.

## Read before write and conflict avoidance

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `findings/ship-memory-M16-radix52-dft-limb-carry-gate.md` SHA `850aafe94e5ee9c96ea7c1d70ad559722419949f`, M15 SHA `0c53414fc4e3b37372138ac0fccd018e92380aa6`, and checked separate `findings/ship-memory-STATE.md` (concurrent I217, SHA `bcc3b86af3cdd4c6954b14f6ddbf0b7dac04db5b`) and global `STATE.md` (vFHE V17, SHA `7af97fb3ee38ae139fd12f867fd9eccb18d22d16`). The intended independent M17 target did not exist. **DO NOT write/replace either shared state or old finding files.**

## ONE primary falsifiable hypothesis + ONE decisive environment/execution gate

**[HYPOTHESIS M17]** The currently available container/connected tools can obtain the fixed Poulpy checkout, compile with Rust and the IFMA backend, and run a **real encrypted** fused-group parity experiment to distinguish correctness/precision failures from M16's merely abstract limb-placement agreement, with measurements of runtime and total evaluation-key memory.

**[DECISIVE TEST]** Check `cargo`/`rustc` executability, a local Poulpy clone, suitable CPU flags, possibility of obtaining the original pinned source/toolchain and performing a compiled test via available execution facilities. Reject/mark blocked if the executable toolchain or source cannot be obtained. Do NOT substitute another toy or uncompiled source speculation for runtime parity. If blocked, deliver an executable-specification/runbook that will let a Rust-capable host run the first true gate and PARK the branch.

## Actual executed environment checks [FACT]

Executed in current container:
- `which cargo`: **nothing**; `which rustc`: **nothing**. No binaries in inspected `/usr`, `/opt`, `/root` standard locations, and no cached rustc/cargo deb packages.
- `/usr/bin/git` exists; `/usr/local/bin/curl` exists. No local `/mnt/data/poulpy*` or `/tmp/poulpy*` checkout.
- `uname -m` is **x86_64**; `/proc/cpuinfo` flags include **avx512f, avx512ifma, avx512vl**. Hardware feature support is **not** the blocking dimension.
- `git ls-remote https://github.com/poulpy-fhe/poulpy.git HEAD` fails `Could not resolve host: github.com`. `curl -I https://static.rust-lang.org/dist/channel-rust-stable.toml` fails `Could not resolve host: static.rust-lang.org`; container outbound DNS prevents fetching sources and rustup.
- Connected GitHub connector can READ named repo files, but cannot execute a Rust binary. Available GitHub connector actions expose workflow runs/logs, yet NO `workflow_dispatch` endpoint; do not create experimental repositories, branches, or new CI infrastructure without PI decision.
- Consequently **0 real Poulpy compilations**, **0 full encrypted CKKS decrypt/parity runs**, **0 trustworthy runtime/RSS benchmarks** this iteration. No other cryptographic hypothesis was tested.

## Pinned exact implementation entry point [FACT]

Independent source `poulpy-fhe/poulpy` pinned **`250d4392656cd313f92ca66d96d8865702d39ddf`**, live-source reads:
- Root `Cargo.toml` blob `0e91c0dbeba13df7def47d7ab85491b681e61f07`: workspace includes poulpy-ckks, poulpy-cpu-avx512, poulpy-core, etc., Rust 2024 edition.
- `poulpy-cpu-avx512/Cargo.toml` blob `160c39ba2a6c8ef05ccae0b0fee59511d62e49ef`: `enable-ifma`, `enable-ckks` feature names.
- `poulpy-cpu-avx512/src/lib.rs` blob `e702549f91a8575a144c600627b7f234f40ab573`: explicitly requires `RUSTFLAGS="-C target-feature=+avx512f,+avx512ifma,+avx512vl"` for `enable-ifma`.
- `poulpy-ckks/src/reference/ship/mux.rs` blob `e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce`: original `ship_mux_rotate` accepts **prepared full rank2** GGLWE groups. Changing keyset/type, independent scalar βhelper construction, public torus-body→integer representation, helper conv then shifted DFT limb into 19-limb buffer is a substantive **new implementation**, not a one-line adaptation.
- M16 mathematical source-semantics: shift **new β-body convolution DFT limb j to index j+1**, after correct 520-bit/428-bit torus modeling and independent keygen; public per-candidate Galois before summation; one per-group IDFT+normalize offset0. Unlike multiplying original GGLWE DFT limb by 2^52 (unsafe CRT wrap). All still unimplemented.

## Delivered reproducer contract [ARTIFACT]

Created and verified container path `/mnt/data/ship_m17_compiled_parity_runbook.md`; sha256 `82de18f6ecf76f3ad708511f1dcb1b6a1b6c85424aa60d41a99a3baf3f921ab3`, 6617 bytes. It details pinned clone and compile command:
```bash
git clone https://github.com/poulpy-fhe/poulpy.git
cd poulpy
git checkout 250d4392656cd313f92ca66d96d8865702d39ddf
RUSTFLAGS='-C target-feature=+avx512f,+avx512ifma,+avx512vl' \
  cargo test --locked -p poulpy-cpu-avx512 \
  --features enable-ifma,enable-ckks --lib ship -- --nocapture
```
**The command is NOT executed here and the test name filter is not guaranteed to match; list tests first.** More importantly, the runbook gives fail/pass criteria for the new βhelper GGLWE split implementation: independently generated β0/β1, output-secret Galois domain, high-magnitude positive/negative public body, signed radix52 carry near k428 boundary, multiple real HMux candidate groups, full CKKS decrypted slot errors vs original (max/RMS), peak RSS, complete evaluation-key payload, keygen time, real mux latency and end-to-end bootstrap latency. Security level and key joint distribution remain unproven; exact M05–M16 illustrative memory saving is **not** a measured secure win.

## End of iteration and strategic judgment

**STATUS:** **IMPLEMENTATION_BLOCKED / HUMAN_REVIEW**, not algorithmic FAIL/PASS.
**RESULT:** Hardware IFMA is present but no Rust compiler, no clone and no network to acquire them; no direct CI workflow execution tool. The next scientifically decisive evidence must be a compiled encrypted Poulpy variant; synthetic calculations are saturated at M16.
**NEXT_ACTION:** **PARK THIS M-SERIES ENGINEERING CANDIDATE** pending PI-provided Rust-capable runner or explicit decision to redirect to a genuinely different theory-first FHE research gap. On a capable host implement the *minimal key-helper parity first*, then one fused group, then full bootstrapping + memory/speed/precision. Do **not** start an M18 toy merely because the PI continues; either environment changes or PI chooses different target.
**STATE_UPDATE:** YES independent immutable M17 file only; do NOT overwrite global `STATE.md` nor concurrent `findings/ship-memory-STATE.md`. This M17 note + M16 findings provide a session handoff and prevent fabricated progress.
