# PURE-FHE — Post-P0-53 Descent/MMPM Multi-Bit Action Gate

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
LATEST_COMPLETED: P0-PRESCOUT-53
NEXT_ITERATION: P0-PRESCOUT-54 NOT_STARTED
STATUS: HUMAN_REVIEW / NO_P0_54
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO
STATE_UPDATE: YES — isolated HUMAN_REVIEW finding only; root STATE.md and other tracks unchanged.

## Scope

This is NOT P0-PRESCOUT-54. It is the one bounded source/interface probe authorized after P0-53. Goal: test whether recent module/monomial-matrix work leaves a credible mechanism for reducing the dominant n log B external-product term in Guimarães–Pereira MPmul without tensor key blow-up, Fourier-dense readout, or an already-known multi-bit time/key tradeoff.

No Codex, native FHE run, GPU/server work, or implementation was performed.

## Sources and provenance

1. Guimarães–Pereira, *Fast amortized bootstrapping with small keys and polynomial noise overhead*, ePrint 2025/686 / CCS 2025.
   - GitHub Notes cached original, VERSION_UNVERIFIED.
   - SHA256: 84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335.
   - Physical pp. 12–14 inspected: MPmul and binary sparse SAB.
2. Duan–Li–Liu–Ma, *Large-Plaintext Functional Bootstrapping in FHE with Small Bootstrapping Keys*, ePrint 2025/1717 / TCC 2025.
   - GitHub Notes acquired original from fixed ePrint mirror, VERSION_UNVERIFIED.
   - SHA256: 26b1e326351f6feffac72de8a3223bfe218a7e707fb79d585f8437c9a8e427f2.
   - Physical pp. 14–20 inspected.
3. Xiong–Wang–Wang–Wang, *Descent-PBS: Programmable Bootstrapping beyond the Ring Dimension*, ePrint 2026/2616, last updated 2026-10-23.
   - Primary PDF was read from an ePrint mirror in the web research tool because direct ePrint/GitHub Notes acquisition returned HTTP 403.
   - Key pages visually inspected: Proposition 1 / module-to-ring observation / shared-key descent / DescPar-S / Table 7 and conclusion.
   - GitHub Notes full-text acquisition remains SOURCE_BLOCKED, so do not claim a cached authoritative copy there.
4. Micciancio–Polyakov, *Bootstrapping in FHEW-like Cryptosystems*, ePrint 2020/086, plus current literature around generalized/multi-bit GINX.
   - Used only for the known radix/key-time tradeoff and accumulator-interface comparison.
5. *Carousel: Fully Homomorphic Encryption*, ePrint 2024/2032.
   - Primary PDF passage confirms generalized multi-value GINX: for secret value set {u_j}, direct selection uses RGSW encryptions of delta_{u_j}(s), can reuse one gadget decomposition, and needs |J|-1 selector keys.

## [FACT] Exact MPmul target

In 2025/686 Algorithm 2, for a binary sparse secret with gaps d = diff(s), the accumulator list c contains n RLWE ciphertexts. Each of h+1 secret gaps is applied via MPmul, and each MPmul decomposes d[i] into log B encrypted bits. Lemma 4.1 gives O(h n log B) external products.

The public subtraction of a(Y) between gap multiplications is almost free in the source interface: each RLWE list entry is multiplied by a public monomial X^{-a_k}; this does not create the dominant EP term.

Thus a genuine main-cost improvement must change the secret list-index action itself, not merely remove automorphism KS.

## [FACT] BootMMPM does NOT provide an encrypted multi-bit permutation matrix

2025/1717 represents the large phase group by public monic monomial permutation matrices Phi(c). Its bootstrapping keys are, for ternary LWE secret coordinate s_k, ordinary base-ring RGSW encryptions of the scalar bits s_k^+ and s_k^-.

Algorithm 1 applies:
  CMux(ct_k^+, ct_k^-; Phi(-a_k)(ACC), ACC, Phi(a_k)(ACC)).

Therefore Phi(±a_k) is PUBLIC. The source does not provide a compact ciphertext Enc(Phi(v)) for a hidden multi-bit v.

Its phase accumulation contains n CMux operations; each CMux performs two RLWE-vector × RGSW products, i.e. 2r ordinary RLWE × RGSW products. This is why the key size can be independent of the vector rank while the online action still pays linearly in rank.

This confirms that "secret multi-bit monomial action" is a real TYPE difference from BootMMPM, not already solved by simply citing its public matrix representation.

## [FACT] Descent-PBS blocks the earlier overly ambitious sub-rank target in a broad copy/select model

The 2026/2616 primary PDF gives Proposition 1, a "2N barrier for copy-only pipelines." For a pipeline that fixes k test polynomials, rotates accumulators, and between rotations only performs collision-free selections/copies/signs/extractions, if the target LUT has v_f distinct nonzero absolute values then k >= ceil(v_f/N). For maximally dense value sets, the first CMux rotation must use module rank tau_0 and therefore pays rank-linear EP cost.

Descent-PBS then pays the module rank only in the first rotation and descends to the ring via a merged public functional key switch when the module secret is embedded from the subring.

This is NOT a universal lower bound for all FHE arithmetic or for MPmul. In particular, the paper explicitly places linear combinations outside the copy-only statement, and a stronger rank/precision statement is only referred to as a full-version auxiliary result. But it is strong evidence against continuing to demand generic o(rank) universal LUT action inside the same copy/select interface.

Hence the strategic target should be weakened/refined from "sub-rank universal action" to "remove the avoidable log B overhead above a rank-linear action."

## [DERIVATION] The tempting O(n) multi-bit MPmul and three immediate realizations

Desired hypothetical operator:
  HiddenShift_d(c_0,...,c_{n-1})
should realize the exact P0-52 two-sheet semilinear cyclic shift for d in [0,B), with about O(n) base-ring EP-equivalent online work instead of O(n log B), compact evaluation-key material, and the same arbitrary-LUT output semantics.

This would be material: for B=128, the dominant MPmul EP count contains a factor log_2 B = 7. Removing this factor is qualitatively larger than P0-51's ~1.05–1.06x ideal KS-deletion ceiling.

However, the three natural implementations fail:

### A. One ordinary RGSW(X^d): WRONG TYPE

An ordinary base-ring RGSW encryption of X^d multiplies each RLWE plaintext by X^d. MPmul instead secretly permutes the LIST INDEX j (with tau-wrap semantics). These are distinct actions.

To make multiplication by a monomial act on the list index, the n-list must itself be embedded as coefficients/components of a larger Y-ring/module accumulator. That returns to P0-52's tensor/module representation issue.

### B. B-way one-hot / q-ary CMux: KNOWN TIME-KEY TRADEOFF

Write the secret action as
  Shift_d(c) = sum_{u=0}^{B-1} delta_u(d) Shift_u(c).

Generalized GINX / Carousel already uses exactly this pattern for arbitrary secret-value sets: RGSW(delta_u(secret)), reuse a gadget decomposition, and omit one key because selectors sum to one.

For d in [0,B), this needs about B-1 encrypted one-hot selector keys per gap, versus log B bit-RGSWs in 2025/686. It trades the log B online stages for an exponential-in-logB key expansion. This is known multi-bit/arbitrary-radix behavior, not a new compact construction.

### C. Encrypt the full permutation/monomial matrix: TENSOR/MATRIX BLOW-UP

Encrypting Phi(d) directly as a generic matrix-GSW or dense tensor-GSW makes the secret routing type-correct, but its key material grows with the representation rank/dimension. This is the same structural obstruction already quantified in P0-52.

BootMMPM avoids this key blow-up only because its matrices Phi(a_k) are public and the encrypted controller is a scalar bit; that trick does not transfer to a hidden Phi(d).

## [DERIVATION] Important correction to the post-P0-53 research target

The prior post-P0-53 shorthand:
  compact key + o(rank) online action + universal cheap readout
was too strong as an immediate target.

After the Descent-PBS source audit, a better target is:

  compact key + approximately rank-linear hidden action + universal cheap readout,
  while eliminating the extra log B bit-decomposition factor in MPmul.

This does NOT assert a lower bound Omega(n) for MPmul. Descent-PBS's proposition is for its copy-only LUT model, not our exact amortized sparse-polynomial multiplication. It is a strategic correction: stop spending rounds on generic sub-rank copy/select representations and focus on the specific n log B -> n gap.

## Why P0-54 still must NOT start

A P0-54-worthy positive mechanism would need a NEW way to represent a hidden cyclic/semilinear group element that simultaneously:

1. is more compact than B one-hot RGSWs;
2. does not require an n-dimensional encrypted matrix/tensor;
3. can act on the list/module state in about O(n), rather than O(n log B);
4. preserves the arbitrary negacyclic LUT output path;
5. has an explicit security/noise route for secret-derived gap material.

No such linking invariant/operator has been constructed in this probe.

The obvious candidates are already killed by wrong type, known radix key-time tradeoff, or P0-52 tensor blow-up. Therefore starting P0-54 now would only rename an open specification as a construction.

## Decision

STATUS: HUMAN_REVIEW / PASS_SOURCE_INTERFACE_REFINEMENT / FAIL_READY_H54
LATEST_COMPLETED: P0-PRESCOUT-53
NEXT_ITERATION: P0-PRESCOUT-54 NOT_STARTED
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO

RESULT:
- Descent-PBS provides a source-backed reason to stop demanding generic sub-rank universal LUT action in copy/select pipelines.
- BootMMPM confirms public monomial-matrix action + encrypted scalar selector, not a compact encrypted hidden permutation matrix.
- The meaningful remaining MPmul target is n log B -> approximately n while retaining compact keys and arbitrary LUT semantics.
- Direct q-ary selection is known and costs ~B selector keys; ordinary RGSW(X^d) is the wrong action type; full encrypted Phi(d) returns to tensor/matrix blow-up.

NEXT_TEST:
Do not implement. Only continue if one can formulate a concrete non-one-hot, non-tensor hidden cyclic-action encoding with an explicit evaluation algorithm and key-size bound. The first killer test must compare it against generalized/multi-bit GINX/AP and BootMMPM at the representation/type level before any noise or benchmark work.
