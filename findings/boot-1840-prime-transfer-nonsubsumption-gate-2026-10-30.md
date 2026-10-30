# BOOT — ePrint 2026/1840 arbitrary-prime transfer / non-subsumption gate

Date: 2026-10-30
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Session: 密码学 15.0 — Research Turn 13/25

Status:
FAIL_DIRECT_SUBSUMPTION_OF_1836_ARBITRARY_PRIME_A2B_BY_1840_TWO_FBT /
PASS_POWER_OF_TWO_MODULUS_SCOPE_BOUNDARY /
PASS_OUTER_DN_THEN_FINAL_MODM_COUNTEREXAMPLE /
ARBITRARY_M_RING_REMARK_DOES_NOT_CARRY_A2B_THEOREM /
1836_FUSED_PRIME_NOVELTY_NOT_KILLED_BY_1840 /
GENERALIZED_ARBITRARY_M_TRANSFER_REMAINS_OPEN

## Context

Turn 11-12 durable state:
- 2026/1836 fused arbitrary-prime A2B remains the strongest BOOT survivor;
- its native task BOOT-1836-FUSED-P64-SECP256K1P-NATIVE-20261030-R12-01 is execution-blocked in this Chat runtime, not scientifically failed;
- 2026/2368 was parked as a source-correct but explicitly probabilistic B=64 correctness trade-off.

Turn 13 checks the strongest apparent prior-art collision:
Xuan Shen, Zhihao Li, Ruida Wang, Xianhui Lu,
Efficient Homomorphic Arithmetic Logical Units with O(1) Bootstrapping,
supplied paper papers/supplied/2026-1840.pdf, Git blob fb5f5c20a61030b8a1ecfdb150cf4602d4dcc4ea.

## Primary hypothesis

2026/1840's two-functional-bootstrap A2B construction already covers the arbitrary-prime modular arithmetic setting of 2026/1836, so the 1836 prime-specific 5->4 fused-FBT candidate is substantially subsumed by prior/concurrent work.

Cheapest decisive falsifiers:
1. check the exact plaintext modulus and digit-base assumptions of the 1840 A2B theorem/Algorithm 4;
2. check whether Remark 1's arbitrary-M ring observation is accompanied by an A2B theorem preserving the shared-overflow/radix identities;
3. test whether Remark 2's 'compute in d^n, reduce mod M after TriDec' route is semantically equivalent to native modular arithmetic mod M under wraparound.

## Source facts

1840 Section 3 defines:
F(Y)=Y^n-Y+d, t=Y-d, and Z_t is isomorphic to Z/(d^n)Z.

Theorem 1 explicitly states the ring isomorphism with Z_{d^n}.

Section 4 begins:
'This section develops an A2B conversion for power-of-two digit bases, mapping the triangle encoding of a message m to its canonical bit encoding.'

Algorithm 4 input explicitly requires:
- d >= 2 a power of two;
- D=d^omega >= B;
- w=omega log2 d;
- candidate bits are bits_t(v_k mod D), relying on D=2^w.

The two functional bootstrappings are:
1. FBT modulo D to compute remainders r_k=s_k mod D;
2. MV-FBT over period 2D to jointly compute carry behavior and candidate bits.

The shared-overflow identity is derived from the special triangle coefficient structure induced by F(Y)=Y^n-Y+d.

## 1. 1840 itself limits the implemented A2B to power-of-two moduli

Section 1.3 Concurrent work explicitly says Wei et al. concurrently obtain two-functional-bootstrap A2B 'for power-of-two moduli'.

Section 4 / Algorithm 4 does not state arbitrary M. It takes the d^n triangle encoding and a power-of-two digit base.

Thus the published two-FBT A2B theorem is a Z_{d^n} / power-of-two-radix result, not an arbitrary-prime canonicalization theorem.

## 2. Remark 1 arbitrary-M algebra does not imply the Section-4 A2B theorem

Remark 1 says that for any M >=2 one may choose a monic G with G(d)=M, set t=Y-d, and obtain an algebraic quotient isomorphic to Z_M.

But Section 4 does not rederive:
- the special-d0 coefficient relation;
- the scaled adjacent-difference digit identities;
- the shared-overflow cancellation formula;
- binary-carry window bounds;
- the candidate-bit extraction formula;
for a general G.

The Section-4 warm-up uses the source-specific normalized coefficient identities:
d0 = -d f0,
di = f_{i-1} - d f_i,
after special-d0 preprocessing and ignoring overflow.

Those are derived from F(Y)=Y^n-Y+d and its d^n plaintext modulus. A generic G(d)=M does not inherit them automatically.

Therefore:
ARBITRARY_M_RING_EXISTENCE != ARBITRARY_M_TWO_FBT_A2B.

## 3. Remark 2's outer-d^n workaround is not a native modular-M ALU

Remark 2 proposes handling an arbitrary M by choosing n sufficiently large that all intermediate and final integer results lie in [0,d^n), computing in the d^n ring, applying TriDec, and reducing the recovered integer modulo M afterward.

This is valid for bounded integer computations with enough headroom.

It is NOT semantically equivalent to arbitrary modular arithmetic mod M when an operation should wrap at M before the final output.

Concrete secp256k1 counterexample:

Let
M=p=2^256-delta,
delta=2^32+977,
d=2, n=256.

Choose:
a=p-1,
b=2.

Desired native prime-field product:
a*b mod p = p-2 = 2^256-delta-2.

Arithmetic in Z_{2^256} gives:
a*b mod 2^256 = 2^256-2delta-2.

Since 2^256-2delta-2 < p, applying a final mod-p reduction changes nothing:
(a*b mod 2^256) mod p = 2^256-2delta-2.

This differs from the desired result by exactly:
-delta = -(2^32+977).

Thus:

(a*b mod 2^256) mod p != a*b mod p.

The failure occurs because the true integer product 2p-2 exceeds 2^256, violating Remark 2's explicit no-overflow-in-d^n precondition.

Choosing a larger n can postpone this problem for a bounded-depth integer computation, but it is not a drop-in leveled prime-field ALU with modular reduction after every field operation.

## 4. Why this preserves the 1836 prime-specific gap

2026/1836 targets large-prime modular arithmetic directly, including secp256k1-style prime moduli, and its arbitrary-prime A2B path has extra prime-wrap canonicalization machinery beyond the power-of-two path.

Turn 9-11 identified a candidate reduction of that prime-specific path from 5 CKKS bootstrappings to 4 by fusing the delta-LUT and boundary-symbol LUT.

1840's two-FBT result does not directly remove that prime-wrap machinery because its correctness proof assumes the d^n radix ring.

Therefore 1840 does NOT, by itself, kill the novelty of the 1836 arbitrary-prime 5->4 fusion.

## 5. Important open transfer direction

Although direct subsumption fails, Remark 1 leaves a potentially nontrivial research direction:
construct a special arbitrary-M polynomial G with G(d)=M whose coefficient representation retains a local radix recurrence strong enough for 1840-style shared-overflow cancellation.

That would require a NEW derivation of:
- coefficient preprocessing;
- overflow refresh compatibility;
- local carry/window identities;
- bit extraction under the new modulus.

This is not established here and should not be counted as a completed contribution.

## Verdict

Primary hypothesis FAILS:
1840's published two-FBT A2B does not directly subsume the arbitrary-prime canonicalization setting of 1836.

PASS_POWER_OF_TWO_MODULUS_SCOPE_BOUNDARY.
PASS_OUTER_DN_THEN_FINAL_MODM_COUNTEREXAMPLE.
ARBITRARY_M_RING_REMARK_DOES_NOT_CARRY_A2B_THEOREM.

1836_FUSED_PRIME_NOVELTY_NOT_KILLED_BY_1840.

## Decision

KEEP the 1836 fused arbitrary-prime A2B candidate pending native execution.

PARK 1840 direct-transfer as a novelty blocker: it is relevant adjacent/concurrent prior art, but not a direct arbitrary-prime solution.

Potential future hypothesis, only after the 1836 native gate or if that gate remains blocked:
derive whether a structured G_M with G_M(d)=M can preserve a rank-local digit recurrence and reduce arbitrary-prime A2B below four bootstraps.

TOP_LEVEL_BOOT_FRONTIER_EXHAUSTED: false.
PENDING_PI_DECISIONS: none.
PENDING_CODEX_TASKS:
- BOOT-1836-FUSED-P64-SECP256K1P-NATIVE-20261030-R12-01 remains pending/execution-blocked.