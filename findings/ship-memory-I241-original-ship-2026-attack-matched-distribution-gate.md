# SHIP-I241 — 2026 published-work attack estimates for ORIGINAL SHIP parameter triples, and structured-support distribution obstruction

Date: 2026-10-16. **PI-selected active SHIP**, no pivot to CGS/VFHE/EXPLORE. Previous I240 SOURCE_BLOCKED matching Sage analysis of illustrative **third-party Poulpy** `N=16384,dense HW192,q_key=2^520`. I241 does NOT rerun the unavailable Sage estimator, invent a key-recovery attack, or change original SHIP code.

## ONE primary falsifiable hypothesis and ONE minimal decisive test

**H241:** There is NO independently published/submitted post-SHIP concrete attack estimate for the **authors' actual SHIP §5.2 modulus/N/HW parameter triples**, so without Sage the original published security claims cannot be screened more directly than extrapolating third-party Poulpy's hypothetical q520 example. **Falsifier:** a later attack paper explicitly identifies SHIP §5.2 and reports its `logN,h,logq` with estimated work below 128 bits. If found, verify whether the attacked **secret distribution** matches the SHIP author secret's *regularly spaced per-support windows*; distinguish the numerical estimate from a demonstrated break of the exact construction.

**Cheapest test:** Read and cross-match the **original sources** (SHIP §5.1/5.2 pp24–25, Hou–Jiang preprint 2026/366 §5.3 Table 5.1 physical pp31–32) and CRYPTO 2026 merged publication metadata/abstract, then calculate a rigorous discrete window-support conditioning probability at one matching SHIP parameter regime. No code infrastructure expansion.

## PRIMARY FACTS and provenance

1. Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT 2025, ePrint `2025/784`, original §5.2 physical page24, says original sparse-secret `h=31`; evaluated security triples `(logN,log(Pq0)) ∈ {(13,55),(14,100),(15,105)}`, using earlier lattice-estimator. §5.1 page24 specifies each nonzero support coefficient index lies in window `[kN/h−w,kN/h+w)` modulo N for `k=0,...,h−1`, `w=max(175,N/(2h))` in experiments, **not arbitrary uniform 31-subset**. Table2 physical p25 lists LL13, LL14, HT14, HT15. Original cached PDF SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, GitHub mirror VERSION_UNVERIFIED.
2. Hou–Jiang, *Careful with the Ring: Enhanced Hybrid Decoding Attacks against Module/Ring-LWE*, ePrint `2026/366`, §5.3 Table5.1 **physical page32** explicitly attributes two records **[33, Sec. 5.2]** to Cheon–Hanrot–Kim–Stehlé SHIP (confirmed ref33 full bibliographic entry physical page36). Its MATZOV/GSA classical bit-work *heuristic estimates*:
   - `logN=13,h=31,logq=55`: plain guess/verify `TgvDec=137.5`, enhanced `TegvDec=130.5`; plain HG-MITM `ThgDec=122.2`, **enhanced HG-MITM `TehgDec=117.7`**; projected-uSVP 547.4.
   - `logN=14,h=31,logq=100`: plain GV 143.2, enhanced GV137.5; plain HG-MITM126.4, **enhanced HG-MITM122.3**; uSVP641.6.
   Two estimated enhanced attack values are BELOW 128, not actual BKZ executions. Enhanced HG-MITM improves this preprint's corresponding unenhanced HG-MITM costs by 4.5 and 4.1 bits. The unenhanced costs are also <128. **Neither row refers to third-party Poulpy's q520 denseHW192 benchmark**, which has a different secret and key modulus. No estimate here for original SHIP `(logN15,h31,logq105)` (thus HT15 cannot be labelled vulnerable from these rows).
   - Preprint mirror `2026/366`: 58 physical pages, SHA256 `b9c22040d6aed8cbdf6e83921b8b7835ef5bfb4b3b9b3fcb8c86b0d5dbfbca4a`, source_kind github-mirror, VERSION_UNVERIFIED. Extracted tabular text read directly using Research MCP; visual PDF web screenshot unavailable due ePrint 403/GitHub mirror cache miss; treat formula/table transcription as extracted-data verification and avoid invented precision.
3. Hou–Jiang–Ogilvie, *Careful with the Ring! Concrete Hardness Gaps Between LWE and MLWE*, **CRYPTO 2026**, DOI `10.1007/978-3-032-35377-1_15`, Springer first published 2026-08-09. Merged publication confirms enhanced ring-structure primal hybrid security degradation for some sparse FHE sets. **NOTE:** The published Springer abstract reports 10/16 below 128 in its particular comparisons, while the acquired preprint `2026/366` page31 claims 12/16. Thus do NOT automatically attribute exact Table5.1 numbers in the VERSION_UNVERIFIED preprint to the final published Springer table; cite preprint source for exact numbers and DOI only for publication context. Ogilvie ePrint `2026/279` is a related independent predecessor, not the table source.

## New rigorous source-parameter distribution obstruction [DERIVED + executed]

At SHIP `N=16384,h=31`, `w=max(175,N/(2h))=N/(2h)=8192/31`. The `h` consecutive source support windows `[kN/h−w,kN/h+w)` partition the full ring modulo N into exactly 31 DISJOINT integer coefficient cells, of sizes **15 cells×528** and **16 cells×529** (counts sum to 16384). Since there are precisely 31 nonzero positions, satisfying source constraints means exactly **ONE** nonzero in every cell.

If `S` were a uniformly random *unstructured* 31-subset of `{0,...,N−1}`, the probability to have one in every source cell is EXACTLY
```
Pr[structured pattern | uniform Hamming weight31]
 = (528^15 * 529^16)/binomial(16384,31)
 = 4.956062327810504e−13 ≈ 2^(-40.8758709025).
```
This is an **event probability/support-family restriction**, not a security-bit difference, not a direct speedup nor an attack on SHIP. It proves that indiscriminately treating the actual SHIP window-constrained support as an unconditional uniformly chosen fixed-HW31 support is **not distribution-identical**. Conditioning on this ~2^-40.88 event can alter guessing probabilities and especially the claimed rotational advantage. The true SHIP support generator, sign distribution, leakage and encapsulation key samples still need to be checked. It does **NOT** prove the attack fails on SHIP; the constrained support may make an attack EASIER or HARDER depending on the technique.
At `N=8192,h31`, `w=175 > N/(2h)`, so support windows OVERLAP. It is NOT valid to use the disjoint-cell product formula for N8192; no event probability is asserted for that regime.

Exact rational combinatorics script executed and verified at `/mnt/data/ship_i241_ship_security_table_window_audit.py` SHA256 `c225946cb073bb78afd606735a01352fbd4b884210853fce1a6cfc2dcd0e5c8f`, JSON `/mnt/data/ship_i241_ship_security_table_window_audit.json` SHA256 `0cd94e4279b12ebbbef5cd56e5464a3491173c7a2fba7b4106a347c6e2e59fa9`. Script includes original table transcription, exact `fractions.Fraction` window boundaries, `math.comb` full unrestricted support count and model limits. No cryptanalytic computation, no Sage, and no publication novelty claim.

## What these findings DO and DO NOT say

- **PASS**: There EXISTS later independent direct `(N,h,q)`-matched SHIP parameter *heuristic attack cost* warning, **117.7 and 122.3 model bits** under 2026/366 Table5.1, more directly grounded than I239's q468 hypothetical parameter.
- **PASS**: Source window-constrained support distribution differs sharply from uniform fixed-HW, with a rigorous N2^14 support-condition event probability ≈2^-40.88. This **prevents asserting that the attack model already accounts for the authors' precise secret family**.
- **UNCLEAR**: Impact of nonuniform windows on rotated hybrid attack's hit probability, MITM cost, real sample resource and correlated evaluation keys; true security of original SHIP LL13/LL14/HT14/HT15; accuracy of publisher final revised table relative to preprint; proof or real key recovery; actual III party Poulpy denseHW192/q520 security (I240 remains SOURCE_BLOCKED).
- **No source SHIP weakness, practical attack, new crypto primitive or publication novelty has been established.** This is a legitimate scope-versus-parameter-model audit and a strong call for distribution-matched analysis, with independent 2026 prior art explicitly identified.

## End of I241

**STATUS: FAIL H241 (no post-SHIP direct original-parameter attack work)** because 2026/366 already evaluated two original SHIP source triples below 128 in its heuristic model. **PASS exact paper/triple/table match and support-window counting**; **UNCLEAR distribution-matched original SHIP security and actual cryptanalytic cost**. Parent SHIP crypto HMux key-memory compression remains HUMAN_REVIEW / recommend PARK; original author's reported λ128 and newer estimated λ<128 require reconciliation, not a public claim that original SHIP is broken.

**NEXT_TEST I242 only on PI continue:** ONE cheap but decisive **attack-assumption correction**: for actual `h31` SHIP support-window condition, determine how rotated primal-hybrid guessing/hitting probabilities need to change vs unconditional sparse ternary `B_h^-`. Use original 2026 attack probability formula and a mathematically rigorous source-specific support distribution or state exact missing assumptions; test minimal toy/counterexample before running full estimator. Focus explicitly on real SHIP author parameters `(13,55),(14,100)`; do not relaunch exploratory q520/HW192 parameter scans. If no exact support generator or attack formula is accessible, SOURCE_BLOCKED/HUMAN_REVIEW; no invented security bits. **STATE_UPDATE YES** preserve CGS and other research lines.
