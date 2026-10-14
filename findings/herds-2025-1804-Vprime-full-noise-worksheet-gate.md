# HERDS H-HERDS-03 — Table 3 V′ k=32 128-bit-labeled Lemma 5–7 approximate noise-margin worksheet

**Date:** 2026-10-14 Asia/Tokyo. Independent HERDS source audit (third round after H-HERDS-01 trace / H-HERDS-02 fixed gadget length). PI said continue. **Read before write:** START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, global STATE.md (concurrent vFHE V23 READ ONLY), both earlier HERDS finding files, and SHIP workstream state context read-only. No changes to frozen global I192, vFHE/SHIP, original paper, source code or related backlog.

## Exactly ONE primary falsifiable hypothesis and ONE cheapest decisive test

**H-HERDS-03:** For HERDS' concrete **Table 3 set V′** (k=32 parties, **claimed/estimated** λ128, q=2^64), applying the authors' **full three-stage approximate noise variance expressions from Lemma 5/6/7**, with all actual distinct gadget parameters rather than a toy single-component asymptotic formula, produces **6*σ_out/q >= 1/16**. If so, the displayed parameter set would fail to satisfy the paper's own Theorem 1 six-sigma output-noise diagnostic *as certified by those approximate formulas* (not automatically be incorrect in experiments).

**ONE decisive test:** Retrieve source p16 Lemma5, p18 Lemma6, p19 Lemma7 and Appendix B.7 pp41-42, and p26-27 Table3. Convert beta torus to coefficient units sigma_key=beta*q, evaluate those *source-given upper/approximate expressions* with exact high-precision Decimal. The falsifier is an output noise ratio strictly below 1/16. Do NOT treat 1,000 successful decryption trials as proving negligible DFR, and distinguish paper's author-estimated λ128 hardness from independently certified 128 bits.

## Primary source [FACT + provenance]

Binwu Xiang et al., **HERDS: Multi-Key Fully Homomorphic Encryption with Sublinear Bootstrapping**, EUROCRYPT 2026, ePrint **2025/1804** https://eprint.iacr.org/2025/1804. Public official metadata says last revised 2026-03-04. Full 46-physical-page Research MCP PDF from fixed Github ePrint mirror, sha256 **c08a83cea17b352df1006a7051cee26c133bf92a4212860d3cf28f6b6426e7d7**, mirror source revision **d68d3723d26dc2978fcb8f0506946a6314eca0c9**, **VERSION_UNVERIFIED** vs the official current version and publisher PDF. Read physically numbered p16 Lemma5, p18 Lemma6, p19 Lemma7, p21 Theorem1, p26 experimental setup, p27 Table3, pp40-42 Appendices B.6/B.7. Text extraction can scramble precise mathematical glyphs and superscripts; the formula below is a careful but NOT publisher-version/visual-authenticated transcription; do not allege a proof defect on it. Original Code repository linked in p26: https://github.com/SNUCP/mktfhe-parallel-go ; not run locally.

**Selected source V′ parameters:** k32, n636, N2048, q2^64, packed-RLEV length d8, block length ell2, BRK B_br=2^9,d_br=4, TRK B_tr=2^5,d_tr=8, hybrid pk/rlk B_r=2^4,d_r=10, torus Gaussian noise beta=4.4e-16. q divisible by each B^gadget_length (BRK 2^36, TRK 2^40, pk/rlk 2^40). The source calls this a 128-bit-security **estimate**, NOT an independently audited security proof. The assumption that the BRK/TRK/pk/rlk coefficient-noise stddev is **beta*q** is explicit and not independently source-code-verified.

## Reconstructed noise equations [DERIVATION conditioned on source transcription]

Let sigma_key = beta*q; eps_br=q/B_br^d_br; eps_tr=q/B_tr^d_tr; eps_r=q/B_r^d_r. All noises here are **coefficient integer units modulo q**, not normalized torus units.

**Lemma 5 p16:**
`V_br = d_br*n*N*B_br^2*sigma_key^2/3 + 2*n*(N+1)*eps_br^2/(3*ell)`.

**Lemma 6 p18:**
`V_ms=(N+1)/12; V_ks=d_tr*N*B_tr^2*sigma_key^2/12+N*eps_tr^2/3; V_RLEV=V_br+d^2*V_ms+(d^2-1)*V_ks/3`.

**Lemma 7 p19, Appendix B.7 pp41-42 (approximate bound):**
`A= d_r*N*B_r^2/12; C1=(k*(k-1)/2)*N+k; C2=k^2*N+k;`
`V_out = C1*(A*V_RLEV + eps_r^2/3) + C2*A*sigma_key^2`.

Note the paper describes its Lemma7 variance as **approximately bounded** and B.7 states it simplifies by neglecting part of gadget decomposition error under adjustable parameters. The source `q/16` is a **six-standard-deviation heuristic** on the approximate noise model; it is not a rigorous DFR tail certificate. This worksheet *does* include the displayed eps_r approximation term; no hidden zero assumption about it. **Do not assert the actual measured scheme reaches this output SD; it is a model evaluation.** The potential additional coefficient extraction and final key switching beyond source's core bootstrapping proof are not included.

## Executed reproducible high-precision arithmetic [COMPUTED]

Using Python Decimal with 70 digit precision, independent of random samples, from exact integers / exact beta decimal:
- sigma_key = 8116.56739243220271104 coefficient units;
- sqrt(V_br) = 177005498533.0910;
- sqrt(V_ks) = 438458309.4802102;
- sqrt(V_RLEV) = 177016902216.7665;
- sqrt(V_out) = 117929301717696097.8798;
- **6*sqrt(V_out)/q = 0.03835776153660739171217 < 0.0625 = 1/16**;
- headroom factor `(1/16)/(6*sqrt(V_out)/q) = 1.62939643754633717`; used model six-sigma budget ~61.37%.
- At these parameters Lemma7's amplified input RLEV variance contribution dominates (~0.99999999999999566 of its displayed output variance), the fresh hybrid relinearization key error is negligible in this particular model; this is not a general dominance theorem.
- All three B^gadget_length divisibility conditions PASS.

Reproducible actual files created in container and validated by running script:
- `/mnt/data/herds_H03_Vprime_noise_worksheet.py` SHA256 `f5cc889744ea6eb6615a9b0872b6792df80f23d294a087a0db8dc85e1d3ce27a`
- `/mnt/data/herds_H03_Vprime_noise_worksheet.json` SHA256 `4ed8a93f992cdf189ef46c127061904976b53acb80b5f5ad2f971d1f6b4e2649`

**STATUS:** **FAIL H-HERDS-03** the asserted violation of *this approximate Lemma5–7 model's* six-sigma cutoff. **PASS** source-specific V′ transcribed arithmetic and component parameter/divisibility checks, conditional on correct reading and noise-unit mapping. **UNCLEAR** source final PDF parity, real output DFR, joint noise correlation, omission assumptions in Lemma7, extra final extraction/key switching, security hardness estimator parameters, real code agreement. No original HERDS correctness attack or novelty established.

**RESULT:** The actual V′ 32-party parameters have a modeled 6sigma/q of ~0.03836, below 1/16 by factor ~1.63. This is a substantive *negative technical check*, not an endorsement of 128-bit security. Prior H01/H02 negative suspicions likewise stand independently. The paper's noise formulas, under its displayed assumptions, do NOT immediately contradict its V′ example.

**NEXT_ACTION:** PARK further blind source arithmetic of related rows without fresh mechanism. Any meaningful further audit should source-authenticate rendered Lemma7 and verify against a **pinned actual author Go implementation** (sampling precision and noise unit, exact TRK and pk/rlk parameter mapping) or compute an independent joint-security/DFR certificate. If either required artifact unavailable, return HUMAN_REVIEW and select a different FHE hypothesis; do not call 1000 no-failure tests a DFR proof. No need to add another iteration for the same worksheet. **NOVELTY NOT VERIFIED.**

**STATE_UPDATE: YES** this isolated HERDS finding only. **NO** edits to global `STATE.md`, independent SHIP state, active vFHE state, or upstream.