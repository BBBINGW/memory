# CGS-40: Cardinality of negacyclic Gram covariance catalog

Date 2026-10-15. PI-selected CGS investigation, after CGS-39.

HYPOTHESIS: The public catalog of all conditioned Gaussian distributions used in the prior scalar norm-selector MPC can be extended to MLWE with polynomially many separate covariance-specific entries.

RESULT: FAIL for complete explicit exact table enumeration. Let n=4m and R=Z[X]/(X^n+1). For each b in {0,1}^m set s_b=1+X^m sum_(j=0)^(m-1) b_j X^j. Define s*=s(X^-1). The multiplication Gram is mat(s_b)mat(s_b)^T=mat(s_b s_b*). The coefficients of X^(m+j) in s_b s_b* equal exactly b_j; the other self-correlation and negative terms fall outside positions m..2m-1. Therefore all 2^m choices yield DISTINCT integer Gram matrices. Fixing Hamming weight of b to m/2 fixes ||s_b||^2=1+m/2 but leaves binomial(m,m/2) distinct matrices. At n1024, this is about 2^251.673 distinct covariances even at one norm.

Original anchor: Okada-Takagi ePrint2025/409, full 40-page MCP mirror, Algorithm7 physical p29 and Lemma7.1 pp30-31. Target integer Gaussian shape is Bpub^2 I-Sigma_s. For positive definite target, distinct matrices produce distinct exact full-support integer Gaussian distributions: ratios p(z)/p(0) at e_i and e_i+e_j identify the inverse quadratic form. Sufficient source positivity Bpub^2>k n^2 B_mlwe^2+1 can hold e.g. k2,Bmlwe1,Bpub=3n+1, but this is not a fully security-validated source parameter selection.

Exact executable check: /mnt/data/cgs40_mlwe_covariance_catalog_gate.py SHA256 008e85ae1a57dd4073bdfb9ab018b47ffae5003d681ce43d0e1267964e88bf40. JSON /mnt/data/cgs40_mlwe_covariance_catalog_results.json SHA256 25b102eaed75bafe5d59aa62f32ca1fa96f7c8cb176e49e8c3e36a90d1831089. Exhaustive n8:4 unique; n16:16; n32:256; fixed-norm counts 2,6,70. Complete n by n integer matrix correctness cross-checked for n8,n16 representatives.

LIMITS: Sparse constructed family has negligible probability under iid Bernoulli full secret; no average-key complexity or lower bound on statistically approximate catalogs is proved. Source may use another coefficient distribution or require singular-value bounds. No lower bound on compact general covariance-input sampling circuits or interactive secure MPC. Not a security attack or new ThFHE.

STATUS: FAIL explicit catalog extension, PASS injective Gram count and exact exhaustive tests, HUMAN_REVIEW original O(LDec) problem OPEN. NEXT CGS-41: test a concrete online private multivariate discrete Gaussian rejection sampler with public spherical proposal and secret quadratic-form acceptance, assessing success probability and MPC round/storage tradeoff. STATE_UPDATE YES.
