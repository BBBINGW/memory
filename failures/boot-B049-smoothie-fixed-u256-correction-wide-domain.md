# BOOT-B049 failure archive — fixed U256 public offset cannot encode generic 512-bit radix correction

TRACK_ID BOOT
ITERATION B049
DATE 2026-10-20
STATUS FAIL_GENERIC_WIDTH_REPRESENTABILITY / PASS_PUBLIC_LIMB_REPAIR / NO_NATIVE_DECRYPT_FAILURE_CLAIM

Author source KULeuven-COSIC/SMOOTHIE, smoothie.patch Git blob SHA 48aa5d2072c6f043e879bd0f698322d570ccf3c2, patch lines2090–2164 and2817+, multi-scalar bucket aggregation in tfhe-rs pinned by README at commit37934e42c11b634d8156ecd2faceab5ee33fceb3. README blob SHA150a6bf3fa44dae4130a85a874828736438f961b. SMOOTHIE CRYPTO2026 / ePrint2025/1267 author preprint full PDF retrieval failed INVALID_PDF (ePrint403 and invalid title mirror); paper itself NOT read, paper correctness or intended supported widths NOT claimed. Patch introduces benchmark U512 scalar type, but vector correction offset, sum, mod expression and neg-offset helpers all use U256. Number message bits hardcoded 2*num_blocks, test vector function arithmetic uses u128 and cannot cover arbitrary widths.

NECESSARY representability obstruction: for block count n>=128, w=2n>=256, mathematical 2^w does not fit in U256; code attempts U256::ONE <<w and modulus by it. For n256,w512, public correction C=3*2^300 has lower256 bits0; C=0 has same lower256 bits but different modular value in Z/2^512. Correct (0-C) mod2^512 nonzero, truncated U256 derived value zero. No fixed U256 representation can preserve both. This is a precise information loss, not a measured native panic/decryption failure. The paper may only benchmark narrower numbers and 2bit message modulus, so no claim publication false.

Correct fully-public arithmetic repair: (off+2^w-(C mod2^w)) mod2^w = (off-C) mod2^w; avoid constructing 2^w and do base4 n-limb borrow/subtraction. Pure public preprocessing O(n), zero additional PBS in algebraic model. Python fixed seed20261020, 2000 trials at w64,128,254,256,258,512 (12k) matched exact Python big-int modulo reference in 12000/12000; wide witness succeeds. No Rust, crypto, DFR, metadata, source correctness or latency native verification. Because basic modular subtraction is trivial and no bootstrapping algorithm change/acceleration shown, not a publishable FHE contribution.

Full evidence: findings/boot-B049-smoothie-public-offset-u256-radix-width-gate.md
NEXT B050: source-first *different* core bootstrap structural hypothesis. Stop repairing public integer bookkeeping without original algorithm novelty. Track BOOT only; SHIP PAUSED_BY_PI after I407. B050 not started.