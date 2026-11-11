# BOOT / B158_OVERALL — Successor Research Turn 11/25
Date: 2026-11-12 (Asia/Singapore)
Phase: PROBLEM_SELECTION
Candidate: boot-b158-two-square-polarization-si-v1
Result: PARKED / FAIL_FREE_NOISE_DIVISION / FAIL_VALUE_SOURCE_DISTINCTNESS
No native or Codex task launched.

## Authority restored / distinctness
TRACK_ID=BOOT, ACTIVE_SUBLINE=B158_OVERALL, entering controller ACTIVE=UNKNOWN, BACKUPS none.
Read and independently verified:
- Turn10 findings/boot-b158-successor-turn10-affine-recentering-compensated-si-error-invariance-gate-2026-11-12.md, Git blob 4570d2919a284daa14eae844772336f77140b6d6 (PARKED);
- B175 findings/boot-B175-source-level-si-error-bounds-2026-10-29.md, blob c75aa60e080b28b688de7ee8859c5df4d1951c02;
- B176 archived order-eight packed CMux findings/boot-B176-order8-three-bit-packed-cmux-2026-10-29.md, blob 6159bc9c07e4ecc44a3783f7051e24939075396e.
- B175 native artifact SHA256 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa, Q_L18 bitlength649; LT8 required bits577, GROUPED633, SI final664; 32767/32768 decoded mismatches.
This candidate substitutes a CROSS CT-CT BGV SI multiplication with TWO SI SQUARES and a public linear difference (quadratic polarization), not an affine shift+compensation as closed Turn10; no public zero gauge, no change to centered Q->QMul basis extension, no alternate scheme switching.

## Registered decisive question, decisions, and gates
QUESTION: Can the identity AB = ((A+kB)^2 - (A-kB)^2)/(4k), with k matching B175 public scale metadata, be implemented with stock SI squares at fixed Q and give a genuinely smaller dominant tensor/reference noise or better all-in value than one B175 cross-SI multiplication?
CURRENT_BELIEF: Ideal phase-product noise identity reconstructs AB, not a contraction. Mod-T inverse of 4k is a large integer-lift factor, not a free exact integer noise division. The two SI squares cost at least two terminal ct×ct rather than one. New source-specific carry cancellation is possible in principle but unsupported.
CHEAPEST_DECISIVE_TEST: Compute exact B175 scale alignment k, the inverse 4k in F_65537 and its smallest signed lift. Prove ideal symmetric square polarization noise identity and quantify minimal operation count and quotient divisibility conditions. Compare to B175 E_tref domination. No native.
IF_PASS: If a typed stock source construction with an exact integer/CRT divisibility invariant and contraction of total dominant E_tref plus all costs exists, retain ACTIVE for scale/carry correctness and DFR gates.
IF_FAIL: If only the textbook mod-T identity holds, while the inverse has no certified small integer noise action and two squares increase ct×ct count without a source-backed 16-bit benefit, PARK.
IF_UNCLEAR: If the real SI quotient behavior could cancel correlated carry terms, preserve that possibility as UNKNOWN and require prequantized tensor/reference evidence, not a native offset/square sweep.
WHICH_PAPER_GATE_CHANGES: Gate1 exact whole-output and scale/carry; Gate2 stock SI square and correction interfaces; Gate3 dominant noise/DFR and all-in value.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: A genuine native square advantage would require a provable correction of the B175 failing tensor/reference term, not merely a polynomial identity that doubles terminal multiplications.

## Exact algebra and required scalar / ciphertext scales
T=65537. B175 scale_A=43352, scale_B=43178, and (scale_A * scale_B^{-1}) mod T = 256. This can be independently checked: 43178*256 mod65537=43352. Let k=256 as optimistic public scalar that aligns B's decoded plaintext value to A's scale convention; this DOES NOT itself prove stock Scale metadata compatibility. Form U=A+kB and V=A-kB; both sum ciphertexts require matching actual scale and modulus.
Exact plaintext-ring identity:
  U^2 - V^2 = 4 k A B = 1024 A B,
so AB = (1024)^{-1} (U^2-V^2) in R_T.
Since 1024*(-64)=-65536=1-T, the modular inverse is 65473, with minimal signed integer lift -64. Equivalently 1024^(-1) mod65537=65473.
The two SI square outputs, if both correct, have the same scale law sigma_U^2*(-Q)^(-1), but this is 256 * sigma_A sigma_B*(-Q)^(-1) modT if sigma_U=sigma_A; so the result's metadata need not equal original B175 output scale 30059. Any candidate must explicitly preserve the intended values under actual scale and later Algorithm5 interfaces, not manually relabel metadata.

## Exact ideal error invariant
Use ring elements A=M_A+e_A, B=M_B+e_B, with U=A+kB and V=A-kB. Under exact integer polynomial operations before rounding and with a TRUE exact division by 1024:
  (U^2-V^2)/(4k) = AB,
  so the output residual is E_AB=M_A e_B+M_B e_A+e_A e_B.
The quadratic terms of U and V cancel, but this is exactly the original cross-product residual; no systematic <=2^-16 contraction of the dominant ideal tensor/reference term is obtained. This does NOT establish that stock SI(U,U) and SI(V,V) have identical carry to SI(A,B); source-specific rounding/carry may differ.

Critically, -64 is a modular inverse over T, NOT exact integer division by 1024. If W=U^2-V^2=1024 AB at the ideal integer phase level, then multiplying by -64 gives
  (-64)W = (1-T)AB.
For the ideal noise direction E_AB, the raw integer multiplier is 1-T=-65536, not 1. A lifted reference re-encoding may absorb some message-dependent T multiples but cannot be presumed to absorb stochastic E_AB for all inputs. This is a necessary caveat for *all* claims of free noise reduction. In R_Q, one could instead multiply by 1024^{-1} modQ, since Q is odd, but then dividing a noisy, independently rounded W by 1024 requires a provable congruence/divisibility invariant: if W=1024 AB+epsilon with epsilon not divisible by 1024 as an integer, multiplication by inverse modQ sends the epsilon term to a potentially large centered residue; an inverse in R_Q is not a bounded integer division. The stock Lattigo v6.2.0 SI evaluator has componentwise rounding, RNS conversion, and relinearization; no new guarantee that the two independent SI rounding errors combine to an integer multiple of 1024 was demonstrated.

## Optimistic complete cost / novelty
Replacing one B175 final ct×ct with two square ct×ct operations makes at least 27 through pointwise, versus B175 26, before scale-alignment ct-pt, additions, public -64 multiplication, any special division/carry check, possible extra noise and keys. Even if source square path optimizes symmetric tensor arithmetic, no verified runtime, memory, key or DFR advantage. The old operation count (26) and positive headroom have not been rescued.
The concept is textbook quadratic polarization; squares are stock arithmetic rather than a novel cryptographic representation. A complete beneficial construction would need a NEW source-backed carry/divisibility and noise invariant, not this identity alone. Compare prior B175 distributive hybrid value ceiling and archived B176 selector screens; none grant special noise cancellation for this candidate.
Novelty PREFLIGHT, no independent novelty-clear assertion. No matching benchmark or source canary because optimistic decisive semantic/value gate fails.
Scope: This is a no-go for *free ideal tensor-noise contraction and free mod-T integer noise division via two squares*, NOT a universal no-go for all alternative BGV SI implementations, correlated rounding strategies, or cryptographic error correction. Exact actual output/noise of stock two SI squares remains UNKNOWN.
Decision: PARKED, NEW_MECHANISM=NO_CREDIBLE_NEW_MECHANISM for standalone polarization.
REOPEN_CONDITION: Exact audited Q/T scale-compatible stock or custom polarized multiplication implementing whole output for all legal phases, with a proven rounding-carry divisibility/cancellation invariant that shrinks the actual B175 aggregate E_tref by the needed >=16 required bits or provides a useful DFR, plus a positive end-to-end comparison that pays for two squares, corrections, keys and memory, and independent novelty beyond quadratic polarization.
ELIMINATED_UNCERTAINTY: Can the textbook polarization identity plus the B175-compatible modular scalar inverse alone provide free integer-noise division or eliminate the dominant ideal product error? No; ideal error is identical, while -64*1024=1-65537, not integer 1.
DECISION_CHANGED=true, research_frontier_exhausted=false, no pending native task used.
