# BOOT RMFE Chained-Frobenius Physical-Key-Switch Realization Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 1/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

Authoritative predecessor checkpoint read first:
`BBBINGW/memory main@e2bce55cad61755c6ddab1ee2bb7e96679da257e`.

The native task `BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01`
was not rerun. Accessible durable Git/Library snapshots still expose only the pre-completion
RUNNING/PENDING record, not the completed raw artifact/log/hash bundle. Therefore the
user-delivered summary (`PASS_BASELINE_RETAINED_SHARE_HEADROOM`, rho_ret median
0.06649923, 95% CI [0.06619683,0.06678483], 125 plaintext comparisons passed) remains
UNVERIFIED_BY_THIS_TURN pending raw provenance access.

This turn tests an independent question: are direct one-hop matrices for all Frobenius
targets j=1,2,3,4 necessary to realize the Turn-8 rank-5 joint recovery with four
physical key switches?

## Fixed algebra

Turn 8 established on the actual restricted post-RM10 domain:

[
(D_t\circ C2S)(x)=\sum_{j=0}^{4}\theta_{t,j}\sigma^j(x),\quad t=0,1,2,3.
]

All four outputs therefore use the same Frobenius orbit of one ciphertext.

## Exact HElib source audit

Pinned source: `homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1`.

Relevant locations:
- `src/keySwitching.cpp:297-304`: `KSGiantStepSize(D)=ceil(sqrt(D))`.
- `src/keySwitching.cpp:528-560`: BSGS generates baby j=1,...,g-1 and giant j=g,2g,...
- `src/keySwitching.cpp:598-618`: full and BSGS Frobenius helper wrappers.
- `src/keySwitching.cpp:620-663`: minimal Frobenius generation always creates j=1 and, for order>8, one giant-step matrix.
- `src/Ctxt.cpp:2462-2514`: each smartAutomorph path step is automorph + reLinearize; one physical KS per path step.
- `src/Ctxt.cpp:2526-2544`: BGV frobeniusAutomorph(j) invokes smartAutomorph(p^j mod m).
- `src/keys.cpp:115-165`: keySwitchMap is BFS over direct matrices.

For m=32768,p=5:
[
ord_m(5)=8192,\qquad g=\lceil\sqrt{8192}\rceil=91.
]

Standard Frobenius helper keysets:
- FULL/addFrbMatrices: direct j=1,...,8191; 8191 matrices.
- BSGS/default addSomeFrbMatrices for ord=8192/addBSGSFrbMatrices: direct j=1,...,90 and j=91,182,...; 180 matrices.
- MIN/addMinimalFrbMatrices: direct j=1 and j=91; 2 matrices.

Thus every standard helper contains the direct j=1 matrix
[
W[s(X^5)\to s(X)].
]

## Chained orbit schedule

Direct j=2,3,4 matrices are unnecessary:

```text
z = x
for t=0..3:
    out[t] = theta[t,0] * z

for j=1..4:
    z.frobeniusAutomorph(1)      # one direct p^1 key switch
    for t=0..3:
        out[t] += theta[t,j] * z
```

Successive z values are exactly sigma(x), sigma^2(x), sigma^3(x), sigma^4(x).
Keep z unmodified by applying public multipliers to temporary copies/accumulators.

Consequences:
- exactly 4 physical Frobenius key switches for the four nonidentity orbit images;
- only the direct j=1 Frobenius key type is sufficient;
- same 20 theta public-multiplier terms and same Turn-7/8 multiplier tax;
- no additional automorphism term.

Under MIN, four independent smartAutomorph calls on fresh copies have shortest hop counts
1,2,3,4 (10 total) with direct exponent steps {1,91}; the chained orbit reuses successive
states and reduces this to exactly 4.

## Key-storage consequence

All standard HElib Frobenius helper strategies need zero additional Frobenius matrices
for the chained schedule.

For an unknown/custom benchmark keyset that permits Frobenius reachability but lacks a
direct j=1 matrix, adding one direct
[
W[s(X^5)\to s(X)]
]
matrix is sufficient. Therefore candidate-specific augmentation is at most one direct
Frobenius matrix, not four. Exact byte size of that possible one-matrix augmentation is
not established statically.

Turn-25 public-benchmark provenance remains incomplete: zero additional key bytes for
Aung's exact unpublished key configuration is still not proven.

## Claim boundary

Permitted narrow claim:
The rank-5 joint R8 C2S+correction recovery can be realized with exactly four physical
Frobenius key switches by chaining four direct j=1 steps, provided the direct p^1 matrix
is present. All standard HElib Frobenius helpers at the pinned source provide it.

Still forbidden:
- `75 -> 19 physical key switches`;
- whole-pipeline physical-KS count;
- zero extra evaluation-key bytes for the exact Aung benchmark;
- acceptance of the unaudited R4 timing result.

The durable structural claim remains `75 -> 19 transform/automorphism terms`.

## Verdict

```text
RESULT:
  PASS_STATIC_CHAINED_FROBENIUS_FOUR_PHYSICAL_KS_REALIZATION

DIRECT_J2_TO_J4_REQUIRED:
  NO

SUFFICIENT_DIRECT_MATRIX:
  j=1 / X -> X^5

PHYSICAL_KS_FOR_J1_TO_J4_ORBIT:
  EXACTLY 4

STANDARD_HELIB_FULL_HAS_DIRECT_J1:
  YES
STANDARD_HELIB_BSGS_HAS_DIRECT_J1:
  YES
STANDARD_HELIB_MIN_HAS_DIRECT_J1:
  YES

STANDARD_HELIB_EXTRA_FROBENIUS_MATRICES_FOR_CHAIN:
  0

UNKNOWN_CUSTOM_KEYSET_SUFFICIENT_AUGMENTATION:
  +1 direct j=1 matrix

EXACT_EXTRA_BYTES_FOR_UNKNOWN_CUSTOM_KEYSET:
  UNRESOLVED

WHOLE_PIPELINE_75_TO_19_PHYSICAL_KS:
  NOT ESTABLISHED

R4_RESULT_AUDIT:
  BLOCKED ON MISSING RAW DURABLE PROVENANCE/ARTIFACT

CANDIDATE:
  SURVIVES / PHYSICAL-KS FEASIBILITY STRENGTHENED

WHOLE_PIPELINE_CAPACITY:
  UNRESOLVED
NATIVE_CANDIDATE_LATENCY:
  UNRESOLVED
PUBLISHABLE_NOVELTY:
  NOT ESTABLISHED
```
