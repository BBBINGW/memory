# Iteration 128 — Native two-half paired-diagonal producer–Softmax–consumer: exact plaintext composition without standalone stride conversion

Date: 2026-10-13. PI authorized I128 after I127. ONE primary hypothesis with ONE small exact-algebra toy verification, as specified by STATE.md. No actual ciphertext evaluation, actual CKKS noise/precision/cost measurement, or novelty claim. Distinct from FAILED I127 attempt to insert a formatter between *unchanged* MOAI Algorithms 3/4.

## Primary source and research context

Linru Zhang, Xiangning Wang, Jun Jie Sim et al., *MOAI: Module-Optimizing Architecture for Non-Interactive Secure Transformer Inference*, ICLR 2026; the algebra in this note is pinned to IACR ePrint **2025/991**, https://eprint.iacr.org/2025/991, Research MCP original PDF 32 physical pages, SHA256 `8c694fb9249c4ed4ed2269542c6bef424d7e8a4aa984a7eb2f310b8949b2f1fd`, latest official version `VERSION_UNVERIFIED`. §3.1 physical pp5–6: column/diagonal encodings; §3.2 pp6–7: interleaved row rotation, Lemma 3.2; §4 Algorithm 1 pp8–9: diagonal Softmax; Appendix B Algorithm 3 physical p19, Algorithm 4 p20: original col×col→diag and diag×col→col; Appendix F Algorithm 9 p29: bootstrap denominator. Original Algorithm 4 uses **BSGS baby/giant rotations**, NOT the simple naive formula used as a counting comparison below.

Prior notes read first: `findings/moai-paired-diagonal-low-batch-softmax-tradeoff-iteration126.md`; `failures/moai-interleaved-to-half-pair-conversion-cost-iteration127.md`; `STATE.md` was I127_CLOSED, no active hypothesis.

## ONE falsifiable hypothesis / test

[HYPOTHESIS] If the client *natively encodes all column ciphertexts with duplicate data in two half-rings*, then a separately defined paired-diagonal Algorithm-3 producer and Algorithm-4 consumer can compute
`(Q,K,V) → QK^T → row-wise polynomial-normalized C → CV` with **m/2 packed diagonal ciphertexts** and **m/2 ciphertext products per inner column** on BOTH matrix multiplication stages, while preserving duplicate-column format on output and **WITHOUT independent m-way stride-permutation conversion from I127**. This claim is a functional and ciphertext-product-count statement under a changed native layout, **NOT** a low-latency statement against BSGS.

[FALSIFIER / CHEAPEST TEST] Implement exact slot arithmetic for **m=4, S=16, two different batches B=2, feature dimension d=2, output d_v=2**, and check all outputs entrywise against exact plaintext `f(QK^T) / row_sum f(QK^T)` times V with genuinely nonlinear **f(x)=1+x+x²**, using rational fractions. An inter-half boundary collision, mixed row denominator, or incorrect CV would kill the proposal. Explicitly record ciphertext-product and mask/rotation counts against unoptimized standalone-diagonal reference.

## Native layout and derivation

Let `S` denote CKKS SIMD slots, `H=S/2`, `m` even, `L=H/m`, and `1≤B≤L`. Define `D(v)=[v|v]`, a length-S ciphertext plaintext embedding where each half contains the **same** length-H, row-stride L, B-batch interleaving of a column vector `v`: active sample index r for matrix row i lies at iL+r in first half and H+iL+r in second. This is the **native client/input format** and is closed under columnwise linear combinations for plain-weight Q,K,V and next-layer FC layers; we DO NOT start from the old MOAI S/m row-stride output and shift it.

Let `M_0=[1^H|0^H]`, `M_1=[0^H|1^H]`; `Rot_u` is cyclic left rotation by u slots. Because D(v) repeats across halves, `Rot_{jL}D(v)=D(Rot_{jL}v)` rotates each matrix's rows cyclically within both halves. In particular it is essential NOT to replace D(v) with staggered different halves *before* rotations; doing so would cause boundary crossovers.

**Native paired col×col producer** (modified MOAI Lemma 3.1 / Algorithm 3), pair j=2k:
```
P_k = Σ_{i=0}^{d−1}
       D(q_i) ⊙ [ M_0 ⊙ Rot_{2kL}(D(k_i))
                + M_1 ⊙ Rot_{(2k+1)L}(D(k_i)) ].
```
In low half of P_k: `Diag_{2k}(QK^T)`; in high half: `Diag_{2k+1}(QK^T)`; ONE ciphertext–ciphertext multiply per (k,i), plus two branch plaintext masks.

**Native paired Softmax:** for any slotwise positive map f (e.g. exp polynomial), compute `W_k=f(P_k)`; `U=Σ_k W_k`; `Z=U+Rot_H(U)=[Z_rows|Z_rows]`. Reciprocal Z once, output `C_k=W_k⊙Z^{-1}`, containing two correctly normalized diagonals. One half rotation. Same depth as original per pair before masks/noise. Actual CKKS approximate inverse, denominator bootstrapping and f errors NOT tested.

**Native paired diag×col consumer** (modified MOAI Algorithm 4, NO BSGS yet):
```
R_{k,j}= M_0 ⊙ Rot_{2kL}(D(v_j)) +
         M_1 ⊙ Rot_{(2k+1)L}(D(v_j));
G_j = Σ_{k=0}^{m/2−1} C_k ⊙ R_{k,j};
Y_j = G_j + Rot_H(G_j).
```
Then `Y_j = D((CV)_{:,j})`, a duplicate-half column ciphertext directly consumable by another plaintext linear layer or next attention block. One half-rotation per output column. Both paired boundaries avoid I127's expensive m-way row stride-permutation and unpacking.

## One exact nonlinear toy

Parameters `m=4,S=16,B=2,L=2,d=2,d_v=2`.
```
Q[0] = [[1,0],[0,1],[1,1],[2,1]]
K[0] = [[1,2],[2,1],[1,0],[0,1]]
V[0] = [[1,2],[3,4],[5,6],[7,8]]

Q[1] = [[0,2],[1,1],[2,0],[1,3]]
K[1] = [[2,0],[0,1],[1,2],[2,1]]
V[1] = [[2,5],[1,2],[4,3],[3,1]]
```
For every sample, row and pair:
1. `P_k` halves exactly match corresponding upper diagonals `Diag_{2k}` and `Diag_{2k+1}` of `A=QK^T`: PASS.
2. With **f(x)=1+x+x²**, row denominator `Z` for samples 0 and 1 is respectively [14,32,36,50] and [14,62,36,108]; both half lanes match exactly: PASS.
3. `Y=G+Rot_H G` matches each component of exact rational `(f(A)/row_sum f(A))·V` in both output halves: PASS.
   Sample0 expected 4×2:
   `[[23/7,30/7],[3,4],[11/4,15/4],[85/31,116/31]]`.
   Sample1:
   `[[19/6,89/36],[3,31/12],[67/25,149/50],[29/9,263/108]]`.
All comparisons executed on exact in-memory arrays with Python `fractions.Fraction`, one combined end-to-end toy test. No encrypted code and no claim of CKKS feasibility/security from plaintext exactness.

## Cost scope, prior art and next falsifier

For toy `m=4,d=d_v=2` comparing **non-BSGS direct** reference formulas:
- Col×col ciphertext products: original `m d=8`, native `m d/2=4`.
- Diag×col ciphertext products: original `m d_v=8`, native `m d_v/2=4`.
- Final normalization ct products: original m=4, native m/2=2. Polynomial f circuits evaluated for 4 instead of 2 ciphertexts.
- Thus core ct×ct calls (excluding internal f) `20→10` for this toy.
- The two matrix products each introduce `m d` or `m d_v` ciphertext×plaintext masks (two masks per paired rotation), i.e. 8 + 8 = **16 masks** here. These are **not free** and may consume levels / introduce noise.
- Global rotations needed to prepare per-feature offsets in this direct algorithm can remain comparable to a **naive** m-diagonal implementation, but consumer also requires `d_v` half-rotations and Softmax one. This does NOT establish improvement over MOAI's existing **BSGS Algorithm 4**, whose V/diagonal rotation count is `O(√m)` rather than this direct pairing's `O(m)` per output. At `m=128,d_v=64`, naïvely replacing BSGS could increase automorphism key switches dramatically.
- The original published MOAI full batch has B=256 at m=128, whereas native paired capacity `B≤S/(2m)=128`; NO full-batch throughput gain.
- End-to-end latency, actual encrypted CKKS precision/scale/rescale/bootstrapping, evaluation-key storage, masks' cost, and whether a BSGS-compatible paired consumer can be derived are ALL UNRESOLVED.
- SIMD two-lane packing and half-sum are known techniques, not inherently novel: e.g. 2022 PoPETs paper on private mobility (https://petsymposium.org/popets/2022/popets-2022-0132.pdf §6.2) exploits independent BFV lanes and combines their outputs; MOAI itself already has SIMD interleaving. Not a direct prior-art match for this exact CKKS paired end-to-end circuit established here. `NOVELTY NOT VERIFIED`.

## Iteration end

STATUS: **PASS exact native pipeline correctness / UNCLEAR practicality and novelty / HUMAN_REVIEW**.
RESULT: One explicit native duplicated-column → paired diagonal → normalized paired diagonal → duplicated-column construction is correct for two m=4 inputs with nonlinear f and halves ciphertext–ciphertext product call counts *against unoptimized formulas*. It escapes the particular I127 standalone stride-conversion bottleneck by changing the initial/client column representation. It does NOT prove overall faster than MOAI's BSGS baseline or full-batch results.
NEXT_ACTION: PI authorizes ONE decisive **BSGS-vs-paired cost falsifier** for I129 (or pivots): compare MOAI Appendix B Algorithm 4 `m=128,d_v=64` BSGS key-switch counts and rescale/key/noise cost with the direct paired consumer, including `m d_v` plaintext masks and final half-sums. If BSGS makes saving uneconomic, PARK; if promising, test BSGS-compatible paired consumer next. Do not start implementation before this gate.
STATE_UPDATE: YES (I127's open 'native producer/consumer' hypothesis resolved at algebraic level; preserve distinction from cheap inserted converter).
