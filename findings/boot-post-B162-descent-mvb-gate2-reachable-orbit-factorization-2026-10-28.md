# BOOT — DESCENT_MVB_GATE_2: reachable-orbit factorization gate
Date: 2026-10-28
TRACK_ID: BOOT
RESEARCH_MODE: PAPER_LEVEL / NO CODEX / NO NATIVE

## Provenance and source limitation
Read-before-write: findings/boot-post-B162-descent-mvb-gate1-coefficient-projection-no-go-2026-10-28.md.
Fresh public source: ePrint 2026/2616 Descent-PBS, official mirrored abstract (2026-10-23 version): module first rotation; subring-secret-compatible truncation and merged-column functional key switching; remaining Meta-PBS in ring.
Public PDF eprint.iacr.org/2026/2616.pdf and eprint.iacr.asia/2026/2616.pdf could not be opened through available web PDF access in this round. Accordingly exact Descent-PBS D, FKS semantics and attainable states are NOT VERIFIED.
Additional relevant prior art: ePrint 2024/323 Circuit Bootstrapping: Faster and Smaller already describes multiple LUTs through a single bootstrapping with a specialized encoding. Generic shared PBS/multi-output claims are not novel.

## Correction to the earlier abstract gate
Let a_j=T^j v_0 (j in J) be all possible plaintext accumulator states from a function-independent blind rotation of a common test vector. Let D:V->W be a linear plaintext-level descent map. Let y_{f,j}=L_f(a_j) be the wanted function-f output (possibly vector-valued) under some pre-descent linear readout L_f.

Two distinct tests:
(A) A post-descent arbitrary (possibly nonlinear) function h_f exists on the finite set D(A) iff D(a_j)=D(a_k) implies y_{f,j}=y_{f,k}. This is purely set-theoretic fiber consistency. It does not guarantee a cheap, linear, FHE-computable readout.
(B) A post-descent LINEAR readout H_f:span(D(A))->Y exists for all j iff
    ker U subseteq ker Y_f
where U has columns D(a_j), and Y_f has columns y_{f,j}. Equivalently rank([U;Y_f])=rank(U), or each row of Y_f lies in rowspace(U).

Proof (B):
Necessity: Y_f=H_f U implies ker U subseteq ker Y_f.
Sufficiency: define H_f(Uc)=Y_fc; it is well-defined exactly when Uc=0 implies Y_fc=0. Extend linearly if desired.

For several functions f_1,...,f_s, stack all Y_f into Y_all: a common post-descent state permits all linear readouts iff ker U subseteq ker Y_all.

## Useful necessary capacity bound
If desired outputs across possible rotation states have rank r over a FIELD K, then a linear shared state in W must have dimension >=r: rank(U)>=rank(Y_all). This is a capacity lower bound, not a runtime lower bound.
Over Z/qZ with composite q, use module-factorization/kernel condition rather than naive field rank; if q is prime, field rank applies.

## Exact small counterexample: finite fibers may be enough but linear gate fails
Let K be a field with characteristic !=2, V=K^2 and A={e1,e2,e1+e2}.
Set D(e1)=(1), D(e2)=(2), so D(e1+e2)=(3), with char(K)>3.
Let target y(e1)=0, y(e2)=0, y(e1+e2)=1.
D is injective on A so a set-theoretic h exists.
But any linear H with H(1)=0,H(2)=0 must be zero and cannot map 3->1.
Therefore 'no collisions among reachable states' is insufficient for a low-cost LINEAR MVB readout.

## What this does and does not prove
- PASS_ABSTRACT: reachable-orbit fiber lemma and linear factorization criterion.
- PASS_ABSTRACT: rank/capacity lower bound for field-linear readouts.
- FAIL_INFERENCE: finite orbit injectivity does NOT imply cheap post-descent linear readout.
- UNRESOLVED_ACTUAL_SOURCE: exact map D and reachable states of Descent-PBS 2026/2616.
- UNRESOLVED_NOVELTY: 2024/323, classical MVB and newer many-readout work need more detailed collision audit.
- NO PERFORMANCE/NOISE claim: existence of H_f does not imply low ring-operation cost, small keys, or acceptable DFR.

## Cheapest next decisive gate
1. Obtain author PDF/full definitions, especially truncation and merged-column FKS; derive plaintext-linear D (if the correct interface is linear at all).
2. Recover precise blind-rotation orbit a_j, including negacyclic signs and packing.
3. Build U=[D(a_j)] and Y_all from intended f-specific readouts, over the actual plaintext ring.
4. Compare kernel factorization and minimal output span before any implementation.
5. If abstract gate passes, constrain H_f to the ACTUAL cheap post-descent operator algebra (public additions, rotations, plaintext multiplications, sample extraction), not all linear maps.
6. Check key/noise/DFR and prior art before any native test.

## BOOT authoritative state — unchanged
LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE: B163_PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
B158_NATIVE_FEASIBILITY: UNRESOLVED
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B162_B161_HYBRID: VALID_FAIL_AT_K1024
B163: NOT_RUN
