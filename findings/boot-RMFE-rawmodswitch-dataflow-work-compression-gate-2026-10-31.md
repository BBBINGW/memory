# BOOT RMFE rawModSwitch Dataflow Work-Compression Gate

Date: 2026-10-31
Session: 密码学 16.0
Logical Research Turn: 13/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

The authorized native task
\`BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01\`
remains pending and untouched.

This turn audits the pinned HElib rawModSwitch dataflow under the Turn-12 compact-carry result:

> If only one aggregate raw polynomial plus the compact carry state is ultimately required, which rawModSwitch substeps can actually be reduced from k=5 branches to one, and which still require five-way work?

No native execution, source mutation, Codex resubmission, or second heavy local task occurred.

## Pinned source path

Pinned HElib lineage:

\`homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1\`.

In \`Ctxt::rawModSwitch\`, for each ciphertext part:

1. \`PowerfulDCRT::dcrtToPowerful(pwrfl, parts[i])\`;
2. coefficientwise scale/round and plaintext-residue correction;
3. final centering modulo q;
4. \`PowerfulDCRT::powerfulToZZX(zzParts[i], pwrfl)\`.

After relinearization, thin bootstrapping requires exactly two ciphertext parts.

For k=5 RMFE branches, the stock branchwise path therefore invokes these per-part stages 10 times.

## Power-of-two special case: powerful basis conversion is trivial

Current bootstrapping geometry has

\[
m=32768
\]

and

\[
mvec=[32768].
\]

HElib \`PowerfulDCRT\` sets

\[
\texttt{triv}=(\texttt{mvec.length()}==1).
\]

The source comment states:

\`triv means poly and pwfl bases are identical\`.

Hence in the current parameter regime:

### dcrtToPowerful

\[
\texttt{dcrtToPowerful}
=
\texttt{DoubleCRT::toPoly}
+
\text{VectorCopy}.
\]

No nontrivial ZZX-to-powerful basis conversion is executed.

### powerfulToZZX

\[
\texttt{powerfulToZZX}
=
\texttt{NTL::conv(poly,powerful)}.
\]

Thus the final powerful-to-ZZX stage is only a linear vector/polynomial conversion, not an FFT/CRT basis transformation.

This removes the main motivation for treating Turn-12 output materialization as a potentially large rawModSwitch saving.

## The actual heavy stage: DoubleCRT::toPoly

\`DoubleCRT::toPoly\` performs two explicit heavy phases.

### 1. Inverse FFT phase

For every active CRT prime:

\[
\texttt{ithModulus(i).iFFT(...)}
\]

is executed to recover coefficient residues.

The source wraps this stage in

\[
\texttt{toPoly_FFT}.
\]

### 2. Integer CRT phase

For every one of the

\[
\phi(m)=16384
\]

coefficients, the residues over the active primes are reconstructed into one centered integer coefficient.

The source wraps this stage in

\[
\texttt{toPoly_CRT}.
\]

The whole function also has its own function-level timer \`toPoly\`.

Therefore the expensive branch-local conversion is not \`powerfulToZZX\`; it is the DCRT-to-centered-integer reconstruction inside \`toPoly\`.

## Why 10 toPoly calls remain unavoidable in the current source-level design

Turn 12 derived compact carries

\[
\kappa_P,\kappa_q
\]

such that the exact branchwise raw sum can be reconstructed from an aggregate raw state plus the two carries.

However those carries depend on branch-specific rounding decisions:

\[
x_i,\delta_i,t_i.
\]

The pinned HElib implementation computes those decisions only after the branch's centered integer powerful coefficients \(c_i\) have been recovered.

Those \(c_i\) are produced by

\[
\texttt{DoubleCRT::toPoly}.
\]

Thus, using the current HElib dataflow and APIs:

- each of 5 branches still needs both ciphertext parts converted;
- each conversion still needs the branch's own inverse-FFT/CRT reconstruction;
- the coefficient rounding loop still runs on all 10 branch parts.

Hence:

\[
\boxed{
T_{\rm toPoly}:\ 10\to10
}
\]

and

\[
\boxed{
T_{\rm round-loop}:\ 10\to10.
}
\]

This is a source-level work statement, not a universal lower bound on all possible RNS implementations.

## What can actually be compressed

Although the dominant conversion remains branchwise, several downstream operations can be streamed.

### 1. Branch raw ZZX materialization

Instead of materializing ten branch \`zzParts\` polynomials, process one branch part at a time:

- recover its centered coefficient vector;
- execute the exact branch rounding loop;
- accumulate the shifted raw coefficients directly into two aggregate powerful/coeff vectors;
- accumulate whatever carry data is needed;
- discard the branch scratch vector.

Only two aggregate ciphertext-part vectors are retained.

Thus

\[
\text{full branch raw ZZX outputs}:10\to0
\]

as persistent objects.

### 2. powerfulToZZX

Because the current powerful/poly bases are identical, the candidate needs at most one final conversion for each of the two aggregate parts:

\[
\boxed{
\texttt{powerfulToZZX}:10\to2.
}
\]

This is only an \(O(N)\) conversion and is expected to be much cheaper than \`toPoly\`.

It can even be delayed until after aggregate coefficientwise carry/divisibility processing.

### 3. newMakeDivisible / divide

Turn 11 established carry-corrected aggregation across the divisibility-lift map.

Therefore coefficientwise divisibility processing changes from

\[
5\times2=10
\]

branch-part polynomial passes to

\[
1\times2=2
\]

aggregate-part passes, plus cheap public carry correction.

### 4. common boot-key reconstruction

The already-established exact post-round identity retains:

\[
5\to1
\]

for copying \`recryptEkey\`, multiplying by the second public polynomial, and adding the first.

### 5. inverse/recovery transform

Turn 8 retains the 4-call joint restricted recovery.

## Revised static work ledger

### Baseline five-branch middle path

Raw-conversion-related work:

- \`DoubleCRT::toPoly\`: 10 calls;
- coefficient rounding loops: 10 full coefficient-vector passes;
- \`powerfulToZZX\`: 10 conversions;
- \`newMakeDivisible/divide\`: 10 full polynomial passes;
- boot-key reconstruction: 5;
- five independent inverse thin transforms.

### Current revised candidate

- \`DoubleCRT::toPoly\`: **10 calls**;
- coefficient rounding loops: **10 passes**;
- persistent branch raw polynomial materialization: **eliminated**;
- \`powerfulToZZX\`: at most **2**;
- \`newMakeDivisible/divide\`: **2 aggregate passes**;
- boot-key reconstruction: **1**;
- recovery: **4 nonidentity automorphism/key-switch calls** after RM10.

Thus compact carry state compresses representation and downstream work, but does not reduce the main branchwise DCRT-to-integer conversion count in the pinned implementation.

## Asymptotic interpretation

Let

\[
N=\phi(m)=16384
\]

and \(L\) be the number of active ciphertext CRT primes at rawModSwitch.

The retained dominant conversion work is approximately:

\[
2k
\left[
L\cdot \operatorname{iFFT}(N)
+
N\cdot\operatorname{CRT}(L)
\right].
\]

For k=5 this is 10 branch-part conversions.

The newly removable work is primarily linear coefficient processing:

\[
O(2(k-1)N)
\]

for output materialization/divisibility passes, plus the already-known inverse-transform/reconstruction savings.

Therefore Turn-12 compact carry state does **not** create a new k-to-1 rawModSwitch asymptotic improvement under the stock HElib representation.

## Existing timers already expose the decisive substage

No modification of the pending native task is needed.

\`DoubleCRT::toPoly\` already contains:

- function timer \`toPoly\`;
- named timer \`toPoly_FFT\`;
- named timer \`toPoly_CRT\`.

Therefore, if the pending Turn-4 run preserves \`printAllTimers\` / timer logs as required, its result can be audited for the total cost of the dominant branchwise raw conversion without adding new instrumentation.

This is especially important because Turn 11 superseded the old simple retained-share hard-kill rule.

The revised timing interpretation should distinguish:

\[
T_{\rm unavoidable}
\approx
T_{\rm S2C}
+
T_{\rm reLinearize}
+
T_{\rm toPoly}
+
T_{\rm branch-round-loop}
\]

from removable:

- branch raw ZZX materialization;
- five-way newMakeDivisible/divide;
- four extra boot-key reconstructions;
- five branch-local inverse transforms.

## Can toPoly itself be reduced from 10 to 2?

Not with the current exact compact-carry construction.

\`DoubleCRT::toPoly\` is linear, so the ten DCRT parts could be shifted/aggregated before conversion and converted only twice.

But aggregate-only coefficients are insufficient to reconstruct the branchwise rounding decisions, as shown by the Turn-11 rawModSwitch collision.

To use only two aggregate \`toPoly\` calls, one would need a new algorithm that extracts the compact carry state directly from branch RNS residues without reconstructing each branch's centered integer coefficients.

That is a different RNS/base-conversion research problem.

No such algorithm is established here.

## Scientific disposition

The Turn-12 compact carry-state branch survives as:

- an exact semantic compression;
- a low-memory/streaming implementation aid;
- a way to move fusion before \`newMakeDivisible\`.

It does **not** currently support a claim that branchwise rawModSwitch computational work has been substantially collapsed.

The research-value center remains:

1. remove repeated reconstruction/inverse-transform work;
2. possibly remove repeated divisibility-lift work;
3. measure whether the retained 10 \`toPoly\` calls are already too expensive.

## Verdict

\`\`\`text
RESULT:
  FAIL_COMPACT_CARRY_TO_COLLAPSE_DOMINANT_RAW_WORK

POWERFUL_BASIS_CONVERSION_CURRENT_M:
  TRIVIAL

DCRT_TOPOLY:
  10 -> 10 / UNAVOIDABLE IN CURRENT DATAFLOW

BRANCH_ROUNDING_LOOP:
  10 -> 10

POWERFUL_TO_ZZX:
  10 -> <=2 / LOW-VALUE LINEAR SAVING

NEWMakedIVISIBLE_DIVIDE:
  10 -> 2 + PUBLIC CARRY CORRECTION

BOOTKEY_RECONSTRUCTION:
  5 -> 1

PERSISTENT_BRANCH_RAW_MATERIALIZATION:
  ELIMINATED

RAW_ASYMPTOTIC_K_TO_1_SPEEDUP:
  NO

RNS_DIRECT_CARRY_EXTRACTION:
  NEW ALGORITHM REQUIRED / NOT ESTABLISHED

PENDING_NATIVE_TASK:
  UNCHANGED / DO NOT RERUN

NATIVE_LATENCY:
  NOT ESTABLISHED

WHOLE_PIPELINE_CAPACITY:
  NOT ESTABLISHED

PUBLISHABLE_NOVELTY:
  NOT ESTABLISHED

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Next independent side-research

If the pending timer is still unavailable, do not continue local micro-optimizations of raw materialization.

The next highest-value independent question is a static **best-case revised latency ceiling**:

- treat the retained ten \`toPoly\` conversions and ten branch rounding loops as unavoidable;
- set every now-removable downstream raw/divisibility/reconstruction/recovery cost optimistically to zero or to the exact 4-call recovery proxy;
- combine with the published 4.732 s MultKey block and any source-level timer ratios available from HElib benchmarks/literature.

If even that optimistic ceiling cannot cross the throughput frontier, kill the branch before native candidate implementation.

AI_PROVISIONAL_CHOICE:
  RETAIN_MAIN_POSTRAW_FUSION
  PARK_COMPACT_CARRY_AS_RAW_WORK_SPEEDUP
  USE_PENDING_TOPOLY_TIMERS_TO_REVISE_VALUE_GATE

INDEPENDENT_RESEARCH_AVAILABLE: true
RESEARCH_FRONTIER_EXHAUSTED: false
