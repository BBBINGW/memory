# Iteration 67 — Character-modulated fast Walsh–Hadamard blocks fail constant-distance CRT-compatible coding

Date: 2026-10-10
Target: repair of CRT-diagonal lookup soundness in Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, IACR ePrint 2025/286, CRYPTO 2025, §4.3–§5.
STATUS: FAIL for ONE explicit fast bounded-integer coding candidate. A stack of K Walsh–Hadamard transforms with diagonal masks drawn from Walsh characters has relative Hamming distance ≤1/m between distinct legal Boolean messages, even though it is fast, bounded and CRT-compatible for p_min>2m.
NO PUBLICATION/NOVELTY CLAIM: Walsh character modulation is a frequency-index permutation; an elementary Fourier orthogonality identity. No attack on original scheme, no end-to-end repair produced.

## Research discipline and provenance
Read AGENT.md, RESEARCH_PHILOSOPHY.md, unrelated parked RIG-HE STATE.md, and I66 finding `findings/vfhe-bounded-integer-code-crt-compatible-distance.md` BEFORE setting one primary hypothesis. Read paper source physical pages 24–26 via Research MCP, cached 52pp full mirror, PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, VERSION_UNVERIFIED. Original §4.3 uses scalar-table lookup PIOP; §5 builds finite-field Brakedown/RS PC from component commitments. The WHT code is OUR hypothetical repair test, not in paper. No author contact, no state change.
Classic WHT harmonic analysis reference: https://en.wikipedia.org/wiki/Hadamard_transform (Fourier on (Z/2Z)^r). The connection between character modulation and Fourier shift is standard, so not novel. See original group Fourier theory.
I66 established existence of a dense random integral 0/1 generator with restricted Boolean-message constant relative distance and no wrap for all p_i>m, but evaluation O(m²). I67 tests exactly one proposed O(m log m) fast transform and no other variant.

## One primary hypothesis and falsifier
[HYPOTHESIS — FAIL] Let m=2^r, H the *unnormalized* m×m Walsh–Hadamard matrix H_(a,x)=(-1)^{a·x} (a,x∈F_2^r). Let K be a fixed block count, and let D_(b_k) be the diagonal sign matrix of the **Walsh character** chi_(b_k)(x)=(-1)^{b_k·x}. Define fast integer code
 E(z)=concat_(k=1..K) H D_(b_k) z, z∈{0,1}^m.
Each output integer lies in [−m,m]. If p_i>2m, its AFFINE SHIFT `Eplus(z)=m*ones_(Km)+E(z)` lies in [0,2m] and has an unambiguous common canonical integer representative in each CRT prime field. Computing the unnormalized transforms is O(Km log m). Hypothesis asserts the code has constant relative Hamming distance uniformly over all distinct Boolean messages.
[FALSIFIER] Exhibit two *legal* Boolean messages z,z' whose codewords differ in o(Km) coordinates while each block is a valid fast WHT output. One exact symbolic identity plus a minimal integer checker, not a benchmark.
[CHEAPEST DECISIVE TEST] Compare all-zero and all-one messages under arbitrary Walsh-character masks.

## Universal exact counterexample for all m, all K and all character masks
Take z0=0^m and z1=1^m. Let v=z1−z0=1^m. By character orthogonality, for each mask index b,
 (H D_b v)_a=∑_(x∈F_2^r)(−1)^{(a+b)·x}
 = m if a=b and 0 otherwise.
Therefore H D_b v=m e_b has EXACTLY one nonzero coordinate. Across K blocks the full length is Km and difference support is K. Hence minimum relative Hamming distance over Boolean messages is at most
 δ_E ≤ K/(Km)=1/m.
No constant δ>0 is possible as m→∞, even if K varies, **as long as every diagonal mask remains a Walsh character**. Output-coordinate permutations likewise preserve this weight. An affine +m shift for nonnegative common integer symbols preserves differences exactly. For p_i>2m all symbols are in [0,2m]⊂[0,p_i) so no modular wrap and distance over target characteristic fields equals this integer weight.
This is NOT a no-go for arbitrary random ±1 diagonal masks: a random non-character mask produces a diffuse Walsh spectrum with high probability for the all-ones input. The result also says nothing about more sophisticated alternating-sign/butterfly products, nonlinear bounded codes, or a credible cross-characteristic commitment protocol.

## Exact minimal computation
[EXPERIMENT] Script `/mnt/data/iteration67_vfhe_character_modulated_wht_nogo.py`, SHA256 `1c34654f1277958520d78f547e934e7c670723d1bd8581488bce9e78cb7fa872`. Output `/mnt/data/iteration67_vfhe_character_modulated_wht_results.txt`, SHA256 `344c9a8d7d4b34dd57a2bed823ff8c816c902a1d9f3a797af92c3ac06721aa80`. Both created and validated in active container.
Exact integer butterfly m=16, K=4, masks b=[0,1,3,7], external prime-field moduli [37,41] satisfy p_min>2m. Compare Eplus(0^16) and Eplus(1^16): each 16-symbol block has one differing position exactly at b, total 4 differing coordinates among 64 (relative distance 1/16). Canonical outputs integers in [0,32], no modular wrap in either prime. All script assertions PASS; this does NOT instantiate a full CKKS Rq nor PIOP.
At illustrative paper-inspired m=32768, K=4, encoder length M=131072, and algebraic identity gives exactly 4 differing outputs; relative distance 1/32768≈3.0518×10^−5. Ordinary WHT butterfly cost O(4m log₂m) rather than dense I66's O(m²). Valid if 49-bit CRT p_i>65536, which they are. This is algebraic extrapolation, not a large-N timing benchmark.
An ideal verifier checking uniformly chosen encoded coordinates WITH replacement misses this specific difference with probability (1−1/m)^t. For prior I66 conditional t=665, that is approximately 0.979910, nowhere near 2^−128. A uniform without-replacement protocol likewise needs almost all symbols to get extreme soundness for four isolated differing coordinates; don't mistake hypothetical codeword openings for §4.3's 25 ring-oracle queries.

## Research judgment and limitations
[FAIL] Fast O(m log m), bounded integer outputs and CRT compatibility do NOT alone imply error-correcting distance. This particular character-modulated block family is frequency-shift equivalent and therefore has no constant restricted Boolean-message distance. No new proof system is delivered.
[NOT UNIVERSAL] A general random sign mask is NOT a Walsh character, so the Fourier-shift argument does not refute arbitrary randomized Hadamard preconditioners or fast Johnson–Lindenstrauss-type transforms; their uniform distance over the entire 3^m ternary difference set needs a separate rigorous analysis. Multi-round mixing, non-character diagonal masks and integer-code construction remain open. Avoid claiming all WHT/circulant encoders fail.
[EXTERNAL BRIDGE STILL OPEN] Even a hypothetical fast code with constant restricted distance would NOT, by itself, prove that an external shared integer message and all CRT per-field PCs are consistently encoded; need cryptographically binding, cross-characteristic opening/proximity and efficient verification. This candidate fails before that expensive stage.
[RESEARCH PRIORITY] I67 is a scoped negative result about a particularly cheap structured transform. As I63–I65 already yielded consecutive low-novelty negatives, avoid endlessly cycling slight diagonal mask variants. If next iteration still finds no nontrivial fast construction/sound protocol, escalate HUMAN_REVIEW on whether to pause repair design pending authenticated official PDF and author version/hidden-check confirmation; no disclosure without explicit PI authorization.

## End of Iteration 67
STATUS: FAIL — character-modulated WHT block stack has relative distance at most 1/m.
RESULT: For legal Boolean messages 0^m and 1^m, K masks yield only K differing symbols out of Km; exact m=16 no-wrap two-prime witness verifies, general theorem for any m=2^r. Fast encoding and no wrap survive but cannot supply sufficient coded proximity amplification.
NEXT_ACTION: For ONE next technical iteration, test whether replacing character masks by independent random ±1 masks in a small constant K Walsh–Hadamard block encoder admits a **rigorous uniform restricted-message distance bound** via hypercontractive/anti-concentration tools over all 3^m−1 differences, WITHOUT resorting to empirical sweeps. Start by testing the pairwise sign-correlation obstruction or deriving a union bound that could plausibly overcome 3^m. If no such proof route, HUMAN_REVIEW to pause the branch; do not add more character-mask variants.
STATE_UPDATE: NO — unrelated parked RIG-HE STATE.md unchanged.
