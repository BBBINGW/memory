# Iteration 152 — One-coordinate-flip Walsh–Hadamard integer encoder has distance 4, not source-comparable at scale

**Date:** 2026-10-13. Explicit PI authorization to perform the next iteration after the I151 session handoff. **One primary encoder-distance hypothesis + one minimal exact rank test**, with a short algebraic extrapolation of the *same* distance obstruction. No new PCS, security proof, or implementation was attempted.

## Authority, source, and scope

Read, in order, `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md`; then `findings/OPEN_RESEARCH_BRANCHES.md`, `failures/vfhe-original-rs-merkle-column-crt-integer-comparison-iteration151.md`, and I59–60 parent findings. Research MCP verified a cached 52-page ePrint 2025/286, PDF SHA-256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, **VERSION_UNVERIFIED** against current official binary. Re-read original Appendix F.2/F.3, physical pp50–52. F.2 authenticates *columns* of independently row-encoded matrices and F.3 uses native-field RS with source relative-distance lower bound `gamma=N/(8m)` at rate `rho=1/2` in its piecewise setting. Equations in extracted PDF are quality-warned; this iteration's elementary linear algebra is independently calculated.

**Parent question:** can a new *field-independent integer-coefficient* encoder make already-opened F.2 testing Merkle columns comparable across CRT factors without new costly native MLE evaluation-phase vectors, preserving useful code distance, no-wrap and reasonable encoding complexity? I151 ruled out comparing original per-prime RS columns directly, since roots differ.

## ONE primary hypothesis and predeclared falsifier

**[HYPOTHESIS]** With Sylvester Walsh–Hadamard `H4`, `D=diag(1,1,1,-1)`, and `Enc_Z(x)=(H4*x,H4*D*x)`, the induced rate-1/2 linear code over the two source-form base fields F29 and F37 has `d_min>=2` (relative >=1/4) and `beta=2` honest outputs do not wrap. This is the narrow toy necessary-condition gate, not a full repair claim.

**[FALSIFIER]** Find any nonzero input yielding output weight <2, a deficient rank for a larger-than-allowed zero-coordinate subset, or a structural distance obstruction making this single-flip family unusable as a source-comparable high-distance replacement. If so, reject this candidate without building PCS. Predeclared illustrative target was `d_min>=2`.

**[MINIMAL TEST]** Build `8x4` encoding matrix `A=[H4;H4*D]` from the prescribed transform; over p=29 and37 exhaust the 256 subsets of the eight coordinate rows, compute modular ranks, and obtain `d_min=8-max{|Z|:rank(A_Z)<4}`. Check the beta2 coefficient/absolute-sum bound `max_j sum_i|A_{j,i}|<=4<29`.

## Exact experiment

```
 H4 = [[ 1, 1, 1, 1], [ 1,-1, 1,-1],
       [ 1, 1,-1,-1], [ 1,-1,-1, 1]]
 D = diag(1,1,1,-1)
 A = [H4; H4 D]     # eight output coordinates, four message variables

 field    max deficient zero coordinates    d_min    relative distance
 F29                     4                    4             1/2
 F37                     4                    4             1/2
```

**[DERIVED/EXACT]** Every subset of five coordinate rows has rank 4 modulo 29 and modulo 37; a four-coordinate subset `Z=(0,1,4,5)` has rank<4. Witness common signed integer message `x=(-1,0,1,0)` gives `Enc_Z(x)=(0,0,-2,-2, 0,0,-2,-2)`, weight 4, valid over both fields. The program chose modular representatives x=(28,0,1,0) mod29 and x=(36,0,1,0) mod37. Since base-field rank is unchanged by extending scalars, these dmin values also hold over F_(29^4) and F_(37^4).

**[DERIVED/TOY COMPLETENESS]** For honest digits `x_i in {0,1}` (`beta=2`), each coordinate is an integer sum of at most four signed unit coefficients; `|Enc_Z(x)_j|<=4<29` for either prime. Thus the encoder's genuine honest outputs have common signed small integers, unlike original field-root-dependent F.3 RS columns. It meets the *predeclared toy gate*; it does not imply CRT-coherence soundness or full Brakedown correctness.

## Structural distance obstruction discovered within the same distance hypothesis

**[DERIVED — GENERAL EXACT UPPER BOUND]** The toy distance PASS hides a fatal length-scaling obstruction for the *same single-coordinate-sign-flip construction*. Let `m=2^k>=4`, `H_m^T H_m=m I`, `D=I-2 e_m e_m^T`, over any field of odd characteristic. Set `y=H_m x` and `u=H_m e_m` (each `u_i=+-1`). Then
```
 H_m D H_m^{-1} = I -(2/m) u u^T =: T .
 Enc_Z(x) = (y,T y).
```
Choose any distinct coordinate indices i,j and `y=u_i e_i-u_j e_j`. Since `u^T y=1-1=0`, `T y=y`. Hence `Enc_Z(H_m^{-1}y)=(y,y)` has **exactly four** nonzero positions for *every* m>=4: `d_min<=4`, so `delta_min<=4/(2m)=2/m ->0`. This witness is field independent (all odd characteristics; m invertible).

Indeed **d_min=4** for every such m: `T^2=I`; for a weight-1 vector `e_i`, `T e_i=e_i-(2/m)u_i u` has at least `m-1>=3` nonzero coordinates (all off-diagonals `+-2/m`). Thus a nonzero pair `(y,Ty)` cannot have total weight 2 or3: a total weight <=3 would require one vector weight1 and the other weight<=2, contradicting involutivity and the weight-1 image bound. The four-weight witness achieves equality. No large-instance brute force was needed.

**[NEGATIVE — candidate at practical lengths]** Rate stays 1/2, but relative distance is *exactly* `2/m`. For any intended large `m`, this is vanishing, so it cannot simply replace a native constant/meaningful-distance Brakedown code while inheriting the original source's testing-query parameters. In the source Appendix F.3 piecewise regime, its stated conservative `gamma_RS=N/(8m)` exceeds `gamma_H=2/m` by factor `N/16` whenever `N>16`. This is a mathematical comparison of code distances, **not** a benchmark or full security lower bound. To restore strong soundness one would have to change testing-query parameters or code design; no cost advantage is established. The original code and paper have not been attacked.

## Reproduction and caveats

Local exact script: `/mnt/data/vfhe_i152_integer_hadamard_distance_gate.py`, SHA256 `94b917b72632f3ebfa4913bac44abd86a3c1f5f4742a378a296a2bf95a20a323`.
Local stdout: `/mnt/data/vfhe_i152_integer_hadamard_distance_results.txt`, SHA256 `5080c6c0fdc9f216f65370deddb5d89fd64a5f516d99f52e3cbe481313939908`.
The script's exact test is only the `m=4` finite-field subset ranks and beta2 no-wrap bound; the m-general obstruction above is an **independent written derivation** rather than a numerical exhaustive test. Local artifacts are not committed to Git. Paper ePrint revision remains VERSION_UNVERIFIED. No native PCS proof, Fiat–Shamir/VC privacy proof, 128bit soundness claim, broad benchmark, novelty claim or author contact.

## End of Iteration 152

**STATUS:** **FAIL for the candidate as a scalable source-comparable high-distance encoder**; **PASS** for the expressly predeclared `[8,4,d_min>=2]` toy/no-wrap gate. Parent vFHE problem remains **OPEN/HUMAN_REVIEW**.
**RESULT:** Exact ranks show dmin4 at F29 and F37 and honest beta2 no-wrap. More decisively, the very same family has exact dmin4 for *all* m>=4, hence relative distance2/m→0; a lone signed Hadamard replica with single-coordinate flip is not a viable unmodified Brakedown high-distance replacement at scale.
**NEXT_ACTION:** **HUMAN PI DECISION:** choose whether to keep P1 open and explicitly authorize a *different* concrete fast field-independent bounded-integer code candidate with demonstrably nonvanishing/source-comparable distance, or park this line. Do **not** recycle this single-flip construction or start a different research branch autonomously.
**STATE_UPDATE:** **YES** — I152 completed and a meaningful family-level negative result should be recorded, without changing the active research direction.
