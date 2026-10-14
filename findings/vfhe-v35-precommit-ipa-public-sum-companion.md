# vFHE V35 COMPANION — Precommitted Pedersen vector and Bulletproofs IPA dynamic canonical linear openings disclose lifted quotients

**2026-10-15; COMPANION, NOT a second V35 or V36.** Authoritative V35 is `findings/vfhe-v35-mmp-subvector-range-vs-canonical-linear-link-gate.md`, which source-audits Yang et al. ePrint2024/827 SINGLE-vector range proof, finds its unmodified AoKagg z-geometric weights cannot prove arbitrary native MLE canonical-lift rows, and leaves V36 NEXT. Global general I192 remains frozen. This companion tests one explicitly published **alternative generalized arbitrary-linear opening**, Bulletproofs §3 Protocol1/2, and its critical privacy/cost gate. Does not overwrite main.

## One primary hypothesis and decisive test

**Our H-V35C [FAIL full hiding composition; PASS core linear opening]:** Fix one blinded Pedersen vector commitment C_a to the entire canonical digit vector *BEFORE* native F.2 challenges, then after native MLE point u use published Bulletproofs §3 IPA to prove the exact canonical integer weighted sum S=Σ_b lift_p(chi_b(u)) a_b from that SAME C_a. Hope this gives a drop-in, **private and efficient** cross-prime equality without an extra linked ZK protocol. **Falsifier:** two legal a,a' with the SAME native public y but different publicly disclosed canonical integer S at fixed query; also implement the actual recursive argument to rule out a merely symbolic interface claim.

## Primary source evidence [FACT]

- Bünz, Bootle, Boneh, Poelstra, Wuille, Maxwell, *Bulletproofs: Short Proofs for Confidential Transactions and More*, ePrint **2017/1066** https://eprint.iacr.org/2017/1066, full Research MCP 45pp GitHub mirror SHA256 `c79f9c32d061c6814e57d1d4007958efed66923f0194497e8596aa3edd387a53`, VERSION_UNVERIFIED. Source **§3 physical pp12–16**, Protocol1/2: binding vector commitment `P=g^A h'^B` and public `c=<A,B>`, with logarithmic-size recursive proof; §3 explicitly says standalone IPA itself is **NOT zero-knowledge**, in contrast to §4/5 ZK constructions. §3 p14 estimates source standard prover work ~8n exponentiations and verifier work ~4n exponentiations per IPA, with multi-exponent optimizations.
- Cascudo et al. vFHE ePrint **2025/286**, source inspected 52pp mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19` VERSION_UNVERIFIED vs Feb2026 latest. Appendix F.1 p50 native factor PC, F.2 p51 authenticated publicly sent native evaluation `y=<v',q2>` and additional `v,v'`, without an automatically linked global canonical integer witness.
- Prior local authoritative V31 canonical quotient target; V32 insecure executable public-y CP; V34 postchallenge adaptive-a failure; V35 main single subvector range proof with z-power AoKagg. This companion concerns OUR attempted mixed protocol, not a flaw in either cited published work.

## Two-phase IPA relation [DERIVATION]

Precommit `C_a=product_b g_b^{a_b} h0^rho` to one a∈[0,beta−1]^H. After C_a fixed, verifier asks coefficient vector c_b=lift_p(chi_b(u))_t from authenticated native reference-field MLE at challenge u. Build padded IPA dimension n=next_pow2(H+1) with witness vectors `A=(a_0,...,a_{H−1},rho,0,...)`, `B=(c_0,...,c_{H−1},0,...)`. Put h0 as a g-generator for blinding coordinate. Let public IPA statement `P=C_a * product_j h'_j^{B_j}` and public scalar `S=sum_b c_b a_b`. Bulletproofs §3 proof of knowledge for `P=g^A h'^B`, `<A,B>=S` computationally binds the postchallenge **PUBLIC** linear opening to a precommitted same vector (proper DL-hard group, public generator independence, and correct binding transcript assumed). If 0≤S<r (scalar group order) and a itself is proved bounded, comparing S mod p with native authenticated y rules out proof-field wrap. But stock IPA alone does NOT enforce digit range a_b<beta and directly reveals S.

## Exact privacy boundary [DERIVATION + REPRODUCTION]

Source-legal N4,d2,p13=1+4*3, H8=2³,beta4, native actual extension K=F13[T]/(T²−5), choose offcube vector u=(2+T,3+2T,5+3T). Exact brute-force search over [0,3]^8 found **two legal bounded vectors**
`a=(0,0,0,0,0,0,0,0)`,
`a'=(0,0,0,0,0,3,3,1)`.
Both have the **SAME** native MLE value `y=(0,0)` in K. Yet the canonically lifted integer weighted base-coordinate sums are `S=(0,0)` and `S'=(39,26)`, with true nonzero quotient `(3,2)` because 39=0+13*3,26=0+13*2. These are <r1009; no group-order alias. Revealing S differentiates these legal witnesses although native public y alone does not. This is an extra-leakage claim **RELATIVE TO y ONLY**; original native F.2 also publicly sends v,v', and the full transcript's ZK privacy is not analyzed. Original source does not claim IPA §3 is ZK.

## Actual recursive group IPA [EXPERIMENT, NOT secure crypto]

Stand-alone Python faithfully implements source BP Protocol1/2 algebra: C_a group commitment and public h'^B, verifier independent first x for adding u^{x*S}, recursively generate L,R, verify P_next=L^(x²) P R^(x^−2), fold g,h and a,b, check final one-dimensional relation. Tiny group order **1009** in F10091^*, SHA-derived generators, deterministic seeded interaction: **for each of the two witnesses**, ONE fixed blinded C_a reused by separate public-coordinate t=0,1 IPAs; all 4 pass and each mutated S+1 public statement fails. Two executed runs byte-identical. Small group is trivially DLog-breakable and provides NO cryptographic security, random-oracle FS proof, published BP full end-to-end protocol, ZK, or side-channel guarantee. Illustrates exact algebra only.

## Honest proof and computation cost [DERIVATION NOT BENCHMARK]

For H=2^24 and one separate rho coordinate, naïve BP §3 vector padded to n=2^25: one IPA proof BODY `2log2(n)=50` group elements +2 proof scalars, ~**1664B** @32B each. Eight native 2prime*d4 coordinate claims would send ~**13,312B** IPA proof bodies, excluding C_a, original F.1/F.2, a committed-a RANGE proof and privacy. This demonstrates V33 stock H public individual commitments are not mandatory for arbitrary PUBLIC vector linear opening. But source §3 ordinary prover about 8n group exponentiations/IPA => ~**2,147,483,648** across eight; optimized verifier still a ~**536,871,312**-base MSM (eight checks), two n-length generator vectors 2GiB if cached, and 8H=134,217,728 canonical lifted public weight coefficients in direct design. None are absolute lower bounds; no optimized execution at source-scale.

**STATUS:** PASS *conditional*, actual executable unsecure toy prechallenge single vector+dynamic public IPA linear binding; FAIL stock IPA as HIDDEN quotient/effective full ZK patch or proof of cheap end-to-end implementation. IMPORTANT: main V35 Yang §4 already establishes an actual single-commitment RANGE proof but its geometric-weight interface is not our generalized IPA; combining their security properties into one coherent sound/ZK cross-transcript construction is **NOT automatically justified**. No claim of independent publication novelty or original published vulnerability.

**NEXT_ACTION:** Keep authoritative V35's **V36** as next. Prioritize one real ZK hiding general-linear-opening for the SAME prebound range-approved vector commitment, with native y and bounded integer quotient CP, or HUMAN_REVIEW/PARK. No further plain PUBLIC S proof retests.
**STATE_UPDATE:** COMPANION ONLY; main V35 remains completed/V36 next; global I192 FROZEN.

**Artifacts exact generated SHA256**
- Report: `/mnt/data/VFHE_V35_Precommitted_IPA_Public_Sum_Privacy_Gate_2026_10_15.md` SHA256 `1debed700a7ad5c9123b818b7655b289a573dc5db692ce0cb5c40273c5bd3d63`.
- Script: `/mnt/data/vfhe_v35_precommit_ipa_public_sum_gate.py` SHA256 `8ae35b9b48b62fdb3172d4ea2e5368247f3d77e6ec71243cd1a934d4bfb9efb6`.
- JSON: `/mnt/data/vfhe_v35_precommit_ipa_public_sum_results.json` SHA256 `8886be5aab52b6973d281bdb58effd601689e4a6578b2e79e782e1cb391a2abf`.
