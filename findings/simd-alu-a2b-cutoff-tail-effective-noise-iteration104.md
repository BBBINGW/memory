# Iteration 104 — Iterated SIMD ALU A2B cutoff injects deterministic effective input residue not captured by original v alone

Date: 2026-10-12. Paper Gao–Zheng, *FHE for SIMD Arithmetic Logic Units with Amortized O(1) Bootstrapping per Ciphertext*, ePrint 2026/233. Research MCP PDF full 43 physical pp SHA256 `f16f4004d76450fb2264e6a5b36c3eceac2f87586148b96073c76ca7775f0f92`, official/latest VERSION_UNVERIFIED.
RESULT STATUS: **PASS scoped deterministic scalar cutoff residue**, **FAIL naive O(d) independent cumulative cutoff growth**, **UNCLEAR whether published global Theorem6 proof is complete or any real ciphertext violates correctness**. Critical: authors explicitly acknowledge treating low bits as noise and cutoff, so it is **not a previously unrecognized implementation issue**. This is a proof-composition bookkeeping / parameter-boundary question, not a protocol attack or novelty.

## Read before write / evidence
GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, active STATE.md I103, I103 failure; primary ePrint 2026/233 physical p14 Definition8, pp21–23 §5.2 A2B iterative and cutoff, p25 Table3 empirical bottom noise, p27 Theorem6, p28 §7.3 param cutoff -16 and κ=1. Used Research MCP full-text keyword search for 'cutoff', 'noise accumulation', 'iteration' and 'error propagation'; absence of exact extracted match is not proof absence of full recurrence.
[FACT] Definition8 p14: D-CKKS LUT for input ΔI+Δm/p+e outputs Δf(m)/p+e'+e'', where e'/(Δ/p) is O((ep/Δ)^{κ+1}) and e'' accounts homomorphic evaluation noise; one-step local statement.
[FACT] Theorem6 p27 as extracted: For A2B initial arithmetic-mode ΔI + (Δ/t)[m]_t + v, require C3(∥v∥p/Δ)^{κ+1} < ∥e_B∥p/Δ; proof says 'See Def. 8'. It does NOT explicitly write a recurrence indexed over all n/w iterations in this passage. Theorem6 may be *intended as an invariant* with an effective per-step v; extraction cannot certify its complete proof generality.
[FACT] §5.2 p22 explicitly says A2B-cutoff treats lower bits as **noise**; for w4, cutoff -16, only 3 rotations of LUTID per ciphertext subtraction step. §7.3 p28 uses A2B-cutoff -16; Table3 p25 gives empirical log2(∥e_B∥/Δ)=-20.4.
[FACT] Pin public repository `tsinghua-ideal/fhe-simd-alu`, HEAD `08f1eb87434e7be072cba889270a8400bbffc08e`, file `src/pke/lib/scheme/ckksrns/z-fhe.cpp` SHA `8ac367867f9928f6f5712ff5e8c9cb6f8a18ca02`, lines 534–565 (full A2B) and lines 693–727 (batched); similarly sparse at lines449–467. Code has:
`diff=iter-nextIter; rotationIndex=diff*w; if(rotationIndex<=precomp.m_cutoff){break;}`
plus `scaled = EvalMultInC(lut, pow2(diff*w))` and `EvalSubWithAdjustInPlace(core,scaled)`. Therefore for w4/cutoff−16, only distances s=1,2,3 are subtracted; s>=4 intentionally retained in later core components.
[FACT] Pinned `z-fhe-precompute.cpp` SHA `7412caec6bb755ee43eb08785158159983c37e92` lines 239–269 sets p=1<<w and D-CKKS.LUTID (input x=0→0, x=1..p−1→x−p) with Hermite order `lutOrder=1`. A preexisting ≤p−1 digit occupies magnitude ≤(p−1)/p normalized (not necessarily x=0xF literal x-value, since source operates in negative fraction convention). Example all relevant magnitudes 15/16 is representable with LUTID x=1.
[FACT] Source `src/pke/examples/example.cpp` calls `EvalBootstrapSetup(...,4,-16,1)`.

## ONE primary hypothesis and cheapest decisive falsifier
HYPOTHESIS: Theorem6's single inequality, interpreted as a condition on the *original input v alone*, directly bounds each of d=n/w successive D-CKKS.LUTID/LUTMSB inputs **without** an independent cutoff-tail term or re-bound after subtraction.
FALSIFIER: show under ideal arithmetic (initial v=0, exact D-CKKS.LUTID and no cryptographic noise), the deterministic source-mandated cutoff leaves a nonzero earlier-digit residual in a later round. Such an input deviates from exact grid by that residual despite original v=0. This is a falsifier of the *naive single-v-to-all-rounds inference*, not by itself a failing bit/result.

## Toy scalar derivation [DERIVATION / PASS]
Let p=2^w=16, normalized LUTID digit contribution a_i satisfy |a_i|≤(p−1)/p=15/16. In round j (zero based) the source removes old blocks at distances s=j−i≤3. Blocks s≥4 are not removed and contribute a deterministic tail
`H_j = ∑_{s=4}^{j} a_{j-s} p^{-s}`.
In extremal aligned-sign case a_i=−15/16 (possible LUTID residue at x=1), for j≥4,
`|H_j|=(15/16)∑_{s=4}^{j}16^{-s} = 16^{-4}(1−16^{-(j−3)})`;
for j≤3 it is zero. Thus even if initial v=0 and all LUT errors=0, the **fifth** iteration has H_4=15/1048576≈1.430511474609375e−5, whereas H_15≈1/65536 and H_63≈1/65536; for any d and any signs, |H_j|<16^{-4}=2^{-16}. Hence NO linear-in-d growth: cutoff scalar tail saturates geometrically.
This is an exact *single location* scalar projection of the bit-transfer code. The real packed CKKS implementation also has transforms, partial sums, key switching, scale correction etc.; no statement that the full cryptographic error equals H_j.

## What a composition-aware proof would need [DERIVATION CONDITIONAL]
Write normalized error into j-th D-CKKS.LUT as
`E_j/Δ = (v_j^{base}/Δ) + H_j + η_j^{ops}/Δ + Σ_{s=1}^{min(3,j)} p^{-s} ε_{j−s}^{ID}/Δ`
(with coefficients/signs and actual operation-dependent mapping to be checked; triangle values / E_j not all in same representation without precise transforms). Bound by triangle inequality
`|E_j|/Δ ≤ |v_j^{base}|/Δ + p^{-4} + |η_j^{ops}|/Δ + Σ_{s=1}^3 p^{-s}|ε_{j−s}^{ID}|/Δ.`
`Σ_{s=1}^3 16^{-s}=273/4096≈0.066650390625`, so any uniform prior-ID-error upper bound G yields feedback ≤(273/4096)G (plus cutoff-tail and fresh per-stage errors), NOT d·G. Distinguish LUTID error ε from LUTMSB output noise; Theorem6 as printed uses only C3 and e_B but does not visibly quantify ε_ID or fresh operation noise. This is a request for formal compositional invariant, not a proof published argument is false.
For illustrative *conditional* `E=2^{-16}`, `p=16`, `κ=1`, paper Table3's **empirical** `e_B/Δ≈2^{-20.4}`: a single LUT satisfies its inequality from cutoff tail alone if `C3 (16 E)^2 < 16·2^{-20.4}`, i.e. `C3<2^{7.6}≈194.0`. This is **not** verified because C3 is unspecified and the complete E includes v, ε_ID and operation noise; Table3 empirical bottom noise is not a cryptographic worst-case/security guarantee. Do not infer the chosen parameters are correct or broken from this illustration.
Also the source may intend initial v of Theorem6 to encompass all effective deterministic perturbations under an implicit invariant; need consult full source/experiment carefully before gap claim.

## Exact reproducibility [TEST]
Python Fraction scalar exact arithmetic at n64,d16 and n256,d64, p16, cutoff−16:
- first residual nonzero stage j4;
- H4=15/1048576 exactly;
- H15=281474976710655/18446744073709551616≈1.52587890625e−5;
- H63 differs from 1/65536 by less than float precision;
- uniform upper bound 1/65536 independently of d; feedback three-term coefficient sum 273/4096.
Verified `/mnt/data/iteration104_simd_alu_cutoff_residual.py` SHA256 `b07ec6c9cb05edfcb36b2f81a86db0205ddd12d946632b3f5fea913cb5d97492`, JSON `/mnt/data/iteration104_simd_alu_cutoff_residual_results.json` SHA256 `29f4b9cb0cadde6de66bae3b93efe67cb693c7c72fba8da83cb760270d29beab`.
No full CKKS execution, actual key switching noise, security attack, failure probability, or author contact.

## End
STATUS: **PASS** exact residual / **FAIL** naive zero-input-noise→zero-per-step-input-perturbation and naive linear-d growth; **UNCLEAR** authors' global bound/correctness status.
RESULT: Implementation intentionally keeps ≤2^-16 deterministic normalized earlier-digit tail; one-step Theorem6 source expression requires per-round reinterpretation including tail and LUTID injected noise to justify all stages. A numerical budget may be ample, but not proven.
NEXT_ACTION (I105): From pinned Gao–Zheng source (`z-fhe-precompute.cpp` HermiteTrig LUTID order1 and LUTMSB; `z-fhe.cpp` multi-LUT evaluation), isolate ONE scalar end-to-end ideal polynomial LUT evaluation for input *exact grid point plus worst admissible tail 2^-16*, and compute the actual output error of BOTH LUTID and LUTMSB with the implemented approximation and truncation under w4/κ1, comparing to reported empirical e_B/Δ≈2^-20.4. If the polynomial/multi-value LUT can't be isolated without full CKKS or missing coefficients, record EVIDENCE MISSING rather than pretend numerical correctness; do not broaden. This is necessary to determine whether cutoff was adequately budgeted; no new paper error claim.
STATE_UPDATE: YES. No author outreach/email/public disclosure.
