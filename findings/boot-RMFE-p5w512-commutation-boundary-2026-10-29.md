# BOOT RMFE p=5, w=512 Commutation-Boundary Gate

Date: 2026-10-29  
Session: 密码学 11.0, Research Turn 16/25  
Classification: `FAIL_EXACT_FULL_PATH_COMMUTATION`

## Scope

This gate tested the proposed proof that five split-thin RMFE paths could be aggregated into one restricted R8 envelope and commute exactly through the complete HElib boot-key middle path. It corrected the source ordering and separated the linear boot-key operation from the nonlinear representative-selection and rounding operations around it.

No key generation, encryption, ciphertext evaluation, `rawModSwitch` execution, DFR, timing benchmark, or parameter sweep occurred in this research turn.

## Result

```text
PRIMARY_RESULT: FAIL_EXACT_FULL_PATH_COMMUTATION
PASS_STATIC_PAPER_CONFORMING_INSTANCE_CONSTRUCTIBILITY
PASS_STATIC_RESTRICTED_RANK5_ADAPTER
PASS_STATIC_POST_RAW_BOOTKEY_LINEARITY
FAIL_FULL_GPRIME_TO_E8_EMBEDDING
FAIL_ORDERED_INTERFACE_AS_PREVIOUSLY_WRITTEN
CORRECTED_PIPELINE_ALGEBRA: PASS
STANDALONE_AGGREGATE_CORRECTNESS: UNCLEAR_NOT_KILLED
WHOLE_FIXEDQ_CAPACITY: UNCLEAR
VALIDATED_CANDIDATE: NONE
```

## Source-order correction

The actual HElib order is:

```text
S2C
-> relinearize
-> rawModSwitch
-> newMakeDivisible
-> boot-key multiply/add
-> C2S
```

It is not `rawModSwitch -> S2C`, as the prior interface statement assumed.

For fixed raw-switched inputs, the boot-key operation

```text
BK(z0,z1) = z1*K + z0
```

is outer-ring linear and can commute with R8 aggregation. The complete preceding path cannot be proven by this argument because `rawModSwitch` and `newMakeDivisible` use coefficientwise rounding and balanced-representative selection.

A source-level recurrence counterexample is:

```text
ptxtSpace = 5
q = 26
Q = 101

raw(1) = 1
raw(3) = 3
raw(4) = -1
```

Thus `raw(1+3) != raw(1)+raw(3)` in the chosen representative system. The following division-by-five representative step also differs (`5` versus `6`). The exact split-path commutation proof is therefore killed.

## Preserved algebraic facts

For

```text
S = Z/625Z
k = 5
w = 512
eta = 125
```

the degree condition holds:

```text
eta*(k-1) = 500 < 512.
```

With evaluation points `0,1,2,3,4`, the Vandermonde determinant is `288`, a unit modulo 625. A new paper-conforming RMFE instance is therefore statically constructible.

A full `GR(625,512)` object cannot inject into rank-eight `GR(625,8)`. The only admissible adapter is a restricted rank-five linear map on `V = im(phi)`. No full subring embedding or ring-homomorphism claim is allowed.

## Killed and retained claims

Killed or parked:

- exact five-split-path commutation proof through the full middle path;
- full `G' -> E8` embedding claim;
- the previously written `rawModSwitch-before-S2C` interface.

Retained conditionally:

- a standalone RMFE aggregate construction with a corrected proof boundary;
- the exact R8 map and six-key-switch schedule;
- the linearity of the post-raw boot-key multiply/add stage.

The retained aggregate construction is not validated and has no established fixed-Q capacity, native correctness, DFR, runtime, memory advantage, novelty, or paper contribution.

## Next cheapest decisive test

The bounded plaintext-algebra task

```text
BOOT-RMFE-P5W512-DETERMINISTIC-INSTANCE-MASK-GENERATOR-20261029-R16-01
```

was delegated to Codex to generate one deterministic, hashable p=5, w=512 instance, its five exact trace-dual projection constants, and the restricted rank-five R8 adapter. It must stop before key generation or ciphertext work and must not use the incompatible `subring_bts` patch.

```text
AI_PROVISIONAL_CHOICE: RETAIN_RMFE_PROVISIONAL_WITH_CORRECTED_PROOF_BOUNDARY
INDEPENDENT_RESEARCH_AVAILABLE: true
RESEARCH_FRONTIER_EXHAUSTED: false
```
