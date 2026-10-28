# BOOT — Post-B162 fresh scout: CRYPTO 2026 fast/shallow bootstrapping residual gates

Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER_LEVEL_ONLY
CODEX: NOT_USED
NATIVE: NOT_RUN

## Authoritative BOOT state (unchanged)

LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE_GATE: B163_CORRECTED_B160_NOSCALE_SELECTOR_GATE
B163_STATUS: PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
DO_NOT_AUTO_RUN_CODEX: YES

B145+B152: PARK / FAIL_NATIVE_VALUE
B158_ALGEBRA: PASS
B158_CTCT_MULT_COUNT: OPTIMAL
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B158_NATIVE_FEASIBILITY: UNRESOLVED
B162_B161_HYBRID: VALID_FAIL_AT_K1024
B163: NOT_RUN

## Primary target

Aayush Jain, Huijia Lin, Zeyu Liu, Sagnik Saha,
"New Techniques for Fast and Shallow FHE Bootstrapping and Beyond",
CRYPTO 2026, pp. 428–460, DOI 10.1007/978-3-032-35374-0_14,
IACR ePrint 2026/1730.

Springer CRYPTO 2026 proceedings and author publication pages confirm the venue/authors.
The exact current full text was NOT acquired through the research MCP in this round:
- official IACR PDF returned HTTP 403;
- exact-title arXiv fallback was unavailable;
- fixed arturo-kong IACR mirror did not yet contain 2026/1730.pdf.
Therefore all scheme-internal questions below remain SOURCE-GATED.

## Abstract-level facts that are safe to use

The paper reports two distinct contributions.

### Contribution A — sparse small-norm LWE secret

For an LWE secret of dimension n and Hamming weight h, the bootstrapping arithmetic complexity in Z_q multiplications is reduced from approximately O~(n^2) to O~(n h), while preserving the same asymptotic number of additions.

The abstract reports 4.5–7.5x practical speedup for gate and functional bootstrapping over the state-of-the-art OpenFHE implementation.

Important interpretation:
- the gain is specifically a multiplication-work reduction;
- the abstract does NOT claim the additions fall from n^2 to n h;
- hence low multiplication count alone does not imply proportional reduction in total word work or memory traffic.

### Contribution B — Binary NTT RLWE + relinearization-free BV multiplication

The paper introduces a structured-secret RLWE variant called Binary NTT RLWE and a relinearization-free BV multiplication technique.

At concrete parameters it reports:
- only 3 sequential NTT/INTT layers for bootstrapping,
- versus >500 for standard FHEW/TFHE,
- while the total number of unit 32/64-bit word operations remains comparable to standard FHEW/TFHE.

This is a major closure result:
  "remove most sequential transform depth" is no longer an open generic idea around standard FHEW/TFHE.
The residual research problem moves from transform depth toward total work, key traffic, and data movement.

## Axis-separation observation

Let an implementation cost be decomposed schematically as

  W_total = W_mul + W_add + W_key/memory + W_other,

and critical path depth as D_seq.

At abstract level:
- sparse-LWE contribution primarily decreases W_mul;
- Binary-NTT contribution primarily decreases D_seq;
- Binary-NTT explicitly keeps total unit-word operations comparable;
- sparse-LWE explicitly keeps the same asymptotic addition count.

Therefore neither contribution alone proves simultaneous reduction of both total work and sequential depth.

The tempting combination is:
  sparse-secret compiler/reduction + Binary-NTT shallow execution
to seek low W_mul and low D_seq simultaneously.

But this is NOT yet a construction. It requires exact representation compatibility and may still be addition/key-bandwidth dominated.

## Gate A — BINARY_NTT_SPARSE_COMPOSITION_GATE

Smallest falsifiable question:

Can the sparse-secret work reduction from Contribution A be instantiated inside the Binary-NTT RLWE shallow bootstrapping path of Contribution B without reintroducing sequential NTT/INTT layers, relinearization, or comparable replacement work?

Required source checks:
1. identify which secret is sparse in Contribution A (first-layer LWE input secret) and which secret is structured in Binary NTT RLWE;
2. identify the exact homomorphic-decryption / multiplication interface between them;
3. test whether the sparse batching/encoding operations remain valid in Binary-NTT representation;
4. count sequential layers after composition;
5. count additions and unit-word operations after composition;
6. check security assumptions jointly rather than independently.

Status:
  COMPOSITION_CORRECTNESS: UNKNOWN
  COMPOSITION_ALREADY_IN_PAPER: UNKNOWN
  ASYMPTOTIC_GAIN: UNKNOWN
  NOVELTY: NOT_ESTABLISHED
  NATIVE_REQUIRED_NOW: NO

Do not propose code before the paper source resolves items 1–3.

## Strong prior-art warning — sparse + shallow/NTT-free is already crowded

A current 2026 secondary research index reports a later work:
"Compiling Sparse Keys for Bootstrapping FHEs: Algorithms, Hardware Acceleration, and Beyond"
by Binwu Xiang, Songyu Wu, Baoyu Li, Xinwei Qiang, Benqiang Wei, Yu Yu.

The indexed abstract states that it is inspired by Jain et al. (CRYPTO 2026), uses Cuckoo hashing to transform an n-dimensional sparse binary LWE secret of weight h into one-hot buckets, reduces sequential external products from O(n) to O(h), and further explores an NTT-free variant eliminating all online NTT/iNTT operations.

This is only SECONDARY-SOURCE evidence in this round: no authenticated primary PDF/ePrint identifier was recovered.
Nevertheless it is a serious novelty warning:

  GENERIC_SPARSE_SECRET_PLUS_LOW_DEPTH: PRIOR_ART_CROWDED
  GENERIC_SPARSE_SECRET_PLUS_NTT_FREE: PRIOR_ART_CROWDED

Thus even if the 1730 composition is possible, "combine sparse keys with shallow/NTT-free bootstrapping" is not by itself a CCF-A/B contribution.
Any surviving novelty must exploit a Binary-NTT-specific property that the NTRU compiler does not have.

## Gate B — BINARY_NTT_KEY_TRAFFIC_GATE

The 1730 abstract gives transform depth and total word-operation statements but does not give enough information about:
- bootstrapping/evaluation-key size,
- number of independent key objects,
- online bytes read,
- key reuse/cache behavior,
- intermediate working-set size,
- whether the structured Binary-NTT secret forces replicated/pretransformed key material.

Since D_seq is already only 3, key/memory movement is a plausible remaining systems bottleneck, but this is only a hypothesis.

Minimum source-level test after full text acquisition:
1. recover exact evaluation-key objects and dimensions;
2. derive byte size as a function of N, gadget digits, modulus limbs, and structured-secret parameters;
3. derive an online key-read lower/upper bound per bootstrap;
4. compare with arithmetic intensity of the 3-layer path;
5. reject the line immediately if key traffic is already asymptotically/empirically small or fully reused.

Status:
  KEY_SIZE: UNKNOWN
  ONLINE_KEY_BYTES: UNKNOWN
  MEMORY_BOUND_CLAIM: NOT_ESTABLISHED
  CANDIDATE: SOURCE_GATE_ONLY

## Research decision

The generic idea "reduce sequential NTT layers further" is PARKED: depth 3 is already reported by CRYPTO 2026.

The generic idea "combine sparse secret with lower depth/NTT-free blind rotation" is DEPRIORITIZED because a later 2026 sparse-key compiler already claims exactly that broad pattern in the NTRU setting.

The only two worthwhile 1730 follow-ups are:
1. Binary-NTT-specific sparse composition, if full text reveals a nontrivial compatibility theorem or simultaneous work/depth gain not already present;
2. Binary-NTT-specific key-traffic/memory bottleneck, if exact key dimensions reveal a new structural target.

Neither is currently a research contribution.

## Gate decision

FAST_SHALLOW_DEPTH_ELIMINATION: CLOSED_BY_1730
GENERIC_SPARSE_PLUS_SHALLOW: PRIOR_ART_CROWDED
BINARY_NTT_SPARSE_COMPOSITION: PENDING_SOURCE
BINARY_NTT_KEY_TRAFFIC: PENDING_SOURCE
NOVELTY: NOT_ESTABLISHED
CCF_A_B_READINESS: NO
CODEX_REQUIRED_NOW: NO

## Next action

Acquire the exact 2026/1730 full text before spending more cycles on this subline.
Meanwhile, continue BOOT scouting for structural bottlenecks that remove an entire expensive stage/key family rather than another generic NTT micro-optimization.
