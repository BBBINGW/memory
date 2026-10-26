# PURE-FHE P0-PRESCOUT-14 — PreTrace vs ModRaise Commutator Gate
- Date: 2026-10-26 (Asia/Hong_Kong)
- TRACK_ID: PURE-FHE
- PREVIOUS: P0-PRESCOUT-13
- STATUS: FAIL_UNRESTRICTED_PRETRACE; PASS_SUBRING_INVARIANCE_SUFFICIENT_CONDITION
- NOVELTY: NOT_ESTABLISHED
- CODEX: NOT_RUN

## Primary falsifiable claim and one minimal test

H14: If CKKS plaintext m lies in a proper subring A, project both RLWE ciphertext components into A before ModRaise to avoid post-ModRaise SubSum without special handling of the encryption key. The cheapest test is P(c0+c1*s) ?= P(c0)+P(c1)*s for arbitrary s.

## [DERIVATION] Counterexample

R=Z[X]/(X^8+1), A=Z[X²]/(X^8+1), q=5. P(f)=(f(X)+f(-X))/2 means exact even-coefficient selection on the integer monomial basis.
s=X, c0=1+X²+2X, c1=3, so c0+c1*s=1+X²+5X gives plaintext m=1+X² ∈A modulo q. But P(c0)=1+X², P(c1)=3, and P(c0)+P(c1)*s=1+X²+3X, which is NOT equivalent modulo q.
A synthetic counterexample to a universal algebraic identity, not an assertion about the distribution of sampled CKKS ciphertexts.

Let s=u+Xv, c1=a+Xb with u,v,a,b in A, Y=X². Then P(c1*s)=au+Ybv, while P(c1)P(s)=au: discarding the odd ciphertext part loses the Ybv cross-term. This rules out the straightforward componentwise projection for generic key but not a key-assisted module/RLWE construction.

## [DERIVATION] Sufficient condition and ModRaise

If s∈A then P(c1*s)=P(c1)*s, so componentwise projection preserves the projected decryption relation. Symbolic verification: s=1+X², c0=1+X²-3X-3X³, c1=2+3X; decryption is 3+3X² and projected components c0'=1+X²,c1'=2 decrypt to 3+3X².
If the ciphertext components *and* encryption key are inside A, coefficientwise modulus lifting to the larger modulus keeps those components in A and yields lifted decryption m+qI with I∈A when m∈A.
Merely having m∈A is not enough: q=5, s=1, c0=m+2X, c1=3X gives m mod5 but lifted decryption m+5X∉A.
Trace T=Id+tau, tau(X)=−X, is an integer ciphertext operation; P=T/2 is the normalized formal even-coefficient selector. Applying normalization homomorphically needs scale/modulus/noise accounting; not a free divide-by-two.

## [FACT] Source verification

User-supplied primary PDF papers/supplied/2025-1594.pdf (blob SHA 049872913a58b55d7833688e66756b01371745a3): Shihe Ma, Tairong Huang, Anyu Wang, Xiaoyun Wang, "Practical Dense-Key Bootstrapping with Subring Secret Encapsulation," ASIACRYPT 2025, https://eprint.iacr.org/2025/1594 . Reviewed physical PDF pp9–16:
* p9 §2.4: ModUp→SubSum→CtS→homomorphic rounding→StC, plus StC-first alternative.
* p10 §2.5: classical Ring Switching and dimension/modulus security constraints.
* p11 §3: switch to a dense subring key before bootstrapping, without completing all three stages of ring switching.
* pp13–15 §3.2: use invariant key under a subset of Galois automorphisms to hoist/reuse key switching.
* p16 sparse-packing discussion: when N'≤N* SubSum is key-switching-free because every automorphism fixing the sparse plaintext subring fixes the key subring; for N'>N* relative trace splits into stages.
This is strong prior art for the invariant-subring/trace/keyswitch mechanism; no direct evidence that EVERY proposed pre-ModRaise scheduling variant was empirically evaluated.
Additional sources: Gentry–Halevi–Peikert–Smart, "Field Switching in BGV-Style Homomorphic Encryption," 2013, https://web.eecs.umich.edu/~cpeikert/pubs/ring-switching.pdf (abstract-level reference; primary PDF open timed out); Min–Lee–Song, ePrint 2025/429 PDF p5 §2.4, https://eprint.iacr.org/2025/429.pdf (explicit conventional ModRaise→SubSum path).

## [SPECULATION] Systems cost boundary

Doing projection while the ciphertext has fewer RNS limbs *might* lower trace arithmetic, but does not imply end-to-end gain: key-switch to invariant subring key, normalization, changed security parameters, extra noise/precision loss, full eval keys and output representation must be included. In addition, existing subring encapsulation already allows key-switch-free SubSum, and projection might fuse with ModRaise at negligible cost. No benchmark, no noise theorem, no novel algorithm claim.

## Decision

Kill general pretrace-and-copy scheme; archive the special invariant-key case as existing algebra rather than publishable novelty. After repeated rejections of this optimization family, pivot away from representation-transform scheduling instead of spending another synthetic iteration on small variants.

NEXT_TEST: STRUCTURAL_PIVOT_EVALMOD_ERROR_CONTRACT_SOURCE_GATE — start from Ma et al. p13 explicit lack of a precise L1 EvalMod noise analysis; check newer rigorous estimates and propose exactly one falsifiable analytical assertion. This is a prescout, not already a viable contribution.
STATE_UPDATE: YES, isolated finding only. No global STATE.md or other track modified.
