# BOOT — Lossy key switching before exact error bootstrap: source-gated tradeoff

Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER_LEVEL_ONLY
CODEX: NOT_USED
NATIVE: NOT_RUN

## Authoritative BOOT state

LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE_GATE: B163_CORRECTED_B160_NOSCALE_SELECTOR_GATE
B163_STATUS: PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
DO_NOT_AUTO_RUN_CODEX: YES

B158_ALGEBRA: PASS
B158_CTCT_MULT_COUNT: OPTIMAL
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B158_NATIVE_FEASIBILITY: UNRESOLVED
B163: NOT_RUN

## Source trigger

Philippe Chartier and Mohammed Lemou,
"Exact Error Bootstrapping and Comb Bootstrapping in FHEW/TFHE",
IACR ePrint 2026/2630.

Public abstract facts safe to use:
- it refreshes by bootstrapping the ciphertext error rather than the decryption message;
- rounding at a resolution aligned with the message modulus preserves the message;
- a small reduction exposes a noise-free encryption of the error, then one blind rotation lifts it exactly and the result is subtracted;
- comb bootstrap refreshes several ciphertexts with one blind rotation;
- between refreshes an integer remains in one ciphertext and supports modular additions and multiplications without programmable bootstrapping;
- the error bootstrap is refresh-only; arbitrary functions still require programmable bootstrapping.

Public abstract:
https://eprint.iacr.asia/2026

Full text is currently unavailable through the research MCP:
- official IACR PDF: HTTP 403;
- exact-title arXiv fallback: unavailable;
- fixed arturo-kong mirror: 2026/2630.pdf absent.

Therefore the exact recoverable-error interval, rounding quantum, ring-size condition, and key-switch placement in the authors' pipeline are UNKNOWN.

## Research question

If an exact error bootstrap follows a key switch, can we intentionally use a coarser/smaller approximate key switch, tolerate a larger deterministic key-switch residual, and let the subsequent error bootstrap remove it?

This is interesting only if it reduces a material key/runtime cost without forcing a compensating increase in the error-bootstrap ring/error domain.

## Generic approximate-key-switch residual lemma

Consider an input LWE mask a=(a_1,...,a_n) under secret t, with at most h nonzero secret coordinates and |t_i|<=S.

Suppose the key switch replaces each a_i by an approximant a~_i with residual

    rho_i = a_i - a~_i

and uniform bound

    |rho_i| <= eps.

Then the deterministic phase residual from approximate decomposition is bounded by

    |e_res|
      = |sum_i rho_i t_i|
      <= h S eps.

For centered base-B decomposition with l kept digits over integer modulus q, the standard truncation-scale model gives approximately

    eps <= q/(2 B^l),

hence

    |e_res| <= h S q/(2 B^l).            (1)

This is only the deterministic decomposition term; ordinary encryption noise in the switching key and digit-weighted noise must be added separately.

## Standard-decryption comparison

If an ordinary post-switch ciphertext must itself remain decryptable for plaintext modulus p with spacing roughly q/p, the deterministic term alone needs approximately

    h S q/(2 B^l) < q/(2p),

or

    B^l > h S p.                          (2)

An exact error-refresh stage may allow a larger pre-refresh error budget E_boot.

If the concrete 2630 theorem permits total pre-refresh error up to E_boot, then the analogous deterministic condition becomes

    h S q/(2 B^l) < E_boot,

or

    B^l > h S q/(2 E_boot).              (3)

Thus a real key-size opportunity exists only if the error-bootstrap admissible interval is materially larger than the ordinary decryption/standard-PBS tolerance.

## Cost-conservation gate

Removing one gadget digit shrinks key material and key-switch work, but multiplies the truncation residual by B.

If the error bootstrap requires a larger ring, larger small-error modulus, or more table capacity in proportion to the enlarged error support, the saving may merely migrate downstream.

The decisive ratio after recovering the full source is:

    saved_KS_cost_per_removed_digit
        versus
    added_error_bootstrap_cost_from_B-times-larger error range.

PARK immediately if the second term cancels or exceeds the first.

## Prior-art boundary

Approximate gadget decomposition itself is mature TFHE prior art:
- TFHE already uses approximate gadget decompositions;
- ePrint 2023/771 revisits key decomposition techniques;
- ePrint 2024/909 develops approximate CRT-based gadget decomposition;
- Circuit Bootstrapping: Faster and Smaller (ePrint 2024/323) explicitly reduces gadget length through approximate decomposition.

Therefore novelty cannot be:
    "use fewer gadget digits."

Any novelty would have to come from a new cross-stage theorem showing that exact error bootstrapping enlarges the admissible approximation region enough to support a strictly better end-to-end key/runtime tradeoff than conventional approximate decomposition.

## Why this is not yet high priority

Three uncertainties are source-critical:
1. the exact 2630 recoverable-error bound;
2. how that bound scales with ring dimension / blind-rotation resolution;
3. whether the authors already exploit coarse key switching or otherwise absorb previous-stage approximation error.

Without those, no positive construction or value claim is authorized.

## Gate decision

LOSSY_KS_RESIDUAL_BOUND:
    PASS, scheme-independent.

ERROR_BOOTSTRAP_CAN_ABSORB_COARSER_KS:
    PLAUSIBLE BUT NOT ESTABLISHED.

END_TO_END_COST_GAIN:
    UNKNOWN.

PRIOR_ART:
    APPROXIMATE_DECOMPOSITION CROWDED;
    CROSS-STAGE EXACT-ERROR-ABSORPTION NOT DIRECTLY FOUND IN TARGETED SEARCH.

NOVELTY:
    NOT ESTABLISHED.

PRIORITY:
    LOW-MEDIUM / SOURCE_GATED,
    below the 2026/1779 partial-recovery interaction-rank candidate.

CODEX/NATIVE:
    NOT REQUIRED NOW.

## Next minimum verification

After obtaining ePrint 2026/2630:
1. extract exact pre-bootstrap error interval;
2. extract dependence on ring dimension and error support;
3. identify all key switches immediately before error refresh;
4. substitute (1) into the authors' correctness bound;
5. test l -> l-1 and l -> l-2 symbolically;
6. compute total key bytes / operations saved versus any parameter increase;
7. PARK if savings only move from KSK to larger error-bootstrap parameters.

B163 remains untouched and stays the highest native gate when Codex quota returns.
