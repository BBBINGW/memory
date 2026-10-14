# Nested RNS N01 — Algorithm 4 / Theorem 7 rules out the old lazy-CRT-wrap example

**Date:** 2026-10-14 Asia/Tokyo. **Independent new parent:** Boneh–Kim Nested RNS integer FHE. N01 COMPLETED; N02 NOT STARTED. This is NOT continuation of PARKED SHIP-M17–M19 or concurrent SHIP I220 and vFHE V-series.
**STATUS:** PASS exact source-guard implication; FAIL transfer of P21 prior wrap witness to Theorem7; UNCLEAR full encrypted correctness/noise/security, source version and novelty. No original-paper flaw or attack alleged.

## Read before write / source provenance

Read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, global STATE.md SHA 7af97fb3ee38ae139fd12f867fd9eccb18d22d16 (separate vFHE), parallel findings/ship-memory-STATE.md SHA bc0c34db4b3b0ed1b012588883f16835240beb3d (separate I220), prior findings/ship-memory-M19-fixed-depth-radix-group-cost-frontier.md SHA 1f1429e034614a1a3ae78b4f2b00211658f133ef and findings/OPEN_RESEARCH_BRANCHES.md section P21 SHA e3b7e7b1d65c0b2d18bce65e5ec0ce55110fc98b. M19 had parked radix micro-audits. P21's previous counterexample was to an assistant-proposed shortcut, NOT a claimed author theorem failure. Do not overwrite any of those files.

**Primary source:** Dan Boneh and Jaehyung Kim, Homomorphic Encryption for Large Integers from Nested Residue Number Systems, IACR ePrint 2025/346. Connected Research MCP full mirror READY (31 physical pages), PDF SHA256 7a26e911b00368dace336f4324e8e3f036927a57683cf5fbea1e26ee19777ef5, VERSION_UNVERIFIED. Inspected physical p15 Theorem2 HPS integer bound, p16 Algorithm3, p17 Theorem3 lazy output, p18 Definitions7/8, p19 layered setting, pp20–22 Theorem7/Algorithm4 with detailed input and modulus restrictions. PDF extractor warns mangled math glyphs/control chars on pp17,21,22; official PDF URL robots denied and raw GitHub mirror web cache missed, so rendered screenshot / original edition parity UNAVAILABLE. Do not assert exact adverse source wording without visual verification.

## ONE smallest falsifiable technical claim; ONE decisive test

[HYPOTHESIS N01] The earlier general HPS witness x=-1, p=(37,997), target r=79, for which the lazy integer x'=18485 crosses the centered P=36889 boundary and changes residue modulo r when centered, can still occur within the FULL settings of Algorithm4/Theorem7: max_j r_j^2 << P_notI and P_I > ell*(k+4+sum p_i)/2.

[FALSIFIER] Derive from source conditions that EVERY ideal inner HPS integer x'_j necessarily obeys |x'_j| < P/2, and show the old witness cannot satisfy those conditions for any subset I. Confirm with exact integer/rational HPS arithmetic for an illustrative parameter tuple respecting divisibility and widely separating the inequalities. If passes, reject the extension of the old attack to Theorem7. Do not invent new noise attacks or re-run unrelated toy studies.

## Source facts [FACT] and exact derivation [DERIVED]

Let P=product p_i = P_I * P_notI, T=k+sum p_i, ell>=1, each r_j>=2.

Theorem2 physical p15: the HPS output in integers x'_j = sum_i y_i*[P/p_i]_(r_j) - v*[P]_(r_j), where y_i=[[x]_(p_i)*(P/p_i)^(-1)]_(p_i) are centered, v=round(sum_i y_i/p_i), obeys x'_j congruent x mod r_j and |x'_j| <= r_j*T/4 for a centered input |x|<P/2. Theorem3 physical p17 promises a LAZY ciphertext result modulo P, not a canonical normalized mod-r_j lift.

Algorithm4 Setting physical p21 imposes ADDITIONAL conditions:
(1) max_j r_j^2 << P_notI;
(2) P_I > ell*(k+4+sum p_i)/2 = ell*(T+4)/2.
The qualitative source << implies strict < for any valid concrete instantiation. Thus P_I > T/2. Because r_j>=2 and P_notI>r_j^2>=r_j, P=P_I*P_notI > r_j*T/2. Combining Theorem2 yields

  |x'_j| <= r_j*T/4 < P/2.

Hence for every such ideal inner conversion, center_P(x'_j)=x'_j, and reducing the centered representative modulo r_j retains the correct target residue. The two source assumptions already provide a strong no-wrap certificate. This is a basic implication of the existing published margins, NOT a new theorem or claim of novel FHE security.

### Why the prior wrap example is inadmissible

Original P21 arithmetic: p0=37,p1=997,P=36889,r=79,x=-1. Lazy HPS x'=18485>P/2=18444.5; canonical P value = -18404, target residues differ. That example remains a VALID refutation of the assistant's UNRESTRICTED canonical-lift shortcut.
However even at the most lenient ell=1, P_I must exceed (2+4+37+997)/2=520 and P_notI must exceed 79^2=6241. None of the four I subsets of {0,1} satisfies both. For ell>1 the product threshold is even more restrictive. Therefore the earlier wrap is NOT a counterexample to the actual Algorithm4/Theorem7 theorem.

## One executed exact source-shaped parameter gate

Local actually executed script: /mnt/data/nested_rns_m20_theorem7_wrap_gate.py SHA256 e0fc0d5122c833984d3cc4b1f32958ab7b494a92d93c0838a3c46a676843dd63.
Local JSON: /mnt/data/nested_rns_m20_theorem7_wrap_results.json SHA256 cb83ee1abbe734af8b6e49221873a3e3b2fc12df0383b4a3b21840faa0e630d6.
The filename retained scratch prefix m20, but the independent formal research counter is NRNS-N01, not SHIP-M20.

Illustrative (not a security parameter claim): N=64,k=8,ell=4 (satisfy k|N/2, ell|(N/2)/k), pairwise-coprime primes p=(101,103,107,109,1013,1021,1031,1033), I=(4,5,6,7), target r_j=(19,23,29,31), r=392863 and input x=-1 (with possible output modulus s=2). Exact P_I=1101524533279, P_notI=121330189, P=133648179810877859731, T=4526.
Relative margins P_I/[ell*(T+4)/2] = 1.2158e8 and P_notI/(max r_j^2)=126254; x=-1 corresponds to inner centered CRT residues -1 and |x|/r is ~0.00263 of 1/max_{i∈I}p_i. The paper's << notation remains qualitative; ratios are substantial but not a formal full CKKS noise/precision certificate.

Compute source HPS exactly with Fraction and modular inverses, verifying centered y_i, nearest integer v and unwrapped equality sum_i y_i*(P/p_i)-vP=x. For x=-1, obtained:
  r_j=19: x'=-2034; correct target residue 18
  r_j=23: x'=252;   correct target residue 22
  r_j=29: x'=-1364; correct target residue 28
  r_j=31: x'=4556;  correct target residue 30
All have |x'| much less than P/2 and satisfy Theorem2 bound. Exhaustively checked inputs x in {-1,0,1} against all four targets: 12/12 HPS congruences, bounds, and canonical-P identities PASS. Enumerated prior p=(37,997),r=79 over four I subsets: 0/4 source admissible.

These are exact arithmetic checks, not an encryption/CKKS binary run. They do NOT verify full Algorithm4 errors, approximate Rescale_r, later input-output distribution, decryption-failure probabilities, security, paper novelty or official source edition.

## End of iteration

**STATUS:** PASS theorem-premise internal no-wrap implication, FAIL earlier lazy-wrap attempt within full Algorithm4 source restrictions, and UNCLEAR broader FHE performance/accuracy/security/novelty.
**RESULT:** Algorithm4 has stronger simultaneous P_I and P_notI separation conditions than Theorem3. Together with Theorem2 they preclude the exact wrap that P21 found under the weak assumptions. This particular attack path is KILLED, not the entire paper's research potential.
**NEXT_ACTION:** Only on PI continuation, inspect ONE NEW genuine theorem-critical interface in authenticated Boneh–Kim text (e.g. residual/approximate rescale error propagation under Theorem7) with a nontrivial falsifier, or pivot to a different full-text-verifiable high-value FHE result. Do not repeat canonical-lift toy variations. Confirm rendered source/publisher version before any author-impacting allegation.
**STATE_UPDATE:** YES this independent NRNS-N01 file only; NO writes to global STATE.md, findings/ship-memory-STATE.md, or shared findings/OPEN_RESEARCH_BRANCHES.md. NRNS-N01 is the checkpoint for a future independent next round.
