# BOOT-B062 — Grouped NTRU-CMux equivalence and algorithmic novelty gate

Date: 2026-10-20
TRACK_ID: BOOT; SHIP PAUSED
STATUS: PASS_EXACT_GROUPED_CMUX_EQUIVALENCE / FAIL_NEW_PRIMITIVE_AND_ASYMPTOTIC_NOVELTY / UNCLEAR_SECURE_NATIVE_SYSTEM_DELTA

## Primary hypothesis
Replacing Dai et al. 2026 GIPEval with B059/B061 serial binary-selector NTRU supplies a cryptographically new primitive or new asymptotic grouped MKFHE bootstrapping architecture beyond published NTRU-CMux and Dai's hybrid grouping. Cheapest decisive test: exact group-and-final-correction functional identity plus source-based cost and key/material comparison.

## Sources
[FACT] Dai, Xiang, Deng, Zhang, "Accelerating MKFHE bootstrapping via parallel-friendly NTRU-based blind rotation," Cybersecurity 9:136 (2026), https://link.springer.com/article/10.1186/s42400-026-00563-w , Definition 5, Lemma 4, GIPKeyGen Eq.4, GIPEval Algorithm 2, Theorem 3 Eq.5 and Performance. Per group g=n/l: g-1 vector multiplications, g automorphisms (counted as equivalent vector-gadget products), with special final-group X^(-sum s_j) correction. Existing multi-key hybrid aggregator has kl external products each (3k+5) gadget-equivalents. Author ideal parallel model T_Dai(l)=2n/l+(3k+5)kl; l|n.
[FACT] Li et al., "Faster NTRU-based Bootstrapping in Less Than 4 ms," TCHES 2024(3):418-451, https://d-nb.info/1336785470/34 , section 3.2 / Algorithm 1: known binary NTRU-CMux using public X^a-1, encrypted selectors, and special NGS'(1/f) initialization; key unrolling and approximate decomposition already considered. Standalone scalar NTRU-CMux timing is NOT a vector NTRU / MK-RLWE comparable benchmark.

## Exact compilation
[DERIVATION] With s_j binary, 1+(X^{w_j}-1)s_j = X^{w_js_j} in R_Q=Z_Q[X]/(X^N+1). Hence repeated CMux steps C <- C+(X^{w_j}-1)(C external_product Enc(s_j)) yield precisely a grouped plaintext exponent sum(w_js_j), and the final group must multiply X^(-sum_all s_j) as in Dai Theorem 3, so aggregate phase equals (2N/q)*sum(a_js_j). No new plaintext functionality or new grouped aggregation primitive.
[DERIVATION] With exact gadget reconstruction h(C)*G=C, EXT(C,G+(X^w-1)S) = C+(X^w-1)EXT(C,S) exactly modulo Q, even for noisy S. This is the NTRU-CMux identity already corroborated in B061 1000/1000. Does NOT imply equality of distributions or noise bounds for different key encodings.
[INTERFACE] Dai's grouped MKFHE pipeline requires d-limb VECTOR NTRU outputs; Li's standalone CMux operates on scalar accumulator. Vectorizing a scalar CMux may require d scalar external products per vector external product. Never transfer Li's 3.8ms or a scalar cost into Dai's vector pipeline without a matched native implementation.

## Smallest executable evidence
[TEST] Independent script verify_b062_cmux_group_cost.py, SHA-256 5d4cadf4e0c4553901939cda8665b5013247a74e1f0e6e54639df9405d2cca96, exact R=Z_257[X]/(X^8+1), n=4,q=4, all 256 public coefficient tuples and all 16 binary secret tuples, l in {1,2,4}.
Dai group-target vs CMux compiled outputs 28672/28672 PASS, full corrected aggregate phase 12288/12288 PASS; separately 2000/2000 randomized exact base16 mod2^16 gadget-linearity identities PASS. Zero noise functional toy, NOT real NTRU encryption, DFR, native runtime, or security proof.

## Cost and key gate
[DERIVATION] beta=(3k+5)k. Dai source's ideal parallel model T_Dai(l)=2n/l+beta*l. Candidate model, **ignoring public sparse multiplications, extra key loads, noise and security**, T_CMux(l)=n/l+beta*l. Both have continuous optimized order O(k sqrt(n)); continuous ideal cost ratio sqrt(2), not any asymptotic exponent improvement. Divisor-constrained ratios vary.
[TEST] Exhaustively enumerating l|n in this simplified model:
n=256,k=2: 216 vs 152, ratio1.421; n=512,k=4: 528 vs392, ratio1.347; n=1024,k=8:1440 vs976, ratio1.475. These are symbolic gadget-equivalent costs, NOT speedups, and can exceed continuous sqrt(2) due to discrete divisors.
[KEY] Dai evk n+q vector NTRU ciphertexts (n+1 BRK + q-1 automorphism keys). Candidate conceptual n bits selectors + 1 encrypted sum correction + 1 normalized unity key = n+2, saving q-2 *vector entries* under corresponding key types. Requires l normalized first-bit selector encryptions, safe K_f reuse, proof of full joint KDM/circular-security, and noise/error correlations. Not new primitive: bit-encrypted NTRU selectors and unity initialization are Li prior art. Exact security-matched bytes, real DFR, and latency unmeasured.

## Research decision
The main B059-B061 binary reencoding is existing NTRU-CMux plus Dai's already published vector grouping and hybrid product. PASS ideal algebra and conditional constant-factor cost. FAIL as a stand-alone NEW cryptographic primitive or asymptotic algorithm; secure end-to-end engineering gain remains UNCLEAR. **ARCHIVE B059–B062 as a new-algorithm publication line**, not a theorem that any future systems optimization is impossible.

NEXT_TEST (B063 not started): a genuinely new interface reducing Dai's remaining (3k+5)kl hybrid aggregation term. One falsifiable candidate: shared decomposition across distinct grouped NTRU accumulators with no hidden same-input assumption, no exponential cross-group keys, and a clearly defined MK-RLWE output. Check existing BOOT B035/B036 and literature before any claim.
STATE_UPDATE NO: GitHub Notes read_repo_file on boot-STATE.md returned empty object; preserve existing 187967-byte STATE rather than overwrite. This is an append-only B062 findings record. 
Local full report, executable Python and JSON: BOOT_B062_handoff.zip.