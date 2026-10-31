# BOOT Turn 22 — MRFHE m-RLWE / Lattice-Estimator Parameter-Link Gate

Recovered scientific disposition from ChatGPT conversation
`6ae441d4-6358-83ec-ad8b-14168b9e9db0` during conversation/database reconciliation.

## Verdict at the end of Turn 22

- `PASS_NONTRIVIAL_REDUCTION_NOISE_SCALING`
- `SECURITY_CERTIFICATE_PARAMETER_LINK = UNCLEAR`
- `NO_BELOW_128BIT_CLAIM`
- `PARK_PENDING_EXACT_ESTIMATOR_REPLAY`

The turn observed the Appendix A scaling factor `c ≈ 3.1162339` for radix 3
and distinguished the claimed implementation noise from the ordinary-RLWE
source point under its then-current interpretation. It explicitly did not
claim that MRFHE falls below 128-bit security and parked the question pending
the exact estimator invocation. Turn 23 subsequently corrected the direction
of this interpretation and killed the candidate.

Original fallback artifact SHA-256:
`7754d82c6c8b5807a3a55aad7a0acf15fbd93f226b2d80d5d7ac0609a3941dca`.

