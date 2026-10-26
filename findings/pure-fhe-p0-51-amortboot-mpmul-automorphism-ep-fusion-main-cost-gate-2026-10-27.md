# PURE-FHE · P0-PRESCOUT-51 — MPmul automorphism-parametrized external-product fusion: typed feasibility vs main-cost ceiling

Date: 2026-10-27 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
PREVIOUS: P0-PRESCOUT-50, findings/pure-fhe-p0-50-batchboot-zenodo-artifact-key-residency-fft-precision-gate-2026-10-27.md, commit 17b8c6926f1f33ab1dd560f289ca2bba5e99e7ac
LATEST_COMPLETED: P0-PRESCOUT-51
NEXT_ITERATION: P0-PRESCOUT-52 NOT_STARTED
STATUS: PASS_TYPED_MIXED_SECRET_CMUX_TOY / FAIL_NAIVE_AUTOMORPHISM_EP_FUSION_COST / FAIL_MAJOR_SPEEDUP_HEADROOM / NOVELTY_NOT_ESTABLISHED
NOVELTY: NOT_ESTABLISHED; source Bernard-Joye already has automorphism-parametrized EP, classic multi-key hybrid products and 2019 TFHE multi-key constructions cover generic mixed-secret multiplication.
CODEX_REQUIRED: NO. No Codex, native FHE/GPU, remote servers, model downloads or infrastructure changes.
STATE_UPDATE: YES one isolated PURE-FHE finding; global STATE.md and SHIP/BOOT/CGS/VFHE/EAI unchanged.

## One primary smallest falsifiable H51

Can applying Bernard–Joye's published automorphism-parametrized EP (ePrint2025/163) to Guimarães–Pereira's amortized-bootstrapping MPmul (ePrint2025/686) fuse ALL -1 automorphism key switches into existing EPs without increasing dominant EP count, and yield material end-to-end speedup at the same secret, security, noise and key budget?

Cheapest decisive source-first test: type-check 2025/686 Algorithm1 line3, and 2025/163 Definition4.1–4.2 operator input/output; calculate source-specific count of external products versus automorphism KS for n outputs and log_2 B binary stages. A single exact toy mixed-key product checks algebraic possibility but does not justify novelty/noise/performance. Do NOT repeat BatchBoot twisted-key or matrix representation screens.

## [FACT] Directly inspected complete original manuscripts

[1] Antonio Guimarães and Hilder V. L. Pereira, *Fast Amortized Bootstrapping with Small Keys and Polynomial Noise Overhead*, ePrint2025/686, https://eprint.iacr.org/2025/686 . Acquired verified parseable 34-physical-page GitHub Notes mirror sha256 84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335, final version not cross-authenticated. Reread primary §3 physical pp10–12 and Algorithm1 p12, §4 physical pp12–16. MPmul takes n ordinary RLWE ciphertexts c_j under z, an encrypted GSW bit C_i=GSW_z(v_i), and automorphism key KSK from τ_{-1}(z) to z. Its Algorithm1 line3, for j<2^i, is
  out_j = c_j + (HomAut_{-1}(c_{n-2^i+j}) − c_j) ⊠ C_i .
For 2^i≤j<n, line5 is analogous without automorphism:
  out_j=c_j+(c_{j-2^i}−c_j)⊠C_i .
Each of n outputs has ONE external product per binary stage, but only the first 2^i outputs per stage require automorphism switching. Their text gives O(n log B) EP and auto-key switching overhead, with log B stage count and B≤n assumed in this test. This is an amortized-bootstrapping operation, and no claim is made it has the SAME parameters/performance as BatchBoot's algorithm.

[2] Olivier Bernard and Marc Joye, *Bootstrapping (T)FHE Ciphertexts via Automorphisms: Closing the Gap Between Binary and Gaussian Keys*, ePrint2025/163, https://eprint.iacr.org/2025/163 , 37-page GitHub Notes mirror sha256 ce81021fca19132729765ad652a2f4a8f1d27d6b9c7f084777b6386fa5e08387 (version unverified). Read full original physical pp6–7,13–17,26–30. Definition4.1 extends GGSW to encrypt secret-dependent −ψ(z)v in the mask rows and v in the body row under OUTPUT secret z. Definition4.2 allows
  RLWE_z(m) ⊛_ψ GGSW_{z,ψ}(v) → RLWE_z( ψ(m)*v )
in one parametrized EP, avoiding an intermediate automorphism KS. Proposition4.3 derives its noise bound under centered gadget digits; known author's already original contribution, not ours. Source §2 p7 gives same gadget-level cost model for k=1, ℓ=1..3:
  r=cost(KS_ψ)/cost(EP)=(ℓ+2)/(2(ℓ+1)) in [5/8,3/4];
not a measured universal runtime or statement all hardware ratios lie in this interval. The paper uses this operation when the automorphism is immediately FOLLOWED by an EP; our MPmul has a SUBTRACTION of an independently encrypted value between those stages.

[3] Chen, Chillotti, Song, *Multi-Key Homomorphic Encryption from TFHE*, ASIACRYPT2019, publisher paper https://www.iacr.org/archive/asiacrypt2019/119210155/119210155.pdf . Publisher abstract describes general hybrid products multiplying mixed-key RLWE ciphertexts by bootstrapping material and classical multi-key ciphertext extension, already prior art for generic vector-of-secret/extended-GSW constructions. Its PDF was indexed and opened via web, and screenshot attempts returned cache miss; do not claim full line-by-line author proof audit here. It is a warning that constructing a mixed-secret gadget product is unlikely a standalone novel primitive. Ordinary single-secret CMUX also existed in CGGI/TFHE.

## [DERIVATION] Why naive 1EP fusion FAILS and incurs 2EP

Set m_s = Dec_z(c_source) and m_j=Dec_z(c_j); ψ=τ_{-1}. The desired MPmul wrap branch is m_j + v(ψ(m_s)−m_j).

One can use the 2025/163 parametrized EP directly on c_source and GGSW_{z,ψ}(v) to get v ψ(m_s) under z, then a STANDARD EP on c_j and GGSW_{z,id}(v) to get v m_j, then add c_j:
  c_j + [c_source ⊛_ψ Kψ(v)] − [c_j ⊛_id Kid(v)].
This is correct in ideal plaintext and avoids explicit automorphism KS, BUT costs TWO EPs per wrap position instead of original ONE EP plus ONE automorphism KS. This does not preserve EP count or key-object count: must provide BOTH tagged and standard selector keys and may share body rows only if compatible.
Since source cost ratio r in [0.625,0.75] for k=1, ℓ1..3, its direct local cost is 2 EP vs 1+r EP in [1.625,1.75] EP equivalents: a LOCAL SLOWDOWN of about 14%–23% in the simple source model, before expanded selector key bytes and noise.

## [DERIVATION + TOY_EXECUTED] A different 3-gadget-row mixed-secret CMUX is algebraically valid but not promising

Define c_source=(a_s,b_s) under z, c_j=(a_j,b_j) under z, sign convention b−a*z=m. Let ψ act on ciphertexts and secret. Publicly assemble a THREE-component mixed-secret ciphertext
  A1=ψ(a_s), A2=−a_j, B=ψ(b_s)−b_j,
which decrypts under vector secrets (ψ(z),z) to
  B−A1 ψ(z)−A2 z = ψ(m_s)−m_j.
Use an extended gadget-GSW keyed to OUTPUT z with THREE row payloads (at each of ℓ gadget levels) encrypting under z
  R1=Enc_z(−ψ(z) v), R2=Enc_z(−z v), R3=Enc_z(v).
Then the mixed-secret external product
  A1*R1 + A2*R2 + B*R3
encrypts v(ψ(m_s)−m_j) under z. Add c_j to obtain the desired CMUX output under z for both v=0,1.

A private exact negacyclic-ring toy executed with N8, q257, z small polynomial, 8 independent randomly chosen noiseless source/branch ciphertext pairs at v0 and 8 at v1: 16/16 exact plaintext outputs equaled intended m_j+v(ψ(m_s)−m_j). This is ONLY exact ideal polynomial arithmetic with direct products; not real gadget decomposition, actual key-generation distributions, noise/security/DFR, or a runnable speedup.

Cost obstacle: at each stage, ordinary GSW(v) has 2ℓ gadget rows, a shared automorphism KSK has ℓ_ks rows, while mixed selector has 3ℓ rows. When ℓ_ks=ℓ, it merely FUSES THE SAME THREE GADGET ROW-LEVEL CONTRIBUTIONS as baseline, not a reduction of main work. It also needs extra secret-dependent row Enc_z(−ψ(z)v) PER selector bit (rather than one shared KSK) and mixes secrets; security and noise proof require new auxiliary-KDM/circular-secret analysis. Multi-key TFHE hybrid product is already prior art; even if arithmetic is correct, no new original FHE primitive is established. A better fused FFT/read scheduler might change constants but requires source-matched performance and a larger headroom than shown below.

## [DERIVATION + TOY_NUMERIC] Absolute optimistic effect of eliminating every MPmul KS

For B a power of two, B≤n:
 EP=n log2 B;
 KS=Σ_{i=0}^{log2B−1}2^i=B−1.
Let r=cost(KS)/cost(EP). Ignoring all other steps, source's first-order relative baseline cost in EP-equivalents is
 T_base/CostEP=n log2 B+r(B−1).
If a hypothetical algorithm could completely eliminate ALL KS, cost ZERO extra EP, NO extra keys/noise/FFT (a deliberately UNREALISTIC best case),
  SpeedupIdeal=1+r(B−1)/(n log2 B).
For n=B=4096, EP=49152, KS=4095:
 r=5/8 → speedup1.05207062x;
 r=3/4 → speedup1.06248474x.
Even allowing r=1 for a very conservative accounting gives max1.083313x. For n=B=1024: 1.06244–1.07493x over r range. If B smaller than n, actual headroom is smaller. For the full SAB bootstrapping after h repeated MPmul, this KS-to-EP ratio remains approximately unchanged, while other extraction/test-vector costs can further DILUTE the best-case end-to-end gain.
For the naive twice-EP rewrite and n=B=4096:
  T_new ≈EP+KS=53247 EP units
  T_base ≈EP+r KS ∈[51711.375,52223.25];
  local-paper model therefore estimates an MPmul OPERATION-PROXY slowdown 1.96%–2.97% overall rather than acceleration. Not a native benchmark, and gadget row scheduling/cache/FFT and added key bytes/noise not included.

The counting assumptions may change under an alternative MPmul circuit different from author Algorithm1 or an implementation which executes a different number of KS; then fresh evidence is needed. These formulas prove no universal theoretical lower bound, only a decisive original-source cost ceiling for THIS candidate route.

## Novelty and decision

The strongest **positive** construct tested here is a typed 3-row mixed-secret CMUX; it is algebraically correct but reduces neither gadget-row count nor dominant EP count, and generic multi-key GSW/hybrid product and 2025 automorphism-parametrized EP are already known. The direct cross-paper fusion doubles EPs in the wrap branch and is predicted slower under author's own cost model. Even perfect deletion of all original MPmul KS offers only 1.05–1.06x on an illustrative n=B4096 MPmul dominated path, far below a clear systems-crypto contribution threshold, with new key/noise/security costs.

=> STOP / PARK H51. Do NOT ask Codex to implement this or spin more similar transform fusions. If PURE-FHE is to continue, it must target the dominant n log B EP term in 2025/686 with a genuinely new reduction in total external products or a different verified major per-EP operation, and clear prior-art comparison to 2025/686 and BatchBoot2026. Such a new mechanism has NOT been constructed in this round, and P0 program remains STAGNATION/HUMAN_REVIEW after 51 screens.

END_OF_ITERATION
STATUS: PASS_MIXED_SECRET_CMUX_IDEAL_ALGEBRA / FAIL_MPMUL_FUSION_1EP / FAIL_LARGE_HEADROOM / NOVELTY_NOT_ESTABLISHED
RESULT: Direct automorphism-parametrized MPmul requires 2 EP rather than 1EP+1KS in wrap positions. A 3-row mixed-secret key can do the same selection algebraically but not with reduced gadget-level work. n=B4096 source-model perfect KS deletion at most1.052–1.062x for usual k1 ell1..3, ignoring other costs.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: NO automatic P0-52. Renew only on one new source-backed FHE mechanism that changes dominating n log B EP cost rather than side automorphism KS, or a primary-source artifact enabling a genuine distinctive construction. Other tracks unchanged.
STATE_UPDATE: YES single isolated PURE-FHE finding; no global STATE.md.
CODEX_REQUIRED: NO.