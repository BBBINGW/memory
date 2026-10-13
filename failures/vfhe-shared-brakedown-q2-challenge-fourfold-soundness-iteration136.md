# Iteration 136 — Common Brakedown PCS q2 suffix destroys independent fourfold sumcheck amplification

**Date:** 2026-10-13. PI said "好的，请继续" after I135, authorizing ONE next iteration and selection from backlog. Target vFHE CRT range consistency, not reopening the **I88–95 bounded-public-A/direct-Brakedown repair** as an active implementation. Only test this NEW *cross-proof PCS compression shortcut*, not another arbitrary CRT counterexample or full proof design.

## Read before write / source versions

Read `STATE.md` after I135, `findings/OPEN_RESEARCH_BRANCHES.md`, previous vFHE `logs/vfhe-state-2026-10-12-pre-paco-handoff.md`, I59/I60 CRT lookup ideal PIOP findings, I63 `findings/vfhe-crt-diagonal-lookup-local-algebraic-no-go.md`, I66 code and I77 external commitment finding, I86 rank obstruction, I94 `findings/vfhe-fourfold-scalar-sumcheck-amplification-cost-iteration94.md`, and I95 `failures/vfhe-bounded-public-A-direct-brakedown-repair-archived-iteration95.md`. Avoid known pure R-local scalar checks and naive full expensive external PCS links.

Original Cascudo, Costache, Cozzo, Fiore, Guimarães, Soria-Vazquez, *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, IACR ePrint **2025/286** https://eprint.iacr.org/2025/286; via Research MCP 52-physical-page mirror PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, **VERSION_UNVERIFIED** vs latest official PDF. Primary §2.2 p9 Theorem 2.6: ℓ-variable ring `Π_sum` sends `g_j(X)` and verifier samples `r_j∈S` each round, checks endpoints and terminal `g_ℓ(r_ℓ)=f(r)`. Original Appendix F.2 **physical p51** Brakedown evaluation: `f(a)=⟨q1(a)·U_f,q2(a)⟩`; prover sends `v'=q1(a)·U_f`, terminal verifier checks `y=⟨v',q2(a)⟩`; testing phase may be shared over repeated evaluations, **but evaluation phase is distinct**. I94's additional fourfold masked public-A repair independently samples **both mixing rho and all sumcheck challenge tuples**, achieving only a conditional ideal soundness bound `((1+2ℓ)/p_min)^4`; original source Brakedown cost remains huge (μ field components times every ring opening). That specific direct repair was archived at I95, not the vFHE CRT issue.

## Exactly ONE research hypothesis / decisive test

[HYPOTHESIS] To compress four independent I94-style extra ring PCS evaluations, one can **force their Brakedown right query factors `q2(r^(j))` to be identical**, by letting the four sumcheck runs share the final `r_ℓ` (or suffix coordinates) while retaining independent mixing challenges `ρ^(j)` and independent other `r_i^(j)`; the *fourth-power* soundness amplification still holds. If true, a linear combination of the four left vectors `q1(r^(j)) U` against common q2 could be checked with one vector PCS evaluation rather than four (this batch interface itself would still need proof/security and does NOT follow automatically from original F.2).

[FALSIFIER / minimal test] Construct a legal degree-≤2 sumcheck prover for false claim over scalar S=F29, with FOUR independent nonzero public claim values T_j (allowing different rho_j) and independent first ℓ−1 challenges but a shared final challenge, such that **all four false proofs are accepted on the SAME single event `r_ℓ=1` with probability 1/29**, not the nominal fourth power. Use ℓ=4, exact modular arithmetic. This kills any claim that sharing terminal suffix is free of a soundness consequence.

## An explicit exact cheating prover; no cryptographic assumptions

Take source-compatible small scalar subring R=Z_(29·37), scalar challenge set S={0,1,...,28}, and true virtual polynomial `f_j(X_1,X_2,X_3,X_4)≡0` in R for EACH run j∈{1,2,3,4}. Each run asserts the false claimed hypercube sum `Y_j=T_j` where `T_j∈{1,...,28}`. For example set T=(1,2,5,11), representing four independent chosen nonzero random-mixing outcomes on a fixed bad public aggregate with h=0 and public A=1. Each prover knows T_j before sending its first sumcheck polynomial, as in original protocol.

A cheating prover for any run with initial claim Y_j=T_j sends:
```
  round a=1:  g_1(X)=T_j / 2
  round a=2:  g_2(X)=T_j / 4
  round a=3:  g_3(X)=T_j / 8
  round a=4:  g_4(X)= (T_j / 8)*(1-X)
```
All operations are in R, with 2 invertible (29 and37 odd). In every first 3 rounds, `g_a(0)+g_a(1)` equals the previous claim and `g_a(r_a)=T_j/2^a`, **regardless** of r_1,r_2,r_3. The fourth likewise has `g_4(0)+g_4(1)=T_j/8`. The source terminal check is `g_4(r_4)=f_j(r)=0`; for all nonzero T_j∈[1,28]⊂R this holds iff `r_4=1` when r4∈S. This uses degree 0/1 `g_j` and fits source's max-degree 2.

For four independent sumcheck transcripts but ONE shared `r_4`: `Pr[all accept]=1/29`. With independent `r_4^{(j)}`: `Pr[all accept]=(1/29)^4=1/707281` **for this fixed prover strategy and conditional on four nonzero T_j**. A larger sample bound is not being claimed; I94's general theorem upper bound contains other mixing/sumcheck errors. Even with independently random `ρ^(j)`, the common r4=1 event guarantees all accept for ANY T_j including zero (for T=0 the proof can be honest), so the non-amplifying floor survives.

[EXACT LOCAL TEST] Python integer modular assertions for p29, ℓ4, T=[1,2,5,11], four distinct first-3 r-vectors, all 29 shared r4 values: **exactly one** r4 (1) accepts all four. Fully independent last variables would give 1 in 29^4 possible tuples under the same strategy. No compiled SNARK, PCS, Merkle/Brakedown implementation, Fiat–Shamir security proof, RNS noise, or deployed attack was tested. Formal equations also hold componentwise in source-style CRT ring because T/8 and endpoints use scalar units.

## Interpretation and scope

- [NEGATIVE] The proposed **shared final q2/suffix challenge** destroys I94's conditional *independence-based* error bound. A verifier cannot safely claim four independent soundness trials after forcing one or more terminal sumcheck variables to coincide merely to batch a PCS vector opening. The exact acceptance probability for this adversary is Ω(1/p_min), not O(p_min^-4). At ~49-bit p_min this is far above 128-bit security target.
- [SOURCE] Brakedown F.2 does **not** already assert multi-point evaluation proof batching. Even if the q2 vectors happen to match and an algebraic linear fold exists, it needs an explicit independent security proof; sharing terminal randomness to enable that fold is specifically unsafe.
- [LIMIT] This does NOT prove that all batched PCS constructions are impossible. One may preserve fully independent sumcheck coordinates while using a **new** multivariate linear-functional PCS / batched-opening argument that handles four distinct q2 vectors, potentially with improved communication. No such scheme/verified cost or novelty found in this iteration. Reusing testing phase was already source-defined and safe; this note critiques only coalescing the evaluation suffix.
- [PRIOR] Correlated randomness and soundness amplification are standard cryptographic concerns. This is a rigorous *cheap shortcut filter*, not publishable proof-system theory. The original authors' Pi_range cross-component soundness concern is unchanged and still requires review; I95 archive remains restricted to its original specific attempt. No authors contacted or public vulnerability disclosure.

## End

STATUS: **FAIL shared-Brakedown-q2 fourfold amplification / PASS exact correlated-challenge falsifier / HUMAN_REVIEW**.
RESULT: Shared final r_ℓ gives an explicit false-claim sumcheck prover with acceptance probability 1/29 across four alleged repetitions (vs 1/29⁴ under independently sampled last variables), despite fresh mixing/nonterminal challenges. Thus do NOT pursue cheap q2-equalized opening aggregation as a soundness-preserving fourfold repair. New PCS with *independent* terminal queries is a separate unresolved research problem.
NEXT_ACTION: I137 requires PI authorization. Recommend PARK *this* identical-q2 batching shortcut. If PI wants vFHE further, require ONE genuinely different batch PCS construction that preserves all independent terminal coordinates (including a concrete rank/communication bound versus original F.2 and a falsifiable binding/security condition); otherwise choose MRFHE noise-aware full pipeline or another higher-upside backlog target. Do not re-open archived I88–95 or repeat locality folklore.
STATE_UPDATE: YES — novel-to-this-project negative result and corrected admissible PCS-batching design condition; long-term vFHE remains OPEN/HUMAN_REVIEW.
