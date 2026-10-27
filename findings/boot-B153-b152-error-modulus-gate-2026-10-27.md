# BOOT-B153 — Error and modulus plausibility gate for the B152 eight-LUT backend

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Parent: B145/B152
- Status: PASS_ERROR_MARGIN / PASS_DEPTH_NEUTRALITY / NATIVE_GATE_REACHED
- CODEX_REQUIRED: YES FOR NEXT DECISIVE TEST, BUT NOT LAUNCHED WITHOUT PI AUTHORIZATION

## Question

B152 replaces four direct 4096-point Hermite LUT outputs by thirteen ordinary ciphertext multiplications that synthesize D0,...,D4. Does this destroy the exact-bit correctness margin or require extra critical-path depth/modulus?

## 1. Carry path is unchanged

The carry scan still consumes the direct Hermite outputs F5 and D5.

Therefore:
- the six-round affine carry prefix has the same input type as the direct B151/2368-style construction;
- B152's newly synthesized D0,...,D4 do not feed back into the carry recurrence;
- any extra approximation they introduce affects only the final lower-bit corrections.

This isolates the new error to a shallow side branch.

## 2. Conservative algebraic error bound

Let every directly looked-up real value Fk and L have absolute error at most epsilon before the side-branch products.

Exact factors have magnitudes:
- L in {0,1};
- 1-F_r in {0,1};
- 1-2F_k in {-1,+1}.

The worst synthesized correction is D4, whose exact product has:
- L;
- four lower-zero factors (1-F0),...,(1-F3);
- one sign factor (1-2F4).

Ignoring homomorphic multiplication rounding for the moment, perturbing the five unit/Boolean factors by at most epsilon and the sign factor by at most 2 epsilon gives

    |D4_tilde-D4|
      <= (1+epsilon)^5 (1+2epsilon) - 1.

Representative values:
- epsilon=2^-5      -> bound 0.2393;
- epsilon=2^-5.5    -> bound 0.1648;
- epsilon=2^-6      -> bound 0.1144;
- epsilon=2^-6.25   -> bound 0.0955;
- epsilon=2^-7      -> bound 0.0559;
- epsilon=2^-8      -> bound 0.0277.

The other Dk have fewer factors and smaller bounds.

## 3. Final bit margin

The exact lower-bit output is

    bit = F_k + C * D_k,

where C is the incoming carry in {0,1}.

If the lookup bit, incoming carry and synthesized correction have errors epsilon_F, epsilon_C, epsilon_D, then

    |error_out|
      <= epsilon_F + epsilon_D + epsilon_C + epsilon_C*epsilon_D

in the worst |C|,|D|<=1 case.

Taking the conservative common value epsilon_F=epsilon_C=epsilon=2^-6.25 and the D4 bound 0.0955 gives approximately

    error_out <= 0.122.

This leaves about 0.378 absolute margin before the 1/2 threshold needed to round an approximate bit to the exact Boolean value.

Even epsilon around 2^-4.5 gives an algebraic bound around 0.455 before adding homomorphic-evaluation noise, showing substantial structural slack.

2368's measured complete digit outputs are in the ~6.25-7.74 bit range without output cleaning, and 1840/1869 report exact A2B outputs with roughly 8-12 measured error bits in their implementations. These are empirical compatibility checks, not a proof that B145 inherits the same epsilon.

## 4. Added HE arithmetic error

The thirteen extra CMults occur over four side-branch levels. At the source-style scales (roughly high-30s/40s bits), the raw rescale rounding unit is far below the 0.1-scale algebraic margin.

Key switching/relinearization error and the exact scale schedule still need concrete verification, but there is no indication that ordinary CKKS evaluation noise alone should consume the remaining ~0.38 correctness margin.

This is precisely the part best tested by a minimal native prototype rather than a more elaborate symbolic bound.

## 5. Critical depth and modulus

B152 does not increase the critical post-LUT multiplicative depth relative to B151:

- D0..D4 synthesis: depth 4;
- carry prefix: depth 6;
- these run in parallel;
- final bit correction: +1.

Thus critical post-LUT depth remains 7.

Consequently B152's main modulus-chain requirement is the same as the direct twelve-LUT B145 architecture, despite doing more total multiplications.

The one-root B^2 construction of 2368 is already implemented at N=2^16 and B=64. B145 uses u=43 rather than the paper's u<=10 benchmark, adding two prefix levels (6 instead of 4); this is a modest depth increase but must be included in the matched native parameter selection.

Unlike B148 phase splitting, B152 does not add a new six-level serial chain and therefore does not create the same obvious HEStd_128 modulus-headroom obstruction.

## 6. Decision

- Algebraic error margin: PASS.
- Carry correctness path: unchanged.
- Critical depth: unchanged from B151.
- Security assumption: unchanged; no secret-distribution change.
- Exact output precision / scale schedule: requires implementation verification.
- Native gate: REACHED.

The next cheapest decisive test is no longer another paper derivation. It is a minimal native comparison of:
A. source-faithful 1869 two-FBS A2B;
B. B145/B152 one-Root4096 eight-LUT construction;
under the same OpenFHE/HEaaN2 backend, N/security/word size and packing.

Do not run Codex automatically; PI authorization is required.
