# Iteration 121 — Bounded-gap sparse keys: exactly-one-per-block is a known structural fix, not a same-assumption drop-in

Date: 2026-10-12. PI authorized continuing I120. ONE primary hypothesis and ONE cheapest decisive source-anchored construction/prior-art test. Do not reopen archived sparse-SAB terminal-sign issue I110–111; no code implementation, attack, or external disclosure.

## Primary sources and evidence
1. Antonio Guimarães and Hilder V. L. Pereira, *Fast amortized bootstrapping with small keys and polynomial noise overhead*, CCS 2025, IACR ePrint **2025/686**, full 34 physical pages from Research MCP fixed GitHub mirror, SHA256 `84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335`, VERSION_UNVERIFIED. §6.1–6.2 physical pp21–22: SAB amortized external-product count `O(h log B)`; reject uniformly sampled sparse keys whose **interior** nonzero-position gaps are not <B, tracking the conditional security loss δ; Appendix C pp33–34 gives finite empirical rejection probabilities.
2. Changmin Lee, Seonhong Min, Jinyeong Seo, Yongsoo Song, *Faster TFHE Bootstrapping with Block Binary Keys*, ASIACCS 2023, IACR ePrint **2023/958**, full 19 physical pages via Research MCP GitHub mirror, SHA256 `0ab8c83d5aebbbf0185e200c7c3aab10150aa4e3bad0470a839246d33954e6de`, VERSION_UNVERIFIED. §3 physical p6 defines B_{L,h}: independent blocks with **at most one** nonzero (zero vector allowed), total (L+1) equiprobable block values; pp6–9 analyze a different structured-secret LWE/T(R)LWE setting (conditional proof and concrete attack estimates), not a general same-distribution RLWE transfer theorem.
3. Jean-Sébastien Coron and Robin Köstler, *Low-Latency Bootstrapping for CKKS using Roots of Unity*, IACR ePrint **2025/651**, full 42 physical pages via Research MCP GitHub mirror, SHA256 `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6`, VERSION_UNVERIFIED. §4.3 physical p15 **explicitly uses exactly one 1 per block** in h blocks of length L=N/h; §4.5 pp18–19 carries separate concrete LWE/security estimator reasoning and credits LMSS23. Thus the exact-one block distribution/idea is already prior art.
Primary sources obtained and read through connected Research MCP. No claims about latest official versions beyond available mirror.

## ONE technical hypothesis / decisive falsifier
[HYPOTHESIS] Existing block-binary sparse-secret methods provide a **drop-in, security-preserving, substantively new** solution to the I120 bounded-gap rejection-sampling problem in FAB, without changing its original uniformly sampled fixed-weight secret assumption.

[FALSIFIER / ONE TEST] Read original block-secret definitions and compare their support distributions algebraically to the uniform fixed-h support and the strict interior-gap bound needed by FAB. If a prior paper already uses exactly one selector per block, while conditioning a uniform h-sparse key to that event costs exponential probability mass, the asserted novel, same-assumption drop-in solution is falsified.

## Source-grounded derivation
[DERIVED] Let n=hL and divide indices into h contiguous blocks of size L. Directly sample one uniformly random index U_b in each block, and set j_b=bL+U_b. For consecutive selected positions,
  j_{b+1}-j_b = L+U_{b+1}-U_b ∈ [1,2L−1].
Taking B=2L=2n/h satisfies FAB's strict **interior** gap bound deterministically; direct KeyGen takes O(h) draws, no rejection. The support is exactly L^h binary vectors (one 1 in each block). This is ALREADY the key structure specified in SPRU §4.3, not a novel primitive or representation.

[FACT/DISTINCTION] LMSS23's original B_{L,h} allows **zero blocks**. It does not itself guarantee bounded maximum consecutive nonzero gap. In that product distribution the probability no block is empty is (L/(L+1))^h, exponentially small for constant L. The exactly-one variant must not be conflated with LMSS23's general at-most-one formulation.

[DERIVED] Let U_{n,h} be uniform among all fixed-weight-h supports in n=hL coordinates and let E be the event of exactly one nonzero per block. Then
   Pr_{U_{n,h}}(E) = L^h / binom(Lh,h).
For any fixed L>1, with binary entropy H_2,
   -log2 Pr(E) = [L H_2(1/L) - log2 L] h + O(log h).
For L=16 this is 1.396641065872222*h + O(log h), i.e. Pr(E)=2^{−Ω(h)}. Hence naive security/indistinguishability transfer by conditioning original uniformly h-sparse RLWE on E may incur an exponential loss and does not automatically provide a polynomial reduction. The distribution is NOT unchanged. This fact does NOT imply that structured-secret RLWE is insecure: the prior works perform separate analysis, and applicable high-entropy LWE reductions may be useful with their own parameters/assumptions.

[NEGATIVE] Hypothesis FAIL: the exact-one block **functional fix** is elementary AND has prior art, and it is not an assumption-preserving black-box repair of original uniform sparse secret. No novel improvement or actual compiled FAB performance gain established.

## Scope and next gate
- FAB finite Table 4 security, rejection rates, and Table 5 benchmarks are not disproved.
- FAB's §6.1 asymptotic cost with a suitable B is an operation-count statement; I120 isolates the original key generation asymptotic and I121 does NOT show the SAB algebra is wrong.
- This iteration did NOT analyze SAB end-term d[h], existing archived sparse-SAB sign failures, entire concrete RLWE estimator or proof of a new security theorem.
- [OPEN] Whether a separately justified exactly-one/block-conditioned sparse-RLWE family preserves the **polynomial approximation factor** hardness promise and achieves a new meaningful FAB cost/key/noise frontier. That would require stronger source-specific reduction and baseline analysis, not just an O(h) key sampler.
- NOVELTY NOT VERIFIED for any potential new distribution/security proof; the naive 'block one per block' modification is known and low-novelty.

## End-of-iteration
STATUS: **FAIL naive novelty/same-assumption hypothesis; PASS prior-art+combinatorial obstruction; HUMAN_REVIEW**.
RESULT: exact-one block sampler guarantees interior B=2n/h and O(h) key generation, but is already present in SPRU, unlike LMSS23's original at-most-one blocks; under uniform fixed-h secrets exactly-one-per-block event has exponentially small probability.
NEXT_ACTION: **PI decision gate**. Recommend PARK the direct block-binary 'repair' as known. If PI explicitly authorizes I122, ONE cheapest first test should inspect whether an existing applicable polynomial-hardness reduction covers the exact block secret under FAB's original *ring* and noise assumptions, or instead choose a different FHE structural problem. Do NOT conflate empirical 128-bit estimators with a formal same-assumption proof.
STATE_UPDATE: YES; no author contact, GitHub issues, PRs or public disclosure.
