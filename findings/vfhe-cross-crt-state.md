# vFHE Research State — Independent V-Series

**Checkpoint:** 2026-10-14 (Asia/Tokyo)
**LAST COMPLETED vFHE ROUND: V15. V16 NOT STARTED.**
**STATUS:** V15 FAIL the shortcut “batched extension-field linking with vector Pedersen / standard IPA has sublinear VERIFIER group work merely because proof bytes are logarithmic.” PASS exact operation-count model for two explicitly limited baselines and a degree-4 field coefficient rank check. Whole vFHE repair/protocol speedup, joint knowledge extraction, ZK, Fiat–Shamir/128-bit security and novelty remain OPEN/UNCLEAR.
**GLOBAL GENERAL FHE ITERATION COUNTER:** FROZEN at I192. Independent V-series; earlier vFHE notes mislabeled I193–I196 correspond to V1–V4 only and do not advance global rounds.

## Research trajectory

V1 integer common-code toy; V2/V3 binary row-weight-2 single/cyclic double prefix distance obstructions; V4 prime-to-extension code-distance equality; V5–V8 cross-prime low-support minor/rank gates including V8 true 49-bit prime-divisible five-minor; V9 bounded-digit global distance from binary RAA plus integer no-wrap; V10 sampled codeword Merkle range not deterministic binding; V11 systematic-only check one-digit mismatch miss probability 1−t/m; V12 third-field commitment without links and range is insufficient; V13 128-bit INTEGER challenge in 49-bit prime subfield gives only 48-bit soundness for one false relation; V14 genuine extension challenge requires four base-basis modular quotient equalities and an actual linear-functional commitment proof; **V15 simple Pedersen / separate IPA linking saves communication potential but does not by itself eliminate O(Fm) MSM work**.

## Parent source target and scope

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, IACR ePrint 2025/286, https://eprint.iacr.org/2025/286. Verified research-MCP mirrored 52pp PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`; official latest VERSION_UNVERIFIED. §3.1 physical p10 decomposes each ring prime into k=N/d extension field factors; Appendix F.2 pp50–51 uses NATIVE field Merkle/Brakedown PCS; none of our auxiliary common-integer Pedersen/IPA protocols appear in paper. Historical cross-CRT rectangular-vs-diagonal digit lookup remains ideal-oracle/source-form audit ONLY, NOT confirmed compiled SNARK exploit. No full correction protocol.

## V15 — one hypothesis, one decisive operation-count gate

**Hypothesis falsified in tested baselines:** Once V14 proves four extension basis-coordinate quotient relations S_t=z_t+p k_t, using a naive collection of separately homomorphic Pedersen digit commitments OR a compact Pedersen vector commitment with ordinary independent IPA linear-functional openings should require just O(F log m) **verifier group work** for F independently linked F_(p^4) instances (as opposed to O(Fm)), on the strength of O(log m) proof communication.

**[DERIVATION PASS]** Four independent coefficient forms per extension instance in F_(p^4); L=4F linear forms. Path A with public commitments C_j=g^(a_j)h^(rho_j), for each functional D_t=∏_(j<m) C_j^(ctilde_jt), a direct verifier/group aggregation MSM processes m terms; overall 4Fm scalar-base pairs. The CP link still needs quotient/range/knowledge-sound native value statement and a binding of derived D_t to original C_j. Path B with one Pedersen vector commitment C, conventional separate IPA functional proofs can have O(F log m) **communication**, approximately 2log2m folding L/R points per form, but the conventional IPA verifier performs a length-m MSM per form, i.e. O(Fm) scalar-base pairs. See Halo2 book `https://zcash.github.io/halo2/background/pc-ipa.html` and `https://zcash.github.io/halo2/background/recursion.html`. Those are STANDARD direct baselines, NOT a universal lower bound: multipoint aggregation, IPA recursion/accumulation, preprocessing or alternate commitments may change work. These simple approaches do NOT yield verified overall improvement.

**[EXACT MODEL PASS]** Source-like hypothetical m1024,d4,N8192,beta2^20,p281474976829441, integer S_t upper bound 302231166800824369152000=78 bits; k_t maximum1073740799=30 bits. If F=mu (ONE linked field per prime), with mu=4: L16 forms, 16384 MSM input terms; standard independent IPA L/R fold points ~320 (EXCLUDING full ZK proof). If EACH of k=N/d=2048 fields per prime is independently linked (CONDITIONAL workload, not proven necessary), with mu4: F8192, L32768 forms, 33554432 MSM terms and approx 655360 IPA fold points. This is NOT the original paper's commitment cost or a benchmark; batching across CRT extension factors could sharply improve.

**[EXACT ALGEBRA]** Toy K=F29[theta]/(theta^4+theta+5), alpha=28+theta. First four powers [1,alpha,alpha²,alpha³] have F29 coordinate rank4, so the native full-extension equality genuinely contains four independent prime-field component relations. Revalidated V14's S=(562,423,253,282), z=(11,17,21,21), k=(19,14,8,9). Existence of four base relations does NOT require four distinct SNARK proofs.

**[ARTIFACTS, LOCAL ONLY]** /mnt/data/vfhe_v15_batch_link_cost_gate.py SHA256 82406ea2e47ba58b700cec73c0aa069608af24b951000f7a2208619148843855; /mnt/data/vfhe_v15_batch_link_cost_results.json SHA256 d74231e2ba9d84811a55ecbca5715a9c5e753bf4bcc2667969e8f3dcdea89859. Executed twice with identical hashes. Symbolic exact arithmetic/operation counts, NOT timed scalar multiplication, IPA proof bytes, SNARK, privacy or an actual PCS implementation.

**Novelty:** The asymptotic IPA tradeoff and ring factorization are prior art. No new commitment/cryptographic construction or speedup evidenced.

**Full technical proof:** `findings/vfhe-cross-crt-consistency-research.md` Section24 V15, §23 V14, §22 V13.

## NEXT_ACTION V16 — only on PI continuation

One precise probability/operation test: Within ONE source CRT prime p with k=N/d native extension factors, can a postcommit random F_p linear combination of the 4k quotient/field-link residuals reduce the expensive group-based linear-functional openings to O(1) PER PRIME rather than 4k, retaining a known 1/p false-accept bound per independent challenge? Must still bind ALL native values/zs and the canonical integer vector before challenge, and account for O(km) cheaper field-arithmetic work and multiple challenges to attain ≥128-bit composed soundness. Do not assume a free cross-characteristic homomorphism or an actual native F.2 extractor. If no cheap sound protocol is found, mark UNCLEAR/HUMAN_REVIEW.

## Files and researcher roles

Root STATE.md frozen global I192 and index only. Independent vFHE state here; full evidence in the cumulative research file. Human PI controls pivots, novelty and contact with authors. Follow AGENT.md: one smallest falsifiable hypothesis and test, read before write, reread afterward.
