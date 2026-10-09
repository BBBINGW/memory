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
