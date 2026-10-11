# Iteration 70 — Strongest natural sound relation supported by revised fieldwise vFHE lookup argument

Date: 2026-10-11
Paper: Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, IACR ePrint 2025/286.
STATUS: **PASS** — algebraically identify the exact rectangular-CRT table relation matching the existing decomposition+fieldwise lookup; reconstruct original revised Theorem4.8 field-projection proof for that RELAXED language and quantify its dramatic strict enlargement in paper-legal N8,d4 example. No modified SNARK built and no author communication.
Primary text: complete 52pp mirror PDF SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19, Git blob a549654c5dffa3484e95e8244056f4a27c48c3e6, VERSION_UNVERIFIED; source pinned by I69 to 2026-04-28 mirror commit postdating 2026-02-16 official revision. Version NOT byte-authenticated to current official site.
Source anchors: §4.3 p20 eq21 original T_B={Σ_j a_jX^j: 0≤a_j<B}; Lemma4.3 p20-21 eq22-23 decomposes into h digits t_beta; Theorem4.4 p21 composes Pi_decomp and Pi_beta_range with SAME h; revised Lemma4.6 p22 is FIELD-only given 2^ell*<p; Figure1/Theorem4.8 p23, Remark4.9 p24; Appendix E.2 p48 uses false global-diagonal to some-illegal-field implication.

## Read before write
Read AGENT.md, RESEARCH_PHILOSOPHY.md, unrelated RIG-HE STATE.md, I69 findings/vfhe-theorem48-post-revision-mirror-provenance-diff.md, I60 full-Pi_range finding. State remains unchanged. One primary hypothesis tested by a mathematical equivalence plus exact cardinality computation; no new attack or repair candidates.

## Primary hypothesis
[HYPOTHESIS — PASS within stated paper conditions] Replace scalar lookup table t_beta by its CRT-rectangular closure T_digit,rect=Phi^-1(prod_k Phi_k(t_beta)). Then (i) the fieldwise reduction in revised Theorem4.8 is valid against the *relaxed* digit-table membership relation, while (ii) Pi_decomp + this relaxed digit relation corresponds **exactly** to T_B,rect=Phi^-1(prod_k Phi_k(T_B)), which can be enormously larger than original coefficient-range table T_B.
[FALSIFIER] Failure of CRT equivalence for Pi_decomp, proof's fieldwise step failing despite illegal rectangular input, or relaxed T_B equal original table in tested legal ring. Cheap exact proof and image-count check, no further random experiments.

## Formal relation equivalence
Rq~prod_(k=1..mu) F_k via Phi. Let A_beta={0,..,beta-1}*1_R embedded diagonally; let A_beta,rect=Phi^-1(prod_k Phi_k(A_beta)).
Paper's coefficient-digit recomposition map L(h)=sum_(j=0..N-1) sum_(t=0..c-1) beta^t X^j h_(j,t), with beta=B^(1/c), B=2^b, c divides b (c=2^gamma).
Original T_B = L(A_beta^{Nc}); fieldwise projection satisfies Phi_k(T_B)=L_k(Phi_k(A_beta)^{Nc}), because each field has the expected base-beta expansion and L commutes with CRT. Then:
  L((A_beta,rect)^{Nc})
 =Phi^-1(prod_k L_k(Phi_k(A_beta)^{Nc}))
 =Phi^-1(prod_k Phi_k(T_B))
 =: T_B,rect.
The componentwise witnesses h_k and their multilinear extensions CRT-glue to a SINGLE Rq-valued h, so sharing h between Pi_decomp and Pi_beta_range imposes no hidden cross-field consistency. For each public index i, relaxed relation is `v_i∈T_B,rect`, not `v_i∈T_B`.
This set equality holds without requiring injectivity of individual projection Phi_k(T_B); it is a set image identity. It does not itself ensure the full compiled SNARK has correct opening soundness.

## Reconstructed soundness for RELAXED relation, not original theorem
If h outside A_beta,rect at any Boolean point, by definition there exists k with Phi_k(h) outside Phi_k(A_beta). Revised field-only Lemma4.6 then forces a genuine projected memory multiset mismatch for any first-round projected read_ts/final_cts. Thus the projected grand-product polynomial P_k(sigma,tau) is nonzero over F_k, and P in Rq[sigma,tau] is nonzero. The remaining grand-product/oracle-check argument and generalized Schwartz–Zippel over exceptional set S proceed as in Appendix E.2, conditional on all other proof hypotheses, yielding paper's form of knowledge error O((2^ell*+2^(b/c))/|S|) for this RECTANGULAR target. Pi_decomp Theorem4.5 + Theorem4.4 composition passes this relaxed h relation to T_B,rect. We have not independently rebuilt a complete knowledge extractor or checked every hidden definition and so claim soundness supported by the paper's proof architecture, NOT an independent fully formal security theorem.
The original disputed implication `h notin diagonal A_beta => exists bad CRT projection` remains false. Rectangular version `h notin A_beta,rect => exists bad projection` holds tautologically. Therefore the precise claimed-versus-supported relation distinction is identified.

## Exact cardinality in paper-legal N8 d4 ring
Take q=29*37=1073, N=8,d=4, B=beta=2, ell=1, nu=3, gamma=0, ell*=4 and 2^ell*=16<29 and beta2<29.
Factor X8+1 mod29 = (X4+12)(X4−12); mod37=(X4+6)(X4−6). All four quartics are irreducible (proved in I61). CRT gives four separate F_(p^4) factors.
For each factor X4−t with t∈{12,−12} mod29 or t∈{6,−6} mod37, a Boolean polynomial u=Σ_(j=0..7)a_jX^j maps to remainder
  rem_t(u)=Σ_(j=0..3)(a_j+t*a_(j+4))X^j.
The four possible integer residue coefficients `0,1,t,1+t` are all DISTINCT modulo each respective p. Therefore every one of the 2^8 Boolean polynomials has a different image in EACH field factor. So |Phi_k(T_B)|=256 for k=1,2,3,4. Their direct product image set has exact cardinality
  |T_B,rect|=256^4=2^32=4,294,967,296.
Original |T_B|=2^8=256 because coefficient representatives are unique modulo q when 0≤a_j<2. Relaxation factor=2^24=16,777,216, with original fraction in relaxed =2^-24. This is a cardinality comparison, NOT an attack success probability. The invalid scalar e=667 (mod29=0, mod37=1) lies in T_B,rect \ T_B and is consistent with original I61 transcript.
[REPRODUCIBLE] Exact Python enumeration for each of four 256-element projected tables, rather than enumerating 2^32 product:
  /mnt/data/iteration70_vfhe_rectangular_relation_audit.py SHA256 38f0add7e8f41d98632bd19bffa0118c1572cba4943c3284ec0067143a0ef4a8
  /mnt/data/iteration70_vfhe_rectangular_relation_results.txt SHA256 ccceb276f7521a3315b4c00a36c50c18adb942cb28c726d1c2b1c5c5e1d7ff6c
Script executed PASS with four field images size 256, relaxed 2^32 and ratio 2^24.
[BOUNDARY] In general |Phi_k(T_B)| may be smaller than B^N if local polynomial factor reductions cause collisions, so DO NOT extrapolate 2^(N*mu) universally. The identity T_B,rect=CRT product of images always holds; cardinality product follows the images' actual sizes. If R has just one field factor, rectangular=diagonal and no gap.

## Consequence and next action
This shows original proof is not worthless: it protects a clear rectangular-CRT lookup language, rather than desired true coefficient-bound diagonal language. Changing the stated target language alone would be a theorem erratum but could invalidate intended vFHE semantics because T_B,rect permits coefficients outside [0,B-1]. Fixing original intended language needs genuinely cross-CRT coherence in protocol or stronger assumption eliminating CRT product. Prior I63 no-go says purely ring-polynomial equations cannot enforce it, I64–68 low-cost encoder variants failed/no suitable bridge. Thus next decisive work is NOT another encoding toy, but impact audit: for ONE actual §3–§4 proof-friendly CKKS gadget/wire value using T_B range check, test whether accepting T_B,rect rather than T_B can invalidate the stated arithmetic-circuit/CKKS-computation relation or whether a separate bound still applies. This connects abstract soundness mismatch to actual application semantics and cost. Do not claim deployed exploit without formal complete transcript.
Official 2026-02-16 PDF byte authentication remains UNCLEAR; 52pp mirror pinned to April28 update and version corrected with Remark4.9. Author review requires PI explicit authorization.
End:
STATUS: PASS for relaxed-relation characterization and exact gap count, UNCLEAR for full-system security effect.
RESULT: revised fieldwise Theorem4.8 proof supports rectangular A_beta,rect, Pi_range then checks T_B,rect; in N8,d4 legal ring, 2^32 relaxed values vs 2^8 true values.
NEXT_ACTION: Select one concrete proof-friendly CKKS operation / wiring constraint in §3–4 that invokes Pi_range and try to create a false arithmetic statement admitted when its T_B check is weakened to T_B,rect, excluding any unverified extra constraints. Use one falsifiable computation-level test; else HUMAN_REVIEW.
STATE_UPDATE: NO — parked RIG-HE STATE.md untouched.
