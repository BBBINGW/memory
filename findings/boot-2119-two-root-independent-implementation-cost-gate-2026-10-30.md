# BOOT — ePrint 2026/2119 two-root independent-implementation cost/frontier gate

Date: 2026-10-30
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Session: 密码学 15.0 — Research Turn 7/25

Status:
PASS_CODE_LEVEL_TWO_ROOT_FACTORIZATION /
PASS_INDEPENDENT_EXECUTED_FOUR_ROOT_BASELINE /
FAIL_MATERIAL_TOTAL_PACKED_KEY_SIZE_GAIN /
PASS_PARTIAL_SETUP_WORK_REDUCTION /
FAIL_TWO_X_SETUP_SPEEDUP_AS_AN_OPERATION_COUNT_CLAIM /
ONLINE_BOOTSTRAP_AND_EVALUATION_READY_MEMORY_UNCHANGED /
NATIVE_TWO_ROOT_PATCH_NOT_EXECUTED

## Parent durable state

Turn 5: findings/boot-2119-two-root-selector-packing-gate-2026-10-30.md
commit 2ee6820a81726483b9fdef5f39b7d3c33dabc14b

Turn 6: findings/boot-2119-two-root-shared-leaf-noise-covariance-gate-2026-10-30.md
commit c939d538f038c690dd8697cea65df5d903caa52b

The parent candidate factors the supplied ePrint2026/2119 narrow selector key from four coefficient-packed roots to two private sign/candidate roots, deriving head/tail layouts by public masks. Static type, deterministic-noise and ideal-slot covariance gates passed. Online 8.2ms/4.6ms path is unchanged because reconstruction is setup-only.

## Primary hypothesis

The surviving 4->2 root factorization materially changes a practical key-size or setup frontier in an executable source-shaped implementation, rather than being only a small representation cleanup.

Cheapest decisive test:
1. inspect a public independent implementation of ePrint2026/2119 at the exact packed-key/reconstruction code level;
2. verify whether the current four roots really duplicate plaintext information;
3. use executed reconstruction receipts and exact object sizes to separate packed-root bytes, substitution-key bytes, extraction-tree key switches, leaf public-mask work, and final evaluation-ready selector storage.

No two-root implementation was executed in this turn.

## Independent implementation provenance

Public repository: virtualsecureplatform/TFHEpp
Inspected commit: 1dd9a1addef4cae01da9bb6bfff0d22b55bec683

This is NOT the ePrint authors' implementation and is not used as evidence of author-code behavior.

Its repository audit states objective: Implement refs/2026-2119.pdf using Double Decomposition in TFHEpp, CPU only. docs/narrow-dd-final-implementation-audit.json marks the paper's head/tail narrow selector layout, four packed indicator ciphertexts, public substitution keys, evaluator-only coefficient extraction, and full N16384 packed reconstruction as implemented/evaluated, with explicit limitations: no matched paper latency and no complete 128-bit/circular-security qualification.

## 1. Exact code-level duplicate roots

include/ckks/narrow_bootstrapping.hpp defines std::array<Packed,4> indicators.

In CKKSNarrowPackedKeyGen, channels 0..3 use wanted = +1 for even channels and -1 for odd channels. A coefficient bit is set iff source[j] == wanted.

Therefore channel 0 and channel 2 encrypt exactly the SAME +1-indicator polynomial; channel 1 and channel 3 encrypt exactly the SAME -1-indicator polynomial. Only fresh encryption randomness differs.

This is stronger than the Turn-5 algebraic observation: the independent executable implementation literally materializes two duplicate plaintext pairs.

## 2. Head/tail distinction is only public reconstruction

CKKSNarrowExtractSelectorTerms decompresses every packed.indicators[channel]. At each leaf, channel<2 applies the public HEAD slot mask; channel>=2 applies the public TAIL placement mask; channel parity selects real(+)/imaginary(-) packing.

Thus the exact code normal form is duplicate private root plaintext -> same coefficient extraction tree -> different PUBLIC mask/layout.

A two-root implementation can traverse only the + and - roots once, and at each leaf emit BOTH corresponding head and tail masked terms. The downstream key.head/key.tail data structure and online blind-rotation path need not change.

## 3. Existing baseline is actually executed, not dead code

docs/narrow-dd-packed-file-validation.json: N=512,h=31, packed reconstruction exits 0, all head/tail selectors match the in-memory baseline exactly, raw/prepared substitution paths pass.

docs/narrow-dd-final-implementation-audit.json marks four packed indicators and evaluator reconstruction as verified.

Full N=16384 retained reconstruction in docs/narrow-dd-ll14-packed-mask42-reconstruction-validation.json:
- all checks passed;
- completed terms = 65536 = 4N;
- all 14 substitution depths cached;
- extraction elapsed = 5185.53 s;
- total reconstruction = 5742.459063455 s;
- 31 head groups + 5 tail groups retained;
- no new private/evaluation keys generated.

docs/CKKS.md summarizes this as about 95.7 min one-time reconstruction and about 34.95 GB retained reconstructed selectors.

These measurements are for the independent CPU port, NOT the paper's RTX PRO 6000 implementation.

## 4. Exact operation-count consequence: tree work halves, leaf-mask work does NOT

Current four-root reconstruction:
- 4 binary coefficient-extraction trees, each with N-1 internal automorphisms/key switches;
- N leaves per root, each generating one public-masked selector term.

Therefore:
automorphism/key-switch count = 4(N-1)
public-mask plaintext-mul/rescale terms = 4N

Two-root reconstruction:
- 2 extraction trees;
- every leaf produces BOTH head and tail public-mask terms.

Therefore:
automorphism/key-switch count = 2(N-1)
public-mask plaintext-mul/rescale terms = 4N

So decompression-tree switches halve exactly, but a 2x reconstruction-time claim is FALSE as an operation-count implication. The irreducible leaf-mask work is unchanged.

## 5. Full packed-key bytes: indicator-root saving is tiny

For the LL14 packed-bounded profile, repository storage accounting gives:
packed archive payload = 2,756,182,017 bytes
packed key object = 2,756,182,128 bytes

The packed ciphertext level uses 448-bit storage words. One RLWE ciphertext with k=1 and N=16384 occupies:
2 * 16384 * (448/8) = 1,835,008 bytes.

Four roots = 7,340,032 bytes.
Two-root rewrite saves exactly two roots = 3,670,016 bytes = about 3.50 MiB.

Relative to the entire packed archive:
3,670,016 / 2,756,182,017 = 0.00133156 = 0.133156%.

Thus root payload itself drops 50%, but TOTAL PACKED ARCHIVE drops only about 0.133%. The reusable substitution/key-switch keys dominate.

Therefore the candidate does NOT materially move the transmitted/persistent total-key-size frontier in this implementation.

## 6. Evaluation-ready memory is unchanged

The final reconstructed selectors are identical in type/count. The independent implementation retains about 34.95 GB of selector files after reconstruction.

The two-root rewrite changes neither number of head/tail evaluation-ready selectors, matrix payload used online, selector caches, product tree, nor online refresh algorithm.

Therefore steady-state selector storage, evaluation-ready key memory, and online 8.2ms/4.6ms paper latency are unchanged by construction.

## 7. Setup-time ceiling from operation accounting

A full native two-root patch was NOT run.

The implementation's qualified full-ring public-mask kernel profile reports about 0.0320979512 s per mask call on its profiling host. At 4N=65536 leaf-mask calls this corresponds to about 2103.57 s of mask-kernel work under that cross-run diagnostic.

The qualified full reconstruction has extraction elapsed 5185.53 s.

Treating the difference (~3081.96 s) as an optimistic envelope for all tree/other extraction work and granting a perfect 50% reduction to ALL of that non-mask work gives an optimistic diagnostic:
new extraction >= ~3644.55 s
old/new extraction <= ~1.423x.

Keeping measured post-extraction reconstruction overhead (~556.93 s) fixed gives:
old total = 5742.46 s
optimistic new total ~4201.48 s
optimistic total speedup ~1.367x
optimistic saving ~1541 s (~25.7 min).

CRITICAL LIMIT: these timings come from separate profiling/validation runs and are NOT a controlled two-root benchmark. They are only a ceiling-style diagnostic explaining why 2x setup speedup should not be claimed.

The exact result is the operation split: tree KS halves; mask work unchanged.

## 8. Scientific interpretation

The two-root factorization is REAL and independently source-shaped: it is visible directly in executable code, current implementation encrypts duplicate plaintext roots, and public layout masks are the only reason for separate channel pairs.

But the frontier value is much smaller than initially hoped.

PASS:
- exact 4->2 private-root factorization;
- exact 50% reduction in extraction-tree automorphism/key-switch calls;
- no static correctness/noise/security blocker from Turns 5-6.

FAIL:
- material total packed-key size improvement;
- steady-state evaluation-ready memory improvement;
- online bootstrapping latency improvement;
- automatic 2x reconstruction-time improvement.

UNVERIFIED:
- actual native two-root reconstruction wall-clock;
- finite CKKS precision parity in the independent port after code rewrite;
- final novelty against all query/evaluation-key compression literature.

## Decision

AI_PROVISIONAL_CHOICE: PARK the 2119 two-root candidate as a standalone contribution after this turn.

Reason: it is a clean and correct representation cleanup, but in the executable source-shaped baseline total packed-key saving is only ~0.13%, evaluation-ready 34.95GB selector state is unchanged, online path is unchanged, and setup work only partially decreases because leaf masking remains 4N.

Do NOT spend the next turn implementing it solely to validate an engineering constant-factor setup saving.

Reopen only if:
1. reconstruction/setup latency itself is an important deployment bottleneck in a workload that frequently changes keys, OR
2. a new mechanism avoids materializing the full head/tail evaluation-ready selector set and thereby moves steady-state memory/key-transfer frontier, OR
3. the two-root factorization combines with a distinct compression method to eliminate a substantial fraction of substitution-key material.

TOP_LEVEL_BOOT_FRONTIER_EXHAUSTED: false.
PENDING_PI_DECISIONS: none.
PENDING_CODEX_TASKS: none.