# BOOT RMFE BSGS+10 Comparator Global-Route Strengthening Bound

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 20/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Pending native task boundary

Authorized native task:

\`BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01\`

remains UNKNOWN / BACKGROUND.

This turn does not:
- inspect or assume its result;
- modify its source/workdir/binary;
- resubmit it;
- start another heavy native task.

## Read-before-write authority

Current durable authority at turn start:

\`BBBINGW/memory main@3eec4741fff58028399fd7c608bd5926c3d22962\`.

Relevant durable prerequisites:
- Turn 19 equal-resource augmented-comparator classification;
- Turn 7 exact Corr./TnM recovery BFS paths;
- Turn 3 BSGS+10 direct-key strategy gate.

## Primary hypothesis

The ten added RM10 direct matrices may materially strengthen thin or Corr./TnM in many outer stages, making the equal-resource comparator much stronger than the already-known Corr./TnM recovery change \(100\to95\).

Falsifier:
enumerate the source-level automorphism families used by the p=5,w=512 workflows and show that the ten new BFS edges create only a bounded small reduction in physical KS count.

## Source provenance

Pinned HElib:

\`homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1\`.

Relevant source:
- \`src/EvalMap.cpp:509-660\`: ThinEvalMap construction/application;
- \`src/matmul.cpp:2865-2960\`: \`traceMap\`;
- \`src/recryption.cpp:773-787\`: thin coeffToSlot/slotToCoeff construction;
- \`src/recryption.cpp:1003-1119\`: thinReCrypt transforms and DigitExtract;
- \`src/keys.cpp:115-165\`: BFS \`setKeySwitchMap\`;
- \`src/Ctxt.cpp:2462-2514\`: \`smartAutomorph\`.

Aung et al. ePrint 2025/350:
- physical p16: Method 1 projection/recode uses
  \[
  (id+\sigma^s)\circ(id+\sigma^{2s})\circ\cdots\circ(id+\sigma^{(w/2)s});
  \]
- physical p17: SlotsToCtxts Method 1 applies \(k\) projection maps; CtxtsToSlots is constant-multiply-and-sum;
- physical p23: Corr./TnM uses Method 1 both for SlotsToCtxts and for the one correction-style recode;
- p5,w512 correction row has \(e=4,k=5\).

## 1. Standard and augmented Frobenius edge sets

For:

\[
m=32768,\qquad p=5,\qquad d=\operatorname{ord}_m(5)=8192,
\]

standard HElib BSGS Frobenius direct exponent edges are:

\[
E_{\rm BSGS}
=
\{1,\ldots,90\}
\cup
\{91,182,\ldots,8190\}.
\]

The candidate appends:

\[
E_{\rm RM10}
=
\{888,2032,3968,4096,5088,6080,6144,7168,7680,7936\}.
\]

The augmented graph is:

\[
E_+=E_{\rm BSGS}\cup E_{\rm RM10}.
\]

Exact BFS distances below are in the additive Frobenius-exponent group \(\mathbb Z/8192\mathbb Z\).

## 2. ThinEvalMap has only one ordinary D=2 matrix plus trace

Current bootstrapping geometry has:
- one mvec factor, \(mvec=[32768]\);
- \(\phi(m)=16384\);
- \(d=8192\);
- two thin SIMD slots.

Thus the sole ordinary dimension has order:

\[
D=2.
\]

The ThinEvalMap:
- slotToCoeff (\`invert=false\`) applies one D=2 matrix transform;
- coeffToSlot (\`invert=true\`) applies one D=2 matrix transform and then \`traceMap\`.

The nonidentity D=2 ordinary automorphism is outside the Frobenius subgroup and already has a direct one-hop matrix under BSGS 1D keys.

The ten added RM10 matrices lie in the Frobenius subgroup.

Therefore neither D=2 transform can improve below one physical KS:

\[
\boxed{
D=2:\ 1\to1.
}
\]

## 3. Exact thin trace strengthening: one physical KS

For \(d=8192\), the non-MIN \`traceMap\` requests the binary Frobenius indices:

\[
\{1,2,4,8,16,32,64,128,256,512,1024,2048,4096\}.
\]

Under standard BSGS:
- \(1,\ldots,64\): seven direct one-hop calls;
- \(128,256,512,1024,2048,4096\): six two-hop calls.

Hence:

\[
7+6\cdot2=19
\]

physical trace KS.

Under BSGS+10:
- 4096 becomes direct;
- 2048 still follows \([16,2032]\), hence remains two hops;
- the other paths are unchanged.

Thus:

\[
\boxed{
\text{traceMap}:19\to18.
}
\]

A complete thin bootstrap therefore changes its linear-transform physical count from:

\[
1_{\rm S2C}
+
19_{\rm trace}
+
1_{\rm C2S-D2}
=
21
\]

to:

\[
1+18+1=20.
\]

Hence:

\[
\boxed{
\text{thin transform KS}:21\to20.
}
\]

DigitExtract itself is polynomial arithmetic and does not introduce a hidden RM10-key routing benefit.

## 4. Corr./TnM branch MultKey strengthening: exactly five KS

Algorithm 2 applies, for each of \(k=5\) thin branches:
- SlotsToCoeff: one D=2 transform;
- CoeffToSlots: one D=2 transform plus one traceMap.

Therefore per branch:

standard BSGS:
\[
1+(1+19)=21;
\]

BSGS+10:
\[
1+(1+18)=20.
\]

Across five branches:

\[
\boxed{
105\to100
}
\]

for the combined branch SlotsToCoeff + CoeffToSlots transform work.

Equivalently, the CoeffToSlots/recovery portion alone is the already-established:

\[
\boxed{
100\to95.
}
\]

Thus the direct 4096 edge gives the Corr./TnM branch loop exactly five fewer physical KS.

## 5. Method-1 RMFE projection/recode automorphisms

Aung Method 1 for one projection map is:

\[
(id+\sigma^s)
\circ
(id+\sigma^{2s})
\circ\cdots\circ
(id+\sigma^{(w/2)s}).
\]

For \(w=512\), there are nine requested Frobenius exponent indices:

\[
s\{1,2,4,8,16,32,64,128,256\}.
\]

Since \(sw\mid d=8192\), the possible positive \(s\) values are divisors of 16:

\[
s\in\{1,2,4,8,16\}.
\]

Exact shortest-hop sums for one projection are:

| \(s\) | standard BSGS | BSGS+10 | saving |
|---:|---:|---:|---:|
| 1 | 11 | 11 | 0 |
| 2 | 12 | 12 | 0 |
| 4 | 13 | 13 | 0 |
| 8 | 14 | 14 | 0 |
| 16 | 15 | 14 | 1 |

The only improvement occurs at \(s=16\), because the final requested index is 4096, which becomes direct.

No other added RM10 edge shortens the nine-request projection schedule for these allowed s values.

## 6. SlotsToCtxts strengthening is bounded by five KS

Corr./TnM SlotsToCtxts Method 1 computes \(k=5\) projection maps.

Therefore the extra ten keys change its physical KS count by:

\[
\boxed{
0
}
\]

for \(s\in\{1,2,4,8\}\),

or at most:

\[
\boxed{
5
}
\]

for \(s=16\).

Thus the outer split stage cannot receive a larger hidden routing advantage.

## 7. Final correction-style recode has the same bound

Aung p23 states Corr./TnM also uses Method 1 for evaluating the correction-style recode.

There is exactly one recode for the p=5 correction row.

That recode uses the same \(k=5\) projection structure followed by CtxtsToSlots constant multiplication/addition.

Therefore its augmentation benefit is also:

\[
\boxed{
0\text{ or }5\text{ physical KS}
}
\]

depending on \(s\), with five possible only at \(s=16\).

CtxtsToSlots itself introduces no automorphism: Aung explicitly reconstructs by constant-multiplying each split ciphertext by a basis image and summing.

## 8. Total Corr./TnM augmentation bound

Combine:
- branch MultKey transform saving: exactly 5;
- outer SlotsToCtxts Method-1 saving: 0 or 5;
- one final Method-1 recode saving: 0 or 5.

Hence relative to the same algorithm under standard BSGS keys:

\[
\boxed{
5
\le
\Delta KS_{\rm Corr/TnM}
\le
15.
}
\]

The maximum 15 occurs only if the experimental RMFE has \(s=16\).

So BSGS+10 does strengthen Corr./TnM, but the total hidden effect is statically bounded and small relative to the hundreds of automorphism/key-switch operations in the RMFE workflow.

## 9. Likely p=5 experimental s value

Aung does not publish the exact \(s\) used in each Table-2 row.

For the p=5 correction case:

\[
e=4,\qquad
\eta=p^{e-1}=125,\qquad
w=512.
\]

Corollary 1 gives:

\[
k
\le
\min
\left\{
5^s+1,
\left\lfloor\frac{511}{125}\right\rfloor+1
\right\}
=
\min\{5^s+1,5\}.
\]

Already at \(s=1\):

\[
k_{\max}=5.
\]

Aung Example 1 chooses the smallest tested \(s\) once increasing \(s\) no longer increases \(k\): there \(s=2\) is chosen and larger s values are rejected because they keep the same maximum \(k\).

Applying that stated selection logic to p=5,w512 implies:

\[
\boxed{
s=1\text{ is the source-implied likely experimental choice}.
}
\]

This is strongly consistent with the reported \(k=5\).

However the paper does not explicitly print the row's \(s\), and no public source artifact was found.

Therefore:

\[
\boxed{
s=1\text{ is LIKELY, not source-explicit}.
}
\]

If \(s=1\), then:
- SlotsToCtxts receives zero BSGS+10 routing benefit;
- final Method-1 recode receives zero benefit;
- Corr./TnM total strengthening is exactly the known five physical KS from the five branch CoeffToSlots traces.

## 10. Thin comparator strengthening is exact regardless RMFE s

Thin does not use the RMFE parameter \(s\).

Its BSGS+10 strengthening is exactly:

\[
\boxed{
21\to20
}
\]

linear-transform physical KS.

Thus there is no hidden large thin-baseline acceleration from the ten RM10 matrices.

## 11. Pending artifact audit

The native artifact should make this fully decidable.

For Corr./TnM, report:
- actual RMFE \(s\);
- automorphism path/log for SlotsToCtxts;
- branch CoeffToSlots trace path;
- final Method-1 recode path.

Expected:
- branch trace contains the direct 4096 matrix and \(2048=[16,2032]\);
- if \(s=1\), projection requests are
  \[
  1,2,4,8,16,32,64,128,256
  \]
  and receive no +10-key shortening.

For thin:
- only its trace 4096 request should gain one hop;
- D=2 transforms remain one hop.

## Verdict

\`\`\`text
RESULT:
  PASS_GLOBAL_AUGMENTED_COMPARATOR_STRENGTHENING_BOUND

THIN_D2_S2C:
  1 -> 1

THIN_TRACE:
  19 -> 18

THIN_D2_C2S:
  1 -> 1

THIN_TOTAL_LINEAR_TRANSFORM_KS:
  21 -> 20

CORR_TNM_FIVE_BRANCH_TRANSFORMS:
  105 -> 100

CORR_TNM_COEFF_TO_SLOTS_ONLY:
  100 -> 95

METHOD1_PROJECTION_PER_MAP_SAVING:
  0 FOR s=1,2,4,8
  1 FOR s=16

SLOTS_TO_CTXT_K5_SAVING:
  0 OR 5

FINAL_ONE_RECODE_K5_SAVING:
  0 OR 5

CORR_TNM_TOTAL_BSGS_PLUS10_STRENGTHENING:
  BETWEEN 5 AND 15 PHYSICAL KS

P5_W512_SOURCE_IMPLIED_s:
  LIKELY 1
  NOT EXPLICITLY PUBLISHED

IF_s_EQUALS_1:
  CORR_TNM TOTAL STRENGTHENING = EXACTLY 5 KS

HIDDEN_LARGE_COMPARATOR_ACCELERATION:
  RULED OUT STATICALLY

TURN19_EQUAL_RESOURCE_INTERPRETATION:
  RETAIN

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  RETAIN PENDING SYSTEMS VALUE

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

Turn 19's augmented-resource warning is real but quantitatively bounded.

The ten candidate-added direct keys cannot secretly transform thin or Corr./TnM into dramatically different algorithms.

For the source-implied likely p=5 choice \(s=1\), the only comparator routing improvements are:
- thin: one fewer physical KS;
- Corr./TnM: five fewer physical KS across the five branch CoeffToSlots traces.

A Strong PASS against these augmented comparators remains a clean equal-resource algorithmic result.
