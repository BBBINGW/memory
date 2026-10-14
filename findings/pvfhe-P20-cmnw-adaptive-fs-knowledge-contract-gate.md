# PVFHE-P20 — CMNW Γ-star challenge and 2026 adaptive FS extractor

2026-10-15 Asia/Tokyo. P20 COMPLETE; P21 NOT STARTED. STATUS: FAIL naive t_Gamma <= xi+1 transfer, PASS source theorem and exact Γ countercheck; UNCLEAR/HUMAN_REVIEW CMNW nested ROM/SIS/Ring-PCS/QROM, full PCS integration PARK pending PI.

## Read before write
Read START_RESEARCH_SESSION.md SHA 6235e9d376a8b143719a40178132f02a6a41d4f3; RESEARCH_PHILOSOPHY.md SHA 49da3f7fa3e75f502525482ce4a7ab6867; AGENT.md SHA b3e73b2c7f852c05aa674dd97b632e9f99ac5f22; STATE.md SHA c25d596784e3d07c9807854dc634298b9c960cf7 (separate vFHE V37), P19 SHA 4fe559ff472081f3231518df50a485684c23a7ba and P18 SHA faae7931e1cc330b198f940ae57252c1bffdafb0. Target absent; no global state or parallel SHIP/vFHE edits.

## Source facts
CMNW 2024/281, full Research MCP original PDF 52 physical pages SHA256 a9be7b5c1e9024d2d0c03865978d7f3ea1ed941dce8883f93f9576ae46a73b73 VERSION_UNVERIFIED. Physical p13 defines Γ(S,xi) as center plus one one-coordinate neighbor each, p14 Definition9 and Theorem2 source condition (xi+1)^ell=poly(lambda) for its OWN recursive classical CWSS extraction, pp19–21 Lemma3, p22 Theorem2 beta_*=(2*r_fold*kappa)^ell beta with interactive error ell*r_fold*kappa/2^kappa, p13 Definition8 full polynomial opening f,st and p15 Theorem4 binding norm 2beta for two beta openings. Concrete Theorem4 is over Z_q; actual ring adaptation and full nested scheme not yet proved.

NEW 2026 paper missed by P19: Attema–Fehr–Klooß–Resch, The Fiat–Shamir Transformation of (Γ1,…,Γmu)-Special-Sound Interactive Proofs, J Cryptology 39, article19, 2026-03-06, DOI https://doi.org/10.1007/s00145-025-09569-y, authoritative full HTML https://link.springer.com/article/10.1007/s00145-025-09569-y, Definitions5–8, Theorem5 Section6.7 and Remark13. Historical preprint ePrint2023/1945.

Source Theorem5: global Γ-multiround special sound, nonempty monotone Γ_i, T_Gamma=product_i(t_Gamma_i+1) polynomial in statement size, efficient uniform sampling from useful U_Gamma_i(S) for |S|<=t_Gamma_i. Then for Q_inner RO queries, extractor expected prover calls <=(Q_inner+1)*T_Gamma/(1-kappa_Gamma) and success >=(epsilon-(Q_inner+1)*kappa_Gamma)/(1-kappa_Gamma); Remark13 addresses adaptive strong FS variant hashing the statement. This NEW theorem has no AFK2023 Definition10 extra polynomial q(lambda) denominator. Conditional on original-main-branch coupled extraction, it gives Pr[accept AND extraction failure] <=(Q_inner+1)*kappa_Gamma/(1-kappa_Gamma). But source has not instantiated actual CMNW nested Ring-PCS.

## ONE primary falsifiable hypothesis / ONE decisive test
HYPOTHESIS P20: CMNW Γ-star has t_Gamma <= xi+1, so source (xi+1)^ell=poly(lambda) AUTOMATICALLY meets 2026 Theorem5 T_Gamma=poly(lambda) efficiency without any new lemma.
FALSIFIER: EXACT finite enumeration of Γ, useful U_Gamma(S), and t_Gamma for binary alphabet coordinate-star challenge sets xi=2,3,4; exhibit t_Gamma>xi+1.

Minimal star for binary challenge c is {c} UNION {c XOR 2^j : j in [xi]}; Γ upward closed. For Γ-free set S, c useful iff there exists minimal star G containing c such that (S UNION G) minus {c} remains Γ-free (equivalent to 2026 Definition7 because a minimal star can be selected from any witnessing Γ set). Dynamic programming t(S)=1+max_{c useful} t(S union{c}), zero after S enters Γ. Enumerated all 2^(2^xi) subsets, checked C minus U_Gamma(S) Γ-free for EVERY Γ-free subset.

ACTUAL exact executed results:
xi2: 4 challenge vectors, 16 subsets, t_Gamma=3, xi+1=3, max Γ-free set=2.
xi3: 8 challenge vectors, 256 subsets, t_Gamma=5 > xi+1=4, max Γ-free set=6.
xi4: 16 challenge vectors, 65,536 subsets, t_Gamma=12 > xi+1=5, max Γ-free set=12.
Verified explicit ξ=4 full useful-extension chain: [0,1,2,3,4,12,13,9,14,10,7,5].
Thus the source simplification t_Gamma<=xi+1 FAILS already at xi=3. This small binary exact example does NOT prove asymptotic t_Gamma superpolynomial for CMNW real alphabet S={0,1}^kappa, xi=r_fold*kappa, or impossibility of efficient Γ sampling / a CWSS specialized proof. Do NOT confuse CMNW existing (xi+1)^ell extractor complexity with 2026 different T_Gamma.

Verified local research files:
- /mnt/data/pvfhe_p20_gamma_contract_check.py SHA256 b0b8e406ba08dd2372e047208486782f37bee220744e5f90795ec00ad020b055
- /mnt/data/pvfhe_p20_gamma_contract_results.json SHA256 f373e6206ecd82480ea4da3e504fd0c44bce0d6aaff60aa15ba186b076d986ef
- /mnt/data/PVFHE_P20_Gamma_FS_Extractor_Transfer_Gate.md SHA256 d6a388bd5f31d2a91e1829b5d06b1b6a55c8b31eb980eb57fe53f9c775ff355a

## Remaining separate obligations
(1) Bound asymptotic t_Gamma and give efficient uniform U_Gamma sampler on actual CMNW challenge alphabet. (2) Align round-by-round CMNW Lemma3 with accepted-leaf global Γ-special-sound relation at extracted norm beta_*. (3) Preserve original stopped main branch (statement,C,pi_anchor) and simulate inner/outer random oracles when stopped before answering H_outer; bound Q_inner and Q_outer. (4) Source verified same-C extracted-opening SIS binding at 2beta_*; concrete Ring-R_Q adaptation, R1CS mask linkage, strict polynomial runtime. (5) Separate QROM theorem; no unconditional original-paper flaw or repaired-SNARG security theorem. P17 speed claims remain PARK.

## End of Iteration
STATUS FAIL naive Γ-extractor efficiency shortcut; PASS stronger 2026 theorem source contract and finite exact Γ violation; UNCLEAR/HUMAN_REVIEW full integrated CMNW/ROM/QROM.
RESULT P19's extra polynomial extractor success denominator can potentially be removed by 2026 Theorem5, but CMNW's known (xi+1)^ell efficiency bound alone does not prove Theorem5's T_Gamma premise: exact Γ t=12 vs xi+1=5 at xi=4.
NEXT_ACTION / HUMAN_REVIEW: PI choose (A) ONE rigorous asymptotic t_Gamma and efficient U_Gamma sampler for actual S={0,1}^kappa, xi=r_fold*kappa, then nested RO/SIS, or (B) PARK PCS-security integration and pivot to a separate FHE audit. No more similar finite toy enumerations.
STATE_UPDATE YES new independent P20 file ONLY, no shared STATE.md or concurrent vFHE/SHIP changes.
