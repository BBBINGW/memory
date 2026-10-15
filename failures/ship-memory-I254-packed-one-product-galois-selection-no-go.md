# SHIP-I254 — Packed selector one-product Galois rotation no-go under candidate-independent invertible preprocessing

Date 2026-10-16. **PI-selected TRACK_ID SHIP, I254 only**; no CGS/VFHE/EXPLORE modifications. I253 failure path was verified with source directory listing; I252 local record exists but GitHub STATE update from I252 was blocked by tool read failure. This iteration read attempt of RESEARCH_PHILOSOPHY.md, AGENT.md, START_RESEARCH_SESSION.md, root and topic STATE, I253 and I251 **all returned empty object `{}` from Research GitHub Notes read_repo_file**, while listing works. Therefore root/topic shared states were intentionally NOT blindly appended; this self-contained archive is the sole intended repo mutation. Public independent Poulpy source code could be fetched via GitHub connector and was rechecked. Previous SOURCE_BLOCKED original-author security I245 and project PARK recommendation stand.

## Primary falsifiable hypothesis H254

**H254:** Replace B separate HMux candidate-specific encryptions of selector bits `beta_d` / rank2 switching keys with a single packed encrypted selector polynomial `P_beta`, and realize `F_beta(m)=Σ_d beta_d σ_{g_d}(m)` using just **one ring multiplication/external product** between encoded selector and **one common candidate-independent representation of input m**, with no additional secret-dependent nonlinear selector operations, no candidate-specific input rotation materializations, and only candidate-INDEPENDENT public unit monomial and Galois preprocessing/postprocessing.

**Cheapest decisive falsification:** Even ignoring noise/security, if this restricted plaintext operator class cannot equal the desired family of Galois automorphisms on basis inputs 1 and X, it cannot yield a correct ciphertext construction. Read the source operator, give analytic proof, execute toy exact finite-ring checks. One hypothesis, one proof/test; no arbitrary parameter sweep or hardware implementation.

## Primary source facts

- Original Cheon–Hanrot–Kim–Stehlé SHIP, ePrint 2025/784 §4.2/§5.1: ciphertext mux rotates `Σ_d beta_d sigma_{g_d}(m)` for hidden onehot digit; precise output security and original h31 keygen not re-evaluated here.
- Pinned **independent third-party** `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`, `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4` shows rank2 input `(beta*s,beta)` under rotation-dependent destination secret. `poulpy-ckks/src/reference/ship/mux.rs` blob `e9df6b5e4958fea1af6af3334d99fcb8b8f8b5ce`, lines66–147, performs candidate GGLWE products, PUBLIC output DFT Galois per candidate, then sum. Direct packed scalar GGSW is NOT the implemented algorithm.
- Prior SHIP I205 already ruled out a different shared-key + linear encrypted-`beta` factoring by bilinear mixed finite difference; I227 binary CMux and I246–I253 key-column sharing, gadget multiplication fusion and high noise shortcuts are distinct archived failed/non-Pareto candidates. The current gate is specifically **algebraic nature of rotation vs ring multiplication**; no independent novelty claim.

## Exact theorem / obstruction [DERIVATION]

Let `R_Q=(Z/QZ)[X]/(X^N+1)`, `N>=4`, `g_i,g_j` distinct odd units mod2N, `sigma_g:X→X^g`. Let candidate outputs be `F_d(m)=sigma_{g_d}(m)`, which follows by selecting onehot `beta_d=1`. Consider the permitted architecture
```
F_d(m) = C(m) + V(P_d · U(m))
```
where `P_d∈R_Q` may depend on hidden selector d, `C` is **any selector-independent additive/linear** map, `U,V` are selector-INDEPENDENT invertible public transformations composed of ring automorphisms and multiplication by monomial **units** `uX^r` (u invertible). Thus `U(1)` is a unit of R_Q and V is injective. All public preprocessing/ postprocessing is common to choices.

For two different choices i,j, `F_i(1)-F_j(1)=sigma_gi(1)-sigma_gj(1)=0`. The C term cancels, so
```
0 = V((P_i-P_j)U(1)).
```
Injectivity of V and invertibility of U(1) imply `P_i=P_j`. Consequently `F_i(m)-F_j(m)=0` for ALL m. Taking `m=X` yields `sigma_gi(X)=sigma_gj(X)` in contradiction, because the monomials `X^gi` and `X^gj` are different in R_Q for distinct odd units (for Q>2, the signs are distinguished). Thus **one packed ring multiplier plus only common public unit-monomial/Galois transforms cannot select among distinct Galois automorphisms**, even with arbitrary selector-independent affine bypass C.

Simpler direct special case: `P_d m=σ_gd(m)` for m1 forces `P_d=1`; for m=X then requires X=X^gd, impossible for gd≠1.

This is a precise restricted architecture no-go, **NOT a universal no-go** for packed SIMD selectors or representation changes: noninvertible U mapping 1 to zero-divisor, arbitrary large-dimensional public linear isomorphisms, candidate-specific rotated data, custom ring extensions, extra nonlinear ciphertext multiplication, and selector-dependent preprocessing are explicitly outside the hypothesis. Any escape needs its own cost/security/noise and operational proof.

## Exact executed toy [TEST]

Program `/mnt/data/ship_i254_packed_selector_one_product_gate.py`, SHA256 `b39d9fdc76243b95c104271138b2d5746f1bb980c266f01e27487b9bce5bbae5`; JSON `/mnt/data/ship_i254_packed_selector_one_product_gate.json`, SHA256 `dd065956f2e357a6d723053a534306d1efcea3e9b10987c6d90d91875d429af1`. Verified exact run using Python `runpy.run_path` and reread JSON with assertions after an initial notebook variable name collision (corrected prior to archive).

Toy `N=8,Q=257`, Galois `g=1,5,9,13`, 128 random pairs of public invertible monomial+Galois transformations; for all `C(4,2)=6` pairs = **768/768** exact necessary-condition checks PASS. All g fix 1; different g have distinct image of X. No adversarial key recovery/actual cryptographic sample/noise/CKKS precision or IFMA benchmark. It is unnecessary to run ciphertext test since plaintext functionality is already contradicted.

A tempting **INVALID bound** in the illustrative source `h32,radices[4,4,4,3]`: baseline480 candidate keys vs128 groups if one magical packed candidate key existed would suggest **73.333% FEWER KEY OBJECTS**, not correctly determined prepared bytes and **NOT an achievable scheme** under H254. We DO NOT claim 75% realized memory or speed.

## End I254

**STATUS:** **FAIL H254** direct one-ring-product packing under source-shaped fixed invertible public pre/post; **PASS** exact formal necessary proof & 768 tiny algebra checks; **UNCLEAR** more general SIMD/group-algebra transform (no theorem/no cost). Existing real SHIP evalkey resident Pareto remains not improved; original-authors h31 security I245 SOURCE_BLOCKED. **RESULT:** Galois branch selection is not ordinary selector-conditioned ring multiplication on a common input representation. Any proposed packing scheme must either provide distinct rotated inputs, change representation with nontrivial transforms, or pay more encrypted computation. Previous I205 essentially flagged related bilinear control; this is not asserted a novel primitive or general impossibility theorem. **NEXT_TEST only if material new mechanism:** one explicit alternative encoding with full decryption identity, security, transformed-key bytes, and fair IFMA online/RSS accounting, else PARK and PI HUMAN_REVIEW. Do not repeat simple onehot/mixed-radix/seeded-gadget scans. **STATE_UPDATE PARTIAL:** this new standalone failure archive; shared root/topic checkpoint held due GitHub Notes read_repo_file returning `{}`, do not append blind.
