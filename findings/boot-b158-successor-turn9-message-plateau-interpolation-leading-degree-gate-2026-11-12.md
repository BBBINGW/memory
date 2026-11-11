# BOOT / B158_OVERALL — Successor Research Turn 9/25
Date: 2026-11-12 (Asia/Singapore)
Phase: PROBLEM_SELECTION
Candidate: boot-b158-message-plateau-interpolation-v1
Outcome: FAIL_MESSAGE_PLATEAU_HIGH_DEGREE / FAIL_BLOCK_DEPTH_VALUE -> PARKED
Native/Codex: NOT_RUN
TRACK_ID=BOOT; ACTIVE_SUBLINE=B158_OVERALL

## Authority, provenance, and distinctness
Entered with durable ACTIVE=UNKNOWN and ranked BACKUPS=none. Before derivation, GitHub repo verified:
- predecessor findings/boot-b158-successor-turn8-replica-lane-multilut-packed-si-gate-2026-11-12.md, Git blob e436406f0cc0e1a45ef9f2d3093642683f1603af (PARKED)
- findings/boot-B175-source-level-si-error-bounds-2026-10-29.md, blob c75aa60e080b28b688de7ee8859c5df4d1951c02
- findings/boot-B176-order8-crt-trace-linearization-2026-10-29.md, blob f3313571adb32e0fa6628eb9843a0799eddccc66
- findings/boot-B175-hybrid-frontier-research-value-ceiling-2026-10-29.md, blob 8923388e3e21796a2787b5b7043e2a62bbdf3eaa.
- prior closed Turn7 findings/boot-b158-successor-turn7-phase-domain-vanishing-polynomial-degree-value-gate-2026-11-12.md, Git blob 851ac6d6e7320559d517f4e6d477fbe10cacca64 (PARKED).
- B174 audited source finding findings/boot-B174-audit-si-grouped-marginal-and-pointwise-gate-2026-10-28.md, fixed T=65537, p=512, phase point (m,e,x)=(128,-63,16321) with x=128m+e and H=8192, eight PS blocks; B175 ZIP SHA256 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa, terminal SI required bits 664, Q bitlength 649, 32767/32768 decoded errors.

This candidate is NOT a reattempt to change the legal phase domain via vanishing-polynomial remainder (closed Turn7). Instead it tests a distinct source-semantic structure Turn7's arbitrary-phase-function degree dimension argument did not capture: the intended LUT is CONSTANT over all legal noise phases belonging to a single message, hence its function family has only 512 degrees of freedom, not 65024. The proposal is to exploit the message-plateau subspace for low-degree, low-depth *arbitrary message-LUT* interpolation even when the 65024-point input domain is large. This can in principle affect paper-level construction/value and is tested once before candidate admission. It does NOT reopen or rename the closed generic vanishing-polynomial candidate, and it makes no unsupported assertion about the complete source error distribution.

## Pre-registered decisive test
QUESTION: Under the most favorable canonical phase model x=128m+e in F_65537 with all 512 messages m and e in [-63,63], does restricting functions to message plateaus f(128m+e)=g(m), for ANY arbitrary g:{0,..,511}->F_65537, force the unique degree<65024 interpolant below the critical 8192-block or depth threshold, unlike arbitrary functions on 65024 phases?
CURRENT_BELIEF: The plateau constraint reduces the dimension of the function family but may not eliminate the top interpolation coefficient. One message-indicator function could still have a degree-65023 interpolant.
CHEAPEST_DECISIVE_TEST: Compute the coefficient of X^(|S|-1) for the message-zero indicator, using a complement-polynomial Lagrange identity; independently verify with direct barycentric denominator products. No native, Codex or FHE source change.
IF_PASS: If ALL 512 message-indicator leading coefficients vanish to an extent sufficient to remove a whole PS block or depth layer, retain ACTIVE for source-domain, source typed evaluator, full DFR, novelty and all-in value gates.
IF_FAIL: If ONE message indicator has a nonzero X^65023 coefficient, the generic arbitrary-message LUT family still requires degree65023; PARK this plateau-only degree compression because block/depth counts cannot change.
IF_UNCLEAR: If exact source legal domain differs, retain the computation explicitly conditional, verify legal phase support before any unconditional conclusion, and do not run native.
WHICH_PAPER_GATE_CHANGES: full-function correctness (message noise-plateau requirement), constructive polynomial degree lower bound and optimistic all-in value/novelty.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: If message constancy eliminated the high-degree terms, the earlier Turn7 no-value result could have been an artifact of treating phase-point outputs as independent. A nonzero leading coefficient for one legitimate message LUT eliminates that route for generic 512-entry functions under the tested domain, independent of runtime optimizations.

## Exact conditional message-plateau model
Let p=65537 be the prime plaintext modulus, M=512 messages, Delta=128. Define
 S_m = {128m+e (mod p): e=-63,..,63},  m=0,..,511,
 S=union S_m.
The 512 sets are disjoint, each 127 points: |S|=65024. This domain is an explicitly TESTED MODEL, not established as the entire formally guaranteed legal error set by B174's three fixed cases. It is consistent with a sampled B174 phase (m,e)=(128,-63), but that one sample cannot certify all errors in [-63,63].
Define plateau subspace W={ f:S->Fp | f(x)=g(m) for all x∈S_m for some arbitrary g on 512 messages}. W has dimension 512, not 65024. This corrects an important *interpretive weakness* of Turn7's argument: generic arbitrary per-phase f is strictly more general than an arbitrary message LUT with noise tolerance. We explicitly test whether W nevertheless contains a high-degree polynomial.

Complement C=Fp\S has |C|=513, exactly:
 C = {64+128m: m=0,..,511} union {65473}.
Proof: The contiguous 127-point intervals around consecutive centers 128m omit midpoint 128m+64; the top interval ends at 65471, the first negative interval wraps to 65474..65536, adding omitted 65473. There are no overlaps.
Define
 V_S(X)=prod_{x∈S}(X-x), D(X)=prod_{z∈C}(X-z).
Over Fp, X^p-X=V_S(X)*D(X).
For x∈S, differentiate: (-1)=V_S'(x)*D(x) because derivative of X^p-X is -1 in characteristic p and V_S(x)=0.
Hence
 1/V_S'(x) = -D(x) (mod p).
For any f:S->Fp, its unique interpolating polynomial L_f of degree<|S|=65024 satisfies
 [X^65023]L_f = sum_{x∈S} f(x)/V_S'(x) = -sum_{x∈S} f(x)D(x) (mod p).
Choose legitimate message indicator g_0(m)=1 for m=0, zero otherwise, so f(x)=1 on S_0, 0 elsewhere. Thus
 A0 := [X^65023]L_(g0) = -sum_{e=-63}^{63} prod_{z∈C} ((e-z) mod p) (mod p).
Exact modular computation gives A0=55591 !=0 in F65537. Therefore the UNIQUE interpolant for the valid arbitrary message LUT g0 has degree EXACTLY 65023, despite being piecewise constant on 512 error plateaus. A generic arbitrary message LUT has nonzero leading coefficient except for the one codimension-1 kernel of the nonzero linear functional g↦A(g) over Fp; all functions cannot be guaranteed a lower degree.

### Independent numerical confirmation
All modular multiplication uses residues below p and products below p^2 (< 2^53), so JavaScript Number arithmetic is exact:
Method A: Construct C by exact enumeration of F65537 outside S, evaluate D(e)=prod_(z in C)(e-z), compute (-sum_(e=-63..63)D(e)) mod p: 55591.
Computed four indicator leading coefficients for messages m=0,1,2,3 respectively: 55591,31397,15004,35511.
Method B: Independently enumerate the 65024-element set S and, for each x∈S0, compute V_S'(x)=prod_(y in S,y!=x)(x-y), modular inverse V_S'(x)^(p-2), and sum 127 inverses: 55591. Sample barycentric weights: x=65474 (e=-63):5756; x=0 (e=0):40699; x=63 (e=63):62825. Both algorithms agree.
Reproducible minimal pseudocode (source-independent):
  P=65537
  S={((128*m+e)%P+P)%P: m=0..511,e=-63..63}
  C={0,..,P-1}\S
  def D(x): return product((x-z)%P for z in C)%P
  A0=(-sum(D(e%P) for e in range(-63,64)))%P
  assert len(S)==65024 and len(C)==513 and A0==55591
  def inv(a): return pow(a,P-2,P)
  A0_check=sum(inv(product((x-y)%P for y in S if y!=x)%P) for x in S0)%P
  assert A0_check==A0
No native FHE operation was executed.

## Paper killer gates and value ceiling
Gate 1: The conditional message plateau semantics are fully modeled in finite field algebra, but actual B174/B175 source legal error support is still UNKNOWN. Exact model result: output is constant over all 127 noisy phases of message0 for indicator LUT, yet polynomial degree is 65023.
Gate 2: A polynomial of degree65023 is mathematically constructible, but a source-compatible implementation with lower cost is not provided; the candidate aimed solely to exploit semantic plateau to lower polynomial degree. Existing EvalPower/PS still needs ceil((65023+1)/8192)=8 blocks; and degree≥65023 implies ordinary arithmetic ct-ct depth≥ceil(log2(65023))=16 for a direct polynomial-in-x evaluation using constants/linear operations and binary multiplications. This is a lower bound in the stated ordinary arithmetic circuit model, not for full bootstrapping or arbitrary encoded/non-arithmetic function evaluation.
Gate 3: Under S63 even the best-case degree of one required message LUT crosses neither the eight-block threshold nor the algebraic depth threshold. No reduction in mandatory dynamic encrypted selector or B175 failing final SI follows. The particular random 512-output LUT may accidentally have a zero top coefficient but that does not establish an arbitrary-function construction. Additional effort to build the 65024-degree interpolation would only incur offline cost and has no credible new scientific value.
Novelty: classical Lagrange interpolation, vanishing-polynomial-based interpolation and known restricted functional bootstrapping ePrint2024/172; this proposed plateau observation is a mathematical obstruction/clarification, NOT a newly verified paper contribution. NOVELTY_STATUS=PREFLIGHT, not CLEAR.
Status: PARKED. NO_CREDIBLE_NEW_MECHANISM for the plateau-only degree reduction. No native, source modification, re-encryption, parameter change or new Codex task.
REOPEN_CONDITION: a source-authenticated narrower/different legal phase distribution with all-message and DFR coverage that provably reduces arbitrary-message LUT polynomial degree across a real block/depth threshold, or a genuinely distinct representation/evaluation primitive using plateau structure beyond single-polynomial interpolation, with full correctness, security, DFR, cost and novelty.
ELIMINATED_UNCERTAINTY: Does the 512-dimensional message-plateau restriction force all arbitrary 512-message LUTs to have low-degree interpolation over a 65024-phase domain? No: the message0 indicator has nonzero highest coefficient 55591, degree65023.
DECISION_CHANGED=true: distinct plateau-only candidate was screened and PARKED. No active/backups. research_frontier_exhausted=false, continue BOOT/B158_OVERALL new independent problem selection.
