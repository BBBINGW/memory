# FHE × MPC — Approximate Output Semantics vs UC / Collaborative Sampling

Date: 2026-10-26 | `STAGE: PRESCOUT_FHE_MPC_01` (unofficial; broad FHE scope PI-selected) | `STATUS: FAIL_NAIVE_CROSS_OUTPUT_NOISE_REUSE / SOURCE_GAP_CURRENT_COMPOSITION`.

## Decision and research boundary

**Target problem, not yet a construction:** reduce the *real* multi-party collaborative-smudging-sampling cost while preserving standard simulation security for approximate CKKS, with malicious/semi-malicious partial-decryption transcripts and UC-composable MGHE/OtF-MPC. Do not just attach MPC/ZK to CKKS. Important potential mechanism must be novel versus OT/Discrete-CKKS bit-sharing, PRSS/key-homomorphic PRF, generic UC-MGHE, and modern malicious zk compilers.

**Related preserved idea** (separate workstream): `findings/fhe-zk-hoisted-keyswitch-proof-reuse-engineering-candidate-2026-10-26.md`, committed as PARKED_ENG_CANDIDATE; not a new FHE/MPC hypothesis.

## Evidence and exact provenance

1. Intak Hwang, Yisol Hwang, Miran Kim, Dongwon Lee, Yongsoo Song, `ePrint 2025/395` **Provably Secure Approximate Computation Protocols from CKKS** (2025 title), later author blog titled **On the (In)security of Approximate Computation Protocols from CKKS** (2026-06-15). https://eprint.iacr.org/2025/395 and https://ckks.org/blog/2026/Insecurity-ckks-protocol/ . Full current PDF unavailable to Research MCP as of this date (ePrint HTTP403, alternative title mismatch). **Source evidence level: AUTHOR_BLOG and indexed public abstracts, not full-source algorithm audit.** The author states independently chosen smudging by parties fails standard simulation security when the corrupted party knows its noise share; collaborative sampling makes the *total* noise e jointly sampled and shares hidden. Their two-party protocol uses OT; multi-party random-bit-sharing uses discrete CKKS bootstrapping + cleaning and pairwise PRF zero-share masking.
2. Author's 2026 benchmark (same blog), single-thread 2^16 bit shares: two party 0.12 s vs multi-party 33.96 s; 2^18 shares: 0.41 vs 135.84 s. **Caveat:** 2-party and multi-party are different mechanisms; multi-party experiment only implemented bootstrapping+cleaning part, NOT full cost, not an apples-to-apples speedup comparison. Shows concrete bottleneck candidate, not dominance within all MPC.
3. Ganyuan Cao, Sylvain Chatel, Christian Knabenhans, `ePrint 2025/1845`, **HE-based On-the-Fly MPC, Revisited: Universal Composability, Approximate and Imperfect Computation, Circuit Privacy**, 2026 ASIACRYPT publication page https://s-chtl.github.io/publication/ucmhe/. Full 61-page PDF obtained via `get_eprint_paper` from a GitHub mirror, sha256 `191dc8e8f15c4cd90bcefa5c6c42429dd8211aff76e65c3e6059292046611c47`, source `arturo-kong/IACR-eprint-mirror 2025/1845.pdf`, **VERSION_UNVERIFIED** (do not silently treat as latest September 2026). Physical p5 Theorem 1: `IND-CPApD + IND-CIRC + SIM-PDEC + Rob` sufficient for semi-malicious UC MGHE. Physical p16 Remark 1: `IND-CPA + SIM-PDEC` insufficient; bootstrapping failure attack can survive smudging. Physical p22 **Remark 2**: approximate extension by explicit error tracking aligns with **liberal security**; for standard security cite Hwang et al's mechanism fixing total error and distributing shares. Physical pp23-28: malicious OtF-MPC compilers with `REnc/REval/RDec` ZK/NIZK. 2026 author homepage additionally announces split-witness NIZK enhancement not present in older inspected PDF; must get current revision before source-level novelty claim.
4. For CGS lesson: `findings/cgs-52-shifted-gram-hybrid-leakage-gate.md` demonstrated dangers of multiple correlated secret-conditioned hints in a **stronger** game, not attack on original. This is a methodological warning when exposing collaborative-sampling transcripts, not evidence that Hwang's scheme is broken.

## One smallest hypothesis and one decisive cheap test

**H_NAIVE_REUSE**: An expensive collaborative smudging sample e can be *reused without refreshing* in two otherwise identical independent approximate outputs, reducing bit-sharing generation cost without changing the standard ideal output distribution.

[DERIVATION / COUNTEREXAMPLE, source-independent conditional model]
Assume ideal functionality samples independent e1,e2 uniformly from finite noise alphabet S with |S|=M, and computes identical deterministic plaintext value m twice. Under desired ideal execution, z1=m+e1, z2=m+e2, so Pr[z1=z2]=1/M. If candidate reuses exactly the same e, z1=z2 always. The public distinguisher T=[z1=z2] has advantage 1-1/M. For nonuniform D, ideal equality probability Σ_x Pr_D[x]^2, while shared e still equality 1; advantage 1-Σ p_x². Thus **reuse-one-total-error across independent calls does NOT implement the fresh-sampling functionality.** If additional intrinsic random CKKS noise exists the equality test must be adapted; this restricted model is NOT a universal no-go theorem for every CKKS transcript. Deriving *fresh pseudorandom independent outputs from properly protected seeds* is not excluded; PRSS/PRF-related prior art and malicious-abort/security must be audited.

Status `FAIL_NAIVE_REUSE`. Test was paper/math derivation only, **no executable code, full protocol proof or timing benchmark**.

## Constructive interpretation / important next discriminator

Do not attempt a generic UC wrapper around Hwang's protocol and claim novelty: the prior art already gives UC MGHE compilers and standard-security collaborative sampling separately. The key research challenge is a jointly compatible *sampling-and-decryption interface* under malicious/nonadaptive corruption, where:
- simulator can explain only adversary shares/transcripts **from designated approximate output** without exact plaintext;
- per-evaluation total error has the specified fresh distribution even after partial decryption / abort / multiple evaluations;
- key shares, RNS/modulus, noise tail, coefficient lifting and public ZK statements compose with `IND-CPApD, SIM-PDEC, IND-CIRC, Rob`;
- online cost/rounds/communication beat actual baseline at matched security and no hidden trusted dealer/key-dependent setup.

**NEXT single preflight:** obtain/version-check 2026 Cao et al full final source and the 2025/395 full PDF, then assess *whether* latest formal malicious UC theorem already realizes standard approximate total-error shares in multi-group dynamic setting. If it does, **kill generic composition novelty** and only investigate a specific quantified unoptimized sampler; if not, propose one typed ideal functionality and minimum attack/game before building anything. In the meantime `SOURCE_GAP_VERSION`, not a claim the interface is an established open problem.

`STATUS: FAIL_NAIVE_REUSE / CONTINUE_SOURCE_GATE`
`EVIDENCE: AUTHOR_BLOG + VERSION_UNVERIFIED_SOURCE_PDF + DERIVED_COUNTEREXAMPLE`
`NOVELTY: UNVERIFIED; NO_NEW_PRIMITIVE`
`CODEX: NOT_RUN`
`STATE_UPDATE: THIS_PRESCOUT_NOTE_ONLY; NO_OFFICIAL_TRACK_ITERATION_OR_ROOT_STATE_CHANGE`
