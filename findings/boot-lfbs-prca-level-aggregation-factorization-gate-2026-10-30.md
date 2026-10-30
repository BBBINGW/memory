# BOOT — LFBS PRCA level-aggregation factorization gate

Date: 2026-10-30
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Session: 密码学 15.0 — Research Turn 3/25
Status: FAIL_ONE_AUTOMORPHISM_PER_LEVEL_AGGREGATION / PASS_B4_LINEAR_FACTOR_OBSTRUCTION / GENERAL_ARBITRARY_PACKING_LOWER_BOUND_UNPROVED

## Reprioritization

This turn is independent of:
- parked SPRU stride=2 custom cryptanalysis (Turn 1);
- source-gated FHEW AKU matched-DFR repair (Turn 2);
- completed B145–B157 4096-domain backend work;
- completed LFBS I188 call counting and I189 standard-hoisting screen.

The selected bottleneck is LFBS PRCA packing cost in Li et al., ePrint 2025/022. I189 only showed that conventional same-ciphertext hoisting cannot share decomposition across distinct PRCA operands. It did NOT rule out a stronger algebraic rewrite that aggregates all same-index automorphisms at one tree level into one automorphism call.

## Primary hypothesis

For PRCA Algorithm 5, because all nodes at level i use the same power automorphism psi_i, arbitrary public ring-linear pre/postprocessing can aggregate all B/2^i node operands and use only ONE call to psi_i per level, giving O(log B) tree automorphisms instead of B-1, without changing the input/output relation.

Cheapest decisive falsifier: solve the smallest nontrivial B=4 case. If even B=4 cannot be represented with one psi_1 call and one psi_2 call under arbitrary public R-linear operations, the one-per-level family is killed before implementation.

## Primary source

Zhihao Li et al., "Leveled Functional Bootstrapping via External Product Tree", IACR ePrint 2025/022, official PDF text accessible at https://eprint.iacr.org/2025/022.pdf, 35 physical pages.

Physical pp17–18 / Algorithm 5 gives, for i=1,...,log B,

c_j^(i)
 = (c_(2j)^(i-1) + X^(N/2^i) c_(2j+1)^(i-1))
 + HomoAuto_(psi_i)(
     c_(2j)^(i-1) - X^(N/2^i)c_(2j+1)^(i-1)
   ),

with psi_i: X -> X^(2^i+1), followed by a final HomTrace. The paper counts B-1+log(N/B) RLWE key switchings.

The PDF screenshot tool was attempted again on the relevant pages and returned HTTP 403; therefore exact source use here is based on the official PDF text layer, consistent with the already archived I189 extraction. No rendered-glyph parity claim.

## B=4 exact target operator

Work over R_Q = Z_Q[X]/(X^N+1), N a power of two, Q>2. Let

sigma_1: X -> X^3,
sigma_2: X -> X^5,
M_1 = X^(N/2),
M_2 = X^(N/4).

Algorithm 5 first computes

d_0 = c_0 + M_1 c_1 + sigma_1(c_0 - M_1 c_1),
d_1 = c_2 + M_1 c_3 + sigma_1(c_2 - M_1 c_3),

then

y = d_0 + M_2 d_1 + sigma_2(d_0 - M_2 d_1).

Because sigma_1 and sigma_2 are commuting power automorphisms, y is an R_Q-linear combination of

id(c_j), sigma_1(c_j), sigma_2(c_j), sigma_2 sigma_1(c_j).

The coefficients of sigma_1(c_j) are

T_1 =
[ 1,
 -sigma_1(M_1),
 M_2,
 -M_2 sigma_1(M_1) ].

Using sigma_1(M_1)=-M_1,

T_1 = [1, M_1, M_2, M_1 M_2].

The coefficients of sigma_2 sigma_1(c_j) are

T_21 =
[ 1,
 -sigma_2 sigma_1(M_1),
 -sigma_2(M_2),
 sigma_2(M_2) sigma_2 sigma_1(M_1) ].

Since

sigma_2(M_1)=M_1,
sigma_2(M_2)=-M_2,
sigma_2 sigma_1(M_1)=-M_1,

we again obtain

T_21 = [1, M_1, M_2, M_1 M_2].

However

sigma_2(T_1)
 = [1, M_1, -M_2, -M_1 M_2].

Therefore the componentwise ratios are

T_21,j / sigma_2(T_1,j)
 = [ +1, +1, -1, -1 ].

All entries are monomial units in R_Q, and +1 != -1 because Q>2.

## Normal form for ANY circuit with one sigma_1 call then one sigma_2 call

Allow arbitrary public ring multiplications, additions, fan-out, and input mixing for free.

With only one call to sigma_1, its input must be

v = sum_j p_j c_j,

so

u = sigma_1(v)
  = sum_j sigma_1(p_j) sigma_1(c_j).

Before the unique sigma_2 call, arbitrary linear processing can form

w = sum_j a_j c_j + b u.

After sigma_2 and arbitrary final public-linear processing, the output has the normal form

out =
sum_j C_j c_j
+ d u
+ f sigma_2(w).

Thus the sigma_1 and sigma_2 sigma_1 coefficients for input j necessarily satisfy

A_j = d sigma_1(p_j),
B_j = f sigma_2(b) sigma_2 sigma_1(p_j).

If the target A_j are units (they are: T_1,j are monomials), then d and sigma_1(p_j) are units. Hence

B_j / sigma_2(A_j)
 = f sigma_2(b) / sigma_2(d)

must be THE SAME ring element for every j.

PRCA violates this necessary rank-one/factorization condition because its ratios are

[+1,+1,-1,-1].

Therefore no such one-sigma_1 / one-sigma_2 public-linear circuit can implement B=4 PRCA exactly.

## Reverse ordering also fails

If the unique sigma_2 is evaluated before the unique sigma_1, the analogous necessary condition links the sigma_2 and sigma_1 sigma_2 coefficient families by one common factor after applying sigma_1.

For PRCA, already j=0 and j=1 give different ratios (+1 versus -1), so the reverse-order two-call circuit is also impossible.

If the two automorphisms are evaluated independently in parallel, no sigma_2 sigma_1 term can be generated at all, while the exact PRCA target has nonzero such terms. Thus that case also fails.

Hence every circuit in this model needs at least THREE automorphism invocations for B=4, exactly matching Algorithm 5's B-1=3 tree calls.

## Exact symbolic sanity checks

Independent symbolic monomial reduction in Z[X]/(X^N+1) for N in {8,16,32,64,128}, with psi_1=3 and psi_2=5, gives the forward factor ratios exactly

[1,1,-1,-1]

in every case.

This is an algebra sanity check, not an FHE benchmark.

## What this proves

PASS:
- B=4 PRCA cannot be collapsed from 3 tree automorphisms to 2 by the natural "one automorphism per level" strategy, even allowing arbitrary public ring-linear pre/postprocessing and fan-out.
- The obstruction is stronger than I189's same-ciphertext-hoisting observation: it is an exact factorization obstruction on the target linear operator.

FAIL:
- ONE_AUTOMORPHISM_PER_LEVEL_AGGREGATION.

## What this does NOT prove

This is NOT an unconditional Omega(B) lower bound for every possible RLWE packing algorithm.

It does not rule out:
- additional automorphism types not equal to the source psi_i;
- nonlinear/external-product operations;
- changed ciphertext/secret representation;
- multi-output evaluation-key primitives;
- larger temporary ciphertext spaces;
- alternative packing relations that avoid exact PRCA;
- special structured input-message families.

It also does not show an error in Li et al.; the source itself counts B-1 tree key switchings.

## Scientific disposition

The cheap LFBS PRCA "same level -> aggregate -> one automorphism" rescue is KILLED.

Together with I189:
- conventional hoisting across same-index distinct operands: killed;
- arbitrary public-linear one-call-per-level aggregation: killed already at B=4.

A further LFBS turn would need a genuinely different packing primitive or representation, not another scheduling/hoisting rewrite.

No native/Codex experiment is justified.

TOP_LEVEL_BOOT_FRONTIER_EXHAUSTED: false.
PENDING_CODEX_TASKS: none.
NEXT: reprioritize to a different BOOT bottleneck rather than extend this PRCA scheduling family.
