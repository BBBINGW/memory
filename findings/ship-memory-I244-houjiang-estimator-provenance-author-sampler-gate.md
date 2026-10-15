# SHIP-I244 — Primary 2026 attack estimator source recovered; SHIP input parameters confirmed, author secret windows NOT modeled

Date 2026-10-16. **User PI authorized continuation SHIP**, active line SHIP h31 security prior / original HMux key-memory security baseline; follows I243. No automatic pivot to CGS, VFHE or EXPLORE. Read-before-write: RESEARCH_PHILOSOPHY.md, AGENT.md, START_RESEARCH_SESSION.md, STATE.md, findings/ship-memory-STATE.md, I243. Single falsifiable gate: whether accessible actual authors' attack estimation outputs/author secret sampler resolve previous SOURCE_BLOCKED status.

## Primary H244 and cheapest decisive falsifier

**H244:** The original authors' `h=31` SHIP secret-key generation and/or 2026 attacker SHIP Table5.1 full model and optimized dropped-set/hg/BKZ parameters are presently available as independently verifiable source artifacts, so the numerical estimates 117.7/122.3 can now be interpreted as **secret-distribution-matched** for SHIP. **Test:** Follow paper 2026/366's exact code-and-data footnote, read *its* first-party improved lattice estimator, actual parameter builder and **saved result dataset**, inspect signed-support and window-handling, then look for author h31 implementation. Stop if author sampler / optimized attack dimensions unavailable; no invented Sage execution or security correction.

## New decisive first-party source [FACT]

The key previously missed paper clue is footnote 1 on physical page2 of Hou–Jiang, ePrint **2026/366**, revised March2026. It explicitly says revised evaluation code/data/figures at **https://github.com/identitymapping/enhanced_lattice-estimator**. This is NOT the previously inspected GPU execution project `identitymapping/enhanced_hybrid_attack` (which mainly saves toy/benchmark results, not original FHE parameter cost table). Exact primary GitHub source files read through connected GitHub:
- `identitymapping/enhanced_lattice-estimator/README.md`, blob SHA **583be99956df430aba6b50cffdfa9219ac21db83**: confirms `deg_ring=params.n,structure_leverage=True`, change to augmented N rotations and a two-stage search for optimal dropped dimension/other BKZ parameters; generation of original paper Table5.1/TableG.1 via `FHE_paper_estimate.py` and result dataset. Based on prior lattice-estimator e35f45b plus updates.
- `FHE_paper_estimate.py`, blob SHA **ef845580494722aff5d4ed3382e11460117d5b6b**. Explicit original-SHIP-labeled parameters:
```python
ec25_q_13=LWEParameters(n=2**13,q=2**55,
                         Xs=SparseTernary(15,16),
                         Xe=DiscreteGaussian(stddev=3.19),tag="ec25_q_13")
ec25_q_14=LWEParameters(n=2**14,q=2**100,
                         Xs=SparseTernary(15,16),
                         Xe=DiscreteGaussian(stddev=3.19),tag="ec25_q_14")
res_ehg = LWE.primal_hybrid(params, mitm=True,babai=True,
                red_cost_model=RC.MATZOV,
                deg_ring=params.n,structure_leverage=True)
```
**The signed support prior is precisely 15 positive,16 negative at arbitrary coordinates; there is NO SHIP `w`, `i_k`, regularly-spaced window or per-window conditioned sampling argument in these source parameter objects.** The scorer in `estimator/lwe_primal.py` blob **08c7b0bb1c301f4b14ff85cb5cb8da16f5718410** uses `new_prob = 1-(1-p)^N` from assumption under ring rotation; does not add secret window constraints. `estimator/nd.py` blob **c244ad2e32094be8dc64561ffbf7a9d92e5f1a88** explicitly documents `SparseTernary(p,m)` as exactly p entries +1 and m entries -1 in n (i.e. balanced **by fixed sign counts**, not independent signs).
- **NEW definitive published author computation artifact** `FHE_paper_estimate_results.csv`, blob **e7e5d1da0b85599a50a136996f510e5dba4930f8**. Rows:
  `ec25_q_13,3590.76,547.41,130.48,137.51,117.65,122.2,470.31,99.0,104.37,100.13,104.32` and
  `ec25_q_14,7141.2,641.65,137.48,143.22,122.3,126.41,555.12,104.88,109.11,105.53,110.12`,
  columns `Scheme,TimeElapsed,usvp,egv,gv,ehg,hg,qusvp,qegv,qgv,qehg,qhg`. Thus Table5.1 classical `ehg` exactly **117.65 and122.30 model work bits**, which round to 117.7/122.3; ordinary hg **122.20 and126.41**. `Time Elapsed (seconds)` are ESTIMATOR's worker runtimes (~3590.76 /7141.2), **NOT** real key-recovery attack runtimes. Quantum results are likewise estimated, not attacks.
- Importantly, `FHE_paper_estimate.py` currently PRINTS the detailed `res_ehg` cost object (including optimal `β,zeta,d` etc) to standard output, but the CSV only SAVES rounded cost scalars; neither the source-generated CSV nor previously inspected GPU `results/attack_estimate_results.txt` exposes optimized `k,h_g,β,d` for these two SHIP rows. `FHE_paper_estimate_results.xlsx` referred to in README was NOT accessible at that path; project actually contains `FHE_paper_estimate_results.csv`. A GitHub API directory listing verified the source py and CSV are present, and no FHE xlsx root.
- The official archived author SHIP ePrint **2025/784** §3.2 p15 motivates ordered i.i.d uniform indices, then suggests a tighter public high-bits/window restriction. §5.1 p24 asserts `i_k∈[kN/h−w,kN/h+w)` with `w=max(175,N/(2h))`. §5.2 p24–25 original experiment uses `h=31,N∈{8192,16384,32768}` and different q. The paper does NOT provide an authenticated precise `h31` algorithm implementation for these windows in inspected sources, and the accessible independent Poulpy `ShipPlan::new` **requires h|N**, which none of three pairs meet (I243). Web, public GitHub source, targeted `snucrypto/HEAAN` and author code queries did not resolve an author-labeled compiled SHIP sampler. **Never claim it does not exist anywhere: SOURCE_NOT_FOUND_IN_INSPECTED_EVIDENCE.**
- Subsequent published *Careful with the Ring! Concrete Hardness Gaps Between LWE and MLWE*, Hou–Jiang–Ogilvie CRYPTO2026 DOI `10.1007/978-3-032-35377-1_15`, independently confirms this is an attacker model but doesn't prove author source distribution matching. Specific numbers above attributable to ePrint2026/366 and GitHub csv, NOT assumed final published Table5.1.

## Key analytical consequence [DERIVATION, important correction]

The two `(N,h,q)` are **numerically identical** to original SHIP author Table5.2 h31 security modulus pairs (confirmed), but `SparseTernary(15,16)` is **uniform across all C(N,31)*C(31,15) balanced signed supports**, while the SHIP author uses strongly position-constrained support, AND may have different sign distribution. Thus published attack work 117.65/122.30 **is an actual first-party computed estimate for numerical triples under a different secret prior**. It is not an actual attack on SHIP author secret, not distribution-matched cryptographic proof and not a demonstrated invalidated estimate. I242 at a non-optimized random-J attack parameter showed hypothetical independent-uniform-one-per-window support roughly preserves the independent-rotation heuristic; can't assert a safer true SHIP threshold from mismatch.

**No exact k,h_g,β,d for original rows** can be read from saved CSV. To obtain them, run correct fork under Sage and persist the complete `Cost` objects; local runtime `command -v sage` absent and Python imports sage and fpylll fail. Do not reverse-engineer k from 117.65 scalar cost, or treat program printed estimate as measured break.

## Reproduction interface and minimal verification [EXECUTED STATIC ONLY]

Created `/mnt/data/ship_i244_reproduce_author_hybrid.py`, SHA256 **072f235dbc5d14e3433a5dea7e2d212c32c1678ed2175ed493c24980dd7499a6**; `/mnt/data/ship_i244_source_gate.json` SHA256 **303089cf2b3c79a9aa8d4075327c6e0774db63213860a010dee05cd2e35fd08a**. Standalone CLI re-creates both exact `LWEParameters`, MATZOV enhanced HG calls using the newly found author fork, and serializes complete `Cost` fields and comparison to source saved CSV; has `--dry-source-check` without Sage. Local **python -m py_compile PASS**, **dry source check PASS**, real Sage estimator NOT RUN (no Sage/fpylll). It also explicitly marks true SHIP window prior and sample counts NOT matched. Use after a correctly pinned checkout installed under Sage, e.g. `sage /mnt/data/ship_i244_reproduce_author_hybrid.py --repo /path/to/enhanced_lattice-estimator --run-only 13`. Since the source `main` runs 20 processes for full parameter table and each original estimate can take minutes/hours, only invoke targeted 1 case once dependencies are installed; do not claim a result until then.

## End I244

**STATUS:** **PASS locate first-party corrected attacker Table5.1 generation code AND saved exact numerical costs; FAIL the hypothesis it includes actual SHIP secret-window sampling; SOURCE_BLOCKED obtaining exact author h31 HEaaN sampler and optimized attack k,h_g,β,d without Sage.** One new concrete, source-backed mismatch confirmed in executable parameter builder: balanced signs SparseTernary(15,16) and *unrestricted positions* vs SHIP §5.1 windows. No claim of key recovery, corrected security bits, practical break, or new SHIP compression primitive.

**RESULT:** Close origin-of-numbers uncertainty: ePrint Table5.1 `117.7/122.3` arises from first-party saved `117.65/122.30`, not prior indirect third-party proxy. Precisely pin attack's **wrong-for-SHIP windowed secret prior** and recovery path for full optimization dimensions. Does not determine if distribution mismatch increases/decreases attack effectiveness.

**NEXT_TEST I245 only on PI continue:** If new source capability exists, execute ORIGINAL AUTHOR `identitymapping/enhanced_lattice-estimator` optimized attack rows under real Sage, capturing k,h_g,β,d and testing window-conditioned hit probabilities under verified author sampler. Without author distribution + Sage, mark this security auditor SOURCE_BLOCKED/HUMAN_REVIEW and do not extend identical source searches or toy parameter variations; PI decides freeze/pivot. Separate SHIP HMux key-memory compression branch remains recommend PARK absent a genuinely safe Pareto primitive. **STATE_UPDATE YES.**
