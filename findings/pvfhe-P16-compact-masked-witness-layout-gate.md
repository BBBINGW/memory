# PVFHE-P16 — Compact selected-Y face in the existing private PCS

**Date:** 2026-10-15, Asia/Tokyo. **PVFHE-P16 COMPLETED; P17 NOT STARTED.**
**STATUS:** PASS source-shaped compact private-face R1CS/MLE algebra; FAIL a claim of unconditional padding savings; UNCLEAR source's actual private wire/row occupancy, lattice PCS runtime, full vFHE compilation and ROM/QROM security. This is NOT a measured optimization or completed SNARG.

## Read-before-write and original source

Read START_RESEARCH_SESSION.md SHA 6235e9d376a8b143719a40178132f02a6a41d4f3, RESEARCH_PHILOSOPHY.md SHA 49da3f7fa3e75f502525482ce4a7ab6867, AGENT.md SHA b3e73b2c7f852c05aa674dd97b632e9f99ac5f22, global STATE.md SHA e6c16fd28fb14de6bf71426e6909497ad74e990a (**independent vFHE V34; DO NOT EDIT**), prior findings/pvfhe-P15-full-constraint-count-succinctness-gate.md SHA d2189d2db7455b8a0fd5fe56cca37693d3265bb3, and P14 SHA fc0613aa8a890dbd39b904207172f73d92b7374b. P16 destination absent before write; no old findings overwritten.

Original Huang–Li–Mao–Zhang, *Fully Homomorphic Encryption with Efficient Public Verification*, IACR ePrint **2024/1764**, Research MCP full PDF 29 physical pp SHA256 **7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089**, VERSION_UNVERIFIED. Source pp15–17 Lemmas4.4–4.11, p21–22 Theorem5.7, p26 AppendixB, p27 AppendixC.3 and pp28–29 AppendixD establish sparse arithmetic R1CS, original N=2048/Q=2^53+5, private-only witness commitment and verifier-known public IO, and matrix A/B/C public preprocessing. Printed AppendixD step12–13 private point arity remains unclear without visually verified latest PDF; no source bug asserted.

## ONE primary hypothesis and one decisive test

**[HYPOTHESIS P16]** Packing only selected original BitDecomp reconstructed values Y_i into a single aligned Boolean FACE of the **already padded PRIVATE multilinear polynomial**, with nonconsecutive original-wire-to-Y mapping bound via explicit Ring-R1CS rows, allows P11 anchor and P12 sigma check via the SAME single private PCS while preserving original public IO and A/B/C MLE, and may avoid P13's full-width W||Y duplication and associated 4x nominal dense-matrix encoding growth.

**[FALSIFIER]** Compile a source-shaped instance with nonconsecutive original wire indices, an aligned face with zero anchor and linked copies, three regenerated actual sparse R1CS matrices and their Boolean/off-Boolean MLE identities. Forge Y=0 without changing W and demand actual row rejection. Independently test the packing boundary W+nextpow2(K+1) <= old private padded L, and matrix-row capacity. If source geometry forces next power-of-two anyway, reject unconditional cost savings.

## Exact candidate layout and necessary/sufficient condition [DERIVED]

Let L=2^d be existing padded private-PCS coefficient capacity; W is the number of occupied old PRIVATE wires **including newly required comparator helper wires**; K is the number of selected reconstructed coefficients to duplicate. Reserve an extra zero anchor. Set B=nextpow2(K+1). Reindex old private wires within the first L−B slots, locate Y[0..K] in an aligned B-slot suffix face, padding remaining Y slots with zeros. In a standard little-endian MLE indexing, Y(r)=F_private(r,1,...,1) where r has log2(B) coordinates and all d−log2(B) high-prefix Boolean coordinates are 1. The anchor is F_private(0,...,0,1,...,1)=0. EVERY Y[j] is constrained by a normal source-compatible sparse row Y[j]*1=W[orig(j)], with orig(j) possibly nonconsecutive. Original FHE rows/public IO are reindexed and updated A/B/C public matrix commitments re-generated. No second private PCS C is needed.

For this simple aligned-face design, EXISTING private dimension suffices **iff** W<=L−B (assuming freely reindexable old wires). Independently the existing square row capacity must satisfy R_actual+DeltaR<=m_old; source real R_actual is NOT known. If either fails, padding may DOUBLE L even for small K. A one-face PCS query is typed as PRIVATE length d, not full PUBLIC+PRIVATE length d+1.

## ACTUALLY EXECUTED one source-shaped exact matrix/R1CS verification

Use original Q=2^53+5 and its faithful two-CRT-field subalgebra F_Q×F_Q⊂R_Q. Toy original padded private capacity L=32 and public branch capacity32; full 64. Twenty genuine old PRIVATE positions are nonconsecutive under 28, with three selected original PRIVATE wires at indices [4,12,19]. Source W4 is nonscalar idempotent e=(1,0); W12=8, W19=3. Face occupies private positions [28,29,30,31]: Y0=0, Y1=W4,Y2=W12,Y3=W19. Source public IO P0=11,P1=1 remains in original public half at full coordinates32–33. **Eight actual sparse rank-one Ring-R1CS rows** include original idempotence/copy/public, three Y-copy links and one zero anchor; each A/B/C row has ≤2 nonzeros.

Results from exact integer modular CRT calculations:
- All eight honest Ring-R1CS residual rows zero.
- Full Boolean A/B/C coefficient encodings independently reconstructed: **12,288/12,288 PASS**.
- Off-Boolean matrix/vector multilinear contraction **36/36 PASS**.
- Independently dense versus sparse A/B/C 12-variate MLE **12/12 PASS**.
- Original AppendixD public/private MLE **12/12 PASS** and 64 Boolean witness coefficients recovered.
- Masked Y-face isolation F_private(r0,r1,1,1,1)=Y(r0,r1): **25/25 PASS**; zero anchor PASS.
- Fraudulent Y_face=0 while unchanged W4=e makes anchor and local sigma test pass but EXACT R1CS rows 3,4,5 reject, proving real matrix link is indispensable.
- Original source-shaped full witness z has arity6 while private committed F has arity5; queries use correct private coordinate length.
- Comparator/source-LWE correctness, real FHE.EvalGate compiler, lattice PCS proofs and Fiat–Shamir/QROM were NOT executed.

## P15 source-counted layout vs true unknown costs

P15 original AppendixB real settings n=q=1024, N=2048, ell=53 yield **K=9,217** BitDecomp sites per EvalGate, repaired strict sparse new rows ≤**55,303** (~2.18% of original **2,533,572** source **nonring** rows), helper wires ≤**36,868** before Y. B=nextpow2(9,217+1)=**16,384**, so selected masked slice has **14** random PCS challenge coordinates. P12 exceptional set E4 requires **4 F_Q coefficients PER coordinate**, i.e. 56 per 14-coordinate r, plus 8 fixed prefix coordinates in the illustrated L=2^22 case. This is not 4 coefficients total. P12 algebraic SZ component ≤14/Q^4, conditional on genuine same-C opening and R1CS enforcement.

**Clearly illustrative hypothetical occupancy (NOT actual compiled FHE):** Set original old-private active wires=R0=2,533,572 and comparator helpers 36,868, so W=2,570,440. L=nextpow2(W)=**4,194,304**, unused padding=1,623,864, plenty for B=16,384. Old full m=2L=8,388,608. Compact full m remains 2L; P13 equal-width duplicated private+public design would have m=4L=16,777,216. Conditional **nominal dense A/B/C interpolation domain ratio** (4L)^2/(2L)^2=**4**. Also illustrative new nonring rows R0+55,303=2,588,875 fit in square row budget m=2L if ignoring UNKNOWN other source ring rows. No wall-clock, SIS, matrix actual memory or packed source full-compilation claim.

**Decisive negative capacity case:** Set W=L−B+1=**4,177,921**. Only B−1 slots remain: aligned selected-Y face CANNOT fit in old L without sharing/restructuring wires. Its next padded private capacity rises to 2L. This disproves any unconditional compact-packing win. Source full-gate W and R_actual are NOT available in original theorem or this repo's source extracts; real cost savings remain **UNCLEAR**, despite proven layout algebra.

## Executed reproducibility

- Python: `/mnt/data/pvfhe_p16_compact_face_layout_gate.py`, SHA256 **e98540f64675dd46dd8bc764702096254a6eddbc9bd30b46f8b57041aff6ef50**.
- Results JSON: `/mnt/data/pvfhe_p16_compact_face_layout_results.json`, SHA256 **0ec8455c80b5246181b0f831da2b1f935601c8544e5fb05c22ae9e3d29d9a4db**.
- Detailed report: `/mnt/data/PVFHE_P16_Compact_Masked_Witness_Face_Gate.md`, SHA256 **b808417badcca282da0acacebc038c0b5191efba2594e8f1845105ef4fd6331a**.
This is one exact matrix-level case and a source-derived symbolic occupancy gate, not a new benchmark or actual lattice commitment.

## End of iteration

**STATUS:** PASS conditional compact one-private-PCS face with nonconsecutive wire links and full toy A/B/C MLE; FAIL claim that a small K always prevents PCS/matrix padding expansion; UNCLEAR ACTUAL original private wire occupancy, row capacity, runtime, full CMNW adaptive FS/QROM security and contribution novelty.

**RESULT:** Equal-width private witness duplication in P13/P14 is not algebraically necessary. An aligned selected-Y face with B=nextpow2(K+1) can consume unused existing padding and preserve one private commitment, while proving all selected values via ONE postchallenge PC.Eval. Savings hinge on private and row slack; cannot be claimed concretely without source compiler data.

**NEXT_ACTION (PVFHE-P17 only if PI continues):** STOP toy geometry and synthetic width sweeps. Attempt to locate an actual original author compiler/parameter trace or source-faithfully enumerate FULL FHE gate wires/rows/public preprocessing to establish genuine W and R_actual. If unavailable, mark concrete layout overhead HUMAN_REVIEW/PARK and prioritize the unresolved full CMNW adaptive FS/ROM/QROM security/novelty. Do not hallucinate measured time.

**STATE_UPDATE:** YES independent P16 file ONLY. No edits to global STATE.md, SHIP/vFHE concurrent state, or P01–P15.