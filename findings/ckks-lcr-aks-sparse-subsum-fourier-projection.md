# Iteration 40 — Sparse SubSum can be fused into the final CoeffsToSlots Fourier factor (algebraic)

Date: 2026-10-10
Branch: CKKS bootstrapping / LCR+AKS sparse packing compatibility
STATUS: PASS for an exact **Fourier–SubSum intertwining identity** and **factor-support inclusion** only.
Conjectured practical optimization: NOT VERIFIED. Originality: NOT VERIFIED. Do not claim end-to-end LCR+AKS sparse bootstrapping correctness or speedup.

## State and source provenance
[FACT] Read GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md (RIG-HE parked), last Iteration39 archive and complete failures/findings indexes BEFORE selecting this new target; leave parked STATE.md unchanged. Did not reopen GL BigSwitch, CKL key derivation, MRFHE joint packing.
[FACT] Attempted primary FBS source ePrint 2026/975 with Research MCP; RETRIEVAL_BLOCKED: official PDF 403, exact arXiv missing, configured mirror missing. User Library has no matching full text. No technical conclusions from its abstract alone. Selected different available CKKS primary source.

[FACT / PRIMARY] Lianglin Yan, Pengfei Zeng, Heyang Cao, Peizhe Song, Mingsheng Wang, *Faster Bootstrapping for CKKS with Less Modulus Consumption*, ePrint 2025/1403 (PKC 2026). Research MCP full text 51 physical pages from GitHub mirror, SHA256 784db16f5a3f7c79c68c52f0a99e03c8ca7ce3e4c06824736f5fd4dfff1f5c29, VERSION_UNVERIFIED.
- §2.1 / §2.2, physical pp.9–11: canonical embedding indexed by `zeta^(5^j)` for powers of two, matrix `A_{j,k}=zeta^(k * 5^j)` for the complex half.
- §3.1 Theorem 1, physical p.13: LCR requires small **unreduced integer lift** <ct,sk> before automorphism key-switches; it is not a claim that any ciphertext with small *centered modular decryption* can be level-preserving rescaled.
- §3 Remark 1, physical p.14, and note §1.3 physical p.6: *sparsely packed ciphertexts excluded*, because SubSum after ModRaise uses rotations/key switching before first LCR.
- §3.2 physical p.15: first matrix transform can move LCR ahead of rotations if performed on the original still-small ct.
- §5.1 physical pp.23–24: lossless LCR+AKS only for first CtS factor with r<=64, using GHS-type switching; last-factor algebraic fusion is not analyzed there.
[FACT / PRIOR WORK] Bossuat et al., *Efficient Bootstrapping for Approximate Homomorphic Encryption with Non-Sparse Keys*, ePrint 2020/1203, Research MCP full text 46 physical pages (SHA256 3b53cf70c8cde60571edc749ce9ff5d7e5c09201cf316cbd178055fe8a2aeabe), §5.1–5.2 physical pp.17–18: SubSum maps q0 I(X)+m(Y) to (N/2n)*(q0 I_tilde(Y)+m(Y)) in smaller subring, followed by small-domain CoeffsToSlots. §5.2 and §5.5 physical pp.18,21 already fuse scalar N/(2n) into CtS matrix coefficients. This is **prior art** for the trace and scalar fusion, but does not establish the LCR+AKS sub-sum bypass as novel or non-novel.
[SOURCE QUALITY] Research MCP provides original extracted PDF text; matrix equations checked by independent exact modular arithmetic below. ePrint mirror version statuses remain unverified.

## One primary hypothesis / minimum falsifier
[HYPOTHESIS] For conventional power-of-two sparse CKKS with N=2^m, n=N/2, t=2^a dividing n, the SubSum S_t that accumulates the t rotations by h*(n/t) slots (h=0..t-1) can be moved to the *output* of the full Fourier CoeffsToSlots map F^{-1} as a diagonal mask/projection D_t. Then, for *any* factorization F^{-1}=M_L...M_1, the mask D_t can be absorbed into the LAST factor, with no increase in its diagonal support. This removes the algebraic need to execute SubSum key-switches before the first LCR, though it may not preserve the low-dimensional bootstrapping cost.
[FAILURE CONDITION] Exhibit any valid N,t, Fourier Galois 5-power row convention where F^{-1} S_t != D_t F^{-1}, or show the row mask creates a previously zero diagonal offset in D_t M_L.
[TEST] Exact quotient-ring Galois trace + finite-field Fourier matrix inversion for smallest valid powers of two; no expensive FHE estimator or benchmark.

## Exact theorem and derivation
[DERIVATION] Define K=Q(zeta_{2N}), n=N/2, Galois generator sigma(X)=X^5, which has order n for N=2^m (m>=3). For t=2^a|n, H=<sigma^(n/t)> of order t is the Galois subgroup fixing the cyclotomic subfield K'=Q(zeta_{2N}^t). The ring Z[X]/(X^N+1) is a free Z[X^t]/((X^t)^(N/t)+1)-module of rank t with basis 1,X,...,X^(t-1). Its relative trace is
  Tr_{K/K'}(X^j) = t X^j if t|j, otherwise 0
for j=0,...,N−1.
Proof: the extension has monogenic presentation T^t−X^t; the trace of T^r is zero for 0<r<t and t for r=0. Equivalently, it is sum of the automorphisms sigma^(h*n/t).
For the CKKS Galois-ordered complex-half Fourier matrix F of shape n×n, `F_{j,k}=zeta_{2N}^{k·5^j}`, the rotation subgroup sum is S_t=Σ_{h=0}^{t−1} ρ_{h*n/t}. Hence each Fourier column (monomial X^k) is either eigenvalue t if t|k, or annihilated, yielding
  S_t F = F D_t;  F^-1 S_t = D_t F^-1,
  D_t=t·diag(1_{t|k}:0<=k<n).
The full CKKS CoeffsToSlots also has a conjugate output branch; D_t is real and commutes with complex conjugation, but this has NOT been verified for an actual two-ciphertext implementation here.
Since F^-1 = M_L M_(L-1) ... M_1, we can algebraically replace the final factor by D_t M_L. Its j-th row is multiplied by either t or zero, so `DiagSupp(D_t M_L) ⊆ DiagSupp(M_L)`. Thus no *additional diagonal offsets* (and in a diagonal linear-transform representation no extra rotation offsets) for that factor.
This is a **symbolic/plaintext identity**, NOT a claim that dropping SubSum without changing CtS factor matrices works; arbitrary sparse factor M need not commute/intertwine the subgroup.

## Exact minimal verification
[EXPERIMENT] Local reproducible script `/mnt/data/iteration40_ckks_subsum_fourier_projection.py`. Prime q=257; q−1=256 permits primitive 2N roots for N=16,32,64. Modular Gauss–Jordan exact matrix inversion; ten (N,t) cases: (16,2),(16,4),(16,8),(32,2),(32,4),(32,8),(64,2),(64,4),(64,8),(64,16). Each case passed exact n×n matrix identities `S_t F=F D_t`, `F^-1 S_t=D_t F^-1`, and 100 independent random-vector trials: 10/10 matrix identities, 1000/1000 vector comparisons. Separate exact ring-automorphism trace verification of *all* monomial basis elements for (N,t)=(16,2),(16,4),(32,4),(64,4),(64,16),(128,32), including N=128 over coefficient arithmetic without field diagonalization: all pass.
A random 4-diagonal last-factor model with offsets {0,1,3,7} at n=32 has the same diagonal offsets after masking by D_4; confirmed exact inclusion. A generic unrelated sparse factor M fails `M S=D M`, preventing an invalid claim that SubSum could be moved through just any isolated first stage.
Limitations: these are precise finite-field/characteristic-zero algebra identities, not actual CKKS approximate encoding, key switching, RNS ModDown or noise/precision tests.

## Research value and open blockers
[POSITIVE] Algebraically no SubSum is needed *before* the Fourier CtS transform if one replaces the last factor with D_t times the original last factor. This is a potential path to use the author's first-factor LCR+AKS without prior SubSum key switching. The selected frequency mask has coefficients t/0, so ordinary standalone CKKS mask multiplication could consume scaling/modulus; absorb it into the last factor instead rather than assuming a free multiplication.
[OPEN -- DOMINANT COST] Bossuat et al. use the original SubSum to reduce the domain to a *small subring*, then run CtS on smaller n/t slots. Bypassing SubSum and evaluating a FULL n×n F^-1 circuit may cost much more rotations, plaintext operations and/or levels than the original sparse low-dimensional transform; no net speedup claim. It is not enough that last-factor diagonal support stays unchanged.
[OPEN -- REAL PIPELINE] Verify canonical output ordering, conjugate splitting, bit reversal, pre- and post-SubSum normalization, packed-slot layout, and actual RNS LCR preconditions; merge mask into the factor that is chronologically last, not first, and check EvalMod receives same scaled coefficients. Because CKKS is approximate, accumulation of rounding and key-switch errors changes despite plaintext equality; no correctness failure probability claims.
[OPEN -- NOVELTY] Subring trace/projection is old, and scalar absorption in Fourier transforms appears explicitly in 2020/1203. New applicability to LCR+AKS and a *pruned* full-transform implementation might have technical value, but has not been proven novel. Search did not establish an existing identical LCR+AKS SubSum fusion, but absence of hits is not positive novelty evidence. STATUS should not be inflated to publishable.
[REALISTIC NEXT TEST] Retrieve the actual CtS linear-transform factor sequence used in 2025/1403's Lattigo reference implementation (github.com/Fainabi/Lattigo-LCR-AKS). For ONE small power-of-two setting (e.g. N=2^12, t=4), inspect first/last matrix order and exact slot mapping, build a row-mask D_t at output, and count remaining nonzero diagonal offsets, rotation key-switches, and levels after pruning against baseline SubSum + n/t-domain CtS. Stop if total operation count is already worse before attempting RNS noise testing.

## End of iteration
STATUS: PASS (algebraic composition / support), with HUMAN_REVIEW required before costly implementation, novelty still uncertain.
RESULT: Exact Fourier intertwiner F^-1 S_t=D_t F^-1 and last-factor diagonal support inclusion; a candidate way to move SubSum key-switching after the first LCR, but NOT a proven end-to-end sparse LCR+AKS algorithm or speedup.
NEXT_ACTION: Inspect the precise first/last CtS factors and bit-reversed index order of the Lattigo-LCR-AKS implementation for one fixed N=2^12,t=4; compute a pruned masked-transform *operation count* versus conventional SubSum + small-subring CtS, before expensive CKKS implementation.
STATE_UPDATE: NO. Parked RIG-HE STATE.md unchanged.
