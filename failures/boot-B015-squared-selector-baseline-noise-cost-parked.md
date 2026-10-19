# BOOT B015 archive — same-shape reduced-T squared selector
TRACK_ID: BOOT
ITERATION: B015
DATE: 2026-10-19
STATUS: PARK_DIRECT_REPLACEMENT / BASELINE_NOISE_FALSIFIED

Source 2025/686 FBS1/FBS2 keys at Q=2^64 are ALREADY approximate one-level GSW (N=2048/8192, beta=2^23/2^22, h=512, original Q/sigma=2^50/2^51). 2025/1711 squared k=r=1 gives the same four transforms/four ring pointwise products, four polynomial key elements, plus Q/T rounding. Any T>Q has strictly larger raw key coefficient bitwidth. Under its sufficient Delta Q²<T, modulus T is at least 129 bits; its basic construction T>Q permits smaller T but does not create an arithmetic-count saving.

For standard independent integer-discrete-Gaussian Mat-MGSW key errors, selector message in top row shifts by r(1,S), r=round(T/Q). With h=512, KL between b=0 and1 shifted Gaussian (conditioned on mask and secret) equals pi r²(1+h)/s², and Pinsker bounds TV by r sqrt(513)/(2sigma_T). At SAME relative noise sigma_T/T as original 686 (2^-50/2^-51), TV<=0.001037 (FBS1) or <=0.002074 (FBS2) for any T>Q. Thus it cannot correctly distinguish/select two otherwise decodable outputs with negligible failure. This is an information-theoretic falsifier for preserving the original relative noise in this explicit Gaussian model; not a proof all smaller-alpha parameters insecure or all squared variants inefficient.

1711 Lemma3.4 key-error proxy Q²(sigma_T/T)sqrt(N) requires approx alpha<=2^-89.73/-89.79 to match the original 686 Appendix B single-CMUX noise budget (one-level GSW noise proxy about 2^43.77/2^44.71). This is a *sufficient proxy*, not a lower bound or DFR; choosing very small alpha changes lattice hardness, so no source 128-bit security estimate transfers. No lattice estimator run or native benchmark. Do not claim insecurity of any untested reduced-T parameters.

DECISION: PARK direct squared Mat-MGSW substitution under current Q,N/CMUX primitive. Reopen only with a genuinely novel lower-cost algorithm, a vetted lattice security and DFR estimate, and a matched runtime/key benchmark. Full proof: findings/boot-B015-reduced-T-statistical-noise-and-cost-gate.md.
NEXT: BOOT B016 — test 2-bit one-hot selector fusion for 2025/686 MPmul using 2023/958 block binary intuition, first exact algebraic interaction/cross-term cost. BOOT isolation only.