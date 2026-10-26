# FHE × ZK — Hoisted KeySwitch Proof-Witness Reuse (Engineering Candidate)

Date: 2026-10-26. Status: **PARKED_ENG_CANDIDATE / NOT_NOVELTY_ESTABLISHED**. This is a **preserved implementation optimization idea**, explicitly retained on PI request; it is NOT a new primitive, theorem, verified speedup, official BOOT/SHIP/VFHE iteration, or permission to run Codex/GPU. The current PI-selected next *research* focus is FHE × MPC (not a retroactive change to the older CGS series).

## Practical problem and supported fact

CKKS linear transforms may rotate one ciphertext by many Galois elements. Lattigo v6 genuinely hoists an RNS Q/P gadget decomposition of c1:

- `schemes/ckks/evaluator.go` function `RotateHoisted` calls `DecomposeNTT(..., ctIn.Value[1], ..., buffDecompQP)` **once before** iterating over rotations, then `AutomorphismHoisted(..., buffDecompQP, galEl,...)` per rotation.
- `core/rlwe/evaluator_automorphism.go` `AutomorphismHoisted`: per-Galois-key `GadgetProductHoisted`, add c0 and apply automorphism.
- `circuits/common/lintrans/lintrans_evaluator.go` `EvaluateMany`: one `DecomposeNTT` reused through multiple linear transforms; lazy pre-rotations may also be cached across transforms.
- Version pinned to the verified GitHub source commit `tuneinsight/lattigo@536d641dbe0c1b29e9819e0bac1f2fa71a10a520`, blob SHAs: `schemes/ckks/evaluator.go@dfac46630ef90b31ed9a6a07e5ce1eef59bef359`; `core/rlwe/evaluator_automorphism.go@527b1fdf8fdd92b705896b555597c9cc40ee2609`; `circuits/common/lintrans/lintrans_evaluator.go@2df240b10b5535def5fe99653e7c5ef82661bd6e`.
  URLs: https://github.com/tuneinsight/lattigo/blob/536d641dbe0c1b29e9819e0bac1f2fa71a10a520/schemes/ckks/evaluator.go ; https://github.com/tuneinsight/lattigo/blob/536d641dbe0c1b29e9819e0bac1f2fa71a10a520/core/rlwe/evaluator_automorphism.go ; https://github.com/tuneinsight/lattigo/blob/536d641dbe0c1b29e9819e0bac1f2fa71a10a520/circuits/common/lintrans/lintrans_evaluator.go

## Candidate proof circuit / engineering optimization [DERIVED; NOT EXECUTED]

For one source ciphertext c and a batch of k rotations, express:

```text
ONE shared authenticated decomposition D := Decomp_QP(c1)
ValidDecomp(c1,D)
AND for each rotation g:
  ValidGadgetProduct(D, evk_g, tmp_g)
  ValidModDown(tmp_g, post_g)
  ValidAutomorphism(c0, post_g, out_g)
```

A baseline that blindly copies each `ValidDecomp` k times could instead commit/check the common witness once and fan it out in a DAG-shaped GKR/PIOP relation. Lattigo's computational hoisting is existing HE technique; vFHE's public PIOP implementation already features shared oracles, virtual oracles, claim DAGs, and generic batch-evaluation primitives. Thus the direct proposal is an **engineering CSE/prover-compiler optimization**, not an established novel cryptographic protocol.

Candidate cost expression **only relative to a naive non-CSE proof baseline**:

```text
C_naive  = k*(C_decomp + C_gadget + C_moddown) + C_other
C_shared = C_decomp + k*(C_gadget + C_moddown) + C_other + C_DAG_overhead
Gross avoided repetition = (k-1)*C_decomp
Net improvement UNKNOWN; might be zero against a modern CSE/BatchFold baseline.
```

**Key caveats:** The different evaluation keys imply per-rotation gadget product results, Q/P residues and ModDown quotient/remainder witnesses generally differ. Shared Decomp does NOT permit omitting those checks. The actual vFHE compiled CKKS circuit may already CSE the expression, and the available repo provides abstraction rather than proof of runtime optimization. Source PIOP doc https://github.com/vfhe/vfhe/blob/main/modules/piop/piop.md ; crypto paper https://eprint.iacr.org/2025/286 ; subsequent batching prior art `Batch, Pack, and Prove` (FHE.org 2026).

## Future optional Codex / engineering gate — PENDING, not approved

Only reopen if PI requests implementation **and** the verified baseline compiler actually duplicates decomposition work. Minimal test: use the SAME ciphertext, rotation set, evaluation keys and CKKS parameters; compare (a) proof DAG with naive duplicated witness and (b) CSE shared witness in the same proof system; require full correctness, boundary tests for Q/P conversion, malicious witness-binding checks and matched prover time/peak memory/proof size/verifier cost. Separate arithmetic work saved from added openings and soundness effects. No promised percentage, no GPU task, no automated GitHub update or formal novelty claim.

## End status

`STATUS: PARKED_ENG_CANDIDATE`
`EVIDENCE: SOURCE_VERIFIED + DERIVED; NATIVE_ZK_NOT_RUN`
`NOVELTY: FAIL_NAIVE / POSSIBLE_ENGINEERING_ONLY`
`NEXT_TEST: ONLY_IF_PI_REOPENS — check if actual proof compiler already shares decomposition and measure cost`
`STATE_UPDATE: THIS_PRESERVATION_NOTE_ONLY; NO_OFFICIAL_ITERATION_CHANGE`
