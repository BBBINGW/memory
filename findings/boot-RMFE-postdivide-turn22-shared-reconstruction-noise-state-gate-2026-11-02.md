# BOOT Research Turn 22/25 — shared reconstruction ciphertext-state / noise-bound soundness gate

Date: 2026-11-02
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Phase: CORRECTNESS_GATE
Candidate: PRE-TAG + POST-DIVIDE LATE AGGREGATION
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Infrastructure preflight — NOT the scientific hypothesis

The frozen revised recovery-only canary was restored at blob
6ae4bc7e48e0390f8dec97429f4ddb89565928c0.

The current execution container has:
- g++ / clang++ / cmake / pkg-config;
- GMP development files;

but has no:
- HElib headers or library;
- NTL headers or library;
- HElib source tree.

Container DNS cannot resolve github.com. Direct dependency download attempts also failed.
Therefore the frozen canary was NOT executed and no PASS/FAIL is inferred.

This infrastructure preflight is not counted as a scientific canary result.

## Primary hypothesis

Turn 18 established the legal post-divide aggregation point and the plaintext affine identity.

The remaining source-level uncertainty is stronger:

does performing one reconstruction from the aggregate pair

  A0 = sum_i a0_i
  A1 = sum_i a1_i

produce a HElib ciphertext state whose
- ciphertext parts;
- ptxtSpace;
- intFactor;
- key ID;
- prime set;
- tracked noise bound

are sound for the downstream pure EvalMap / recovery path?

Hypothesis:
the shared reconstruction

  R_shared = E * A1 + A0

with E = recryptEkey is ciphertext-module exact relative to summing the five separate stock
reconstructions, preserves the same temporary-625 metadata interface, and has a mathematically
valid canonical-embedding noise envelope no worse than the conservative sum of the five separate
stock envelopes.

Falsifier:
- addConstant uses branch-dependent metadata scaling that does not commute with aggregation;
- multByConstant changes ptxtSpace/intFactor/keyID/primeSet;
- summing before multiplying E omits independent encryption noise that would exist in five stock
  branches;
- the aggregate constant norm can invalidate the bound even though separate branch bounds are valid;
- or shared reconstruction emerges with a different key/plaintext-space interface.

No native execution or software-floating-point inequality is claimed.

## 1. recryptEkey has the exact temporary interface

Pinned SecKey::genRecryptData computes:

  p2ePr = context.getRcData().alMod->getPPowR()
         = p^(e-ePrime+r).

Current:
  p=5, e=4, ePrime=1, r=1,

so:
  p2ePr = 625.

It then calls:

  Encrypt(recryptEkey, keyPoly, p2ePr).

Pinned BGV Encrypt finishes by setting:

  ctxt.ptxtSpace = ptxtSpace;
  ctxt.intFactor = 1.

The comment and key construction establish that recryptEkey encrypts the recryption secret under
key #0.

Therefore E begins with:
  ptxtSpace = 625;
  intFactor = 1;
  keyID = 0.

This is the exact state required before the candidate pure inverse.

## 2. Polynomial multiplication preserves the reconstruction metadata

Pinned:

  Ctxt::multByConstant(const ZZX& poly)

computes embeddingLargestCoeff(poly), constructs a DoubleCRT over the current primeSet, then calls
the DoubleCRT overload.

The BGV DoubleCRT overload:
- multiplies every ciphertext part by the public DoubleCRT;
- updates noiseBound by multiplication with the supplied size;
- does NOT modify ptxtSpace;
- does NOT modify intFactor;
- does NOT modify primeSet;
- does NOT change secret-key handles.

Hence for any public integer polynomial a1_i or A1:

  E * a1

still has:
  ptxtSpace = 625;
  intFactor = 1;
  keyID = 0;
  primeSet = primeSet(E).

## 3. addConstant uses one common representation scaling factor

Pinned BGV addConstant(DoubleCRT,size) computes:

  f = productOfPrimes(primeSet) mod ptxtSpace;
  f = intFactor * f mod ptxtSpace;
  f = balanced representative.

Then it adds the public constant as:

  f * constant

to the part whose handle is 1, and increases the noise bound by:

  size * |f|.

Because polynomial multiplication in Section 2 changes none of:
- primeSet;
- ptxtSpace;
- intFactor,

every separate reconstruction R_i uses EXACTLY the same f.

The shared reconstruction uses the same E state and therefore the same f as well.

Thus there is no branch-dependent representation scale hidden inside addConstant.

## 4. Exact ciphertext-part identity

For each post-divide pair define stock-style reconstruction:

  R_i = reconstruct(E,a0_i,a1_i).

At the raw ciphertext-part level, after the common representation factor f is made explicit:

  R_i.parts
    = E.parts * a1_i
      + f * a0_i * one_handle.

Summing five copies gives:

  sum_i R_i.parts
    = E.parts * sum_i a1_i
      + f * sum_i a0_i * one_handle.

The shared path is:

  R_shared = E;
  R_shared.multByConstant(A1);
  R_shared.addConstant(A0),

so:

  R_shared.parts
    = E.parts * A1
      + f * A0 * one_handle
    = sum_i R_i.parts.

Therefore:

  R_shared == sum_i R_i

at the ciphertext-module parts level over the current ciphertext modulus, not merely after
decryption and not merely modulo 5.

This also covers reduction of arbitrary ZZX representatives into the ciphertext ring because
DoubleCRT construction is linear.

## 5. Why there are not five independent recryptEkey noise samples

A possible hidden objection is:
stock runs reconstruct five branches, so perhaps it has five independent E noises whereas the
shared candidate has only one.

This is false for the actual source structure.

recryptEkey is generated once in SecKey::genRecryptData and stored in PubKey.

Every branch reconstruction executes:

  ctxt = recryptEkey

which copies that same stored ciphertext E.

It does NOT freshly encrypt the recryption key for each branch.

Hence the five stock reconstruction noise terms are perfectly correlated copies of the same
underlying E noise.

Their algebraic sum is exactly:

  n_E * sum_i a1_i,

which is precisely the E-noise term inside the shared reconstruction.

The shared path therefore does not omit any independent stochastic noise source.

## 6. ptxtSpace / factor / key / prime-set equality to the separate reconstruction

Each R_i has:
  ptxtSpace = 625;
  intFactor = 1;
  keyID = 0;
  primeSet = primeSet(E).

If the five R_i are added, pinned addCtxt sees:
- identical ptxtSpace;
- identical intFactor;
- identical primeSet;
- identical context / public key.

Therefore it requires:
- no plaintext-space reduction;
- no factor harmonization;
- no mod-up for prime-set matching.

The sum keeps the same interface.

R_shared begins from E and Sections 2-3 do not alter that interface.

Thus:

  metadata(R_shared) = metadata(sum_i R_i)

for all of:
  ptxtSpace;
  intFactor;
  keyID;
  primeSet.

This justifies Turn 16's factor-1 input assumption for the pure inverse from the actual shared
reconstruction design.

## 7. Exact mathematical noise envelope

Let:
  B_E = tracked noise bound of E,
  N(a) = exact canonical-embedding L_infinity norm of public polynomial a,
  F = |f|.

For a separate stock reconstruction, the source ledger is:

  B_i <= B_E * N(a1_i) + F * N(a0_i).

Adding the five reconstructed ciphertexts conservatively gives:

  B_sep
    <= sum_i B_i
    <= B_E * sum_i N(a1_i)
       + F * sum_i N(a0_i).

The shared reconstruction has the exact correlated noise expression corresponding to:

  E_noise * A1
  plus the representation contribution from A0.

Therefore the natural bound is:

  B_shared
    <= B_E * N(A1) + F * N(A0).

Canonical embedding is linear and L_infinity is a norm, so:

  N(sum_i a1_i) <= sum_i N(a1_i),
  N(sum_i a0_i) <= sum_i N(a0_i).

Hence:

  B_shared <= B_sep

under the same exact canonical-norm ledger.

This is a correctness/noise-envelope result, NOT a measured capacity improvement.

## 8. HElib's actual size estimator and numerical caveat

Pinned ZZX multByConstant and addConstant both obtain their default public-polynomial size from:

  embeddingLargestCoeff(poly, zMStar).

Pinned norms.cpp computes the canonical-embedding largest coefficient through floating FFT
machinery, with explicit coefficient scaling when integers exceed 400 bits to avoid double
overflow.

Therefore HElib is attempting to instantiate exactly the canonical norm N above.

However this is floating numerical code, not an interval-certified exact norm evaluator.

Accordingly Turn 22 does NOT claim the software values always satisfy bit-for-bit:

  embeddingLargestCoeff(sum a_i)
    <= sum embeddingLargestCoeff(a_i)

for every possible input despite floating roundoff.

The correct statement is:
- mathematically the shared bound is no worse;
- HElib uses the same estimator family as stock;
- native correctness should assert the actual recorded shared noiseBound and exact decryption.

There is no new structural underestimation caused by correlated E noise.

## 9. Stronger implementation oracle for the Turn-18 native gate

After helper A produces five post-divide pairs, the future native exact-interface gate should build
both paths in a correctness-only harness:

Separate oracle:
  for i=0..4:
    R_i = reconstruct(E,a0_i,a1_i)
  R_sum = sum_i R_i

Shared:
  R_shared = reconstruct(E,sum_i a0_i,sum_i a1_i).

Require BEFORE any inverse transform:

1. exact decrypted plaintext equality R_shared == R_sum;
2. for a debug/internal harness, exact equality of Ctxt parts/handles modulo the same prime set;
3. ptxtSpace(R_shared) == 625;
4. intFactor(R_shared) == 1;
5. keyID(R_shared) == 0;
6. primeSet(R_shared) == primeSet(E);
7. R_shared.noiseBound is finite and exact decrypt succeeds;
8. record both shared and separate-sum noiseBound values, but make no performance/capacity claim
   solely from their relation.

Any metadata or ciphertext-part mismatch is:
  FAIL_SHARED_RECONSTRUCTION_INTERFACE.

## 10. Scope

Established:
- one shared reconstruction is source-exact at the ciphertext-module level;
- there is no missing independent recryptEkey encryption noise;
- all downstream temporary metadata match the stock reconstructed-sum state;
- exact canonical-norm noise analysis is subadditive and therefore sound for aggregation.

Not established:
- native execution;
- actual floating estimator inequality on concrete post-divide pairs;
- actual bit capacity after shared reconstruction;
- recovery canary;
- baseline/candidate end-to-end correctness;
- DFR or performance.

## Verdict

PASS_SHARED_RECONSTRUCTION_CIPHERTEXT_PART_EXACTNESS
PASS_NO_MISSING_INDEPENDENT_RECRYPT_EKEY_NOISE
PASS_SHARED_RECONSTRUCTION_METADATA_EQUIVALENCE
PASS_SHARED_RECONSTRUCTION_EXACT_NORM_ENVELOPE
SOFTWARE_FLOATING_NORM_INEQUALITY=NATIVE_ASSERTION_REQUIRED

RECOVERY_CANARY=NATIVE_NOT_EXECUTED_ENVIRONMENT_MISSING_HELIB_NTL
NATIVE_EXECUTION=NOT_OBTAINED

This closes a source-level correctness/noise-state interface immediately before the pure EvalMap.

CORRECTNESS_GATE remains BLOCKED because the mandatory native evidence order has not advanced past
the missing small recovery canary.

BASELINE_CORRECTNESS remains PENDING.
NOVELTY_STATUS remains PREFLIGHT.
SECURITY_GATE remains PENDING.
VALUE_GATE remains PENDING.
PAPER_READINESS remains NOT_READY.

## Next decisive test

The primary blocker remains execution of the frozen revised recovery-only canary in an environment
containing pinned HElib with HELIB_DEBUG=ON.

After that PASS, the exact parameter/interface gate must first instantiate the dual reconstruction
oracle above and require ciphertext-part/metadata/decryption equality before applying the real
normal_basis=false EvalMap.

No capacity or timing interpretation is authorized before those native checks pass.
