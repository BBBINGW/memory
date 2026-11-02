# BOOT Research Turn 14/25 — production FULL-Frobenius temporary-625 keyset gate

Date: 2026-11-02
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Phase: CORRECTNESS_GATE
Candidate: PRE-TAG + POST-DIVIDE LATE AGGREGATION
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Primary hypothesis

The Turn-11 recovery-only canary uses 13 explicitly generated direct Frobenius matrices with
ptxtSpace=625. For that canary to represent the production candidate rather than a stronger
artificial keyset, the stock FULL HElib bootstrapping setup must generate the same Frobenius
matrices at temporary plaintext space 625.

Hypothesis:
for the canonical p=5,r=1,e=4,ePrime=1 bootstrappable context, calling
addFrbMatrices(secretKey) after Context::enableBootStrapping but before
SecKey::genRecryptData generates every FULL Frobenius KeySwitch with ptxtSpace=625.

Falsifier:
- addFrbMatrices passes an explicit p=5 to GenKeySWmatrix;
- Context::isBootstrappable is still false before genRecryptData;
- rcData.alMod uses p^r rather than p^(e-ePrime+r);
- or the current canonical parameters imply a temporary plaintext space other than 625.

This turn does not run the blocked canary and does not claim native evidence.

## 1. Exact default-p path of FULL Frobenius matrix generation

Pinned src/keySwitching.cpp implements:

  addFrbMatrices(sKey,keyID)
    -> addSomeFrbMatrices(sKey,LONG_MAX,keyID)
    -> add1Dmats4dim(sKey,-1,keyID).

For Frobenius dimension -1, add1Dmats4dim iterates every nonidentity Frobenius power and calls

  sKey.GenKeySWmatrix(1, zMStar.genToPow(-1,j), keyID, keyID);

with NO explicit plaintext-space argument.

Therefore GenKeySWmatrix receives its default p value (<2) and resolves the actual KeySwitch
plaintext space internally.

## 2. GenKeySWmatrix resolves default p from Context, not PubKey

Pinned SecKey::GenKeySWmatrix contains the BGV rule:

  if (p < 2) {
    if (context.isBootstrappable())
      p = context.getRcData().alMod->getPPowR();
    else
      p = pubEncrKey.ptxtSpace;
  }

and then sets

  ksMatrix.ptxtSpace = p.

This distinction is decisive.

There are TWO bootstrappability predicates in pinned HElib:

Context:
  bool Context::isBootstrappable() const
  { return rcData.alMod != nullptr; }

PubKey:
  bool PubKey::isBootstrappable() const
  { return recryptKeyID >= 0; }

addFrbMatrices/GenKeySWmatrix uses the CONTEXT predicate.

Hence addFrbMatrices does not require genRecryptData to have already created the public
recryptKeyID. It only requires the Context recryption data to have been initialized.

## 3. Context::enableBootStrapping initializes rcData before key generation

Pinned Context::enableBootStrapping executes:

  rcData.init(*this,mvec,...)

and Context::isBootstrappable becomes true as soon as rcData.alMod is non-null.

Pinned RecryptData::init reads:

  e       = context.getE();
  ePrime  = context.getEPrime();
  r       = context.getAlMod().getR();

and constructs

  alMod = PAlgebraMod(context.getZMStar(), e-ePrime+r).

The HElib header explicitly documents this object as the algebra for plaintext space

  p^(e-ePrime+r).

Therefore after enableBootStrapping, before any secret key or recryptEkey is generated,

  context.isBootstrappable() == true

and

  context.getRcData().alMod->getPPowR()
    = p^(e-ePrime+r).

## 4. Canonical current parameters give exactly 625

Current durable candidate parameters are:

  p=5
  r=1
  e=4
  ePrime=1.

Thus:

  e-ePrime+r = 4-1+1 = 4

and therefore

  p^(e-ePrime+r) = 5^4 = 625.

Hence every default-p GenKeySWmatrix call made by addFrbMatrices in this context receives

  p = 625

and stores

  KeySwitch::ptxtSpace = 625.

This holds for all 8191 nonidentity FULL Frobenius matrices, including the 13 exponents used by
the target-pruned recovery.

## 5. Stock HElib bootstrapping call order confirms the condition

Pinned tests/GTestThinboot.cpp follows the sequence:

  context.buildModChain(..., willBeBootstrappable=true);
  context.enableBootStrapping(mvec,...);

then, only afterward:

  SecKey secretKey(context);
  secretKey.GenSecKey();
  addSome1DMatrices(secretKey);
  addFrbMatrices(secretKey);
  secretKey.genRecryptData();

Thus addFrbMatrices occurs BEFORE genRecryptData, but AFTER Context::enableBootStrapping.

At the moment FULL Frobenius matrices are generated:

  Context::isBootstrappable() = true,
  PubKey::isBootstrappable()  = false.

This is not a contradiction. GenKeySWmatrix deliberately queries the Context, so the generated
Frobenius matrices already use the larger bootstrapping plaintext space.

The same ordering appears in pinned fat/thin bootstrapping examples/tests.

## 6. Consequence for the Turn-11 canary

Turn 11 generates only the 13 needed matrices explicitly as

  GenKeySWmatrix(1,k,0,0,625)

to avoid generating the entire FULL keyset in a small correctness canary.

Turn 14 establishes that, with respect to:
- automorphism handle k;
- from/to key ID 0;
- direct one-hop matrix semantics;
- matrix plaintext space 625,

these targeted matrices are the same TYPE of KeySwitch object that the production standard FULL
bootstrapping setup generates.

The canary does NOT emulate:
- the memory cost of all 8191 FULL matrices;
- production key-generation latency;
- a matched Aung artifact run.

Those remain outside small-correctness evidence.

## 7. No extra evaluation-key family is required under the declared FULL comparator

The current production candidate requires only 13 Frobenius exponents from the already-existing
FULL family.

Since the standard bootstrappable FULL keyset already stores all Frobenius matrices at
ptxtSpace=625, the candidate does not require:
- a second temporary-625 Frobenius key family;
- replacement of stock mod-5 matrices;
- evaluator secret-key access;
- a new key type.

Therefore the exact production resource statement is:

  candidate-specific Frobenius KEY TYPE delta = 0

under SAME FULL bootstrapping resource parity.

This is not yet a byte-memory benchmark. FULL-vs-BSGS/MIN comparators still require explicit
resource accounting.

## 8. Aung-artifact boundary

This turn proves the pinned STANDARD HElib FULL bootstrapping key-generation semantics.

It does not independently authenticate a public Aung implementation artifact showing its exact
key-generation call order. The current paper candidate and preregistered native comparator both
require the same pinned standard FULL HElib context/key object.

Therefore future native baseline/candidate execution MUST assert the actual instantiated object,
rather than infer it from the paper:

  context.isBootstrappable() == true
  rcData.e == 4
  rcData.ePrime == 1
  rcData.alMod->getPPowR() == 625
  getKSStrategy(-1) == HELIB_KSS_FULL
  every required getNextKSWmatrix(k,0).ptxtSpace == 625.

If the source-faithful Aung artifact uses a different Frobenius resource strategy, the comparator
must be reclassified and resource parity recomputed rather than silently transferred.

## Verdict

PASS_STANDARD_FULL_FROBENIUS_PTXTSPACE_625
PASS_TARGETED_CANARY_KEY_TYPE_EQUIVALENCE
PASS_NO_SECOND_625_FROBENIUS_KEY_FAMILY
AUNG_ARTIFACT_EXACT_KEYGEN_ORDER=UNVERIFIED

This is source/static exact-parameter/interface evidence only. It does not advance the native
evidence order past the still-missing recovery canary execution.

CORRECTNESS_GATE remains BLOCKED.
BASELINE_CORRECTNESS remains PENDING.
NOVELTY_STATUS remains PREFLIGHT.
SECURITY_GATE remains PENDING.
VALUE_GATE remains PENDING.
PAPER_READINESS remains NOT_READY.

## Next decisive test

Primary blocker remains execution of the frozen recovery-only canary.

If an execution environment remains unavailable, the next independent correctness unit should
audit a DIFFERENT unresolved end-to-end interface rather than revisit recovery canary/keyset
source semantics.

For eventual native exact-parameter verification, add the six runtime assertions listed in
Section 8 before accepting any recovery or baseline result.
