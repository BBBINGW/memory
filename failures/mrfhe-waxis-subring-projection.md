# MRFHE W-axis special-key proposal: subring projection obstruction

Date: 2026-10-09
Decision: NEGATIVE / ARCHIVED for the proposed W-independent key, NOT for the original MRFHE scheme.
Primary reference: Cheon et al., MRFHE, IACR ePrint 2026/853; Sections 2.4-2.5, 3.2, 5.2, Appendix A (m-RLWE distribution), Table 5. Source: previously attached PDF 2026-853.pdf; Research MCP retrieval of this paper was blocked, so the evidence was NOT obtained from the MCP ePrint cache.

Hypothesis: Constrain the MRFHE key to s(U) (no W-dependence) to permit no-switch W-direction DFT. Does that create low-dimensional public RLWE samples?

[DERIVED] Put n1=2^(w2-2), n2=2*3^w3, A=Z[U]/(U^(2n1)+1), R=A[W]/Phi_(3^(w3+1))(W). This makes R a free A-module of rank n2. If a,b,e are expanded as sum_j a_j W^j, b_j W^j, e_j W^j, and s=s(U) is in A, the high-dimensional RLWE equation b+a*s=e implies EACH b_j + a_j*s = e_j mod q. Coefficient extraction is an A-linear module projection, NOT generally a ring homomorphism, and that suffices. Uniform a means uniform independent a_j; in Appendix A's coefficient-independent discrete Gaussian tensor noise model, e_j remain Gaussian with the same per-coordinate variance. One full-ring sample thus exposes n2 base-ring samples sharing a dimension-(2n1) key instead of the dimension-(2n1*n2) key of the full ring.

[FACT] Paper Table 5 gives:
FHE(8,4)-D N=20736, h=1024;
FHE(10,3)-D N=27648, h=1024;
FHE(9,4)-S N=41472, h=192;
FHE(9,4)-D N=41472, h=20736;
FHE(8,5) N=62208, h=31104.
[DERIVED] New key dimensions 2n1 are respectively 128,512,256,256,128, with reductions x162,x54,x162,x162,x486. Hamming weights are defined in the scheme's original power basis, so do NOT claim the bound h<=2n1 in that basis. Under U=X^(3^(w3+1)) and Phi_(3N)(X)=X^N-X^(N/2)+1, a W-constant key in the subring has a univariate power-basis support contained in a set of respective sizes 170,682,341,341,170. Hence all specified h values except 192 are impossible for the proposed restricted-key subring choice. These figures are support upper bounds, not security estimates.

[FACT / EXPERIMENT] Reproducible toy /mnt/data/fhe_audits/mrfhe_w_constant_secret_projection_audit.py: w2=3,w3=1,q=97, R=F97[U,W]/(U^4+1,W^6+W^3+1). 600/600 exact coefficient RLWE projections pass. For 100 independent toy samples, one full-ring pair yields six projected pairs; exhaustive 3^4 bounded-error candidate enumeration recovers the unique four-coordinate ternary key 100/100 times. This toy is NOT a cryptanalytic benchmark for deployed MRFHE parameters and q=97 is not asserted to be an NTT deployment modulus.

[SCOPE] The original paper DOES NOT use the suggested restricted-key modification. This audit does NOT break original MRFHE, does NOT prove an explicit 128-bit attack, and does NOT transfer its original security assessment to the modified construction.
[PRIOR ART] Subfield/subring cryptanalysis is established: Albrecht et al. and Chen-Lauter-Stange, 'Attacks on the Search-RLWE problem with small errors' (2017), examine related but not identical subfield attacks. NO NOVELTY claimed.

Result: The proposed zero-key-switch W-axis transform by suppressing W-dependence of the key sacrifices effective key dimension and invalidates reusing the original key-weight/security rationale. ARCHIVE this special-key shortcut. No STATE.md modification: the RIG-HE task remains parked in that file.
NEXT: Select a different FHE hypothesis not depending on an unanalysed reduced-dimension key distribution.

## Independent verification addendum (2026-10-10, Iteration 30)

This addendum validates the existing archived result; it does not reopen the rejected special-secret shortcut.

[SOURCE VERIFIED / FACT] The original 18-physical-page `2026-853.pdf` was read from the user's ChatGPT Library (844,699 bytes), after the GitHub Notes `get_eprint_paper(2026/853)` again returned RETRIEVAL_BLOCKED (ePrint PDF HTTP 403; configured mirror absent). This is **Library original PDF parsed text**, not MCP ePrint cache or visually verified pages. Original paper: §2.1 physical p.4 (N=2^{w2}3^{w3}, n1=2^{w2-2}, n2=2·3^{w3}, rank R=N), §§2.4–3.2 physical pp.4–6 (tensor presentation and b+a s=m+e), Appendix A Proposition A.1 / Definition A.2 / Lemma A.3 physical pp.13–14 (multivariate tensor ring, uniform a and coefficient-i.i.d. Gaussian error in the defined m-RLWE model, RLWE-to-m-RLWE reduction), Table 5 physical p.18 (original Hamming weights). The actual encryption error sampling basis is not fully specified by the abstract `Enc` interface in §3.2, so the same-width / independent projected-error assertion should be interpreted under Definition A.2's model, **not automatically any univariate implementation**.

[DERIVED] Write A=Z[U]/(U^{2 n1}+1), R=A[W]/Phi_{3^{w3+1}}(W), with A-rank(R)=n2. When s in A, coefficient extraction `pi_j(sum_k x_k W^k)=x_j` is A-linear and yields exactly `pi_j(b)+pi_j(a)s=pi_j(e)` for a zero-message `b+a s=e`. Coefficient extraction need NOT be a ring homomorphism; indeed in the toy R with W^6+W^3+1, `pi_0(W·W^5)=-1` but `pi_0(W)pi_0(W^5)=0`. Uniform a in R_q gives independent uniform a_j in A_q. In the tensor power-basis independent-error model of Appendix A, each projected e_j has the same marginal coefficient Gaussian, and the blocks are independent before conditioning on the common secret. This establishes n2 ordinary low-rank A-RLWE samples (rank 2n1) from one ideal restricted-secret m-RLWE sample (rank 2n1 n2), NOT an estimated practical attack or a claim against unrestricted MRFHE.

[DERIVED: relative trace] Let t=3^{w3}, n2=2t, W primitive 3^{w3+1}-th root. For 0<=j<2t, Tr_{R/A}(1)=2t, Tr_{R/A}(W^t)=-t, and all other basis powers have relative trace zero. Thus Tr_{R/A}(x)=t(2x_0-x_t). If gcd(t,q)=1, the normalized map t^{-1}Tr gives the small-integral combination 2x_0-x_t, and projected noise has coefficient variance 5 sigma^2 under coefficient-i.i.d. Gaussian errors, as compared to sigma^2 for coefficient extraction pi_0. Traces themselves are a second route, but not needed for the decisive test.

[FACT: independent exact toy] New deterministic check (seed 20261010, q=97, A_q=F97[U]/(U^4+1), R_q=A_q[W]/(W^6+W^3+1), secret ternary rank 4, coefficient errors in {-1,0,1}) verified 1200/1200 exact projected equations over 200 independently sampled high-ring zero-message pairs. Exhaustive 3^4 bounded-error enumeration uniquely recovered the toy secret 200/200 times. Companion-matrix relative traces of W^0..W^5 were [6,0,0,-3,0,0]. Reproducible conversation script: `/mnt/data/iteration30_projection_check.py`. This toy does not estimate deployment security.

[DERIVED: parameter incompatibility check] Take U=X^{3^{w3+1}} in Z[X]/(X^N-X^{N/2}+1). A W-independent secret has univariate-power-basis support inside at most 170, 682, 341, 341, 170 positions for Table 5's FHE(8,4)-D, FHE(10,3)-D, FHE(9,4)-S, FHE(9,4)-D, FHE(8,5), respectively. Thus dense h=1024/1024/20736/31104 cannot be retained by those restricted-key families; h=192 is support-feasible for FHE(9,4)-S but still has effective base-ring dimension 256. These are support bounds, not cryptanalytic cost estimates.

[PRIOR ART / SCOPE] Chen–Lauter–Stange, *Attacks on the Search-RLWE Problem with Small Errors*, SIAM J. Appl. Algebra Geom. 2017 (arXiv:1710.03739), studies subfield vulnerabilities but not necessarily this identical coefficient-projection construction. No novelty claimed. No explicit 128-bit distinguishing/recovery attack against practical MRFHE parameters has been proved. Restricted-key modification remains archived and should NOT inherit unrestricted MRFHE's Table 5 security estimate.

[END] STATUS=PASS for the precise low-dimensional sample extraction, NEGATIVE for the unanalysed original-security-preserving special-key shortcut. No update to STATE.md; RIG-HE parked state remains untouched.
