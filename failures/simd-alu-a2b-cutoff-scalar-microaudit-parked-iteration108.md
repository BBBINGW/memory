# I108 strategic decision — Park Gao–Zheng A2B elementary scalar cutoff/LUT audit I103–107

Date: 2026-10-12. PI responded '好的，请继续' after I107 status HUMAN_REVIEW and recommendation option B: archive the specific low-novelty scalar cutoff branch and seek a genuinely independent primary-source FHE technical gap. This archives ONLY the narrow audit, NOT the Gao–Zheng paper nor any broader A2B application.

## Source-grounded retained status
- ePrint 2026/233, Gao–Zheng, `FHE for SIMD Arithmetic Logic Units with Amortized O(1) Bootstrapping per Ciphertext`, Research MCP primary mirror full 43 physical pages, SHA256 `f16f4004d76450fb2264e6a5b36c3eceac2f87586148b96073c76ca7775f0f92`, latest official VERSION_UNVERIFIED. Pinned author source `tsinghua-ideal/fhe-simd-alu` commit `08f1eb87434e7be072cba889270a8400bbffc08e`.
- I103 `failures/simd-alu-synthetic-batch-from-one-ciphertext-no-independent-data-iteration103.md`: cannot manufacture B independent ciphertext payloads from a single ciphertext by masks/rotations; author explicitly assumes sufficient independent data.
- I104 `findings/simd-alu-a2b-cutoff-tail-effective-noise-iteration104.md`: w4 cutoff−16 intentionally leaves deterministic scalar normalized low-bit tail of magnitude <2^-16, not linear in n/w. This is disclosed by authors, NOT a novel attack.
- I105 `findings/simd-alu-hermite-lut-cutoff-tail-polynomial-response-iteration105.md`: pinned source order1 Hermite dual-LUT and exp46 polynomial cleartext reproduction with ±2^-16 grid perturbations: max MSB 1.09e−7 below author's empirical bottom noise ~7.23e−7; **not** all-round CKKS.
- I106 `findings/simd-alu-uniform-hermite-msb-cutoff-bound-iteration106.md`: conditional high-precision finite Taylor majorant for all 16 tiny intervals, conservative MSB scalar error ≤1.66e−7, conditional on compiled coeff bound; not independently formal outward rounding.
- I107 `findings/simd-alu-a2b-lutid-three-lag-feedback-invariant-iteration107.md`: ideal scalar three-lag LUTID feedback contractive (α=273/4096), a uniform bound on input perturbation R=1.01*2^-16 for 16/64 rounds, **IF** extra per-round CKKS normalized noise |η_j|≤1.42317e−7. There is NO verified implementation bound on η_j; cannot infer correctness from scalar.
- No demonstrated author correctness flaw, security attack, performance gain or new algorithm. No claim of proof beyond source-faithful scalar model; no further low-return scalar tests without a specific new ingredient.

Previous STATE snapshot `logs/simd-alu-state-pre-carousel-handoff-iteration108.md`; original vFHE CRT lookup ideal-IOP discrepancy remains open and separately recorded; nested-RNS, PaCo, RIG, GL branches all retained as documented. No author contact, emails or public disclosure.

**New target**: Carousel ePrint 2024/2032, Hwang–Min–Song, automorphism-group full-domain blind rotation. One I108 hypothesis: missing first-round fractional slack in `|e|<N/(2p)` when `p∤N`; test one paper-valid prime cyclotomic parameter and tiny exact CRT/LUT arithmetic. Do not conflate with implementation attack.
STATUS: PARKED narrow SIMD ALU microaudit.
