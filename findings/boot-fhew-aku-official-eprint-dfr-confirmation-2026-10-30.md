# BOOT — FHEW AKU official-ePrint DFR model/table confirmation

Date: 2026-10-30
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Session: 密码学 15.0 — Research Turn 2/25
Status: PASS_OFFICIAL_EPRINT_MODEL_TABLE_INCONSISTENCY / CANS_FINAL_AND_ACTUAL_DFR_UNVERIFIED

## Primary hypothesis

The previously source-gated discrepancy in Zhang–Wang–Cheng, "Faster FHEW Bootstrapping with Adaptive Key Update" (ePrint 2025/381), can be resolved by authenticating the current official ePrint source: either the official ePrint formula differs from the cached extraction, or its Table 3 Algorithm 6 DFR remains numerically incompatible with the displayed Gaussian-key error model.

## Durable parent context

Prior findings:
- findings/fhew-aku-gaussian-dfr-consistency-iteration190.md
- findings/fhew-aku-ms2-rounding-code-gate-iteration191.md
- findings/fhew-aku-author-repro-source-gate-iteration192.md

I190 derived a conditional lower floor from the extracted model.
I191 checked current upstream OpenFHE Gaussian-key and Qks->q rounding semantics and found no convention-level rescue.
I192 parked the allegation because the official rendered ePrint formula / proceedings edition and author artifact were not authenticated strongly enough.

## Current official ePrint identity

Official landing https://eprint.iacr.org/2025/381 currently reports:
- received: 2025-02-27
- approved: 2025-03-04
- no later revision entry

Thus there is no evidence of a later ePrint correction superseding the inspected PDF.

The official PDF text at https://eprint.iacr.org/2025/381.pdf directly exposes §5.1 physical p19 and Table 3 physical p21. Web screenshot attempts for physical pp19/21 were made again and returned cache-miss; therefore this result is based on the official PDF text layer plus existing independent mirror extraction, not a successful rendered-image parity check.

## Source statements confirmed in the official PDF text

Table 2 / §5.1:
- Algorithm 6 parameter set 128_OURS
- Gaussian key parameter sigma = 3.19
- n = 447
- q = 1024
- Q = 2^28
- Qks = 2^14

The paper writes refreshed-ciphertext standard deviation beta as

beta^2 = (q^2/Qks^2) * ((Qks^2/Q^2) sigma_acc^2 + sigma_ms1^2 + sigma_ks^2) + sigma_ms2^2,

with

sigma_ms2^2 = (||s||_2^2 + 1)/12,

and for Gaussian secrets

||s||_2 = sqrt(n sigma^2).

It states that LWE_q,s(q/4*m) has largest noise standard deviation sqrt(2)*beta, fails beyond q/8, and gives per-NAND failure probability

1 - erf((q/8)/(2 beta)).

Table 3 reports Algorithm 6 failure probability 2^-36 (Algorithm 5: 2^-37).

## Cheapest decisive arithmetic

All variance terms in the displayed beta^2 expression are nonnegative. Therefore the final ModSwitch term alone gives

||s||_2^2 = 447 * 3.19^2 = 4548.7167,

sigma_ms2^2 = (4548.7167 + 1)/12 = 379.14305833333333,

beta >= 19.471596193772438.

Using the paper's displayed failure formula,

P_fail >= erfc(128 / (2*19.471596193772438))
       = 3.346946255388498e-6
       ~= 2^-18.1887231846.

This is about 230,000 times larger than 2^-36.

Conversely, even setting every earlier variance contribution to zero, P_fail <= 2^-36 would require

beta <= 13.404271464416768,
||s||_2^2 <= 2155.0939219013317,

equivalent to an RMS Gaussian key standard deviation at most about 2.19573 if n=447, not the source's sigma=3.19 substitution.

Under a continuous Gaussian diagnostic only, ||s||^2 <= 2155.09 has probability about 1.86e-23 (~2^-75.5) when sigma=3.19 and n=447. This diagnostic is not needed for the model contradiction and is not a discrete-Gaussian security claim.

## Verdict

PASS_OFFICIAL_EPRINT_MODEL_TABLE_INCONSISTENCY.

The current official ePrint text itself confirms the exact ingredients needed for the contradiction. Therefore the previous I192 label can be refined:

- current official ePrint model/table numeric consistency: FAIL
- later ePrint correction: NONE FOUND
- CANS proceedings formula/table parity: UNVERIFIED (Springer full chapter remains access-gated)
- author-specific implementation / complete beta worksheet: UNVERIFIED
- actual empirical decryption failure rate: UNVERIFIED
- 128-bit lattice hardness: NOT CHALLENGED
- claimed 20.7% runtime measurement: NOT CHALLENGED

This is a confirmed source-internal numerical inconsistency for the ePrint, not yet a proof that the deployed/author implementation fails at 2^-18 or that the CANS final contains the same defect.

## Follow-up significance

This branch is now worth one later source-faithful parameter-repair gate only if the final proceedings or author code becomes available: recompute a matched DFR<2^-32 parameter set and test whether Algorithm 6 retains its speed/key-size advantage. Without that evidence, do not repeat Gaussian toy calculations.

The later Bernard–Joye ePrint 2025/163 develops a distinct automorphism-based method and does not visibly cite or reproduce the AKU DFR table in the inspected text; no downstream baseline contamination is established here.

TOP_LEVEL_BOOT_FRONTIER_EXHAUSTED: false.
PENDING_CODEX_TASKS: none.
