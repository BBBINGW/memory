# MKFHE Levis 2026/2263 — Extension-free novelty exclusion, critical full-text source blocked

Date: 2026-10-14, Asia/Tokyo. Independent MKFHE **second preselection** after `findings/mkfhe-mps-2026-322-extension-operation-count-screen.md`. This is NOT the shared global general I193, does NOT supersede concurrent independent vFHE V21 or SHIP I226. Read before write: `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, global `STATE.md` (vFHE, read-only), `findings/ship-memory-STATE.md` (I226, read-only), prior MPS finding (SHA d39a69e92dba56022267ce52f5b3debcff3fe232), `MISSING_SOURCES.md`.

## ONE primary hypothesis and cheapest decisive test

**H-L02 [FALSIFIABLE NOVELTY CLAIM]:** Eliminating the `O(d k²)` cGSW-to-joint-key RGSW extension of Min–Park–Song (MPS), CRYPTO2026/ePrint2026/322, remains an unaddressed standalone general innovation: there is no publicly disclosed plain-model RLWE multi-key FHE construction claiming this exact extension-free functionality.

**Falsifier:** Identify one named primary subsequent construction that *explicitly* claims to eliminate MPS's `O(dk²)` extension, not just reduce its constant; audit original paper abstract and retrieval provenance. Full construction/security proof comparison is a SEPARATE source-gated step, not something this abstract alone can establish.

## Primary publication evidence and access boundaries

**Baseline:** Seonhong Min, Jeongeun Park, Yongsoo Song, *Multi-key Fully Homomorphic Encryption with Non-Interactive Setup in the Plain Model*, CRYPTO 2026, ePrint **2026/322**. Verified full Research MCP mirror 41 physical pages PDF SHA256 `bd9bd6793f585e04602262426f4336e01760031ebf673c98852a0212ed6299cc`, `VERSION_UNVERIFIED`. Original physical p17 Algorithm 1 cGSW→RGSW extension and p16 O(k²) one-input gadget operation count. Previous independent counting obtained one input-owner idx `d(k(k+1)/2+idx-1)` gadget invocations, all k owners `d(k³+2k²-k)/2`; no MPS source error established.

**Direct successor:** Baoyu Li, Binwu Xiang, Kang Yang, *Levis: Extension-Free Multi-Key Fully Homomorphic Encryption in the Plain Model*, ePrint **2026/2263**, listed with update date **2026-09-29** in independent Cryptology ePrint archive mirror `https://eprint.iacr.asia/2026?offset=100` and authors' selected publications `https://yangkang2048.github.io/collection-archive/`. **Only the public title+author+ABSTRACT were reliably obtained.** The original PDF remains MISSING.

**Exact public-abstract claims [FACT ABOUT WHAT AUTHORS CLAIM, NOT INDEPENDENTLY PROVED]:**
- Levis describes MPS extension as `O(dk²)` gadget products **per input**, for k parties and gadget length d.
- **Levis-fast** claims to eliminate this prior joint-key ciphertext extension before homomorphic evaluation, under the plain model.
- Its core *Cofactor Compatibility* technique claims a **common projective decryption relation** among ciphertexts encrypted under independently generated local keys, allowing direct evaluation.
- **Levis-small** claims to reduce *fresh ciphertext communication* from `O(dk²)` to `O(d)` ring elements using a **lightweight lifting operation**. Do not treat "extension-free" as proof that **every** key/communication/online lifting cost is eliminated, or confuse Levis-fast with Levis-small.
- Authors' abstract reports proof-of-concept evaluation speedups (versus MPS) for k=2/4/8: Levis-fast **67.7×/52.8×/139.4×**; Levis-small **11.8×/19.7×/54.4×** and communication reduction **2.5×/8.7×/14.2×**. **These are UNVERIFIED author-reported numbers**, not reproducible independent benchmarking or necessarily matched all-security parameters.

**Access attempts and exact limitations [FACT]:**
1. Research MCP `get_eprint_paper("2026/2263")` returned `RETRIEVAL_BLOCKED` (IACR primary PDF HTTP403, no exact-title-author-matched arXiv result, fixed GitHub ePrint mirror missing `2026/2263.pdf`).
2. Web attempted `https://eprint.iacr.org/2026/2263.pdf`, `https://eprint.iacr.asia/2026/2263.pdf` and mirror paper landing page: no accessible parseable PDF; author website lists a download link but no independent authenticated PDF retrieved from it.
3. Targeted title + PDF + Cofactor Compatibility + author searches, public GitHub repository searches for Levis and exact technique: no verified accessible full preprint, code or theorem source. Failure to find a public repository is NOT evidence none exists.
4. Consequently **no access** to the **formal Cofactor Compatibility definition/equations**, key-generation assumptions, ciphertext/matrix layout, security proof, noise/multiplicative growth, exact lightweight lifting algorithm, benchmark settings or actual code. **No formal comparison of security/noise/parameter tradeoffs is possible.** Prior MPS full text cannot substitute for Levis source.

## One decisive result and interpretation

**H-L02 FAILS at the novelty-screen level**: a dated paper by named authors expressly claims to solve the same *general* MPS extension-elimination task in a plain-model construction. Therefore our own “remove MPS O(dk²) extension” would require material technical differentiation; presenting that high-level idea as undiscovered or as a novel contribution is untenable.

**This is NOT a theorem-level independent reproduction** of Levis-fast or its Cofactor Compatibility security claims and does not establish that the same solution covers every MKFHE architecture/assumption, or that Levis is secure/correct. The larger technical hypothesis of *where Levis shifts cost* is SOURCE_BLOCKED and remains UNCLEAR; do NOT infer it must trade against noise, key size, or assumption merely because of “projective” terminology.

## End of iteration

**STATUS:** **FAIL H-L02** standalone novelty of generic extension-free MPS; **PASS reliable abstract-level prior-art scope and two-variant distinction**; **SOURCE_BLOCKED/HUMAN_REVIEW** precise mechanism/security/performance.
**RESULT:** Levis-fast publicly claims no MPS-style pre-extension; Levis-small publicly claims O(d) ciphertext communication with lightweight lifting. Exact algebra/security/cost are unknown because full PDF unavailable. No newly identified original-paper defect, cryptanalytic break, fresh publishable algorithm or benchmark.
**NEXT_ACTION:** An authorized full PDF or author-provided code for Levis 2026/2263 is a **prerequisite**. If supplied, inspect exact Cofactor Compatibility definition, its compatibility proof, ciphertext-space dimensions and security game, and side-by-side MPS Algorithm1 cost, one smallest falsifiable limitation only. Otherwise **PARK MKFHE extension-removal as presently overtaken/blocked**; user PI selects any fresh unrelated FHE parent or approves source acquisition. Don't iteratively repeat public abstract findings.
**STATE_UPDATE:** This scoped finding + MISSING_SOURCES entry only. **No edits** to concurrent global `STATE.md`, independent `findings/ship-memory-STATE.md`, `OPEN_RESEARCH_BRANCHES.md`, or source repos. **NOVELTY NOT VERIFIED** for any alternative idea.
