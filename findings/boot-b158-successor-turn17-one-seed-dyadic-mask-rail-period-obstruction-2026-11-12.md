# BOOT / B158_OVERALL — Successor Research Turn 17/25
Date: 2026-11-12 Asia/Singapore
Candidate: boot-b158-one-seed-dyadic-mask-rail-v1
Phase: PROBLEM_SELECTION
Outcome: PARKED / FAIL_PERIOD_DOUBLING_SOURCE_SEMANTICS / NO_CREDIBLE_NEW_MECHANISM
Native/Codex: NOT_RUN

## Authority and independent read-before-write
Entering durable state ACTIVE=UNKNOWN, backups=none; TRACK_ID=BOOT, ACTIVE_SUBLINE=B158_OVERALL. Independently fetched:
- findings/boot-b158-successor-turn16-three-involution-hypercube-selector-axis-source-gate-2026-11-12.md, blob 98f78fd4611aaf053465b3fb644c8e89b164044d, PARKED.
- findings/boot-B158-residual-structural-rescue-scout-2026-10-28.md, blob d87795880d9df2f16c710f38fc7dfd94a0f4d771: original state S_k=[P_k repeated H/k | x^k one_H], late mask noise 16-26 bits; uniform x^k row not patternable by rotations alone.
- findings/boot-B158-selector-norm-lift-layout-gate-2026-10-28.md, blob 17fdf11bffe6044326fa243750d5b3869eb297f7: exact B163 selector M_k(i)=1 iff i mod(2k)>=k on left row, right row zero; H=16384. k=32 centered coefficient L1=1151314, k=4096 L1=134115624; late delta noise quantitatively correlated.
- findings/boot-B158-checkpoint-decoupled-halfbasis-gate-2026-10-28.md, blob 49a85b46bf23566b24324e0994b7f2830b136dc5: different existing construction carries unmasked clean A_k=[0|x^k one_H], squares to A_2k, but REAPPLIES fresh M_k per stage. This candidate is NOT a rename or reopen: it attempts to eliminate ALL further per-stage M_k by carrying a SINGLE already-masked extra rail, a strictly stronger algorithmic claim.
- findings/boot-B163-native-artifact-audit-2026-10-28.md blob b586517ec9e1505e69dd5e299c390357ec87b225: B163 k4096->8192 fails at required bits665, L18 logQ649.
Primary source Lattigo v6.2.0 schemes/bgv/encoder.go blob db146d55271b67f868a53fca94ebf7a6d3a01974. No new source changes.

## Pre-registration — ONE paper-changing test
QUESTION: In the FIXED B158 two-row layout and parameters, can a SINGLE mask-seeded auxiliary RLWE rail U_k=[M_k*x^k|0], initialized at checkpoint k0=32, be updated for all subsequent doublings into U_2k=[M_2k*x^(2k)|0] using only stock row rotations/row swap, pointwise ct arithmetic and uniform-public-scalars or spatially constant rails, but NEVER another spatially nonconstant public mask or imported prepatterned rail? If yes, eliminate multiple very noisy public selector applications with at most existing extra unmasked squarings.
CURRENT_BELIEF: No. M_k has period exactly 2k across row slots, M_2k period 4k. Shift-equivariant rotations, sums, products and uniform constants preserve 2k-periodicity when all input rails have it. The legitimate x=1 specialization makes target difference manifest.
CHEAPEST_DECISIVE_TEST: At legal x=1, establish subalgebra P_(2k) of row vectors invariant under cyclic shift by 2k; show every permitted stock operation preserves it; observe M_2k outside P_(2k). Read-only 256-slot control at k=32. No native.
IF_PASS: A source-supported update violating this invariant through some allowed, costed non-mask operation would admit ACTIVE for exact full recurrence, source/key and noise/value canary gates.
IF_FAIL: If all allowed operations preserve periodicity while M_2k does not, PARK the one-seed no-fresh-mask claim immediately.
IF_UNCLEAR: If a proposed primitive introduces nonuniform public masks, a different layout, nonlinear data-dependent routing, or fresh independently patterned auxiliary inputs, treat as DIFFERENT full construction; request typed source costs before testing.
WHICH_PAPER_GATE_CHANGES: Gate1 exact B158 selector/whole-output semantics; Gate2 stock automorphism operation class; Gate3 number of eliminated high-norm masks vs extra ciphertexts, rotations and key material.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: One-mask-seeded rail would amortize 12+ public selector operations and their observed 16-26-bit amplification without the failed 3-involution assumption. If period doubling cannot be achieved without importing new spatial structure, the advertised fixed-cost amortization mechanism is impossible within its interface grammar, so no native task is justified.

## Exact algebra and proof
Take H=16384 (one row), k=32, H divisible by 4k. Source mask
 M_k(i)=1 iff (i mod 2k)>=k, 0<=i<H,
so pattern 0^k 1^k repeated, exact period 2k. The next selector mask M_2k has pattern 0^(2k)1^(2k) repeated and satisfies M_2k(i+2k)=1-M_2k(i) on all indices mod H, so it is NOT 2k-periodic. At legal test input x=1, requested U_k row is exactly M_k, while U_2k must be M_2k.

Define P_(2k)={f∈F_T^H: f(i+2k)=f(i) for all i mod H}, extend row-wise to pairs of H-vectors. P_(2k) is a subalgebra under componentwise addition/multiplication, stable under each cyclic row shift and the row swap. Every row-constant public scalar, 0/1 rail, and even the full B158 state S_k at x=1 (all powers equal1) lies in P_(2k). Therefore a circuit built from the seed masked U_k, only such homogeneous rails/constants, stock row cyclic rotations/row swap, additions and ciphertext×ciphertext products can NEVER leave P_(2k), by induction over gates.
But U_2k requires M_2k outside P_(2k). Contradiction already for x=1; hence no exact all-legal-input construction using this grammar exists. This is a typed plaintext-function counterexample and does not rely on stochastic noise or any unverified Q-carry.
Read-only JS control k32,N256 (four 64-blocks) independently computed: seed M_32 shift by64 identical=true; next M_64 shift by64 identical=false; 32-slot block sums for M_64 are [0,0,32,32]. This is just an algebra sanity check, not a native cryptographic correctness canary.

## Distinctness / boundaries / prior art
Prior checkpoint-decoupled half-basis uses CLEAN unmasked A_k, then multiplies its row swap by NEW M_k at EACH stage; our impossibility does NOT apply to that route because it injects a fresh nonuniform public mask each stage. Prior Turn16 needed THREE independent involutive Galois axes; our proof uses ordinary existing cyclic shifts and rules out a SINGLE mask-seeded rail without new period structure. Prior B158 selector no-go established constant x^k row cannot yield *one* patterned row without a mask; here the SEED is ALREADY patterned, but no additional larger-period mask can be generated. This is a nonidentical obstruction with the same underlying equivariant algebra.
The result does NOT prohibit dyadic masked rails if the initializer contains masks of every later period, if arbitrary nonuniform plaintexts are supplied in later multiplication, if an independently computed extra rail with longer period is injected, if a different non-shift-equivariant slot layout/repacking is supported, or if programmable nonlinear selection or nonstandard automorphisms are charged. Such variants must pay full key, ct-pt, ct-ct, rotation, memory and offline costs; no paper-worthiness follows from the counterexample.
Closest prior art: basic equivariant circuit invariant / shift-periodic subalgebra; archived B158 current-layout mask-free obstruction, checkpoint half-basis scheme and Turn16 cyclotomic 2-torsion gate. The obstruction is not independently audited or demonstrably a publishable theorem.

## Gate and decision
Gate1 FAIL exact required M_2k slot semantics even under ideal noiseless x=1. Thus gate2 and gate3 cannot rescue the one-seed design; no use of native, no invalid performance claim. B175/B163 noise and full output stay as previously audited.
Candidate PARKED, NEW_MECHANISM=NO_CREDIBLE_NEW_MECHANISM for one-seed same-layout shift-equivariant masked rail.
REOPEN_CONDITION: A genuinely new source-compatible nonperiod-preserving operation or prepatterned rail with an explicit complete B158/8-block+root0 output construction, verified key/material/memory costs, a measured or proved positive fixed-Q noise/DFR and whole-system value bound, plus independent novelty; merely renaming a rotation or suppressing M_2k is insufficient.
ELIMINATED_UNCERTAINTY: Can one 2k-periodic encrypted selector rail generate the next 4k-periodic selector exactly through shift-equivariant ring operations without importing new spatial pattern? No, P_(2k) invariant contradicts M_2k.
DECISION_CHANGED=true; research_frontier_exhausted=false. No other active/backups selected.
