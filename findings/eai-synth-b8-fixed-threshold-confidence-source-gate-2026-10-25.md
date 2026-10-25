# EAI-SYNTH B8 — Fixed threshold versus full-tree high-confidence envelope
Date: 2026-10-25 Asia/Singapore
TRACK_ID=EAI | ACTIVE_TOPIC=SYNTHETIC_DATA | ACTIVE_SUBLINE=EAI-SYNTH
Previous complete B7; B8 is ONE PI-authorized read-only original-source/math test. EAI-SYS and every FHE or other EAI topic unchanged.
No Codex, remote GPU/server, model download, training or source edits. All future Codex requirements remain pending until explicitly requested; PENDING_CODEX=NONE_REQUIRED_FOR_B8.

## ONE hypothesis / ONE cheapest decisive test
[HYPOTHESIS H-B8, FALSIFIED for the specified uniform-envelope proof technique] Fix He's Algorithm2 threshold T0=9 ln H / eta (eta is its actual local parameter, i.e. epsilon_{j,i}/2 in Algorithm3). At a finite epoch i, all M_i=2^(i+1)-2 active spatial cell counters can receive failure probabilities beta_{j,i}>0 summing at most delta=0.05 while applying the standard per-window maximum-noise envelope proof with T0>2B(beta_{j,i}) (positive-progress sufficient condition), without retuning threshold constant 9.
[CHEAPEST TEST] On ONE fixed epoch i=8, global privacy epsilon=1 and dimension d=2, use original H_i=256 and M_i=510; compare the minimum beta needed for the union-bound envelope to ensure positive progress with the available whole-epoch failure budget. No algorithm construction or experiments.

## Source-first facts
[FACT He] He–Vershynin–Zhu, 'Online Differentially Private Synthetic Data Generation', arXiv:2402.08012v3 (2024-10-23), https://arxiv.org/html/2402.08012v3 , https://arxiv.org/pdf/2402.08012 . Original PDF screenshot physical page7 (zero index6) Algorithm1–2, p8 (zero index7) Algorithm3, p11 (zero index10) Proposition4.1/Eq4.1, p20 (zero index19) Appendix A Lemma3.2 proof. He sets T0=9ln H/eta in Algorithm2; each threshold/test noise has integer-Laplace scale 2/eta; authors use max-noise bound B=(2/eta)(2ln H+ln 2), with original failure O(1/H); positive sealed-segment true mass follows from T0>2B for H>16. Algorithm3 calls Algorithm2 at time level i for every extant cell with eta=epsilon_{j,i}/2. Original epsilon_{j,i}=C1 epsilon 2^((j-i)(1-1/d)/2), so each eta depends on j,d but CANCELS from T0>2B(beta).
[FACT prior art] He §3.3 explicitly says Algorithm2 changes prior [24] (Dwork–Naor–Reingold–Rothblum, 'Pure Differential Privacy for Rectangle Queries via Private Partitions', ASIACRYPT 2015, https://omereingold.wordpress.com/wp-content/uploads/2014/10/intervals.pdf ) by removing/altering its confidence-dependent partition threshold. The original paper §2 Figure1 has threshold 3(ln D+ln(1/beta))/epsilon and Theorem3.1 §3.1 provides an explicit all-time beta failure guarantee, with an accuracy cost involving ln(1/beta). Thus generic beta-dependent threshold retuning is STRONG PRIOR ART, not new.
[FACT] B6 established a finite-horizon conditional-noise-free count bound on simultaneous good events. B7 counted active cells and showed unmodified beta_i=1/H_i cannot directly certify a global all-good event. B8 tests whether merely redistributing beta, WITHOUT retuning T0, works using this specific envelope.

## Exact one-test derivation
[DERIVATION] Let Z~Lap_Z(2/eta). A conservative elementary two-sided tail inequality for integer discrete Laplace is P(|Z|>B)<=2exp(-eta B/2) for B>=0. By presampling up to 2H independent threshold/test variables, one sufficient confidence envelope for a fixed window is
 B(beta)=(2/eta) ln(4H/beta),    P(max_l |Z_l|>B(beta))<=beta.
This constant 4 is conservative; sharper exact geometric tails can alter constants but not the gap shown below. This is a certificate using a random tape of 2H candidate noises on a positive-progress event, not a claim that the original code uses at most 2H noises on every possible bad event.

Original fixed threshold T0=(9/eta) ln H. The exact condition for THIS B(beta) to imply positive segment progress is
 9ln H > 4 ln(4H/beta)
 iff 5ln H > 4ln(4/beta)
 iff beta > 4 H^(-5/4).
The local eta cancels; therefore same inequality holds for ALL cell depth j under He Eq4.1.

Choose epsilon=1, d=2, epoch i=8: t_i=2^i, window H=256, active cells M_i=sum_{j=1}^8 2^j =510. Fix overall epoch failure target delta=0.05.
- Needed beta for EACH cell under this proof: beta>4*256^(-5/4) =4/1024 = 0.00390625.
- Any beta allocation with sum_j beta_{j,i}<=0.05 fails to meet all 510 lower bounds, since required sum >510*0.00390625=1.9921875 >0.05. Not merely a criticism of equal split.
- For equal split beta=0.05/510=0.0000980392156863:
  eta*T0=9ln 256=49.9065970003,
  eta*(2B(beta))=4ln(4*256/(0.05/510))=64.6464592195,
  (2B)/T0=1.29534897 >1.
Thus T0>2B(beta) is FALSE in this epoch and this entire fixed-9, all-cell union-envelope certification strategy is impossible for target delta=0.05.

Careful logical qualifications:
- The lower bound on beta is **necessary only to satisfy the displayed sufficient envelope condition**, not necessary for actual positive segment progress or W1 accuracy. This failure is a proof-technique failure, NOT an information-theoretic impossibility, DP violation or concrete failing input of He algorithm.
- The source Appendix A's original threshold envelope uses slightly sharper tail constants than our conservative 4; even replacing 4 by 2 gives required budget >510*2*256^(-5/4)=0.99609375>0.05, so the illustrative conclusion survives the constant change.
- Allocating a higher beta to a few cells or replacing this all-success certificate with weighted concentration could give meaningful Wasserstein accuracy despite failure of this strong global event. No lower bound on real Wasserstein error, no He adaptive failure, no privacy budget change, no training performed.
- Taking short window H<=16 violates the authors' positive-margin premise already; i8 H256 specifically avoids that ambiguity.

## Source-first novelty evaluation / recommendation
[NEGATIVE] Generic confidence-dependent threshold retuning was already present in Dwork et al. ASIACRYPT2015, and He states that its fixed 9ln H choice is a modification. Merely replacing 9 by a function of ln(1/beta) cannot establish novelty or a new DP primitive.
[UNCLEAR] Source did not demonstrate that a truly nontrivial lower-cost high-confidence adaptive W1 guarantee is impossible or requires a special new primitive. Current finding is a bounded proof mismatch and may be trivial to avoid via existing beta-dependent threshold, pathwise weighted Wasserstein control, or a different target.
[AGENT_RECOMMENDATION] PARK fixed-threshold/max-envelope-based "research gap" as non-novel. Do NOT run more adjacent constant/threshold toy sweeps.
Potential ONE next novelty falsifier, only on explicit PI continuation: inspect He §4.2 Lemma4.2 and original COLT2023 stability proof to decide whether a weighted spatial-error bound can bypass *all counters good* and still yield meaningful adaptive W1 confidence using known techniques. A prior-art-located solution kills this branch. This is not authorization for algorithm implementation.

STATUS: FAIL_B8_FIXED_THRESHOLD_GLOBAL_CONFIDENCE_ENVELOPE
RESULT: Explicit i8 H256, M510, delta.05 shows original constant-9 T0 and conservatively beta-tuned all-cell max-noise envelopes cannot jointly certify positive progress; eta privacy schedule cancels from condition. Existing ASIACRYPT2015 already uses confidence-dependent thresholds.
NOVELTY: FAIL for basic retuning/certificate-gap claim; broader EAI-SYNTH NOT_ESTABLISHED.
NEXT_TEST: Only upon PI continuation, ONE source-first weighted W1 stability/mass proof check (He Lemma4.2 / COLT2023 original), testing whether aggregate weighted error rather than all-good cell certificates already suffices, without assuming new originality.
PENDING_CODEX: NONE_REQUIRED_FOR_B8. Do not prepare/send Codex prompts or run Codex until PI explicitly requests.
STATE_UPDATE: YES only after GitHub finding, failure note and root checkpoint written/read back.
