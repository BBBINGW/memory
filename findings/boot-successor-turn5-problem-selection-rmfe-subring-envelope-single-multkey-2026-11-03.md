# BOOT / B158 — Successor Research Turn 5 — Problem Selection: RMFE subring-envelope single-MultKey candidate

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: PROBLEM_SELECTION
Native execution: NONE

## Authority / read-before-write

GitHub Notes repository state was recovered first. The immediately preceding durable result is:
  findings/boot-RMFE-postdivide-successor-turn4-second-Fe-cubic-P6-proof-no-go-2026-11-03.md
  blob f6b119b7d891f19ca6f0e819c9615d74fc38c9ee
  commit 915a3f57e3e3e4aebe97a436b314e098683aa5dd.

That result PARKED legacy-484479fe4613 after its one bounded structural redesign failed at the second-Fe cubic coefficient-L1 gate. It explicitly instructed autonomous BOOT reprioritization rather than further local redesign.

For candidate prescout this turn also recovered:
- boot-post-B162-rmfe-direct-multkey-trace-recode-candidate-2026-10-28.md, blob abaceab3cc926a6a70b29c0aa695b477a93d171a;
- boot-post-B162-rmfe-subring-envelope-single-multkey-candidate-2026-10-28.md, blob 14613722b7708955a6aab1a93cc7619d8d180d3a;
- boot-post-B162-rmfe-subring-envelope-key-capacity-value-gate-2026-10-28.md, blob 10f21f5a32f9c9df3161bba528b17336074a5d8a;
- boot-RMFE-post-aung-2025-2026-followup-priorart-gate-2026-11-01.md, blob 90e3b9fa4300ac7eb8ce3f20b63bfb4aab56592f.

The target finding path was checked absent before write.

## One primary problem-selection hypothesis

H5:
Among currently durable BOOT opportunities, the best next ACTIVE paper candidate is the previously positive but unresolved RMFE subring-envelope single-MultKey construction, because it attacks the same important Aung repeated-MultKey bottleneck while avoiding the specific repeated-dirty-lift Algorithm4 proof architecture that just forced legacy-484479fe4613 to PARK.

Falsifier for selection:
do not activate it if durable evidence already kills its algebraic correctness, if a later direct prior-art collision exists in the recovered portfolio, or if its remaining uncertainty is merely implementation tuning rather than a paper-level correctness/value question.

## Important problem

Aung et al. ePrint 2025/350 / PKC 2025 explicitly leave open whether the MultKey portion can be performed directly on an RMFE-packed ciphertext instead of executing MultKey k times after splitting.

For the p=5,m=32768,w=512,k=5 correction/TnM benchmark, the durable source summary records:
  SlotsToCtxts ≈2.284 s,
  MultKey ≈4.732 s,
  CtxtsToSlots ≈0.078 s,
  DigitExtract ≈4.240 s,
  total ≈11.33 s.

Thus repeated MultKey remains an important, source-identified bottleneck.

## Closest prior art and exact delta

Closest prior:
1. Chen-Han slim/thin BGV bootstrap: rank-1 constant-slot case.
2. Geelen et al. 2024/153: sparse/subring Slot<->Coeff and coefficient-selection trace machinery.
3. Ma et al. 2024/164: Hom-NTT / RM_k coefficient clearing / small-subring optimizations inside ordinary BGV bootstrapping.
4. Aung et al. 2025/350: RMFE-packed bootstrapping, but still k split MultKey executions; high-level goal of direct RMFE MultKey is explicitly future work.

Therefore the high-level objective "do direct RMFE MultKey" is PRIOR-DISCLOSED and cannot be the novelty claim.

Mechanism-specific delta of the selected candidate:
  RMFE_5
  -> existing RMFE component projections
  -> embed the five components into the first five power-basis coordinates of a degree-8 power-of-two subring envelope E8
  -> ONE ModSwitch + ONE boot-key inner product
  -> RM_10 coefficient selection back to the embedded subring
  -> degree-8 inverse transform/unpack
  -> reassemble RMFE_5
  -> use the existing Aung correction DigitExtract once.

The purpose of the degree-8 envelope is structural: preserve coefficient-domain high p-adic digit semantics while avoiding the invalid carry-commuting shortcut that killed raw CRT recoding.

The prior 2025-2026 search did not establish publication-grade novelty for this exact subring-envelope construction; it only established no visible post-Aung collision for another narrow mechanism. Therefore:
  NOVELTY_STATUS = PREFLIGHT,
not CLEAR.

## Why this candidate survives current durable evidence

Durable positive evidence from 2026-10-28:
- exact p=5 algebraic layout exists with r=8,m_r=32,Y=X^1024;
- five RMFE scalar components fit distinct power-basis coordinates of E8;
- RM_10 is a strict subset of the ordinary RM_13 coefficient-selection chain;
- the candidate does not increase the number of critical-path linear plaintext-multiplication levels;
- input merge adds at most log2(5)=2.322 bits in the simple deterministic branch-sum envelope;
- the structural middle block replaces five ModSwitch/boot-key-inner-product executions by one;
- old status was KEEP_ACTIVE / CAPACITY decisive unresolved gate.

No later durable finding recovered this turn kills this exact E8-envelope mechanism.

Most importantly, the reason legacy-484479fe4613 was parked does not automatically transfer:
that candidate generated arbitrary residue-correct Z625 lifts and then needed repeated F_e propagation under a very conservative independent modulus-switch rounding certificate.
The E8 candidate instead seeks to preserve the standard coefficient-domain MultKey intermediate before reassembling RMFE coordinates and then invokes the existing Aung correction-map DigitExtract once. Whether that claim survives a full source-faithful noise/capacity audit is still unresolved, but the failed repeated-Fe route is not itself a falsifier.

## Paper-level uncertainty that makes this worth one next test

The decisive unresolved gate is not "can the algebra be written"—that already has positive static evidence.

The live uncertainty is:
  can the E8 envelope path preserve enough independent correctness/capacity after
    projection merge
    -> degree-8 SlotToCoeff
    -> one ModSwitch/boot-key reconstruction
    -> RM_10
    -> degree-8 CoeffToSlots/unpack
for the subsequent standard RMFE DigitExtract to remain correctness-safe and scientifically valuable?

This is paper-level because:
- FAIL would eliminate the candidate before native implementation;
- PASS would establish a constructive direct-MultKey mechanism specific enough to justify novelty preflight and later native work.

The recent BOOT work now provides stronger tools than when this candidate was last active:
absolute coefficient-L1 provenance, explicit BGV factor handling, fixed-prime-set source audits, and disciplined separation of certified envelopes from heuristic HElib noiseBound. That makes revisiting the old unresolved capacity gate materially different from repeating prior work.

## Selected candidate

CANDIDATE_ID:
  rmfe-subring-envelope-single-multkey-v1

STATUS:
  ACTIVE

PHASE:
  PROBLEM_SELECTION

Working thesis:
A power-of-two degree-8 subring envelope can carry the five RMFE components through one source-faithful BGV MultKey stage, then select/repack those coefficient-domain intermediates back into RMFE form for Aung's existing correction DigitExtract, reducing five MultKey executions to one without changing the cryptographic assumption.

This is a hypothesis, not a proven contribution.

## Constructive design spec at selection time

Fixed target point:
  p=5
  m=32768
  d=8192
  ell=2
  w=512
  k=5
  temporary RMFE envelope degree r=8
  m_r=32
  Y=X^1024.

Input transform:
  A(c)=sum_{i=0}^4 X^(1024 i) tau_i(c),
where tau_i are the existing RMFE component projections.

Middle:
  degree-8 SlotToCoeff on the E8 envelope
  -> ONE ModSwitch
  -> ONE ordinary boot-key inner product.

Recovery:
  RM_10 coefficient-selection trace
  -> degree-8 CoeffToSlots
  -> unpack 8 scalar coordinates
  -> keep first five
  -> multiply by RMFE basis phi(e_i) and sum
  -> existing Aung correction DigitExtract once.

Invariants to preserve:
- no raw high-digit extraction is moved across arbitrary CRT mixing;
- coefficient positions for the five components remain distinct;
- ptxtSpace/intFactor semantics must be source-faithful;
- no new secret or cryptographic assumption;
- any extra automorphism keys must be explicitly accounted;
- baseline/candidate comparison must eventually be matched.

## Cheapest decisive next test

NO Native.

Derive one source-faithful absolute coefficient-L1/capacity ledger for the whole E8 middle path:
  A(c)
  -> degree-8 SlotToCoeff
  -> one ModSwitch/boot-key inner product
  -> RM_10
  -> degree-8 CoeffToSlots/unpack.

The test should use exact/public linear-map coefficient norms where recoverable and the already-established independent modulus-switch/key-switch methodology, then compare:
1. correctness margin before the existing Aung DigitExtract; and
2. the resulting capacity loss against the baseline split-thin path.

Falsify early if the E8 transform/RM_10 envelope consumes enough margin that the standard downstream DigitExtract cannot be independently certified, or if the only rescue requires a new structural redesign.

Do not launch Native until this static gate passes.

## Verdict

PASS_PROBLEM_SELECTION.

The E8 subring-envelope single-MultKey route is the new ACTIVE PAPER_CANDIDATE.

This turn does NOT establish:
- complete correctness;
- novelty;
- security;
- value;
- baseline correctness;
- native feasibility;
- paper readiness.

Previous candidate legacy-484479fe4613 remains PARKED and is not reopened.

Research frontier remains nonempty.
