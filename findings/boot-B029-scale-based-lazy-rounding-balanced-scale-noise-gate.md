# BOOT-B029 — Lazy scale-based Mat-MGSW external-product rounding: wrap annihilation and balanced-scale noise barrier

TRACK_ID: BOOT
ITERATION: B029
DATE: 2026-10-19
STATUS: FAIL_SAME_MODULUS_LAZY_TWO_STAGE / PASS_NOISELESS_BALANCED_SCALE_REPAIR / FAIL_BALANCED_SCALE_ERROR_GATE / NO_PROVEN_NET_GAIN
STATE_UPDATE: YES

## Primary falsifiable hypothesis
PI-priority1 original BOOT optimization, NOT VFHE/ZK. After B027–B028 orbit-mask dead end, revisit original paper set: 2025/1711 scale-based Mat-MGSW external product, 2025/1892 heterogeneous approximate gadget and 2025/686 amortized/MPmul repeated operations. Proposed substantive new dataflow: combine TWO successive scale-based external products, deferring the first coefficient rounding and temporary return to Q-sized Vec-MLWE ciphertext, thereby amortizing inverse NTT/rounding/forward NTT while retaining the exact native encrypted plaintext semantics, security, noise/DFR and reasonable key modulus. CHEAPEST DECISIVE TEST: exact no-noise scalar projection of the scale-based eigenvector relation, then a repaired staged-scale 2x2 ciphertext matrix with real encrypted random T-masks and small key errors, comparing source stepwise scale and one-end rescale. This is one main construction hypothesis and one repair search with mathematical/numerical falsifiers.

## Primary sources and version caveat
[FACT] Wang–Luo–Xia–Wang–Hou, "Accelerating FHEW-like Bootstrapping via New Configurations of the Underlying Cryptosystems," ePrint 2025/1711, source obtained via research Notes mirror, title verified but VERSION_UNVERIFIED; SHA256 0f003b5e91dfb6acd4bb48103e03127e0da94394544aa24eda1b636676ca57ff, 29 physical pp. Physical p11 §3.1: C∈R_T^((k+r)×(k+r)), input c∈R_T^(k+r) with centered coefficients in [−Q/2,Q/2], EP_C(c)=coefficientwise round((Q/T)*(C*c modT)) modQ and output is AGAIN represented in R_T with centered Q-sized coefficients. p12–14 Lemma3.4 derives E1*c2*(Q/T) and M1*e2, key rounding and output rounding as separate error sources. p15–16 §3.3: one scale EP with rank k+r=m costs m² component-wise products, 2m transforms + m coefficient rounds (under their chosen NTT input/output interfaces); requires T>Δ Q².
[FACT] Hong–Lee ePrint 2025/1892 physical pp11–13 §3.1–3.2, title verified VERSION_UNVERIFIED mirror SHA256 508a5a0b3914e23e8d71198476a50879c471a6f192e6f65bcd68314b89622018: heterogeneous gadget bases and approximate decomposition are noise/runtime/key tradeoff tools; do NOT allow ignoring new noise sources.
[FACT] Guimarães–Pereira ePrint 2025/686 original Algorithm1 MPmul pp11–12 involves multiple CMUX and keyswitch stages; there is no source proof that it can directly accept a lingering T-modulus intermediate of the 2025/1711 representation. TITLE VERIFIED VERSION_UNVERIFIED mirror SHA256 84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335.
[PRIOR ART] Li et al., "Faster Bootstrapping via Modulus Raising and Composite NTT," TCHES 2024(1):563–591 DOI 10.46586/tches.v2024.i1.563-591 uses composite NTT and integrates modulus raising and gadget decomposition inside external product. Reorganizing one EP's modulus/gadget computation is prior art. It does not automatically validate cross-EP delayed rescaling. Other 2026 work includes USENIX Security 2026 BatchBoot and 2026 HPCA Peregrine GPU external-product co-design. No global novelty proof given.

## Exact fatal scalar test (FAIL naive deferred rounding)
Let Q,T positive even with Q|T and Q²|T, T>Q², define α=T/Q. Perfect zero-error selector m=1 in a one-dimensional eigenprojection has C=α; input c=1.
Sequential scale products:
   EP_C(1)=center_Q(round((Q/T)*center_T(α)))=1
   EP_C(EP_C(1))=1.
Naively removing FIRST rescale and multiplying both C's mod T:
   center_T(C² c)=α² modT=(T/Q)²≡0 modT
   so ANY FINAL rescaling of this residue yields0, not1. The normal plaintext disappears even with zero noise, no FFT, no secret key. In fact for any nonzero centered-Q scalar x, two naive C multiplications modT return0 while sequential steps preserve x, provided α*x is represented canonically and α²=0 modT.
Concrete Q16,T4096 (>Q²), α256: sequential input1→1→1; raw C² mod4096=0.
Exact enumeration using arbitrary-precision integer centered mod and nearest rounding:
   Q8,T1024: all 8 centered inputs preserve sequential, naive only zero agrees (7/8 failures for m1=m2=1).
   Q16,T4096: 15/16 nonzero inputs differ (for all binary m1,m2 possibilities 15/64 wrong).
   Q32,T8192: 31/32 nonzero inputs differ (31/128 across binary m1,m2 choices).
This is a NECESSARY algebraic projection of the full scheme, not a ciphertext attack on the author's construction. The Q²|T condition is a broad source-compatible family, not every possible prime modulus.

## Two constructive REPAIR attempts
(A) Lift the TWO unreduced products into larger integer/modular precision: in ideal scalar case use α²x over Z (without modT loss) and final scale by (Q/T)². On all enumerated signed scalar values x and m1,m2∈{0,1} for Q8/16/32, this lifted variant reproduced true sequential behavior exactly (0 errors). But centered no-wrap for |x|<Q/2 requires next modulus T' > 2*(T/Q)²*(Q/2)=T²/Q, not T. For Q16,T4096 it requires T'>1,048,576, smallest power-of-two option 2,097,152 (21 bits vs12, +9 bits) even for pure diagonal zero-error key projections. Real encrypted Mat-MGSW matrix entries contain uniform T-sized masks, so forming full integer C2*C1 before modular projection may require much more precision and reconstructing/sk-tracking secret-dependent wraps. This is NOT a usable actual MLWE ciphertext lifting scheme, no end-to-end FFT/key cost saving demonstrated.
(B) BALANCED-SCALE MATRICES: Instead of using α at each stage, choose α1 α2=α, e.g. α1=α2=√(T/Q) when integral, and do ONE final rescale Q/T. This avoids α²≡0 modT in noiseless scalar case, keeps original modulus T, and is a more creative whole-construction repair. However after first matrix multiply C1*c, ciphertext mask components are close to UNIFORM T, not centered Q. At second multiplication with C2=Mat-MGSW at weaker encoding α2, e2*C1*c is large. With secret row vector sk and ideal key matrices obeying sk*C_i=α_i sk+E_i, exact invariant:
   sk*C2*C1*c = α2α1*(sk*c) + α2 E1*c + E2*(C1*c) (modT).
After final Q/T, term (Q/T) E2*(C1*c) has magnitude ~Q σ_key when C1*c has T-sized random components. In original sequential EP each intermediate is rounded/re-centered to Q-sized coefficients BEFORE feeding it to next EP, so analogous second-stage key error is scaled Q/T * O(Q σ_key) rather than Q σ_key. Thus the intermediate reduction is a NOISE-CONTROL mechanism, not merely a bookkeeping/FFT detail. Heterogeneous approximations from 2025/1892 do not remove this amplification automatically.

## Independent exact reference test of the balanced-scale repair
Use N=1 scalar (one-coefficient projection of ring; no ring-security claim), k=r=1, Q=256, T=2^24=16,777,216; α=T/Q=65,536, balanced α1=α2=256. Secret scalar s=1 (INSECURE illustrative key); secret decryption row sk=(1,−s). Input c=(b,a) with a uniform centered Q and b=center_Q(a+64), so sk*c=64 modQ; target message=64. Each key matrix C with scale α_i is generated using SAME per-trial uniform T-mask bottom row a0,a1 and error e0,e1 independent in {−1,0,1}:
   C = [[a0+α_i+e0, a1−α_i+e1], [a0,a1]] modT.
Then sk*C = α_i*(1,−1)+(e0,e1) (modT), exactly the intended key-eigenvector relation, with key-level error.
Source-like sequential: c0=round_Q((Q/T)*(C1_std*c modT)); c_out=round_Q((Q/T)*(C2_std*c0 modT)).
Balanced: v=C1_balanced*c modT; c_out'=round_Q((Q/T)*(C2_balanced*v modT)).
Noiseless-balanced: use same masks but e0=e1=0 for each key, same balanced algorithm.
For 5000 FIXED-SEED PAIRED trials (identical masks/errors between standard and balanced key pairs within each trial; source random.Random(20261019); all arithmetic exact Python integers and centered modular nearest rounding), measure centered phase error modulo Q from target64:
  Standard stepwise: max abs error1, 0/5000 |err|≥Q/8=32.
  Balanced delayed (with errors ±1): median abs33, max128, 2545/5000 (50.9%) |err|≥32.
  Balanced delayed with key errors0: max abs1, 0/5000 |err|≥32.
This strongly falsifies naive claim that noiseless balanced-scale correctness implies FHE viability. NOT a concrete TFHE DFR, since toy s=1, N1, T/Q, selector/noise distribution, security/precision and parameter choices are intentionally tiny/insecure. Output threshold Q/8 is a chosen illustration, not the exact source message threshold.
[FORMAL REPAIR GATE] To kill E2*C1*c while preserving randomized encryption and all possible inputs, one might seek a structured E2 in the left annihilator of C1 or a key-conditioned correlated error generator. For a generic full-rank C1 over R_T, E2*C1=0 for ALL c forces E2=0, causing a near-noiseless public LWE relation requiring separate security proof; C1's rank and distribution must be analyzed. Sharing masks/errors across keys may recreate B022/23's security problems. No such repair established; brute selecting α2=0 also loses selector. A new scheme preserving short intermediate masks without canonical rescale remains conceivable but demands true new ciphertext type/security machinery. Mark SPECULATION only.

## Whole algorithm cost, security/novelty gates
[CORRECTNESS] The original 2025/1711 output is centered-Q Vec-MLWE after EVERY scale EP; MPmul and 2025/686 CMUX expect this normal input. Naive lazy-round leaves T-sized ciphertext, fails source native type.
[NOISE/DFR] Exact matrix error formula and paired simulation show key error amplification; no complete subgaussian proof or secure estimate for balanced scheme. Any claim of FHE success is false.
[SECURITY] Need legitimate MLWE distributions and key-dependent GSW; toy fixed s=1 is NOT secure. Attempting zero error or secret-conditioned annihilator invalidates ordinary RLWE assumptions unless independently analyzed.
[KEY/COMPLEXITY] Original Mat-MGSW external product §3.3 incurs 2(k+r) transforms plus (k+r)² pointwise products. In theory a full multi-stage fused scheme could save one inverse/forward pair, but naive fusion destroys plaintext; wider modulus/secure intermediate small-mask transforms or GSW-key composition cost must be counted. No native end-to-end gain. Multi-bit precomputed composed selector keys are heavily prior-art-adjacent (multi-bit TFHE, blockbinary, BatchBoot) and may increase eval key size.
[HETEROGENEOUS] 2025/1892 permits per-key base/approximation and tunes key/time/noise; merely choosing different α_i is NOT its established result. No credible parameter selection can ignore the scale-induced E2*v error with v T-sized.
[NOVELTY] Restricted algebraic obstruction is a useful scientific filter, NOT a publication. Modulus raising plus composite NTT is published TCHES24; no novel primitive/protocol or benchmark.
STATUS FAIL_LAZY_ROUND_NATIVE_MOD_T / PASS_BALANCED_EXACT_ZERO_NOISE / FAIL_BALANCED_END_TO_END_NOISE / NO_NEW_BOOT_ALGO.
REPAIR_SEARCH actually done, not just instant topic pivot. Source is from original priority1 family. Multiple B022–B029 attempts exhausted specific key/rounding/mask rearrangements, but broad BOOT goal still active by PI policy.
NEXT_TEST B030: stay within initial BOOT source priority1; seek one truly new structure not another naive "remove rounding": investigate **conditional/precision-aware stage selection** for existing single-level scale-based Mat-MGSW / MPmul, especially whether stage-specific selector reuse, high/low-cost automorphism regions, and actual noise influence justify *per-operation mixed precision* without duplicating evaluation keys. Read 2025/686 FBS1 ℓ_A=1; if this blocks online precision knobs, do not waste another iteration. Apply cost+security+novelty gate, and prepare HUMAN_REVIEW/pivot recommendation if no surviving whole algorithm after systematic repair.
END ITERATION: STATUS FAIL / RESULT corrected via explicit noise counterexample / NEXT_TEST above / STATE_UPDATE YES. BOOT-only.
