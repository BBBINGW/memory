# Iteration 148 — Bounded-integer rank-one fingerprints sharpen vFHE CRT component-consistency mask checks, but do not fix Brakedown cost

Date: **2026-10-13**. PI authorized I148 (“好的，请继续”) following I147 and delegated pivot from low-novelty SPRU to open vFHE CRT scalar-consistency backlog. Exactly **one primary new technical hypothesis and one source-parameter + tight toy arithmetic falsifier**. This note introduces OUR modified alphabet for random rank-one masks; it is NOT an original vFHE paper feature or an end-to-end proof.

## Read-before-write, archives, and source

Read Research MCP `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → `STATE.md` after I147 (SHA `1f4ab35f6735e03b72973d2e0222eef1840f56bf`) → `findings/OPEN_RESEARCH_BRANCHES.md`; I59 `findings/vfhe-crt-lookup-cross-component-soundness.md`, I60 `findings/vfhe-crt-full-range-piop-and-commitment-audit.md`, I63 `findings/vfhe-crt-diagonal-lookup-local-algebraic-no-go.md`, I77 `findings/vfhe-external-commitment-crt-full-opening-link-iteration77.md`, I78 `failures/vfhe-batched-crt-aggregate-without-shared-integer-opening.md`, I83/I84/I85 source privacy/witness constraints, I87 `findings/vfhe-rankone-bernoulli-mask-constant-detection-iteration87.md`, I88, I90, I91, I94 `findings/vfhe-fourfold-scalar-sumcheck-amplification-cost-iteration94.md`, I95 `failures/vfhe-bounded-public-A-direct-brakedown-repair-archived-iteration95.md` (do not re-propose archived **full** repair), and I136–I138 independent challenge vs Brakedown PCS cost failures. The present round is **mask alphabet only**, not another PCS folding fix.

Read original **full PDF** Research MCP `read_eprint_pages("2025/286",20–23), (25–26), (28–29)`; 52-physical-page GitHub mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, official latest `VERSION_UNVERIFIED`. Source §4.3 Eq(22)–(23) physical pp20–21 specifies a ring-valued `h` whose Boolean points MUST belong to diagonal scalar integer table `{0,...,β−1}⊂Rq`, and Lemma/Theorem 4.8 p22–23 attempts range lookup through CRT field checks. Source §5 pp25–26 independently commits each CRT field with Brakedown, one ring opening = μ native PCS openings. §6.3 p29 describes Medium circuit W1,D1,L3,N8192,c5, max range input 286720 ring elements, 20-bit lookup table, and §6 p27 uses 49-bit RNS primes. Previous I90 conservatively modeled `m=2^19=524288` padded envelope (NOT author's verified single-h digit-oracle layout), `β≤2^20` under ordinary 20-bit table interpretation (NOT independently verified c=5 digit decomposition), and p_min≥2^48. This large β is deliberately a pessimistic upper bound.

## ONE primary technical hypothesis and decisive test

**[HYPOTHESIS]** With componentwise legal scalar digits `h_k(i,j)∈{0,...,β−1}` fixed by sound native field commitments **before masks**, and one **public canonical integer** aggregate A for each mask checked as equal to all component-field weighted sums, switching from I87 Bernoulli rank-one masks `α_ij=u_i v_j`, `u_i,v_j∈{0,1}`, to small **bounded integer** independent rank-one masks `u_i,v_j←uniform{0,...,D}` can preserve *exact cross-CRT no-wrap integer equality* while reducing the masks necessary for a ≤2^-136 component-consistency miss bound by at least 5× at conservative source-inspired Medium parameters, without adding more PCS terminal evaluation families. This is a LOCAL mask-check improvement; no hypothesis about original vFHE soundness repair or 10× total verifier bytes.

**[FALSIFIER/ONE TEST]** Enumerate the LARGEST integer alphabet D satisfying `m(β−1)D²<p_min` with source conservative m2^19,β2^20,p_min≥2^48. Derive a tight per-mask anti-concentration bound for any fixed nonzero CRT discrepancy matrix `Γ` over F_p^d, compute number of independent masks for 136-bit target, compare I87's Bernoulli rank-one t328 mask computations/description. Validate single-entry tightness and no-wrap by one exhaustive p29,p37,m4,D2 toy over all distinct Boolean-vector pairs and rank-one mask choices. Fail if D≤1, mask count reduction <5×, or discrepancy can be hidden under no-wrap.

## Algebraic detection lemma

Let `Γ∈F^{a×b}` be any nonzero discrepancy between TWO precommitted projected scalar digit matrices (F arbitrary field, including F_(p^d) extension), with `p>D`. Sample independent `u∈{0,...,D}^a`, `v∈{0,...,D}^b`, reduced to F.

Choose a nonzero row Γ_i and a pivot column j with Γ_ij≠0. Condition on all v_l except v_j: `(Γv)_i=C+v_j Γ_ij` has D+1 distinct values, so **at most 1** value makes it zero. Hence `Pr[Γv≠0]≥D/(D+1)`. For any nonzero vector w=Γv, repeat with u_i pivot: `Pr[u^T w≠0 | w≠0]≥D/(D+1)`. Therefore
```
  Pr[u^T Γ v = 0] ≤ ε_D := 1−(D/(D+1))² = (2D+1)/(D+1)².
```
This is **tight** for Γ with exactly ONE nonzero entry: event `u_i v_j=0` has probability `1−(D/(D+1))²`. The proof requires masks independent of PRECOMMITTED fixed witnesses and native per-field digit validity, and p>D ensures distinct alphabet residues. Unlike CRT-glued ring constraints alone, the verifier must parse/check ONE **ordinary bounded integer A** and compare its embedded value to all field aggregates, with actual native original-h PCS/sumcheck binding. If field-component sums are unequal as INTEGERS, no A can match both; even if prover chooses A **after** seeing mask, the chance any shared A exists is ≤ε_D.

**No-wrap gate:** With `m=a b`, `0≤h_k(i,j)≤β−1`, and `0≤u_i v_j≤D²`,
```
    0 ≤ S_k = Σ_ij u_i v_j h_k(i,j) ≤ m(β−1)D².
```
If RHS < every CRT prime p_k, then `S_k modp_k` canonically lifts to THE SAME ordinary integer S_k; equality to public canonical `A∈[0,T_D]` checked separately in every F_(p_k^d) is therefore a genuine cross-characteristic integer comparison. Do **not** merely publish one CRT **ring element** A_fake or an uncertified per-field residue (I77–I78 no-go). If no-wrap fails, matching modular projections is not sufficient to infer integer equality. Direct binary soundness check of all per-component digits, actual sumcheck, PCS extraction/Fiat-Shamir and accepted-proof privacy NOT implemented here.

**Rank-one MLE factorization:** `α~(X,Y)=u~(X)v~(Y)` still holds for small integer vectors, so verifier point evaluation uses O(a+b) native field/ring arithmetic rather than materializing all m entries. Computing aggregate sums on prover side still takes O(m) terms and requires real ring-h oracle binding; sampling u,v and evaluating their MLEs is *not* a complete native PCS evaluation or a speed benchmark.

## Exact conservative source-parameter cost frontier

Set `m=2^19=524288`, `β=2^20` worst allowed assumption, smallest guaranteed 49-bit CRT prime bound `p_min≥2^48=281474976710656`. With integer arithmetic,
```
D_max = floor(sqrt((2^48−1) // (m(β−1)))) = 22.
T_22=m(β−1)*22² = 266081560166400 < 281474976710656.
T_23=m(β−1)*23² = 290820548198400 > 281474976710656.
ε_22 = 45/529 ≈ 0.08506616257;
−log₂ ε_22 ≈ 3.55527081578 bits per mask.
```
For mask-only miss error <=2^-128 require `t=37` such masks (I87 binary t309); for <=2^-136 require `t=39` (I87 binary t328). This is **8.410256× fewer masks** at 136-bit component mismatch detection, while not changing FOUR independent native sumcheck/Brakedown PCS evaluation families used in I94, or any other system error budget.

At an illustrative balanced split a512,b1024 (m524288), each integer u,v is 0..22 (5 bits), mask descriptions:
```
136-bit target:
binary I87: t=328, (a+b)*328 =503808 bits =62976 B =61.5 KiB
new bounded: t=39, 5*(a+b)*39 =299520 bits =37440 B ≈36.5625 KiB.
```
So **mask count/arithmetic/evaluation decreases 8.41×, mask description decreases ONLY 1.68×** since entries grow to5 bits, and source extra **four** expensive per-field Brakedown openings stay as expensive as I94. Weighted-multiplier operations may be slower than bit-mask additions; no actual runtime claimed. The 136-bit target is an arithmetic screening subbudget, not entire proof 136-bit security; native sumcheck mixing/PCS/Fiat–Shamir have separate errors. Paper's c5 vs formal c=2^γ and real h-digit-oracle m remain unverified; numbers are conditional NOT chosen implementation parameters.

## ONE exhaustive toy and reproducibility

Executed offline stdlib exact file `/mnt/data/i148_vfhe_bounded_alphabet_rankone_mask.py`, SHA256 `ac559b855bc344cf6b9c4c6b79361da6665cbaf39b781a27a6b4ff026e9892ef`. Source conservative cost and tight ratio via Python Fraction; tiny CRT instance two primes p29,p37, field component digit vectors Boolean length m4 reshaped2×2, rank-one alphabet D2, scalar aggregate ≤m(β−1)D²=16<29. Exhausted **240 ordered distinct pairs** h0,h1∈{0,1}^4 (16×15), and all `3²*3²=81` u,v rank-one masks, counting integer-sum equality:
```
max #accepting masks = 45 of 81 = 5/9,
equal to ε_D=(2D+1)/(D+1)² =5/9;
all honest native sums are ≤16.
```
At real paper-conservative dimensions symbolic exact algebra (not full transcript) confirms D22 and t39; did **NOT** enumerate source-length mask vectors or run native PCS. This toy verifies lemma tightness and no-wrap, not cryptographic soundness.

## Scientific assessment

**[PASS, sharply scoped]** A small-integer (D22) rank-one mask can lower fixed-discrepancy screening from I87 t328 to t39 under I90's pessimistic **m2^19,β≤2^20,p_min≥2^48**, preserving no-wrap and O(t√m) mask-MLE evaluation. This is a new conditional parameter/cost observation beyond the previously tested **binary** I87 masks, not a new PCS.

**[NOT a soundness fix]** Requires all CRT projections independently proved legal digits, a **shared bounded canonical public integer A** truthfully certified by *the very same* committed h field sumchecks, commitment order, fresh challenge randomness, I94 four independent sumchecks to suppress ~2^-49 native error, original source μ Brakedown field PCS opens and real security budget. I63 ring-only CRT algebra no-go and I95 archive remain; altering mask alphabet neither removes I136–I138 4-opening cost nor produces a >10× end-to-end communication gain. No Fiat–Shamir, full VC IND-CPA/VO privacy, proof system implementation, security exploit, actual author flaw, latest edition identity, or runtime measurement.

**[NOVELTY]** Rank-one fingerprints, pivot anti-concentration and larger sample alphabets are elementary Freivalds-style techniques. Likely NO standalone publication contribution; marginal improvement of an archived expensive PCS repair. Preserve as a small conditional optimization in Backlog without resurrecting I95 as active.

## End of iteration

**STATUS:** **PASS_BOUNDED_ALPHABET_RANKONE_MASK_NARROW_COST_GATE / FAIL_END_TO_END_10X_PCS_COMMUNICATION_GOAL / HUMAN_REVIEW / NO_ACTIVE_HYPOTHESIS**.
**RESULT:** Tight `Pr[miss]≤45/529` under D22, source conservative no-wrap and 8.41× fewer rank-one component-discrepancy mask tests for 136-bit mask-only error; 1.68× fewer raw mask description bytes, but FOUR independent original F.2 ring PCS evaluations still required for I94 full-security route, likely dominate.
**NEXT_ACTION:** I149 only on PI authorization: because this is only a routine fingerprint alphabet gain atop a source-expensive archived repair, **PARK it** unless a genuinely different across-CRT integer linking proof / arbitrary-rank PCS is presented with source-costed ≥10× end-to-end savings and full soundness/privacy. Consider switching from vFHE cheap verifier-mask tweaks to a higher-novelty backlog issue rather than trying more alphabets; human PI decides pivot. Preserve private I59–60 CRT original issue and refrain from author contact/public disclosure.
**STATE_UPDATE:** YES — one exact new weight-alphabet parameter/cost result, but do NOT change parent vFHE OPEN/HUMAN_REVIEW or revive archived I95 branch.
