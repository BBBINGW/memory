# FHE research program — integrated thematic map and PI strategy (2026-10-15)

**AUTHORITY:** Cross-series thematic index and historical integration; not a new proof, automatic research continuation, or replacement for the original findings/failures, STATE.md, or the PI. PI has approved strategic pivot to **nontrivial FHE optimization composition obstructions** with source-verified corrective technique and end-to-end cost/noise/security evidence. Context: 2026-10-15; no fresh technical experiment performed in this integration.

## 1. Round provenance and exact indexing (do not renumber)

| Historical workstream | Scope / authoritative location | Last evidenced point | Handling |
| --- | --- | --- | --- |
| Global independent/general FHE I-series | Global historical I1–I192, prior reports spread across findings/, failures/, and logs/. STATE.md freezes I192. | I192 completed, GLOBAL COUNTER FROZEN. | Preserve filenames and prior conclusions; do **not** back-fill unrelated P/T/V rounds as I193+. Legacy I193–I196 labels were cross-identified with V1–V4 in STATE.md; preserve physical filenames. |
| vFHE CRT consistency V-series | findings/vfhe-cross-crt-state.md; findings/vfhe-cross-crt-consistency-research.md and associated V logs/findings | V42 COMPLETED, V43 NOT STARTED, SOURCE_BLOCKED/HUMAN_REVIEW | Canonical vFHE state remains independent; do not overwrite its 116k-char history; source official current ePrint2025/286 PDF unresolved. |
| PVFHE Ring-R1CS/CMNW P-series | findings/pvfhe-P01...P27...md; related source register MISSING_SOURCES.md | P27 COMPLETED, P28 NOT STARTED | Two intertwined but distinct mechanisms integrated below. Root cause/claims kept conditional to original compiler and PCS source versions. |
| TFHE-ISA T-series | failures/tfhe-isa-T01-radix16-program-reliability-scope-gate.md; findings/tfhe-isa-T02-average-accumulator-overflow-gate.md | T02 COMPLETED, T03 NOT STARTED | Retain as low novelty examples / negative prioritization evidence. |
| Earlier OPEN_RESEARCH_BRANCHES P1–P22 | findings/OPEN_RESEARCH_BRANCHES.md is a **separate backlog P-numbering**, not PVFHE P-numbering. | Various branches mostly PARKED/HUMAN_REVIEW (2026-10-14 checkpoint) | Cross-link by underlying topic, never merge by number. |

The visible independent follow-on comprises PVFHE P01–P27, TFHE-ISA T01–T02, with recent P19–P27 nine PVFHE iterations plus T01–T02 eleven recent turns. **Never sum overlapping namespaces into a fictitious count of unique historical experiments.** Repository directory snapshot: findings 252 files, failures 69, logs 11 as of audit; these are file counts, not iterations nor distinct validated contributions.

## 2. Theme A — Publicly verifiable FHE / Ring-R1CS / CRT scalar coherence

### A1. Older global + V-series: source ePrint2025/286
Cross-reference prior global vFHE I59–I151 and corresponding opportunity backlog **P1**, plus V1–V42. Core objection: field-wise CRT digit membership may not impose one globally consistent scalar digit/index. Some ideal or source-shaped counterexamples and conditional field evaluations verified, **not** a confirmed latest-edition proof defect or accepting deployed SNARK forgery. Repairs involving sumcheck batching, Brakedown, masks and communication have multiple separate failed/parked sub-branches. **V42 requires actual latest official IACR PDF bytes; mirror has VERSION_UNVERIFIED.** Keep independent record findings/vfhe-cross-crt-state.md authoritative. DO NOT automatically reopen.

### A2. PVFHE ePrint2024/1764: source-gadget and compilation audit
**P01–P04 initial finding:** under source Q=2^53+5, inclusive j=0..53 modular bit reconstruction does not ensure unique canonical integer digits; algebraic scalar/CRT issues and Galois-based conditional repair proposals investigated.
**P23:** with an aliasable input coefficient, normal independent KeySwitchGen masks make different bit selections give generally different PUBLIC ciphertext masks; this is ciphertext exact-output semantics, not proved different plaintext.
**P24:** honest self-XOR c XOR c yields accumulator extracted mask zero for any legal keys, removing a prior input-distribution premise. Strong local exact-output witness, not global proof.
**P25:** explicitly built a SOURCE-SHAPED 755-row Ring-R1CS terminal subcircuit with Coeff/KeySwitch 54-bit shared wires; both source-valid bit paths satisfy **separate public output statements**; pinning false witness to the honest public output correctly fails. The actual author complete compiler and proof were not run.
**P26:** source Lemma4.11 proof uses Coeff ell=53 helper digits while Lemma4.5 uses ell+1=54; a plausible (but unverified) 53-bit Coeff / KeySwitch low-bit shared-witness policy blocks P25's alias. Other sharing patterns allow it. Thus no unconditional compiler-wide extension.
**P27:** IACR indexed original paper and Research MCP mirror independently exhibit arity discrepancy; 53-bit coverage omits five legal Q representatives while named 54-bit gadget remains noncanonical. No authenticated author FHE.EvalGate→R1CS compiler/wire mapping or current rendered PDF. **SOURCE_BLOCKED/HUMAN_REVIEW/PARK complete exploit**. Source registry: MISSING_SOURCES.md PVFHE-P27 entry.
**Integration decision:** unifies the *problem family* with old V-series under "public-verification scalar/index representation coherence" but DOES NOT equate their threat models, proofs or statement languages. Retain independent P and V rounds and separate published source identities. If an actual compiler arrives, restart only exact dependency on width/wire sharing and full public IO relation. No researcher should describe an accepted SNARG forgery or a security break based on local R1CS alone.

## 3. Theme B — Extractable PCS, nested FS and efficient soundness repair for PVFHE

**P05–P18:** Galois-invariance/fixed-subring repair, commitment/witness linking and source-shaped matrix/row count (P13–P16), plus CMNW PCS relaxed-binding, zero-anchor, classical interactive vs nested FS composition. P17 finds original paper's N vs q/2 concrete row-count inconsistency, so previously advertised overhead is conditional. P18 proves naive FS inner forking changes full anchor and outer hash key; not a no-go for sophisticated nested extraction.

**P19:** read existing adaptive FS/AoK theorem; a stopped-before-outer-RO query approach is possible *conditionally*, but theorem extraction success semantics differ from desired strong bound.
**P20:** 2026 multi-round Gamma special sound FS theorem gives stronger success guarantee, but *its* extraction complexity t_Gamma is not bounded by CMNW source's (xi+1) automatically. Exact small binary Gamma t at xi=4 reaches12 >5.
**P21:** independent rigorous lower bound t_Gamma >= |Sigma|^floor(xi/3) for exact coordinate-star Gamma; original CMNW challenge Sigma={0,1}^kappa and xi=r*kappa -> t >=2^{kappa floor(r*kappa/3)}. Therefore direct efficient instantiation of **that particular 2026 FS theorem** fails in standard growing parameters; neither original PCS unsoundness nor universal impossibility proved.
**P22:** broader rank-F2 Gamma has polynomial t but lacks guaranteed *integer* right inverse (4x4 J−I det−3). Gamma_Z integral-lattice full-generation has t=O(xi² log xi), yet unitriangular 0/1 B_n=I+S+S³ has unique integer inverse with coefficients >=2^floor((n-1)/3); short opening/SIS slack not preserved merely by widening Gamma. Original CMNW proof still uses a sparse ±1 integer right inverse. **PARK PCS/FS integration pending genuinely new short-inverse extraction theorem AND usable t/sampling + ROM/SIS details**.

**Integration with earlier I-series:** compare to old vFHE Brakedown/PCS multi-open cost/batching and CKKS optimization composability only at level of abstract costs; DO NOT transplant soundness as if different PCS transcript/statement structures were identical.

## 4. Theme C — TFHE ISA / PBS / precision / program effects

**T01** source ePrint2024/1201 (full PDF read, 48pp mirrored VERSION_UNVERIFIED): radix16 fastest in source measured workload; Table2 per MVB-tree error bound B4 2^-30 vs B16 2^-23. Conservative union bound changes program-level certifiable operations, but authors ALREADY point out in conclusion p29 that lower DFR may make B4 preferable. **FAIL novelty; PARK**, file failures/tfhe-isa-T01-radix16-program-reliability-scope-gate.md.
**T02** same source: Average Algorithm3 adds encrypted bytes via ADD mod256 (Appendix B.2.2), so true sum>=256 loses carry before average division. Source-level ideal plaintext counterexample [128,128,0,0,0] gives arithmetic 51.2 while accumulator 0. Valid application precondition sum<=255 or wider accumulator. This is elementary program arithmetic, NOT TFHE primitive break or strong publishable novelty; **PASS narrow correctness, LOW NOVELTY/PARK** findings/tfhe-isa-T02-average-accumulator-overflow-gate.md.
**Crosslink:** earlier TFHE/FHEW/PBS I-series, Carousel, alternative PBS optimization, threshold FHE PRSS and LFBS PRCA already have negative/composition and source-version cases in OPEN_RESEARCH_BRANCHES; do not restart simple radix/overflow, tiny LUT rounding or minor error-budget variations absent a new mechanism.

## 5. Theme D — Existing CKKS and matrix-FHE optimization composition

Historically covered in findings/OPEN_RESEARCH_BRANCHES.md and numerous findings/failures:
- CKKS LCR+AKS sparse CtS/StC, Fourier projection, key reuse, I40–45 and I168–169. Existing source ePrint2025/1403 is accessible full text but its known composition attempts and recent ePrint2026/1023 prior art were already screened. **Do not restart same native LCR+AKS / symmetric CtS–StC shortcut** without new premise.
- GL ePrint2025/1935, CKL/MRFHE matrix arithmetic and W-axis/native-right-mul: archived composition obstruction and legal parameter counterexample; GL generic BigSwitch structure intentionally ARCHIVED. Keep theorem semantics and operator-domain mismatch explicit.
- dBFV→BGV, GBFV, Nested RNS lazy-CRT lift, Carousel p∤N LUT radius, generalized CKKS linear transforms, FHEW key-update, LEAF/PRSS and SIMD-ALU have extensive prior negative, repaired, or source-blocked notes; consult original exact path before selecting future hypothesis.
- Algorithmically meaningful new search should pursue **untried** interface conditions, not repeat a previous no-go with cosmetic names.

## 6. New strategic research filter (PI APPROVED)

**Primary thesis:** prioritize meaningful **composition holes** and new FHE-specific resolution rather than continuing a "paper bug hunt" or endlessly generating tiny counterexamples. In particular source-complete CKKS bootstrapping/packing/linear transform and matrix homomorphic arithmetic; possible TFHE/FHEW batching/selector/PBS compatibility if genuinely unaddressed. True novelty requires **one concrete obstruction plus one nontrivial technique** that improves a clearly measured frontier.

A new candidate must have:
1. **Accessible primary source and reproducible definition** of A, B, input/output representation, ring/slot/coefficient, scale, level/modulus, secret/evaluation/rotation keys and freshness; source citation by theorem/algorithm/page.
2. **Early prior-art and author-limits audit**, including previous related I/V/P/T failures. Kill if author already acknowledges/repairs or if the only fix is a sentence, a wider ordinary integer accumulator, an obvious canonical range check, or a loose union bound.
3. **ONE smallest falsifiable composition claim** with explicitly testable obstruction. Example template: Under A, adding optimization B to baseline C fails/succeeds due to X; fixing X with R changes cost Y without violating invariants.
4. **Separate correctness, security and precision/noise/parameter verification**, including key-size, evaluation-key compatibility, level consumption, rotations, memory, NTT/external-product and end-to-end benchmark comparison. Algebraic soundness never implies usable FHE.
5. **Novelty + baseline + importance + evidence** should be stated before accepting a research branch as promising; otherwise PARK with an exact reopen condition.
6. **No silent source substitutions:** if current paper version, original compiler, crucial lemma or official benchmark is missing, mark SOURCE_BLOCKED and stop dependent claim rather than serially inventing toy tests.

Potential future categories—not yet active hypotheses: CKKS bootstrapping/linear-transform with independently optimized scale/noise/key-switch paths, FHE matrix multiplication representation conversion with native transform assumptions, and amortized TFHE PBS/external-product selector generation under realistic key and memory budgets. Prior I-series obstruction and recent papers must be checked first.

## 7. Status ledger / reopening conditions

| Theme | Integrated status | Reopen trigger |
| --- | --- | --- |
| General I1–I192 | HISTORICAL, global I192 frozen | PI selection of new global numbering; no automatic I193 |
| V1–V42 vFHE cross-CRT | SOURCE_BLOCKED / HUMAN_REVIEW | Authentic latest official 2025/286 PDF and fresh theorem audit, PI authorization |
| PVFHE P01–P04/P23–P27 Ring-R1CS local exact-output | SOURCE_BLOCKED / HUMAN_REVIEW | Full original 2024/1764 compiler / Coeff-KeySwitch-XPow wiring and output binding |
| PVFHE P05–P22 PCS/FS repair | PARK | Novel bounded-norm extractor preserving soundness, efficient Gamma/t/sampling, and complete ROM/SIS proof |
| TFHE-ISA T01 | ARCHIVED LOW NOVELTY | New security-grade equal-DFR radix optimization, not acknowledged union-bound observation |
| TFHE-ISA T02 | ARCHIVED LOW NOVELTY | Nontrivial cheaper encrypted carry/aggregation than obvious width expansion, significant runtime frontier |
| CKKS LCR+AKS / GL/CKL etc. | PRIOR RESULTS: mixed archived/source-blocked | One genuinely new interface/technique and exact non-repeated hypothesis |

## 8. Session starting contract

Start with START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, STATE.md, this thematic index and only relevant archived files. The currently PI-selected **strategy** is composition-first; it is NOT yet an identified next paper/one primary hypothesis. When PI selects a specific research problem, start a fresh **separately named** track and choose ONE smallest falsifiable claim and one decisive test; preserve I192 frozen, V42 and P27 source gates. All findings/failures stay in Git history. Research assistant must not claim full 200+ investigations have been reproduced by this mapping: this is a navigational synthesis of repository files, not independent revalidation of all math, security or benchmarks.

**END OF INTEGRATION UPDATE: Strategy PASS (PI direction codified), archival/thematic mapping PASS, new technical research NOT STARTED.**
