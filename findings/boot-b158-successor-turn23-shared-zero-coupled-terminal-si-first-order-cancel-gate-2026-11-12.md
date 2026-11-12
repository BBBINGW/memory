# BOOT / B158_OVERALL — Successor Research Turn 23/25
Date: 2026-11-12 Asia/Singapore
TRACK_ID=BOOT
ACTIVE_SUBLINE=B158_OVERALL
PHASE=PROBLEM_SELECTION
CANDIDATE_ID=boot-b158-shared-encrypted-zero-terminal-operand-error-coupling-v1
STATUS=PARKED
VERDICT=FAIL_UNIVERSAL_FIRST_ORDER_ZERO_COUPLING / NO_CREDIBLE_NEW_MECHANISM
NATIVE/CODEX=NOT_RUN
research_frontier_exhausted=false

## Authority and read-before-write
Controller entry ACTIVE=UNKNOWN, backup none, immediately preceding valid Turn22 separately reexecuted as requested. Read and independently verified:
- findings/boot-b158-successor-turn22-valid-replay-l19-rescale-budget-invariant-gate-2026-11-12.md Git blob 832b0389f63f6de02dc3a6a107d43a7a33b6ce37, PARKED.
- findings/boot-B175-source-level-si-error-bounds-2026-10-29.md Git blob c75aa60e080b28b688de7ee8859c5df4d1951c02. LT8 required577, GROUPED required633, terminal required664 vs Qbits649; E_tref tensor/reference dominant, quant and relinearization insufficient.
- findings/boot-B174-audit-si-grouped-marginal-and-pointwise-gate-2026-10-28.md Git blob ffffc7e6a9c56ff0e4208a5c5ff5fe2cb786cf29. Exact plaintext GROUPED at physical packed slot j is y^(j mod8), y=x^8192; at j=0, GROUPED=1 for every x. Full grouped has 3-case native audited correctness restricted to endpoint.
- Lattigo v6.2.0 schemes/bgv/evaluator.go Git blob 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f. Stock ciphertext arithmetic and SI tensor quantization.
Closest mechanisms: ordinary public shared encryption-of-zero rerandomization, correlated noise, B175 post-claim analysis. Not Turn10 compensated *plaintext* affine recentering (which changes plaintext representatives with add-back correction); this candidate changes only the error correlation and keeps both plaintext operands exactly unchanged. Also different from previous unmerged rails, L19 modulus, scalar-mask scale factor.

## One pre-registered paper-level decisive question
QUESTION: Can two public constants alpha,beta (or static per-slot constants), applied to ONE shared public/encrypted-zero ciphertext Z in A'=A+alpha Z and B'=B+beta Z, deterministically cancel the leading terminal SI cross-error in the B175 LT8-by-GROUPED product for ALL legal phases and arbitrary public LUT functions while preserving every plaintext output, without new ciphertext multiplications or input-dependent encrypted controls?
CURRENT_BELIEF: No. The first-order error coefficient from Z is alpha*GROUPED_plain + beta*LT8_plain, which cannot vanish on the full functional family if LT8 varies while GROUPED is 1 in slot0. Exact SI Q-centered carry may further complicate; it cannot turn failed necessary first-order invariant into a proven universal cancellation mechanism.
CHEAPEST_DECISIVE_TEST: Symbolically expand the two noise-coupled ciphertext products, use SOURCE-AUTHENTICATED B174 packed slot j0 GROUPED=1, instantiate the legally representable arbitrary LUT polynomial F(X)=X so LT8(slot0)=x, and compare two distinct legal phase inputs x. Avoid native, zero cipher generation and benchmarking.
IF_PASS: If a nonzero alpha,beta with source-backed identities cancels first-order injected cross terms for all x and full polynomial outputs (and supports carry-aware 16bit improvement), retain ACTIVE for key/security/noise and full all-in value gates.
IF_FAIL: If universal cancellation forces alpha=beta=0, PARK this precise input-independent shared-Z coupling; do not falsely infer an impossibility for adaptive or nonlinear error cancellation.
IF_UNCLEAR: If stock source exposes a distinct dynamic per-slot correction or decrypted/raw residual information, leave such differently specified mechanisms UNKNOWN and require exact type/security/cost evidence; no new native.
WHICH_PAPER_GATE_CHANGES: exact whole-output and zero-mask semantics, algebraic tensor-reference noise mechanism, and credible >=16-bit fixed-Q rescue/value. Source primitive compatibility and all legal inputs matter.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: A fixed public zero-correlation method would be a minimal same-modulus repair to B175's dominant terminal tensor error; if algebraically incapable of generic first-order cancellation, spending on native DFR or security is unjustified.

## Source-grounded semantics and exact algebraic obstruction
Let A and B be the decoded ideal plaintext values of LT8 and GROUPED for a chosen packed slot, and write actual lifts as A+eA and B+eB in a formal small-error model before modular Q wrap/quantization. Let Z be an independently supplied RLWE encryption of plaintext zero whose decryption error is z. For public fixed coupling scalars alpha,beta, A'=A+eA+alpha*z and B'=B+eB+beta*z retain the SAME plaintexts. Ignoring final Q/T quantization solely for the *necessary algebraic leading-term test*, the difference in their product due to Z is exactly:
  (A+eA+alpha z)(B+eB+beta z) - (A+eA)(B+eB)
  = z[alpha (B+eB) + beta (A+eA)] + alpha*beta*z^2.
The coefficient of z at plaintext/error-independent first order is alpha*B+beta*A. To have deterministic universal first-order cancellation of the injected shared-Z effect, necessarily alpha*B(x)+beta*A(x)=0 for all legal x at each targeted slot. This condition is necessary only for the candidate's claimed universal *exact cancellation*, NOT for every possible statistical noise improvement or exact SI carry treatment.

B174 source-authenticated full-domain plaintext target for packed slot j: GROUPED(j)=y^(j mod8), where y=x^8192. Therefore B(0)=1 for every phase x, including x=0 and all nonzero x. The B175 LT8(j) is a public-coefficient weighted baby-basis polynomial block. For a permitted arbitrary LUT polynomial F(X)=X (set first block coefficients so coefficient of x is one and all others zero), LT8(slot0) has ideal plaintext A(x)=x. Then for j=0, universal cancellation requires
   alpha + beta*x = 0 for every legal x.
Two distinct legal phases (e.g. x=0 and x=128 in the source's 512-message phase model) yield alpha=0 and 128*beta=0 mod65537; since 128 !=0 mod65537, beta=0. Even if alpha,beta are allowed to depend on the public function F or slot index, they remain constants at slot0 for this fixed F and must vanish. Hence there is no nontrivial static shared-zero coupling that gives the claimed universal first-order cancellation for arbitrary F on all legal x.

Check that F=X is a valid public polynomial in the arbitrary-LUT *algebraic evaluation contract*, but do not assert it is necessarily a valid 512-message error-plateau LUT under every bootstrapping semantic: an implementation may restrict LUT polynomial values on phase intervals. If the paper contract is strictly plateau functions rather than arbitrary F, the same obstruction follows whenever two legal x with the same nonzero GROUPED(slot0)=1 produce distinct LT8(slot0), and source has not independently provided a sufficient pair in the 512-message LUT family. Therefore this result is a strict no-go for the candidate's *arbitrary-public-LUT polynomial evaluation* claim, not a theorem forbidding correlated-noise optimizations on an arbitrarily restricted function family.

Furthermore, adding correlated encrypted zero is an extra encryption/ciphertext/operation, not necessarily zero system cost; Z noise magnitude/correlation and scales may be adversely amplified by SI tensor and carry. It is invalid to assert measured noise or a general lower bound for adaptive source-informed coupling from this algebraic test.
Source feasibility: adding ciphertext multiples of shared Z is representable with stock add/public scalar operations subject to scale/level matching; encrypted Z provenance, key, security and exact Q/T reference/carry remain unverified. The equality with ideal products preserves plaintext for correct ciphertexts but no full SI decrypted correctness/DFR established.
No native experiment warranted because the universal first-order cancellation necessary condition already fails. No meaningful standalone novelty beyond generic shared-zero rerandomization; NOVELTY_STATUS=PREFLIGHT, not an independently confirmed collision.
Dominant E_tref bitlength647 and B175 deficit15 are unchanged from audited baseline.

## Scientific disposition
Killer gate1: algebraic plaintext preservation holds in ideal ring, but advertised universal first-order cancellation fails on a legal arbitrary polynomial F=X, two phases at slot0.
Killer gate2: stock add/scalar supported in principle; exact enc0 scale/key/carry compatibility unknown; no need to execute since first gate failed.
Killer gate3: BLOCKED/FAIL_HYPOTHESIS: no demonstrated 16bit reduction and extra Z operation/key/memory costs.
STATUS=PARKED; NEW_MECHANISM=NO_CREDIBLE_NEW_MECHANISM; no active or backup after this turn. Research frontier remains NOT PROVEN exhausted.
REOPEN_CONDITION: A different concrete correlation protocol satisfying full message-plateau and zero-root semantics with data-dependent or structurally nonconstant, source-compatible coefficients, a verifiable source-level E_tref cancellation bound across all valid inputs, fixed-Q DFR >=16bit recovery, complete security, low all-in keys/memory/offline costs, and independent novelty. Repackaging constant alpha/beta is not such evidence.
ELIMINATED_UNCERTAINTY: Can fixed public shared-zero coefficients alpha,beta universally eliminate first-order correlated error for arbitrary public polynomial evaluation under B175's exact slot0 GROUPED=1? No: F=X forces alpha=beta=0. The theorem is scoped to the stated public-polynomial contract.
DECISION_CHANGED=true; VALUE_REVIEW_COMPLETED=false (Turn21 already completed a value review); no new native task.
