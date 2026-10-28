# BOOT — Post-B162 structural scout: Descent-compatible MVB
Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER_LEVEL / SOURCE_LEVEL
CODEX: NOT_USED

## Authoritative state preserved
LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE: B163_PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
B145+B152: PARK / FAIL_NATIVE_VALUE
B158_ALGEBRA: PASS
B158_CTCT_MULT_COUNT: OPTIMAL
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B158_NATIVE_FEASIBILITY: UNRESOLVED
B162_B161_HYBRID: VALID_FAIL_AT_K1024
B163: NOT_RUN

## Structural sources worth follow-up
- ePrint 2026/1779, *Bootstrapping via Ring Switching without Slot Recovery*: whole-stage slot recovery elimination already prior art. Unrestricted continuous CKKS independent nonlinear leaf evaluation is blocked by its affine-only criterion.
- ePrint 2026/2368, *Low-Latency Parallel Digit Decomposition and Sign Evaluation for CKKS*: transform sequential bootstraps into one parallel bootstrap plus logarithmic carry correction with slot-capacity tradeoff. Do not transplant blindly into classical BGV digit extraction.
- ePrint 2026/2616, *Descent-PBS: Programmable Bootstrapping beyond the Ring Dimension*: module-rank penalty moved largely to first rotation; descent into ring and subsequent ring refinement already prior art. Residual first-module-rotation/descent bottleneck.
- ePrint 2026/2630, *Exact Error Bootstrapping and Comb Bootstrapping in FHEW/TFHE*: error refresh does not make arbitrary functional PBS free. Do not reopen generic free-functional extension.
- ePrint 2026/1847 and 2026/2076: symmetry-based BGV extraction is crowded; naive higher-order-symmetry idea deprioritized.
- Recent MVB (including 2026/2332 and 2026/2310) increases direct prior-art risk for generic rotate-once/read-many claims.

These source-derived summaries and candidate interpretations require full-paper verification before a novelty claim.

## New structural research question
Combine Descent-PBS and multi-value bootstrapping on several large-domain LUTs of the same encrypted input:
one function-independent first module rotation and descent, then several function-specific ring-side readouts.

The idea must not be stated as generic; Descent may discard information needed by a function-specific MVB factor.

## Algebraic necessary and sufficient condition
Let D:V→W be a linear descent map and B_f:V→V be the function-specific linear post-factor. An induced linear operator ~B_f on im(D) satisfying
    D B_f = ~B_f D
exists if and only if
    B_f(ker D) ⊆ ker D.

Proof: if induced operator exists, x∈ker D implies DB_fx=0. Conversely, define ~B_f(Dx)=D(B_fx); representative independence is exactly B_f(ker D)⊆ker D.

Consequences:
- GENERIC_DESCENT_MVB_AFTER_DESCENT: FAIL_GENERIC.
- Narrow candidate: C_D={B : B(ker D)⊆ker D}, and intersection with concrete MVB readout factors.
- Do not claim C_D contains useful LUT families before reconstructing exact Descent-PBS D.

## Next paper-level gate — DESCENT_MVB_GATE_1
1. Extract exact 2026/2616 truncation/FKS descent linear map D and its representation.
2. Characterize ker(D) and stabilizer C_D.
3. Express MVB second-phase plaintext-polynomial operators in the same space.
4. Compute the intersection; PARK if only trivial factors, advance to correctness/security/noise/value if a useful nontrivial LUT family survives.
5. Check whether 2026/2332, 2026/2310, or Descent-PBS already covers this intersection.

No Codex/native/GPU/server runs authorized. B163 stays highest priority once PI explicitly restores Codex quota.
