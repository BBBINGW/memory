# Iteration 123 — LEAF's packing and ring-switch keys form a cross-key KDM cycle

Date: 2026-10-12. PI authorized I123 after I122, delegating selection of a NEW independent structural FHE target. One primary hypothesis and ONE cheapest decisive technical test: public evaluation-key dependency graph. No implementation, no adversarial break, no author contact or public disclosure.

## Target / sources / provenance

**[FACT]** Linru Zhang, Xiangning Wang, Xianhui Lu, Huaxiong Wang, Kwok-Yan Lam, *LEAF: A Low-Latency Evaluation Architecture for Feedforward Block in Privacy-Preserving Transformer Inference*, IACR ePrint **2025/956**, https://eprint.iacr.org/2025/956.
Read actual full 43-physical-page Research MCP mirror PDF, SHA256 `937fbae4dcd32f421c91f7df4ad83c3a003861b168f4bfd7798be1476a736267`, fixed source revision `811323a5133478d67d2bf9525ef58af1f50d02a0`, `github-mirror`, official ePrint latest `VERSION_UNVERIFIED`.
Primary technical citations, *physical* page:
- §3 p12: distinct low-degree RLWE key s (degree n) and high-degree BFV key s (degree N), despite the PDF's similar variable notation.
- §3.2 Algorithm 1 pp14–15: packing key `BFV.ct_packing = Enc_{s_H}(Ecd_slots([s_L,s_L,...]))`; used to homomorphically compute the low-degree RLWE decryption linear form in the high-degree BFV cipher.
- §3.5 p20: ring/key switch key `ks_{s_H→s'_L} = Enc_{s'_L}(s_H)`, where `s'_L(X)=s_L(X^{N/n})` (coefficient interleaving: `s'_L[i]=s_L[i/(N/n)]` when divisible by N/n; 0 otherwise); then degree-N ciphertext switched and split into degree-n RLWE ciphertexts.
- §3.6 Security analysis p23 states the security of combined scheme can “be easily derived from the semantic security of RLWE cryptosystem and BFV scheme” because the keygen/encryption algorithms were not changed. It does not there separately prove KDM/circular security for these public auxiliary keys.
- §4 p23 uses concrete n=1024,N=32768,p=512, low-level q=65537, BFV plaintext modulus P=q=65537, so relevant key dependencies exist in the reported benchmark configuration. This is NOT a hypothetical unused code path.

Security background: KDM/circular security is a distinct guarantee from IND-CPA/semantic security; see Barak–Haitner–Hofheinz–Ishai, *Bounded Key-Dependent Message Security*, ePrint **2009/511**, https://eprint.iacr.org/2009/511, and the KDM survey https://www.cs.columbia.edu/~tal/papers/kdm-survey.pdf. No special LEAF attack follows from this general principle. The repository was checked for earlier LEAF/KDM named findings; no matching file title was found. NOVELTY NOT VERIFIED as a cryptographic concept.

## Exactly ONE hypothesis + decisive test

[HYPOTHESIS] The LEAF paper's simple combination-of-semantic-security argument already handles the **actual public packing + return ring-switch keys**, without requiring any KDM/circular-key security property or separate joint-distribution proof.

[FALSIFIER / CHEAPEST TEST] Build the encrypted-secret dependency graph directly from Algorithm 1 and §3.5; if it forms an encryption cycle between two related decryption keys, the usual *independent message* IND-CPA hybrid does not directly apply, so “just semantic security” is not in itself an adequate stated justification for the auxiliary-key joint distribution.

## One test — graph-level derivation

Define secrets:
```
s_L: degree-n low RLWE key
s_H: independent degree-N BFV key
ι(s_L): degree-N key with ι(s_L)(X)=s_L(X^(N/n))
Rep(s_L): degree-N BFV plaintext-slot repetition of low-key coefficients
```

[FACT] From the actual stated key material:
```
K_pack   = Enc_{s_H}(Rep(s_L)).
K_switch = Enc_{ι(s_L)}(s_H).
```

[DERIVED] `ι(s_L)` is a deterministic embedding of `s_L`, not fresh independent entropy. Public key-dependency graph has edges `s_L → s_H` (packing), `s_H → ι(s_L)` (ring switching), closing an effective 2-key KDM cycle `s_L ↔ s_H`.

[DERIVED] A simple hybrid that tries to replace `K_pack` with encryption of zero under s_H would treat `K_switch` as public side information, yet this side information is an encryption **of s_H** and so is correlated with the challenge encryption's decryption key. Standard IND-CPA does not give the required hybrid for such related auxiliary information. Reversing the order fails symmetrically. One must invoke a suitable circular/KDM security theorem or an explicit different reduction which accounts for **both** disclosed keys and their deterministic key embedding. Ordinary BFV rotation/relinearization keys may bring further key dependence; the *two-edge cycle alone* already suffices to show why the one-sentence standard IND-CPA reasoning is incomplete.

[NEGATIVE] The precise hypothesis that *the presented plain semantic-security sentence itself suffices as a complete security proof for the actual public auxiliary-key distribution* is not supported; its direct IND-CPA hybrid justification is blocked by the above correlated-key side information.

[OPEN] It may be possible that the exact existing BFV/low-RLWE instantiation enjoys enough KDM security for these **linear** secret functions, or that a reduction to an accepted circular-security assumption and precise distribution works. No actual distinguishing adversary or security failure was constructed. We have not verified whether existing specific KDM results already fully settle this instantiation. It is important not to claim a break from mere existence of a key cycle.

## Importance and novelty discipline
- **Real setting:** coefficients-to-BFV-to-coefficients roundtrip at N=32768,n=1024; public helper keys are central to LEAF's 53.4s claimed application benchmark. KDM assumption changes matter to formal end-to-end privacy even if runtime unchanged.
- **Known primitive issue:** the need to reason about KDM/circular encryption is well-established in FHE, so a bare observation of a cycle is **not publishable by itself**. `NOVELTY NOT VERIFIED`.
- **Possible nontrivial future work (not yet researched):** show an *applicable* affine-KDM security theorem under LEAF's exact key distributions and gadget/rotation keys, or develop an **acyclic** sequence-of-keys conversion with measured key-size/latency consequences. Neither has been tested here.
- No authors contacted; no allegation of actual exploit or bug in measured behavior.

## End-of-iteration
STATUS: **PASS (existence of explicit KDM dependency cycle) / UNCLEAR (actual KDM insecurity or viable repair) / HUMAN_REVIEW**.
RESULT: the joint auxiliary keys are `Enc_{s_H}(Rep(s_L))` and `Enc_{ι(s_L)}(s_H)`, which form a two-key secret-dependence cycle not covered by *generic* independent-message IND-CPA alone. The proof obligation is concrete but the issue is known in FHE and no novelty is established.
NEXT_ACTION: PI gate before I124. If continuing this target, ONE hypothesis should test applicability of a specifically identified **affine/linear KDM or 2-circular security result** to the exact LEAF auxiliary-key distribution (including the ring-degree embedding). If it is already established, PARK; if not, assess nontrivial/real-value repair. Alternatively PI delegates selecting another structural FHE paper. Do not automatically re-open I120–122 FAB or historical archived failures.
STATE_UPDATE: YES — new named proof-obligation finding alters repo checkpoint; keep other branches unchanged.
