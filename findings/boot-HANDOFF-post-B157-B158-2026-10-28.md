# Resume BOOT after B157 audit and B158 paper-level gates

Date: 2026-10-28  
TRACK_ID: BOOT

## Authoritative transition

LATEST_COMPLETED: B157_AUDIT

B157 exact secure native point:
- HEStd_128_classic instantiation: PASS
- N=65536
- depth=32
- scaleBits=50
- NumLargeDigits=33
- Q=1650 bits
- P=60 bits
- QP=1710 bits
- no output repacking
- one sequential Root4096/FBS

Native result:
- FAIL_NATIVE_PRECISION
- FAIL_NATIVE_PERFORMANCE
- 3615/65536 exact bits
- 256/256 failed words
- max abs error 1,053,561.251602464
- core latency 288.337000858 s
- fair baseline 48.99471343 s
- candidate 5.885x slower
- shared powers + 8 LUT alone 259.090102449 s
- peak sampled memory ~201 GiB

Interpretation:
- B145 algebra remains VALID / POTENTIALLY_NOVEL
- B145+B152 practical backend is PARK / FAIL_NATIVE_VALUE
- reopen B145 only if a genuinely different 4096-domain one-FBS backend can
  plausibly make shared powers + eight LUTs about <=20 s with robust precision
- do not spend further rounds on local scale/digit/repacking/Hermite tuning

MAIN_POSITIVE_CANDIDATE: NONE after B157
until B158 passes native/value gates.

## Current fresh candidate: B158

B158 = co-packed optimal EvalPower for the sparse BFV functional-bootstrap
framework of ePrint 2026/975.

Core result:
- uses duplicated slots + BFV two-row hypercube
- co-packs the power-basis accumulator and current x^(2^i) squaring value in
  one ciphertext
- each round uses RowRotation + public selectors so ONE ct-ct multiplication
  simultaneously:
  1. extends P_k=(1,x,...,x^(k-1)) to P_2k
  2. squares x^k to x^(2k)

For s=2^ell:
- paper Algorithm 3: 2ell-2 ct-ct Mult
- B158: ell ct-ct Mult + ell RowRotation
- ell is a lower bound because the output contains x^(s-1)
- therefore B158 is optimal in ct-ct multiplication count

9-bit important case:
- s=r=32768=2^15
- 28 -> 15 ct-ct Mult (46.43% reduction)
- adds 15 uses of the same RowRotation

Paper-level gates already passed:
- exact algebra toy falsification
- batch-layout generalization
- output-layout compatibility
- auxiliary x^(s/2) compatibility
- Lattigo API/level gate

Prior art:
- no direct collision found in preliminary search
- novelty remains PROMISING_NOT_ESTABLISHED

Value caveat:
- key-switch count does not fall:
  paper ~28 relinearization KS
  B158 ~15 relinearization KS + 15 rotation KS
- value comes from removing 13 tensor multiplications + rescale steps
- native latency therefore remains unresolved

Level candidate:
- one-Q-prime-smaller 9-bit chain is mechanically plausible
- not yet claimed because final scale/noise alignment needs native validation

Selector noise:
- exact Lattigo batching ordering was reconstructed
- 0/1 selector plaintexts can have large centered polynomial norms
- worst late B158 selector l2 ~= 2^21.21, l1 ~= 2^28.01
- so selectors are NOT noise-neutral
- next ~34-bit prime rescale means no immediate paper-level impossibility
- native per-stage noise trace is required

## Current status

B157_STATUS: FAIL_NATIVE_PRECISION_AND_PERFORMANCE
B145_ALGEBRA_STATUS: VALID / POTENTIALLY_NOVEL
B145+B152_STATUS: PARK / FAIL_NATIVE_VALUE

ACTIVE_FRESH_CANDIDATE: B158
B158_STATUS: PAPER_LEVEL_PROMISING / NATIVE_NOT_RUN
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B158_CODEX_REQUIRED_FOR_DECISIVE_NATIVE_GATE: YES
DO_NOT_AUTO_RUN_CODEX: YES

## Next action

Before native work:
1. one more focused prior-art audit for the exact co-packed accumulator+squaring
   fusion;
2. write the recurrence/proof in paper-ready form;
3. define the minimal matched native experiment.

Only if PI explicitly authorizes Codex/native work:
- patch the public 2026/975 implementation,
- replace only the large MonomialGenExtra power-basis stage,
- keep parameters/functions/input vectors fixed,
- first test same Q chain,
- log level/scale/noise after every selector and fused multiplication,
- only after correctness test the one-Q-prime-smaller candidate.
