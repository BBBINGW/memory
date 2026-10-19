# BOOT-B050 — Repeated A2B correction rotation hoisting and CKKS key-switching noise

TRACK_ID: BOOT
ITERATION: B050
DATE: 2026-10-20
STATUS: PASS_IDEAL_ROTATION_MASK_COMMUTATION / PASS_SUBLOOP_ROTATION_COUNT / FAIL_UNCHANGED_NOISE_ASSUMPTION / UNCLEAR_NATIVE_DFR_LATENCY_NOVELTY
STATE_UPDATE: YES
ISOLATION: BOOT only; SHIP paused after I407; no SHIP changes.

## Recovery and one primary hypothesis
GitHub Notes list_repo_files identified latest preexisting BOOT B049 finding, findings/boot-B049-smoothie-public-offset-u256-radix-width-gate.md (SHA f51562e0065dc026f062c28417665cb3d397da9d), B048 YATA, and STATE. read_repo_file persistently returned an EMPTY object {} even for known files, so their exact text/NEXT_ACTION was NOT actually accessible; do not falsely assert it was read. This is one genuinely different B050 experiment chosen from verifiable source outside prior smoothie/YATA lines.
PRIMARY: In Gao–Zheng CRYPTO2026 SIMD-ALU FHE, batched arithmetic-to-boolean (B-A2B) code rotates separately for EACH public plaintext mask j, even though rotation amount is identical across all j for any fixed iter,nextIter. Can we rotate the LUTID ciphertext once per pair then multiply by rotated masks, reducing rotation KSK calls while preserving correctness/noise/DFR and key storage? Cheapest tests: exact algebra, source-derived operation count, and a precise key-switching-error position counterexample.

## Original paper and source [FACT]
Mingyu Gao, Hongren Zheng, "FHE for SIMD Arithmetic Logic Units with Amortized O(1) Bootstrapping per Ciphertext", CRYPTO 2026, pp299–330, ePrint 2026/233. Full original research MCP mirror PDF source GitHub IACR mirror SHA256 f16f4004d76450fb2264e6a5b36c3eceac2f87586148b96073c76ca7775f0f92, 43 physical pp, VERSION_UNVERIFIED. Physical pp20–23 §5 A2A and B-A2B: each iteration extracts LUTID/LUTMSB and subtracts shifted, scaled low digit; published n/w batched ciphertext approach. Authored code https://github.com/tsinghua-ideal/fhe-simd-alu :
- src/pke/lib/scheme/ckksrns/z-fhe.cpp git BLOB SHA 8ac367867f9928f6f5712ff5e8c9cb6f8a18ca02, lines583–784 EvalArithToBooleanBatched. For each iter < nextIter, until (iter-nextIter)*w <= cutoff, the inner j loop lines705–732 executes twice: public mask getATBSubtractMaskFullPacking(iter+j,...,scaleDown); scaled=EvalMult(lut0/lut1, mask); scaled=EvalRotate(scaled, rotationIndex); ModReduceInPlace(scaled); subtract from j-th core ciphertext. rotationIndex depends on iter,nextIter, may have half-crossing correction, NOT j. Each LUTID result changes with iteration: DO NOT move rotation across the nonlinear LUT or hoist across iterations.
- src/pke/lib/scheme/ckksrns/z-fhe-precompute.cpp git BLOB SHA 7412caec6bb755ee43eb08785158159983c37e92, lines817–853: getATBSubtractMaskFullPacking creates PUBLIC slot one-hot mask, coefficient value scaleDown=2^((iter-nextIter)*w), encoded at scalingFactor sf; it caches masks by (iter,w,zN,zSlots,modulus,sf,scaleDown). For first next iteration at w=4, amplitude is 1/16, NOT one. Further iterations 1/256,1/4096. Wrapper z-fhe.cpp lines1039–1080 ALREADY pads small batches by cloning input and calls batched method; NOT B050 novelty.
- Original cached benchmark logs exist but no native build/bench was executed in this turn. Per-file SHA, repository-wide commit not pinned.
[PRIOR ART] Halevi–Shoup ePrint2018/244 hoisted automorphisms and BSGS for HE linear maps are known. Yan et al. PKC2026 ePrint2025/1403 level-conserving rescale and aggregated key switching (https://ckks.org/blog/2026/less-mod-ckks/) explicitly investigate such ordering and memory/noise interplay. Algebraic rotation/public-mask fusion alone is NOT cryptographically novel.

## Algebraic construction and deterministic exact gate [DERIVATION]
For CKKS slot rotation rho_r, public slot mask P_j and LUTID ciphertext x, as exact plaintext messages
  rho_r(x ⊙ P_j) = rho_r(x) ⊙ rho_r(P_j).
Original: for every j, EvalRotate(EvalMult(x,P_j),r) then ModReduce.
Proposed: EvalRotate(x,r) ONCE per (iter,nextIter), then for all j EvalMult(that, public pre-rotated rho_r(P_j)) and ModReduce. Apply independently for LUTID halves lut0/lut1; keep same accumulator updates/valid slot selections. This is an IDENTITY of ideal slots, but CKKS approximate ciphertext key-switch/rescale order differs.
Local /tmp/boot_b050_test.py deterministic random.Random(20261020): for slot vector sizes 16,32,64,128, 2500 random integer vectors and binary masks per size with uniformly varying signed shifts; 10000/10000 exact lhs=rhs PASS. No ciphertext/torus/CKKS native test.

## Precise source op count
Let Z-bit width zN, w=4, iteration count d=ceil(zN/w), source full batch size d; half=d/2, cutoff=-16 implies only positive nextIter−iter<4, so count pairs R=sum_{k=1}^3(d−k).
Each pair and j in [0,half) source 2 rotations (lut0 and lut1), total 2*half*R. Candidate 2*R. The mask/plain-multiply and correction count is UNCHANGED.
  zN64, d16,R42 => original672, candidate84, 87.5% fewer rotations IN THIS ONE CORRECTION LOOP.
  zN128, d32,R90 => original2880, candidate180 (93.75% less in loop).
  zN256,d64,R186 => original11904, candidate372 (96.875% less in loop).
  zN64,w4,cutoff=-24 => R65, source1040, candidate130.
Not a total bootstrapping latency or memory saving; many LUT, transforms and other rotations remain. Since source masks cached already, rotated mask cache will be additional public plaintext memory/encoding work.

## Decisive CKKS rescale/key-switch noise placement obstruction
The source orders EvalMult(x,P_j) -> EvalRotate -> ModReduce. With original input scale Δ, mask plaintext P_j encoded at scale Δ and slot value p_j of magnitude 2^(-kw), the multiplied ciphertext has scale ~Δ²; a key-switch raw error kappa_post injected by rotation BEFORE final rescaling by ~Δ yields final error kappa_post/Δ.
If rotation happens BEFORE multiplying by encoded mask, raw key-switch error kappa_pre enters ciphertext scale Δ, is multiplied by Δ p_j and rescaled /Δ, yielding error p_j*kappa_pre. Under same raw key-switch error distribution at identical modulus, candidate vs baseline error stdev ratio is approximately Δ|p_j| and variance ratio Δ²|p_j|². This error is correlated across j because one rotated LUT is shared; real decomp/digit distribution can change and must be re-proved.
Exact single-coefficient constructed example: Δ65536, public p=1/16, key-switch error kappa=16. Baseline relative output KS error16/65536≈0.000244, candidate error16/16=1, factor4096. A second seeded 100000-sample scalar experiment with kappa uniform[-16,16] measured normalized mean squared KS contribution baseline 2.1085960324853657e−8, candidate 0.3537637109375, exactly ratio 16777216=(65536/16)^2. This is intentionally schematic, NOT measured secure-parameter CKKS noise, not 2^-128 DFR; actual key-switch error may depend on data, modulus and plaintext encoding, and this conditional counterexample is enough to reject claim that old DFR can be reused without analysis.
A prior quick toy with p1,Δ256, κ[-3,3], 100000 paired samples had 0 errors of |noise|>=3 in post-mask rotation and 14347 in pre-mask rotation; REAL code masks have p1/16 or smaller, so this is only a generic caution, not source-faithful performance result.
There is no demonstrated safe reduction in key switching error: to achieve same late rotation residual, pre-rotation raw KS error generally must be reduced by Δ|p| or the scheme's precision margin must absorb it. Enlarging auxiliary modulus/keys or shifting CKKS modulus levels could eliminate naive speed/memory gains. Pre-rotation also changes error correlation across outputs, and repeated LUT iterations can amplify the new noise.
The ciphertext modulus/level of these operations must be verified with native OpenFHE before precise numerical claims; no binary native benchmark performed.

## Scientific decision
[CORRECTNESS] PASS pure message equality for eligible input/output types. Full ciphertext approximate correctness UNPROVED because keyswitch/rescale order differs.
[NOISE/DFR] FAIL unchanged-noise assumption in a standard fixed-raw-KS-error scale model; source theorem doesn't cover moving KS before multiplied masks. Not a vulnerability of author's original scheme.
[SECURITY] Same original Galois keys and original encrypted LUTs (no new secret-dependent publication), but security and DFR for changed arithmetic are not automatically inherited.
[PERFORMANCE] Strong source-local rotation-count potential, but multiplication/ModReduce unchanged, native key/aux-modulus/latency trade-off UNKNOWN.
[NOVELTY] Rotation commutation, plaintext masks and hoisting known; no new cryptographic algorithm or paper-grade speedup established.
STATUS: PASS_IDEAL_SUBLOOP_HOIST / FAIL_FREE_NOISE_PRESERVATION / UNCLEAR_NATIVE_END_TO_END / NO_PUBLISHABLE_SCHEME.
NEXT_TEST B051: ONE targeted possible rescue only: investigate source-exact post-mask aggregated key-switching / level-conserving techniques (PKC26 LCR+AKS) or a certified CKKS precision margin that supports pre-mask hoist without larger keys/DFR impact. Cheapest mathematical/noise bound first, then native code if promising. If no method preserving late noise, archive B050 and audit new substantive BOOT construction, not endless rotation microchanges. SHIP remains PAUSED.
END OF ITERATION: STATUS above / RESULT local speed opportunity plus noise obstruction / NEXT_TEST above / STATE_UPDATE YES. Only BOOT files.
