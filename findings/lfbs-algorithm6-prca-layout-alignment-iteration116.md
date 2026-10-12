# Iteration 116 — LFBS Algorithm 6 does not explicitly reconcile PRCA bit-reversed layout with natural test-polynomial indexing

Date: 2026-10-12. Primary Li–Shen–Lu–Wang–Zhao–Wang–Wei, *Leveled Functional Bootstrapping via External Product Tree*, IACR ePrint 2025/022, https://eprint.iacr.org/2025/022.pdf.

## Protocol and source
Read connected Research GitHub Notes `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, `STATE.md` (last completed I115), and `findings/lfbs-prca-bit-reversal-and-trace-subring-iteration115.md`. Used full primary 35-physical-page public PDF as web `turn592374view0` and `turn558988view1`/`turn558988view2`. `web.run` screenshot of physical pp16–17 was ATTEMPTED and returned internal error, so typeset PDF independent visual check remains unverified. Research MCP `get_eprint_paper("2025/022")` fails because of leading-zero ID normalization; do not claim Research MCP SHA or latest version verification.
Public implementation search: GitHub connected repository + code search on full title, LFBS, PRCA, authors' identifying string; public web search for full title with Github, PRCA LFBS OpenFHE. No **verifiable authors' paper-specific OpenFHE source** was located. This is non-exhaustive negative evidence, NOT proof that no such repository exists. The current OpenFHE CKKS functional-bootstrapping example is a DIFFERENT scheme and not author LFBS code. Do not substitute it.

## ONE primary hypothesis + cheapest decisive test
[HYPOTHESIS] Although PRCA Algorithm5 with naturally ordered B ciphertexts introduces bit reversal (I115), Algorithm6 explicitly applies an inverse permutation or changes testPt's input block ordering so the full described LFBS pipeline has natural `j` LUT semantics without additional convention.
[CHEAPEST FALSIFIER] Cross-reference original §4.1 testPt encoding with Algorithm6's input indexing, and run ONE exact noiseless, legal single-indicator sub-LUT in the intended B16,N1024 configuration through *literal* PRCA to see whether the target block remains at j=1.

## Source facts
- §4.1 physical p14–15 encodes each test polynomial with natural plaintext blocks `testP_i(X)=Σ_(j=0)^(B−1) f(j,m1,...,m_(l−1)) Σ_(k=0)^(N/B−1) X^(jN/B+k)`, and indexes `i=m1 B^(l−2)+...+m_(l−1)`. It does NOT state bit-reversed j blocks.
- §4.2 physical p17 Algorithm5 natural `ct_j` order, merge shifts `X^(N/2^i)`, automorphism `ψ_i: X→X^(2^i+1)`, printed trace `Tr_(K_N/K_(N/B))`, temp multiplier. Our I115 exact algebra showed a source-literal PRE-trace index transformation `j→bitrev_(log2B)(j)`.
- Physical p18 (PDF page labeled19) Algorithm6 lines ~1072–1090 defines `CT_k=CCH(ct_k,CCK)` and nested `ct_(t,k,i)=testPt,i ⊡ CT_k`. Subsequent PRCA invocation is over **consecutively ordered** ciphertexts `ct_(t,k,(i−1)B), ..., ct_(t,k,iB−1)`; no explicit `bitrev`, permutation, or reconciling natural `j` convention appears in Algorithm6 or adjacent horizontal-packing encoding formulas (physical p18 lines1095–1129, still X^(jN/B+...)). A cyclic-encoding or application-wide bitreversal convention outside inspected passages might compensate implicitly: no whole-system proof either way.
- Algorithm5 printed trace K_(N/B) target and I115 candidate K_B target differ; for *this test* N1024,B16, printed K64 happens to CONTAIN K16, so **it does NOT kill the one-hot signal**. Therefore this particular test isolates pure order mismatch, not the unrelated subring case B²>N.

## One exact minimal test [DERIVATION/TEST]
Choose N=1024, B=16, at any fixed remaining input u=2, a perfectly valid indicator subfunction `f(j,u)=1` for j=1, and zero otherwise. The natural plaintext blocks are width N/B=64 and the desired test polynomial is `X^64 (1+X+...+X^63)`.
Feed the 16 corresponding *ideal constant sub-LUT outputs* (one at j=1) into literal PRCA Algorithm5's tree and paper trace K64. It produces the block `X^512 (1+X+...+X^63)`, because bitrev_4(1)=8. Under the source's intended natural j=1 subsequent block selection, value read is 0 rather than 1; j8 incorrectly carries 1. This is exact negacyclic polynomial arithmetic with no noise.
As independent repair sanity check, publicly bitreverse the 16 input ciphertext positions AND select trace K_B (K16); resulting plaintext is exactly the natural-order target test polynomial. This correction is not a new FHE algorithm and no end-to-end security/precision properties follow.
ONE actual semantic LUT toy + two layouts, not a mass parameter search.
Executed `/mnt/data/iteration116_lfbs_algorithm6_layout_gate.py` sha256 `c0bde968de8cf5a7651511ade1711e062ab56399ed9e645ef1d06dc0c3b9505b`; JSON `/mnt/data/iteration116_lfbs_algorithm6_layout_gate_results.json` sha256 `ae9bf39a03f15979ef630b4f87faae5b7f5db63387b9fe404a3e5693911d801c`. It reuses exact tested I115 Fraction/noiseless polynomial evaluator. Its module import reruns deterministic I115 basis test as a side effect; not a separate hypothesis.

## Scope / scientific value
[PASS] Under the LITERAL published test-polynomial natural-block indexing and Algorithm6 consecutive natural input ordering, there is no explicit inverse bitreverse and an intermediate index-layout mismatch persists. The one-hot LUT demonstrates semantic relevance to function values.
[FAIL AS SOURCE CLAIM] The narrow claim that Algorithm6 itself **explicitly** repairs the I115 ordering mismatch is not supported by relevant source passages.
[UNCLEAR REAL SYSTEM] No pinned author LFBS OpenFHE code found; `CCH` cyclic monomial encoding, implementation pre-layout, or hidden bit-reversed test array MAY account for it. A proof of complete LFBS decrypted output failure and ciphertext attack was NOT performed. PDF subscript precision also unverified by screenshot due tool error. Neither a security failure, a real deployed implementation bug, nor novelty is established.
[LOW NOVELTY] If missing, a public bit-reversal of B inputs and correction of printed trace subscript is a minor code/pseudocode repair. No fundamentally new bootstrapping primitive. In accordance with research philosophy, **PARK the source-only layout/notation audit** unless code or original proof supplies a substantive new complication. Do not email authors or publish claims without PI authorization.

## End of iteration
STATUS: **PASS source-literal alignment counterexample / FAIL explicit Algorithm6-compensation hypothesis / UNCLEAR actual implementation correctness, low novelty.**
RESULT: natural LUT block j1 moves to PRCA block j8 for N1024 B16, and no explicit permutation is documented in printed Algorithm6.
NEXT_ACTION (I117): HUMAN_REVIEW. Recommended park narrow LFBS PRCA layout discrepancy I114–I116 and choose a genuinely new original-FHE gap with source-verified code or a nontrivial proof/parameter barrier. If PI explicitly prefers LFBS, the only meaningful remaining test is obtain **the actual author implementation** and show a mismatched decoded LUT on a pinned official example or demonstrate full flow compensates. Otherwise do not revisit.
STATE_UPDATE: YES.
