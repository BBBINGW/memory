# BOOT Research Turn 11/25 — recovery-only HElib canary construction / false-positive gate

Date: 2026-11-02
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Phase: CORRECTNESS_GATE
Candidate: PRE-TAG + POST-DIVIDE LATE AGGREGATION
Pinned HElib target: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Primary hypothesis

Turn 10 closed abstract-to-HElib API realizability but no concrete ciphertext canary source existed. The highest-information next step is to construct the exact recovery-only HElib canary and audit that its TEST SETUP itself cannot silently reduce the temporary plaintext space from 625 to 5 or otherwise share an invalid oracle assumption.

Hypothesis:
a standalone recovery-only canary can be instantiated in an application-style r=1 HElib context while encrypting the synthetic recovery input at exact ptxtSpace=625, using only 13 explicitly generated direct Frobenius matrices at ptxtSpace=625, and can independently verify every retained Ctxt node, five exact dirty Z_625 leaves, routing, and L0..L3 without requiring full bootstrapping or performance work.

Falsifier:
- the available Encrypt path silently reduces 625 to 5;
- direct key-switch matrices are generated only for ptxtSpace=5;
- private intFactor prevents external semantic verification;
- the canary only tests clean selected coordinates rather than dirty Z_625 lifts;
- or implementation requires production-private recryptEkey/newMakeDivisible access.

## Source findings

### 1. Public-key encryption is a false-positive trap; secret-key test encryption is valid

Pinned PubKey::Encrypt for BGV harmonizes a requested plaintext space with pubEncrKey.ptxtSpace via gcd. In an application r=1 context the public encryption key has ptxtSpace=5, so requesting PubKey::Encrypt(...,625) would reduce the effective plaintext space to 5.

Such a canary could pass while proving only mod-5 correctness. It is forbidden.

Pinned SecKey overrides Encrypt and calls skEncrypt directly. skEncrypt:
- accepts an explicit BGV ptxtSpace >=2;
- assigns ctxt.ptxtSpace to that requested value;
- initializes intFactor=1;
- uses RLWE with that ptxtSpace.

Therefore a TEST-ONLY call

  secretKey.Encrypt(ctxt, plaintext, 625)

in the same r=1 context constructs a genuine ptxtSpace=625 ciphertext under secret-key index 0.

This use of the evaluator secret key is only canary input generation; it is not part of the candidate mechanism and provides no production secret-key requirement.

### 2. Targeted direct Frobenius matrices can be generated at exact ptxtSpace=625

Pinned SecKey::GenKeySWmatrix accepts an explicit plaintext-space argument p. The generated KeySwitch object stores that ptxtSpace and RLWE1 noise is sampled with p.

Thus the small canary can generate exactly the 13 required direct matrices:

  GenKeySWmatrix(1, 5^j mod32768, 0, 0, 625)

for

  j in {4096,2048,1024,512,256,128,64,32,16,8,4,2,1}

and then call setKeySwitchMap(0).

This avoids generating all 8191 FULL Frobenius matrices. It tests Ctxt correctness, not production resource parity. Turn 10's source proof that canonical FULL resources also make each requested Frobenius one-hop remains a separate statement.

The canary explicitly asserts for every target:
- haveKeySWmatrix(...);
- isReachable(k,0);
- getNextKSWmatrix(k,0).fromKey.getPowerOfX()==k.

### 3. Private intFactor does not require an HElib patch

Ctxt::intFactor is private and has no public getter in the pinned API. Therefore Turn 10's proposed external runtime assertion of intFactor cannot literally compile.

No source patch is necessary.

The canary instead decrypts every constructed state against a completely independent coefficient-ring oracle:
- root;
- every Frobenius image;
- every retained even child;
- every retained odd child;
- every final leaf;
- every L0..L3 output.

SecKey::Decrypt applies the actual ciphertext ptxtSpace/intFactor semantics. Exact mod-625 equality at every stage therefore detects any semantic intFactor divergence even though the private integer cannot be directly read.

Directly readable assertions still cover:
- ptxtSpace==625;
- keyID==0;
- primeSet unchanged;
- Ctxt::isCorrect().

### 4. The canary exercises both selected and nonselected dirty state

Distinct base messages are used in the two physical CRT components.

Every selected target coordinate is then perturbed by a distinct multiple of 5, so the actual selected lifts are

  a_i = m_i + 5 delta_i in Z_625

with unchanged mod-5 messages.

Additional deterministic 5-divisible dirty coefficients are placed off-target at:

  [1,3,17,511,1023,1025,1536,3072,4095,4096,5000,7000,8191].

The expected leaves are the exact dirty selected lifts, not the clean source messages.

The L0..L3 reference is also built from those exact dirty lifts. This directly exercises the Turn-4/5 theorem that Aung Algorithm-4 correction images operate on arbitrary Z_625 scalar lifts congruent to the intended messages mod5.

### 5. Independent per-node oracle

The canary does not use HElib plaintext automorphism APIs as its reference.

It implements independent sparse coefficient arithmetic in

  (Z/625Z)[X]/(X^16384+1):

- global automorphism coefficient permutation/sign;
- global X^{-s} negacyclic shift;
- addition/subtraction;
- CRT idempotents;
- RMFE correction constants.

Thus a shared HElib encoding bug cannot make both implementation and oracle pass together.

Production normalization is respected: factor 28 is applied to the synthetic pre-tree plaintext before encryption, so the tree output is already normalized.

### 6. Frozen source artifact

The complete canary source is durable at:

  findings/boot-RMFE-postdivide-turn11-helib-recovery-only-canary-source-2026-11-02.txt

Latest blob SHA:

  e16d2b34221922752b5320eaec58d3a2997b9761

Its required success output is:

  PASS_HELIB_RECOVERY_ONLY_EXACT_Z625_CANARY
  calls=17
  pruned_coord_order=0,2048,6144,1024,7168
  pruned_branch_order=2,1,4,0,3
  branch_reorder_indices=3,1,0,4,2
  selected_dirty_lifts=PASS
  L0_L3_exact=PASS

No timing is present.

## Execution status

Native execution was attempted only insofar as checking whether the current sandbox already contained a usable HElib/NTL build.

Result:
- no HElib library/config/header was installed;
- NTL headers/library were absent;
- sandbox DNS/network access prevented cloning the pinned HElib source;
- no package candidate was locally available.

Therefore the canary was NOT compiled or executed.

This is an infrastructure limitation of this Research GPT environment, not evidence against the candidate.

No native PASS is claimed.

## Verdict

PASS_RECOVERY_CANARY_SOURCE_CONSTRUCTION
PASS_EXACT_625_TEST_SETUP_CONTRACT
PASS_DIRTY_SELECTED_LIFT_ORACLE
PASS_PER_NODE_INDEPENDENT_DECRYPT_ORACLE
NATIVE_EXECUTION=BLOCKED_BY_LOCAL_TOOLCHAIN

Overall scientific verdict for the requested small-correctness evidence remains UNCLEAR until the source is compiled and run against pinned HElib.

This turn converts the critical blocker from:

  no concrete recovery canary implementation

to:

  concrete audited canary source exists; execution evidence is still absent.

CORRECTNESS_GATE remains BLOCKED.
NOVELTY_STATUS remains PREFLIGHT.
SECURITY_GATE remains PENDING.
VALUE_GATE remains PENDING.
PAPER_READINESS remains NOT_READY.

## Next decisive test

Compile and run the durable Turn-11 canary once against pinned HElib. Do not time it. Accept only if every per-node exact decrypt assertion and final exact-Z625 leaf/L0..L3 assertion passes.

If it passes, native evidence order advances from small correctness canary to exact current-parameter/interface verification; it still does not authorize performance claims.
