# BOOT RMFE Revised Static Capacity-Ceiling Gate

Date: 2026-10-31
Session: 密码学 16.0
Logical Research Turn: 15/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

The authorized native task
\`BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01\`
remains pending and untouched.

This turn asks one static question:

> After the current 19-call delayed-fusion redesign, can capacity alone already make it impossible to cross the published thin-bootstrap throughput frontier?

No native execution, source mutation, Codex resubmission, or second heavy local task occurred.

## Published p=5 capacity anchors

Aung et al. ePrint 2025/350, Table 2, \(m=32768,p=5,w=512\):

Correction / trace-and-merge:

- Initial: 391.1
- after SlotsToCtxts: 369.2
- after MultKey: 346.5
- after CtxtsToSlots: 333.8
- after DigitExtract / final: 101.0

Correction / BSGS:

- Initial: 391.1
- after SlotsToCtxts: 340.4
- after MultKey: 346.6
- after CtxtsToSlots: 333.7
- after DigitExtract / final: 115.2

The BSGS row is decisive for methodology:

\[
340.4 \to 346.6
\]

across MultKey is a **capacity increase** of 6.2 bits.

Therefore published stage capacities are not an additive "bit-loss ledger". MultKey includes modulus changes, and HElib capacity is a ratio involving both ciphertext modulus and noise.

It is invalid to infer the revised final capacity by subtracting local multiplier taxes directly from 101.

## Revised throughput-capacity frontier

Turn 14 removed the separate 0.078 s CtxtsToSlots stage from the candidate.

The unchanged external latency anchor is therefore

\[
T_{\rm fixed}
=
2.284+4.240
=
6.524\ {\rm s}.
\]

Let \(T_M\) denote the revised middle-block latency and \(C\) the final capacity.

To beat the published thin throughput 107.06:

\[
\frac{10C}{6.524+T_M}>107.06.
\]

Equivalently,

\[
\boxed{
C >
10.706(6.524+T_M)
}
\]

or

\[
\boxed{
T_M <
\frac{10C}{107.06}-6.524.
}
\]

Every one-bit drop in final capacity tightens the allowed middle latency by

\[
\boxed{
\frac{10}{107.06}
=
0.0934056\ {\rm s/bit}.
}
\]

Useful frontier points:

| Final capacity C | Maximum middle latency |
|---:|---:|
| 101 | 2.909962 s |
| 100 | 2.816557 s |
| 98 | 2.629746 s |
| 95 | 2.349529 s |
| 90 | 1.882501 s |
| 85 | 1.415473 s |
| 80 | 0.948445 s |
| 75 | 0.481418 s |
| 70 | 0.014390 s |

## Capacity-only hard-kill floor

Even under the impossible optimistic assumption

\[
T_M=0,
\]

the candidate must have

\[
C>
107.06\cdot6.524/10.
\]

Hence

\[
\boxed{
C>69.845944
}
\]

is necessary for any throughput win.

Therefore a **capacity-only static hard kill** requires proving

\[
\boxed{
C_{\rm final}^{\max}\le69.845944.
}
\]

No current static result comes close to establishing such an upper bound.

## Known revised recovery multiplier tax

Turn 7/8 exact Moore recovery gives four correction outputs with public-multiplier triangle-bound taxes:

- \(L_0\): 13.265459 bits
- \(L_1\): 14.582190 bits
- \(L_2\): 15.740880 bits
- \(L_3\): 15.718298 bits

Worst:

\[
\boxed{
15.740880\ {\rm bits}
}
\]

before automorphism/key-switch noise.

Turn 8 proved that this same map jointly subsumes the old R8 C2S and correction recombination on the restricted state, so the old 14.150203-bit R8 C2S tax is **not** sequentially added anymore.

This 15.740880-bit quantity is a local fixed-Q HElib public-multiplier noise factor, not a measured final-capacity loss.

## RM10 normalization is capacity-free in HElib's scalar ledger

The fixed-Q RM10 path uses normalization by the scalar

\[
224\pmod{625}.
\]

Pinned HElib BGV source:

\`Ctxt::multByConstant(const NTL::ZZ& c)\`

computes

\[
d=\gcd(c\bmod ptxtSpace,ptxtSpace).
\]

If \(d=1\), it updates \`intFactor\` and returns without multiplying \`noiseBound\`.

Since

\[
\gcd(224,625)=1,
\]

the normalization

\[
\boxed{
\times224
}
\]

adds **zero noiseBound tax** under this scalar overload.

This removes one possible hidden fixed-Q penalty.

## Carry correction also adds no encrypted-operation tax

Turns 11–12 move fusion to after branchwise rawModSwitch and represent the divisibility-lift / raw aggregation defect using public integer carry polynomials.

These corrections are applied to public integer coefficient data before the single common boot-key reconstruction.

Thus they do not introduce:

- ciphertext-ciphertext multiplication;
- automorphism/key-switch noise;
- a new encrypted secret term.

They may change the public reconstruction polynomial sizes, but the exact aggregate reconstruction remains algebraically equal to the shifted sum of the five branch reconstructions.

## What remains unresolved

The decisive capacity terms are still not statically closed:

1. five retained thin S2C transforms;
2. five reLinearize/key-switch-to-recrypt-key paths;
3. branchwise rawModSwitch noise behavior;
4. RM10's ten automorphism/key-switch operations;
5. four joint-recovery Frobenius/key-switch operations;
6. the way the revised input noise propagates through correction DigitExtract.

The fixed-Q R8 ledger explicitly left RM10/key-switch/mod-switch noise unresolved.

No durable native result closes those terms for the current revised pipeline.

## Why subtracting 15.740880 from final 101 is invalid

A tempting stress calculation is

\[
101-15.740880=85.259120.
\]

If this were a genuine *net extra final loss*, the corresponding middle-latency budget would be

\[
\frac{10\cdot85.259120}{107.06}-6.524
=
1.439676\ {\rm s}.
\]

Even this artificial pessimistic subtraction would **not** capacity-kill the candidate unconditionally, since 85.26 remains above the 69.85 capacity-only floor.

More importantly, the subtraction is not scientifically valid:

- the 15.740880-bit joint map replaces five branch C2S transforms plus the published CtxtsToSlots recombination;
- stage capacities are not additive across MultKey / ModSwitch;
- the baseline itself demonstrates nonmonotonic stage capacity.

Therefore 85.259 is a stress scenario only, not a capacity prediction.

## Current best capacity statement

The strongest justified static statement is:

\[
\boxed{
\text{known fixed-Q multiplier costs do not statically kill capacity}
}
\]

but:

\[
\boxed{
\text{whole-pipeline final capacity remains unresolved}
}
\]

because the automorphism/key-switch and DigitExtract propagation terms are native/source-state dependent.

Capacity and latency must now be judged jointly on the frontier

\[
C>10.706(6.524+T_M).
\]

## Interaction with the pending timer

The pending baseline timer remains untouched and is still decisive.

Its latency result will determine how much capacity loss can be tolerated:

- if revised \(T_M\approx2.5\) s, final capacity must exceed about 96.61;
- if \(T_M\approx2.0\) s, final capacity must exceed about 91.26;
- if \(T_M\approx1.5\) s, final capacity must exceed about 85.90;
- if \(T_M\approx1.0\) s, final capacity must exceed about 80.55.

Therefore there is no scientifically useful capacity target independent of the pending latency evidence, except the unconditional floor \(C>69.845944\).

## Verdict

\`\`\`text
RESULT:
  PASS_NO_STATIC_CAPACITY_KILL

CAPACITY_ONLY_HARD_KILL_FLOOR:
  C_final <= 69.845944

KNOWN_JOINT_RECOVERY_PUBLIC_MULTIPLIER_TAX:
  15.740880 bits worst output

RM10_NORMALIZATION_224:
  ZERO HElib noiseBound tax via scalar-unit path

PUBLIC_CARRY_CORRECTION:
  NO encrypted-operation tax

PUBLISHED_STAGE_CAPACITY_ADDITIVITY:
  FALSE / demonstrated by 340.4 -> 346.6 across MultKey

WHOLE_PIPELINE_CAPACITY:
  UNRESOLVED

STATIC_FINAL_CAPACITY_PREDICTION:
  NOT JUSTIFIED

STATIC_HARD_KILL:
  NO

PENDING_NATIVE_TIMER:
  GENUINELY DECISIVE / DO NOT RERUN

NATIVE_LATENCY:
  NOT ESTABLISHED

PUBLISHABLE_NOVELTY:
  NOT ESTABLISHED

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

Do not spend another turn trying to turn stage-capacity numbers into an additive static ledger.

The current capacity and latency uncertainties are coupled, and the pending source-faithful timing result is needed before a meaningful final-capacity threshold can be assigned.

If the timer remains pending, the next independent turn should target a **different falsifier**, not another local capacity arithmetic refinement.

A high-value option is to audit whether the revised carry-compensated single reconstruction preserves the exact HElib \`intFactor\` / plaintext-space semantics required by downstream correction DigitExtract. A failure there would kill correctness independently of latency/capacity.

AI_PROVISIONAL_CHOICE:
  RETAIN_REVISED_POSTRAW_FUSION
  STOP_STATIC_CAPACITY_LEDGER_REFINEMENT
  NEXT_STATIC_PRIORITY = INTFACTOR_AND_DOWNSTREAM_SEMANTICS_GATE

INDEPENDENT_RESEARCH_AVAILABLE: true
RESEARCH_FRONTIER_EXHAUSTED: false
