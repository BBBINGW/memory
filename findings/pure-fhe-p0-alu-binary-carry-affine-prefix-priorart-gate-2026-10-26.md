# PURE-FHE · P0-PRESCOUT-32 — Binary ALU carry-state affine prefix and prior-art gate

Date: 2026-10-26 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: INDEPENDENT_PURE_FHE_SOURCE_FIRST_SCOUT
PREVIOUS: P0-PRESCOUT-31
STATUS: PASS_EXACT_BINARY_AFFINE_COMPOSITION / FAIL_CORE_NOVELTY / UNCLEAR_END_TO_END_VALUE
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO (no GPU, native, remote server, or FHE implementation)
STATE_UPDATE: YES, isolated PURE-FHE finding only; global STATE.md and other lines unchanged.

## Scope / one hypothesis
Latest CI-CKKS ePrint 2026/2618 revised Oct25 full PDF remains SOURCE_BLOCKED: official ePrint 403, arXiv exact-title and known mirror unavailable, GitHub papers/supplied does not contain it. We neither infer its algorithm from an abstract nor extend the P0-31 single-cosine toy. Instead inspect user-supplied full PDF ePrint 2026/1869 and comparison ePrint 2026/1840.

H32: In the B=32, M=2^n specialization of Liu–Ma–Wang–Wang (ePrint 2026/1869), replace encrypted binary carry-state transition matrices by an affine generate/propagate representation and then evaluate output bit functions, reducing **carry-stage ciphertext-ciphertext multiplications** with the same two FBT calls. Test algebraic correctness, operation count, extra depth and novelty against contemporaneous first-party papers. This is one hypothesis/one test.

## [FACT] Source provenance
- Supplied papers/supplied/2026-1869.pdf blob SHA 9de785af66b3106e509283c84816513d56f6f7dd, original physical pp21–26 Section5.2 and Algorithm2 Section5.4-5.5 plus Appendix C.1-C.3 pp36-39, reread. For B=32 (s=5), carry C={0,1}; FBSB outputs |C|(|C|+s−1)=12 local indicator and bit functions; each nonfinal doubling level costs 12 ciphertext multiplications and final level costs 5. Original A2B online reported CPU latencies (Table5 p28) are 88.48s (64 bits), 107.09s (128), 121.28s (256), measured in author setup and NOT experimentally decomposed by subroutine.
- Supplied papers/supplied/2026-1840.pdf SHA fb5f5c20a61030b8a1ecfdb150cf4602d4dcc4ea, Shen–Li–Wang–Lu, Section4.2 original pp18–21 read. Their Theorem5 has the SAME three monotone binary carry behaviors (constant0, constant1, propagate/identity), maps c_next=chi(u)+pi(u)c_in, and Section4.2 p20 combines encrypted carry states with ONE ciphertext multiplication u_R+pi(u_R)(u_L−u_R) then logarithmic prefix. This is explicit direct prior art for compressed binary carry-map composition; the present H32 is not an original cryptographic mechanism.
- Ancillary public description of homomorphic parallel-prefix carry in Zama TFHE-rs Boolean SHA-256 tutorial https://docs.zama.org/tfhe-rs/tutorials/sha256-bool . FHE carry-lookahead generate/propagate is established general technique.

## [DERIVATION] Exact affine binary map and composition
Any total f:{0,1}->{0,1} satisfies f(c)=a+pc on Boolean c, with a=f(0),p=f(1)−f(0) in {-1,0,1}. For f_L(c)=a_L+p_L c and f_R(c)=a_R+p_R c:
 f_R(f_L(c))=(a_R+p_R*a_L)+(p_R*p_L)c.
So two CMult and public add suffice to compose adjacent intervals on SIMD slots. For monotone maps c∈{0,1}, only constant0, identity, constant1 occur, and a,p∈{0,1}, the standard generate/propagate semigroup. The source input bound for M=2^n and B=32 ensures binary carries on the ACTUAL c0=0 path; no claim of general-modulus λ-candidate validity.

Use doubling δ=1,2,4,... for each slot j≥δ:
 a_new[j]=a_old[j]+p_old[j]*a_old[j−δ]
 p_new[j]=p_old[j]*p_old[j−δ],
while preserving positions j<δ. After D=ceil(log2 ell) rounds a_prefix[j] is total transition 0→ output at index j; incoming carry c_j=a_prefix[j−1] (c0=0). Source second FBT already provides local bit-output functions h_jk(0),h_jk(1). Select after prefix:
 h_jk(c_j)=h_jk(0)+(h_jk(1)−h_jk(0))*c_j,
one ciphertext multiplication for each of s=5 bit functions. No extra FBT calls but **one extra multiplication layer** versus source Algorithm2, which propagates bit functions together with carry states. The candidate can possibly need extra CKKS level/modulus/precision and has not been native-validated.

General arbitrary M Algorithm4 is excluded: some candidate λ transitions may be invalid and indicators are all zero. Naively totalizing invalid states as zero can create false accepted candidate paths without an absorbing-invalid marker. No transfer claim to that algorithm.

## [TOY_EXECUTED] Exact rational/symbolic correctness and counts
Private deterministic Python checked all 4 total Boolean functions in chains of lengths 1..5 (all possibilities). It also ran 100 seed-fixed arbitrary binary map and 5 random bit-output function trials at ell=7,13,26,52, using the exact in-place doubling algorithm and final bit selection. All 400 random SIMD-position tests matched direct sequential carries/bit outputs (no noise or FHE implementation). This establishes just the ideal algebra.
For nbit=64,128,256 with s=5, ell=ceil(nbit/5) is 13,26,52 and D=4,5,6. Source count =12(D−1)+5 =41,53,65 CMult. Literal two-parameter schedule =2D+5=13,15,17 CMult, reductions 68.3%, 71.7%, 73.8% for the **carry/output selection subcircuit only**. Add one multiplicative depth (the source §5.5 says FBSB=19 levels; its concrete p27 allocations are one level larger than that simple formula, so do not give an exact actual extra q-bits claim).
Note the 2026/1840 single encrypted 3-state u encoding gives a ONE-CMult composition semigroup and could be better in CMult count (potentially D+5) but demands compatible encoding, public/complex conjugation, rescaling, and noise accounting. Its transfer is known-algebra prior art, not a new FHE idea or proven runtime gain.

## [OPEN] Noise, cost, novelty and decision
At exact Boolean values |a|,|p|≤1, so errors in the two-parameter composition satisfy a crude single-merge envelope |err_a'|≤3ε+ε² and |err_p'|≤2ε+ε² when three input errors are individually ≤ε, PLUS CKKS multiplication/rescaling/rotation errors. More exact joint DFR and scale management is needed; the saved CMult count excludes rotations, PMult, conjugations, FBT time, extra prime bits, evaluation key storage and total security. For power-of-two ALU Table5 the two FBT calls likely remain a large fixed cost, so a 68–74% carry-subcircuit CMult cut cannot be translated into end-to-end acceleration without matched native evidence.

The core compressed binary carry semigroup and log-depth parallel prefix were already explicit in 2026/1840 Section4.2, and elementary in classical carry-lookahead. Therefore H32 passes exact algebra and localized count but FAILS originality as an independent publishable cryptographic mechanism. PARK as a possible implementation comparison only, not a CodeX task without PI authorization. Do not continue similar binary-carry representations. Find a substantially different source-accessible PURE-FHE problem next.

END_OF_ITERATION
STATUS: PASS_EXACT_AFFINE_CARRY / FAIL_NOVELTY_PRIOR_ART / UNCLEAR_SYSTEM_GAIN
RESULT: 2026/1869 Algorithm2 carry CMult proxy 41→13 (64-bit), 53→15 (128-bit), 65→17 (256-bit) using affine prefix plus bit selection, at +1 multiplication depth; 2026/1840 independently contains more compact one-state carry semigroup.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: Source-first select one independent FHE technical bottleneck with credible nontrivial mechanism not already covered by contemporary papers; 2026/2618 and 2026/2616 require accessible complete originals before technical assertions.
STATE_UPDATE: YES only this isolated PURE-FHE finding.
CODEX_REQUIRED: NO. Native comparison pending explicit PI approval.
