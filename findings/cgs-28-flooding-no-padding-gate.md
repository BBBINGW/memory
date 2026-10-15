# CGS-28 — Stronger independent server flooding instead of prestored conditional Gaussian

Date: 2026-10-15. Root STATE.md single active research task. Prior CGS-27 parked the structured NG secret detour. One hypothesis and one decisive statistical test. **Status: PASS statistical lemma; UNCLEAR complete source-level security and costs.**

## Hypothesis

Maintain original Okada–Takagi standard LWE/MLWE secret distribution and one-output Shamir PartDec. Set session Gaussian padding zeta=0 and increase the independent ServerDec flooding E until it hides **the full secret-dependent randomized-rounding disturbance** W, not just evaluation noise. This may trade O(LDec) persistent storage for larger flooding and modulus; it is based on **known** Gaussian smudging, not a claimed new primitive.

## Primary original sources

Okada–Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025, ePrint 2025/409, https://eprint.iacr.org/2025/409, cached 40pp mirror PDF SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301, version unverified. §5 Algorithm3 physical p19 ServerDec samples E independently from discrete Gaussian on half-integers; Lemma5.1 pp20–21 Eq(13)–(18) explicitly includes r^T s + E; Theorem5.5 pp24–25 needs publicly known norm to simulate this residual. §6 Algorithm6 p26 prepads norm-dependent Gaussian for every sid, Theorem6.3 p28 simulates. §7 Algorithm7 p29, Lemma7.1 p30–31 cover ring/MLWE. Algorithm5 p23 adversarial decryption oracle reveals ALL active partial shares, not just plaintext. Existing independent server noncollusion assumed.

Published prior art: Micciancio, *On the Hardness of Learning with Errors with Binary Secrets*, Theory of Computing 2018, https://www.theoryofcomputing.org/articles/v014a013/ already uses fixed-length +/-1 norm; thus a binary-secret known-norm proposal is no new work and scalar Algorithm3 is already unpadded. Known flooding and better bounds: https://github.com/openfheorg/openfhe-development/blob/main/src/pke/examples/CKKS_NOISE_FLOODING.md and Dai/Wu/Feng, IET Information Security 2025 DOI 10.1049/ise2/7550044.

## ONE decisive exact theorem and conditional source bound

Let E follow D_(hZ,sigma), density proportional to exp(-pi x^2/sigma^2), h>0, and tau∈hZ. Then
`TV(E+tau,E) <= min(1,abs(tau)/sigma)`.
PROOF: symmetric unimodal pmf shifted by h has TV exactly its largest point mass 1/Z. Telescoping over abs(tau)/h lattice steps gives TV <= abs(tau)/(h Z). Poisson summation yields Z >= sigma/h, proving the bound.

For independent fresh E and pre-existing shift W∈hZ, if Pr(abs(W)>M)<=delta, joint distribution of (W,E+W) vs (W,E) has TV <=delta+M/sigma. With d independent flooding coordinates and coordinatewise shift bounded by M except delta, TV <=delta+d M/sigma. The bound holds conditionally on public/secret prior state that does not include E, so it can be applied sequentially to adaptive sessions when each E is fresh.

From source scalar Eq(17), W=r^T s - {Q/2}mu + e_eval + e_fresh. If |s_i|<=B, |e_eval|,|e_fresh|<B_eval, and Gaussian-rounded r has max coordinate <=R except probability delta_r, then M_LWE = n B R + 2B_eval + 1/2. Conservative fresh flood target: sigma_flood >=2^(kappa+2) M_LWE, alongside ALL prior source requirements.

For rank-k MLWE in ring dimension n, bound a coefficient of sum_i r_i s_i by k n B R, so M_MLWE=k n B R+2B_eval+1/2. For independent coefficientwise Server flooding, sigma_flood >=2^(kappa+2) n M_MLWE suffices to hide the n-vector under the tail condition. Division by p, randomized rounding, and mod q are postprocessing and cannot increase TV. Must independently prove rounding-tail delta_r and original full simulator, including adaptive multi-sid transcript.

## Reproducer and illustrative cost gate

Local Python /mnt/data/cgs28_flood_only_statistical_gate.py SHA256 d1f19f8b66910b54656b49c924086d734cbdbf723660910de26921fc0d22ff19; JSON /mnt/data/cgs28_flood_only_statistical_gate.json SHA256 ed73e7ab02b75e3fb181d7ab4957cdecb242ece1c688673914c4fdd30859b10c. Half-integer Gaussian sigma=32, shift=3: computed TV 0.093522827246723, strictly below 3/32=0.09375, truncated mass <=2.16e-85.

**NOT SOURCE-VALIDATED SECURITY PARAMETERS:** kappa128, n1024, k2, B1, p=2^20, sigma0=16, rounding cutoff R=2^28, B_eval=2^30. Baseline one source flood lower bound log2 sigma_flood0=158; sufficient new scalar 168.011 bits (+10.011), module 179.006 bits (+21.006). If q dominated by sigma_flood/p, q/share bit lengths increase similarly. This is not an actual lattice security estimate.

## End of iteration

STATUS PASS elementary joint statistical lemma and source-shaped flooding-only candidate; UNCLEAR complete adaptive ThFHE security, modulus feasibility, concrete LWE/MLWE hardness, evaluation key security, efficiency and novelty. **Do not claim original open problem solved.** Need to reprove source Theorem6.3/7.5 replacing per-sid zeta with fresh larger E and appropriately scaling q/Q; the enlarged q/Q might break security/performance, defeating compactness goals. 
NEXT_TEST CGS-29: ONE decisive genuine source-parameter/q/Q/security tradeoff gate; explore tighter variance-based bounds only when needed to avoid excessive flooding. STATE_UPDATE YES if committed and reread.
