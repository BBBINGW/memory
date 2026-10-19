# BOOT-B041 — Shared radix-2 HomTrace tree for multi-valued RGSW ciphertext conversion

TRACK_ID: BOOT
ITERATION: B041
DATE: 2026-10-20
STATUS: PASS_EXACT_UNNORMALIZED_TRACE_SHARING / PASS_IID_KEYSWITCH_ERROR_PROJECTION_MODEL / FAIL_STANDALONE_NOVELTY_AND_FULL_BOOTSTRAP_SPEEDUP_CLAIM / UNCLEAR_NATIVE_NOISE_AND_SOURCE_CODE
STATE_UPDATE: YES
SCOPE: BOOT only. SHIP remains PAUSED_BY_PI after I407. No SHIP reads/writes.
NUMBERING NOTE: Existing BOOT findings already include TWO distinct B040-named archives, "boot-B040-cmt-lowrank-lut-contraction-source-cost-gate.md" and "boot-B040-whitebox-signboot-ternary-cleaning-hermite-prior-art-gate.md", with corresponding failures. DO NOT overwrite either; this new separate effort is B041. Notes read_repo_file returned {} for old files; metadata verified via list_repo_files. Existing BOOT state not rewritten, only appended.

## One minimally falsifiable source-first hypothesis
After B039 FEFBS affine-odd Fourier evaluation and two B040 branches already persisted, study DIFFERENT nontrivial source paper: Zhihao Li et al., "Leveled Functional Bootstrapping via External Product Tree" ePrint 2025/022. Its Algorithm 3 (Ciphertext Conversion with HomTrace, CCH) obtains all d RGSW gadget rows from ONE blind rotation but computes d separate HomTrace projections of shifted accumulator, each log2 d automorphism key switches. Hypothesis: multi-output trace extraction can be implemented as ONE radix-two *shared-output* butterfly tree of d−1 automorphisms and no new eval keys, while keeping ALL d separately usable RLWE gadget rows and correct exact ring semantics even at 2-power ciphertext modulus. The decisive cheapest test: derive ring-automorphism identity, exact exhaustive random ring-operation comparison for several d and even moduli, then analyze full row-error covariance and end-to-end dominant blind-rotation cost/prior art. Not a SHIP research direction.

## Source identification and limitations
[FACT] Zhihao Li, Xuan Shen, Xianhui Lu, Ruida Wang, Yuan Zhao, Zhiwei Wang, Benqiang Wei, "Leveled Functional Bootstrapping via External Product Tree", IACR ePrint 2025/022, https://eprint.iacr.org/2025/022.pdf (public official PDF 35 pages, archived web text tool ref turn555958view0); source pdf physically page12–14 / original print sections3.1–3.3: Algorithm3 constructs acc=Σ_(j=0)^(d−1) B_j X^(-b'+j), performs ONE blind rotation and for every i performs ct_(i+d)=acc X^(−i), Eval.Tr_(K_N/K_(N/d))(ct_(i+d),ATK), then RLWE.SKSwitch; Table2 p14 gives one BR, d(log2d+1) RLWE key switches/gadget products 2n+d(log2d+1). Paper's special modulus switch forces all phase exponents ≡0 mod d to separate gadget factors into distinct residue classes. Exact source uses unnormalized trace c+HomoAuto(c) (not free division by2); modulus Q can be 2-power, so 2 is NOT invertible.
[FACT] Same paper Algorithm5, physical page17–18 ("Packing RLWE Ciphertexts via Automorphism / PRCA") ALREADY exploits a paired butterfly identity (a+X^r b)+Auto(a−X^r b) to reduce automorphisms, with B−1+log(N/B) group operations. Thus sharing automorphism outputs across two branches is ALREADY IN THIS PAPER and an elementary FFT/NTT-style technique; applying it to Algorithm3 is not a novel cryptographic primitive absent distinct secure/efficient algorithm proof and benchmarking.
[QUALITY] Research GitHub Notes get_eprint_paper("2025/022") FAILS due an interface normalization to "2025/22" -> metadata HTTP404 (no repository cache). Official public PDF text was read via web and exact lines/source linked. Web PDF screenshot was attempted for physical pages12,13,16 but the screenshot service returned HTTP403; the displayed formulas were checked against text-extracted equations and independently mathematically derived, not separately visually validated. Authors claim OpenFHE implementation in abstract, but no matching AUTHOR SOURCE FUNCTION for Algorithm3 was verified this round. DO NOT claim native source/code/FFT benchmark, nor SHA256 of acquired bytes, nor an independently confirmed 2026 final revision. This is a published-source math and code-independent reference test.

## Public arithmetic construction [DERIVATION]
Let R_q=Z_q[X]/(X^N+1), N=power-of-two, d=2^ell|N. Define Galois involutions
  sigma_t:f(X)↦f(X^(1+N/2^t)),  t=0,...,ell−1.
The Galois exponent 1+N/2^t is odd for t≤ell−1≤log2 N−1, hence automorphism of R_q.
For a polynomial F whose monomial exponents are ALL divisible by 2^t (the invariant after t splits), on an exponent 2^t k:
  sigma_t(X^(2^t k)) = X^(2^t k+N k) = (−1)^k X^(2^t k).
This sign distinguishes parity of k. Make TWO outputs from ONE automorphism:
  EVEN_t(F) = F + sigma_t(F)
  ODD_t(F)  = X^(−2^t)*(F−sigma_t(F)).
Both outputs have monomial exponents divisible by 2^(t+1), and their coefficients are multiplied by2. Recurse on both children and maintain the low-to-high binary residue prefix (leaves appear in bitreverse order).
For arbitrary F=Σ f_i X^i, each final leaf j=0,...,d−1 equals
  T_j(F)=Tr_(R/R_d)(X^(−j) F)=d Σ_(k=0)^(N/d−1) f_(kd+j) X^(kd)  (with ring signed exponent convention),
exactly the independent source Algorithm3 trace output, including overall factor d and proper negacyclic shifting. No division by2 or ring automorphism of invalid exponent required.
For one source-output row after CCH, retain existing RLWE.SKSwitch of each separate leaf, so result is still the d encrypted gadget rows necessary to assemble output RGSW under original ring secret. No illegal replacement of d RLWEs with ONE packed RLWE; earlier B028 type mismatch avoided.
Key material: need the same ell Galois automorphism key exponents 1+N/2^t as source independent traces, plus the original d RSK calls. Data dependency: all shared nodes are level-parallel; online automorphism call count is sum_(t=0)^(ell−1)2^t=d−1 vs independent d*ell. No claim original implementation does or does not have an extra optimized path absent verified source.

## Exact independent negacyclic correctness tests
Implement coefficient-vector ring operations under negacyclic X^N=−1, Galois ψ_u multiplication of each monomial exponent by u mod2N and sign when crossing N, arbitrary monomial shift X^k, addition moduloq.
Independently implement (a) d shifted individual unnormalized traces with ell autos each and (b) unnormalized binary multi-output tree with one auto/internal node. Test random general F∈R_q, NOT only intended sparse gadget F; all d entire RLWE plaintext polynomials exactly equal, not just constant coefficients.
Tests (random deterministic RNG20261020):
  q∈{2^12,2^32,65537}
  N∈{16,32,64,128}
  d∈{2,4,8,16}, d<=N
  40 full-ring randomized samples each of3*4*4=48 configurations
  1920/1920 exact comparisons PASS. Additional 1520/1520 q65537 random tests across N8/16/32/64/128 and valid d passed in earlier native Python reference, but report 1920 as the authoritative multi-modulus gate. The equality is an algebraic theorem, so test scale is a sanity check rather than proof.
Reference operations were run privately with Python exact integer arithmetic, not actual OpenFHE or CRT/RNS firmware. Correctness of encrypted Galois key-switching at original level follows original primitive semantics if keys exist, but approximate rounding and its total tails remain to prove.

## Decisive one-level cost model
Source Algorithm3 Table2: one blind rotation (about 2n external products), d log2d Galois-based RLWE key switches for d separate traces, plus d distinct RSK switches. Candidate: one blind rotation, d−1 Galois key switches, d RSK switches.
  d=2: source trace2, tree1, total source KS4 vs tree3.
  d=4: trace8→3 (62.5% trace reduction), total KS12→7.
  d=8: trace24→7 (70.83%), total KS32→15.
  d=16: trace64→15 (76.56%), total KS80→31.
Total major operations in an oversimplified equal-gadget-product cost model 2n +d(log2d+1) → 2n +(2d−1). At illustrative n=630:
  d4: 1272→1267, 0.3931% fewer model products;
  d8: 1292→1275, 1.3158% fewer;
  d16:1340→1291,3.6567% fewer.
These are NOT elapsed-time savings because automorphism key switches differ in kernel cost from BR external products, and host memory/cache/NTT/FFT may dominate. Nothing changes key count, output RGSW size, BR noise, gadget-digits, or number of SKSwitch rows. d is normally small, so this is a promising local implementation optimization but very weak standalone new full PBS algorithm contribution.
Avoid conflating Algorithm3 CCH with Algorithm5 PRCA! Their tree operations are at different stages. Homomorphic trace algorithm cost may already be optimized in the original OpenFHE code; source implementation not verified.

## Linearized noise / correlation test and precise limitations
A new tree shares the SAME automorphism switched ciphertext (and new key-switch error polynomial) between two sibling branches with opposite signs, unlike independent d trace invocations. To check necessary covariance impact, model each Galois key-switch invocation as adding an independently sampled *coefficientwise independent* error polynomial e_node with Var(each coeff)=1, 0 mean, independently across nodes and from inputs. Treat all other evaluation and rounding exact. Construct exact linear transfer matrices from EACH error coefficient at every internal tree node to ALL final active coefficients (indices 0,d,2d,...,N−d in each leaf). Similarly for separately evaluated independent traces, errors at each of d*ell autos. N16, d=2,4,8,16:
  d2: marginal output coefficient var shared=separate=1, max cross-output coefficient covariance=0.
  d4: var=5 both, max cross-output coefficient covariance=0.
  d8: var=21 both, max cross-output coefficient covariance=0.
  d16: var=85 both for leaf coefficient0, max cross-output covariance coefficient0=0. Full active cross-output covariance checked for d2,4,8, all zero.
These variances include UNNORMALIZED trace scaling: level-k auto error multiplied by factor2 for each later pass; general scalar model marginal variance Σ_(r=0)^(ell−1)4^r=(4^ell−1)/3, same in tree and independent baseline. Under IID coefficient error assumption, different residue outputs read DISJOINT original coefficient classes from the same shared error polynomial after exact projections, explaining zero cross covariance. This is a useful positive form of the B036 projection-aware error reasoning, but DOES NOT GUARANTEE REAL FHE equality:
- True RLWE KS errors are sums of gadget-digit/convolution terms depending on ciphertext and evaluated encrypted selector, and can correlate across coefficients, nodes and across repeated use of the SAME Galois keys. Also input BLIND ROTATION noise and RSK errors are not captured.
- Source paper Appendix B already noise-analyzes HomoTrace, but cannot automatically apply an independence-based sum to new shared-key error graph. Need a full analytic noise and DFR bound including original key correlations, the RGSW external product with all d rows, and final LUT extraction, before claiming unchanged DFR/128-bit security.
- Simultaneous reveal of multiple row ciphertexts are deterministic public homomorphic functions of the SAME blind-rotation ciphertext and the original public Galois keys. Cryptographic indistinguishability may inherit secure input public-key transcript under allowed circular/KDM assumptions, but actual joint RGSW encryption form and statistical error law differ from independently switched rows; no security proof here.

## Prior art novelty + decision
This implementation is the textbook all-output radix-2/FFT factorization of multiple residue-class projections. The VERY SAME PAPER already uses a paired automorphism butterfly in its packing Algorithm5 PRCA, and general projection/trace-tree methods are long-established. Therefore not a new primitive, no author-source confirmation that actual code misses this sharing, and no end-to-end runtime/DFR advantage. Stronger than mere local trick because it preserves exact native Algorithm3 output types and admits a favorable coefficient-IID covariance result, but should NOT be presented as a cryptographic paper-ready contribution. CONDITIONAL engineering candidate if author implementation repeats traces.
STATUS: PASS_EXACT_RING_OUTPUTS / PASS_CONDITIONAL_IID_VARIANCE / FAIL_PUBLISHABLE_NOVELTY_AND_SIGNIFICANT_MODEL_SPEEDUP / UNCLEAR_NATIVE_IMPLEMENTATION.
RESULT: 1920/1920 exact negacyclic ring tests pass, 64→15 trace key-switch count for d16, same d final RSK + one BR; conditional no added iid-coefficient noise covariance in final separate gadget rows, but real KS noise/circular security and author-code/perf not verified. Good transfer of problem-first and projection-aware lessons, yet no original new Bootstrapping algorithm.
NEXT_TEST B042: Since B039 and TWO B040 branches plus B041 all lack paper-grade novel whole algorithm, prioritize identifying a truly substantive current 2026 bootstrapping primitive/correctness/representation gap with FULL PAPER+AUTHOR IMPLEMENTATION. If no such source, request HUMAN_REVIEW on scope/pivot rather than infinite simple trace/gadget/key-format dedups. Do NOT spend a further BOOT round merely applying textbook trace butterfly; only resume this if original native code and secure noise bound reveal a material win. SHIP still paused. B042 NOT STARTED.
STATE_UPDATE YES. BOOT-only paths.
