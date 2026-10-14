# HLUT H06 — Paper samples D over full Fp, author offline generator samples binary D; conditional fixed-budget difference



Date: 2026-10-15 Asia/Tokyo. Standalone HLUT follow-up H06, after H05 was closed and archived. Human PI said continue. Prior materials read: START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, STATE.md (concurrent vFHE V28/next V29, READ ONLY), H04/H05 source citations; SHIP I226 READ ONLY. No update to global, vFHE, SHIP, other workstreams.



## Primary falsifiable hypothesis

H-HLUT-06: Replacing the public author's binary D-coefficient sampler by the full-field D~Uniform(F3) stated in the original paper, while keeping the SAME nonlinear chain U, target Boolean LUT y, decomposition shape (lambda,t), and exact Encoding Switching rule, increases **first-output candidate acceptance probability by at least 10 percentage points** across the small source Table1 regimes n=4,5,6 without adding any online PBS.



Falsifier: Run one paired U/y source-shaped exact finite-field experiment with both D samplers, enforcing rank(UD^T)=t, and calculate acceptance including canonical and Encoding Switching cases. If gain <10 percentage points in a tested regime, disprove the broad hypothesis. Beware structural issue: changing D distribution could change coefficient norms and required TFHE parameter sets even though raw PBS CALL count stays constant.



## Primary paper and author code [FACT]

Sonia Belaid, Nicolas Bon, Matthieu Rivain, Decomposition of Large Look-Up Tables for Fast Homomorphic Evaluation, TCHES 2026 2026(3):247–278, https://eprint.iacr.org/2026/724 , DOI https://doi.org/10.46586/tches.v2026.i3.247-278 . Research MCP complete 32 physical-page PDF fixed-mirror SHA256 cc45b49e20958f5c3fc1e327d84d1549d7fef08bdb4ba973dac75fd3a67efeb4, source revision 108e41a7dc5788eb2d61023f9aecbcb72889d1d9, VERSION_UNVERIFIED relative to publisher. §4.3 printed p14 says random D in Fp^{t×L}, i.e. D sampled uniformly over all p residues. Table1 p21 gives (s=2,p=3) first-output shapes n4:(lambda2,t2), n5:(lambda7,t2), n6:(lambda10,t3); Table3 p25 experimental gamma1 full-rank proportions 9%,76%,0% respectively (sample-dependent, does not prove which code produced published results).



Author released artifact https://github.com/CryptoExperts/artifact-HLUT-TCHES pinned commit 088029cb4cd3a6b33ac10e0c78ea193b1835216d. **Real decomposition generator** `decomposer/src/decomposer/decomposition.py` blob ce5d25df0ec2296c56a75c24e158f6cbe15f90f1, `Decomposition.initialize`: `self.D = self.field(np.random.randint(0, 2, size=(self.t_i, self.n_i)))` (both initial draw and redraw). This is **uniform binary subset** {0,1}, not full F3. Contrast experiments.py blob 1d3d0fa177c31c1c5600efae97bd5f6b5c1ecbe0, `generate_one_random_matrix_A`: `np.random.randint(0, p - 1, ...)`, which for p3 ALSO samples only {0,1} because upper bound is EXCLUSIVE. Thus even the author's rank-distribution experiment does not sample the full F3 for p3. No security flaw in a correct arbitrary source-compatible D; paper's mathematical proof is valid for any sampled D where A is accepted.



## Controlled smallest test [COMPUTED]

File `/mnt/data/hlut_H06_binary_vs_field_D_gate.py` SHA256 **140a2b0cc5cecb8a9c590436163bdcb3fa055f4132e1c5712bf27e3e6adf4515**, uses Numba exact mod3 source-shaped U and A from the earlier verified H05 helper module `/mnt/data/hlut_H05_paired_prefilter_benchmark.py` SHA256 c50675b30ca7f3b499270d9e168e915a9d7ea6ebdee5f1fe1d61ae5a743bbc9b; results `/mnt/data/hlut_H06_binary_vs_field_D_results.json` SHA256 **2790e27433e65f4e8874176426cc87bb7c17316a06695a71f9beb2423ecfca1e**. Random alpha ∈F3, psi among 18 nonlinear unary maps, U full-column rank required. Each SAME U and SAME balanced Boolean target y evaluated under independent binary D and ternary D, redrawing any D until rank(UD^T)=t. Exactly the same (lambda,t) and source encoding-switch check for both. Samples per setting: n4 600 U×12 valid D per variant; n5 220 U×6; n6 90 U×4. No source Rust compiler or ciphertext experiment run.



|n | sampled D per variant | binary D accepted | full F3 D accepted | absolute accepted increase (F3 minus bin) | binary full-A-rank | F3 full-A-rank |

|--:|--:|--:|--:|--:|--:|--:|

|4|7200|3194 (44.3611%)|3637 (50.5139%)|**+6.1528 pp**|687 (9.54%)|1113 (15.46%)|

|5|1320|1194 (90.4545%)|1213 (91.8939%)|**+1.4394 pp**|1016 (76.97%)|1063 (80.53%)|

|6|360|68 (18.8889%)|69 (19.1667%)|**+0.2778 pp**|0|0|



Source's gamma1 Table3 rank 9%,76%,0% aligns approximately with independent binary samplers in these small experiments but is **not provenance proof** of exact author table generation settings. At n4, F3 sampling reduces conditional mean D trials from 1/0.4436≈2.25 to 1/0.5051≈1.98 (rough geometric comparison, NOT actual compiler walltime), and increases full-A-rank frequency. At n6 no full-A-rank candidate in the observed samples, so the restricted circuit shape/chain continues to dominate. Counted independent draws with replacement, clustered by same U/target; these are descriptive conditional finite sampling results, not statistically certified universal probability bounds. No claim D_F3 always improves.



## Impact boundaries and novelty gate



Changing coefficients from 0/1 to 0/1/2 leaves the number of encrypted products and chain PBS calls unchanged algebraically, but can change linear-form coefficient norm νmax, noise amplification, TFHE parameter selection and measured PBS times. In particular, code `norm(vec)` squares unsigned coefficient representatives and its `weighted_sum` handles coefficient2 through `simple_mul_constant`, so do not advertise cost-equivalent, DFR-preserving speedup without full author parameter selection and benchmark. The paper ALREADY specifies Fp sampling in §4.3, so changing the code to it is an existing described option, not a new algorithmic primitive.



**STATUS: FAIL H-HLUT-06** broad ≥10pp acceptance gain across n4/5/6; **PASS** actual paper-vs-implementation sampling-domain discrepancy and exact paired candidate experiment. The gain is modest in target acceptance at all three tested settings, with largest +6.15pp for n4 and essentially nil at n6, despite the more visible n4 full-rank gain. **Result is a bounded reproducibility/implementation sensitivity**, not a paper correctness error, security bug, formal performance benefit, or independent algorithmic novelty. PDF official parity unverified, no FHE code executed.



**NEXT_ACTION: PARK** merely replacing binary D with full Fp as standalone research. It is already in paper, not original novelty; to reopen require (i) original author full-compiler bench with end-to-end parameter/noise selection and updated online latency/DFR, plus material >10% improvement in a realistic precision setting; or (ii) a genuinely new target-aware D-selection algorithm with math/cost/source prior-art gate. Rather than repeatedly searching tiny offline sampling changes, focus next on a distinct high-value FHE research target or PI's active vFHE direction.



**STATE_UPDATE: YES this one HLUT finding file only. NO edits to global STATE.md/vFHE, SHIP memory, HERDS, upstream implementation, or open backlog. NOVELTY NOT VERIFIED.