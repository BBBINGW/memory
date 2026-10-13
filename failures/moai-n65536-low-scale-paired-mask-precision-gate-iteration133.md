# Iteration 133 — MOAI-sized CKKS reduced-scale boundary mask does not meet a conservative 0.01 maximum-error gate

Date: 2026-10-13. PI explicitly authorized I133, one primary hypothesis, one deterministic full-ring canonical-encoder/paired-BSGS output falsifier. NO actual SEAL/Phantom encrypted operation, no public disclosure, and no proof of universal infeasibility or real BERT accuracy loss.

## Research context and primary sources
Read latest `STATE.md` after I132 (Git blob SHA `6c764e62aba84815097b4f04c46b032b09038809`), plus `failures/moai-preproduct-giant-mask-push-fixed-chain-scale-gate-iteration132.md` and I131. Original MOAI: *MOAI: Module-Optimizing Architecture for Non-Interactive Secure Transformer Inference*, ePrint **2025/991**, ICLR 2026, https://eprint.iacr.org/2025/991. MCP full original PDF 32 physical pages, GitHub ePrint mirror SHA256 `8c694fb9249c4ed4ed2269542c6bef424d7e8a4aa984a7eb2f310b8949b2f1fd`, VERSION_UNVERIFIED. §6 / physical p11 specifies `N=2^16`, CKKS `S=N/2=32768` slots, `Δ=2^46` and SEAL CPU backend. Appendix G.3 physical p31 reports **median absolute layer output error 0.01–0.03**, NOT a formal per-gadget worst-case error requirement. The BSGS comparator remains Appendix B Eq.(3) p18 / Algorithm 4 p20. Microsoft SEAL official coeff modulus user-prime max 60 bits and CKKS scale multiplication/rescale apply as already documented in I132.

## ONE hypothesis / cheap decisive test
[HYPOTHESIS] Under the I132 push-mask one-rescale budget `q≈Δ·Δ_M`, restricting scale to `Δ_M=2^κ` with `κ≤14` at full `N=65536` provides a sufficiently precise half-boundary selector for a **conservative auxiliary 0.01 maximum absolute error budget** in the output of a single low-batch paired-BSGS `C V` (with `|V_i|≤1`, positive row-normalized `C`) and thus preserves a plausible error margin at the unchanged main scale `Δ=2^46`. The 0.01 target is a RESEARCHER-CHOSEN local screening budget, NOT attributed to MOAI's theorems/experiments.

[FALSIFIER / SINGLE TEST] Implement the complete N65536 cyclotomic CKKS canonical embedding, inverse FFT to polynomial coefficients, multiply by mask scale, nearest-integer coefficient rounding, and decode; use the resulting decoded approximate plaintext masks **for every giant group of I132's exact m128,t8,g8 paired-BSGS formula**. Compare `C V` with exact dense plaintext `C@V`. Exhibit one attention score `QK^T/√64` realizable with 64 feature dimensions, `|V_i|≤1`, for which max output error at the most generous κ=14 exceeds 0.01. This is ONE combined encoder-to-output falsifier, not separate studies.

## Canonical embedding procedure

Let `N=65536`, `S=32768`, `H=16384`, `L=H/m=128`; `ζ=exp(πi/N)`. Standard CKKS slots correspond to primitive 2N-th roots `ζ^{5^j mod 2N}` for `0≤j<S`, other roots are their conjugates. For real mask slot values M_j, form N complex evaluation values `y_t` at odd roots exponent 2t+1 and fill conjugate pairs:
```
 y[( (5**j mod 2N) - 1)//2 ] = M_j
 y[( (2N - (5**j mod 2N)) - 1)//2 ] = M_j.
```
The real ring coefficients `p_k` are computed from `p_k = (FFT(y)_k/N) exp(-π i k/N)`, then rounded `c_k=round(2^κ Re(p_k))` (nearest integer). The decoded target-order mask is obtained from `IFFT(c_k exp(πik/N)) N/2^κ` evaluated at the selected primitive slots. Numerical accuracy of this inverse/forward FFT construction was cross-checked by exactly reproducing I131's N16/k2/J-mask error values at scales 1,16,256,4096,65536. This is an **ideal canonical-coefficient encoder simulation**; it is not a compiled SEAL implementation and different rounding/precision methods may alter results.

I132's giant-specific selector P_α with `a=2048α`, α=0,…,7 has ones on first a slots of the lower half and last H−a slots of upper half, zero elsewhere. The mask computed at each α is from the full 32768-slot binary P_α. For all eight α the observed mask-error norms coincide (they are related by cyclic structure/Galois automorphisms in this arrangement); the table below is one representative.

### Ideal mask encoder error (full 32768 slots)
```
κ / mask scale     global max |err|   global RMS |err|   max on 256 B=1 active row slots
10 / 2^10           0.21214050        0.05219511             0.14600136
12 / 2^12           0.05042098        0.01280115             0.03216683
14 / 2^14           0.01444360        0.00317027             0.00900300
16 / 2^16           0.00345432        0.00079675             0.00216095
```
κ=16 is **OUTSIDE** I132's one ≤60-bit prime budget, since `46+16=62` bits; diagnostic only. For κ=14, q≈2^60 is at the absolute largest SEAL prime-bit boundary, leaving essentially no headroom, and in any case requires **changing** the original ~46-bit prime chain.

## Full paired-BSGS output stress test

Choose `m=128,B=1,d_v=1,t=g=8`, a single encrypted V column `V_i=(-1)^i∈[-1,1]`. D(V)=[V|V] in native duplicated-half sparse-row format, with active slots iL in both halves.

Choose a positive row-stochastic C with:
- row 0: `C_00=0.99`, `C_0j=0.01/127` for j≠0;
- all other rows: uniform `C_ij=1/128`.

**Crucial rank feasibility cross-check:** C is exactly the row-wise softmax of a **rank-one** attention logit matrix A having `A_00=log(0.99·127/0.01)≈9.43930694` and other A entries zero. Such A is feasible as `QK^T/√64`: Q_0 has first coordinate 8·9.4393, K_0 first coordinate1, every other Q/K coordinate zero, so `rank(A)=1≤d_k=64`. Thus the counterexample does **not** require impossible full-rank 128×128 logits. It is an intentionally concentrated stress input, NOT measured BERT activations.

Form C paired upper diagonals directly. For every α,r, compute exact cyclic `A_r=Rot_{2rL}(D(V))`, `E_r=Rot_{(2r+1)L}(D(V))`. Use **decoded approximate** CKKS P_α in the I132 pre-masked baby `A_r+Ptilde_α⊙(E_r−A_r)`; pre-rotate each paired C by `Rot_{-a}`, do elementwise products/sum, global giant `Rot_a`, final `G+Rot_H(G)`. No ciphertext encryption or other error sources. This is the entire consumer, not just isolated single-mask error.

Validation first using **exact binary P_α masks**: max output error at B1 active slots `3.33×10^-16` (FP64 rounding), PASS intended algebra.

Using encoded approximate masks:
```
κ             first-row absolute error    max row absolute error   RMS over 128 rows
12                0.02471190                 0.02471190               0.00218424
13                0.01878853                 0.01878853               0.00166069
14                0.01782452                 0.01782452               0.00157548
15                0.00478041                 0.00478041               0.00042253
16                0.00265849                 0.00265849               0.00023498
```
At κ14 the true row0 output is `0.9899212598425201`; approximate output is `1.0077457820161797`, error `0.01782452217>0.01`. κ15 and κ16 are diagnostic only: they require ~61/62-bit q and therefore cannot be a direct single-prime SEAL 60-bit remedy at Δ=2^46. This result is before encryption noise, key switching or rescale error.

Separate *stronger but rank-unverified* stress case C_ii=0.99 for every i and C_ij=0.01/127 else, V alternating, produced κ14 max error 0.01782452 and RMS 0.00596627, but generally requires rank128 logits; the principal falsifier above is the legitimate **rank-one** case with same max error and RMS 0.00157548.

**[NEGATIVE]** The most generous one-prime mask κ14 fails the chosen 0.01 max-absolute-output screening budget on a valid rank-one 64-feature attention-score instance. This strongly weakens the idea that the simple low-bit mask push is an *obviously safe* practical option. **DO NOT INFER:** (a) all CKKS optimized encoders/noise-aware scale schedules must fail; (b) actual MOAI BERT/GLUE task accuracy worsens by a specific amount; (c) 0.01 is an author-required max error; (d) the actual code was tested; (e) 0.01444 mask error automatically means all CV inputs have 0.01444 error (propagation depends on data).

## Technical and decision consequences

- κ14 needs a roughly **60-bit** prime replacing MOAI's original ~46-bit rescale prime; the 60-bit SEAL bit limit leaves no headroom. κ≤13 leaves room but generally increases canonical encoding error.
- I132 pushed-mask BSGS requires **4096 masks** for m128,d_v64 vs I130 original 1016; even if error were acceptable, they have nonzero runtime, keys, rounding and scale consequences.
- Since I126–132 already involved multiple source-standard SIMD/BSGS and CKKS scale mechanisms, and the most direct available reduced-mask workaround fails a conservative error stress gate, RECOMMEND **PARK MOAI I126–133** to avoid endless non-novel mask/scale iterations. A restart would need a clearly nontrivial mechanism (e.g. alternative exact/pseudocyclotomic lane selector with error proof, or empirically justified level-free CKKS encoding) plus genuine prior-art value, or a real precise application tolerance/profile. PI retains final decision.
- A concrete future performance claim would require N=65536 compiled SEAL/Phantom encrypted operations, actual CHAIN selection/security check, error over task distribution, and comparison to source original end-to-end B=256 throughput as well as low-batch latency. NONE done here.

## End of iteration
STATUS: **FAIL reduced-scale low-batch 0.01 precision-screening hypothesis / PASS full-N canonical-encoder and rank-one score falsifier / HUMAN_REVIEW**.
RESULT: For valid rank-one 128×128 attention scores with d_k64 and V alternating ±1, N65536 Δ2^46 κ14 packed-boundary mask introduces `0.01782452` maximum CV output error solely from plaintext encoding, exceeding a **chosen** 0.01 single-stage precision screen. κ16 reduces error but needs >60-bit one-prime rescale. This does NOT prove universal CKKS infeasibility or practical model accuracy failure.
NEXT_ACTION: PI to decide whether to PARK MOAI I126–133 and delegate another higher-upside FHE target; recommended PARK. Avoid recycling other parked branches or restating source folklore. I134 NOT STARTED.
STATE_UPDATE: YES — settles I132's remaining natural reduced-mask parameter window for the stated precision-screening target and source-dimension sample.
