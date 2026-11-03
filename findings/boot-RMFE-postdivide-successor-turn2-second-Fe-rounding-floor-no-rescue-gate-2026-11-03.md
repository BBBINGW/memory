# BOOT / B158 — Successor Research Turn 2 — second-Fe rounding-floor / no-bookkeeping-rescue gate

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: legacy-484479fe4613
PHASE: CORRECTNESS_GATE
Native execution: NONE

## Authority / read-before-write

PI-provided verified local durable authority at turn start:
  BBBINGW/memory main HEAD=origin/main=fdbf8ccf92b4751a4cc9678f5ef9c26ac64c48f4.

GitHub Notes is degraded for file reads but its repository listing was available. The target path was checked absent before write. Immutable previously-persisted blobs were used read-only to recover the exact active formulas:
- successor Turn1 blob a8fa515874cfe93795a3a47b08d8e48dacc2b42a;
- Turn22 derivation blob 01381a2a7098e94eace04582f7a14d90505bde8d;
- Turn22 source audit blob 7696a17405337610038da25a405e7172e9661720;
- Turn17 first-Fe gate blob 49b839ccb00201b9f16fa5de74db2855e22a7b50;
- Turn20 derivation blob 2ac7c94591e784b703a01bc84b52b3fe966de79a;
- Turn21 derivation/source blobs 6d10eae4307bee92831d5e6e71a85d3d7df52c42 / 7acc0261fbb8996911b857012519526b23842e31.

Pinned HElib source was inspected at homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1:
- include/helib/Context.h lines 34-35: MIN_SK_HWT=120 and BOOT_DFLT_SK_HWT=120;
- include/helib/Context.h around line1075: ContextBuilder default skHwt_=0;
- src/Context.cpp around lines1037-1060: buildModChain maps skHwt==0 to BOOT_DFLT_SK_HWT when willBeBootstrappable=true.
These are source-interface facts for the pinned library; no native candidate execution occurred.

Aung et al. ePrint2025/350 §6.1 reports m=32768 and HElib initialization with bits=400, but the paper text inspected does not state a secret-key Hamming-weight override. This turn does not infer the hidden implementation's exact hwt from omission; it instead derives a necessary hwt threshold that applies to any source-faithful instantiation using the inherited mod-down certificate.

## Closest prior / exact delta

Closest prior remains Aung Algorithm4 plus pinned HElib BGV modulus switching and multiplication. Successor Turn1 proved that the q-independent worst-case first-Fe envelope EFhat cannot be squared safely on the inherited P window.

This turn asks a strictly stronger paper-level question:

> Could Turn1's failure be repaired merely by using the actual fixed-prefix q, exact residues, exact key-switch K(q), and exact factor bookkeeping, while retaining the existing Turn14/17 independent modulus-switch rounding certificate?

If NO, the blocker is not the Turn23 q-independent EFhat coarse bound; it is the inherited mod-down rounding floor itself. This adds no novelty claim.

## One primary hypothesis / falsifier

Hypothesis H2:
A node-specific tightening at the already-fixed Turn22 prefix Pdagger (183 <= log2 q < 247) can still make the second Fe's first square certifiable without changing the secret-key regime, mod-down proof, or evaluation schedule.

Cheapest falsifier:
derive a necessary condition from the leading degree-5 term of the existing coefficient-L1 recurrence before using any residue or K(q) overapproximation. If this necessary condition already forces an insecure/unsupported secret-key Hamming weight, H2 fails independently of exact q residues and K(q).

## 1. Existing node-specific recurrence has a hard leading-term floor

Let A denote the certified envelope of the first-Fe input after mod-down to the fixed P:
  A = (q/Q0) E0 + R.

The source-faithful Turn20-23 first-Fe envelope uses nonnegative quantities:
  E2 = A^2 + K,
  E3 = A(E2+1872)+K,
  E4 = E3 + H(A+C1),
  ET = E4 E2 + K,
  EF = ET + U2(E2+5 U1 A).

Therefore, without assuming any worst-case residue value and without using K>0:
  E2 >= A^2,
  E3 >= A E2,
  E4 >= A E2,
  ET >= A E2^2 >= A^5,
  EF >= A^5.

This is a lower bound on the *certified upper-bound expression* produced by this proof architecture, not a lower bound on the actual ciphertext error.

The second Fe first square uses:
  E_sq2 <= EF^2 + K2.

For this proof architecture to certify E_sq2 < 0.48 q, it is therefore necessary that
  EF < sqrt(0.48 q),
hence necessarily
  A^5 < sqrt(0.48 q).

Since A=(q/Q0)E0+R >= R, an even simpler necessary condition is
  R^5 < sqrt(0.48 q),
equivalently
  q > R^10 / 0.48.                    (NC)

Any tightening of H,C1,U1,U2 or K(q), and any exact q residue computation, cannot evade (NC) while the same R certificate is retained.

## 2. Bind R to the source-level sparse-secret certificate

Turn17's independent source formula is
  R(h) = 312.5 * phi(m) * (1+h),
where h is the coefficient-L1 bound of a ternary secret. Here m=32768 and phi(m)=16384, so
  312.5*phi(m) = 5,120,000,
and
  R(h) = 5,120,000 (1+h).

For the inherited fixed prefix:
  log2 q < 247.

Substituting q<2^247 into (NC) gives the necessary condition
  10 log2 R(h) - log2(0.48) < 247.

Exact values:
  h=0: q must exceed 2^223.9360174845;
  h=1: q must exceed 2^233.9360174845;
  h=2: q must exceed 2^239.7856424918;
  h=3: q must exceed 2^243.9360174845;
  h=4: q must exceed 2^247.1552984334.

Therefore every integer h>=4 is impossible for this proof architecture on the entire inherited Turn22 window.

Equivalently:
  REQUIRED_HWT_ON_Pdagger <= 3.

This statement is stronger than Turn1's EFhat failure: it is independent of the exact prefix residue modulo625, exact K(q), exact public-unit aligners, and the q-independent EFhat replacement.

## 3. The only possible h<=3 escape is incompatible with the intended security regime

Pinned HElib source has:
  MIN_SK_HWT = 120,
  BOOT_DFLT_SK_HWT = 120.

ContextBuilder initializes skHwt_=0, and buildModChain changes 0 to 120 for a bootstrappable BGV context. Thus the pinned default bootstrappable regime has h=120, not h=0.

For h=120:
  R = 619,520,000,
  log2 R = 29.2065756168,
  necessary log2 q > 293.1246498573.

At q<2^247 the leading-term certificate alone misses the second-square threshold by at least:
  5 log2 R - 0.5 log2(0.48*2^247)
  = 23.0623249286 bits.

This is before adding any key-switch K or sibling/alignment terms.

Could one explicitly set h<=3? Algebraically the API accepts positive h, but that is not a security-preserving rescue. For a ternary secret of exact Hamming weight h, the support/sign secret space has at most
  2^h * C(16384,h)
possibilities. At h=3:
  log2(2^3*C(16384,3)) = 42.4147733205 bits.

Hence h<=3 cannot provide a 100-bit secret-space entropy ceiling, independently of lattice-estimator details. Aung §6.1 reports at least 100-bit security for its implementation. Therefore the only h values that could satisfy the inherited Pdagger proof necessity are incompatible with preserving that security target.

No claim is made that the public Aung paper exposes its exact hidden implementation hwt; the result is conditional and stronger:
  any h>=4 fails this proof gate on Pdagger,
  while h<=3 cannot serve as a 100-bit-security-preserving repair.

## 4. Classification

FAIL_NODE_SPECIFIC_BOOKKEEPING_RESCUE_ON_INHERITED_PREFIX.
FAIL_SECURITY_PRESERVING_HWT_RESCUE_ON_INHERITED_PREFIX.
PASS_ISOLATION_OF_ROUNDING_FLOOR_AS_CURRENT_PROOF_BLOCKER.

This is still NOT an actual ciphertext correctness counterexample.
It does NOT prove F_e(F_e(z)) is mathematically wrong.
It does NOT prove HElib's real runtime noise exceeds the threshold.
It proves that the current estimator-independent coefficient-L1 architecture, when combined with the inherited mod-down rounding certificate R and the Turn22 fixed prefix window, cannot certify the second Fe first square under a security-compatible secret-key regime.

Thus Turn1's obstruction is not merely caused by replacing q-dependent EF(q) with the global EFhat.

## 5. Why the candidate is not killed yet

Turn22 previously established that the first F5 outer multiplication has a conservative safe interval:
  182.4978960136 < log2 q < 353.5343333566.

For the pinned default h=120, the new *necessary* second-square floor only requires:
  log2 q > 293.1246498573.

These intervals overlap:
  293.1246498573 < log2 q < 353.5343333566.

This overlap is NOT a PASS and not yet a redesign proof. It only shows a credible bounded structural redesign remains: choose a larger proof-driven prefix jointly for the first and second Fe rather than freezing the first prefix immediately after crossing183 bits.

Therefore the active candidate remains ACTIVE rather than PARKED/KILLED, and FRONTIER_CANDIDATES_REMAINING=true.

## Verdict

Primary H2: FAIL.

Named uncertainty reduced:
The second-square blocker on the inherited Pdagger is not removable by exact q residue/K/factor bookkeeping while retaining the existing modulus-switch rounding certificate and a security-compatible secret-key regime.

Evidence grade: MATH / STATIC source audit.

Native recovery canary: NOT_EXECUTED.
Baseline correctness: PENDING.
Security gate: PENDING.
Value gate: PENDING.
Audit gate: PENDING.
Novelty: PREFLIGHT.
Paper: NOT_READY.

## Next decisive Paper-First test

Use the one allowed bounded structural redesign:
replace the first-crossing-183 prefix policy with a **joint two-Fe proof-driven prefix selector**. Under the pinned/default h=120 source certificate, solve the complete first-F5 envelope and the complete second-Fe first-square inequality on a common larger prefix q, not merely the necessary R^5 condition. Test whether any q in the already-source-valid first-F5 interval (especially the overlap beginning near 2^293.125) satisfies the full recurrence, exact BGV factor ledger, and same-prime-set constraints.

No Native action is authorized by this finding.
