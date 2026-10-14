# vFHE Research State — Independent V-Series

**Checkpoint date:** 2026-10-14 (Asia/Tokyo).
**LAST COMPLETED vFHE ROUND:** **V6**. **NEXT:** **V7 NOT STARTED**.
**Status:** PASS necessary but limited coding-theory gate at input support≤4; all-support linear minimum distance and complete cross-CRT ZK repair OPEN / HUMAN_REVIEW; NOVELTY NOT VERIFIED.

**Global FHE research counter:** FROZEN at general I192. This is an independent project V-series. Legacy vFHE archive labels I193–I196 mean V1–V4 only; do not advance global I-series.

## Independent vFHE sequence

| Round | Outcome |
|---|---|
| V1 (legacy I193) | Common bounded-integer single-prefix toy m8, distance3/16, finite feasibility |
| V2 (legacy I194) | Uniform row-weight2 single-prefix family has vanishing relative distance |
| V3 (legacy I195) | Fixed cyclic first expansion + any second interleaver and prefix also vanishing relative distance |
| V4 (legacy I196) | Base prime→extension field distance invariant when code generator is in Fp; weighted nonbinary RAA theorem not directly applicable to unweighted n2,L2 |
| V5 | For fixed integer true two-interleaver repeat2 double-positive-prefix generator, all codewords from input support≤3 have prime-independent minimum distance at p>384m³ |
| **V6** | **Stronger monotone parity-minor theorem**: d_{≤4} is independent of CRT prime p>2^48 (including extension fields), for actual encoder message dimension m≤1024 |

Original vFHE audits in much earlier general I59–I151 remain historical evidence unchanged. Avoid renumbering legacy files.

## Research target

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint 2025/286, https://eprint.iacr.org/2025/286. MIRRORED 52-page source SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, VERSION_UNVERIFIED versus latest official binary. §3.1 gives p=1+2aN/d for odd a; §6 pp27–29 benchmark with 49-bit native RNS primes.

Original structural gap: per-CRT-field digit table membership checks larger RECTANGULAR lookup relation instead of intended DIAGONAL common integer scalar index (earlier I59–I60 source-form ideal PIOP counterexample). Not authenticated deployed final-version SNARK attack or author-confirmed current flaw. Goal: provably cross-field-bound and hidden one canonical integer digit vector with usable cost, but no full protocol exists.

## V6 ONE PRIMARY HYPOTHESIS / DECISIVE TEST

**[HYPOTHESIS, refuted]** Since generic V5 four-minor upper bound `4!(4m)^4` exceeds p≈2^49 for source-scale m1024, distinct CRT primes could introduce new support-4 linear dependencies or extra low-weight codewords in the fixed bounded-integer generator.

**[DERIVATION, PASS]** The parity block P of `G=[I_m|P]` for independently permuted repeat2 / positive-prefix / independently permuted / positive-prefix is rowwise nonnegative MONOTONE IN OUTPUT POSITION and every entry ≤4m. For any nonnegative monotone row k×k integer matrix M with entries≤B, factor M=D U with nonnegative row-wise increments D and unit-upper-triangular cumulative U (det1). Hence `|det M|=|det D|≤∏_i Σ_j D_ij≤B^k`. Unit columns of systematic I_m reduce arbitrary k×k generator minors to smaller parity minors; bound `|det minor|≤(4m)^k`. For m≤1024,k≤4, upper bound≤(4096)^4=2^48. All primes p>2^48 preserve ranks of all submatrices with ≤4 selected generator rows and hence `d_{≤4}(G;Q)=d_{≤4}(G mod p;Fp)=d_{≤4}(G mod p;F_(p^d))`. This equality also holds ACROSS different qualifying CRT primes for the SAME fixed integer G. **This is only restricted input support≤4 and CONDITIONAL on the actual code input dimension m.**

**[EXPERIMENT, PASS]** Source-form compatible 49-bit primes `281474976829441, 281474976894977` both prime, both p≡4097(mod8192), valid N8192,d4 p=1+4096a odd a. For m8 true double independent permutations, exhaustive all **743820** 4×4 minors: 0 prime-related zero-status mismatches; max integer determinant128 (<32^4). Additional independent random parity minors m256 (500), m1024 (500), m2048 (100): all same zero-status, but universal theorem only covers m≤1024 at p>2^48. Local executable `/mnt/data/vfhe_v6_monotone_minor_gate.py` SHA256 `aa98b19c0783e33e9997c9d4bc26f18017bc42633ea3bd6e931154d3a71193f3`; local result JSON SHA256 `e1d0182f1c3758622cdf347ffc2e6161bfea37c5201531dc02922e6770e48557`. LOCAL ONLY, not Git files.

**Source and technical details:** `findings/vfhe-cross-crt-consistency-research.md` **Section 15**. Earlier V5 §14, V4 §13, V3 §12, V2 §11.

## Main unsolved research problem

Can unweighted repeat2/two-independent-interleaver/two-positive-prefix **integer generator code** simultaneously have **positive constant unrestricted Hamming distance** across all source CRT primes, no-wrap for honest small integer table indexes, near-linear encoding, and be used in an actually binding/hiding cross-field shared Merkle PCS? All-support distance, binding/extraction and 128-bit soundness, zero knowledge, FS transcript and total proof cost remain OPEN; these low-support lemmas are not a vFHE protocol repair or publishable contribution.

## NEXT_ACTION — V7 only if PI continues

ONE falsifiable question: whether support5 can have a source-prime-specific rank change/low-weight codeword at m1024 because `(4m)^5` exceeds 49-bit p. Prefer a structural argument or exact small submatrix witness; do not mistake a coarse bound's failure for existence of a discrepancy. Do NOT switch to full PCS before a satisfactory global code-distance gate or PI pivot.

## Archival and workflow

Global `STATE.md`: index only and frozen I192. This file: vFHE round state. `findings/vfhe-cross-crt-consistency-research.md`: full independent subject findings. Follow `AGENT.md`: one hypothesis and one cheapest decisive test, read before write, verify commits by rereading. Human PI controls main research decisions and external disclosure.
