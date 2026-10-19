# BOOT B016 — Two-bit one-hot fusion in MPmul: algebraic rank and work gate

TRACK_ID: BOOT
ITERATION: B016
DATE: 2026-10-19
STATUS: PASS_FUNCTIONAL_EQUIVALENCE / FAIL_ONE_PRODUCT_FUSION / PRIOR_ART_MULTIBIT
STATE_UPDATE: YES

## Primary hypothesis
Can the 2023/958 block-binary selector aggregation principle compress TWO successive encrypted-bit stages of the 2025/686 MPmul into a single-stage update using strictly fewer than the source's 2n scalar GSW external products, with the original n independently encrypted exponent coefficients (no repacking or different ciphertext type)?

## Source-grounded setup
[FACT] Guimarães–Pereira 2025/686, version-unverified mirror PDF SHA256 84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335, physical pp.11–12, Algorithm 1: each exponent bit b_i selects between current n encrypted exponent coefficients and their negacyclic shift by 2^i; all n positions use one CMUX/external product, first 2^i positions also require automorphism X->X^-1 and key switch. Lemma 3.1 controls noise. Real FBS selector has ell_A=1, Table 3 p.23; do not invent multiple gadget levels.
[FACT] Lee et al. 2023/958, version-unverified mirror SHA256 0ab8c83d5aebbbf0185e200c7c3aab10150aa4e3bad0470a839246d33954e6de, physical pp.10–11 (block-binary selector: at most one nonzero s_i per block, so accumulator product can factor a sum of weighted BRKs), p.16 (FFT/pointwise costs). This constraint is on SPECIAL SECRET COORDINATES, not on binary digits of 2025/686's arbitrary gap values.
[PRIOR ART] TFHE-rs already has multi-bit PBS/GGSW keys for each grouped bit pattern; https://docs.rs/tfhe/latest/src/tfhe/core_crypto/algorithms/lwe_multi_bit_bootstrap_key_generation.rs.html says grouping_factor.ggsw_per_multi_bit_element() per group, and Zama's 2023 TFHE-rs v0.3.0 multithreaded bootstrapping explicitly trades bigger key for parallelized PBS. This is relevant to novelty, not a direct measured baseline against MPmul.

## Decisive algebraic falsifier
[DEFINITION] Let P_s be the negacyclic signed shift operator by s of the vector of n ciphertext plaintexts, with the wrap sign implemented by exponent inversion X^u -> X^-u. Thus P_1 P_2 = P_3 and each P_s is additive-linear on the underlying exponent plaintexts (not linear over ciphertext polynomial ring under arbitrary coefficients).
Two encrypted controls b0,b1∈{0,1} require
    F_b(c)=P_(b0+2b1)(c).
The four operations are I, P_1, P_2, P_3.

[DERIVATION] Set n=8 and inspect output index j=3, for which no wrap occurs at shifts 0,1,2,3. The four candidate ciphertext plaintexts are c3,c2,c1,c0. Relative to c3, the three difference operators are
    d1=c2-c3, d2=c1-c3, d3=c0-c3.
Their 3x4 coefficient matrix in formal independent basis (c3,c2,c1,c0) has rank exactly 3.
Consequently ANY one-depth expression
    F_b(c)=D0(c)+sum_(r=1)^m f_r(b0,b1) D_r(c)
with fixed bit-independent linear preprocessors D_r and scalar encrypted-selector products requires m>=3 to realize all four branches for arbitrary c. In particular, no one-depth ONE standard scalar GSW external-product per output implements a generic two-bit MPmul control without changed representation; even two are insufficient in this restricted model. This does not rule out two sequential GSW products (nonlinear in bits through intermediate ciphertext), matrix-GSW, repacking, or other schemes.

[CONSTRUCTION] Exactly three one-hot nondefault selectors suffice:
    g1=b0*(1-b1), g2=(1-b0)*b1, g3=b0*b1.
    F_b(c)=c+g1(P1 c-c)+g2(P2 c-c)+g3(P3 c-c).
Encode g1,g2,g3 as independent GSW key ciphertexts during key generation; since these are public evaluation keys encrypting functions of the secret gaps, their joint security/circular assumptions must be re-evaluated if this construction is implemented. Online: 3n external products, vs 2n in the original two successive stages. Selector key count increases from 2 to 3 per group. Same-depth independent products might run in parallel and remove one serial CMUX stage, but this is not an operation-count improvement. Precomputing automorphism for the last three ORIGINAL input positions once costs at most 3 automorphisms, equal to 1+2 source sequential per two stages; naive independent branches without reuse take 1+2+3=6. Noise/DFR may differ and are not derived.

[INDEPENDENT REFERENCE TEST] In n=8 with RLWE exponent ambient R_X=Z[X]/(X^16+1), encode each exponent u_j modulo 32, define P_s(u)_j=u_(j-s) if j>=s, else -u_(n+j-s) modulo 32. For a fixed-seed sample of 2048 randomly generated exponent vectors and bit pairs, verify:
    P_(2*b1)(P_(b0)(u)) = P_(b0+2*b1)(u)
and the 3-one-hot selector chooses precisely that result for every coefficient. 2048/2048 PASS. The 3x4 exact coefficient difference matrix has rank3. This is no-noise plaintext integer emulation, not actual GSW ciphertext code.

## Security and novelty constraint
[FACT] In 2023/958 the block-binary key has at most one nonzero secret coordinate in each selected block; in 2025/686 binary digit pairs of a gap d_i can be 11, so the cross term b0*b1 is not automatically zero. Restricting those gaps so each pair avoids 11 changes the secret distribution and the accepted-key probability. As a purely combinatorial illustration, for a uniform L-bit number with L=22 or23, requiring no 11 in each of 11 independent nonoverlapping pairs retains a fraction (3/4)^11≈0.042235 of values, removing 11 log2(4/3)≈4.565 bits of gap entropy. Real index differences are NOT independent uniform random variables, and this figure is NOT an estimate of 2025/686's actual rejection-sampling loss or security; those need measured distribution and lattice analysis.
[FACT] Multi-bit PBS prior art already uses pre-encrypted grouped selector patterns and exchanges additional key size/work for parallel depth. Merely adapting 2-bit one-hot selection is not established novel. Unique feature of 2023/958, aggregating many encrypted selectors against ONE COMMON ACC, does not transfer directly: MPmul's four choices at each output are different independently encrypted operands, so factoring a shared ACC out of a sum is not justified.

## Decision
RESULT: FAIL claim that two CMUX stages can be replaced by one ordinary GSW external product per MPmul output, while retaining independent ciphertext representation and no additional selector ciphertext type. PASS correctness of 3-product onehot alternative, but this uses 50% more keys/online external products and is strong prior art in multi-bit PBS; no latency benchmark, security analysis, or DFR proof.
DECISION: PARK naive grouped selector fusion; do not claim universal lower bound on all multi-bit automorphism/matrix-GSW schemes, and do not falsely claim parallel depth improvement means total-work reduction.
NEXT_TEST: BOOT B017 test a genuinely source-compatible computational hoist for 2025/686 MPmul at its ell_A=1 approximate gadget: can predecomposing each encrypted coefficient once permit cheap subtraction of gadget digits for every neighbor difference (c_(j-s)-c_j), avoiding repeated digit transforms without dense carry corrections? First exact borrow/carry identity under q=2^64,beta=2^23 and smallest random-coefficient sample; compare actual transform counts and prior art. Kill if correction is dense or no cost savings. BOOT isolation only.
