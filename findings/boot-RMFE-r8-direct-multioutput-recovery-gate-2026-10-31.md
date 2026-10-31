# BOOT RMFE R8 Direct Multi-Output Recovery Gate

Date: 2026-10-31
Session: 密码学 16.0
Logical Research Turn: 5/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

This turn does not rerun the pending baseline timing task
`BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01`.
No scientifically auditable native result for that task was present in the supplied authority context.

The single question tested here is whether the current post-raw recovery

[
	ext{RM10} 	o 	ext{R8 C2S} 	o 	ext{E8 unpack} 	o 	ext{CtxtsToSlots/correction outputs}
]

can be structurally improved by replacing

[
	ext{R8 C2S}+	ext{unpack}+	ext{CtxtsToSlots}
]

with one direct R8-to-RMFE linear transform.

No Codex/native execution, parameter change, or new correctness assumption occurred.

## Source boundary from Aung et al. 2025/350

For p=5 and plaintext modulus 625=5^4, correction-map digit extraction uses
`e=4` and therefore requires the main RMFE ciphertext

[
L_0(z)=z
]

plus

[
L_1(z),L_2(z),L_3(z).
]

Thus the recovery interface is a **four-output** linear-map problem, not a one-output problem.

Aung et al. §5.1 explicitly states that `CtxtsToSlots` combines the k thin ciphertexts by constant multiplying each branch with the appropriate RMFE basis image and summing. It can likewise compute other linear maps by using the corresponding precomputed basis images.

Aung et al. §5.2/Algorithm 4 uses those correction-map images during digit extraction. Therefore removing `CtxtsToSlots` requires reproducing all four outputs, not only reconstructing z.

## Existence of direct maps

Let

[
S=mathbb Z/625mathbb Z,
qquad
A=S[Y]/(Y^{16}+1)
]

be the established embedded R8 Galois algebra, with automorphism group

[
H=(mathbb Z/32mathbb Z)^*.
]

For each t in {0,1,2,3}, define the desired composite

[
D_t:
A
	o
R
]

as

[
	ext{R8 coefficient state}
	o
	ext{E8 slot coordinates}
	o
	ext{retain first five coordinates}
	o
L_t	ext{-weighted RMFE recombination}
	o
	ext{outer plaintext ring }R.
]

Each D_t is S-linear.

For a finite ring-Galois extension, the skew group algebra realizes all S-linear endomorphisms as automorphism-multiplier sums. After scalar extension from A to the outer A-algebra R, each D_t therefore has an exact representation

[
D_t(x)=
sum_{hin H} a_{t,h},h(x),
qquad
a_{t,h}in R.
]

So a direct R8-to-RMFE recovery exists algebraically. This is an existence result only; multiplier norms/capacity are not bounded here.

## Four-output automorphism schedule

Write

[
H=langle a=5angle	imeslangle b=31angle,
]

with ord(a)=8 and ord(b)=2.

For one arbitrary full-support automorphism-multiplier map, use the decomposition

[
j=r+4s,
qquad
rin{0,1,2,3},
quad
sin{0,1}.
]

For the common input x:

1. Precompute baby steps
   [
   x,a(x),a^2(x),a^3(x),
   ]
   requiring 3 automorphisms.

2. For each output t and each b-coset epsilon in {0,1}, combine the four baby steps with public multipliers for the two giant groups s=0,1, then apply a^4 to the s=1 accumulator.
   This costs 2 giant-step automorphisms per output.

3. Apply b once to the epsilon=1 accumulator for each output.
   This costs 1 additional automorphism per output.

Thus four outputs require

[
3+4(2+1)=15
]

automorphism/key-switch calls.

Equivalently, materializing the complete 16-element H-orbit once also costs 15 nonidentity automorphisms and can feed all four public linear combinations.

The important distinction from the prior cross-branch-hoisting failure is that all four outputs here come from the **same ciphertext**, so the baby/source orbit is genuinely shareable. The 15-call figure is therefore a valid generic upper-bound construction.

## Comparison with current recovery

Current conservative recovery after RM10:

- exact R8 C2S: 6 automorphism/key-switch calls;
- E8 unpack: 7 automorphisms;
- then CtxtsToSlots produces z,L1,L2,L3 using only constant multiplications and additions.

Total after RM10:

[
6+7=13
]

automorphism-scale calls.

Generic direct four-output recovery:

[
15.
]

Therefore

[
oxed{15>13}.
]

The direct multi-output map is **not** a structural automorphism-count improvement.

Including RM10:

Current:
[
10+13=23.
]

Generic direct:
[
10+15=25.
]

The direct route removes the published ~0.078 s CtxtsToSlots stage and avoids explicit scalar-ciphertext materialization, but it introduces two extra automorphism/key-switch calls. Without a native cost measurement, neither latency dominance nor a capacity advantage follows.

## Impact on the Turn-4 timing threshold

The Turn-4 hard-kill ratio

[
ho_{max}=0.5984704142
]

was derived for the current recovery path while conservatively leaving CtxtsToSlots outside the candidate middle.

This turn does **not** justify relaxing that threshold.

A single-output fused-map calculation would have incorrectly removed the 0.078 s CtxtsToSlots cost while ignoring that correction-style digit extraction needs four outputs.

The actual generic four-output direct transform does not dominate the existing 6+7 recovery in automorphism count.

Therefore the pending baseline timing task remains scientifically valid as written. Its measured data, if/when returned, should still first be judged against the original Turn-4 hard-kill threshold; no rerun is required merely because of this turn.

## Verdict

```text
RESULT:
  FAIL_GENERIC_DIRECT_MULTIOUTPUT_RECOVERY_AS_COST_IMPROVEMENT

DIRECT_R8_TO_RMFE_LINEAR_MAP_EXISTENCE:
  PASS_STATIC

CORRECTION_OUTPUT_COUNT_AT_P5_PLAINTEXT625:
  4  (L0,L1,L2,L3)

CURRENT_POST_RM10_RECOVERY_AUTOMORPHISMS:
  13

GENERIC_DIRECT_FOUR_OUTPUT_AUTOMORPHISMS:
  15

STRUCTURAL_DOMINANCE:
  FAIL

TURN4_TIMING_THRESHOLD:
  PRESERVED

PENDING_BASELINE_TIMER_TASK:
  DO_NOT_RERUN / RESULT_NOT_PRESENT_IN_CURRENT_AUTHORITY_CONTEXT

CANDIDATE_STATUS:
  RETAIN_ORIGINAL_POST_RAW_FUSION_PENDING_BASELINE_TIMING_GATE

GENERIC_DIRECT_MULTI_OUTPUT_FUSION:
  PARK / KILL_AS_DEFAULT_OPTIMIZATION

SPECIAL_CORRECTION_MAP_STRUCTURE:
  NOT_TESTED / UNCLEAR

RESEARCH_FRONTIER_EXHAUSTED:
  false
```

## Next information boundary

The highest-value next action remains the existing baseline timing decomposition result.

If that result is unavailable, a future static branch may test whether the specific correction maps L1,L2,L3 possess special algebraic structure that beats the generic 15-call four-output construction. Do not assume such structure from the generic Galois-map existence theorem.
