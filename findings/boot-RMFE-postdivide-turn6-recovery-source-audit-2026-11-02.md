# BOOT Research Turn 6/25 — current-candidate 17-call recovery source audit

## Durable provenance

- Session: `de72fdd0-c665-4611-9d0a-2e3575957355`
- Research turn row: `342`
- Logical turn: `6/25`
- Message ID: `assistant@0470c027`
- Durable verdict: `UNCLEAR`
- Counted: `true`
- Recorded at: `2026-11-02T06:49:03.686Z`
- Source of truth: `data/orchestrator.db`
- Preservation: the Research Turn body below is copied verbatim; it was not regenerated and does not increment the turn counter.

## Verbatim durable Research Turn

Research Turn 6/25 — current-candidate 17-call recovery source audit

TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Logical session: de72fdd0-c665-4611-9d0a-2e3575957355

Overall verdict: UNCLEAR
Attribution: SOURCE_BLOCKED / IMPLEMENTATION_ABSENT

本轮严格只审计当前 PRE-TAG + POST-DIVIDE LATE AGGREGATION 候选的 17-call target-pruned recovery。没有启动 native/Codex，没有借用历史 POST-RAW candidate 的 correctness/timing/capacity 证据，也没有执行 novelty/performance 工作。

1. Concrete implementation inventory：没有找到可审计的当前候选实现

当前 late-aggregation 的 Turn-22 preregistration 本身把

纯文本
pure inverse
→ 17-call target-pruned unpack
→ four RMFE recombinations

描述为候选未来要执行的路径，并紧接着写成“future native candidate must assert”的 runtime contract。
boot-r22-late-aggregation-imple…
 更明确地，该文档末尾把自身定义为“future reproducibility/preregistration contract”，而不是现存 candidate source。
boot-r22-late-aggregation-imple…

我检查了当前 runtime、conversation/library 中能够定位的 BOOT recovery artifacts。找到的代码证据只有静态 checker，而不是 HElib/Ctxt implementation：

BOOT-T17-PRUNED-UNPACK-LEDGER-CHECK-20261101.py 根据 
𝐽
J 的 residue classes 计算 active-node/child counts，并断言 
17
17 automorphisms、
21
21 add/sub、
5
5 odd multipliers；它没有 ciphertext、Frobenius call、mask application 或 leaf assembly。
BOOT-T17-PRUNED-UNPACK-LEDGER-C…
BOOT-T16-RHO-STABLE-PRUNING-CHECK-20261101.py 验证 
𝜌
ρ 的 monomial transport、
182
−
1
=
443
182
−1
=443 以及矩阵 
𝐴
−
1
A
−1
，之后同样只是计算 active residue counts。
BOOT-T16-RHO-STABLE-PRUNING-CHE…
同一 checker 验证 
8192
 
mod
 
625
=
67
8192mod625=67 且 
67
−
1
=
28
67
−1
=28，但没有把 
28
28 应用到任何真实 recovery source path。
BOOT-T16-RHO-STABLE-PRUNING-CHE…
four-correction checker 枚举 branch labellings 并以 public-constant norm ledger 选出 [2,0,3,1,4]; 它没有消费 17-call unpack outputs，也没有执行 
𝐿
0
,
…
,
𝐿
3
L
0
	​

,…,L
3
	​

 ciphertext assembly。
BOOT-T22-FOUR-CORRECTION-RECOMB…

因此，在本轮可审计库存里，没有找到能回答以下问题的 concrete bytes：

纯文本
for each active node:
    actual Frobenius call
    actual even/odd masks
    actual X^{-2^i} multiplier
    actual pruning decision
    actual 8192^{-1} normalization placement
    actual selected-leaf routing
    actual C0..C4 output assembly
    actual rho correction
    actual L0..L3 ciphertext assembly

这不是算法反例；它意味着 当前 correctness claim 仍缺 implementation witness。

2. 五个 rho-conjugated projector：抽象代数重新核对通过，但不是 source PASS

冻结的

𝐽
=
[
0
,
1024
,
7168
,
2048
,
6144
]
J=[0,1024,7168,2048,6144]

具有：

𝜌
(
𝑋
0
)
	
=
𝑋
0
,


𝜌
(
𝑋
1024
)
	
=
182
𝑋
7168
,


𝜌
(
𝑋
7168
)
	
=
182
𝑋
1024
,


𝜌
(
𝑋
2048
)
	
=
182
𝑋
6144
,


𝜌
(
𝑋
6144
)
	
=
182
𝑋
2048
.
ρ(X
0
)
ρ(X
1024
)
ρ(X
7168
)
ρ(X
2048
)
ρ(X
6144
)
	​

=X
0
,
=182X
7168
,
=182X
1024
,
=182X
6144
,
=182X
2048
.
	​


静态 checker 对这五条映射和

182
−
1
=
443
(
m
o
d
625
)
182
−1
=443(mod625)

都有精确断言。
BOOT-T16-RHO-STABLE-PRUNING-CHE…
 我也重新算得

182
⋅
443
=
80626
≡
1
(
m
o
d
625
)
.
182⋅443=80626≡1(mod625).

所以 Turn 5 要求的 projector target 在抽象上确实是：

physical slot 0
	
physical slot 1


coeff
⁡
0
	
coeff
⁡
0


coeff
⁡
1024
	
443
 
coeff
⁡
7168


coeff
⁡
7168
	
443
 
coeff
⁡
1024


coeff
⁡
2048
	
443
 
coeff
⁡
6144


coeff
⁡
6144
	
443
 
coeff
⁡
2048
physical slot 0
coeff
0
	​

coeff
1024
	​

coeff
7168
	​

coeff
2048
	​

coeff
6144
	​

	​

physical slot 1
coeff
0
	​

443coeff
7168
	​

443coeff
1024
	​

443coeff
6144
	​

443coeff
2048
	​

	​

	​


此外，

8192
≡
67
(
m
o
d
625
)
,
67
⋅
28
=
1876
≡
1
(
m
o
d
625
)
,
8192≡67(mod625),67⋅28=1876≡1(mod625),

所以 
28
=
8192
−
1
(
m
o
d
625
)
28=8192
−1
(mod625) 也是合法 unit。

**但本轮不能把这些静态等式升级成 implementation PASS：**没有实际 17-call recursion source 可检查它是否真的在正确 node、正确 child、正确 physical slot 上实现这些 projectors。

3. [2,0,3,1,4] ordering：数学逆置换明确，实际 output boundary 未验证

若真实 unpack 的 
𝐽
J-order outputs 为

(
𝐶
0
,
𝐶
1
,
𝐶
2
,
𝐶
3
,
𝐶
4
)
(C
0
	​

,C
1
	​

,C
2
	​

,C
3
	​

,C
4
	​

)

且标签确实为

[
2
,
0
,
3
,
1
,
4
]
,
[2,0,3,1,4],

那么逆映射唯一是：

(
𝐴
0
,
𝐴
1
,
𝐴
2
,
𝐴
3
,
𝐴
4
)
=
(
𝐶
1
,
𝐶
3
,
𝐶
0
,
𝐶
2
,
𝐶
4
)
.
(A
0
	​

,A
1
	​

,A
2
	​

,A
3
	​

,A
4
	​

)=(C
1
	​

,C
3
	​

,C
0
	​

,C
2
	​

,C
4
	​

).
	​


这部分没有代数歧义。

但是现有 checker 对 [2,0,3,1,4] 的验证是 public-constant cost/embedding-norm enumeration，而不是对实际 recovery output array 的 source assertion。
BOOT-T22-FOUR-CORRECTION-RECOMB…

所以：

纯文本
MATH ORDERING: consistent
ACTUAL SOURCE OUTPUT ORDERING: unverified
4. 
𝐿
0
,
𝐿
1
,
𝐿
2
,
𝐿
3
L
0
	​

,L
1
	​

,L
2
	​

,L
3
	​

 完整接口：条件式成立，实际实现未闭合

条件于 concrete recovery 真正返回上述五个 exact 
𝑍
625
Z
625
	​

 lifts，则 Turn 5 的 complete interface 立即闭合：

𝐿
𝑟
=
𝐶
1
𝜙
(
𝑒
0
)
5
𝑟
+
𝐶
3
𝜙
(
𝑒
1
)
5
𝑟
+
𝐶
0
𝜙
(
𝑒
2
)
5
𝑟
+
𝐶
2
𝜙
(
𝑒
3
)
5
𝑟
+
𝐶
4
𝜙
(
𝑒
4
)
5
𝑟
L
r
	​

=C
1
	​

ϕ(e
0
	​

)
5
r
+C
3
	​

ϕ(e
1
	​

)
5
r
+C
0
	​

ϕ(e
2
	​

)
5
r
+C
2
	​

ϕ(e
3
	​

)
5
r
+C
4
	​

ϕ(e
4
	​

)
5
r
	​


for 
𝑟
=
0
,
1
,
2
,
3
r=0,1,2,3.

其中：

纯文本
L0 → z
L1,L2,L3 → Aung Algorithm-4 correction images

第二 physical slot 的 global constants 自动带上对应 
𝜌
ρ-transport；这一点与上面的 projector algebra 相容。

但 requested gate 是 source-level complete semantic interface，不是条件 theorem。因此当前证据只能支持：

纯文本
ABSTRACT L0..L3 ALGEBRA: consistent
CONCRETE LEAF→L0..L3 IMPLEMENTATION: absent / unverified
5. Mechanism firewall

历史

纯文本
work/BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01/
  source/benchmark.cpp
  source/canary.cpp

属于 POST-RAW carry-corrected fusion，不是当前 PRE-TAG + POST-DIVIDE late-aggregation candidate。

本轮没有使用它们来证明：

17-call recovery；
leaf correctness；
𝐿
0
…
𝐿
3
L
0
	​

…L
3
	​

 correctness；
noise/capacity；
latency/value；
novelty。

所以不存在跨机制证据污染。

Turn 6 verdict
纯文本
OVERALL_VERDICT:
UNCLEAR

ATTRIBUTION:
SOURCE_BLOCKED / IMPLEMENTATION_ABSENT

STATIC_RHO_ARITHMETIC:
CONSISTENT

17_CALL_COUNT_FORMULA:
STATICALLY SUPPORTED

ACTUAL_17_CALL_RECURSION:
NOT LOCATED

ACTUAL_MASKS_AND_NORMALIZATION:
NOT LOCATED

ACTUAL_FIVE_LEAF_ROUTING:
NOT LOCATED

ACTUAL_BRANCH_INVERSION:
NOT VERIFIED IN SOURCE

ACTUAL_L0_L1_L2_L3_ASSEMBLY:
NOT VERIFIED IN SOURCE

ALGORITHMIC_OBSTRUCTION:
NOT ESTABLISHED

IMPLEMENTATION_ERROR:
NOT ESTABLISHED

这轮减少的完整论文不确定性很具体：此前我们不知道“17-call recovery 已经存在但尚未审计”还是“只有数学 schedule”。现在可用证据支持后者——当前 paper correctness gate 的缺口不是又一个未知代数 lemma，而是缺少 current-candidate concrete implementation witness。

因此状态变化是：

Gate	Turn 5 前	Turn 6 后
Phase	CORRECTNESS_GATE	CORRECTNESS_GATE
Novelty	PREFLIGHT	PREFLIGHT
Abstract projector algebra	Math-consistent	仍 math-consistent
Concrete 17-call source	Unknown	not located / implementation absent in audited inventory
Correctness gate	Pending	BLOCKED on implementation evidence
Security	Pending	Pending
Value	Pending	Pending
Paper readiness	Not ready	Not ready

下一单一 decisive experiment： CURRENT-CANDIDATE RECOVERY IMPLEMENTATION CANARY——先取得或实现真实 target-pruned recovery bytes，然后对 deterministic full-ring inputs 精确检查五个双-slot projector leaves、`[C1,C3,C0,C2,C4]` ordering 和 
𝐿
0
…
𝐿
3
 
mod
 
625
L
0
	​

…L
3
	​

mod625。在此通过前不进入 timing。

<PAPER_CANDIDATE_UPDATE>
{"CANDIDATE_ID":"legacy-484479fe4613","RANK":1,"STATUS":"ACTIVE","PHASE":"CORRECTNESS_GATE","PAPER_THESIS":"Hypothesis under validation: reduce Aung et al.'s repeated MultKey bottleneck by keeping five tagged RMFE branches independent through branch-local nonlinear HElib preprocessing, aggregating only exact post-divide reconstruction inputs, performing one shared recryptEkey reconstruction, and recovering the five exact Z_625 branch lifts with a target-pruned 17-call full-domain unpack before forming Aung correction outputs L0,L1,L2,L3.","IMPORTANT_PROBLEM":"Inherited important problem remains Aung et al.'s repeated per-branch MultKey cost in the canonical p=5,m=32768,w=512,k=5 Corr./TnM workflow. This turn did not reassess problem importance.","BASELINE":"Primary baseline remains source-faithful Aung Corr./TnM at p=5,m=32768,w=512,k=5; secondary frontier remains matched vanilla HElib thin bootstrapping.","CLOSEST_PRIOR_ART":"Inherited prior-art state only. No independent novelty verification was performed in Turn 6; therefore novelty remains PREFLIGHT.","NEW_MECHANISM":"Hypothesis under validation: pre-tag five scalar branches; run five source-identical forward/nonlinear preprocessing paths independently through rawModSwitch, newMakeDivisible and division by 5; aggregate the post-divide pairs; reconstruct once; apply a pure power-basis inverse; execute a target-pruned 17-call recovery whose five projectors are rho-conjugate across the two physical slots; invert J-order [2,0,3,1,4] to branch order [C1,C3,C0,C2,C4]; then form exact Z_625 L0,L1,L2,L3 and invoke Aung Algorithm 4.","CONTRIBUTION_TYPE":"ALGORITHM","FULL_CONSTRUCTION":"Algorithmically specified but not concretely implemented in the audited current-candidate inventory. Canonical parameters are p=5,m=32768,w=512,k=5,r=1,e=4,e'=1,q=626, temporary modulus 625, d=8192, eta=125, J=[0,1024,7168,2048,6144], J-order labels [2,0,3,1,4]. The unresolved concrete component is the actual target-pruned recovery recursion, masks, normalization, leaf routing and L0..L3 output assembly.","CORRECTNESS":"Turn-5 algebra remains internally consistent: 443 is the inverse of 182 modulo 625; 28 is the inverse of 8192 modulo 625; the required second-slot projector actions are coeff_0, 443coeff_7168, 443coeff_1024, 443coeff_6144 and 443coeff_2048; and [2,0,3,1,4] mathematically inverts to [C1,C3,C0,C2,C4]. However the audited artifacts contain only counting/rho/cost checkers and preregistration descriptions, not a concrete current-candidate HElib/Ctxt implementation of the 17-call recursion. Therefore actual masks, normalization placement, five-leaf routing and L0..L3 assembly cannot be source-verified. No algorithmic counterexample was established; native correctness remains unknown.","SECURITY":"No status-changing security evidence was produced. The proposed recovery remains a public-linear operation under the inherited model, but resource/key/security parity remains PENDING and cannot be upgraded without concrete implementation evidence.","NOISE_PRECISION_DFR":"No new noise, precision, DFR or capacity evidence was produced. Existing static ledgers are not upgraded by this source-inventory result.","VALUE":"PENDING. No timing, throughput, key-memory, RSS or Pareto claim was made or inferred in Turn 6.","CRITICAL_BLOCKER":"Concrete current-candidate target-pruned recovery implementation is absent from the audited inventory. Without actual recursion/masks/normalization/leaf-routing/L0..L3 source, the correctness gate cannot distinguish a correct realizable 17-call implementation from a merely valid abstract schedule.","NEXT_DECISIVE_TEST":"CURRENT-CANDIDATE RECOVERY IMPLEMENTATION CANARY: obtain or implement the concrete target-pruned recovery path and deterministically verify exact Z_625 outputs for all five two-slot rho-conjugated projectors, branch order [C1,C3,C0,C2,C4], and L0,L1,L2,L3 before any timing or value interpretation.","NOVELTY_STATUS":"PREFLIGHT","PAPER_READINESS":"NOT_READY","REOPEN_CONDITION":"Once concrete current-candidate recovery source exists, re-run the source/correctness audit against the Turn-5 projector oracle. If the implementation mismatches but the abstract projector construction remains realizable at the declared 17-call cost, classify it as an implementation repair; if the required projector cannot be realized under the stated recursion/resource contract, treat that as an algorithmic obstruction and reassess the candidate.","CONSTRUCTIVE_DESIGN_SPEC":"Five branch-local tagged forward/nonlinear preprocessing paths through /5; post-divide Z0/Z1 aggregation; one ptxtSpace-625 reconstruction; pure power-basis inverse; target-pruned recovery intended to use 13 Frobenius levels with 17 physical calls; first-slot targets coeff_0,coeff_1024,coeff_7168,coeff_2048,coeff_6144 and second-slot rho-conjugates coeff_0,443coeff_7168,443coeff_1024,443coeff_6144,443coeff_2048; J-order labels [2,0,3,1,4] inverted to [C1,C3,C0,C2,C4]; L_r=C1phi(e0)^(5^r)+C3phi(e1)^(5^r)+C0phi(e2)^(5^r)+C2phi(e3)^(5^r)+C4*phi(e4)^(5^r), r=0,1,2,3. This remains a design specification until source bytes implement it.","CORRECTNESS_GATE":"BLOCKED","SECURITY_GATE":"PENDING","VALUE_GATE":"PENDING","AUDIT_GATE":"PENDING","BASELINE_CORRECTNESS":"PENDING","ASSESSMENT":{"MECHANISM_PROGRESS":false,"THEOREM_PROGRESS":false,"CORRECTNESS_PROGRESS":true,"SECURITY_PROGRESS":false,"VALUE_PROGRESS":false,"NOVELTY_PROGRESS":false,"REDUCES_CRITICAL_UNCERTAINTY":true,"EVIDENCE_GRADE":"STATIC","BASELINE_MATCHED":false,"PERFORMANCE_CLAIM":false,"OBSTRUCTION_VALUABLE":true,"STRICT_NO_GO":false,"CREDIBLE_NEW_MECHANISM":true,"FRONTIER_CANDIDATES_REMAINING":true,"INDEPENDENT_AUDIT_PASSED":false,"VERDICT":"UNCLEAR"}}
</PAPER_CANDIDATE_UPDATE>

<ORCHESTRATOR_CONTROL>
action: CONTINUE
milestone: false
requires_pi: false
independent_research_available: true
</ORCHESTRATOR_CONTROL> 

Copy for Word