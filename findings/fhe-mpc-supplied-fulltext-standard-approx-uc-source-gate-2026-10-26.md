# FHE × MPC — Full Supplied-Source Check: Standard-Approximate CKKS × UC-MGHE

Date: 2026-10-26 | `PRESCOUT_FHE_MPC_03` | PI-supplied two full PDFs | **not a formal CGS/BOOT/SHIP iteration**.

## Recovery and exact provenance

Two primary texts were placed in `papers/supplied/` by PI. Both opened with page-aware GitHub Notes PDF reader on 2026-10-26:
- `papers/supplied/2025-395.pdf`, Git blob `84710edb51998a1c9d50a8c306ec1970d8d389f5`, **35 physical pages**. Paper cover: **On the (In)security of Approximate Computation Protocols from CKKS**, Intak Hwang, Yisol Hwang, Miran Kim, Dongwon Lee, Yongsoo Song. Physical pages 1–3,5–7,9–17,29–31, etc. legible. Source is author-topic matching; independently authenticated byte identity against IACR official current PDF is NOT verified. Repo URL: https://github.com/BBBINGW/memory/blob/main/papers/supplied/2025-395.pdf
- `papers/supplied/2025-1845.pdf`, Git blob `754d6ed681195e39488cc30175ba0f14ae5ff043`, **62 physical pages**. Cover: **HE-based On-the-Fly MPC, Revisited: Universal Composability, Approximate and Imperfect Computation, Circuit Privacy**, Ganyuan Cao, Sylvain Chatel, Christian Knabenhans; explicitly contains **split-witness NIZK** (physical pp1,24–28), unlike an older 61pp mirror. Physical pp1–11,15–22,24–30, etc. legible. Official-origin byte parity/version date NOT independently authenticated. Repo URL: https://github.com/BBBINGW/memory/blob/main/papers/supplied/2025-1845.pdf
- IACR ePrint IDs and landing pages https://eprint.iacr.org/2025/395 and https://eprint.iacr.org/2025/1845.
- `MISSING_SOURCES.md` updated separately to mark **SUPPLIED_READABLE** with residual official version authentication caveat.

## ONE primary hypothesis and decisive test

`H_DIRECT_COMPAT:` Hwang's proved standard approximate MPC with collaborative sampling **already directly instantiates** the strong malicious/UC MGHE-based OtF-MPC compiler of Cao *without new adversarial-model, oracle or ideal-functionality assumptions*.

**Falsifier:** Verify that the source Hwang theorem and ideal functionality themselves cover the same adversarial behaviors required as inputs to Cao's full malicious-UC construction: at minimum honest-but-adversarially chosen randomness, share tampering, key/ciphertext/partial-decrypt oracles, online extraction/split witnesses, and output function semantics.

**RESULT: FAIL_DIRECT_COMPATIBILITY_CLAIM** (missing hypotheses, not an insecurity or impossibility theorem).

### Detailed source-grounded comparison

**Hwang 2025/395:**
- Physical p7, Definition 3 defines standard simulation security for **semi-honest** adversaries: joint distribution of simulated corrupt-party view and **probabilistic ideal output** must match real-world view and output.
- pp15–16, Figs 8–10, Theorem 3: `Fn-ColSamp` picks `e←D` and uniformly additive-shares it in `Rq_out`; `FNewMPC` outputs `z=C(x1,...,xn)+e`. Theorem 3 assumes ThCKKS IND-CPA, E-smudging D and a **Fn-ColSamp-hybrid**. It does NOT prove malicious/UC realization of the ColSamp *implementation*.
- pp16–17, §4.3 and Fig11: real multi-party bit-sharing via Discrete CKKS encrypted bit contributions, `BinBoot`, `Clean`, distributed decryption and pairwise PRF zero-share masking. This is not a general malicious, adaptive-coins, robust UC-security theorem. Authors explicitly report only bootstrapping/cleaning implemented: `2^16` bit shares = 33.96 sec, `2^18` = 135.84 sec on stated CPU; benchmark not full end-to-end malicious MPC.
- pp29–30, Appendix D, Fig15–17 & **Theorem 7**: t-out-of-n setting picks participating set `T`, then realizes `FThColSamp` with a corresponding **t-out-of-t** bit-sharing once `T` is determined. Theorem7 is still standard *semi-honest* security in `FThColSamp`-hybrid. This is not a publicly substantiated asynchronous, malicious, dynamic-group, offline subset-independent sampler.

**Cao 2025/1845 (62pp):**
- Physical pp7–10, Fig1 `FMGHE`: models dynamic groups, stores plaintext/ciphertext with error values, allows decryption-shares and corrupted party views, explicit adversarial coins. Physical p8: **semi-malicious can choose arbitrary protocol randomness**; author notes proving coins syntactically bounded does not prove distributional honesty; clients non-adaptively corrupted, possibly server corrupted.
- Physical p17 `Theorem 1`: if **both clients and server corrupted**, needs `IND-CPApD`, `Rob`, `SIM-PDEC` under conditions (NOT `IND-CIRC` in this corruption case).
- Physical p18 `Theorem 2`: **uncorrupted server** case additionally calls for `IND-CIRC` for server-side privacy. Clarification: prior prescout erroneously summarized all four as simply Theorem1 premise; actual splitting must be preserved.
- Physical p21–22: `FOtF-MPC` approximate error tracking is described as aligning with **liberal approximation security**; explicitly refers to Hwang et al. for standard fixed-total-error shares. This is a semantic difference, not a proof that standard UC composition is impossible.
- Physical pp24–28: the **new supplied source DOES include split-witness functionality** `FNIZK`, with knowledge witness w, existential w*, Naor–Yung double encryption/rounds and malicious UC OtF-MPC Theorem5. §3.4.1 physical p26 **leaves a formal realization theorem for the split-witness functionality from any-simulation-sound NIZK to future work**; the ideal-hybrid UC theorem does not by itself instantiate all concrete proof components.
- Physical p28: authors analyze approximate outputs `m+δ1` and `m+δ2`, accepted within `Estimate(·)`, explicitly referencing indistinguishability of `m+δ` with **liberal** semantics. It does not present a separate standard-approximate-CKKS `Fn-ColSamp` to `FMGHE` realization theorem.

**Conclusion:** There is an **accurately typed interface mismatch / unverified proof obligations**:
1. honest semi-honest error shares + hybrid-model theorem **≠** maliciously generated correctly distributed shares;
2. n-out-of-n or after-T-selection t-out-of-t sampling **≠** free dynamic-group subset-independent preprocessing;
3. standard `z=f(x)+e` with globally sampled fresh `e` **≠** automatically Cao's tracked `m+δ` (liberal) or dual-session `m+δ1,m+δ2`;
4. malicious-UC theorem additionally needs actual `IND-CPApD / SIM-PDEC / Rob / (uncorrupted server: IND-CIRC)`, and corresponding valid proof-system instantiation.

This is NOT an attack on either published construction, nor proof they cannot be composed with extra work. It is NOT a novelty claim; the exact missing instantiation may have generic or specific prior art.

## Leading research candidate from precise sources (NOT a proven gap)

`CANDIDATE:` Online/on-demand **committee-flexible threshold collaborative bit-sharing** for CKKS standard simulation security with stronger malicious/UC-compatible partial-decryption interfaces. The specific baseline: Hwang Appendix D once-`T`-chosen `t`-out-of-`t` sampler using expensive Discrete-CKKS BinBoot+Clean, contrasted against Cao's dynamic group and strong randomness/decryption security. Seek a new *linking invariant* preserving a fresh global small error e per output and simulatability of every proper corrupt share subset, while enforcing malicious consistency and avoiding exponential pre-computation over all T. This remains **PRIOR_ART_PENDING**, including PRSS/PCF, UC-threshold protocols, asynchronous key-homomorphic PRF and existing correlated random bit sharing (notably our separate CGS52 failures). No proposed construction, no measured improvement.

**NEXT TEST (one primary):** read specific prior art already cited by Hwang §4.3 and Appendix D — [Dahl et al.] generic shared random bits, Discrete CKKS [49], and the 2026 synchronized-decryptor/async-CKKS PRSS approaches — then determine whether a constant-round subset-independent maliciously secure random-bit-share generator already exists at lower complete online cost. If prior art already gives it, kill the naive novelty. If the source-defined gap remains, propose ONE joint share-distribution/commitment invariant and the cheapest counterexample. No Codex or server until permitted and warranted.

## End of iteration

`STATUS: FAIL_DIRECT_COMPAT_CLAIM / PASS_PDF_RECOVERY / NEW_CANDIDATE_NOVELTY_UNVERIFIED`
`EVIDENCE: SOURCE_VERIFIED_GITHUB_TEXT + DERIVATION; NATIVE_NOT_RUN`
`NEXT_TEST: PRSS + malicious bit-sharing closest prior art for post-selected T`
`STATE_UPDATE: MISSING_SOURCES and this finding ONLY; no root STATE or existing active-series override`.
