# BOOT-B148 — Phase-quotient root splitting from one B^2 root

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Parent: B145/B147
- Source: supplied 2026/2368 and supplied 2026/1869; OpenFHE HE-standard parameter table
- Status: PASS_ALGEBRA / FAIL_AS_PRIMARY_BACKEND / PARK
- CODEX_REQUIRED: NO

## Question

From the single root

    Rw = zeta_{B^2}^w,   w=Bb+c,

can we derive separate B-th roots for c and b without the extra root production of 2026/2368 Remark 2, then evaluate all B145 factors by cheap B-point LUTs?

## Algebra

The low-part root is

    Rc = Rw^B = zeta_B^c.

If a B-point LUT on Rc returns

    q(c)=zeta_{B^2}^{-c},

then

    Rb = Rw*q(c)=zeta_B^b.

Therefore the algebra is exact on the B^2 roots, and all B145 factors can then be evaluated as B-point LUTs on Rb or Rc.

This avoids the second RootB call of 2368 Algorithm 5.

## Why it is not a free root split

Producing Rc from a slot ciphertext holding Rw is itself a homomorphic power operation. For B=64, a power-of-two chain needs six dependent squarings.

The branch-selection map

    zeta_B^c -> zeta_{B^2}^{-c}

is not a monomial on the B-th roots. Its exact interpolation has full B-point support; it is the branch choice that recovers c/ B rather than an integer power of the root. Evaluating it therefore costs a genuine B-point LUT.

After q(c), constructing Rb costs another ciphertext multiplication, and the b-dependent functions then require another B-point LUT stage.

Thus the explicit phase-quotient route has the dependency pattern

    Rw
      -> six-level B-th power
      -> B-point q(c) LUT
      -> one multiplication
      -> B-point b-LUT.

By contrast, 2368 Algorithm 3 evaluates the required functions directly as shared B^2-point LUTs on Rw; all outputs reuse the same powers of the root.

The phase route may reduce the size/number of power bases and scalar coefficient work, but it adds roughly one extra log2 B-sized dependent stage.

## Relation to 2368 Remark 2

2368 already gives the alternative "two roots of period B":
1. RootB(B*window) gives Rc;
2. LUT_id and StC recover c in coefficient encoding;
3. subtract c from the window;
4. a second RootB gives Rb;
5. B-point LUTs evaluate the carry/function data.

B148 replaces steps 2-4 by a leveled phase-quotient computation. It is therefore a direct latency-vs-depth alternative to the paper's two-root route, not a new one-bootstrap conceptual architecture.

## Parameter headroom

2026/1869 uses N=2^16 and HEStd_128_classic. For n=256 its analytical conversion modulus is

    log2 Q = 44 + 43*(19+6) = 1119 bits,

with a 400-bit special modulus, total about 1519 bits. The implementation paragraph reports one additional level, corresponding to roughly 1562 bits if charged at 43 bits.

OpenFHE's HE-standard table gives, for ring dimension 65536:
- HEStd_error, 128-bit classic: max logQ 1749;
- HEStd_ternary, 128-bit classic: max logQ 1747.

So the remaining standard headroom is only about 185-228 bits, depending on which 1869 depth accounting is used.

An extra six 38-bit levels already cost 228 bits; six 43-bit levels cost 258 bits, and the additional Rb multiplication makes the explicit phase route still tighter. Therefore the route cannot be assumed to preserve the N=2^16 / 128-bit / same-scale parameter point. It is at best on the boundary under an aggressively small level scale and otherwise requires rebalancing the chain or increasing N.

This is a value/security-parameter obstruction, not a universal impossibility result.

## Decision

- Algebra: PASS.
- Removes second RootB of 2368 Remark 2: YES.
- Direct one-root B^2 MVB already available in 2368 Algorithm 3: YES.
- Extra dependent depth: substantial, about log2 B plus an additional multiply compared with direct B^2 lookup factorization.
- Matched N=2^16 modulus headroom: too tight to regard the extra levels as free.
- Novelty: weak; this is a factorization tradeoff adjacent to an explicit paper remark.
- Native/Codex: NO.
- Decision: PARK / FAIL_AS_PRIMARY_BACKEND.

B145 should keep the direct single B^2-root route as its primary architecture. Optimization effort should target the cost of that shared 12-bit lookup without introducing a second sequential root or a large extra depth chain.
