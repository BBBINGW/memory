# BOOT-B066: Published NTRU gadget parameters — implementation availability and two repair models
DATE: 2026-10-20
TRACK_ID: BOOT
STATUS: PASS_DOCUMENT_PARAMETER_INCONSISTENCY / PASS_MATH_REPAIR_GATES / BLOCKED_AUTHOR_IMPLEMENTATION / UNCLEAR_REAL_DFR_SECURITY_AND_PERFORMANCE
SHIP: PAUSED; no other track writes.

## Primary hypothesis
Dai et al. (2026) publicly provide sufficient source evidence to reconcile their Table 4 gadget B,d,Q with the centered exact decomposition stated in Section 2. If not, test both minimal exact-length and scaled-approximation representations before any claim about their actual implementation.

## Verified paper locations
[FACT] Yiran Dai, Binwu Xiang, Yi Deng, Jiang Zhang, "Accelerating MKFHE bootstrapping via parallel-friendly NTRU-based blind rotation", Cybersecurity 9:136 (2026), official https://link.springer.com/content/pdf/10.1186/s42400-026-00563-w.pdf .
Printed PDF p5: h_B:Z_Q -> Z_B^d with gadget G=(1,B,...,B^(d-1)), centered a_i in (-B/2,B/2] and intended a=sum_i a_i B^i mod Q. Theorem1 further asserts Gaussian sampling with exact modulo Q reconstruction. The paragraph allows approximation epsilon but does not specify a large enough epsilon and changed scaling mechanism matching Table4. p13 Table4: 100-bit N2048 Q2^32 B16 d4; 128-bit N2048 Q2^32 B8 d5; p13 Table5 symbolic polynomial multiplication count 2knd²+(3k²+5k)ld; p14 Table6 parallelism P=k*l*d uses these same d values. Therefore an isolated Table4 typography error is not independently established.
[SOURCE STATUS] The official paper Data availability states data held by authors and available to researchers on demand. Direct GitHub repository search for precise paper title and author/MKFHE and targeted public web searches returned no identifiable author implementation. This is NOT proof the original code is unavailable; no binaries/author code have been inspected, and there is no demonstrated real-code bug.

## Primary mathematical falsifier
[DERIVATION] Each of d centered digits has exactly B options, thus any unscaled bounded-digit gadget image contains at most B^d modular values. With Q=2^32, Table4 has B^d=2^16 and 2^15; cannot support exact reconstruction of all a mod Q. The natural truncation of centered balanced digits for a=Q/2 returns 0 in either case, violating even the scalar identity external-product reconstruction by Q/2. The latter is a test of the natural truncation model, NOT author code.

## Candidate repair A — ordinary full-length exact decomposition
Retain same unscaled G and Q; minimum d=ceil(log_B Q)=8 (base16,100-bit) and 11 (base8,128-bit). 10,000 sampled modular coefficients per row all exactly reconstructed by full-length centered digits. Hypothetical Table5 costs for k2: 100-bit n560 l8, source d4 36544 versus corrected d8 144768 (=3.96x); 128-bit n572 l4, source d5 57640 versus corrected d11 277816 (=4.82x). Abstract symbolic operations, not author runtime, actual security/noise/DFR unverified. Larger d also changes BSK sizes.

## Candidate repair B — scaled approximate gadget
If keeping short d, define Delta=Q/B^d (65536/131072), G_Delta=Delta*(1,B,...,B^(d-1)); quantize a to nearest multiple Delta, then decompose quantized quotient modulo B^d. This works coefficientwise with |epsilon|<=Delta/2 (32768 or 65536), but **both gadget vector and key material must change**. Theoretical per-coefficient uniform modular quantization error RMS approximately Delta/sqrt(12), 18918.61 and 37837.23. 10,000 uniform samples per row: empirical RMS 18966.70 and 37809.06, all within stated max error; these are **scalar** results. Rounding only a while retaining original G yields at a=Q/2 values 32768/16384, not Q/2. The scaled output has additional deterministic error and cannot silently inherit paper Lemma2–4 or the Table5 cost/noise guarantees; full FHE noise correlations and DFR unknown.

## Reproducible test
[TEST] Python b066_gadget_repair_gate.py: 10,000 random full-length exact reconstruction checks plus 10,000 scaled-nearest coefficient reconstruction checks PER row; all PASS. Original unscaled truncated identity at a=Q/2 FAIL. SHA256 script 95065b586121e69ca8ec3d72e1ad29e2f4e2cc6e9ff07767e348c94055ec97f5; result b066_repair_gate.json SHA256 bab2523cf34585b2ba4f1c2693a65a97986396100709e1068b0bb2ca3ec718ca.
Local full report/scripts/logs in BOOT_B066_handoff.zip.

## Research conclusion and stopping condition
PASS: Table4 incompatible with the paper's globally exact *unscaled* centered gadget. PASS: both mathematical alternatives can repair scalar representability, but they fundamentally alter operations or error/noise assumptions.
BLOCKED: no authoritative original implementation from author, so DO NOT assert published binaries have a correctness fault, security break, fabricated timings or DFR failure.
This is **documentation reproducibility evidence**, not a new Bootstrapping primitive.
NEXT_TEST: obtain author implementation or clarification of actual gadget h, G, key generation and runtime Table4 d (author says data on request). Without it, park this audit; do not spend endless rounds guessing.
For BOOT next B067, pivot to a new primitive with one small falsifiable hypothesis rather than recycling B063–B066. SHIP unchanged.
STATE_UPDATE=NO: Research GitHub Notes read_repo_file for existing findings/boot-STATE.md has returned {}; preserve original 187967B state and use append-only new findings record.