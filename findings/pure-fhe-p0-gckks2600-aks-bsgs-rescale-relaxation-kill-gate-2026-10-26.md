# PURE-FHE · P0-PRESCOUT-29 — Kill-or-keep AKS vs BSGS: source-bound relaxation audit

Date: 2026-10-26 (Asia/Singapore)
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: GCKKS_HIGH_PRECISION_BOOTSTRAPPING
PREVIOUS: P0-PRESCOUT-28; findings/pure-fhe-p0-aks-gckks-unused-noise-mismatch-gate-2026-10-26.md, SHA 88a763e9c45c738d879ef05039f3642639e11b21.
STATUS: PASS_BOUND_TIGHTENING / FAIL_STRUCTURAL_UNAVOIDABLE_AKS_NOISE_BARRIER / KILL_GENERIC_AKS_STEP7_CONTRIBUTION
NOVELTY: NOT_ESTABLISHED
CODEX: NOT_RUN; GPU/NATIVE/REMOTE: NOT_RUN
OTHER_TRACKS: UNCHANGED; global STATE.md UNTOUCHED

## One falsifiable hypothesis H29

H29: In GCKKS 2026/2600 Step7, the (L/g)Bks outer-rotation term is an r-independent fundamental floor, and the additional AKS key-encryption error (2025/1403 Appendix C) creates a parameter-irremovable normalized unused-slot noise obstruction, requiring genuinely new AKS key representation.

Cheapest decisive test: re-read the *preceding unrelaxed* p23 GCKKS BSGS inequality and p41 AKS error expansion. Preserve ALL denominators. Check one fixed illustrative parameter tuple before attempting any new construction. If P/r adjustment and existing proof-bound tightening already remove the claimed floor, reject H29 and park this candidate.

## Sources

[FACT] Ma, Liu, Wang, Wang, High-precision Bootstrapping for GCKKS, ePrint 2026/2600, supplied papers/supplied/2026-2600.pdf SHA 8db712155d087284d21e924623496bc48e36eb72, physical pp14–16 and p23 §5.3 were read anew. The **UNRELAXED** p23 formula is
  B_out,xi <= [ L a_xi Brnd (a_xi Bks+B_xi) + (L/g) a_xi Bks ] / rho + a_xi Bms
at unused embedding xi, a_xi=|F(xi)|.
Author then simplifies with rho>=1 and rho/a_xi>=r to
  g_BSGS,r(B) = (L Brnd/r)(B+Bks) + (L/g)Bks + Bms.
The second term loses its divisor rho by intentionally using 1/rho<=1. The simplified expression is a VALID conservative sufficient bound; this is NOT a paper mistake. Previous P0-27 finding derived g>L Bks/(K-Bms) as necessary for the *printed relaxed certificate*, but should NOT be interpreted as a necessary condition of the original algorithm or the sharper p23 intermediate inequality. P0-29 explicitly repairs that possible overinterpretation while keeping historical files immutable.

[FACT] Yan et al., Faster Bootstrapping for CKKS with Less Modulus Consumption, ePrint 2025/1403 cached 51-page PDF from GitHub mirror sha256 784db16f5a3f7c79c68c52f0a99e03c8ca7ce3e4c06824736f5fd4dfff1f5c29, source VERSION_UNVERIFIED; physical p20 Theorem2, p26-27 §6.3, p40-41 Appendix C verified. AKS fuses mask multiplication and rescaling into a weighted switching key. Source Appendix C gives underlying RLWE error
  e_AKS = (m/q_ell)e' + (1/P) sum_j [c1]_{D_j}(r_j+e_j) + r'_0+r'_1*s2+r'_2.
Generic AKS on StC is explicitly foreseen by the authors (§6.3). LCR+AKS extra level saving uses special small-lift post-ModRaise CtS conditions, not freely transferable to GCKKS Step7.
A public author exposition https://ckks.org/blog/2026/less-mod-ckks/ also confirms the AKS vs BSGS time/key-memory tradeoff.

## [DERIVATION] Corrected one-step BSGS normalized bound

Let B_xi <= a_xi B, c_e = max_unused a_xi. Divide exact p23 inequality by a_xi >0:
  B_out,xi/a_xi <= [L a_xi Brnd(B+Bks)+(L/g)Bks]/rho+Bms.
For a common rho and c_e, a uniform valid upper bound is
  g_tight,rho(B)=[L c_e Brnd(B+Bks)+(L/g)Bks]/rho+Bms.
If K>Bms, selecting
  rho >= [L c_e Brnd(K+Bks)+(L/g)Bks]/(K-Bms)
ensures g_tight,rho(K)<=K for this one BSGS gate, alongside rho>=max(1,r c_e) and OTHER GCKKS source requirements.
When rho→infinity and L, c_e, etc. fixed, BOTH former BSGS terms vanish. The only fixed term in this source-level upper bound is Bms. Therefore the (L/g)Bks barrier from the PRINTED g_BSGS,r formula is a proof-looseness artifact, not a fundamental rotation-induced floor.
IMPORTANT: Increasing rho is NOT free under FHE: p15–16 §4.2 enforces sufficient useful scale, possibly auxiliary H or HomPMult; modulus primes, security, RNS limbs, noise and end-to-end cost are still unverified. The algebraic certificate establishes no native feasibility.

## [TOY_EXECUTED] Correct P0-27 example on original exact bound

Exact rational arithmetic on the same illustrative (NOT AUTHOR) values:
 N=65536, k=256, L=512, g=32, K=16, Brnd=Bks=Bms=1, a_xi=c_e=1, rho=r=2048.
Published relaxed formula at B=K:
  g_BSGS,r(K)=512*17/2048 + 16 +1=21.25 > K (=16), so the RELAXED source certificate fails.
Retained-denominator bound:
  g_tight,rho(K)=(512*17+16)/2048+1=5.2578125 < K.
Required rho_min=(512*17+16)/(16-1)=1744/3≈581.3333, so 2048 easily meets this single-gate inequality.
Thus THE SAME g=32 and rho2048 is certifiable by the unrelaxed p23 inequality without moving to g=64. The previous statement that increasing g to64 was 'necessary' refers only to the deliberately relaxed printed model. This demonstrates a structural source-bound correction; not a real cryptosystem parameter/security certificate.

## [DERIVATION] AKS error: P is an existing adjustable knob, not a proven fundamental obstruction

At any GCKKS unused embedding xi, multiplying an underlying AKS RLWE decryption error by F(xi) and normalizing by |F(xi)| yields its underlying magnitude, subject to unchanged valid-F rotations and correct lift/modulus assumptions.

Let, for one fused step, T_xi = |m(xi)e'(xi)|/q_ell, C_xi = sum_j |tau_xi([c1]_{D_j}(r_j+e_j))|, and D_xi = |tau_xi(r'_0+r'_1*s2+r'_2)|. Appendix C yields a purely conditional scalar bound:
  |tau_xi(e_AKS)| <= T_xi + C_xi/P + D_xi.
If finite T,C,D independent of a chosen P envelope and K > T+D, then P >= C/(K-T-D) suffices for this individual source-level error term. For d independent masks/weighted keys, their contributions must be summed or bounded with justified tails; no automatic savings or independent Gaussian assertion. Actual P also changes special primes, key size, modulus, RNS arithmetic and security, so this is NOT a valid concrete author parameter set. The *unmasked* key noise in AKS is real but not shown unavoidably >K: it contains 1/P, while the separate fixed rounding floor D remains.

## Decision and limits

H29 FAILS as a supposed **unavoidable new mechanism requirement**: a crucial BSGS obstacle came from loosening 1/rho<=1, and the AKS key error already exposes an ordinary 1/P budget. Neither observation proves practical end-to-end speedup, but there is currently no source-supported nontrivial GCKKS-specific obstruction that mandates a novel key design. Applying AKS to StC and trading time for key storage is existing prior art. **KILL/PARK generic 'AKS on Step7' as publishable contribution.** Do not confuse 'unable to prove a need for new mechanism' with 'proved any realistic configuration feasible or faster'.
No new construction, no attack or theorem flaw, no native results. Do NOT silently launch another similar parameter toy series. PI may select a DIFFERENT Pure FHE research hypothesis; a future AKS revival requires real GCKKS F/Delta/rho/P/security/key-memory ledger and a verified advantage not explained by standard AKS/BSGS/factorization.

END_OF_ITERATION
STATUS: PASS_SOURCE_BOUND_TIGHTENING / FAIL_H29_UNAVOIDABLE_OBSTRUCTION / PARK_AKS_STEP7
RESULT: P0-27 bound floor is from 1/rho<=1; sharper g_tight certifies earlier toy g32 at rho2048; AKS source key-error term scales 1/P plus fixed rounding; general AKS-to-StC and time-memory tradeoff are known prior art.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: PI-prioritized independent PURE-FHE gap with clear source and critical path, not further AKS/BSGS mask parameter scans. Current strongest newness gate is nonunit GCKKS Step8 conversion and end-to-end parameter feasibility, but first find an author-source-specific unresolved cost or incompatible interface before proposing a mechanism. Alternatively park the whole GCKKS line pending 2026/2531 full PDF.
STATE_UPDATE: YES (one isolated PURE-FHE finding); no shared STATE.md update.
CODEX_REQUIRED: NO (PENDING only under explicit PI authorization).
