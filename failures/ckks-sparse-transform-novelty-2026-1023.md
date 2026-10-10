# Iteration 45 — Sparse CKKS CtS/StC prior-art audit: Zheng ePrint 2026/1023

Date: 2026-10-10
STATUS: FAIL for the hypothesis that exploiting sparse-slot repetition to make CKKS CoeffToSlots / SlotsToCoeffs cheaper at depth 1 is unaddressed in current literature. There is directly relevant prior art; whether *LCR+AKS specifically* composes with Zheng's technique remains OPEN, NOT solved by this audit.
Novelty judgment: stand-alone sparse Fourier/trace/repack concept VERY LOW; LCR+AKS combination UNKNOWN pending full-text comparison.

## Research discipline and background
Read AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md, and the previous I44 archive before starting; retain user's parked RIG-HE STATE.md unchanged. I40–I44 branch had:
- exact algebraic Fourier trace projection F^-1 S_t = D_t F^-1;
- bit-reversal-aware pruning;
- two-rotation real/imag repacking and reuse of ordinary rotation keys;
- extra nominal switch events (31 vs 21 in the particular N=4096,t=4 source model);
- asymmetrical CtS.LogSlots=11 / StC.LogSlots=9 + Trace bypass impossible without patching the author Lattigo's constructor and ModUp path;
- NO real CKKS ciphertext-level run due missing Lattigo modules and network. Decision at I44: keep branch low priority, no more nearby plaintext toy checks.

## Single hypothesis and decisive test
[HYPOTHESIS — FALSIFIED] For sparse CKKS, leveraging repetition of the meaningful small slot vector to obtain cheaper depth-1 CtS/StC plus end-to-end bootstrapping advantage is a currently uncovered technique/target.
[FAIL CONDITION] Identify a public pre-existing paper that specifically uses the repeated slot pattern to optimize both transforms, supplies formal complexity and EvalMod-range analysis, and implements FHE bootstrapping. Cheapest decisive test is a *targeted prior-art publication and abstract/claim check*, not implementation.

## Newly identified prior work, exact source and limitations
[FACT, VERIFIED FROM PRIMARY ABSTRACT ONLY] Xiaopeng Zheng, *Faster CoeffToSlot and SlotToCoeff for Sparsely Packed Ciphertexts with Application to CKKS Bootstrapping*, IACR ePrint **2026/1023**, https://eprint.iacr.org/2026/1023. ePrint record states initially approved 2026-05-24, thus predates these research iterations.
- Author states the method **exploits repeated slot pattern itself**, instead of only using smaller effective dimension.
- Let N denote ring dimension, n/2 the effective slots, and r=N/n. For each of CtS and StC at multiplicative depth 1, abstract gives:
  if n <= r/2: 1 plaintext-ciphertext multiplication and O(log n) rotations;
  if n > r/2: (2n/r) plaintext-ciphertext multiplications and O(sqrt(2n/r) + log r) rotations.
- Author further claims a sub-Gaussian range bound for *auxiliary slots* of the revised CtS layout, enabling usual logarithmic EvalMod union-bound margin. This is an important correctness/precision issue NOT checked by I40–I44's ideal algebraic repacking tests.
- Author reports OpenFHE implementation and, for N=2^16 with effective slots <=1024, 3.53x–7.95x faster CtS/StC vs OpenFHE depth-1 sparse transform baseline, and 1.71x–5.28x whole-bootstrapping improvement. These are **author-reported** for this distinct parameter regime; not independently reproduced and not portable to our fixed N=4096,t=4 cost model.
[FACT, SECOND SOURCE] Curated openfheorg/awesome-openfhe GitHub README lists this specific work among ASIACRYPT 2026 publications that have OpenFHE implementations and notes new algorithms not necessarily in the official OpenFHE distribution: https://github.com/openfheorg/awesome-openfhe .
[RETRIEVAL LIMITATION] Research MCP `get_eprint_paper("2026/1023")` returned RETRIEVAL_BLOCKED (ePrint PDF HTTP 403, alternative mirror not available); web PDF click also HTTP 403. No parseable PDF was acquired, no original theorem/algorithm pages independently read. Claims above derived solely from the officially published ePrint abstract and curated implementation directory. **DO NOT CLAIM** we inspected the construction proof, exact FFT factor sequence, key-switch timing, source implementation, theorem numbers, or interactions with LCR+AKS.
[SOURCE] eprint 2026/1023 HTML abstract accessible in web; official record eprint page https://eprint.iacr.org/2026/1023; conference classification OpenFHE curated repository.

## Rigorous scope separation
[NEGATIVE] The generic novelty premise “efficient depth-1 sparse CtS/StC from repeated slots with implementation-level gains is open” is falsified. This new ASIACRYPT 2026 prior art sets a strong relevant baseline. I40–I44 did NOT demonstrate a new nontrivial reduction mechanism, and performed no end-to-end CKKS test; they cannot be framed as an independent publishable algorithm based solely on trace, bit-reversal pruning and repacking.
[NOT PROVED] Zheng 2026/1023 is NOT established as computing the identical Fourier-projection/pruned-full algorithm used in I40–I44. We cannot say it already composes with Yan et al. PKC 2026 LCR+AKS (ePrint 2025/1403), removes pre-first-LCR key switching, saves a modulus level, or dominates our candidate at the fixed N=4096,t=4.
[REGIME CAUTION] Substituting N=4096,t=4 with effective slots m=512 => n=1024, r=4 places Zheng's formula in the second branch (n>r/2), with 2n/r=512 plaintext-ciphertext multiplications and O(sqrt(512)+log 4) rotations per transform as a *formal expression*. This is a different cost unit from I41's ~31 vs21 nominal key-switch events and does not imply dominance or non-dominance for this setting. Author performance numbers are at ring N=2^16, not N=2^12.
[RESEARCH INTERPRETATION] A potential narrowly scoped gap remains: compatibility of a genuinely fast sparse transform (Zheng 2026/1023 or another) with Yan et al.'s first-factor LCR+AKS, especially the condition that input unreduced integer lift is small before any automorphism/key-switch and the behavior of auxiliary slots under EvalMod. But with 2026/1023 full text blocked, no new mechanism/viability/novelty for that composition is established. Further toy loop repeats would be low value.

## End of iteration
STATUS: FAIL for novelty of generic repetition-exploiting sparse transform; HUMAN_REVIEW warranted before further work on the LCR composition.
RESULT: Found direct 2026 paper with matching sparse CtS/StC bottleneck, depth-1 low-cost transformations, sub-Gaussian auxiliary-slot analysis, and OpenFHE measurements. Corrected research baseline and prevented redundant optimization work. PDF unavailable, so only verified abstract-level claims; no theorem-level overlap asserted.
NEXT_ACTION: Suspend I40–I44 and do NOT benchmark or develop the prior pruned-full candidate. For an independently executable next technical audit, use Research MCP to obtain a DIFFERENT fully available modern CKKS/TFHE construction (e.g. ePrint 2025/1786 high-precision bootstrapping), locate one concrete theorem-level bottleneck, and test a single falsifiable modification; if revisiting sparse LCR, FIRST acquire full 2026/1023 PDF, then compare exact LCR ordering and noise constraints before any test.
STATE_UPDATE: NO (unrelated parked RIG-HE STATE.md unchanged).
