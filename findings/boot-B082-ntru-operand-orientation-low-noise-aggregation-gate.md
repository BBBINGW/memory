# BOOT-B082 — Low-noise NTRU group aggregation by reversed operand orientation
Date: 2026-10-20; TRACK_ID BOOT; SHIP paused.
STATUS: PASS_REVERSED_TYPED_PRODUCT_TOY / FAIL_LOW_NOISE_H2_GATE / FAIL_LONG_CHAIN_REVERSE_ORIENTATION / UNCLEAR_SECURE_NATIVE.

## One falsifiable technical hypothesis
In B063–B064 partial NTRU group coalescing before Dai et al.'s NTRU-to-MK-RLWE HProd conversion, replace normalized-left × raw-right gadget product L⊗R by raw-left × normalized-right product R⊗L, keeping normalized output, same k*l/h HProd conversions, same keys and noises. Is final h=2 MK-RLWE accumulator noise no worse than original h=1 (no group merge) while saving approximately half the HProd calls?

## Sources/prior art
Dai et al., Accelerating MKFHE bootstrapping via parallel-friendly NTRU-based blind rotation, Cybersecurity 9:136 (2026), https://link.springer.com/article/10.1186/s42400-026-00563-w, Section improved hybrid product and Lemmas 2–4. Original B064 formula-derived hybrid implementation archived at findings/boot-B064-partial-hybrid-merge-final-noise-gate.md. Pre-existing NTRU CMux/key-unrolling prior art Li et al., Faster NTRU-based Bootstrapping in Less Than 4 ms, TCHES 2024(3). Choosing which ciphertext operand to decompose in an asymmetric gadget product is not per se new cryptography. No new key distribution is proposed.

## Exact ring derivation
In R_Q=Z_Q[X]/(X^N+1), G_j=B^j and exact centered gadget digits h(c), define
 E^L_i=f*L_i−G_i*μ_L,
 E^R_i=f*(R_i−G_i*μ_R).
For O_LR=Ext(L,R), f*O_LR_i−G_i μ_L μ_R =
 μ_R*E^L_i + Σ_j h(L_i)_j*E^R_j.
For O_RL=Ext(R,L), f*O_RL_i−G_i μ_L μ_R =
 μ_L*f^(-1)*E^R_i + Σ_j h(R_i)_j*E^L_j.
Both produce normalized L-type output. Reverse may reduce h(R) coefficient energy vs h(L), but adds f^(-1) convolution error. Repeated reverse merging can compound that term. No distribution-independent noise dominance theorem follows.

## Pair-exact source-formula-derived experiment
Reused B064 toy HProd and full MK-RLWE accumulator phase decryption with isolated local source files; only intra-block group composition direction changes. Ring N8,Q2^28,B16, signed gadget length8, k2, f0=1+X+X², f1=1−X+X², primitive coefficient errors each uniform {-1,0,1}, same sampled original group bit encryptions and correction, CRS, PK and 1 UniEnc per party across both orientations, identical hybrid call order. Each executed reverse product asserts coefficientwise recurrence moduloQ. Explicit zero-noise reverse-product identity 32/32 PASS.
Full four-config check at 10 paired trials each:
(g,l)=(2,2): h1 RMS median2129.50; h2 reversed6011.77; paired median h2rev/h1=3.15, h2rev beat h1 in 1/10.
(2,4): h1 3122.60; h2rev20983.74; paired ratio5.05, wins0/10.
(4,4): h1 6367.06; h2rev65683.16; paired ratio11.04, wins0/10.
(8,4): h1 11055.04; h2rev145354.44; paired ratio11.63, wins0/10.
Original forward h2 median RMS respectively 6907.15, 31261.99, 55648.68, 134137.41, so reverse can beat forward for one configuration yet still loses to h1.
Longer h=4 reverse is dramatically worse than h=4 forward, paired median ratios of order 62x–110x in 10 trials. Some h=4 values may approach torus wrap; no DFR claimed.
Partially completed extended 40-trial run: first 3 config jobs FINISHED, last fourth NOT finished (timeout). Paired h2rev/h1 median ratios: (2,2) 2.855× (wins4/40); (2,4) 6.610× (wins0/40); (4,4) 10.830× (wins0/40). Do not represent these as four completed 40-trial datasets.

## Correctness/noise/security/cost/novelty
PASS exact modular typed product and recurrence; same algebraic product function, no new keys, no extra HProd calls. FAIL h2 final accumulator noise vs h1 in tested default toy cases; reversing is sometimes better than forward h2 but cannot repair original coalescing gate. Noise growth from f^-1 must be accounted for explicitly. No source-native Gaussian security parameters, cryptographic hardness reduction, 128-bit DFR, native HProd, measured runtime, or publication-level novelty established. The original Dai Table4 decomposition specification has separate B065–B066 precision ambiguity and must be checked before security parameter extrapolation. Toy Q/8 observations are NOT real DFR. Distinct primitive proposal absent; direct direction reversal is basic known operation.
Decision: ARCHIVE simple operand reversal. Reuse exact LR/RL error formulas for new primitive screening, but avoid blind parameter scans.

## Next iteration B083 (NOT STARTED)
One decisive novel-interface comparison: inspect Park–van Leeuwen–Zajonc FINALLY ePrint2024/1505 Sec4.4 offline/preprocessable hybrid switching and Dai2026 single-to-multi-key hybrid product. Can an *input-agnostic* encrypted cross-term basis reduce HProd calls without multiplying independent noisy group ciphertexts? Derive one correct typed map, its key transcript and noise recurrence, then check against published offline amortization. Kill if only source-known offline derived keys or precomputing ciphertexts that depend on public LWE input values. If unavailable, pivot to other structural blind-rotation techniques. Do not continue B063/B064 toy sweeping absent an actual secure noise mechanism.
STATE_UPDATE NO (findings/boot-STATE.md is large and unreadable through Notes, preserve original). SHIP paused, no cross-track writes.
LOCAL REPRODUCTION: /mnt/data/BOOT_B082_handoff.zip (full detailed report, exact Python scripts, independent 10-trial JSON and partial 40-trial log, manifest), verified SHA256 5a00621e94f9dc1dc62b0b82f55b40c1eecce935bf16fbb58861a3a6caceee93. Script SHA256 e234a649808d854b9ac0473efdf018b454ef7ef94c2be105b601218373eba19b; full coverage JSON SHA256 7ea3846ddb655f5d9217d4c4f6db177f2373b1201befb4b98ff7b76c6055ce00.
