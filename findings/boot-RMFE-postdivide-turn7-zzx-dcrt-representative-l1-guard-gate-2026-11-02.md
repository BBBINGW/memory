# BOOT / B158 — Research Turn 7/25 — ZZX-to-DoubleCRT representative / exact-L1 guard gate

Date: 2026-11-02 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
PHASE: CORRECTNESS_GATE
Candidate: legacy-484479fe4613 / PRE-TAG + POST-DIVIDE late aggregation
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Read-before-write / provenance

GitHub Notes read remains degraded for existing findings. Current durable state was recovered from
BBBINGW/memory at verified HEAD:

    02714acd580197928224a37eb3d21c98f6fce087

Immediate relevant findings:
- Turn6 full-ring dimension / exact-L1 provenance:
  findings/boot-RMFE-postdivide-turn6-full-ring-dimension-l1-guard-provenance-gate-2026-11-02.md
  blob 9ede92696c664ccc360eef9a432d28cc920ebbca
- Turn5 exact coefficient-L1 guard:
  findings/boot-RMFE-postdivide-turn5-exact-l1-reconstruction-noise-guard-gate-2026-11-02.md
  blob 3ba4587077e930372e2354d3f2943b61fcaf806d
- Turn22 shared reconstruction ciphertext-state/noise gate:
  findings/boot-RMFE-postdivide-turn22-shared-reconstruction-noise-state-gate-2026-11-02.md
  blob a83d906581b41d3cff380d2df165e7161544db7b

No prior finding explicitly tied the exact-L1 guard to the precise integer-polynomial representative
encoded by DoubleCRT at the shared reconstruction API boundary.

The target path was absent before write.

No native execution occurred.

## Closest implementation prior / exact delta

Closest implementation prior remains stock HElib recryption:

    ctxt = recryptEkey;
    ctxt.multByConstant(zzParts[1]);
    ctxt.addConstant(zzParts[0]);

Pinned HElib internally converts each public ZZX into a DoubleCRT over the current primeSet.

Turn5/6 established rigorous L1 bounds on the post-divide ZZX polynomials.
The remaining uncertainty is whether the DoubleCRT conversion changes the relevant representative
through a hidden reduction modulo Phi_m or a centered CRT lift, invalidating the supplied L1 size.

No novelty claim is added.

## Primary hypothesis

For the current fixed instance:

    m=32768=2^15
    phi(m)=16384
    q_boot=626
    rcData.mvec=[32768]

the aggregate post-divide polynomials

    Z0=sum_i z0_i
    Z1=sum_i z1_i

remain degree <16384 and are exactly the integer-polynomial lifts encoded by:

    DoubleCRT(Z0, context, primeSet)
    DoubleCRT(Z1, context, primeSet).

Pinned Cmodulus's power-of-two FFT path performs no extra reduction modulo Phi_m on such inputs.
Coefficient reduction modulo each ciphertext prime only encodes the same integer polynomial as a
residue-class element.

Therefore the exact coefficient-L1 bounds from Turn5/6 are valid canonical-size bounds for the
actual public ring multipliers/addends used by shared reconstruction.

## Falsifier

FAIL if any reachable pinned-source fact shows:
1. aggregate Z0 or Z1 can have degree >=phi(m);
2. DoubleCRT's ZZX constructor replaces the degree<phi(m) input by a different polynomial modulo
   Phi_m before multiplication/addition;
3. the power-of-two FFT path applies an additional cyclotomic remainder that can increase the chosen
   representative's canonical norm;
4. explicit size is interpreted as a bound on DoubleCRT::toPoly's centered CRT representative
   rather than on a valid integer-polynomial lift of the encoded ring element;
5. multByConstant/addConstant use a different public ring element from the supplied ZZX modulo the
   ciphertext modulus.

## Minimal decisive test

Audit only:
- degree/coefficients of post-divide and aggregate ZZX;
- DoubleCRT(ZZX,context,primeSet);
- Cmodulus::FFT for m power-of-two;
- multByConstant/addConstant use of DoubleCRT and explicit size.

## 1. Aggregate Z0,Z1 remain degree < phi(m)

Turn5/6 established that each post-divide z0_i,z1_i is produced from a length-phi(m) powerful vector
through the trivial converter and hence has:

    deg(z*) < 16384
    |coeff(z*,j)| <= 313.

Summing five such polynomials cannot increase degree.

Therefore:

    deg(Z0),deg(Z1) < 16384.

Coefficientwise:

    |coeff(Z0,j)| <= 5*313 = 1565
    |coeff(Z1,j)| <= 5*313 = 1565.

No polynomial reduction is needed merely to place Z0,Z1 in the canonical degree<phi(m)
representative space.

## 2. DoubleCRT constructor encodes the supplied ZZX directly

Pinned DoubleCRT::DoubleCRT(const ZZX&,context,s) does:

    map.insert(s);
    if deg(poly)<=0:
        special scalar path
    else:
        FFT(poly,s).

Pinned DoubleCRT::FFT then invokes, for every active ciphertext prime q_i:

    context.ithModulus(i).FFT(map[i], poly).

The source comment explicitly states that if coefficients exceed the product of used moduli they are
effectively reduced modulo that product. This is residue encoding, not a different semantic ring
element.

## 3. Current power-of-two Cmodulus FFT has no hidden Phi_m remainder

Pinned Cmodulus::FFT first converts the integer ZZX coefficientwise into zz_pX modulo the current
prime q_i, then calls FFT_aux.

For m a power of two, FFT_aux enters the special branch:

    if (zMStar->getPow2()).

It sets:

    phim = 1 << (k-1) = 16384

and directly copies the degree<=dx polynomial coefficients into a length-phim buffer, zero-padding
the remaining positions, followed by the FFT.

There is NO call to:

    rem(poly, Phi_m)

in this power-of-two forward path.

The non-power-of-two inverse implementation contains an explicit Phi_m remainder, but that path is
irrelevant here.

Since deg(Z0),deg(Z1)<phim, the current constructor never aliases or folds high-degree coefficients.

Thus each DoubleCRT row is precisely the evaluation/residue encoding of the supplied integer
polynomial Z modulo q_i.

## 4. Modular coefficient reduction does not invalidate the exact-L1 lift

Conversion to each q_i naturally replaces integer coefficients by congruent residues modulo q_i.

This does not require the L1 guard to be recomputed on a centered DoubleCRT::toPoly representative.

The actual ciphertext-ring multiplier is the residue class:

    [Z] in (Z/QZ)[X]/(Phi_m),

where Q is the current ciphertext modulus.

The original small integer polynomial Z is itself a valid lift of this residue-class ring element.

For every primitive m-th root zeta:

    |Z(zeta)| <= ||Z||_1.

Hence ||Z||_1 is a valid canonical-norm bound on a concrete integer lift of the multiplier actually
used modulo Q.

Noise analysis tracks the pre-modulus integer product using such a lift. If that resulting noise is
too large relative to Q, native capacity/correctness fails later; that is a genuine margin failure,
not a representative mismatch.

No requirement exists that the size bound be computed from DoubleCRT::toPoly's centered CRT lift.

## 5. multByConstant uses exactly the supplied DoubleCRT ring element

Pinned Ctxt::multByConstant(const ZZX& poly,double size):

    DoubleCRT dcrt(poly,context,primeSet);
    multByConstant(dcrt,size).

The BGV DoubleCRT overload:
- multiplies every ciphertext part by dcrt;
- updates:

    noiseBound *= size.

Therefore using:

    size = S1

where S1 rigorously bounds the chosen integer lift Z1 is source-consistent with the actual public
multiplier.

No alternate polynomial is substituted.

## 6. addConstant uses exactly the supplied DoubleCRT ring element

Pinned Ctxt::addConstant(const ZZX& poly,double size):

    addConstant(DoubleCRT(poly,context,primeSet),size).

The BGV DoubleCRT overload computes the standard representation factor f and adds:

    f*dcrt

to the one-handle part, while updating:

    noiseBound += size*|f|.

Thus S0 is a bound on the chosen integer lift Z0 of the exact public ring element being added.

Again, no centered DoubleCRT::toPoly representative is semantically privileged.

## 7. Consequence for Turn5/6 guard

The exact-L1 guard survives the API boundary unchanged.

For current candidate:

    S1 >= ||Z1||_embed
    S0 >= ||Z0||_embed

with the already proven hard bounds:

    S0,S1 <= 25,640,960.

The shared reconstruction:

    E*Z1 + Z0

therefore receives valid explicit size bounds on the actual public ring elements encoded by HElib.

The exact ciphertext-parts identity from Turn22 is unaffected because DoubleCRT construction is
linear in the supplied ZZX modulo every active prime.

## 8. Step3 native assertions

After Step2 PASS, Step3 should additionally assert:

1. deg(z0_i),deg(z1_i) < 16384;
2. deg(Z0),deg(Z1) < 16384;
3. every aggregate coefficient satisfies abs<=1565;
4. construct DoubleCRT(Z0/1,primeSet) on the actual shared reconstruction prime set;
5. optional debug round-trip:
   toPoly(back,false) must be coefficientwise congruent to Z modulo Q;
6. use the exact-L1 explicit sizes and verify finite noiseBound;
7. do NOT recompute correctness acceptance from the centered toPoly representative's L1.

The optional round-trip is an interface diagnostic, not the mathematical guard definition.

## Verdict

PASS_AGGREGATE_ZZX_DEGREE_LT_PHIM
PASS_POWER2_DOUBLECRT_NO_HIDDEN_PHIM_REDUCTION
PASS_ZZX_INTEGER_LIFT_MATCHES_DCRT_RING_ELEMENT
PASS_EXACT_L1_GUARD_SURVIVES_DCRT_ENCODING
PASS_SHARED_RECONSTRUCTION_SIZE_ARGUMENT_REPRESENTATIVE_SOUNDNESS

NATIVE_EXECUTION=NOT_OBTAINED
RECOVERY_CANARY=NOT_EXECUTED
CORRECTNESS_GATE=BLOCKED
BASELINE_CORRECTNESS=PENDING
NOVELTY_STATUS=PREFLIGHT
SECURITY_GATE=PENDING
VALUE_GATE=PENDING
AUDIT_GATE=PENDING
PAPER_READINESS=NOT_READY

## Scope boundary

This does NOT establish:
- positive native capacity;
- tightness of the L1 bound;
- native recovery correctness;
- Algorithm4 native correctness/noise;
- DFR;
- matched value.

It only closes a representation mismatch that could otherwise invalidate the Turn5/6 noise guard.

## Next decisive test

Mandatory evidence order remains blocked at Step2:
execute the frozen revised recovery-only canary against pinned HElib with HELIB_DEBUG=ON.

After Step2 PASS, Step3 should incorporate the ZZX/DoubleCRT representative assertions above before
the actual pure inverse/recovery checks.

No timing or performance inference is authorized.
