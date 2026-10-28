# BOOT — Character Block Encoding refresh scout closure
Date: 2026-10-28
TRACK_ID: BOOT
CODEX_USED: NO
NATIVE_RUN: NO

## Source observations
Fresh source: Dumezy–Suvanto, ePrint 2026/1200 / ASIACRYPT 2026, plus public repositories jdumezy/ckks-block-encoding and jdumezy/poulpy-blck-ecd.

The public abstract separates functional CKKS bootstrapping into LUT evaluation, application modular reduction, cleaning, and ciphertext refresh. Block encodings make LUTs affine, make arithmetic modulo the finite alphabet native, and make cleaning constant-depth. Refresh remains a maintenance CKKS bootstrap.

The released precision-chain artifact calls Lattigo FullEvaluator.Bootstrap when levels are exhausted. Its shown parameter construction still contains C2S, S2C, and a conventional Mod1/EvalMod stage (degree 30, interval 16, double-angle 3, with eight 60-bit Mod1 primes in that experiment).

## Algebra gate
Block-encoding arithmetic modulo alphabet t is not the same operation as removing the unknown q*I polynomial created by CKKS modulus raising.

Therefore:
FREE_CKKS_EVALMOD_FROM_BLOCK_RESIDUE_REPRESENTATION = FAIL.

A linear representation change cannot in general erase the ModRaise ambiguity while preserving distinct codewords when the allowed wrap directions span the plaintext coefficient space.

## Prior-art gate
The narrower idea of using the finite plaintext alphabet to simplify CKKS bootstrap recovery has strong prior art:
- EUROCRYPT 2024 BinBoot specializes bootstrap recovery to binary messages and includes cleaning.
- ASIACRYPT 2024 SI-BTS gives dedicated small-integer functional bootstrapping and roots-of-unity output plus cleaning.
- CRYPTO 2025 nested-RNS work explicitly treats discrete bootstrap as correctness over a discrete set, allowing interpolation rather than generic continuous approximation.
- CRYPTO 2024 MaMBo provides generic fusion of plaintext-ciphertext matrix multiplication with bootstrap linear transforms.

## Cleaning implementation gate
Current poulpy-blck-ecd cleaning is already shared across packed block coordinates:
- Indicator/Thermometer use one SIMD binary cubic.
- Walsh-Hadamard uses one SIMD sign cubic.
- BRU/LBRU first use an affine transform into Indicator coordinates, then the same packed cubic, then an optional affine transform back.
The cubic uses two ciphertext multiplications (square and multiply by input) plus public linear operations.

Thus:
SHARED_NONLINEAR_CLEANING_ACROSS_BLOCK_COORDINATES = ALREADY_IMPLEMENTED.

## Decision
CHARACTER_BLOCK_NATIVE_REFRESH_BROAD = DEPRIORITIZE
FREE_EVALMOD = FAIL
FINITE_ALPHABET_SPECIALIZED_BOOTSTRAP = STRONG_PRIOR_ART
BLOCK_COORDINATE_SHARED_CLEANING = ALREADY_IMPLEMENTED
AFFINE_PRE_POST_BOOTSTRAP_FUSION = CLOSE_GENERIC_PRIOR_ART

No sufficiently narrow high-value fresh claim remains from this branch.

## Authoritative state unchanged
LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE: B163_PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
B158_NATIVE_FEASIBILITY: UNRESOLVED
B163: NOT_RUN
