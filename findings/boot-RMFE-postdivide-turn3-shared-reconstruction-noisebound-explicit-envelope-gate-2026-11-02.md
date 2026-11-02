# BOOT / B158 — Research Turn 3/25 — shared-reconstruction explicit noise-envelope fallback gate

Date: 2026-11-02 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613 / PRE-TAG + POST-DIVIDE late aggregation
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Evidence-order / native status

The preferred Step-2 recovery-only canary was attempted first in this turn.

Infrastructure only:
- current container has no HElib/NTL;
- outbound GitHub access from the container is unavailable;
- the pinned HElib commit has no reusable historical GitHub Actions run/artifact exposed through the connected GitHub action interface.

These are NOT scientific evidence and are not counted as the substantive test.

The frozen canary remains NOT_EXECUTED.

## Read-before-write

GitHub Notes read calls remain degraded for existing content, so the current durable state was recovered from the same BBBINGW/memory repository:
- HEAD before this write: 745d51d5a45909a64b79035fb1afd09939d25159
- Turn-2 finding blob: b1163200476b979f920e7f207fa60aabca7f112f
- frozen canary blob: 6ae4bc7e48e0390f8dec97429f4ddb89565928c0

The new target path was checked before write and was absent.

Historical duplicate check: previous BOOT work proved exact ciphertext-part shared reconstruction and a mathematical conservative norm envelope, but explicitly left the software floating-estimator relation as a native assertion. No prior durable BOOT finding established the public-size envelope fallback below.

## Closest prior art / exact delta

Closest implementation prior remains stock HElib recryption at the pinned commit.

Stock reconstruction executes:

    ctxt = recryptEkey;
    ctxt.multByConstant(zzParts[1]);
    ctxt.addConstant(zzParts[0]);

with default size estimation for the ZZX constants.

The current candidate differs only because five exact post-divide branch pairs are summed first:

    Z1 = sum_i z1_i
    Z0 = sum_i z0_i

and then one reconstruction is executed.

This turn introduces NO novelty claim. It asks only whether a candidate-specific software-noise-estimator risk can be eliminated using existing public HElib interfaces.

## Primary hypothesis

Even if the default floating-point estimate

    embeddingLargestCoeff(sum_i z_i)

does not satisfy a bit-for-bit subadditivity relation against the sum of the five separately computed estimates, the CURRENT candidate can deterministically carry a noiseBound envelope at least as conservative as the five hypothetical stock branch reconstructions WITHOUT:
- constructing five reconstructed ciphertexts;
- mutating private Ctxt::noiseBound;
- changing ciphertext parts;
- changing ptxtSpace, intFactor, keyID, or primeSet.

The proposed fallback is to compute the five branchwise public constant-size estimates before summing the ZZX pairs, add them with upward rounding, and pass those totals through the existing public size arguments of multByConstant and addConstant.

## Falsifier

FAIL if any pinned-source fact below is false:
1. the ZZX multByConstant overload with explicit positive size bypasses the default size computation and uses the supplied value only to update noiseBound;
2. addConstant likewise accepts an explicit size and updates noiseBound linearly with it;
3. the five hypothetical reconstructed branches have the same ptxtSpace/intFactor/primeSet, so their addCtxt path does not introduce factor harmonization;
4. supplying explicit size changes the encrypted algebra rather than only the estimator metadata;
5. the resulting shared-envelope formula cannot dominate the sum of the five separate HElib envelopes.

## Minimal decisive test

Read only the relevant pinned HElib source formulas and derive the exact metadata recurrence for:
A. five separate hypothetical reconstructions followed by addition;
B. one shared reconstruction using explicit branch-summed size bounds.

No native timing, capacity, DFR, or performance inference is made.

## 1. Pinned source formulas

### 1.1 multByConstant(ZZX,size)

Pinned src/Ctxt.cpp:

    void Ctxt::multByConstant(const NTL::ZZX& poly, double size)
    {
      ...
      if (size < 0 && !isCKKS())
        size = conv<double>(embeddingLargestCoeff(poly,...));
      DoubleCRT dcrt(poly, context, primeSet);
      multByConstant(dcrt, size);
    }

The BGV DoubleCRT overload multiplies every ciphertext part by the supplied constant and then performs:

    noiseBound *= size;

Therefore an explicit nonnegative size bypasses the default embeddingLargestCoeff computation. The actual polynomial multiplier remains poly.

### 1.2 addConstant(ZZX,size)

Pinned src/Ctxt.cpp computes for BGV:

    f = balRem(intFactor * productOfPrimes(primeSet), ptxtSpace);
    noiseBound += size * abs(f);

then adds the actual DoubleCRT constant to the part pointing to one.

The ZZX overload computes embeddingLargestCoeff only when size<0; otherwise the supplied size is forwarded.

Thus explicit size affects the software noise estimate but does not replace the plaintext polynomial being added.

### 1.3 addCtxt

For BGV, addCtxt harmonizes integer factors only if:

    intFactor != other.intFactor.

After part-wise addition it performs:

    noiseBound += other.noiseBound.

The current Turn22 reconstruction theorem already fixes every hypothetical branch reconstruction to the same:
- ptxtSpace=625;
- intFactor=1;
- keyID=0;
- primeSet=primeSet(recryptEkey).

Hence no branch-to-branch factor harmonization is triggered in the comparator envelope.

## 2. Exact separate-envelope formula

Let:
- E be the stored recryptEkey;
- N_E be E.getNoiseBound();
- Q_E be productOfPrimes(primeSet(E));
- f_E = balRem(Q_E mod625,625), because intFactor=1.

For branch i after exact divide-by5, let:

    s1_i = stock ZZX size estimate for z1_i
    s0_i = stock ZZX size estimate for z0_i.

A hypothetical stock-style branch reconstruction has metadata:

    N_i = N_E * s1_i + |f_E| * s0_i.

If the five reconstructed ciphertexts are subsequently added, their identical metadata types avoid factor harmonization, so the conservative HElib envelope is:

    N_sep
      = sum_i N_i
      = N_E * (sum_i s1_i)
        + |f_E| * (sum_i s0_i).                  (1)

This formula counts the stored recryptEkey noise five times, exactly as the five-separate HElib metadata path would.

## 3. Shared explicit-envelope formula

The candidate already forms exact public integers:

    Z1 = sum_i z1_i
    Z0 = sum_i z0_i.

Before discarding the individual pairs, compute:

    S1 >= sum_i s1_i
    S0 >= sum_i s0_i,

where S0,S1 are accumulated with upward rounding.

A simple implementation is to use the same per-branch stock ZZX size estimator and, for positive terms, advance each running floating sum with std::nextafter(...,+infinity). This avoids a candidate-specific downward rounding of the five-term accumulation.

Then execute:

    ctxt = recryptEkey;
    ctxt.multByConstant(Z1, S1);
    ctxt.addConstant(Z0, S0);

Pinned source formulas give:

    N_shared_guard
      = N_E * S1
        + |f_E| * S0
      >= N_sep.                                  (2)

Therefore the shared reconstruction can carry metadata at least as conservative as the five-separate stock envelope without constructing five R_i ciphertexts.

## 4. Ciphertext semantics are unchanged

The supplied size is not used as the plaintext multiplier/addend. The actual operations still use Z1 and Z0.

Hence the exact Turn22 ciphertext identity remains:

    R_shared
      = E * Z1 + Z0
      = sum_i (E*z1_i + z0_i)
      = sum_i R_i.

The explicit-envelope guard changes only HElib's software estimator metadata.

It does not:
- alter ciphertext parts;
- alter keyID;
- alter ptxtSpace;
- alter intFactor;
- alter primeSet;
- introduce a new key;
- introduce secret-key evaluator access.

## 5. What this does and does NOT prove

This result eliminates one candidate-specific implementation blocker:

The candidate does NOT need to assume that HElib's floating implementation of

    embeddingLargestCoeff(sum_i z_i)

is numerically subadditive relative to five separately evaluated floating estimates.

If the future native Step3 oracle finds that the default shared estimator is unexpectedly smaller/larger than the preregistered comparator relation, there is a source-valid conservative fallback using only public HElib APIs.

However, this is NOT a formal proof that HElib's own embeddingLargestCoeff floating estimate is a rigorous upper bound on the true canonical norm. Both stock and guarded candidate reuse HElib's same per-branch estimator semantics.

Thus:
- candidate-specific estimator discrepancy: CLOSED by construction fallback;
- true native capacity/noise margin: still PENDING;
- DFR: still PENDING;
- performance effect of using the conservative envelope: NOT MEASURED;
- recovery-only canary: still NOT EXECUTED.

## 6. Construction / Step3 refinement

The canonical mathematical construction is unchanged.

The implementation contract gains one robustness rule at shared reconstruction:

1. retain z0_i,z1_i long enough to compute the same branchwise size estimates stock HElib would use;
2. compute upward-rounded S0,S1;
3. form Z0,Z1 exactly;
4. reconstruct once with explicit sizes S1,S0;
5. assert native metadata is no less conservative than the five-separate estimator ledger;
6. continue to the pure inverse/recovery.

For a later optimized benchmark, use of the tighter default summed-polynomial estimator may be reconsidered only after correctness/capacity evidence. No performance claim is authorized now.

## Verdict

PASS_PUBLIC_SIZE_ENVELOPE_FALLBACK
PASS_SHARED_RECONSTRUCTION_STOCK_ESTIMATOR_DOMINATION
PASS_NO_PRIVATE_NOISEBOUND_MUTATION_REQUIRED
PASS_EXACT_CIPHERTEXT_PART_IDENTITY_PRESERVED

REFINE_SHARED_RECONSTRUCTION_IMPLEMENTATION_WITH_EXPLICIT_BRANCH_SUMMED_SIZE_GUARD

NATIVE_EXECUTION=NOT_OBTAINED
RECOVERY_CANARY=NOT_EXECUTED
CORRECTNESS_GATE=BLOCKED
BASELINE_CORRECTNESS=PENDING
NOVELTY_STATUS=PREFLIGHT
SECURITY_GATE=PENDING
VALUE_GATE=PENDING
AUDIT_GATE=PENDING
PAPER_READINESS=NOT_READY

## Next decisive test

The evidence-order blocker remains Step2:
execute the frozen revised recovery-only canary at the pinned HElib commit with HELIB_DEBUG=ON.

After Step2 PASS, Step3 exact parameter/interface verification must additionally instrument the shared reconstruction estimator ledger:
- record each branch s0_i,s1_i;
- record upward S0,S1;
- execute the explicit-size shared reconstruction;
- assert its noiseBound follows equation (2);
- compare exact ciphertext parts/metadata against the five-separate oracle;
- then proceed through the already-preregistered mod5-to-Z625 bridge, real inverse, factor67, rho/443, L0-L3, Algorithm4, final Recode and f_in restoration.

Do not time the candidate before correctness assertions pass.
