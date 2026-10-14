# SHIP Evaluation-Key Memory — Independent State

**Last updated:** 2026-10-14
**PI-selected separate parent:** SHIP evaluation-key / prepared selector memory, Cheon–Hanrot–Kim–Stehlé, EUROCRYPT 2025 / ePrint 2025/784.
**Latest SHIP round:** **SHIP-M02 COMPLETED**, **SHIP-M03 NOT STARTED**.
**Research isolation:** Each SHIP round uses its own `findings/ship-memory-MNN-*.md` file. The shared repository `STATE.md` was simultaneously advanced by a distinct vFHE research session to I194; never infer current SHIP round from that shared state, and do not overwrite vFHE state in a SHIP workstream without PI coordinating the two.

**Completed SHIP-specific files:**
- `findings/ship-memory-M01-complex-paired-selector-key-gate.md` — ideal CKKS slot identity for pairing two secret-derived *real* selector masks in one complex ciphertext; 4hθ → 2hθ prepared object-count candidate, costs online conjugation and extra accumulator.
- `findings/ship-memory-M02-early-conjugation-source-modulus-gate.md` — source-verified existing Galois -1 key and aligned-k conjugation path at masking precision; level/key gate PASS; **real FHE encryption/decryption/noise/latency UNCLEAR**.

**Active open obstruction:** The planned paired selector reconstruction adds ~h early key switches for real and ~2h for complex SHIP, before mux/product tree. The existing Galois key supports source-level lookup, but extra numerical noise and runtime may eliminate value. No performance results, published novelty, or security conclusion established.

**NEXT_ACTION, only when PI continues SHIP:** SHIP-M03 — in a *local scratch fork* of pinned `poulpy-fhe/poulpy` commit `250d4392656cd313f92ca66d96d8865702d39ddf`, do **one** rank-1 CKKS encrypt → packed masked-sum → conjugation → decrypt comparison with baseline using actual complex public P1/P2. Measure error and operational count at the same precision before full benchmark; kill if precision/key-switch frontier is unacceptable. One primary hypothesis, one minimal test. If executable Rust/CKKS environment cannot be made available, report evidence missing instead of assuming a pass.

**No active SHIP technical hypothesis before PI authorizes M03.** Preserve vFHE I193/I194 separately, no cross-archive merging.
