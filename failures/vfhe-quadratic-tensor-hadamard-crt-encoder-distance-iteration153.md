# Iteration 153 — Quadratic/tensor-sign Hadamard pair has low-weight codewords despite many flipped coordinates

**Date:** 2026-10-13. Human PI said “好的，请继续” immediately after I152, interpreted narrowly as permission to continue the same P1 vFHE encoder-distance investigation with ONE genuinely different candidate. No research pivot, PCS redesign, full theorem attack, or author contact.

## Read-before-write / provenance

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md`, archived I152 failure, I151 original-native-RS failure, and prior I59–60 parent findings (from context). Re-read primary Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes* (CRYPTO 2025; ePrint 2025/286), Appendix F.2/F.3 **physical pp51–52** using Research MCP, cached 52-physical-page GitHub-mirror PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, **VERSION_UNVERIFIED**. F.2 authenticates row-encoded matrix columns via Merkle leaves. F.3 uses block RS encoding `[N/2,N/4,N/4+1]`, rate 1/2, code length `2m`, with relative-distance lower bound `N/(8m)` in the piecewise regime. PDF extraction marks formula/reading order caution; parameters and symbolic ranks below were checked by integer arithmetic independently.

## ONE primary hypothesis and ONE predeclared falsifier

**[HYPOTHESIS]** A genuinely multi-coordinate, field-independent, fast integer-coefficient dual-Hadamard encoder with **quadratic sign pattern** 
`Enc_m(x)=(H_m x, H_m D_m x)`, `m=4^t`, `H_m=H_4^{⊗t}`, `D_m=D_4^{⊗t}`, `D_4=diag(1,1,1,-1)`, may avoid I152's one-flip rank-one obstruction and achieve source-comparable **minimum Hamming distance** at the same [2m,m] rate, with integer output no-wrap for honest digits.

**[FALSIFIER / ONE TEST]** At the source-form instance `N=m=256,d=4`, primes `p0=641,p1=1153`, `beta=2`, show just ONE nonzero codeword of weight < the source F.3 piecewise-RS distance **65**. If found, kill this candidate as a drop-in Brakedown code-distance replacement **before** PCS/security/cost investigation. This is a rank/weight witness test, not a full exhaustive minimum-distance calculation.

## EXACT construction and source-compatible parameters

- `p0=641=2·5·256/4+1` and `p1=1153=2·9·256/4+1`; both are primes, the `a` parameters 5 and 9 odd, both `p_i-1` divisible by `N/2=128`. The source components may be `F_(641^4)`, `F_(1153^4)`; a base-field codeword is valid over each extension.
- Candidate `[M,k]=[512,256]` rate 1/2. `D_4^{⊗4}` contains **120 negative and 136 positive** signs among its diagonal entries, so this is distinct from I152's one-flip D. Two Fast Walsh–Hadamard transforms cost `O(m log m)` ring/field additions (not a measured wall-clock improvement).
- For honest `x_i∈{0,1}`, every unmodded code coordinate is a **common integer** with `|c_j|≤m(beta-1)=256<p_min/2=320.5`. This ensures unique centered/signed lifts at these two primes, hence no honest signed-lift wrap in this **toy** regime. No claim for actual 49-bit benchmark digit ranges.

## One explicit low-weight witness

Use Sylvester `H_4` and `D_4=diag(1,1,1,-1)`; let `T_4=H_4 D_4 H_4^{-1}=I-(1/2)uu^T` with `u=H_4 e_4=(1,-1,-1,1)^T`. For `y_4=(1,1,0,0)^T`, `u^Ty_4=0`, so `T_4 y_4=y_4`.

For `m=4^t`, `T_m:=H_mD_mH_m^{-1}=T_4^{⊗t}`; set `y=y_4^{⊗t}`, and `x=H_m^{-1}y` (nonzero, valid over both odd-prime fields since `m` invertible). Then
```
 H_m x = y,
 H_m D_m x = T_m y = y,
 wt(Enc_m(x)) = wt(y)+wt(y) = 2·2^t = 2√m.
```
At `t=4,m=256`, this is a **nonzero length-512 codeword of exact weight 32** in both `F641` and `F1153`, hence `d_min(candidate)≤32` and relative distance `≤1/16`. No need to compute the exact candidate minimum distance. For arbitrary `t≥1`, `δ_min≤1/√m→0`; this is an explicit tensor-supported obstruction for this *particular* sign-pattern family, **not** for arbitrary diagonal D or all integer fast codes.

**[SOURCE COMPARISON]** Appendix F.3 with `N=m=256` uses `τ=m/(N/4)=4` independent RS blocks, each `[128,64,65]` over an appropriate native field. Thus the direct-sum encoder has total `[512,256]` and **exact minimum distance 65**, relative `65/512>1/8`. Candidate has the same dimension and output length but `d_min≤32<65`; it cannot preserve source code distance or source testing-query bound by unchanged parameters.

**[SCOPE CAUTION]** `x=H_m^{-1}y` is an arbitrary *field message*, generally NOT a Boolean vector/difference of honest digit vectors. However F.2 Brakedown PCS requires the underlying field-linear code's minimum distance against arbitrary malicious field words. Therefore this directly refutes **source-equivalent code distance**; it does NOT exhibit an illegal digit accepted by a completed proposed CRT repair, compromise the original PCS, or prove the parent I59–60 source soundness issue has any compiled end-to-end exploit.

## Reproducibility

Local exact executable: `/mnt/data/vfhe_i153_quadratic_tensor_hadamard_distance_gate.py` SHA256 `7fe3be33d0f423c533221aa9fa1d5d8eb20705bd211b3103a1f5a65a6b02cef0`.

Local stdout: `/mnt/data/vfhe_i153_quadratic_tensor_hadamard_distance_results.txt` SHA256 `8ba6b5d9f177d898e1704bddb320b01c5363397cf0a440333b2a01fa20055388`.

Script verifies prime/source parameter form, both finite-field fast Walsh transforms with `x=H_m^{-1}y`, exact weight 32 in both primes, centered honest no-wrap, and the RS block comparison. No random trials, precision approximations, actual evaluated Merkle proof, benchmarking, or novelty claims.

## End of Iteration 153

**STATUS:** **FAIL (quadratic/tensor-sign dual-Hadamard candidate as source-comparable PCS encoder)**.
**RESULT:** A D with 120 sign flips and near-linear integer fast transforms still has an exact `(y,y)` low-weight codeword (weight32 at m256) versus source RS distance65. A tensor-product obstruction yields `δ_min≤1/√m`. Toy signed honest no-wrap PASS. Existing source RS prime-dependence issue and vFHE global CRT scalar-index consistency remain **OPEN/HUMAN_REVIEW**; no fix, attack, or publishable result established.
**NEXT_ACTION:** **HUMAN PI DECISION REQUIRED**: park the field-independent-int-encoder repair path after two failed explicit Hadamard candidates, OR authorize a clearly **nonseparable / non-tensor** different fast integer ECC with a predeclared source-comparable minimum-distance test. Avoid another nearby sign-diagonal/Hadamard variant; do not start new P1 candidate or pivot autonomously.
**STATE_UPDATE:** **YES** — a distinct multi-flip tensor fast-encoder family has a rigorous low-weight obstruction, materially refining P1's encoder architecture boundary.
