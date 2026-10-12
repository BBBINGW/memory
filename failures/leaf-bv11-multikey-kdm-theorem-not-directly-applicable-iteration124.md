# Iteration 124 — BV11 multi-user KDM theorem does not directly certify LEAF's cross-ring BFV evaluation keys

Date: 2026-10-12. PI explicitly authorized continuation from I123 and its UNIQUE NEXT_ACTION. Exactly ONE primary hypothesis, ONE cheapest decisive original-theorem-to-real-construction test. No code, no implementation attack, no author contact.

## Source provenance

**Target LEAF:** Linru Zhang, Xiangning Wang, Xianhui Lu, Huaxiong Wang, Kwok-Yan Lam, *LEAF: A Low-Latency Evaluation Architecture for Feedforward Block in Privacy-Preserving Transformer Inference*, IACR ePrint **2025/956** https://eprint.iacr.org/2025/956, Research MCP full 43 physical-page PDF (mirror SHA256 `937fbae4dcd32f421c91f7df4ad83c3a003861b168f4bfd7798be1476a736267`; official VERSION_UNVERIFIED). `findings/leaf-cross-key-kdm-cycle-security-obligation-iteration123.md` provides independently source-anchored I123 result. Primary LEAF anchors: §3.2 Algorithm 1 physical pp14–15; §3.5 physical p20; §3.6 security paragraph p23.

**Precisely identified candidate prior theorem:** Zvika Brakerski and Vinod Vaikuntanathan, *Fully Homomorphic Encryption from Ring-LWE and Security for Key Dependent Messages*, CRYPTO **2011**, source author-hosted complete 20-page PDF, https://www.wisdom.weizmann.ac.il/~zvikab/localpapers/IdealHom.pdf, §4 physical pp15–17; **Theorem 4**, p17, `KDM^(1)_{P_d}` security for THEIR PLWE-based scheme; **Theorem 5**, §4.1 physical p17, `KDM^(ν)_{P_d}` for polynomial ν under their `PLWE_{Φ_m,q,χ*}` assumption. Theorem 5 was inspected in original PDF visually (physical p17) and surrounding construction/parameter rules visually (physical p16). Source does not promise KDM security for arbitrary other encryption constructions.

## ONE primary hypothesis and decisive theorem-applicability test

[HYPOTHESIS] The already-published CRYPTO 2011 **multi-key** affine/polynomial KDM Theorem 5 can be directly invoked as-is to certify the actual paired public evaluation keys in LEAF, under its original BFV/low-RLWE schemes and concrete ring embedding, so no separate joint-key proof or assumption mapping is needed.

[FALSIFIER / ONE TEST] Compare four theorem prerequisites: (i) **exact encryption algorithm**, (ii) **key-generation distribution**, (iii) **ring/parameter family across multiple recipients**, and (iv) **message-function class**, against LEAF Algorithm 1 and §3.5. A definite algorithm/key/ring mismatch falsifies **direct as-is application**. This is an applicability test, NOT a general theorem-impossibility statement.

## One test outcome — rigorous scope mapping

**LEAF [FACT]:**
- Let s_L denote low degree-n RLWE secret; s_H denote independent high degree-N BFV secret.
- Public packing ciphertext: `K_pack = BFV.Enc_{s_H}(Rep(s_L))`, where Rep makes a BFV-slot vector of repeated low-key coefficients (§3.2 Alg1).
- Return switch ciphertext/key: `K_switch = BFV.Enc_{ι(s_L)}(s_H)` (schematic key-switch encryption/key entries), where `ι(s_L)(X)=s_L(X^{N/n})` in the degree-N ring (§3.5).
- §4 parameters: n=1024,N=32768, p=512, q=P=65537, BFV ciphertext modulus log Q=669. `ι(s_L)` is deterministically derived, highly structured / sparse as degree-N key; neither a fresh independent draw from BV11's specified small Gaussian χ* nor the standard high BFV key distribution.

**BV11 [FACT]:**
- Theorem 5 on physical p17 **does prove multi-user KDM** for **their own** PLWE-based scheme over a ring R_t, with the explicitly defined KDM.Encryption scheme / distribution in §4 (not an arbitrary BFV instantiation), and a ν-user construction requiring specified secret distributions and parameter swallowing.
- Definition `P_d[R_t]` is the polynomial family `p(z)=Σ_{i=0}^d α_i z^i` for α_i∈R_t. Its proof chooses *keys in the same scheme's ring* with Gaussian χ*, and the KDM-specific encryption construction has ciphertext tuples and parameter choices including sufficiently large/super-polynomial q (§4, physical pp15–17).
- Theorem 5 neither speaks of **LEAF's BFV.Enc** (rounding/rescaling plaintext modulus with its own ciphertext representation), nor directly handles recipients with deterministically related secret keys in **two ring dimensions**, nor by itself certifies the entire evaluation-key distribution of LEAF. KDM message class is potentially linear in input coefficients, but even if linearity maps into the class, the mismatches above remain decisive.

**[DERIVED / NEGATIVE]** The chosen candidate theorem's **direct-use** hypothesis is FALSE. Multi-key capability in a specific PLWE construction ≠ KDM security of every BFV/low-RLWE scheme; additionally, multi-key for its specified independently generated key setup ≠ automatic key security for LEAF's embedding `ι(s_L)`.

## Interpretation and closure

[FACT] Prior art on *multi-user* affine/polynomial KDM exists since at least 2011; do not suggest that simply identifying a 2-key cycle is a novel cryptographic issue. This checks **one prominent theorem**, not exhaustive literature. Other scheme-specific affine KDM reductions for LWE/RLWE or an acceptable circular-security assumption might be applicable after independent proof. Neither an attack nor a compelling novel repair was produced.

[OPEN] A custom formal reduction/lemma for LEAF's actual KDM joint keys could be possible; would need precise security game including ordinary rotation/relinearization keys, actual BFV key distributions, embedding and ciphertext noise, and to distinguish assumptions vs provability. No such work authorized or tested here. **Actual LEAF insecurity NOT ESTABLISHED.** No performance result refuted.

[NOVELTY] NOT VERIFIED for any repair. Source-specific applicability mismatch is a useful audit boundary but weak contribution, justifying PARKING repeated KDM microaudits.

## End of iteration
STATUS: **FAIL direct BV11 theorem application / PASS source-backed theorem-assumption mismatch / HUMAN_REVIEW**.
RESULT: BV11 Theorem 5 proves polynomial multi-user KDM for its own PLWE construction, but cannot be directly invoked for LEAF's `BFV.Enc_{s_H}(Rep(s_L))`, `BFV.Enc_{ι(s_L)}(s_H)` with ring-degree/key-distribution differences; no insecurity shown.
NEXT_ACTION: **PI must authorize a different, higher-upside technical FHE target** (or identify a specifically applicable new KDM construction/proof technique) before I125. Recommend PARK LEAF I123–124; do not recycle basic circular-security lore as future iterations.
STATE_UPDATE: **YES** — close the one I124 hypothesis and park LEAF, preserving I123 observation and all historical failures.
