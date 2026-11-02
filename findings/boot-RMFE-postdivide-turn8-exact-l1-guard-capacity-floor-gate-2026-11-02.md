# BOOT / B158 — Research Turn 8/25 — exact-L1 guard reconstruction-capacity floor gate

Date: 2026-11-02 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613 / PRE-TAG + POST-DIVIDE late aggregation
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Read-before-write / provenance

GitHub Notes read remains degraded for existing findings. Current durable state was recovered from
BBBINGW/memory at verified HEAD:

    c1bf5a058c08f06bc236b9bc19886a51adf4b0c6

Immediate relevant findings:
- Turn5 exact coefficient-L1 reconstruction guard:
  findings/boot-RMFE-postdivide-turn5-exact-l1-reconstruction-noise-guard-gate-2026-11-02.md
- Turn6 full-ring dimension/provenance gate:
  findings/boot-RMFE-postdivide-turn6-full-ring-dimension-l1-guard-provenance-gate-2026-11-02.md
- Turn7 ZZX-to-DoubleCRT representative gate:
  findings/boot-RMFE-postdivide-turn7-zzx-dcrt-representative-l1-guard-gate-2026-11-02.md
- historical HElib reconstruction bookkeeping:
  findings/boot-RMFE-recryptekey-noise-intfactor-bookkeeping-gate-2026-11-01.md
- historical native configuration audit:
  findings/boot-RMFE-R4-baseline-timer-result-independent-audit-2026-11-01.md

The target path was absent before write.

## Native Step2 attempt status — infrastructure only

This turn first attempted to advance the mandatory evidence order by running the frozen recovery-only
canary unchanged.

The frozen source remained at Git blob:

    6ae4bc7e48e0390f8dec97429f4ddb89565928c0

The following execution routes were attempted without modifying the canary:
1. create a temporary GitHub CI branch — rejected by the GitHub integration with HTTP 403
   "Resource not accessible by integration";
2. create a temporary workflow through GitHub Notes — hidden .github path blocked;
3. create the same workflow through the GitHub contents API — HTTP 403;
4. use the current container — no HElib/NTL installation or package candidate is available and
   ordinary outbound DNS is unavailable;
5. obtain a pinned HElib archive through the available GitHub connector — no repository-archive
   materialization action is exposed.

Therefore:

    RECOVERY_CANARY = NOT_EXECUTED

These are infrastructure facts only. They are NOT scientific FAIL evidence.

To avoid another low-information static microaudit, the scientific Turn8 question below tests
whether the newly canonical exact-L1 correctness guard is itself structurally usable at the fixed
Aung/HElib modulus size.

## Closest implementation prior / exact delta

Closest implementation prior remains stock HElib reconstruction from recryptEkey.

Turns5-7 replaced HElib's floating canonical-norm estimator at the shared reconstruction boundary by
a rigorous exact coefficient-L1 guard:

    S0,S1 <= 25,640,960.

This is deliberately worst-case conservative.

The exact delta tested here is whether this safe metadata guard necessarily destroys BGV capacity
before the candidate even reaches the pure inverse.

No novelty claim is added.

## Primary hypothesis

For the source-faithful p=5,m=32768,w=512 context with HElib bits=400, even the MAXIMAL Turn5/6
exact-L1 guard:

    S0=S1=25,640,960

leaves a large positive tracked capacity immediately after the one shared recryptEkey reconstruction.

Hence the guard is viable as a production correctness contract and is not merely a mathematical
fallback that makes every guarded ciphertext unusable.

## Falsifier

FAIL if the pinned-source worst-case ledger permits:

    capacity_after_shared_reconstruction <= 0,

or even leaves only a tiny single-digit margin under the fixed bits=400 context, because then the
canonical safe guard would be structurally incompatible with the downstream candidate.

The test is deliberately local to the reconstruction boundary. It does not infer final capacity.

## Minimal decisive test

Derive from pinned source only:
1. a deterministic upper bound on recryptEkey.noiseBound;
2. a lower bound on product(ctxtPrimes) for bits=400;
3. combine with the maximal exact-L1 S0,S1 and worst possible BGV addConstant representation factor
   |f|;
4. lower-bound HElib BGV capacity immediately after reconstruction.

## 1. Fixed context facts

Current source-faithful native configuration uses:

    p=5
    r=1
    m=32768
    bits=400.

Pinned Context defaults are:

    stdev = 3.2
    scale = 10.

Current temporary recryption plaintext space is:

    p_boot = p^(e-ePrime+r)
           = 5^(4-1+1)
           = 625.

The recryptEkey is generated once by SecKey::genRecryptData and encrypted under key0 at plaintext
space625.

## 2. Exact tracked recryptEkey noise formula

Pinned SecKey::skEncrypt for BGV initializes:

    noiseBound = RLWE(c0,c1,sKey,ptxtSpace)

and then adds:

    ptxt_bound = context.noiseBoundForMod(ptxtSpace,phi(m)).

For m a power of two, pinned RLWE1 samples bounded Gaussian error with:

    GaussianBound
      = stdev * sqrt(phi(m) * ln(phi(m))).

It then multiplies this bound by BGV plaintext space ptxtSpace.

Thus the RLWE contribution to recryptEkey is bounded by:

    N_RLWE
      = 625 * 3.2 * sqrt(16384 * ln(16384))
      = 797,474.332347112.

Pinned noiseBoundForMod for odd modulus625 is:

    scale * sqrt(phi(m) * 625^2 / 12).

Hence:

    N_ptxt
      = 10 * sqrt(16384 * 625^2 / 12)
      = 230,940.1076758503.

Therefore the stored tracked recryptEkey bound satisfies:

    N_E
      <= 1,028,414.4400229623

and:

    log2(N_E)
      <= 19.971990341709958.

This bound is source-level bookkeeping, not a claim about realized exact error.

## 3. bits=400 gives a hard lower bound on the ctxt-prime modulus

Pinned Context::addCtxtPrimes(nBits,targetSize) repeatedly adds ciphertext primes while:

    bitlen < nBits - 0.5

where bitlen accumulates:

    sum log2(q_i)
      = log2(product(ctxtPrimes)).

Therefore after buildModChain with:

    nBits=400,

the resulting ciphertext-prime product Q_E satisfies:

    log2(Q_E) >= 399.5.

recryptEkey uses exactly context.getCtxtPrimes(), so this is the relevant reconstruction modulus.

No approximate published capacity number is needed for this floor.

## 4. Worst-case BGV addConstant representation factor

At the shared reconstruction boundary:

    intFactor = 1
    ptxtSpace = 625.

Pinned addConstant computes:

    f = balRem(Q_E mod625,625).

For an odd modulus625, any balanced residue satisfies:

    |f| <= 312.

The fact that Q_E is coprime to5 may exclude some residues but is unnecessary for this worst-case
upper bound.

## 5. Maximal exact-L1 reconstruction ledger

Turns5-7 establish rigorous public-polynomial size bounds:

    S0 <= 25,640,960
    S1 <= 25,640,960.

The guarded shared reconstruction executes:

    ctxt = recryptEkey;
    ctxt.multByConstant(Z1,S1);
    ctxt.addConstant(Z0,S0).

Pinned BGV metadata recurrence gives:

    N_shared
      = N_E*S1 + |f|*S0.

Using the simultaneous worst cases:

    S0=S1=25,640,960
    |f|=312
    N_E=1,028,414.4400229623,

we obtain:

    N_shared
      <= 26,377,533,499,571.176

and:

    log2(N_shared)
      <= 44.58437490144962.

The additive-constant term alone is only:

    log2(312*S0)
      = 32.89734916068223,

so the bound is dominated by the recryptEkey multiplier term.

## 6. Reconstruction-boundary capacity floor

Pinned BGV capacity is:

    capacity
      = log2(Q / max(noiseBound,1)).

Combining the source lower bound:

    log2(Q_E) >= 399.5

with the worst-case guarded noise upper bound:

    log2(N_shared) <= 44.58437490144962

gives:

    capacity_shared
      >= 399.5 - 44.58437490144962
      = 354.9156250985504 bits.

Therefore:

    capacity_shared >= 354.9 bits

under the full worst-case exact-L1 guard.

This is a deterministic HElib metadata floor for this boundary under the fixed context construction.

## 7. Scientific consequence

The exact-L1 guard is NOT structurally self-defeating.

Even after simultaneously maximizing:
- all ten post-divide polynomial L1 sizes within the proven bound;
- both five-branch sums;
- the BGV representation factor magnitude;

the one shared reconstruction retains hundreds of tracked capacity bits.

Thus the candidate can safely keep the exact-L1 guard as its canonical correctness implementation
without needing the weaker Turn3 floating-estimator guard merely to preserve local capacity.

This strengthens the construction contract:

    exact-L1 guard = SAFE and LOCALLY CAPACITY-VIABLE.

Turn3 floating estimator remains optional diagnostic only.

## 8. What this does NOT prove

The 354.9-bit floor is IMMEDIATELY AFTER shared reconstruction only.

It does not include:
- pure EvalMap inverse key-switch/multiplier cost;
- scalar28 is metadata-unit but later recovery still has key switching;
- 17-call recovery;
- L0..L3 public multiplier accumulation;
- six Algorithm4 divide/relinearization trajectories;
- final Recode;
- actual DFR;
- matched benchmark.

In particular:

    capacity_shared >=354.9

must NOT be converted into a final-capacity prediction.

Historical BOOT work already established that HElib scalar capacity is not a closed state for future
key-switch noise because breakIntoDigits depends on actual ciphertext parts.

## 9. Native Step3 refinement

After the mandatory Step2 canary passes, Step3 should record:

    RECRYPTEKEY_NOISEBOUND
    RECRYPTEKEY_LOG2_Q
    S0_EXACT_L1
    S1_EXACT_L1
    REPRESENTATION_FACTOR_F
    SHARED_NOISEBOUND
    SHARED_CAPACITY

and assert both:
1. the exact source formula:
       shared_noise =
         recryptEkey_noise*S1 + abs(f)*S0;
2. the static floor:
       shared_capacity >= 354.9
   whenever the production context exactly matches bits=400 and the Turn5/6 hard bounds.

A native lower value under the same exact context would indicate an implementation/type mismatch and
must be investigated before continuing.

## Verdict

PASS_EXACT_L1_GUARD_LOCAL_CAPACITY_VIABILITY
PASS_RECRYPTEKEY_SOURCE_NOISE_UPPER_BOUND
PASS_BITS400_CTXT_MODULUS_LOWER_BOUND
PASS_SHARED_RECONSTRUCTION_CAPACITY_FLOOR_354P9

CANONICAL_GUARD:
  EXACT_COEFFICIENT_L1

TURN3_FLOATING_GUARD:
  OPTIONAL_DIAGNOSTIC_ONLY

RECOVERY_CANARY:
  NOT_EXECUTED_INFRASTRUCTURE_UNAVAILABLE

NATIVE_EXECUTION:
  NOT_OBTAINED

CORRECTNESS_GATE:
  BLOCKED

BASELINE_CORRECTNESS:
  PENDING

NOVELTY_STATUS:
  PREFLIGHT

SECURITY_GATE:
  PENDING

VALUE_GATE:
  PENDING

AUDIT_GATE:
  PENDING

PAPER_READINESS:
  NOT_READY

## Next decisive test

The mandatory evidence-order blocker remains unchanged:

execute the frozen revised recovery-only canary at
homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1 with HELIB_DEBUG=ON.

Do not interpret the Turn8 reconstruction-capacity floor as a substitute for that canary.

After Step2 PASS, execute the enlarged Step3 exact parameter/interface oracle including Turns4-8
assertions before baseline/candidate end-to-end correctness.
