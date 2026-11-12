# BOOT / B158_OVERALL — Successor Research Turn 22/25
Date: 2026-11-12 Asia/Singapore
TRACK_ID=BOOT; ACTIVE_SUBLINE=B158_OVERALL
PHASE=PROBLEM_SELECTION
CANDIDATE_ID=boot-b158-preserve-step1-l19-unspent-prime-free-headroom-v1
STATUS=PARKED
VERDICT=FAIL_FREE_L19_HEADROOM_ACCOUNTING / NO_CREDIBLE_NEW_MECHANISM
NATIVE/CODEX=NOT_RUN
research_frontier_exhausted=false

## Authority and read-before-write
At entry ACTIVE UNKNOWN, no backups. Independently read and verified:
- findings/boot-b158-successor-turn21-fixed-logq-small-inverse-residue-si-tensor-value-gate-2026-11-12.md, Git blob 9d7c17a33e4c580e4201c05246cc8f9e19f73878, PARKED.
- findings/boot-B174-audit-si-grouped-marginal-and-pointwise-gate-2026-10-28.md, Git blob ffffc7e6a9c56ff0e4208a5c5ff5fe2cb786cf29: inherited LWE->RLWE Step1 normalization performs L19 to L18 rescale before polynomial basis; B174 GROUPED no rescale; N32768, T65537, LogQ=[36,34x18,30], LogP=[34,34,34,34].
- findings/boot-B175-source-level-si-error-bounds-2026-10-29.md, Git blob c75aa60e080b28b688de7ee8859c5df4d1951c02: terminal B175 SI required bits664, Q18 bitlength649, deficit15; dominant tensor/reference term.
- findings/boot-B158-checkpoint-decoupled-halfbasis-gate-2026-10-28.md Git blob 49a85b46bf23566b24324e0994b7f2830b136dc5.
- Primary Lattigo tag v6.2.0, schemes/bgv/evaluator.go, Git blob 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f, lines1353-1392.

## Distinct candidate and prior art
Propose retaining the original pre-Step1 L19 modulus and running the existing B175 babybasis, LT8, GROUPED, SI pointwise at L19. Hypothesis: the approximately 30-bit highest RNS limb otherwise consumed by Step1 is FREE extra modulus headroom and therefore necessarily repairs the B175 15-bit deficit with unchanged noise, plaintext, keys and source semantics. Unlike archived Turn5 post hoc modulus raising, no later lift is performed; unlike Turn21 small inverse scale residue, this changes the actual level. Closest prior art: routine leveled-BGV rescaling and scale-invariant BFV-style multiplication. Only the claimed free budget, not every possible redesigned L19 algorithm, is under test.

## Mandatory pre-registration
QUESTION: Is the Step1 consumed L19->L18 prime truly a spare ~30-bit modulus whose retention provides >=16 bits B175 final noise-budget gain without corresponding residual growth, scale changes, key or cost changes?
CURRENT_BELIEF: No. Normal BGV Rescale decreases both modulus and coefficient error and changes Scale. A scale-invariant evaluator's Rescale is a no-op. Level count is not noise headroom.
CHEAPEST_DECISIVE_TEST: Check audited B174 Step1 level path against exact Lattigo Rescale implementation and derive its Q/error/Scale accounting. No native.
IF_PASS: If source proves unchanged residual and compatible Scale at L19 while supplying full evaluation keys, retain ACTIVE for full correctness/security/DFR and cost audit.
IF_FAIL: If actual Rescale divides residual and updates Scale, PARK free-headroom hypothesis without native and do not infer any L19 design is universally impossible.
IF_UNCLEAR: If a fully redesigned L19 SI schedule changes tensor/reference carry favorably, retain that distinct mechanism as UNKNOWN until concretely specified, without a false free 30-bit claim.
WHICH_PAPER_GATE_CHANGES: complete ciphertext phase/scale semantics; source evaluator mode and key edges; optimistic noise and whole-system value.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: A free 30-bit headroom rescue would resolve a 15-bit deficit at near zero cost; if source already trades 30 modulus bits for 30 noise bits, no such shortcut exists and no native work is justified.

## Decisive source facts
Lattigo BGV source:
- lines1354-1361 explicitly documents last-prime Rescale divides noise, preserves plaintext while changing output Scale by qi^{-1} modulo T;
- lines1363-1366 if eval.ScaleInvariant is true Rescale returns nil (NO-OP);
- lines1381-1388 apply DivRoundByLastModulusNTT and Resize to level-1;
- lines1390-1391 assign updated Scale using division by consumed last prime qi.
Thus successful L19->L18 normalization does not preserve the raw error magnitude or Scale.
Writing q for consumed prime, Q19=q*Q18. If e19 is residual and e18 the residual after real Rescale, idealized accounting has e18 approximately e19/q plus a roundoff/reference-embedding term epsilon. If epsilon is negligible, Q19/|e19| approximately Q18/|e18|. Therefore merely retaining the extra q multiplies *both* the modulus and the unrescaled input noise at first order: the added approximately 30 logQ bits are not necessarily additional *relative* headroom. This is an idealized necessary-accounting argument, NOT an exact B175 full-circuit relation; tensor E_tref, CRT carries and rounding are nonlinear and remain UNKNOWN for a redesigned L19 run.
More subtle source interface issue: if the Step1 operator is a BGV evaluator configured ScaleInvariant=true, invoking its Rescale would NOT perform L19->L18. The audited transition must use a non-SI evaluator or some other explicit normalization path; detailed B174 call-site mode was not independently inspected this turn. One cannot simply remove an alleged SI Rescale without source call-site verification.
Preserving L19 also makes all downstream ctct, ctpt, rotations, NTT, key switching and eval-key level cost nonzero higher-level operations; extra RNS limb is not free online/offline. Security and post-evaluation ciphertext modulus Q increase and need explicit re-verification. The L19 schedule may still offer advantages for carefully costed carry/noise tradeoffs, but none are established here.
No 30-bit deterministic gain, 16-bit recovery, fixed-Q correctness, speed, DFR or novelty claim follows from this source. Standard rescale scheduling alone is not independent novelty. No native task launched.

## Gate disposition
Gate1: FAIL for asserted unchanged-error/unchanged-Scale transfer; complete new L19 phase/carry semantics unsupported.
Gate2: PASS_SOURCE for actual Rescale behavior and ScaleInvariant no-op caveat; typed Step1 call-site, high-level keys and new full construction UNKNOWN.
Gate3: FAIL_FREE_VALUE: extra Qbits are accompanied by larger pre-rescale residual and extra evaluation/key cost. Actual L19 final error and DFR UNKNOWN, not a no-go for all L19 designs.
STATUS=PARKED / NEW_MECHANISM=NO_CREDIBLE_NEW_MECHANISM as a free-headroom standalone paper mechanism.
NOVELTY_STATUS=PREFLIGHT; PAPER_READINESS=NOT_READY.
REOPEN_CONDITION: A genuinely new source-typed L19 Step1 path and complete algorithm, with full phase/scale/carry and zero-root output, measured or proven >=16bit actual final error advantage, matched security and evaluation-key/NTT/memory/offline+online cost, independent novelty. Merely retaining the consumed prime is insufficient.
ELIMINATED_UNCERTAINTY: Does the audited L19->L18 BGV Rescale consume 30 modulus bits without dividing error and changing Scale? NO. Thus a retained L19 modulus does not supply a source-proven free 30bit B175 noise budget.
DECISION_CHANGED=true; research_frontier_exhausted=false; no ACTIVE and no BACKUP after park.
