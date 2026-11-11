# BOOT / B158_OVERALL — successor Research Turn 4/25
Date: 2026-11-12 (Asia/Singapore)
Phase: PROBLEM_SELECTION
Candidate: boot-b158-period8-reynolds-output-projector-v1
Verdict: FAIL_UNIVERSAL_ERROR_CONTRACTION / FAIL_SOURCE_BACKED_DFR_VALUE -> PARKED
Native/Codex: NOT_RUN
Novelty: PREFLIGHT (not CLEAR)

## Read-before-write authority
Durable predecessor Turn3 findings/boot-b158-successor-turn3-fullpoly-direct-lt-expansion-source-correctness-gate-2026-11-12.md, verified blob 83a53e279980830b007b1bf007be51def3fd2ea9, status PARKED.
Turn2 findings/boot-b158-successor-turn2-fullslot-trace-qcarry-modulus-compatibility-gate-2026-11-12.md, verified blob 1743982b6ef24046a92aeb2449e93b4e21bb20d1, status PARKED; this earlier candidate attempted trace to annihilate Q-carry after modulus extension, whereas this distinct candidate performs SAME-Q output-subspace error projection after SI.
B175 raw audit findings/boot-B175-audit-direct-si-pointwise-noise-failure-2026-10-28.md, blob a9e8fe850c86a77717836ad414f8b6192290dd9a, native ZIP SHA256 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa; correct inputs, final SI required bits 664, Q bitlength 649, budget -15, 32767/32768 slot mismatches.
B175 source attribution findings/boot-B175-source-level-si-error-bounds-2026-10-29.md, blob c75aa60e080b28b688de7ee8859c5df4d1951c02; dominant aggregate E_tref unseparated, quant and relin terms tiny relative to observed.
B174 subgroup reference findings/boot-B174-audit-si-grouped-marginal-and-pointwise-gate-2026-10-28.md: GROUPED(j)=y^(j mod 8) at tested cases. B175 independent reference: public LT block sums indexed j mod8, hence reference product is period-eight in physical slots in fixed test. A full legal-domain invariant requires additional proof; the bounded primary gate assumes that period-eight target.
Closest prior art: classical Reynolds averaging / subgroup trace over cyclotomic automorphisms and stock BGV rotations; B170 ParallelLT already uses rotation-sum linear operations. No independent novelty audit performed.

## Registered question and decisions
QUESTION: Can the free public-linear projection onto the period-eight slot-invariant subspace, applied after B175 final failing SI, retain all intended output slots and certify >=16 required-bit noise recovery without new secrets, ciphertext multiplications or custom modulus backend?
CURRENT_BELIEF: The intended period-eight plaintext is invariant, but its invariant residual components are unaffected by exact projection, and stock plaintext modulus normalization can magnify them.
CHEAPEST_DECISIVE_TEST: Define the rotation-eight subgroup and its Reynolds operator; check exact invariant message and error action over R_Q and the small signed inverse of subgroup size mod T. Use an explicit invariant nonzero error witness. No native execution.
IF_PASS: If a verifiable distributional or algebraic mechanism contracts all legally occurring dominant B175 errors while preserving whole-output, retain ACTIVE and audit source interface, noise/DFR, security and complete conversion/rotation/key/memory costs.
IF_FAIL: If invariant error survives while the necessary plaintext normalization does not give a useful bound, PARK: output redundancy alone cannot guarantee the fixed-Q margin.
IF_UNCLEAR: Inspect exact slot permutation or source scalar-encoding representation, retain UNKNOWN, do not initiate native experiments.
WHICH_PAPER_GATE_CHANGES: correctness/whole output (gate 1) then stock source (gate 2) and end-to-end value/noise (gate 3).
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: Saving 16 required bits demands an actual contraction of dominant E_tref. If a valid residual subspace is fixed by the candidate, additional rotations without a DFR proof are not a credible paper mechanism.

## Exact algebra
Let N=32768 and T=65537. BGV slot layout comprises two rows each length N/2=16384. A rotation by eight columns is a Galois automorphism tau; its subgroup H=<tau> has size d=16384/gcd(16384,8)=2048. Let S=Fix(H) in R_T or R_Q; its plaintext slots repeat every eight columns in each row. For target m with this exact periodicity, sigma_h(m)=m for all h in H. If additionally rows match, this is still true.

Because Q is a product of ODD RNS primes, d is invertible modulo Q. Define the exact Q-ring Reynolds projector:
  P_Q := d^{-1} (mod Q) * sum_{h in H} sigma_h.
For every v in Fix(H), P_Q(v)=v exactly mod Q; hence for any m,e in Fix(H), P_Q(m+e)=m+e. In particular e=1 lies in Fix(H) and has ||rho_Q(e)||_infty=1, and the projected residual is the same e. There cannot be a deterministic factor-2, let alone factor-2^16, universal reduction of coefficient-infinity norm on arbitrary invariant residuals. This alone does NOT rule out a distribution-specific benefit on mostly non-invariant real errors.

Plaintext T-normalization: the intended projection under R_T can be written λ * sum_h sigma_h where λ≡d^{-1} (mod T). Since d=2048=2^11 and T=2^16+1=65537, d*(-32)=-65536=1-T. Thus the minimum-absolute-integer representative is λ=-32, and any integer lift λ=-32+kT has |λ|>=32.
If source permits an ideal signed scalar -32 effective Q-lift, the unnormalized trace of invariant residual e is d*e, so the normalized trace contribution is (-32)*2048*e=-65536e in ordinary integer arithmetic. For e=1 and Q≫65536, there is no Q wrap and the actual coefficient error magnitude is 65536, not 1. Actual stock RingT2Q canonical plaintext lifting could use λ mod T=65505 instead, making this integer multiplier even larger, so -32 is an optimistically favorable lift, not a claim of a stock exact call. For nonzero plaintext, compare the *complete* reference/carry, not just λ d e; no complete source-compatible residual formula was derived for this candidate.
A Q-normalized trace P_Q with d^{-1} modulo Q avoids that scalar amplification but is identity on all invariant residuals. Its scalar representative may be huge and its BGV scale/encoding behavior requires additional type/parameter proof.

## Probabilistic and cost boundaries
A conditional idealized independent equal-variance model for d=2048 independent additive noise samples yields only sqrt(d) reduction in standard deviation, i.e. 0.5*log2(2048)=5.5 bits, versus the approximately 16-bit B175 conditional target. This is an illustration under independent-samples assumptions, NOT an upper bound on possible special noise distributions: rotations of the SAME ciphertext are correlated, not 2048 independent encryptions, and projection can delete entire anti-invariant error components. No actual B175 E_tref component/covariance trace is persisted; no transferable DFR claim exists.
The subgroup trace sum can be implemented as 11 doubling stages, each involving a Galois automorphism/rotation and an addition, rather than 2047 separate rotations, assuming the necessary keys are available; it adds online operations and potentially key material. Key overlap with B175 existing keys UNKNOWN. It removes zero ct-ct multiplications and changes no failing SI tensor itself. It may change decoded ciphertext semantics because plaintext normalization, coefficient carrying and other scale factors must be counted. There is no demonstrated fixed-Q positive budget or independent full-system value.
Bounded conclusion: Exact Reynolds projection fails UNIVERSAL deterministic contraction. The distribution-specific possibility is UNKNOWN, not proven impossible. Because no source-backed DFR or useful 16-bit gain, no new paper mechanism is admitted. Do not native search on one trace.

## Gates and disposition
Gate 1: conditional period-eight plaintext invariant established; complete Q/T reference/carry and general legal-domain correctness still UNKNOWN/BLOCKED.
Gate 2: Galois rotations and linear combination are stock, but Q-normalization and BGV scale may require a nontrivial public scalar interface and keys. No source-distinct noise-control primitive identified.
Gate 3: FAIL credible fixed-Q value mechanism, as invariant error subspace cannot be contracted, extra rotations and keys are paid, and no DFR/tensor error distribution is available.
STATUS PARKED; NEW_MECHANISM=NO_CREDIBLE_NEW_MECHANISM for deterministic or unsupported statistical redundancy averaging.
REOPEN_CONDITION: Supply an actual B175 legal-domain correlated error model plus verified source-level coefficient lifts/reference carries showing useful probability-mass contraction >=16 required bits, with exact whole-output scale/carry semantics, all rotations/key memory/noise costs and prior-art-distinct value. Repeating different rotation subgroup sizes or assuming i.i.d. errors from one ciphertext does not satisfy it.
ELIMINATED_UNCERTAINTY: Does a message-preserving period-eight Galois projector automatically contract all possible coefficient errors, or can small plaintext normalization deliver free averaging of a common error? No: invariant residual e=1 is fixed by exact Q projection and the smallest signed plaintext inverse induces integer gain -65536.
DECISION_CHANGED=true; reason: proposed candidate PARKED before native experiment.
EVIDENCE_GRADE=MATH. Scientific scope is exact linear algebra on Q-ring and plaintext scalar representatives, not a B175 distributional DFR theorem.
