# BOOT / B158_OVERALL — Research Turn 17/25
## PROBLEM_SELECTION — leaf-ring clean-factor sidecar

Date: 2026-11-12 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_OVERALL
Candidate: boot-b158-leaf-ring-clean-factor-sidecar-v1
Phase: PROBLEM_SELECTION
Final status: PARKED
Evidence grade: STATIC / SOURCE / SECURITY-BOUND
Native: NOT RUN

## Why this is a distinct candidate

The durable state entering Turn 17 had ACTIVE=UNKNOWN and explicitly PARKED the prior q0 sparse-gateway candidate. This turn does not resume, rename, or locally patch that route.

The new candidate is also distinct from the earlier same-ring checkpoint-decoupled half-basis proposal:
- checkpoint-decoupling keeps the clean binary-power sidecar A_k in the original N=32768 ring;
- this candidate moves the late clean sidecar into a smaller ring (target n=N/2=16384), evolves it there, and merges only the needed late factor back into the parent ring.

The intended benefit is to change the late B158 noise/cost law by paying auxiliary squarings in a smaller ring, while preventing the large-norm selector M_k from acting on the dirty recurrent B158 state.

## Pre-registration

QUESTION:
Can a clean late-stage B158 binary-power auxiliary be ring-switched from N=32768 to n=16384, evolved securely in the smaller leaf ring, and merged back only when needed to supply late selector factors, while preserving the fixed source-point correctness budget and yielding a plausible whole-system advantage?

CURRENT_BELIEF:
The plaintext split/merge algebra should be type-correct using Liang-Ding/Lattigo RingPackingEvaluator. The likely blocker is that a same-Q leaf at n=16384 cannot safely carry the fixed B158 logQ≈649, while lowering the leaf modulus may make Merge return a parent ciphertext at too small a level to interact with the high-Q recurrent state.

CHEAPEST_DECISIVE_TEST:
Before any native implementation:
1. inspect the exact source semantics of SplitNew/MergeNew and the author experiment's top/leaf parameter relation;
2. compare the fixed B163/B158 working modulus to the 128-bit ternary-security modulus ceiling at n=16384;
3. if secure leaf operation requires a lower Q, determine whether Merge can restore the parent ciphertext to the original high-Q level without a new cryptographic primitive;
4. compare the resulting parent Q to the already-measured B163 required_logQ at the last correct stage.

IF_PASS:
If n=16384 can securely retain the needed working modulus, or source-backed Merge can lift a secure low-Q leaf result back to the high-Q parent modulus without a new trust/security assumption or material noise penalty, admit the candidate ACTIVE and next run a small Split -> one leaf square -> Merge correctness/noise canary.

IF_FAIL:
If same-Q leaf security fails and the source-compatible secure low-Q leaf can only merge back at that same low level, causing a known correctness-budget deficit for the main B158 state, PARK immediately. Do not rescue by increasing N, weakening security, or inventing a low-to-high modulus-raising key switch.

IF_UNCLEAR:
Do not admit the candidate ACTIVE. Recover the exact missing source/security fact first; no native job.

WHICH_PAPER_GATE_CHANGES:
Killer gate (2): stock/source feasibility including parameter/security feasibility. A failure here blocks correctness and value gates.

WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION:
This candidate only matters if the smaller ring can actually host the clean auxiliary at a modulus compatible with late B158. If security or Merge semantics force the sidecar back to a modulus already known to be insufficient, native implementation cannot rescue the mechanism and should not consume a turn.

## Closest prior art / exact delta

### Liang-Ding 2026/1779 author implementation

Primary source used here is the authors' public repository:
  Zhaoyang-Liang/bootstrapping-via-ring-switching-without-slot-recovery

Verified source file:
  code/table_3_ckks_bootstrapping_and_table_9_slot_recovery/code_ckks_shared/source/deps/subring_bts-main/core/rlwe/ring_packing.go
  blob 74b7c25eaf199a501251673c6badce9893d0f17e

Its exact Merge relation is:
  ct_N[X] = ct_even(Y) + X * ct_odd(Y),  Y=X^2.

MergeNew constructs the parent ciphertext at:
  level = ctEvenNHalf.Level()
and Merge applies the small-secret -> big-secret evaluation key at that same level. There is no low-Q -> high-Q modulus raise in Merge.

Verified author experiment source:
  code/table_3_ckks_bootstrapping_and_table_9_slot_recovery/table_9_ckks_slot_recovery_baseline/source/main.go
  blob 8806b327e824ea7703511fb2011a856b0b845e1c

Its exactLeafParameters(top) copies the parent's exact Q and P bases into the leaf parameter set, and sameBasis checks equality of every Q and P modulus.

Thus the stock/source ring-packing interface is a same-basis, same-level split/merge mechanism.

Full ePrint 2026/1779 PDF was not acquired in this turn (configured ePrint retrieval returned HTTP 403); no theorem/page claims from the unavailable PDF are used.

### Earlier internal B158 checkpoint sidecar

The durable same-ring checkpoint-decoupling candidate already retained a clean A_k and squared it independently in the original ring. The new candidate's only new mechanism is moving that auxiliary arithmetic to a lower-degree leaf ring and merging the result back late.

### LEAF / ring-switch background

General ring switching is prior art. The paper-level novelty question would therefore be whether the specific B158 late-factor sidecar use changes the noise/cost frontier, not ring switching itself.

## Fixed B158 source point

Authoritative B163 native audit:
  findings/boot-B163-native-artifact-audit-2026-10-28.md
  artifact SHA256 bb35766751a0439de8e92db3668082930afc84fa49b32ae44b8df093ce85bfad

Fixed parameters:
- N=32768;
- T=65537;
- LogQ=[36, 34x18, 30];
- total logQ=649;
- no-rescale B158 state stays at L18/logQ=649.

Measured native noise:
- exact through k=4096;
- state at k=4096: required_logQ=620, budget +29;
- target k=8192 selector factor: required_logQ=646, budget +3;
- fused output: required_logQ=665 > 649 and fails.

These numbers are direct native obstruction data, not an estimate.

## Security feasibility gate

The Homomorphic Encryption Security Guidelines parameter table for 128-bit classical security and ternary secrets gives a maximum coefficient-modulus size of:
- log q <= 438 bits for ring dimension n=16384;
- log q <= 881 bits for ring dimension N=32768.

The candidate wants the auxiliary in n=16384.

Therefore:
  649-bit same-Q leaf > 438-bit 128-bit security ceiling.

So the simplest desired construction,
  Split at logQ≈649 -> leaf arithmetic -> Merge,
is not security-feasible at n=16384.

This is already a killer-gate failure unless the leaf first reduces its modulus.

## Secure-low-Q repair test

Suppose the leaf is modulus-switched before or after Split to q_leaf satisfying
  log q_leaf <= 438.

Could it then Merge back to the 649-bit parent state?

No, not with the verified RingPackingEvaluator interface.

Source behavior:
- MergeNew allocates the parent at the child level;
- Merge evaluates the ring-switching key at that level;
- no operation in this interface modulus-raises the output to a larger parent Q.

Thus a secure leaf result at <=438 bits returns a parent-ring ciphertext at <=438 bits.

To multiply it with the main B158 recurrent state, the main state must be aligned to that same/lower modulus level, or an entirely new low-to-high refresh/modulus-raise construction must be supplied.

## Exact correctness-budget contradiction

The native B163 recurrent state already needs:
  required_logQ = 620
at k=4096.

If the main state is aligned down to a leaf-compatible 438-bit modulus before the late sidecar factor is injected, the deficit is at least:

  620 - 438 = 182 bits.

This is before the next late selector and fused multiplication.

At the target k=8192 selector factor:
  required_logQ = 646,
so the analogous deficit is:
  646 - 438 = 208 bits.

These deficits are far larger than any ordinary rescale-placement or rounding slack and arise from already-measured native noise.

Therefore the secure-low-Q leaf cannot feed the late B158 recurrence using the stock/source Merge interface.

## Why this is not eligible for the one-bounded-redesign exception

A hypothetical operation

  low-Q n=16384 leaf ciphertext
    -> secure key/ring switch
    -> N=32768 parent ciphertext at ~649-bit working modulus

would not be a local dispatch or layout repair.

It would need a new cryptographic refresh/modulus-raising mechanism, with:
- a defined ciphertext relation;
- new key material or bootstrapping/refresh semantics;
- security proof;
- noise/DFR analysis;
- cost sufficient to beat the same-ring checkpoint sidecar.

That is a different research mechanism. It cannot be silently added to this candidate after its killer-gate failure.

Increasing the leaf ring back to N=32768 would satisfy the modulus-security range but removes the intended smaller-ring mechanism and collapses to the prior same-ring sidecar family.

## Optimistic value consequence

No value benchmark is warranted.

The smaller-ring arithmetic could only matter if the source/security gate passed. Since it does not, any optimistic NTT-cost saving is irrelevant to the current candidate.

No performance claim is made.

## Decision

FAIL_SOURCE_SECURITY_GATE -> PARKED.

Candidate:
  boot-b158-leaf-ring-clean-factor-sidecar-v1

The Split/Merge plaintext algebra and ciphertext typing are real and source-backed, but the candidate cannot simultaneously satisfy:
1. smaller leaf ring n=16384;
2. 128-bit ternary security;
3. B158's fixed late-stage working-modulus requirement;
4. source-compatible Merge back into the recurrent parent state.

No native experiment is justified.

## Reopen condition

Reopen this candidate family only if there is concrete source-backed evidence for at least one of:

A. a secure low-to-high leaf-to-parent refresh/merge primitive that:
- accepts an n=16384 leaf at logQ<=438;
- outputs an N=32768 parent ciphertext at a working modulus sufficient for the measured late B158 requirement (at least about 620 bits at k=4096);
- preserves exact BGV/BFV semantics;
- has complete security/noise/key analysis;
- is materially cheaper than the prior same-ring checkpoint sidecar / full refresh;

OR

B. a genuinely smaller leaf dimension/parameter regime whose 128-bit security ceiling itself supports the measured late working modulus while retaining a real ring-size cost advantage.

Merely adding Q, increasing N to the parent dimension, weakening security, or renaming the same-ring checkpoint construction does not satisfy this condition.

## Eliminated uncertainty

Eliminated:
"Can a standard Liang-Ding/Lattigo same-basis N/2 leaf ring directly host the clean late B158 sidecar at the fixed source-point modulus, or safely lower Q and then merge it back for late multiplication?"

Answer:
No. Same-Q violates the leaf security ceiling; secure low-Q Merge returns a low-Q parent, which has at least a 182-bit measured correctness-budget deficit at the last correct B158 stage.

## Evidence references

- findings/boot-B163-native-artifact-audit-2026-10-28.md; B163 artifact SHA256 bb35766751a0439de8e92db3668082930afc84fa49b32ae44b8df093ce85bfad.
- findings/boot-B158-checkpoint-decoupled-halfbasis-gate-2026-10-28.md.
- findings/boot-B158-selector-norm-lift-layout-gate-2026-10-28.md.
- Liang-Ding author repo ring_packing.go blob 74b7c25eaf199a501251673c6badce9893d0f17e, Merge/MergeNew.
- Liang-Ding author Table-9 source main.go blob 8806b327e824ea7703511fb2011a856b0b845e1c, exactLeafParameters/sameBasis.
- Homomorphic Encryption Security Guidelines, 128-bit classical ternary table: N=16384 -> max logq 438; N=32768 -> max logq 881.
