# BOOT / B158 — Turn 22 — independent-style prior-art stress test of the fixed-ring carrier mechanism

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: rmfe-subring-envelope-single-multkey-v1
PHASE: CORRECTNESS_GATE
BACKGROUND_NATIVE_TASK: BOOT-T11-R8-SMALL-CANARY-20261103-R2
BACKGROUND_TASK_STATUS: PENDING / UNKNOWN / DO_NOT_RERUN / UNTOUCHED

## Authority / scope

GitHub Notes read-before-write was attempted first and remains degraded.
Exact Turn-21 durable finding:
    findings/boot-successor-turn21-paper-level-value-review-anchor-vs-family-2026-11-03.md
    commit ae7a8199c159080948d2dedc0bc4ace22e8ffdfb
    blob 7c0bfc8a701e4392ca7acbfc3b8a108776966d97.

The target Turn-22 path was checked absent before write.
The background R2 source/workdir/binary/result were not read, modified, resubmitted, inferred, or duplicated.
No native task was launched.

This turn is a bounded independent-style novelty stress test, NOT the protocol's required independent prior-art audit.
NOVELTY_STATUS cannot become CLEAR here.

The web PDF screenshot requirement was attempted on the relevant public ePrint PDFs:
- Gentry-Halevi-Peikert-Smart field switching;
- Alperin-Sheriff-Peikert practical bootstrapping;
- Aung et al. FIMD.
The ePrint host returned HTTP 403 to screenshot requests. Claims below are restricted to text-extracted source passages and non-PDF public metadata/abstracts where applicable.

## Primary hypothesis

H22:
The broad "fixed-ring module carrier + trace-dual recovery + one key-switch/multi-output reuse" pattern may already be prior art. The active candidate survives novelty preflight only if its exact contribution is narrower:

    carry Aung Method-1 RMFE components through ONE ordinary HElib MultKey/recryption-key reconstruction
    in the SAME outer BGV ring/key context,
    then recover one common arbitrary p^e dirty-lift vector
    and derive the Aung correction-map interface.

Falsifier:
find prior art that already performs an ordinary BGV/BFV bootstrapping-key/recryption inner-product once on an RMFE/component carrier and then reconstructs all component/correction outputs from the same post-raw reconstruction state.

## 1. Strong prior art: field switching already contains the broad module/trace pattern

Primary source:
Craig Gentry, Shai Halevi, Chris Peikert, Nigel Smart,
"Field Switching in BGV-Style Homomorphic Encryption",
ePrint 2012/240, dated 2013 in the inspected PDF.

### 1.1 Extension/module viewpoint is old

The paper treats:
    K/K'
as a cyclotomic extension and:
    R/R'
as the corresponding ring extension/module.

It explicitly constructs R'-bases of R and uses the intermediate trace:
    Tr_{K/K'}.

The source states the standard universality fact:
for any K'-linear map L:K->K',
there exists fixed r in K such that:

    L(a)=Tr_{K/K'}(r*a).

At the quotient/plaintext level it further proves a bijection between:
- R'-linear functions on the cyclotomic quotient;
and
- componentwise finite-field linear functions on packed plaintext coordinates.

Thus the mathematical principle:
    "module coefficients can be recovered by trace-dual/trace-r maps"
is not novel.

### 1.2 One key switch followed by multiple linear outputs is explicitly old

The field-switching procedure is:

1. key-switch the big-ring ciphertext to a secret s' lying in the small subring R';
2. multiply by a public r encoding the desired R'-linear plaintext map;
3. take Tr_{K/K'} of the ciphertext components.

Crucially, the source explicitly states that steps 2 and 3 may be repeated multiple times on the SAME ciphertext produced by step 1, applying several different R'-linear functions and preserving the entire input plaintext in decomposed form.

Therefore the broad structural statement:

    one key switch
    -> several public trace-linear outputs from one ciphertext

is prior art.

### 1.3 Why this is not the exact candidate

Field switching changes:
- the target ciphertext ring/dimension;
- the secret-key domain, by switching to s' in a subring;
- the security argument, which relies on RLWE over the small field.

Its purpose is dimension/ring switching.

The active candidate instead:
- stays in the same outer m=32768 BGV ring;
- does not require the secret key to lie in the carrier fixed ring;
- introduces no small-ring key-switch hint;
- runs HElib's ordinary bootstrapping-key MultKey/recryption reconstruction;
- only afterward applies carrier-coordinate recovery as ordinary homomorphic plaintext linear maps.

So this is a very close structural prior, but not the exact Aung/MultKey mechanism.

## 2. Practical bootstrapping already uses common-subring linear maps and selected coefficients

Primary source:
Jacob Alperin-Sheriff, Chris Peikert,
"Practical Bootstrapping in Quasilinear Time",
ePrint 2013/372.

The paper uses hybrid cyclotomic rings and their largest common subrings E^{(i)}.
It homomorphically evaluates E^{(i)}-linear functions through ring-switching and explicitly develops "Mapping Selected Coefficients", using product-structured bases/subrings to retain only selected coefficients needed for bootstrapping.

Therefore the following broad ingredients are also old:
- choose a structured subring/module carrier;
- exploit a common subring to define legal linear maps;
- select/recover a chosen coefficient subset;
- compose these maps inside bootstrapping.

This further rules out novelty claims phrased merely as:
    "use a fixed subring/module to hold selected coefficients during bootstrapping."

## 3. Power-of-two subring coefficient selection is direct modern prior art

Geelen-Vercauteren BGV/BFV bootstrapping work and the later slot-to-coefficient treatment explicitly:
- encode sparse plaintext vectors in a power-of-two subring;
- use trace/subsum coefficient selection;
- remove coefficients whose exponents are not in the chosen subring;
- compensate the trace scale in a later linear transformation.

Thus the candidate's:
    RM10 coefficient clearing
and:
    power-of-two carrier subring
are supporting prior-art techniques, not standalone novelty.

## 4. FIMD/RMFE prior art already owns shared Frobenius decode/recode structure

Aung et al., ePrint 2022/771 "Field Instruction Multiple Data", already establishes:
- RMFE encode/decode/recode as linearized-polynomial/Frobenius maps;
- arbitrary linear transformations fused into recode;
- composite-RMFE three-stage recoding;
- hoisting/shared automorphism evaluation.

The public FIMD patent family, with priority 2021-03-12, is even more explicit:
for k' decode-like maps on one ciphertext, evaluate the same Frobenius automorphisms once and reuse them across all k' outputs; later recombine refreshed entries using a basis.

The patent text inspected contains no "MultKey" occurrence.
Its bootstrapping references cite ordinary HElib/FHE background rather than disclose direct RMFE bootstrapping-key multiplication.

Therefore:
- shared Frobenius bank;
- basis decomposition/recombination;
- multi-output RMFE linear maps

are prior art.

The candidate cannot claim them independently.

## 5. 2026 structural analogies further narrow generic claims

### Descent-PBS 2026/2616

The current ePrint index abstract states that a module accumulator's components are merged/repacked into a ring using one public functional key switch, removing a per-component repacking factor.

Different setting:
- TFHE/FHEW;
- module accumulator;
- public functional key switch;
- no RMFE correction maps;
- no HElib MultKey/recryptEkey reconstruction.

But it kills generic novelty phrasing such as:
    "merge components before one expensive key switch."

### Ling et al. 2025/957 / ACISP 2026

Multi-valued functional bootstrapping derives several functions from a shared encrypted input and shares substantial computation.

Again not an RMFE/BGV collision, but generic:
    "one shared encrypted intermediate gives several bootstrap outputs"
is not novel.

## 6. Closest 2026 subring-FHE source is SOURCE-GATED

He, Ling, Shi, Tan, Wang, Yang:
"Fully Homomorphic Encryption on the Ring of Gaussian Periods",
ePrint 2026/927 / CT-RSAC 2026.

Official abstract says:
- FHE over a decomposition subring of a decomposition ring;
- new encoding/decoding maps in that subring;
- reduced dimension and improved efficiency;
- up to 5.06x operation-latency improvement for selected parameters.

This is close enough in topic and has overlapping authors with Aung/FIMD that it must be included in an independent novelty audit.

However:
- official PDF fetch returned HTTP 403;
- GitHub Notes could not acquire a verified parseable full text;
- fixed public mirror did not yet contain the PDF;
- exact-title arXiv fallback was unavailable.

Therefore:
    FULL_TEXT_2026_927 = UNVERIFIED / RETRIEVAL_BLOCKED.

The abstract does NOT mention:
- RMFE;
- direct MultKey;
- correction maps;
- one dirty bootstrapping reconstruction.

So there is no abstract-level collision, but this source blocks NOVELTY_STATUS=CLEAR until its full text is independently checked.

## 7. Current 2026 RMFE/publication scan

A bounded current-publication scan found:
- Aung's 2025 RMFE bootstrapping remains the listed RMFE/FHE bootstrapping publication for the original author group;
- Khin Mi Mi Aung's 2026 listed works do not show a follow-up direct-RMFE-MultKey paper;
- current 2026 ePrint RMFE hit Nenya 2026/2672 concerns zkSNARKs over Z/2^kZ, not FHE bootstrapping;
- no current ePrint hit in this bounded search advertises direct RMFE MultKey closure.

This reduces, but does not eliminate, collision risk.

## 8. Reviewer-level collision matrix

### CLAIM A
"Use a cyclotomic/subring extension as a module over a fixed/common subring."

Verdict:
    PRIOR ART.

Sources:
    field switching;
    hybrid-ring bootstrapping;
    modern subring FHE.

Do not claim novelty.

### CLAIM B
"Recover module coordinates by trace-dual / Tr(r*a) maps."

Verdict:
    PRIOR ART / standard algebra.

Field switching already states universality of trace for subfield-linear maps and realizes packed coordinate maps.

Do not claim novelty.

### CLAIM C
"After one key switch, obtain several trace-linear outputs from the same ciphertext."

Verdict:
    PRIOR ART.

Field switching explicitly repeats its multiply+trace stage after a single key switch.

Do not claim novelty.

### CLAIM D
"Reuse a Frobenius bank across several RMFE linear maps."

Verdict:
    PRIOR ART.

FIMD paper/patent.

Do not claim novelty.

### CLAIM E
"Use trace/subsum to select a sparse power-of-two coefficient carrier."

Verdict:
    PRIOR ART.

Geelen/Vercauteren and earlier bootstrapping coefficient-selection work.

Do not claim novelty.

### CLAIM F
"Carry Aung Method-1 component ciphertexts through ONE ordinary HElib MultKey/recryptEkey reconstruction in the same outer ring, and only after the common raw reconstruction recover a same-lift p^e component vector for correction DigitExtract."

Verdict:
    NO EXACT COLLISION FOUND IN THIS STRESS TEST.

This is the surviving candidate-specific mechanism.

## 9. The precise technical distinction from field switching

A reviewer could reasonably ask:

    "Is this just Gentry-Halevi-Peikert-Smart field switching with a different basis?"

Answer: no, if and only if the paper states the distinction precisely.

### Field switching

The linear map is made ciphertext-compatible by FIRST switching to a secret key s' inside the small subring.
Then trace commutes with decryption because:

    Tr(c0+c1*s') = Tr(c0)+Tr(c1)*s'

for s' fixed by the trace group.

This produces a ciphertext in a smaller ring.

### Active candidate

The secret key is not placed in the carrier fixed ring.
Taking the carrier trace directly on a normal outer-ring ciphertext would not in general commute with:
    c0+c1*s.

Instead the candidate:
1. performs the ordinary source MultKey/recryption reconstruction under the stock HElib bootstrapping mechanism;
2. obtains one ordinary outer-ring ciphertext whose plaintext is the dirty reconstructed carrier Z;
3. only then evaluates the carrier trace-dual maps homomorphically, with ordinary automorphism key switching preserving the outer secret.

No ring switch or subring secret is required.

This is a different ciphertext interface.

## 10. The second precise distinction: dirty p^e reconstruction

The hardest candidate-specific correctness issue is also absent from the field-switching prior art.

HElib MultKey reconstruction contains:
    reLinearize(recryptKeyID)
    -> rawModSwitch(q=p^e+1)
    -> newMakeDivisible
    -> divide by p^{e'}
    -> recryptEkey reconstruction.

Integer rounding/carry in this path is not a linear map over the lifted integers.

Naively splitting/recovering components before and after these operations need not commute.

The candidate avoids that invalid commutation:
- all Method-1 components are first encoded into ONE carrier;
- one common raw reconstruction is executed;
- arbitrary high p-adic digits are accepted;
- coordinate recovery is applied only to the common post-reconstruction plaintext;
- all L_r are derived from that same arbitrary lift vector.

This "common dirty reconstruction -> same-lift correction interface" is the nontrivial bridge to Aung Algorithm 4.

Neither inspected field-switching work nor FIMD recode prior art supplies this HElib raw-reconstruction theorem.

## 11. Revised paper novelty thesis

The paper should NOT headline:

    "fixed-ring module carrier theorem"

by itself.

That theorem is best presented as a design abstraction / specialization of known trace-linear subring machinery.

The narrower defensible novelty thesis is:

> We resolve Aung et al.'s direct-RMFE-MultKey interface for a concrete BGV/HElib setting by
> embedding the split Method-1 components as fixed-ring module coefficients before the stock
> bootstrapping-key multiplication, carrying them through one common HElib raw reconstruction,
> and recovering a same-lift p^e component vector afterward for correction DigitExtract.
> The construction uses known subring/trace/Frobenius tools, but the placement across MultKey
> and the dirty-lift correctness bridge are the new mechanism under test.

The parameterized carrier family from Turns 19-20 remains useful as:
- a general design lemma;
- evidence that the mechanism is not p=5-specific;
- an implementation/value family.

Do not describe the underlying module/trace theorem as wholly new.

## 12. Exact collision criterion for the required independent audit

Mark NOVELTY_STATUS=COLLISION if any verified prior source is found that already does the following, regardless of terminology:

1. starts from multiple RMFE/FIMD/component plaintext values in one BGV/BFV ciphertext context;
2. encodes them as coordinates of one carrier before the bootstrapping-key/recryption inner product;
3. performs that expensive MultKey/recryption reconstruction only once;
4. after the integer/raw reconstruction, recovers all component p^e lifts from that same post-reconstruction state;
5. uses those common lifts to continue RMFE bootstrapping/digit extraction.

A prior source need not use:
    "fixed ring",
    "RM10",
    "R8",
or
    "same lift"
terminology to collide.

Field switching does not meet items 2-5 in this sense because it replaces the secret/ring interface rather than carrying the components through Aung's MultKey raw reconstruction.

## Verdict

FAIL_FIXED_RING_MODULE_THEOREM_AS_STANDALONE_NOVELTY.
FAIL_ONE_KEYSWITCH_MULTI_TRACE_OUTPUT_AS_NOVELTY.
FAIL_TRACE_DUAL_COORDINATE_RECOVERY_AS_NOVELTY.
FAIL_SHARED_FROBENIUS_BANK_AS_NOVELTY.
FAIL_GENERIC_SUBRING_COEFFICIENT_CARRIER_AS_NOVELTY.

PASS_NARROW_DIRECT_RMFE_MULTKEY_PLACEMENT_SURVIVES_STRESS_TEST.
PASS_DIRTY_LIFT_SAME_RECONSTRUCTION_BRIDGE_REMAINS_CANDIDATE_SPECIFIC.
NO_EXACT_COLLISION_FOUND_IN_BOUNDED_STRESS_TEST.

SOURCE_GATE:
    ePrint 2026/927 full text unavailable; must be checked before NOVELTY_STATUS=CLEAR.

NOVELTY_STATUS=PREFLIGHT.
INDEPENDENT_AUDIT_PASSED=false.

NATIVE_STEP2_RESULT=UNKNOWN / PENDING.
CORRECTNESS_GATE=BLOCKED.
BASELINE_CORRECTNESS=PENDING.
SECURITY_GATE=PENDING.
VALUE_GATE=PENDING.
AUDIT_GATE=PENDING.
PAPER_READINESS=NOT_READY.

## Next action while R2 remains pending

Do not touch or resubmit R2.

If R2 becomes ready, independently audit it immediately.

Otherwise the next independent side unit should not repeat general novelty search.
The remaining cheap paper-level uncertainty with highest value is a security/key-footprint pre-audit:
- compare candidate-required automorphism/recryption keys with the matched Aung baseline;
- determine whether the unguarded candidate actually adds any new RLWE key material or merely changes which existing matrices are used;
- separately account for the guarded union-key variant.

Independent prior-art audit must later obtain/check 2026/927 full text and the old field-switching/FIMD sources before NOVELTY_STATUS may become CLEAR.
