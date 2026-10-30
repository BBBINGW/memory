# BOOT — 2026/1840 arbitrary-M post-Truncate error-envelope / LUT-domain tradeoff gate

Date: 2026-10-30
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Session: 密码学 15.0 — Research Turn 16/25

Status:
FAIL_SOURCE_ERROR_ENVELOPE_PRESERVATION /
PASS_EXACT_WINDOW_ENDPOINT_ERROR_AMPLIFICATION /
PASS_DELTA_OVER_D_TRADEOFF /
FAIL_PARAMETER_ONLY_RESCUE_WITH_SMALL_LUT /
POSTTRUNCATION_TWO_FBT_ROUTE_PARK_BOUNDARY_REPAIR_REQUIRED /
1836_NATIVE_SURVIVOR_UNCHANGED

## Parent state

Turn 14 derived the unique exact arbitrary-M rank-1 localizer
  y_i = x_i + alpha_i x_{n-1},
with
  alpha_0 = 1-delta/d,
  alpha_i = -delta/d^{i+1}, i>=1,
for M=d^n-delta.

Turn 15 showed:
- large transform coefficients cancel from all radix recurrences except the initial/boundary recurrence;
- secp256k1-p at 50-bit scale is not immediately killed by the fresh-encoding N-sized error bound;
- global scalar normalization cannot remove the cost while preserving the same LUT interface.

Turn 16 asks a stronger source-compatibility question:
Does the post-Truncate arbitrary-M route preserve the same usable input-error envelope as the original 1840 two-FBT A2B, or does it require a much cleaner ciphertext?

## Primary hypothesis

The post-Truncate/pre-ModRaise rank-1 route is a drop-in extension of the 1840 two-FBT A2B in the sense that, for the same window radix D=d^omega and the same first-FBT interpolation tolerance tau, it tolerates coefficient errors of the same order as the d^n source construction.

Cheapest falsifier:
compare the exact error entering the INITIAL window's modulo-D FBT in the source d^n path and in the arbitrary-M localized path. This avoids any implementation-specific noise model.

## 1. Source d^n initial-window error

Let the post-Truncate coefficient vector be x+e with
  ||e||_infinity <= E.

For window length omega and radix
  D=d^omega,
the initial window uses endpoint
  i0=omega-1.

In the d^n source construction, the special-d0/local-radix representation gives the initial scaled difference
  s0_source = -D x_{i0}
up to the public offset/overflow terms handled by RefreshI.

The approximation-error contribution is therefore
  eta_source = -D e_{i0},
so
  |eta_source| <= D E.

If tau denotes the maximum input perturbation tolerated by the first modulo-D FBT at its chosen precision, a necessary source-style condition is
  E < tau/D.

No concrete numerical value of tau is needed for the comparison.

## 2. Arbitrary-M rank-1 route initial-window error

For i0=omega-1,
  alpha_{i0} = -delta/d^{omega} = -delta/D.

Thus
  y_{i0} = x_{i0} - (delta/D) x_{n-1}.

The same source initial-window operation gives
  s0_M = -D y_{i0}
       = -D x_{i0} + delta x_{n-1}.

For errors e,
  eta_M = -D e_{i0} + delta e_{n-1}.

Hence
  |eta_M| <= (D+delta) E.

To feed the SAME first FBT with the SAME tolerance tau, the arbitrary-M route requires
  E < tau/(D+delta).

Therefore the admissible coefficient-error envelope shrinks by the exact factor
  R = (D+delta)/D
    = 1 + delta/D.

This is an algebraic consequence of the boundary recurrence and is independent of CKKS implementation details.

Verdict:
PASS_EXACT_WINDOW_ENDPOINT_ERROR_AMPLIFICATION.

## 3. secp256k1-p concrete tightening

For
  delta = 2^32 + 977,

the tightening factor is:

D=32:      R ~= 2^27.00000034
D=64:      R ~= 2^26.00000035
D=256:     R ~= 2^24.00000041
D=1024:    R ~= 2^22.00000067
D=2^16:    R ~= 2^16.00002234
D=2^20:    R ~= 2^12.00035251
D=2^24:    R ~= 2^8.00562488
D=2^28:    R ~= 2^4.08746315
D=2^32:    R ~= 2^1.00000016

Thus any practically small D leaves a many-bit tightening of the pre-FBT coefficient-error requirement.

The Turn-15 50-bit fresh-encoding check corresponds only to one exceptionally clean operating point. It does not show preservation of the source arithmetic-mode error envelope after nontrivial homomorphic computation.

## 4. Why Truncate does not solve the envelope problem by itself

The 1840 RefreshI ordering uses Truncate to remove INTEGER overflow while retaining the fractional/message part before fresh modulus raising.

The proposed T is intentionally placed after Truncate so the old integer overflow does not become fractional.

But this ordering does not algebraically clean the approximation error e. The rank-1 transform is applied to whatever residual coefficient error remains after Truncate.

Therefore the exact comparison above applies to the post-Truncate residual error, regardless of how that residual arose.

A separate cleaning/rounding mechanism would be needed to reset E to a much smaller source-independent bound before T.

No such mechanism is part of the current proposed transfer.

## 5. Parameter-only rescue conflicts with the LUT domain

The only direct way to make
  R = 1+delta/D
constant is to choose
  D = Omega(delta).

For secp256k1-p this means a window radix on the order of 2^32.

But 1840's first bootstrap evaluates x -> x mod D using a D-entry periodic LUT / interpolation polynomial whose degree scales with D (and whose polynomial depth grows with log D).

Thus choosing D~delta converts the small-domain functional bootstrap into a roughly 2^32-domain lookup, destroying the reason the 1840 A2B is efficient.

Conversely, keeping D small enough for the source's low-precision FBT forces a large delta/D precision penalty.

This yields a structural tradeoff:

  small D  -> efficient LUT, but very tight coefficient-error envelope;
  D~delta  -> source-like error envelope, but infeasible/huge LUT domain.

Verdict:
PASS_DELTA_OVER_D_TRADEOFF.
FAIL_PARAMETER_ONLY_RESCUE_WITH_SMALL_LUT.

## 6. Drop-in transfer hypothesis fails

The direct post-Truncate rank-1 construction does NOT preserve the source d^n A2B error envelope.

For the same D and same FBT tolerance tau:
  source:       E < tau/D
  arbitrary-M:  E < tau/(D+delta).

For close-to-power-of-two primes with delta >> D, this is a qualitatively stronger precondition.

Hence the route is not a drop-in two-FBT arbitrary-prime extension of 1840.

This does NOT prove that a carefully prepared fresh ciphertext can never pass. It proves that the transferred algorithm loses the source's robustness to accumulated coefficient error by a factor 1+delta/D.

## 7. Scientific interpretation

The obstruction is now localized very precisely:

- algebraic locality can be restored exactly;
- integer-overflow compatibility can be restored by moving T after Truncate;
- numerical conditioning is NOT globally bad;
- BUT the initial modular window equation is a high-sensitivity boundary with coefficient delta.

The missing technique is therefore not another global transform.

A meaningful repair must specifically protect the boundary equation, e.g. one of:
- boundary-only cleaning before the first FBT;
- split high/low representation of the delta*x_{n-1} correction;
- a different G_M whose boundary defect is small while retaining a local recurrence;
- a separate small-domain boundary correction combined with the 1840 interior two-FBT machinery.

These are future hypotheses only.

## Verdict

FAIL_SOURCE_ERROR_ENVELOPE_PRESERVATION.
PASS_EXACT_WINDOW_ENDPOINT_ERROR_AMPLIFICATION.
PASS_DELTA_OVER_D_TRADEOFF.
FAIL_PARAMETER_ONLY_RESCUE_WITH_SMALL_LUT.

AI_PROVISIONAL_CHOICE:
PARK the direct post-Truncate/pre-ModRaise arbitrary-M two-FBT transfer.

Reopen only with a NEW boundary-specific mechanism that removes or isolates the delta-sensitive row without enlarging the main LUT domain to Omega(delta).

The independent 1836 fused-prime 5->4 candidate remains the strongest BOOT survivor and its native task remains execution-blocked, not scientifically failed:
BOOT-1836-FUSED-P64-SECP256K1P-NATIVE-20261030-R12-01.

TOP_LEVEL_BOOT_FRONTIER_EXHAUSTED: false.
PENDING_PI_DECISIONS: none.
PENDING_CODEX_TASKS:
- BOOT-1836-FUSED-P64-SECP256K1P-NATIVE-20261030-R12-01 remains pending/execution-blocked.
