# BOOT — ePrint 2026/2368 B=64 window/correctness coverage gate

Date: 2026-10-30
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Session: 密码学 15.0 — Research Turn 12/25

Status:
FAIL_DETERMINISTIC_THEOREM_COVERAGE_FOR_B64_H32 /
PASS_EXPLICIT_PROBABILISTIC_WINDOW_COVERAGE_UNDER_IID_ROUNDING_MODEL /
PASS_REMARK5_NUMERIC_REPRODUCTION /
CONCRETE_DISCRETIZATION_FAILURE_BOUND_APPROX_2^-56.906 /
NO_SOURCE_MATH_ERROR_FOUND /
PARK_AS_EXPLICIT_CORRECTNESS_TRADEOFF

## Reprioritization context

The highest-priority 2026/1836 fused-prime A2B native task remains scientifically alive but is temporarily execution-blocked in this Chat runtime:
- local container cannot resolve github.com;
- GitHub integration is read/write for notes but branch creation is forbidden by integration (403 Resource not accessible by integration);
- no verified local clone of the author repository is mounted.

This is NOT a scientific failure of the 1836 candidate. Its pending task remains:
BOOT-1836-FUSED-P64-SECP256K1P-NATIVE-20261030-R12-01.

Per protocol, this turn reprioritizes to an independent BOOT source rather than spending another iteration on static analysis of the same fusion.

## Fresh source

Jung Hee Cheon, Kyungah Cho, Junyoung Jung, Junho Lim,
Low-Latency Parallel Digit Decomposition and Sign Evaluation for CKKS,
supplied PDF papers/supplied/2026-2368.pdf, Git blob SHA 6245413c027adb709f897bcc982426426e15dcfa, 27 physical pages.

Relevant source locations:
- pp2-4: one-bootstrap digit/sign overview and B>4E carry-zone condition;
- pp8-10: window equation, Lemmas 1-2 and prefix carry recurrence;
- pp12-13: Theorem 1 discretization error and Remarks 3-5;
- pp14-17: sign correctness and modulus-complexity statements;
- pp18-20: concrete experiments, N=2^16 and B=64.

## Primary hypothesis

The concrete B=64 experiment with sparse secret Hamming weight 32 is covered by the paper's deterministic discretization-error theorem and therefore satisfies the B>4E carry-zone condition without an additional probabilistic modeling assumption.

Cheapest falsifier:
plug hwt(s_tilde)=32 into Theorem 1, propagate its integer coefficient bound into the strict window hypothesis |epsilon_j|<E, and compare the smallest valid deterministic E with B=64.

## 1. Deterministic Theorem-1 bound

Theorem 1 gives for the inner-grid integer error polynomial epsilon:

||epsilon||_infinity <= ceil((hwt(s)+1)/2).

At hwt(s_tilde)=32:

ceil((32+1)/2) = 17.

Section 3.4 then states that the window displacement epsilon_j in equation (3) is:
- one coefficient of this integer epsilon;
- plus the difference between Disc(m) and the target two-digit quantity at that position, which is 0 or 1.

Therefore a worst-case integer bound is:

|epsilon_j| <= 18.

The window hypothesis is strict:

|epsilon_j| < E.

Hence the smallest integer E that deterministically covers every Theorem-1 case is:

E_det = 19.

Lemma 1 / Proposition 2 require:

B > 4E.

So deterministic coverage requires:

B > 76.

The experiment fixes B=64.

Therefore:

64 > 4*19 is false.

Result:
FAIL_DETERMINISTIC_THEOREM_COVERAGE_FOR_B64_H32.

## 2. This mismatch is explicitly acknowledged by the paper

Remark 5 states essentially the same boundary:
- worst-case ceil((hwt(s_tilde)+1)/2)=17;
- this would require B>4*19=76;
- the authors instead use a probabilistic rounding-remainder model.

Therefore this is NOT a hidden theorem contradiction and NOT a claim that the source proof is mathematically wrong.

The asymptotic claims are also explicitly conditional:
- Proposition 4: 'Under the window hypothesis (3)';
- Theorem 2: the discretized route comparison is likewise under the window hypothesis.

Thus the formal source carefully separates conditional theorem statements from the concrete probabilistic instantiation.

## 3. Exact reproduction of Remark-5 probability

Remark 5 models the hwt(s_tilde)+2 = 34 rounding remainders contributing to a coefficient of epsilon as independent Uniform[-1/2,1/2].

Let:

S = sum_{i=1}^{34} U_i, U_i iid Uniform[-1/2,1/2].

To choose E=15, the paper needs the coefficient part to satisfy |S|<14, because the additional sub-grid difference can add one integer unit.

For T=S+17, T is Irwin-Hall(34). By symmetry:

Pr[S >= 14] = Pr[T >= 31] = Pr[T <= 3].

The exact Irwin-Hall CDF at t=3 is:

Pr[T<=3] = 1/34! * sum_{k=0}^{3} (-1)^k C(34,k) (3-k)^34
          = 5.6486263173888698e-23.

Therefore:

Pr[|S|>=14] = 1.1297252634777740e-22
             = about 2^-72.906446.

Union bounding over N=2^16 coefficients gives:

2^16 * Pr[|S|>=14]
= 7.403767486727939e-18
= 2^-56.90644611949.

This independently reproduces the source's reported approximately 2^-56.9 value.

Result:
PASS_REMARK5_NUMERIC_REPRODUCTION.

## 4. Conditional B=64 correctness

On the event ||epsilon||_infinity < 14:
- the coefficient error magnitude is at most 13 because epsilon is integer;
- adding the 0/1 target-grid difference gives |epsilon_j| <=14;
- hence |epsilon_j|<15.

So choose:

E=15.

Then:

B=64 > 4E=60.

Therefore Lemma 1, Lemma 2, Proposition 1 and Proposition 2 become valid conditional on the probabilistic event.

Under the source's iid-uniform remainder model, one discretization over all N=2^16 coefficients has failure probability at most approximately:

2^-56.906.

## 5. B=64 imposes a concrete correctness ceiling in this model

For integer E and strict B>4E, B=64 permits at most:

E<=15.

Thus the window proof cannot use a looser E while retaining B=64.

Under the same iid-uniform 34-summand model, useful coefficient tail thresholds are:

|S|>=14: union bound 2^-56.906  -> E=15, B=64 passes;
|S|>=15: union bound 2^-76.795  -> E=16, but B>64 is required and B=64 fails;
|S|>=16: union bound 2^-110.795 -> E=17, but B>68 is required;
worst-case / deterministic: E=19 -> B>76.

Therefore the approximately 57-bit concrete bound is not merely a loose presentation choice while holding B=64 and this proof structure fixed. Tightening the tail threshold forces E upward and violates B>4E.

## 6. Cryptographic interpretation

The experiment's B=64/hwt32 correctness level should not be conflated with 128-bit lattice security.

The 2^-56.9 figure is:
- a decryption/carry-window failure estimate;
- for one discretization across N=2^16 coefficients;
- under an iid-uniform rounding-remainder heuristic;
- not an RLWE attack probability and not a reduction-based 128-bit security claim.

For repeated uses, a simple union bound scales this failure probability with the number of discretizations. For example, one million independent-or-union-bounded invocations would move the bound to roughly 2^-37 bits. This is only an arithmetic union-bound observation; independence across full protocol invocations is not asserted.

## 7. Experiment/source consistency

Section 5 fixes:
N=2^16, B=64.

The digit benchmark uses radix-64 and up to u=10 digits; the sign benchmark uses p up to 60 and one bootstrap.

Remark 5's numerical example uses exactly N=2^16 and hwt(s_tilde)=32, so it is clearly tailored to the concrete regime used by the implementation.

The experiment section reports empirical correctness over its tested samples, but the deterministic Theorem-1 bound alone does not certify that B=64 configuration.

## 8. Scientific value / novelty boundary

This turn does NOT identify a source error:
- the authors explicitly disclose the deterministic B>76 requirement;
- they explicitly label the B=64 rescue as a probabilistic model;
- formal asymptotic propositions retain the window-hypothesis condition.

The result is instead a precise parameter/correctness boundary:

the attractive radix-64 one-bootstrap configuration trades deterministic theorem coverage for an approximately 57-bit heuristic discretization-failure bound.

A trivial repair is to increase B (e.g. a larger radix such as 128), but that changes the B^2 lookup domain and is a parameter trade-off rather than a nontrivial research contribution.

A potentially nontrivial continuation would require either:
1. a rigorous distributional tail theorem for the actual correlated CKKS rounding remainders that yields stronger bounds than the heuristic iid model, or
2. a carry/window representation tolerating larger E at B=64 without expanding the root/LUT domain.

Neither mechanism is established in this turn.

## Verdict

FAIL_DETERMINISTIC_THEOREM_COVERAGE_FOR_B64_H32.
PASS_EXPLICIT_PROBABILISTIC_WINDOW_COVERAGE_UNDER_IID_ROUNDING_MODEL.
PASS_REMARK5_NUMERIC_REPRODUCTION.
CONCRETE_ONE-DISCRETIZATION_FAILURE_BOUND_APPROX_2^-56.906.
NO_SOURCE_MATH_ERROR_FOUND.

AI_PROVISIONAL_CHOICE:
PARK 2026/2368 as a source-correct but explicitly probabilistic correctness trade-off; do not pursue a trivial larger-B parameter tweak.

TOP_LEVEL_BOOT_FRONTIER_EXHAUSTED: false.
PENDING_PI_DECISIONS: none.
PENDING_CODEX_TASKS:
- BOOT-1836-FUSED-P64-SECP256K1P-NATIVE-20261030-R12-01 remains pending/execution-blocked in this runtime.