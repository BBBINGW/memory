# vFHE Research State — Independent V-Series

**Checkpoint:** 2026-10-14 (Asia/Tokyo)
**LAST COMPLETED vFHE ROUND: V7. V8 NOT STARTED.**
**STATUS:** V7 PASS exact two-prefix Cauchy–Binet minor bound and source-form high-49-bit restricted-distance gate. UNCLEAR for lower 49-bit primes and unrestricted code distance, complete cross-CRT PCS, ZK/security/cost. NOVELTY NOT VERIFIED.
**Global FHE research counter remains FROZEN at I192**, independent of this separate V-series. Legacy V1–V4 were originally labeled I193–I196 in old vFHE notes; keep those original filenames as provenance and do not advance the global I-series.

## vFHE independent historical map

| Separate round | Verified scope |
|---|---|
| V1 (legacy I193) | Small-integer shared-code toy m8, nonzero distance only |
| V2 (legacy I194) | Row-weight2 one-prefix systematic code family cannot have positive constant relative distance |
| V3 (legacy I195) | Fixed cyclic first stage + any second permutation and prefix also low relative distance |
| V4 (legacy I196) | For fixed G over Fp, Hamming minimum distance is same over extension F_(p^d); weighted RAA results cannot directly certify our unweighted n2,L2 |
| V5 | Restricted input-support≤3 rank/distance prime invariance from small minors |
| V6 | Restricted input-support≤4 rank/distance prime invariance for m≤1024, p>2^48, via monotone parity minors |
| **V7** | **Sharper two-stage Cauchy–Binet bound** certifies restricted support≤5 for **m1024, p>368933561632000**; source legal near-tight 5×5 minor >lower 49-bit p but NOT divisible by p |

## Research target / primary source

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025, ePrint2025/286 https://eprint.iacr.org/2025/286. Full 52-page research MCP GitHub-mirror PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`; latest official version equivalence **VERSION_UNVERIFIED**. §3.1: p=1+(2N/d)a for odd a; §6: 49-bit CKKS benchmark primes (code m need not equal ring N).

Original cross-CRT gap [legacy general I59–I60]: native per-field lookup enforces RECTANGULAR digit membership rather than DIAGONAL common integer digit. A source-form R=Z77[X]/(X²+1) CRT-idempotent ideal-PIOP counterexample exists under inspected mirror version. **Not** a verified fully compiled/deployed SNARK exploit or latest officially confirmed vulnerability.

## V7 — ONE PRIMARY HYPOTHESIS, ONE MINIMAL DECISIVE TEST

**Question:** Does the two-accumulator prefix structure materially tighten the 5×5 integer-minor upper bound enough to preserve rank/distance at source-form CRT primes, versus the generic V6 bound which exceeds 49-bit primes? Counter-test with one near-maximizing exact legal permutation to see if bound is almost tight.

**[DERIVED/PASS]** Let G=[I_m|P], P=Rep2·Perm1·U1·Perm2·U2 with n=2m, positive prefix U. For any r×r parity minor, Cauchy–Binet gives det P_{S,J}=Σ_{T} det Z_{S,T} det U2_{T,J}, Z=Rep2·Perm1·U1·Perm2. Since before Perm2 each row is nonnegative monotone ending at 2, |det Z_{S,T}|≤2^r. For sorted parity columns J, the U2 minors are 0 or 1, with nonzero count ∏ℓ_i where positive interval lengths sum≤n. Therefore

  |det P_{S,J}| ≤ D(n,r)=2^r·q^{r−h}(q+1)^h,  n=qr+h, 0≤h<r.

Unit systematic columns expand to lower-degree parity minors; at m1024,r≤5 maximum is D(2048,5)=**368933561632000**. For every p above this threshold, zero/nonzero status of all generator minors involving≤5 message rows survives mod p. Hence restricted d_{≤5} is identical over Q, qualifying CRT base fields and their extensions, for a **fixed integer G**. At m256/m512 the threshold <2^48, so ALL p>2^48 qualify. At m1024 only SOME 49-bit primes qualify. Full unrestricted d_min unchanged? UNKNOWN.

**[EXACT COUNTER-WARNING / TIGHTNESS]** Legal m1024 first permutation places both repeats of inputs 0–4 at starts of consecutive blocks [410,410,410,409,409], filling other positions with other repeated symbols; second permutation identity. The sampled 5×5 parity minor is triangular with diagonal [819,819,819,817,817], determinant **366687257496651**, 99.3911% of universal bound. Valid source-form 49-bit prime p_L=**281474976829441** is smaller than this determinant (but does NOT divide it; remainder **85212280667210**). Valid higher source-form 49-bit prime p_H=**368933562830849** exceeds bound and is guaranteed. p_L and p_H both are prime and p mod8192=4097 for N8192,d4. This explicitly defeats any hope of certifying *all* 49-bit primes by an absolute minor bound below p_L, but is **NOT** an actual rank-changing CRT example.

**[MINIMAL EXPERIMENT PASS]** Python script `/mnt/data/vfhe_v7_cauchy_binet_five_support.py` SHA256 `1e4c90e62215a45dd73ba1cfc91841919719819acbb0b72ba1eef66f670afda1`; JSON `/mnt/data/vfhe_v7_cauchy_binet_five_support_results.json` SHA256 `cee8f200a75d5ce890dca8b4c0dfa92ed96a42480fd3f86bcce7d5f058f03142`. Files LOCAL ONLY, not Git. Exact 5×5 determinant construction and 60-term independent small Cauchy–Binet identity match; random 5-minor samples for m256,1024,2048 support numerical bound but do not certify missing lower-prime cases.

## Main unresolved FHE+ZK research

- **Global Hamming relative distance** of genuine unweighted two-independent-interleaver n2,L2 integer RAA across entire prime-field code: **OPEN**. Local support≤5 gates do not establish asymptotic good code.
- **Full shared canonical integer Merkle commitment**, proximity/extraction, fieldwise Appendix F.2 evaluation compatibility, zero-knowledge masking/hiding, Fiat–Shamir security/error, full system proof cost and true novelty: **OPEN**. A few code minors cannot repair vFHE's diagonal digit flaw.
- Original paper current official-version parity / full compiled protocol: VERSION_UNVERIFIED.

**Full proof and provenance:** `findings/vfhe-cross-crt-consistency-research.md`, Section16 V7; §15 V6, §14 V5; earlier V1–V4 mapping at top.

## NEXT_ACTION — V8 only on PI continuation

ONE decisive investigation: find a real legal **49-bit CRT prime divisor** of a nonzero 5×5 parity minor of this actual RAA integer generator (giving first genuine rank-change witness); OR rigorously exclude divisibility for a meaningful source-compatible subclass. Do not confuse having |det|>p with p|det. If no cheap decisive result, halt narrow low-support work and recommend PI consider global-distance or cross-CRT shared-commitment proof directly. Maintain one primary hypothesis/test.

## Archive process

Global root `STATE.md` is only the frozen I192 index into this track. This file holds vFHE rounds; technical record in `findings/vfhe-cross-crt-consistency-research.md`. Follow `AGENT.md`, read-before-write and read-after-write, [FACT]/[DERIVED]/[OPEN] provenance, PI controls strategic pivots and any disclosure.
