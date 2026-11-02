# BOOT / B158 — Research Turn 6/25 — full-ring dimension / exact-L1 guard provenance gate

Date: 2026-11-02 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613 / PRE-TAG + POST-DIVIDE late aggregation
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Read-before-write / provenance

GitHub Notes read remains degraded for existing findings. Current durable state was recovered from
BBBINGW/memory at verified HEAD:

    bc7a4dc9bef535e878fade6c5923e9b947922fae

Immediate relevant findings:
- Turn5 exact coefficient-L1 reconstruction guard:
  findings/boot-RMFE-postdivide-turn5-exact-l1-reconstruction-noise-guard-gate-2026-11-02.md
  blob 3ba4587077e930372e2354d3f2943b61fcaf806d
- Turn17 pure-EvalMap keyset parity:
  findings/boot-RMFE-postdivide-turn17-pure-evalmap-keyset-parity-gate-2026-11-02.md
  blob 1efcc7bdbe913d9cb137db1cc51a6c94e2a4b2d6
- frozen recovery canary source:
  findings/boot-RMFE-postdivide-turn11-helib-recovery-only-canary-source-2026-11-02.txt
  blob 6ae4bc7e48e0390f8dec97429f4ddb89565928c0

No prior finding explicitly proved that the Turn5 L1 guard uses the exact same rcData PowerfulDCRT
converter as rawModSwitch/newMakeDivisible while distinguishing the full ring dimension phi(m)=16384
from the slot extension degree d=8192.

The target path was absent before write.

No native execution occurred.

## Closest implementation prior / exact delta

Closest implementation prior remains pinned stock HElib bootstrapping.

No novelty claim is added.

Turn5's exact-L1 guard uses the hard coefficient bound after:

    rawModSwitch(q=626)
    -> newMakeDivisible(5)
    -> exact /5.

The remaining correctness uncertainty is representation provenance:
does that hard powerful-coordinate bound pass to the actual ZZX coefficients through the SAME
bootstrapping converter, and is the correct number of possible ZZX coefficients 16384 rather than
the local slot degree 8192?

This matters because using 8192 instead of 16384 would understate the deterministic L1 envelope by a
factor of two.

## Primary hypothesis

For the current fixed instance:

    m=32768
    p=5
    rcData.mvec=[32768]
    phi(m)=16384
    d=ord_32768(5)=8192
    nslots=2,

the actual p2dConv used by BOTH rawModSwitch and newMakeDivisible is exactly the PowerfulDCRT
constructed from rcData.mvec=[32768].

Because that mvec has length one:
- p2dConv is trivial;
- powerful coordinates and ordinary polynomial coefficients are identical;
- the vector length is phi(m)=16384.

Therefore Turn5's coefficient-L1 guard MUST count up to 16384 coefficients.
The local extension degree d=8192 is a slot-algebra dimension and MUST NOT be used to halve the
shared-reconstruction L1 bound.

## Falsifier

FAIL if any of the following is found:
1. RecryptData mutates or refactors mvec before constructing p2dConv;
2. rawModSwitch and newMakeDivisible use different PowerfulDCRT objects/factorizations;
3. p2dConv with current rcData.mvec is nontrivial;
4. the trivial converter copies only d=8192 entries instead of phi(m)=16384;
5. HElib's d=8192 is actually the polynomial-ring dimension rather than the slot extension degree;
6. the Turn5 5,128,192 per-polynomial L1 limit can be safely replaced by an 8192*313 bound.

## Minimal decisive test

Audit only:
- RecryptData::init provenance of mvec and p2dConv;
- rawModSwitch/newMakeDivisible converter calls;
- PowerfulDCRT trivial conversion length;
- EvalMap's d vs phim vs nslots split for this fixed m,p.

## 1. RecryptData preserves mvec exactly and constructs p2dConv from it

Pinned RecryptData::init accepts mvec_ and first checks:

    computeProd(mvec_) == context.getM().

It then records:

    mvec = mvec_;

and constructs:

    p2dConv = std::make_shared<PowerfulDCRT>(context, mvec).

There is no intermediate refactor, permutation, splitting, or replacement of mvec.

The same stored mvec is also supplied to the bootstrapping EvalMap objects.

Therefore the conversion basis and transform factorization share the same durable mvec contract.

## 2. Current m=32768 fixes mvec=[32768]

Turn17 already established the current exact parameter/resource contract:

    rcData.mvec.length() == 1
    rcData.mvec[0] == 32768.

This is also forced by the current prime-power structure:

    32768 = 2^15.

HElib EvalMap requires distinct mvec entries to be pairwise coprime.
There is no nontrivial decomposition of 2^15 into multiple pairwise-coprime prime powers >1.

Hence the production bootstrapping factorization is the one-factor vector:

    [32768].

## 3. rawModSwitch and newMakeDivisible consume the same rcData.p2dConv

Pinned Ctxt::rawModSwitch obtains:

    const PowerfulDCRT& p2d_conv = *context.getRcData().p2dConv;

and uses:

    p2d_conv.dcrtToPowerful(...)
    ...
    p2d_conv.powerfulToZZX(zzParts[i], pwrfl).

Pinned newMakeDivisible independently obtains:

    const RecryptData& rcData = context.getRcData();
    const PowerfulDCRT& p2d_conv = *rcData.p2dConv;

then uses:

    p2d_conv.ZZXtoPowerful(pwrfl, poly)
    ...
    p2d_conv.powerfulToZZX(poly, pwrfl).

Thus the rawModSwitch output, divisibility correction, and post-divide ZZX all use one and the same
converter instance/factorization.

There is no hidden cross-basis handoff between Turn5's coefficient-bound stages.

## 4. mvec length one makes the actual converter exactly identity

Pinned PowerfulDCRT constructor sets:

    triv = (mvec.length() == 1);

with the source comment:

    "triv means poly and pwfl bases are identical".

For current mvec=[32768], triv=true.

Pinned trivial conversions are:

    ZZXtoPowerful:
      VectorCopy(out, poly, phim);

    powerfulToZZX:
      conv(poly, powerful);

    dcrtToPowerful:
      dcrt.toPoly(poly);
      VectorCopy(powerful, poly, phim).

Therefore Turn5's powerful coefficient bound is literally an ordinary polynomial coefficient bound
for the actual rcData path.

No matrix/norm amplification is hidden between rawModSwitch and the ZZX pair aggregation.

## 5. The relevant vector length is phi(m)=16384

The trivial ZZXtoPowerful and dcrtToPowerful paths explicitly use:

    long phim = context.getPhiM();

and copy exactly phim coordinates, padding as needed.

For:

    m=32768=2^15,

    phi(m)=2^14=16384.

So every post-divide z0_i,z1_i belongs to the full cyclotomic ring basis:

    1, X, ..., X^16383

in:

    Z[X]/(X^16384+1).

The safe deterministic coefficient count is therefore 16384.

## 6. Why d=8192 is NOT the coefficient count

Pinned EvalMap separately defines:

    d = zMStar.getOrdP();
    phim = product_i phi(mvec[i]);
    nslots = phim / d.

For current:

    ord_32768(5)=8192,
    phim=16384,

hence:

    d=8192,
    nslots=2.

So d is the extension degree of each physical plaintext slot, while phim is the dimension of the
full polynomial/cyclotomic ring.

These quantities answer different questions:

    d=8192
      -> coordinates INSIDE each of the two physical slots;

    phim=16384
      -> coefficients of the full ZZX/cyclotomic polynomial representation.

The post-rawModSwitch/newMakeDivisible pairs are full-ring ZZX objects, not one isolated slot's
degree-8192 polynomial.

## 7. Concrete representation sanity check

The frozen recovery canary encodes this exact decomposition structurally:

    N = 16384
    D = 8192

and works in:

    (Z/625Z)[X]/(X^16384+1).

Its two CRT idempotent-like slot selectors contain both:

    X^0
    X^8192.

Thus even a state described by two degree-8192 physical slot components naturally occupies both
halves of the degree<16384 ring representation after CRT recombination.

This is a source-shape sanity witness only; the frozen canary remains unexecuted.

## 8. Turn5 bound is validated; an apparent factor-2 tightening is rejected

Turn5 established for every post-divide coefficient:

    |c_j| <= 313.

The correct rigorous whole-polynomial bound remains:

    ||z||_1
      <= 16384*313
      = 5,128,192.

For five branches:

    S0,S1 <= 25,640,960.

A tempting bound:

    8192*313 = 2,564,096

would use the slot extension degree in place of the full ring dimension and is NOT justified for
the rawModSwitch/post-divide ZZX objects.

Therefore:

    REJECT_L1_BOUND_USING_LOCAL_DEGREE_8192.

Turn5's existing numeric limits are confirmed, not loosened and not tightened.

## 9. Step3 exact-interface implication

After Step2 PASS, Step3 must explicitly distinguish:

    context.getPhiM() == 16384
    context.getOrdP() == 8192
    rcData.ea->size() == 2
    rcData.mvec == [32768].

The exact-L1 oracle must iterate over the full degree<16384 ZZX coefficient range or equivalently
over the actual ZZX coefficient representation with zero padding to phim.

Acceptance:
- every coefficient abs<=313;
- branch L1<=5,128,192;
- five-branch totals <=25,640,960.

Do NOT use d=8192 as the L1 coefficient count.

## Verdict

PASS_RCDATA_P2DCONV_PROVENANCE
PASS_RAWMODSWITCH_NEWMAKEDIVISIBLE_SAME_CONVERTER
PASS_CURRENT_TRIV_POWERFUL_POLY_IDENTITY
PASS_FULL_RING_DIMENSION_16384
PASS_SLOT_DEGREE_8192_DISTINCTION
PASS_TURN5_L1_NUMERIC_BOUND_VALIDATION
REJECT_LOCAL_DEGREE_8192_L1_TIGHTENING

NATIVE_EXECUTION=NOT_OBTAINED
RECOVERY_CANARY=NOT_EXECUTED
CORRECTNESS_GATE=BLOCKED
BASELINE_CORRECTNESS=PENDING
NOVELTY_STATUS=PREFLIGHT
SECURITY_GATE=PENDING
VALUE_GATE=PENDING
AUDIT_GATE=PENDING
PAPER_READINESS=NOT_READY

## Next decisive test

The mandatory evidence-order blocker remains Step2:
execute the frozen revised recovery-only canary against pinned HElib with HELIB_DEBUG=ON.

After Step2 PASS, Step3 should first assert the full dimension/provenance tuple above, then apply the
Turn5 exact-L1 reconstruction guard and the Turn4 path invariants before the real inverse/recovery
interface checks.

No timing, capacity, DFR, or performance conclusion is authorized from this static result.
