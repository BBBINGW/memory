# PURE-FHE · P0-PRESCOUT-49 — Official BatchBoot artifact versus independent TFHEpp key-layout source gate

Date: 2026-10-27 (Asia/Singapore)
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: BATCHBOOT_TWISTED_RGSW_DERIVATION
LATEST_COMPLETED: P0-PRESCOUT-49
NEXT_ITERATION: P0-PRESCOUT-50 NOT_STARTED; source access or new precise hypothesis required
PREVIOUS: P0-PRESCOUT-48, findings/pure-fhe-p0-48-batchboot-mosfhet-source-digit-conditional-key-tail-gate-2026-10-27.md, commit 17eff4dde1953fb3756a2eaa131d5029d7993c40
STATUS: PASS_INDEPENDENT_BATCHBOOT_IMPLEMENTATION_KEY_LAYOUT / AUTHOR_ARTIFACT_NOT_FETCHED / NO_END_TO_END_DFR_OR_MEMORY_GAIN_CERTIFICATE / NOVELTY_NOT_ESTABLISHED
CODEX_REQUIRED: NO. No Codex, GPU, native tests, compilation, downloads/model setup or infrastructure actions.
STATE_UPDATE: YES isolated PURE-FHE findings only; root STATE.md and SHIP/BOOT/CGS/VFHE/EAI untouched.

## One primary falsifiable H49

Can the AUTHOR-SUPPLIED official USENIX26 BatchBoot artifact confirm that its actual 6-bit bootstrapping key stores independent ordinary/special RGSW rows, with a public Fourier/coeff representation and automorphism-key layout that leaves a measurable cryptographically sound storage advantage for P0-44's on-demand twisted-RGSW derivation? A yes would permit a full noise/online-time/headroom gate. A no (already derived, uncompressible layout, unsafe reuse, too much RAM) kills candidate. Cheapest test: retrieve and read author source first; if unavailable, clearly separate independently written TFHEpp implementation as a *different* evidence tier and list exact remaining obligations; no fake native measurements.

## [FACT] Author artifact exists but CONTENT UNREAD

Publisher USENIX conference: https://www.usenix.org/conference/usenixsecurity26/presentation/li-zhihao .
Publisher prepublication paper, Open Science section, states code at DOI 10.5281/zenodo.17936945: https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_li-zhihao.pdf .
Independent artifact-evaluation listing, 'Artifacts Available' not 'Reproduced': https://secartifacts.github.io/usenixsec2026/results .
Zenodo original archive target https://zenodo.org/records/17936945 and https://zenodo.org/api/records/17936945 returned INACCESSIBLE in web reader this turn. Public searches for a directly browsable mirrored github source did not yield a verified author repository. Therefore the actual author artifact's BSK serialization, transformed key generation, user parameters, exact decomposition and prepared caches remain UNKNOWN, and there is NO author-source DFR/compression claim in this record. Do not silently treat upstream MOSFHET or alternative TFHEpp as the author code.

## [FACT] A separate *independently written* implementation IS AVAILABLE and code was directly read

TFHEpp independent implementation, pinned actual GitHub source commit 1dd9a1addef4cae01da9bb6bfff0d22b55bec683, https://github.com/virtualsecureplatform/TFHEpp/tree/1dd9a1addef4cae01da9bb6bfff0d22b55bec683 .
 docs/BATCHBOOT.md: states implementation independently written from published USENIX algorithms and explicitly *no source file from reference artifact included or copied*. It supports full/sparse functional BatchBoot / half BatchCBS and flags that evaluation-key **shape leaks domain-key Hamming weight** unless that weight is a fixed public profile. Thus it is evidence for implementability/structure only, not author benchmark/DFR.
 include/tfhe/batchboot.hpp, directly fetched full 38K, key lines:
  101–111 `BatchEMPDigitKey<P>` comprises `direct[4]` ordinary `TRGSWFFT` plus `inverse[3]` tau-tagged `TRGSWFFT`, all serializable via cereal arrays.
  115–167 grouped keys hold per-position radix4 digits, and per-secret-component gap vectors (negative_gaps, final_positive).
  174–207 `BatchTauInverseTRGSWEncrypt()` directly constructs special key using known secret target_key: fresh independent zero RLWE rows, if selector is 1 add -tau_-1(s) gadget in the nonce row and +1 gadget in body row, then `ApplyFFT2trgsw`. This is DIRECT native secret-based key generation, not from an existing ordinary RGSW via public KSK.
  210–240 `BatchEMPKeyGen()` selects the one-hot digit and separately calls `trgswSymEncrypt` 4 times, `BatchTauInverseTRGSWEncrypt` 3 times, PER digit.
  243–286 `BatchBootKeyGen()` creates one key per sparse key gap and a final positive key. It does NOT deduplicate across digit positions, by design.
  323–474 in online `BatchHoist/BatchEMP`, input ciphertexts are decomposed and FFT prepared, then each output uses 3 selector EPs selecting either `digit_key.direct[row]` or `digit_key.inverse[row]` plus ordinary `digit_key.direct[3]`; prepared RGSW keys are *already stored* in Fourier format.
 include/tfhe/batchboot.hpp top comment specifically warns DO NOT SHARE selector ciphertext across different digits: equality of secret digits could be visible from eval-key representation. Publicly deriving twisted from original **within the same digit** is different; cross-digit key deduplication is not authorized by this evidence. Reusing the very same shared ciphertext bitwise across independent positions may reveal a secret relation via publicly identical key bytes. This code comment is a security-design rationale, not a separate formal proof or an observed attack.
 include/tfhe/evalkeygens.hpp `annihilatekeygen()` generates automorphism indices (1<<(i+1))+1, not explicit `2N-1` corresponding to tau_-1. This implementation would need an additional direct tau_-1 switching key or another justified composition. Standard automorphism evaluation-key construction is known prior art.
 include/params.hpp actual aliases:
  PolynomialInFD<P> = aligned_array<double,P::n>,
  TRLWEInFD<P> = array<PolynomialInFD<P>,P::k+1>,
  TRGSWFFT<P> = aligned_array<TRLWEInFD<P>,P::k*P::l_a*P::lbar_a+P::l*P::lbar>.
Thus the 7 slots are actual PREPARED Fourier cryptographic objects, not mere metadata pointers.
 Source repo developer v12 release describes BatchBoot functionality but expressly warns that it validates structural constraints only, does not select production cryptographic parameters; do not turn its toy/tests into 128bit security or DFR evidence.
 Public upstream MOSFHET (Antoniocgj) source at commit a6e7fbb... had balanced **non-centered** signed digits in polynomial_decompose_i. That is upstream's code, NOT proof of this independent TFHEpp or official author's Decom implementation. These three source tiers must remain clearly separate.

## [DERIVATION] Illustrative key representation footprint in independent implementation

For toy/conditional exact **type assumption** P::k=1, l_a=l=lbar_a=lbar=1, n=N=4096 and double Fourier representation:
  1 PolynomialInFD=4096*8=32768 bytes;
  1 TRLWEInFD=2*32768=65536 bytes;
  1 TRGSWFFT=2*65536=131072 bytes;
  per digit group=7*131072=917504 bytes (896KiB);
  if there were G=(h+1)*log4(4096)=34*6=204 independent digit groups, 204*917504=187170816 bytes (~178.5MiB) as a raw Fourier key type estimate before alignment/vector/memory allocator overhead.
To persist only 4 ordinary prepared RGSWs, the missing 3 specials represent 3*131072 per group =80216064 bytes (~76.5MiB) of THIS hypothetical baseline, BEFORE adding a direct tau_-1 Auk key, other keys/FFT copies and avoiding stagewise re-materialization costs.
Crucial: this is NOT the verified 6-bit TFHEpp or USENIX run/Key Sizes, which uses its own parameters and shaped secret gaps; USENIX Table4 source Key Sizes=120.1 MB is not directly comparable. The size mismatch proves simply that source type-level counting alone cannot identify the authors' archived format.

## [DERIVATION] Real on-demand path is computationally non-free

P0-44 algebraic relation remains ideal-plaintext correct for constant selectors u:
  K^-_s(u)=KS_{tau(s)→s}(tau(K^+_s(u))) rowwise.
The independent TFHEpp stores K^+ as TRGSWFFT, while standard KeySwitch accepts decomposable torus coefficient ciphertexts. A simple implementation therefore needs (i) inverse Fourier preparation for all K+ rows to get coefficient-domain RLWE (or an equivalent proven fusion), (ii) tau automorphism, (iii) RLWE key switching with NEW matching tau_-1 key (not present in ordinary annihilatekeygen set), then (iv) FFT to produce prepared K^- for the online EMP. Any claim that only the KS cost exists is incomplete. A fused Fourier key-switch may be possible but is NOT constructed, and no actual costs measured.
Retaining all derived K^- to avoid repeated conversions retains essentially the original live RGSW key footprint (only serialized input size shrinks). To reduce resident RAM, must lazily materialize only used digit group/stage, reuse across all outputs at that stage, then evict; this may shift pressure onto extra FFT/scratch and repeat conversions. Different digit positions must receive distinct independently randomized source keys so the evaluator does not learn equality relations. Key material and schedule must respect source fixed weight profile for hiding secret metadata.
The added Auk_-1 changes evaluation-key security assumptions (keys for another automorphism); extra KS noise is key-dependent and shared, requiring joint conditional tail not a copy of original author's DFR.

## [CORRECTION / QUANTIFIER GATE] P0-48 Hoeffding lemma is over *partial key-generation randomness*

Previous P0-48 correctly derived a Hoeffding inequality **conditional on a fixed KSK error vector E**, while treating independent freshly generated BSK masks D_i as random. But once the COMPLETE evaluation-key generation is fixed, BOTH E and D_i are fixed (the row ciphertexts' randomness is not resampled on each query). Therefore its conditional-on-E bound cannot be presented as a *fixed fully published evaluation key* adaptive multiquery DFR certificate. It is a valid averaged-over-remaining-keygen-randomness tail bound under assumptions, not a final security guarantee for all fully generated keys. An actual proof must explicitly quantify over keygen and inputs and show a high-probability good-key event, conditional concentration for input ciphertext randomness (if any), effects of same key repeated across queries, and correlation through actual staged external products. This corrects a scope gap without alleging a published paper bug.

## Strongest possible conclusion in THIS turn

- PASS: an independently written close implementation explicitly stores 4 direct+3 inverse prepared RGSW per digit, and its online code consumes both; simple within-digit derived-key proposal remains a technically meaningful alternative *in this implementation*.
- FAIL_SOURCE: the PRIMARY original author Zenodo artifact remains unread, so no claim about its key layout, implementation digit means, actual key byte savings, or security.
- UNCLEAR: added tau_-1 key storage plus FFT/IFFT/materialization overhead and new joint tails; no DFR pass at 2^-64 and no peak-RAM or latency measurement.
- NOVELTY NOT ESTABLISHED: key switch / tau transforms are long-known; on-demand representation is not yet a publishable scheme or validated improvement, and obvious compression may have prior art.
- RECOMMEND PARK/HUMAN_REVIEW pending author artifact, exact first-party per-key footprint, and a fundamentally different way to share prepared representations or bound key correlations. Do NOT launch Codex/native merely to reproduce key layout when primary author artifact is inaccessible.

END_OF_ITERATION:
STATUS: PASS_INDEPENDENT_KEY_STRUCTURE / FAIL_TO_ACCESS_OFFICIAL_ARTIFACT / UNCLEAR_REAL_RAM_DFR / HUMAN_REVIEW
RESULT: pinned third-party source shows actual 4+3 Fourier keys and direct KeyGen; identifies missing tau_-1 key and coefficient/Fourier preparation cost; fixes P0-48 fixed-key quantifier interpretation; official source blocked.
NOVELTY: NOT_ESTABLISHED.
NEXT_TEST: P0-50 NOT_STARTED: original Zenodo source author KeyGen, decomposition, BSK key-byte breakdown; if source still inaccessible or merely duplicates alternative implementation, PARK and pivot to source-complete NEW cryptographic mechanism rather than toy covariance repeats.
STATE_UPDATE: YES one new isolated finding only.
CODEX_REQUIRED: NO.
