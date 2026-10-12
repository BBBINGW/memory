# Iteration 122 — Entropic Ring-LWE TCC 2020 theorem does not certify exact-one-per-block FAB keys

Date: 2026-10-12. PI authorized I122 after I121. ONE primary hypothesis and ONE decisive theorem-assumption alignment test. No authors contacted; no security attack, compiled FHE run, or claim of outright RLWE insecurity. Earlier I110–111 sparse-SAB local terminal-sign archive NOT revisited.

## Research target and source provenance

**Target setting:** Guimarães and Pereira, *Fast amortized bootstrapping with small keys and polynomial noise overhead*, CCS 2025, ePrint **2025/686**, Research MCP original 34-physical-page mirror PDF SHA256 `84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335`; source §6.1–6.2 physical pp21–22 and Table 4 p24 (concrete q=2^64). This setting needs small sparsity h and an interior maximum selector-index gap < B. Iterations I120–I121 already established (a) exponential uniform rejection cost in a valid asymptotic family and (b) exact-one-per-block direct sampler gives B=2n/h but changes distribution and is known prior art.

**Formal theorem to check:** Zvika Brakerski and Nico Döttling, *Lossiness and Entropic Hardness for Ring-LWE*, TCC 2020, IACR ePrint **2020/1185**, https://eprint.iacr.org/2020/1185, accessed as full **25 physical pages** via Research MCP GitHub ePrint mirror, PDF SHA256 `8ee650d5d05d2e7fe33657e35ff5bb9c79be6d16d8a0d8604d8278eb87aa7e46`, source revision `147218513eee9823a019a33ad75df663d2e6420d`, official latest VERSION_UNVERIFIED. Original §1.1 pp3–4, Definition 3.3 p11, Theorem 6.2 p20, **Theorem 6.9 p22** were read. The abstract alone was NOT used.

**Comparison context:** Lee–Min–Seo–Song, *Faster TFHE Bootstrapping with Block Binary Keys*, ASIACCS 2023, ePrint **2023/958**, physical p6 cites Goldwasser et al. arbitrary high-min-entropy result specifically for **plain LWE**; Coron–Köstler SPRU ePrint **2025/651** §4.3 p15 already uses exactly one 1 per block with a separate concrete security analysis. These are not standard-RLWE proofs for the exact FAB setting.

## ONE hypothesis / ONE decisive test

[HYPOTHESIS] The *existing general entropic Ring-LWE theorem* of Brakerski–Döttling (Theorem 6.9) already supplies a direct polynomial-hardness-security justification for **uniform exactly-one-per-block binary** secrets in FAB's small-noise/polynomial-modulus FHE setting, **without** a stronger separate DSPR assumption.

[FALSIFIER / TEST] Substitute the exact min-entropy of the structured secret into the theorem's required **noise-lossiness** lower bound and check if any σ can meet the precondition under its RLWE-only route. Distinguish Ring-LWE from Goldwasser's ordinary LWE result and the theorem's mildly hard search conclusion from full decisional/CPA security. One theorem-to-parameter alignment test, no attacks or further construction.

## Exact bound

[DERIVED] For a ring of length n=hL, exactly one uniformly random 1 in each of h fixed blocks of length L, the distribution has L^h equally likely secrets. Hence

  H∞(S)=h log₂L=(n/L) log₂L.

At L=16, h=n/16, H∞(S)=n/4 bits. Conditional noise-lossiness νσ(S)=H̃∞(s|s+e) cannot exceed the original secret entropy by the factor required here (up to negligible smoothing slack), independently of how σ is chosen.

[FACT] Theorem 6.9 on physical p22 states, **under DSPR with γ plus Ring-LWE**, the condition

  νσ(S) ≥ n log₂(γ log(n) sqrt(n)) + ω(log λ),

and an inflated Gaussian output noise σ0. For its **RLWE-only instantiation**, the paper invokes Theorem 6.2 using γ ≥ poly(n) q^(1/2+α) with α∈(0,1/3), and **explicitly** says it needs a stronger lower bound of the form

  νσ(S) ≥ (1/2+α)n log₂q + O(n log n).

[DERIVED/NEGATIVE] For FAB's concrete q=2^64, the leading required entropy contribution alone exceeds 32n bits (α>0), whereas exact one-per-block L=16 has only n/4 bits. The gap is not repairable by increasing the Gaussian smoothing parameter because the secret's entropy cannot be increased. Even with DSPR, the theorem's explicit γ·sqrt(n)·log(n) threshold is asymptotically incompatible with O(n) total entropy for fixed L if γ is in its admitted admissible regime.

[FACT] The source §1.1 physical p4 directly cautions that its known entropic-RLWE results remain insufficient for **binary ring secret distributions** and that reducing entropy further entails stronger assumptions. This is acknowledged prior literature, NOT a new gap claim.

[FACT / further scope] Theorem 6.9 yields `mildly hard` entropic Ring-LWE, defined as a *search* formulation in Definition 3.3 p11. The paper discusses amplification to standard search hardness with unbounded samples, but this does NOT automatically imply the particular decisional security plus evaluation-key circular-security requirements of SAB. Also, the DSPR-removal Theorem 6.2 needs a prime modulus q splitting the cyclotomic polynomial in the stated form; FAB Table 4 uses q=2^64. The entropy failure already suffices to close the proposed direct theorem application, so these additional scope limits were not separate tests.

## Scientific interpretation

**STATUS:** FAIL proposed already-available theorem-certification hypothesis; PASS specific formal theorem-assumption mismatch.
**RESULT:** The general TCC 2020 theorem is Ring-LWE (not merely standard LWE), but its stated entropy/noise-lossiness prerequisites cannot be met by exact-one binary block secrets in the specified FAB setting. This DOES NOT prove block-secret RLWE insecure, nor exclude all conceivable novel specialized reductions.
**NOVELTY:** Known theorem boundary explicitly recognized by original authors; no new reduction, cost frontier, or FHE correctness counterexample. `NOVELTY NOT VERIFIED`.
**RECOMMENDATION:** PARK the direct block-secret security-repair branch I120–122. Further research here requires a new, nontrivial formal security mechanism with suitable concrete assumptions and FHE efficiency; do not repeat entropy substitutions, naive block sampling or archived sparse-SAB sign work.

## End
STATUS: **FAIL / HUMAN_REVIEW**.
RESULT: **Existing BD20 Theorem 6.9 does not formally certify FAB's exact-one-per-block binary ring-secret construction under RLWE-only assumptions**.
NEXT_ACTION: **PI authorizes a different, explicitly sourced FHE structural research target or a genuinely new security mechanism; absent that authorization, remain NO_ACTIVE_HYPOTHESIS and do not execute I123.**
STATE_UPDATE: YES — materially closes the I122 theorem-certification candidate and parks the FAB I120–122 branch.
