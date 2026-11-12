# BOOT / B158_OVERALL — Successor substantive Research Turn 21/25
Date 2026-11-12 Asia/Singapore
TRACK_ID=BOOT
ACTIVE_SUBLINE=B158_OVERALL
PHASE=PROBLEM_SELECTION
CANDIDATE_ID=boot-b158-fixed-logq-small-qmodt-inverse-si-tensor-rescue-v1
FINAL_STATUS=PARKED
VERDICT=FAIL_INVERSE_FACTOR_IS_METADATA_NOT_TENSOR_GAIN
RESEARCH_FRONTIER_EXHAUSTED=false
NATIVE/CODEX=NOT_RUN
VALUE_REVIEW_COMPLETED=true

## Authority / read before write
At entry controller ACTIVE=UNKNOWN, no backed-up candidates; this is a distinct hypothesis, never an extension/reopening of an earlier parked candidate.
Factual read from GitHub repository BBBINGW/memory:
- findings/boot-b158-successor-turn20-guard-gap-phase-translation-zero-root-elision-gate-2026-11-12.md, verified blob 32f1210d1d2d2bc8da719b8eef6609d9503b5990; PARKED.
- findings/boot-B175-source-level-si-error-bounds-2026-10-29.md, verified blob c75aa60e080b28b688de7ee8859c5df4d1951c02; B175 terminal SI needs 664 bits, Q level bitlength649; tensor/reference dominant; quant+relin bounded much smaller.
- findings/boot-B175-hybrid-selector-pareto-screen-2026-10-29.md blob f12765dd3d2526bf9f9d5ae8771621aa184862c3; no validated redesign among 43 selector-subcube circuits and 2 optimistic classes, no whole-system proof.
- findings/boot-b158-successor-turn15-plaintext-scale-tagged-mask-numerator-value-ceiling-2026-11-12.md blob db0c2fd47cd334bb95cda93a5ae5482c29159395; standard BGV plaintext scale-tagging not standalone 16bit fix.
Primary code: Lattigo tag v6.2.0, schemes/bgv/evaluator.go verified Git blob 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f, lines 897–989, 991–1069.

## Closest prior art, exact proposed delta
Baseline B175 uses N32768, T65537, Q level18 bitlength649, output scale
 sigma_out=43352*43178*44421 mod65537 =30059,
 where k=(-Q modT)^(-1) modT =44421.
Candidate suggests selecting a DIFFERENT 19-limb RNS-Q prime set, with no increase of bitlength Q or nominal ring dimension/security, such that (-Qnew modT)^(-1) has a SMALL centered representative (ideally 1). Claim: the apparent nearly 16-bit multiplier 44421 is amplifying dominant tensor/reference noise, so eliminating its integer magnitude directly supplies the missing ~16 required-logQ bits. This is not Turn15 plaintext scalar mask tags (different input scale scheduling), Turn10 terminal affine recenter (different messages/carry), or closed Turn5 non-secret ModRaise (not changing level/Q length or decrypting Q-carry). Distinctness holds but the claim must be checked before new prime search.

## Pre-registered decisive source/value gate, conditional decisions
QUESTION: Does the explicit 44421 inverse factor enter source ct×ct tensor coefficients as a large integer multiplier that can be reduced by choosing a fixed-bitlength Q with (-Q modT)^(-1)=1, thereby recovering the observed B175 >=16 bits of required-logQ at the complete final-output level?
CURRENT_BELIEF: No. Source formula lists inverse as output scale metadata, not an integer amplification of tensor coefficients. Changing Q prime set does change integer modulus geometry and carry and could affect actual noise, but 44421->1 alone does not establish any corresponding gain.
CHEAPEST_DECISIVE_TEST: Check the exact tagged Lattigo MulRelinScaleInvariantNew / tensorScaleInvariant source, trace all uses of inverse factor, identify actual tensor/reference and quantization operations; compare with authoritative B175 residual attribution. No native, no hypothetical prime search.
IF_PASS: If 44421 explicitly multiplies tensor/ref ciphertext coefficients, retain ACTIVE for a fixed-bitlength source-valid NTT-prime CRT search, exact legal domain + correctness canary, security, DFR and all-in value.
IF_FAIL: If 44421 is only used for output scale metadata, PARK this exact small-inverse-as-16bit-tensor-rescue claim; do NOT assert other fixed-Q prime optimization is impossible.
IF_UNCLEAR: If hidden computations use it indirectly, keep mechanism UNKNOWN, audit exact code first; do not infer deterministic 16bit gain or run native.
WHICH_PAPER_GATE_CHANGES: source feasibility of central tensor/reference mechanism and optimistic 16bit noise/value rescue; exact full-output semantics/security remain prerequisite.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: A prime-search/native experiment is unjustified if the proposed nearly 16bit gain is a misinterpretation of modular metadata. PASS would change decision to material source-level optimizations; FAIL archives it and reprioritizes without retesting small patches.

## Source inspection and mathematical decision
Lattigo schemes/bgv/evaluator.go:
- line 897: tensorScaleInvariant computes (ct0 x ct1)*(T/Q).
- lines 927–951: modUpAndNTT, tensorLowDeg, quantize three degree-2 components.
- lines 953–973: relinearization after quantization.
- line 975: opOut.Scale = MulScaleInvariant(params, ct0.Scale, tmp1Q0.Scale, level).
- lines 980–989: MulScaleInvariant calculates output scale = a*b / (-Q[level] modT). This is where inverse 44421 is computed, on the Scale field.
- lines 991–1000: modUpAndNTT uses basis extender from Q to QMul, with no 44421 multiplication.
- lines 1050–1069: quantize uses ModDownQPtoP, ModUpPtoQ, MulScalar(PlaintextModulus=T), then NTT; no multiplication by 44421.

Therefore within this source implementation **the inverse factor is never explicitly multiplied into ciphertext tensor coefficients**. It corrects metadata associated with the BFV-style T/Q arithmetic and the modular scale law. A modular residue in F_T has no canonical archimedean 16-bit noise-amplification interpretation; integer 44421 is equivalent to -21116 modulo 65537, and changing the plaintext decoding scale can change the reference embedding and carry. One cannot infer that assigning k=1 decreases any centered R_Q residual by factor44421 or recovers 15/16bits.

Critical qualification: changing the product of RNS primes Q to enforce (-Q modT)^(-1)=1 DOES change the entire physical Q modulus, centered coefficient representatives, CRT basis-extension, P/Q quantization and potentially the noise/carry geometry. This audit DOES NOT prove identical noise distributions, impossibility of all Q-specialization, unchanged security, nor a universal invariance theorem. There is no source-supported monotonic relation from smaller centered representative k to the dominant tensor/reference term; actual gains require a separate new mechanism and correctly matched full-Q experiments.

Even if one selected primes q_i ≡1 mod2N and similar bit widths while arranging the product Q modT to be -1, that mathematical residue condition is NOT a correctness/DFR certificate or a whole-system value result. It may affect RNS arithmetic, evaluation keys, memory, and hardness/security through Q parameters. None was verified/benchmarked. Also p=T=65537, its residue group is a field, and output 30059 is already consistent with reference scale law; there is no hidden metadata mismatch to repair.

## Value review and decisions
Because repeated low-value local patch candidates have been parked, this Turn21 includes explicit VALUE_REVIEW. All-in:
- true bottleneck: B175 required bits664 at Q bitlength649, 32767/32768 mismatches; actual largest tensor/reference residual bitlength647;
- source-certified quant error <2^46 and relin <2^22, insufficient alone;
- inverse residue k44421 is scale metadata, NOT independently an integer noise gain;
- to create a paper-worthy algorithm/system require whole-output correct at same security/noise budget, a new reduction in tensor/ref carry or low-headroom GROUPED noise, all conversion/keys/offline costs counted and independent novelty.
Result of review: no viable path from the proposed sole k-residue trick. The candidate is PARKED, no ACTIVE candidate or ranked BACKUP retained. Other BOOT/B158_OVERALL structural representation or source-specific tensor geometry questions remain not proven exhausted; research_frontier_exhausted=false and no WAIT_PI.
No new scientific result about a specific alternative Q was tested. No new native task. No performance claim.

Gate1 exact semantics: output modular-scale formula is sound as documented, but candidate claimed noise gain does not follow. Gate2 source: explicit inverse only Scale field; FAIL_TARGET_MECHANISM. Gate3 optimistic value: FAIL because zero evidence 16-bit tensor rescue and changed Q incurs full security/reference re-audit. NOVELTY_STATUS=PREFLIGHT; PAPER_READINESS=NOT_READY.
ELIMINATED_UNCERTAINTY: Is inverse output scale 44421 an explicit ~16-bit amplitude multiplier inside Lattigo BGV SI tensor that can be set to 1 to recover the whole B175 deficit? NO. Verified by source operation dataflow.
REOPEN_CONDITION: Supply a distinct source-proven Q-prime-selection mechanism explicitly relating a constrained Q mod T or CRT/carry distribution to actual E_tref and >=16-bit improvement, with complete fixed-security and full-output correctness, matched noise/DFR, key/offline costs, and independent novelty; small output Scale by itself is not such evidence.
