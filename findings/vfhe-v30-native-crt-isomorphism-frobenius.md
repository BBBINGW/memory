# vFHE V30 — Native CRT-Factor Isomorphism and Frobenius Scalarity Gate

**Date:** 2026-10-15. **Independent vFHE V30**; GLOBAL I192 FROZEN.

**ONE PRIMARY HYPOTHESIS [PASS CONDITIONAL]:** Can verifier check **prime-local scalarity of every Boolean digit** without using vFHE Remark4.1's potentially circular claimed scalar coefficient decompositions, by one F.1 native-field isomorphism-aligned polynomial evaluation per prime and an independently authenticated Frobenius reference evaluation? **YES mathematical / ideal PCS**, NOT cheap end-to-end canonical RNS integer repair.

## Source [FACT]

Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, ePrint2025/286, inspected 52pp Research MCP mirror SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19, VERSION_UNVERIFIED against 2026-02-16 official revision. §3.1 physical p10: p_i=1+2N/d*odd, k=N/d field factors K_(i,j)=Fp_i[X]/(X^d−ζ^(2j+1)); §4.3 pp20–23: digit table t_beta; §5/F.1 physical pp25,50: ring PC equals native field PC tuple and authenticates arbitrary CRT projected MLE queries; F.2 p51: native Merkle/encoded evaluation phase publicly sends vector v'=q1 U_f of length m where m=2^(ellstar/2) for even ellstar; Remark4.1 pp15–16 suggests automorphism via alleged degree-zero coefficients. Proposal below is OUR add-on, not an authors' claimed tool or flaw. Prior V12–V16 and V23–V29 archived.

## Construction [DERIVATION]

For each prime p_i, fix public VERIFIED Fp_i-algebra isomorphisms φ_(i,j):K_i→K_(i,j), where reference K_i=K_(i,0), **before any challenges**. The candidate's existing native field commitments to h define K_i-MLE polynomials G_(i,j)(U) = φ_(i,j)^−1(Φ_(i,j)(h)(φ_(i,j)(U))) with coefficientwise conjugation of field values. At a postcommit random u_i∈K_i^ellstar query the existing native PCs at points φ_(i,j)(u_i), and check all mapped evaluations G_(i,j)(u_i)=G_(i,0)(u_i). Then authenticate ONE EXTRA reference native PC evaluation at u_i^[p_i] and check G_(i,0)(u_i)^p_i = G_(i,0)(u_i^[p_i]). The latter is the base-field coefficient test.

**Perfect honest completeness:** If each Boolean value h(b) is a common scalar a_i(b)∈Fp_i in every factor j, every transported G_(i,j) is the same Fp_i-coefficient MLE; both checks are exact for all u_i. No alleged coefficient-vector witness and no automorphism proof.

**Soundness bound (ideal knowledge-sound native PC):** If some factors' transported MLE differ, one nonzero multilinear difference of total degree≤ellstar has zero probability ≤ellstar/p_i^d. Otherwise all transported MLEs equal G, but some Boolean coefficient c_b∉Fp_i; the polynomial F(V)=Σ_b (c_b^p_i−c_b)χ_b(V) is nonzero multilinear. Frobenius relation fails except when F(u_i^[p_i])=0, also with probability ≤ellstar/p_i^d, since extension Frobenius permutes K_i. For any false fixed witness either case applies, so Pr[false accept] ≤ellstar/p_min^d (no union factor-count needed). This is source F.1 **evaluations authenticated** and public isomorphism correctness, **not** implemented compiled CP/Fiat–Shamir soundness. Sampling need NOT be from a common R exceptional set; choose each prime's native reference u_i independently and assemble corresponding CRT ring query point, which F.1 permits.

## ONE decisive exact toy census [EXPERIMENT]

Source-style p=13,N=4,d=2: R13=F13[X]/(X^4+1)=K5×K8, K5=F13[T]/(T²−5), K8=F13[U]/(U²−8). Exact φ(T)=5U, φ^-1(U)=8T, 5²*8=5 mod13. Exhaustively enumerate ALL |K5|²=169²=28561 two-variate native challenge pairs:
- honest four-Boolean digit pattern (0,1,1,0) in both factors: **0** false rejects on aligned comparisons and Frobenius.
- invalid each-factor-valid scalar-digit pattern differing at ONLY Boolean index 11: exactly **337** false accepts among 28561 challenge pairs = (2*169−1)/169² <2/169; the nonzero difference is u1*u2.
- equal transported factors but a non-base-field Boolean coefficient T at index 11: equality check passes, Frobenius check false-accepts exactly **337/28561**, matching algebra.
- prior V20 e=7+4X² has factor images (1,0), rejected at all 28561 points.
- deliberately naive same-pair-of-basis-coordinates without φ would falsely reject valid honest data at **24336/28561** points. Exact field isomorphism is not optional.

## Minimum native PCS work [SOURCE-FORM ESTIMATE, NOT BENCHMARK]

Take independent previously verified 49-bit source-format prime p_min=281474976768001=1+8192*34359738375, N=2^14,d4,L2 CRT primes, ellstar24, beta4. Conditional ideal error bound 24/p_min^4≈2^(-187.415). Source F.1 ring h-opening invokes **L*N/d=8192** native field openings. To check Frobenius additionally open two reference factors at u_i^p (requires direct use of the available internal native-component F.1 PC verifiers; if only ring-level F.1 API is exposed, 1 additional FULL ring opening is needed). In the naive per-factor original F.2 interface, matrix side m=2^12=4096; each field evaluation sends a vector v' of m native field elements. ONE extra fully aligned ring evaluation thus sends 8192*4096=33,554,432 full extension-field elements, at a compact d*49bit=196bit→25B each = **838,860,800 bytes / 800 MiB**, EXCLUDING Merkle/code samples and other messages. Two extra native reference evaluations add 204,800B of v' vectors. Source actual implementation may batch multi-evaluation/commitments or choose other parameters: this is **not** a cryptographic lower bound, measured runtime or a claim about authors' benchmarks. There is no evidence of a net practical improvement.

## Critical limits and status

The new field-aligned/Frobenius check authenticates **ONE scalar vector per p_i** and is noncircular under field PCS binding, so unlike V29 it does not ask for a scalar coefficient decomposition. It does **NOT** require different base primes to select the same integer! Existing q=13*29 example h=261 selects digit1 mod13 and0 mod29 and passes all prime-local consistency, so a SEPARATE canonical integer commitment/link/quotient proof remains necessary. This replayed known witness is a reminder of already archived gap, not a new attack. This extra query may also reveal private MLE evaluations; no ZK privacy proof supplied. No verified latest official paper, compiled attack, publication novelty or end-to-end efficiency.

**STATUS:** PASS conditional native one-query scalarity math and exhaustive exact test; FAIL unqualified low-cost FULL CRT repair; current practicality and whole-argument security UNCLEAR/HUMAN_REVIEW.
**RESULT:** Removes circular alleged-scalar-coefficient witness from PRIME-LOCAL part only, at potentially very high native PCS message cost.
**NEXT_ACTION V31:** ONE concrete sound cross-prime canonical integer commitment/reduction link with a real F.1/F.2 cost/knowledge gate, or HUMAN_REVIEW/pivot and authenticate original Feb2026 PDF; stop repeating prime-local tricks or unproven large-batch folds. PI controls disclosure.
**STATE_UPDATE:** YES independent V30; GLOBAL I192 frozen.

**Reproducibility**
- Report: /mnt/data/VFHE_V30_Native_CRT_Isomorphism_Frobenius_Gate_2026_10_15.md SHA256 75602debe4b8c0d83abd378461a6ffb421161285ea58c631730170e9e015d3ed
- Python: /mnt/data/vfhe_v30_aligned_native_field_gate.py SHA256 634d2f7bc413fd3b6811eceaa7b04cab5bfb45f6640b223b509675dcd832b06f
- JSON: /mnt/data/vfhe_v30_aligned_native_field_results.json SHA256 12604e69acd5fc82bbbd85b2e7dc580d9e9b61b720139639bf6be6162fcafaa3
