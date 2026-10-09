# Current state

Current Question: Independently audit large-modulus LLL/Fourier attacks on the September 10, 2026 "Random Insertion Gaussian" paper's RIG-HE, especially its IND-CPA implications.

Primary Hypothesis: For plaintext modulus t=2, a public short Fourier relation suffices to distinguish Enc(0) from Enc(1) using ONE challenge ciphertext and NO encryption-oracle queries, without locating genuine slots.

Current Evidence:
- [FACT] Uploaded paper: Section 1 (split NTT and iid symmetric coefficient Gaussian), Section 5 Eq. (13) (Enc), Section 6.2 Eq. (22) (sufficient depth bound).
- [DERIVED] Under prime q ≡ 1 (mod 2N), N a power of 2, σ ≥ 1, and q^(1/N) ≥ 4πσ·2^((N−1)/4), LLL finds v∈Z^N with v_k≡v_0 r^k (mod q) and ||v||≤q/(4πσ). Divide by 2 while all coefficients even; use negacyclic rotation to make integer v_0 odd without raising norm. For genuine coordinates, Fourier bias β≥7/8; after scaling t=2 ciphertext by 2^(-1), plaintext 1 flips the character phase: cos(2πv_0·2^(-1)/q)=−cos(πv_0/q).
- [DERIVED] One-random-coordinate randomized classifier has success probability 1/2+(N/(N+n))·β·(1+cos(πv_0/q))/4 ≥ 1/2+7(1+cos(1/(4σ)))/64 ≥ 0.7153. The proof uses no encryption-oracle queries; n can equal N.
- [FACT: numerical experiment] N=n=16, t=2, σ=1, H0=17, L=4; smallest prime satisfying the paper's sufficient correctness bound has 127 bits. Reproducible independent LLL/finite-Gaussian experiment: theoretical single-challenge success ≈0.7498505; full ciphertext + secret permutation Monte Carlo 4490/6000=0.748333; uniform negative control 3000/6000=0.5. At L=3 the smallest sufficient correctness prime is ~62 bits and the instance-specific success calculation is ~0.7123347 (not a universal lower bound).

Main Uncertainty: Novelty vs known Fourier/PLWE evaluation attacks remains UNVERIFIED; the theorem only covers the stated extremely large modulus condition, and the depth bound is sufficient, not necessary. Establishing security/insecurity for conventional q regimes is open.

Next Minimal Test: Independent mathematical peer review of the parity/rotation argument and sharper sufficient Fourier-shortness criteria at minimal correctness q, followed by narrow prior-art comparison. Human decides whether to pivot from standard-RLWE reduction toward a cryptanalytic result.

Status: PASS for the one-challenge attack proof and reproducible tests; HUMAN_REVIEW for novelty, impact and strategic direction.
