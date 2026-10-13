# Iteration 150 — Full-RNS-CRT modulus Q does not rescue one-free-native-opening scalar consistency at negligible error

Date: 2026-10-13. Human PI explicitly authorized I150 with “好的，请继续” following I149. One primary falsifiable compound claim: **single original h-MLE point opening plus full-CRT signed-short integer lift is sufficient for one-shot negligible component-consistency error with no extra PCS phase**, in a source Medium-like short-lift parameter regime. One decisive combined completeness-interval / explicit-degree-one soundness falsifier. Do not interpret as a compiled vFHE SNARK attack or new security theorem on the published protocol.

## Read before write / primary source

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` after I149 (sha `bebd5670e50f779f5b4896145fe90116af5d5758`), `findings/OPEN_RESEARCH_BRANCHES.md`, I149 `failures/vfhe-small-integer-mle-point-opening-crt-lift-iteration149.md`, I59/I60 original ideal-PIOP CRT soundness issue, I86 arbitrary-weight mask rank obstruction, I87/I94/I95/I136–138 prior expensive masked/PCS attempts. Source Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, IACR ePrint **2025/286**, original full **52 physical pages** from Research MCP GitHub mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, exact current official PDF VERSION_UNVERIFIED (source revision 2026-02-16 separately noted). This iteration freshly inspected primary §2 pp7–9: Def2.1 exceptional challenge set S, Theorem2.6 `δ=dℓ/|S|` for ring sumcheck, original MLE definition; §3.1 pp10–11: source `q0=∏p_i` RNS primes each format 2aN/d+1, each field factor is F_(p^d); §4.3 pp20–23 Eq22–23 diagonal scalar digit table `tβ={0,...,β−1}`; §5 pp25–26 CRT-field PCS point openings; §6 pp27–29 Medium `(N,L,d,c)=(8192,3,4,5)` and 49-bit primes, 20-bit lookup, Π_range reported upper input286720 ring elements.

**Parameter caveat:** §3.1 indexes `q0=∏_{i=0}^L p_i` while §6 cost counts `L N/d` components for `L=3`; avoid silently assuming whether active modulus has 3 or 4 prime factors. Audit BOTH optimistic Lprime=3 and Lprime=4 (4-prime scenario gives more generous room). Also treat I90 `ell=19` from padding size2^19 and `beta=2^20` as conditional conservative envelope: author's Medium 20bit table with nominal `c=5` may imply an actual smaller digit radix (e.g. 2^4=16), not verified source exact table-oracle structure. Evaluate **beta=16** AND **beta=2^20** so conclusion does not rest on the pessimistic radix. This is a source-like parameter ***gate***, not a source claim of exact ell or radix.

## ONE primary hypothesis / falsifier

**[HYPOTHESIS]** Unlike I149's failed small single-prime lift, using the **entire active integer RNS modulus `Q=∏_{i=1}^{Lprime}p_i`** and a common *balanced ordinary integer* coordinate challenge set `S⊂Z`, a verifier can authenticate the already-committed CRT projections at one existing source `h~(r)` PCS evaluation and require their CRT recombination `A` be in the source-known honest-integer MLE interval. Hope to achieve (1) perfect honest completeness via a unique interval-valued lift, **and** (2) at least 128-bit rejection of a fixed non-diagonal, componentwise-legal digit table with **one** shared random point and no extra original h PCS evaluations/Sumchecks. This is a PROPOSED NEW REPAIR, not actual source verifier behavior.

**[DECISIVE FALSIFIER]** For paper-source 49bit RNS count Lprime3 and generous4, derive the LARGEST possible integer challenge set `S` under the **guaranteed-unique whole-Q integer-interval** condition for all honest digit tables. Then construct one fixed componentwise legal but non-diagonal scalar digit MLE whose projected opened values agree with a valid interval-valued full-Q integer on at least `1/|S|` of challenges. If `|S|` is orders of magnitude below2^128 and the false witness passes a single opening with ≥1/|S|, one-shot 128-bit hypothesis FAILS. This test assumes native original h PCS is binding and first committed before random r; *does not require breaking PCS*.

## Honest interval width and OPTIMAL integer alphabet geometry

For Boolean basis `χ_b(r)=∏_j ((1−r_j) if b_j=0 else r_j)`, with `0≤h(b)≤β−1`, the ordinary integer MLE value `V_h(r)=Σ_b h(b)χ_b(r)` belongs to the interval
```
 I_r = [ (β−1) Σ_{χ_b(r)<0}χ_b(r),   (β−1) Σ_{χ_b(r)>0}χ_b(r) ].
```
This interval contains0 and has **EXACT width**
```
 width(I_r) = (β−1) Σ_b |χ_b(r)|
            = (β−1) ∏_{j=1}^{ell} (|r_j|+|1−r_j|).
```
At a coordinate alphabet S, its maximum is `W(S)=(β−1) H(S)^ell` where `H(S)=max_{t∈S}(|t|+|1−t|)`. For the **simple unique integer lift by an interval known from r**, the source-independent sufficient/no-ambiguity strategy is `W(S)<Q`, so no two different integers in the interval reduce to the same full-Q residue. This is NOT a universal necessity for all hypothetical proof systems or non-interval-representable digit sets.

For **any M=|S| distinct integers**, minimizing maximum H(S) is achieved by choosing S roughly symmetric about 1/2; the number of eligible integers with `|t|+|1−t|≤H` for odd H≥1 is at most H+1. Consequently `H(S)≥M−1`, even for BEST symmetric alphabets. Given only per-prime `p_i<2^49`, the actual Q satisfies `Q<2^(49 Lprime)`. Necessary *for this certified width template*:
```
 (β−1)(M−1)^ell < 2^(49 Lprime).
```
An optimistic ceiling (attained relative to the *artificial upper-bound modulus* 2^(49 Lprime), not guaranteed for actual primes) is obtained with odd H and symmetric integer `S={−k,...,k+1}`, `|S|=H+1`. At ell=19 the EXACT ceilings by integer exponent arithmetic are:
```
     Lprime   beta        max H     |S| upper  log2(W)          1/|S| floor
       3        16           183          184      146.705188        1/184
       3       2^20          101          102      146.506017        1/102
       4        16          1105         1106      195.993673        1/1106
       4       2^20          613          614      195.935121        1/614
```
Since actual primes are **strictly less** than2^49, real achievable alphabets may be smaller. In the most favorable generous four-prime and smaller-radix case `|S|≤1106`, the univariate degree-one root collision lower bound will be ≥1/1106≈9.04e−4, nowhere near 2^−128. Original source Theorem2.6 soundness certification `δ=d ell / |S|` independently cannot certify 128bit at these sizes (e.g. at three-prime beta16 `ell/|S|=19/184≈0.1033` even taking d1). Note upper-bound failure alone not proof of an attack, so next exact false witness matters.

**One-shot lower bound without violating componentwise digit membership.** Choose ANY integer `t∈S∩[1,β−1]` (optimized symmetric S contains t=2 for all displayed cases with β≥16); before r, commit two native CRT projections corresponding to `h_1(X)=t−X_1` and `h_2(X)=0` (all additional RNS and extension-field factors can be set0). At every Boolean b, `h_1(b)∈{t,t−1}⊂{0,...,β−1}` and `h_2(b)=0`; so each projection has individually LEGAL SCALAR digits and all polynomial degrees are ≤1, yet the Rq Boolean digit is **NONDIAGONAL** across CRT factors. At verifier challenge r with first coordinate `r_1=t`, **all field evaluations equal0** and full-Q CRT reconstructs **A=0∈I_r**. Thus this illegal common-digit witness is accepted by the PROPOSED single-point CRT short-lift equality test with probability ≥1/|S| (uniform independent coordinate r1∈S). Choosing a larger alphabet can't fix both guarantees within the indicated modulus size. This is NOT an accepted transcript for the entire original vFHE `Π_range=Π_decomp+Π_beta_range`; other checks may reject it. It falsifies only the added single-opening consistency mechanism's purported strong standalone soundness.

## ONE exact small full-Q CRT experiment

Executable offline stdlib script **`/mnt/data/i150_vfhe_full_crt_lift_challenge_tradeoff.py`** SHA256 `2352fc8e1120e215e35e0a0ee8d98dcdd4ec866ce56cac850bd32b1ff6dafde7`, executed and verified.

- Choose legal toy `p0=29,p1=37,Q=1073,ell3,beta4,S={−1,0,1,2}, |S|4`. Full-Q honest MLE integer interval at every r has width at most `(β−1)*3^3=81<Q`. This is **a successful complete/unique full-CRT signed-integer interval regime**; in contrast to I149, honest MLE value42 admits a unique lift even though42>29.
- Construct precommitted non-diagonal but CRT-componentwise-legal digit polynomials `h0(X)=2−X_1`, `h1(X)=0`. Boolean vectors in lex order `(2,2,2,2,1,1,1,1)` and `(0,0,0,0,0,0,0,0)`; all digits in {0,1,2,3}, but there is NO common scalar table index at Boolean positions.
- Exhaust ALL `|S|^ell=4^3=64` point challenges. Evaluate exact MLE basis, native residues, signed centered full-Q CRT recombination A (solving A≡h0(r) mod29 and A≡0 mod37), and compare to the **source-known per-r honest integer interval I_r**. Exactly **16 of64 challenges accept**, and these are precisely r1=2. Therefore false accepted with probability **1/4**, in spite of honest completeness/unique full-Q lift width81<Q and original field-oracle binding (polys fixed before challenge). No actual PCS proof or original PIOP transcript compiled.
- Also exact-integer sweep shows optimistic |S| ceilings (3/4 primes, β16/2^20). The actual prime lists and full source h-dimension remain unverified, so numerical ceilings are conditional not measured implementation settings.

## Scientific interpretation

**[FAIL narrow full-Q one-free-opening ≥128bit repair]** Moving from single p to full Q fixes the I149 **honest integer overflow** issue in a sufficiently small challenge set, but cannot simultaneously support a large enough integer challenge set for one-shot negligible detection of a non-diagonal CRT digit. The problem exists **even when no-wrap/interval uniqueness is satisfied** (toy exact soundness failure1/4). Max optimistic 3/4 prime challenge alphabets at ell19 cannot provide even~2^−10 one-point collision floor, far from128bit. The elementary `t−X_1` forged component is legal under every individual digit table; the false *diagonal* property is detected only if random challenge avoids its root. It is a counterexample against our **proposed new one-point integer-lift check**, **not** the original protocol and not a universal theorem about external integer commitments, full-Q PCS, repeated independent challenges, or other proof architectures.

**[LIMITATIONS]** `Q` may involve 3 or4 RNS primes due the §3.1 vs §6 notation (both covered), actual h MLE ell/beta not confirmed and could yield different numeric ceilings, random challenges might live in extension fields `F_(p^d)` in the original protocol (our new proposed signed integer lifting requires special ordinary integer challenges). Repeating checks or replacing proof system can amplify security but introduces independent challenge/PCS costs; I94/I95 already found this expensive in source Brakedown. Some noninterval short representations or cryptographic protocols could work; this bounds only direct full-Q interval-lift one-point strategy. No novel algorithmic contribution, no threat claim about deployed vFHE. The original source revision/corrected Theorem4.8 official binary remains VERSION_UNVERIFIED. No author outreach.

## End
STATUS: **FAIL_SOURCE_BOUND_FULL_Q_SINGLE_EXISTING_POINT_128BIT_CRT_LINK / PASS_EXACT_NONDIAGONAL_WITNESS_AND_INTEGER_CHALLENGE_FRONTIER / HUMAN_REVIEW / NO_ACTIVE_HYPOTHESIS**.
RESULT: For simple certified honest integer interval width `(β−1)H(S)^ell<Q` and Medium-like ell19, 3×49bit RNS primes allow at most optimistic |S|184 (β16) or102 (β2^20), 4×49bit at most1106 or614; false scalar digit components `h1=t−X1,h2=0` pass shared existing one-point full-Q lift with probability ≥1/|S|. Exact toy full Q1073, ell3 beta4, S4 interval width81<Q, false CRT digit witness accepted16/64. Full intended 128bit cannot follow from one point under this proposed mechanism, so no cheap escape from archived I94 native-PCS soundness amplification.
NEXT_ACTION: I151 ONLY with PI explicit approval: recommend PARK the "reuse one h~(r) PCS eval plus ordinary integer full-Q interval lift" shortcut. If pursuing original CRT common-index repair, demand a genuinely distinct cross-characteristic scalar commitment/lookup or independently secured multi-point PCS and source cost model; do NOT repeat I149 single-prime, I150 full-Q one-point, I148 mask alphabet or archived I95/I136–138. Consider pivot to more algorithmic FHE backlog for scientific novelty. No authors contacted.
STATE_UPDATE: YES — precise new single-point whole-Q soundness obstruction with honest interval completeness in the very same toy; preserves original I59/60 issue OPEN/HUMAN_REVIEW.
