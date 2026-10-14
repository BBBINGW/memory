# PVFHE-P19 — Adaptive Fiat–Shamir extraction source-transfer gate

**Date:** 2026-10-15 Asia/Tokyo. Independent PVFHE-P19 COMPLETED; P20 NOT STARTED.
**STATUS:** PASS generic adaptive-FS source theorem and exact CMNW challenge-error-parameter correspondence; PASS conditional first-external-query stopping technique; FAIL assuming P11’s strong additive-error, prefix-preserving nested ROM bound is a plug-and-play consequence. UNCLEAR/HUMAN_REVIEW actual CMNW Ring-PCS/SIS/ROM/QROM. P17 performance branch remains PARK.

## Read-before-write / provenance
Read START_RESEARCH_SESSION.md SHA 6235e9d376a8b143719a40178132f02a6a41d4f3; RESEARCH_PHILOSOPHY.md SHA 49da3f7fa3e75f502525482ce4a7ab6867; AGENT.md SHA b3e73b2c7f852c05aa674dd97b632e9f99ac5f22; separate STATE.md SHA 4ae5fc4af8a6f297f8620979dda5df71c83b03c3 (concurrent vFHE V36); previous P18 SHA faae7931e1cc330b198f940ae57252c1bffdafb0 and P11 SHA 165dfc36f7ba9914561ebe93ef5ff113316b083c. P19 absent before write; preserve all other files and vFHE/SHIP workstreams.

## Original primary sources, exact contracts
CMNW (Cini–Malavolta–Nguyen–Wee), ePrint **2024/281**, 52-page full Research MCP mirror SHA256 a9be7b5c1e9024d2d0c03865978d7f3ea1ed941dce8883f93f9576ae46a73b73, VERSION_UNVERIFIED. p12 Definition6 interactive rewinding, p13 Definition8 full polynomial-opening extraction (f,st), p17 Figure6 challenge matrices {0,1}^(r_fold*kappa × kappa), pp19–21 Lemma3 round-by-round coordinate-wise special soundness; p22 Theorem2 slack beta_*=(2r_fold*kappa)^ell_fold beta and error ell_fold*r_fold*kappa/2^kappa; p24 Theorem4 multilinear PCS over Z_q, not a proof of this nested Ring-PCS.

Attema–Fehr–Klooß, J. Cryptology 36 article36 (2023), https://doi.org/10.1007/s00145-023-09478-y. §2.4 on arguments via enlarged relations; §2.5 Definition10 adaptive FS extraction preserving joint original (x,pi,aux,v) distribution; §6.3 Theorem4 FS knowledge-error (Q+1)*kappa for suitable special sound multi-round proofs. IMPORTANT: its Definition10 guarantees extracted valid witness with probability at least (epsilon_accept-kappa_fs)/q(n), for polynomial q(n), and does NOT by itself guarantee Pr[accept and extraction invalid]<=kappa_fs.

Fenzi–Moghaddas–Nguyen, J. Cryptology 37 article31 (2024), https://doi.org/10.1007/s00145-024-09511-8. §2.7 Definition2.26 states a full-opening extraction relation on the original adaptive (C,u,z,pi); §2.9 Lemma2.32 INFORMAL and §8.2 give generic coordinate-wise special-sound multi-round adaptive FS knowledge error (Q+1)*mu*t*(k-1)/|S|, with expected-time and structural assumptions; detailed multi-round extension refers to Attema et al. Their concrete PCS uses DIFFERENT PowerBASIS assumptions, so do not transplant its concrete binding to CMNW’s SIS.

## ONE primary hypothesis and decisive source-contract falsifier
**[HYPOTHESIS P19]** Existing adaptive FS knowledge theorems, without any new source-level proof obligation, directly instantiate P11’s strongly pre-r, joint full-opening extractor and additive linear-binding bound for the specific CMNW Ring-PCS in a nested external RO.
**[FALSIFIER]** Verify published proof interface, quantified valid-witness extraction success, CMNW CWSS parameters and oracle ordering. If neither paper directly proves the complete strong, original-branch nested CMNW application, reject the automatic inference without rejecting possible new composition proof. No new CRT/algebra toys or performance sweeps.

## Exact positive parameter match
For CMNW take mu=ell_fold folding rounds, t=r_fold*kappa coordinate slots per round, k=2, S={0,1}^kappa of size 2^kappa. FMN interactive formula mu*t*(k-1)/|S| becomes ell_fold*r_fold*kappa/2^kappa, EXACTLY CMNW Theorem2 p22 error. Candidate adaptive FS error, IF all theorem hypotheses and original statement relation hold, is (Q_inner+1)*ell_fold*r_fold*kappa/2^kappa. This is a serious transfer lead, NOT yet a proven CMNW nested theorem, and says nothing about 2beta_* SIS security or ring adaptation.

## Conditional stopped-outer-query technique
Nested proposal: SAME private commitment C; completed fixed-public-zero inner FS PC.Eval anchor pi0; external r=H_ext(domain,statement,C,x0,pi0); ONE further same-C PCS eval at sigma-fixed r and check v=sigma(v), plus Ring-R1CS mask-link.

For the j-th DISTINCT fresh H_ext query, simulate the classical malicious prover, including all prior H_ext replies and separate H_inner domain, then STOP immediately BEFORE returning the new external answer. The candidate key already specifies C and pi0, so a stopped adversary A_j can output its anchor statement/proof, with earlier history as auxiliary data. Under an ADAPTIVE AUXILIARY-HISTORY-PRESERVING FULL-OPENING inner FS extractor for this stopped adversary, obtain a valid F0 opening of that same C on auxiliary classical forks, retaining the saved original execution. The new r_j has NOT been sampled and remains independently uniform. Auxiliary forks may change their own pi0; they are not required to make the ORIGINAL main pi0 change, correcting overstrong P18 reasoning.

Resume original run with r_j and extract F1 from post-r PCS proof. If f0,f1 are both valid at extracted slack and the same-C two-opening SIS binding at 2beta_* precludes F0≠F1, the false masked witness produces a nonzero sigma-difference polynomial fixed before r_j. Generalized Schwartz–Zippel contributes delta=s/|E|. By first-query classification and unqueried-final-output case, the CONDITIONAL strong-extractor candidate bound is:

  Adv_bad_classical_ROM <= (Q_ext+1)*(s/|E| + eps_K_anchor + eps_K_post + eps_B(2beta_*)).

This is **not** a published security theorem for the CMNW Ring-PCS. Need prove original-prefix auxiliary distribution coupling, expected-time extraction and actual quantified errors, full masked R1CS relation, ring adaptation and domain separation. QROM remains OPEN.

## Decisive negative source-quantifier check
AFK Definition10 only implies Pr[accept AND extracted witness valid] >= (epsilon_accept-kappa_fs)/q(n). For mathematical illustration epsilon_accept=1,kappa_fs=0,q(n)=10 gives a guaranteed success floor 0.1, NOT forced success=1. Therefore its theorem statement alone does not imply Pr[accept AND failed extraction] <= kappa_fs, the stronger bound used in P11. This is a logical nonimplication between theorem contracts, not an attack. FMN Definition2.26 has a stronger-looking original-proof full-opening condition; rigorously transporting that guarantee through CMNW’s round-by-round CWSS/slack and this stopped nested adversary is still needed.

## Research decision
**STATUS:** PASS generic theorem/CMNW error correspondence and source-backed conditional stopping strategy; FAIL assumption-free H19. UNCLEAR/HUMAN_REVIEW full CMNW adaptive noninteractive opening proof, SIS 2beta_*, Ring-PCS, QROM.
**RESULT:** P18 transcript coupling need not be fatal: generic adaptive FS tools can extract from a stopped pre-outer-challenge adversary using auxiliary forks while preserving an original main branch. But both the concrete reduction hypotheses and strong error quantifiers must be established rather than assumed.
**NEXT_ACTION P20 only on PI continuation:** One precise proof-or-obstruction for CMNW Lemma3 round-by-round coordinatewise special soundness satisfying FMN/AFK adaptive full-opening extractor with auxiliary main-branch preservation, exact extraction error and SIS at 2beta_*. If unavailable, provide final HUMAN_REVIEW/PARK technical obligations instead of further toy tests.
**STATE_UPDATE:** YES this independent P19 finding only; NO shared STATE.md, concurrent SHIP/vFHE or P01–P18 edits.
**Full local report:** /mnt/data/PVFHE_P19_Adaptive_FS_Source_Theorem_Transfer_Gate.md (verified SHA256 8c37a702ea5b41b10cd97532a107f1e4f48595f7eb64d6fd86c44e571e5395b4).
