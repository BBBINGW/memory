# BOOT-B159 — independent native artifact audit

Date: 2026-10-28
TRACK_ID: BOOT
Artifact: BOOT-B159-B158-COPACKED-EVALPOWER-NATIVE-20261028.zip
SHA-256: 0ca50f807411790ff5da5ea57d0edca61dffc5d22e8a66abd997bca5963a77e3

## Artifact integrity

Independent audit:
- outer ZIP SHA-256 matches the reported digest
- every entry listed in SHA256SUMS.txt verifies
- exact baseline/candidate source, commands, logs, go.mod/go.sum, environment,
  task spec, and report are present

No Codex/server/GPU execution was launched by this audit.

## Pinned implementation

- upstream: xiaopeng-stu/bfv-functional-bootstrapping
- commit: b113742d83d772fd0d1b353e72ac6e31f2838bea
- Go 1.25.0
- Lattigo v6.2.0
- host: Threadripper PRO 7975WX, 251 GiB RAM

Frozen 9-bit m=1 point:
- N=32768
- r=32768
- degree=65536
- T=65537
- p=512
- LogQ=[36, 34 x 18, 30]
- LogP=[34,34,34,34]
- LWE n=2048
- sparse ternary h=512

## Baseline

Source-faithful baseline:
- 5/5 runs correct
- median online = 2.609731116 s
- median Step1 = 0.913491810 s
- median Step2 = 1.598660784 s
- median Step3 = 0.095902826 s
- mean BuildBasis = 1.437466600 s
- max final |error| = 10
- max RSS ~=1.934 GiB

## Candidate operation count

The candidate implementation faithfully realizes the intended B158 recurrence:
- 15 ct-ct multiplications
- 15 relinearizations
- 15 rescales
- 14 RowRotations
- first k=1 transition uses zero RowRotation
- 31 ct-pt selector multiplications
- 30 additions

The supporting smoke path reached:
- input L18
- basis L3
- auxiliary L4
and printed the exact 15/14 operation count.

Its final output was incorrect, so the smoke timing is diagnostic only and is
not a valid speedup result.

## Mandatory deterministic stage gate

For native phase x=1:

k=1:
- level L18 / logQ 649
- 0/32768 slot mismatches
- noise budget 608 bits
- required logQ 41 bits

k=2:
- level L17 / logQ 615
- 0/32768 slot mismatches
- noise budget 562 bits
- required logQ 53 bits

k=4:
- level L16 / logQ 581
- 32768/32768 slot mismatches
- max centered slot difference 32768
- noise budget -16 bits
- required logQ 597 bits

Thus the failure is not a layout/algebra mismatch visible before noise
exhaustion. The exact recurrence is correct through k=2; k=4 crosses the native
coefficient-noise limit.

Decision:
- B159_STATUS = FAIL_NOISE
- B159_ALGEBRA_NATIVE_EARLY_STAGES = PASS
- B159_PERFORMANCE = NOT_RUN by design

## Attribution

The candidate uses scale-one selector plaintexts and deliberately does not
rescale after selector ct-pt products. This preserves the one-level-per-doubling
schedule, but the selector plaintext polynomials have large coefficient-domain
norms. The factor ciphertext therefore becomes noisy before the next fused
ct-ct multiplication, and standard tensoring catastrophically amplifies the
noise by k=4.

This is consistent with the prior B158 selector-norm prescout.

The source-faithful 2026/975 MonomialGen does NOT use this schedule: each
binary-mask ct-pt multiplication is followed by Rescale before multiplying the
factor into the accumulator.

Therefore B159 establishes:

FAIL for the specific realization:
  scale-1/no-rescale selectors + regular ct-ct tensoring

It does NOT prove an impossibility for the B158 algebraic recurrence under all
BFV multiplication variants.

## Track decision

- B158_ALGEBRA = PASS
- B158_OPTIMAL_CTCT_COUNT = PASS
- B158_STANDARD_TENSORING_REALIZATION = PARK / FAIL_NOISE
- do not add Q primes, increase N, or weaken security to rescue B159
- do not benchmark the incorrect path

A rescue is worth considering only if it changes the multiplication/noise
mechanism rather than merely increasing modulus headroom.
