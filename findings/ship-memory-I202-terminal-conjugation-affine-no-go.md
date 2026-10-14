# SHIP I202 — No public-affine, conjugation-free paired-mask leaf

2026-10-14. Independent SHIP track following I201. Not global I-series or separate vFHE V-series. Source: `poulpy-fhe/poulpy` pinned `250d4392656cd313f92ca66d96d8865702d39ddf`; inspected `poulpy-ckks/src/encoding/ship/masks.rs` (blob 2754eafd1ad24c1eca1382204d37005449f88cca), `encoding/ship/coeff_enc.rs` (e0b5bb3e2cd5bb681a22b1798039061429ba17fe), `layouts/ship/{plan,secret}.rs` and `reference/ship/bootstrap.rs`. Independent Poulpy, not the SHIP authors' HEaaN. Read existing `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, SHIP state and I201, plus global vFHE state; do not alter global state.

## ONE HYPOTHESIS

H202: Existing two packed selectors C_A=M1+i*M2, C_B=M3+i*M4 can recover all four source-legal SHIP one-hot masked operands F=sum(Mk*Pik), using ONLY a public affine complex-linear leaf formula F=gamma+alpha*C_A+beta*C_B with no early conjugation and no new ciphertext-ciphertext multiplications. This would enable a naive attempt to defer conjugation to the original post-product-tree root. Counterexample criterion: one legal plan with four legal secret assignments at the same public slot/operand setting for which the affine equations are inconsistent.

## ONE SOURCE-LEGAL EXACT TEST

Plan: N=16, h=2, window=1, theta=1, log_gamma=6, log_delta_work=40, budget=104, mux_base=2; all fit `ShipPlan::new` checks. Sparse support slot0 allows j=15,0,1 and signs ±; slot1 can be fixed at j=8 to complete a globally legal sparse secret. At slot0 output index i=6, mask public rotation p=7, corresponding source index (i-p) mod 8=7. Choose public bottom ciphertext mask residues a[7]=0, a[15]=2^51, q0=2^52; the pinned coefficient encoder gives (pi1,pi2,pi3,pi4)=(1,1,-1,-1) in ideal slot semantics.

Poulpy's mask generator, evaluated at this source index:
- (j=15,s=-1): (M1,M2,M3,M4)=(1,0,0,0), (CA,CB)=(1,0), F=1
- (j=15,s=+1): (0,1,0,0), (i,0), F=1
- (j=1,s=-1): (0,0,1,0), (0,1), F=-1
- (j=1,s=+1): (0,0,0,1), (0,i), F=-1

Affine reconstruction forces four equations:
gamma+alpha=1; gamma+i*alpha=1; gamma+beta=-1; gamma+i*beta=-1.
First two give alpha=0,gamma=1. Third gives beta=-2. Fourth would require 1-2i=-1: contradiction. Exact SymPy rank(A)=3 and rank([A|b])=4 for A rows [1,CA,CB]. Hence **H202 FAIL**.

Why the naive postpone-to-root shortcut also fails: for two leaves F_j=(U_j+conj(V_j))/2, their product is one quarter times U1U2 + U1*conj(V2) + conj(V1)*U2 + conj(V1V2). The two mixed terms are lost if one computes only (U1U2+conj(V1V2))/4 at the end. This is an algebraic observation, not a full lower bound for all possible delayed designs.

Scope and caveats: the four-state impossibility rules out only PUBLIC COMPLEX-AFFINE leaf reconstruction from the two packed selectors, even allowing a public constant gamma. It does not rule out extra ciphertext-ciphertext multiplications (e.g. exploiting C in {0,1,i}), multiple branches, special mux automorphisms, more elaborate terminal product formulas, or other representations. No cryptographic implementation, noise or real latency test was run. The original M01 construction WITH per-leaf conjugation remains algebraically valid; its performance remains unknown. This is NOT a flaw in original SHIP.

Executed local reproducibility: `/mnt/data/ship_i202_source_onehot_affine_gate.py` SHA256 056012083dc41b3cded76e94f0686488b9e87366acf096d04800ec4bf33f3be8; JSON `/mnt/data/ship_i202_source_onehot_affine_results.json` SHA256 9a2d4c58447840e221a7c69c0e7e06365d2bd9fab65eee7887ff63e31a3d3eec. Both local only, no Rust/Poulpy ciphertext run.

STATUS: FAIL narrow H202; PASS exact legal-source counterexample. UNCLEAR universal delay-conjugation feasibility, original paired M01 real CKKS precision/runtime/memory, novelty.
RESULT: the free public-affine leaf reconstruction needed for a drop-in zero-extra-Galois rewrite is impossible at one legal SHIP source instance. M01's online Galois cost remains an unresolved tradeoff.
NEXT_ACTION: PI HUMAN_REVIEW to either enable one compiled pinned Poulpy in-crate masking-leaf baseline-vs-M01-packed test, or PARK the latency-neutral/no-extra-Galois subbranch. Do not substitute another toy benchmark for FHE timing.
STATE_UPDATE: YES independent SHIP state only, NO global vFHE STATE.md.
