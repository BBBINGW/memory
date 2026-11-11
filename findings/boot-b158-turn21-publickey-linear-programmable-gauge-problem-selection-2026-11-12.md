# BOOT / B158_OVERALL — Research Turn 21/25
## PROBLEM_SELECTION — public-key linear programmable gauge

Date: 2026-11-12 (Asia/Singapore)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_OVERALL
Candidate: boot-b158-publickey-linear-programmable-gauge-v1
Phase: PROBLEM_SELECTION
Final status: PARKED
Evidence grade: MATH / STATIC / SOURCE
Native: NOT RUN

## Distinctness

The durable state entering Turn 21 had ACTIVE=UNKNOWN. This candidate is distinct from:
- Turn 19 explicit finite zero-ciphertext codebook selection;
- Turn 20 exhaustive standard-PK EncryptZero coin-space selection;
- Turn 18 lazy relinearization;
- Turn 17 leaf-ring clean sidecar;
- prior B176 RGSW/CMux external-product routes.

Turn 20 bounded the support of standard PK EncryptZero because its runtime ephemeral multiplier is ternary. This turn removes that restriction: the evaluator multiplies a single public-key RLWE zero encryption by an arbitrary public ring polynomial v. That produces a much larger programmable gauge family without enumerating standard encryption coins.

## Registered decisive test

QUESTION:
Can a compact public evaluation object let the evaluator generate, for an arbitrary publicly chosen ring polynomial v, a valid zero ciphertext whose second component shifts the B175 gauge by v*a, while keeping the added error small enough and providing a polynomial-time public method to choose a useful short v?

CURRENT_BELIEF:
The RLWE public key algebra gives the programmable family cheaply, so Turn 20's support-cardinality ceiling is not fundamental. The likely blocker is the selection problem: finding a short v that makes c1+v*a land in the favorable centered region is a high-dimensional modular short-preimage/CVP problem. Stock Lattigo supplies the multiplication primitive, not a public short-preimage selector.

CHEAPEST_DECISIVE_TEST:
1. inspect exact Lattigo v6.2.0 public-key / secret-key zero-encryption relations;
2. derive the exact public programmable-zero construction;
3. derive its added-error bound and optimistic cost;
4. identify the exact public selection problem for v;
5. compare that problem with standard lattice short-preimage/trapdoor prior art;
6. admit the candidate only if a source-backed polynomial-time public selector exists or follows directly from the available interfaces.

IF_PASS:
If a polynomial-time public short-preimage selector exists with controlled error/cost and without changing the trust/security model, promote the candidate ACTIVE and next run a small B175 component-shaping correctness/noise canary.

IF_FAIL:
If the algebraic programmable family exists but selecting a useful short v requires an unavailable trapdoor/new primitive or an unsupplied CVP/preimage algorithm, PARK. Do not native-test an oracle-only construction.

IF_UNCLEAR:
Do not promote. Preserve programmable-gauge-with-trapdoor as a separate future mechanism requiring a new security proof and cost model.

WHICH_PAPER_GATE_CHANGES:
Killer gate (2): complete constructive/source feasibility, including the public selection algorithm. Killer gate (3) is evaluated only as an oracle optimistic ceiling.

WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION:
Turn 20 left one natural escape: compact programmable gauge generation. If a standard public key already supplies the gauge image but the remaining selection task is exactly a missing short-preimage solver, then the frontier moves from information-theoretic support to computational construction. Native execution cannot resolve that missing algorithm.

## Exact source facts

### Lattigo public key is an RLWE zero encryption

Primary source:
  tuneinsight/lattigo v6.2.0
  core/rlwe/keygenerator.go
  blob 3583c5bb72e802a9b338d0d1fc8ba24a9ea58e72.

`GenPublicKey(sk, pk)` invokes secret-key `EncryptZero` on a QP degree-one element.

Source:
  core/rlwe/encryptor.go
  blob ce9b051c11e062b9b5db82dd392b86bdf279e52c.

For secret-key zero encryption the exact relation is constructed as
  c1 = a uniform ring element,
  c0 = -a*s + e,
so
  c0 + c1*s = e.

The same relation holds modulo any Q-prefix level used by the B175 gate.

## Programmable-zero theorem

Let the public key Q-part at the target level be
  PK=(b,a)
with
  b + a*s = e_pk mod Q.

For any evaluator-chosen public ring polynomial v in R_Q define
  Z_v := (v*b, v*a).

Then
  Dec_s(Z_v)
    = v*b + v*a*s
    = v*(b+a*s)
    = v*e_pk mod Q.

So Z_v is a valid noisy encryption of plaintext zero, generated with no secret and no additional evaluation key.

Adding it to a runtime ciphertext C=(c0,c1) gives
  C' = C + Z_v
with
  c1' = c1 + v*a
and plaintext unchanged modulo T, subject to the added phase error v*e_pk.

This strictly dominates the Turn-20 standard EncryptZero support restriction: standard PK encryption permits only small ternary ephemeral multipliers plus fresh errors, whereas this construction lets the evaluator choose arbitrary v and directly multiply the public key.

## Gauge-image condition

If the public polynomial a is a unit in R_Q, multiplication
  v -> v*a
is a bijection of R_Q.

Thus unrestricted v gives the ENTIRE c1 gauge image R_Q. The Turn-20 support-cardinality obstruction is therefore not a fundamental obstacle to programmable gauge generation.

At the NTT-friendly B175 modulus factors, a uniform public-key a is a unit except when at least one CRT/NTT coordinate is zero. This event is small for the large source primes and can in principle be detected publicly at key generation; a retry policy is possible. No exact probability claim is needed for the decision of this turn.

## Error bound

Let E_pk bound the coefficient infinity norm of the public-key zero-encryption error e_pk and let B bound ||v||_infinity. Then negacyclic convolution gives
  ||v*e_pk||_infinity
    <= ||v||_1 * ||e_pk||_infinity
    <= N * B * E_pk.

Using the source-level conservative bounded-error value E_pk<=20 and N=32768, the B175 required-bit convention
  r(Z_v) = bitlength(2*T*||v*e_pk||_infinity)
gives the optimistic sufficient condition
  log2 B <= r_target - log2(2*T*N*20).

Since
  log2(2*T*N*20) ~= 36.322,
one may allow approximately
- B <= 2^580.68 while keeping r(Z_v)<=617;
- B <= 2^596.68 while keeping r(Z_v)<=633.

Therefore the added public-key error does NOT by itself produce an immediate numerical impossibility. Under an oracle short-preimage selector, a very large coefficient range for v remains compatible with the existing B175 input-noise scale.

This is an optimistic ceiling only. Actual cancellation/wrap, component carry and the final SI output still require native verification if the construction ever becomes algorithmically complete.

## Cost ceiling under an oracle selector

The current B175 implementation has no public key. Durable source auditing estimated a full public key at roughly 12 MiB raw payload under the fixed parameters, small relative to the approximately 1.1 GiB existing evaluation-key material.

At runtime, once v is known and represented in the appropriate ring domain, forming Z_v requires only:
- one public polynomial multiply into pk0;
- one public polynomial multiply into pk1;
- two ciphertext-component additions.

No ciphertext-ciphertext multiplication, relinearization or new gadget key is inherently required.

Hence the oracle whole-cost ceiling is potentially attractive. The candidate is NOT parked on arithmetic cost.

## Exact missing construction: short public preimage selection

The evaluator must choose v so that two objectives hold simultaneously:
1. the public component representative is favorable, e.g.
     r = cent_Q(c1 + a*v)
   lies in a substantially smaller centered region;
2. v is short enough that v*e_pk does not destroy the decryption/noise budget.

Abstractly the selection problem is:
  given public a,t in R_Q and bounds B,R,
  find v,r with
     a*v - t = r mod Q,
     ||v|| <= B,
     ||r|| <= R.

For B175, t=-c1 and R is the desired favorable component region.

This is a bounded modular-convolution short-preimage / closest-vector style problem. Exact cancellation is easy algebraically when a is a unit:
  v0 = -c1*a^{-1} mod Q,
but the centered representative v0 is uncontrolled and generally gives no useful deterministic bound on v0*e_pk.

Therefore algebraic invertibility is not a selection algorithm.

## Prior-art boundary

Lattice trapdoor literature treats efficient short-preimage sampling for arbitrary targets as a trapdoor capability. For example:
- GPV-style/ring trapdoor implementations formulate the task as finding short ring-polynomial vectors mapping to an arbitrary syndrome and use a secret trapdoor to sample such preimages;
- recent Partial Lattice Trapdoors work likewise treats arbitrary short-preimage sampling as the functionality enabled by lattice trapdoors and discusses hardness without the relevant trapdoor.

These works are conceptually adjacent, not a direct collision with this B175 representation objective.

Important scope caution:
this turn does NOT prove that the single-ring bounded approximate-preimage problem above is SIS-hard under the exact B175 parameters, and it does NOT claim a reduction from B175 security. The literature comparison only establishes that 'publicly find a short preimage for an arbitrary modular target' is a standard trapdoor-type lattice task, not an operation supplied by stock Lattigo.

## Why stock gadget/evaluation keys do not close the gap

Lattigo `EvaluationKey` is a `GadgetCiphertext` encrypting an input-key gadget vector under an output key. `GadgetProduct(u, evk)` can homomorphically produce an encryption of a secret-dependent product with evaluation-key error.

A same-secret evaluation key can therefore be used to manufacture another programmable noisy-zero family. However:
- it adds a full gadget-product/key-switch-like online operation;
- its output c1 is itself a decomposition-weighted combination of random evaluation-key second components;
- choosing u to obtain a favorable final component again requires solving a public preimage/selection problem;
- it is strictly heavier than the direct public-key linear construction for this purpose.

Therefore the ordinary same-secret gadget key is not the missing selection algorithm and is dominated as a first implementation route.

## Decision

FAIL_CONSTRUCTIVE_SELECTION_GATE -> PARKED.

Candidate:
  boot-b158-publickey-linear-programmable-gauge-v1.

Important scientific outcome:
Turn 20's standard-PK support ceiling is NOT a fundamental no-go. A single RLWE public key, multiplied by arbitrary public v, exposes a full programmable gauge image when its second component is a unit.

But the candidate is not a complete algorithm: no source-backed polynomial-time public procedure is known here for finding a sufficiently short v that simultaneously moves the runtime B175 component into the favorable tensor/quantization region. Stock Lattigo provides the ring multiplication but not this selector.

Under the paper-first policy, an oracle-only preimage choice is insufficient to admit an ACTIVE algorithm candidate.

No native execution is justified.

## Reopen condition

Reopen this programmable-gauge family only with a concrete public polynomial-time selection mechanism that, for actual B175 runtime components, computes v satisfying both a useful component-shaping bound and a provable added-error bound.

Acceptable reopen evidence must include all of:
1. exact algorithm for solving the bounded modular-convolution preimage problem at the fixed source parameters, or a new trapdoor/evaluation-key construction that makes it efficiently solvable without exposing the FHE secret;
2. security analysis showing the new public selection/trapdoor material does not enable RLWE secret recovery or otherwise change the trust model unacceptably;
3. useful DFR/correctness bound including v*e_pk, component carries and downstream SI quantization;
4. key/storage/runtime cost, including any trapdoor-derived evaluation material;
5. at least a plausible route to >=16 required-bit recovery at the B175 pointwise gate.

Merely observing that a is invertible, using the uncontrolled exact inverse v0, publishing an ordinary same-secret evaluation key, or assuming an oracle short-preimage solver does not satisfy this condition.

## Eliminated uncertainty

Eliminated:
Is Turn 20's finite standard-PK support cardinality the fundamental reason public gauge shaping cannot work?

Answer:
No. Public linear multiplication of one RLWE public key yields a much larger programmable zero family and, when pk1 is a unit, the full c1 gauge image.

New localized blocker:
the missing public polynomial-time SHORT-PREIMAGE SELECTION algorithm with controlled added error and preserved security.

## Evidence references

- findings/boot-b158-turn20-standard-pk-coinspace-gauge-shaping-problem-selection-2026-11-12.md; blob 9b090a29f8553d7d77e9d7b573241b38bf27695f.
- findings/boot-B175-common-lineage-gauge-accessibility-2026-10-29.md.
- findings/boot-B175-decryption-fiber-gauge-realizability-2026-10-29.md.
- findings/boot-B175-source-level-si-error-bounds-2026-10-29.md.
- Lattigo v6.2.0 core/rlwe/keygenerator.go blob 3583c5bb72e802a9b338d0d1fc8ba24a9ea58e72.
- Lattigo v6.2.0 core/rlwe/encryptor.go blob ce9b051c11e062b9b5db82dd392b86bdf279e52c.
- Lattigo v6.2.0 core/rlwe/gadgetciphertext.go blob 6a0aeb4b209944f5f946d2352f46faf1683c762a.
- Lattigo v6.2.0 core/rlwe/evaluator_gadget_product.go blob 4cb8ab5f0db874fb41eea57c6e26527aa2c4b3e9.
- Lattigo v6.2.0 core/rlwe/utils.go blob 98f760bd2b226b860d5d51599e12a578f9b9a0a6.
- Albrecht, Lai, Lapiha, Woo, Partial Lattice Trapdoors, ePrint 2025/367.
- Dai et al., Implementation and Evaluation of a Lattice-Based Key-Policy ABE Scheme, ePrint 2017/601, for ring short-preimage/trapdoor background.
- B175 native artifact SHA256 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa.