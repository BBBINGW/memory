# BOOT / B158_OVERALL — Research Turn 1/25
Date: 2026-11-12 Asia/Singapore
Phase: PROBLEM_SELECTION
Candidate: boot-b158-same-ring-plaintext-crt-sharding-v1
Final: PARKED / FAIL_SEMANTIC / FAIL_SOURCE_FEASIBILITY
Research track: BOOT; active subline: B158_OVERALL
Native execution: none.

## Registered paper-level decision
QUESTION: Can the B175 pointwise scale-invariant plaintext modulus T=65537 be replaced by several strictly smaller CRT plaintext primes, while preserving the same N=32768 full batching, polynomial semantics, and Lattigo v6.2.0 interfaces, in order to lower the SI multiplication noise?
CURRENT_BELIEF: No. Full scalar slot batching requires each prime p congruent to 1 mod 2N.
CHEAPEST_DECISIVE_TEST: Check exact algebraic constraints and the pinned source parameter contract. No native trial.
IF_PASS: If a p<T exists with same N full scalar batching, admit ACTIVE for exact semantic-oracle construction and optimistic noise/value envelope.
IF_FAIL: If p>=T always, PARK because the proposed noise-lowering mechanism has no legal parameter instance.
IF_UNCLEAR: Leave UNKNOWN, inspect parameter constructor/encoder source; do not benchmark.
WHICH_PAPER_GATE_CHANGES: semantic correctness and source parameter feasibility (killer gates 1/2), then value ceiling.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: Existence of smaller valid p is a necessary condition for the candidate's claimed gain.

## Derivation / result
Let N=32768, T=65537, R_T=Z_T[X]/(X^N+1). Original T=65537 is prime, so Z_T cannot decompose by nontrivial integer CRT into smaller coprime plaintext-modulus factors with product T. For any full N scalar SIMD slots over F_p in this cyclotomic ring, X^N+1 must split into N distinct degree-one factors; hence F_p^* contains a primitive 2N-th root of unity, forcing 2N | p-1. Therefore p=1+k*65536 with positive integer k, and p>=65537. Equality is achieved at the existing T. There is no strictly smaller full-slot compatible prime.
Pinned Lattigo v6.2.0 BGV API documentation explicitly specifies the NTT-friendly plaintext prime requirement T == 1 mod 2n, where n is the plaintext ring degree.
This is a mathematical necessity for FULL scalar batching, not a general no-go for all lower-dimensional extension-field packing, reduced ring degree, or different message representation.
Parallel evaluation over newly selected p_i does not preserve arbitrary Z_65537 arithmetic for free. To restore original modular semantics one needs bounded-integer lifts and reduction modulo 65537, or a separate cross-ring conversion, with new semantic and cost obligations. It also does not obtain any smaller p_i at fixed N.
At most, it provides multiple branches with p_i >= T and extra encoding, ciphertext, keys, memory, and reconstruction costs; claimed lower-T SI tensor benefit is unavailable. No deterministic positive B175 precision/DFR recovery, particularly the conditional >=16 required-bit margin, follows.

## Prior art / exact delta
Baseline B175: Lattigo v6.2.0 BGV full scalar batching at N=32768 and T=65537, L18 fixed Q; final SI multiplication required bits 664 vs allowed <=648.
Proposed delta: replace one T channel with parallel lower-p full batching channels and CRT recombination.
Closest source interface: Lattigo v6.2.0 schemes/bgv parameters and Encoder, package documentation; see https://pkg.go.dev/github.com/baahl-nyu/lattigo/v6@v6.2.0/schemes/bgv . Classical CRT batching root-of-unity condition also stated in SEAL manual §7.4 https://www.microsoft.com/en-us/research/wp-content/uploads/2017/06/sealmanual_v2.2.pdf .
Novelty PREFLIGHT, not independently cleared. The mechanism fails necessary correctness/source feasibility before novelty or benchmark.

## Gates / decision
Killer gate 1: FAIL for literal CRT decomposition of original prime coefficient ring; altered bounded-integer reconstruction is a different, unspecified semantics and cannot be asserted equivalent.
Killer gate 2: FAIL for strictly smaller p with N scalar batching in pinned stock interface.
Killer gate 3: No claimed positive noise or full-system ceiling survives, since strictly smaller p_i do not exist; additional parallel branches increase baseline overhead (no numerical runtime bound asserted).
Status PARKED. NO_CREDIBLE_NEW_MECHANISM for this particular same-ring lower-T sharding route; no active candidate remains from this turn.
REOPEN only if concrete, source-compatible construction demonstrates correct original whole-output Z_65537 semantics using some different packing representation or modulus conversion, proves useful full B175 noise/DFR recovery and positive all-in system value. Do not relabel a smaller-ring or extension-slot design as this candidate.
ELIMINATED_UNCERTAINTY: Whether fixed-N full SIMD BGV supports any smaller plaintext prime than 65537. No.
DECISION_CHANGED: true (new candidate considered and killed prior to native or costly design).
EVIDENCE_REFS: Pinned B175 finding findings/boot-B175-static-noise-attribution-audit-2026-10-29.md; pinned B175 error finding findings/boot-B175-source-level-si-error-bounds-2026-10-29.md; Lattigo v6.2.0 BGV parameter docs URL above; elementary multiplicative group divisibility proof above.
