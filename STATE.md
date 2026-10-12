# Research State

Updated: 2026-10-12
ACTIVE: vFHE / FHE+ZK soundness discrepancy and efficient cross-CRT repair.
PARKED: RIG-HE — preserve full prior state at `logs/rig-state-2026-10-12-pre-vfhe-handoff.md`; do not resume or archive without PI decision.
ARCHIVED PRIOR BRANCH: GL generic BigSwitch structure (see `failures/gl-generic-bigswitch-structure.md`). Other old findings/failures retain their own statuses.

## CURRENT TARGET
Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes* (CRYPTO 2025), IACR ePrint 2025/286, particularly §4.3 Eq. (21)–(23)/Theorem 4.8/Appendix E.2 (CRT digit lookup), §4.1–4.2 (CKKS rescale/ΠAC), and §5 (componentwise Brakedown polynomial commitments).
Audited source: 52-page post-revision-looking mirror PDF, SHA-256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, pinned to a 2026-04-28 mirror commit after official 2026-02-16 revision; **current official PDF byte identity VERSION_UNVERIFIED**.

LAST COMPLETED ITERATION: **79 (2026-10-12)**. No research iteration 80 started.

## CURRENT QUESTION
Can a low-cost, zero-knowledge, cross-characteristic witness-binding interface link an **externally committed hidden canonical integer residue** `u_k=A mod p_k` to the **field-native Brakedown-PC aggregate** `Σ_i α_i h_{k,i}`, without importing the entire field-PC verifier into an external SNARK?

## PRIMARY HYPOTHESIS — UNTESTED / ONE NEXT TEST
Under pre-challenge binding of a common small-integer vector `b` and per-CRT-field vectors `h_k`, an existing Brakedown field-PC evaluation/opening and a published dual-PCS/commit-and-prove construction MAY expose a reusable commitment/witness-link API proving `u_k = Σ_i α_i h_{k,i}` without a full non-native verification circuit. **Falsifier:** the concrete interfaces do not support hidden cross-characteristic equality without externalizing field verifier logic or similarly costly per-entry checks. No such efficient API is established yet.

## CURRENT EVIDENCE
- [FACT / SOURCE] Revised-looking Theorem 4.8, Appendix E.2 physical p48, uses a global-digit-outside-table ⇒ some CRT-component-outside-table inference. Audited 52-page mirror has a remaining diagonal-vs-rectangular CRT lookup discrepancy; latest official bytes not authenticated.
- [DERIVED / PASS, I59–I70] CRT mixing gives `t_beta ⊊ t_beta^rect`; the paper's fieldwise argument naturally supports `T_B^rect`, not original global coefficient table `T_B`. If `B >= max_i p_i`, then `T_B^rect=R_q`. Explicit algebraic counterexamples, source comparison and range PIOP checks archived.
- [DERIVED / PASS, I71–I76] In paper-formatted small algebraic CKKS parameters `(N,d)=(8,4)`, primes `(149,157,173)`, `q=4046989`, zero ciphertext inputs have true rescale output 0; claimed public output `y=(173,0)` is coefficient-range valid and satisfies `0-4017060-173*173=-q≡0 (mod q)` using an illegal remainder. Source-equivalent ΠAC Eq. (16)–(20), one adaptive six-step/20-round ideal-oracle transcript and negative binding controls checked. **No exact authors' compiled PIOP/PC/Fiat–Shamir proof forged; not a deployed attack or practical-security-parameter example.**
- [NEGATIVE / I63–I68] Local product-ring polynomial checks cannot enforce global scalar digits; raw position sampling, naive cross-characteristic RS coding and constant-block sign-WHT repair variants fail in specified regimes.
- [DERIVED / I77–I78] A single CRT-reduced “shared commitment” or post-challenge aggregate can be patched across fields (FAIL). Exact external shared opening plus sound field links is conditionally binding; random binary-mask inner product catches a fixed, precommitted nonzero difference with probability ≥1/2 per round **only if** exact aggregate is proven tied to the external committed vector. Publishing it leaks witness information.
- [NEGATIVE / PASS REFINED FIX, I79] Hidden integer carry check over `F_P`: `P>T=m(β−1)` alone is not enough with independently bounded `u,c`. Exact witness `T=1920,P=1931,A=144,u_173=172,c_173=11` satisfies field equality due to `2075=144+1931`, but violates integer congruence. Sound sufficient condition: `P>max(T, floor(T/p_k)p_k+p_k−1 for all k)`, or prove `0≤u_k+p_k c_k≤T`. This fixes only the carry gadget, **not** cross-field ZK linking.

## MAIN OBSTRUCTION
[OPEN] No efficient, *hiding and knowledge-sound* equality link `external C_{u_k} ↔ native field PC opening of Σα_i h_{k,i}` is known from current evidence. Simply equating modular projections does not work; generic full non-native verification may erase the original Πrange efficiency. Prior-art compatibility and realistic prover/verifier costs unverified.

## OPEN UNCERTAINTY
- Latest official ePrint PDF SHA/version identity is unverified; authors have NOT been contacted. User explicitly directed **DO NOT SEND EMAIL**; no external/private disclosure or Gmail draft without explicit new permission.
- No original-source exact optimized ΠAC byte transcript, original PC commitments/openings, compiled SNARK/Fiat–Shamir forgery, or practical security-parameter counterexample.
- No complete fast ZK repair, no cross-characteristic link soundness theorem or quantified end-to-end costs; novelty/publishability unverified.
- Earlier RIG-HE practical-dimension/novelty questions remain PARKED in preserved snapshot.

## NEXT_ACTION — ONE SMALLEST DECISIVE TEST
Read **ePrint 2025/286 §5's Brakedown field-PC evaluation/opening interface** and **Ganesh–Nair–Sharma, CCS 2024, *Dual Polynomial Commitment Schemes and Applications to Commit-and-Prove SNARKs***. Extract the exact commitment/opening/linked-witness API and test whether it can prove the HIDDEN canonical `u_k=A mod p_k` equals the NATIVE `Σ_i α_i h_{k,i}` across different characteristics **without placing the whole field-PC verifier into the external proof**. Record an explicit compatible interface or the first precise incompatibility; if incompatible, report a defensible cost obstruction or UNCLEAR/HUMAN_REVIEW. Do not open another repair variant or contact authors.

## RELEVANT FILES — read selectively in the new session
- Protocol: `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `START_RESEARCH_SESSION.md`.
- Last result / current proposed bridge: `failures/vfhe-hidden-aggregate-carry-wrap-even-when-P-above-T-iteration79.md`.
- Previous bridge falsifier: `failures/vfhe-batched-crt-aggregate-without-shared-integer-opening.md`.
- External commitment requirement: `findings/vfhe-external-commitment-crt-full-opening-link-iteration77.md`.
- Primary soundness discrepancy: `findings/vfhe-crt-lookup-cross-component-soundness.md`, `findings/vfhe-theorem48-actually-sound-rectangular-relation.md`.
- Computation-layer evidence: `findings/vfhe-ckks-public-output-binding-robust-rescale-counterexample.md`, `findings/vfhe-piac-adaptive-six-step-oracle-binding-audit.md`.
- Source/version caveat: `findings/vfhe-theorem48-post-revision-mirror-provenance-diff.md`.
- Unsent report and contact draft: `findings/vfhe-confidential-pi-review-package-iteration74.md`, `findings/vfhe-confidential-author-inquiry-draft-iteration75.md`. DO NOT send.
- Parked RIG history (verbatim): `logs/rig-state-2026-10-12-pre-vfhe-handoff.md`.

## STATUS
**ACTIVE vFHE | LAST I79: FAIL** naive `P>T` carry criterion, **PASS** corrected arithmetic bound, **UNCLEAR** efficient zero-knowledge cross-characteristic PCS link. Continue only the recorded single interface audit when the PI requests another research iteration. **SESSION HANDOFF COMPLETE; NO NEW RESEARCH IN THIS HANDOFF.**
