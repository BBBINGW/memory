# SHIP Evaluation-Key Memory — Independent Research State

**Date:** 2026-10-14 (Asia/Tokyo).
**PI-selected parent:** SHIP evaluation-key resident/prepared selector memory, Cheon et al. ePrint 2025/784. NOT vFHE.
**LAST COMPLETED:** **SHIP-M03 COMPLETED**; **SHIP-M04 NOT STARTED**.
**STATUS:** M03 toy encrypted arithmetic PASS, precision-parity FAIL under simplified toy parameters; production FHE/latency/peak RAM UNCLEAR; **NOVELTY NOT VERIFIED**. Await PI continuation.
**Important isolation:** Global `STATE.md` belongs to a concurrently advancing vFHE I-series (most recently I195 on read). DO NOT overwrite that state from SHIP branch. Each SHIP round gets its OWN `findings/ship-memory-MNN-*.md`.

## One active candidate: complex-paired private selectors

**M01** `findings/ship-memory-M01-complex-paired-selector-key-gate.md`: pair two private real SHIP masks `M1,M2` via single complex ciphertext `C=Enc(M1+i M2)`, reconstruct linear masked sum by `(C(P1−iP2)+Conj(C(conj(P1)−i conj(P2))))/2`; one conjugation per entire masked accumulator after aggregating pairs. Source-shaped plaintext enumeration PASS, 4hθ→2hθ possible selector prepared objects, extra h early conjugations (real) or 2h (complex), and 2 accumulator transform paths. No novelty established.

**M02** `findings/ship-memory-M02-early-conjugation-source-modulus-gate.md`: pinned independent Poulpy commit `250d4392656cd313f92ca66d96d8865702d39ddf` has pre-existing dense-key Galois −1 key, early stage structurally supports same scale/k with no new multiplicative level; numeric noise and latency unverified.

**M03** `findings/ship-memory-M03-toy-rlwe-early-conjugation-noise.md`: local executable **N16 toy RLWE/CKKS arithmetic simulator**, NOT actual Poulpy. Encryption, polynomial negacyclic ct×pt, rescale Q2^104→2^74, CKKS slot encode/decode, Galois X→X^-1 plus independent evaluation-key radix-64 key-switch, decrypt on 8 fixed seeds. Source-shaped mask pair (bands k1,k4, j3, sign+1, p1,u2) and nontrivial public complex phases. All ciphertext reconstructions PASS coarse 0.001 tolerance, but worst baseline error ≈1.9595e−8 vs packed ≈3.1509e−6, with isolated added KS error ≈3.1526e−6. This FAILS negligible-KS-error hypothesis **in toy model only**. No 128-bit parameters, real HEaaN/Poulpy measurements, latency, or actual prepared-memory reduction.
Local script `/mnt/data/ship_m03_toy_rlwe_conjugate.py`, SHA256 `2642ad66d313a548c9dbd973521ecf1eeb2e464798da53dc02b6b81e83dd03f0`; JSON `/mnt/data/ship_m03_toy_rlwe_results.json`, SHA256 `2f3f3e2b7d6811151dc663dfe58c443c692be44c60d242d58eb6d8856436e7dc`.

## Main obstruction

Added per-leaf Galois automorphism noise might be multiplied through h-input product tree; keeping a pre-existing Galois key does not make online KS free. Toy results illustrate this error mechanism, not a paper/production failure. Separately ~h extra higher-k conjugations, two masking IDFTs and extra scratch may erase memory advantage.

## NEXT_ACTION — SHIP-M04 only after PI agrees

ONE source-grounded **noise falsifier**: examine pinned Poulpy automorphism key digit decomposition and output normalization and derive a conservative bound for early `k≈428` conjugation noise in a representative source-compatible plan, relating it to the full SHIP precision/error target. Prefer a mathematically decisive bound/counterexample before a full benchmark. If inconclusive because constants and correlations cannot be grounded, request one real Poulpy execution runner; do not claim a production failure from toy samples. One primary hypothesis + one cheapest decisive test; continue only by PI.

No changes to vFHE I193/I194/I195, original SHIP authors' HEaaN, or upstream Poulpy; no paper bug or publication claim.
