# BOOT / B158_OVERALL — Successor Research Turn 6/25
Date: 2026-11-12, Asia/Singapore
Phase: PROBLEM_SELECTION
Candidate: boot-b158-limb-local-si-quantization-v1
Verdict: FAIL_LOCAL_CRT_QUOTIENT_SEMANTICS / PARKED
Native/Codex: NOT RUN

## Authority and distinctness
TRACK_ID BOOT; ACTIVE_SUBLINE B158_OVERALL. Controller entering turn: PAPER_CANDIDATE=UNKNOWN, backups none. Turn5 source finding findings/boot-b158-successor-turn5-public-l19-phase-preserving-modraise-no-go-2026-11-12.md Git blob 25a2073aa24dc50a9e0e9486f0faa205704a8614 (PARKED) read and verified at start. B175 source-level attribution findings/boot-B175-source-level-si-error-bounds-2026-10-29.md Git blob c75aa60e080b28b688de7ee8859c5df4d1951c02. Native B175 audit ZIP SHA256 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa: LT8 577, GROUPED 633, SI POINTWISE 664 required bits, Q bitlength 649, 32767/32768 mismatches.
Distinct mechanism proposal: replace the cross-RNS-limb centered quotient used in SI tensor quantization at an UNCHANGED fixed modulus Q with independent, parallel, no-cross-limb quantizers q_i for each RNS limb. Unlike Turn5, no persistent modulus extension; unlike Turn25, no change to centered ModUpQtoP component lift; unlike Turn2, no trace or projected carry; unlike Turn1, no standard BGV multiplication mode switch. It is a proposal to change the *nonlinear CRT quotient interface*, not only the error distribution.

## Pre-registered test
QUESTION: Can each output residue of the complete centered SI scaling quotient, z=round(T*x/Q) mod q_i, be computed solely from x mod q_i, with NO information from other RNS limbs or common CRT correction, for the full legal tensor component domain?
CURRENT_BELIEF: No, as nearest-integer scaling by T/Q is not a homomorphism or a local function on each q_i. The quotient depends on the entire CRT representative of x.
CHEAPEST_DECISIVE_TEST: Produce two valid centered x values, identical modulo one fixed q0 but different exact full-Q nearest quotients modulo q0. Use the actual structural inequalities of the B175 prime chain, not native execution.
IF_PASS: If such a limb-local representation exists, retain ACTIVE to specify per-prime evaluator, exact carry/reference semantics, noise/DFR and complete online/offline/key costs.
IF_FAIL: If a collision of local input residues yields different desired q0 outputs, PARK this no-cross-limb construction before implementation.
IF_UNCLEAR: Verify precise source quantizer operator (rounding/tie convention and auxiliary QMul interpretation) and retain UNKNOWN; no native experiment.
WHICH_PAPER_GATE_CHANGES: Killer gate 1, exact whole-output and carry semantics; then source feasibility and value.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: With an invalid quotient primitive the proposed replacement cannot be integrated into BGV for arbitrary legal tensor inputs. Its hoped-for reduced inter-limb conversion cost is moot without a distinct correction mechanism.

## Exact mathematical counterexample
Let Q=q0*Q1 where q0 is one B175 odd NTT prime, Q1 is the product of the remaining primes. T=65537 and all factors large; specifically Q1>2*T and q0>2. Work in R=Z[X]/(X^N+1), but use constant polynomials so scalar algebra suffices. Define x0=0 and x1=q0*k, k=ceil(Q1/T).
Then x0 mod q0=x1 mod q0=0. Also:
  T*x1/Q = T*k/Q1,
which lies in [1,1+T/Q1), a subset of [1,1.5) since Q1>2*T.
Therefore nearest-integer round(T*x1/Q)=1 and round(T*x0/Q)=0, independent of half-tie conventions (strict inequality at upper bound).
Furthermore x1/Q=k/Q1 <= 1/T + 1/Q1 < 1/2 for T>=3 and Q1>2*T, so x1 and x0 are legitimate positive centered integers in (-Q/2,Q/2). For any output prime q0>1, target residues are 1 and 0 mod q0. No function f_q0: Z/q0Z -> Z/q0Z can simultaneously satisfy
  f_q0(x0 mod q0)=0
  f_q0(x1 mod q0)=1.
The same argument works as a subproblem of coefficientwise tensor quantization in BGV. For full correctness over all arbitrary tensor components, even this simple constant-polynomial pair cannot be ignored.

This is a bounded, precise no-go: independently rounding each RNS limb without cross-limb information cannot exactly implement global centered round(T*x/Q) at fixed Q. It does NOT rule out HPS/BEHZ-style RNS algorithms with auxiliary correction bases, quotient estimation, carry sidecars, or other across-limb aggregates; nor does it rule out approximate quantization with a rigorously bounded DFR, which would be a different mechanism requiring proof.

## Structural source boundary and relevance
Pinned Lattigo v6.2.0 BGV SI path: schemes/bgv/evaluator.go, blob 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f; ring/basis_extension.go, blob fb9f0e877d928984b57b1db9917c03417f2fd211, as authenticated in the predecessor centered-lift finding. The exact v6.2.0 scaling/quantization is derived from a global Q-dependent centered quotient; the candidate's assumption that each limb can independently quantize the same integer is invalid by algebra. This turn did NOT implement or independently byte-audit the entire precise quantizer source, and the counterexample should be understood as a necessary-condition result for any exact full-Q nearest-integer scaling primitive, not proof of detailed source API failure.
Closest existing algorithmic family: classical RNS basis-extension, full-Q scale-and-round for BFV/BGV (including HPS/BEHZ-style inter-limb algorithms), and the pinned Lattigo scale-invariant multiplication. Novelty remains PREFLIGHT; no exact collision/independent audit verified.

## Why not a B175 noise rescue even if another correction exists
B175 source analysis bounds its actual quantization rounding and relinearization-only terms below 2^46 and 2^22 respectively, much smaller than the observed ~2^647 dominant tensor/reference term. Therefore making the quantizer cheaper or a few bits more accurate by itself cannot supply the approximately 16 required-bit rescue; a new inter-limb correction mechanism would need to additionally and substantially modify tensor/reference or Q-carry geometry, justify DFR, and prove complete system value after conversions, extra modular arithmetic, keys/memory, noise and offline costs. An unproved approximate quotient or one particular trace's coincidence is not a paper mechanism.
Killer gate 1: FAIL exact local quotient / whole-output primitive. This stops the candidate; no new source/native work.
Killer gate 2: BLOCKED for proposed source construction (no valid local primitive), existing global RNS quantizers remain feasible.
Killer gate 3: no demonstrated tensor/reference contraction or favorable all-in value. It would be a known optimization class even if corrected for cross-limb effects.
Status PARKED, NEW_MECHANISM=NO_CREDIBLE_NEW_MECHANISM for no-cross-limb exact SI quantization.
REOPEN_CONDITION: A concrete source-compatible cross-limb summary or correction sidecar with exact complete SI quotient/carry semantics (or a useful probabilistic error bound), plus a provable >~16-bit B175 tensor/reference noise/DFR benefit and positive all-in cost and independent novelty; mere per-prime division/rounding fails.
ELIMINATED_UNCERTAINTY: Can complete global centered SI rounding be implemented by independent q_i-local residue maps with zero cross-limb information? No, explicit exact collision.
DECISION_CHANGED=true from previously untested distinct proposal to PARKED. research_frontier_exhausted remains false. No pending native task inferred.
