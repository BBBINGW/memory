<!--
Authority provenance:
- track: BOOT
- subline: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
- logical session: de72fdd0-c665-4611-9d0a-2e3575957355
- research turn: 7/25
- research_turn_id: 343
- message_id: assistant@a0a8bf73
- model: gpt-5.6-sol
- reasoning: xhigh
- zero_api_billing: true
- exactly_once: true
- body_sha256: e23f97f2d6fa03db978c600d478c0835cc290d24c7796d320c2a65ac59dc1c6b
-->

Research Turn 7/25 — exact 17-call split-recurrence theorem

TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

Primary hypothesis

Geelen's 13-level power-of-two unpack recurrence remains an exact coordinate projector in our actual local algebra

𝐸
=
𝑍
625
[
𝑋
]
/
(
𝑋
8192
+
182
)
,
E=Z
625
	​

[X]/(X
8192
+182),

despite 
𝑋
8192
≠
±
1
X
8192

=±1; hence the claimed 17-call pruning does not hide missing 
182
/
443
182/443-type unit factors inside the recursion.

This is independent of the pending BOOT-T7-RECOVERY-WITNESS-20261102; I do not use or infer that task's result.

Source facts

Geelen's unpacking uses, at level 
𝑖
=
1
,
…
,
log
⁡
2
𝑑
i=1,…,log
2
	​

d,

𝑚
0
=
𝑚
+
𝜎
𝑑
/
2
𝑖
(
𝑚
)
,
𝑚
1
=
𝑋
−
2
𝑖
−
1
(
𝑚
−
𝜎
𝑑
/
2
𝑖
(
𝑚
)
)
,
m
0
	​

=m+σ
d/2
i
(m),m
1
	​

=X
−2
i−1
(m−σ
d/2
i
(m)),

and states that the factors of 2 accumulate to 
𝑑
d, removable by folding 
𝑑
−
1
d
−1
 into the preceding transformation. 
Cryptology ePrint Archive
+1
 His Frobenius is 
𝜎
=
𝜏
𝑝
σ=τ
p
	​

, acting slotwise as 
𝑎
(
𝜁
)
↦
𝑎
(
𝜁
𝑝
)
a(ζ)↦a(ζ
p
). 
Cryptology ePrint Archive

Our audited local algebra is exactly

𝐸
=
𝑆
[
𝑋
]
/
(
𝑋
8192
+
182
)
,
𝑆
=
𝑍
/
625
𝑍
,
E=S[X]/(X
8192
+182),S=Z/625Z,

with the second-slot coordinate transport

𝜌
(
𝑓
)
(
𝑋
)
=
𝑓
(
𝑋
16383
)
ρ(f)(X)=f(X
16383
). 
BOOT-T16-FULL-EVALMAP-COORDINAT…
 
BOOT-T16-FULL-EVALMAP-COORDINAT…

The PDF screenshot path was also attempted as required, but the host returned HTTP 403; the indexed PDF text above remained available.

1. The apparent unit-factor problem

Because

𝑋
8192
=
−
182
=
443
(
m
o
d
625
)
,
X
8192
=−182=443(mod625),

one might worry that later Frobenius stages produce powers of 
443
443, not clean signs, invalidating the ordinary binary split.

However,

182
2
≡
−
1
(
m
o
d
625
)
,
182
2
≡−1(mod625),

hence

𝑋
16384
=
443
2
=
−
1
,
𝑋
32768
=
1.
X
16384
=443
2
=−1,X
32768
=1.

That is the decisive relation.

Let

𝑑
=
8192
=
2
13
,
𝜏
𝑖
=
𝜎
𝑑
/
2
𝑖
,
d=8192=2
13
,τ
i
	​

=σ
d/2
i
,

and write

𝑔
𝑖
=
5
2
13
−
𝑖
(
m
o
d
32768
)
.
g
i
	​

=5
2
13−i
(mod32768).

By the standard 2-adic valuation identity,

𝑣
2
(
𝑔
𝑖
−
1
)
=
15
−
𝑖
,
v
2
	​

(g
i
	​

−1)=15−i,

so

𝑔
𝑖
=
1
+
2
15
−
𝑖
𝑢
𝑖
g
i
	​

=1+2
15−i
u
i
	​


for an odd integer 
𝑢
𝑖
u
i
	​

.

Now consider a node after the first 
𝑖
−
1
i−1 splits. Its shifted monomials all have exponent

2
𝑖
−
1
𝑘
.
2
i−1
k.

Then

𝜏
𝑖
(
𝑋
2
𝑖
−
1
𝑘
)
	
=
𝑋
2
𝑖
−
1
𝑘
𝑔
𝑖


	
=
𝑋
2
𝑖
−
1
𝑘
𝑋
2
𝑖
−
1
𝑘
(
𝑔
𝑖
−
1
)


	
=
𝑋
2
𝑖
−
1
𝑘
𝑋
2
14
𝑢
𝑖
𝑘


	
=
(
−
1
)
𝑘
𝑋
2
𝑖
−
1
𝑘
.
τ
i
	​

(X
2
i−1
k
)
	​

=X
2
i−1
kg
i
	​

=X
2
i−1
k
X
2
i−1
k(g
i
	​

−1)
=X
2
i−1
k
X
2
14
u
i
	​

k
=(−1)
k
X
2
i−1
k
.
	​


Therefore on the actual current node, 
𝜏
𝑖
τ
i
	​

 is exactly the required next-bit sign test:

𝑘
 even
⇒
+
1
,
𝑘
 odd
⇒
−
1.
k even⇒+1,k odd⇒−1.

So the troublesome 
𝑋
8192
=
443
X
8192
=443 never injects an extra unit into the split.

This is stronger than the old active-node counting argument.

2. Exact induction invariant

Let the original dirty full-domain slot be

𝑚
(
𝑋
)
=
∑
𝑗
=
0
8191
𝑧
𝑗
𝑋
𝑗
.
m(X)=
j=0
∑
8191
	​

z
j
	​

X
j
.

For a node corresponding to residue 
𝑟
 
mod
 
2
𝑖
−
1
rmod2
i−1
, define the invariant

𝑁
𝑖
−
1
,
𝑟
=
2
𝑖
−
1
∑
𝑘
≥
0
𝑧
𝑟
+
2
𝑖
−
1
𝑘
𝑋
2
𝑖
−
1
𝑘
.
N
i−1,r
	​

=2
i−1
k≥0
∑
	​

z
r+2
i−1
k
	​

X
2
i−1
k
.

Using the sign identity above:

𝑁
𝑖
−
1
,
𝑟
+
𝜏
𝑖
(
𝑁
𝑖
−
1
,
𝑟
)
N
i−1,r
	​

+τ
i
	​

(N
i−1,r
	​

)

retains exactly even 
𝑘
k, and

𝑋
−
2
𝑖
−
1
(
𝑁
𝑖
−
1
,
𝑟
−
𝜏
𝑖
(
𝑁
𝑖
−
1
,
𝑟
)
)
X
−2
i−1
(N
i−1,r
	​

−τ
i
	​

(N
i−1,r
	​

))

retains exactly odd 
𝑘
k and shifts it down one binary position.

Hence the two children are exactly

𝑁
𝑖
,
𝑟
=
2
𝑖
∑
ℓ
𝑧
𝑟
+
2
𝑖
ℓ
𝑋
2
𝑖
ℓ
,
N
i,r
	​

=2
i
ℓ
∑
	​

z
r+2
i
ℓ
	​

X
2
i
ℓ
,

and

𝑁
𝑖
,
𝑟
+
2
𝑖
−
1
=
2
𝑖
∑
ℓ
𝑧
𝑟
+
2
𝑖
−
1
+
2
𝑖
ℓ
𝑋
2
𝑖
ℓ
.
N
i,r+2
i−1
	​

=2
i
ℓ
∑
	​

z
r+2
i−1
+2
i
ℓ
	​

X
2
i
ℓ
.

At level 
13
13,

𝑁
13
,
𝑗
=
8192
 
𝑧
𝑗
N
13,j
	​

=8192z
j
	​

	​


for every coordinate 
𝑗
j.

There is:

no hidden 
182
182;
no hidden 
443
443;
no branch-dependent unit;
no approximation;
no assumption that nonselected coordinates are zero.

So after normalization by

8192
−
1
=
28
(
m
o
d
625
)
,
8192
−1
=28(mod625),

the leaf is exactly 
𝑧
𝑗
∈
𝑍
625
z
j
	​

∈Z
625
	​

.

The existing checker independently verifies 
8192
−
1
=
28
8192
−1
=28 and the frozen 
𝜌
ρ units. 
BOOT-T16-RHO-STABLE-PRUNING-CHE…

3. Pruning preserves this theorem

For

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
,
J=[0,1024,7168,2048,6144],

only nodes containing at least one target need to survive.

The audited target-residue counts are

[
1
,
1
,
1
,
1
,
1
,
1
,
1
,
1
,
1
,
1
,
1
,
2
,
4
]
,
[1,1,1,1,1,1,1,1,1,1,1,2,4],

whose sum is exactly

17.
17.

The existing static checker also derives 21 retained add/sub operations and five odd-child monomial multiplications. 
BOOT-T17-PRUNED-UNPACK-LEDGER-C…

The induction above now supplies what that checker did not establish:

every retained target leaf is not merely reachable in 17 calls; it equals 
8192
𝑧
𝑗
8192z
j
	​

 exactly in the actual 
𝑋
8192
+
182
X
8192
+182 local algebra.

Thus:

纯文本
17-call count     = static combinatorial fact
17-call exactness = now mathematical theorem
4. Important refinement of the second-physical-slot oracle

This exposes a useful distinction for the pending witness.

The same unpack tree applied to the second physical slot naturally extracts the raw coordinates of 
𝜌
(
𝑏
)
ρ(b). From the audited transport,

0
	
↦
0
,


1024
	
↦
182
⋅
7168
,


7168
	
↦
182
⋅
1024
,


2048
	
↦
182
⋅
6144
,


6144
	
↦
182
⋅
2048
,
0
1024
7168
2048
6144
	​

↦0,
↦182⋅7168,
↦182⋅1024,
↦182⋅6144,
↦182⋅2048,
	​


with 
182
−
1
=
443
182
−1
=443. 
BOOT-T16-RHO-STABLE-PRUNING-CHE…

If first-slot branch labels in 
𝐽
J-order are

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

then normalized raw second-slot leaves in the same 
𝐽
J-order are

[
𝑏
2
,
  
182
𝑏
3
,
  
182
𝑏
0
,
  
182
𝑏
4
,
  
182
𝑏
1
]
.
[b
2
	​

,182b
3
	​

,182b
0
	​

,182b
4
	​

,182b
1
	​

].

Therefore there are two mathematically equivalent implementation forms:

Aligned-leaf form

Apply 
𝜌
ρ-conjugated projector correction immediately, so each leaf ciphertext already contains the same logical branch in both slots.

Fused-recombination form

Let the 17-call tree return raw 
𝐽
J-coordinate leaves and absorb the permutation

𝜌
p
o
s
=
[
0
,
2
,
1
,
4
,
3
]
ρ
pos
	​

=[0,2,1,4,3]

and factor 
443
443 into the 
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

 public constants.

Crucially, the existing four-correction checker uses exactly the second form: it records rho_pos=[0,2,1,4,3], 
BOOT-T22-FOUR-CORRECTION-RECOMB…
 and for nonzero coordinates chooses the 443-scaled second-slot table with the rho-permuted branch index. 
BOOT-T22-FOUR-CORRECTION-RECOMB…

So a future audit must not falsely reject an implementation merely because its intermediate leaves remain rho-permuted.

The true end-to-end oracle is:

raw leaf extraction
  
∘
  
rho correction/reindexing
  
∘
  
𝐿
𝑟
raw leaf extraction∘rho correction/reindexing∘L
r
	​

	​


and the rho correction may legally be fused into the 
4
×
5
4×5 correction constant tables.

This does not change the mechanism or operation count.

Turn 7 verdict

Overall side-research verdict: PASS

纯文本
PASS_EXACT_LOCAL_RING_BINARY_SPLIT_THEOREM
PASS_NO_HIDDEN_182_443_FACTORS_INSIDE_13_LEVEL_RECURRENCE
PASS_EXACT_8192_SCALING_ONLY
PASS_17_CALL_PRUNING_MATH_CORRECTNESS

REFINE_RECOVERY_ORACLE:
rho correction may occur either
  at leaf alignment
or
  fused into L0..L3 recombination constants

This is not a complete candidate-correctness PASS.

The contribution-level uncertainty reduced this turn is important: Turn 6 left open whether the proposed 17-call algorithm was only a combinatorial schedule that might fail in the actual nontrivial slot algebra. That uncertainty is now removed mathematically. If the pending implementation witness fails, we can distinguish:

failure to realize a mathematically valid recurrence → implementation error;
versus a failure of the recurrence itself → now ruled out for this specific local algebra.

The CORRECTNESS_GATE remains blocked pending concrete implementation/native evidence.

NOVELTY_STATUS stays PREFLIGHT; Security and Value stay pending.

Next single decisive test: when BOOT-T7-RECOVERY-WITNESS-20261102 is delivered, independently audit its concrete source/output against this exact invariant:

𝑁
13
,
𝑗
=
8192
𝑧
𝑗
,
N
13,j
	​

=8192z
j
	​

,

plus either of the two equivalent rho-handling factorizations above, and finally exact 
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
 
mod
 
625
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

mod625.

<PAPER_CANDIDATE_UPDATE>
{"CANDIDATE_ID":"legacy-484479fe4613","RANK":1,"STATUS":"ACTIVE","PHASE":"CORRECTNESS_GATE","PAPER_THESIS":"Hypothesis under validation: reduce Aung et al.'s repeated MultKey bottleneck by keeping five tagged RMFE branches independent through branch-local nonlinear HElib preprocessing, aggregating only exact post-divide reconstruction inputs, performing one shared recryptEkey reconstruction, and recovering the five exact Z_625 branch lifts with a target-pruned 17-call full-domain unpack before forming Aung correction outputs L0,L1,L2,L3.","IMPORTANT_PROBLEM":"Inherited important problem remains Aung et al.'s repeated per-branch MultKey cost in the canonical p=5,m=32768,w=512,k=5 Corr./TnM workflow. Turn 7 does not reassess problem importance.","BASELINE":"Primary baseline remains source-faithful Aung Corr./TnM at p=5,m=32768,w=512,k=5; secondary frontier remains matched vanilla HElib thin bootstrapping.","CLOSEST_PRIOR_ART":"Inherited prior-art state only. Geelen's power-of-two unpack recurrence is confirmed source prior art, but no independent complete novelty audit is performed in Turn 7; NOVELTY_STATUS therefore remains PREFLIGHT.","NEW_MECHANISM":"Hypothesis under validation: pre-tag five scalar branches; execute five branch-local forward/nonlinear preprocessing paths independently through rawModSwitch, newMakeDivisible and division by 5; aggregate post-divide pairs; reconstruct once; apply a pure power-basis inverse; execute a target-pruned 17-call coordinate recovery; correct the second physical slot's rho permutation/unit either at leaf alignment or equivalently inside the L0..L3 public recombination tables; then invoke Aung Algorithm 4.","CONTRIBUTION_TYPE":"ALGORITHM","FULL_CONSTRUCTION":"Canonical parameters remain p=5,m=32768,w=512,k=5,r=1,e=4,e'=1,q=626, temporary modulus 625, local degree d=8192, eta=125, J=[0,1024,7168,2048,6144], J-order labels [2,0,3,1,4]. Turn 7 proves the exact binary-recovery recurrence in E=Z_625[X]/(X^8192+182): at split level i, sigma^(8192/2^i) acts as the next-bit sign on the already-shifted node because v2(5^(2^(13-i))-1)=15-i and X^16384=-1. After 13 levels the leaf for coordinate j is exactly 8192z_j, so multiplication by 28 yields z_j exactly. Target pruning retains the same target leaves with 17 physical parent automorphisms. Rho correction may be factored into leaf constants or into the final 4x5 correction table.","CORRECTNESS":"Math-level recovery correctness has materially advanced. The 17-call structure is no longer supported only by active-node counting: the exact induction shows N_(13,j)=8192z_j for arbitrary full-domain dirty inputs in the actual local algebra Z_625[X]/(X^8192+182), with no hidden 182/443 unit inside the split recurrence. Normalization by 28 is exact. For the second physical slot, raw J-order leaves are rho-permuted and scaled; this can be corrected either before branch alignment or equivalently fused into the L0..L3 public constants, matching the inherited rho_pos=[0,2,1,4,3] and 443 compensation. Concrete Ctxt implementation/native correctness remains unverified and the pending BOOT-T7-RECOVERY-WITNESS-20261102 result is not inferred.","SECURITY":"No status-changing security evidence was produced. The split theorem uses only public Frobenius automorphisms, additions/subtractions and public unit monomials; complete resource/key/security parity remains pending concrete implementation evidence.","NOISE_PRECISION_DFR":"No new measured noise, precision, DFR or bitCapacity result was produced. The theorem confirms that the only deterministic algebraic normalization from the 13 splits is factor 8192, invertible modulo 625 by 28; inherited capacity ledgers are not upgraded to native predictions.","VALUE":"PENDING. No performance, latency, throughput, key-memory or RSS claim is made in Turn 7.","CRITICAL_BLOCKER":"Concrete current-candidate implementation/native witness remains the correctness blocker. The abstract 17-call recurrence itself is now mathematically closed for the actual local ring, so the pending witness must demonstrate faithful realization of this recurrence, correct normalization, rho handling and exact L0..L3 assembly.","NEXT_DECISIVE_TEST":"Independently audit the delivered BOOT-T7-RECOVERY-WITNESS-20261102 source and evidence against the exact invariant N_(13,j)=8192*z_j for all five targets, normalization by 28, and either valid rho-handling factorization (aligned leaves or raw leaves with rho_pos/443 fused into L0..L3), followed by exact Z_625 L0,L1,L2,L3 equality.","NOVELTY_STATUS":"PREFLIGHT","PAPER_READINESS":"NOT_READY","REOPEN_CONDITION":"If the concrete witness fails while respecting the mathematical recurrence, classify and repair at most the implementation/routing/constant-table layer; the local-ring binary-split recurrence itself should not be reopened absent contradictory evidence. If later independent prior-art audit finds the complete mechanism, update novelty to COLLISION and reassess the paper thesis.","CONSTRUCTIVE_DESIGN_SPEC":"Five branch-local tagged preprocessing paths through /5; post-divide Z0/Z1 aggregation; one ptxtSpace-625 reconstruction; pure power-basis inverse; 13-level binary split with tau_i=sigma^(8192/2^i), using plus for the even child and X^(-2^(i-1)) times minus for the odd child; prune children containing no target J; normalize accumulated factor 8192 with 28; obtain raw selected coordinates; handle second-slot rho permutation [0,2,1,4,3] and 182 unit via 443 either at leaf alignment or in the four correction tables; use J-order labels [2,0,3,1,4] and form exact L0,L1,L2,L3 before Aung Algorithm 4.","CORRECTNESS_GATE":"BLOCKED","SECURITY_GATE":"PENDING","VALUE_GATE":"PENDING","AUDIT_GATE":"PENDING","BASELINE_CORRECTNESS":"PENDING","GATE_JUSTIFICATIONS":{"CORRECTNESS_GATE":"The exact recovery recurrence is mathematically established, but complete ALGORITHM correctness still requires concrete current-candidate source/native evidence; the authorized recovery witness is pending and its result is not inferred."},"ASSESSMENT":{"MECHANISM_PROGRESS":true,"THEOREM_PROGRESS":true,"CORRECTNESS_PROGRESS":true,"SECURITY_PROGRESS":false,"VALUE_PROGRESS":false,"NOVELTY_PROGRESS":false,"REDUCES_CRITICAL_UNCERTAINTY":true,"EVIDENCE_GRADE":"MATH","BASELINE_MATCHED":false,"PERFORMANCE_CLAIM":false,"OBSTRUCTION_VALUABLE":true,"STRICT_NO_GO":false,"CREDIBLE_NEW_MECHANISM":true,"FRONTIER_CANDIDATES_REMAINING":true,"INDEPENDENT_AUDIT_PASSED":false,"VALUE_REVIEW_COMPLETED":false,"VERDICT":"PASS"}}
</PAPER_CANDIDATE_UPDATE>

<ORCHESTRATOR_CONTROL>
action: CONTINUE
milestone: false
requires_pi: false
independent_research_available: true
</ORCHESTRATOR_CONTROL> 

Copy for Word
