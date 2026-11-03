# BOOT / B158 — Turn 18 — bounded novelty/value preflight for sparse-R8 one-MultKey RMFE bootstrapping

Date: 2026-11-03 Asia/Singapore
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
CANDIDATE_ID: rmfe-subring-envelope-single-multkey-v1
PHASE: CORRECTNESS_GATE
BACKGROUND_NATIVE_TASK: BOOT-T11-R8-SMALL-CANARY-20261103-R2
BACKGROUND_TASK_STATUS: PENDING / UNKNOWN / DO_NOT_RERUN / UNTOUCHED

## Authority / scope

GitHub Notes was attempted first and remains degraded.
The user-supplied local Git authority for this turn is BBBINGW/memory HEAD==origin/main at
7e88e69d0282b991eb20a3258b45a81987ec7f64.
The current active-candidate state in the turn request additionally carries the Turn-17 guarded-fallback result.
This finding does not claim that any connector-visible branch supersedes the supplied local authority.

The background R2 source/workdir/binary/result were not read, modified, resubmitted, inferred, or duplicated.
No native task was launched.

This is a bounded public-literature preflight, not an independent novelty audit.
NOVELTY_STATUS cannot become CLEAR from this turn.

## Primary hypothesis

H18:
As of 2026-11-03, no inspected public work implements the exact current mechanism:

    Aung Method-1 projections
    -> sparse R8 coefficient carrier
    -> ONE ordinary BGV/HElib MultKey
    -> RM10 coordinate clearing
    -> one common recovered arbitrary-Z625 lift vector
    -> exact L0,L1,L2,L3 correction inputs,

although multiple sub-techniques and broad structural ideas are already prior art.

Falsifier:
a prior/public work already carries the k RMFE components through one BGV/BFV bootstrapping-key multiplication or an equivalent single MultKey and then reconstructs the correction-map interface needed by RMFE digit extraction.

## Search boundary

Bounded public search covered:
- IACR ePrint 2025/350 and related FIMD work;
- 2026 IACR ePrint index/searches for RMFE/FIMD/bootstrapping/direct MultKey;
- Geelen 2024/153 subring/sparse slot-to-coefficient work;
- Ma et al. 2024/164 power-of-two BGV bootstrapping transforms;
- Aung et al. 2022/771 FIMD/composite-RMFE recoding;
- Ling et al. ePrint 2025/957 / ACISP 2026 multi-valued functional bootstrapping;
- Descent-PBS ePrint 2026/2616;
- He et al. ePrint 2026/927 subring/decomposition-ring FHE;
- author publication listings and broad web/code searches for direct RMFE MultKey / single MultKey / RMFE-packed MultKey.

This is not exhaustive of unpublished work, patents in every jurisdiction, private artifacts, or all non-English literature.

## 1. Aung 2025/350 remains the direct problem statement

Aung et al. explicitly state in future work that:

    "It also remains to be seen whether the MultKey portion can be done directly on
     RMFE-packed ciphertext to avoid executing MultKey multiple times on the split ciphertexts."

Their p=5 correction/TnM workflow still performs:

    SlotsToCtxts
    -> k=5 split MultKey executions
    -> CtxtsToSlots
    -> correction DigitExtract.

Therefore the exact top-level gap:
    avoid repeated split MultKey in RMFE bootstrapping
is source-authentic and important.

But "the authors left it as future work" is not, by itself, novelty.

## 2. Broad shared-Frobenius / multi-output claims are NOT novel

### FIMD 2022/771

The original FIMD work already:
- represents RMFE linear maps by Frobenius/linearized-polynomial evaluations;
- exploits hoisting for many automorphisms of one ciphertext;
- introduces a three-stage composite-RMFE recode that reduces Frobenius/key-switching cost;
- permits arbitrary linear transformations during recoding.

The public patent-family disclosure associated with FIMD is even more explicit:
when several decode-like maps act on the same ciphertext, the same Frobenius automorphisms are computed once and reused across the maps.

Therefore the current Turn-13 observation:

    "compute one bank of sigma^j(R) and reuse it for G0,G1,G2,G3"

is a good implementation/composition result, but NOT a standalone novelty claim.

### Ling et al. 2025/957 / ACISP 2026

This work evaluates multiple functions over a shared input in BFV-based functional bootstrapping.
It shares the linear transformation/digit-extraction prefix and shared polynomial-power precomputation across outputs.

Therefore the broad statement:

    "derive multiple bootstrapping outputs from a shared encrypted intermediate"

is also prior art at the structural level.

## 3. "Merge before one expensive key switch" is also too broad

Descent-PBS 2026/2616 proves that module components can be merged/repacked through one public functional key switch,
removing a per-component repacking factor in a TFHE/FHEW module-to-ring setting.

This is not an RMFE/BGV collision:
- different ciphertext family;
- different secret structure;
- different bootstrapping semantics;
- functional key switching rather than Aung/HElib MultKey;
- no RMFE correction maps.

But it is a strong structural analogy.

Therefore do NOT claim generic novelty for:
    "merge k components before key switching"
or
    "pay one key switch instead of k."

The paper claim must stay specific to the RMFE/BGV bootstrapping obstruction and representation.

## 4. Subring/coefficient packing is known

Geelen 2024/153 gives power-of-two:
- sparse subring packing;
- slot-to-coefficient / coefficient-to-slot transforms;
- coefficient selection by trace/subsum.

Ma et al. 2024/164 gives highly optimized power-of-two BGV bootstrapping linear transformations and homomorphic-NTT machinery.

He et al. 2026/927 develops FHE directly over decomposition subrings / rings of Gaussian periods.

Thus:
- use of power-of-two subrings;
- sparse coefficient locations;
- trace-based coefficient selection;
- subring-aware FHE representations

are all prior-art ingredients.

The current sparse R8 carrier is only potentially novel in its exact role as a bridge between Aung Method-1 RMFE projections and ONE ordinary MultKey.

## 5. No exact public collision found

The bounded search did NOT find a public work that simultaneously does all of:

1. start from Aung-style RMFE/FIMD bootstrapping;
2. take the k Method-1 scalar projection ciphertexts;
3. inject them into one sparse coefficient carrier inside the same BGV ring;
4. execute one ordinary coefficient-domain HElib MultKey/recryption-key reconstruction;
5. recover the k arbitrary higher-p-adic component lifts from that one reconstruction;
6. derive all correction inputs L0,L1,L2,L3 from the SAME lift vector;
7. continue with Aung correction DigitExtract.

No inspected 2026 RMFE follow-up by the Aung/Lim/Tan/Wang author group closes this exact future-work item.
The 2026 RMFE ePrint hit found in the current archive (Nenya 2026/2672) concerns zkSNARKs over Z/2^kZ, not FHE bootstrapping.

Therefore:

    NO_EXACT_COLLISION_FOUND_IN_BOUNDED_PREFLIGHT.

This is NOT:
    NOVELTY_STATUS=CLEAR.

## 6. Revised novelty statement

The previous candidate description should be narrowed.

### Do not claim as standalone novelty

- shared Frobenius images across several linear outputs;
- subring coefficient selection;
- sparse coefficient packing;
- merge-before-key-switch as a generic principle;
- public fallback/guard as a cryptographic primitive.

### Candidate-specific technical delta

The strongest surviving delta is:

> A representation change that turns Aung's five post-projection thin plaintexts into one sparse R8
> coefficient carrier before the bootstrapping-key multiplication, so a single source-faithful ordinary
> MultKey reconstruction preserves enough exact coordinate information to recover one common arbitrary
> Z625 lift vector; RM10 plus public linear maps then reconstruct all four Aung correction inputs without
> restoring the five split MultKeys.

The nontriviality is not any one ingredient.
It is the compatibility proof across:
- Method-1 projection semantics;
- sparse coefficient placement;
- rawModSwitch/recryptEkey reconstruction;
- arbitrary dirty lifts;
- subring coefficient clearing;
- exact four-output correction maps;
- BGV metadata/noise semantics.

That should be the paper's novelty thesis if the native gates pass.

## 7. Conceptual contribution framing

A potentially stronger conceptual framing is:

    the repeated MultKey cost is not forced by RMFE semantics;
    it is a representation/interface artifact of splitting the RMFE components before the coefficient-domain
    bootstrapping-key multiplication.

The sparse carrier shows a route to delay the split/recode boundary until AFTER the expensive MultKey.

This is more defensible than:
    "we invent shared Frobenius maps"
or
    "we invent subring packing."

Whether this framing is publishable still depends on native correctness and value.

## 8. Published p=5 value ceiling

Aung Table 2 for m=32768,p=5,w=512,Corr.(TnM),k=5 reports approximately:

    SlotsToCtxts   2.284 s
    MultKey        4.732 s
    CtxtsToSlots   0.078 s
    DigitExtract   4.240 s
    Final         11.33 s
    post capacity 101
    throughput ratio vs thin 0.832.

The paper states that "MultKey" is the complete per-split lines 3--6 block:
ModSwitch, SlotsToCoeff, InnerProduct, CoeffToSlots.

Thus the published MultKey stage is about:

    4.732 / 11.33 = 41.8%

of end-to-end Corr.(TnM) latency.

### Idealized 5-to-1 ceiling

Under the deliberately optimistic screening assumption that:
- the five split executions cost equally;
- one candidate MultKey costs exactly one fifth of the published stage;
- all new RM10/G_r/certificate overhead is zero;

the saved time is:

    (4/5)*4.732 = 3.7856 s.

Ideal total:

    11.33 - 3.7856 = 7.5444 s.

Idealized maximum speedup:

    11.33 / 7.5444 ~=1.502x,

or about:

    33.4% latency reduction.

If the old 0.078 s CtxtsToSlots stage is also completely eliminated at zero replacement cost,
the ceiling is only about:

    1.52x.

Therefore the paper should NOT expect a multi-fold end-to-end latency win on the p=5 correction row.
The value case is a moderate but meaningful latency/throughput frontier improvement.

## 9. Break-even overhead gate

Using the same screening assumptions, the one-MultKey fast path has at most about:

    3.79 s

of new overhead budget before losing all latency advantage versus Aung Corr.(TnM).

If removal of the old 0.078 s CtxtsToSlots stage is credited, the budget is about:

    3.86 s.

The actual candidate adds at least:
- RM10: ten direct automorphism/add stages;
- shared recovery bank: seven nonidentity Frobenius/key-switch operations;
- four outputs: 32 public constant multiplications and 28 additions;
- cleanups;
- optional certified-canonical guard overhead.

These operations must fit inside the budget.

This is a pre-registered VALUE falsifier:

    if matched new recovery/certificate overhead >= approximately 3.8 s
    on the Aung p=5 reference profile,
    the candidate has no latency win over its direct RMFE baseline.

No benchmark is run in this turn.

## 10. Throughput-to-thin screening threshold

Aung reports the p=5 Corr.(TnM) throughput ratio versus vanilla thin bootstrapping as:

    rho_base =0.832

with:
    C_base=101
    T_base approximately11.3 s.

The current candidate retains the same RMFE packing count k=5.

Let:
    C_fast = measured post-bootstrap candidate capacity;
    T_fast = measured fast-path latency.

Holding slot count fixed relative to Aung's RMFE row, candidate throughput ratio versus thin is:

    rho_fast
      =0.832 * (C_fast/101) * (11.3/T_fast).

Thus candidate beats the published thin-bootstrap throughput only if:

    T_fast
      < 0.832*11.3*(C_fast/101)

      =9.4016*(C_fast/101) seconds.

If:
    C_fast approximately101,

then:

    T_fast < approximately9.40 s

is the preregistered threshold for throughput ratio >1.

Against the idealized 7.54 s one-MultKey ceiling, this leaves only about:

    1.86 s

for all new recovery/certificate overhead if capacity remains approximately101 and the goal is to beat thin throughput.

If capacity falls, the allowable latency decreases proportionally.

This is a screening formula, not a performance result.

## 11. Guarded-wrapper value consequence

The Turn-17 guarded variant preserves correctness by falling back to the split baseline.

It also requires:

    Keys_guarded = Keys_candidate union Keys_baseline

and five live post-projection snapshots.

Therefore the guarded paper variant currently has NO credible evaluation-key-size reduction claim.

Its value must come from:
- fast-path latency;
- expected latency after fallback;
- throughput/capacity;
- possibly reduced average MultKey work.

The Step-7 value report must include:
- unguarded fast latency;
- certificate overhead;
- fallback rate;
- guarded expected/worst-case latency;
- snapshot memory;
- union key footprint;
- post-bootstrap capacity;
- throughput ratio.

## 12. Paper-value interpretation

The published p=5 baseline has a real 4.732 s MultKey bottleneck, so the problem is important enough to test.

However, because the absolute best-case end-to-end speedup on that row is only around 1.5x under optimistic linear scaling,
a paper cannot rely on "5 MultKeys ->1" as a headline operation count alone.

A strong contribution needs at least two of:
- the representation-level conceptual result;
- convincing matched latency improvement;
- preserved/improved post-bootstrap capacity;
- throughput crossing a meaningful frontier such as thin baseline;
- a broader parameter regime where k or MultKey fraction is larger;
- reusable methodology for other RMFE/FIMD linear outputs.

No broader parameter claim is made yet.

## Verdict

PASS_IMPORTANT_SOURCE_GAP.
FAIL_BROAD_SHARED_FROBENIUS_NOVELTY.
FAIL_BROAD_SUBRING_PACKING_NOVELTY.
FAIL_GENERIC_MERGE_BEFORE_KEYSWITCH_NOVELTY.
NO_EXACT_COLLISION_FOUND_IN_BOUNDED_PREFLIGHT.
PASS_NARROW_REPRESENTATION_DELTA_SURVIVES_PREFLIGHT.
PASS_VALUE_CEILING_AND_BREAK_EVEN_GATE.

NOVELTY_STATUS=PREFLIGHT, not CLEAR.

PREBENCH_VALUE_GATES:
    direct-RMFE baseline latency win requires new recovery/guard overhead < approximately3.8 s
    under the published p=5 screening model.

    throughput-vs-thin requires:
        T_fast <9.4016*(C_fast/101) s.

GUARDED_KEY_SIZE_CLAIM:
    BLOCKED; union key set required.

NATIVE_STEP2_RESULT:
    UNKNOWN / PENDING.

CORRECTNESS_GATE=BLOCKED.
BASELINE_CORRECTNESS=PENDING.
SECURITY_GATE=PENDING.
VALUE_GATE=PENDING.
AUDIT_GATE=PENDING.
PAPER_READINESS=NOT_READY.

## Next action while R2 remains pending

Do not touch or resubmit R2.

If R2 becomes ready, independently audit it immediately.

Otherwise the next independent side unit should not repeat broad novelty search.
Highest-value options:
- audit whether the p=3 or other Aung rows create a materially larger value ceiling for the same mechanism, without native benchmarking; or
- prescout whether sparse-R8 one-MultKey generalizes from k=5 to the other interpolation-RMFE correction parameter sets.

Independent prior-art audit is still required before NOVELTY_STATUS can become CLEAR.
