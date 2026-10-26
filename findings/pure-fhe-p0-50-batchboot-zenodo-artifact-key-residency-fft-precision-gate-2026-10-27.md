# PURE-FHE · P0-PRESCOUT-50 — Official artifact source gate, key-residency break-even and prepared-FFT obstruction

DATE: 2026-10-27 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: BATCHBOOT_TWISTED_RGSW_DERIVATION
PREVIOUS: P0-PRESCOUT-49 — findings/pure-fhe-p0-49-batchboot-author-artifact-vs-independent-tfhepp-key-layout-source-gate-2026-10-27.md; commit bfc72975970372344548efa526676102900c595d
LATEST_COMPLETED: P0-PRESCOUT-50
NEXT_ITERATION: P0-PRESCOUT-51 NOT_STARTED, requires qualitatively new source/proof/PI review
STATUS: FAIL_OFFICIAL_ARTIFACT_ACCESS / PASS_CONDITIONAL_KEY_RESIDENCY_BREAK_EVEN / FAIL_UNCONDITIONAL_NATIVE_SAVINGS_CLAIM / PARK_RESEARCH_CANDIDATE
NOVELTY: NOT_ESTABLISHED. No new original FHE construction, DFR guarantee, performance measurement, or independent storage break.
CODEX_REQUIRED: NO. No Codex, native benchmark, compile, downloaded binaries, remote, keygen, or infrastructure changes authorized.
STATE_UPDATE: YES only this isolated PURE-FHE finding; do NOT edit root STATE.md or other SHIP/BOOT/CGS/VFHE/EAI research lines.

## One H50 and cheapest decisive test

H50: The AUTHOR'S official, released BatchBoot artifact should provide source-complete evidence that the 6-bit bootstrapping keys contain independently stored FOUR ordinary plus THREE twisted FFT-prepared RGSW ciphertexts per grouped selector, and that an on-demand public automorphism+key-switch rewrite offers *net* peak RAM / total evaluation key memory headroom after a NEW Auk_tau, transient materialization, inverse/forward FFT and noise/security costs. Test author artifact access first, inspect source if accessible; else derive ONLY explicit, conditional no-free-lunch memory and compute inequalities from separately pinned independent TFHEpp implementation, then PARK if neither evidence nor new mechanism emerges.

## [FACT] Official author source available as a URL but not accessible as CONTENT

- Peer-reviewed USENIX Security 2026, Li et al., "BatchBoot: Fast Batched Bootstrapping for TFHE scheme and Practical Applications" publisher page https://www.usenix.org/conference/usenixsecurity26/presentation/li-zhihao ; official prepub PDF https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_li-zhihao.pdf . Previous P0 findings inspected author Algorithms and Table4/13 directly; this P0 did NOT reinterpret unseen PDF formulas.
- Official USENIX 2026 Security Research Artifacts evaluation listing https://secartifacts.github.io/usenixsec2026/results at line for BatchBoot: **Artifacts Available** badge only; no listed **Artifacts Evaluated–Functional** or **Results Reproduced** badge in visible row. Click artifact link resolves to EXACT https://zenodo.org/records/17936945 , DOI https://doi.org/10.5281/zenodo.17936945 .
- This turn attempted web OPEN of https://zenodo.org/api/records/17936945, and artifact results page CLICK to the canonical record; both failed (web access unavailable/cache miss). A separate container-level urllib/requests experiment could not resolve zenodo.org host through available DNS; same for datacite/doi hosts. Neither the author source archive nor even a verified file manifest/checksums were downloaded. Additional search of public GitHub code for exact DOI and source author BatchBoot gave ONLY alternative implementation TFHEpp, not attributable official author mirror. Therefore DO NOT claim 'artifact read', original author's KeyGen/Decom/key byte proportions known, or 120.1MB Table4 exactly itemized.
- IMPORTANT: prior P0-48 confirmed separately cited upstream MOSFHET uses signed radix decomposition {-2,-1,0,1} for b=2 with nonzero digit mean; **not** proof of author's fork. Upstream full-word b2,d32 has a negative bit shift in one key-switch decompose function; this applies to that upstream code path, not published BatchBoot or independent TFHEpp.

## [FACT] Provenance of the alternative independent implementation

Pinned GitHub virtualsecureplatform/TFHEpp@1dd9a1addef4cae01da9bb6bfff0d22b55bec683 (all following direct code facts anchored to that exact Git tree):
- docs/BATCHBOOT.md explicitly says the implementation is independently written based on the publication, copying NO source files from original Zenodo artifact. It gives a separate code origin and implementation limitations. It warns BSK key-shape may leak sparse secret Hamming weight if not fixed as public profile.
- include/tfhe/batchboot.hpp lines 101–111: each BatchEMPDigitKey has direct[4] plus inverse[3], all TRGSWFFT<P>; they are serialized as arrays. Lines 174–240: keygen constructs four ordinary from trgswSymEncrypt and three special directly with the secret τ_-1(s) via BatchTauInverseTRGSWEncrypt, separately sample fresh RLWE encryptions of zero, then ApplyFFT2trgsw; no key-switch derivation. Lines 243–286: one BatchEMPKey per domain sparse secret gap plus one final positive key per nonempty component. Lines 419–481: the online algorithm hoists input decomposition FFT, accesses the stored direct and inverse arrays by output boundary, consumes all needed choices across all outputs and all stages. There is no lazy derivation of inverse keys already implemented in this reviewed version.
- include/tfhe/evalkeygens.hpp annihilatekeygen constructs automorphism exponents (1 << (i+1))+1, NOT explicitly τ_-1 indexed 2N−1; the candidate needs one additional suitable automorphism switching key or a *proven* composition with its own noise/latency cost. Do not claim it already exists.
- include/params.hpp: PolynomialInFD<P>=aligned_array<double,P::n>; TRLWEInFD<P>=array<PolynomialInFD<P>, P::k+1>; TRGSWFFT<P> consists of k*l_a*lbar_a+l*lbar such TRLWEInFD rows. The examined basic case k=1 and all lengths1 has two rows each with two FFT polynomials of 8-byte doubles.
- include/mulfft.hpp lines around 193 and 305: for 64bit torus, TwistFFT invokes execute_direct_torus64 (Fourier→integer torus), and TwistIFFT invokes execute_reverse_torus64 (torus→Fourier). These are numerical double-precision transforms. Converting an *existing Fourier-only stored RGSW* back into coefficient domain to run ordinary RLWE key switching, and then back to FFT, is not a proven exact/invertible ciphertext conversion. The floating precision error of that round trip must be bounded and incorporated into the NEW RGSW row noise / final DFR; no such bound was read. This is a new implementation-specific accuracy obstacle, not evidence of actual catastrophic loss.
- include/tfhe/batchboot.hpp explicit comment: digit-key ciphertexts are separately encrypted across positions because sharing equality of selectors could leak secret digit equality. P0-44 derives special FROM matching ordinary per same digit; it must NOT collapse distinct digit positions bitwise.
- Important: source is ALTERNATIVE implementation and cannot be used to claim paper's reported Table4 120.1MB keys/8.43ms msg, or Table13 1425MB peak RAM.

## [DERIVATION] Exact structural memory break-even under stated assumptions

Assume G independent radix4 digit groups, exactly seven equal-size stored FFT RGSWs/group of R bytes each (four direct and three inverse). Original persistent BSK group storage M_old=7GR.

To remove all THREE pre-stored twisted keys/group and produce at most one group live:
  M_new_peak≈4GR + K_tau + 3R + W,
where K_tau is *additional* new automorphism-key bytes, W is working FFT/KS state and any extra concurrently resident intermediates. All quantities must be same measurement boundary; other unchanged keys/base RAM cancel in the algebraic difference.
Therefore
  M_new_peak < M_old ⇔ K_tau+W < 3(G−1)R.
This is a NECESSARY & SUFFICIENT algebraic inequality *within this simplified residency model*, not a demonstrated total application RSS reduction. If all inverse RGSWs are reconstructed and cached, peak BSK storage returns to ~7GR plus K_tau/W; then serialization/network benefit might remain, but on-line resident RAM may WORSEN.

Illustrative INDEPENDENT TFHEpp source type example ONLY, NOT the actual USENIX implementation:
  k=1, l_a=l=lbar_a=lbar=1, N=4096, double Fourier store => 1 PolynomialInFD=32768B, one TRLWEInFD=65536B, one TRGSWFFT=131072B=128KiB.
  For h=33 and 6 radix-4 positions, assumed G=(h+1)*6=204:
  7GR=187170816B=178.5MiB; 4GR=106954752B=102.0MiB; 3GR=80216064B=76.5MiB.
  If extra tau key were itself a 31-digit half-RGSW FFT key with only one TRLWE row per digit, its *hypothetical* bytes would be K_tau≈31*65536=2031616B=1.9375MiB, but actual new key's type, dimension and needed keygen security/row variants are NOT implemented or verified. The transient THREE inverse RGSWs add 393216B=0.375MiB. Before W, such an ideal configuration would save about 74.19MiB of these assumed BSK-related objects. Do NOT use this to claim a 74MiB peak RAM measurement or compare it with official 120.1MB source Table4; parameters/layout do not match.
  Another key memory consideration: prepared FFT keys can dominate BSK type footprint but unrelated accumulator buffers/packing KSK/automorphism keys can dominate full RSS. No source-matched itemization exists.

## [DERIVATION] Mandatory online materialization work

Given the same hypothetical G204 and 3 special keys/group, 3G=612 on-demand inverse RGSWs per full batch. Each RGSW has two RLWE rows for k1, one-digit online BSK gadget length:
  612*2=1224 extra rowwise *RLWE key switches*.
If a 31-digit new Auk_tau key is used:
  1224*31=37944 gadget-digit multiply-accumulate stages, before materialization FFT, buffer allocation, key switching errors and late reuse. Comparing 37944 to BatchEMP full-path 3,342,336 EP calls is NOT a fair runtime ratio: these are different weighted computational primitives, input/output representation, cache behavior, FFT/kernel timings. Actual candidate may derive only selected groups/lazy on demand but needs the three special keys for all relevant output boundary indices at a stage and must rederive if evicted before subsequent uses.
Given TFHEpp stores K+ as TRGSWFFT double, a naive coefficient-only KS requires up to 4 torus-poly conversions per special RGSW (2 RLWE rows *2 polynomials), hence 2448 Fourier→torus transforms and 2448 torus→Fourier transforms for 612 keys, plus KS NTT/FFT data flow. This is an upper count for this straightforward full conversion design, NOT proven fundamental minimum (a fused/compatible Fourier KSK might avoid some, but no such scheme derived).
Double-precision FFT roundtrips may inject representation noise comparable to or larger than native BSK noise; no quantitative certificate. Original P0-45/46 had only matched-noise HYPOTHETICAL sigma_A=2^-53 from mismatched Table9 auxiliary row and independence; P0-47/48 disproved the naive shared-Auk Gaussian independence and identified fixed-key quantifier problem. None of those obstacles solved by the new artifact access attempt.
New τ switching key also changes the evaluation-key security assumptions, may require longer gadget decomposition whose key bytes/timings consume savings.

## Research decision

H50 source-complete net value certification FAILS due direct official artifact inaccessibility and no source-matched full hardware/parameter/security/noise evidence. The independent source supports only a CONDITIONAL raw opportunity. Unlike the apparent 3/7 compression, there is now explicit key-residency inequality, added format-conversion cost, and proof risk. No independent cryptographic primitive, new noise bound for *actual BatchBoot algorithm*, nor measured/validated memory, latency and security outcome obtained in 50 P0 rounds. Treat current P0-44..50 subline as PARK/HUMAN_REVIEW, NOT a ready-to-build crypto idea. Stop redundant Zenodo fetch retries and gadget noise toys absent new evidence. To reopen, user can upload the ORIGINAL Zenodo code archive and ideally benchmark key-size breakdown, followed by exact author artifact source audit and complete key-conditioned DFR + all-keys memory ledger. Any future implementation proposal requires a genuinely new compatible FFT/key-switch fusion or rigorous exceptional conditional tail mechanism with material system headroom, not off-the-shelf aut+KS composition.

END_OF_ITERATION:
STATUS: FAIL_AUTHOR_ARTIFACT_SOURCE_GATE / PASS_CONDITIONAL_KEY_RESIDENCY_BREAK_EVEN / PARK_ON_DEFINITIONAL_AND_PERFORMANCE_GAPS
RESULT: Official Zenodo 17936945 record address and AE Available badge confirmed, source still unread. Independently pinned TFHEpp stores 4+3 prepared RGSW; conditional on-demand residency is beneficial iff K_tau+W<3(G−1)R; naïve derivation has at least 1224 RLWE row transforms and 37944 KSK-digit MAC proxy plus Fourier conversion and noise obligations under toy Boot6-like dimensions.
NOVELTY: NOT_ESTABLISHED.
NEXT_TEST: No P0-51 automatic; source-complete original author artifact or qualitatively new theorem/representation first, then PI review; no CodeX task.
STATE_UPDATE: YES isolated finding only; global STATE.md and unrelated lines unchanged.
CODEX_REQUIRED: NO.