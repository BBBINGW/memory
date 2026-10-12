# Iteration 111 — Pinned C sparse-SAB descending differences produce GLOBAL X inversion but preserve constant-coefficient LUT extraction

Date: 2026-10-12. Primary paper Guimarães–Pereira, *Fast amortized bootstrapping with small keys and polynomial noise overhead*, CCS 2025 / IACR ePrint 2025/686. Research MCP full 34 physical pp, PDF SHA256 `84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335`; official latest VERSION_UNVERIFIED. Pinned author's source repository `antoniocgj/Fast-Amortized-Bootstrapping` commit `8938ab5bd42a80c93ed5ee4caef36efbb01bf7ef`.

## One smallest falsifiable hypothesis + one cheapest decisive test
[HYPOTHESIS] For a binary sparse key with one nonzero position j, author C's *descending positive difference* schedule `(n-j,j)`, its *X -> X^-1* wrap automorphism, and actual test-vector packing produce the correct **constant coefficient LUT extraction**, despite differing from the paper's suspicious `d_h=-j_last` formula.
[FALSIFIER] One exact noiseless input where actual-source-scheduled constant coefficient differs from `f(m_i)`, after respecting the torus exponent/message scaling, in `Z[X]/(X^N+1)` and `Z[Y]/(Y^n+1)`.

## Read-before-write source provenance [FACT]
Read live GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md last iteration110, and I110 finding. Used GitHub connector to read pinned `src/sparse_amortized_bootstrap.c` blob `b86d4d7f8f578665196a94dd6a2c9ca155f8bde7`:
- lines 146-185 `previous=in_N`; traverse descending current j and store positive gaps `previous-current`, terminal positive `previous`. h1 s=Y^j yields **d0=n-j, d1=j**, total n.
- lines 215-245: CMUX and NCMUX apply **automorphism X->X^-1 to the wrapped source slot**, not a unary plaintext scalar negation. Bitwise `RGSW_monomial_mul` realizes S_d(p)_i = σ(p_{n-d+i}) for i<d, else p_{i-d} when controls encode d, 0<=d<n.
- lines 260-280: binary key `sub_a` applies `trlwe_mul_by_xai(...,a[i])`, so it is **X^(+a[i])**. At the wrapped slots already under σ this corresponds to subtracting a in the underlying exponent.
- lines 283-301: positive shift, then sub_a, then last positive shift.
- lines 334-355: setup_tv_xb multiplies T by monomial exponent obtained from torus-scaled b. `sab_LUT_packing` lines 407-414 puts negative lookup values into reversed coefficients, so constant coefficient of T X^e is the LUT entry for the properly encoded e.
Pinned `main.c` blob `a55fcfaa78151b71ae3aca1e434e0ec69b8afe27` actual encrypted test calls LUT packing, bootstrapping, and compares every output to expected LUT at lines223-242, but we did not run C. Pinned mosfhet `src/mosfhet/src/trlwe.c` lines276–310 defines encryption b=a*s+noise+m and decryption phase b-a*s, removing possible opposite-sign convention doubt.

## Exact algebraic derivation [DERIVATION]
Let p_i = T(X) X^(b_i), secret s(Y)=Y^j with 1≤j<n, ring R_Y=Z[Y]/(Y^n+1), output test-vector ring R_X=Z[X]/(X^N+1), sigma(T)=T(X^-1). Ignore encryption noise and modswitch error, allow the underlying input exponent to represent exact message phase.
Step 1: first shift d0=n-j:
 `q_i = sigma(p_{i+j})` for `i<n-j`; `q_i=p_{i+j-n}` otherwise.
Step 2: C binary sub_a: `u_i=q_i X^(a_i)`.
Step 3: final shift d1=j:
- For i<j: `C_i=sigma(u_{i+n-j})=sigma(p_i X^(a_{i+n-j}))=sigma(T X^(b_i+a_{i+n-j}))`.
- For i>=j: `C_i=u_{i-j}=sigma(p_i) X^(a_{i-j})=sigma(T X^(b_i-a_{i-j}))`.
These two cases are exactly the negacyclic convolution `m=b-a Y^j`: m_i=b_i+a_(i+n-j) for i<j and m_i=b_i-a_(i-j) for i>=j. Hence for ALL output i,
`C_i = sigma(T(X) X^(m_i))` as FULL polynomials, not necessarily equal to T X^(m_i).
And coefficient-zero is sigma-invariant: `[X^0]C_i=[X^0]T X^(m_i)`. Therefore code schedule's global inversion does NOT harm constant-coefficient LUT evaluation.
This proves an **ideal symbolic identity for h1** and indicates why the positive terminal gap is not the printed negative shift. No actual FHE proof.

## One faithful minimal test [TEST PASS]
Choose toy n=N=8, BPREC=3, message f=[1,3,2,0], m=[2,1,0,3,0,1,2,3], a=[1,0,2,1,0,1,0,1]. Source message-exponent scaling is **(2N)/2^BPREC=2**, since torus2int of a 3-bit message scaled to 2N=16 yields exponent 2m. b is constructed exactly as b=2m+aY^j, with signed b allowed modulo 2N. LUT packing source gives:
`T(X)=1 - 2X^3 -2X^4 -3X^5 -3X^6 -X^7`.
For j=1, d=[7,1], final output slot0 X-polynomial coefficients `(2,2,0,0,-1,-1,-3,-3)`; expected sigma(T X^4) is exactly the same, while uninverted T X^4 `(2,3,3,1,1,0,0,-2)` differs.
The output constant coefficients across all 8 slots are `(2,3,1,0,1,3,2,0)`, exactly f applied to m. Repeated same SINGLE hypothesis over **7 possible h1 key locations j=1..7**, 56 slot cases: all 56 FULL output polys equal sigma(T X^(2m_i)), all 56 extraction constants correct. Not equal to uninverted polys: confirmed difference.
[IMPORTANT DEBUG] First local test erroneously used exponent m rather than 2m while using actual source packed LUT; failed (j1 outputs wrong LUT). Corrected to actual torus-to-exponent scale 2; regression test then passes. Do not interpret first attempt as code bug. This debugging provenance distinguishes correct behavior from hidden encoding convention.

## Scientific scope
[PASS] In author's pinned **binary h1 exact noiseless code operation model**, the descending key-gap schedule compensates for the printed Horner terminal sign by leaving a global output ring conjugation which preserves the only extracted coefficient. This NEGATES the I110 suspicion that a printed sign alone implies an actual implementation correctness failure.
[NOT CLAIMED] No compiled C execution, actual ciphertext GSW/RLWE, key-switching noise, torus rounding, multi-key h>1, arbitrary secret magnitudes, security or runtime assessed. The paper's printed `d_h=-j_last` vs exact Eq(3) remains a likely *textual sign/notation issue* unless typeset PDF is manually verified; formula extraction warns of possible sign loss. No evidence of a nontrivial cryptographic repair, attack or new optimization.
[DECISION] PARK I110–111 literal terminal-sign branch as low-value possible erratum. Continue only on PI-authorized genuinely new technical target; no publication claim, no author outreach.

## Repro
Verified and executed:
- `/mnt/data/iteration111_sab_c_schedule_phase_alignment.py`, SHA256 `db8abbfc9466df3de97b1049fcffaa2ed143d602561f216c5a42439d5972ad0c`.
- `/mnt/data/iteration111_sab_c_schedule_phase_alignment_results.json`, SHA256 `2aec8bea075c13533b4ce48346f16497d409e72b5e4343a62998a541389f0ba0`.
These exact local paths were independently SHA-verified. Results record all tested key positions, sample intermediate polys and source TV.

## End of iteration
STATUS: **PASS** ideal C schedule phase alignment; **FAIL** I110 code-impact suspicion; **UNCLEAR** complete implementation correctness; **LOW NOVELTY** local paper sign.
RESULT: the output is sigma(T X^m) and sigma fixes coefficient0.
NEXT_ACTION (I112): PI review/choose an independent FHE technical target with nontrivial scope; avoid repeated petty sign and rounding errata. Do not self-extend I111 to new problems.
STATE_UPDATE: YES.
