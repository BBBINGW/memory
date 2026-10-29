# BOOT RMFE R8 Fixed-Q Ledger and Six-Key-Switch Schedule Gate

Date: 2026-10-29  
Session: 密码学 11.0, Research Turn 14/25  
Classification: `PASS_STATIC_EXACT_FIXED_Q_LEDGER_AND_6KS_SCHEDULE`

## Scope

This was the next static gate for the reversible provisional candidate `RMFE_SUBRING_ENVELOPE_SINGLE_MULTKEY`. It used the exact `normal_basis=false` R8 maps established at Turn 13 and tested whether they admit a lower-cost exact automorphism schedule whose public-multiplier tax does not by itself exhaust the pinned fixed-Q capacity.

No native trace, fresh-encryption surrogate, key generation, DFR run, full Algorithm 5 run, timing benchmark, RSS measurement, or parameter sweep was performed in this research turn. RMFE remains provisional and is not a validated redesign.

## Exact BSGS schedule

For both S2C and C2S, the direct 16-branch automorphism-multiplier operator was reconstructed exactly as

```text
P0 + sigma_17(P1) + sigma_31(Q0 + sigma_17(Q1)).
```

The grouped schedule agrees with the direct operator on all `16/16` plaintext basis images for each direction.

Per map, the exact operation ledger is:

```text
automorphism/key-switch calls: 6
ciphertext-plaintext multiplications: 16
additions: 15
ciphertext-ciphertext multiplications: 0
```

For the two maps together:

```text
automorphism/key-switch calls: 12
ciphertext-plaintext multiplications: 32
additions: 30
ciphertext-ciphertext multiplications: 0
```

The direct 15-nonidentity-branch realization is strictly dominated by this exact schedule and is parked.

## Optimistic fixed-Q ledger

Using the pinned HElib conservative public-multiplier noise ledger, while deliberately excluding key-switch and mod-switch additions that require native evidence:

| Map | Canonical mask-norm sum | Optimistic capacity loss |
|---|---:|---:|
| S2C | 9184.392654286061 | 13.164968606584 bits |
| C2S | 18181.747112241468 | 14.150203216544 bits |
| Sequential total | — | 27.315171823128 bits |

This is an optimistic HElib ledger tax, not a lower bound on decryption error. It excludes the actual `D_u E_u/P` terms, mod-down behavior, `InnerProduct`, and RM10 noise. The published fixed-Q baseline begins near 391.1 bits and retains about 101.0 bits after its complete correction workflow, so the map tax alone does not statically kill the candidate. Those baseline stage capacities cannot be transferred to the proposed pipeline as a correctness or final-capacity result.

When the baseline `addFrbMatrices`/`addSome1DMatrices` key set is retained, exponents `5,25,125,625,g` do not require map-specific additional key bytes. This does not establish a key-memory advantage and says nothing about RSS.

The normalization constant `224` must be applied exactly once through the scalar-unit overload; it must not be encoded as a polynomial mask. Its inverse modulo 625 is `399`.

## Verdict

```text
RESULT: PASS_STATIC_EXACT_FIXED_Q_LEDGER_AND_6KS_SCHEDULE
OPTIMISTIC_FIXED_Q_FEASIBILITY: PASS
WHOLE_PIPELINE_CAPACITY: UNCLEAR
NATIVE_CORRECTNESS: NOT_ESTABLISHED
VALIDATED_CANDIDATE: NO
AI_PROVISIONAL_CHOICE: RETAIN_RMFE_PROVISIONAL_AND_EXECUTE_BOUNDED_NATIVE_MIDDLE_GATE
```

## Next cheapest decisive test

The bounded native task

```text
BOOT-RMFE-R8-BSGS-MIDDLE-FIXEDQ-NATIVE-20261029-R14-01
```

was delegated to Codex with fixed `p=5`, `r=4`, plaintext modulus 625, `m=32768`, `bits=400`, width 512, five retained coordinates, one deterministic run, and no rescue or sweep. It must use the real RMFE projection/envelope interface and execute only:

```text
one ModSwitch
-> exact BSGS S2C_R8
-> one InnerProduct/MultKey
-> one RM10
-> scalar normalization by 224
-> exact BSGS C2S_R8
-> unpack and compare the first five coordinates
```

It stops before correction DigitExtract, full Algorithm 5, DFR, or benchmarking. The native result must return to the same Research GPT for independent audit before any scientific PASS/FAIL claim is accepted.

## Accepted boundary

Established:

- exact six-key-switch schedule for each R8 map;
- `16/16` direct-operator basis equivalence for each map;
- exact operation counts;
- optimistic public-multiplier fixed-Q tax;
- a bounded, source-faithful native falsification task.

Not established:

- source-interface reconstruction or native correctness;
- actual key-switch/mod-switch ledger closure;
- whole-pipeline capacity;
- final key memory, RSS, runtime, DFR, full Algorithm 5 correctness;
- novelty, end-to-end speedup, or a paper contribution.

```text
RESEARCH_FRONTIER_EXHAUSTED: false
PENDING_PI_DECISIONS: NONE
```
