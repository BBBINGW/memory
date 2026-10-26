# PURE-FHE · P0-PRESCOUT-35 — Adaptive heterogeneous gadget schedule: single-query union certification gate

Date: 2026-10-27 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: INDEPENDENT_PURE_FHE_SOURCE_FIRST_SCOUT
PREVIOUS: P0-PRESCOUT-34 (findings/pure-fhe-p0-heterogeneous-cggi-adaptive-failure-mixture-tail-gate-2026-10-27.md, git blob 91b9e464ae5c503952e6ead9528fcc59ebfc99e3)
STATUS: FAIL_PER_FIXED_SCHEDULE_BOUND_TRANSFERS_UNCHANGED / PASS_FINITE_SCHEDULE_UNION_CERTIFICATE / PUBLISHABLE_NOVELTY_NOT_ESTABLISHED
NOVELTY: NOT_ESTABLISHED — standard event union is sufficient for a conservative single-query setting; rare-event component prior art already exists
CODEX_REQUIRED: NO. No native, GPU, remote environment, repository infrastructure or model downloads.
STATE_UPDATE: YES: one isolated PURE-FHE findings file ONLY, shared STATE.md and other tracks untouched.

## One primary falsifiable H35
H35: If every pre-generated static heterogeneous gadget decomposition schedule has fresh-input single-query decryption failure probability at most delta, any public-quality-guided *adaptive* choice among those schedules necessarily has failure probability <= delta, without new conditional analysis, multi-schedule penalty, or full-composition noise certificate.
Cheapest decisive falsifier: use exact failure-event quantifiers for two fixed schedules and a publicly chosen selector; then give the strongest unconditional **valid** replacement using the union bound, and compare with the real number of duplicated keys reported in 2025/1892 Table4. No need for native cryptography to falsify this logical transfer.

## Source-based facts, no source overclaims
[FACT] Deokhwa Hong and Yongwoo Lee, *Optimizing FHEW-Like Homomorphic Encryption Schemes with Smooth Performance–Failure Trade-Offs*, ePrint 2025/1892, 26-page GitHub-cached PDF source SHA256 508a5a0b3914e23e8d71198476a50879c471a6f192e6f65bcd68314b89622018, mirror VERSION_UNVERIFIED.
- Original §3.1 physical p12 Theorem3.1 assigns heterogeneous bases to CGGI RGSW blind rotation keys, gives an expression for **fixed-choice** blind-rotation variance.
- §5.1–5.2 physical p18 considers a fixed-iteration noise-quality procedure and gray-area duplicated (e.g. dg2/dg3) bootstrapping keys which the server may select at runtime based on observed public switching-quality statistic. §5 p19 Table4 labels the resulting FP range an *approximation* from E[Z*]±10 std and lists a configuration {2:319,3:215,both:22}; this does not prove all 2^22 combinations are reachable/used, nor a rigorous all-adaptive-secret DFR guarantee.
[FACT] Mathieu Ballandras, Jean-Baptiste Orfila, Samuel Tap, *Concrete Estimation of Correctness and IND-CPA-D Security for FHE via Rare Event Simulation*, ePrint 2026/610, 45-page GitHub-cached PDF SHA256 a202bddc7abefa96aa2cd931eb071552a5d2605e70eaaf89322a48d3b1ba3ee5, mirror VERSION_UNVERIFIED.
- Physical §5.1 pp20–22 importance splitting applies to fresh LWE ciphertext distributions and specific component score functions, using Gibbs resampling with input noise.
- Crucial §5.2 pp23–24 explicitly states the WHOLE KS→modswitch and whole atomic pattern are unsuitable for their direct importance-splitting sampler since changing a single input mask coordinate can re-randomize the key-switch output mask, violating the smooth variation assumption; they instead study KS and MS separately and justify broad empirical confidence, not a blanket theorem for *all arbitrary adapted gadget schedules*. The reference paper's rare-event method/conditional quality test are already prior art, and this scope limit is expressly acknowledged by its authors.
- Appendix B.2 pp36–37 derives input-noise-aware quality tests for multibit drift mitigation. This is existing functionality, not a new invention by this note.
- §5.1 chooses a random LWE input with a **fixed binary secret of Hamming weight n/2** for importance splitting, whereas appendix B discusses uniform binary secret for independent block variance. §3 of 2025/1892 uses ternary secret in primary tuning examples. Sampling distributions, fixed key, and the reuse threat model are NOT silently interchangeable.

## [DERIVATION] Precise disproof H35

Let Omega contain all keys, public input mask/rand, ciphertext, and all precomputed versions of duplicated evaluation keys as needed for a single execution. For a static schedule s in finite set S, F_s is the event that evaluation with s fails when all randomness is drawn from the specified static-schedule experiment. Let S(omega) be a publicly observable-state-determined schedule. The actual event is F={omega : omega in F_{S(omega)}} = union_s ({S=s} ∩ F_s).

Unconditional static guarantees Pr(F_s)≤delta do **not** imply adaptive Pr(F)≤delta, since selection and per-schedule error can be correlated even if selection only uses public information.

Exact toy: U is public uniform from {0,...,2^k−1}. F_A={U=0}, F_B={U=1}, each probability delta=2^−k. Public policy S(U)=A if U=0, B if U=1, arbitrary otherwise; actual failure event is {U∈{0,1}} and has probability 2delta. This tests the quantifier logical inference only, not a plausible concrete FHE cryptanalytic attack or author-claimed theorem.

## [DERIVATION] Valid conservative fallback

For any even malicious/adaptive choice of a schedule among a FINITE family in this SAME single-query experiment,
  Pr(F) ≤ Pr(union_s F_s) ≤ min(1, sum_s Pr(F_s)).
If each bound is ≤delta, then Pr(F)≤min(1, |S| delta).
This is an elementary union-bound *single-query* certificate, so a new probabilistic primitive is not **necessarily** required just to have SOME sound bound. Independence between schedule-choice event and failure is neither required nor presumed.

For Table4 example with 22 duplicated keys, if independent gadget-versions on each key can in principle be chosen freely, the number of theoretical combinations is |S|≤2^22=4,194,304 (a bound on **possible options**, not an author's reported actual policy), yielding the *worst-case union certificate* per static 2^-128 up to 2^-106; to achieve <=2^-128 by that crude union bound requires each static option <=2^-150.

If the authorized public policy first commits to a fixed nested ordering of the 22 duplicate keys and only allows prefix-length j∈{0,...,22} high-accuracy versions, there are at most 23 schedules, incurring ceilish log2(23)=4.523561956... worst-case bits from union bound. Same static per-schedule 2^-128 would yield ≤23·2^-128 ≈2^-123.4764, so each requires ≤2^-132.52356 for a combined 2^-128. Whether such nesting is materially slower than the source's unrestricted gray-area strategy or results in a valid desired predicted noise profile was NOT tested. This is transparent **existing algebraic policy restriction**, NOT a new FHE mechanism.

For an additional q=2^20 adaptively chosen queries, a naive *extra union* would lower the formal exponent to 86 bits in the 2^22 unrestrained case, or 103.476 bits with 23 restricted schedules, BUT ONLY IF each relevant query has a justified, conditional-on-history bound. Static fresh-random-ciphertext DFR from papers is NOT by itself a per-adaptive-query bound, so these q numbers are purely illustrative requirements and NOT proven IND-CPAD parameters. A generic anytime guarantee requires bounding Pr(F_j | history_before_j) uniformly, or otherwise a full multi-query security game; then sum of per-query risks is sound.

## Novelty / priority decision

H35 FAILS, but a conservative single-query certificate is available through elementary union bound with no new cryptographic primitive. Source 2026/610 itself already notes why its original importance-splitting sampler cannot be directly run end-to-end over KS→MS; it does not certify the adaptive gray-area combined operation as an automatic corollary. There is an **exactly stated verification gap**, not yet a positive new construction, attack, security flaw, or publishable theorem.

The only plausibly publishable mechanism would be either:
(a) a rigorous *joint/conditional rare-event sampler* that handles discontinuous re-randomization and the **actual** 2025/1892 adaptive policy, with variance/DFR tail statistics, acceptable statistical confidence, and explicit key-and-query security model; or
(b) a sound schedule-selection rule that provably dominates the union-bound conservative cost under real correlated distributions and beats existing fixed choices in matched native runtime/key-RAM with no uncompensated security/DFR loss.
Neither was designed/tested here. Similar compiler/state-conditioning, union bound, multi-risk budgeting and already-published source techniques are PRIOR ART. Without an actual mechanism and nontrivial gap size, PARK this subline; don't consume Codex or resume repetitive noise toy scans.

END_OF_ITERATION
STATUS: FAIL_STATIC_TO_ADAPTIVE_SAME_DELTA / PASS_SAFE_FINITE_UNION_CERTIFICATE / PUBLISHABILITY_UNCLEAR_NOT_ESTABLISHED
RESULT: fixed schedule δ does not transfer without cost to public-input-adapted schedule; two-schedule exact counterexample; union fallback ≤|S|δ; 22 duplicated keys allow up to 2^22 options versus 23 nested options, with worst-case bits 22 vs 4.52356.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: HUMAN_REVIEW/PARK 1892+610 unless one specific *new* conditional tail mechanism and its expected performance advantage over finite-union fallback is derived from the original algorithm and compared with 610's own sampler limitation. Else select an independent source-complete PURE-FHE problem.
STATE_UPDATE: YES isolated finding only; other tracks/root unchanged.
CODEX_REQUIRED: NO (deferred until explicit PI authorization).
