# Resume Independent FHE Bootstrapping Research — Post B163

Date: 2026-10-28
TRACK_ID: BOOT

## Authoritative state

LATEST_COMPLETED: B163_AUDIT
B163_STATUS: FAIL_B163_NATIVE_NOISE
B158_PRACTICAL_LINE: PARK
NEXT_NATIVE_GATE: NONE
CURRENT_MODE: PAPER_LEVEL / SOURCE_LEVEL RESEARCH

The user remains PI. Do not run Codex/native/server jobs or change parameters without explicit authorization.

## B163 decisive evidence

Artifact SHA-256:
`bb35766751a0439de8e92db3668082930afc84fa49b32ae44b8df093ce85bfad`

Independent audit:
- outer hash PASS;
- all SHA256SUMS entries PASS;
- fixed source parameters confirmed;
- corrected row key L18;
- first row use L18;
- 12/12 reached RowRotations exact;
- selector Rescale count 0;
- fixed logQ=649 throughout B163 recurrence.

Failure:
- exact through k=4096;
- k=4096 state budget +29;
- target-k=8192 dominant selector factor budget +3, exact;
- after fused k=4096->8192:
  required_logQ=665,
  logQ=649,
  budget=-16,
  mismatches=32768/32768.
- counts: ct-ct 13/15, RowRotation 12/14.
- no timing benchmark.

B163 therefore genuinely falsifies the corrected no-rescale source-point realization.

## B158 final practical status

Keep:
- algebra PASS;
- power-basis recurrence PASS;
- 15 ct-ct count OPTIMAL under ordinary arithmetic SIMD model;
- novelty PROMISING_NOT_ESTABLISHED at the narrow state-invariant level.

Change:
- native feasibility -> FAIL_AT_FIXED_SOURCE_POINT;
- practical line -> PARK.

Do not rescue by adding Q primes, increasing N, weakening security, or ordinary Rescale placement.

Lattigo v6.2.0 Rescale divides both ciphertext/noise and the last modulus prime; it approximately preserves coefficient-noise budget rather than creating new headroom. B162's frequent-rescale trajectory is empirically worse. Therefore do not start a B164 sparse-Rescale tuning round unless a new mechanism changes the noise law.

## Current paper-only priority

1. ePrint 2026/1779 — ring-switch partial recovery / interaction-rank candidate.
   Next gate: type-check and cost the quadratic uv cross-leaf statistic in the actual scheme.
2. ePrint 2026/2630 — lossy/coarse KS followed by exact error bootstrap.
3. fresh structural scout.

Preserve prior PARK/CLOSED decisions from the post-structural-scout handoff.

No other research track is modified.
