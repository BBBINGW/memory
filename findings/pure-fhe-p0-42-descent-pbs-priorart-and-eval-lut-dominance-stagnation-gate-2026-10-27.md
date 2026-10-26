# PURE-FHE · P0-PRESCOUT-42 — Module-to-ring Descent-PBS prior-art gate, LUT dominance, and mandatory stagnation

Date: 2026-10-27 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: INDEPENDENT_PURE_FHE_CORE_CONSTRUCTION_SOURCE_GATE
PREVIOUS: P0-PRESCOUT-41 `findings/pure-fhe-p0-ckks-output-noise-simulation-tv-precision-gate-2026-10-27.md` commit `6e386cfb20c3bf9b3549d6621bf2328f3e7b7a16`
LATEST_COMPLETED: P0-PRESCOUT-42
NEXT_ITERATION: P0-PRESCOUT-43 NOT_STARTED; HUMAN_REVIEW before further expansion
STATUS: FAIL_H42_NEW_MODULE_TO_RING_DESCENT_NOVELTY / PASS_PUBLISHED_FUNCTIONAL_LUT_AMDAHL_COST_GATE / STAGNATION_HUMAN_REVIEW
NOVELTY: NOT_ESTABLISHED, no independent crypto construct/theorem, no author finding attributed to us.
CODEX_REQUIRED: NO, no GPU, native tests, servers or downloads/environment changes.
STATE_UPDATE: YES, only this isolated PURE-FHE finding; root STATE.md and SHIP/BOOT/CGS/VFHE/EAI other tracks unchanged.

## H42 — one smallest falsifiable novelty hypothesis (not an implemented construction)

Could a multi-bit TFHE/FHEW PBS for lookup tables larger than negacyclic ring capacity become a *novel* independent cryptographic contribution simply by paying the module-rank accumulator cost once, applying one merged public functional key switch to descend into a ring, then performing subsequent refinement rotations in the ring rather than inside the module? The compelling apparent gain is eliminating a repeated factor of module rank, i.e. changing a main complexity term rather than local key/NTT tweak.

Cheapest decisive test: PRIOR-ART search and original-source metadata against the newly released October 2026 paper; original-text algorithm audit if the paper can be obtained. If authors explicitly already implement EXACTLY this, H42 fails NOVELTY without speculative independent derivation. A separate source-complete older packed-FBT cost table checks whether pivoting instead to linear formatting stages is likely to meet a 2x gain; it is contextual quantitative cost evidence, not a second novel constructive hypothesis.

## [FACT] New first-party primary publication / full-source limitation

Zhenyu Xiong, Mingsheng Wang, Han Wang, Zhedong Wang, *Descent-PBS: Programmable Bootstrapping beyond the Ring Dimension*, ePrint2026/2616, current publicly indexed metadata updated 2026-10-23: https://eprint.iacr.org/2026/2616 . Public mirror with author's abstract/metadata: https://eprint.iacr.asia/2026 and https://eprint.iacr.asia/days/7 . The indexed abstract explicitly says the authors:
- exceed 2N negacyclic signed rotation positions with module-based LUT and pay module rank on FIRST rotation;
- prove truncation commutes with a subring-embedded module secret;
- use one merged-column **public functional key switch** to repack all tau_0 module accumulator components into an ordinary ring, eliminating an extra per-component tau_0 factor;
- continue Meta-PBS refinements inside ordinary ring at tau_0+K, versus (K'+1)tau_0 external products per key;
- optimize block one-hot secret selector keys to share a key per block, and use ties-to-even gadget rounding to remove specific half-up FFT-grid bias;
- report, in *their* TFHE-rs derived implementation and configuration, 16bit negacyclic LUT 196ms one-thread under 128bit computational security with model-predicted DFR <2^-64; general 13–16bit LUT 179–368ms; authors' 3.8–6.6x improvement against WoP-PBS in the same named comparison; approximately 1208MB 16bit key storage; model failure estimates validated where errors observable.
These are from PUBLIC ABSTRACT metadata only; no theorem, specific key byte layout, exact operation count proof, detailed threat model, real DFR certificate or source implementation independently audited. Repeated GitHub Notes get_eprint_paper("2026/2616") = RETRIEVAL_BLOCKED official ePrint 403 / no authenticated matching PDF. `papers/supplied` listing has no 2026-2616.pdf. `2026/2618` CI-CKKS and `2026/2513` shaped rounding original PDFs also blocked; no guesses about their methods beyond public author abstracts. Do not claim all these papers are 'insecure' or can be modified trivially for lower memory; 128bit computational security and 2^-64 model DFR are distinct notions.

## [DECISION] H42 direct novelty failure

The exact central dataflow and merged public key switching are literally the named contribution of 2026/2616; independently proposing "module-to-ring descent, rank paid once" is NOT a new idea. This is a direct public-abstract novelty rejection even before the complete technical construction is independently read. It does NOT mean the new paper's correctness/security is independently proven by this assistant, or a lower bound that no other construction can improve over it.
No source-supported "new mechanism" identified at this stage. To invent genuinely new FHE source-dataflow in the large-LUT regime must meet ALL: (i) novel algebraic operation/representation distinct from Descent-PBS author truncation and key switch; (ii) proof of decryption correctness/secret security/noise and real failure target; (iii) same-parameter end-to-end key/RAM/latency and DFR performance vs 2026/2616. No Codex absent a new candidate.

## [FACT] Full-source older packed Functional Bootstrapping: expensive stage verified

Dongwon Lee, Seonhong Min, and Yongsoo Song, *Functional Bootstrapping for Packed Ciphertexts via Homomorphic LUT Evaluation*, ePrint2024/181, PDF via GitHub Notes get_eprint_paper (cached original mirror 31 physical pages, SHA256 498fb574204ec160cd65b61df86a42dd98c85d0aaeaceed469a65c01d1cafa95, VERSION_UNVERIFIED), original pp25–27 Table1/2/3, was read directly. Scheme bootstraps from CKKS ciphertext into FV and has `Slots2Coeffs → ModSwitch → Coeffs2Slots → EvalLUT` flow. The benchmark Table2 for delta/sign LUT (one particular implementation/hardware, NOT a TFHE/Descent/PBS configuration) reports:
- ID I: S2C 0.03s, ModSwitch 2.5s, C2S 0.6s, EvalLUT44.2s, TOTAL47.3s. Stage timing sums=47.33 due published rounding.
- ID II: S2C 0.2s, ModSwitch4.0s, C2S1.5s, EvalLUT166.5s, TOTAL172.1s. Stage timing sums=172.2 due independent source rounding.
Author prose says LUT eval dominates ~93–96%; actual ratios using listed TOTALS are 93.446% and 96.746%. This is evidence about ONLY these two 2024/181 benchmarks and must never be transferred as a universal fact about BatchBoot, Descent-PBS or CKKS in general.

## [DERIVATION + TOY_NUMERIC] Amdahl headroom for 2024/181 non-LUT optimization only

For fixed source baseline T and reported EvalLUT E, if we make all *non-EvalLUT* work free while leaving EvalLUT unchanged, optimistic speedup bound is T/E. From source data:
 ID I: 47.3/44.2=1.0701357466x, so even total elimination of linear transforms and modswitch saves at most about 6.55% of the measured baseline time;
 ID II: 172.1/166.5=1.0336336336x, at most 3.25% of baseline time.
For whole-bootstrapping ≥2x on SAME implementation while leaving non-EvalLUT unchanged, the EvalLUT stage must be reduced at least
  r ≥ 0.5*T/E,
i.e. 53.507% ID I, 51.682% ID II. (These reductions are not a constructive algorithm or claims about asymptotic lower bounds.) Both examples are approximate because published stage table rows sum slightly differently from totals; total values used per source.
This is source-specific Amdahl arithmetic, not a theoretical impossibility for other packed FBT dataflows. In 2024/181, merely sharing rotations/FFT outside EvalLUT cannot plausibly yield dramatic 2x speedup. Authors themselves mention existing BSGS, Paterson-Stockmeyer, and Okada et al. polynomial-evaluation speedups; do not count basic polynomial evaluation speedups as fresh original contributions.

## [OTHER PREVIOUS P0 EVIDENCE] Avoid repeated low-value "new" ideas

The P0-38 portfolio and P0-39–41 record shows failed genuine originality gates for BatchBoot 4 one-hot selector complement (source has ordinary/tagged secret mismatch), Gentry–Lee ciphertext-component Karatsuba (four separately secret-tagged products), and CKKS output-only Gaussian noise (statistical precision conflict). Descent-PBS now directly occupies another high-upside direction. Fresh Oct2026 ePrint pages suggest other recent CI, shaped rounding, compact multi-key constructions but full source blocked, and abstracts alone cannot authorize deep derivations. Simple Amdahl/degree/TV/one-hot toy outcomes should not be multiplied into artificial claims of researcher progress.

## Scientific conclusion and PI review request

PASS primary source prior-art triage, FAIL new mechanism. After **42** P0-PRESCOUT rounds there is still no original PURE-FHE cryptographic construction simultaneously supported by novelty, proof/noise/security, and measured or convincingly modeled end-to-end material benefit. Declare `STAGNATION / HUMAN_REVIEW` rather than autonomously launch P0-43 or produce more small algebraic modifications.
Possible future HUMAN choice:
- Procure full first-party 2026/2616 Descent-PBS, 2026/2618 CI-CKKS and 2026/2513 shaped-rounding PDFs, and then invest in ONE clearly distinct high-value algorithmic bottleneck with nearest novelty gate;
- Direct original Pure-FHE from fresh major problem/top-level algorithm goals rather than adjacent incremental speed tweaks;
- If publication speed matters more than Pure-FHE construction, PI may prefer separate preexisting BOOT/SHIP tracks, but DO NOT automatically reopen or merge them.

No runnable experiment, no Codex task justified today, and no claim that earlier pure-FHE negative results are original theorems.

END_OF_ITERATION:
STATUS: FAIL_H42_NEW_DESCENT_MECHANISM_NOVELTY / PASS_2024_181_AMDAHL / STAGNATION_HUMAN_REVIEW
RESULT: The appealing module-to-ring paid-once method is already Descent-PBS' central contribution (public author abstract, full PDF blocked). Original packed FV-FBT source table shows non-LUT-only work ≤3.25–6.55% of measured baseline time and max perfect removal speedup 1.034–1.070x.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: HUMAN_REVIEW choose one materially different sourced crypto mechanism; if only Descent/CI/shaped-rounding paper claims are available, request exact original PDFs to unlock real novelty audit. P0-43 remains NOT STARTED; no auto iteration/implementation.
STATE_UPDATE: YES only the isolated file; global root and other tracks unchanged.
CODEX_REQUIRED: NO. All engineering and native tests PENDING PI explicit authorization.
