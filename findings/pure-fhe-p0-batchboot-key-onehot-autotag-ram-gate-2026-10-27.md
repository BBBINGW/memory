# PURE-FHE P0-PRESCOUT-39 — BatchBoot one-hot / automorphism-tagged key-memory gate

DATE: 2026-10-27 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: BATCHBOOT_KEY_REPRESENTATION_GATE
PREVIOUS: P0-PRESCOUT-38 findings/pure-fhe-p0-portfolio-stagnation-priority-review-2026-10-27.md, commit f0f7c0f63278fda68ad93cfe34460d237f4651ca
STATUS: PASS_ONE_HOT_LINEAR_REDUNDANCY / FAIL_FREE_FULL_KEY_DEDUP / NO_PUBLISHABLE_MECHANISM_ESTABLISHED
NOVELTY: NOT_ESTABLISHED; the affine one-hot/CMux identity is standard and author use of variant RGSW is already the core innovation.
CODEX_REQUIRED: NO. No native FHE/GPU/Codex/remote execution or changes to other projects.
STATE_UPDATE: YES this single isolated PURE-FHE finding, NOT root STATE.md / BOOT / SHIP / CGS / VFHE.

## One smallest falsifiable H39 and cheapest test
H39: The approximately 6.46x size increase in BatchBoot vs AmortBoot for the source-paired six-bit 4096-message parameter family is *predominantly freely removable public representation redundancy* (e.g. four one-hot selectors or re-encodings of identical plaintext), rather than secret-tagged evaluation keys needed to preserve the author's FFT/CMux online work.
Cheapest test: fully inspect first-party USENIX BatchBoot paper Table1, Eq7-9, Algorithms2/3, §6.1, Table4, Table10, Table13 and compare ordinary RGSW_s to RGSW^{tau-1}_s; derive the exact one-hot elimination operation/keys/noise/time tradeoff, with original i-th boundary lengths and no native runs.

## [FACT] Primary first-party evidence, visually verified
Zhihao Li et al., "BatchBoot: Fast Batched Bootstrapping for TFHE scheme and Practical Applications", USENIX Security2026 prepublication official 20-page PDF https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_li-zhihao.pdf ; conference https://www.usenix.org/conference/usenixsecurity26/presentation/li-zhihao .
PDF visually screened via web screenshot 0-index p3,4,5,6,7,11,19. Official preprint: physical p6 (0-index5) Table1 and Eq(7)–(9), physical p7 Alg2, physical p8 Alg3, physical p11 §6.1, physical p12 Table4, physical p20 Tables9/10/13.
Paper Table1 at every two-bit grouped selector stage specifies:
  * ordinary Bsk^+_{i,j} = RGSW_s(u_j) for j=0,1,2,3, where (u0,u1,u2,u3) encode the four mutually exclusive bit pairs; plaintext sum u0+u1+u2+u3=1 exactly;
  * parametrized Bsk^-_{i,j} = RGSW_s^{tau_-1}(u_j), j=0,1,2, and Bsk^-_{i,3}=RGSW_s(u3) (same type as ordinary Bsk^+_{i,3}). Thus naive ciphertext inventory if independently realized is FOUR ordinary plus THREE special = SEVEN distinct full RGSWs per grouped pair, not eight (ordinary j3 is shared).
  * source defines RGSW_s^{tau_-1}(m) with secret-dependent first row encrypting -tau_-1(s)*m under output secret s, as opposed to ordinary RGSW_s(m) first row encrypting -s*m. So their difference requires (s−tau_-1(s))*m, not a public constant unless tau_-1(s)=s; the tag is semantically nontrivial. Whether a special public key translation could be constructed with additional key material or extra noise remains OPEN and cannot be declared impossible.
  * source Eq8 hoists FFT over automorphisms, and Alg2 produces 4 external product terms per output coefficient in its *source version*, carrying V_EMP<Var(input)+2ell V_EP (Lemma4.1). Alg3 full pack h+1 EMPmul plus Repack(Auk) and RLWE.KeySwitch(Rlk); sparse case additionally uses RtM extraction and k-dependent EMPmul. §6.1 also defines Ssk for circuit bootstrapping, not a mandatory key for basic functional full packing.
  * Table10 Boot6 nominal parameters: plaintext 2^6, ring n=2^12=4096, h=33, N=2^12, B_Bsk=2^23,d_Bsk=1; B_Auk=2^23,d_Auk=1; B_Rlk=2^17,d_Rlk=2 (from visual page).
  * Table4 six-bit paired source numbers: AmortBoot8.92ms/msg, "Key Sizes"18.6 MB vs BatchBoot8.43ms/msg,"Key Sizes"120.1MB, reported DFR2^-64, 4096 messages, single-thread same server; key size ratio 120.1/18.6=6.45699 and performance relative 8.92/8.43=1.058125 (5.49% time reduction). Table4 HEADER "Key Sizes" and §6.1 discuss multiple types of bootstrapping-related evaluation keys, but paper DOES NOT disaggregate sizes by Bsk^+, Bsk^-, Auk, Rlk and Ssk. Correct earlier P0-10/38 framing that called the entire 120.1MB "BSK-only" without definitive component proof. The authors discuss "bootstrapping key sizes" collectively, so 120.1MB is *reported key-size total of unclear inclusions*, NOT verified complete all-evaluation key/peak RSS or exclusively BSK.
  * Table13 physical p20 single-thread peak RAM at same full packed precision: 2-bit360MB, 4-bit360MB, 6-bit1425MB, 8-bit3743MB. 6-bit 120.1/1425=0.0842807 ratio of *reported key size* to *measured peak RAM*, not a mathematical upper bound on peak reduction from key compression: prepared copies, FFT scratch, allocator and retained copies could amplify a key-size reduction.

## [DERIVATION] Exact one-hot identity and candidate key omission

Let U0..U3 be the four binary one-hot indicator plaintext values for a pair (v_i,v_(i+1)): sum Uj=1. For public input RLWEs C0..C3 and ordinary external-product selector encryptions Kj=RGSW_s(Uj), ideal output:
  Out=Σ_{j=0}^3 Cj ⊡ Kj.
It has identical plaintext as
  Out=C3 + Σ_{j=0}^2 (Cj−C3) ⊡ Kj.
Thus in the ordinary-only selector region, omit a *separately stored* K3 and implement three external products plus one public linear RLWE combination instead of four. For a real gadget implementation this equality is at *ideal plaintext semantics* and changes decomposition/rounding errors and distribution; ciphertext bitwise equality, DFR and IND-CPA security are NOT established.
However the mixed-automorphism region of original Eq(9) has:
  Out=Σ_{j=0}^2 Cj ⊡_{tau^-1} Kj^- + C3 ⊡ K3^+.
Replacing K3^+ using 1−Σ_{j=0}^2 Uj yields
  Out=C3+Σ_{j=0}^2 (Cj ⊡_{tau^-1} Kj^-)−Σ_{j=0}^2 (C3 ⊡ Kj^+).
This requires SIX external products instead of source FOUR (three under each secret-dependent RGSW tag) plus a clear RLWE addition. A naive design that substitutes K_j^+=K_j^- would be semantically wrong because the "ordinary" and "parametrized" external products have different secret/automorphism relations. Mixed index intervals in Algorithm2 likewise require explicit typing, not a blanket 3-CMux claim.

For ring size n=2^12=4096, ell=12 and paired stage index i=0..5 in Alg2, mixed-boundary range at each i is b_i=2^(2i)+2^(2i+1)=3*4^i, and ordinary-only range n−b_i.
Original pure external-product count across all slots/stages is Σ_i 4n =4*n*6=98,304.
The basic K3-omission rewrite gives Σ_i[3(n−b_i)+6 b_i]=Σ_i(3n+3b_i)=3*n*6+9*Σ_(i=0)^5 4^i=86,013.
Ideal arithmetic proxy reduction 12,291 /98,304=12.50305% external product terms at this FULL power-of-two ring size, notwithstanding the final stage is worse (+5,120 terms) and the first five save. This EXCLUDES changed FFT/decomp reuse, clear RLWE additions, key preparation, memory traffic, and error growth. It is NOT a demonstrated 12.5% latency improvement.
For keys, the ONE obvious relation lets one omit at most 1 of the 7 RGSW objects per grouped pair if the paper implementation stores them all equally and separately: 14.29% of THESE BSK object counts. It says NOTHING about 14.29% of Table4 bytes (other keys and formats), global prepared RAM, or proof of maximal possible compression. It is nowhere near an explanation of a 6.457× reported key-size ratio which would need eliminating 84.51% of BatchBoot's reported key-size budget to match AmortBoot18.6MB, before security/performance concerns.
Potential variance: original source's Lemma4.1 uses four external-product noises per iteration. Omission changes distribution and correlation: mixed boundary output can involve six key-encryption-error terms and positive positions three, so the original V_EMP certificate cannot be copied unchanged. A worst-case bound may worsen rather than match the source DFR=2^-64. Key correlation from constructing missing selector by subtracting multiple key ciphertexts must also be audited.

## [FACT / PRIOR ART / UNCERTAINTY]
Ordinary CMux affine identity FHE selector gate is classic: a public branch plus an encrypted selector applied to a *difference* (see Zama TFHE Deep Dive, Part III https://www.zama.org/post/tfhe-deep-dive-part-3, prior to BatchBoot); multi-bit key groups containing 2^g GGSW encryptions are already in TFHE-rs key-generation code https://docs.rs/tfhe/latest/src/tfhe/core_crypto/algorithms/lwe_multi_bit_bootstrap_key_generation.rs.html . Do not claim adapting that obvious complement identity is a novel cryptographic representation, nor assume it is absent from BatchBoot's unpublished implementation. No new full key generation code was independently inspected for BatchBoot: paper says implementation built on MOSFHE but does not provide keyed byte-level Bsk+/Bsk-/Auk/Rlk breakdown in Table4.
Potential RGSW(-tau(s)m) and ordinary RGSW(-s*m) could share *some lower encryption rows* when generated with aligned randomness, but independent-message/key-distinguishability and error correlations must be proven; knowing a shared plaintext m alone does not create publicly reconstructible full keys. Prior SHIP and BOOT records rejected generic seeded GLWE compression that still fully expands at evaluation and naive shared selectors; do not reassign track names, and do not claim those are complete impossibility theorems.

## H39 decision
FAIL to establish that the 6.457× reported key-size contrast is *predominantly* a set of freely removable duplicate representations. The only obvious linear one-hot relation is a one-of-seven selector-object opportunity and comes with mixed tau-boundary work/noise costs; the more substantial ordinary/parametrized distinction is secret-dependent. Actual implementation stored/prepared/all-keys bytes remain unresolved. This is a negative gate of the naive approach, NOT a proof of a lower bound on evaluation-key storage, nor a crypto break, nor independent theorem novelty.
Because the costed candidate is a routine CMux algebra rearrangement, it has HIGH PRIOR ART and lacks any 2^-128 DFR realization. Recommend PARK/KILL naive BatchBoot BSK selector-complement compression as a *publishable mechanism*. Reopen BatchBoot key memory only if a genuinely novel typed relation between normal/tau-tagged selector keys or an actual high-leverage prepared-key structure with full security/noise/online-cost ledger is established. Do NOT launch GPU or Codex to prototype this on weak originality evidence. Portfolio P2 matrix representation remains source-gated, P3 dynamic noise proof remains high prior-art.

END_OF_ITERATION:
STATUS: PASS_SOURCE_TYPED_KEY_INVENTORY / FAIL_H39_MOSTLY_FREE_PUBLIC_REDUNDANCY / PARK_NAIVE_ONEHOT_KEY_COMPLEMENT
RESULT: grouped pair needs four ordinary and three tau-tagged RGSW key variants; one-hot affine relation saves no more than one nominal RGSW per seven under transparent construction but may increase mixed-branch EP4->EP6; same-source six-bit reported key sizes 18.6 vs120.1MB, peak RAM1425MB, DFR2^-64. No native or complete per-key bytes.
NOVELTY: NOT_ESTABLISHED.
NEXT_TEST: Stop ordinary one-hot/seed/FFT key compression experiments. PI-directed next prescout can inspect source-complete competing matrix-FHE operator bridge or other major source-backed mechanism, but its nearest ASIACRYPT2026 batch CKKS paper may need full original for confident novelty.
STATE_UPDATE: YES only this isolated findings file; no global root/other tracks.
CODEX_REQUIRED: NO; implementation PENDING explicit PI permission.