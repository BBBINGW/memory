# CGS-43 — Private negacyclic Fourier quadratic cost and precision gate

Date 2026-10-15. PI-selected single active CGS, last completed CGS-42. ONE hypothesis and ONE decisive spectral identity plus finite precision test. No secure MPC/FHE implemented.

## Hypothesis

CGS42 conjectured that n-point negacyclic Fourier representation lets parties privately evaluate Q(z)=z^T((Bpub^2 I-Sigma_s)^-1−Bpub^-2 I)z with O(n) secure multiplications per candidate, and implicitly costed those multiplications as two 64/128-bit field-element openings each. Does that algebra actually work, and can a straightforward one-field 64/128-bit FIXED-POINT implementation attain negligible total Gaussian acceptance error across kappa128,J224,LDec2^20?

Status: PASS mathematical O(n) real arithmetic; FAIL treating naive 64/128-bit field values and CGS42 traffic as an established precision-correct secure MPC circuit. Not a universal lower bound on all fixed-point protocols.

## Source facts and grounding

Okada–Takagi, Low Communication Threshold FHE from Standard (Module-)LWE, ASIACRYPT2025, https://eprint.iacr.org/2025/409, full 40-physical-page PDF acquired by connected Research MCP, SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301, VERSION_UNVERIFIED. Definition3.1 physical p12: n power of two, R=Z[X]/(X^n+1), Gram(s)=mat(s)mat(s)^T. §3.3 p13: integer lattice Gaussian mass exp(-pi z^T(S S^T)^-1 z). Algorithm7 p29: original target D_(Z^n,sigma0 sqrt(Bpub^2 I-Sigma_s)). Lemma7.1 p30 has separate smoothing/min-singular-value/noise assumptions, not certified by illustrative numbers. Source has original TWO online communication phases; an interactive secure MPC modification explicitly relaxes that.

CGS41 findings/cgs-41-gaussian-rejection-acceptance-gate.md: exact private spherical proposal and accept exponent -pi Q/sigma0^2. CGS42 findings/cgs-42-constant-acceptance-cost-gate.md: source negacyclic coefficient bound implies constant accept probability and 224 fixed proposals/call in an illustrative kappa128,n1024 scenario. Fixed-point Shamir multiplication/truncation is established but can itself require interaction; relevant independent source https://link.springer.com/article/10.1186/s42400-024-00343-4.

## Exact real spectral identity [DERIVED]

Let omega_j=exp(i*pi*(2j+1)/n), hat z_j=sum_t z_t omega_j^t, gamma_j=sum_(i=1)^k |hat s_i,j|^2, and w_j=gamma_j/[Bpub^2(Bpub^2-gamma_j)]. Unnormalized negacyclic Fourier transform is unitary after division by sqrt(n). Since Sigma_s=sum_i Gram(s_i), with Gram eigenvalues |hat s_i,j|^2,

Q(z)=(1/n) sum_(j=0)^(n−1) w_j |hat z_j|^2.

For REAL input z and s, conjugate frequencies j and n−1−j share the same real weight. With hat z_j=x_j+i*y_j,

Q(z)=(2/n) sum_(j=0)^(n/2−1) w_j (x_j^2+y_j^2).

In an IDEAL real Shamir-sharing model, trusted KeyGen could pre-share n/2 secret real weights w_j, while public-coefficient linear FFT of SECRET shares requires only linear operations. Per frequency pair: two secret real multiplications x^2 and y^2 in parallel, and one subsequent secret multiplication by w. Thus 3*n/2 secure REAL multiplication gates per candidate, multiplicative depth TWO, ignoring distributed Gaussian proposal generation, FFT fixed-point error, selection and private exp/Bernoulli sampling. At n1024,J224: 512 secret real weights pre-shared at KeyGen, 1536 secret multiplications/candidate, 344064 per decryption. This corrects CGS42's illustrative n multiplications/candidate by +50%.

## Decisive exact algebra and modulus test [EXECUTED]

Reproducer /mnt/data/cgs43_private_fft_precision_gate.py, SHA256 2b92a12d6dc7ce011b02245fa8caa1e344393cad04cf38f4cb3bcdc68d360072.
JSON /mnt/data/cgs43_private_fft_precision_results.json, SHA256 614094fb51585c1ba515cf74e935f1ce4d0d1364f281bfdc6e8e233e5a8fd43e.
Executed in current session with exact rational SymPy and independent NumPy FFT, high precision mpmath for error budget. NOT a cryptographic implementation.

- n8, s1=1+X, s2=1, Bpub^2=27, z=(2,-1,0,3,2,-2,1,1). Exact rational matrix inverse yields Q=152353/1482633=0.10275840346194912; independently derived complex Fourier formula and half-frequency pairing agree within double numerical precision.
- Finite-field NTT control n4,p97, a 2n-th root 33, s=1+X,Bpub^2=10,z=(1,2,0,-1). True ordered real Q=42/155≈0.270968, but NTT outputs residue 81 mod97, EXACTLY rational 42/155 reduced mod97. This is mathematically correct MODULAR arithmetic, not real magnitude or exp(-pi Q/sigma0^2). A 64-bit field NTT does not magically provide an exactly ordered real Gaussian exponent.

## Rigorous SUFFICIENT weight-only fractional precision budget [DERIVED+EXECUTED]

Fix SAME previous illustration: kappa128,n1024,k2,Bmlwe2,Bpub2897,sigma0=4, fixed J224, LDec2^20; source-complete FHE parameters remain UNVERIFIED. Private proposal vector has n independent integer discrete Gaussian coordinates from D_Z,w, public spherical width w=sigma0*Bpub=11588.

Use a valid conservative two-sided Gaussian mass tail (partition sum at least 1):
Pr(|Z_i|>=H) <= 2 exp(-pi H^2/w^2)/[1-exp(-pi(2H+1)/w^2)].
Reserve 2^(-kappa-2) of total allowable statistical error for truncation across ALL n*J*LDec proposed coordinates. Exact high precision calculation yields minimum H=72419, total tail upper bound 7.341316145902055e-40 <2^-130. Conditioned on no tail event, ||Z||^2<=n*H^2=5370379838464 (~42.288 bits).

In an extremely FAVORABLE model assume the FFT, x,y squares and Gaussian proposal are all exact real numbers; ONLY each secret spectral weight w_j is quantized with absolute error <=2^-b. Parseval guarantees |Q-Qapprox|<=2^-b ||Z||^2<=2^-b nH^2, even with the n/2 conjugate-pair formula. Clip approximate Q to nonnegative if needed. On nonnegative inputs exp(-pi Q/sigma0^2) is (pi/sigma0^2)-Lipschitz. Therefore ALL J*LDec Bernoulli acceptance decisions contribute at most

epsilon_accept_weight <= (pi/sigma0^2) J LDec nH^2 2^-b

to the sequential statistical-error hybrid. Reserving another 2^(-kappa-2) yields MINIMUM sufficient b=198 fractional binary bits for THIS conservative bound. At b198 its total accept error bound is 6.165150516043003e-40 <2^-130. At b197 the sufficient inequality fails. This is a conservative SUFFICIENT precision requirement, NOT a universal lower bound that all secure Gaussian samplers require at least 198 bits. Further FFT root approximation, fixed-point overflow, exponential/compare, distribution-sampling and final re-sharing errors remain NOT counted.

Thus the earlier assumption that a 64/128-bit element can DIRECTLY represent the private ordered real spectral weights and their negligible-error computations is unjustified under this chosen correctness budget. Multiprecision field elements/limbs are feasible in principle but multiply the actual MPC cost.

## Source-size multiplication/storage cost consequences

344064 private REAL multiplication gates per decryption require 688128 field-value openings in an ideal 2-party Beaver-style online multiplication circuit with two masked opens per multiplication. Merely multiplying by illustrative 64/128/192/256-bit SINGLE field-element sizes yields respectively 5.25/10.5/15.75/21 MiB per party per decryption in openings ALONE; these are NOT measured network bandwidth, valid source moduli, full MPC cost, nor a universal communication lower bound. Earlier CGS42's 3.5/7 MiB used only n gates/candidate and ignored the additional squares/product gate structure.

Pre-generating dedicated independent multiplication triples for every proposed candidate over all LDec2^20 decryptions would require 360777252864 triples over the lifetime, again linear in LDec; that is NOT a free storage removal. Online OT/PCG/correlation generation could avoid literal triple storage but entails separate computational/security/communication tradeoffs.

Even ignoring FFT root error, an integer accumulator that tracks the b198-weight-scaled Q on the chosen public truncation range can require about 228 bits of numerical dynamic range under the corresponding bound. This is only a BEST-CASE range illustration, not a proof that any particular 256-bit prime implements the entire secure fixed-point FFT. Native modular NTT residues provide no order or real Gaussian accept operation.

## Scientific status and next action

PASS: exact real spectral representation and ideal O(n) secure multiplication count; independently confirmed exact rational vs complex FFT, and the modular-NTT/rational-residue distinction.
FAIL: using CGS42 64/128-bit Beaver-opening bandwidth as a verified cost for statistically accurate secret Gaussian accept.
UNCLEAR: actual secure fixed-point FFT representation, authenticated multiplication/truncation, private Gaussian proposal, rejection flag and first-success control, adaptive original Algorithm5 simulator, full source assumptions, genuine publishable efficiency gain. No new FHE or Gaussian protocol implemented; original source O(LDec) TWO-ROUND challenge remains OPEN.

ITERATION CGS-43. STATE_UPDATE YES: own finding, topic archive and sole root checkpoint.
NEXT_TEST CGS-44 (ONLY on PI next "继续"): ONE concrete secure multi-limb fixed-point circuit for a private negacyclic FFT quadratic, with at least b198 weight fractional precision under this selected bound, error accounting for Fourier constants and exponent acceptance, actual authenticated online communication and fresh correlation setup. If low-round/storage gains vanish, recommend PARK or PI pivot rather than another ideal-real arithmetic derivation.