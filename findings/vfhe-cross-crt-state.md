# vFHE Research State — Independent V-Series

**Checkpoint:** 2026-10-14 (Asia/Tokyo)
**LAST COMPLETED vFHE ROUND: V11. V12 NOT STARTED.**
**Status:** FAIL naive systematic-only sampled range-check extraction from ideal native per-field bounded codewords plus one shared CRT-integer Merkle root. PASS exact adversarial one-coordinate mismatch lower bound Pr[miss]=1−t/m, including one genuine Merkle toy; actual shared witness/PCS extraction, ZK/128-bit security and performance OPEN; novelty NOT VERIFIED.
**Global FHE research counter remains frozen at I192.** V1–V4 vFHE research were formerly called I193–I196 in legacy files only. No global I-series increment.

## Sequence of independent vFHE rounds

V1 (legacy I193) bounded integer toy; V2 (legacy I194) row-two single-prefix asymptotic distance obstruction; V3 (legacy I195) cyclic first-stage + arbitrary second permutation/accumulator obstruction; V4 (legacy I196) Fp→extension minimum-distance invariance; V5 (supports≤3) and V6 (supports≤4) prime-independent minor bounds; V7 almost-tight five-minor bound; V8 real source-form 49-bit prime rank-dropping five-minor (not min distance/attack); V9 global bounded-digit pair-distance inherited from binary RAA under no-wrap; V10 failure of deterministic sampled all-encoded-column CRT-lift range binding with exact probability; **V11 systematic-only range checks have one-digit mismatch acceptance probability 1−t/m, even with perfect independent native extractors**.

## Parent research and original source

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025, IACR ePrint2025/286 https://eprint.iacr.org/2025/286. 52-page cached GitHub-mirror source, SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, latest official version identity VERSION_UNVERIFIED.

Original gap source-form old I59–I60: native CRT componentwise digit lookups verify rectangle rather than diagonal shared scalar integer digit; ideal-oracle CRT idempotent shows difference, but NOT established compiled SNARK attack. Appendix F.2 physical pp50–51 describes native field-linear PCS with Merkle columns and arbitrary field random r/q1; not a shared integer commitment, not an extraction of one bounded CRT integer vector.

## V11: ONE primary hypothesis / decisive test

**Hypothesis FALSE:** If field-native component commitments have individually perfect (ideal) exact bounded-digit codeword extractors, and the prover puts their CRT recombination Y∈[0,pq)^{3m} into one binding Merkle commitment, then verifying sampled SYSTEMATIC-leaf integer-range openings in [0,β−1] yields a common integer witness with small soundness error, leveraging full code distance.

**[DERIVATION/PASS COUNTEREXAMPLE]** Two legitimate digit vectors a,b∈[0,β−1]^m with just ONE different digit j*, and each exact systematic integer linear codeword committed through same coordinatewise CRT-lift Y. For j<m, Y_j lies in [0,β−1] iff a_j=b_j (β<min(p,q)); thus exactly ONE systematic leaf violates range, despite potentially Ω(m) parity differences. One-root field projections are BOTH perfectly valid field codewords. Uniform postcommit t distinct SYSTEMATIC leaf checks accept with exact probability

    C(m−1,t)/C(m,t)=1−t/m.

More generally, any FIXED witness-independent query distribution opening at most t systematic positions has some least-covered position with acceptance ≥1−t/m; do NOT extrapolate to arbitrary root-dependent inspection algorithms. For m1024,t128: 87.5% chance of missing; t1023 still 1/1024 chance, so no 128-bit one-shot systematic-only soundness for t<m. If verifier publicly gets BOTH witnesses, it can compare directly; ideal extractors are security-reduction oracles, not public plaintext releases.

**[EXPERIMENT PASS]** Rebuild m8,beta2 genuine two-independent-permutation/two-prefix unweighted integer G, seed20261014; a=zero, b=e6; prime p=281474976829441 and q=353581838970881 both source form, >H=136. CRT-lifted array of 24 integers authenticates with ONE SHA256 Merkle root `7052562f3d88036af8dde743bc064029436bd089f2f71546ffa64741ea9bf7f3`, verified every opening; modified leaf fails. FULL native field encoding/linear scalar identities hold on all 24 positions. Exactly one systematic leaf (index6) out of [0,1], whereas 17/24 encoded leaves differ/out-of-[0,136], proving systematic-only checks lose coding amplification. Exact exhaustive probabilities: t1=7/8; t2=21/28; t4=35/70; t6=7/28; t7=1/8; t8=0.

**Local reproducible artifacts, not Git bytes:** `/mnt/data/vfhe_v11_systematic_extraction_gate.py` SHA256 `6a2275f3305d23071bc62724b31058997c18928a356b56cda7c49411e01f9a17`; results `/mnt/data/vfhe_v11_systematic_extraction_gate_results.json` SHA256 `cc285ae1a6f7fd1b00138ab559161fcfaccfb6be8dd3cb6fb5fbe508748d94ee`.

**Important sufficiency boundary:** If every systematic CRT leaf is soundly proven to lie in common canonical [0,β−1], and exact native codeword extractors really exist, then all extracted witness coordinates coincide automatically. A succinct ZK proof for this may avoid revealing raw digits but is not yet constructed. Sampling all-ENCODED columns (not just systematic) could use V9/V10 full code distance, conditional on bounded codeword extraction; original native F.2 arbitrary field-vector tests do not prove this.

## NEXT_ACTION V12 — only if PI continues

ONE smallest falsifiable noncircular ZK-compatible **joint bounded integer witness binding** method across CRT primes. Assess whether **one commitment over an unrelated arithmetic prime field** can be treated as binding in each native CRT field WITHOUT proving explicit encoding/reduction and range relations; if not, identify minimal missing relation and cost/privacy obligations. Avoid further Merkle probability toy variants; test actual cross-field binding design conditions.

## Files, status, scope

Full technical proof + provenance in `findings/vfhe-cross-crt-consistency-research.md` Section20 (V11), §19 V10, §18 V9. Root `STATE.md` only points here while global I192 is frozen. Follow `AGENT.md`: one primary hypothesis, cheapest decisive test, read-before-write, verify read-after-write. PI controls pivots and author communication. No claim of an original vFHE actual exploit or completed security repair.
