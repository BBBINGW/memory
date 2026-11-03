# BOOT / B158 — Successor Research Turn 1 — second F_e fixed-prefix square-envelope gate

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: legacy-484479fe4613
PHASE: CORRECTNESS_GATE
Native: NOT EXECUTED

## Authority / evidence
PI-provided verified local authority: BBBINGW/memory main HEAD=origin/main=822967e31a8f211485e27e3fd648176f14dd3165, one handoff commit ahead of Turn25 checkpoint 1f66e1c7239fd3e48e22bd8f71c8ff57cf6d2fb2; direct GitHub compare confirms the single added handoff file. The local clone itself is not mounted in this runtime. GitHub Notes read returned empty objects for existing files; exact earlier findings were recovered read-only from connected GitHub by their verified blobs: Turn25 7b771044128b4896401305500a25c52a2743d43d, Turn24 6e5d3c92fda4431801f81632679e8636d177d352, Turn23 3afdaa04beb223e630acc5196901d55bfb785b04, Turn16 07a0d58addfba66d3302ebf6cb42a2049ab51a76. These are repo artifacts; no local HEAD was independently checked and no connector reading changes the PI's authority precedence.

## One primary hypothesis
H: Reusing the fixed P with 183<=log2(q)<247 and the already-certified independent Turn23 F5 output envelope, a source-identical *second* F5 can be propagated through its first ciphertext square using the existing triangle/submultiplicative coefficient-L1 proof rule and remain below the 0.48q correctness threshold, enabling a uniform second 625->125 proof without any new technique.

Cheapest falsifier: substitute the frozen first-F5 bound in the existing relin square rule E_sq<=E_W^2+K(q), and compare its sufficient certificate with 0.48q across the entire original P window. No new native work.

Closest prior: Aung Algorithm4 source-order u_0,2=F_e(F_e(z)) and pinned HElib BGV multiply/relinearize. Delta: isolate the inherited independent-envelope failure at the **first square of the second F_e**, while separately confirming exact p-adic and factor feasibility. This is not a novelty claim.

## Reused frozen inputs
p=5, ptxtSpace=625, a=67, q=product(P) unit mod625, W=F5(z)=z^5-5z^3+5z.
Turn23 factor(W)=d=a^5*q^4 mod625 and uniform independent envelope E_W(q)<EFhat=4155105766733618287140112599228004062478100413979797319, log2(EFhat)=181.4390023246677.
Turn16 full-Q0 coefficient L2 envelope: B2<=A2*E_leaf with A2=240082 and E_leaf_hat=10098509880614386188547250535619. L2 begins with factor a and can be modded to the same P under inherited mod-down assumptions.

## Exact semantics and factor ledger (algebraic, not native)
For the source-identical F5 polynomial template applied to W, its ciphertext square W2 has factor d^2*q mod625. Every multiplication of BGV ciphertexts on the common P contributes one additional q in the factor. The leading degree-5 term therefore has factor
  D=d^5*q^4=a^25*q^24 mod625.
Any other polynomial branch must be explicitly unit-factor-aligned to D, as in Turn23; the original L2(z) with factor a can be aligned by
  h2=D*a^{-1}=a^24*q^24 mod625.
Both are units; every balanced representative h2 satisfies |h2|<=312. The internal mulIntFactor implementation contract remains private/helper-dependent. A same-P, same-625, same-factor subtraction is algebraically available, but is NOT proven noise-safe.

Exact mod-5 divisibility is independent of arbitrary higher lifts: writing z=sum_t b_t phi(e_t) in Z625, F5(x)≡x^5 (mod5) and therefore F5(F5(z))≡z^25≡sum_t (b_t mod5)phi(e_t)^25 (mod5); L2(z) has the same mod5 reduction by its correction-definition. Thus L2(z)-F5(F5(z)) is 5-divisible. Conditional on exact ciphertext correctness at the numerator, divideByP would preserve P, change ptxtSpace625->125, and reduce D mod125 as a unit. This is algebra/type feasibility, not a full ciphertext correctness certificate.

## Decisive independent-envelope test
The **same** inherited estimator-independent propagation that certified the first F5 uses, for second-stage square:
  E_W2(q) <= E_W(q)^2 + K(q).
Replacing the unknown actual E_W(q) by the *certified uniform upper bound* EFhat yields the reproducible sufficient certificate
  E_W2(q) < EFhat^2 + Khat,
  Khat=401679183790909.
log2(EFhat^2)=362.8780046493354.
Even at the LARGEST q of the original prefix window (q<2^247),
  log2(0.48q)<245.9411063109464,
so the propagated sufficient bound exceeds the maximum admissible threshold by >116.9368 bits. At q=2^183, the deficit is >180.9368 bits. Equivalently, an initial W envelope below sqrt(0.48q) (at q=2^183: ~2^90.9705531555) would be needed by this simple first-square sufficient test, whereas EFhat is ~2^181.4390.

**IMPORTANT LOGIC:** This is a falsification of H (uniform closure from the inherited EFhat and the same naïve square envelope), NOT evidence that E_W actually equals EFhat or that W2 actually decrypts incorrectly. An upper bound larger than the threshold cannot establish an actual failure, and no lower bound on actual noise has been shown. No native execution, sample attack, or p-adic obstruction. The first-F5 proof's ~0.5 bit margin is not composable by a second unconstrained multiplication using this ledger.

The L2 public-linear absolute envelope is not the dominant missing fact: it is negligible after mod-down compared with the frozen sufficient first-F5 upper bound; reducing B2 alone cannot repair the second-square certificate.

## Verdict / paper consequence
PASS_MATH_SECOND_BOUNDARY_MOD5_DIVISIBILITY.
PASS_STATIC_SECOND_BOUNDARY_UNIT_FACTOR_ALIGNMENT_FORMULA (private-helper implementation pending).
FAIL_INHERITED_UNIFORM_ENVELOPE_COMPOSITION_AT_SECOND_FE_FIRST_SQUARE.
UNCLEAR_ACTUAL_SECOND_BOUNDARY_CORRECTNESS.
CORRECTNESS_GATE remains BLOCKED, candidate ACTIVE.
Classification: **proof-envelope looseness / unclosed noise budget**, NOT demonstrated algorithmic/p-adic obstruction and NOT an implementation/interface failure. No strengthened claim about actual error distribution or DFR is made.

The selected one-step research question is resolved negatively: source-faithful second Fe cannot be certified by simply plugging the first Fe's *uniform worst-case* envelope into the previous square recurrence at any P in the inherited prefix window. It would be invalid to claim the full second divide proof is closed.

## Next decisive Paper-First test (no Native)
Reconstruct a node-specific, correlation-aware or algebraically reorganized *absolute* independent error bound for the first F5 output W (and its second-square input) at the **actual fixed P**, rather than a q-independent global worst-case EFhat; compare it with sqrt(0.48q), including the factor-aware multiply/relinearize contract. If no such bound clears the criterion, evaluate one bounded representation/evaluation-schedule redesign, then PARK/KILL if the gate truly fails. Do not reopen Turns23–25 and do not claim a native result.

Other gates: Novelty=PREFLIGHT; Security, Value, Baseline, Independent audit=PENDING; Paper=NOT_READY. Mandatory recovery-only native canary=NOT_EXECUTED.
