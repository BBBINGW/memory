# NRNS-N02 — Algorithm 4 / Theorem 7 accumulated-rescale-error certificate

**Date:** 2026-10-14. **Independent Nested RNS stream:** N02 COMPLETED; N03 NOT STARTED. PI repeatedly authorized continuation of the same pending N02 round. **STATUS:** PASS conditional source-theorem integer error certificate; FAIL hypothesized gap *between published aggregate error bound and published P_I threshold*; UNCLEAR completeness of source error bound in actual approximate CKKS operations. No original paper attack or security claim.

## Read before write / separate workstreams
Read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, global STATE.md SHA 7af97fb3ee38ae139fd12f867fd9eccb18d22d16 (independent vFHE), parallel findings/ship-memory-STATE.md SHA 12a77b668003b408381554632c87720c83f0acf2 (independent SHIP I221), and prior findings/nested-rns-N01-algorithm4-theorem7-inner-lazy-nowrap-gate.md SHA 1afbca9b46ef508a849129f58246f3d41a22f1e3. Existing N02 destination absent; no concurrent state modified. N01 KILLED naive canonical lazy-lift wrap under full Algorithm4 margins; N02 tests another distinct interface only.

**Original paper:** Dan Boneh, Jaehyung Kim, *Homomorphic Encryption for Large Integers from Nested Residue Number Systems*, IACR ePrint 2025/346, cached Research MCP 31 physical pages original full mirror SHA256 7a26e911b00368dace336f4324e8e3f036927a57683cf5fbea1e26ee19777ef5, VERSION_UNVERIFIED; read physical pp20–22, especially Algorithm4 Setting p21 and Theorem7's proof p22. PDF extraction has math glyph/control-character warnings: important source expressions not visually checked against authenticated latest edition; original paper wording/source edition cannot be conclusively claimed.

## ONE primary falsifiable hypothesis and ONE decisive test
**[HYPOTHESIS N02]** Under Theorem7's *own stated individual intermediate-rescale error certificate* |e_j| <= (k+Σp_i)/4 and round-and-add error per ℓ-branch rotation sum <=ℓ−1, Algorithm4's requirement P_I > ℓ(k+4+Σp_i)/2 might nevertheless fail to ensure that its aggregate integer perturbation is within P_I/2 for exact Rescale_{P_I} at line7.
**[FALSIFIER]** Derive the true aggregate bound as a rational inequality using precisely extracted pp21–22 assumptions, and calculate one source-shaped example satisfying margin. Show exact quotient recovery for integer multiples of P_I with signed perturbations at the bound; if the margin implies |e'|<P_I/2 reject the hypothesized gap. Test the necessity direction by weakening P_I and constructing an integer ambiguity. Do NOT substitute this for independently certified actual encrypted noise bounds.

## Original source [FACT] and derivation [DERIVATION]
Theorem7 proof p22: after each ideal Rescale_{r_j} of P_I*y_j, represented integer is P_I*y_j/r_j + e_j with |e_j| <= (k+Σp_i)/4 (from Theorem2, conditional validity of prior operations). Rotation-sum rounds an integer to give v approximately, introducing an additional <=ℓ−1 units. For T=k+Σp_i:
    |e'| <= Σ|e_j| + (ℓ−1)
         <= ℓ T/4 +ℓ−1
         < ℓ(T+4)/4 ≡ E.
Algorithm4 Setting on physical p21 requires
    P_I > ℓ(T+4)/2 = 2E.
Therefore, source bounds entail
    |e'| < E < P_I/2.
For a true lifted integer v and an integer perturbation e' with |e'|<P_I/2, center_{P_I}(P_I*v+e')=e' and (P_I*v+e'-e')/P_I=v, so the error lies within the unique centered residue cell. This is a conditional integer rescale correctness certificate; it is already exactly the source's argument, NOT independent cryptographic novelty or an additional source proof gap.
**Precision caveat:** The source excerpt has a written rounding/nearest-integer convention, and real approximate ciphertexts have scale, noise, and CKKS rescale/key-switch effects. The additive e_j inequalities were NOT independently reconstructed from the real complete FHE pipeline; no claim that actual key/error distributions obey them or that ciphertexts satisfy a chosen target DFR. This test audits *logical arithmetic consistency* of Theorem7's stated error allowance with its P_I threshold, not full correctness.

## Actually executed one exact integer certificate gate
Executable source: /mnt/data/nrns_n02_rescale_error_certificate.py, sha256 addb31613afc2ad136ea5d80b1386d6b5568a9cf54e95a3e60f7bb44393b704f.
JSON: /mnt/data/nrns_n02_rescale_error_certificate.json, sha256 1ed95e095b66e2549b00c1f445a9d504efcfb27a50b73634b39db33d0b9441bb.
Illustrative original N01 CRT p=(101,103,107,109,1013,1021,1031,1033), I={4,5,6,7}, k=8, ℓ=4; T=4526, P_I=1101524533279. One-branch bound T/4=1131.5; exact ℓ-branch coarse bound ℓ*T/4+(ℓ−1)=4529; source E=ℓ*(T+4)/4=4530; target 2E=9060, so P_I/2>>E. Exact integer centered CRT quotient recovery for v∈{-3,-1,0,1,7}, e∈{-4529,-1,0,1,4529}: 25/25 PASS.
Constructed a weaker illustrative modulus P_I_weak=9057 and perturbation e'=4529 within the source numerical aggregate upper bound, whose magnitude exceeds P_I_weak/2; centered remainder/quotient extraction fails. This shows the sufficient margin is meaningful, NOT that the bound 2E is tight or that such an actual source error is attainable.
No compiled FHE, ciphertext encryption, measured error, authors' code or 128-bit security analysis executed.

## End of iteration
**STATUS:** PASS conditional Theorem7 integer arithmetic and cited bound; FAIL claimed vulnerability from source's aggregate error exceeding its own threshold; UNCLEAR real CKKS bounded e_j premise, version and cryptographic correctness.
**RESULT:** Theorem7 explicitly uses P_I>2E where E=ℓ(T+4)/4, and the individual stated bounds yield |e'|<E. Thus the N02 aggregate integer-rescale arithmetic does NOT reveal a flaw; changing target to new recurrence ideas absent additional source evidence would repeat low-yield microaudit.
**NEXT_ACTION:** PARK further P21/N01/N02 canonical-lift and coarse-error-budget variants; on PI continuation choose ONE independent, nontrivial and primary-source-verifiable FHE mechanism (e.g., authors' CKKS cleaning parameter failure or other paper), or examine exact quantitative e_j cryptographic correctness only when source-backed realistic error model and code are available. No public error or disclosure allegation.
**STATE_UPDATE:** YES standalone N02 file ONLY. DO NOT modify global STATE.md, parallel SHIP state or OPEN_RESEARCH_BRANCHES.md; PI retains pivot decision.
