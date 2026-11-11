# BOOT / B158_OVERALL — Research Turn 22/25
## PROBLEM_SELECTION — same-ring sparse-key pointwise island

Date: 2026-11-12 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_OVERALL
Candidate: boot-b158-sparse-secret-pointwise-island-v1
Phase: PROBLEM_SELECTION
Final status: PARKED
Evidence grade: MATH / STATIC / SOURCE
Native: NOT RUN

## Distinctness

The durable state entering Turn 22 had ACTIVE=UNKNOWN. This candidate is distinct from the recently closed gauge-search, standard-PK rerandomization, programmable-gauge, lazy-relinearization, and leaf-ring sidecar families.

The mechanism keeps the same N=32768 ring and the fixed B175 modulus chain, but introduces a temporary low-Hamming-weight RLWE secret only around the failing LT8-by-GROUPED scale-invariant pointwise multiplication.

## Candidate mechanism

Let the ordinary B175 secret be s and choose a same-ring sparse secret s'. Add one evaluation key s -> s', one evaluation key s' -> s, and one relinearization key for s'.

Before the B175 pointwise gate: (1) key-switch LT8 from s to s'; (2) key-switch GROUPED from s to s'; (3) execute the same scale-invariant ciphertext-ciphertext multiplication and relinearization under s'; (4) key-switch the output back to s.

Intuition tested: the SI quantization residual is decrypted against (1,s',s'^2), so a much smaller ||s'||_1 and ||s'^2||_1 might reduce the late 31-required-bit multiplication increment enough to recover the fixed-Q deficit.

## Registered decisive test

QUESTION: Can switching both B175 pointwise operands to a common sparse same-ring secret provide at least about 16 required bits of deterministic fixed-Q recovery while keeping a source-compatible key/cost profile?

CURRENT_BELIEF: Source typing is feasible, but the ideal phase-level product error is secret-independent. Secret sparsity can reduce only the recombination of componentwise quantization/relinearization errors. The durable B175 source audit already bounds these terms far below the observed residual. The remaining large component-lift/Q-carry geometry is not contracted by secret sparsity.

CHEAPEST_DECISIVE_TEST: Use exact Lattigo v6.2.0 evaluation-key and scale-invariant multiplication source to derive: (i) the phase relation after s->s' key switching; (ii) which SI error terms actually depend on s'; (iii) whether the ciphertext-component distribution gains any deterministic smallness from sparse s'; and (iv) the minimum extra key-switch/key-material cost. Do not run native work unless a source-backed contraction invariant survives.

IF_PASS: If source derivation yields a deterministic sparse-secret-dependent bound capable of reducing the dominant B175 aggregate term by at least about 16 required bits, admit the candidate ACTIVE and run a minimal dense-vs-sparse pointwise canary.

IF_FAIL: If sparse s' only reduces already-small quantization/relinearization terms while the key-switched components remain uncontrolled/uniform-looking and the dominant aggregate geometry has no contraction invariant, PARK immediately.

IF_UNCLEAR: If source equations cannot separate a secret-sparsity benefit from representation rerandomization, do not promote; any remaining benefit must be treated as the already-closed uncontrolled gauge/randomization family rather than renamed as a sparse-secret mechanism.

WHICH_PAPER_GATE_CHANGES: Killer gate (2): source/key feasibility; killer gate (3): optimistic noise/value ceiling.

WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: If the only deterministic effect of sparse s' is to shrink error terms already proven negligible relative to the B175 failure, then three additional key switches and extra evaluation keys cannot be justified. Native behavior would test uncontrolled representation randomness rather than a sparse-secret paper mechanism.

## Killer gate (1): semantic/correctness oracle

Lattigo v6.2.0 core/rlwe/keygenerator.go, blob 3583c5bb72e802a9b338d0d1fc8ba24a9ea58e72: an evaluation key from skIn to skOut consists of gadget rows of the form (-a*skOut + w*P*skIn + e, a).

Lattigo v6.2.0 core/rlwe/evaluator_evaluationkey.go, blob 980d32cae42d770f75a277fcc1fd9f4cf897c8d1: ApplyEvaluationKey applies GadgetProduct to input c1 and adds original c0. Thus if Dec_s(C)=M+e_C, after s->s' switching Dec_s'(KS(C))=M+e_C+kappa_C where kappa_C is the evaluation-key error.

With ideal kappa_C=0, phase is exactly preserved. Semantic gate: PASS.

## Killer gate (2): stock/source feasibility

GenEvaluationKeyNew supports same-ring input/output secrets; ApplyEvaluationKey accepts the degree-one LT8/GROUPED operands; a separate relinearization key can be generated for s'. Required type/key edges exist with no ring-degree or modulus-chain change.

Source/type gate: PASS. Concrete sparse-secret security remains UNKNOWN and would need its own audit only if value survived.

## Exact phase-product invariant

After switching, operand phases are M_L+e_L+kappa_L and M_G+e_G+kappa_G. Before componentwise SI quantization their exact tensor decrypt is
M_L*M_G + M_L*(e_G+kappa_G) + M_G*(e_L+kappa_L) + (e_L+kappa_L)*(e_G+kappa_G).

With kappa_L=kappa_G=0 this is exactly the original ideal phase product. Secret sparsity does not contract intrinsic message/error cross terms.

## Which SI terms depend on secret sparsity

Lattigo v6.2.0 schemes/bgv/evaluator.go, blob 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f: tensorScaleInvariant basis-extends each component to QMul, forms three tensor components, quantizes each separately by about T/Q, then relinearizes c2.

If each component quantization error has coefficient magnitude below T/2, decryption under (1,s',s'^2) yields
||E_quant(s')||_infinity <= (T/2)*(1+||s'||_1+||s'^2||_1).

So sparse s' can shrink this recombination bound. But durable B175 source analysis already bounded, for the original dense secret, ||E_quant||_infinity<2^46 and ||E_relin||_infinity<2^22 while the observed final pointwise coefficient residual has bit length 647 / required bits 664. Deleting those bounded terms entirely from the current execution does not change its failure classification.

This alone is not a proof that a sparse-secret execution fails, because key switching changes ciphertext components and lift/Q-carry geometry. It does prove that the direct deterministic smaller-secret-norm explanation cannot supply the required 16-bit rescue.

## Why sparse secret gives no component-geometry contraction

The same genEvaluationKey source samples each gadget-row zero encryption under skOut=s' with a fresh UNIFORM second component a_j. The row is (-a_j*s' + gadget*skIn + e_j, a_j). ApplyEvaluationKey forms output c1' from decomposition digits and these random a_j values.

Therefore small Hamming weight of s' imposes no small-coefficient, sparse, or otherwise contracted invariant on switched c1'. Component geometry is controlled by random evaluation-key rows and decomposition, not by ||s'||_1.

The large B175 representation-sensitive lift/Q-carry term may change after switching, but source semantics provide no deterministic direction or >=16-bit contraction. Any benefit from the random new representative is an uncontrolled gauge/rerandomization effect already screened in Turns 19-21.

## Optimistic value ceiling

The pointwise ct-ct count is unchanged. Relative to the original gate, this adds two dense->sparse ApplyEvaluationKey operations and one sparse->dense ApplyEvaluationKey, plus separate s->s', s'->s and sparse relinearization key material.

Secret sparsity does not reduce ring degree, Q/P levels or gadget decomposition dimensions. With no deterministic 16-bit contraction invariant, the whole-system value ceiling is negative before timing.

## Decision

FAIL_SPARSE_SECRET_CONTRACTION / FAIL_VALUE_CEILING -> PARKED.

Candidate: boot-b158-sparse-secret-pointwise-island-v1.

No native experiment is justified.

## Reopen condition

Reopen only with a sparse-key switching construction that proves a new representation invariant: after s->s' switching, the relevant B175 ciphertext components or lift/Q-carry term must contract by at least the needed fixed-Q margin with useful probability or worst-case guarantee. Include exact switched-component distribution/bound, sparse-key security, all switch/relinearization errors, B175 DFR/correctness, and whole key/runtime cost after the three extra key switches. Ordinary dense-to-sparse switching, random representation changes, or only reducing ||s'||_1 do not satisfy this condition.

## Eliminated uncertainty

Can a temporary same-ring sparse secret rescue B175 simply because SI quantization/relinearization errors decrypt against a smaller secret?

Answer: No as a paper mechanism. It shrinks only already-small secret-dependent terms; the ideal phase product is unchanged and switched components have no source-backed contraction because evaluation-key second components are uniform.

## Evidence references

- findings/boot-B175-source-level-si-error-bounds-2026-10-29.md; blob c75aa60e080b28b688de7ee8859c5df4d1951c02.
- findings/boot-B175-static-noise-attribution-audit-2026-10-29.md; blob e31ec2cbee6886ca61b6bc721920938d2a8a072b.
- findings/boot-B175-common-lineage-gauge-accessibility-2026-10-29.md.
- findings/boot-b158-turn19-adaptive-zero-codebook-gauge-shaping-problem-selection-2026-11-12.md; blob 98874687b1b314bd0dccf9ff70dc108b81bef810.
- findings/boot-b158-turn21-publickey-linear-programmable-gauge-problem-selection-2026-11-12.md; blob 5312217d62dd714aabed25b0aac0b49cf896d593.
- Lattigo v6.2.0 core/rlwe/keygenerator.go blob 3583c5bb72e802a9b338d0d1fc8ba24a9ea58e72.
- Lattigo v6.2.0 core/rlwe/evaluator_evaluationkey.go blob 980d32cae42d770f75a277fcc1fd9f4cf897c8d1.
- Lattigo v6.2.0 schemes/bgv/evaluator.go blob 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f.
- B175 native artifact SHA256 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa.