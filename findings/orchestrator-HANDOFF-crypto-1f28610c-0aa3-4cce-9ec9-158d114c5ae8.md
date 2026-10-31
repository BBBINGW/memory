# 密码学 18.0 handoff

Resume research — Session Handoff

你现在继续担任我的 FHE Bootstrapping Research Student，我是 PI，负责最终科研方向、论文贡献判断、实验授权与决策。

这是 同一个 BOOT 研究程序的 successor session，不是重新开始，也不是新研究主题。

0. Session identity
YAML
NEXT_CONVERSATION_NAME: 密码学 18.0

TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

LATEST_COMPLETED:
  Research Turn 25/25 — end-to-end static semantic-equivalence gate

NEXT_ITERATION:
  Resume from this handoff.
  If pending native result has arrived, it MUST preempt the next free substantive turn for independent audit.
  If it remains pending, begin a fresh session-local substantive-turn budget and choose ONE highest-EIG independent BOOT unit.

CURRENT_STATUS:
  SESSION_RESEARCH_COMPLETE / HANDOFF_COMPLETE

CONTINUOUS_AUTONOMOUS_RESEARCH: true
NEXT_ITERATION_REQUIRES_PI_AUTHORIZATION: false

PENDING_PI_DECISIONS: none

The completed session had Research Turns 1–25. The immediately preceding Turn 26 was HANDOFF ONLY and did not perform new research.

The read-before-write Git checkpoint succeeded at:

纯文本
BBBINGW/memory main@88bf6af45632bc3e0afcaf3d08740782b0c4779f

Use that checkpoint as the durable successor-session authority.

Do not silently replace this authority with stale conversational memory. At session start, restore from GitHub Notes if healthy; if connector access fails, use the verified authority material in this handoff/local clone. Do not stop merely because the connector is unavailable.

1. Research philosophy and operating discipline

Follow:

纯文本
smallest falsifiable claim
→ cheapest decisive test
→ minimal verification
→ expand only if warranted

Core philosophy:

先证明有洞，再想怎么填；先 falsify，再 optimize。

One substantive research turn should normally contain:

纯文本
ONE primary hypothesis
+
ONE cheapest decisive test

Always pre-state or make explicit the falsifier:

What result would make us stop believing this hypothesis?

A failed candidate/family must be parked or killed, then autonomously reprioritized within the same top-level BOOT objective.

Do not WAIT_PI merely because:

one candidate failed;
one experiment is pending;
one advisory PI decision exists;
Codex is occupied.

PENDING_PI_DECISION is a durable advisory queue, not automatically blocking.

Use:

纯文本
pending PI decision + independent work available
=> continue reversible/no-regret research

pending PI decision + no independent work
=> WAIT_PI

WAIT_PI or STOP is allowed only if the top-level BOOT research frontier is genuinely exhausted and must explicitly declare:

纯文本
research_frontier_exhausted: true

Candidate/family substantive-turn soft/hard budgets remain:

纯文本
soft: 8
hard: 12

Do not spend turns on low-value work merely to stay active.

2. Completed session headline result

Turn 25 result:

纯文本
PASS_STATIC_END_TO_END_PLAINTEXT_SEMANTIC_EQUIVALENCE

Finding:

纯文本
findings/boot-RMFE-end-to-end-static-semantic-equivalence-gate-2026-11-01.md

Turn-25 substantive commit:

纯文本
56597dfabaf7047a9be26b94172451a29ad356f2

The session then completed a handoff-only state transfer.

Full saved handoff finding:

纯文本
findings/boot-HANDOFF-post-turn25-paired-throughput-native-pending-2026-11-01.md

Latest read-before-write checkpoint supplied for successor authority:

纯文本
88bf6af45632bc3e0afcaf3d08740782b0c4779f
3. Strongest surviving candidate

Current p=5, w=512, k=5 correction-style candidate:

纯文本
Aung SlotsToCtxts
→ 5 × (
    thin SlotsToCoeff
    → reLinearize(recryptKeyID)
    → rawModSwitch
  )

→ aggregate TWO typed raw channels
→ public carry-cocycle correction
→ one aggregate divisibility-lift/divide per channel
→ one reconstruction with the ACTUAL shared recryptEkey
→ RM10
→ ×224 normalization
→ joint rank-5 recovery
→ four outputs L0(z), L1(z), L2(z), L3(z)
→ stock Aung correction DigitExtract / final recode

with:

纯文本
L0(z) = z

The candidate deliberately keeps rawModSwitch branchwise. Exact aggregate-only fusion before branch-local raw representative selection is killed.

4. Turn-25 end-to-end static correctness closure

Under the persisted implementation/type assertions:

纯文本
branch prefix through rawModSwitch:
  source-identical

post-raw carry/divisibility fusion:
  exact branch-equivalent

raw channels:
  exactly two
  typed separately
  no cross-mixing

single recryptEkey reconstruction:
  exact CtxtPart equality to shifted sum of five stock reconstructions

RM10 × 224:
  exact normalized Reynolds / relative-trace projector onto R8

post-RM10 state:
  exactly inside the established rank-5 active domain

joint recovery:
  outputs exactly z, L1(z), L2(z), L3(z)
  prior exact basis checks: 40/40 PASS

ptxtSpace:
  625 required

temporary intFactor after ×224:
  399 mod 625
  valid unit

DigitExtract:
  well-typed with this unit intFactor

final original input intFactor:
  restore multiplicatively, as stock HElib does
  do NOT overwrite

Aung Algorithm-4 precondition:
  eta = 125 = 5^(e-1)
  satisfied for e=4

Static semantic theorem:

Dec
⁡
(
Π
c
a
n
d
(
𝑐
)
)
=
Dec
⁡
(
Π
A
u
n
g
,
C
o
r
r
/
T
n
M
(
𝑐
)
)
=
𝑚
Dec(Π
cand
	​

(c))=Dec(Π
Aung,Corr/TnM
	​

(c))=m

provided the homomorphic execution remains within correctness/noise limits.

Important boundary:

纯文本
PLAINTEXT/BGV SEMANTIC EQUIVALENCE:
  PASS

EXACT POST-MAP CIPHERTEXT TRANSCRIPT EQUALITY:
  NOT CLAIMED

EXACT NOISE / CAPACITY / DFR EQUALITY:
  NOT CLAIMED

The differing RM10/joint automorphism/key-switch paths use different evaluation-key errors, so native correctness/capacity remains decisive.

5. Structural obstruction and exact repair
Pre-raw fusion

Exact aggregate-only fusion before rawModSwitch is structurally impossible for the nontrivial signed RMFE aggregation rows.

Reason: branch-local bounded representative/rounding selection is non-additive.

Do not reopen generic pre-raw fusion without new branch-derived auxiliary state or changed semantics.

Earliest exact fusion boundary

The earliest established exact aggregate-only fusion point is:

纯文本
immediately AFTER branchwise rawModSwitch

For:

𝐷
𝑃
,
𝑞
(
𝑧
)
=
𝑧
−
𝑞
𝜌
𝑃
(
𝑧
)
𝑃
,
D
P,q
	​

(z)=
P
z−qρ
P
	​

(z)
	​

,

the nonlinearity is exactly captured by a public centered-residue carry:

𝐷
 ⁣
(
∑
𝑖
𝑎
𝑖
𝑧
𝑖
)
−
∑
𝑖
𝑎
𝑖
𝐷
(
𝑧
𝑖
)
=
𝑞
𝜅
𝑎
.
D(
i
∑
	​

a
i
	​

z
i
	​

)−
i
∑
	​

a
i
	​

D(z
i
	​

)=qκ
a
	​

.

Thus post-raw aggregation plus carry correction is exact.

The carry-cocycle mathematics itself is classical and is not a novelty claim.

Potential contribution is its FHE-specific use to identify and repair the maximal fusion boundary.

6. Exact secret-handle/reconstruction result

After:

纯文本
reLinearize(recryptKeyID)

every branch has handle basis exactly:

纯文本
(ONE, BASE(recryptKeyID))

and raw pair meaning:

𝑧
0
+
𝑠
𝑅
𝑧
1
.
z
0
	​

+s
R
	​

z
1
	​

.

Every 
𝑌
𝑖
=
𝑋
1024
𝑖
Y
i
=X
1024i
 envelope shift MUST be public ring-monomial multiplication.

Forbidden substitution:

纯文本
automorph / smartAutomorph as the Y^i shift

because that changes powerOfX.

Define:

𝐴
=
∑
𝑖
𝑌
𝑖
𝑎
𝑖
,
𝐵
=
∑
𝑖
𝑌
𝑖
𝑏
𝑖
.
A=
i
∑
	​

Y
i
a
i
	​

,B=
i
∑
	​

Y
i
b
i
	​

.

One reconstruction with the actual shared boot key satisfies an exact CtxtPart identity:

Rec
⁡
(
𝐴
,
𝐵
)
=
∑
𝑖
𝑌
𝑖
Rec
⁡
(
𝑎
𝑖
,
𝑏
𝑖
)
.
Rec(A,B)=
i
∑
	​

Y
i
Rec(a
i
	​

,b
i
	​

).

No fresh boot-key encryption, dummy one-part ciphertext, decryption/re-encryption, secret-key runtime synthesis, or surrogate reconstruction is allowed.

7. RM10 exact structure and lower bound

Turn 24 result:

纯文本
PASS_RM10_EXACT_SUPPORT_MINIMALITY
FAIL_SUB10_AUTOMORPHISM_RM10_IN_CURRENT_LINEAR_MODEL

Current rings:

𝑅
=
𝑍
625
[
𝑋
]
/
(
𝑋
16384
+
1
)
R=Z
625
	​

[X]/(X
16384
+1)
𝑅
8
=
𝑍
625
[
𝑌
]
/
(
𝑌
16
+
1
)
,
𝑌
=
𝑋
1024
.
R
8
	​

=Z
625
	​

[Y]/(Y
16
+1),Y=X
1024
.

Fixed subgroup:

𝐻
=
{
𝑢
∈
(
𝑍
/
32768
)
∗
:
𝑢
≡
1
(
m
o
d
32
)
}
H={u∈(Z/32768)
∗
:u≡1(mod32)}

with:

∣
𝐻
∣
=
1024.
∣H∣=1024.

RM10 is:

𝑃
𝐻
(
𝑥
)
=
224
∑
ℎ
∈
𝐻
𝜎
ℎ
(
𝑥
)
,
P
H
	​

(x)=224
h∈H
∑
	​

σ
h
	​

(x),

because:

1024
−
1
 
mod
 
625
=
224.
1024
−1
mod625=224.

Exact ten targets:

纯文本
16385
8193
4097
2049
1025
513
257
129
65
33

Their 
2
10
2
10
 subset products are 1024/1024 distinct and equal exactly to 
𝐻
H.

Any linear circuit using:

copies;
additions/subtractions;
public constant multiplication;
ordinary automorphism gates;

can expose at most:

2
𝑡
2
t

automorphism labels after 
𝑡
t automorphism gates.

RM10 has unique support size:

1024
1024

so:

𝑡
≥
10.
t≥10.

Current RM10 uses exactly 10.

Therefore:

纯文本
9-call exact RM10 in same linear automorphism-multiplier model:
  KILLED

8-call exact RM10:
  KILLED

Reopen only for:

new primitive;
new representation;
different key relation;
trace/subring-specific evaluation key;
implementation hoisting/parallelism that reduces cost but not support.
8. Joint rank-5 recovery

Current exact joint recovery replaces separate R8 C2S + correction assembly.

Restricted active slot space:

𝑉
a
c
t
=
span
⁡
{
𝑒
0
,
…
,
𝑒
4
,
𝑒
8
,
…
,
𝑒
12
}
.
V
act
	​

=span{e
0
	​

,…,e
4
	​

,e
8
	​

,…,e
12
	​

}.

Pre-C2S restricted domain:

𝑈
=
𝐿
−
1
𝑉
a
c
t
.
U=L
−1
V
act
	​

.

Selected support:

纯文本
{1,5,17,25,29}
=
{5^0,5^1,5^4,5^2,5^3} mod 32

Exact basis checks:

纯文本
40 / 40 PASS

All automorphism supports of size 1–4 were exhaustively tested:

纯文本
2516 / 2516 FAIL

Minimum terms:

纯文本
5 total terms
= identity + 4 nonidentity automorphisms

Thus joint recovery requires at least:

纯文本
4 physical nonidentity automorphism calls

within the established automorphism-multiplier interface.

With RM10:

纯文本
candidate recovery:
  10 + 4 = 14 physical KS

under direct BSGS+10 keys.

This 14-call decomposition is structurally minimal within the current RM10 + joint-recovery model.

9. Equal-resource comparator semantics

Turn-4 native experiment intentionally gives ALL workflows the SAME:

纯文本
BSGS + ten direct RM10 matrices

HElib addTheseMatrices recomputes global BFS keySwitchMap.

Therefore comparator algorithms remain source-faithful, but their physical execution graphs are augmented.

Correct wording:

纯文本
source-faithful algorithm under augmented equal-resource BSGS+10 keyset

not:

纯文本
operationally identical stock-keyset baseline

This is intentional and conservative.

Known BSGS+10 strengthening:

纯文本
thin linear-transform KS:
  21 -> 20

Corr./TnM five branch transforms:
  105 -> 100

Corr./TnM CoeffToSlots/recovery:
  100 -> 95

Possible additional Method-1 improvement:

0 for s=1,2,4,8;
1 KS per projection for s=16;
therefore up to +5 saving per k=5 Method-1 map.

For p=5,w=512,k=5, Aung's selection logic strongly suggests:

纯文本
s = 1

because s=1 already reaches maximal k=5, but exact row-level s is not explicitly published.

If s=1:

纯文本
thin strengthening:
  exactly 1 KS

Corr./TnM strengthening:
  exactly 5 KS

No hidden large baseline acceleration was found.

10. Current physical-KS comparison

Under the COMMON BSGS+10 resource:

纯文本
candidate:
  RM10 = 10
  joint recovery = 4
  total recovery = 14

Corr./TnM:
  recovery-side physical KS = 95

Use:

纯文本
95 -> 14

for current equal-resource BSGS+10 physical comparison.

The older:

纯文本
70 -> 14

is valid only as the FULL/transform-term perspective and must not be mislabeled as current equal-resource BSGS+10 physical KS.

11. Capacity metadata contract

Turn 23:

纯文本
PASS_RECONSTRUCTION_CAPACITY_METADATA_COMPARABILITY
CONDITIONAL_PASS_WHOLE_CANDIDATE_CAPACITY_COMPARABILITY

Stock thin reconstruction and candidate both must use:

纯文本
ctxt = recryptEkey
ctxt.multByConstant(ZZX)
ctxt.addConstant(ZZX)

The ZZX overload computes actual:

纯文本
embeddingLargestCoeff(...)

rather than a generic default.

Fused reconstruction ledger:

𝜈
f
u
s
e
d
=
𝜈
𝐸
∥
𝐵
∥
e
m
b
+
∣
𝑓
∣
∥
𝐴
∥
e
m
b
.
ν
fused
	​

=ν
E
	​

∥B∥
emb
	​

+∣f∣∥A∥
emb
	​

.

Separate reconstruction ledger:

𝜈
s
e
p
=
∑
𝑖
(
𝜈
𝐸
∥
𝑏
𝑖
∥
e
m
b
+
∣
𝑓
∣
∥
𝑎
𝑖
∥
e
m
b
)
.
ν
sep
	​

=
i
∑
	​

(ν
E
	​

∥b
i
	​

∥
emb
	​

+∣f∣∥a
i
	​

∥
emb
	​

).

Triangle inequality gives:

𝜈
f
u
s
e
d
≤
𝜈
s
e
p
.
ν
fused
	​

≤ν
sep
	​

.

Therefore a reconstruction capacity improvement is legitimate, not a bookkeeping cheat.

Current coefficient bounds:

纯文本
rawModSwitch powerful coefficient:
  |x| <= 313

post-divisibility branch coefficient:
  <= 626

aggregate A/B coefficient:
  <= 3130

A/B MaxBits:
  < 12

mvec.length()==1, so powerful and polynomial bases are identical here.

HElib's >400-bit scaled/truncated norm path is unreachable for these 
𝐴
,
𝐵
A,B.

Required candidate artifact rule:

纯文本
A,B reduced canonically mod X^16384 + 1

For custom RM10/joint plaintext multipliers:

SAFE:

纯文本
multByConstant(ZZX poly)

or:

纯文本
multByConstant(DoubleCRT dcrt, explicit_size)
explicit_size = embeddingLargestCoeff(balanced polynomial)

NOT scientifically clean:

纯文本
multByConstant(DoubleCRT dcrt)

with implicit default size.

If candidate custom DCRT multipliers omit explicit actual sizes:

纯文本
FAIL_CAPACITY_METADATA_CONTRACT

even if correctness passes.

Manual noiseBound/capacity reset or favorable metadata forging is forbidden.

12. Throughput metric and statistical contract

Aung metric:

Θ
𝑤
=
𝑆
𝑤
𝐶
ˉ
𝑤
𝑇
ˉ
𝑤
.
Θ
w
	​

=S
w
	​

T
ˉ
w
	​

C
ˉ
w
	​

	​

.

Slots:

纯文本
candidate: 10
Corr./TnM prior: 10
thin: 2

Primary ratios:

𝑅
p
r
i
o
r
=
𝐶
ˉ
𝑐
𝑇
ˉ
𝑝
𝐶
ˉ
𝑝
𝑇
ˉ
𝑐
R
prior
	​

=
C
ˉ
p
	​

T
ˉ
c
	​

C
ˉ
c
	​

T
ˉ
p
	​

	​


and:

𝑅
t
h
i
n
=
5
𝐶
ˉ
𝑐
𝑇
ˉ
𝑡
𝐶
ˉ
𝑡
𝑇
ˉ
𝑐
.
R
thin
	​

=5
C
ˉ
t
	​

T
ˉ
c
	​

C
ˉ
c
	​

T
ˉ
t
	​

	​

.

Strong PASS:

纯文本
lower95(R_prior) > 1
AND
lower95(R_thin) > 1

No prior-work gain:

纯文本
upper95(R_prior) <= 1
=> KILL current candidate on equal-resource systems value

Prior-only pass / thin fail:

纯文本
lower95(R_prior) > 1
AND
upper95(R_thin) <= 1
=> PARK / low publication value absent distinct novelty

CI straddles threshold:

纯文本
UNCLEAR

Bootstrap estimator:

纯文本
B = 100000
seed = 20261101
percentile 95% CI = primary
BCa 95% = sensitivity if well-defined

Use ratio-of-means / aggregate workflow statistic, not mean of invocation ratios.

Resampling:

each workflow's (C_i,T_i) must be resampled jointly;
pair across workflows only if actual matched trial blocks exist;
same-machine/keyset alone does NOT imply statistical pairing;
otherwise bootstrap workflows independently.

If percentile and BCa disagree on threshold crossing:

纯文本
UNCLEAR

If only means are available and no raw invocation arrays:

纯文本
NO SCIENTIFIC CI PASS

Inference is conditional on the measured fixed keyset, not fresh-KeyGen averaged.

13. Capacity–latency frontier

Same-machine point-estimate candidate beats prior iff:

𝑇
ˉ
𝑐
<
𝑇
ˉ
𝑝
𝐶
ˉ
𝑝
𝐶
ˉ
𝑐
.
T
ˉ
c
	​

<
C
ˉ
p
	​

T
ˉ
p
	​

	​

C
ˉ
c
	​

.

Candidate beats thin iff:

𝑇
ˉ
𝑐
<
5
𝑇
ˉ
𝑡
𝐶
ˉ
𝑡
𝐶
ˉ
𝑐
.
T
ˉ
c
	​

<5
C
ˉ
t
	​

T
ˉ
t
	​

	​

C
ˉ
c
	​

.

Strong point-estimate region:

𝑇
ˉ
𝑐
<
𝐶
ˉ
𝑐
min
⁡
(
𝑇
ˉ
𝑝
𝐶
ˉ
𝑝
,
5
𝑇
ˉ
𝑡
𝐶
ˉ
𝑡
)
.
T
ˉ
c
	​

<
C
ˉ
c
	​

min(
C
ˉ
p
	​

T
ˉ
p
	​

	​

,5
C
ˉ
t
	​

T
ˉ
t
	​

	​

).

Comparator with larger measured throughput is the stricter frontier.

Identity check:

𝑅
t
h
i
n
=
𝑅
p
r
i
o
r
Θ
p
r
i
o
r
Θ
t
h
i
n
.
R
thin
	​

=R
prior
	​

Θ
thin
	​

Θ
prior
	​

	​

.
Copy for Word

This must hold at the point estimate and in each coherent bootstrap replicate up to rounding. A material violation indicates a statistics implementation bug.

14. Throughput versus Pareto claim boundary

Turn-4 Strong PASS proves:

statistically higher Aung-style capacity × packing / latency throughput under the same-machine equal-resource configuration.

Preferred publication language:

crosses the Aung throughput frontier.

It does NOT automatically prove:

lower latency than thin;
higher final capacity than thin;
more remaining multiplications than thin;
lower evaluation-key size;
lower RSS;
strict all-axis Pareto dominance.

Most likely successful interpretation:

纯文本
new non-dominated tradeoff point

not:

纯文本
thin is dominated / obsolete

The candidate-specific BSGS+10 direct-key augmentation adds:

10 direct matrices;
+5.555556% Frobenius DCRT payload;
<5.557% serialized PubKey overhead versus BSGS baseline.

Runtime comparison uses equal BSGS+10 keys for fairness.

Deployment/storage comparison must still disclose the candidate-specific extra ten matrices relative to a stock comparator that could omit them.

15. Remaining-multiplications boundary

Turn 22:

纯文本
FAIL_FINAL_CAPACITY_DETERMINES_REMAINING_MULTIPLICATIONS
PASS_REMAINING_DEPTH_REQUIRES_SEPARATE_EMPIRICAL_GATE

HElib BGV:

𝑐
𝑎
𝑝
𝑎
𝑐
𝑖
𝑡
𝑦
=
log
⁡
2
(
𝑄
/
𝑛
𝑜
𝑖
𝑠
𝑒
𝐵
𝑜
𝑢
𝑛
𝑑
)
capacity=log
2
	​

(Q/noiseBound)

is only scalar metadata.

The first post-bootstrap square already calls relinearization, and KeySwitch added noise depends on actual:

纯文本
breakIntoDigits(actual ciphertext part)

Therefore final capacity is not a sufficient Markov state for future squaring depth.

Aung's "Remaining Mults" is measured by:

repeatedly squaring;
performing required recoding;
actual decryption checks;
stopping at failure;
minimum over 10 runs.

Do not infer:

纯文本
remaining multiplications = f(final capacity)

If current systems gate Strong-PASSES, a separate small Aung-matched repeated-squaring depth test becomes high value.

Do not start it while the current native slot is still occupied.

16. Security claim boundary

Turn 21:

纯文本
PASS_AFFINE_KDM_CLASS_UNCHANGED
PASS_POLYNOMIAL_QUERY_REGIME_UNCHANGED
FAIL_PLAIN_LWE_SAMPLE_COUNT_AS_FORMAL_KDM_MODEL

Automorphism secret functions are linear:

𝜎
𝑢
(
𝑠
)
=
𝐴
𝑢
𝑠
.
σ
u
	​

(s)=A
u
	​

s.

Under a broad affine-KDM class with polynomially many queries:

stock automorphism hints and +10 RM10 hints remain in the same function class;
query asymptotics remain polynomial;
key-dependency graph is unchanged.

Added material:

纯文本
+10 matrices
+10D KeySwitch rows

Do NOT claim:

formal HElib affine-KDM security from ACPS09;
a new reduction;
unchanged plain standard-RLWE security;
zero concrete-security cost;
−5.56% security bits.

The row/payload increase of +5.555556% is not a security-loss percentage.

Safe posture:

same HElib/Aung evaluation-key / circular-KDM posture, with ten additional standard same-key automorphism hints.

Aung's published 100-bit estimate cannot be numerically updated from the paper alone because exact estimator version, sample parameter, attack set, and treatment of evaluation-key hints were not published.

17. Novelty boundary

Killed as standalone novelty:

纯文本
"direct RMFE-packed MultKey" broadly
"one linear phase" broadly
joint rank-5 recovery alone
carry cocycle mathematics itself
generic Frobenius linear maps
generic subring/trace map

Aung PKC 2025 already leaves direct packed MultKey as future work, so high-level claim is not enough.

Aung Proposition 3 means joint recovery is a natural specialization/corollary, not standalone novelty.

Targeted post-Aung public search through 2026-11-01 found no direct collision for the narrow mechanism:

纯文本
branchwise nonlinear rounding / rawModSwitch
→ earliest exact post-rounding fusion
→ explicit carry compensation
→ one common boot-key reconstruction
→ restricted recovery

Absence of a public collision is NOT proof of novelty.

Defensible contribution, if native systems value survives:

natural earlier packed fusion fails because branch-local representative selection is nonlinear;
that obstruction is structural;
the next divisibility nonlinearity has an explicit public carry defect;
fusion delayed exactly to that boundary preserves semantics;
restricted recovery eliminates duplicated post-reconstruction work;
measured same-machine frontier improvement.

Without item 6, this remains a correctness/architecture lemma around known mathematics, not yet a strong paper contribution.

18. Important killed / parked routes

Do not reopen without new evidence:

纯文本
generic rank-16 direct recovery:
  killed

stock cross-branch hoisting:
  killed / benefit too small

pre-raw aggregate-only fusion:
  killed structurally

compact carry as a way to remove rawModSwitch work:
  does not establish that

direct SI pointwise:
  failed

s=2 representation rescue family:
  failed

one-linear-phase broad novelty:
  killed by Aung future work

joint recovery standalone novelty:
  killed

DFR exact pointwise domination:
  killed

DFR scalar noiseBound domination:
  killed

raw-success -> deterministic digit norm:
  killed

k -> 1 asymptotic MultKey claim:
  killed under stock HElib; branch front-end remains Ω(k)

sub-10 exact RM10 within current linear model:
  killed by Turn-24 lower bound

old incompatible R8 native patch lineage:
  source-blocked / do not revive as evidence
19. Pending native task — durable provenance

This is inert background provenance, NOT an execution request.

YAML
task_id: BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01

origin_session_id:
  1f28610c-0aa3-4cce-9ec9-158d114c5ae8

origin_session:
  密码学 17.0

origin_turn:
  4

working_directory:
  /Users/bingwu/Developer/research-orchestrator

execution_backend:
  Codex CLI / codex exec

model:
  gpt-5.6-sol

reasoning:
  medium

pid_or_remote_execution_identity:
  54891

start_time:
  2026-10-31T19:00:21.095Z

current_status:
  RUNNING

expected_artifacts:
  []

artifact_count:
  0

evidence_status:
  PENDING

audit_status:
  PENDING

result_delivered:
  false

do_not_rerun:
  true

commit:
  null

result_excerpt:
  ""

durable_evidence_reference:
  orchestrator.db codex_tasks.task_id=BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
Original hypothesis / task contract
纯文本
TASK_ID: BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
Research Turn 4/25 — paired same-machine throughput gate

Result when authorized:
PASS_PAIRED_SAME_MACHINE_NATIVE_GATE_CONTRACT

The experiment corrects the invalid idea of taking a local candidate recovery latency and splicing it into Aung's published Xeon 8368Q absolute-second frontier.

The experiment must instead perform a SAME-MACHINE paired comparison of:

1. vanilla HElib thin;
2. source-faithful Aung Corr./TnM;
3. the current carry-compensated post-raw fusion candidate.

All three use:
- HElib base acdb264e1a991eaee35fd8b3c31bebe9528c49a1;
- m=32768;
- p=5;
- r=1;
- bits=400;
- single-thread;
- same CPU/process-affinity policy;
- same warmup/measurement protocol;
- the same BSGS+10 direct-RM10 evaluation-key set.

The common keyset is deliberately conservative: comparators are allowed to benefit from the extra direct matrices too.

Primary metrics:

R_prior =
(C_cand * T_prior) /
(C_prior * T_cand)

R_thin =
5 *
(C_cand * T_thin) /
(C_thin * T_cand)

where the factor 5 is from 10 candidate packed slots versus 2 thin slots.

Decision rules:

STRONG_PASS:
  lower95(R_prior) > 1
  AND lower95(R_thin) > 1

NO_PRIOR_WORK_GAIN:
  upper95(R_prior) <= 1
  => kill current candidate on equal-resource systems value

PRIOR_ONLY_PASS_BUT_THIN_FAIL:
  lower95(R_prior) > 1
  AND upper95(R_thin) <= 1
  => park / low publication value absent distinct novelty

UNCLEAR:
  confidence interval straddles 1

Any candidate correctness mismatch returns FAIL_NATIVE_CORRECTNESS before performance interpretation.

Full original_hypothesis remains durably stored in:
orchestrator.db
under the task_id above.
The transport copy in the previous controller message was truncated; do not invent missing wording when exact provenance is needed.

These task fields are durable and must be carried across session boundaries.

The task remains background work.

Explicit rules:

纯文本
DO NOT RESTART
DO NOT DUPLICATE
DO NOT RESUBMIT
DO NOT MODIFY ITS SOURCE
DO NOT MODIFY ITS WORK DIRECTORY
DO NOT MODIFY ITS BINARY
DO NOT TREAT RESULT AS KNOWN
DO NOT START ANOTHER HEAVY LOCAL NATIVE TASK WHILE THIS SLOT IS OCCUPIED

Pending tasks may cross Research GPT sessions.

Do not wait for it before handoff or before doing independent lightweight research.

Do not reserve a session-local turn for its audit.

When the orchestrator delivers its result to the latest active session, the result automatically preempts that session's next free substantive turn for independent audit.

20. Mandatory native-result audit when delivered

When the pending result becomes available, stop ordinary side research and audit it first.

A. Provenance

Verify:

纯文本
upstream HElib:
  acdb264e1a991eaee35fd8b3c31bebe9528c49a1

candidate patch:
  exact commit / diff hash required

changed files/functions:
  required

same patched tree/binary:
  required for all three workflows

Reject scientific PASS if provenance is missing.

Forbidden substitutions:

fresh recryptEkey;
dummy one-part state;
secret-key evaluator reconstruction;
decrypt/re-encrypt;
changed rawModSwitch;
fresh-thin surrogate;
materially different comparator binary/configuration.
B. Shared keyset

Verify:

standard BSGS Frobenius keys;
exact +10 RM10 direct matrices;
setKeySwitchMap() recomputed;
all workflows share the same final key object or byte-identical serialized key material.

Ten targets:

纯文本
16385
8193
4097
2049
1025
513
257
129
65
33

Expected physical paths:

纯文本
candidate RM10:
  10 one-hop KS

candidate joint recovery:
  4 direct chained j=1 KS

Corr./TnM recovery:
  95 physical KS under BSGS+10
C. Candidate semantic assertions

Verify:

纯文本
1. source SlotsToCtxts semantics
2. source-identical thin SlotsToCoeff
3. every branch inCanonicalForm(recryptKeyID)
4. exactly two raw channels
5. branchwise rawModSwitch unchanged
6. typed carry channel 0 / channel 1
7. Y^i is public monomial multiplication, never automorphism
8. canonical A,B mod X^16384+1
9. actual shared recryptEkey
10. ptxtSpace == 625
11. exact ten RM10 targets
12. ×224 exactly once
13. established rank-5 active-domain layout
14. exact joint theta maps
15. output order L0,L1,L2,L3
16. stock multiplicative final intFactor restoration
D. Capacity metadata

Verify:

A/B reconstruction uses ZZX or explicit actual norm;
RM10/joint custom DCRT constants carry explicit embeddingLargestCoeff;
no implicit candidate-favorable default size;
no manual favorable noiseBound / capacity reset.

If violated:

纯文本
FAIL_CAPACITY_METADATA_CONTRACT
E. Measurement contract

Required:

5 warmups/workflow;
20 measured invocations/workflow;
single-thread;
fixed affinity policy;
fresh valid ciphertexts;
no retry/rescue;
no sweep;
per-invocation correctness;
raw final-capacity array;
raw latency array;
stage timings;
exact execution order;
trial matching information;
keyset hash / identity;
physical KS counts;
RM10 hop counts;
joint-recovery hop counts;
serialized public/evaluation-key bytes;
RSS if collected without perturbing semantics.

One packed candidate bootstrap invocation is ONE correctness/DFR trial; do not flatten ten logical packed outputs into ten independent Bernoulli trials.

F. Statistics

Use:

ratio of means;
joint (C,T) resampling;
actual paired/block bootstrap only if true matched trial blocks exist;
otherwise independent workflow resampling;
B=100000;
seed=20261101;
percentile 95% primary;
BCa sensitivity.

No raw arrays:

纯文本
no scientific CI PASS
G. Interpretation boundaries

Do not infer:

DFR from 20/20 correctness;
remaining multiplications from final capacity;
strict Pareto dominance from throughput;
new security theorem from +10 keys;
broad novelty from "one linear phase".
21. What to do if pending task is still running in 密码学 18.0

Begin a fresh session-local substantive turn budget.

Do ONE highest-EIG independent BOOT unit.

Permitted classes:

literature/prior-art search;
static mathematical derivation;
correctness/security analysis;
source audit;
cost/novelty analysis;
cheap non-native falsification;
candidate prescout;
reopening-condition analysis;
reproducibility analysis.

Do not do low-value work merely because Codex is occupied.

Do not start another heavy native task.

The next independent unit should be chosen from the current residual uncertainty frontier rather than repeating already-closed gates.

Potential high-level residual categories include:

mechanism-specific novelty closure if new evidence exists;
implementation-level hoisting/cost analysis that does NOT alter the running binary;
publication/reproducibility audit;
remaining security-proof boundary;
additional lightweight falsification of assumptions required by the eventual native artifact.

Do NOT reopen:

9-call RM10 in same model;
pre-raw aggregate-only fusion;
generic rank-16 recovery;
killed DFR domination arguments.
22. GitHub persistence rules

GitHub Notes / BBBINGW/memory is the primary durable research-memory interface.

For every durable scientific result:

纯文本
read-before-write
→ write finding
→ verify file
→ verify branch/commit

If connector access is unhealthy, use the verified local Git authority.

Do not claim connector-derived facts while connector is unavailable.

Do not overwrite newer authority with old STATE.md material from unrelated tracks.

Relevant final session files include:

纯文本
findings/boot-RMFE-end-to-end-static-semantic-equivalence-gate-2026-11-01.md
findings/boot-HANDOFF-post-turn25-paired-throughput-native-pending-2026-11-01.md
findings/boot-RMFE-rm10-support-minimality-ten-automorphism-lower-bound-2026-11-01.md
findings/boot-RMFE-capacity-metadata-comparability-gate-2026-11-01.md
findings/boot-RMFE-final-capacity-to-remaining-multiplications-inference-gate-2026-11-01.md
findings/boot-RMFE-bsgs10-affine-kdm-query-class-concrete-sample-security-gate-2026-11-01.md
findings/boot-RMFE-bsgs10-comparator-global-route-strengthening-bound-2026-11-01.md
findings/boot-RMFE-equal-keyset-augmented-comparator-routing-semantics-gate-2026-11-01.md
findings/boot-RMFE-throughput-vs-pareto-publication-claim-gate-2026-11-01.md
findings/boot-RMFE-capacity-latency-pareto-decision-boundary-gate-2026-11-01.md
findings/boot-RMFE-paired-throughput-statistical-inference-bootstrap-gate-2026-11-01.md
findings/boot-RMFE-source-faithful-implementability-execution-contract-preaudit-2026-11-01.md
findings/boot-RMFE-post-aung-2025-2026-followup-priorart-gate-2026-11-01.md

Checkpoint authority supplied by controller:

纯文本
88bf6af45632bc3e0afcaf3d08740782b0c4779f

No new native artifact SHA256 exists for the still-running paired-throughput task.

Its:

纯文本
expected_artifacts: []
artifact_count: 0
evidence_status: PENDING

must remain unchanged until orchestrator delivery.

23. PI / autonomy rules

Human PI decides:

top-level direction;
whether a contribution is meaningful;
acceptable assumptions/tradeoffs;
major pivots;
final publication judgment.

Research agent may autonomously:

continue;
refine;
kill;
park;
reprioritize;
perform reversible low-regret research;
delegate an already-authorized cheapest-decisive Codex task when a native slot is free.

Do not ask for PI permission every turn.

Authorized cheapest-decisive Codex execution does not require per-task PI approval unless the action changes the top-level research objective or requires an explicitly reserved human decision.

Reversible AI choices must be labeled:

纯文本
AI_PROVISIONAL_CHOICE

and never represented as PI approval.

24. Codex delegation rules

When a heavy native task is appropriate and the native slot is free:

define one falsifiable native question;
pin source commit;
pin parameters;
pin machine/runtime assumptions;
state exact expected artifact/provenance;
state stop conditions;
forbid rescue/sweep unless explicitly authorized;
require raw evidence sufficient for independent audit;
never accept Codex's scientific conclusion without independent Research GPT audit.

Do not rerun completed or do_not_rerun=true tasks.

Pending task lifecycle is independent of the Research GPT session.

25. Strict ORCHESTRATOR_CONTROL protocol for every normal successor answer

Every normal substantive research answer in 密码学 18.0 must end with exactly one valid control block:

纯文本
<ORCHESTRATOR_CONTROL>
action: CONTINUE | EXECUTE | WAIT_PI | STOP
milestone: true | false
requires_pi: true | false
independent_research_available: true | false
</ORCHESTRATOR_CONTROL>

If:

纯文本
action: EXECUTE

also include:

纯文本
task_id: <exact task id>

inside the block, but only if that task ID was explicitly established in that answer.

Additional hard rules:

CONTINUE

Use when:

independent research remains;
no native execution needs to be launched now;
a background native slot is occupied;
candidate is being statically audited/refined/reprioritized.

While BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01 is still RUNNING, do not use EXECUTE for another heavy local native task.

EXECUTE

Use only when:

a concrete cheapest-decisive native/Codex task has actually been specified;
the native slot is available;
the task is authorized by the current autonomous-research protocol.
WAIT_PI

Allowed only when:

a genuine PI decision blocks the next step;
AND there is no independent no-regret work left.

Must additionally include:

纯文本
research_frontier_exhausted: true

inside the block if the top-level frontier is exhausted.

If requires_pi: true, the block MUST include:

纯文本
independent_research_available: true | false

Never omit it.

STOP

Allowed only when:

the top-level BOOT objective is exhausted or deliberately terminated.

Must include:

纯文本
research_frontier_exhausted: true
General

Never use WAIT_PI merely because:

one candidate failed;
a Codex result is pending;
the conversation is near its limit;
a durable PI advisory exists;
a connector is temporarily unavailable.

If the result of the pending paired-throughput task is delivered during 密码学 18.0, the next free substantive turn MUST audit it before ordinary side research.

26. Immediate successor instruction

At the start of 密码学 18.0:

Restore BBBINGW/memory authority beginning from checkpoint:
纯文本
88bf6af45632bc3e0afcaf3d08740782b0c4779f

Read the saved post-Turn-25 handoff and Turn-25 end-to-end semantic-equivalence finding.

Check whether the orchestrator has delivered a result for:

纯文本
BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01

If delivered:

make the first substantive turn an independent audit against the complete contract above.

If still RUNNING/PENDING:

do not touch it;
open a new session-local research-turn budget;
choose one highest-expected-information-gain independent BOOT unit;
maintain TRACK_ID=BOOT;
maintain ACTIVE_SUBLINE=B158_CHECKPOINT_DECOUPLED_HALF_BASIS;
use one hypothesis + one cheapest decisive test;
persist durable results.

Do not treat inheritance itself as a reason to WAIT_PI.

PENDING_PI_DECISIONS: none.

research_frontier_exhausted: false.
