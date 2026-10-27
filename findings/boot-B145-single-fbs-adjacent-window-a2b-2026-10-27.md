# BOOT-B145 — Single-FBS adjacent-window A2B for arithmetic polynomial encoding

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Renumbering note: this candidate was initially written as B144 in the same session, but B144 was already occupied by the pre-existing final-carry-reparameterization round. B145 is the canonical iteration number.
- Sources: supplied ePrint 2026/1869, 2026/2368, 2026/1163, 2026/1836
- Status: PASS_ALGEBRA / PASS_PRIOR_ART_PRESCOUT / PERF_GATED / PROMISING
- CODEX_REQUIRED: NO

## Core construction

For the power-of-two specialization of 2026/1869, with radix B=2^s, alpha_j=0 and the refreshed overflow is bounded by ||I'||_infty <= 16. Write the grouped values as

    x_j = d_j + U_j - B U_{j+1},    U_0=0.

Before functional bootstrapping, form the adjacent window

    y_j := B x_j + x_{j-1}.

Then exactly

    y_j = B d_j + d_{j-1} + U_{j-1} - B^2 U_{j+1},

hence

    y_j mod B^2 = B d_j + d_{j-1} + U_{j-1} mod B^2.

Thus the intermediate overflow U_j cancels before bootstrapping. Adding E=16 gives the same two-digit-window shape used by 2026/2368, but now directly from the arithmetic polynomial representation.

The operation is linear: one adjacent-position rotation/mask plus multiplication by public B.

## Partial top radix

If s does not divide n, reinterpret the reduced arithmetic polynomial as an integer z modulo B^u, u=ceil(n/s). Because F_n(2)=2^n,

    z ≡ m (mod 2^n).

The final B-radix digit may contain guard bits above bit n, but the lower n bits are exactly m. A terminal carry C_u absorbs the top wrap and is multiplied by B^2 in the adjacent-window equation, so it disappears modulo B^2. The same uniform window construction therefore applies to every radix position. Discard guard bits >=n after reconstruction.

## Exact B=4E boundary repair

The simplified recurrence in 2026/2368 assumes B>4E. Here the attractive choice is B=64 and the source-backed E=16, so B=4E.

Let w_j=B b_j+c_j and let delta_j in {0,1} satisfy b_j=a_j+delta_j mod B. Define

    L(c) = 1[c in [0,2E)),
    H(b) = 1[b in [B-2E,B)),
    P(b) = 1[b=0],
    T(b) = 1[b=B-2E].

At B=4E,

    H((b-delta) mod B)
      = H(b) + delta (P(b)-T(b)).

Therefore the exact same-window affine recurrence is

    delta_j = L(c_j) sigma_{j-1},

    sigma_j = H(b_j)
              + L(c_j)(P(b_j)-T(b_j)) sigma_{j-1}.

The affine slope may be -1 at the boundary state. This is compatible with the complex affine-pair composition of 2026/2368, which is algebraically defined for arbitrary real affine pairs.

Randomized exact-integer falsification over n in {32,64,128,256}, B=64, E=16 and partial-top-radix cases passed tens of thousands of cases per width.

## Candidate circuit

For B=64, u=ceil(n/6):

1. Use the 2026/1869 arithmetic-overflow refresh/front-end to obtain x_j.
2. Linearly form w_j = 64 x_j + x_{j-1} + 16.
3. Perform one B^2=4096 root/FBS.
4. On the same root, evaluate:
   - compact affine carry state (G_j,Htilde_j), where
       G_j=H(b_j),
       Htilde_j=L(c_j)(P(b_j)-T(b_j));
   - for each k=0,...,5:
       F_k(w_j)=bit_k(b_j),
       D_k(w_j)=L(c_j)(bit_k(b_j-1)-bit_k(b_j)).
5. Prefix-compose the affine states.
6. Output bit_k(z_j)=F_k(w_j)+G_{j-1:0} D_k(w_j).
7. Discard guard bits above n.

At n=256: u=43 and prefix depth is 6. In the cheap-output variant the post-LUT tail uses about 6 prefix CMults plus six parallel bit corrections = 12 CMults at depth 7.

## Comparison and prior-art boundary

- 2026/1869: two sequential FBS calls; B=32; 65 post-FBS CMults at n=256.
- 2026/2368: one-bootstrap two-digit windows for ordinary slot integer/real input; explicitly identifies 2026/1840 and 2026/1869 as two-sequential-FBS ALU conversions, but does not derive the arithmetic-polynomial adjacent-window cancellation above.
- 2026/1836: power-of-two A2B uses 3 CKKS bootstraps; prime-modulus A2B uses 5; does not subsume B145.
- 2026/1163 SWIFT: demonstrates that 12-bit/4096-point LUTs are practical, but spends extra slots to reduce latency.

## Decision

Algebra PASS. Direct known-prior collision among 1836/1840/1869/2368 NOT FOUND. This candidate attacks the dominant two-sequential-FBS bottleneck found in B143 and is therefore materially stronger than the compact-carry-only optimization.

Remaining gate is performance: the 4096-point multi-value LUT must beat the two smaller FBS stages under matched packing/security/precision. See B146.

No Codex/native experiment until B146 resolves the best LUT backend and predicts material gain.
