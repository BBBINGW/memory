# PVFHE-P11 — Prechallenge full-opening knowledge anchor avoids square-root binding error (conditional)

**Checkpoint:** 2026-10-15 Asia/Tokyo. Independent PVFHE-P11 COMPLETED; P12 NOT STARTED.
**STATUS:** PASS new *conditional* **classical interactive** source-interface protocol and linear binding-loss derivation; UNCLEAR actual CMNW adaptive Fiat–Shamir online extraction, combined Ring-R1CS implementation, parameter security and QROM. No original CMNW/PVFHE attack alleged.

## Read before write / primary source / isolation

Read START_RESEARCH_SESSION.md SHA 6235e9d376a8b143719a40178132f02a6a41d4f3, RESEARCH_PHILOSOPHY.md SHA 49da3f7fa3e75f502525482ce4a7ab6867, AGENT.md SHA b3e73b2c7f852c05aa674dd97b632e9f99ac5f22, global STATE.md SHA a8b244fea294e3cf9aa7bf16cb18b7d67e5f986f (parallel vFHE V29), previous P10 findings/pvfhe-P10-classical-rom-outer-forking-security-budget-gate.md SHA 1c7b985c36fd5aa42c4bc40868491c3423c1e57b, and P08 SHA 96b05e032688f16a5ae24e198a815acc8ed3214f. Target P11 absent; do NOT edit shared state or parallel tracks.

**Original primary sources fully available through Research MCP, versions unverified:**
- Cini–Malavolta–Nguyen–Wee, *Polynomial Commitments from Lattices: Post-Quantum Security, Fast Verification and Transparent Setup*, CRYPTO 2024, ePrint **2024/281** https://eprint.iacr.org/2024/281, mirror 52pp SHA256 **a9be7b5c1e9024d2d0c03865978d7f3ea1ed941dce8883f93f9576ae46a73b73**, VERSION_UNVERIFIED. Physical p4 §2.1 explicitly states **no hiding is required**, pp11–13 Def3 *relaxed binding with slack*, Def6 *classical stateful adversary / rewindable knowledge soundness*, Def8 full functional-commitment evaluation witness; p22 Thm2 enlarged extraction norm beta_*=(2r_fold*kappa_fold)^ell beta; p24 Thm4 multilinear PCS. Mathematical font extraction/version quality caveats; original binary screenshot parity not certified.
- Huang–Li–Mao–Zhang, *Fully Homomorphic Encryption with Efficient Public Verification*, ePrint **2024/1764**, mirror 29pp SHA256 **7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089**, VERSION_UNVERIFIED, pp8–9 source Ring-PCS interface, p21 Ring-R1CS adaptation. Our anchor protocol is NOT present in either paper.

## ONE primary falsifiable technical hypothesis and decisive source-contract test

**[HYPOTHESIS P11]** P10's sqrt(eps_B) loss is not unavoidable if we add **ONE CMNW PC.Eval at a fixed public point BEFORE the external Galois identity-test challenge**: a source single-evaluation knowledge proof extracts the *entire committed polynomial* at prechallenge time, enabling a LINEAR binding-error soundness bound for subsequent postchallenge evaluations.
**[DECISIVE FALSIFIER]** Source-read CMNW's precise evaluation extraction witness relation. If it gives only a scalar claimed value, this anchor fails; if it extracts (whole polynomial, opening state), derive a correct prefix-coupled classical security bound, account for slack, extra proof complexity, oracle FS ordering, and test exact algebraic challenge behavior and sample bit-security budget. Do not claim automatic adaptive FS/QROM security.

## Key source FACT / mechanism

CMNW physical p13 Definition 8 specifies each evaluation statement (ppCM, C, x, u) with witness **(f,st)** satisfying BOTH:
    Open(ppCM,C,f,st,⊥)=1  AND  f(x)=u.
Its knowledge-soundness extractor is a full-polynomial **opening extractor**, *not* merely a procedure returning point value u. The source's p4 technical overview explicitly says its PCS does NOT require commitment hiding, so no hiding-based no-go argument is appropriate. CMNW Def6 allows REWINDING a stateful adversary in the classic setting (full new sequential composition still to be verified).

Pick a public Boolean vertex x0 of an **augmented witness polynomial F** and pad the coefficient at this vertex to public zero (e.g., F(0,...,0)=0). This padding is a NEW ordinary witness-reindex/zero R1CS constraint, not in original paper. Then an anchor evaluation proof (C,x0,0) does not reveal a secret witness entry, but under CMNW knowledge soundness may extract the WHOLE F and valid opening. Only this full-opening property, not mere correctness of u=0, solves the pre-r extraction problem.

## New protocol, ONE extra source PC.Eval [DERIVATION, conditional]

The original P05 extension uses one enlarged committed witness F(b,T) with b=1 selecting masked reconstructed BitDecomp values Y(T); ordinary ring-R1CS constraints link Y to original witness Z. In NEW protocol:
1. Prover fixes full public statement/selector and publishes the SAME commitment C to F. Verifier and prover finish an **interactive PC.Eval(C,x0,0)** proof at fixed public zero coefficient BEFORE ANY external r; rewindable classical extractor gets whole F0 and opening of C, bound beta_*.
2. Then verifier picks INDEPENDENT uniform external r in E^s, E has pairwise unit differences.
3. Prover fixes value claims and provides two authentic **independently internally challenged** evaluations (C,(1,r),v) and (C,(1,sigma^-1(r)),v'), checks v=sigma(v'), plus original R1CS linkage.

**Explicit assumptions:** (A) classical prefix-respecting extraction for the accepted anchor proof, with pre-r F0 and preserved original continuation distribution; (B) two post-r extractions with fixed public tuples and compatible stateful auxiliary information; (C) all three extract whole F/opening valid at extracted norm/slack beta_*; (D) any two distinct extracted polynomials on SAME C yield a relaxed binding/SIS break (sufficient bound on difference 2beta_*), error eps_B1 and eps_B2; (E) for the false public claim, every admissible masked witness slice Y consistent with C/public relation fails sigma invariance; (F) external r is sampled AFTER anchor and INDEPENDENT of F0.

Accepted session with valid F0,F1,F2 and no binding collision entails F0=F1=F2. Let D_{Y0}(T)=Y0(T)-sigma(Y0(sigma^-1(T))). Since Y0 is fixed before r and noninvariant, it is a nonzero degree<=s polynomial over R, and ring Schwartz–Zippel implies Pr[D_{Y0}(r)=0]<=delta=s/|E|.

Thus conditional **CLASSICAL INTERACTIVE** error:
    Pr[false accept] <= s/|E| + eps_K0+eps_K1+eps_K2 + eps_B1+eps_B2.
Binding errors are **LINEAR, NOT sqrt**. Pre-r full polynomial extraction removes need for P08's *two external challenge forks*. This is a new protocol under a stronger anchoring assumption, NOT a "tighter proof" of the original P05 unanchored protocol. Most important unproved instantiation obligation is prefix-coupled extraction on the actual CMNW transcript and enlarged SIS slack.

## FS / ROM / QROM (UNPROVED)

Noninteractive transcript MUST put finished anchor FS proof pi0 **inside the OUTER challenge hash input**, e.g.:
   H_ext("PVFHE-Galois", pp, full statement, mask selector, C, x0=0, u0=0, pi0).
Anchor proof's inner FS oracle is separately domain-separated and binds C, x0 and u0; the two POST-r evaluation FS proofs are separately domain-separated and bind the SAME C, the external r, both claimed values, branch index and prior prefix. A classical query-slot ROM argument could (CONDITIONALLY on adaptive ONLINE inner FS extraction of pi0 and two subsequent proofs) give:
   Adv_bad_ROM <= (q_H+1)*(s/|E| + eps_K0+eps_K1+eps_K2+eps_B1+eps_B2).
This is NOT a source-backed CMNW adaptive FS extraction result; CMNW Definition 6 covers interactive single-statement extraction, not automatically a joint Fiat–Shamir or QROM extractor. With plain H_ext(pp,C) excluding pi0, a malicious FS prover may query external r BEFORE finishing anchor, defeating the ordering. Quantum extraction/rewind, full source Ring-PCS adaptation, practical privacy and security are OPEN.

## One executed minimum exact gate [VERIFIED]

Program /mnt/data/pvfhe_p11_anchor_linear_loss_gate.py SHA256 **f7a609fe7bb93ae62c4b4130c9ae7c378eeb9f1725e8450233cf6435bb2a3402**.
JSON /mnt/data/pvfhe_p11_anchor_linear_loss_results.json SHA256 **ba29fd45da3c41b31185fb15d41f2880a4c4d8924118e649ebf145a6d9f2d894**.
Detailed Markdown report /mnt/data/PVFHE_P11_Prechallenge_Anchor_Linear_Binding_Repair.md SHA256 **af8053cc1e834b2aeec88d6b33cf86dfb966118235324e59a0d9be6d65f034ae**.

Use original PVFHE Q=2^53+5,N=2048 and faithful CRT subalgebra F_Q×F_Q with involution sigma swapping components. For augmented F(b,T)=(1-b)Z(T)+bY(T), choose Z(T)=0 and deliberately bad Y(T)=eT with e=(1,0) nonsigma-invariant. Fixed anchor x0=(b=0,T=0) has **public value F(x0)=0**. Over 4096 scalar r challenges, Galois check accepts exactly **1/4096**; correct point openings at anchor/post-r can be verified symbolically, but NO ACTUAL CMNW PCS WAS EXECUTED. The decisive validation remains the original full-opening *knowledge relation* and security derivation.

**Conditional ROM security budget** at q_H=2^64, s=32: |E|>=2^202, eps_K for EACH of 3 proofs <=2^-198, eps_B for EACH of 2 equal-opening comparisons <=2^-198. Exact Fraction computation shows the linear-loss proposed upper bound, multiplied by q_H+1, is <2^-128. With otherwise same eps_B and P10's sqrt(eps_B), the OLD proof upper bound is >2^-128. These are ILLUSTRATIVE required error targets, NOT measured CMNW lattice security nor verified exceptional-set availability. One extra PCS evaluation adds approximately O(m poly(lambda)) prover, O(log m poly(lambda)) verifier and O(log²m poly(lambda)) proof bits under cited asymptotics; original overall O(m² poly(lambda)) prover and O(log²m poly(lambda)) proof asymptotics plausibly unchanged, real costs UNMEASURED.

## Research decision and next

**STATUS:** PASS conditional classical interactive anchored full-opening linear-loss argument, FAIL suspicion that sqrt(binding) is inherent to ANY existing CMNW-interface extension; UNCLEAR full concrete CMNW/FS/QROM/security/privacy.
**RESULT:** *One extra prechallenge fixed-public-zero PC.Eval proof* can serve as a full opening-knowledge anchor and replace quadratic/sqrt binding loss with linear terms. Important: CMNW itself says hiding not required; don't invoke hiding as obstruction. This is a NEW extension with one extra proof, not a proof of the original unanchored proposal.
**NEXT_ACTION P12 only if PI continues:** Check whether the source ring's Galois FIXED subring can furnish an enormous efficiently samplable exceptional set (pairwise unit differences) so that evaluation at **one** fixed-by-sigma challenge r, with ONE PC.Eval proof, replaces P05's two related points, retaining the prechallenge anchor. Prove or falsify on source Q,N with exact algebra and cost. Only then reconsider concrete FS/QROM extraction and possible novelty. This is a separate primary hypothesis.
**STATE_UPDATE:** YES this independent P11 file ONLY. No changes to global vFHE/SHIP state or P01–P10 records.