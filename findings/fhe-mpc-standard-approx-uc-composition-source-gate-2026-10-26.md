# FHE × MPC — Standard Approximate CKKS vs UC-MGHE Compatibility Gate

Date: 2026-10-26 | stage: `PRESCOUT_FHE_MPC_02`, **not an official numbered CGS/BOOT/SHIP iteration**. PI selected broad FHE/FHE × ZK/MPC research and PI previously approved retaining the separate hoisted-KeySwitch proof CSE engineering candidate. Parent: `findings/fhe-mpc-uc-approximate-collaborative-sampling-prescout-2026-10-26.md`.

## ONE primary hypothesis and falsifier

**H_DIRECT:** The existing Hwang et al. standard-simulation-secure approximate CKKS collaborative-sampling guarantee can be treated **by itself** as sufficient to instantiate the malicious UC OtF-MPC/MGHE compiler proved by Cao–Chatel–Knabenhans, without separately establishing the underlying MGHE requirements.

**Decisive source/theorem-applicability test:** Compare the explicit stated premises of Cao's UC MGHE theorem with the explicit security target and mechanism of Hwang. Any unestablished required premise falsifies the claim that an immediate theorem instantiation has already been proved. It does **not** show incompatibility, practical insecurity, impossibility or an open research problem in the latest revision.

**Result: `FAIL_DIRECT_THEOREM_APPLICABILITY / COMPOSITION_NOT_YET_CERTIFIED`**. The sufficient theorem requires a conjunction, whereas the Hwang author's public description is targeted at standard approximate simulation security and distributed noise shares. No verified source establishes all premises for their particular collaborative-sampling MGHE realization. This is a missing proof obligation, **not** a new counterexample or an attack. It is not justified to claim either existing complete integration or its nonexistence.

## Sources and version boundaries

1. **Hwang, Hwang, Kim, Lee, Song**, ePrint 2025/395, current title **On the (In)security of Approximate Computation Protocols from CKKS**; accepted ASIACRYPT 2026 per Seoul National University Crypto & Privacy Lab publication list `https://crypto.snu.ac.kr/publications` and university public notice. Original earlier ePrint title **Provably Secure Approximate Computation Protocols from CKKS**. Author **Dongwon Lee** technical blog dated 2026-06-15: `https://ckks.org/blog/2026/Insecurity-ckks-protocol/`. Blog gives the simulation separation, collaboration sampling and 2-party OT / multi-party Discrete-CKKS bootstrapping/cleaning + pairwise PRF masking, without being equivalent to the full current proof. **Full current paper PDF SOURCE_BLOCKED** to research MCP: ePrint official HTTP403, alternate arxiv exact title not found, source mirror identity mismatch. The web search index contains an old-PDF text excerpt but no readable/authenticated current PDF source. Do not represent this as verified current Theorems.
2. **Cao, Chatel, Knabenhans**, ePrint 2025/1845, **HE-based On-the-Fly MPC, Revisited**, ASIACRYPT 2026 as shown on `https://s-chtl.github.io/publication/ucmhe/` (September 2026). Earlier PDF **AVAILABLE BUT VERSION_UNVERIFIED**: 61 physical pages, SHA256 `191dc8e8f15c4cd90bcefa5c6c42429dd8211aff76e65c3e6059292046611c47`, mirror `arturo-kong/IACR-eprint-mirror`, readable via research MCP `read_eprint_pages` for 2025/1845. Physical p5 Theorem 1 (informal): `IND-CPApD + IND-CIRC + SIM-PDEC + Rob` imply semi-malicious UC MGHE; pp25–28 malicious OtF-MPC NIZK/zkSNARK compilers; p16 Remark1 `IND-CPA + SIM-PDEC` does **NOT** imply IND-CPApD, and smudging alone does not cure all failure-channel issues; **p22 Remark2**: error-tracking approximate OtF-MPC naturally aligns with *liberal* approximation security, and refers to Hwang's pre-fixed total-error random shares for *standard* security. The author's **September 2026 current abstract** explicitly claims a split-witness NIZK formalism not present in the text we analyzed. Since its PDF link goes to the same ePrint landing, final theorem-level coverage remains VERSION_UNVERIFIED.
3. The two papers are **both ASIACRYPT 2026**, not an old-versus-new temporal gap. Title/venue confirmation is NOT the same as a proof of a specific functional composition. Sources: `https://crypto.snu.ac.kr/publications`; `https://s-chtl.github.io/publication/ucmhe/`.

## Compatibility matrix — evidence, not guesses

| Layer | Existing known contribution | Condition to instantiate both safely | Status |
| --- | --- | --- | --- |
| Approximate output distribution | Hwang author technical blog: `e` jointly sampled, party shares obscure total, standard simulation vs liberal | EXACT conditional output law per evaluation and correct adversarial view in **each** corruption configuration | AUTHOR_CLAIM; full latest simulator not audited |
| Client privacy under malformed/partially decrypted ciphertext | Cao Definition 2 `IND-CPApD` and Theorem 1 | Show proposed MGHE instantiation satisfies this game, not only IND-CPA or standard honest decryption | NOT_ESTABLISHED; cannot conclude failure |
| Server/circuit privacy | Cao `IND-CIRC` | Show masking, randomness, public key configurations and corrupted server views fit game | NOT_ESTABLISHED |
| Threshold share privacy | Cao `SIM-PDEC` | Simulator for partial decryptions given permitted information and corrupted key shares/transcripts | NOT_ESTABLISHED for concrete Hwang cross-MGHE construction |
| Robustness & correctness | Cao `Rob`, including evaluated ciphertexts, adversarial randomness, malformed shares | Distribution and bounded error preserved under abort, malformed shares, threshold reconstruction | NOT_ESTABLISHED |
| Fully malicious UC composition | Cao malicious compilers `REnc,REval,RDec` with NIZK/SNARK and global setup | Demonstrate consistency of sampler transcript, proof statements, rounds, setup, key relations; account for newest split-witness idea | VERSION_BLOCKED at source-specific level |
| Efficiency | Hwang blog 2^16-bit multiparty batch 33.96s; 2^18 135.84s (1-thread) | Comparable complete online latency, interaction, memory and preprocessing at same adversary/security/precision | NEEDS_MEASUREMENT; published figures are partial bootstrapping+cleaning subpath |

## Technical warning — what not to claim

Cao's earlier Remark2 is **not** a theorem that standard-security composition is impossible. It records a distinction between error-tracking liberal semantics and Hwang's standard semantics. Its `IND-CPApD+IND-CIRC+SIM-PDEC+Rob` framework may be strong enough if a candidate satisfies all its conditions; the present gap is one of **instantiation/proof provenance**. Nor does Hwang's standalone standard simulation claim by itself establish those four MGHE properties. Avoid 'combine existing two papers = a new construction'. No new theorem, noise scheme, protocol or exploit is claimed.

**Never replace the paper's author-provided complete protocol with a toy adversary: if latest source unavailable, at most ONE independent necessary-condition test, then SOURCE_BLOCKED.** Prior prescout already tested repeated reuse of the *same* total error and correctly killed that naive proposal in a restricted fresh-output ideal model. Do not repeat or generalize that into a no-go theorem.

## Research decision and priority

`STATUS: FAIL_DIRECT_THEOREM_APPLICABILITY / SOURCE_BLOCKED_FOR_LATEST_COMPOSITION`
`EVIDENCE: AUTHOR_BLOG + UNVERIFIED_VERSION_FULL_TEXT + SOURCE_THEOREM_PREMISE_COMPARISON`
`NOVELTY: NO_CONSTRUCTION_PROPOSED; OPEN_GAP_NOT_CERTIFIED`
`DECISION: PARK generic Hwang+Cao UC composition claims until the current PDFs/algorithms are obtained; DO NOT loop abstract toy lemmas.`

**Highest-ROI next source gate** (only upon valid primary sources): extract Hwang current precise corruption model, sampling ideal functionality and malicious/abort guarantees; extract Cao latest full `FMGHE` functionality + Theorems/Remark and split-witness assumptions; determine whether one full source already closes standard-semantics UC composition. If yes, only investigate quantified sampler backend. If not, propose ONE explicit missing game/interface (not a paper-level fusion).

**Source requests:** original current PDFs of ePrint 2025/395 (2026 title) and ePrint 2025/1845 (September 2026 accepted version). See `MISSING_SOURCES.md`; no author contact, no Codex, no native/GPU, no official iteration nor root `STATE.md` changes authorized.
