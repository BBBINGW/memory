# PURE-FHE · P0-PRESCOUT-22 — GCKKS Stage2 Headroom / Ciphertext Branching Cost Gate

Date 2026-10-26 (Asia/Hong_Kong)
TRACK_ID PURE-FHE; PREVIOUS P0-PRESCOUT-21.
SOURCE papers/supplied/2026-2600.pdf SHA 8db712155d087284d21e924623496bc48e36eb72 (user supplied).
STATUS PASS_ANALYTIC_RESOURCE_LEDGER / UNCLEAR_NATIVE_HEADROOM / NO_NEW_CONSTRUCTION.
ONE PRIMARY H22: Is the source's precision-path modulus saving by itself sufficient to establish a favorable total-resource cost at large k (ciphertext materialization, key switching, scale feasibility), without additional scheduling or implementation evidence?
ONE TEST: expand the paper's exact k-dependent output/KS counts, derive a fully-materialized RNS memory accounting and independently combine the printed modulus headroom / normalized unused-slot constraint.

## [FACT] Primary source exact references

Paper Ma–Liu–Wang–Wang, High-Precision Bootstrapping for GCKKS, ePrint 2026/2600, draft Oct22, 2026:
- physical p18 §5.1: Stage 1 CKKS conversion then balance reduction modulo q, ModRaise to Q, decrypt m+qI. Source reports ||I||∞≤15 with overwhelming probability for h=32 sparse encapsulation; q is a few bits above ||m||∞. Step 5 precision doubling and split, producing log2(32)*k/2 ciphertexts; step6 yields k/2 cts, step7 jointly folds into one using StC.
- physical p19–21 §5.2: each split-and-clean round costs THREE scale-related levels; h1(x)=3x²−2x³, powers shared before splitting, key switching and unused-slot noise bounded. p5 §1.3 separately notes contemporaneous revised Focused CKKS (ePrint 2026/2531, Oct20 revision) has a tree split-then-clean costing TWO levels per round, but no shared pre-split powers and different unused-slot invariant. The authors contrast their 3-level vs 2-level path, and explain different error invariant; do not claim either is superior end-to-end without version-matched analysis.
- physical p24–25 §5.4 Algorithm1/Lemma3: conditional necessary sufficient theorem hypothesis ||b+as||2+||e F||∞ <Q/2; not established solely by congruence modQ.
- p25 §5.5: Stage5 final 5k/2 ciphertexts, ≤15k key switching operations in precision doubling; modulus consumption O((p/k)logk) precision-dependent only; remaining stages independent of p in asymptotic accounting.
- p15–16 §4.1–4.2: a valid unused-slot normalized noise bound under rescaling divisor rho≥max(1,r c_e). When adjusted useful scale Δ' is too small, require HomPMult/rescaling or special H to lift scale without making unused-slot error explode.
- p26 §6: 'Implementation Not available yet'. Thus no measured k-dependent native time or memory and no concrete final parameter ledger in this draft.

## [DERIVATION] Test result: resource accounting

At fixed N, k≥8 power of two:
 usefulSlots=2N/k;
 final Stage5 ciphertexts C5=(log2 32)*k/2=5k/2;
 split iterations d=log2(k/4);
 precise stage5 precision-doubling levels 3d;
 #KS ≤15k (source upper bound; NOT 15k distinct key-switching keys).
 For N=2^16:
 k    slots      C5     3d     upperKS
 8    16384      20     3       120
 16   8192       40     6       240
 32   4096       80     9       480
 64   2048       160    12      960
 128  1024       320    15      1920
 256  512        640    18      3840

If ALL C5 outputs are materialized as two degree-N polys with each RNS-limb coefficient stored in 8 bytes, stage5-output storage is C5*2N*8*L bytes, or C5*L MiB for N=2^16. E.g. k=256: 640 MiB per one limb; 10 limbs =>6.25GiB, 20 limbs =>12.5GiB. This excludes evaluation keys, scratch, decomposition buffers and other live ciphertexts. BUT it is **not** a universal lower bound on optimized live peak: bit recombination/partial StC can stream/fuse outputs and release early, and actual L varies with level/scale. No native memory claim proven.
Storage of fully materialized output **per original useful slot** grows as C5/(2N/k)=5k²/(4N). At N=2^16 and k=256, 640/512=1.25 full ciphertext per useful complex slot *for stage5 outputs*. It is a representation resource ratio not latency lower bound.

## [DERIVATION] Conservative modulus headroom and correction

Choose the exact integer-lift relation in the intended p18 flow d=b+as=m+qI; ||I||∞≤K_I, ||m||∞≤alpha q. Independently nearest-rounding two RLWE-component CRT lifts causes coefficient errors |r_b,j|,|r_a,j|≤1/2; e=r_b+r_a*s. Negacyclic convolution gives
  ||d||2≤sqrt(N)q(alpha+K_I),
  ||eF||∞≤(1/2)(1+||s||1)||F||1.
A sufficient, non-sharp certificate for printed Lemma3:
  Q/q > 2sqrt(N)(alpha+K_I) + ((1+||s||1)||F||1)/q.
For N=2^16, alpha=1/16, K_I=15, the first term is 7712 (~12.913 bits). The second term cannot be numerically instantiated from current source because k,F,q, involved conversion key norm ||s||1 and actual Q/q are unspecified. Important: h=32 on sparse ENCAPSULATED key bounding I does NOT by itself prove ||s||1≤32 for the secret active in algorithm1. Prior P0-21 numeric 33||F||1/q is a hypothetical special case, not GCKKS author parameter certification.
A large Q/q could make 12.913-bit headroom negligible relative to ultra-high-precision budgets, but no PASS_NATIVE or PASS_AUTHOR_PARAMETERS can be claimed.

## [DERIVATION] Additional scale floor

The paper's normalized unused-slot noise-control condition needs each rescale divisor rho≥max(1,r c_e), with target factor’s maximum unused eval c_e. The effective scaling factor after factor-change may fall BELOW this. Source explicitly proposes auxiliary H or HomPMult to correct. Consequently the p-dependent big-O count is not an assertion that all intermediate rescale divisors have merely p/k bits in finite parameter sets; a concrete scale ledger must include the floor rho and any auxiliary operations. For p=1024,k=256, p/k=4 bits (not a proposed safe prime size); 18 layer count from source cannot be costed with 4-bit mod primes without verifying floor/noise/security. No contradiction claimed.

## [FACT] Contemporary context

- Focused CKKS ePrint 2026/2531 revised 2026-10-20, competing tree-like split-first two-level method per GCKKS 2600 p5–6. Original PDF attempted via public ePrint and mirror with 403 / no parseable source; must be obtained before exact theorem comparison.
- Dumezy ePrint 2026/2513 public author site https://jdumezy.com/publications/new-scheme/ : implemented shaped rounding native bootstrapping for small batches, distinct working regime; cannot compare time directly with implementation-less high precision GCKKS 2600. Source author blog https://jdumezy.com/blog/shaped-rounding/.
- ePrint 2026/2600 PDF received and read; no PDF creation/edit required.

## Decision

H22 cannot be affirmed as a full resource claim: modular precision asymptotics alone do NOT establish feasible high-k memory/speed, but no author correctness theorem or paper's stated big-O is falsified. Status PASS_ANALYTIC_COST_GATE / UNCLEAR_TOTAL_FEASIBILITY / NOVELTY_NOT_ESTABLISHED. Do not run Codex.
High-risk path: implement whole new GCKKS bootstrap before parameter set / F values / targeted comparison. Low-cost next technical hypothesis: Is a 2-layer version of shared-power precision doubling possible while maintaining Lemma2 normalized unused-slot invariant (cf Focused CKKS 2-layer split-first vs GCKKS 3-layer share-before-split)? Must read 2026/2531 primary or explicitly mark source missing; test in a minimal two-slot symbolic model, not claim novelty.
NEXT_TEST: SHARED_POWER_TWO_LEVEL_SPLIT_PRECISION_GATE / FOCUSED_PRIOR_ART_PRIMARY_TEXT_VERIFICATION.
STATE_UPDATE YES isolated finding only. No global STATE.md mutation and other tracks unchanged.
