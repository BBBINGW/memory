# BOOT B046 failure — Last-stage-only Boolean Hermite cleaning does not replace one-hot selector precleaning in CMT

TRACK_ID BOOT
ITERATION B046
DATE 2026-10-20
STATUS FAIL_POST_CMT_CLEANING_UNCONDITIONAL_DFR / FAIL_POST_COEFFICIENTS_ENCODING / LOW_NOVELTY
STATE_UPDATE YES
SHIP PAUSED_BY_PI and untouched.

PRIMARY: For source Dumezy et al. TCHES2026 ePrint2025/1301 Algorithm7, replace p*d onehot selector Hermite G=3X²−2X³ cleaners BEFORE CMT with one cleaner AFTER CMT when output LUT is Boolean, saving p*d−1 cleaner invocations at same degree/depth without harming final correctness/noise. This placement differs from prior B045 per-bit influence/partial cleaning, B040 lowrank LUT contraction.

ORIGINAL TEXT: ePrint2025/1301 title verified 35pp research cache SHA256 048ba3ae4fe97eae0417138b816572b1c79b503727db54ce76576a4d38190b19 VERSION_UNVERIFIED. Physical p17 §4.2 explicitly attributes G=3X²−2X³ to BLEACH, applied to binary digit ciphertexts (two extra multiplicative levels). Physical p19 Algorithm6 tensor CMT, p20 Algorithm7 cleaning p*d Kronecker delta ciphertexts PRIOR to CMT, then SlotsToCoeffs output. Physical p20 noise growth worst-case O(P²log_pP)*input error. Physical p25 evaluates cost when P>2^12 and cleaning overhead, p26 explains repeated cleaning rounds for P>2^20. Nearby 2026/1026 sparse arbitrary order Hermite author abstract https://eprint.iacr.org/2026/1026 is verified, full PDF retrieval BLOCKED HTTP403 & ePrint mirror absent; do not claim full text reviewed.

EXACT LEGAL COUNTEREXAMPLE: p=4,d=4,P=256, actual digit tuple allzero. Each approximate digit selector z=(1+eps,−eps,0,0) satisfies onehot sum1, each offtrue component bounded eps. Define a publicly allowed Boolean LUT f(tuple)=1 iff tensor product weight w_tuple=Π_j z_(tuple_j)>0 else0. Since true weight positive, f(0,...,0)=1. Tensor contraction of unclean selectors y=Σ f w =1+δ, δ=((1+2eps)^4−1)/2. Post G(1+δ)=1−3δ²−2δ³, deviation 3δ²+2δ³. Comparing with |y−1|=δ, postclean improves only while δ<δ*=(sqrt17−3)/4≈.2807764. For eps=.07, δ=.34448008; postclean error abs .437756085 WORSENS vs no cleaning .34448008; each preclean selector gives G(1+eps)=1−G(−eps) and G(−eps)>0, so resulting product selector weights are nonnegative. Exact paired source-shaped Boolean LUT evaluations across eps .01,.02,.05,.07,.10:
 eps|unclean error|post-only G error|preclean all selector error
 .01|.04121608|.005236329|.001206906
 .02|.08492928|.022864135|.004846285
 .05|.23205|.186532094|.030286669
 .07|.34448008|.437756085|.058761081
 .10|.5368|1.173825112|.116227899
Another pessimistic p-ary onehot per-digit variant true=1+(p−1)eps, other p−1 selectors =−eps, gives δ=((1+2(p−1)eps)^d−1)/2; for p16,d4 requires eps<.003928817 to keep positive-overshoot within G's improvement basin. Not a real digit noise measurement / IND-CPA-D attack on source.

CIPHERTEXT-TYPE COUNTEREXAMPLE: If postponed G until AFTER SlotsToCoeffs, RLWE polynomial m(X)=1+X∈Z[X]/(X4+1) represents two Boolean coefficients; ordinary encrypted ring polynomial G(m)=3m²−2m³=1−3X²−2X³ rather than intended coefficientwise m. So post-clean MUST happen in CKKS slots before SlotsToCoeffs, or incur further costly CoeffsToSlots conversions/key switches. Full dataflow type matters.

COST/PRIOR ART: At P2^16,p16,d4 original p*d64 cleaners, two ct-ct multiplications each=>128, post output once=>2, nominal126 fewer. But source CMT itself uses Θ(P)≈65536 ct products and P scalar LUT operations; ideal saving is ~0.19% compared to P product count only (not native latency). Both placements need +2 multiplicative levels, postclean after tree shifts mod-chain placement. For small P authors already omit preclean, so substituting postclean only ADDS work. Already known BLEACH cubic plus 2026 arbitrary-order Hermite are prior art; simple placement cannot be called novel protocol.
NO native FHE execution, no real FFT/CKKS noise, key security, DFR or end-to-end benchmark. Generic selector errors may be correlated; counterexample is algebraic possibility and refutes unconditional guarantee, not a failure statement about source author's actual setup.
FINDING findings/boot-B046-post-cmt-output-hermite-cleaning-amplification-gate.md
NEXT B047: archive post-output CMT Hermite simple swap; source-first BOOT DIFFERENT recent full-paper+code, seek substantial algorithm/dataflow novelty with precise tests. SHIP remains PAUSED_BY_PI, no SHIP writes.
STATE_UPDATE YES.
