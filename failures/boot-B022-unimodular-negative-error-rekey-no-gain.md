# BOOT-B022 failure archive — negative-correlated block-key errors via integer prefix rekey do not lower average noise

TRACK_ID: BOOT
ITERATION: B022
DATE: 2026-10-19
STATUS: FAIL_INDEPENDENT_KEY_UNIMODULAR_RECODING_NOISE_GAIN / GENERAL_JOINT_NOISE_SECURITY_UNCLEAR

Sources: Lee et al. ePrint 2023/958 Algorithm2 p11: one-hot block aggregations Σ_i(X^{a_i}−1)RGSW(s_i) in ONE external product per block. Hong–Lee ePrint 2025/1892 pp4,11–12: heterogeneous RGSW gadget bases smooth noise/DFR vs key/time. Broader background Bergerat et al. CHES2025 "Sharing the Mask" ePrint 2025/2112 only official abstract inspected; verified original full PDF unavailable to research MCP (failed identity), so do not claim full-content priority search.

Novel proposal: for one-hot block s, public unimodular prefix transform U with diag1 and subdiag−1, t=U^−1s are binary prefix sums. Encrypt t_j as INDEPENDENT RGSW under native ring secret, publish BRK=U Enc(t), which encrypts exact original s and creates negative adjacent evaluation-key error correlations. Correct native one-product-per-block interface, ℓ keys and public key-mixing preserved. Hypothesis that negative correlation reduces average block-noise FAILS exactly.

On a single RGSW row with coefficientwise error covariance C, public independent uniform rotation exponents ai mod 2N and negacyclic rotations P^ai, aggregate η=Σ_i(P^ai−I)e_i. Expected coefficient energy
  E||η||²/N=Tr C+1^T C 1.
Independent equal-σ keys: 2ℓσ². Integer rekey U: C=σ²UU^T, expected energy/Nσ²=Σ_columns v of U (||v||²+(sum v)²)≥2ℓ because every column is nonzero integer and either one nonzero with nonzero sum or >=two entries when sum=0. ℓ4 prefix-U reaches exactly8Nσ², identical to baseline.
One can beat this algebraic noise proxy with GENERALLY correlated errors at equal marginal variance: ℓ4 ρ=−1/6 gives6Nσ² vs8Nσ², but min covariance eigenvalue falls from σ² to σ²/2. Under conservative C≽σ² I security-screen, no covariance gains possible. Rescale that ρ covariance to min eig=σ² and energy is12Nσ², 50% worse than baseline. Treat eigenvalue-floor as a PROXY/conditional assumption, NOT a proof of RLWE security necessity. Singular ρ=−1/3 makes publicly summed rows error-free and is dangerous for key privacy/ring-key recovery.

Independent toy: N=4, ℓ=4, ALL 8^4=4096 uniform public exponent tuples enumerated using exact signed shift matrices. Mean normalized Gram has diag2, offdiag1; energy scores 8 independent, 8 prefix-rekey, 6 negative correlated,12 security-floor-restored. Matches algebra, no native ciphertext code or DFR/MLWE security estimator.
LIMITATION: Model only one RGSW error row and honest uniform independent ai; adversarial inputs, actual gadget digits, key-row dependencies and worst-case DFR unresolved. Does NOT rule out all exotic secure covariance structures, packed/matrix-key approaches or other original BOOT optimization. Not a new implementable acceleration.
DETAILED_RECORD: findings/boot-B022-block-binary-correlated-key-error-no-go.md
REPAIR_SEARCH: public integer prefix encoding gets correctness but exactly no noise benefit, while arbitrary negative correlations shift hardness to a lower-noise public direction; avoid celebrating 25% proxy gain. Pivot cost lever, NOT research line, next B023 ask if sharing RGSW key *masks* (not errors) inside block preserves security of onehot secret and remains one external product. Check plaintext differences and Matrix-LWE rekey repair, source TCHES2025. Next round one falsifiable claim/test only. BOOT-only.
