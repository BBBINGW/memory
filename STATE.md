# Current state

Current Question: Which legal RIG-HE moduli are vulnerable to an efficient, one-challenge Fourier IND-CPA attack despite satisfying the paper's sufficient correctness bound?

Primary Hypothesis: For N a power of 2, even integer a, and prime q=a^N+1, a short Fourier relation can be constructed explicitly without LLL and yields a one-challenge IND-CPA attack at a much smaller modulus than the generic LLL sufficient threshold.

Current Evidence:
- [FACT] RIG paper (Sep 10 2026), Sections 1, 5 Eq. (13), and 6 Eq. (22): split NTT, coefficient Gaussian error, secret permutation, sufficient correctness q>2 N^(2^L-1) H0^(2^L).
- [DERIVED] q=a^N+1 prime implies a has multiplicative order 2N. Frequency u=1 and v=(1,a,...,a^(N-1)) satisfy v_k≡u a^k mod q; ||v||²/q²=(a^N-1)/((a^N+1)(a²-1))<1/(a²-1). Thus a genuine NTT coordinate has Fourier bias β>1-2π²σ²/(a²-1). Galois invariance transfers the bias to all genuine slots. For t=2, challenge Enc(1) flips the Fourier phase; a single random output coordinate gives P(success)=1/2+[N/(N+n)] β [1+cos(π/q)]/4.
- [FACT: fully certified toy instances] n=N, t=2, σ=1, B=14, H0=29, K=8 input samples; q=a^N+1 verified prime using Lucas certificates; tuples (N,a,q-bits,L,rigorous-success-lower): (8,118,56,2,.7496456), (16,44,88,3,.7474497), (32,30,158,4,.7445108), (64,102,428,5,.7495256). All satisfy the paper's sufficient correctness inequality and K N delta_sigma(14)<2^-128. N32 Monte Carlo: 4460/6000 attacks vs 3036/6000 uniform controls.
- [PRIOR ART] Elias–Lauter–Ozman–Stange, CRYPTO 2015, 'Provably Weak Instances of Ring-LWE', Section 7.3 Proposition 7.1 already analyzes f(2)=0 mod q and associated complete splitting for Fermat-type primes; Section 8 distinguishes roots of small *order* from numerically small representatives. LWE/PLWE evaluation and dual Fourier principles are well-established. Novelty of the hidden-permutation IND-CPA application is NOT VERIFIED.

Main Uncertainty: Explicit four instances do not establish an infinite asymptotic weak family (primality of a^N+1 along infinitely many N is unproved here), nor insecurity of generic polynomial-size q. Need narrow prior-art comparison for ciphertext hidden-permutation setting.

Next Minimal Test: Review whether the Fourier distinguish-and-decrypt attack is subsumed by prior cryptanalysis of hidden-permutation noisy encodings, or prove a broader prime-modulus condition replacing q=a^N+1 without losing polynomial-time exploitability.

Status: PASS (explicit construction, rigorous bias, unconditional Lucas primality certificates, correctness-overlap and experiment); NOVELTY NOT VERIFIED; HUMAN_REVIEW for contribution and pivot decision.
