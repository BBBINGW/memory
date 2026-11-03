# BOOT / B158 — Successor Research Turn 15 — exact canonical runtime-certificate route past the Turn-14 coefficient-L1 floor

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: rmfe-subring-envelope-single-multkey-v1
PHASE: CORRECTNESS_GATE

BACKGROUND_NATIVE_TASK:
    BOOT-T11-R8-SMALL-CANARY-20261103-R2

BACKGROUND_TASK_STATUS:
    PENDING / RESULT UNKNOWN / DO_NOT_RERUN / UNTOUCHED

## Read-before-write / authority

GitHub Notes read of the Turn-14 predecessor was attempted first and remained degraded.
The exact durable predecessor was recovered through Git at:

    findings/boot-successor-turn14-algorithm4-u0-three-Fe-certificate-capacity-no-go-2026-11-03.md
    commit 52ac37783eadf276a8a8883a0323cea55bf1572a
    blob 4d59eef904a020bd2d8be209390e938c95d35b68.

The target Turn-15 path was checked absent before write.

The background R2 source/workdir/binary/result were not read, modified, resubmitted, inferred, or duplicated.
No native task was launched.

Pinned HElib:
    homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1.

Pinned source blobs inspected:
    src/Ctxt.cpp       b346fcd52ddf6bd5c778a918865cc6bb5143787f
    src/DoubleCRT.cpp  e356d6d731af7df74f6c6d99629edf5f4804d5f9
    src/sample.cpp     53ad368110db547db194469adb5fbc5c56570588
    src/keys.cpp       7d3a2dfd3706704edfbddacd556ea44615e959a1
    include/helib/Ctxt.h    da4be8176cc074a409afbace647b16fac47642c8
    include/helib/Context.h 1723b43108101c2bc25c6ba582decf1236e7d0f0.

## Why this turn is paper-level

Turn 14 proves that the existing deterministic total-raw coefficient-L1 proof architecture cannot close all three
u_0 lifting-polynomial evaluations under the R2 h=120 profile.

That result does NOT prove actual ciphertext failure. It isolates the generic coefficientwise modulus-switch rounding
floor as the proof bottleneck.

The highest-information independent next question is therefore:

    Can pinned HElib's canonical-embedding machinery provide a genuinely different, source-compatible,
    auditable correctness certificate that does not assume uniformly independent rounding coefficients?

This turn audits only that route.

No prefix/residue/K-factor tuning of the Turn-14 L1 proof is repeated.

## Closest prior / exact delta

Closest implementation prior is pinned HElib's own BGV noise bookkeeping.

The important distinction is between:

1. modSwitchAddedNoiseBound():
   a heuristic/high-probability estimator used for target-size policy and statistics;

2. the actual real modDownToSet update:
   source computes the exact canonical norm of THIS operation's realized normalized rounding polynomials
   and uses those values to update noiseBound.

Turn 15's delta is to separate these two mechanisms and derive a parallel correctness-certificate contract from
the second one.

No novelty-clear claim is made.

## Primary hypothesis

H15:
Starting from the current Turn-13 certified Algorithm-4 entry envelope, the nonlinear candidate can be audited in
canonical-embedding norm using actual per-operation source quantities:

- actual mod-switch rounding canonical norms;
- bounded secret-key canonical norm;
- actual digit canonical norms in key switching;
- bounded key-switch RLWE error norm;
- canonical submultiplicativity under ciphertext multiplication.

This removes Turn 14's generic coefficient-L1 rounding floor as a fundamental proof obstruction.

Falsifier:
- real modDownToSet actually updates noise with the heuristic noiseBoundForUniform rather than actual rounding norms;
- secret/key-switch bounds are only heuristic and not enforced by sampling;
- breakIntoDigits uses only a distributional estimate;
- or multiplication/addition/divide semantics cannot be mirrored by a canonical norm certificate.

## 1. HElib's policy estimator is heuristic

Pinned Ctxt::modSwitchAddedNoiseBound computes:

    roundingNoise
      = context.noiseBoundForUniform(ptxtSpace/2, phi(m))

and multiplies this by a secret-key-size factor.

Pinned Context::noiseBoundForUniform explicitly documents:

- it assumes coefficients are uniformly and independently distributed;
- it approximates evaluations at roots of unity as normal random variables;
- this is "a bit heuristic".

Therefore:

    modSwitchAddedNoiseBound()

is NOT suitable as a formal deterministic theorem for repeated F4 correctness.

However, this estimator is not the authoritative noise update of real modulus switching.

## 2. Real modDownToSet computes the realized rounding norm

Pinned Ctxt::modDownToSet real-BGV path calls, for every ciphertext part:

    part.scaleDownToSet(intersection, ptxtSpace, delta).

The source then forms the normalized rounding polynomial:

    fdelta[j] = delta[j] / droppedPrimeProduct.

It enforces:

    |fdelta[j]| <= ptxtSpace/2 + tolerance.

Then, crucially, source computes:

    norm_i
      = embeddingLargestCoeff(fdelta_i, ZMStar)

for the ACTUAL fdelta_i produced by this ciphertext and this target set.

The actual added decryption-noise certificate is:

    addedNoise
      = sum_i norm_i * skBound(key_i)^(secretPower_i),

with the handle-one part contributing norm_i directly.

Finally source updates:

    noiseBound /= droppedPrimeProduct;
    noiseBound += addedNoise.

Thus the actual source update has the exact algebraic form:

    C_new
      <= C_old / F
         + Delta_actual,

where:

    Delta_actual
      = sum_i ||fdelta_i||_can * S_i^(d_i).

The uniform/normal approximation is used only to compute:

    addedNoiseBound

for policy/statistical comparison.

The source even records:

    ratio = addedNoise / addedNoiseBound

after the actual update.

This is the central Turn-15 result.

## 3. Secret-key canonical bound is enforced, not merely predicted

Pinned SecKey::GenSecKey for hwt>0 uses:

    sampleHWtBounded(hwt).

For h=120:

    bound_s
      = sqrt(h * ln(phi(m))).

sampleHWtBounded repeatedly samples the secret and computes:

    embeddingLargestCoeff(secret)

until:

    actual_norm <= bound_s,

or throws after 1000 failed attempts.

Only after this check does key generation import the secret and store:

    skBounds.push_back(bound_s).

Therefore, conditional on successful honest key generation:

    ||s||_can <= getSKeyBound(0)

is source-enforced.

For:

    h=120,
    phi(m)=16384,

the stored deterministic post-sampling bound is:

    S_120
      = sqrt(120*ln(16384))
      = 34.12458444202227.

This is qualitatively different from Turn 14's coefficient-L1 secret bound h=120.

## 4. Key-switch RLWE error bounds are also rejection-enforced

Pinned GenKeySWmatrix constructs each matrix column with:

    RLWE1(...).

RLWE1 samples its error using:

    sampleGaussianBounded(stdev).

sampleGaussianBounded computes:

    bound_e
      = stdev * sqrt(phi(m)*ln(phi(m)))

for the power-of-two case and repeatedly samples until:

    embeddingLargestCoeff(error) <= bound_e,

or throws.

RLWE1 then multiplies by the BGV plaintext-space factor p where applicable and returns that bound.

The returned value is stored as:

    KeySwitch::noiseBound.

Hence, conditional on successful honest key generation, W.noiseBound bounds the actual canonical embedding norm of
the key-switch RLWE error used by that matrix.

Again, the sampling distribution motivates the rejection threshold, but after successful rejection the returned
inequality is checked on the actual sampled polynomial.

## 5. breakIntoDigits uses realized digit norms

Pinned DoubleCRT::breakIntoDigits contains an inactive #if 0 branch for the high-probability uniform estimate.

The ACTIVE branch instead reconstructs each actual digit polynomial and computes:

    norm_val
      = embeddingLargestCoeff(actual_digit_poly, ZMStar).

It accumulates:

    digitNormSum
      = sum_i norm_val_i.

Pinned Ctxt::keySwitchPart then computes:

    addedNoise_KS
      = digitNormSum * W.noiseBound

and adds this amount to noiseBound.

Thus the active key-switch update is source-shaped as:

    C_after_KS
      <= C_before_KS_scaled
         + sum_i ||digit_i||_can * ||e_W||_can.

No independent-uniform digit model is needed in the active path.

## 6. Canonical embedding is naturally compatible with multiplication

For the cyclotomic canonical embedding sigma:

    sigma(fg) = sigma(f) * sigma(g)

coordinatewise.

Therefore:

    ||fg||_{can,infty}
      <= ||f||_{can,infty}
         ||g||_{can,infty}.

Pinned BGV tensorProduct mirrors this:

    noiseBound_out
      = noiseBound_1 * noiseBound_2.

This is an exact norm inequality, not a coefficient-convolution overestimate.

For addition/subtraction with matched representation:

    ||f +/- g||_can
      <= ||f||_can + ||g||_can.

Pinned factor harmonization multiplies ciphertext parts and noiseBound by the balanced public unit magnitude.
Explicit factor alignment can therefore be audited canonically as well.

Pinned divideByP performs:

    noiseBound /= p,

matching the source semantic quotient once Aung divisibility holds.

Automorphisms preserve canonical L-infinity norm.

Public polynomial multiplication via the ZZX path computes:

    embeddingLargestCoeff(public_poly)

and multiplies noiseBound by that canonical norm.

Thus every Algorithm-4 operation has a canonical-certificate counterpart.

## 7. A rigorous parallel certificate should not blindly trust floating noiseBound

Pinned HElib evaluates embeddingLargestCoeff numerically in floating point.

The source does not provide an outward-rounding proof that every returned double is a mathematical upper bound.

Therefore the strongest paper-level statement is NOT:

    "HElib noiseBound is formally exact."

The correct contract is:

    replicate the same source quantities in a PARALLEL certified-canonical ledger,
    with interval/upward-rounded canonical norm evaluation for every fdelta/digit/public polynomial.

This is a small audit/instrumentation requirement, not a new cryptographic mechanism.

The candidate correctness artifact should store:
- actual fdelta coefficient vectors or hashes plus certified canonical norms;
- actual digit polynomials/hashes plus certified norms;
- source-stored secret/key-switch sampling bounds;
- every certificate update;
- exact prime sets and factors.

## 8. Deterministic power-of-two fallback bound

Even without using actual fdelta values, the power-of-two ring gives a strictly tighter deterministic canonical
rounding bound than Turn 14's coefficient-L1 bound.

Let:

    n = phi(m)=16384
    m=2n=32768
    B=625/2=312.5.

For any real coefficient vector:

    f(X)=sum_{j=0}^{n-1} a_j X^j,
    |a_j|<=B,

and any primitive m-th root zeta, choose the phase of f(zeta).
Then:

    |f(zeta)|
      <= B * max_phi sum_j |cos(pi*j/n - phi)|.

For even n:

    max_phi sum_j |cos(pi*j/n - phi)|
      = csc(pi/(2n)).

Multiplication by any odd primitive-root exponent only permutes the antipodal direction pairs, so the same bound
holds for every primitive m-th root.

Therefore:

    ||f||_can
      <= B * csc(pi/(2n)).

For n=16384:

    C_n
      = csc(pi/32768)
      = 10430.378366449419.

Hence one normalized rounding polynomial satisfies:

    ||fdelta||_can
      <= 3,259,493.2395154433.

For a canonical two-part ciphertext with the rejection-enforced secret bound S_120:

    Delta_det_can
      <= B*C_n*(1+S_120)
      = 114,488,345.52956091.

Log:

    log2(Delta_det_can)
      = 26.77062550412444.

Turn 14's coefficient-L1 generic floor was:

    R_L1 =619,520,000
    log2(R_L1)=29.206575616824043.

Thus the deterministic canonical fallback already saves:

    log2(R_L1/Delta_det_can)
      ~=2.43595 bits

per modulus-switch floor.

## 9. Turn-14 necessary no-go is removed by the canonical fallback

Turn 14 proved for a degree-5 certificate architecture:

    d_after_one_Fe
      <= d_before_Fe -4r

as a NECESSARY limitation when the per-modswitch floor is R=2^r.

For the three u0 Fe calls, a necessary condition is:

    d0 > 12r + log2(1/0.48).

Using Turn-13:

    log2(E_L0)
      <=75.12833994098358.

Using only the source lower bound:

    log2(Q0)>=399.5,

gives:

    d0>=324.37166005901645.

With the deterministic canonical fallback:

    12*26.77062550412444 + log2(1/0.48)
      =322.3063997385468.

So the Turn-14 necessary impossibility disappears, with:

    2.0652603204696334 bits

of necessary-condition headroom even at the minimum source Q floor.

This is NOT yet a sufficient complete-Fe proof.

It proves that the previous no-go is specific to coefficient-L1/generic rounding and cannot be transferred to
canonical norm.

## 10. Conservative complete-F4 recurrence and source-Q threshold

Reuse the existing source-shaped degree-5 certificate recurrence with canonical quantities:

    A = inherited_scaled + R
    E2 = A^2 + K
    E3 = A*(E2+1872) + K
    E4 = E3 +312*(A+312)
    EF = E4*E2 + K +312*(E2+5*312*A).

Use the existing conservative:

    K <=401,679,183,790,909.

For a fixed rounding floor R, optimize the output certified capacity over all continuous target moduli.
Equivalently, with:

    x = log2(inherited_scaled),

the one-Fe capacity loss is:

    L(R)
      = min_x [
          log2(EF(2^x+R)) - x
        ].

For:

    R=Delta_det_can=114,488,345.52956091,

numerical minimization gives:

    optimal x
      =24.798431911058277

    L(R)
      =110.74797054066967 bits.

Thus three Fe calls require:

    log2(Q0)
      >
      log2(E_L0)
      +3*L(R)
      +log2(1/0.48)

      =408.4311452520461 bits.

Pinned bits=400 source gives:

    399.5 <= log2(Q0) <420

from the previous source audit.

Therefore:

- the deterministic canonical fallback can close the full u0 three-Fe recurrence for sufficiently large actual Q0;
- but the paper/pinned bits value alone does NOT source-guarantee it.

This becomes an exact Step-3/Step-5 serialized-profile predicate:

    log2(Q0) >408.4311452520461

is sufficient under the conservative canonical fallback and existing K/constants.

## 11. Exact runtime rounding can rescue smaller Q0

The deterministic fallback above ignores the actual fdelta values even though source computes them.

At the minimum source floor:

    log2(Q0)=399.5,

the entry capacity is:

    d0=324.37166005901645.

For the same complete-F4 recurrence, the maximum constant rounding floor that permits three optimized Fe calls satisfies:

    L(R_crit)
      = (d0-log2(1/0.48))/3.

Solving gives:

    R_crit
      =67,143,366.1530421

with:

    log2(R_crit)
      =26.00074153086519.

Therefore, even at the minimum allowed Q0:

if the actual certified canonical rounding contribution before each u0 Fe can be held at or below approximately:

    67.14 million,

the complete three-Fe capacity recurrence has a viable certified route under the same conservative K/constants.

For context only, NOT as a theorem:

pinned modSwitchAddedNoiseBound's scale=10 heuristic comparator at h=120 is approximately:

    8,111,675.313110119
    log2=22.951568475913383,

which is about:

    8.277x

below R_crit.

This does NOT establish DFR or independence.
It only shows why measuring the ACTUAL source fdelta norms is scientifically decisive rather than cosmetic.

## 12. Runtime certificate contract

After mandatory evidence Steps 2 and 3 permit complete candidate correctness work, the Algorithm-4 candidate run
should maintain a parallel canonical certificate C.

### Entry

For each L_r:

    C(L_r)
      <= existing Turn-13 coefficient-L1 envelope E_Lr,

because coefficient-L1 upper-bounds canonical L-infinity.

### Real mod-down

For every candidate target set:
- use a copy or instrument the source path;
- materialize the actual normalized fdelta for every part;
- compute an upward-certified canonical norm;
- use stored public skBounds.

Update:

    C_new
      = C_old/F
        + sum_i ||fdelta_i||_can_cert * S_i^(d_i).

Do not use noiseBoundForUniform in the certificate.

### Ciphertext multiplication

At the common target:

    C_tensor <= C1*C2.

### Relinearization / key switch

Use:
- actual breakIntoDigits digit polynomials;
- upward-certified digit canonical norms;
- source KeySwitch::noiseBound values from bounded RLWE sampling.

Charge:

    Delta_KS
      = sum_digit_norms * W.noiseBound.

After special-prime cleanup, apply the same actual mod-down certificate rule.

### Public constants / factor alignment

Use exact/upward canonical norms of public polynomials and balanced public-unit magnitudes.

### Addition/subtraction

After explicit factor/prime-set alignment:

    C_sum <= C1+C2.

### divideByP

Once Aung semantic divisibility is independently asserted:

    C_after <= C_before/5.

### Acceptance

At every named node require:

    C_node * polyNormBnd <0.48*Q_node.

For m=32768 the exact serialized polyNormBnd must be recorded; no implicit value is assumed in the final artifact.

## 13. Scientific classification

Turn 15 establishes a credible correctness route beyond the Turn-14 coefficient-L1 obstruction.

It does NOT establish:
- that the pending R2 task passes;
- that actual Algorithm-4 fdelta norms satisfy R_crit;
- complete candidate correctness;
- a rigorous DFR over all encryption/key randomness;
- matched performance.

The route is deterministic for a realized honest key/ciphertext trace once all actual canonical norms are certified.

Distributional DFR remains a separate Step-6 obligation.

If the implementation elects to use the certificate as a runtime guard with fallback/abort, the correctness theorem can be unconditional for non-aborting traces; availability/fallback rate is then a value/DFR question.

No such production fallback mechanism is adopted in this turn.

## Verdict

PASS_SOURCE_REAL_MODDOWN_USES_ACTUAL_CANONICAL_ROUNDING_NORMS.
PASS_BOUNDED_SECRET_CANONICAL_NORM_ENFORCEMENT.
PASS_BOUNDED_KSWITCH_RLWE_CANONICAL_NORM_ENFORCEMENT.
PASS_BREAKINTODIGITS_ACTUAL_CANONICAL_NORM_PATH.
PASS_PARALLEL_EXACT_CANONICAL_RUNTIME_CERTIFICATE_ROUTE.

PASS_DETERMINISTIC_POWER2_CANONICAL_ROUNDING_BOUND.
PASS_TURN14_NECESSARY_NO_GO_DOES_NOT_TRANSFER_TO_CANONICAL_NORM.

CONSERVATIVE_CANONICAL_STATIC_Q0_THRESHOLD_BITS:
    408.4311452520461.

MIN_Q0_RUNTIME_ROUNDING_CRIT:
    Delta_actual <=67,143,366.1530421
    is sufficient under the stated conservative three-Fe recurrence if achieved at each u0 Fe target.

FAIL_COMPLETE_STATIC_CANONICAL_CLOSURE_FROM_BITS400_ALONE:
    paper/source only gives Q0 lower floor399.5, not the >408.431 sufficient threshold.

NATIVE_STEP2_RESULT:
    UNKNOWN / PENDING.

CORRECTNESS_GATE:
    BLOCKED.

BASELINE_CORRECTNESS:
    PENDING.

SECURITY_GATE:
    PENDING.

VALUE_GATE:
    PENDING.

AUDIT_GATE:
    PENDING.

NOVELTY_STATUS:
    PREFLIGHT.

PAPER_READINESS:
    NOT_READY.

## Next action while R2 remains pending

Do not modify, duplicate, or resubmit the background R2 task.

If R2 becomes ready, independently audit its raw artifacts immediately.

Otherwise the next side-research unit should not return to coefficient-L1 prefix tuning.
The highest-value independent options are:
- formalize the exact-canonical runtime certificate into a complete six-boundary Algorithm-4 acceptance oracle; or
- perform a bounded novelty/prior-art audit of the sparse-R8 + shared-four-output mechanism.

No benchmark.
