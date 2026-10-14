# PVFHE-P17 — Real compiler trace source gate; N-versus-q/2 concrete count correction

**2026-10-15 Asia/Tokyo. Independent PVFHE P17 COMPLETED; P18 NOT STARTED.**
**STATUS:** UNCLEAR/HUMAN_REVIEW actual FHE witness allocation, R1CS rows, matrix padding and lattice PCS runtime; **FAIL** assertion that P15's K=9217 and 2.18% constitute unique, validated source-concrete counts; **PARK** concrete compact-witness speedup pending author trace. No attack on original paper or experimental performance improvement claimed.

## Read before write and verified sources
Read START_RESEARCH_SESSION.md SHA 6235e9d376a8b143719a40178132f02a6a41d4f3, RESEARCH_PHILOSOPHY.md 49da3f7fa3e75f502525482ce4a7ab6867, AGENT.md b3e73b2c7f852c05aa674dd97b632e9f99ac5f22, separate STATE.md e6c16fd28fb14de6bf71426e6909497ad74e990a (concurrent vFHE V34), findings/pvfhe-P16-compact-masked-witness-layout-gate.md SHA e772258c0b9fec05972cc8708f4d33accd166b2a and P15 d2189d2db7455b8a0fd5fe56cca37693d3265bb3. Destination P17 absent. Do NOT edit parallel SHIP/vFHE STATE or prior P-series notes.

Primary original: Huang, Li, Mao, Zhang, *Fully Homomorphic Encryption with Efficient Public Verification*, ePrint 2024/1764, 29 physical pp, acquired through Research MCP mirror SHA256 **7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089**, VERSION_UNVERIFIED. Detailed source physical §4.1 p12, GINX accumulator/KeySwitch p13, Appendix B p26, Appendix C.3 p27, Appendix D pp28–29. Original ePrint landing https://eprint.iacr.org/2024/1764, author sites https://mimihuang.github.io/ and https://sparkmxy.github.io/. Web screenshot attempts original pp12,27–28 returned cache miss; latest PDF rendering parity not verified. Targeted GitHub repo/code and web paper-title searches found NO usable paper-specific author compiler or complete quantitative wire/row trace in the searched sources. This is NOT global proof of code absence; unrelated ringSNARK/Rinocchio code cannot be substituted.

## ONE smallest falsifiable hypothesis / decisive test
**[HYPOTHESIS P17]** The available paper and accessible author code provide sufficient complete instance-level dimensional data for Appendix B parameters to determine actual private occupied witness count W, total rows R_actual, padded square dimension m, and the P16 aligned masked-face fit condition W+nextpow2(K+1)<=L, without a hypothetical occupancy assumption.
**[FALSIFIER]** Source-read precise N versus q/2 convention and seek original executable compiler/trace; test whether the 9217 count is uniquely source-instantiated at N=2048,q=1024. If not, mark real packing saving unverified rather than fabricate measured W or speedup.

## New technical evidence [FACT and interpretation]
- Source §4.1 p12 explicitly says N multiple of q/2 and “WLOG N=q/2” for its SIMPLIFIED construction.
- Source Appendix B p26 says concrete N=2^11=2048 and q=1024, so N=4(q/2), NOT that assumption.
- §4.1 accumulator p13 extracts indexed a_0..a_{q/2-1} but describes a length involving N, while KeySwitch key has indices N; Appendix C.3 p27 literally calls KeySwitch N=q/2 bit decompositions and uses N in coefficient extraction count.
- Theorem4.12 and AppendixD establish big-O complexity and matrix commitments but NOT the complete actual private wire allocation/padding for a concrete gate. No faithful mapping from §4.1 simplified gadget to Appendix B larger ring degree was verified this round.
- Thus P15 replacing **every** N in the operation ledger by 2048 is an INTERPRETATION, not verified as the precise concrete Appendix B circuit. This is NOT evidence that authors' entire construction is wrong; lifting/truncation or padding may reconcile it, but requires specification/implementation.

## ONE actually executed source-scope comparison [DERIVATION, test]
Under the SAME source symbolic gadget formulas for ell=53,n=q=1024, two independently ambiguous coefficient-count convention slots are considered. Four scenarios are COUNTERFACTUAL alternatives, **not all implementations or a proof that any one is correct**:

| keyswitch coefficients | extraction coefficients | source-style K BitDecomp | face B=nextpow2(K+1) | source-style nonring rows |
| 512=q/2 | 512=q/2 | **4609** | **8192** | 1450692 |
| 512=q/2 | 2048=N | 7681 | 8192 | 1957572 |
| 2048=N | 512=q/2 | 6145 | 8192 | 2026692 |
| 2048=N | 2048=N | **9217** | **16384** | **2533572** |

The P15 figure K=9217, B=16384, original nonring rows 2533572 and +55303 repaired rows is reproducible ONLY under the last substitution, not uniquely fixed by quoted source equations with the actual Appendix B N>q/2. The P15 claimed 2.18% is similarly conditional. P16's purely algebraic face proof and condition W+B<=L remain valid for any correctly determined K; concrete face width and real savings UNCLEAR. Moreover real W, R_actual and matrix padding m remain uncomputed even if K were fixed.

Reproducible actually RUN script and output (NO full compiler or speed benchmark):
- /mnt/data/pvfhe_p17_source_parameter_scope_gate.py SHA256 **d1b21304e17730df5fe2d7ece8f3a84c3eafa21c240ccdd8d257b3cb8da64ad7**
- /mnt/data/pvfhe_p17_source_parameter_scope_results.json SHA256 **cc49fd95db429e6289ffa9f2957fa0001febcd014fe0ad8a27f20da334f7e003**
- /mnt/data/PVFHE_P17_Source_Compiler_Trace_And_N_Scope_Gate.md SHA256 **16db040a2219bf6f1f87722722b9af02659a177b05fdce4052b73aca0ba9260e**

No R1CS gates were newly generated, no ring-SNARG PCS executed, no speed measured and no claims of concrete source-author actual K based on alternatives.

## End of iteration
**STATUS:** UNCLEAR/HUMAN_REVIEW source concrete witness/row/padding information; FAIL unique source-backed P15 actual K=9217; PARK concrete performance branch.
**RESULT:** Published simplified N=q/2 conflicts with numerical Appendix B N=2048,q=1024; no usable author compiler trace found in targeted sources. Source supports asymptotic P13–P16 design but not real mask-packing overhead. Prior P15/P16 numerical figures must be read as assumption-dependent, without overwriting historical records.
**NEXT_ACTION PVFHE-P18 ONLY after PI continuation:** Stop padding/geometry toys. Attempt one source-grounded prechallenge-anchor **Fiat–Shamir adaptive full-opening knowledge extraction** gate against actual CMNW 2024/281: prove transcript prefix soundness and ROM composition or pinpoint exact missing hypothesis. If not possible, HUMAN_REVIEW/PARK complete PCS repair; QROM still separate.
**STATE_UPDATE:** YES only NEW P17 finding; NO shared state or previous P01–P16 edits.
