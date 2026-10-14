# vFHE V37 COMPANION — Segev 2025 ZK R1CS* prefix-rank/hidden quotient arithmetic and source CRS incompatibility

**Date 2026-10-15. COMPANION to AUTHORITATIVE parallel V37** `findings/vfhe-v37-bulletproofs-circuit-scalar-vs-indexed-vector-commitment-gate.md`; NOT a second V37, NOT V38. Main V37 found stock Bulletproofs §5 scalar committed-input API cannot accept Yang indexed subvector directly; identified original Bulletproofs++ ePrint2022/510 §5 as V38 candidate. Preserve V38 NEXT, I192 GLOBAL FROZEN.

## ONE falsifiable hypothesis H-V37C [FAIL unmodified splice; PASS explicit hidden integer R1CS algebra]

Can original Gil Segev **2025/327** zero-knowledge R1CS* relation be inserted UNMODIFIED over the very SAME Yang 2024/827 prechallenge Pedersen-subvector commitment to prove **hidden** canonical-lift native F.2 integer sums/quotients with no extra prefix opening, CRS compatibility, public-ONE anchoring or substantive prover costs? **NO**. We independently constructed an exact circuit and exposed its positive prefix-rank sublemma as well as two source/semantic blockers.

## Sources [FACT]
- Gil Segev, *Bulletproofs for R1CS: Bridging the Completeness-Soundness Gap and a ZK Extension*, Communications in Cryptology 2025 / ePrint2025/327 https://eprint.iacr.org/2025/327; Research MCP complete **31 physical pages**, PDF SHA256 `029c913fbd6b4f9e1146b9ccdad4e2c0f5b5af860645cc2272603970cd0331c6`, VERSION_UNVERIFIED. Source §3 physical pp7–8 gives R_R1CS* relation: commitment T to prefix x, auxiliary deviations x',y', constraints Az◦Bz=Cz, Az'◦Bz'=0, mixed constraints, AND `A_prefix*x'=B_prefix*x'=C_prefix*x'=0`. Source p8 explicitly advises additional AoK if strict original prefix commitment relation needed (mentions Attema/Cramer logarithmic AoK). Source Theorem4.1 pp9–10: perfect completeness, perfect special honest-verifier ZK and computational witness-extended emulation for its EXACT relaxed relation, assuming `2(n+m)+2` uniformly independently sampled group generators and DL hardness. Proof body `(2log2(n+m)+3) group +3 scalar`. This theorem is NOT about arbitrary mixed CRS/proof compositions.
- Yang et al., *Multivariate Multi-Polynomial Commitment and its Applications*, ePrint2024/827 https://eprint.iacr.org/2024/827, Research MCP inspected **40pp** SHA256 `ae0baa1357ef38a40e8203b291162818a423a157940cc182264a22d954ae887e`, VERSION_UNVERIFIED; Fig5 physical p18 uses STRUCTURED indexed generator array `g_i=g^(alpha^(i−1))`, Section4 pp19–22 single Pedersen-subvector commitment `C_a=h^rho prod g_i^(a_i)` and zero-knowledge aggregated digit range proof. NOT the independently uniform generator distribution of the cited Segev theorem: security theorem cannot just be transplanted to SAME Yang CRS (not evidence Yang's paper broken).
- Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO2025/ePrint2025/286 https://eprint.iacr.org/2025/286, Research MCP inspected **52pp** SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, VERSION_UNVERIFIED vs official Feb2026; §3.1 p10 CRT p_i field extension shape, §4.3 pp20–24 digit scalar table, Appendix F.1/F.2 pp50–51 Merkle/RS original PUBLIC authentic y. Proposed third-field circuit is OUR add-on, no source security-flaw claim.

## Exact R1CS construction [DERIVATION]

BEFORE verifier native extension challenges, knowledge-commit same integer digit vector `a=(a_b)` in a prefix vector commitment C_a (under a secure generator family). AFTER original native F.2 accepts same public y, compute canonical coordinate coefficients `c_(i,t,b)=lift_[0,p_i−1](chi_b(u_i)_t)`. For β=4 use 2 bits b0,b1/digit and impose:
1. `a_j * ONE = b0_j+2*b1_j`;
2. `b*(b−ONE)=0` for 2H digit bits and each quotient bit;
3. `(sum_j c_(i,t,j) a_j − lift(y_(i,t))*ONE − p_i sum_s 2^s kbit_(i,t,s))*ONE =0` for every D=L*d native coordinate.
Here ONE **MUST BE PUBLICLY FIXED/BOUND TO 1**, not an arbitrary witness scalar. All integer S and quotients k remain private; only the original F.2 verified y are public. Bounds: β4,H2^24 imply quotient k<3H<2^26; with group scalar prime r ≈2^252 and p_i≈2^48, BOTH sides of exact relation are nonnegative <2^75<r, so equality mod r implies equality over integers. A separate proof must bind original C_a prefix opening to THIS exact circuit witness and to range; this note does NOT construct the complete secure argument or FS composition.

**Positive R1CS* observation:** For H digit reconstruction rows, their A-block on a's prefix is EXACT identity I_H, so rank(A_prefix)=H and Segev R_R1CS* condition `A_prefix*x'=0` forces **x'=0**. This is *not* the same as proving ALL other relaxed auxiliary y'=0 or CRS-independent extraction; the theorem still targets its actual relation, with additional AoK if desired.

**Decisive flaw in improperly anchored constant wire [EXPERIMENT]:** Without separate ONE=1 public constraint, witness sets ONE=0,a=0,all digit bits=0,kbits=0; then ALL multiplication constraints above pass even if native verifier actually authenticates incompatible y13=1 and y29=0 at Boolean index0. With proper ONE=1, simple equality row at y13=1 gives −1≠0 in F1009 and rejects. This defeats OUR intentionally incomplete R1CS compiler, not published Segev or any standard correctly anchored R1CS.

## ONE fully executable finite-field exact relation gate [EXPERIMENT]

Source-form N4,d2,p13=1+4*3,p29=1+4*7,ellstar3,H8,beta4, native fields K13=F13[T]/(T²−5), K29=F29[U]/(U²−12), both irreducible. Same challenge components (2+w,3+2w,4+3w), honest a=(0,1,2,3,0,1,2,3). Actual lifted S/y/k:
```
(p,t)    S   y   k
(13,0)   47  8   3
(13,1)   96  5   7
(29,0)  124  8   4
(29,1)   92  5   3
```
Exact R1CS over INSECURE toy field F1009: 45 variables (8 digits+16 digit bits+4×5 quotient bits+ONE), 48 constraints (8 digit reconstruction+36 bitness+4 integer eq), **48/48** satisfied honestly with ONE=1. A_prefix rank exactly8. Source CRT conflicting h13=1,h29=0 at Boolean challenge index0 cannot be represented by common a0∈{0,1,2,3}; all choices rejected. If naively ONE=0, zero-wire witness passes the entire *incorrectly anchored* circuit; anchoring ONE=1 makes integer equation fail (residue 1008 in F1009). Deterministic script executed twice identically. This is NOT execution of Segev argument prover/verifier or actual native F.2 PCS, no 128bit claim.

## Source-shape symbolic complexity [NOT BENCHMARK]

For H=2^24,L2,d4,D8, quotient 26 bits per coord:
- n=3H+8×26+1=50,331,857 witness scalar wires;
- m=3H+8×26+8=50,331,864 multiply/equality rows;
- n+m=100,663,721; direct Segev power-of-two padding to 2^27=134,217,728;
- Thm4.1 idealized proof BODY `(2*27+3) G +3 scalar` = **60 objects/1,920 bytes** at assumed 32B encodings, EXCLUDING prefix PoK, original native F.2, Fiat–Shamir, setup and other protocols.
- Independent prover/verification generator arrays G/H each length padded n+m imply **8 GiB** if naïvely resident as 32B group points; generator streaming may trade RAM for work; real secure implementation not benchmarked.
- D*H=134,217,728 dense canonical-lift public coefficient terms by direct method; V32 companion already falsified naive multiplicative factorization of their external canonical lifts. No general algorithmic or communication lower bound claimed.
- Critically cannot claim identical `Yang indexed SRS` satisfies Segev theorem's independent-generator assumptions. A completely separate random-generator C and Segev R1CS proof could express range internally but is not Yang's original optimized range proof and still very large.

## Verdict / future
**STATUS:** FAIL free drop-in same-CRS Yang+Segev secure 128bit succinct full vFHE repair; PASS exact hidden-quotient R1CS arithmetic and full-rank digit-prefix observation; HUMAN_REVIEW missing secure prefix PoK, ZK composition, structured-vs-independent CRS reduction, actual prover/PCS cost, official Feb2026 source PDF.
**NEXT_ACTION:** MAIN V37 already recorded next V38: independently audit actual published **Bulletproofs++ 2022/510 vector-committed inputs and ZK circuit** and its compatible prechallenge vector basis, native-y canonical quotient checks, true work cost. Alternative HUMAN_REVIEW/pivot. No author outreach or unsafe source edits.
**STATE_UPDATE:** companion only, authoritative main V37 COMPLETED / V38 NEXT; general I192 FROZEN.

**Local files:** report `/mnt/data/VFHE_V37_Segev_ZK_R1CS_Prefix_Rank_CRT_Gate_2026_10_15.md` SHA256 `b62b216d58679574a84261a4398a28bbc653df290a40669e6a7fe6f6ad64f344`; script `/mnt/data/vfhe_v37_segev_prefix_r1cs_gate.py` SHA256 `be223044f007b8ddd8b7af28f70237e2e47b09ca34abd5a8b82b06940dc2f46d`; JSON `/mnt/data/vfhe_v37_segev_r1cs_prefix_gate_results.json` SHA256 `47423f35fc3e629b5398dd17eb4f7776bc6ed71a302cff40c0bb6c66f8dee65a`.
