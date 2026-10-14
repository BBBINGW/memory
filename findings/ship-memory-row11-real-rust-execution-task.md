# SHIP row11 — Real Rust execution gate (RUNNER BLOCKED)

2026-10-14. STATUS: HUMAN_REVIEW / IMPLEMENTATION BLOCKED. This is a source-anchored execution specification, **NOT** a completed new cryptographic iteration or FHE ciphertext result. A more detailed handoff exists in the current conversation at /mnt/data/ship_hmux_row11_real_rust_execution_gate.md, SHA256 6b04aff2fec6d59833cf1860b79675e4614cfdb5c4cb6193be94f8cc60637e71.

Parent: SHIP, EUROCRYPT 2025, ePrint 2025/784. Implementation third-party Poulpy (NOT HEaaN), fixed source commit 250d4392656cd313f92ca66d96d8865702d39ddf. Read-before-write checked START_RESEARCH_SESSION, RESEARCH_PHILOSOPHY, AGENT, global STATE (separate active vFHE, read only), independent SHIP state after I214, and I214 source finding.

## Verified environment gate
Current runtime has NO cargo or rustc, no pinned Poulpy checkout; git ls-remote github.com fails DNS. GitHub connector reads pinned files but has NO available direct Rust execution/workflow-dispatch action. Upstream rust-toolchain.toml specifies nightly-2026-05-14, poulpy-ckks Cargo.toml supports test-utils and source test_suite/ship.rs has the needed helper patterns. Upstream .github/workflows/ci.yml includes AVX512-IFMA tests but does not run the as-yet-unimplemented variant. No upstream code or CI actions modified.

## ONE next actual falsification test
With genuine source-generated N16384 ternary dense sk and RNGs, in an in-crate Rust test use hmux_rot_key_encrypt_sk directly (same nonidentity public rotation) to generate just beta=false and beta=true raw keys at k_ct624, base2k52, dsize1. Inspect GGLWE input second column (col=1), gadget row11, physical k676/13 limbs. Apply gal_el automorphism to BOTH GLWE components, then OUT-OF-PLACE vec_znx_normalize with offset+40, res_k624/radix52, from 13 to12 limbs into a rank1 CKKS ciphertext. Stamp log_delta40, SlotsKind Complex, checked metadata. Do not substitute in-place normalize_assign.
Decrypt with genuine dense secret, quantify max coefficient and slot error for both beta bits, predeclaring screening tolerance <2^-18. Run ckks_prepare_right and check effective k624/log_delta40/Complex slots and IFMA prepared-right storage N*2*12*16=6MiB. On success test exactly ONE real widened ct×ct multiplication against independent nonzero ciphertext with a proper tensor key, verifying beta*x. Record exact commit, compiler toolchain, backend, command, seeds, first errors. Fail at any step and stop (no full 480-key benchmark).
Important: unmodified ShipPlan::raised_k formula still produces 468 when h32,ld40,budget_out104; one-key test must explicitly pass k_ct624. Full candidate must add an extra four mux depth field rather than abuse desired output budget field. No source change is claimed as implemented or compiled.

## Interpretation
I213 128/128 N16 exact modular cases are NOT genuine N16384 ciphertext execution. I210 augmented joint-key KDM security remains unproven, I207 81.45% IFMA prepared-key savings are only a conditional allocation model, I206 ~480 extra CT×CT and four serial depth levels unbenchmarked. No novelty claim or original SHIP attack.

NEXT_ACTION: provision/authorize real runner then execute exactly the above test, or PARK the branch. STATE_UPDATE:NO — no new cryptographic claim validated since I214. Global vFHE STATE and upstream Poulpy remain unchanged.