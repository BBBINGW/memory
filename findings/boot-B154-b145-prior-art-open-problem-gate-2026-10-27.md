# BOOT-B154 — Prior-art/open-problem gate for B145 single-FBS arithmetic A2B

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Parent: B145/B152/B153
- Sources:
  - ePrint 2026/233, Gao–Zheng, "FHE for SIMD Arithmetic Logic Units with Amortized O(1) Bootstrapping per Ciphertext"
  - supplied 2026/1836
  - supplied 2026/1840
  - supplied 2026/1869
  - supplied 2026/2368
- Status: PASS_NO_DIRECT_COLLISION / OPEN_PROBLEM_ALIGNMENT / NOVELTY_PROMISING_NOT_ESTABLISHED
- CODEX_REQUIRED: NO for this gate

## Question

Does existing SIMD-ALU / arithmetic-to-Boolean prior art already contain the essential B145 result: one non-amortized sequential functional bootstrap from an arithmetic polynomial representation to Boolean digits/bits?

## 1. Gao–Zheng 2026/233

2026/233 starts from a CKKS-compatible triangle arithmetic representation and describes A2B as inherently iterative for one ciphertext.

Its batching technique B-A2B processes n/w ciphertexts together so that the n/w iterative bootstrap rounds are amortized across n/w ciphertexts. The paper's contribution statement is explicitly:
- A2B conversion uses an amortized constant number of CKKS bootstrappings per ciphertext;
- this is achieved by processing many ciphertexts across the iterative rounds.

Most importantly, its conclusion states:

"An interesting open problem is whether it is possible to convert from arithmetic to boolean mode using O(1) bootstrapping without amortization."

Therefore 2026/233 does not solve the B145 target and explicitly identifies the non-amortized constant-bootstrap version as open.

Version caveat: the cached PDF is from a fixed GitHub ePrint mirror and the exact ePrint version is not independently verified, but it is a full parsed copy of ePrint 2026/233.

## 2. Concurrent/later ALU conversion papers

### 2026/1836
Power-of-two A2B uses three CKKS bootstrap calls (and prime-modulus conversion more). No collision.

### 2026/1840
Uses two functional bootstrapping stages:
1. radix reduction / overflow preparation;
2. carry-state and candidate-bit LUTs;
then leveled carry and bit correction.

It improves over 233 by making the number of bootstrap calls independent of word length, but it remains two sequential FBS calls for one arithmetic ciphertext.

### 2026/1869
Also uses exactly two FBS calls for arithmetic-to-digit/Boolean conversion. Section 5.2 makes the sequential boundary explicit:
1. first FBS obtains each radix remainder r_j from x_j;
2. linear quotient/neighbour combination obtains a_j and cancels boundary overflow;
3. second FBS evaluates local carry/bit functions.

B145 moves the neighbour combination before FBS1 using the exact identity
B*x_j+x_{j-1}, so its architecture is not already present in 1869.

### 2026/2368
2368 achieves one bootstrapping for parallel digit decomposition by forming two-digit windows before root production, but its declared starting point is an ordinary CKKS ciphertext containing real/integer slot values.

Its related-work discussion explicitly distinguishes the ALU-conversion papers:
- 1840/1869 start from arithmetic-encoded ciphertexts;
- they take neighbouring linear combinations after a functional bootstrap and therefore need two sequential functional bootstrappings;
- 2368's window already contains the two neighbouring digits, so its ordinary-slot setting needs only one.

The paper does not derive a pre-bootstrap window directly from the arithmetic-polynomial boundary-overflow representation.

## 3. B145's remaining novelty delta

The potential new technical step is therefore narrow and identifiable:

1. Start from the 1869 power-of-two arithmetic polynomial representation.
2. Before any functional bootstrap, exploit
       x_j=d_j+U_j-BU_{j+1}
   to form
       B*x_j+x_{j-1},
   exactly cancelling the intermediate U_j modulo B^2.
3. Use a 2368-style B^2 window/carry-lookahead circuit in one functional bootstrap.
4. Handle the B=4E boundary exactly and the partial top radix/guard bits.

This is not merely "apply 2368 to 1869": the necessary pre-bootstrap cancellation identity and the equality-bound recurrence are not stated in the audited sources.

## 4. Novelty assessment

Evidence in favor:
- directly answers the open problem articulated in 2026/233 for the power-of-two arithmetic representation;
- improves 1840/1869 from two sequential FBS calls to one;
- 2368 identifies the two-FBS structure of those concurrent ALU works but does not give the arithmetic-encoded reduction;
- direct broad searches for one-bootstrap arithmetic-to-Boolean / adjacent-window arithmetic encoding found no matching construction.

Risks:
- the combination may be judged conceptually close/obvious after 2368 and 1869;
- later revisions after the audited versions could add the same bridge;
- full novelty still requires a conventional paper-search sweep and ideally author/code revision checking before submission.

## Decision

PASS_NO_DIRECT_COLLISION.

B145 now has a credible novelty story:
**non-amortized one-FBS A2B directly from the 1869-style arithmetic polynomial representation, by moving overflow cancellation before bootstrapping.**

Do not upgrade to NOVELTY_ESTABLISHED yet. Label:
**NOVELTY_PROMISING / DIRECT_COLLISION_NOT_FOUND.**

Given B153's correctness/value gates, the next scientifically decisive step is now a minimal native falsification experiment.
