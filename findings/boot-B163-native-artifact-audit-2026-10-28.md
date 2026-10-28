# BOOT-B163 — independent native artifact audit and closure

Date: 2026-10-28
TRACK_ID: BOOT

## Artifact integrity

Artifact:
`BOOT-B163-B158-CORRECTED-NORESCALE-SI-NATIVE-20261028.zip`

Observed size: 205445 bytes

Outer SHA-256:
`bb35766751a0439de8e92db3668082930afc84fa49b32ae44b8df093ce85bfad`

Independent audit result:
- outer ZIP SHA-256 matches the reported digest;
- every entry listed by `SHA256SUMS` verifies;
- source, B162->B163 diff, exact command, stdout/stderr, stage/selector/fused/rotation CSVs, operation counts, evaluation-key sizes, environment and parameters are present;
- the non-zero exit is the intended first-failure panic.

Pinned implementation:
- upstream: `xiaopeng-stu/bfv-functional-bootstrapping`
- commit: `b113742d83d772fd0d1b353e72ac6e31f2838bea`
- Lattigo: `github.com/tuneinsight/lattigo/v6 v6.2.0`
- evaluator construction in B163 source: `bfv.NewEvaluator(params, evaluationKeys, false)`

Run parameters are the fixed source point:
- N=32768
- m=1
- r=32768
- degree=65536
- T=65537
- p=512
- LogQ=[36,34x18,30]
- LogP=[34,34,34,34]
- LWE n=2048
- h=512
- deterministic gate message=0, phase error=+1, x=1

No parameter/security change was observed in the B162->B163 experiment diff or invocation.

## Corrected RowRotation status

B158 row key:
- key level: L18
- first B158 row use in this no-rescale schedule: L18
- assertion L18 >= L18: PASS

All 12 reached RowRotations preserve exact decoded slots.

Thus:
`ROWROTATION_IMPLEMENTATION = PASS`

The previous B159-B161 under-leveled-key bug is not present.

## Genuine B163 failure

B163 schedule:
- selector plaintext multiplication at scale one;
- selector Rescale count = 0;
- fused `MulRelinScaleInvariantNew`;
- no explicit fused ct-ct Rescale;
- ciphertext remains at L18 / logQ=649.

Exact stages:
- k=1 ... 4096: exact, positive coefficient-noise budget;
- k=4096 stage: required_logQ=620, budget=+29;
- target k=8192 selector branch M_k*RowRotation(S_k): required_logQ=646, budget=+3, still exact;
- target k=8192 R*S_k branch: required_logQ=636, budget=+13, still exact;
- fused k=4096->8192 output: required_logQ=665 > logQ=649, budget=-16, mismatches=32768/32768.

Final counters:
- logical ct-ct = 13/15
- RowRotation = 12/14
- selector ct-pt = 26/31
- selector Rescale = 0
- explicit fused ct-ct Rescale = 0

Therefore:
`B163_STATUS = FAIL_B163_NATIVE_NOISE`
`FIRST_FAILING_K = 8192`
`FAILURE_PHASE = after fused ct-ct`
`LAST_CORRECT_STAGE = 4096`
`FINAL_BASIS_CORRECT = no`

No performance benchmark was run, correctly, because correctness failed.

## B162 vs B163

B163 is materially better than B162:
- B162 at k=1024: logQ=309, required=325, budget=-16.
- B163 at k=1024: logQ=649, required=515, budget=+134.

So removing selector Rescale retained 340 Q bits while accumulated absolute noise was 190 bits larger at the same stage; the net budget improved by 150 bits.

This validates the B163 hypothesis that B162's per-round selector Rescale was a major source of premature failure.

However B163 still fails before completing the recurrence.

## Strategic/sparse Rescale residual gate

Exact Lattigo v6.2.0 source for `bgv.Evaluator.Rescale` states that Rescale divides the ciphertext (rounded) by the last Q prime, divides the noise by that prime, and drops one level. B163's evaluator is instantiated with `ScaleInvariant=false`, so Rescale is not the BFV-style no-op.

Ignoring rounding, if q_i is the consumed prime:
- Q' = Q/q_i
- |e'| approximately |e|/q_i

Hence a coefficient-noise budget of the form
`log2(Q) - required_logQ(e)`
is approximately invariant under a pure Rescale. Rounding can perturb the margin but does not provide a structural source of a new +16 bits of budget.

This is also empirically consistent with the B162/B163 bracket:
- frequent selector Rescale reduces absolute required_logQ;
- but it removes Q faster and produces a strictly worse budget trajectory.

At k=4096 B163 has only +29 bits at the state, and the dominant selector factor has only +3 bits before the failing fused multiplication. A pure late Rescale cannot be expected to manufacture positive budget; aligning operands after a one-sided level drop also forces the multiplication to the lower level.

Therefore a B164 consisting only of "one or a few strategic Rescales" is not justified by the current evidence.

This is not a universal impossibility theorem for every hybrid arithmetic schedule. A genuinely different multiplication/noise-control mechanism could reopen the line. Ordinary Rescale placement is not enough evidence for another native round.

## Publication/value decision

B158 algebraic results remain valid:
- recurrence/algebra: PASS
- exact power-basis layout: PASS
- ct-ct count: 15 for r=32768
- lower bound: ceil(log2(r-1))=15
- ct-ct multiplication count in the ordinary arithmetic SIMD model: OPTIMAL
- direct prior collision: not found
- close conceptual prior: yes

But at the fixed secure/source parameter point:
`B158_NATIVE_FEASIBILITY = FAIL`

Decision:
`B158_PRACTICAL_LINE = PARK`

Do not:
- add Q primes automatically;
- weaken security;
- increase N merely to rescue this candidate;
- start B164 as a Rescale-placement tuning experiment;
- benchmark B158 despite failed correctness.

Reopen B158 practical work only if a new cryptographic/representation mechanism changes the noise recurrence materially, rather than redistributing modulus levels.

The narrow algebraic theorem may remain useful as a technique/lemma, but by itself it is not currently a CCF-A/B contribution because the source-valid native realization fails the correctness gate.

## Authoritative BOOT state after audit

LATEST_COMPLETED: `B163_AUDIT`

B163: `FAIL_B163_NATIVE_NOISE`

B158_ALGEBRA: `PASS`

B158_CTCT_MULT_COUNT: `OPTIMAL`

B158_NATIVE_FEASIBILITY: `FAIL_AT_FIXED_SOURCE_POINT`

B158_PRACTICAL_LINE: `PARK`

NEXT_NATIVE_GATE: `NONE` unless PI explicitly reopens a materially different B158 mechanism.

Paper-only priority returns to:
1. ePrint 2026/1779 interaction-rank / partial recovery scheme gate;
2. ePrint 2026/2630 lossy-KS / exact-error-bootstrap gate;
3. fresh structural BOOT scout.

No SHIP, PURE-FHE, CGS, VFHE, EXPLORE or EAI state changed.
