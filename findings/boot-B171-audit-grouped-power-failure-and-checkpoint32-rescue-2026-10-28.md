# BOOT — B171 audit: grouped power chain failure and checkpoint-32 rescue hypothesis

Date: 2026-10-28
TRACK_ID: BOOT

## Artifact audit

Artifact:
\`BOOT-B171-B158-PS8192-ALIGNED-POINTWISE-INPUTS-20261028.zip\`

Reported and independently recomputed SHA-256:
\`6d78f48628d56544ce413cfeedbfc030a6447aad4a3245f0d2894876816c6081\`

Internal SHA256SUMS:
- 24/24 entries PASS
- no mismatches

The packaged parent identifies the audited B170 artifact:
\`BOOT-B170-B158-PS8192-8BLOCK-LT-NATIVE-20261028.zip\`
with SHA-256
\`be1970c874a7a89472be6bceceb1f3d27a141ab43dab78e9ea6b36eeea02e7a8\`.

The B170->B171 diff introduces the isolated grouped-power and aligned-LT gate, without changing Q/N/T/p/secret/security/checkpoint parameters.

## Native result

\`STATUS = FAIL_B171_GROUPED\`

All three cases reproduce:
- exact H=8192 checkpoint basis at L18;
- exact repeated \(y=x^{8192}\) at L18;
- basis ct×ct count = 20.

Y_REP budgets:
- CASE_0: 107
- CASE_1: 107
- CASE_2: 105

The source-faithful s=8 \`MonomialGenExtraPrecomp\` path then executes:
- grouped ct×ct = 4
- grouped ct×pt = 3
- Rescale = 7
- grouped output level = L14

All grouped outputs fail with budget -16.

The saved \(y^4\) extra already fails at L16:
- required_logQ = 597
- logQ = 581
- budget = -16
- essentially all slots wrong

for all three cases.

Therefore the failure occurs **before the grouped accumulator is the decisive bottleneck**.

## Exact source location of first structural failure

For s=8:
- \`pre.Ell = 3\`;
- \`xPow[0]=y\`;
- \`xPow[1]=y^2\`;
- \`xPow[2]=y^4\`.

The returned \`extra\` is:
\[
\texttt{xPow[pre.Ell-1]} = y^4.
\]

Thus B171 proves that the source-faithful binary power subchain
\[
y \rightarrow y^2 \rightarrow y^4
\]
using
\[
\texttt{MulRelinNew + Rescale}
\]
has already exhausted correctness by \(y^4\), before the later mask/accumulator combination is the main issue.

This is distinct from the checkpoint auxiliary chain, which uses:
\[
\texttt{MulRelinScaleInvariantNew}
\]
without Rescale and empirically grows by only about 30--31 required-logQ bits per square.

## Why k0=32 is the cheapest next structural rescue

In the current k0=64 path, the checkpoint auxiliary is created as:
\[
A_{64}=R S_{64}.
\]

For the B171 fixed cases, this has required_logQ about 325--326.

But the same pre-checkpoint recurrence already computes:
\[
R S_{32}
\]
as part of the ordinary \(32\to64\) factor construction.

Observed required_logQ:
- approximately 276--278 across the fixed cases.

If this already-computed ciphertext is retained as:
\[
A_{32}:=R S_{32},
\]
then one scale-invariant square gives a predicted
\[
A_{64}\approx 307--309
\]
instead of 325--326.

That is roughly an 18-bit cleaner auxiliary state, and the advantage should persist through later clean auxiliary squares to \(A_{8192}\).

B171's first observed \(y^4\) failure is exactly 16 bits beyond the available L16 modulus.

Therefore k0=32 is a quantitatively targeted next gate: one additional auxiliary square may recover approximately the same amount of headroom as the observed deficit.

## Operation-count tradeoff

For degree \(D=2^{16}\), baby basis H=8192, and checkpoint \(K=2^c\), the previously derived full skeleton count is:
\[
2d-c.
\]

Thus:
- k0=64, c=6: 26 ct×ct projected full skeleton;
- k0=32, c=5: 27 ct×ct;
- k0=16, c=4: 28 ct×ct.

The source reference skeleton remains approximately 31 ct×ct.

So k0=32 would still preserve a projected 4-ct×ct reduction (about 12.9%) while potentially recovering enough noise to make grouped generation feasible.

## Recommended next gate

B172 should change only the checkpoint from k0=64 to k0=32 while keeping:
- H=8192;
- s=8;
- all source/security parameters;
- source-faithful grouped MonomialGenExtraPrecomp;
- no aligned LT or pointwise yet.

It should:
1. retain the already-computed \(R S_{32}\) as \(A_{32}\);
2. use checkpoint-decoupled main factors starting at k=32;
3. square the clean auxiliary from 32 to 8192 with \`MulRelinScaleInvariantNew\`;
4. construct PH8192 and Y_REP;
5. run the unchanged s=8 grouped helper;
6. probe y^2, y^4, every grouped internal factor/accumulator stage if possible;
7. stop after grouped output.

Decision:
- if k0=32 makes y4 and grouped output exact with positive budget, advance;
- if y4 passes but grouped accumulator fails, the next bottleneck is then isolated;
- if y4 still fails by only a small amount, k0=16 is the next finite checkpoint tradeoff;
- do not change multiplication primitive in the grouped helper yet, because checkpoint placement is a cleaner global design parameter and preserves source-faithful downstream semantics.

## State

- B170 PS8192 LT8: PASS_STRONG
- B171 grouped source-faithful path: FAIL
- failure locus: binary power subchain by y4
- k0=32 rescue: OPEN / HIGH-PRIORITY
- aligned LT: NOT_RUN because grouped failed first
- pointwise/lower polynomial: NOT_RUN
- active candidate remains ACTIVE_NATIVE_CANDIDATE
