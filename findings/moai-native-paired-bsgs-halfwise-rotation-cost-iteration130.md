# Iteration 130 — Native paired-diagonal BSGS consumer: exact two-lane semantics and a lower key-switch-count candidate

Date: 2026-10-13. PI authorized I130 by “好的，请继续” after I129. ONE new primary falsifiable hypothesis plus ONE cheapest decisive exact-arithmetic half-lane boundary + BSGS operation-count test. NO CKKS implementation/noise or actual latency measurements. Do not reopen failed unchanged-layout repacking (I127) or misstate I129's direct naive consumer as source BSGS.

## State/source provenance / read before write
- Latest STATE.md I129 read: sha `b85373e8c580c9163e66e0e0d71d164902871c2a`; original I128 note `findings/moai-native-paired-diagonal-producer-consumer-exact-toy-iteration128.md` sha `e42fb8a534f2caebe5d6e8e2b8677f6d2669c708`. I129 source result in `failures/moai-native-paired-consumer-bsgs-key-switch-cost-iteration129.md`.
- Original Linru Zhang et al., *MOAI: Module-Optimizing Architecture for Non-Interactive Secure Transformer Inference*, ICLR 2026, ePrint **2025/991**, https://eprint.iacr.org/2025/991; full 32 physical page Research MCP mirror PDF sha256 `8c694fb9249c4ed4ed2269542c6bef424d7e8a4aa984a7eb2f310b8949b2f1fd`, VERSION_UNVERIFIED. Re-read source §B.1 p18 Eq.(3), Appendix B Algorithm3 p19, **Algorithm4 p20**, Appendix C interleaved batching pp21–22.
- The source Algorithm4 does **BSGS** and pre-rotates individual diagonal ciphertexts across output columns, with baseline BERT parameters m=128,d_v=64 and b=ceil(sqrt m)=12,g=11. Fair *shared pre-rotation* baseline: 8192 Ct×Ct products, 116 pre-diagonal rotations +64*(11 baby+10 giant)=1460 rotations, 9652 aggregate KS if each Ct×Ct relin and rotation counted once. Original paper performance benchmark is 256-input amortized at S=32768 slots, whereas paired layout permits at most B=128 and is considered LOW BATCH B=1 here.

## Exactly ONE primary hypothesis and falsifier
[HYPOTHESIS] The I128 **native two-half duplicated-column / paired-diagonal** layout admits a **BSGS consumer with reusable baby-step and hoisted diagonal rotations**, using correct boundary-safe half-wise rotations, so that at m=128,d_v=64 it **halves Ct×Ct products without increasing TOTAL approximate key-switch count** relative to MOAI's true BSGS Algorithm4. 

[FALSIFIER / CHEAPEST DECISIVE TEST] Derive two-lane BSGS identity with explicit half-wise rotator rather than globally rotating distinct halves, implement its slot-index semantics using exact rational data for two different m=8 matrices and nonlinear row normalization f(x)=1+x², compare entry-by-entry with C·V, and analytically count both rotation and mask operations at m=128,d_v=64 for reasonable group size t. A wrong half-boundary output or ≥9652 aggregate KS for best practical t falsifies the hypothesis. This is ONE composed construction/cost test, not benchmark.

## Definitions, exact BSGS identity

CKKS SIMD slots S=2H. Let m even, L=H/m, and `D(v)=[v|v]` repeated-half input columns, with each half holding m row positions stride L (with B≤L interleaved samples). Let `C_k=[diag_{2k}(C)|diag_{2k+1}(C)]`, the native paired diagonals verified in I128. Each half's content differs, so a standard `Rot_s(C_k)` will generally mix the halves across their boundary.

Define **half-wise rotation** `T_δ([x|y])=[Rot_{δ mod H}x|Rot_{δ mod H}y]`. For `0≤k<H`, let `G_1=Rot_k(C)` and `G_2=Rot_{k−H}(C)` (both ordinary FULL-length cyclic rotations). Define plaintext mask `J_k` as ones on the last k slots of each half, zeros elsewhere. Then
```
  T_k(C)= G_1 + J_k ⊙(G_2 − G_1).
```
This is **TWO ordinary rotations + ONE Ct×Pt mask**, plus additions, for nonzero k; T_0 is identity. Direct integer-slot tests passed for arbitrary distinct half content with S=16,32,256 and offsets 0,1,S/4,H−1. Failing to use this correction invalidates naive whole-ciphertext paired BSGS due half mixing. No assumption that the distinct halves are periodic.

Choose `t` pairs per baby group and `g=ceil((m/2)/t)` giant groups. Let `δ_α=2αtL` and
```
  B_r(v) =
      M0 ⊙ Rot_{2rL} D(v)
    + M1 ⊙ Rot_{(2r+1)L} D(v),
  r=0,...,t−1.
```
Use one-mask identity
```
 B_r(v)= A_r+M1⊙(E_r−A_r),
 A_r=Rot_{2rL}D(v), E_r=Rot_{(2r+1)L}D(v).
```
The baby input requires 2t−1 nontrivial ordinary rotations per output column and t Ct×Pt half masks (some zero shifts are free).

**Native paired BSGS result:**
```
  G(v) = Σ_{α=0}^{g−1} T_{δ_α}(
            Σ_{r : αt+r < m/2}
                T_{−δ_α}(C_{αt+r}) ⊙ B_r(v)
         );
  Y(v) = G(v)+Rot_H(G(v)).
```
At lane level, `T_δ(T_{−δ}C ⊙ B_r)=C ⊙ T_δ B_r`, and `T_δ B_r` yields the even/odd shifted copies of the original v at offsets 2αt+2r and 2αt+2r+1. The last half sum adds contributions from both diagonals and duplicates the true CV column. Only `m/2` encrypted Ct×Ct products per output v, not m.

## ONE EXACT TOY — PASS

Tested in-memory with Python `fractions.Fraction` for all slots (not encoded ciphertexts): 
- m=8,S=32,H=16,L=2,B=2 samples, feature dimension d=3, output d_v=3; source Q,K,V constructed deterministically with two different arrays and many positive/negative entries:
```
Q[r][i][u] = ((i+2)*(u+2)+r+3)%5−2
K[r][i][u] = ((i+3)*(u+3)+2*r+1)%7−3
V[r][i][u] = ((i+1)*(u+3)+r+2)%9−4
```
Set A=QK^T; `C_ij=(1+A_ij²)/Σ_l(1+A_il²)`, *genuinely nonlinear* normalization. Build native pairs C_k in 2 halves for two samples, and compute BSGS with t=2,g=2 with pre-halfrot of C, baby paired shifts, halfrot of each giant partial sum, and final half sum.
- Every row and column in both halves exactly equals dense rational C·V for both samples. First sample output first three rows:
```
[[191/197,263/197,452/197],
 [583/292,-3/2,-77/146],
 [41/34,91/408,563/408]]
```
- Halfwise rotation implemented **via the explicit two-global-rotations/one-mask circuit**, not as an unsupported oracle, and cross-checked against direct half-local circular permutations.
- EXACT PASSES: no boundary mixing, no wrong per-row denominator, no wrong output slot. No real CKKS correctness/security/precision result.

## Count at m=128,d_v=64 (one consumer, no producer)

Let `n_p=m/2=64`. For any t between 1 and n_p, g=ceil(n_p/t):
- hoisted pre-halfrot of pairs from giant groups α>0: n_p−t distinct pairs, each 2 global rotations and 1 mask;
- per output v: `2t−1` baby global rotations, t half masks; `g−1` giant half-wise rotations, **2(g−1)** global rotations and **g−1** masks; 1 global Rot_H to sum the halves;
- `M_PAIR=n_p*d_v=4096`;
- `R_PAIR=2(n_p−t)+d_v((2t−1)+2(g−1)+1) = 2(n_p−t)+d_v(2t+2g−2)`;
- `P_PAIR=(n_p−t)+d_v(t+g−1)`;
- heuristic key-switch count `KS_PAIR=M_PAIR+R_PAIR`, one relinearization and one automorphism KS per respective operation.

For comparison, source baseline (b=12,g0=11):
```
               Ct×Ct     rotations   half masks   KS sum
MOAI Alg4 BSGS   8192       1460          0         9652
I129 direct pair 4096       8192       4096       12288
new pair BSGS
 t=6,g=11        4096       2164       1082        6260
 t=8,g=8         4096       2032       1016        6128
```
We explicitly enumerated integer t choices, 1≤t≤32 and found t=8 lowest crude KS among these, while this is not a claim of *runtime-optimal* t. For t=8, aggregate consumer KS changes **9652→6128**, saving 3524 (~36.51%) despite +572 rotations and +1016 masks. The 4096 Ct×Ct products saved can outweigh added rotations/masks in a homogeneous weighted model if
```
  4096*M > 572*R + 1016*P
  i.e. M > 0.1396484375 R + 0.248046875 P
```
where M=cost of ctct+relin, R=cost of full rotation/KS, P=cost of plaintext-mask multiplication. No actual costs measured. Noise/precision and rescale/scheme compatibility UNKNOWN.

For broader intuition ONLY, original Alg3 producer with d=64 consumes 8192 Ct×Ct, 8128 rotations; native I128 producer consumes 4096 Ct×Ct, 8128 rotations and 4096 masks. MOAI baseline Softmax with 8 squarings per diag and final normalization consumes 1024+128 Ct×Ct; paired 512+64, plus one denominator half rotation. Thus crude attention counts:
```
                       ctct       rotations     extra masks    KS sum
MOAI baseline          17536       9588            0          27124
native pair + BSGS      8768      10161          5112          18929
```
BUT all such totals are schematic: source BSGS may have additional plaintext transforms, native 1/0 masks may consume extra CKKS levels at different points, and the 8-squaring exp model is a **simplification of the reported depth**, not a reprofile of MOAI implementation. Full paper B=256 batch would require 2 waves using native pair layout with capacity B≤128, possibly undoing amortized count benefits; never infer full-batch throughput.

## Prior-art and scientific limitations

[FACT] BSGS diagonal rotation reuse itself is classic HE prior art (also already in MOAI). Two-lane SIMD handling in HE is also established. Related: Dobraunig et al., *PASTA*, section 5.3.2–5.3.3 https://iacr.steepath.eu/2021/731-PastaACaseforHybridHomomorphicEncryption.pdf discusses BSGS plus splitting packed state into two independent halves; mobility HE protocols likewise perform independent per-half BSGS and half-vector summing: https://iacr.steepath.eu/2020/522-PrivatelyConnectingMobilitytoInfectiousDiseasesviaAppliedCryptography.pdf §7.3. Different encryption schemes/semantics and not verified as exact same MOAI Ct×Ct pair mechanism. General 2-half BSGS cannot count as our novelty. Specific native encrypted-diagonal C×V paired grouping novelty NOT VERIFIED.

[OPEN] Extra masks at pre-rotated encrypted C pairs and giant post-product sums may change CKKS scale/level, even if the masks are 0/1; if they each consume an extra level or require rescale, cost advantage can evaporate. Need check scale-one masks and key-switch/noise at exact modulus and decryption precision in smallest possible CKKS implementation before any publishable claim. Also key-storage overhead for `Rot_{δ-H}` offsets not in original eval keys; plus hoisting/relinearization variants may change simple KS count. Full capacity halves throughput at B=256. No GPU runtime test or formal error bound.

## End of iteration
STATUS: **PASS exact two-half BSGS algebra / PASS count-level KS reduction / HUMAN_REVIEW (runtime, noise, novelty unverified)**.
RESULT: Explicit boundary-safe 2-global-rotation+1-mask halfrot allows a hoisted, native paired BSGS consumer. One exact m=8, B=2 nonlinear-normalized test passes. At m=128,d_v=64,t=8 it saves 4096 Ct×Ct products, costs +572 rotations and +1016 masks, and lowers schematic consumer key switches from 9652 to 6128 against source MOAI BSGS. This is NOT an encrypted practical speedup; potential precision/level overhead is decisive.
NEXT_ACTION: PI decides whether to authorize one cheapest **actual CKKS feasibility falsifier** for mask-after-multiply and halfwise rotations under scale/level alignment, first with one pair+two BSGS groups and small CKKS parameters, before GPU benchmarks. If mask-induced extra rescale/level or keys dominate, PARK; if feasible, investigate prior art and implement a scoped MOAI consumer microbenchmark. No automatic expansion.
STATE_UPDATE: YES — novel candidate structural circuit and stricter bounds, unlike I129's unoptimized paired consumer, need record and handoff.
