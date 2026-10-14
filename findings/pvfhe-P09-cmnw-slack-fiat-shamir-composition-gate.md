# PVFHE-P09 — ROM commitment grinding falsifies unchanged P08 Fiat–Shamir transfer; CMNW slack gate

**2026-10-15 (Asia/Tokyo); independent PVFHE-P09 COMPLETED, P10 NOT STARTED.**
**STATUS:** FAIL using P08's interactive delta=s/|E| error *unchanged* after Fiat–Shamir; PASS exact-source-ring ideal-PCS ROM commitment-grinding countermodel; UNCLEAR genuine CMNW joint PCS+SIS classical ROM security, real exceptional-set parameterization, and QROM. No CMNW/original PVFHE attack claimed.

## Read before write, source edition and independence

Read START_RESEARCH_SESSION.md SHA 6235e9d376a8b143719a40178132f02a6a41d4f3, RESEARCH_PHILOSOPHY.md SHA 49da3f7fa3e75f5025258cf525482ce4a7ab6867, AGENT.md SHA b3e73b2c7f852c05aa674dd97b632e9f99ac5f22, global STATE.md SHA a7b184491083f027696160b6204f4ed75483cebe (independent vFHE V28), P08 findings/pvfhe-P08-classical-precommit-joint-extraction-gate.md SHA 96b05e032688f16a5ae24e198a815acc8ed3214f and P07 SHA 4eb5b1a1af088f90166e90c93500ad3b3ed9968e. P09 was absent before writing. Do NOT alter concurrently maintained vFHE/SHIP state, earlier P-series, or originals.

**Original primary PDF sources (Research MCP):**
- Cini, Malavolta, Nguyen, Wee (CMNW), *Polynomial Commitments from Lattices: Post-Quantum Security, Fast Verification and Transparent Setup*, CRYPTO2024, ePrint **2024/281**, 52 physical pp, GitHub mirror PDF SHA256 a9be7b5c1e9024d2d0c03865978d7f3ea1ed941dce8883f93f9576ae46a73b73 VERSION_UNVERIFIED. Physical p11 Def3 relaxed binding with slack, p12 Def6 single-statement knowledge soundness and rewinding, p13 Def8 evaluation relation, p15 Thm4 SIS binding, p22 Thm2 beta_*=(2r_fold*kappa)^ell beta, p24 Thm4 multi-linear PCS, physical p39 Appendix A.4: for the authors' own **internal** FS concrete example, up to 2^64 random-oracle queries and λ=192 to accommodate linear FS loss for 128-bit security.
- Huang, Li, Mao, Zhang, *Fully Homomorphic Encryption with Efficient Public Verification*, ePrint **2024/1764**, 29pp, mirror PDF SHA256 7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089 VERSION_UNVERIFIED. Physical pp8–9 PCS Definition2.5; p21 Lemma5.6/Theorem5.7 and source public-coin→FS in ROM discussion; AppendixB Q=2^53+5,N2048. Latest binary edition / rendered formulas not independently verified: web PDF screenshot produced cache miss. This P09 audits OUR proposed P05 extension, not their source published actual SNARG.

## ONE smallest falsifiable hypothesis / ONE decisive test

**[HYPOTHESIS P09]** P08's classical-interactive false-accept bound p<=delta+sqrt(eps_bind)+eps_extract, delta=s/|E|, remains valid UNCHANGED in the **non-interactive Fiat–Shamir ROM** extension simply by deriving r=H(domain,statement,C) from the same pre-r commitment C, even with perfectly binding PCS and honest evaluations.

**[FALSIFIER]** Construct many different precommitted *false* polynomials in original source ring; for each distinct commitment C_j independently query ideal RO challenge H(domain,x,C_j). Choose any j whose random r_j makes P05 Galois-twisted check hold and provide TWO *honest* point evaluation proofs. If q_H candidate attempts give p>single-shot delta despite eps_bind=eps_extract=0, the unchanged-bound implication FAILS. No actual FS/SIS forgery needs to be simulated for this falsifier.

## Exact source-ring proof [DERIVATION]

Let Q=2^53+5, N=2048, R=F_Q[X]/(X^2048+1). Source P01 established an exact nontrivial idempotent e=(1+i X^1024)/2 with e²=e, sigma(e)=1-e for automorphism sigma(X)=X^{-1}. For ANY scalar t∈F_Q, define one-variate multilinear Y_t(T)=e(T-t) over R. It is a FALSE invariant-coefficient witness because e≠sigma(e). For scalar verifier challenge r, sigma^-1(r)=r, giving
    Y_t(r)=e(r-t)
    sigma(Y_t(sigma^-1(r)))=(1-e)(r-t).
Since (2e-1)^2=1, the proposed P05 equality holds iff r=t. Choose the valid exceptional set E={0,1,...,4095}⊂F_Q⊂R (all nonzero scalar differences invertible), so a FIXED commitment C_t to Y_t passes external random r only with probability 1/4096.

A CLASSICAL ROM prover can generate q_H=64 distinct t_j and valid commitments C_{t_j} BEFORE making the corresponding H query, then independently hash each commitment; choose any query with r_j=t_j and provide correctly evaluated v_j,v'_j plus honest PCS point-opening proofs. Every C_j is fixed before its OWN hash challenge, and all PC evaluations can be genuine; perfect binding is not violated. The 64 ideal RO responses at 64 distinct hash inputs are independent. Hence
    p_ROM=1-(1-1/4096)^64=0.015505441076417246...
    p_single=1/4096=0.000244140625
    amplification ≈63.510286649×.
Even with eps_bind=eps_extract=0, p_ROM>p_single. Domain separation prevents cross-protocol transcript confusion but DOES NOT prevent standard RO commitment grinding. The two correlated PCS evaluations constitute ONE external polynomial identity test, not two independent SZ trials.

This is a lower-bound falsifier for the claimed unchanged-FS bound, NOT a break of CMNW, the actual Huang et al. SNARG, encrypted plaintext authenticity, or lattice hardness. Full vFHE witness-mask linkage, secure real PCS commitments, and random-oracle quantum queries are not instantiated.

## Executed one exact test [VERIFIED]

Actual script /mnt/data/pvfhe_p09_fiat_shamir_commitment_grinding.py SHA256 a3518a9e7a46cbdc368b1821a310878f0874ccb46081dfcd3a5b8b849068500f.
Actual JSON /mnt/data/pvfhe_p09_fs_commitment_grinding_results.json SHA256 34c8d1acf72d12450b8dbfe3cb0ac9fb1a673bc040235ac75073d152f0975d66.
Full report /mnt/data/PVFHE_P09_FS_Grinding_and_CMNW_Slack_Audit.md SHA256 987b125e2e8bfc5abbd3dada526a2c5fc3a308ba78352b7ace5388942f82dbc3.

Exact arithmetic verifies twisted identity iff t=r under source parameters; Fraction ratio and acceptance probability computed exactly, NOT Monte Carlo. Independently enumerated all 7, 7²=49, 7³=343 RO output vectors for 1/2/3 attempts on a tiny valid seven-scalar E, yielding exact success 1/7, 13/49, 127/343, agreeing with p_q=1-(1-1/7)^q. No compiled CMNW PCS, real SIS, SNARG transcript, deployed FHE or QROM experiment.

## Source CMNW slack & suggested FS transcript [SOURCE FACTS / DERIVATION]

CMNW Theorem2 p22 single-instance extraction gives beta_*=(2r_fold*kappa_fold)^ell beta. Comparing TWO potentially different extracted valid polynomials against the SAME C needs binding on differences norm <=2beta_*, a sufficient SIS bound. The published multilinear Theorem4 p24 displays β'_source≥(2rλ)^ell β with kappa=λ. This is not automatically documentation of the extra factor 2 in P05's **two-extracted-opening** argument; to complete it choose stronger SIS hardness that really covers 2beta_* and check full lattice security, norms and parameter selection. This is not a claim the source's own theorem is invalid.

CMNW p39 Appendix A.4 already acknowledges up to **2^64** RO queries and chooses λ=192 for 128-bit in ITS SEPARATE internal PCS instantiation. A simple CONSERVATIVE sufficient target for an additional outer P05 identity test under a union-bound style ROM argument would be
    q_H*s/|E| <=2^-λ_target => |E|>=q_H*s*2^λ_target.
At q_H=2^64, s=32, λ_target=128, this requires |E|>=2^197. This is not a universal lower bound or a proved secure combined protocol. Source scalar subfield has only Q~2^53 elements: for such high concrete outer-ROM security one must consider large nonscalar exceptional subsets of R and verify unit-difference, efficient sample and consistency with arbitrary sigma^-1(r) PCS point queries. The full source ring is much larger than its scalar subfield.

Candidate transcript (new design, NOT source): public instance/selector fixed → augmented witness commitment C → external r=H_ext(protocol,params,statement,selector,C) → both claims v,v' fixed → two INTERNAL domain-separated CMNW FS evaluations for tuples (C,r,v) and (C,sigma^-1(r),v'), each binding branch ID, whole statement, C, both claims, subproof commitments and prior challenges → same-commitment masked witness-link proof. Even perfect domain separation does not erase q_H grinding. Need a CLASSICAL ROM forking/reprogramming theorem with q_H security loss, extraction failure and 2beta_* binding; no automatic QROM/post-quantum composition.

## End of iteration

**STATUS:** FAIL unchanged interactive-to-ROM soundness translation for proposed P05; PASS explicit source-parameter ideal-PCS ROM grinding countermodel and CMNW source parameter audit; UNCLEAR classical ROM full proof, joint SIS security, QROM, real large E selection and novelty.
**RESULT:** 64 candidate RO hashes raise false Galois-check pass probability from 0.0244% to 1.5505% even with perfect binding + honest point openings. CMNW's published concrete internal FS proof explicitly budgets RO-query loss, consistent with needing to account for it in OUR outer protocol. This is a standard ROM correction, not a novel cryptographic attack.
**NEXT_ACTION P10 only after PI continuation:** ONE actual classical ROM outer-forking proof-or-obstruction for the complete domain-separated transcript, with q_H loss, P08 joint-extraction error and source-extracted SIS slack at 2beta_*. Audit efficient large non-scalar E compatibility with actual Ring-PCS ONLY if first proof gate passes. QROM remains separately OPEN; no claims about existing CMNW security failure.
**STATE_UPDATE:** YES standalone P09 record ONLY. Neither concurrent global vFHE/SHIP states nor P01–P08 edited.