# BOOT / B158_OVERALL — Successor Research Turn 2/25
Date: 2026-11-12 (Asia/Singapore)
Phase: PROBLEM_SELECTION
Candidate: boot-b158-fullslot-trace-qcarry-annihilator-v1
Final status: PARKED
Verdict: PASS_CASE1_TRACE_LAYOUT_COMPATIBILITY / FAIL_STOCK_ODD_RNS_CARRY_ANNIHILATION / FAIL_CONSTRUCTIVE_SOURCE_GATE
No native or Codex task launched.

## Authority and distinctness
Current durable controller candidate UNKNOWN; BACKUPS none; no pending task. Preserve BOOT/B158_OVERALL. The predecessor scientific Turn 25 centered-QMul representation is PARKED, and successor Turn 1 stock standard-BGV terminal mode swap is PARKED. This candidate is not centered basis-extension, ordinary reciprocal-operator preconditioning, a public zero-gauge, sparse secret switching, late relin, selector reassociation or RGSW/CMux. It instead attempts to apply a nontrivial Galois-subgroup trace that annihilates modulus-raise alias terms in a larger coefficient modulus, transferred from the known HERDS decoding trace mechanism to the B175 final interface.

Primary durable anchors:
- findings/boot-B175-audit-direct-si-pointwise-noise-failure-2026-10-28.md, B175 artifact SHA256 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa
- findings/boot-B175-static-noise-attribution-audit-2026-10-29.md, blob e31ec2cbee6886ca61b6bc721920938d2a8a072b
- findings/boot-B175-source-level-si-error-bounds-2026-10-29.md, blob c75aa60e080b28b688de7ee8859c5df4d1951c02
- findings/herds-2025-1804-modraise-trace-residual-cancellation-gate.md, fixed older ePrint mirror cited in that finding, not independently PDF re-audited in this turn.
- Existing stock Lattigo ring v6.2.0 API https://pkg.go.dev/github.com/tuneinsight/lattigo/v6@v6.2.0/ring
- Existing stock Lattigo BGV v6.2.0 API https://pkg.go.dev/github.com/baahl-nyu/lattigo/v6@v6.2.0/schemes/bgv

Closest prior art: HERDS (Xiang et al., EUROCRYPT 2026, ePrint 2025/1804), Appendix B.6 and Algorithms 2/3 in the previously verified-in-2026-10-14 GitHub memory finding; the exact HERDS mechanism uses a power-of-two coefficient modulus q divisible by trace degree d and a trace T_d with T_d((q/d)zeta)=0 mod q. A distinct proof transferring it to B175's odd-prime NTT-RNS chain is not in the source, and this candidate fails that transfer.

## Pre-registered decisive gate
QUESTION: Can a public Galois-subgroup trace applied around an expanded-modulus B175 final stage cancel the entire arbitrary Q-multiple carry after componentwise lifting from odd Q while preserving the relevant CASE_1 j mod 8 whole-slot output and using the original stock N=32768 NTT-RNS implementation?
CURRENT_BELIEF: CASE_1's public j mod 8 output is invariant under the half-row rotation, so discarding the anti-invariant message component need not be fatal for that test family; however, an odd added Q-prime cannot divide a power-of-two trace degree, so exact annihilation of arbitrary Q-carry should be impossible.
CHEAPEST_DECISIVE_TEST: First prove CASE_1 output-layout preservation under T_2; then test the universally necessary constant-carry witness zeta=1 modulo Q*q_new for any NTT-friendly added prime q_new. Use exact integer arithmetic, no encryption run.
IF_PASS: If a nontrivial trace has zero Q-carry image modulo an admissible extended stock Q' while preserving all legal output slots, keep candidate ACTIVE for full carry/ref rounding, secret/Galois-keys, noise/DFR and value gates.
IF_FAIL: If even zeta=1 survives in every compatible odd-prime modulus extension, PARK because its central carry-annihilation invariant cannot hold in the stock source.
IF_UNCLEAR: Preserve UNKNOWN, verify exact group order/modulus-constructor contract; do not native execute.
WHICH_PAPER_GATE_CHANGES: first whole-output semantics (killer 1); then source feasible type/modulus/key edge (killer 2); hypothetical full-system value ceiling (killer 3).
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: The entire claimed benefit is exact generic alias cancellation; if the modulus makes even the constant carry survive, neither implementation nor benchmark can establish the paper mechanism without an entirely different modulus/backend.

## Case-1 message subspace oracle — restricted positive fact
The audited B175 CASE_1 pointwise expected value at physical slot j is one of 8 independently constructed public block sums according to j mod 8; GROUPED expected all ones for x=1. Standard BGV row rotations are induced by X -> X^{5^k mod 2N}. Let N=32768, 2N=65536, tau = sigma_{1+N}. Exact modular exponentiation gives 5^8192 mod 65536 = 32769 = 1+N. The corresponding Galois element rotates each physical row by 8192, which is 0 mod 8. Thus it preserves the CASE_1 j mod 8 expected-slot vector. In coefficient space tau(X^i)=(-1)^i X^i. For the plaintext encoding m of such an invariant vector, tau(m)=m and T_2(m):=(I+tau)m = 2m. Since plaintext modulus T=65537 is odd, factor 2 is invertible in R_T.
Therefore it would be INCORRECT to reject the candidate merely because T_2 has rank N/2 on all of R_T: the specific CASE_1 output reference lies in the invariant subspace. This does not prove the whole algorithm over all input settings retains the same invariant, or certify B175 candidate correctness after lifting.

## Exact Q-carry annihilation necessity and counterexample
Let the original B175 coefficient modulus be Q, a product of odd 2N-NTT-friendly RNS primes; bitlength(Q)=649. Suppose a new stock RNS level q_new, a distinct odd prime congruent to 1 modulo 65536, is added, giving Q'=Q*q_new. Componentwise lift of an R_Q ciphertext to R_Q' generically introduces an alias term Q*zeta(X) into its secret-decryption phase; exact zeta distribution/magnitude for B175 is NOT established, so this is a universal necessary-condition screen, not an attribution claim about the observed E_tref.

Let H be any finite subgroup of Gal(R/Q), |H|=d. Because Gal(Z[X]/(X^N+1)) ≅ (Z/2N)^× is a 2-group for N=32768, d=2^a. For its unweighted full orbit sum T_H = sum_{h∈H} sigma_h, every sigma_h fixes constant 1 and T_H(1)=d.

The claimed generic alias elimination requires for every zeta:
  T_H(Q*zeta) ≡ 0 (mod Q*q_new).

Set zeta=1, an admissible integer alias:
  T_H(Q*1) = d*Q.
This is zero modulo Q*q_new iff q_new | d. But q_new is odd and d is a power of two. Impossible for q_new>1.
In particular T_2(Q)=2Q !=0 mod Q*q_new for every legal q_new. This single counterexample decisively invalidates *universal exact trace annihilation of Q-carry* for every stock odd-prime modulus extension.

Contrast source HERDS special algebra: Q'=dQ with d=2^a and a trace of degree d WOULD kill Q*zeta modulo dQ after the integer coefficient projection T_d=d*Proj_d. But Q'=dQ includes an even prime factor 2 and is not representable as a chain of distinct NTT-friendly primes congruent to 1 mod 2N in the pinned Lattigo standard Ring/NewRing. Merely adding an odd NTT prime is not algebraically equivalent. A custom even-modulus backend plus changed key-switch and noise would be a NEW scheme/implementation, not the candidate's claimed stock transfer.

## Scientific / value limits
A trace of nonzero errors does not guarantee contraction. For any invariant error e, T_H(e)=d*e, so increasing ciphertext modulus from Q to dQ would leave normalized worst-case error unchanged on the invariant subspace; no generic 16-bit recovery follows. For non-invariant errors, some components may cancel, but B175's actual tensor/reference residual decomposition is unavailable. No actual noise reduction or useful DFR was shown.
Stock RNS extension additionally requires compatible prime(s), Galois key(s), full 32768-coefficient transforms and extra key-switch work; these costs cannot be omitted. No numerical benchmark/value claims.
This candidate fails the source-compatibility killer gate, even though the restricted CASE_1 plaintext invariance is not a semantic blocker. Do not perform a native canary.

## Decision, exact scope, and reopening
Final: FAIL_STOCK_ODD_RNS_CARRY_ANNIHILATION => PARKED. NO_CREDIBLE_NEW_MECHANISM for a free stock-RNS trace-annihilator. Novelty PREFLIGHT (not CLEAR); existing HERDS provides trace-cancellation prior art but in a different coefficient-modulus family.
This is NOT a strict impossibility theorem against every custom even-modulus trace scheme, key-assisted alias correction, tailored coefficient distribution, or more general carry treatment. It rules out the stated universal Q-alias annihilation with stock odd-prime RNS extensions.
REOPEN only with (1) a concrete source-compatible carry representation not requiring odd q_new | power-of-two d, or a secure and useful custom coefficient-modulus/keyswitch backend, (2) exact whole-output and reference-encoding carry invariants for full B175 domain, (3) deterministic or useful DFR >=16 required-bit recovery at fixed security, and (4) independent prior-art distinction and complete online/offline/key/memory cost.
ELIMINATED_UNCERTAINTY: Whether a power-of-two Galois trace can universally annihilate Q-multiple aliases after an ordinary odd-prime NTT-RNS modulus extension while retaining CASE_1 output. No; constant alias survives even though restricted output is trace-invariant.
DECISION_CHANGED=true: proposed new candidate rejected at source-semantic compatibility before native execution.
