# BOOT / B158 — Successor Research Turn 4 — second-Fe cubic P6 proof no-go and candidate parking

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: legacy-484479fe4613
PHASE: CORRECTNESS_GATE
Native execution: NONE

## Authority / read-before-write

GitHub Notes repository state was recovered first. The current durable predecessor is successor Turn3:
  findings/boot-RMFE-postdivide-successor-turn3-joint-two-Fe-prefix51-static-rescue-2026-11-03.md
  blob 9ffb4ee115168637deafedb71b0c16017abcc924
  commit 5a420e026cea3f4bf7a7843cef054960c09efc4d.

A direct repository commit search shows 5a420e0... as the current latest memory commit before this write. The PI-supplied fallback excerpt still names the older fdbf8cc... local head, so it is treated as a stale fallback excerpt rather than used to erase the already-persisted Turn2/Turn3 results in this same logical session.

Read-only prerequisites:
- Turn3 P6 rescue blob 9ffb4ee115168637deafedb71b0c16017abcc924;
- Turn16 L0-L3 absolute envelope blob 07a0d58addfba66d3302ebf6cb42a2049ab51a76;
- Turn24 first-divide semantics blob 6e5d3c92fda4431801f81632679e8636d177d352.

The target path was checked absent before write.

## Closest prior / exact delta

Closest prior remains Aung Algorithm4's sequential application u_0,2=F_e(u_0,1)=F_e(F_e(z)) together with pinned HElib BGV fixed-target multiplication semantics.

Turn3's bounded structural redesign changed the candidate build/prefix policy to:
  HELIB_SP_NBITS=51,
  common first-six-ctxt-prime prefix P6,
and proved:
- complete first F5 at P6;
- first square of the second F5 at the same P6.

This turn tests whether that ONE bounded redesign actually carries through the next source-order node, the second-F5 cubic multiplication. No second redesign is introduced.

## One primary hypothesis / falsifier

H4:
The Turn3 P6 construction can propagate the same estimator-independent coefficient-L1 proof through the remaining second-F5 cubic branch
  W*(W^2-6)+(W-1),
where W=F5(z), without changing modulus, proof architecture, or evaluation schedule.

Cheapest falsifier:
evaluate only the first still-unclosed multiplication
  W*(W^2-6).
If its certified envelope already exceeds 0.48q for every source-possible P6, stop; later sibling, L2 subtraction, and divide cannot restore correctness of an already-unclosed intermediate ciphertext.

## 1. Frozen P6/input certificate from Turn3

For every source-possible P6 under HELIB_SP_NBITS=51:
  q_min = 117649 * 2^288,
  q_min <= q < q_max = 2^306.

Turn3's uniform complete first-F5 output certificate is:
  B =
  97,631,199,420,645,816,100,334,968,529,769,915,061,277,924

with:
  log2(B) ~= 146.130250335083.

Using Khat=401,679,183,790,909, the second-F5 first square certificate is:
  E2 = B^2 + Khat
     = 9,531,851,100,313,911,937,361,317,161,094,233,434,267,322,720,975,555,918,260,207,991,326,490,181,869,583,153,540,685

and:
  log2(E2) ~= 292.260500670166.

At q_min:
  log2(0.48 q_min) ~= 303.785235843292,
so the square retains Turn3's ~11.524735-bit uniform margin.

## 2. The very next cubic multiplication fails decisively

Source-faithful second-F5 evaluation forms:
  W2 = W^2,
  W2m6 = W2 - 6,
  M = W * W2m6.

The same independent recurrence used for the first F5 gives:
  E_M <= B*(E2 + 1872) + Khat.

Using the frozen uniform B:
  E_M =
  930,606,055,622,649,783,863,419,613,880,847,398,216,709,089,094,629,647,264,387,971,126,922,497,991,837,407,636,038,475,452,058,664,289,624,476,122,198,865,568,795,322,402,577.

Thus:
  log2(E_M) ~= 438.390751005249.

The LARGEST correctness threshold available to any P6 is below:
  log2(0.48*2^306)
  ~= 304.941106310946.

Hence the certified cubic multiplication exceeds even the maximal P6 threshold by:
  > 133.449644694302 bits.

Exact integer failure certificate:
  25*E_M
  =
  23,265,151,390,566,244,596,585,490,347,021,184,955,417,727,227,365,741,181,609,699,278,173,062,449,795,935,190,900,961,886,301,466,607,240,611,903,054,971,639,219,883,060,064,425

while
  12*2^306
  =
  1,564,443,629,824,885,314,254,166,288,698,402,427,687,527,726,335,439,040,488,555,865,104,164,838,218,242,590,348,849,184,768,

so:
  25*E_M > 12*2^306 > 12*q
for every source-possible q on P6.

Therefore the second-F5 cubic branch is the first failing node after the Turn3 square PASS.

## 3. This is not an artifact of the uniform first-F5 number B

There is a stronger proof-architecture obstruction.

In the current coefficient-L1 recurrence, after the one initial mod-down to P6:
  A = (q/Q0)E0 + R >= R
as an expression in the certified upper-bound ledger, with h=120:
  R = 619,520,000.

The complete first-F5 certificate is a sum of nonnegative terms whose leading multiplication chain contains A^5. Therefore:
  E_F5_cert >= A^5 >= R^5.

The second-F5 cubic certificate contains:
  E_cubic_cert >= E_F5_cert^3 >= R^15.

This is a lower bound on the VALUE OF THE CURRENT SUFFICIENT UPPER-BOUND EXPRESSION. It is NOT a lower bound on the actual ciphertext noise.

Numerically:
  log2(R^15) ~= 438.098634252361.

Even at q<2^306:
  log2(0.48q) < 304.941106310946,

so this proof-expression floor alone misses the P6 correctness threshold by:
  > 133.157527941414 bits.

Equivalently:
  25*R^15 > 12*2^306.

Thus exact q residues, exact K(q), or replacing worst-case 312 aligners by smaller actual residues cannot rescue the P6 cubic certificate while retaining the current one-mod-down coefficient-L1 proof architecture.

The Turn3 B certificate is itself only about0.09737 bits above R^5, so the 133-bit failure is not coming from a loose sibling/alignment constant.

## 4. BGV factor/type path is not the blocker

Let the first-F5 output factor be:
  alpha = d = a^5 q^4 mod625.

Second F5:
  factor(W^2) = beta = alpha^2 q = a^10 q^9 mod625;
  factor(W*(W^2-6)) = gamma = alpha*beta*q
                     = alpha^3 q^2
                     = a^15 q^14 mod625.

For the W-1 sibling, the explicit factor aligner would be:
  h = gamma * alpha^{-1}
    = alpha^2 q^2
    = a^10 q^10 mod625.

Since a and q are units modulo625, beta, gamma and h are units. A balanced public representative always exists with absolute value <=312.

Therefore this turn does NOT identify:
- a p-adic obstruction;
- an intFactor nonunit;
- a prime-set mismatch;
- or an implementation-interface failure at the cubic boundary.

The blocker is specifically the current independent coefficient-L1 correctness certificate.

## 5. Paper-first candidate decision

Turn2 identified an obstruction on the original Pdagger policy.
Turn3 consumed the protocol's one bounded structural redesign and established a genuine local rescue using P6/HELIB_SP_NBITS=51.
Turn4 shows that this redesign does NOT extend through the next required nonlinear node: the second-F5 cubic multiplication misses the proof threshold by >133 bits.

Possible ideas such as:
- another modulus switch inside the second F5;
- a different composed-polynomial/evaluation schedule for F5(F5(x));
- a fundamentally tighter certified modulus-switch rounding theorem;
would constitute a further structural redesign or a new mechanism. They are NOT pursued in this turn.

Under the paper-first bounded-redesign rule, the current candidate therefore no longer has a credible complete-correctness path within its authorized design budget.

Candidate decision:
  PARK legacy-484479fe4613.

This is NOT a theorem that the actual ciphertext algorithm fails.
It is NOT a strict no-go for every possible representation/evaluation of repeated F_e.
It is a decisive failure of the current candidate construction/proof architecture after its one permitted bounded structural redesign.

## Verdict

FAIL_P6_SECOND_FE_CUBIC_INDEPENDENT_L1_GATE.
PASS_FACTOR_AND_TYPE_FEASIBILITY_AT_THE_FAILED_NODE.
FAIL_BOUNDED_STRUCTURAL_REDESIGN_TO_REACH_COMPLETE_SECOND_FE.
PARK_CURRENT_CANDIDATE.

CORRECTNESS_GATE:
  FAIL for this paper candidate construction/proof route.

NATIVE:
  NOT EXECUTED.

Mandatory recovery canary:
  NOT_EXECUTED; do not infer a result.

Novelty:
  PREFLIGHT.

Security:
  PENDING.

Value:
  PENDING.

Baseline:
  PENDING.

Audit:
  PENDING.

Paper:
  NOT_READY.

## Reopen condition

Reopen legacy-484479fe4613 only with genuinely new evidence/technique that changes the failed cubic certificate, for example:
- a certified tighter modulus-switch rounding theorem that materially removes the R-driven proof floor;
- a separately justified repeated-F_e evaluation representation/schedule that avoids this cubic growth while preserving the candidate's cost thesis;
- or later native/raw evidence that motivates and supports a new proof architecture.

Do not reopen merely by choosing another P6 residue, shrinking K, or using smaller unit aligners.

## Next research action

No ranked BACKUP candidate is currently durable.

The authorized BOOT research frontier is not exhausted. The next substantive turn should autonomously reprioritize/prescout exactly one new BOOT paper candidate or previously parked family whose explicit reopen condition is now plausibly satisfied, rather than spending another local redesign turn on legacy-484479fe4613.

No Native execution is authorized by this finding.
