# BOOT-B091 — Bit-Reversal-Conjugated HalfMuxRot via masked KSK, cost and noise gate
Date 2026-10-20 | TRACK_ID BOOT only | unrelated isolated SHIP eval-key-memory line UNTOUCHED.
STATUS PASS_TYPED_MASKED_HALF_MUX / FAIL_KEY_AND_ONLINE_COST / FAIL_TOY_SHORT_INPUT_NOISE / FAIL_NOVELTY / REAL_CKKS_UNVERIFIED.

## Primary falsifiable hypothesis
B090 disproved the idea that merely relabeling encrypted cyclic-rotation indices implements bit-reversal-conjugated rotation. B091 tests ONE stronger interface: use SHIP-style encrypted selector KSK whose encrypted target ALSO contains a public slot mask; use these keys to compute P T_(2^j) P^-1 with no separate online mask-rescale and no added HE level, while maintaining competitive key memory, online cost and low noise. P is bitreverse, T is cyclic CKKS slot rotation.

## Verified original sources
[FACT] Cheon–Hanrot–Kim–Stehlé, SHIP CKKS Bootstrapping, EUROCRYPT2025, ePrint 2025/784 https://eprint.iacr.org/2025/784, original cached full33pp SHA256 3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4, VERSION_UNVERIFIED; physical pp19–23 Definition1, Lemma2, Algorithms3–5 and §4.4: two evaluation-key ciphertexts encrypt selector times rotated secret and selector, to fuse mux with key-switch; column-method masks also already fused.
[FACT] Coron–Seuré PaCo, ASIACRYPT2025, ePrint 2025/886 https://eprint.iacr.org/2025/886, cached full35pp SHA256 ee427d006097fabdbd30a0a4dc36ed09df5ffea68df30a0511cc154b303a936a, VERSION_UNVERIFIED; physical p4 author-open SHIP migration question, pp14–17 bit-reversed S2C sparse butterfly with bit-reversed INPUT. This is the EUROCRYPT SHIP PAPER, not our independent research line TRACK_ID SHIP.
[PRIOR] Poulpy v0.8.3 PaCo slot layout has Natural and BitRevLow variants and folds bit reversal into PaCo transform/key conventions: https://docs.rs/poulpy-ckks/latest/poulpy_ckks/layouts/paco/enum.PaCoSlotOrder.html and https://www.poulpy.dev/docs/paco/. Generic mask/layout folding NOT NEW. CKKS general linear transforms by cyclic diagonals and key switching NOT NEW.

## Exact permutation and arithmetic construction
For n=2^k, define br_k, Pi(v)[i]=v[br_k(i)], T_r(v)[i]=v[(i-r) modn].
phi_r(i)=br_k((br_k(i)-r) modn); D_r={i-phi_r(i) modn}. Indicator public mask M_(r,d)[i]=1 iff i-phi_r(i)=d modn. Exact operator:
  Pi T_r Pi^-1 = sum_(d in D_r) Diag(M_(r,d)) T_d.
For binary step r=2^j, |D_r|=k-j+1 by carry-chain lengths, verified exact for n4..4096. Sum over j0..k-1 gives k(k+3)/2 masked rotated HalfMux and k identity HalfMux: total k(k+5)/2 vs baseline 2k, factor (k+5)/4. At n4096,k12: 90 rotated+12 identity=102 vs24 (4.25x), encrypted key rows 204 vs48 before gadget splitting. This is a count for FULL binary selection, NOT an inherent bound for the authors' experimentally tuned SHIP hybrid window or all possible bootstrapping constructions.

## Typed fused encrypted bit/rotation/mask operator
Use SHIP sign convention Dec_s(a,b)=b+a*s in R_Q=Z_Q[X]/(X^N+1), ct phase=m+e_input, encrypted secret selector beta. Let sigma_d be the automorphism implementing T_d on half-slots, M_d the corresponding ring plaintext. At key generation, independently RLWE encrypt under output key s two high-modulus targets:
  K0_d=Enc_s(Paux*beta*M_d*sigma_d(s))
  K1_d=Enc_s(Paux*beta*M_d).
For public input ct=(a,b) mod Q, produce coefficientwise Round_Paux [sigma_d(a)*K0_d+sigma_d(b)*K1_d] mod Q. Before rounding the decryption phase is EXACT:
  Paux*beta*M_d*sigma_d(m+e_input)+sigma_d(a)*eta0_d+sigma_d(b)*eta1_d  (mod Paux*Q).
Sum over D_r, plus beta-complement identity HMux, yields conditional PiT_rPi^-1 output. These mask factors are carried INSIDE high-modulus key plaintexts, so ideal gate needs no separate mask ct-pt/rescale online stage. It nevertheless needs each masked secret-dependent KSK accumulation, adds evaluation-key memory, and transports input noise through M_d. Its KDM/circular security has NOT been proven; independently uniform public masks alone do not imply security.

## Reproducible toy, independent checks
In /mnt/data/boot_B091/verify_b091.py: standard Python, deterministic seed910271; small negacyclic N16, q65537, auxiliary Paux=2^32, 8 CKKS-like slots, exact finite-field CRT projection masks, input ternary secret, fresh full-support random high-modulus eval-key masks, independently small key errors. All exact computations and key-switch/error equations are in the executable source. Two modes each 160 secrets x3 tested rotations=480 ciphertext cases, total960:
  (A) Input e=0: 480/480 outputs match desired branch with max absolute residual7; KSK error RMS median1.199.
  (B) Input e in {-1,0,1}: 480/480 outputs match the operator applied to the ACTUAL input decryption phase with max extra KSK coefficient error7; median extra error RMS1.118. But for the 230 samples choosing conjugated rotation beta1, 230/230 have at least one output error versus CLEAN plaintext >300, conditional RMS median17025.95. The 250 identity beta0 cases have median RMS1.25. Exact CRT slot indicator masks have coefficient lifts of order q, so multiplying them by a short input error can yield a long coefficient error (explicit e=1 implies mask M itself). This is a WARNING for this exact CRT representation, NOT proof of failure for CKKS approximate masks with explicit delta, RNS rescaling or matched noise parameters. No native CKKS benchmark, 128bit estimator, DFR or KDM proof.

## Decision
PASS algebraically typed fused masked HalfMux + independently masked evaluation-key ciphertext toy. FAIL compact online cost: 4.25x basic HMR and key rows at n4096 with no measured native win over dense S2C or tuned hybrid, and fail preserving short coefficient error in the chosen exact CRT toy. Generic per-diagonal KSK+mask transform and layout changes are prior art in concept; no standalone novel secure primitive, corrected asymptotic online work, or cryptographically validated performance result. This negative result does not refute the broader PaCo author-open SHIP migration possibility; it rejects this narrow naive decomposition.

## End of iteration
STATUS PASS_TYPED_MASKED_HMR / FAIL_COMPACTNESS / FAIL_TOY_INPUT_NOISE / FAIL_STANDALONE_NOVELTY.
NEXT_TEST B092 NOT STARTED: archive this exact per-diagonal bitrev-HMR interface and scout a DIFFERENT full-source bootstrapping primitive; retain PaCo-SHIP only for a new compact ciphertext operation with explicit key security/noise/runtime rationale, not per-diagonal replication.
STATE_UPDATE NO: findings/boot-STATE.md listed 187967 bytes but read_repo_file returns empty; preserve existing original. No writes to unrelated SHIP.
LOCAL FULL EVIDENCE /mnt/data/BOOT_B091_handoff.zip, verified SHA256 5781cc9591953a713860dc865d703313047532b6a15c9ea42c70b2d7f5be72df, includes detailed report SHA256 cacfce8db3ab03c23931dfa7688e703c4452439ff6e6c5022995d0c8abbfea76, independent script, JSON output, run log, README and hash manifest. ZIP CRC PASS.
