# BOOT / B158_OVERALL — Successor Research Turn 18/25
Date: 2026-11-12 Asia/Singapore
TRACK_ID=BOOT; ACTIVE_SUBLINE=B158_OVERALL
PHASE=PROBLEM_SELECTION
CANDIDATE_ID=boot-b158-two-rail-virtual-selector-axis-unmasked-merge-v1
DECISION=FAIL_SINGLE_CIPHERTEXT_MASKFREE_MERGE / PARKED
NATIVE/CODEX=NOT_RUN

## Authority and novelty boundaries
Controller entry ACTIVE=UNKNOWN; no ranked BACKUP. Read-before-write retrieved:
- findings/boot-b158-successor-turn17-one-seed-dyadic-mask-rail-period-obstruction-2026-11-12.md, blob b5976c9bad23ccd8416a4b052c608cda3b649f67 (PARKED).
- findings/boot-b158-successor-turn16-three-involution-hypercube-selector-axis-source-gate-2026-11-12.md, blob 98f78fd4611aaf053465b3fb644c8e89b164044d (PARKED).
- findings/boot-B158-checkpoint-decoupled-halfbasis-gate-2026-10-28.md, blob 49a85b46bf23566b24324e0994b7f2830b136dc5 (historical alternative explicitly uses fresh masks).
- findings/boot-B158-residual-structural-rescue-scout-2026-10-28.md, blob d87795880d9df2f16c710f38fc7dfd94a0f4d771 (B163 late selectors increase required-logQ by ~20–26 bits).
- findings/boot-B163-native-artifact-audit-2026-10-28.md, blob b586517ec9e1505e69dd5e299c390357ec87b225 (fixed L18, final k8192 fails).
- Lattigo v6.2.0 source core/rlwe/evaluator_automorphism.go, blob 527b1fdf8fdd92b705896b555597c9cc40ee2609, lines10–17 and 24–50: Galois automorphism X->X^galEl, matching key, degree1 input/output, permutation on ring components.
Distinct from closed Turn16: that required THREE involutive Galois actions WITHIN ONE ciphertext, which do not exist. Here a physically separate rail-swap gives an additional VIRTUAL binary axis without requiring such Galois element. Distinct from Turn17: that attempted to propagate ONE spatially masked seed to later periods; here the two rails carry alternative UNMASKED branch values and no prepatterned masks.

## Registered question and distinct decisions
QUESTION: Can two degree-one RLWE ciphertext rails, an additional public swap of rail identities, existing row rotations/row swaps, public *spatially uniform* scalars, ciphertext adds and ct×ct operations, implement the output mux F_M(u,v)=(1−M)u+Mv for a nonconstant public B158 selector mask M while returning ONE standard packed ciphertext (the existing B158/Algorithm5 input contract), WITHOUT any per-slot nonuniform plaintext mask or independently patterned rail/key?
CURRENT_BELIEF: No: the listed operations are equivariant under simultaneous cyclic shift of the two input rails, whereas F_M with fixed nonconstant M is not.
CHEAPEST_DECISIVE_TEST: Prove the shift-equivariance invariant for permitted operations and falsify F_M on u=0,v=1, M=M32 with period64, and shift by one slot. Check stock automorphism operation class. No native or expensive derivation.
IF_PASS: If a stock, costed operation breaks equivariance and realizes the EXACT mux while preserving complete Q/T scale/carry and full output, admit ACTIVE for source/DFR/whole-system value preflight.
IF_FAIL: If all permitted operations are equivariant and F_M is not, PARK the exact mask-free two-rail-to-one-ct construction without native.
IF_UNCLEAR: If output remains two ciphertexts and external extraction changes the output contract, or there is a custom nonuniform layout-conversion operation, preserve it as a DIFFERENT candidate subject to explicit output/security/cost gates.
WHICH_PAPER_GATE_CHANGES: killer gate1 exact standard packed-output semantics, gate2 supported slot routing/key interface, gate3 optimistic all-in cost and fixed-Q noise advantage.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: Physical rail swap may evade the fixed-ring Galois 2-torsion restriction, but it is not the same as placing one public alternating selector across output positions. A purported mask-free design is not a complete construction if it cannot restore the required single-ciphertext slot layout; no native benchmarking can fix a failed exact mux.

## Full semantic theorem: two rails do NOT provide a spatial selector for free
Model the public decoded plaintext space of one physical row as F_T^H, H=16384 and T=65537. Inputs u,v are arbitrary row vectors; a candidate maintains them on distinct encrypted rails, which permits rail-swap (u,v)->(v,u). Let tau be a one-slot cyclic row shift, and D_tau act simultaneously on all rails and both rows. The primitive gates permitted by the candidate all COMMUTE with D_tau:
- row cyclic rotations commute as elements of the same abelian cyclic shift group;
- row-swap and rail-swap commute with a simultaneous same-offset row shift;
- public spatially UNIFORM scalar multiplication and addition commute;
- componentwise multiply commutes because tau(a*b)=tau(a)*tau(b) for slotwise product, as do all polynomial circuits built from these gates.
This applies to any bounded-depth/size circuit of the indicated grammar, regardless of number of rail swaps and multiplications. Hence its single-output plaintext function G obeys
  G(tau u,tau v)=tau G(u,v).
The desired fixed-mask selector function is
  F_M(u,v)=(1−M)*u+M*v,
where M_i∈{0,1} is nonconstant and position-dependent (B158 M_k).
Set legal inputs u=0_H and v=1_H. Then F_M(0,1)=M. Since tau 0=0 and tau1=1, any equivariant circuit G on these inputs must give a shift-invariant output, i.e. the SAME constant at all row positions. But F_M(0,1)=M32 is nonconstant: M32 has repeated pattern 0^32 1^32; tau M32 ≠M32. Contradiction.
Equivalently F_M(tau0,tau1)=M while tauF_M(0,1)=tau M≠M. Thus there is no EXACT mask-free two-rail-to-one-ciphertext operator in the specified grammar for all inputs.

Important scope: this is a general F_M(u,v) multiplexer theorem. It also directly applies to the specified full selector operation if the candidate's design contract requires an independent rail-to-slot selection for arbitrary branch values. It is NOT a proof that every more structured B158 state or any multi-ciphertext final output is impossible. The input control (0,1) is an algebraic legal plaintext control; whether arbitrary (0,1) arises as a particular restricted B158 intermediate state is not asserted. The candidate explicitly claims a reusable branch-agnostic selector conversion, so the control belongs to its stated interface domain.

## Source and cost implications
Lattigo's automorphism is a homogeneous Galois permutation/key-switch of a WHOLE degree-one ciphertext, not an arbitrary output-position-dependent cross-rail mux. A rail exchange in host code is simply exchanging ciphertext references; it does not insert a spatial selector into an RLWE ciphertext. Moving two rail outputs into ONE standard packed ciphertext requires a non-equivariant step, e.g. at least one public nonuniform slot-mask product, a special cross-rail packer/trace with equivalent output index knowledge, a modified packing encoding, or data-dependent selection; the cost and noise must be included. For a standard mask if legal, the identity
  F_M(u,v)=u+M*(v-u)
uses one mask multiplication plus additions; it defeats the candidate's promised *zero* spatial-mask operations. This is an existence example and not an optimal-cost lower bound for all custom packing algorithms. The proposed mechanism can maintain two RLWE rails at roughly 2x the live ciphertext component storage (degree1: two polynomials per rail), even before Galois/relin evaluation keys; the exact runtime, peak memory, and key costs are unmeasured and UNKNOWN.
Prior data demonstrate original B158 late masks cost ~20/26 required bits and B175 terminal SI remains incorrect; the ideal possibility of replacing many earlier masks but paying one final mask could still be interesting IF a completely different typed schedule/changed output-interface is supplied. This finding does NOT assert that changing one output contract is always unprofitable. It only kills the purported *mask-free single ciphertext mux primitive*. No full value/DFR/security proof or full Algorithm5 correctness is inferred.

## Paper gates, decision, reopening
Gate1: FAIL for branch-agnostic mask-free correct single packed output, by exact shift-equivariance proof.
Gate2: supported source operations implement only the equivariant action; no stock masked-rail-free one-ciphertext mux edge.
Gate3: BLOCKED because the intended interface does not exist; at least the simple public-mask reconversion pays a ct-pt mask and adds, plus two-rail memory (not a universal lower bound). Even an optimistic value comparison is not meaningful without valid whole-output.
Novelty: classical equivariant-function argument, not independent research contribution. No native/Codex.
STATUS=PARKED; NEW_MECHANISM=NO_CREDIBLE_NEW_MECHANISM under the defined grammar.
REOPEN_CONDITION: Provide an explicit source-compatible NON-equivariant cross-rail conversion OR different output contract with complete B158/Algorithm5 all-message/root-zero semantics, typed keys, exact Q/T scale and carry, verified DFR/noise plus fair conversion/rotation/ct×ct/memory/offline costs, and independent novelty. Merely swapping two rails is not evidence of a spatial mask.
ELIMINATED_UNCERTAINTY: Does an extra binary axis encoded only by two ciphertext rails, standard row rotations and uniform arithmetic suffice to implement a fixed nonconstant per-position mux when returning to a single standard packed ciphertext? No: homogeneous shift-equivariant circuits cannot output M from constant (0,1) inputs.
DECISION_CHANGED=true. research_frontier_exhausted=false; no active candidate/backup after PARK.
