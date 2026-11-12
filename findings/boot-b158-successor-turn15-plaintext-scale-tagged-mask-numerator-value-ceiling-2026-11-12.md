# BOOT / B158_OVERALL — Successor Research Turn 15/25
Date: 2026-11-12 Asia/Singapore
Candidate: boot-b158-scale-tagged-selector-numerator-v1
Phase: PROBLEM_SELECTION
Final decision: PARKED / PASS_STOCK_SCALE_INTERFACE / FAIL_SINGLE_MASK_16BIT_OPERATOR_CEILING / NO_CREDIBLE_COMPLETE_MECHANISM
No native/Codex execution.

## Authority and distinctness
TRACK_ID=BOOT; ACTIVE_SUBLINE=B158_OVERALL; controller ACTIVE=UNKNOWN and no backups at entry.
Pre-read verified:
- prior Turn14 findings/boot-b158-successor-turn14-centered-public-mask-integer-lift-minimax-gate-2026-11-12.md, Git blob aea0608a924b31b810610e9f41bdc3d75d16a5be (PARKED). Turn14 optimizes a fixed coefficientwise R_T lift, whereas this distinct candidate changes plaintext metadata Scale and thereby the plaintext R_T element actually embedded (αM) while preserving the DECODED selector M after normalization by α in the ciphertext scale.
- findings/boot-B175-public-mask-convolution-screen-2026-10-29.md blob 98cf77cd70f589812f48fe904e0d4f8c2c86eb09, source-reconstructed c2/d2 and M0..M3, support sizes 9 and 7, centered L1 norms 214538 and 79086 respectively.
- findings/boot-B175-public-mask-operator-kernel-screen-2026-10-29.md blob 36798b49f9cbfacf05e303943d559e166aef774b, actual RNS residual E_mask=rho_Q(A_Q*e+C_A(m)); integer-lift-only norm is not full carry or DFR.
- findings/boot-B158-residual-structural-rescue-scout-2026-10-28.md blob d87795880d9df2f16c710f38fc7dfd94a0f4d771, late B163 selector +20/+26 required-logQ increments.
- findings/boot-B175-source-level-si-error-bounds-2026-10-29.md blob c75aa60e080b28b688de7ee8859c5df4d1951c02, dominant terminal E_tref and no complete B175 rescue.

## One preregistered paper-changing test
QUESTION: Can a nonunit plaintext scale α∈F_T^* representing mask numerator αM, tracked by BGV's ciphertext Scale, avoid the large centered coefficient denominators of the B158/B175 selector masks and yield a justified >=16 required-bit end-to-end fixed-Q recovery at no extra ciphertext multiplication cost?
CURRENT_BELIEF: Lattigo v6.2.0 deliberately supports plaintext Scale; applying αM rather than M is semantically correct after output Scale multiplication, but single-mask L1 operator improvement for known masks is bounded by support and cannot by itself supply >=16 bits, and complete mixed-branch/carry gains are unverified.
CHEAPEST_DECISIVE_TEST: Authenticate v6.2.0 Encoder.EncodeRingT and evaluator plaintext multiplication scale laws; derive full functional equality when both public selector branches share α; use independently reconstructed archived mask L1 and support to establish an optimistic theoretical ceiling on any α∈F_T^*. No native.
IF_PASS: If both whole-output source semantics and a >=16-bit useful error/DFR advantage after all alignment and conversion costs can be established, retain ACTIVE and specify smallest correctness canary after source audit.
IF_FAIL: If stock scale mechanism exists but the singled-out mask improvement cannot hit the 16-bit threshold and no authenticated full-recurrence error contraction or independent novelty exists, PARK the scale-tag-only direct rescue.
IF_UNCLEAR: Preserve uncertainty for genuinely coupled multi-mask stage schedules, actual Q-carry and stochastic DFR; require complete source-typed schedule and legal-family evidence before implementation.
WHICH_PAPER_GATE_CHANGES: Gate1 exact decoded mask and scale/carry semantics; Gate2 stock type/scale interfaces; Gate3 optimistic fixed-Q error and complete value ceiling.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: It distinguishes a genuine stock-supported representation mechanism from the unsupported claim that using plaintext Scale automatically yields a paper-level noise advantage, and excludes single-mask-only >=16-bit rescue without native cost.

## Source audit (verified via GitHub connector, Lattigo v6.2.0)
Tag v6.2.0, tuneinsight/lattigo/schemes/bgv/encoder.go blob db146d55271b67f868a53fca94ebf7a6d3a01974:
- lines 203-259 EncodeRingT: place user slot values at permuteMatrix indices, apply RingT INTT, then ringT.MulScalar(pT, scale.Uint64(), pT).
- lines 264-323 EmbedScale: uses metadata.Scale to embed; optional T^-1 modulo Q scaling in RingT2Q.
- lines 340-347 DecodeRingT: multiply RingT polynomial by scale^-1 before NTT decoding.
Tag v6.2.0, tuneinsight/lattigo/schemes/bgv/evaluator.go blob 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f:
- lines 445-465 and 729-750 vector operand overload explicitly makes temporary plaintext Scale=1, so candidate MUST use an explicit degree-zero plaintext with metadata.Scale=α, not the []uint64/[]int64 convenience overload.
- lines 669-681, 716-725: plaintext degree-zero multiplication uses tensorStandard, not a BFV-style new ciphertext-ciphertext tensor/relinearization.
- output Scale product on plaintext path (Mul docs and tensorStandard source); Add between differently scaled elements uses matchScaleThenEvaluateInPlace lines 120-140,227-243; this may add noise, hence compatible branch planning is mandatory.
Source functionality is real, NOT a novel scale API. It is closely related to BGV scale tracking and polynomial coefficient scale planning in published Lattigo discussion 401 (2023), and the technique in ePrint2020/1203 referenced therein. Novelty for complete B158 application is NOT established.

## Ideal semantics, not fake metadata relabeling
Let coefficient mask M∈R_T, public invertible α∈F_T^*, and encrypted input with plaintext m and scale σ. Encode the ORIGINAL decoded slot mask M as an explicit BGV plaintext with Scale α. Encoder first creates the R_T polynomial αM, which is what gets lifted into Q. Ciphertext×plaintext produces physical scaled payload ασ·(Mm) with output metadata Scale ασ; BGV decoding removes ασ and returns Mm, provided exact source encoding and plaintext multiplication semantics hold. No ciphertext scalar inversion or manual metadata relabeling occurs.
For a general two-branch selector F=(1−M)+M Y (or corresponding ciphertext factors), encode both branch masks (1−M) and M at the SAME α, so the terms are at compatible output scale ασ; preserve constant terms using explicit compatible plaintext Scale and avoid gratuitous source scale-match corrections. A terminal ct×ct SI then receives inputs with changed scale metadata; the exact whole-output scale law must be propagated across the entire B158 recurrence, including case y=0, and Q reference carries and downstream extractor. This latter complete source-level propagation is UNKNOWN, not an experimentally supported PASS.
This mechanism differs from Turn14 fixed-R_T-integer-lift minimax: αM≠M in R_T, but decoded mask function can remain M when α is tracked and inverted by the normal decoder.

## Exact optimistic single-mask operator ceiling
For nonzero α mod T, multiplication by α is a bijection of F_T, so every NONZERO coefficient of M stays nonzero. For centered coefficients b_j=center_T(αm_j), every nonzero b_j has |b_j|>=1, giving
 ||center_T(αM)||_1 >= nnz(M).
For the archived B175 source masks:
 c2/d2: original centered L1=214538, support=9. For ANY α≠0, maximum conceivable improvement in the integer convolution induced l_inf operator norm is
 log2(214538/9) = 14.5409486804 bits <16.
 M0..M3: original centered L1=79086, support=7. Maximum is
 log2(79086/7) = 13.4637797853 bits <16.
These are extreme optimistic upper ceilings; equality need not be achievable because α is ONE shared field scalar acting on all polynomial coefficients, not independently selected per coordinate.
The B175 final SI has 664 required bits and logQ 649, requiring at least 16-bit required-bits reduction to achieve strictly positive budget (<=648). Thus neither ONE of the known public mask operators, considered as sole source of the deficit with unchanged rest of computation and measuring only its integer convolution operator norm, can independently certify the needed 16-bit recovery. Multiple masks or changed upstream residuals COULD combine benefits; the above is NOT a whole-algorithm impossibility, and not a bound on actual residual or DFR.
The numeric signal also cannot be conflated with B158 late M_k whose exact RingT coefficients/support have not been authenticated here. Archived B163 selector noise rises +20/+26; this requires full recurrence and actual Q-carry evidence.

## Additional exploratory example NOT source-level evidence
A read-only approximate NTT reconstruction was attempted for illustrative alternating-block selectors in a 32768-slot permutation under assumed primitive 65536th root 3. For k=1024,2048,4096,8192, power-of-two α from 1 to 1024 gave L1 values of the same rough order, not ~2^16 reduction (e.g. k4096 α1=134115624, α2=133286351). The illustrative slot assignment and NTT indexing were NOT independently checked against original B163 exact masks or v6.2.0 RingT output, so this exploratory calculation must NOT support a native value/noise verdict. No claim of B158 measured coefficient norm or DFR is made from it.

## Gate decision and cost
Gate1: ideal decoded plaintext mask semantics PASS_SOURCE; full fused B158/B175 post-scaling Q/carry/whole-output UNKNOWN/BLOCKED.
Gate2: explicit plaintext Scale=α encoding and resulting output-scale propagation are stock v6.2.0 interfaces PASS_SOURCE; vector convenience overload silently forces Scale=1, so it must NOT be used.
Gate3: FAIL_SINGLE_MASK_16BIT_OPERATOR_CEILING for archived selectors and UNSUPPORTED_ALL_IN_VALUE for the full recurrence. The candidate has no matched baseline/DFR and no audited reduction of terminal E_tref; extra scale alignment, key and memory costs unmeasured; adjusting α may create large coefficients or carry, and prior art already supports scale planning. No performance claim.
STATUS=PARKED, NEW_MECHANISM=NO_CREDIBLE_NEW_MECHANISM for the *standalone scale-tag-only 16-bit B175 rescue*.
REOPEN_CONDITION: An independently authenticated full B158/B175 source-typed numerator/Scale schedule over all mask branches and full 8-block+zero-root semantics, actual coefficient/carry-aware >=16 required-bit recovery or useful complete DFR, fair all-in runtime/key/memory/offline cost, security and independently audited novelty beyond BGV scale planning. A mere smaller one-mask L1 or scale metadata change is insufficient.
ELIMINATED_UNCERTAINTY: Can scale-tagged explicit BGV plaintexts encode a physically scaled public mask while preserving decoded mask semantics (yes), and can a SINGLE known B175 mask operator alone offer 16 bits of integer convolution-operator norm reduction under such scaling (no, by immutable support size)?
DECISION_CHANGED=true; no native. Research_frontier_exhausted=false.
