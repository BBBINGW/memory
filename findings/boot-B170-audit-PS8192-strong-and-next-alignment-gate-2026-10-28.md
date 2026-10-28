# BOOT — B170 audit: PS8192 strong PASS and next aligned-input gate

Date: 2026-10-28
TRACK_ID: BOOT

## Artifact audit

Artifact:
\`BOOT-B170-B158-PS8192-8BLOCK-LT-NATIVE-20261028.zip\`

Reported and independently recomputed SHA-256:
\`be1970c874a7a89472be6bceceb1f3d27a141ab43dab78e9ea6b36eeea02e7a8\`

Internal SHA256SUMS:
- 24/24 entries PASS
- no mismatches

Packaged B169 parent:
\`parent-b169/main.go\`
SHA-256:
\`a36168f664e102b6c9fff0259cc8d7c7ccebb6aa4ba5776b4730e765c2f84ed4\`

This is byte-for-byte identical to \`source/main.go\` in the independently audited B169 artifact.

The B169->B170 diff is limited to:
- adding the H=8192 / s=8 isolated gate;
- stopping checkpoint recurrence at H=8192;
- building the 8-block exact LT reference;
- adding exact operation counters;
- adding the required raw-L18 Galois-key plan/assertions;
- B170 reporting/evidence logic.

No Q/N/T/p/secret/security change, refresh/bootstrap, pre-LT DropLevel, or Rescale is introduced.

## Native result

\`STATUS = PASS_B170_PS8192_LT8\`

\`HEADROOM = STRONG\`

All three fixed cases pass:
- PH8192_REP exact, 0/32768 mismatches
- LT8 exact, 0/32768 mismatches
- raw LT remains at L18

Per-case:
- CASE_0: PH budget 87, LT8 budget 52, LT delta +35 bits
- CASE_1: PH budget 87, LT8 budget 53, LT delta +34 bits
- CASE_2: PH budget 87, LT8 budget 52, LT delta +35 bits

Thus:
\[
\boxed{\min \mathrm{budget}(PH_{8192})=87,\qquad
\min \mathrm{budget}(LT_8)=52.}
\]

This validates the noise-aware PS-aspect-ratio hypothesis: reducing baby basis H from 16384 to 8192 recovers about 36 bits of input headroom while the LT itself still costs approximately the same 34--35 required bits.

## Native operation counts

Executed:
- main fused ct×ct = 13
- auxiliary square ct×ct = 7
- basis total ct×ct = 20
- basis RowRotation = 13
- ParallelLT ct×pt = 8
- baby rotations = 2
- giant rotations = 2
- sum-column rotations = 11
- final row rotation = 1
- ParallelLT total rotations = 16

Projected-only values are correctly marked as projected:
- grouped-power ct×ct = 4
- pointwise ct×ct = 1
- leading ct×ct = 1
- projected full skeleton = 26 ct×ct

The 26-ct×ct invariant remains algebraically consistent:
\[
13+7+4+1+1=26.
\]

## Key-memory consequence

B170 key summary:
- relinearization L18: 57.50 MiB
- Galois/rotation L18: 6 keys, 345.01 MiB
- Galois/rotation L19: 11 keys, 660.02 MiB
- total evaluation keys: about 1.04 GiB (sum approximately 1062.53 MiB)

B169:
- relinearization L18: 57.50 MiB
- Galois/rotation L18: 4 keys, 230.01 MiB
- Galois/rotation L19: 11 keys, 660.02 MiB
- total: 947.53 MiB

Thus the raw-L18 s=8 geometry adds two high-level LT rotation keys (notably shifts 3 and 6) and about 115 MiB relative to B169.

This does not invalidate B170, but it means the final design should not automatically retain raw-L18 LT if an equivalent lower-level schedule exists.

## Important next scheduling opportunity

For s=8, the author's MonomialGenExtra-style grouped-power path from a level-L18 ciphertext has theoretical output level:
\[
L18-(\log_2 8+1)=L14.
\]

The same path uses:
- 4 ct×ct operations;
- an output grouped basis at L14;
- an extra \(y^4=x^{32768}\) ciphertext on the binary-power branch for the eventual leading term.

B170 currently evaluates LT8 at L18. To use the grouped basis later, LT must ultimately be aligned downward.

A genuine BGV Rescale approximately reduces both Q and absolute error and was already observed in B167 to preserve noise budget exactly across sequential levels.

Therefore the next high-value gate is:

1. natively generate the s=8 grouped powers from \(y=x^{8192}\);
2. observe their actual output level and budget;
3. Rescale PH8192_REP down to that actual grouped-output level before LT;
4. run the same exact LT8 at that lower level;
5. compare exact correctness/noise with the B170 raw-L18-then-align schedule;
6. measure the resulting evaluation-key size.

This tests a stronger scheduling principle:
\[
\boxed{\text{Rescale-before-public-linear-LT instead of DropLevel or high-level LT.}}
\]

If it preserves the ~52-bit LT headroom, it should be preferred because:
- it naturally aligns with grouped powers;
- it avoids unnecessary high-level LT arithmetic;
- it can lower required LT Galois-key levels and memory.

## State

- B165 checkpoint robustness: PASS_STRONG
- B169 LT attribution: PASS
- B170 H=8192 / s=8 aspect ratio: PASS_STRONG
- noise-aware PS aspect ratio: VALIDATED_NATIVELY
- grouped powers at s=8: PROJECTED_NOT_YET_NATIVE
- aligned lower-level LT schedule: NOT_RUN
- pointwise/lower polynomial: NOT_RUN
- active candidate: ACTIVE_NATIVE_CANDIDATE
- novelty: PROMISING_NOT_ESTABLISHED

## Recommended next gate

B171 = aligned pointwise-input preparation:
- H=8192, s=8, k0=64;
- generate \(y=x^{8192}\) repeated;
- native s=8 grouped-power generation;
- record grouped output level/budget and \(y^4\) extra;
- genuine Rescale PH8192 to the grouped output level;
- run LT8 there with level-correct keys;
- verify both pointwise inputs exact and positive-budget;
- compare evaluation-key memory with B170;
- stop before pointwise ct×ct.

Only after this passes should B172 execute the pointwise multiply and rotate-and-sum lower polynomial.
