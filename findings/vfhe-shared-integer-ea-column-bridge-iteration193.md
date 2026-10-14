# I193 — vFHE cross-CRT integer-code bridge: explicit small-field-independent encoder gate

Date: 2026-10-14. PI explicitly selected vFHE cross-CRT consistency, after I192 handoff. Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` and P1 index, I59–I60, I94, I138, I151. ONE primary hypothesis + ONE exact minimal necessary algebraic-code test. No author's code modified, no external author contact, no full protocol forgery.

## Primary question / hypothesis

[HYPOTHESIS] A replacement for the native prime-dependent F.3 RS encoder can use **one bounded-integer, small-coefficient, field-linear code** across all CRT prime factors, with (i) identical honest codeword *integer* symbols under different primes (no wrap), and (ii) nonzero Hamming distance between distinct table-index vectors over every relevant extension field. If so, a future **common integer-coded Merkle column commitment** might be usable as a cross-component bridge instead of comparing the incompatible current native RS/NTT columns.

[CHEAP FALSIFIER / ONE TEST] Construct an explicit nontrivial tiny source-form pair of primes and one O(m)-encodable systematic expand-and-accumulate toy code; verify EVERY pair of binary message vectors has nonzero codeword distance, with an exact field-independent argument, and verify honest canonical integer symbols coincide and remain < p_min. If no, reject the bridge at the first algebraic gate. This test does NOT presume a full PCS, asymptotic distance, or a 128-bit construction.

## Primary source / prior-art check

[FACT] Original Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint 2025/286, Research MCP mirrored **52 physical pages**, PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, VERSION_UNVERIFIED. §5 and F.1 pp25/50 split commitment into independent fields; F.2 pp50–51 commits each field's m×M *coded columns*, with testing `Enc(v)|Q = r Uhat[:,Q]` and evaluation `Enc(v')|Q' = q1 Uhat[:,Q']`; F.3 pp51–52 uses native-prime-dependent RS evaluation nodes. I151 already **falsified direct comparison of unchanged RS columns on honest input** (p29/p37, [0,1] gives j1 12 vs6), and proposed a NEW bounded-integer encoder as unconstructed future architecture. This iteration explicitly tests that outstanding architecture's first algebraic gate, not the failed source RS reuse.

[FACT, newly read original research papers]
- Golovnev et al., *Brakedown*, CRYPTO 2023, ePrint 2021/1043, Research MCP original section 5 physical pp18–20: linear-time **field-agnostic** recursive sparse-code generator, but samples nonzero edge coefficients from the native field. That property alone does NOT furnish the same bounded *integer* generator over different primes.
- Block et al., *Field-Agnostic SNARKs from Expand-Accumulate Codes*, CRYPTO 2024, ePrint 2024/1871, original physical pp4–8: accumulator A is an all-1 prefix operator, sparse expanding E, field-agnostic distance analysis uses randomly generated nonzero field elements over general F; binary variant is different. Its published distance proof CANNOT be reused unmodified after fixing all nonzero entries to literal integer 1.
- Nair et al., *BrakingBase*, ASIACRYPT 2025, ePrint 2024/1825: alternate PCS efficiency / field-agnostic inspiration but field agnosticism alone does not impose CRT cross-field shared witness.
- Setty et al., *Lasso*, EUROCRYPT 2024: structured indexed lookup inspiration, not a cross-prime equality proof. NO directly matching exact common-integer vFHE code bridge found in limited literature search; **NOVELTY NOT VERIFIED**.

## Concrete constructive test [DERIVED + EXACT TEST]

Take m=8, beta=2, source-form N=8,d=4,p0=29,p1=37 (p=4a+1 with odd a=7,9). Let E=Enc_Z:
```
 Enc_Z(x) = (x, prefix(x A)) in Z^16,
 prefix(y)_j = sum_{k<=j} y_k.
```
A is a public 8×8 {0,1} sparse matrix, each row has exactly two ones, at zero-based positions:
```
 row0: (4,7)  row1: (1,4)  row2: (1,2)  row3: (0,5)
 row4: (3,4)  row5: (3,6)  row6: (5,6)  row7: (2,6).
```
Encoding costs 2m sparse additions plus m prefix sums O(m), rate 1/2. It is *integer-linear*, hence after reducing coefficients modulo any prime, the exact same generator is linear over F_p and its extensions.

**No-wrap/completeness (necessary gate PASS):** for any honestly shared x in {0,1}^8, every prefix value is in [0,16], below p_min=29. Thus Enc_Z(x) is the SAME canonical ordinary integer vector in both F29 and F37; native RS j1=12 vs6 failure from I151 does not arise. More generally for nonnegative A with fixed row weight d and x_i in [0,beta−1], maximum prefix ≤ d m (beta−1). The needed source parameter condition is d m (beta−1)<p_min; this is **not** a sufficient full-protocol condition.

**Minimum-distance calculation (necessary gate PASS):** exhaustive enumeration of all 3^8−1=6560 distinct nonzero differences x−x' with x,x' in {0,1}^8 yields min Hamming weight **3 out of16**, relative distance 3/16=18.75%. Witness d=e7−e5 (zero-based): Enc(d) is nonzero at systematic positions 5,7 and parity coordinate10.

**Stronger exact proof over every ODD-CHARACTERISTIC field and its extensions:** If an arbitrary field vector u has wt(u)≥3, the systematic part already has ≥3. If wt(u)=2, distinct fixed-weight 2 Boolean rows of A are linearly independent in every field (they cannot be nontrivial scalar multiples), so u A ≠0; the prefix map is invertible, giving at least one nonzero parity position and wt Enc(u)≥3. If wt(u)=1, u A contains two nonzero impulses of equal coefficient. In odd characteristic, at least two of its prefix coordinates are nonzero (at the earlier and later positions), giving wt Enc(u)≥3. The exhibited weight-3 witness attains equality; thus field code minimum distance is EXACTLY 3, not only a bounded-digit phenomenon or experimental observation. No security statement for full PIOP/Fiat–Shamir follows.

Reproduction: local file `/mnt/data/i193_vfhe_universal_integer_ea_toy.py`, SHA256 `70e27821a362761316d36c2f097ec1634b20349e00c8bcf566d33e07c67d7502`, executed and PASS. This local file is not accessible by GitHub MCP; reproduce from generator rows above and the distance proof.

## New *candidate* common-column architecture [HYPOTHESIS / OPEN, NOT TESTED HERE]

- Existing fieldwise lookup ensures each Boolean-domain digit vector x^(k) has entries in [0,beta−1] inside its native field, but alone allows x^(k) ≠ x^(l).
- Replace only h's native F.3 per-field code with Enc_Z whose public integer matrix G is the SAME over all fields and whose **honest** codeword coordinates lie in [0,p_min).
- Hash/Merkle-commit ONE vector of canonical bounded-integer encoded columns, possibly with necessary per-column randomness/hiding. Open SAME sampled columns after field-dependent PCS response vectors have been fixed. Interpret opened integer columns in each field to run the original-form F.2 linear checks.
- If a full field PCS binding/proximity proof makes the shared committed columns sufficiently close to Enc_Fk(x^(k)) for each field, and a **uniform positive relative distance** holds across extension fields, then two different field digit vectors must be incompatible with one committed codeword. Must explicitly prove this extraction, closeness threshold, sampling order, and bad-column boundedness.

***Very important NOT a protocol result***: F.2 sends per-field evaluation vectors `v'^(k)`, which remain different at arbitrary random extension-field evaluation points, so they cannot be collapsed merely because input Boolean digits share an integer representation. Cross-field repeated original encoded COLUMN data may become shareable, but field-specific evaluation vectors stay mandatory.

**Illustrative communication envelope (NOT benchmark or 128-bit bound):** Take source-inspired mu=6144, m=256, t=32, 25 bytes/F_(p^4) element. Original *one F.2 evaluation's* explicit native field-symbol payload ≈ mu*m*(1+t)*25 =1,297,612,800 bytes=1237.5 MiB. Hypothetical common codeword-column interface with 4 bytes per bounded integer has mu*m*25 + t*m*4 =39,354,368 bytes=37.53125 MiB, ≈32.97× reduction in this isolated interface; it ignores Merkle, testing, other PIOP messages, binding/privacy, and might be invalid if suitable code demands larger t, extra checks, or fields do not share commitment leaves. This is NOT overall vFHE gain. Unlike I138 (<4×) which reused columns only ACROSS FOUR evaluations of the SAME field commitment, this candidate seeks reuse ACROSS mu CRT field commitments.

## Major unresolved / possible falsifiers

1. **Asymptotic field-code distance at source-sized m**: the toy min 3/16 says nothing about positive distance independent of m. Original EA code's field-generic theorem uses random nonzero F coefficients; forcing coefficients to {0,1} invalidates automatic transfer. Prove/code/test one explicit sparse bounded-integer family at m256/1024, including extension-field dependence. If only distance O(1/m), this fails decisively.
2. **No-wrap budget**: with sparse row-weight d and prefix accumulation, d*m*(beta−1)<p_min needed. p_min≈49bit and beta16 or beta2^20 are individually plausible for moderate d,m, but published full layout and all generated intermediate values must be verified. This formula applies ONLY to honest bounded input, not arbitrary prover PCS evaluation vectors.
3. **One shared commitment + field-specific F.2 correctness**: replacing separate field commitments with one canonical INTEGER Merkle tree is a different PCS construction; needs new proof of binding/extraction and sufficiently many bounded-column checks. Plain fieldwise testing of separately chosen roots does NOT solve the original CRT hole. Challenge sets Q across components must be sampled *after* prover's claimed evaluation vectors; independence/security accounting and Fiat–Shamir must be redone.
4. **Privacy**: direct hash commitments to low-entropy digit columns and their direct openings can reveal witness values or admit guessing. Require hiding/salting/zero-knowledge analysis; don't assert original vFHE privacy remains.
5. **Cost/performance**: source uses fast NTT RS; actual high-distance code must preserve quasilinear/linear encoding with acceptable parameters/t, and achieve meaningful total-system gain; native per-field evaluation response cost remains.
6. **Novelty**: encoder itself draws from known systematic and EA techniques. Need mechanism-specific literature check for common integer code and cross-field commitment. No novelty claims; no author contact/public disclosure.

## End of I193

**STATUS:** PASS for the narrow necessary toy algebraic/common-canonical-codeword gate; **UNCLEAR** viable scalable global shared-Merkle PCS repair; NOVELTY NOT VERIFIED.
**RESULT:** G=[I, sparse expansion + prefix] toy has exact field-independent minimum distance 3/16 and common integer honest encoding for p29,p37, overcoming I151's *honest encoded-column mismatch* for this NEW encoder. Found the natural large-μ data reuse opportunity and identified the missing asymptotic-code/security/privacy gates. **NO complete repaired vFHE or proved practical speedup**.
**NEXT_ACTION:** I194 (ONLY ON PI CONTINUATION): ONE decisive **source-sized sparse integer EA code-distance gate**. Use author-relevant m=256 or 1024, beta=16 or precisely verified h layout; inspect Block et al. 2024/1871 §4 proof to see if fixing every nonzero expansion coefficient to 1 preserves a uniform constant relative distance over all native odd-characteristic extension fields. First look for an explicit low-support codeword family or mathematical counterexample; if such a family forces δ→0, KILL this direct EA encoder and preserve only the abstract common-codeword architecture. Do not build PCS first.
**STATE_UPDATE:** YES — new human-selected parent target, completed I193, small positive constructive gate, next obstruction.
