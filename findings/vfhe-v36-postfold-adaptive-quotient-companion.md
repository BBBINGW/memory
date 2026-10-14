# vFHE V36 COMPANION — Postfold auxiliary quotient adaptivity invalidates a one-challenge Schwartz–Zippel claim

**Date:** 2026-10-15. **NOT a second V36 or a V37 round.** Authoritative V36 main: `findings/vfhe-v36-same-commitment-ipa-privacy-and-work-gate.md`; it established original Yang Pedersen vector commitment + source-Bulletproofs public IPA algebra and separately falsified privacy/computational cheapness. V37 NEXT remains unchanged; general FHE I192 FROZEN. This companion tests a **different optimization**, not any original publication's security theorem.

## One falsifiable hypothesis H-V36C — FAIL

**Our potential optimization:** Fix globally canonical bounded digit vector `a` in a knowledge-bound vector commitment **BEFORE native F.2 challenges**. Let later auxiliary canonical integer quotient vector `k` be chosen AFTER the verifier picks a random external scalar `alpha`, and rather than proving all `D=L*d` exact native-to-integer coordinate relations `S_t=lift(y_t)+p_t*k_t`, use ONE folded R1CS field relation
```
sum_(t=0)^(D-1) alpha^t (S_t - lift(y_t) - p_t*k_t) = 0 mod r.
```
Claim incorrect acceptance bounded by `(D−1)/r` using Schwartz–Zippel. **False**: k varies with alpha, so this is existential satisfaction of a DIFFERENT polynomial for each alpha. Even a perfectly sound zero-knowledge R1CS proof can prove a false *conjunction* as a true *folded existential relation*. Prebinding a is not sufficient to fix the polynomial residual coefficients.

This differs from archived V34 late-digit attack: `a` is genuinely prebound; only quotient auxiliaries are adaptive. Prior V28 abstractly required all folded residuals be fixed, but did not execute THIS exact bounded postfold quotient counterexample.

## Exact original-source anchors [FACT]

- Gil Segev, *Bulletproofs for R1CS: Bridging the Completeness-Soundness Gap and a ZK Extension*, IACR Communications in Cryptology 2025 / ePrint **2025/327**, https://eprint.iacr.org/2025/327. Research MCP cached 31pp GitHub-mirror original PDF SHA256 `029c913fbd6b4f9e1146b9ccdad4e2c0f5b5af860645cc2272603970cd0331c6`, VERSION_UNVERIFIED. §3 physical pp7–8 explicitly defines R_R1CS* commitment T to prefix x and auxiliary y, and §4/Theorem4.1 physical p10 proves perfect completeness, special HVZK and computational witness-extended emulation for the **exact R1CS*** relation and published prefix commitment assumptions. It does NOT make any claim for OUR weakening of original D integer equalities.
- Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025/ePrint **2025/286** https://eprint.iacr.org/2025/286. Research MCP inspected 52pp original PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, VERSION_UNVERIFIED vs official 2026-02-16 revision; §3.1 p10 source CRT field primes, §4.3 pp20–23 digit range, Appendix F.1/F.2 pp50–51 original native Merkle/RS PCS PUBLIC authenticated y. The random quotient fold is OUR candidate, not original source.

## ONE decisive exhaustive toy [DERIVATION + EXPERIMENT]

Source-compatible p13=1+(2N/d)*3, p29=1+(2N/d)*7, N4,d2,H8,beta4. External proof field F1009 (toy, INSECURE group security). Fix GLOBAL PRECOMMITTED canonical `a=(0,0,0,0,0,0,0,0)` before any challenges. Bind honest native MLE field polynomials `h13(b)=1` and `h29(b)=0` at each Boolean point. Both separate native per-prime polynomials are valid and will always honestly open native F.2 y13=(1,0),y29=(0,0); they **cannot** share a correct global bounded integer digit a. No native Merkle/RS forgery is attempted.

For p13, canonical integer S=(0,0) from prebound a. Allow each quotient `k0,k1∈{0,...,22}`, since generic source-friendly bound Smax=(beta−1)H(p−1)=288 and floor(Smax/p)=22. All separate RHS `y0+p*k0 ≤287<1009`, `y1+p*k1≤286<1009`; therefore individual equation no-wrap checks are satisfied. Both required exact coordinate equalities are false for k0=0,k1=1:
```
0 != 1 + 13*0,
0 != 0 + 13*1,
alpha=388: (-1) + 388*(-13) = -5045 = (-5)*1009 = 0 mod1009.
```
Set p29 quotients zero; all p29 residuals zero. Thus even global FOUR-coordinate folding over p13,p29 retains this cheat (zero last two coefficients).

**Full census, NOT Monte Carlo:** Enumerate ALL nonzero `alpha=1,...,1008` and all `k0,k1=0,...,22` in two independently implemented ways. For `k1≠0`, the unique root is `alpha=−(1+13*k0)/(13*k1) mod1009`. Exactly **435/1008=43.1547619%** distinct challenge values admit a bounded post-alpha fake k. If k fixed before alpha, each nonzero linear polynomial has at MOST 1/1008 false accept. This is a toy field counterexample, NOT an estimate of attack success against 253-bit groups or source compiled vFHE.

**Source-scale analytic gate only:** L2,d4→D8 canonical quotient coords; H=2^24,beta4 give max honest quotient <3H<2^26, so there are ≤2^(8*26)=2^208 possible quotient vectors. For any FIXED a and native y which are inconsistent, each *fixed-k* folding polynomial is nonzero with degree ≤7. A union bound with k selected AFTER alpha is **at best** `2^208*7/(r−1)` for external r=2^252+27742317777372353535851937790883648493, log2 ≈**−41.193**. This upper bound cannot certify 128-bit; it is NOT a lower bound on actual failure probability. Two independent random folds with SAME shared late k would have a formal loose bound log2 ≈−290.385 under fixed a,y, but proof composition and costs are NOT yet checked; leave for optional V37 if PI desires. Alternatives: precommit k before folding (and prove same k opened), or prove all D equations directly in ONE Segev R1CS*.

## Provenance and research decision

**STATUS:** FAIL the single postfold random-equation shortcut/naive SZ claim; PASS exact all-alpha bounded-quotient falsifier. Complete 128bit secure CP/native-F2/Fiat–Shamir integration and privacy UNVERIFIED. Not a published paper bug and not a contradiction of Segev's Theorem4.1 (it proves a weaker statement perfectly correctly). No public author disclosure.

**NEXT_ACTION:** Main V36's V37 target remains **a genuine hiding generalized linear quotient proof on same C**, with audited prebinding, source cost, or HUMAN_REVIEW. If exploring folding, minimally compare (i) sound prebound quotient k, (ii) TWO independent fold challenges with a single shared k, (iii) no folding/all D direct equalities. Do not claim external scalar length alone suffices.

**STATE_UPDATE:** COMPANION ONLY. Preserve global I192 frozen and any other active workstreams.

**Local full standalone Markdown:** `/mnt/data/VFHE_V36_Postfold_Adaptive_Quotient_Companion_2026_10_15.md` SHA256 `4ecf5229598f190f167bf8b1330a21b347d3dbe47e6109f3721c3b83d6cbf688`.
**Python exact census:** `/mnt/data/vfhe_v36_adaptive_quotient_fold_gate.py` SHA256 `26e3e42b2b042168d2f81bb4d95147681e34aa08d41a10e0890202f274af8a19`.
**JSON:** `/mnt/data/vfhe_v36_adaptive_quotient_fold_results.json` SHA256 `a25d386bcae539ec8f31a8558e81a8ee33799d0c446d880cf42ba4037d1beedd`.
