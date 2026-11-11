# BOOT / B158_OVERALL — Research Turn 14/25
## Single-limb sparse gateway: exact source-feasibility / bounded-repair gate

Date: 2026-11-11 (Asia/Singapore)
Candidate: boot-b158-single-limb-sparse-gateway-composite-v1
Phase: CORRECTNESS_GATE
Status entering turn: ACTIVE
This version is the valid logical Research Turn 14/25 and supersedes the prior infrastructure-invalid draft at this same path.

## Pre-registration

QUESTION:
Can the degree-2 q0-only sparse-security gateway be realized by a single bounded source-interface repair on PR #1381, reusing the existing one-limb sparse key switch and single-digit KeySwitchRaise arithmetic, or does the stock source reveal a mechanism-level incompatibility that requires parking the candidate?

CURRENT_BELIEF:
The arithmetic needed by the candidate already exists, but stock parameter precomputation binds both the low sparse switch and the single-digit raise switch to compositeDegree-derived conditions. If those bindings are only provenance/interface guards, a candidate-local parameter descriptor should be sufficient; if the underlying algorithms consume q1-dependent residues, the candidate must be parked.

CHEAPEST_DECISIVE_TEST:
Source-audit every use of the sparse-switch Q/P parameters, sparse Hamming-weight selection, and PR #1381 single-digit raise path. Determine whether the one-limb branches are algebraically parameterized by the actual input basis or structurally depend on compositeDegree=1.

IF_PASS:
Retain ACTIVE and allow exactly one bounded candidate source repair: a q0-provenance sparse-gateway descriptor that supplies Qg={q0}, Pg, h=32/K=16 and authorizes the existing exact-q0-lift single-digit KeySwitchRaise path. Next test is a candidate-native canary with explicit interface/tower assertions plus whole-output FBT correctness.

IF_FAIL:
PARK the candidate. In particular, if KeySwitchRaise or its evaluation key requires the missing q1 residue before q1 restoration, or the low key switch cannot be parameterized to Qg={q0} without a new key-switch construction, this is mechanism-level failure.

IF_UNCLEAR:
Keep CORRECTNESS_GATE=PENDING but do not launch the full FBT benchmark; first obtain the exact missing source interface.

WHICH_PAPER_GATE_CHANGES:
Killer gate (2), stock/source feasibility, and the source-feasibility prerequisite of CORRECTNESS_GATE.

WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION:
The durable candidate previously treated the existing one-limb h32 regression and PR #1381 single-digit raise implementation as calibration. This audit decides whether those implementations are actually reusable in a degree-2 context, which determines whether a native canary is meaningful or whether the candidate must be parked before execution.

## Closest source/prior-art boundary and exact delta

OpenFHE PR #1286 explicitly defines SPARSE_ENCAPSULATED over the whole bottom basis Ql={q0,...,q_{d-1}}, d=compositeDegree. Its auxiliary P' is sized against that whole bottom modulus; for a >60-bit composite bottom modulus it uses the larger sparse-key regime.

OpenFHE PR #1318 makes the Hamming weight / overflow bound depend on the first-modulus size: h=32,K=16 at <=60 bits and h=64,K=28 above 60 bits.

OpenFHE PR #1381 introduces the raised-basis switch-back before R normalization. In its cryptoparameter patch, the fast single-digit case is enabled only when:
  compositeDegree == 1 && q0 <= 16*P'
and creates a single digit spanning the raised basis. KeySwitchRaise then reconstructs that digit by taking cv[1]'s bottom limb and exactly lifting it into Q'*P.

The candidate's exact delta is therefore NOT a new key-switch formula. It changes the provenance boundary:
  logical bottom period remains B=q0*q1,
  but the temporary sparse-secret ciphertext is first physically reduced to q0,
  so its low sparse switch and later raised switch may use the same one-limb/exact-q0-lift arithmetic that stock code only authorizes for degree 1.
q1 is restored only after the sparse-to-dense switch and before R normalization.

## Source evidence

### A. Stock low sparse switch is hard-bound to the whole composite bottom basis

Current OpenFHE source (the sparse-encapsulation code introduced by #1286/#1318) precomputes:
  sizeQl = compositeDegree;
  modulusQl = product(q_i, i < sizeQl);
and derives firstModSize from the sum of all bottom-limb bit lengths. The same value selects m_sparseKSHammingWeight and hence h=64 above 60 bits. The auxiliary sparse modulus is then ~127 bits in that regime.

KeySwitchGenSparse and KeySwitchSparse obtain GetSparseKSParamsQ/P/QP from the crypto parameters; they therefore use the whole Ql in a degree-2 context. Stock degree-2 code cannot become q0-only merely because the ciphertext has physically lost q1.

This is a real source-interface blocker for an unmodified candidate.

### B. The low key-switch arithmetic itself already supports Q={q0}

ExtendSparseKSToP branches on the actual number of Ql limbs:
  if sizeQl == 1:
      use centered SwitchModulus from q0 to each P' prime;
  else:
      use exact HPS SwitchCRTBasis.

KeySwitchSparse subsequently performs the same GHS-style switch and exact balanced P' -> Ql reduction using whatever Ql parameter set it is given.

A repository-wide search found GetSparseKSParamsQ/P usage localized to this sparse-key-switch implementation plus the parameter getters/tests. Therefore a candidate-local Qg={q0}, Pg table bundle does not require changing generic DCRT arithmetic.

### C. PR #1381 single-digit KeySwitchRaise is also provenance-driven, not intrinsically degree-1

PR #1381 precomputation currently sets m_modRaiseKSSingleDigit only when compositeDegree==1 and q0 <= digitBound. This is the stock source reason the degree-2 candidate cannot simply call the fast path.

But KeySwitchRaise's single-digit branch does not consult compositeDegree. It:
  1. reads cv[1].GetElementAtIndex(0);
  2. converts that q0 limb to coefficient form;
  3. constructs DCRTPoly d(x0, paramsExt), i.e. the exact centered lift to Q'*P;
  4. evaluates the one-row raise key over Q'*P;
  5. ApproxModDowns by P'=P/R back to the raised Q'*R basis.

KeySwitchGenRaise likewise constructs the key over Q*P from the old sparse and new dense secrets. Its one-row gadget is determined by GetModRaiseKSDigits; it does not mathematically require compositeDegree==1.

Therefore compositeDegree==1 is serving as a sufficient source-level proof that the switched element is an exact lift of a q0 value. The candidate establishes the same invariant by construction after the physical q1 rescale.

### D. One bounded repair is sufficient at the source-interface level

The allowed bounded repair is one candidate-local 'sparse gateway descriptor' (name illustrative, not an API claim) threaded through the existing code paths:

1. Low switch descriptor:
   Qg={q0}; Pg chosen with the same one-limb h32 sparse-KS rule (~66 total bits in the 64-bit build); Qg*Pg and exact ModDown tables generated by the existing sizeQl==1 formulas.

2. Sparse secret / FBT approximation:
   draw the temporary sparse secret with h=32 for this gateway; select K=16 from that actual gateway Hamming weight. Do not globally rewrite ordinary degree-2 SPARSE_ENCAPSULATED behavior.

3. Raise provenance flag:
   explicitly assert that cv[1] entering KeySwitchRaise is the exact lift of a value modulo q0. Under that assertion, instantiate the existing single digit [0,sizeRaised] even though the ambient context has compositeDegree=2.

4. Raise implementation:
   reuse the existing PR #1381 one-limb exact-lift branch and KeySwitchGenRaise/KeySwitchRaise/ApproxModDown arithmetic. No new digit decomposition, external product, or RNS basis-switch primitive is required.

5. Candidate ordering invariant:
   physical q1 rescale -> q0-only sparse switch -> exact q0 lift -> single-digit sparse-to-dense switch -> q1 restoration -> R normalization.
   q1 restoration algebra/noise was already discharged in the preceding durable turn and is not re-proved here.

This repair is bounded because it changes parameter provenance and dispatch only; it does not alter the generic key-switch equations or ApproxModDown implementation. It is nevertheless mandatory: the unmodified degree-2 source is NOT a valid implementation of the candidate.

## Decision

SOURCE_FEASIBILITY_BOUNDED_REPAIR_PASS.

This is not candidate correctness PASS and not native evidence. The candidate remains ACTIVE because the source obstruction is interface/provenance-only and the exact arithmetic paths needed by the candidate already exist.

The prior belief that baseline UnitTestSparseKS alone calibrates the candidate is narrowed:
  - baseline one-limb sparse KS validates the arithmetic family;
  - it does NOT validate the degree-2 candidate's q0-only parameter/key edge;
  - PR #1381's single-digit raise validates the arithmetic family;
  - it does NOT validate enabling that path under a degree-2 context.

## Next decisive test

One candidate-native canary on the exact PR #1381 tree, with the bounded repair above and no further mechanism changes.

Mandatory pre-output assertions:
- ambient compositeDegree == 2;
- gateway Q size == 1 and gateway modulus == q0;
- gateway sparse Hamming weight == 32;
- FBT overflow table selected is K == 16;
- raise switch reports exactly one digit;
- the digit is the exact q0-lift path, not ApproxSwitchCRTBasis decomposition;
- same temporary sparse secret is used by low switch and switch-back key;
- tower order before switch-back is the intended Q'*R / Q'*P order;
- q1 restoration occurs before R normalization.

Decisive semantic assertions:
- low switch added-noise over >=7 trials, compared only as calibration with the existing one-limb h32 regression;
- epsilon_L and epsilon_H measured in temporary q0 units;
- q1*epsilon_L/B == epsilon_L/q0 and q1*epsilon_H/B == epsilon_H/q0 numerically modulo aliases;
- post-switch q1 restoration preserves the full B-period decomposition;
- R normalization leaves correct tower count, level, scaling factor and noise-scale metadata;
- full-packed 8-bit zero LUT has zero modular output error on the test vector(s).

IF the bounded source repair cannot compile or requires a second independent representation/key-switch redesign, park the candidate rather than patching again.

## Eliminated uncertainty

Eliminated: whether the degree-2 source binding itself constitutes a mechanism-level impossibility.
Result: NO. Stock source is incompatible as written, but both required arithmetic subpaths are already present and can be reached by one explicit q0-provenance parameter/dispatch repair.

Still unknown:
native correctness, epsilon_H tails/DFR, security estimator, matched value, independent novelty audit.

## Evidence references

- OpenFHE PR #1286: composite SPARSE_ENCAPSULATED defines sparse switch over full bottom Ql and larger P'/h for large bottom modulus.
- OpenFHE PR #1318: h/K selection by first-modulus size, h32/K16 <=60 bits and h64/K28 >60 bits.
- OpenFHE PR #1381 patch:
  src/pke/lib/scheme/ckksrns/ckksrns-cryptoparameters.cpp — single-digit raise precompute requires compositeDegree==1 and q0<=digitBound.
  src/pke/lib/scheme/ckksrns/ckksrns-fhe.cpp — KeySwitchGenRaise and KeySwitchRaise single-digit exact-q0-lift implementation.
- OpenFHE current sparse source:
  src/pke/lib/scheme/ckksrns/ckksrns-cryptoparameters.cpp — sizeQl=compositeDegree, whole-bottom firstModSize, sparse parameter generation.
  src/pke/lib/scheme/ckksrns/ckksrns-fhe.cpp — ExtendSparseKSToP one-limb branch, KeySwitchGenSparse, KeySwitchSparse.
