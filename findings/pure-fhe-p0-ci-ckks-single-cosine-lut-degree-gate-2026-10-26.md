# PURE-FHE · P0-PRESCOUT-31 — Real CI-CKKS single-cosine universal-LUT degree gate

Date: 2026-10-26 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: INDEPENDENT_PURE_FHE_SOURCE_FIRST_SCOUT
PREVIOUS: P0-PRESCOUT-30, findings/pure-fhe-p0-gckks2600-step8-factor-parseval-headroom-gate-2026-10-26.md.
STATUS: FAIL_UNIVERSAL_CONSTANT_DEGREE_SINGLE_COSINE_LUT / PASS_STRICT_ALTERNATION_LOWER_BOUND / SOURCE_BLOCKED_FULL_PAPER
NOVELTY: NOT_ESTABLISHED (elementary algebraic lower bound, not a new scheme)
CODEX_REQUIRED: NO. No native, remote, GPU, or repo infrastructure changes.
OTHER_TRACKS: UNCHANGED; no shared STATE.md edit.

## Context / source-first novelty gate
The previous GCKKS 2026/2600 P0-23–30 subline is PARKED for lack of new mechanism and primary Focused 2026/2531 §6 PDF; do not re-open without relevant evidence. New independent FHE topic: real-only CI-CKKS functional bootstrapping. Broad 2026/1836/1840/1869 two-FBT arbitrary-precision A2B and GCKKS high-precision bootstrapping were already verified under P0-20; do not count as open problems.

[FACT] Public ePrint index current as of Oct 26, 2026: Liu, Ma, Wang, Wang, *Efficient (Functional) Bootstrapping for CKKS over the Conjugate-Invariant Ring*, ePrint 2026/2618, updated October 25, 2026; https://eprint.iacr.org/2026/2618. Its publicly indexed abstract states:
- native real FFT and bootstrapping directly in conjugate-invariant ring;
- real-valued AKP interpolation with radial correction and one-real-ciphertext single-cosine Hermite interpolation; complex-value interpolation emulated with two real ciphertexts;
- Lattigo implementation and paper-reported native single-ciphertext speedup 1.46–1.80x, FBT throughput 1.16–1.68x vs stated comparative CKKS configurations.
[FACT / LIMITATION] Attempted get_eprint_paper(2026/2618) through GitHub Notes on 2026-10-26: exact official PDF HTTP403, matching-title arXiv not found, fixed GitHub PDF mirror lacks paper; no first-party full text parsed. Do NOT claim to have examined authors' formal algorithm, input range, noise theorem, interpolation degree, DFR, or actual code. A 2023 Lattigo discussion and current release suggest older CI bootstrap converts to standard CKKS; these do NOT contradict the new 2026 authors' claimed **native** algorithm. 2026/2616 Descent-PBS is another recent source-first lead, but FULL PDF also retrieval-blocked and is NOT the current primary hypothesis.

## One smallest falsifiable claim H31
Claim: A construction that represents an arbitrary t-entry real lookup table solely as evaluation P(cos(theta(x))) of ONE fixed-degree real polynomial in a single real ciphertext input, with theta(x) mapping t distinct message values monotonically into [0,pi], achieves uniform output distinguishing error <1 for all t while keeping degree bounded independently of t. This is a NARROW hypothetical *direct polynomial* instantiation. It is NOT asserted to be Liu et al.'s full native CI FBT implementation.

## Cheapest decisive test: sign alternation on t ordered real nodes

[DERIVATION] For any t≥2 choose x_j=j, theta_j=pi j/t (j=0..t−1), and z_j=cos(theta_j). Cos is strictly decreasing on [0,pi], so z_0>z_1>...>z_{t-1}; any other t distinct ordered real inputs give the same argument. Choose a valid alternating LUT f(x_j)=(-1)^j. If a real polynomial P obeys |P(z_j)-(-1)^j|≤epsilon with epsilon<1, then P(z_j) is nonzero and has sign (-1)^j. By IVT, P has at least one real zero in each disjoint open interval (z_{j+1},z_j). These t−1 roots are distinct. A nonzero univariate polynomial of degree d has at most d real roots, hence
 deg(P)≥t−1.
This lower bound is strict and robust to any uniform real approximation error epsilon<1, under the stated single-polynomial/no-additional-input-interface restriction. It is not a lower bound on arbitrary encrypted LUT algorithms: multi-output vector slots, precomputed secret-dependent transforms, extra bootstrap, alternative nonpolynomial primitives, circuit-dependent ring representations or restricted LUT classes can escape.
[DERIVATION] A binary arithmetic circuit with depth D in ciphertext-ciphertext multiplications, starting from affine dependence on z and using additions/scalar multiplications, produces degree≤2^D. Thus D≥ceil(log2(t−1)). For t=16,256,65536 the lower bounds are respectively degree≥15,255,65535 and D≥4,8,16. This is an algebraic degree bound, not a concrete native CI-CKKS latency, modulus or DFR measurement. Slots/rotations permitted only if they do not introduce other independent variables or bootstrapping.

## Decision / value
H31 FAIL: direct low-degree one-cosine evaluation CANNOT be an arbitrary-table, precision-independent constant-depth real-only FBT. A special shape (smooth functions, sign/cosine via well-chosen restricted domains), multiple ciphertexts, or additional functional bootstrap might still be useful; author paper already claims a successful single-cosine Hermite technique in some tested scope, so do not assert paper contradicts theorem. The **broad target** of native CIR bootstrap itself is claimed implemented in ePrint 2026/2618: novelty of simply doing native CIR bootstrapping is likely already gone, pending full text verification.
This is a negative scope gate, not a novel FHE algorithm, no paper flaw, and no demonstrated improvement. Avoid inventing a new 'single-cosine all-LUT' project. Before a followup contribution claim: procure 2026/2618 first-party full PDF to inspect domain restrictions, actual interpolation targets, depth vs throughput/DFR/security, and overlap with any proposed construction. If still blocked, move to a different accessible primary-source FHE bottleneck rather than repeating toy polynomial scans; recent Descent-PBS 2026/2616 is source-blocked and should not be analyzed as a verified algorithm from the abstract alone.
PI alone decides track pivot / major experimental work. No Codex is needed for this simple mathematical rejection.

END_OF_ITERATION:
STATUS: FAIL_H31_UNIVERSAL_CONSTANT_DEGREE / PASS_ALTERNATION_LOWER_BOUND / FULL_SOURCE_BLOCKED
RESULT: all t-point alternating-sign real LUTs composed with injective cosine need polynomial degree≥t−1 (uniform error<1), multiplicative depth≥ceil(log2(t−1)) in the narrow arithmetic model.
NOVELTY: NOT_ESTABLISHED.
NEXT_TEST: original Liu et al. revised ePrint 2026/2618 PDF §real FFT/functional interpolation, cost/noise/DFR primary verification, or pick one DIFFERENT source-backed FHE bottleneck; do not infer publication novelty from the abstract.
STATE_UPDATE: YES isolated PURE-FHE finding only; no global STATE.md / other tracks.
CODEX_REQUIRED: NO. Future engineering PENDING explicit PI approval.
