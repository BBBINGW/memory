# BOOT RMFE Post-Raw Fusion Static Cost-Ceiling Gate

Date: 2026-10-31
Session: 密码学 16.0
Logical Research Turn: 3/25 (same-turn infrastructure retry does not increment)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Primary hypothesis

The exact post-raw fusion established in Turn 2 may still have enough structural cost margin to justify one minimal native timing gate, even though it leaves five branch-local nonlinear preprocessing paths intact.

The question is deliberately weaker than claiming speedup:

> Is the candidate already ruled out by source-faithful operation counts and the published p=5 correction/TnM throughput threshold?

Falsifier: if the unavoidable candidate middle work is already at or above the published break-even middle-block budget, or if the operation reduction is too small to plausibly clear the required latency reduction even under optimistic accounting, kill the partial-fusion family before native work.

No Codex/native execution, key generation, parameter sweep, or new correctness claim occurred.

## Durable inputs

### Published p=5 correction/TnM baseline

Aung et al., ePrint 2025/350, Table 2, m=32768, p=5, w=512, k=5:

- SlotsToCtxts: 2.284 s
- MultKey: 4.732 s
- CtxtsToSlots: 0.078 s
- DigitExtract: 4.240 s
- total: 11.33 s
- final capacity: 101
- thin throughput benchmark: about 107.06 capacity-slots/s

The prior value gate therefore uses the thin-throughput break-even condition

[
T_{m total} < rac{10C}{107.06}.
]

At (C=101),

[
T_{m total}<9.433962 {m s}.
]

Keeping the unchanged external stages

[
T_{m outside}=2.284+0.078+4.240=6.602 {m s},
]

the candidate middle must satisfy

[
T_{m middle}<2.831962 {m s}.
]

Relative to the 4.732 s baseline MultKey block, this requires at least

[
1-rac{2.831962}{4.732}
=0.40153
]

or **40.15% block-latency reduction** if final capacity remains 101.

Equivalently, all retained work plus candidate overhead may consume at most **59.85%** of the old MultKey latency.

## Source-faithful transform counts

Durable HElib source audit for m=32768,p=5 gives:

- each thin SlotsToCoeff: D=2 transform, at most 1 nontrivial automorphism;
- each thin CoeffToSlots: D=2 transform plus traceMap;
- traceMap with d=8192=2^13: exactly 13 Frobenius automorphisms.

Thus the five-branch baseline MultKey transform side is

[
5	imes(1+1+13)=75
]

automorphism/key-switch-scale calls:

- thin S2C: 5
- thin C2S D=2 part: 5
- thin C2S trace: 65.

This count excludes reLinearize-to-recrypt-key, rawModSwitch/newMakeDivisible, public multiplications/additions, and ordinary integer work.

## Candidate unavoidable transform work

Turn 2 keeps all five branches separate through nonlinear preprocessing, so the five thin S2C calls remain:

[
5.
]

After post-raw fusion:

1. RM10 coefficient selection: **10 automorphisms**;
2. exact R8 C2S BSGS map: **6 automorphism/key-switch calls**, 16 ct-pt multiplications, 15 additions;
3. conservative E8 unpack/recovery: **7 automorphisms** before retaining five coordinates and returning to the existing RMFE recombination interface.

Therefore conservative transform-side automorphism count is

[
5+10+6+7=28.
]

Compared with baseline:

[
75	o28,
]

a structural reduction of

[
1-rac{28}{75}=62.67%.
]

Looking only at the post-raw inverse/recovery side:

[
70	o23,
]

a reduction of

[
1-rac{23}{70}=67.14%.
]

In addition, the exact Turn-2 identity reduces the common boot-key reconstruction

[
a_i+b_iK
]

from 5 ciphertext reconstructions to 1.

## What remains fully five-way

The candidate does **not** reduce:

- RMFE component projections / SlotsToCtxts;
- five thin SlotsToCoeff transforms;
- five canonicalization / reLinearize-to-recrypt-key paths;
- five rawModSwitch calls;
- five newMakeDivisible balanced-carry computations;
- five divisions by p^{e'}.

These retained costs are precisely why automorphism-count reduction cannot be converted into a latency claim.

## Static cost-ceiling verdict

The candidate is **not statically cost-killed**.

The required latency reduction at C=101 is 40.15%, while the source-faithful transform-side reduction is 62.67% and the post-raw transform reduction is 67.14%, with an additional 5->1 boot-key reconstruction collapse.

This gives a meaningful structural margin over the required threshold.

However, the result is only a **feasibility margin**, not a latency estimate. The unknown decisive quantity is the share of the 4.732 s baseline MultKey block consumed by retained branch-local:

[
	ext{S2C + reLinearize + rawModSwitch + newMakeDivisible}.
]

If those retained operations plus the new RM10/R8/unpack overhead exceed 2.831962 s, the candidate still loses.

Therefore:

```text
RESULT:
  PASS_CONDITIONAL_STATIC_COST_MARGIN

STATIC_COST_KILL:
  NO

TRANSFORM_AUTOMORPHISMS:
  75 -> 28  (-62.67%)

POST_RAW_TRANSFORM_AUTOMORPHISMS:
  70 -> 23  (-67.14%)

BOOTKEY_RECONSTRUCTION:
  5 -> 1

REQUIRED_MIDDLE_BLOCK_REDUCTION_AT_C101:
  >= 40.15%

LATENCY_SPEEDUP:
  NOT_ESTABLISHED

FINAL_CAPACITY:
  NOT_ESTABLISHED

NATIVE_GATE_JUSTIFIED:
  YES, BUT BASELINE-TIMING-DECOMPOSITION FIRST
```

## Capacity sensitivity

The 2.831962 s middle budget assumes final capacity remains 101.

More generally:

[
T_{m middle}^{max}(C)
=rac{10C}{107.06}-6.602.
]

Thus any capacity loss tightens the timing requirement. In particular, the candidate should not be promoted from a timing-only PASS unless measured capacity remains close enough to the baseline that the latency gain survives the same throughput comparison.

The existing optimistic R8 C2S public-multiplier tax is 14.1502 bits, but whole-pipeline capacity, RM10 noise, unpack cost, and interaction with DigitExtract remain unresolved. No capacity transfer from the old pipeline is claimed.

## Cheapest next decisive test

Do **not** implement the new candidate yet.

The next highest-information native gate should instrument the existing faithful k=5 correction/TnM baseline only and report the timer decomposition of the 4.732 s MultKey block, at minimum:

- five thin SlotsToCoeff total;
- five reLinearize-to-recrypt-key total;
- five rawModSwitch + newMakeDivisible/division total;
- five recryptEkey multiply/add reconstructions total;
- five thin CoeffToSlots total.

Decision rule:

- if the retained pre-raw share alone is already near or above 2.83 s, kill post-raw fusion before implementation;
- if enough budget remains for RM10 + R8 C2S + unpack, then a bounded candidate implementation becomes justified.

This baseline-only timing decomposition has higher value of information than immediately implementing the candidate because it can kill the family without changing cryptographic code.

AI_PROVISIONAL_CHOICE:
  RETAIN_POST_RAW_FUSION_FOR_ONE_BASELINE_TIMING_DECOMPOSITION_GATE

INDEPENDENT_RESEARCH_AVAILABLE: true
RESEARCH_FRONTIER_EXHAUSTED: false
