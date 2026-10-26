# PURE-FHE · P0-PRESCOUT-44 — BatchBoot special/twisted RGSW derived from ordinary RGSW by automorphism + RLWE key switching

Date: 2026-10-27 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: PURE_FHE_ORIGINAL_KEY_REPRESENTATION_SOURCE_GATE
PREVIOUS: P0-PRESCOUT-43, findings/pure-fhe-p0-43-shape-gckks-rounding-commutator-2026-10-27.md, commit a0f54ef3f214d9dd86bd8d5f2c741be32b6937cd.
LATEST_COMPLETED: P0-PRESCOUT-44
NEXT_ITERATION: P0-PRESCOUT-45 NOT_STARTED (PI continuation).
STATUS: PASS_TYPED_IDEAL_PLAINTEXT_DERIVATION / OPEN_CRITICAL_NOISE_DFR_KEY_SECURITY / NOVELTY_UNESTABLISHED
NOVELTY: NOT ESTABLISHED — key-switching and automorphism are standard, specialized on-demand use against this BatchBoot key table not located in checked authors' source but search is NOT exhaustive.
CODEX_REQUIRED: NO. No native FHE, GPU, remote server, code modifications, downloads, or repository infrastructure changes authorized.
STATE_UPDATE: YES one isolated PURE-FHE findings file; shared STATE.md and unrelated BOOT/SHIP/CGS/VFHE/EAI lines unchanged.

## Motivation and one smallest falsifiable H44

P0-39 found BatchBoot's two-bit multi-CMux grouped selector has FOUR ordinary and THREE automorphism-tagged RGSW variants per key group, and discarded FREE public one-hot complement compression because cross-secret row differences and 4→6 EP in negative-boundary branch. It did NOT rule out a *nonfree homomorphic conversion using automorphism and key switching*.

H44: For scalar one-hot u∈{0,1}, can a server derive the NEGATIVE/twisted RGSW key K^-_s(u) from the ordinary K^+_s(u) using a public RLWE automorphism plus RLWE key switching, and thereby choose to NOT persist 3 special variants for each two-bit selector group, without modifying the online BatchBoot parametrized external product? One decisive CHEAP first test: derive type-correct two-row ciphertext relation, check existing automorphism key domain, exercise exact small negacyclic ring algebra, calculate maximal object-level savings and identify source noise/security barriers. This first test must not claim native viability or novelty.

## [FACT] Complete first-party source

Li, Wang, Zhao, Li, Wang, He, Wei, Yan, Guo, *BatchBoot: Fast Batched Bootstrapping for TFHE scheme and Practical Applications*, USENIX Security 2026, official accessible 20-page pre-publication PDF https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_li-zhihao.pdf ; main https://www.usenix.org/conference/usenixsecurity26/presentation/li-zhihao .
PDF page screenshots were obtained through web for zero-index p5 §4.1 Table1 Eq(7–9), p6 Algorithm2 and sparse background, p7 Algorithm3, p11 Table4 and p17 Alg5/6, p19 Table9/10 and peak memory Table13. Physical p5 Eq7–9:
 ordinary K_s^+(u)=[RLWE'_s(-s*u),RLWE'_s(u)];
 special K_s^-(u)=[RLWE'_s(-tau(s)*u),RLWE'_s(u)], tau=automorphism X→X^-1.
Both are rows of gadget RLWE' encryptions with the SAME OUTPUT encryption secret s (here s abbreviates the LARGE-RING ACCUMULATOR/BOOTSTRAPPING AUXILIARY secret, NOT the main incoming sparse RLWE secret). Selector bits u_j are scalar one-hot binary plaintexts 0 or 1, so tau(u_j)=u_j. Source Table1 requires ordinary Bsk+ j=0..3 and special Bsk- j=0..2, with j3 shared ordinary. Original online Eq9/Algorithm2 uses both type-tagged keys and author noise Lemma4.1 V_EMP < V_in+2ell V_EP.
Source Algorithm3 p7 defines BSK under LARGE-RING aux secret tilde{s} (notation e s in extracted PDF); repacking Auk_i=RLWE'_{tilde{s}}(tau_i(tilde{s})), and Rlk switches tilde{s}→s_sparse. This means a hypothetical direct AuK_-1 under tilde{s} is type-compatible with Bsk. However Algorithm5 and Algorithm6 use published repacking automorphisms with indices i=2^{logN−k+1}+1, NOT an explicitly listed i=−1. Do NOT claim required key Auk_-1 is already in Table10! It must be added or synthesized via a separately certified automorphism composition. Table10 Boot6 specifies ring degree N=4096, h=33, B_Bsk=2^23, d_Bsk=1, B_Auk=2^23,d_Auk=1; before deploying, inspect exact key generation and possible FFT/preparation differences.
Table4 same 6-bit full-packing nominal DFR 2^-64 author benchmark: BatchBoot amort 8.43ms/msg, reported "Key Sizes" 120.1MB; AmortBoot 8.92ms/msg and "Key Sizes" 18.6MB. Key Sizes ARE NOT decomposed into individual Bsk+/Bsk-/Auk/Rlk. Table13 same author 6-bit peak RAM 1425MB, not equal to key bytes; no promised 6.46x savings.

Other first-party near prior art: De Micheli–Kim–Micciancio–Suhl *Faster Amortized FHEW Bootstrapping Using Ring Automorphisms*, https://par.nsf.gov/servlets/purl/10505100 and ePrint2023/112, §3.1 p10 explicitly explains a GENERIC RGSW_s(m) cannot simply be key-switched into a GENERIC RGSW_{s'}(m), because the message -s*m in row1 must ALSO change. Our candidate explicitly targets a **different twisted output format** K^-_s(u), where the desired first row is -tau(s)*u under s; applying tau first to K^+_s(u) makes the first row ALREADY contain -tau(s)*u. Then only the encryption-key secret τ(s) must change back to s. Thus there is no logical conflict with their general negative observation. Aut/KeySwitch are long-established primitives (also the source of its own technique), so this compositional adaptation has serious novelty/obviousness risk. Search for these exact words did NOT return an already-used identical special-BSK memory format, but novelty is NOT established by absence of a search hit.
Parametrized external product itself is prior work credited by BatchBoot to Bernard et al. Any new publication claim requires exact nearest-algorithm novelty inspection and a substantial proven storage/runtime/DFR improvement.

## [DERIVATION] Type-correct rowwise transform

Let R=Z_Q[X]/(X^N+1), s∈R, τ:X→X^-1, and u∈{0,1}⊂R fixed under τ. Define standard gadget-RLWE' row encryption under key s:
  K^+_s(u)=( RLWE'_s(-s*u), RLWE'_s(u) ).
Applying τ to each coefficient of every encrypted RLWE row maps a plaintext v to τ(v) but also maps the encryption secret s to τ(s). Thus:
  τ(K^+_s(u))=(RLWE'_{τ(s)}(-τ(s)*u), RLWE'_{τ(s)}(u)).
Now key-switch EACH RLWE row using a public KS key AK_{τ(s)→s} (with same ring degree/modulus/gadget representation and suitable noise):
  Derive(K^+_s(u);AK):= KS_{τ(s)→s}^{rowwise}( τ(K^+_s(u)) )
   = (RLWE'_s(-τ(s)*u), RLWE'_s(u))
   = K^-_s(u)
in IDEAL PLAINTEXT semantics. The result is not bitwise identical to fresh K^- and need not have same encryption randomness/noise. It is vital that the key switch does NOT attempt to convert generic RGSW_s(m)→RGSW_{τ(s)}(m); it only restores the ENCRYPTION secret after τ has correctly twisted the key-dependent plaintext.

More generally if u is not τ-invariant, output encrypts τ(u); scalar-BatchBoot one-hot u is invariant; monomial/packed selectors are not and need a distinct operation.

## [TOY_EXECUTED] Tiny ring algebra

N=8, q=257, s=1+X², τ(s)=1−X⁶. With random fixed public RLWE masks, noiseless row encryptions were formed under s for u=0 and u=1. Rowwise τ followed by a toy exact one-component encrypting τ(s) key switch under s was executed by negacyclic coefficient convolution modulo (q,X^8+1). Decrypted transformed row pairs for u=0/1 reproduced precisely (-τ(s)*u,u) in all four row tests (4/4). Toy KS used zero added KS noise and a full exact coefficient factor in place of real gadget decomposition: toy confirms the plaintext identity only; does NOT verify true RGSW encoding distribution, DFR, key-size, security or real implementation.

## [DERIVATION] Conditional key-object inventory & processing model

Per standard two-bit selector GROUP (Table1):
 Original keyed objects = 4 K^+ plus 3 independent K^- = 7 RGSW objects; j=3 shared.
 Proposed *persistent* objects = 4 K^+; construct 3 K^- via Derive on demand, plus ONE shared extra direct Auk_-1 for all groups if existing repack Auk set lacks it. If ordinary and twisted RGSW ciphertexts have the same row sizes, ideal gross BSK object reduction = 3/7 ≈42.857% (NOT 42.857% of reported Table4 120.1MB or Table13 peak1425MB). For large number G of groups, storing vs on-demand RGSW rows: original7G objects, reduced4G objects + O(1) automorphism switching-key objects. Source B_Bsk=2^23,d_Bsk=1 and B_Auk=2^23,d_Auk=1 in Boot6; exact bytes depend on ciphertext formats, key representation and possibly original compression, and G, client/server key metadata not audited.
If the server GENERATES K^- once and caches every special key, only serialized key / distribution size decreases; peak resident eval-key RAM is basically unchanged. RAM benefit needs a *stage-wise lazy materialization/eviction schedule* that holds only a small number of derived K^- at a time while K^+ remain loaded. Online Algorithm2 uses both K^+ and K^- in the same stage, so RAM cannot be reduced by discarding K^+ entirely.
For a stage which uses G groups and n packed accumulator components, key derivation incurs at most 3*(2d_Bsk) =6d_Bsk automorphism/KS per group (if two RLWE' bundles each d rows), while the baseline original Algorithm2 computes 4*n EP per group in the naive operation count. The *number* ratio at n=4096, d_Bsk=1 is 6/(4*4096)=0.0003662, but an RLWE KS can be much more expensive than an EP and FFT/preparation traffic is omitted. There is NO measured latency gain or negligible overhead claim. The same key can be reused for all n outputs of one stage after derived.
Table4 6bit Bsk key-size contrast 18.6 vs120.1MB and 6bit peak RAM1425MB do NOT tell us the actual byte-share of these special selector keys. Full per-object storage breakdown remains a key blocking observation.

## [OPEN — CRITICAL] Proof/systems obstacles before promotion

(1) Noise: original BSK RGSW rows contain errors e_r. After τ and KS, each derived row error becomes τ(e_r)+ε_{KS,r}. Source Appendix B.2–B.3 gives gadget-product error variance V_GP and RLWE.KS variance from the gadget product. The derived keys will inherit the additional KS error, and all derived rows share the SAME Auk_-1; their errors and normal Bsk+ errors may be correlated. Original Lemma4.1 was proved for authors' native key generation; cannot transplant it with V_EP unchanged or assume independence. Need a certified bound for final 6bit DFR 2^-64, ideally future 2^-128 parameters. Because failure tails can be sensitive to even small variance changes, this is main decisively cheap next falsifier.
(2) Key security: publishing Auk_-1 = RLWE'_s(τ(s)) is key-dependent auxiliary material. Similar keys are used by BatchBoot for other automorphisms, but adding a new direct index changes the joint evaluation-key security assumptions and estimator accounting; postprocessing itself adds no independently generated leakage only GIVEN the original BSK+ AND new Auk_-1 are safe jointly. Sparse secret challenge and circular security not automatically addressed.
(3) Prepared key/FFT: transformed special ciphertexts may need prepared Fourier representations and must satisfy source's RGSW variant message/scaling/gadget contract. Constructing one group could induce extra key-switch FFTs and peak working buffers, and on-demand time may offset storage savings. If source implementation already derives twisted keys or uses seeded/prepared on-demand versions, novelty disappears.
(4) Innovation: ordinary RLWE automorphisms and KSK are standard; even if engineering speeds are good, would be an implementation/compression technique more readily publishable in a systems-crypto venue than an original new FHE scheme. Need first-party closest Bernard parametrized EP and De Micheli 2023/112 source novelty gate. This note DOES NOT claim a publishable new scheme.

## Decision

Unlike P0-39 complement and P0-43 trivial basis rewrite, H44 yields a NONTRIVIAL, TYPE-CORRECT latent key-generation strategy with a measurable best-case object-share, contingent on adding/reusing a τ_-1 automorphism key and meeting the author’s noise budget. Prior stagnation warning remains; retain precisely this ONE conditional candidate rather than resume broad random prescouts. It is NOT an approved experiment or ready-to-build scheme. Next cheapest decisive iteration P0-45, only if PI continues: insert source Table9/10 Boot6 noise values into a full rowwise \tau→KS transformation bound, quantify resulting V_EP and author Lemma4.1/V_Boot, evaluate model DFR vs 2^-64. If provably incompatible at reasonable gadget parameters, KILL. If noise plausible, inspect implementation/near prior art and full BSK allocation BEFORE requesting Codex. Explicitly do not reopen SHIP/BOOT research records or borrow their experiment results as our evidence.

END_OF_ITERATION:
STATUS: PASS_TYPED_RGSW_TWIST_DERIVATION / FAIL_FREE_REUSE_OF_AUK_-1 / NOISE_DFR_NOVELTY_UNCLEAR
RESULT: K^-_s(u) plaintext rows obtained exactly by KS_{τ(s)→s}^{rowwise}(τ(K^+_s(u))) for scalar one-hot u fixed under τ. Conditional 3/7 selector object storage opportunity with added/synthesized Auk_-1; four toy row checks passed; real performance/security not established.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: P0-PRESCOUT-45 (not started), source Boot6 noise-budget and end-to-end DFR KILL gate; thereafter novelty / peak-RAM breakdown.
STATE_UPDATE: YES, isolated PURE-FHE findings file only.
CODEX_REQUIRED: NO.
