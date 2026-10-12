# Iteration 129 — Direct native paired MOAI consumer loses BSGS key-switch advantage; full-pipeline latency still OPEN

Date: 2026-10-13 (user timezone Asia/Tokyo). PI explicitly authorized I129 through “好的，请继续”. ONE primary cost hypothesis and ONE decisive operation-count comparison at paper-realistic m=128,d_v=64, low batch B=1. Do not restart I127 converted layout, nor call a count inequality an actual CKKS benchmark.

## Read before write / primary source

- Latest `STATE.md` read, checkpoint I128 sha `26f4b6048b71c0268274aa1d60dce142d6280ecb`. Read `findings/moai-native-paired-diagonal-producer-consumer-exact-toy-iteration128.md` SHA `e42fb8a534f2caebe5d6e8e2b8677f6d2669c708` before analysis.
- Linru Zhang et al., *MOAI: Module-Optimizing Architecture for Non-Interactive Secure Transformer Inference*, ICLR 2026, IACR ePrint 2025/991, https://eprint.iacr.org/2025/991; verified prior 32-page original via Research MCP fixed GitHub mirror PDF SHA256 `8c694fb9249c4ed4ed2269542c6bef424d7e8a4aa984a7eb2f310b8949b2f1fd`, VERSION_UNVERIFIED. Re-read Appendix B §B.1 Eq.(3) physical p18, Algorithm 3 p19, **Algorithm 4 p20**, Appendix C §C.2 pp21–22, paper §5 p10 and §6.1 p11.
- Original Algorithm 4 uses BSGS and shares pre-rotations of diagonal ciphertexts across output columns. The direct I128 paired consumer did **not** use BSGS; a comparison against a naive non-BSGS baseline is misleading.
- Original BERT ring N=2^16, S=N/2=32768 slots, m=128, and full published batch 256; present analysis B=1 fits I128's half-duplicated S/2/m=128 input capacity, and does not preserve published batch throughput.

## ONE hypothesis and falsifier

[HYPOTHESIS] At m=128,d_v=64, I128 **direct** native half-paired Algorithm-4 consumer enjoys a plausible efficiency advantage over the actual MOAI BSGS Algorithm 4 **without a major increase in automorphism key switches**, when accounting for the cost of masked preparation of even/odd V-row rotations.

[FALSIFIER / ONE TEST] Derive source-anchored exact rotation and ciphertext product counts for the **best straightforward hoisted BSGS** baseline and direct paired consumer; optimize the pair-masking algebra (avoid counting two masks where one suffices), compare key-switch counts and derive a weighted latency break-even inequality. Check algebra with one toy two-half replicated vector, and compute integer counts analytically. No encrypted benchmark or security test.

## Operation counts for the consumer C·V

Let b=ceil sqrt(m)=12, g=ceil(m/b)=11, and d_v=64.

**Original MOAI BSGS**, Appendix B Eq.(3)/Algorithm 4:
```
 Y_j = Σ_{α=0}^{g−1} Rot_{αb}( Σ_{r: αb+r<m}
                  Rot_{−αb}(c_{αb+r}) ⊙ Rot_r(v_j) ).
```
Precompute and share `Rot_{−αb}(c_{αb+r})` across all j for α>0: `128−12=116` nontrivial rotations (the α=0 group needs no rotation; last group has 8 live members). For EACH of 64 encrypted output columns: baby `b−1=11` nonzero rotations of V_j and giant `g−1=10` rotations of intermediate sums, totalling 21. Thus total `R_BSGS=116+64*21=1460`. Ordinary products `M_BSGS=m*d_v=8192`. Masks needed solely to select halves `P_BSGS=0`.

**I128 direct native paired consumer:**
```
 D(v)=[v|v], H=S/2, L=H/m;
 A_k = Rot_{2kL}(D(v_j)), B_k = Rot_{(2k+1)L}(D(v_j));
 R_k = M0⊙A_k + M1⊙B_k;
 G_j = Σ_{k=0}^{m/2−1} C_k⊙R_k;
 Y_j = G_j+Rot_H(G_j).
```
For each column, the m distinct row offsets are used: identity for k=0 even (0), remaining `m−1=127` global rotations. One half-swap `Rot_H` per output column. Hence `R_PAIR=d_v*(m−1+1)=64*128=8192`. Ct×Ct products `M_PAIR=d_v*(m/2)=4096`.

**Important mask optimization:** because `M0+M1=1`, use
```
  R_k = A_k + M1⊙(B_k−A_k),
```
so EXACTLY ONE half-mask plaintext multiplication per pair and output col, not two. Verify with integer slot arrays and independently varying two half lanes; result is `[A_k.low | B_k.high]`. Total `P_PAIR=(m/2)*d_v=4096` Ct×Pt masks, not 8192 in the original unoptimized I128 formula. This masks-per-pair shortcut is elementary prior art/algebra and NOT a novel contribution; mask CKKS encoding/levels/noise not verified.

**Consumer summary**:
```
             MOAI BSGS   paired direct    delta
Ct×Ct         8192          4096          −4096
rotations     1460          8192          +6732
half masks       0          4096          +4096
key switches  9652         12288          +2636
```
Key-switch accounting assumes one relin per Ct×Ct multiplication and one automorphism key-switch per rotation. This is a conventional simple count, **NOT** a proof of exact library runtime; lazy relinearization/hoisting could change cost. Single-rot Softmax denominator is distinct, adds +1 paired rotation and +1 KS across the pipeline, so if comparing consumer PLUS I128 normalization gate the rotation delta is +6733 and KS delta +2637.

[NEGATIVE] Primary HYPOTHESIS FAILS as a key-switch-count claim: consumer's total KS count **increases 2636/9652=27.31%** vs source BSGS. No reduction in BSGS rotations was actually achieved by the direct paired design.

## Weighted break-even, no premature runtime claims

Set M = time of one relevant ciphertext×ciphertext multiplication including relin, R = time of one relevant automorphism rotation including key switch, P = time of one half-select plaintext mask multiplication (plus its necessary rescale when applicable). Assuming homogeneous costs only as a toy:
```
T_PAIR(C·V) < T_BSGS(C·V)
 iff 4096*M > 6732*R + 4096*P
 iff M > 1.6435546875*R + P.
```
Including the new half-rotation for Softmax denominator gives coefficient `6733/4096 ≈ 1.64380`. No actual M/R/P ratios have been benchmarked at the same CKKS level, modulus, batching and GPU environment. Thus **cannot logically assert paired direct is slower by wall time** even though consumer KS count grows.

Crucial *whole pipeline caveat*: preceding original Algorithm 3 at d=64 has 8192 Ct×Ct products and 8128 rotations, while native paired producer has 4096 Ct×Ct products and same 8128 rotations plus **4096 one-mask Ct×Pt ops**. Plaintext masks on producer also use the `A+M1(B−A)` algebra; only in the native duplicated-half layout. For producer+consumer combined, paired reductions in products are 8192 but additional rotations only 6732 (plus softmax+1), and additional masks 8192 (one per pair per feature/output). Including Softmax with an 8-square exponent model, baseline total Ct×Ct products `8192+8192+1024+128=17536`; paired `4096+4096+512+64=8768`; baseline rotations `8128+1460=9588`; paired `8128+8192+1=16321`; additional half masks `4096+4096=8192`. Therefore the pair pipeline may even reduce crude **total key-switch count** from `17536+9588=27124` to `8768+16321=25089`, despite worsening the standalone consumer. Mask cost, stages/levels and published batch capacity could dominate. NEVER claim the entire native I128 pipeline has been falsified.

## Hard boundary, novelty assessment

- The decisive negative is restricted to the **unoptimized direct native paired consumer vs original *actual* hoisted BSGS** at m=128,dv=64, for key-switch count and needed weighted cost.
- Masks may consume multiplicative depth, scale or increase rounding error; whether scale-one masks are accurate and rescale-free in an actual CKKS implementation is unproven. Any extra level can change minimum ciphertext modulus and change all cost ratios.
- One-half duplicated slots reduce max batch from 256 to 128 for m=128,S=32768. At the paper's full batch size, the ideal algebraic per-wave 2× Ct×Ct savings are offset by at least two waves, with extra masks/rotations. No improvement to the paper's published B=256 throughput is established.
- A **native paired BSGS** consumer, potentially hoisting rotated paired diagonals and avoiding m mask-dependent V row shifts, is an entirely different, OPEN construction and has not been proved possible or quantified here. Do not re-run simple duplication demos as a next iteration. Native pairing of adjacent diagonals and the one-mask algebra may have standard SIMD prior art; **NOVELTY NOT VERIFIED**.
- This note neither challenges MOAI's correctness nor asserts a universal impossibility or experimentally confirmed failure.

## End of iteration
STATUS: **FAIL consumer key-switch advantage / PASS original-BSGS operation-count falsifier / HUMAN_REVIEW**.
RESULT: Direct native paired C·V: −4096 Ct×Ct but +6732 rotations, +4096 masks, +2636 aggregate key switches vs MOAI BSGS. Full attention chain not killed by this standalone consumer comparison; actual speed/noise/novelty unresolved.
NEXT_ACTION: PI choice for I130: (A) authorize ONE new structural hypothesis deriving a **BSGS-compatible paired consumer** with shared baby/giant rotations and an m=4 or m=8 exact correctness/cost falsifier, testing whether extra masks still dominate, OR (B) PARK MOAI I126–129 and choose a fresh matrix-FHE target. No encrypted implementation before an improved key-switch/mask frontier passes.
STATE_UPDATE: YES, I129 closes the direct paired-consumer key-switch-efficiency claim, materially refines I128 scope, and archives a negative cost result.
