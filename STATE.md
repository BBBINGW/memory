# FHE Research State — Session Handoff after Iteration 192

**Checkpoint date:** 2026-10-14 (Asia/Tokyo)  
**LAST COMPLETED ITERATION:** **I192 COMPLETED**. **I193 NOT STARTED.**  
**STATUS:** **NO ACTIVE TECHNICAL HYPOTHESIS** / `HUMAN_REVIEW`. Current AKU audit `PARKED — SOURCE_VERSION_GATED` until missing primary material is verified. No new parent target has been selected by the human PI.

## CURRENT TARGET

Last investigated: Qi Zhang, Mingqiang Wang, Xiaopeng Cheng, *Faster FHEW Bootstrapping with Adaptive Key Update*, **CANS 2025**, IACR ePrint **2025/381**, https://eprint.iacr.org/2025/381. This is the **most recent PARKED audit**, not an active construction or confirmed paper vulnerability.

## CURRENT QUESTION

Can the §5.1 Gaussian-key theoretical failure model and reported Table 3 Algorithm 6 DFR `2^-36` be reconciled using the **actual author-edition paper equation and experiment code**? Source verification remains blocked, so do not treat this question as an active hypothesis test without new material.

## PRIMARY HYPOTHESIS

**NONE ACTIVE.** The last tested hypothesis (I192)—that authenticated publisher equations or original author experiment artifacts were publicly available and sufficient for an exact DFR reproduction—was **FAIL** for the evidence then accessible. Conditional question for any future authorized reopening: whether the author-version complete `β` calculation yields its reported `2^-36` DFR.

## CURRENT EVIDENCE

- **[FACT/source]** Public 27-page ePrint version, Research MCP GitHub-mirror PDF SHA256 `bbc507b8323f4a65dea806bb663c9eea8ef2954e41259cad3b9db11256a03faf`, **VERSION_UNVERIFIED** against CANS publisher edition. Springer DOI: https://doi.org/10.1007/978-981-95-4434-9_14 (CANS 2025 LNCS 16351, pp. 292–312).
- **[DERIVED, I190]** Under the **extracted** §5.1 model (not an experimentally verified failure distribution), parameters `n=447, σ=3.19, q=1024, Qks=16384`, `σ_ms2²=(||s||²+1)/12`, `||s||²≈nσ²` imply `β≥19.4716` from final ModSwitch alone; extracted `DFR=erfc((q/8)/(2β))` gives a **modeled** lower estimate `≈3.347×10^-6≈2^-18.19`, conflicting with Table 3's `2^-36`. This is **conditional model/table inconsistency**, NOT proof of actual ciphertext failure, flawed cryptographic security, or inaccurate latency.
- **[FACT+DERIVED, I191]** Present-day upstream OpenFHE uses Gaussian small-key `dgg(3.19)` and coefficientwise final `qKS→q` round. At ratio 16, exact scalar rounding residual has **mean +1/32** (ties upward), variance `255/3072`; source-style `β_MS2≈19.4335`. Integer-level ModSwitch verification passed, but this is **NOT** the author's fixed 2025 implementation, nor full FHE bootstrapping or DFR replication.
- **[NEGATIVE, I192]** Verified final CANS chapter existence, but full rendered §5.1 is restricted; original author AKU source/commit/DFR estimator not authenticated or accessed; rendered ePrint equation screenshot unavailable. No author contacted. The source-availability hypothesis **FAIL**; alleged actual correctness error **UNCLEAR**.

## MAIN OBSTRUCTION

Missing **authenticated primary evidence**: the full final CANS §5.1 with rendered formulas and/or the author's exact AKU implementation/commit, Gaussian-key parameters, full `β` worksheet and Table 3 DFR estimation code. Current OpenFHE HEAD is not evidence of what authors ran. Registered in `MISSING_SOURCES.md` as `Zhang–Wang–Cheng AKU DFR author-edition source (I192)`.

## OPEN UNCERTAINTY

Publisher/ePrint formula equivalence; possible normalization/typographic/implementation differences; complete `σ_acc,σ_ms1,σ_ks,σ_ms2` contributions and dependence; actual Gaussian-key decryption tail and DFR; any impact on 20.7% source-reported speedup under matched DFR, key size and >=128-bit lattice security. **No confirmed paper error, attack, or new FHE algorithm.**

## NEXT_ACTION — new session, not an authorized research iteration

**ONE minimal source-availability/legibility gate:** Check the AKU entry in `MISSING_SOURCES.md` for **NEW** authenticated publisher §5.1 pages or author-pinned implementation/DFR script supplied since I192. If present, verify actual identity/commit/SHA and that the exact formula or estimator is readable; report whether `SOURCE_VERSION_GATED` can be lifted, then await PI authorization for the next single hypothesis. **If none is present, STOP the AKU audit, report PARKED, and ask PI to select the next research target. Do not autonomously select one or begin I193 on handoff.** Do not repeat the previous Gaussian/ModSwitch toy checks.

## RELEVANT FILES

Read in order: `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md`. Then read:
- `findings/fhew-aku-gaussian-dfr-consistency-iteration190.md`
- `findings/fhew-aku-ms2-rounding-code-gate-iteration191.md`
- `findings/fhew-aku-author-repro-source-gate-iteration192.md`
- `MISSING_SOURCES.md` (AKU section)
- `findings/OPEN_RESEARCH_BRANCHES.md` (P18, I190–I192) for other direction statuses only when needed.

**OTHER BRANCHES:** LFBS PRCA I188–189 naive hoisting/bookkeeping PARKED; threshold FHE PRSS I184–187 simple repairs PARKED (broader unbounded-`LDec` open); GBFV I182–183, direct dBFV→BGV I178–181 and earlier unsuccessful ideas archived in corresponding findings/failures and branch index. Preserve all. Research principle: one smallest falsifiable hypothesis + one cheapest decisive test; the human PI controls target, pivots and final scientific judgment.
