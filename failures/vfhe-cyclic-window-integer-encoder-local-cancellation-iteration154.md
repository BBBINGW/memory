# Iteration 154 — Fast cyclic-window integer encoding fails source-comparable code distance by adjacent cancellation

**Date:** 2026-10-13. Human PI said “好的，请继续” following I153; interpreted as permission for ONE more concrete candidate under existing P1 vFHE CRT-scalar-index repair, not permission for a direction pivot. This is a new, non-tensor / non-Hadamard candidate; do not extrapolate to all integer codes.

## Read before write and primary source

Read in order `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md`, then `findings/OPEN_RESEARCH_BRANCHES.md`, I153/I152/I151 failure archives, I59/I60 parent findings. Re-read the *Cascudo et al.*, CRYPTO 2025, *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, ePrint 2025/286, **Appendix F.2–F.3, physical pp51–52**, through Research MCP. PDF: 52 pages; GitHub-mirror source `https://github.com/arturo-kong/IACR-eprint-mirror/blob/master/2025/286.pdf`, SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`; **VERSION_UNVERIFIED** vs most recent official ePrint binary; extraction warnings for formulas/layout. Source F.3 supplies direct-sum `[N/2,N/4,N/4+1]` RS blocks when `m≥N/2`, rate1/2, encoded length `2m`, source relative-distance bound `N/(8m)`. Full ideal PIOP I59/60 parent soundness issue is OPEN/HUMAN_REVIEW, no compiled attack established.

## ONE precise primary hypothesis + one decisive falsifier

**[HYPOTHESIS]** Instead of I152/I153 diagonal-sign Hadamard pairs, try a **one-dimensional, non-tensor, systematic cyclic sliding-window parity encoder** over integers:
```
f_L(X)=sum_{j=0}^{L-1} X^j
E_{m,L}(x)=(x(X), f_L(X)*x(X) mod (X^m-1)).
```
Both output halves have length `m`; generator `[I;C_L]` is the same 0/1 integer matrix over every CRT prime. Cyclic moving-window sums can be updated in **O(m)** additions, independent of NTT roots. A one-sparse input has weight `1+L`, superficially matching F.3's RS distance when `L=N/4`. Hope: at `m=N=256,d=4,L=64,beta=2,p=(641,1153)`, candidate should retain **`d_min≥65`** required for source-comparable Brakedown distance.

**[FALSIFIER / MINIMAL TEST]** Find *one* nonzero field message `x` such that the codeword has Hamming weight <65 over either p, without a full code-distance search, implementation/benchmark, PCS redesign or security proof. Check source parameter form and honest no-wrap as a basic precondition, not a second hypothesis.

## Exact source-form parameters and expected baseline

- `N=m=256, d=4, p0=641=2·5·N/d+1, p1=1153=2·9·N/d+1`, with odd `a∈{5,9}`, primes and `N/2=128 | p_i-1`; appropriate `F_(p_i^4)` extension components.
- Source F.3 `tau=m/(N/4)=4` disjoint blocks of `[128,64,65]` RS, so **source total `[512,256]` minimum distance EXACT 65** (direct sum of four MDS blocks).
- Candidate is likewise `[512,256]` with rate1/2, one systematic half and one cyclic window parity half. For honest `beta=2` digits x_i∈{0,1}, parity integers are in `[0,64]`, below `p_min/2=320.5`; all prime components share the same centered/signed integer value. This is toy honest no-wrap only, NOT actual implementation beta/parameter proof.
- A one-sparse message `x=1` has weight `1+64=65` in both primes (calibration, not sufficient to infer minimum distance).

## ONE exact decisive test and explanation

**[DERIVED/EXACT NEGATIVE]** Set the adversarial **field-code message** `x(X)=1-X`. This is nonzero modulo both odd primes and legal as an arbitrary message to the field-linear PCS code. A telescoping identity in `Z[X]` yields
```
    f_L(X)(1-X) = (1+X+...+X^(L-1))(1-X) = 1-X^L.
```
With `L=64<m=256`, cyclic quotient introduces no collision. Thus
```
    E_{256,64}(1-X) = (1-X,1-X^64),
    Hamming weight = 2+2 = 4.
```
The executable uses full exact integer modular convolution and independently verifies the two codeword supports: **positions `[0,1,256,320]`**, values `[1,p-1,1,p-1]` for `p=641,1153`. In particular `d_min(candidate)≤4` versus **65** for source RS. Relative distance `≤4/512=1/128` (vs original exact `65/512`). For ANY family with `1≤L<m` and characteristic ≠2, the same witness gives `d_min(E_{m,L})≤4`, so `δ_min≤2/m→0`; increasing the window width does not rescue high distance.

**[INTERPRETATION]** Unlike I152/I153's sparse Hadamard invariant vectors, the obstruction here is *neighboring-message cancellation* in overlapping integer convolution windows. Good spread for singletons, linear-time encoding, and honest common integer lifts do not imply robust distance against arbitrary malicious field messages. Input `1-X` has a negative coefficient and is generally NOT an honest Boolean digit row; nonetheless Brakedown F.2 demands Hamming distance over arbitrary field-word differences, not only honest rows. This is **not** a forged global CRT proof and **not** a claim that every non-tensor fast integer code is impossible.

## Reproduction, caution, and relevance

Local reproducible test script: `/mnt/data/vfhe_i154_cyclic_window_integer_code_gate.py`; SHA256 `81a5bd8174581e3fe13e7053d288f3562535ee64218975921e3b1e5c465337b0`.

Local stdout: `/mnt/data/vfhe_i154_cyclic_window_integer_code_results.txt`; SHA256 `b64c5783c6e05a00c56d7ca57b05e1a7543216fe6304b52397f64f2b75178890`.

The test is elementary exact modular arithmetic; no full original author's executable benchmark, PCS proof, Fiat–Shamir privacy/cost, 128bit parameters, literature novelty check, or confirmed latest official 2025/286 revision. No author contact / disclosure. A full prior-art search would be required for any positive candidate before claiming novelty; this negative sliding-window identity is elementary, not research contribution.

## End of Iteration 154

**STATUS:** **FAIL** — cyclic sliding-window integer encoder is NOT source-comparable in native field-code minimum distance.
**RESULT:** Its singleton weight65 matches source RS baseline, but adjacent-difference x=1-X gives weight4 over both source-compatible primes; universally dmin≤4 and relative distance≤2/m. Beta2 honest integer no-wrap PASS, but does not rescue code distance. This **closes only this candidate**, while P1 CRT scalar consistency remains OPEN/HUMAN_REVIEW.
**NEXT_ACTION:** **HUMAN_REVIEW** after three distinct cheap encoder families (I152–I154) fail to preserve RS code distance. PI should choose to PARK new integer-encoder search pending a genuinely different constructive coding-theory idea / prior-art identification, or explicitly authorize a new non-local high-distance code architecture with a *credible* source-comparable fast-encoding and bounded-output rationale. Do not generate another nearby tweak, nor change research target autonomously.
**STATE_UPDATE:** **YES** — closes independent cyclic-window code family, records new local-cancellation mechanism and switches current immediate next action to explicit PI decision; no parent-direction pivot.
