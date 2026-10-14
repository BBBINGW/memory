# HLUT H05 — Quadratic full-rank prefilter rejects correct target-specific decompositions and slows paired search



Date 2026-10-15 Asia/Tokyo. Independent HLUT H05 follow-up to H04, with read-before-write START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, STATE.md and prior H04 finding. Global old general I192 frozen; independent vFHE V28 and SHIP I226 READ ONLY, no state changes.



## One primary hypothesis

H-HLUT-05: Testing rank_Fp W(U)=s^n before random D search is a semantics-preserving and offline-faster drop-in prefilter for the paper's target-specific HLUT decomposition compiler, at the same circuit shape and PBS count. W(U) is the span of singleton U columns and all pairwise entrywise products.



Falsifier: either exhibit target y in Col(A(D)) when rank W(U)<s^n, or show actual original accepted target-specific encodings lost, or measure negative wall-clock overhead in paired fixed-tape exact search.



## Original source/implementation [FACT]

Sonia Belaid, Nicolas Bon, Matthieu Rivain, Decomposition of Large Look-Up Tables for Fast Homomorphic Evaluation, TCHES 2026 Vol3, ePrint 2026/724, https://eprint.iacr.org/2026/724 . Full 32pp original Research MCP public fixed mirror PDF SHA256 cc45b49e20958f5c3fc1e327d84d1549d7fef08bdb4ba973dac75fd3a67efeb4; revision 108e41a7dc5788eb2d61023f9aecbcb72889d1d9; official parity VERSION_UNVERIFIED. Original §4 Eq(1),(4),(6)–(8) pp9–14 and §5.2 pp24–25 permit target-specific success even if rank(A)<s^n via canonical y in Col(A) or extended output encoding.



Author implementation https://github.com/CryptoExperts/artifact-HLUT-TCHES pinned commit 088029cb4cd3a6b33ac10e0c78ea193b1835216d: decomposer/src/decomposer/decomposition.py blob ce5d25df0ec2296c56a75c24e158f6cbe15f90f1: base chain passes rank(U)=n+lambda, D draws **binary** entries using np.random.randint(0,2) and resamples while rank(UD^T)<t, then checks A and target via use_encoding_switching=True. gauss.py blob 84d4c8b9889720cf4a8207b7bedc054cbbae6863 verifies the full target vector under canonical / augmented output encoding; first-output failures refresh entire chain. atomic_function.py blob 8599ee4cd39e318b68ca6be9ee03a2d7ef68fb9e samples alpha in F3, psi uniformly among 18 nonlinear unary maps; chain.py blob 5434a5917c9dc413204f0250391c6936d9706bff. Our independent exact F3 search emulates THIS logic, not author's compiled Python/Rust artifact.



## Decisive mathematical counterexample [DERIVATION]

Use source-shaped n4,s2,p3,lambda2,t2 chain x4=(2x0+2x2+x3)^2; x5=(2x0+2x1+2x2+x4)^2, binary D=((1,0,0,0,1,1),(1,1,1,1,1,0)). Exact finite-field ranks: rank(U)=6, rank W(U)=15, rank(A(D))=15. Choose target y=x0, the first output bit of the bijective identity 4-bit S-box. Because the source Eq(1) matrix A ALWAYS includes each column of U in the final linear block, choose beta to select U's x0 column: A beta=y exactly, canonical encoding. The new prefilter would reject this LEGAL and CORRECT source decomposition. Therefore rank W(U)=16, a necessary condition for decomposing EVERY target LUT, is NOT a necessary condition for compiling ONE chosen LUT. This kills H-HLUT-05 as a drop-in optimization without needing any runtime evidence.



## One paired exact local search test [COMPUTED]

Standalone script /mnt/data/hlut_H05_paired_prefilter_benchmark.py SHA256 c50675b30ca7f3b499270d9e168e915a9d7ea6ebdee5f1fe1d61ae5a743bbc9b; full reproducible JSON /mnt/data/hlut_H05_paired_prefilter_results.json SHA256 c041fcf524db1d8d4a93778f95ce8da225744f760d2ce8677a8106660faaf036. Ran exact mod3 Gauss–Jordan with Numba after JIT warmup on same presampled chains, same binary D (resampled until rank UD^T=t), and same balanced target y; baseline versus added W prefilter. Emulates first-output candidate acceptance including output encoding switching and all-index checking, not complete author MultiDec backtracking.



| n | (lambda,t) | candidates | baseline accepted | legitimate accepts lost by W prefilter | baseline paired local kernel median | filtered paired median | cost ratio |

|---:|---:|---:|---:|---:|---:|---:|---:|

|4|(2,2)|1800|761|312 = 135 canonical + 177 extended|10.45ms|12.20ms|1.17× slower|

|5|(7,2)|650|553|5 = 2 canonical + 3 extended|18.75ms|45.63ms|2.43× slower|

|6|(10,3)|250|45|0|37.47ms|101.43ms|2.71× slower|



The 4-bit first-accepted-solution paired episodes (100) increased average chain attempts from 2.36 to 3.46, and 35/100 selected a different successful chain. At 6-bit the prefilter rejected no full-U-rank candidate, merely added expensive W rank computation. An independent Numba test at n4 produced candidate index4: rank U6, rank W15, rank A15, balanced target y=(1,0,0,1,1,0,0,0,1,1,1,0,1,0,1,0), satisfying A beta=y EXACTLY under canonical encoding; prefilter incorrectly rejects. Fixed-tape rather than original exact PRNG-call sequence, common chain construction costs excluded, short local JIT timings NOT the paper's real compiler time nor FHE latency. This exact semantic counterexample remains decisive irrespective of benchmark timing.



## Research judgment

STATUS: FAIL H-HLUT-05 as a correctness-preserving and faster prefilter. PASS source-compatible explicit target-specific counterexample plus local paired finite-field test. Actual author Rust/Python compiler runtime and FHE ciphertext/DFR NOT measured; no original-paper error or cryptographic vulnerability shown.

RESULT: The symmetric-square rank lemma from H04 is true only as a universal representability necessary condition. Using it to discard a rank-deficient chain for a specific target LUT (and author's Encoding Switching) silently changes accepted outputs. The extra W elimination often outweighs eliminated full-A checks. No useful drop-in speed gain demonstrated.

NEXT_ACTION: PARK unconditional W full-rank prefilter. Only reopen after a semantics-preserving, target-aware and cheaply falsifying test, with author-equivalent offline walltime validation; avoid repeated local 'rank U vs rank W' toy work. Prefer a new source-grounded FHE problem or PI-selected vFHE. NOVELTY NOT VERIFIED.

STATE_UPDATE: YES this one failure file ONLY. NO global STATE/vFHE/SHIP/HERDS changes.