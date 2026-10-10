# Iteration 50 — Universal sprout bit size is not a monotone key-switching cost metric

Date: 2026-10-10
Branch: Grafting RNS-CKKS (independent of parked RIG-HE).
STATUS: FAIL for **smaller selected sprout always yields fewer KS gadgets or cheaper sprout NTT arithmetic**. NO demonstrated Grafting correctness bug. No demonstrated full key-switching slowdown: full Algorithm4 normalizes both input moduli to SAME Q_inter, so equal active gadget work in the fixed test.

## Read-before-write, objective, provenance
[FACT] Read latest GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md and prior I49 `failures/grafting-ks-rs-order-rounding.md`. I49 naive rescale-before-relin scheduling already archived and NOT reopened. STATE.md concerns a separate parked RIG-HE project and must remain unchanged.
[FACT / PRIMARY] J. H. Cheon, H. Choe, M. Kang, J. Kim, S. Kim, J. Mono, T. Noh, *Grafting: Decoupled Scale Factors and Modulus in RNS-CKKS*, ePrint 2024/1014, full 20 physical-page text via connected Research MCP, mirror PDF sha256 `f50de6671019f6f71c69f24f7686f21a21ab1cb5dd70bb2f66cb12a96da1ce4c`, VERSION_UNVERIFIED. Peer-reviewed 15-page CCS 2025 postprint also acquired independently from https://orbilu.uni.lu/bitstream/10993/68347/1/3719027.3765083.pdf , DOI 10.1145/3719027.3765083. Original 20-page full ePrint contains an appendix not present at the same page offsets in published shorter paper.
- §3.2 Example3.2, physical ePrint p.9: universal sprout `r_top=2^15*r1*r2`, `r1=2^16+1` and `r2=2^30-2^18+1`, for ring N<=2^15. Both `2^15*r2` and `r1*r2` are allowed divisors in displayed sample sprout set; q_i are ~61-bit NTT primes.
- §3.2 Algorithm3 physical ePrint p.9: picks output sprout based on proximity to target logarithmic bit length. This is **not** a global fastest-hardware schedule; changing sprout to one 1 bit larger need not respect a fixed scale target.
- §3.2 gadget-block placement and Algorithm4 physical ePrint pp.9–10, published postprint pp.8–9: sprout-containing group first; `Q0=r_top q0 ... q_(alpha-2)`, other groups word-sized primes, `d=ceil((ell+1)/alpha)`. Algorithm4 first Inv-RS to `Q_inter=Q0 ... Q_(d-1)`, then ModUp/gadget KS under that modulus, then RS back to input Q. The full target block always uses `r_top`, not the smaller active `r`.
- Appendix A.2.1, Example A.1, physical ePrint pp.16–17: supports composite NTT with `r1*r2` as one ~46-bit NTT modulus; power-of-two part requires emulation with helper prime `g>N*2^30`; product needs more than a single 64-bit modulus if paired with 30-bit `r2` for the particular large power-of-two factor; authors discuss opportunities for single-word special cases, and explicitly acknowledge hardware-dependent NTT cost. This is **prior art already in the paper**.
[VERSION/QUALITY] Exact equations in ePrint text extraction can be garbled; independently checked published Algorithm4 PDF screenshot p.9. All concrete numerical facts and CRT-root existence checked by an exact Python script; no ambiguous formulas inferred from text alone.

## One primary hypothesis / cheapest decisive falsifier
[HYPOTHESIS — FALSE] With same 61-bit unit-prime prefix and same gadget partition, reducing current sprout r strictly reduces the number of gadget key switches and does not increase the number of 64-bit NTT channels required for sprout arithmetic.
[FALSIFIER] A permitted pair `r_small < r_large` with inverse standalone sprout NTT-channel order, while both invoke identical gadget block count and same expanded Q_inter in Algorithm4.
[CHEAPEST TEST] Fix N=2^15; use exact paper Example3.2 r1,r2; choose three distinct NTT-friendly ~61bit unit primes and alpha=2, so d=2; verify size, roots, divisibility and key-switching block layout without implementing RLWE encryption or running timing benchmarks.

## Exact instantiated arithmetic and independent CRT verification
[EXPERIMENT] Python 3 + sympy script `/mnt/data/iteration50_grafting_sprout_cost_audit.py`, SHA256 `5a0ec05f12585bfca408a711e91406990d8feebf4b1306138ca403430a16ca07`, output `/mnt/data/iteration50_grafting_sprout_cost_results.txt`, SHA256 `e5017a4efc079026138fd8a1fffae5c6914636cdbf08ebb513b1fa1d137a1013`; run + re-run PASS. Real dimension N=32768, required primitive root order 2N=65536.
r1=65537 (prime; near-16bit); r2=1073479681 (prime; near-30bit);
r_top=2305315237189943296 (61-bit).
r_small=2^15*r2=35175782187008 (45-bit).
r_large=r1*r2=70352637853697 (46-bit).
r_small<r_large and ratio r_large/r_small=65537/32768=2.000030517578125.
Both r1 and r2 are 1 modulo 65536. Used exact primitive roots on each prime and CRT to construct root w=20393998829189 mod r_large with w^(65536)=1 and w^(32768)=-1 (mod r_large): direct 46-bit composite negacyclic NTT possible.
For r_small, reduction mod 2^15 rules out 2N-order root (unit-group exponent λ(2^15)=2^13 <2^16). The paper's helper-NTT approach for handling 2^15 requires g>N*2^30=2^45. Pairing this helper with 30bit r2 exceeds one 64bit arithmetic channel, so under the Appendix A.2 representation, **two** word-sized NTT channels for independent sprout polynomial arithmetic; for r_large, **one** composite NTT modulus r1*r2. This is an NTT-representation cost comparison, not a theorem on every possible algorithm or CPU instruction count.
Selected distinct actual 61-bit unit NTT primes:
q0=1152921504608747521,
q1=1152921504614055937,
q2=1152921504615628801.
All prime, 1 modulo 65536, coprime with r_top. Fix ell=3 active unit primes, alpha=2, then d=ceil((3+1)/2)=2 gadget blocks:
  Q0 = r_top * q0,
  Q1 = q1 * q2.
Two actual ciphertext moduli:
  Qsmall=q0*q1*q2*r_small,
  Qlarge=q0*q1*q2*r_large.
Algorithm4 uses SAME intermediate Q_inter=Q0*Q1=q0*q1*q2*r_top in both cases.
The two exact Inv-RS multipliers Q_inter/Qsmall=65537 (r1) versus Q_inter/Qlarge=32768 (2^15) differ, but all active key-switch gadget blocks (2) and inner full Q_inter NTT arithmetic are identical. Thus **NO proof** that total key switching for smaller Q is actually slower. The distinct pre/post modulus-switch conversion pathways may have different costs and error; not analyzed via runtime.

## Research conclusion / important distinctions
[NEGATIVE] "Fewer ciphertext bits ⇒ strictly fewer key-switch gadgets" is false even at relevant ring N=2^15: number of gadgets determined by ell and alpha, not the particular sprout divisor. Both tested ciphertext moduli use d=2. Moreover a smaller sprout may have more standalone 64-bit NTT channels than a larger composite NTT-friendly sprout.
[CRITICAL NON-EQUIVALENCE] Although standalone sprout-product cost is nonmonotonic (2 channels vs 1), Algorithm4 first expands **both** to the same full sprout r_top inside Q_inter. Consequently this pair CANNOT be used to claim an actual larger total key-switching cost for the smaller ciphertext; the gadget inner cost is equal in this fixed model. The earlier intuition of simply transferring the 2-vs1 standalone sprout NTT gap into full KS cost would be wrong.
[PRIOR-ART / NOVELTY] Paper §3.2 explicitly minimizes gadget participation by placing sprout in bottom group, and Appendix A.2 already addresses special non-NTT-friendly power-of-two sprouts and composite NTT. No overlooked correctness error or new speed-up mechanism discovered. High-level modulus bit-size alone is not a sufficient cost metric.
[APPLICATION BOUNDARY] At fixed target rescale ratio, r_large/r_small≈2: choosing the cheaper-to-multiply r_large rather than r_small would change the scale/modulus by about one bit and is NOT automatically within the tight universality approximation or CKKS precision budget. This is an observation only, not an optimizer recommendation.
[OPEN] Full KS conversion costs, NTT transform counts of Inv-RS/RS under varying sprout and security/precision remain unmeasured. For a new contribution, need an admissible near-equal-scale pair with identical security margin but materially different conversion/NTT cost and a proven scheduling algorithm that beats Algorithm3; this study establishes none.

## End of iteration
STATUS: FAIL for strict monotone gadget/NTT cost claim; no paper flaw.
RESULT: N=32768 paper-legal 45bit and 46bit sprouts reverse the standalone one-word NTT expectation, but both are normalized by Algorithm4 to two gadgets and common Q_inter; smaller Q does NOT imply fewer key-switching gadgets and the result does NOT imply total KS slowdown.
NEXT_ACTION: ARCHIVE this negative monotonicity hypothesis. If testing a refined, potentially nontrivial claim next, inspect **Algorithm3's** exact scale-mismatch tolerance (Theorem3.4) for a single fixed target and ask whether any two *both admissible* sprout candidates differ in actual conversion cost; first rule out ±1bit alternatives that violate the error budget. Do not launch general sweeps or implementations without that precise admissibility condition.
STATE_UPDATE: NO (separate parked RIG-HE STATE.md unchanged).
