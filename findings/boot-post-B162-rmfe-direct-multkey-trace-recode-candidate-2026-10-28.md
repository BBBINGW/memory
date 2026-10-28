# BOOT — RMFE direct-MultKey scout: correction and rank-k subspace candidate
Date: 2026-10-28
TRACK_ID: BOOT
CODEX_USED: NO
NATIVE_RUN: NO

## Correction to the earlier trace/recode candidate
The earlier idea
    existing thin MultKey on RMFE-packed slots -> relative trace -> recode
is NOT source-faithful.

Pinned source audit:
- 2025/350 uses HElib commit acdb264e1a991eaee35fd8b3c31bebe9528c49a1.
- HElib ThinEvalMap is explicitly documented for thin bootstrapping "where slots are assumed to contain constants".
- thinReCrypt actually applies ThinEvalMap::slotToCoeff before the boot-key inner product and ThinEvalMap::coeffToSlot afterwards.
- ThinStep1Matrix uses a trace/deflation construction specialized to that constant-slot subspace.

Therefore feeding arbitrary RMFE extension elements into the existing thin map is not justified.

A second attempted shortcut,
    raw inner-product intermediate -> slotwise trace/recode -> RMFE DigitExtract,
also fails generically: Halevi-Shoup digit extraction recovers selected HIGH p-adic digits of coefficient integers, and high-digit extraction does not commute with CRT/linear mixing because of carries. Example p=5,e=2: 4 and 1 each have top digit 0, but 4+1=5 has top digit 1.

Thus:
OLD_TRACE_RECODE_DROPIN = SUPERSEDED / FAIL_AS_DROPIN.

## New candidate: rank-k RMFE-subspace slim transform
Let each slot j contain
    phi(a_0j,...,a_(k-1)j)
with a_ij in Z_(p^e), and let b_i=phi(e_i).
Let S be the existing thin SlotsToCoeff map, so for scalar slots
    S((a_j)_j) = sum_j a_j X^(d j).

Let tau_i be the RMFE component projection.
Define a single public linear transform

    T(c) = sum_(i=0)^(k-1) X^i * S(tau_i(c)).

Then the plaintext after T is

    M(X)=sum_j sum_i a_ij X^(d j+i).

Because k <= d, all k*l scalar components occupy distinct coefficients of one plaintext polynomial; no split ciphertext is information-theoretically necessary.

Now run the ordinary optimized ModSwitch + boot-key inner product ONCE on T(c).
For each active coefficient d j+i, the resulting integer has exactly the same p-adic decryption/digit invariant that the corresponding split thin bootstrap would have had. Coefficients outside the active set carry no message and may be ignored.

Define the inverse partial transform R to:
1. select coefficient positions d j+i,
2. map each residue class i back to scalar slots,
3. multiply by b_i=phi(e_i),
4. sum over i.

R therefore yields slots of the form
    phi(z_0j,...,z_(k-1)j),
where every z_ij is the noisy integer decryption intermediate for component a_ij.

The existing RMFE correction-map DigitExtract from 2025/350 then applies directly and returns
    phi(a_0j,...,a_(k-1)j).

This preserves coefficient-domain high-digit semantics; unlike the superseded shortcut, it does not interchange nonlinear digit extraction with CRT mixing.

## Relation to prior art
Chen-Han slim/thin bootstrap is the rank-1 special case: every slot contains one base-ring scalar.
General/thick bootstrap is effectively rank d and performs d digit extractions.
2024/153 sparse packing handles plaintexts encoded in a subring and does not establish arbitrary proper linear-submodule rank-k bootstrapping.
RMFE im(phi) is generally a proper Z_(p^e)-linear submodule of E, not a subring (e.g. paper p=5 point has k=5,w=512).

Targeted search found no direct prior for this RMFE-aligned rank-k slim transform.

## Value: conservative, not the old 1/k estimate
The paper's current Algorithm 2 pays:
    SlotsToCtxts -> k separate thin MultKey blocks -> CtxtsToSlots -> one RMFE DigitExtract.

The proposed T/R path pays:
    one rank-k linear transform T -> ONE ModSwitch/boot-key inner product -> one inverse rank-k transform R -> one RMFE DigitExtract.

Even a naive implementation of T/R may still contain work comparable to k component projections/thin transforms. Therefore the previous estimate "MultKey cost becomes exactly 1/k" is withdrawn.

Guaranteed structural saving, if T/R are implemented correctly:
- k -> 1 ModSwitch/boot-key-inner-product executions;
- k live ciphertexts through the MultKey stage -> 1;
- one common coefficient-domain decryption intermediate instead of k independent ones.

Possible additional saving:
T and R are each single public linear maps and may share automorphisms/hoisting across the k components. This is promising but NOT yet proved.

## Current status
RMFE_DIRECT_THIN_MULTKEY = FAIL_AS_DROPIN
RMFE_RAW_SLOT_RECODE = FAIL_GENERIC_BY_CARRY
RMFE_RANKK_SUBSPACE_MULTKEY = ACTIVE_PAPER_LEVEL_CANDIDATE
ALGEBRAIC_LAYOUT = PASS
CORRECTNESS = PASS_AT_LINEAR/COEFFICIENT_INVARIANT_LEVEL
DIRECT_PRIOR_COLLISION = NOT_FOUND
VALUE = PROMISING_BUT_UNQUANTIFIED
CAPACITY/NOISE = UNRESOLVED
NOVELTY = PROMISING_NOT_ESTABLISHED
NATIVE = NOT_RUN

## Next gates
1. Derive T/R as source-faithful HElib-style linear transforms and count automorphisms/plaintext multiplications.
2. Determine whether T/R can share the same Galois keys/hoisting as existing thin maps plus RMFE projection maps.
3. Bound noise/capacity of T -> single MultKey -> R against k independent thin MultKeys.
4. Only if a clear paper-level value margin remains, prepare a Codex/native gate. Do not run it while quota is unavailable.

## BOOT authoritative state unchanged
LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE: B163_PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
B158_NATIVE_FEASIBILITY: UNRESOLVED
B163: NOT_RUN
