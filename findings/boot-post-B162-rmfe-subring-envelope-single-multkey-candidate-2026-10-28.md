# BOOT — RMFE subring-envelope single-MultKey candidate (refined)
Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER / ALGEBRA LEVEL ONLY
CODEX_USED: NO
NATIVE_RUN: NO

## Source/open problem
Aung et al., ePrint 2025/350 / PKC 2025 explicitly leave open whether the MultKey portion can be performed directly on an RMFE-packed ciphertext instead of k split thin ciphertexts.

For m=32768,p=5,w=512,k=5 correction/TnM:
SlotsToCtxts 2.284 s; MultKey 4.732 s; CtxtsToSlots 0.078 s; DigitExtract 4.240 s; total 11.33 s.

Existing thin MultKey is NOT a drop-in for extension-valued RMFE slots: pinned HElib ThinEvalMap assumes constant slots. A raw inner-product -> CRT slot recode shortcut is also invalid because high p-adic digit extraction does not commute with arbitrary CRT mixing.

## Exact p=5 subring envelope
Outer ring:
m=32768, N=16384,
d=ord_32768(5)=8192,
ell=N/d=2,
E=GR(5^e,8192).

Choose r=2^ceil(log2 5)=8 and m_r=32.
Then N_r=16, ord_32(5)=8, ell=N_r/r=2.
Embed R_r=Z_(5^e)[Y]/(Y^16+1) into R by Y=X^1024.
Its slots are E_r=GR(5^e,8).

### Input map uses only existing RMFE projections
Let tau_i be the paper's RMFE component projections, so tau_i(phi(a_0,...,a_4)) has scalar slot value a_i.

Define
    A(c)=sum_{i=0}^4 X^(1024 i) * tau_i(c).

In slot j, X^(1024 i) evaluates to zeta_(32,j)^i, so A maps the five RMFE integer components into the first five power-basis coordinates of E_r and pads three coordinates with zero.

Method-1 tau_i already cost k log2(w)=5*9=45 automorphisms in the baseline SlotsToCtxts. The monomial X-powers are coefficient permutations and do not amplify noise in the usual coefficient norm. Summing k branches increases a deterministic additive noise bound by at most a factor k, i.e. <= log2(k)=2.32 bits for k=5, relative to the worst branch.

Keep A before ModSwitch, as baseline SlotsToCtxts is also before ModSwitch.

### One MultKey
Run ONE ModSwitch on A(c), then a degree-8 SlotToCoeff transform for R_r, then ONE boot-key InnerProduct.

This preserves the standard coefficient-domain p-adic decryption intermediate for all 16 R_r coefficients.

### Post-inner-product coefficient selection
The inner-product result may have full outer-ring noise.
Apply the known power-of-two coefficient-selection map RM_10 = Tr_(R/R_r).

For c=N/N_r=1024, Geelen's trace is
    sum m_i X^i -> 1024 * sum m_(1024 j) X^(1024 j).
Thus it SELECTS the desired coefficient positions rather than summing unrelated coefficients. The factor 1024^(-1) mod 5^e can be folded into the next linear map.

This is why the p-adic carry counterexample that killed the raw CRT-recode shortcut does not apply.

### Return to RMFE and digit-extract once
Run degree-8 CoeffToSlots in R_r.
For a conservative implementation, unpack the E_r slot into its 8 scalar coordinates using the standard r-way unpacking tree (r-1=7 automorphisms), retain the first five coordinates, multiply them by the RMFE basis phi(e_i), and sum.

The resulting slot is
    phi(z_0,...,z_4),
where each z_i is exactly the selected integer decryption intermediate for one original RMFE component.

Apply the existing 2025/350 correction-map Algorithm 4 ONCE.

Therefore:
RMFE_5 -> E_8 -> ONE MultKey -> E_8 -> RMFE_5 -> one RMFE DigitExtract
returns the original RMFE plaintext under the standard BGV bootstrapping correctness conditions.

## Prior-art boundary
Close prior:
- Chen-Han slim/thin: one base-ring scalar per CRT slot.
- Geelen 2024/153: full/sparse/subring Slot<->Coeff and coefficient-selection trace.
- Ma et al. 2024/164: Hom-NTT, RM_k coefficient clearing, and small-subring optimizations inside ordinary thin/general BGV bootstrapping.
- Aung et al. 2025/350: RMFE digit extraction/correction maps, but still k split MultKey executions and explicitly leaves direct MultKey as future work.

2024/164 does NOT collapse the 2025/350 k split MultKeys; its subring F is used inside ordinary transform optimization.

Targeted current search found no exact RMFE -> intermediate power-of-two subring -> one MultKey -> RMFE correction-map construction.

DIRECT_PRIOR_COLLISION = NOT_FOUND
CLOSE_PRIOR = YES
NOVELTY = PROMISING_NOT_ESTABLISHED

## Conservative structural cost proxy
Baseline Method-1 transform-dominated terms:
    k log w + k*(log ell + log d + log ell)
  = 45 + 5*(1+13+1)
  ~= 120 automorphism-scale units,
plus 5 ModSwitch/boot-key-inner-product executions.

Candidate conservative proxy:
    k log w                         = 45
    + degree-8 SlotToCoeff          ~ O(r+log ell)
    + RM_10                         = 10
    + degree-8 CoeffToSlots         ~ O(r+log ell)
    + degree-8 unpacking            = 7
  giving roughly 80 proxy units if O(r+log ell) is counted as about 9 per transform,
plus ONE ModSwitch/boot-key-inner-product execution.

This is NOT an exact operation count or latency claim. It is only a structural value gate.

Published p=5 correction/TnM throughput is 0.832x vanilla thin. Holding post-bootstrap capacity fixed, latency below about 9.42 s (from 11.33 s) would already cross the paper's thin throughput, so only ~1.20x latency improvement is needed for holistic value.

## Security / keys / capacity
No secret, ring dimension, plaintext modulus, or security assumption changes.
RM_10 is structurally shorter than the RM_13 coefficient-selection path used in ordinary thin recovery.
The degree-8 transforms/unpacking may need a small additional automorphism-key set; exact delta is unresolved.

Main remaining risk is capacity/noise. In particular:
- A adds <=2.32 bits to a worst-case additive branch-noise bound before ModSwitch;
- degree-8 general transforms may cost more capacity than thin transforms;
- candidate must preserve a practically useful post-bootstrap multiplication budget.

## Current status
RMFE_SUBRING_ENVELOPE_SINGLE_MULTKEY = ACTIVE_PAPER_LEVEL_POSITIVE
P5_ALGEBRA = PASS
P5_CORRECTNESS_STRUCTURE = PASS
DIRECT_PRIOR_COLLISION = NOT_FOUND
VALUE = PROMISING
CAPACITY_NOISE = UNRESOLVED
KEY_MEMORY = UNRESOLVED_SMALL_DELTA
NATIVE = NOT_RUN

## Next gates
1. source-faithful noise/capacity bound for A -> degree-8 SlotToCoeff -> one MultKey -> RM_10 -> CoeffToSlots/unpack;
2. exact Galois-key set comparison with the existing HElib/RMFE workflow;
3. only if paper-level capacity remains credible, prepare a native Codex gate after quota restoration.

## BOOT authoritative state unchanged
LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE: B163_PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
B158_NATIVE_FEASIBILITY: UNRESOLVED
B163: NOT_RUN
