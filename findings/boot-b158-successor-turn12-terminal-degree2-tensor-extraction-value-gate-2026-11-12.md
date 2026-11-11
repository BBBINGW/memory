# BOOT / B158_OVERALL — Successor Research Turn 12/25
Date: 2026-11-12 (Asia/Singapore)
Candidate: boot-b158-terminal-degree2-tensor-extraction-v1
Phase: PROBLEM_SELECTION
Final verdict: FAIL_DOMINANT_NOISE_RESCUE / FAIL_STOCK_DEGREE2_AUTOMORPHISM -> PARKED
No native/Codex launch.

## Authority / distinctness
TRACK_ID BOOT; ACTIVE_SUBLINE B158_OVERALL; incoming active UNKNOWN, backups NONE. Read GitHub repo sources before any new finding:
- previous findings/boot-b158-successor-turn11-polarized-si-two-squares-scale-carry-value-gate-2026-11-12.md, blob 561dd520f2010624d40439d7a36872b70205bbc4, PARKED;
- findings/boot-B175-source-level-si-error-bounds-2026-10-29.md, blob c75aa60e080b28b688de7ee8859c5df4d1951c02, dominant tensor/reference term;
- findings/boot-B175-post-claim-boundary-synthesis-2026-10-29.md, blob 3b61d23d11e78e7f0bf111a905d3c6b99d918ccb, later full Algorithm5/extraction not executed;
- findings/boot-b158-turn18-late-lazy-relinearization-problem-selection-2026-11-12.md, blob 9c13d60811aea450103922df302df0f61cb02ad3, prior PARKED stock lazy relin at INTERMEDIATE power basis stages;
- B175 native archive SHA256 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa; Q bitlength649, required bits LT8=577, GROUPED=633, terminal SI=664, 32767/32768 mismatches.
This candidate is NOT a renamed intermediate-lazy-relin: it leaves a degree-2 tensor only at the FINAL SI merge, proposing terminal degree2 rotate-and-sum and RLWE->LWE extraction with an enlarged secret-key basis (1,s,s²) so no relinearization is required. Unlike an ordinary relinearization scheduling tweak, it changes the terminal output representation/extraction interface. The source feasibility and value of this NEW mechanism are tested independently, without reopening the prior candidate.

## Pre-registration
QUESTION: Can the B175 final SI output remain a degree-2 ciphertext (v0,v1,v2) under secret powers (1,s,s²), skip relinearization, and still support the later 8-block rotate-and-sum plus RLWE-to-LWE extraction under the fixed scheme, eliminating enough dominant noise or key/runtime cost for a paper-worthy fixed-Q solution?
CURRENT_BELIEF: No. Omitting only the terminal relinearization removes the E_relin term bounded below 2^22 against a dominant E_tref residual around 2^647. Rotations are stock degree-1 only, while a custom degree-2 automorphism needs s²-specific switching; terminal LWE extraction must also handle s² terms or a later relinearization.
CHEAPEST_DECISIVE_TEST: Audit exact source degree contracts and B175 source-derived error decomposition; derive the exact secret-power transformation under automorphism and optimistic cost frontier for a saved terminal relin. No native.
IF_PASS: If a source-compatible degree-2 linear/rotated output and extraction plan exists with an invariant reducing the dominant tensor/reference term by >=16 required bits (or a useful DFR bound), plus net positive whole-system cost, retain ACTIVE and specify a small exact correctness canary.
IF_FAIL: If the only guaranteed error removed is bounded E_relin and stock automorphism cannot consume degree2, while custom extraction/rotation costs are uncompensated, PARK before native.
IF_UNCLEAR: Preserve UNKNOWN for hypothetical bespoke higher-degree key-switch/extraction and any correlated downstream noise cancellation; require a complete typed algorithm and source evidence, not speculative speedup.
WHICH_PAPER_GATE_CHANGES: full Algorithm5 output semantics, degree/type/source interface feasibility, quantitative error/DFR contribution and complete cost.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: Degree-2 terminal ciphertext could avoid an otherwise mandatory relinearization only if its changed extraction pathway is correct and saves meaningful cost or noise; if it merely moves a low-noise conversion into a custom extractor, it does not solve B175.

## Exact degree-2 semantics and source boundary
For degree-1 ciphertexts A=(a0,a1), B=(b0,b1), raw tensor U=(a0b0,a0b1+a1b0,a1b1) decrypts under the ORIGINAL secret s as
  Dec_s(U)=U0+U1*s+U2*s²=(a0+a1*s)(b0+b1*s).
BGV SI first needs centered Q->QMul extension and componentwise approximate Q-related scaling to v_i, then would normally relinearize v2. The proposed terminal representation keeps V=(v0,v1,v2) after quantization and before relin, with secret power basis (1,s,s²). It has correct IDEAL raw-product algebra, but complete source-scaled BGV output/reference semantics remain unproven if an explicit degree2 consumer is substituted.
An automorphism σ of the tensor components changes decrypt-under-s phase to
  σ(v0)+σ(v1)*s+σ(v2)*s²,
whereas the intended rotated plaintext is
  σ(v0+v1*s+v2*s²)=σ(v0)+σ(v1)*σ(s)+σ(v2)*σ(s)².
Thus ordinary coefficientwise σ requires switching from σ(s), σ(s)² back to s, s² or an equivalent high-degree key evaluation. It cannot be silently interpreted as the stock degree1 RowRotation under unchanged s.
Pinned Lattigo v6.2.0 core/rlwe/evaluator_automorphism.go blob 527b1fdf8fdd92b705896b555597c9cc40ee2609 restricts Automorphism to input/output degree1, as authenticated in findings/boot-b158-turn18-late-lazy-relinearization-problem-selection-2026-11-12.md. That finding also establishes BGV stock Mul rejects degree>1 ciphertext operands. In the terminal interface, no additional ct×ct need be performed if Algorithm5 extraction truly follows, but required later rotate-and-sum operations and standard RLWE-to-LWE extraction are NOT validated for degree2.
An LWE extracted coefficient of V's degree2 decryption has secret-dependent form
  b= v0[j]+ sum_i alpha_i(s)*v1[i]+sum_i beta_i(s²)*v2[i] (mod Q),
where alpha_i,beta_i are convolution-sign permutations depending on coefficient index j. A degree-1 RLWE-to-LWE extractor expecting only coefficients of s cannot simply drop the v2 term. An enlarged LWE secret including coeffs(s²), or a key conversion/KS to a supported LWE secret, is needed. Security for this correlated nonuniform secret and any output LWE requirement must be proved; cost, key dimensions and memory are UNKNOWN, not free.

## Decisive noise/value obstruction
Authoritative source decomposition:
 e_out=rho_Q(E_tref+E_quant+E_relin),
 with conservative ||E_quant||_∞<2^46 and ||E_relin||_∞<2^22, and observed ~647-bit centered coefficient residual, B175 required bits664. Omitting relinearization changes this to
 e_degree2=rho_Q(E_tref+E_quant)
at the corresponding phase/reference before any new output transform. The modular centered-distance triangle inequality gives
 ||e_degree2||∞ >= ||e_out||∞ - 2^22,
which, per the prior source finding, retains the SAME 647-bit residual bitlength/664 required bits. This is not a statistical argument; it applies to the archived B175 tested instance. Thus *merely* deleting terminal relinearization cannot flip the B175 failure to a positive coefficient-noise budget. Any later rotation/sum could in principle cancel particular correlated components, but no source-backed necessary cancellation or useful legal-domain DFR exists, and B175 already has 32767/32768 incorrect slots prior to such postprocessing. Claiming restoration from a downstream output reducer without measuring the complete reference would be unjustified.
Operation upper benefit: at most ONE relinearization per B175 final SI product; 26 ct×ct through pointwise remain, and earlier power-basis relinearizations remain so the relin key family/binary size is not eliminated. The existing B175 serialized evaluation-key total ≈1062.54 MiB; no meaningful key saving follows solely from suppressing one terminal call. A degree2 terminal retains 3 components instead of the normal 2 (1.5x component count for that live ciphertext) and custom Galois/degree2 extraction may require additional key material and memory. No matched runtime claim.
Hence gate1 exact ordinary raw tensor algebra PASS but full degree2 output/carry/extraction UNKNOWN; gate2 stock later automorphism FAIL, special custom construction unverified; gate3 fixed-Q >=16-bit recovery FAIL and no optimistic net positive value established. No native justified.

## Closest prior / novelty
Lazy relinearization, high-degree RLWE ciphertext evaluation, secret-power-basis ciphertext tensoring and standard degree-1 key switching; historical Turn18 covers intermediate use, not terminal extraction. Merely omitting relin and changing extractor is a conventional representation tradeoff. Exact new typed extractor, complete security and favorable end-to-end metrics would be necessary before asserting novelty. NOVELTY_STATUS=PREFLIGHT, no verified CLEAR.

## Decision
Status PARKED, NEW_MECHANISM=NO_CREDIBLE_NEW_MECHANISM for the proposed terminal no-relin/degree2 extraction as fixed-Q correctness fix.
REOPEN_CONDITION: A source-compatible degree2 output automorphism and RLWE-to-LWE extraction with full legal-message/phase scale and carry semantics, a provable tensor/reference error contraction >=16 required bits or useful DFR not explained by saved relin noise, and positive complete cost (including s² keys, ciphertext memory, conversion and offline) plus independently audited novelty. No renewal through ordinary lazy relin alone.
ELIMINATED_UNCERTAINTY: Can simply keeping terminal B175 degree2 ciphertext and omitting final relinearization remove enough observed error to restore fixed-Q correctness? No: the removed error is <2^22 against the observed ~2^647 dominant residual; stock RowRotation also cannot consume degree2.
DECISION_CHANGED=true: new candidate screened and PARKED; no native task, research_frontier_exhausted=false.
