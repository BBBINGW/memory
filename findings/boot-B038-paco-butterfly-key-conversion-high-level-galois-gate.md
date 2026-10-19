# BOOT B038 — PaCo multi-C BSK conversion: exact butterfly factorization, operator norm, and highest-level Galois-key obstruction

TRACK_ID: BOOT
ITERATION: B038
DATE: 2026-10-20
STATUS: PASS_EXACT_PUBLIC_BUTTERFLY_REENCODING / PASS_NONAMPLIFYING_OLD_SLOT_ERROR_OPERATOR / FAIL_FREE_OR_EXISTING_KEY_LEVEL_CONVERSION / UNCLEAR_NATIVE_SECURE_PARAMETER_END_TO_END_COST / ARCHIVE_MULTIC_MICROBRANCH
STATE_UPDATE: YES
SHIP: PAUSED_BY_PI after I407. No SHIP experiments, no SHIP files touched.

## Primary hypothesis and cheapest decisive test
Continue the single B037 question: for Coron–Seuré PaCo (ePrint 2025/886, ASIACRYPT 2025), different coefficient capacity C requires four BSK ciphertexts at that C. B037 showed a dense public linear map A_C=M_C pinv(M_B) can derive smaller-C BSK plaintext vectors from the maximal B=N/(4h) version, but native CKKS diagonal encoding of this particular dense A_C used all slots' cyclic diagonals. Is there a factorization USING AUTHOR'S OWN PARTIAL-COEFF-TO-SLOT BUTTERFLIES and one-hot layout to reduce conversion to O(log N) public rotation-linear layers, with negligible noise/memory/level cost and actual multi-C evaluation-key savings? Cheapest decisive: derive a source-specific explicit factor, verify at more than one N and all t, check full ambient-vector equality to pseudoinverse, then audit source's Galois key modulus levels and full operation/novelty cost. ONE primary hypothesis, not an additional SHIP project.

## Sources [FACT], precise original and code provenance
Coron–Seuré, "PaCo: Bootstrapping for CKKS via Partial CoeffToSlot", ePrint 2025/886, ASIACRYPT 2025 proceedings Springer DOI 10.1007/978-981-95-5122-4_2, pp36–67, online 2025-12-08. Research Notes title-matched, full 35pp ePrint PDF SHA256 ee427d006097fabdbd30a0a4dc36ed09df5ffea68df30a0511cc154b303a936a VERSION_UNVERIFIED. Author postprint https://orbilu.uni.lu/bitstream/10993/64983/1/PaCo.pdf. Physical pp18–25 Algorithms1–5, pp26–27 Table4 cost/security; pp28–30 §8 sparse secret structure, full coefficient limit.
Original AUTHORS repository https://github.com/se-tim/PaCo-Implementation:
- paco_package/ckks_x.py Git BLOB ea8073682c82dadcc892ab48b29e8d8bc4ccc237: bsk_gen lines116–151 exactly uses k=N/(4hC), n=2hC, per-t/r/v onehot layout and source butterfly get_matrix_D(n,l) for l=log2 C down to0, extended bit reversal by C/2; lines199–217 generate Galois switch keys at q=cls.moduli_boot[-2], P=cls.moduli_boot[-2], NOT highest modulus q_L. seq_PaCo lines280–300 first multiplies coeff encoding ×BSK then trace/rotation/complex plaintext operations. parallel_PaCo lines302–342 calls separate seqPaCo on public monomial-shifted input for each processor; source normally configures ONE C.
- paco_package/fast_dft_with_ext_bit_rev.py blob604fdcf0c3b82b6c3784a7454aa47c0e97d17d03: get_matrix_D(n,l) delegates to get_E(n,l) in author submodule.
- paco_package/ext_bit_rev.py blob8eaa7cd04e3e0b97bc932a936a58926cf05c347c: permutation P_C.
- author submodule se-tim/CKKS-in-SageMath, ckks_package/fast_dft.py blob ee6c9dfbb7393c1b78ba6f994d7b802e5800d3e8: get_E(n,l) is 2×2 root-weighted butterflies, l=log C down to0; operator norm/root details from the published exact public matrix.
- same author submodule ckks_package/ckks.py blob d93f13fe7a49382b75feb0e375dd3810b26cb732: get_swk lines186–216 keys modulo q*P; get_galois_swk lines219–251; __matmul__ lines931–944 performs multiplication then rescale; galois lines1057–1087 requires Galois key to call key_switch; BSGS_left_mult lines1319–1352 applies rotations and plaintext diagonals, then .rescale(). THIS IS SOURCE-EXACT functional constraint, not merely a theoretical CKKS requirement.
Original paper physical p23 Table3 gives PaCo total L=ceil(log(2C)/g0)+ceil(log(C/2)/g1)+log h+3; physical p26 Table4 PaCo I N=2^15 h64, L14, logΔ32, log(PQ)934; PaCo II N=2^16 h64, L15, logΔ48, log(PQ)1496. p26 specifically states existing Galois switching keys used only at L−1 and below, contrasting original CKKS at L. Main advertised key material saving depends on that low-level switching-key modulus.
Modern prior art: conventional CKKS diagonal linear transforms + BSGS/hoisting already optimize public matrices, FFT/bitrev butterflies are textbook. Orion CKKS.org current article https://ckks.org/blog/2026/orion/ details one-level BSGS rotations/memory cost. Generic public permutation via a 2log n−1 stage Beneš switching network is also classical; no novelty claim for factorization itself.

## [DERIVATION] Exact explicit PaCo cross-capacity conversion, NO PSEUDOINVERSE COMPUTATION
Let B=N/(4h) (powers2), C|B, k=B/C, Lslots=N/2=2hB. Let d_t∈C^(hB) index hypothetical onehot positions pos=0..B−1 within each v∈[0,h) for fixed t. The true key plaintext is sigma_t(C)=P_C F_C Q_C d_t, all maps public:
 - Q_B: embed d_t[v,pos] into raw vector length Lslots at index v*(2B)+pos; other positions zero. Q_B^T Q_B=I.
 - for smaller C, construct Q_C using source index arithmetic: for each (v,pos), choose r=(-pos) mod k, j=(pos+r)/k=ceil(pos/k); send d_t[v,pos] to concatenated raw vector block r of length n=2hC, local index v*2C+j. Since u=j k-r, the map (v,pos)↦(r,v*2C+j) is injective, and 0≤j≤C; hence Q_C^T Q_C=I. This is an exact public PARTIAL PERMUTATION, no multiplication between secret coordinates.
 - F_C: apply author E(n,l) for l=log2C down to0 IN EACH r block; each E is root-weighted pair butterfly [[1,w],[1,−w]] after pair ordering, with |w|=1, so E*E=2I. F_C*F_C=2C I, same for F_B*F_B=2B I.
 - P_C: per-author extended-bit-reversal permutation after concatenating r blocks. P_B similarly.
For maximum C=B, k1 and Q_B as above, sigma_t(B)=P_B F_B Q_B d_t. Since F_B is invertible, recover position data by Q_B^T F_B^-1 P_B^-1 sigma_t(B). Then re-encode at C:
   A_C^structured = P_C F_C Q_C Q_B^T F_B^-1 P_B^-1;
   sigma_t(C)= A_C^structured sigma_t(B)  EXACTLY for all onehot secret choices in this model.
Because F_B^-1=F_B* /(2B) and Q_B^T Q_B=I, Moore-Penrose left inverse of M_B=P_B F_B Q_B is M_B^dag=Q_B^T F_B^-1 P_B^-1. Therefore A_C^structured=M_C M_B^dag as a map on the ENTIRE ambient Lslots-dimensional vector space, not just the valid key subspace. This strengthens B037's existence statement and means its canonical pseudoinverse was precisely a FACTORIZED public FFT/packing operator.
Singular values: P and F/√(2C) and F_B/√(2B) are (block) unitary; Q_B^T is partial isometry and Q_C is isometric embedding. Therefore A_C=sqrt(C/B) U_C (Q_C Q_B^T) U_B*, with U_B and U_C unitary; nonzero singular values ALL sqrt(C/B), operator norm ||A_C||2=sqrt(C/B), rank hB. This gives a norm bound on any PREEXISTING plaintext-slot noise vector; DOES NOT bound new CKKS rotation/key-switching/rescale errors, or any high-modulus evaluation-key security concern.

## [VERIFIED] Independent exact-source-shaped algorithm tests
Local scripts in current container, source-matched complex NumPy (not Sage/native ciphertext), deterministic RNG:
  /tmp/boot_b038_fact.py SHA256 1fee9467d0ebe9add7ec54aa56a187e0b6c9675d0247ceec9d4b033a5d67e8b6;
  /tmp/boot_b038_compare.py SHA256 1ca63b944e52e5fcd89959cddeec7d364cc553032dc62e94f347ca2f9d86d67e;
  B037 basis model /tmp/boot_b037_paco.py SHA256 4bf38223a4b47241c326a4015a08355a8f89587db056cf37d095beda086a6b9e.
The source-shaped factor code first undoes public bitrev, applies inverse E_l stages in increasing l to reconstruct d_t, extracts exactly v*2B+pos coordinates, scatters to smaller C via r=(-pos)%k, j=(pos+r)//k, applies exact author E_l in decreasing l, and finally public ext-bit-reverses.
Independent valid secret onehot tests, four t keys:
 N64,h2,B8,target C2,C4: 400/400 PASS, max err2.49e−16.
 N128,h2,B16,target C2,C4,C8: 600/600 PASS, max err4.01e−16.
 N256,h4,B16,target C2,C4,C8: 600/600 PASS, max err4.01e−16.
 N512,h4,B32,target C2,C4,C8,C16: 800/800 PASS, max err5.67e−16.
 Total 2400/2400 PASS; all FLOAT complex plaintext linear tests, insecure toy N/h. Not a real CKKS noise/DFR/security/native correctness test.
On full ambient vectors, explicit A_C assembled from applying factor to EVERY standard basis vector and compared to M_C*pinv(M_B):
 N64,h2,C4: max difference1.95e−16, rank16, ||A||2=0.70710678=sqrt(C/B).
 N128,h2,C8: max difference1.95e−16, rank32, same norm.
 N256,h4,C8: max difference1.89e−16, rank64, same norm.
 These verify exact operator equality to numerical tolerance, not an integer-field theorem from mere simulation; mathematical identity above is independent.

## [DERIVATION] Layered rotation schedule, CONDITIONAL asymptotic positive result
Each source butterfly E_l or inverse is a 2×2 pair matrix using diagonal offsets 0,+2^l,-2^l on each corresponding block; if implemented as ungrouped CKKS diagonal method, <=2 nontrivial slot rotations per stage. Public P_B^-1, P_C and partial scatter Q_C Q_B^T are each either a permutation or an injected partial permutation + a plaintext mask. Any public permutation of n=2hB power-of-two slots can be implemented through a standard 2log2(n)−1 stage Beneš 2×2 switch network; at each network stage, each pair switches or stays based ONLY on a public mask, and uses <=2 nontrivial ±2^l slot rotations with masks. For partial injection, extend to any total permutation and mask unused positions. The existence bound is valid but this Beneš stage network was NOT compiled or optimized in the original CKKS library; it is not measured code.
Naive upper number of nontrivial rotations per ONE key conversion <=2[(log2B+1)+(log2C+1)+3(2log2(N/2)−1)], plus a final partial-injection plaintext mask. This is O(log N) rotations / O(log N) sequential PUBLIC linear layers, not a proven tight lower bound.
Examples for C=B/2:
 N64,h2,B8,C4, slots32: <=68 rotations (versus dense diagonal31).
 N128,h2,B16,C8, slots64: <=84 (versus dense63).
 N256,h4,B16,C8, slots128: <=96 (versus dense127).
 N512,h4,B32,C16, slots256: <=112 (versus dense255).
 Real PaCo I N32768,h64,B128,C64, slots16384: inverse+forward butterfly15 stages, 3 Beneš permutations <=81 layers, <=192 rotations PER converted BSK (4 BSK=>768), under generic loose construction.
 Real PaCo II N65536,h64,B256,C128, slots32768: 17 butterfly stages +<=87 permutation layers, <=208 rotations PER converted BSK (4 keys=>832).
 One can alternatively use the DIRECT dense A_C plus textbook baby-step/giant-step, ~2sqrt(n) rotations but potentially 1 plaintext multiplication level, or group/fuse many butterflies. Source already uses BSGS and grouping for its NORMAL procedure. The layered construction is NOT a measured win vs tuned BSGS: for n16384, naive BSGS ~254 rotations/key at one level, close to <=192 but with much more conservative stage depth; for n32768 BSGS ~361 vs<=208, with same caveat.
 All stage bounds above are theoretical UPPER bounds, not native timing, not necessarily multiplicative LEVEL counts: plaintext masks with special scale/fusion may be optimized, but source's BSGS_left_mult explicitly rescale() once per grouped linear transform and __matmul__ also rescale(). Explicit stage-by-stage realization could far exceed the AVAILABLE PaCo bootstrap depth, which Table4 sets to L14 or L15. No low-level/noise-safe compiler of this factoring has been verified.

## [DECISIVE] Native keyset and modulus-level mismatch
The maximal-C BSK ciphertext is encrypted at the HIGHEST boot modulus Q_L (PaCo I log2 Q_L=499, PaCo II log2 Q_L=796). The normal first usage in seqPaCo line283 is encoded_coeff ×bskt, a plaintext-ciphertext multiplication followed by rescale, so the paper can arrange all NORMAL Galois key switching after this first level drops; original PaCo paper p26 explicitly says ALL switching keys are used only at level L−1 and below.
Source bsk_gen lines203–217 creates Galois keys with q=moduli_boot[-2] (Q_{L-1}), P=Q_{L-1}, resulting key modulus q*P=Q_{L-1}², i.e. original logPQ PaCo I 934bits; PaCo II 1496bits. If one ROTATES the encrypted maximal-C BSK BEFORE the first ciphertext×plaintext bootstrap operation, input modulus is Q_L, and standard same-modulus key switching cannot safely assume an evaluation key made ONLY for q=Q_(L−1) is valid at Q_L. The source key-switching formulas lift a from input q and multiply by swk under q*P: to do high-level rotation, new keys at least appropriate to Q_L*P are required (or modulus switch the BSK to Q_(L−1) first, thereby losing a level and upsetting current bootstrap chain). This is an ACTUAL SOURCE-FORMAT/capability obstacle, beyond extra rotation count.
Holding P=Q_(L−1) for high-level BSK rotation would require switch-key modulus Q_L*Q_(L−1):
   PaCo I log=499+467=966 bits vs existing934 (32 extra).
   PaCo II log=796+748=1544 bits vs existing1496 (48 extra).
Choosing P=Q_L for comparable original P/q precision yields Q_L² modulus logs998 vs934 (PaCo I) and1592 vs1496 (PaCo II), potentially even bigger evaluation key bytes. Whether numerical security and KDM remain credible requires new estimator; not evaluated.
On-paper BSK stored only 4 objects per ONE C; a multi-C evaluator storing 8 or12 is hypothetical. Adding new highest-level Galois keys may outweigh saving 4–8 BSK ciphertexts, especially since switching keys use larger modulus. Need count the new Galois exponents (±2^j) not already in source key set, serialization, use-level, noise, and untrusted-key security. No actual secure memory gain proven. Source's standalone BSK encryption can be generated separately at keygen time, making multi-C conversion only a key-distribution/time tradeoff.

## Prior art, correctness/security/noise, and final decision
Local plaintext correctness PASS, explicit general algebraic factoring PASS with rank/norm, source equivalent to pseudoinverse. Security: issuing public homomorphic functions of secure BSK with high-level rotation keys adds no independent secret oracle under suitable key-security assumptions, but WHICH circular/KDM assumptions govern those HIGHER modulus keys is unproved. Even without norm amplification of old key plaintext error, every rotation key-switch/round introduces NEW correlated noise, and composing many mask multiplications likely changes levels or key precision. No native Sage/CKKS full ciphertext test, no secure-parameter error/precision/latency/memory profile and no comparison to author's separately generated keys or grouped BSGS. No cryptographic novelty beyond classical FFT, sparse embedding, permutation routing and public CKKS linear transforms.
STATUS: PASS_PUBLIC_STRUCTURED_REENCODING / PASS_OLD_NOISE_NORM_BOUND / FAIL_OLD_EVAL_KEY_MODULUS_FOR_HIGH_LEVEL_CONVERSION / NO_EVIDENCE_NET_MEMORY_OR_PAPER_NEW_BOOTSTRAP.
RESULT: This completes decisive B038 repair gate. The best constructive piece is an exact public, factorized, isometry-scaled A_C for key-plaintext multiresolution conversion; but the real on-line conversion requires higher-level Galois keys (not present in original PaCo profile), many rotations/linear layers, and benefits only an unusual multi-C setup. Therefore archive B037–B038 PaCo multi-C key-format microbranch as presently noncompetitive and low novelty; do not indefinitely tune butterfly wiring.
NEXT_TEST B039: Resume BOOT source-first broad paper audit with a DIFFERENT real bootstrapping algorithm and strongest chance of NEW CORE computation/dataflow/correctness/keys/noise innovation. Do not return to CMS knapsack, BatchBoot row dedup, or PaCo multi-C reencoding unless new independent genuine primitive enables a nontrivial secure full construction. Seek paper with complete PDF and author code; pick ONE smallest falsifiable hypothesis, test all source types and end-to-end implications. SHIP remains PAUSED_BY_PI, no SHIP research or write.
STATE_UPDATE YES, only BOOT paths changed.
