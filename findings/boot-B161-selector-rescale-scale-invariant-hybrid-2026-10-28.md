# BOOT-B161 — selector-rescale + scale-invariant fused multiplication hybrid

Date: 2026-10-28
TRACK_ID: BOOT
Status: PAPER_LEVEL_RESCUE_HYPOTHESIS / NATIVE_NOT_RUN

No Codex/native run was launched.

## Motivation

B159:
- selector ct-pt: no rescale
- fused ct-ct: regular multiply + rescale
- FAIL_NOISE at k=4

B160:
- selector ct-pt: no rescale
- fused ct-ct: scale-invariant multiply, no rescale
- FAIL_NOISE at k=4

Source-faithful 2026/975 MonomialGen:
- masked selector ct-pt multiply
- immediate Rescale
- then masked factor enters accumulator multiplication

Thus the untested schedule is:

    selector ct-pt + Rescale
    +
    scale-invariant fused ct-ct with NO Rescale

## Key observation: level count is preserved

Let the current state be at level L.

For each B158 doubling:
1. RowRotation stays at L.
2. selector ct-pt products are computed at L and Rescaled to L-1.
3. factor is assembled at L-1.
4. state at L is multiplied by factor at L-1 using
   MulRelinScaleInvariantNew.
5. output is at min(L,L-1)=L-1.
6. no explicit ct-ct rescale occurs.

Therefore each doubling consumes exactly ONE level.

For r=2^ell:
- total level consumption remains ell
- B158's level advantage is preserved
- 9-bit r=32768 path still predicts basis output around L3 from input L18

This is not the two-level-per-round schedule that would kill B158.

## Why B161 directly targets the failure

B159/B160 both allowed the large coefficient-domain selector product to enter
the fused ct-ct multiplication without normalization.

B161 normalizes the selector via exactly the Rescale mechanism already used by
the source-faithful 2026/975 masks, then uses scale-invariant tensoring to avoid
paying a second level for the fused ct-ct product.

So B161 exchanges where the one mandatory level drop occurs:

B159:
    selector no-rescale + ct-ct rescale

B161:
    selector rescale + ct-ct no-rescale

The recurrence/algebra, N/T/Q/P/security, packing, and 15/14 logical counts are
unchanged.

## Operation structure

For r=32768:
- logical ct-ct multiplications: 15
- RowRotations: 14
- fused ct-ct explicit rescale: 0
- selector branches: same B158 masks, but each variable selector product is
  normalized before factor assembly

The two selector products in a regular round are independent and can be
rescaled in parallel logically; they consume one common level, not two
sequential levels.

## Smallest decisive native gate

Use deterministic x=1 only.

At each stage:
- build selectors with MulNew + Rescale as in source-faithful MonomialGen
- assemble factor at L-1
- call MulRelinScaleInvariantNew(state_L, factor_L-1)
- no ct-ct Rescale
- check exact slots/noise immediately

Required stages:
k=1,2,4,8,... until failure or complete r=32768.

No benchmark unless complete correctness passes.

## Stop / decision

If k=4 still fails or noise budget <=0:
- PARK B158 practical line
- do not add Q primes or increase N
- retain only algebra/optimality result as a paper-level observation

If k=4 passes but a later stage fails:
- record first failing k
- continue only if the noise slope suggests a bounded/local issue, not repeated
  exponential collapse

If all stages pass:
- run matched BuildBasis benchmark
- then evaluate full pipeline value
- only afterwards revisit one-Q-prime reduction

## Status

B158_ALGEBRA = PASS
B158_CTCT_OPTIMALITY = PASS
B159 = FAIL_NOISE
B160 = FAIL_SCALE_INVARIANT_CTCT_RESCUE
B161 = HYBRID_SELECTOR_RESCALE_RESCUE / NOT_RUN

Do not auto-run Codex.
