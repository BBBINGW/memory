# BOOT B023 — Mask sharing gate for one-hot RGSW selectors

TRACK_ID: BOOT
ITERATION: B023
DATE: 2026-10-19
STATUS: FAIL_SHARED_MASK_SAME_SECRET_SECURITY / FAIL_NAIVE_MATRIX_SECRET_AGGREGATION
STATE_UPDATE: YES

## Primary falsifiable claim
Can the RGSW bootstrapping keys within one 2023/958 one-hot block share the same RLWE mask for corresponding message-bearing rows, reducing key storage without losing key secrecy or the original one ordinary external product per block? Check ciphertext-body differences first, and one source-inspired matrix-secret repair.

## Source facts
- Lee–Min–Seo–Song, ePrint 2023/958, full verified-title 19-page mirror PDF, version unverified, SHA256 0ab8c83d5aebbbf0185e200c7c3aab10150aa4e3bad0470a839246d33954e6de; physical pp10–12 Algorithm2 and Lemma1: one-hot block with selectors s_i, block key sum of (X^a_i−1)*RGSW(s_i), one ordinary external product per block under SAME RLWE secret.
- Bergerat et al., Sharing the Mask, TCHES 2025(4):925–971 DOI 10.46586/tches.v2025.i4.925-971, ePrint 2025/2112. Source full paper HTML text at ResearchGate article 395320098, printed p934 Definition7 and p937 Definition11/Theorem2: CM-GLWE=(A,AS+Delta*M+E) with DIFFERENT per-body secret-key columns S; CM-GGSW times CM-GLWE gives CM-GLWE, a changed matrix-key ciphertext interface. Cross-slot private linear operations and extra evaluation material are also covered in that publication. ePrint original verified full PDF unavailable via research MCP, a mirror failed AUTHOR identity; do not claim official PDF was acquired or visually verified. DOI/TCHES metadata matches six authors in independently confirmed published article.
- Zama TFHE-rs documentation documents already existing seeded/compressed server/evaluation key representations, using PRNG regeneration. Generic seeded independent masks not a new contribution. BatchBoot USENIX 2026 still relevant for strongest competing implementation.

## Same-secret leakage proof
At a body-plaintext gadget row of standard RGSW over ring R_q, write B_i=A*t+E_i+g*s_i modq with SAME mask A and SAME RLWE secret t, for one-hot block s_i binary and sum<=1. The attacker publicly subtracts B_i−B_0=g*(s_i−s_0)+E_i−E_0 modq. Thus t and A cancel. If relevant error coefficients bounded by E and g>4E, with sufficient mod-q distance between 0 and +/-g, nearest-center rounding gives every s_i−s_0. For block length>=2, those differences uniquely reconstruct the one-hot vector including all-zero: all0 => allzero; all−1 => s0 active; unique +1 => that position active. For unbounded Gaussian noise, recovery is high probability conditional on small-error event, not literally perfect. Standard RGSW contains body-message gadget rows; sharing even one such row is dangerous. Ideal per-row memory count for ell4 drops 2ell=8 polys to ell+1=5 (37.5% fewer) but security FAILS; not valid gain.

## Independent minimal test
Exact ring R=Z_4096[X]/(X^8+1), ell=4, g=256, onehot or zero s, shared uniformly random mask A, common ternary secret t, coefficient noise each in [-3,3].
- 5000/5000 fixed-seed randomly generated ciphertext blocks: public body differences from index0 identify s.
- Exhaustive 5*(7^4)=12005 possibilities for one-hot state and four constant-term noise coefficients: 12005/12005 successfully classified; independent of A,t because they cancel algebraically. Toy arithmetic only, not native TFHE/cryptographic parameters and NOT an attack on published TCHES common-mask scheme.

## Nontrivial author-inspired repair and counterexample
Use DIFFERENT secrets t_i per body as in published CM-GLWE: B_i=A*t_i+E_i+g*s_i. The simple difference attack vanishes since A*(t_i−t_0) remains. But source 2023/958 ordinary scalar block aggregation with public polynomial weights w_i=X^{a_i}−1 yields A_sum=(sum w_i)A, B_sum=sum w_i B_i. Relative to any chosen target common ring secret t*, its phase contains unintended term:
  A*sum_i w_i*(t_i−t*) .
This is generally not small encryption noise and does not vanish for arbitrary rotation weights. Deterministic counterexample q4096, A=1024 constant, t0=0,t1=1, w1=X−1, s1=1, errors0: phase relative t0 contains extra 1024(X−1), not a correct encryption of g(X−1).
Exact N8 ring test, ell4, 2000 independent random mask/ternary t_i/rotation-weight tuples: in 2000/2000 the additional term is nonzero and its maximum centered coefficient abs >24 (expected per-output honest bounded-error upper proxy 2*ell*3=24), median of max centered abs ~1868. This is illustrative, not a proof every instance fails.
Crucial qualifier: published CM-GGSW matrix external product is valid for CM-GLWE; the negative result applies to the naive attempted re-interpretation as 2023/958's ORIGINAL single-scalar-secret RGSW aggregation, NOT a universal prohibition on matrix-key PBS.

## Repair search and scientific decision
1) Sharing mask+same ring secret is unacceptable due public one-hot leakage.
2) Matrix-secret common-mask avoids direct cancellation but forces a different native operation, or costly conversion/key switching back to one ring secret. Published TCHES already provides CM-GGSW and cross-slot transforms: no novelty from mere matrix adoption.
3) Independent masks can be seeded and reconstructed; standard seeded eval-key compression already exists. To obtain an actual new speed/memory contribution, must combine regeneration with block aggregation schedule without extra Fourier transforms/key streaming, and compare full online cost to pre-Fourier keys.
STATUS: FAIL_SIMPLE_COMMON_MASK / PASS_EXPLICIT_ATTACK / UNCLEAR_NEW_FUSED_SEEDED_ALGORITHM.
RESULT: No safe new key-memory improvement established. Failure is a useful constraint for a complete construction, not grounds for abandoning original BOOT focus.
NEXT_TEST B024: Stay with original block-binary amortization. One structural hypothesis: fuse seeded independent-mask regeneration, public monomial weighting and block RGSW aggregation in coefficient domain BEFORE Fourier transform, avoiding full on-device Fourier eval-key materialization while retaining one external product. Cheapest gate: source-aligned per block FFT/PRG/read bytes/keys/noise accounting compared with pretransformed RGSW and existing seeded-key methods, plus prior-art GPU fused pipelines; no automatic speedup claim.
STATE_UPDATE YES. BOOT-only files.
