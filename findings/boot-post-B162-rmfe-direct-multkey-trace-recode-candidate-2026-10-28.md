# BOOT — RMFE direct MultKey trace-recode candidate
Date: 2026-10-28
TRACK_ID: BOOT
CODEX_USED: NO
NATIVE_RUN: NO

## Source/open problem
PKC 2025 / ePrint 2025/350 explicitly asks whether MultKey can run directly on RMFE-packed ciphertexts instead of k split ciphertexts.

Current Algorithm 2:
SlotsToCtxts -> k times [ModSwitch + SlotsToCoeff + InnerProduct + CoeffToSlots] -> CtxtsToSlots -> RMFE DigitExtract.

For p=5,w=512,k=5 correction/TnM, Table 2 reports 2.284 s split, 4.732 s MultKey, 0.078 s recombine, 4.240 s DigitExtract, total 11.33 s.

## Candidate (proved s=1 subfamily)
Use G=Z_(p^e), G'=GR(p^e,w) subset E=GR(p^e,d), with s=1.
Let n=d/w and
P = n^(-1) Tr_(E/G').
For odd p and power-of-two n, n is invertible.

Direct packed MultKey produces slot state
y = phi(m) + p*epsilon in E.
Since P fixes G',
P(y)=phi(m)+p*P(epsilon) in G'.

Apply recode pi=phi o psi. Since psi(phi(v))=v,
pi(P(y)) = phi(m + p*delta),
delta=psi(P(epsilon)) in (Z_(p^e))^k.

Thus the result is exactly back in the RMFE image with integer components congruent to m modulo p, which matches Algorithm 4's input invariant.

Pipeline:
ONE packed MultKey -> relative trace E->G' -> ONE recode -> existing correction-map DigitExtract.

Status:
RMFE_DIRECT_MULTKEY_S1_ALGEBRA = PASS.
Correctness depends only on the standard BGV pre-digit invariant message + p*error.

## p=5 parameter gate
For m=32768,p=5, d=ord_32768(5)=8192.
With w=512,s=1: n=16, so relative trace needs 4 recursive Frobenius-sum stages.
For e=4, eta=125, Theorem 1 gives
k <= min(6, floor(511/125)+1)=5.
Therefore the paper's k=5 packing count is preserved.

The same s=1 check preserves k=5 for p=11,e=3,w=512.
It does not preserve p=3,e=5,w=512,k=7 (s=1 permits at most k=4).

## Coarse value gate
Baseline p=5 front end = 7.094 s.
Table 2 indicates MultKey scales approximately linearly with k, giving one-MultKey proxy 4.732/5=0.946 s.
Paper Section 5.1 says Method-1 recode is essentially SlotsToCtxts + CtxtsToSlots, proxy 2.362 s.
Four trace stages are small relative to the ~45 automorphisms in the Method-1 split/recode; rough proxy ~0.20 s.

Paper-level estimate:
candidate front ~3.51 s;
candidate total ~7.75 s versus 11.33 s;
potential latency improvement ~1.46x.

This is NOT a native result.

## Caveat / next gate
Capacity is unresolved. The relative trace adds automorphism/key-switch noise, while the extra pre-recode may largely exchange the baseline split+recombine cost rather than remove its capacity cost.

Targeted search found no direct normalized-trace + recode solution after 2025/350. FIMD prior art already allows generic linear maps to be folded into recoding, so any novelty claim must be narrow and bootstrap-specific.

Current status:
RMFE_DIRECT_MULTKEY_S1 = ACTIVE_PAPER_LEVEL_POSITIVE
DIRECT_PRIOR_COLLISION = NOT_FOUND
CLOSE_PRIOR = YES
LATENCY_VALUE = PROMISING_P5
CAPACITY = UNRESOLVED
NOVELTY = PROMISING_NOT_ESTABLISHED

Next:
1. source-faithful ModSwitch/MultKey correctness check;
2. capacity/noise bound for 4-stage trace + pre-recode;
3. evaluation-key reuse/memory check;
4. no native/Codex until these pass.

## BOOT state unchanged
LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE: B163_PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
B158_NATIVE_FEASIBILITY: UNRESOLVED
B163: NOT_RUN
