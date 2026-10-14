# PVFHE-P26 — Full-Gate DAG BitDecomp Width / Wire-Merge Contract Gate

Date 2026-10-15 Asia/Tokyo. **P26 COMPLETE; P27 NOT STARTED.**

**STATUS:** FAIL unconditional P25-to-full-gate extension under every potentially source-compatible wire merge; PASS original-Q counterpolicy and direct extraction of source arity mismatch; **UNCLEAR/HUMAN_REVIEW** real author FHE.EvalGate compiler, full original Ring-R1CS/SNARG. Direct PCS/FS integration P05–P22 stays PARK. No original-author published cryptographic attack claimed.

## Read-before-write

Read START_RESEARCH_SESSION.md SHA 6235e9d376a8b143719a40178132f02a6a41d4f3; RESEARCH_PHILOSOPHY.md SHA 49da3f7fa3e75f502525482ce4a7ab6867; AGENT.md SHA b3e73b2c7f852c05aa674dd97b632e9f99ac5f22; separate STATE.md SHA 3b83237bc5aba4a77479b09dc1f3ac8bccaebc7c (independent vFHE V42; not edited); P25 findings/pvfhe-P25-compiled-gate-io-bit-witness-sharing-gate.md SHA 27bd63328f3ae749e3afbd0d7c78b82da0a5e354; P24 SHA e42ccdb5d6afea79a98aeb0df5bf3fd2e61b0e92. P26 target absent before writing. No earlier findings or parallel state modified.

Original primary source Huang–Li–Mao–Zhang, Fully Homomorphic Encryption with Efficient Public Verification, IACR ePrint2024/1764. Original mirrored **29-page full PDF** via Research MCP SHA256 7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089 VERSION_UNVERIFIED, inspected physical pp13–17 and 26–27. Independently ePrint indexed PDF text https://eprint.iacr.org/2024/1764.pdf confirms extracted source formula at PDF physical p17; attempts to fetch official PDF rendered screenshots at pp15 and17 FAILED cache miss. Without source binary render do not certify the latest edition's exact typography. No original FHE gate compiler is available here.

## ONE hypothesis and decisive test

**HYPOTHESIS P26:** The self-XOR local P25 alternate satisfying 54-bit BitDecomp and public output can be grafted into the original whole FHE gate for ANY plausible Appendix C.3 value-based variable-sharing/bit-arity interpretation. Particularly, no sharing of Coeff, KeySwitch and XPow auxiliary bits can block the graft.

**FALSIFIER:** Inspect original specified bit arity in Lemma4.5 and Lemma4.11 proof and provide one original-Q Coeff/KeySwitch wire-sharing policy in which the P25 alternate KeySwitch word is incompatible with the original zero coefficient; separately check XPow shared-bit effect while holding honest ACC. Distinguish a genuine source claim from hypothetical compiler policy. Do NOT rerun switching-key random masks; P25 already generated 755 exact sparse terminal R1CS rows.

## Original-source contract [FACT]

- Source p15 Lemma4.5 BitDecomp(y; x0,...,x_ell) has inclusive **ell+1** bit interface, 3ell+4 constraints. With Q=2^53+5, ell=53 so the source KeySwitch decomposition admits 54 bits.
- Source p16 Lemma4.11 STATEMENT uses N_Coeff=N*N_BitDecomp+2N, suggesting its Coeff uses the same full width.
- **Source p17 Lemma4.11 PROOF**, however, explicitly prints BitDecomp(y_i; x_i,0,...,x_i,ell-1), which would be **ell=53 bits** if read literally. This conflicts with the named Lemma4.5's 54-argument interface and its constraints count. It may be an editorial typo or a different intended Coeff gadget; DO NOT claim the genuine author compiler uses shorter coefficients.
- Source p27 AppendixC.3 only instructs merging variables representing the same circuit value. It does not identify which helper bits across DIFFERENT gadget invocations are the same SSA wires. Equality of source coefficient values in an honest run is not by itself equivalence of hidden decomposition witness variables.

## Exact Q arithmetic, all checked [DERIVATION]

Let B=2^53, Q=B+5, N=2048, X^2048=-1 in source R_Q. P24 self-XOR gives extracted a0=0 without assumptions on KSK/ACC randomness. The original 54-bit KeySwitch bit vector may represent integer 0 (all bits0), or Q (ones at j=0,2,53). Both reconstruct a0=0 modulo Q and satisfy the original bit Booleanity.

Policy A: **Coeff53 helper bits distinct from KeySwitch54 helper bits**. Coeff53 zero is all-zero; KeySwitch54 alias Q is allowed. PASS the local graft.

Policy B: **Coeff54 and KeySwitch54 share ALL 54 helper bits**. Both accept Q=0 mod Q. PASS. This corresponds to the explicitly generated P25 755-row model.

Policy C: **Coeff53 and KeySwitch54 share their first 53 helper bits**. Coeff53 zero constrains sum_{j=0}^{52} 2^j c_j=0 modQ. This nonnegative integer sum is <2^53<Q. For actual source R_Q CRT decomposition into 2 fields, idempotent-bit equations also imply the same per-component inequality, so all low53 bits MUST be zero. The fake alias sets bits0 and2 to one, giving low53 sum5 and hence violates Coeff(y0=0). With low53 zero, the final KS top bit alone gives 2^53 which is nonzero moduloQ; no fake remains. **FAIL the P25 alias under this hypothetical sharing policy.** No claim authors use Policy C.

Policy D: **XPow(0) and KeySwitch(0) share all 54 helper bits**, with the honest XPow output held 1 in ACC.Update. Fake alias Q makes XPow yield X^Q = X^5 because Q modulo 2N=5, not 1. **FAIL the unchanged-honest-ACC splicing under that hypothetical sharing policy.** This does not disprove all possible modified ACC witnesses.

A further distinct **source-arity warning**: Literal Coeff53 has max unsigned bit sum 2^53-1, so cannot represent the FIVE legal canonical Q residues 2^53,2^53+1,...,2^53+4. This is a possible source-level completeness issue ONLY if the literal 53-bit interpretation is confirmed as the actual construction. The statement's 54-bit budget and the lack of rendered edition/author compiler prevent calling this a confirmed source vulnerability.

## ONE executed source-typed minimal test

Self-contained script uses original Q and exact Booleanity/modular equality to test ALL four policies and exact XPow exponent residue. The results are:

- distinct Coeff53 / KS54 auxiliary bits: PASS alternate;
- distinct Coeff54 / KS54 auxiliaries: PASS;
- fully shared Coeff54 / KS54 bits (P25): PASS;
- shared Coeff53 lower53 / KS54 bits: **FAIL**; forced Coeff value becomes5 rather than0;
- fully shared zero-XPow54 / KS54 bits holding honest ACC rotation: **FAIL**; X^Q=X^5!=1.

It also models DAG source-wire identity distinct from auxiliary-bit identity and checks the five high-residue gap. **No full source accumulator polynomial, all per-gate A/B/C, CMNW PCS or SNARG proof executed**. Any source-N vs q/2 invocation counts in the script are illustrative, not authenticated exact compiler counts (P17 parameter warning).

Reproducibility:
- Python /mnt/data/pvfhe_p26_bitwidth_wiremerge_contract.py SHA256 **3d0ea5561766ad3cbfcd0e0d85b6a2516ce5ec1dfc6938247fda5b4625252895**.
- JSON /mnt/data/pvfhe_p26_bitwidth_wiremerge_results.json SHA256 **bf7852704f79850fe604169678288bccd6459a1ece8dc21d665e9ae5d916639b**.
- Local full markdown report /mnt/data/PVFHE_P26_Bitwidth_WireMerge_Source_Contract_Gate.md SHA256 **ea181d405c1e15e4c1969e5a110b92c78fed6a2dec1d3f76e9489844aa51ab96**.

## End of iteration / recommended PI decision

**STATUS:** FAIL claim the P25 witness necessarily extends under any global gadget bit arity/merge choice; PASS exact source-Q counterexample against universal graft and positive conditional SSA/full54 cases; full theorem/snarg HUMAN_REVIEW/UNCLEAR.
**RESULT:** Previously P25 tested 54-bit Coeff/KS sharing. The source Lemma4.11 proof uses a different ell-bit signature, which if actual and combined with low-bit wire sharing kills the alias. But Coeff53 cannot cover five valid high Q residues and contradicts its own declared interface/count, so source does NOT tell us which actual compiler policy holds. Two conditional cases must not be conflated with proof of a current-author erratum or live exploit.
**NEXT_ACTION (P27 only upon PI continuation):** source-artifact or authenticated-render arity/SSA-wiring gate: obtain author full gate compiler or visually authenticated printed lemma and inspect whether Coeff/KeySwitch/XPow decomposition helper wires are shared and whether Coeff is 53 or54 bits. If unavailable, PARK complete FHE.EvalGate/SNARG exploitability and prepare HUMAN_REVIEW package; do not generate another random-key toy or reopen parked PCS/FS security integration.
**STATE_UPDATE:** YES only this standalone P26 file; global STATE.md and independent vFHE/SHIP/P01–P25 untouched.
