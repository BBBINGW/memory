# BOOT-B057 — BOLT-FHE CM external-product off-diagonal sparsification: security gate

Date: 2026-10-20
TRACK_ID: BOOT
STATUS: FAIL_NAIVE_EXACT_SPARSE_BODY_BLOCK_SECURITY_GATE (idealized toy); LOW_NOVELTY
Prior: B056 archived; SHIP remains paused.

## Primary hypothesis
Under BOLT-FHE's common-mask (CM) GLWE/GGSW representation, directly deleting publicly visible off-diagonal entries of the body-to-body GGSW block reduces the (k+r)^2 external-product pointwise-multiplication factor to k^2+2kr+r **without additional key material or security cost**, for arbitrary binary CM secret rows.

This statement covers direct exact public-zero sparsification only, not general sparsification or alternate cryptographic constructions.

## Source and provenance
[FACT] Chen et al., *BOLT-FHE: An Efficient Unified Framework for GPU-based TFHE Bootstrapping via On-Chip Local Tiling Strategies*, TCHES 2026(3), pp. 198–223. Author full text: https://zhengfangyu.github.io/assets/papers/CHES2026.pdf. Physical pages 11–12, §4.2/Table 4; physical p.26 Appendix B/Algorithm 2.
[FACT] Authors' implementation https://github.com/Leafxiaotong/BOLT-FHE. Read README; no CUDA native execution in B057.
[FACT] Table 4 gives CM amortized pointwise multiplication cost proportional to (k+r)^2/r.

## Minimum algebraic gate
[DERIVATION] Over F_q, let CM decryption be Dec_S(a,b)=b-Sa, S in F_q^(r×k). For an encrypted-scalar linear operator represented as M=[[A,B],[C,D]], exact scaling by u on every input imposes
  C-SA=-uS,  D-SB=uI_r.
If the public body/body block D is diagonal, every off-diagonal equation forces <S_i,B_j>=0 whenever i != j. Therefore every public B_j is confined to the secret-defined kernel of the other secret rows. Such mask constraints may leak S; one cannot simply zero these blocks while retaining unrestricted, secret-independent public mask sampling.

[TOY] q=257, k=3, r=2; S0=(1,1,0), S1=(1,0,1). For j=0 choose public B0 vectors (1,0,-1) and (0,1,0), both orthogonal to S1; for j=1 choose B1 vectors (1,-1,0) and (0,0,1), both orthogonal to S0. For u in {0,1}, define D=uI_2 + SB.
- Every generated D is diagonal, and D-SB=uI exactly: PASS toy algebraic functional relation.
- Enumeration of nonzero binary candidates consistent with two public mask vectors uniquely recovers S0 and S1: PASS toy secret-row recovery.
- Reproducible script: b057_cm_sparse_toy.py, provided as a local handoff artifact. This is NOT a native BOLT test or a real-world LWE attack.

## Research verdict and boundaries
The direct exact zero-off-diagonal CM-GGSW sparsification hypothesis FAILS its security-distribution premise in the toy model. It is not an impossibility theorem: noisy constructions, alternate encodings, rerandomization, modified assumptions and security analyses are not excluded. No actual DFR, GPU runtime or parameter security is claimed. The `(k+r)^2` factor cannot be eliminated by naive sparse-matrix operations for free.

B057 STATUS: FAIL_NAIVE_EXACT_SPARSE_BODY_BLOCK_SECURITY_GATE / LOW_NOVELTY.
NEXT_TEST: Select a different recent full-text blind-rotation algorithm and test one candidate that eliminates online sequential external products (rather than merely memory traffic). Demand an explicit ciphertext/key/noise mapping and an end-to-end cost gate. Do not adopt withdrawn ePrint 2026/1783 as a reproducible baseline without an accessible valid replacement.
STATE_UPDATE: NO, because GitHub Notes read_repo_file repeatedly returned {} for both policies and STATE; existing STATE was NOT overwritten. This file is a new append-only logical research artifact, not a claim of state handoff completion.
