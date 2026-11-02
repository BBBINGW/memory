# BOOT / B158 — Research Turn 22/25

Authoritative result: the Turn19-21 whole-digit-only modulus policy is not source-guaranteed for the first-F4 outer multiplication. The degree-5 outer product has a bounded safe modulus window, and an ordinary ordered ctxt-prime prefix is source-guaranteed to hit that window. Partial-final-digit support is therefore reinstated in the paper construction.

Verdict:
FAIL_WHOLE_DIGIT_SOURCE_GUARANTEE_FOR_OUTER_F4
PASS_PRIME_PREFIX_SAFE_WINDOW_EXISTENCE
PASS_PARTIAL_FINAL_DIGIT_REINSTATEMENT
PASS_FIRST_F4_OUTER_MULTIPLICATION_STATIC_RESCUE

CORRECTNESS_GATE: BLOCKED.
RECOVERY_CANARY: NOT_EXECUTED.
