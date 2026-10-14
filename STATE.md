# FHE Research State — Independent SHIP-M01 (2026-10-14)

**ACTIVE PARENT / PI-SELECTED:** SHIP evaluation-key **resident prepared memory**, Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint **2025/784**, https://eprint.iacr.org/2025/784.
**ACTIVE SEQUENCE:** **SHIP-M01 COMPLETED**; **SHIP-M02 NOT STARTED**. This uses its **own per-round files**, NOT global old I194 numbering.
**STATUS:** SHIP-M01 narrow **algebraic PASS** / real CKKS key-switch feasibility, full-bootstrapping noise/latency/peak RAM **UNCLEAR**; **NOVELTY NOT VERIFIED**. Await PI confirmation before M02. No author contact/public disclosure.

## CURRENT QUESTION

Can the `4hθ` source-form SHIP encrypted column-selector mask **prepared left operands** be compressed while retaining encrypted support/sign secrecy, low depth and competitive 32-core latency (not only reducing persistent serialized key size)?

## RECENT COMPLETED RESULT — SHIP-M01

**[FACT/source]** Source §3.3 Lemma1, §4.4 Eqs.(7)/(8) & Algorithm4 use four **real-valued** masks for each hybrid column candidate; the actual implementation reverses column/mux stage. Independently pinned Poulpy `250d4392656cd313f92ca66d96d8865702d39ddf` holds all **4hθ** rank-1 `CKKSCiphertext` masks and prepares separate two-column `CnvPVecL` for each; a dense-secret conjugation key already exists. Original HEaaN peak memory unmeasured. Full ePrint mirror 33pp SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, VERSION_UNVERIFIED.

**[DERIVED + EXACT TOY]** Proposed **Complex-Paired Selector Packing**, for private REAL mask values M1,M2 encrypt ONE `C=Enc(M1+iM2)`; given arbitrary public complex P1,P2,
`F=M1 P1+M2 P2=(C(P1−iP2)+Conj(C(conj(P1)−i conj(P2))))/2` in ideal slot semantics. Aggregate all pairs before **one ciphertext conjugation per masking accumulator**. Deterministic source-mask-replica checked **256** legal secret/half configurations ×8 slots=**2048** comparisons, max floating error 2.29e−16. If unchanged encrypted rank/limbs hold, per support prepared selector count **4θ→2θ (50% fewer)**; ciphertext-plaintext term count remains 4θ, with 2 accumulators, extra transform/normalization, and ~one **costly conjugation/key-switch per support/half**. It does not evade KDM/noise/modulus/security obligations or establish full-system speed/memory savings. Generic complex packing already known, novelty NOT established.

**Detail:** `findings/ship-memory-M01-complex-paired-selector-key-gate.md`. Local exact toy file (LOCAL ONLY) `/mnt/data/ship_m01_complex_pair_toy.py`, SHA256 `ae932f5b7a6b9fef7c37d19c847a4832566029a1582cb97db0f7d661e0576af8`.

**PAST NEGATIVE GATES:** SHIP I171–I174 records in `findings/ship-*-iteration17{1,2,3,4}.md` (see exact filenames in M01), especially seeded persistent compression NOT prepared-memory reduction (I173), and direct per-candidate public-four-mask identity FAIL (I174); do not repeat.

## NEXT_ACTION — SHIP-M02 ONLY AFTER PI CONTINUE

**ONE decisive source-level CKKS feasibility gate:** pinned Poulpy implementation — check the dense-key conjugation eval-key's actual supported modulus/precision and the `ship_masking_accumulate` accumulator `raised_k`/scale against candidate split U,V and required rescale. Implement/test **one** minimal rank-1 CKKS convolution+conjugation with nontrivial complex public P1,P2 to measure whether packed reconstruction works at the relevant level with acceptable error; first kill it if extra key-switch/level/noise is structurally prohibitive. Do NOT start a separate hypothesis, full benchmark, or another parent.

## FROZEN PREVIOUS PARENT — vFHE I193 (NOT MERGED)

**vFHE I193 COMPLETED, I194 NOT STARTED**; previous primary target (Cascudo et al. ePrint 2025/286, CRT cross-component same-integer lookup repair) is **PARKED by PI's switch to SHIP**; there was a bounded-integer EA toy code PASS but scalable field-code distance/security/PCS OPEN. Its complete prior authoritative `STATE.md` is archived **verbatim** in:
`logs/vfhe-state-2026-10-14-post-I193-pre-SHIP-M01.md` (source blob SHA `de08a0d82d905de5d386c7902022828f30a5cf6b`).
Primary I193 derivation stays in `findings/vfhe-shared-integer-ea-column-bridge-iteration193.md`; original gap in `findings/vfhe-crt-lookup-cross-component-soundness.md` and `findings/vfhe-crt-full-range-piop-and-commitment-audit.md`. Preserve its existing next source-sized EA distance gate **only if PI explicitly reopens vFHE**. No SHIP result belongs to I193.

Rules: AGENT.md one primary hypothesis + one decisive minimal test per authorized round; read before write, explicit evidence provenance, one independent SHIP-MNN file per round, no auto-pivot, no unverified novelty/security/performance claims.