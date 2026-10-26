# PURE-FHE — Session handoff after P0-PRESCOUT-22

Date: 2026-10-26 (Asia/Hong_Kong / Asia/Singapore)
TRACK_ID: PURE-FHE
ROLE: Human is PI (direction, novelty judgment, experiment authorization, final decisions). ChatGPT is AI Research Student.
LATEST_COMPLETED: P0-PRESCOUT-22
NEXT_ITERATION: P0-PRESCOUT-23 — NOT_STARTED
ACTIVE_TOPIC: Independent PURE FHE research, currently high-precision GCKKS bootstrapping.
READ_BEFORE_WRITE: List/check repository paths and relevant protocol; prefer AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md; never overwrite or append to shared files without reading actual contents and ensuring isolation. During this session GitHub Notes read_repo_file returned {} even for known files, so no shared global files were modified. Exact source-of-truth for this handoff is this isolated log and findings.
TRACK ISOLATION: NEVER conflate PURE-FHE with SHIP, BOOT, CGS, VFHE, EXPLORE, EAI-SYS, EAI-SEC, EAI-SYNTH. Especially 'SHIP' in PaCo prior art is an algorithm-name collision, not user's separate SHIP eval-key-memory track.
EXECUTION: Do not initiate Codex, GPU/native benchmarking, remote server, downloading large models, environment changes, full bootstrap implementation or cross-track repository writes without explicit PI authorization. One iteration = one falsifiable technical claim + cheapest decisive test; falsify before building. The PI may say '继续' to authorize the next lightweight theoretical literature/math step in PURE-FHE. Do not silently begin multiple iterations. Distinguish FACT / DERIVATION / SPECULATION and reported vs independent native evidence. At end: STATUS / RESULT / NEXT_TEST / STATE_UPDATE.

## Verified research archive / sources

Recent isolated findings are already persisted in findings/ under prefix pure-fhe-p0- (the repository list verified all relevant filenames, including P0-11 to P0-22).
Most relevant:
- findings/pure-fhe-p0-supplied-2026-alu-gckks-primary-source-verification-gate-2026-10-26.md (P0-20)
- findings/pure-fhe-p0-gckks2600-nonunit-conversion-modulus-lift-gate-2026-10-26.md (P0-21)
- findings/pure-fhe-p0-gckks2600-stage2-headroom-branching-cost-gate-2026-10-26.md (P0-22)
- findings/pure-fhe-p0-triangle-a2b-bounded-window-obstruction-gate-2026-10-26.md (P0-18)
- findings/pure-fhe-p0-global-prefix-a2b-precision-priorart-gate-2026-10-26.md (P0-19)

Supplied primary PDFs VERIFIED IN-GITHUB and readable with read_repo_pdf:
- papers/supplied/2026-1836.pdf SHA 71ee2d857cd59bd83fe60316120be7a5f428905a
- papers/supplied/2026-1840.pdf SHA fb5f5c20a61030b8a1ecfdb150cf4602d4dcc4ea
- papers/supplied/2026-1869.pdf SHA 9de785af66b3106e509283c84816513d56f6f7dd
- papers/supplied/2026-2524.pdf SHA 5e38e0e5f2095604af7142b5cdba4ad5e5e86683
- papers/supplied/2026-2600.pdf SHA 8db712155d087284d21e924623496bc48e36eb72
Other supplied related: papers/supplied/2025-1594.pdf SHA 049872913a58b55d7833688e66756b01371745a3, and 2025-1760.pdf.
Two important additional papers NOT PRESENT IN supplied at handoff; GitHub Notes ePrint acquisition reported HTTP 403 and mirror unavailable:
- ePrint 2026/2531, Cheon–Lee, revision dated 2026-10-20 *High-Precision CKKS with Focal Units*, https://eprint.iacr.org/2026/2531 . Primary source currently not independently readable; paper 2026/2600 §1.3 provides a SECONDARY characterization.
- ePrint 2026/2513, Dumezy, *Fully Homomorphic Encryption for Small Batches of Complex Numbers*, https://eprint.iacr.org/2026/2513 , also reviewed only through other authors and available abstract/blog, not original PDF. Do not claim full verification. If critical for novelty gate request authorized user PDF be placed in papers/supplied/, but continue useful lightweight algebra while absent.

## Historical outcome (do not restart obsolete lines)

P0-1–10: broad sparse/nonlinear representation and bootstrapping scouting; many author-source checks and conditional cost gates, no independent publishable FHE algorithm. P0-11–16: generic exact square-commutation, rotation-closed subspaces, sparse SubSum/trace, and naive EvalMod tail/contraction proposals failed or overlapped prior art. P0-17–19: Triangle ALU A2B local-window and one-shot normalized global prefix attempts falsified in restricted models; avoid presenting generic impossibility of O(1) A2B. P0-20 verified 2026/1836, 1840, 1869 original PDFs: all authors report nonamortized O(1) A2B (with additional levels/costs). In 1836 power-of-two canonicalization 3 CKKS bootstrap calls, large-prime 5; 1840 two FBT calls *after* overflow RefreshI; 1869 two FBT calls for A2B plus logarithmic-depth carry composition. These newer works have replaced Gao–Zheng CRYPTO26's broad open question; park generic A2B as novel candidate.

P0-20 also verifies 2026/2524 introduced high-precision GCKKS (F-augmented decryption, sacrificing slots for lower modulus consumption), then 2026/2600 (DRAFT 2026-10-22) supplied high-precision GCKKS bootstrapping with low-precision overflow bit extraction, iterative precision-doubling and split, and slot-aware factor conversion. Source p26 §6 explicitly 'Implementation: Not available yet'. The 2524 'bootstrap left for future work' is now answered as a CONSTRUCTION but not as a native benchmark. Do not imply complete feasibility proven or claim paper flaw without evidence.

## GCKKS P0-21: exact correctness gate

Original 2026/2600 physical pp24–25 §5.4 Algorithm1/Lemma3, p18 Stage2. Algorithm1 acts independently on RLWE components: reduce to useful cyclotomic component; scale by c_m^-1; zero unused embeddings by CRT lift; coefficientwise round; reinterpret as GCKKS with target factor F, no need for F inverse if F nonunit. Lemma requires **specific unreduced integer-lift smallness**:
  ||b + a s||_2 + ||e F||_∞ < Q/2,
where e is combined rounding error. Then useful new-old difference = c_m e on useful embeddings, and unused new value=eF on unused embeddings. A N=8 nonunit F toy passed under the stated assumption. A second toy where b+as=QX≡0 (mod Q) failed naive unconditional conversion, but VIOLATED lemma's small-lift assumption. NOT a paper bug. Paper p18 balances components mod q then raises to Q >> q and states (in its model) ||I||∞≤15 with overwhelming probability for encapsulated sparse key h=32.
Derived elementary conservative sufficient condition:
   Q/q > 2 sqrt(N)(alpha+K_I) + (1+||s||_1)||F||_1/q
under b+as=m+qI, ||m||∞≤alpha q, ||I||∞≤K_I and independently nearest-rounded CRT components. For N=65536, alpha=1/16, K_I=15, first term =7712 ≈ 12.91 extra bits. This is only a sufficient derivation, NOT verified author parameter. Critically h=32 for overflow distribution cannot automatically be substituted for ||s||_1 of the active conversion key. Need actual F, q, Q, key and noise model before headroom PASS.

## GCKKS P0-22: paper cost ledger / no native claims

Primary 2026/2600:
- usefulSlots = 2N/k.
- precision doubling from k=4 through log2(k/4) splitting rounds (k powers of two).
- source rounds each consume **3** scale-related levels, use joint powers h1(x)=3x²−2x³ BEFORE ciphertext splitting.
- after Step5 five-bit overflow decomposition yields C5 = 5k/2 GCKKS ciphertexts.
- Step6 recombines into k/2 ciphertexts. Step7 collapses via structured partial StC / linear combinations, avoiding some FFT rotations.
- printed upper bound on precision-doubling key switching operations ≤ 15k; NOT 15k distinct eval keys.
- precision-dependent modulus bits O((p/k)log k) and homomorphic operations O(k), with missing constants and no implementation in this version.
At N=2^16, example k=8,16,32,64,128,256:
 k=8: useful=16384, C5=20, levels3, KS upper120
 k=16: 8192, 40, 6,240
 k=32: 4096, 80,9,480
 k=64: 2048,160,12,960
 k=128:1024,320,15,1920
 k=256:512,640,18,3840.
IF C5 outputs are fully materialized as two degree-N ring polynomials in 64-bit RNS representation, one ciphertext per limb = 2N*8 bytes=1 MiB for N=65536; at k=256, 640 MiB per limb, 10 limbs=6.25 GiB, 20 limbs=12.5 GiB. CONDITIONAL materialization ledger, NOT lower bound on optimized PEAK (fusing/streaming/reclaiming memory can reduce) and NOT measured latency. Intermediate-state count per useful slot = 5k²/(4N), a representation ratio not time lower bound.
Paper p15–16 §4.1–4.2 unused-slot normalized noise demands rescale divisor rho >=max(1,r c_e). When converted useful scale is too small, needs extra HomPMult/rescaling OR auxiliary H correction. So O((p/k)log k) asymptotics do not guarantee prime-bit ledger if p/k small; e.g., p=1024,k=256 gives nominal p/k=4 bits (not a plausible stand-alone RNS prime). Need actual scale floor/extra levels and q/Q, F norms and practical parameter sets.
No author bug, no novelty, no native feasibility established.

## Highest-value next H23 (P0-PRESCOUT-23 not begun)

Potential common optimization problem from primary 2026/2600 pp5–6 (§1.3),19–21 (§5.2):
- 2026/2600 shared-power-before-split h1 needs three scale-related levels per iteration.
- According to 2026/2600's SECONDARY description, Cheon–Lee's REVISED ePrint 2026/2531 uses split-before-clean, two levels per iteration, but evaluates cleaning separately; preserves unused slots through a DIFFERENT invariant. Need 2026/2531 first-party paper for full novelty/performance comparison.
H23 candidate: A joint shared-power-before-split construction of h1(x)=3x²−2x³ that consumes only TWO effective scale-dependent levels while retaining GCKKS's F²→F' decryption-factor transition and normalized unused-slot noise invariant; assess if impossible on simple algebra and scale ledger before constructing.
One test: write exact one-round symbolic dataflow on two useful slots and one unused slot with factors F,F²,F'; count (ciphertext product, relinearization, masking, rescale, key switching), check useful output scale vs required rho >=max(1,r ce') and check normalized unused bound. Compare original 3-level GCKKS variant against Focused 2-level split-first under the same conditions if PDF available. Kill immediately if moving masking or rescale unavoidably breaks factor/scale invariant or merely replicates Focused authors. This is a hypothesis not yet proven, not a Codex request. Need classify any gap due to missing Focused PDF as UNCLEAR, not 'novel'.
If H23 source blocked, alternative targeted cheap test: demonstrate feasibility/infeasibility of fusing Step5→6→7 output streaming without changing modular/precision/KS cost, but distinguish ordinary compiler scheduling from publishable cryptographic novelty.

## Prioritization and rules for new session

P1: GCKKS 2600 shared-power 2-level gate with focused prior-art exact source; one smallest falsifiable derivation.
P2: empirical/resource side (not yet authorized): source-specific actual parameter ledger + native memory/performance relative to Dumezy and Focused. Need explicit PI permission for Codex/GPU/native runs.
P3: ALU A2B constrained implementation optimization only if significant end-to-end cost novelty and baseline-matched advantage. Broad constant-bootstrap A2B already solved.
Do not continue dead local FFT/trace/sine noise or generic ALU-window variants.
Before tool use, check current repo state; if provenance absent, re-read supplied PDFs page-by-page. Source locations 2026/2600: p5–6, p7–8, p14–16, p18–25, p26. Two-factor nonunit conversion p24–25. Source names exact path above.
Writing policy: per round [FACT]/[DERIVATION]/[SPECULATION], provenance paper page/lemma/algorithm, separation of formal proof, security, noise, native. No 'PASS_NOVELTY' just because paper lacks code. Update isolated finding only when warranted. Keep shared STATE.md intact until actual read and authorized scoped edit.

## End of handoff

HANDOFF_STATUS: COMPLETE
LATEST_COMPLETED: P0-PRESCOUT-22
NEXT_ITERATION: P0-PRESCOUT-23_NOT_STARTED
RESEARCH_DIRECTION: GCKKS_SHARING_VS_LEVELS_WITH_NORMALIZED_UNUSED_NOISE
CODEX: NOT_RUN; NOT_AUTHORIZED_AUTO
FILES: five 2026 source PDFs confirmed supplied; Focused 2026/2531 and Dumezy 2026/2513 need source access for exact prior-art comparison.
PAPER_BUG: NONE_VERIFIED
NOVELTY: NOT_ESTABLISHED
STATE_UPDATE: YES — NEW_ISOLATED_HANDOFF_LOG_ONLY
OTHER_TRACKS: UNCHANGED
