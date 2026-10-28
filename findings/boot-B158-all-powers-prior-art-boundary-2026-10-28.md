# BOOT-B158 — academic all-powers prior-art boundary

Date: 2026-10-28
TRACK_ID: BOOT
Status: PRIOR_ART_REFINED / DIRECT_COLLISION_NOT_FOUND

No native execution was performed.

## Purpose

B158 targets the ct-ct multiplication cost of generating the consecutive
power basis 1,x,...,x^(s-1) inside the sparse BFV EvalPower layout of
ePrint 2026/975.

A final academic prior-art pass checked older HE work that explicitly treats
"compute all powers" as the bottleneck.

## ePrint 2023/1407

Paper:
"Fully Homomorphic Encryption-Based Protocols for Enhanced Private Set
Intersection Functionalities"
Jingwei Hu, Junyan Chen, Wangchen Dai, Huaxiong Wang.

The paper explicitly states that in BFV OPE the bottleneck is the number of
ciphertext-ciphertext multiplications used to compute all powers of X.

Its low-depth/windowing strategy changes the input contract:
the receiver prepares and sends separate ciphertexts encrypting powers of two

Enc(r), Enc(r^2), ..., Enc(r^(2^j)).

The sender then builds the needed powers from those independently encrypted
source powers.

Its Paterson-Stockmeyer variant similarly computes / receives separate powers
Enc(X)^j and Enc(X)^(iL), and counts the multiplication graph needed to produce
those ciphertexts.

Therefore this work is strong prior art for:
- recognizing all-power generation as an HE bottleneck;
- reducing depth / multiplication count through source powers and
  Paterson-Stockmeyer structure.

It is NOT a direct B158 collision because:
- the power states are separate ciphertexts;
- the receiver supplies extra encrypted source powers;
- there is no sparse-BFV repeated-slot state
  [consecutive-power accumulator | current binary power];
- no single ciphertext multiplication is shown to simultaneously extend the
  consecutive basis and update x^(2^i).

Decision:
- PROBLEM_MOTIVATION_PRIOR: YES
- B158_STATE_REPRESENTATION_COLLISION: NO

## ePrint 2021/1116 / CCS 2021

Paper:
"Labeled PSI from Homomorphic Encryption with Reduced Computation and
Communication"
Kelong Cong et al.

This paper makes the source-power model even more explicit.

For example it compares powers-of-two source powers {1,2,4,8,16} with an
extremal postage-stamp basis {1,5,8}. The receiver sends ciphertexts encrypting
these source powers and the sender follows a multiplication graph to generate
all powers up to a target bound.

The paper formalizes the question:
which encrypted query powers should be sent so the sender can compute all
powers up to B under a target multiplicative depth?

It then combines extremal postage-stamp bases with Paterson-Stockmeyer and,
for suitable finite-field plaintext spaces, depth-free Frobenius maps.

This is highly relevant prior art for:
- multiplication graphs for all powers;
- source-power selection;
- depth vs communication tradeoffs.

It is not B158's setting:
- it changes receiver-to-sender communication by transmitting multiple
  encrypted powers;
- the remaining powers are materialized as separate ciphertext nodes in a
  multiplication graph;
- it does not exploit duplicated slots within a single BFV ciphertext to
  co-locate accumulator and binary-power state.

Decision:
- ALL_POWERS_MULTIPLICATION_GRAPH_PRIOR: YES
- POSTAGE_STAMP_SOURCE_POWER_PRIOR: YES
- DIRECT_B158_COLLISION: NO

## Consequence for novelty language

Do NOT claim:
- "we are the first to identify power generation as the bottleneck";
- "we are the first to reduce the number of multiplications needed for all
  encrypted powers";
- "we are the first to use spare SIMD slots / rotations in polynomial
  evaluation."

Those claims are too broad.

The narrow defensible B158 claim is:

"Given the single sparsely packed BFV input used by EvalPower, co-pack the
growing consecutive-power accumulator and the current binary power in the two
hypercube halves. This makes each ct-ct multiplication perform both accumulator
extension and binary-power update, yielding the minimum possible ct-ct
multiplication count log2(s) for power-of-two s>=4 without requiring additional
encrypted source powers."

This claim distinguishes B158 from:
- source-power/windowing schemes;
- postage-stamp multiplication graphs;
- Paterson-Stockmeyer power sets;
- the IBM rotate-and-multiply product-tree patent already recorded.

## Current novelty judgment

DIRECT_PRIOR_COLLISION: NOT_FOUND
CLOSE_ACADEMIC_PRIOR: YES
CLOSE_PATENT_PRIOR: YES
NOVELTY: PROMISING_NOT_ESTABLISHED

The remaining material novelty risk is a source using the same co-packed
state invariant under different terminology. Further generic "all powers"
search has diminishing expected value.

Recommendation:
stop broad prior-art micro-search and move B158 to native validation when PI
authorizes it.
