# BOOT-B086 — Fused AP correlated-error rerandomization: public quadratic key recovery
2026-10-20 | TRACK_ID BOOT ONLY | SHIP PAUSED
STATUS FAIL_CORRELATED_CANCELLATION_AND_INDEPENDENT_RERAND_COMPATIBILITY / PASS_PUBLIC_KEY_RECOVERY_TOY / PASS_EXACT_NOISE_RECURRENCES / NO_PUBLISHED_SCHEME_ATTACK

## One primary hypothesis
Could B072/B085's one-row algebraic AP fusion be rescued by choosing correlated evaluation-key errors to cancel the random input mask, then adding independent GLWE encryptions of zero to rerandomize public evaluation-key masks, producing secure *and* low-noise output without standard multilevel gadget decomposition? One test, cheapest exact algebraic falsifier before native study. The proposal tested is OUR OWN AND NOT a published construction.

## Verified original sources
[FACT] Olivier Bernard–Marc Joye, "Bootstrapping (T)FHE Ciphertexts via Automorphisms: Closing the Gap Between Binary and Gaussian Keys," ePrint https://eprint.iacr.org/2025/163 , author PDF https://marcjoye.github.io/papers/BJ25autpbs.pdf , verified screenshot source PDF physical pp14–15: Definitions4.1–4.2 and Proposition4.3 describe AP-GGSW and gadget-controlled error bounds, NOT the special secret-correlated error distribution of the proposed key. Original ePrint cache PDF SHA256 ce81021fca19132729765ad652a2f4a8f1d27d6b9c7f084777b6386fa5e08387, VERSION_UNVERIFIED.
[FACT] Bernard–Joye, "Approximate CRT-Based Gadget Decomposition and Application to TFHE Blind Rotation," https://eprint.iacr.org/2024/909 Section2 gives known precision-quality tradeoff, NOT a B086 invention.
[PRIOR BOOT] B072 direct fused error has uniform-mask multiplication; B085 confirms independent key noise needs standard gadget decomposition (known). B057 warns that naive exact secret-dependent mask constraints can leak secrets.

## Algebra: precise correlated candidate and exploitable public relation
In rank-one GLWE over R_Q=Z_Q[X]/(X^N+1) with Dec_s(a,b)=b−as, let C=(A,B) with B=As+m+e_in. For i-th evaluation-key gadget row, create independently UNIFORM public masks u_Bi,u_Ai but deliberately correlate row errors via t_i as
  v_Bi=u_Bi*s + mu_i + t_i,
  v_Ai=u_Ai*s − s*(mu_i+t_i).
Then K_Bi=(u_Bi,v_Bi) encrypts mu_i with error t_i; K_Ai=(u_Ai,v_Ai) encrypts −s*mu_i with error −s*t_i. For fused Y=B*K_Bi+A*K_Ai:
  Dec_s(Y)=(m+e_in)*(mu_i+t_i);
  e_Y=mu_i*e_in+(m+e_in)*t_i.
Thus A-dependent amplified noise DOES cancel *algebraically*.

However eliminating t_i+mu_i from PUBLIC key rows yields EXACT relation:
  u_Bi*s² + (u_Ai−v_Bi)*s − v_Ai=0.
Given two distinct rows i,j, the PUBLIC polynomials
  D=u_Bj*(u_Ai−v_Bi)−u_Bi*(u_Aj−v_Bj),
  R=u_Bj*v_Ai−u_Bi*v_Aj
satisfy D*s=R EXACTLY. Whenever D is a unit in R_Q, the attacker directly computes s=D^(-1)R from PUBLIC keys alone, independent of unknown mu_i or noise. The proof is cancellation of quadratic coefficient; exact multivariate ring identity, not a statistical distinguisher. For Q=2^w, N power2, unit criterion: D(1) odd because X^N+1 reduces to (X+1)^N mod2. Program computes GF(2) polynomial inverse and Newton/Hensel lift to Q, verifies D*D^-1=1 and recovers original secret. Even if one pair yields nonunit D, testing many key row pairs can recover.

## Rerandomization exact tradeoff
Let fresh zero-GLWE additions to K_B,K_A have public fresh masks and errors z_B,z_A; define delta=z_A+s*z_B. New fused phase and joint key relation:
  Dec_s(Y')=(m+e_in)*(mu_i+t_i+z_B)+A*delta.
  e'_Y=mu_i*e_in+(m+e_in)*(t_i+z_B)+A*delta.
  u'_Bi*s²+(u'_Ai−v'_Bi)*s−v'_Ai=−delta_i.
If delta=0 (zero-error noise or secret-correlated z_A=−s*z_B), exact public quadratic key relation and key recovery persist; fresh public masks alone do not hide the constraint.
If z_A,z_B are independent short RLWE-type noise, delta generally nonzero: the explicit exact algebraic recovery no longer applies in the same way, **but** full-uniform input mask A multiplies delta. When delta is a unit, A*delta is UNIFORM conditional on delta. This is a severe noise obstruction (NOT a proof all alternative schemes insecure; it is the failure of THIS one-row proposal). For a general rerand ciphertext, note zero-error fresh-public-mask zero encryption itself is outside normal RLWE security.
No claim that independent re-randomization is secure as a whole: only the precise algebraic attack is disrupted.

## Reproducible independent toy
Standalone stdlib Python script verify_b086_correlated_rerand.py, deterministic seed860216; R=Z_(2^16)[X]/(X^8+1), uniformly random independent mask polynomials, ternary secret and primitive t/e/z, insecure toy; psi=id is subcase sufficient to falsify broad claim. 256 key transcripts, six independent correlated evaluation-key row pairs per transcript.
- 1536/1536 exact quadratic public relations.
- 1038 explicit D*s=R checks; recovered exact s in 237/256 sessions by choosing invertible public pair D.
- Re-randomized key transcript test: independent error zero ciphertext gave 0/247 exact recovered sessions *among unit-D sessions*; correlated error gave exact 241/241, zero-error gave 244/244. These use separately generated randomized keys; no inference of real IND-CPA from independent case.
- Independent re-randomization z draws: 4096 sets, 2005 unit delta, 0 exact delta zero / quadratic identity.
- For each one-key-pair output condition, 1024 independently masked inputs and EXACT GLWE-phase/error recurrences PASS. Median RMS for correlated original 2.151, correlated rerand 2.669, zero-error rerand 2.151; independent zero-error encryption rerand median RMS 18795.854. With illustrative absolute centered threshold Q/8, correlated 0/1024 crossings, independent 1024/1024, correlated rerand 0/1024. These toy-threshold counts are not DFR or actual normalized TFHE noise.
- 2-adic inverse explicitly checked. No missing PDF or code secrets used by attacker: only public key rows; toy secret read solely by assertion after recovery.
- No native 128-bit security or real AP performance is claimed. This is NOT an attack on published AP-GGSW/TFHE/Bernard-Joye.

## Decision
STATUS FAIL_PRIMARY_CORRELATED_FUSION_RESCRAMBLED_KEYS. Candidate LOW noise by secret-correlated error makes exact leak; independent rerandomization may disrupt that leak but restores huge random-mask-times-error. Do NOT call this new FHE primitive, published-scheme attack, or complete general impossibility for all correlated constructions.
RESULT: decisive exact security falsifier for proposed error correlation; 256-session public-only recovery, 4096 delta tests and reproducible ciphertext noise recurrences.
NEXT_TEST B087 (NOT STARTED): archive B072–B086 simple correlated one-row fused AP family; restart independent Bootstrapping primitive scout from verified full paper; one precise new security/noise/work hypothesis (avoid gadget/CMux/multi-bit schemes already killed). Alternative independent B065–B066 Dai parameter-correctness audit may be re-evaluated for its own merits, not automatically merged.
STATE_UPDATE NO: canonical findings/boot-STATE.md listed size187967 but Notes read returns {}; preserve. Append B086 only and no writes to other tracks.
LOCAL HANDOFF: /mnt/data/BOOT_B086_handoff.zip SHA256 00b737c62aedeef0174371568bdad12f56ce02c554733642e5724b43c81501d1 ; report, stdlib script, JSON, log, README, hash manifest. JSON SHA256 ec8e50022efc071223db842fc8721bbf95cbf667c5c3d6b441d96e39f91ed526.
