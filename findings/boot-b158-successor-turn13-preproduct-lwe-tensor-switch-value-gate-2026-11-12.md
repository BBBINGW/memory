# BOOT / B158_OVERALL — Successor Research Turn 13/25
Date: 2026-11-12 Asia/Singapore
Phase: PROBLEM_SELECTION
Candidate: boot-b158-preproduct-lwe-tensor-merge-v1
Decision: FAIL_ORDINARY_LWE_TENSOR_SOURCE_VALUE / PARKED
No native/Codex execution.

## Read-before-write authority and scope
TRACK_ID=BOOT; ACTIVE_SUBLINE=B158_OVERALL. Controller ACTIVE UNKNOWN, backups none. Inspected and independently verified:
- Turn12 findings/boot-b158-successor-turn12-terminal-degree2-tensor-extraction-value-gate-2026-11-12.md blob 1b243b5d1a507e6fb526326480057405bd5dfc25, PARKED;
- B175 findings/boot-B175-audit-direct-si-pointwise-noise-failure-2026-10-28.md blob a9e8fe850c86a77717836ad414f8b6192290dd9; archive SHA256 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa;
- B176 findings/boot-B176-ordinary-dual-lineage-typed-merge-2026-10-29.md blob e1923520a5e94dcc32e570c9872f443d7885a5d4, PARKED for independent *RLWE-lineage* tensor under cross secrets. This candidate is distinct: move both valid operands to extracted scalar LWE **before** their final multiplication, replace the RLWE pointwise SI with LWE-domain tensor under a quadratic secret-power basis. It still must pass the same bilinear noise test; the prior result is relevant but does not establish an LWE source implementation.
- findings/boot-B175-source-level-si-error-bounds-2026-10-29.md blob c75aa60e080b28b688de7ee8859c5df4d1951c02: SI dominant tensor/reference term, quant <2^46 and relinearization <2^22.
B175 fixed N32768, T65537, L18 logQ649, H8192,s8. Both LT8 and GROUPED pass (577,633 required bits); pointwise SI fails (664 bits, 32767/32768 decoded mismatch). Original LWE dimension n2048, secret sparse ternary h512. NOTE: an RLWE coefficient extraction directly yields LWE secret dimension N32768; n2048 is an *optimistically assumed* result of an additional compatible dimension-switching step, not a demonstrated free available interface.

## Pre-registered paper-level gate
QUESTION: Can scalar-extract both successful B175 operands before the failing RLWE SI multiplication and multiply them via an ordinary small-dimension LWE tensor plus conversion, retaining complete 8-block and final-output semantics at fixed Q, while saving enough error or whole-system cost to justify a paper?
CURRENT_BELIEF: No. An LWE ciphertext product changes the secret basis from linear s_i to quadratic s_i*s_j, and ordinary tensoring preserves exactly the input-noise bilinear cross terms. A switch back to standard LWE requires extensive new evaluation keys or another nonlinear conversion. The existing LWE n=2048 is already an optimistic comparison.
CHEAPEST_DECISIVE_TEST: Exact LWE phase-product expansion; count all quadratic secret monomials under same ternary secret (include diagonal s_i²); derive the minimally naive raw symmetric tensor coordinates and compare to B175 one RLWE SI and known noise terms. Do not use native.
IF_PASS: An independently source-backed compressed LWE quadratic-to-linear conversion with correct full-domain message/scale/carry, provable improved error/DFR and positive all-in cost would admit ACTIVE for canary.
IF_FAIL: If ordinary tensoring retains original multiplication cross-error and demands a huge quadratic secret basis plus unsupported extraction/conversion, PARK without native.
IF_UNCLEAR: Preserve UNKNOWN for genuinely novel packed/function-specific quadratic key representations, but do not infer their existence or schedule native tests.
WHICH_PAPER_GATE_CHANGES: complete multiplication semantics, stock typed interfaces, security, noise/DFR, conversion and full-system scientific value.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: Avoiding the failing RLWE SI is valuable only if the replacement LWE product is correct, less noisy and less expensive end-to-end. A raw tensor that merely moves the same bilinear problem to an enormous secret basis is not a viable construction.

## Exact ordinary LWE tensor law
Adopt sign convention Dec_s(c) = b - <a,s> = M_A+e_A, and Dec_s(d)=d0-<dvec,s>=M_B+e_B. Multiply phases:
  (b-Σ_i a_i s_i)(d0-Σ_j d_j s_j)
= b*d0 - Σ_i (b*d_i+d0*a_i)s_i + Σ_{i,j} a_i*d_j*s_i*s_j.
For same secret and commutativity combine off-diagonal terms:
  coefficient(s_i*s_j), i<j: a_i*d_j+a_j*d_i;
  coefficient(s_i²): a_i*d_i.
The resulting natural secret basis is
  1, s_1..s_n, s_1²..s_n², {s_i*s_j:i<j}.
The number of quadratic coordinates is n(n+1)/2. For n=2048, this is 2,098,176, and with linear and constant coordinates 2,100,225. The diagonal terms s_i² cannot simply be replaced by 1: sparse ternary s_i ∈{-1,0,1} so s_i² ∈{0,1}, depending on unknown secret support. A public selector for the secret support is not provided.
For general different secrets it is n_A*n_B cross quadratic monomials; same-secret symmetry is the most favorable conventional model.
The original ideal phase-product error is
  (M_A+e_A)(M_B+e_B)-M_A M_B
 = M_A e_B+M_B e_A+e_A e_B.
The exact same expression occurs in the LWE tensor prior to any re-encoding. Thus no deterministic 16-required-bit fixed-Q improvement is implied by the representation shift. This does NOT prove a fresh secret-switching or nonlinear output-correction scheme cannot improve errors.

## Optimistic cost and type/value gate
For n2048 a raw, UNCOMPRESSED full symmetric-tensor phase representation needs 2,100,225 Q residues per scalar product. Using the B175 649-bit Q, an ordinary fixed-width 82-byte per coefficient storage would use 172,218,450 bytes (approximately 164.24 MiB) per scalar product, not counting ciphertext metadata, extraction, key switches, or output conversion. This is a representation-size example, NOT a lower bound on all compressed schemes or an evaluated implementation. Eight scalar block products would require ~1.28 GiB raw if not packed/shared. Before any LWE multiplication, 8 or many more RLWE-to-LWE extraction operations and a dimension key switch from N32768 to n2048 may be required. Exact source availability and cost UNKNOWN; the existing B175 only creates a BFV-to-LWE output after stages that were not run.
Linearizing to a supported LWE output requires evaluation material for quadratic secret monomials or a different cryptographic conversion. In a straightforward per-monomial key-switch scheme this is 2,098,176 secret-product relations; key material and generated noise must be charged. No standard Lattigo v6.2.0 endpoint implementing the proposed complete LWE×LWE tensor under n2048 plus BFV-to-LWE compatible relinearization has been evidenced. Stock source type/interface gate therefore BLOCKED/FAIL as a specified ordinary implementation. Plaintext multiplication and arbitrary 8-block aggregation only pass conditional algebra if all conversions preserve plaintext scale/carry.
Closest prior art is generic tensor/relinearization for LWE/RLWE plus the already archived B176 dual-lineage bilinear noise relation. This proposal has no demonstrated novelty beyond relocating an encrypted multiplication. An alternate GGSW/CMux or programmable bootstrap would be a different mechanism, and B176 already screens ordinary three-bit CMux whole costs.
Even before conversion costs, the ideal noise cross terms persist. Therefore no credible >16-bit fixed-Q gain, useful DFR, security assurance or complete value; no native warranted.

## Decision
Gate 1: raw LWE tensor phase identity PASS_MATH, but complete modular scale/whole-output and conversion UNKNOWN.
Gate 2: typed stock LWE multiplication/conversion not established; ordinary quadratic secret basis has >2 million monomials under optimistically reduced n2048.
Gate 3: FAIL optimistic value as a B175 FIX because no guaranteed ideal error reduction and substantial extra representation/conversion costs, compared with one RLWE SI.
STATUS PARKED. NEW_MECHANISM=NO_CREDIBLE_NEW_MECHANISM for ordinary preproduct scalar LWE tensor.
REOPEN_CONDITION: Source-backed compact LWE product/relinearization or nonlinear selector mechanism, fully correct on B175 legal phases including root zero and 8-block outputs, with verified N32768->n2048 conversion, dominant error/DFR advantage >= needed margin, provably fair key/memory/runtime/offline cost and independently cleared novelty. A naked n² secret tensor or assuming pre-product extraction is free does not qualify.
ELIMINATED_UNCERTAINTY: Does moving the terminal B175 bilinear multiplication into an ordinary extracted n=2048 LWE tensor remove the input-noise cross terms and remain a small stock-output interface? No: exact bilinear error identity and 2,098,176 quadratic monomials; conversion unsupported.
DECISION_CHANGED=true. FRONTIER_CANDIDATES_REMAINING=true, research_frontier_exhausted=false. No native task submitted.
