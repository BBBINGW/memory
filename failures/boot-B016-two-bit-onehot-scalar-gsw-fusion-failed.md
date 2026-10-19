# BOOT B016 — Failed shortcut: two encrypted MPmul bits into one scalar GSW external product

TRACK_ID: BOOT
ITERATION: B016
STATUS: FAIL_ONE_PRODUCT_FUSION / PARK_FOURWAY
DATE: 2026-10-19

2025/686 Algorithm 1 performs n CMUX external products per encrypted exponent bit, with a negacyclic shift and known X->X^-1 automorphism on wrapped positions. Grouping two bits b0,b1 requires one of four shifts I,P1,P2,P3. At n=8, output j=3 has four independent input choices c3,c2,c1,c0, and three nonbaseline difference forms (c2-c3,c1-c3,c0-c3) have rank3. Therefore a ONE-DEPTH affine combination of bit-independent linear preprocessed operands and SCALAR GSW encrypted selector functions needs >=3 external products per output. Two serial standard GSW CMUX stages use only two products. This rank argument does not apply to other ciphertext packing, matrix selectors, nonlinear preprocessing or multiple online depth.

Constructive three-key variant: GSW(b0(1-b1)), GSW((1-b0)b1), GSW(b0b1), with three corresponding differences. Saves a serial selection level but uses 3n vs2n online external products and 3 vs2 evaluation-key ciphertexts per pair (50% more work and key count at equal primitive parameters); automorphism inputs can be precomputed for last three coefficients and shared. 2048/2048 independent random exponent-vector/bit-pair plaintext reference tests passed, exact rank3.

The 2023/958 block-binary hypothesis constrains secret bit coordinates s_i, not 2025/686 binary digits of gap differences. Patterns (1,1) are allowed here and introduce nonzero b0b1 term. Removing them changes accepted sparse-secret distribution and needs a fresh rejection-sampling / IND-CPA security analysis. Existing TFHE-rs multibit PBS already encrypts group-pattern GGSW keys and trades larger key size for parallelization; do not claim novelty.

Full source derivation and limitations: findings/boot-B016-two-bit-selector-fusion-rank-gate.md.
NEXT: B017 source-compatible digit-decomposition hoisting across MPmul neighbor differences under ell_A=1 approximate gadget. Start with public digit borrow density and actual transform count; stop if dense corrections. BOOT files only.