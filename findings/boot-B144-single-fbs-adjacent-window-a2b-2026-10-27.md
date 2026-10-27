# BOOT-B144 — Single-FBS adjacent-window A2B for arithmetic polynomial encoding

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Target: power-of-two A2B conversion in ePrint 2026/1869
- Main sources:
  - supplied ePrint 2026/1869, High-Precision Homomorphic ALU over Arbitrary Moduli with O(1) Bootstrapping
  - supplied ePrint 2026/2368, Low-Latency Parallel Digit Decomposition and Sign Evaluation for CKKS
  - supplied ePrint 2026/1163, SWIFT: Shallow and SIMD-Aware CKKS Functional Bootstrapping for Low-Latency
  - supplied ePrint 2026/1836, FHE for ALU over Large Prime Moduli and Application to One-Round Threshold ECDSA
- Status: PASS_ALGEBRA / PASS_PRIOR_ART_PRESCOUT / PERF_GATED / PROMISING
- CODEX_REQUIRED: NO, not yet

## Motivation

2026/1869 converts its arithmetic polynomial representation over Z_{2^n} to Boolean with exactly two sequential functional bootstraps.

For radix B=2^s, after refreshing the arithmetic overflow and grouping coefficients, its power-of-two specialization has alpha_j=0 and gives, at each full radix position,

    x_j = d_j + U_j - B U_{j+1},

where d_j is the target radix-B digit and U_j is a bounded boundary-overflow term. The source proves ||I'||_infty <= 16 after the relevant refresh under its stated correctness condition.

The first FBS reduces x_j modulo B. A linear combination with a neighboring quotient then cancels U_j, and the second FBS evaluates the local carry/bit functions. This post-first-FBS neighbor cancellation is exactly why 2026/2368 identifies 2026/1840 and 2026/1869 as two-sequential-FBS conversion methods.

2026/2368, for ordinary integer/real slot inputs, avoids the second bootstrap by constructing a two-digit window before root production and resolving the remaining one-bit carry by an affine prefix scan.

The question of B144 is whether an analogous two-digit window can be formed directly from the arithmetic polynomial data of 2026/1869 before the first FBS.

## 1. Exact adjacent-window cancellation

Set x_{-1}=0 and U_0=0. For full radix positions define

    y_j := B x_j + x_{j-1}.

Using

    x_j     = d_j     + U_j     - B U_{j+1},
    x_{j-1} = d_{j-1} + U_{j-1} - B U_j,

we obtain the exact identity

    y_j = B d_j + d_{j-1} + U_{j-1} - B^2 U_{j+1}.

Hence modulo B^2,

    y_j ≡ B d_j + d_{j-1} + U_{j-1}  (mod B^2).

The intermediate overflow U_j cancels before bootstrapping. This is the arithmetic-encoding analogue of the two-digit window used by 2026/2368.

Adding a public shift E gives

    w_j ≡ B d_j + d_{j-1} + E + U_{j-1}  (mod B^2).

For 2026/1869 we can conservatively take E=16 from its source-backed overflow bound.

The map x -> (B x_j + x_{j-1}) across packed radix positions is linear: multiplication by B plus a one-position rotation and masking. It adds no ciphertext-ciphertext multiplication level.

## 2. Uniform treatment of the partial top radix

When n is not divisible by s, the final group in 2026/1869 has radix 2^h rather than B. Naively this appears to break the uniform B^2 window.

Instead, reinterpret the reduced arithmetic polynomial as an integer z represented in u=ceil(n/s) radix-B digits modulo B^u.

Evaluation at X=2 gives

    z ≡ m (mod 2^n),

because reduction by F_n(X)=X^n-X+2 changes the evaluation only by multiples of F_n(2)=2^n.

Thus:
- the lower n bits of z are exactly the message m;
- the final B-radix position may contain guard bits above bit n;
- these guard bits absorb the terminal wrap caused by reduction modulo F_n.

Equivalently, there exists a terminal carry C_u such that every position, including the last, can be written uniformly as

    x_j = z_j + C_j - B C_{j+1},

with C_j=U_j for j<u. C_u need not be bounded because it appears as -B^2 C_{j+1} in the adjacent-window identity and vanishes modulo B^2.

Therefore the same B^2 windows recover all radix-B digits of z; the output simply discards guard bits above n. The retained lower n bits equal m exactly.

This removes the need to choose s dividing n or to raise B only to avoid a partial top radix.

## 3. Boundary issue at B=64, E=16

The 2026/2368 paper states its simplified recurrence under B>4E. With the conservative 2026/1869 bound E=16, the attractive radix B=64 lies exactly at B=4E.

The paper's simplified recurrence is not valid unchanged at this equality boundary. A direct algebraic test produces counterexamples.

However, the underlying local carry relation remains valid for integer displacement epsilon in [-E,E].

Write

    w_j = B b_j + c_j
        ≡ B a_j + a_{j-1} + E + epsilon_j  (mod B^2),

with a_j in [0,B), |epsilon_j|<=E, and define delta_j in {0,1} by

    b_j = a_j + delta_j  (mod B).

Let

    L(c) = 1[c in [0,2E)),
    H(b) = 1[b in [B-2E,B)),
    P(b) = 1[b=0],
    T(b) = 1[b=B-2E].

At B=4E, the exact indicator identity is

    H((b-delta) mod B)
      = H(b) + delta ( P(b) - T(b) ).

Therefore, with sigma_{-1}=0,

    delta_j = L(c_j) sigma_{j-1},

and the corrected same-window affine recurrence is

    sigma_j
      = H(b_j)
        + L(c_j)(P(b_j)-T(b_j)) sigma_{j-1}.

Define

    G_j := H(b_j),
    Htilde_j := L(c_j)(P(b_j)-T(b_j)).

Both G_j and Htilde_j are functions of the single B^2 window w_j. The local carry behavior is therefore still an affine map

    s -> G_j + Htilde_j s,

but its slope may be -1 at the boundary state.

This does not break the 2026/2368 prefix construction: that paper's complex-symbol encoding and composition equation are explicitly derived for arbitrary real affine pairs, not only the three Boolean generate/propagate/kill states.

Thus B=64 remains algebraically feasible while using a 4096-point root/LUT domain.

## 4. Candidate one-FBS algorithm

For B=64 (s=6), u=ceil(n/6):

1. Reuse the 2026/1869 front-end that refreshes the arithmetic overflow and linearly forms the radix values x_j.
2. Before functional bootstrapping, linearly form

       w_j = B x_j + x_{j-1} + E,

   with E=16 and appropriate interval masks.
3. Apply one root-production / multi-value functional bootstrap over period B^2=4096.
4. From each w_j, obtain by LUT:
   - the affine-state symbol encoding (G_j,Htilde_j);
   - for each of the s output bits, f_k(b_j);
   - the correction term
         d_k(w_j)=L(c_j)[f_k(b_j-1)-f_k(b_j)].
5. Run the affine prefix scan over the symbols in H=ceil(log2 u) rounds.
6. Recover each output bit as

       bit_k(z_j)
         = f_k(b_j) + G_{j-1:0} d_k(w_j),

   where G_{j-1:0} is the intercept of the prefix composite ending at j-1.
7. Discard guard bits above n.

This uses one sequential functional bootstrap instead of two.

## 5. Post-bootstrap cost

For n=256, B=64:
- u=ceil(256/6)=43;
- prefix depth H=ceil(log2 43)=6;
- one compact affine-state CMult per prefix round;
- six final bit-correction CMults in parallel.

Cheap variant:
- post-FBS CMult count: 6 + 6 = 12;
- post-FBS depth: 6 + 1 = 7.

A same-depth variant can fold digit-function states into the prefix as in Remark 1 of 2026/2368, trading extra operations for removal of the final dependent level.

For comparison, 2026/1869 at B=32 uses:
- two FBS calls;
- 12 output functions from FBS2;
- 65 post-FBS CMults at n=256;
- post-FBS prefix depth 6.

B144 therefore attacks the dominant sequential-FBS cost, not merely the small carry tail.

## 6. Algebraic falsification performed

Randomized exact-integer tests were run locally in the analysis environment for:
- n in {32,64,128,256};
- B=64;
- E=16;
- random radix digits and random bounded overflow coefficients;
- partial top-radix cases included.

The tests verified:
1. the adjacent-window cancellation identity;
2. the uniform radix-B reinterpretation and lower-n-bit correctness;
3. the corrected B=4E affine recurrence;
4. recovery of all retained message bits.

Tens of thousands of random cases per width passed. This is supporting falsification evidence, not a substitute for a proof or native CKKS implementation.

## 7. Prior-art audit

### 2026/2368

This is the closest source.

It explicitly states that 2026/1840 and 2026/1869 need two sequential FBS calls because neighboring digit positions are combined after the first bootstrap. Its own one-bootstrap method instead constructs a two-digit window before root production.

However:
- its input is an ordinary CKKS slot integer/real value;
- its FormWindows fanout derives all windows from that scalar input;
- it does not derive the arithmetic-polynomial adjacent-window identity above;
- it does not analyze the overflow polynomial of the 2026/1869 root-evaluation arithmetic representation.

So 2368 supplies the carry machinery and the one-bootstrap design principle, but it does not by itself establish B144.

### 2026/1836

This does not subsume B144.

For power-of-two A2B, 2026/1836 reports three CKKS bootstrap calls and O(log n) leveled depth. It uses A2A-I plus multi-value LUT/carry-lookahead canonicalization. For prime moduli it reports five bootstraps.

Thus it is not an arithmetic-encoded one-FBS A2B prior.

### 2026/1163 SWIFT

SWIFT establishes that 4096-point / 12-to-12 LUT evaluation is practically viable and can be made shallow by using SIMD slots:
- N=2^15 in the reported SWIFT experiments;
- 12-to-12 LUT measured latency 2.104s (t=1, batch 4), 2.973s (t=2, batch 128), 5.023s (t=3, batch 341);
- prior CKKS baseline 47.955s at much larger batch capacity.

But SWIFT spends additional slots per input to generate exponential powers. B144's attractive feature is different: it preserves a compact one-window-per-radix-position layout and therefore may retain substantially better arithmetic-message packing.

SWIFT is best viewed as evidence that the 4096-point LUT domain is not intrinsically infeasible, plus a possible optional low-latency backend for small batches.

## 8. Remaining risks

### Performance / parameter risk — main gate

B144 changes the LUT domain from the B=32 second-stage lookup of 2026/1869 to a B^2=4096 lookup/root.

A single larger FBS can still lose to two smaller FBS calls if:
- interpolation depth or coefficient norm forces a much larger modulus chain;
- multi-output LUT evaluation is expensive;
- the 4096-point root precision is insufficient under the arithmetic front-end noise;
- packing/layout forces additional ciphertexts or expensive rotations.

SWIFT strongly reduces this risk, but its measurements are not directly comparable to 2026/1869.

### Security / overflow probability

E=16 is conservative and source-backed for 2026/1869's refreshed arithmetic overflow. The equality-bound recurrence was designed specifically so that B=64 does not require weakening this bound.

No probabilistic tightening of E is needed for the algebraic candidate.

### Novelty risk

The construction is an explicit synthesis of:
- 2026/1869 arithmetic polynomial identities and overflow bound,
- 2026/2368 pre-bootstrap two-digit windows and affine carry scan.

The new part is the arithmetic adjacent-window cancellation, partial-top-radix treatment, and B=4E boundary-corrected recurrence.

Novelty is not yet established until broader prior-art search is completed, especially ePrint 2026/1200 and any later ALU conversion work.

## 9. Decision

- Algebra: PASS.
- Small-parameter falsification: PASS.
- Direct known-prior collision among 1836/1840/1869/2368: NOT FOUND.
- Whole-system value: potentially HIGH because it removes one sequential FBS, the dominant cost class identified in B143.
- Native/Codex: NOT YET.
- Status: PROMISING / PERF_GATED.

## 10. Cheapest decisive next test

Before native implementation, build a paper-level cost/parameter model for the exact 4096-point multi-value FBS needed by B144:

1. count the exact number and shape of LUT outputs required for six bits plus one complex affine state;
2. compare ordinary Hermite/PS, SWIFT-style power generation, and character-block/single-level LUT if 2026/1200 becomes available;
3. determine the minimal CKKS depth/modulus for B144 under the same security and target output precision as 2026/1869;
4. estimate slot capacity and amortized conversion time against 1869's n=32/64/128/256 table;
5. only if the model predicts material whole-system gain, request a native Codex/OpenFHE experiment.

No Codex task is justified before this gate.
