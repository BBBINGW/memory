# vFHE V32 COMPANION — Canonical MLE weight lifting breaks external-field product evaluation

**Date 2026-10-15. NOT a second V32 or V33.** The authoritative already-completed V32 `findings/vfhe-v32-public-y-cp-glue.md` builds an explicitly INSECURE small-group executable Pedersen-bit / OR-Schnorr / native F.2 public y cross-characteristic link and finds huge naive costs; it remains PRIMARY with V33 NEXT and GLOBAL general FHE I192 frozen. This is a separate source-grounded falsifier for ONE proposed shortcut in making the representative link cheaper.

## Primary hypothesis H-V32C [FAIL]

Given the original source F.1 authenticated native representative field evaluation `y = MLE(h)(u)` and one prebound canonical integer vector `a_b∈[0,beta−1]`, the required true integer quotient relation for a basefield coordinate is `Σ_b a_b * lift_p(chi_b(u)) = lift_p(y)+p*k`. Can its public weight MLE over an independent external proof field `F_r` be evaluated by merely lifting each of the native multilinear Lagrange factors and multiplying, in O(ell) time, allowing a cheap external sumcheck `Σ_b A(b)C_u(b)`? **NO**. The canonical residue lift `lift_[0,p−1](xy mod p)` is NOT multiplicative over F_r. The scalar outer sumcheck must authenticate the external MLE of the **per-Boolean-index canonically lifted coefficients**, not the multilinear MLE of a different product expression.

## Original paper and scope [FACT]

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes* (CRYPTO2025/ePrint 2025/286), source Research MCP verified **inspected** 52pp mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, **VERSION_UNVERIFIED** vs latest 2026-02-16 revised ePrint. §3.1 physical p10 CRT extension-field parameters p=1+(2N/d)*odd; §4.3 pp20–23 small digit range and original range PIOP; §2.2 p9 standard ring sumcheck; Appendix F.1 p50 native factor PCS and F.2 p51 Merkle/RS authenticated evaluation. The cross-characteristic public weight sumcheck is OUR potential optimization, not a theorem/design in original source. Precursor conditional V31 link `findings/vfhe-v31-transitive-representative-link.md`.

## ONE decisive exact counterexample [PASS test / FAIL hypothesis]

Legal source shape `N=4,d=2,p=13=1+4*3,ellstar=2,beta=4,2^ellstar=4<p`. Basefield native query `u=(2,2)`. Matrix of canonically lifted native Boolean coefficient weights:
```
C = [[ 1, 11 ],
     [11,  4 ]]
```
Determinant `−117=−9*13`, so `rank_(F13)(C)=1` (expected native product) but `rank_(F1009)(C)=2` after **entrywise canonical lift**. At external challenge `z=(3,5)`, the CORRECT externally interpolated value is `MLE_F1009(C)(z)=835` while the erroneous product of lifted separate native factors gives `684`. Hence the naive public verifier checks a different polynomial and breaks candidate proof correctness, despite an honestly committed vector a.

Exact legal source-form stress with same `N=4,d=2,beta=4`, `2^ellstar<p`, and `p=1+4*odd` prime. Flatten coefficients across two equal bit blocks, compute exact Gaussian-elimination rank over native Fp versus external F1000000007:
| ellstar | p | rank mod p | rank of lifted table mod external |
|---:|---:|---:|---:|
| 4 | 29 | 1 | **4 / 4** |
| 6 | 101 | 1 | **8 / 8** |
| 8 | 269 | 1 | **16 / 16** |
| 10 | 1061 | 1 | **32 / 32** |
| 12 | 4133 | 1 | **64 / 64** |

All chosen p satisfy source odd quotient and min table size assumptions. The direct source toy no-wrap envelope `3*2^ellstar*(p−1)` fits F1000000007 for each run, so this is a genuine separate-characteristic lifting phenomenon, not an accidental small external modulus wrap.

**Precise structural consequence:** A flattened lifted table of rank R requires at least R outer-product terms across this particular half-variable partition. Thus a single (or constant small number of) separated tensor products cannot express these examples. This is **NOT** a universal arithmetic-circuit, public-coefficient-evaluation, proof-size, cryptographic lower bound, nor evidence of author-side published flaw; alternate quotient/carry-aware algorithms or authenticated oracles remain possible.

## Research decision

**KILL/PARK only the naive lifted-Lagrange-factor shortcut**; not the authoritative V32 Pedersen/public-y CP experiment and not the entire cross-prime construction. A sound efficient external sumcheck needs a PUBLIC evaluable and authenticated coefficient polynomial whose Boolean values are the actual canonical `lift_p(chi_b(u))`. Straight enumeration of all H coefficients is expensive, and a clever polynomial/evaluation oracle remains UNBUILT. Our certificate explicitly scopes that obstruction. Source latest published text, end-to-end hiding/knowledge soundness and proof runtime NOT established; author outreach requires PI.

**STATUS:** FAIL H-V32C cheap product-weight external sumcheck; PASS exact ranks and direct evaluation counterexample. Full vFHE repair UNCLEAR/HUMAN_REVIEW.
**RESULT:** Per-index canonical lifting destroys the factorization that the original native MLE evaluator relies on, even though original native reduction remains product structured.
**NEXT_ACTION:** Authoritative V32 remains V33 NEXT: evaluate a truly succinct secure aggregated bit-range/vector commitment for public-y native F.2 CP, or PI HUMAN_REVIEW. If revisiting the companion, test ONE concrete verifiable canonical-coefficient oracle / carries algorithm first, not more conditional random folds.
**STATE_UPDATE:** COMPANION ONLY; main V32 complete/V33 next unchanged; global I192 frozen.

**Exact local report:** `/mnt/data/VFHE_V32_Canonical_Lift_Tensor_Rank_Gate_2026_10_15.md`, SHA256 `2b598199997c2854936b7e08c01a431a7c9f6907b181b313789b951c548a7bd4`.
**Script:** `/mnt/data/vfhe_v32_canonical_lift_tensor_gate.py`, SHA256 `f173a6423d18351ad349002f55aaf2ca8cc26546daefc352c871b39e1a86e64f`.
**Exact JSON:** `/mnt/data/vfhe_v32_canonical_lift_tensor_results.json`, SHA256 `76a815c3c4b48a1163f9fe7c5e328d7ea276b6ead7d4fcf97d878ecbb227137e`.
