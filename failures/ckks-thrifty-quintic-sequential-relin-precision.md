# Iteration 46 — A naive sequential quadratic relinearization schedule loses third-order bit-cleaning precision

Date: 2026-10-10
Focus: Choe, Kim, Stehlé, Suvanto, *Leveraging Discrete CKKS to Bootstrap in High Precision*, ePrint 2025/1786 / ACM CCS 2025.
STATUS: FAIL for the **specific naive sequential s^2-key Relin substitution**, not for the paper's actual generalized tensor-then-Relin algorithm.
NOVELTY NOT VERIFIED; basic but quantitatively important relinearization schedule / precision / key-size boundary.

## State and original source
[FACT] Read GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md, and the iteration45 sparse-CKKS prior-art archive before starting. The I40–I44 SubSum–Fourier fusion branch remains paused/archived as low-priority; RIG-HE STATE.md is unrelated and is NOT edited.
[FACT / PRIMARY] Research MCP fetched the original 15 physical-page CCS 2025 PDF for ePrint 2025/1786 from fixed GitHub mirror, source kind github-mirror, source revision cdf2caac0369a6232616ffcea2c020242076e62a, PDF SHA256 3d1e2277a4a64de6094094c86a941f95374528be50fea611847927d8a68b4230, VERSION_UNVERIFIED. Page text parsed with warnings; complex printed equations not visually checked.
- §1.1, physical pp.3–4: use low precision to extract and clean bits/trits; thrifty cleaning makes modular cost grow additively in high-precision parameters rather than with all CtS stages.
- §4.1, Figure 2 and Theorem 4.1, physical pp.9–10: h1(x)=3x^2-2x^3; tensoring itself introduces no NEW homomorphic evaluation error, but Relin and rescaling do. Thrifty cubic consumes Δ of modulus vs black-box Δ^4 in the idealized scale model; theorem explicitly tracks relinearization error.
- §4.1 Theorem 4.2 physical p.10: k rounds consume Δ^(2^k-1) in ideal scale progression, with practical extra gap/rounded scaling cautions below.
- §4.2 physical p.11: for arbitrary integer-coefficient polynomial P(x)=Σ_{j=0}^k α_j x^j, paper proposes **ct_j = Δ^(k-j) Relin(ct^(⊗ j))**, meaning *unrelinearized degree-j tensor* followed by direct high-degree Relin, then combines terms. Paper states normalized error driven by minimum nonzero j0≥2. It does NOT claim an unmodified sequential relinearization chain achieves the same bound.
- §5.1 physical p.11: real implementation uses HEaaN/grafting with actual scale/modulus details beyond our exact toy.
[PRIOR ART] The bit cleaner h1 is from existing prior work; the quintic smootherstep polynomial H(x)=10x^3-15x^4+6x^5 with vanishing first/second endpoint derivatives is standard numerical interpolation, not a novel function.

## One primary hypothesis and falsification condition
[HYPOTHESIS — FALSE FOR NAIVE CHAIN] Replace §4.2's high-degree tensor-then-Relin for the quintic H with the straightforward power chain P_j=Relin(P_(j-1)⊗P_1), relinearizing after EVERY multiplication with only an ordinary s^2→s key. Claim: retain 3rd-order output precision O(Δ^-3) for a noisy bit x near 0 or 1, at output scale Δ^3 and rescale Δ^2, without higher-degree evaluation keys.
[FALSIFICATION] Find any allowed nonzero relinearization error of O(1) resulting in normalized output error Ω(Δ^-2) instead of O(Δ^-3) as Δ grows.
[MINIMAL TEST] Exact scalar-slot decoded-numerator error algebra with x=1, only one early unit key-switching error, all later Relin errors zero; no need for encryption, CKKS parameter search, or stochastic simulations.

## Exact derivation
[DERIVATION] For H(x)=10x^3-15x^4+6x^5, H(0)=0,H(1)=1,H'(0,1)=H''(0,1)=0, and H(b+ε)=b+O(ε^3) locally around bits b∈{0,1}. Desired one-pass output scale Δ^3 and normalized output error O(Δ^-3). A straightforward degree-5 evaluation first forms a raw numerator with scale Δ^5 and then rescale by Δ^2.

Take input decoded value P1=Δ corresponding to b=1 and no initial plaintext error. In the naive quadratic Relin power chain (decoded scalar model):
P_j=P_(j-1)*P1+e_j. Let e2=1, e3=e4=e5=0 (one *unit* early key-switch error, consistent with an O(1) homomorphic error model).
Then
  P2=Δ²+1,
  P3=Δ³+Δ,
  P4=Δ⁴+Δ²,
  P5=Δ⁵+Δ³.
Evaluate raw polynomial numerator
  C = 10Δ² P3 − 15Δ P4 + 6P5 = Δ⁵+Δ³.
Rescale by Δ² (ideal noiseless division in this toy) gives output Δ³+Δ, whose absolute decoded numerator error is Δ and whose normalized error at scale Δ³ is **Δ^-2**, not Δ^-3. Earlier Relin error propagates through successive tensor multiplications; numeric polynomial endpoint smoothness cannot force arbitrary evaluation-key errors to vanish.

For comparison, §4.2-style **direct** degree-j Relin of unrelinearized tensor powers gives Pj_direct=(Δ*b)^j + e_j without inheriting the same quadratic Relin error across higher powers. Let e3=1,e4=e5=0. Then
 C_direct=Δ⁵+10Δ² and (rescale by Δ²) output is Δ³+10, with normalized error 10Δ^-3.
More generally if direct e_j=O(1), after the same rescale the contribution from j=3 is O(1), j=4 O(Δ^-1), j=5 O(Δ^-2), preserving third-order accuracy conditionally.

## Reproducible minimal test
[EXPERIMENT] Run `/mnt/data/iteration46_thrifty_quintic_relin_error.py`, output `/mnt/data/iteration46_thrifty_quintic_results.txt`, script SHA256 4dc0979cede2bdc93139558af4b69addc5e16da29c4503c6549982d798990326. Python exact integers and Fraction, Δ∈{16,256,4096,65536}. For each Δ, sequential post-rescale output error exactly Δ, direct higher-degree Relin post-rescale output error exactly 10, all assertions pass. Endpoint cleaner derivative conditions and cubic approximation bound also tested. No floating-point used for any identities (floats only for printed relative ratios).
The script is a *decoded scalar constant-slot model*, not a secure CKKS implementation, actual noisy RLWE scheme, modulus wrap, stochastic noise distribution, real HEaaN runtime, or honest full relinearization measurement. The counterexample assumes a nonzero legal evaluation-key error that can contribute one in a decoded slot and is not a universal lower bound across ALL possible quadratic-only clever evaluation circuits.

## Why the direct version is not free
[DERIVED] For a general secret, a degree-j tensor ciphertext decrypts under (1,s,...,s^j); directly relinearizing it to degree-one usually needs evaluation-key material for higher powers s^2,...,s^j or equivalent generalized key-switch machinery, NOT merely a single normal s^2 key in the usual interface. The key material/memory, decomposition, modulus/noise and runtime costs for high-degree Relin are NOT quantified by this toy.
[DERIVED / IMPORTANT SCOPE] Paper §4.2 already explicitly asks for the direct high-degree Relin; its theorem does **not** assert naive sequential post-multiplication Relin. The result is an implementation-specific obstruction, not a verified correctness gap, error or cryptanalytic attack in the published paper. Whether a specialized factorization using only s^2 keys can avoid this particular propagation is OPEN. There is no general impossibility claim.
[PRIOR ART] Lazy/delayed relinearization and efficient power generation are known concepts. Quintic smootherstep is a textbook polynomial. NOVELTY NOT VERIFIED and likely low absent a novel scheduling/representation method with demonstrably improved eval-key + modulus/latency frontier.

## End of Iteration
STATUS: FAIL for the naive sequential quadratic-Relin substitution; paper's original generalized method remains valid under its own assumptions.
RESULT: A single O(1) early key-switch error at bit=1 produces Ω(Δ^-2) instead of O(Δ^-3) normalized precision in the simplest degree-5 sequential chain; direct high-degree Relin does not inherit that early error in this toy. The main unexplored tradeoff is higher-degree evaluation-key cost vs saved modulus budget.
NEXT_ACTION: Before committing to an implementation, inspect the exact high-degree Relin key generation and decomposition complexity available in HEaaN or another fully available CKKS reference; test **one** concrete high-power key-size/runtime bound for degree5 against a two-round cubic cleaner. If code is unavailable, archive this tradeoff and pivot instead of using new toy parameter sweeps.
STATE_UPDATE: NO; preserve separate parked RIG-HE STATE.md.
