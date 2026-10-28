# BOOT-B158 — minimal matched native gate specification

Date: 2026-10-28
TRACK_ID: BOOT
Status: SPEC_ONLY / DO_NOT_AUTO_RUN

This file specifies the cheapest decisive native experiment for B158.
It does NOT authorize Codex, remote execution, or a benchmark.

## Why not run full bootstrapping first

B158 changes only the dominant first full-row power-basis generator

MonomialGenExtra(r=32768, wantExtra=true)

inside the 9-bit Algorithm-5 path.

The cheapest decisive test is therefore to fork the exact same real Step-1
ciphertext into two arms and compare only this subroutine.

This avoids confounding from:
- BatchLT,
- grouped powers,
- final polynomial collapse,
- LWE extraction,
- Qprime key switching,
while preserving the true noisy input produced by the source-faithful LWE->RLWE
Step 1.

## Fixed source / parameters

Use the current public repository revision being audited for 2026/975 and
Lattigo v6.2.0.

Matched 9-bit setting:

- N=32768
- m=1
- degree=65536
- T=65537
- p=512
- LogQ = source-matched 9-bit chain (current summary: 36,34x18,30)
- LogP = current source-matched chain
- LWE n=2048
- LWE h=512 for the external LWE input/output secret only
- BFV/RLWE Xs remains the Lattigo default uniform ternary
- real LWE->RLWE Step 1
- one Step-1 rescale, so polynomial input is at the same level as baseline
- same random messages/errors in both arms
- same BFV/RLWE secret key
- same relinearization key
- no parameter/security changes

Do not test a one-Q-prime-smaller chain in this first gate.

## Candidate implementation

Add a new function, conceptually:

MonomialGenExtraCoPacked(...)

for the full-row case s=r=32768.

Do not rewrite Algorithm 5 yet.

The function must implement the B158 invariant from the formal finding:

S_k row =
[first half: repeated P_k(x) |
 second half: repeated x^k].

Operation count must be instrumented and asserted:

- exactly 15 ct-ct MulRelin+Rescale operations
- exactly 14 RowRotations
- only the single row-swap Galois element
- O(log r) public scale-1 selector multiplications
- no hidden extra ct-ct multiplication
- no hidden selector rescale

The original baseline must remain unchanged.

## Evaluation-key handling

The experiment must generate the row-rotation key at the maximum level at
which B158 actually uses it.

Record:
- whether that Galois element already exists in the source key set;
- its previous LevelQ if present;
- new required LevelQ;
- incremental binary key size;
- total evaluation-key size before/after.

Do not silently force every Galois key to full level.

## P0-A: exact algebra / layout in native ciphertexts

For at least 10 independently generated real Step-1 inputs:

Baseline arm:
- run source MonomialGenExtra(r, wantExtra=true).

Candidate arm:
- run B158 co-packed replacement.

Decrypt both outputs.

Require:
1. candidate power-basis slots equal exact clear target for all N slots;
2. candidate auxiliary x^(r/2) slots equal exact clear target;
3. baseline remains correct;
4. candidate and baseline represent the same logical power table, allowing only
   a documented harmless physical repetition/layout equivalence if necessary.

Any mismatch:
- FAIL_NATIVE_CORRECTNESS
- stop before timing claims.

## P0-B: level and scale trace

For every B158 stage record:

- stage k
- input LevelQ / logQ
- input scale mod T
- after RowRotation level/scale
- after each selector-linear operation level/scale
- factor level/scale
- after fused MulRelin
- after Rescale level/scale

Assertions:

- selector multiplications do not consume a level;
- one fused ct-ct multiplication consumes exactly one level;
- final basis is one Q level above the original basis under the same Q chain;
- auxiliary output is at the predicted level;
- no accidental scale-matching multiplication or hidden rescale occurs.

## P0-C: native noise trace

Run this separately from the timing run because detailed noise tracing is slow.

Use the repository's existing exact noise tracing machinery
(poly-noise-trace / mul-trace-noise or a minimal equivalent).

For every candidate stage measure:

1. noise before RowRotation;
2. noise after RowRotation;
3. noise after selector factor construction;
4. noise immediately after fused ct-ct MulRelin;
5. noise after Rescale.

Also record:
- noise budget / max absolute coefficient noise;
- exact level and Q bits;
- first stage where candidate exceeds the matched baseline envelope, if any.

Important diagnostic:

Create a COPY of the final B158 basis and rescale that diagnostic copy once
from its natural L3-like level to the baseline L2-like level.

Compare its noise to the baseline basis at the same level.

This forced-rescale copy is diagnostic only and must not be used for the
candidate timing path.

Interpretation:
- natural candidate correct but forced-L2 diagnostic bad:
  same-Q B158 may remain viable, but one-Q-prime reduction is high risk.
- natural candidate noise margin collapses before final stage:
  FAIL_NATIVE_NOISE.

## P0-D: isolated performance

Noise tracing OFF.

Warm up before recording.

For a matched set of inputs, measure paired timings for:

Baseline:
- MonomialGenExtra(r, wantExtra=true)

Candidate:
- MonomialGenExtraCoPacked(r, wantExtra=true)

Report separately:
- total basis time
- baseline BuildPowers
- baseline BuildY
- candidate selector construction time
- candidate RowRotation time
- candidate ct-ct Mult+Rescale time
- candidate auxiliary-output assembly time

Use medians and paired per-input ratios; at least enough repetitions to make the
ratio stable.

Do not include key generation in the online basis timing.

## Native value threshold

Current public 9-bit m=1 summary has approximately:

- online total: 2.061 s
- BuildBasis: 1.141 s

If all other stages are unchanged, a 10% end-to-end online speedup requires
saving about:

2.061 - 2.061/1.10 ~= 0.187 s

which is about:

0.187 / 1.141 ~= 16.4%

of BuildBasis time.

Therefore use a derived, not arbitrary, first value gate:

- basis speedup >=17%:
  PASS_ISOLATED_VALUE, proceed to full Step-2 integration.
- basis speedup 10--17%:
  CONDITIONAL; continue only if noise is substantially better or a one-Q-prime
  reduction later appears credible.
- basis speedup <10%:
  FAIL_NATIVE_VALUE for the current implementation unless the depth/parameter
  reduction independently creates a strong result.
- candidate slower:
  immediate FAIL_NATIVE_VALUE.

These thresholds should use the matched machine's own baseline timings, not the
repository's historical absolute seconds.

## P1 only if P0 passes

Integrate B158 into the complete polynomial-evaluation Step 2 while keeping the
same Q chain.

Measure:
- Step-2 correctness
- polynomial-output noise
- Step-2 latency
- online total projected/actual delta
- memory and key size

Only after SAME-Q P1 is clean may the one-Q-prime-smaller variant be tested.

## P2 only after same-Q success

Try the one-Q-prime-smaller chain.

This is secondary because the extra prime is the natural safety margin for the
deferred selector normalization.

Require:
- security at least unchanged/improved;
- exact correctness;
- no noise-budget collapse;
- additional latency/memory benefit.

## Stop rules

Stop and record failure immediately on any of:

- algebra/layout mismatch;
- hidden extra ct-ct multiplication;
- selector unexpectedly consumes a level;
- natural same-Q candidate loses decryptability;
- isolated basis speedup <10% with no independent parameter benefit;
- high-level row key causes unacceptable memory growth.

## Current authorization

CODEX_REQUIRED_FOR_NATIVE_GATE: YES
DO_NOT_AUTO_RUN_CODEX: YES
PI_AUTHORIZATION: NOT_GIVEN_IN_THIS_FINDING
