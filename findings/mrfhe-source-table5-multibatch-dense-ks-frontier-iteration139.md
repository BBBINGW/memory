# Iteration 139 — MRFHE source Table 5: joint Y-packing still amortizes fully dense KS2 in FHE(8,5), but only conditionally

Date: **2026-10-13**. PI authorized I139 by “好的，请继续” following I138. Only ONE primary hypothesis + ONE minimal source-parameter arithmetic falsifier. User PI decides whether further implementation is warranted.

## Read-before-write and original source

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` last I138 (SHA `cd7ad9c4d94ea7ec1c47b5d1facf570297c85ee9`), `findings/OPEN_RESEARCH_BRANCHES.md`; recovered MRFHE prior I31 through I35: `failures/mrfhe-unbalanced-radix-uniform-amortization.md`, `findings/mrfhe-aux-ring-cross-batch-coefficient-packing.md`, `failures/mrfhe-joint-packing-noise-isolation.md`, `findings/mrfhe-joint-packing-lifted-ks-noise.md`, `failures/mrfhe-joint-packing-second-switch-sparsity.md`, and `failures/mrfhe-waxis-subring-projection.md`. Do NOT reopen zero cross-batch noise, second-switch sparse Y support, or W-independent secret.

Original FULL PDF: Cheon, Hong, Kang, Kim, Kim, Lee and Lee, *MRFHE: Mixed-Radix Fully Homomorphic Encryption with Better Batch Bootstrapping*, IACR ePrint **2026/853**, https://eprint.iacr.org/2026/853. Source obtained from user's **ChatGPT Library** file `2026-853.pdf`, 18 physical pp and previously recorded size 844699 bytes, not ePrint MCP (previously retrieval-blocked). Current iteration directly read physical **pp9–12,16,18** using Files. §5.1 p9 defines auxiliary `S^(omega)=Z[omega][W,Y,U]/(W^d−omega,Y^d−omega,U^(2n1)+1)` with `d=n2/2`. §5.2 p10 Algorithm 1 gives `star → Switch(s*→s) → d circledast [PPMM] → Switch(s*→s) → Rescale`; p10 Prop5.7 guarantees desired D2' plaintext Y-coefficient-wise operation. §5.2 p11 Algorithm2 has two auxiliary PCMMs per block; p11 Cost Analysis charges **3×n1 + 4×(n2/2)×ceil(2n1/n2)** base-switch-equivalent work per ONE source batch of n1 ciphertexts under rank-linear switching cost. §6.3 p12 states Table4 batch results are for *aligned* parameter shapes, not FHE(8,5). Table5 physical p18 lists source FHE(8,4)-D, FHE(10,3)-D, FHE(9,4)-S/D and FHE(8,5); FHE(8,5) has N=62208, logPQ=1658, h=31104, sparse temporary h=32 and dnum=5. Existing 128-bit security claim is for their original tested parameter model, NOT automatically proven for larger total ciphertext sample count or this proposed multi-batch flow.

## ONE falsifiable hypothesis / one decisive test

[HYPOTHESIS] Even after **fully charging both dense auxiliary PCMM key switches**, there exists at least one actual source Table5 mixed-radix parameter set with **K=2 or K=3 full original same-secret S^(i) batches fitting one S^(omega) Y block** and a **>=1.5× strict improvement** in per-original-ciphertext ring-rank-linear KS-equivalent work over processing these K original batches separately. This is an *operation-count/parameter-regime* hypothesis only; it does not imply noise/precision/runtime gains.

[FALSIFIER/ONE TEST] Enumerate actual Table5 parameter shapes (w2,w3) from source, compute exactly using integer and Python `Fraction` arithmetic `n1=2^(w2-2)`, `d=3^w3=n2/2`, `L_K=ceil(Kn1/d)`, and
```
cost cohort(K)=3 K n1 + 4 d L_K  [in R^(i)-switch equivalents]
C_K=cost cohort(K)/(K n1)
gain_K=C_1/C_K.
```
If no source parameter has K2 or K3 with L_K=1 and gain≥1.5, kill this avenue. This generalizes I32's toy-only K1..4 arithmetic and I31's K1 cost, **without** repeating I35's support test or claiming noise cancellation. Algorithm 1's full second switching is inside 4dL_K for all K.

## Exact source-parameter sweep results

```
Table5 shape      n1    d    L1   C1        C2        C3          gain2       gain3
FHE(8,4)-D          64    81    1   8.0625    8.0625    8.0625      1.000       1.000
FHE(10,3)-D        256    27   10   7.21875   7.0078125 7.078125    1.0301      1.0199
FHE(9,4)-S/D       128    81    2   8.0625    8.0625    7.21875     1.000       1.1169
FHE(8,5)            64   243    1  18.1875   10.59375  8.0625      1.71681     2.25581
```
`K3` at FHE(9,4) uses L3=5 (not a single block); the small benefit reflects removing a ceiling gap, not packing three whole original batches into one auxiliary ciphertext. The only source Table5 shape **meeting the HYPOTHESIS** is **FHE(8,5)**.

FHE(8,5) precise block/cost analysis:
- `n1=64`, `d=n2/2=3^5=243`, n2=486, N=2n1 n2=62208.
- K1: 64 original ciphertexts, `L1=ceil(64/243)=1`, `cost_cohort=3*64+4*243=1164`; `C1=1164/64=291/16=18.1875`.
- K2: 128 original ciphertexts, `L2=1`, `cost_cohort=3*128+4*243=1356`; `C2=339/32=10.59375`, independent K1 baseline cohort 2328. **Avoided 972** base-ring switch equivalents across 128 outputs, `gain=2328/1356=194/113≈1.71681`.
- K3: 192 original ciphertexts, `L3=1`, `cost_cohort=3*192+4*243=1548`; `C3=129/16=8.0625`, independent K1 baseline cohort 3492. **Avoided 1944** base-ring switch equivalents across 192 outputs, `gain=3492/1548=97/43≈2.25581`.
- K4: 256 input ciphertexts, `L4=ceil(256/243)=2`, cost cohort `3*256+4*243*2=2712`, `C4=339/32=10.59375`; worse than K3 even though batch size increases. Nonmonotone packing frontier and precise **1-block viable K∈{1,2,3}**.

## NEW cost gate (explicit missing work) and limits

Compared with K separate one-batch right-W stages, joining K cohorts saves exactly `4d(K−L_K)` base R-switch equivalents if each original cohort needed L1=1. In source FHE(8,5), with K2 or K3 L_K=1:
```
 saved_K=4d(K−1) (KS_equiv in R^(i))
    K=2: saved=972;  per-input spare margin 972/(128)=7.59375 R^(i) KS-equiv
    K=3: saved=1944; per-input spare margin 1944/(192)=10.125 R^(i) KS-equiv.
```
If joint re-packing/conversion, added slot traffic, memory transfer, precision maintenance, and any extra modulus/key operations (after subtracting independent-case conversion cost) exceed this saving under the *same calibrated cost units*, the entire expected gain disappears. The equivalence cost `3Kn1+4dL_K` already counts BOTH full-size dense auxiliary PCMM switches: I35 found KS2 input **dense at K1 AND K2**; DO NOT discount KS2 via Y sparse structure. The saving comes only from **higher utilization of an already-full auxiliary ring for additional same-key S^(i) source batches**, not lower total noise.

Crucial scope limits:
1. **PASS is only symbolic cost and ring capacity.** I32 exact plaintext noninterference, I33 cross-batch error mixing and I35 dense second-switch obstruction remain unchanged. No lifted full-PCMM CKKS noise, rescale, security or actual Lattigo latency. K2/K3 can lose all benefit by increasing modulus/precision or memory-bandwidth cost.
2. I32 already derived the general formula and toy predicted savings. This iteration **does not invent a new algorithm**; it locates one source Table5 regime **not measured as a batch case in Table4** and sets a precise incremental overhead budget. Not independent publishable novelty; substantial overlap with source MRFHE/CKL batch-matrix literature.
3. Entire original parameter Table5 FHE(8,5) setup ring is large; auxiliary rank `d·N=243*62208=15116544` vs original `N=62208`. Even fixed-switch-count processing is very expensive in absolute bytes/key size. Original Table4 does not report FHE(8,5) batch benchmark; cannot claim original 128-bit security survives extra source ciphertext count or that reported performance extrapolates to K2/3.
4. Source proof text for Table5 is from Library parsed PDF, NOT independently visually checked original typeset table. Named parameter values were legible and cross-checked against I31 source audit.
5. No need to re-test whether second-switch Y support is sparse; I35 already killed that hypothesis. Rather, next true gate must look at **K1 versus K2 extra noise after TWO key switches and actual D2' PPMM**, not K1/K2 support counts, using source-compatible scale/rescale and key distributions.

## End

STATUS: **PASS actual-source FHE(8,5) conditional >=1.5× dense-KS-equivalent amortization window / HUMAN_REVIEW overall FHE feasibility and contribution**.
RESULT: Enumerating source Table5 gives one exact source parameter shape FHE(8,5), for which independent full n1=64-batches K2,K3 fit one d243 auxiliary Y block and ideal KS-equivalent gain factors 194/113≈1.7168 and 97/43≈2.2558, **without a sparse second-switch assumption**. Fixed overall Ct switch count and target switching-key/noise model remain untested. Extra conversion/packing overhead must stay below 972 (K2) / 1944 (K3) base-ring KS equivalents per cohort for theoretical gain.
NEXT_ACTION: I140 only after PI authorizes: ONE source-parameter FHE(8,5) noise/precision falsifier for K1 vs K2 **through entire auxiliary PCMM: 1st KS → actual d′2 PPMM → 2nd KS → rescale**, with common full secret/keys and an honest equivalent source baseline. Define output precision/accumulated noise and q/levels before any GPU experiments; kill if K2 needs unacceptably larger modulus/security or erases >972 KS-unit headroom. If unavailable, register missing *implementation/source parameters* rather than claim speedup; PI may PARK MRFHE as low novelty.
STATE_UPDATE: YES — materially refines reopened MRFHE window to FHE(8,5) K2/3 with exact break-even and clear next gate; preserve earlier failure archives.
