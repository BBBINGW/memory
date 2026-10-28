# BOOT — RMFE power-of-two subring envelope for a single MultKey
Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER / ALGEBRA LEVEL ONLY
CODEX_USED: NO
NATIVE_RUN: NO

## Source/open problem
Aung et al., ePrint 2025/350 / PKC 2025 explicitly leave open whether the MultKey portion can be performed directly on an RMFE-packed ciphertext instead of executing MultKey on k split thin ciphertexts.

The existing correction/TnM workflow for m=32768,p=5,w=512,k=5 reports:
SlotsToCtxts 2.284 s; MultKey 4.732 s; CtxtsToSlots 0.078 s; RMFE DigitExtract 4.240 s; total 11.33 s.
Their MultKey denotes ModSwitch + SlotsToCoeff + boot-key InnerProduct + CoeffToSlots.

Earlier BOOT attempt to run the existing thin MultKey directly on extension-valued RMFE slots is invalid: HElib ThinEvalMap assumes constant slots. A raw inner-product -> CRT slotwise recode shortcut is also invalid because high p-adic digit extraction does not commute with arbitrary CRT mixing.

## New construction: nearest power-of-two subring envelope
Focus first on the paper's p=5,w=512,k=5 correction-style point.

Outer plaintext ring:
  m=32768, N=16384,
  d=ord_32768(5)=8192,
  ell=N/d=2 slots,
  E=GR(5^e,8192).

Choose
  r = 2^ceil(log2 k) = 8.
Since r|d, choose the intermediate power-of-two cyclotomic
  m_r = 32, N_r=16,
with ord_32(5)=8 and still ell=N_r/r=2 slots.
Let
  E_r=GR(5^e,8)
and embed the smaller ring R_r into R by
  Y -> X^1024
because N/N_r=1024.

### Input linear map
For an RMFE slot phi(a_0,...,a_4), a_i in Z_(5^e), define a public Z_(5^e)-linear injection A into E_r by mapping the five RMFE basis elements to the first five power-basis coordinates of E_r and padding the remaining three coordinates with zero.

A can be evaluated using the same RMFE component projections tau_i already used by the paper's Method-1 SlotsToCtxts, followed by public constants and summation. Thus this step does not require k independent ciphertexts to remain live.

### Subring SlotToCoeff
Apply SlotToCoeff for the degree-8, two-slot ring R_r. The two E_r slots are mapped to the 16 coefficients
  sum_{j=0}^1 sum_{i=0}^7 a_{i,j} Y^(i+8j),
which in the outer ring occupy only
  X^(1024(i+8j)).
Only the first five coordinates per slot contain messages.

### One MultKey
Now execute the standard optimized modulus-switch/decryption-inner-product stage ONCE on this single ciphertext.

The standard BGV coefficient-domain decryption invariant applies coefficientwise. The desired 10 integer components therefore remain associated with the 10 selected coefficient positions; no nonlinear digit operation has yet been commuted through a CRT mixing map.

### Coefficient selection after the inner product
The inner-product plaintext may contain full-ring noise. Apply the known power-of-two coefficient-selection map
  RM_10 = Tr_{R/R_r},
which keeps exactly coefficient indices divisible by 1024 and zeros the others, up to the known factor 1024.

Geelen 2024/153 gives the same trace as
  sum m_i X^i -> 1024 * sum m_(1024j) X^(1024j),
and Ma et al. 2024/164 give the RM_k implementation with k automorphisms.
The factor 1024^(-1) mod 5^e can be folded into the following linear transformation.

Crucially, this is coefficient selection, not summation of unrelated active coefficients, so it does not create the carry problem of the superseded CRT-recode shortcut.

### Output map and RMFE digit extraction
Run CoeffToSlots for R_r, obtaining two E_r slots whose eight coordinates are the selected p-adic decryption intermediates.
Compose the output transform with a public map B:E_r -> im(phi) that keeps the first five coordinates, discards the three padding coordinates, and maps the five retained integers to the RMFE basis.

The output is therefore a fresh RMFE encoding
  phi(z_0,...,z_4)
of the same five integer decryption intermediates that need digit removal.
Apply the existing correction-map Algorithm 4 from 2025/350 once.

Thus no high-digit extraction is moved across an unsafe mixing operation.

## Correctness statement for the p=5 point
Under the standard correctness conditions of the optimized BGV MultKey/decryption-intermediate step:

RMFE_SUBRING_ENVELOPE_P5:
  RMFE_5
  -> degree-8 subring coordinates
  -> one coefficient-domain MultKey
  -> RM_10 coefficient selection
  -> degree-8 slots
  -> RMFE_5
  -> existing Algorithm-4 DigitExtract

returns the same RMFE-packed plaintext.

Status:
ALGEBRAIC_LAYOUT = PASS
P_ADIC_COEFFICIENT_SEMANTICS = PASS
DIGIT_EXTRACTION_INTERFACE = PASS

Native/noise correctness is NOT claimed.

## Prior-art boundary
Close prior:
- Chen-Han slim/thin bootstrapping: one base-ring scalar per CRT slot.
- Geelen 2024/153: full and sparse/subring Slot<->Coeff transformations and efficient coefficient selection.
- Ma et al. 2024/164: Hom-NTT linear transforms, RM_k coefficient clearing, and small-subring optimizations inside ordinary thin/general bootstrapping.
- Aung et al. 2025/350: RMFE digit extraction/correction maps, but still k split MultKey executions and explicitly leaves direct MultKey as future work.

Targeted current search found no source combining an RMFE-to-intermediate-subring envelope with one MultKey and RMFE correction-map digit extraction.

The novelty claim must NOT be "use a subring in BGV bootstrapping".
The narrow candidate claim is:
  use the smallest convenient power-of-two extension subring r>=k as a temporary bootstrap representation for k RMFE integer components, allowing one coefficient-domain MultKey while retaining one RMFE digit extraction.

DIRECT_PRIOR_COLLISION = NOT_FOUND
CLOSE_PRIOR = YES
NOVELTY = PROMISING_NOT_ESTABLISHED

## Conservative value model
Current Method-1 front-end component projection costs k log2(w)=5*9=45 automorphisms; the candidate can reuse this work to form one E_8 ciphertext instead of retaining five thin ciphertexts.

Using source asymptotics:
- ordinary thin transforms: O(log d + log ell) per split branch;
- degree-r general/subring transforms: O(r + log ell);
- coefficient selection R -> R_r: log2(d/r).

Dominant structural proxy for k=5,d=8192,r=8,ell=2:

baseline transforms:
  k log w + k*(log ell + log d + log ell)
  ~= 45 + 5*(1+13+1)
  ~= 120 automorphism-scale units,
plus k=5 ModSwitch/boot-key-inner-product executions.

candidate:
  k log w
  + O(r+log ell)
  + log(d/r)
  + O(r+log ell)
  ~= 45 + 9 + 10 + 9
  ~= 73 proxy units,
plus ONE ModSwitch/boot-key-inner-product execution.

This is a structural proxy, not a measured operation count or latency claim.
It suggests a meaningful value margin and a much smaller live-ciphertext working set.

For the published p=5 correction/TnM point, throughput is 0.832x vanilla thin. Holding post-bootstrap capacity fixed, reducing latency from 11.33 s below about 9.42 s would already cross the paper's thin-bootstrap throughput. The candidate therefore only needs roughly a 1.20x latency improvement to be application-level meaningful; whether capacity remains comparable is unresolved.

## Security/key/capacity
No secret distribution, ring dimension, plaintext modulus, or security assumption is changed. All new steps are public linear maps around the existing bootstrapping key.

RM_10 uses fewer coefficient-selection stages than the RM_13 used by ordinary thin recovery; its automorphism chain is structurally a subset. The degree-8 transforms may require a small number of additional automorphism keys; exact key-set delta is UNRESOLVED.

Main remaining risk is capacity/noise from:
- RMFE->E_8 linear map,
- degree-8 transforms,
- one RM_10,
- E_8->RMFE map.
The paper's current p=5 output has only 5 remaining multiplications, so capacity must be audited before native work.

## Current decision
RMFE_SUBRING_ENVELOPE_SINGLE_MULTKEY = ACTIVE_PAPER_LEVEL_POSITIVE
P5_ALGEBRA/CORRECTNESS = PASS
DIRECT_PRIOR_COLLISION = NOT_FOUND
VALUE = PROMISING
CAPACITY_NOISE = UNRESOLVED
KEY_MEMORY = LIKELY_SMALL_DELTA / UNRESOLVED
NATIVE = NOT_RUN
CODEX_REQUIRED = NO for next paper gates

## Next gates
1. derive exact linear-transform factorization for A + degree-8 SlotToCoeff and degree-8 CoeffToSlots + B, including multiplicative-level/capacity cost;
2. verify required automorphism keys against the existing RMFE/HElib key set;
3. derive a conservative noise/capacity bound and compare with the published 391 -> 101 capacity trajectory;
4. extend only after the p=5 point is clean; do not generalize to p=3 or p=11 yet;
5. no Codex/native execution until PI explicitly restores quota.

## BOOT authoritative state unchanged
LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE: B163_PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
B158_NATIVE_FEASIBILITY: UNRESOLVED
B163: NOT_RUN
