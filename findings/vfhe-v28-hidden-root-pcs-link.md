# vFHE V28 — Unlinked Hidden Grand-Product Roots Cannot Replace Source PCS Root Openings

**Date:** 2026-10-14. Independent vFHE V28, general FHE I192 FROZEN.
**STATUS:** FAIL hypothetical unlinked hidden-root-only redesign; PASS exact source-style native PCS counterexample and exhaustive finite-field challenge census. Not an attack against original vFHE protocol.

## Primary hypothesis and one test

**Hypothesis H-V28 (falsified):** Replace the four PUBLIC Figure 1 GP root openings f_alpha^(1)(1,0) with four INDEPENDENT hiding/binding root commitments and a perfectly sound ZK proof of the product equation WSt*WSh=RS*S. Retain original fieldwise oracle commitments and GP sumcheck but OMIT knowledge-sound linkage of each new root commitment to the actual original polynomial evaluation. Claim this keeps lookup soundness.

**Cheapest decisive test:** Set up one FALSE memory multiset relation with legitimately committed GP trees, and test whether independent hidden-root witnesses can satisfy the product equality while actual root values do not. Also independently authenticate the tree roots with a source-shaped native F.2/F.3 PCS toy. Do not simulate a full ZK protocol.

## Original source [FACT]

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025, ePrint2025/286. Inspected 52pp GitHub mirror SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19; official 2026-02-16 revision VERSION_UNVERIFIED. §4.3 pp22-23 gives WS,RS,S and Figure1: authentic four GP oracle roots at Boolean (1,0) must obey f_WSt(1,0)*f_WSh(1,0)=f_RS(1,0)*f_S(1,0). Appendix E.2 physical p49 lists root openings; Appendix F.1 physical p50 implements ring PCS as per-CRT field commitments; Appendix F.2 physical p51 authenticates a PUBLIC native polynomial evaluation y by sending v'=q1Uf and checking Enc(v')|Q'=q1 Uhat|Q' AND y=<v',q2>. Appendix F.3 pp51-52 permits piecewise RS. It does not supply ZK proof that an unrelated Pedersen/root commitment opens to the SAME secret evaluation y.

## Exact algebraic counterexample [DERIVATION]

Take legal N4,d2,p13=1+(2N/d)*3. R=F13[X]/(X4+1) ≅ K5×K8 with K_z=F13[u]/(u²−z), z=5,8 are nonresidues. Table t2=(0,1), actual accesses h=(1,1), read_ts=(0,1), but false final_cts=(0,0), all fixed before sigma,tau. Choose sigma=4,tau=2. Computed in BOTH native extension field factors:

| α | Native leaf values | ACTUAL grand-product root |
|--|--|--|
| WSh | 3,7 | 8 |
| RS | 12,3 | 10 |
| WSt | 11,12 | 2 |
| S | 11,12 | 2 |

Original root check LHS=2*8=3 mod13, RHS=10*2=7 mod13, hence original Figure1 REJECTS. All four legitimate GP trees individually satisfy their leaf and recursion constraints; only root product fails. The modified verifier may instead accept independent ideal binding root commitments all to 1, with a VALID ZK proof of 1*1=1*1. The proof is correct about independent commitments but does NOT establish the intended original polynomial-root statement.

For general sigma,tau in native K, original true-side difference simplifies exactly to:
    Delta = (-tau)*(1−tau)*(1+sigma−tau)*(2*sigma).
This is not the zero polynomial. Exhaustively test all 169²=28561 native field challenge pairs: 672 accidental true-root identity passes, 27889 genuine-source product-check rejections. The detached fake roots pass product check for ALL challenges. Thus a perfectly binding ZK root product proof without equality linkage is logically UNSOUND as a replacement.

## Original F.2/F.3 compatible toy [EXPERIMENT]

For each of BOTH CRT extension factors, construct each GP root polynomial as MLE Boolean table U=[[leaf0,leaf1],[true_root,0]]. This obeys source GP tree recurrence. For N4,m2,τ2 use the F.3 piecewise [2,1] RS code Enc([a,b])=[a,a,b,b]. For 4 GP oracles build Merkle roots of all encoded COLUMNS (each leaf has 2 native extension elements) using SHA256, verify authentication. For root Boolean point (1,0), q1=(0,1),q2=(1,0). Exact original F.2 native y=<q1Uf,q2>=true_root and Enc(q1Uf)|Q'=q1Uhat|Q' checks PASS on all columns. These authenticated real roots are DIFFERENT from new fake root commitments. No hash collision, PC-binding failure, or counterfeit polynomial proof is used.

Independent standard-Python reproduction run twice, deterministic:
- /mnt/data/vfhe_v28_hidden_root_link_gate.py, SHA256 87c02afb93f9241eab68d69ba32d4d8ecb3cf5f36e032b3e8718be98cf09eeda
- /mnt/data/vfhe_v28_hidden_root_link_results.json, SHA256 fdf2d228100e7ef5684c1f3a10503e3501b293ed0783101f2610577fdc25f0a6
- /mnt/data/VFHE_V28_Hidden_Root_PCS_Linkage_Gate_2026_10_14.md, SHA256 415c644529b09b73bf54f4d128d888ee7e1ed6695406c315715cda3fb57c1176.
Files are LOCAL and not committed to Git as bytes.

## Correct repair obligations, cost, and research judgment

To replace public root openings with hidden ones, for EVERY CRT field factor i and GP α we need a JOINT, knowledge-sound and (if privacy is intended) zero-knowledge statement:
1. Native cm_alpha^(i) binds a specific original polynomial f_alpha^(i).
2. Hiding C_alpha^(i) binds P_alpha^(i).
3. ZK cross-commitment EVALUATION EQUALITY proves P_alpha^(i)=f_alpha^(i)(1,0) without revealing P_alpha.
4. Correct native field equations P_WSt*P_WSh=P_RS*P_S across all factors, including extension-field coordinates and quotient/range safeguards if using an outside proof group scalar field.
5. Commitments/transcript/order and existing GP sumchecks are preserved.

Proving only item4 omits item3 and fails as tested. This is a necessary cryptographic interface, not a universal impossibility theorem: real hiding PCS, commit-and-prove and ZK-sumcheck designs may provide it. For context see Chiesa/Forbes/Spooner, *A Zero Knowledge Sumcheck and its Applications*, arXiv:1704.02086, but that paper is NOT a drop-in proof of this F.2 Merkle equality.

**Conditional naive counts, NOT a lower bound:** 4 root-to-PCS ZK links plus 2 extension-field multiplications per factor. At illustrative N=2^14,d4, k=N/d=4096 and two CRT primes, 8192 factors imply 32768 direct root links and 16384 native multiplications. Original Figure1 already does root evaluations and an optimized hiding scheme might batch them; no actual prover timing, security level or communication measured.

**Separate research themes:** Hiding Boolean GP roots is OUR optional extra witness-privacy design objective. It does NOT fix the core original cross-CRT diagonal small-INTEGER digit soundness issue. The latter requires another common canonical bounded digit binding protocol; still unbuilt. Latest official Feb2026 PDF not authenticated. No author-facing vulnerability claim or unsolicited disclosure.

**END V28:** STATUS=FAIL unlinked GP-root-only hiding patch / PASS exact 28561 challenge native PCS experiment. RESULT explicit necessary equality-link condition. NEXT_ACTION V29 only with PI continuation: cheapest REAL published hiding PCS/commit-and-prove linking the new root to original native Merkle/RS polynomial root, with proof composition and cost, OR park root-hiding and prioritize official source and original canonical CRT digit soundness. STATE_UPDATE YES independent V28, global I192 frozen.
