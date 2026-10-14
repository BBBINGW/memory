# PVFHE-P25 — Exact shared Coeff/KeySwitch bits and public-output Ring-R1CS boundary

**2026-10-15 Asia/Tokyo. P25 COMPLETED, P26 NOT STARTED.**
**STATUS:** PASS source-shaped 755-row terminal R1CS satisfies two different public-output statements under the SAME switching-key inputs, even when Coeff and KeySwitch share 54 bit witness wires; PASS rejection if fake witness is forced to honest fixed output; UNCLEAR original full FHE.EvalGate A/B/C or SNARG proof. No original-paper cryptographic attack or wrong decryption proved.

## Read before write / primary provenance
Read START_RESEARCH_SESSION.md SHA 6235e9d376a8b143719a40178132f02a6a41d4f3, RESEARCH_PHILOSOPHY.md SHA 49da3f7fa3e75f502525482ce4a7ab6867, AGENT.md SHA b3e73b2c7f852c05aa674dd97b632e9f99ac5f22, shared STATE.md SHA 3b83237bc5aba4a77479b09dc1f3ac8bccaebc7c (independent vFHE V42, NOT EDITED), P24 findings/pvfhe-P24-acc-extract-ks-independence-r1cs-link-gate.md SHA e42ccdb5d6afea79a98aeb0df5bf3fd2e61b0e92, P23 SHA 8c74c73f761571dbced8ed32391985a982c0aede, P02 SHA 9b09262066c61778ce581abbba4dbd5098ee5483. P25 target not found before writing. No writes to parallel vFHE/SHIP STATE or earlier P-series.

Original Huang–Li–Mao–Zhang, Fully Homomorphic Encryption with Efficient Public Verification, ePrint2024/1764. Research MCP full physical 29pp mirrored PDF SHA256 7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089, VERSION_UNVERIFIED; read p12 Definition4.1 Ring-R1CS io, p13 ACC/KeySwitchGen, p14 FHE.KeyGen/Algorithm2 self-XOR, p15 Lemmas4.4/4.5/4.7, p16 Lemma4.8 Rounding / Coeff4.11, p17 Theorem4.12, p27 Appendix C.3 variable merge and final public io. Official IACR landing https://eprint.iacr.org/2024/1764 inspected independently and online PDF text matches paper identity, but web screenshot p15/p27 cache miss; no authenticated current-version PDF bytes and no author compiler.

## ONE primary falsifiable hypothesis / decisive minimal test

**[HYPOTHESIS P25]** Hidden Coeff-KeySwitch bit-witness SHARING and/or public-output io equality in original AppendixC.3 fixes the canonical BitDecomp value and prevents any noncanonical output statement, even in the deterministic P24 self-XOR ACC zero-mask case.

**[FALSIFIER]** Explicitly generate sparse R1CS rows with ONE source 54-bit decomposition witness shared between zero Coeff output y0 and KeySwitch input a0. Include all selected Index equations, summing, canonical output Rounding and binding to the claimed public ciphertext. Verify under fixed ek projection TWO distinct claimed-output instances are simultaneously satisfiable. As an essential negative control, pin fake internal witness to honest claimed public ciphertext; it MUST fail if output binding is implemented correctly. Do not infer actual full SNARG acceptance from a source-shaped subcircuit.

## Source facts and algebra

From P24 and source Fig2/Algorithm2, for any legitimate c reused as XOR(c,c), temporary LWE = 2(c−c)=0 and all alpha_i=0. ACC.Init mask=0 and every ACC.Update correction factor is (X^0−1)=0, so ACC.Extract mask polynomial a(X)=0, yielding ALL source coefficient values y_i=0 for any ek, even with normal errors.

Q=2^53+5 (source AppendixB), ell=53: BitDecomp accepts b_j²=b_j and y0=sum_{j=0}^{53}2^j b_j modulo Q. Both all-zero and b_0=b_2=b_53=1 (integer Q) reconstruct y0=0. This holds with ALL scalar bits, irrespective of CRT-specific non-scalar idempotents. The source Coeff polynomial equality a(X)=sum_i y_i X^i still holds since y_i=0 in R_Q; using identical bit wires for Coeff and KeySwitch does not add integer bound sum 2^j b_j < Q. The source Lemma4.7 Index selects public keys accordingly and KeySwitch output changes. Lemma4.8 canonical Rounding can faithfully constrain either raw output. Definition4.1 includes output in public io, so different claimed outputs are DIFFERENT PUBLIC INSTANCES. Theorem4.12 claims each instance is satisfiable IFF the claimed ciphertext equals actual FHE.Eval; source AppendixC.3 only instructs merging wires representing same circuit value, not a new canonical range predicate. Unspecified graph-sharing outside these gadgets remains an unresolved full-compiler issue.

## ONE ACTUALLY EXECUTED exact sparse terminal Ring-R1CS compilation

Run with SOURCE Q=9007199254740997, n=q=1024,N=2048. Generate one Coeff/KeySwitch common 54-bit witness and actually compile:
- 163 BitDecomp rows = 54 boolean +54 binary-weight +54 prefix +1 output reconstruction.
- 108 Index rows for 54 source key choices across one public mask coordinate plus body.
- 108 source key-switch running sum rows.
- 4 join / subtract rows to form raw mask/body.
- 372 raw Rounding / high-bit reconstruction / public output link rows = 186 per coordinate.
TOTAL **755** actual sparse A/B/C rank-one rows on **973** Ring-R1CS variables; each A, B and C row has <=2 nonzeros, meeting source Lemma4.4. Uses source KeySwitchGen normal independent uniform public masks, ternary LWE secret, z0=3 and nonzero discrete Gaussian support errors, immutable common contribution from the other KSK branches; full KSK for 2048 coefficients NOT materialized.

We set example ACC body symbol to representative 42 (not claimed source f_XOR(0)); mask result is independent of that choice. All remaining 2047 Coeff output scalar zero wires admit trivial honest decomposition; their full source rows were NOT generated in this limited test. The original full ACC, KeyGen, Gate A/B/C, PCS and SNARG transcript not executed.

**Results (verified exact modular arithmetic):**
- Public key projection identical between both statements.
- Honest shared bits all 0: **755/755 rows PASS**, public two-coordinate (mask0,body)=(687,225).
- Alternate shared bits {0,2,53}: **755/755 rows PASS**, public two-coordinate (mask0,body)=(392,665).
- Source-shaped projected public mask vector after ModSwitch has **1023/1024** differing coordinates for this fixed seed; no false claim 1024/1024.
- Pin alternate internal witness to HONEST public output values: FAIL exactly BOTH PUBLIC_output_bind rows. This is proper fixed-statement binding; do NOT label as forgery of an already-fixed true-output statement.
- Secret-phase difference is solely selected switching-key errors, not proof of wrong plaintext.
- Every row is a formal ring R1CS equality over scalar copy of F_Q embedded in original R_Q, not a field-only rewrite.

Reproducible current-session local files:
- /mnt/data/pvfhe_p25_shared_coeff_keyswitch_r1cs.py SHA256 ed4d30e76ee2ae844304e0458789973a48386741e47828431da40e0c39e9c955.
- /mnt/data/pvfhe_p25_compiled_shared_witness_results.json SHA256 1bf7ada08329851d1b665073f06712e0657e504dfca5e57aa65fb84344f36a06.
- /mnt/data/PVFHE_P25_Compiled_Shared_Bit_Witness_IO_Gate.md SHA256 0803926945344c1e171fc913ea2822a284668e4748520f616bf16b22049ec5db.

## Important limitations and research decision
These are SOURCE-SHAPED selected-coefficient terminal R1CS constraints, NOT author's full ACC + Coeff(2048 coefficients) + all output coordinates full Gate compilation; omitted gadgets are only argued to be extensible via honest zero witnesses, not independently compiled. Another hidden relation or accidental auxiliary bit-wire graph merge in an actual compiler could invalidate the proposed extension; no actual author source artifact proves otherwise. Distinguish same circuit wire identity from unrelated wires with accidentally equal values in one honest execution. Primary PDF version unverified; screenshot unavailable. Neither lattice PCS/FS nor proof verification or false plaintext corruption executed.

**STATUS:** PASS subcircuit double-output satisfiability WITH shared Coeff-KeySwitch bits, PASS public-output exact binding negative control; UNCLEAR full author compiler / exact verified current paper / complete SNARG validity.
**RESULT:** Coeff/KeySwitch shared bit witness cannot by itself make 54-bit modulo-Q reconstruction canonical. For one public key and input, two separately satisfiable *output statements* exist in the terminal circuit while fixing the honest output rejects the alternate witness. This is the relevant local Theorem4.12 semantic obstruction; NO confirmed complete-proof forgery.
**NEXT_ACTION P26 only if PI continues:** ONE source-complete gate DAG/wire-merge independence gate to test whether any other BitDecomp XPow zero-valued aux bits must be shared with this KeySwitch bit witness, and whether the full assembled source circuit admits a global satisfying witness. If original compiler remains unavailable, classify full SNARG theorem failure HUMAN_REVIEW rather than claiming exploit. Do not resume parked PCS/FS line or repeat random-key mask tests.
**STATE_UPDATE:** YES THIS independent P25 only, no global STATE, concurrent vFHE/SHIP or P01–P24 edits.