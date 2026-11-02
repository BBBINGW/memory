<!--
Authority provenance:
- track: BOOT
- subline: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
- logical session: de72fdd0-c665-4611-9d0a-2e3575957355
- origin turn: 6
- bounded task: BOOT-T7-RECOVERY-WITNESS-20261102
- model: gpt-5.6-sol
- reasoning: medium
- zero_api_billing: true
- do_not_rerun: true
- task status: COMPLETED
- report sha256: 12983b3467c9a4728ed0add15655a2b26ae0871bc1e0976b1296a3e3321a3305
-->

# BOOT / B158 Turn-7 bounded recovery-witness report

Date: 2026-11-02 (Asia/Hong_Kong)  
Task ID: `BOOT-T7-RECOVERY-WITNESS-20261102`  
Scope: current `PRE-TAG + POST-DIVIDE LATE AGGREGATION` candidate only

## Required verdict fields

```text
CONSTRUCTION_IMPLEMENTED: NO
EXACT_17_CALLS_VERIFIED: UNCLEAR
TWO_SLOT_PROJECTORS: UNCLEAR
EXACT_Z625_L0_L3: UNCLEAR
NOVELTY_STATUS: NARROW / CONDITIONAL / NO EXACT COLLISION FOUND; the 17-call recovery is prior-art/natural-specialization material, not standalone novelty
SECURITY_GATE: PENDING / UNCLEAR; public-linearity and inherited FULL-Frobenius key-family compatibility are only conditional until the concrete global circuit is defined
VALUE_GATE: PENDING; optimistic window remains, but requires at least a 10% end-to-end latency gain or a strict Pareto gain under matched resources
PAPER_READINESS: NOT_READY
```

Overall disposition: **STOP — SOURCE/CONSTRUCTION SPECIFICATION BLOCKED**.

This is not an algorithmic no-go and not a resource-limit obstruction. It is an incomplete-construction error: the durable material does not define the mathematical object needed to execute one global 17-call circuit on both physical slots. Constructing a same-coordinate extractor and post-hoc swapping/scaling its slot-1 answers would be a simulated oracle, not an implementation witness.

## Step-0 novelty/value preflight

Preflight decision: **VIABLE ONLY AS A NARROW, CONDITIONAL FULL-MECHANISM CANDIDATE; proceed to the construction sufficiency check, but do not attribute novelty to recovery itself.**

### Comparison with the historical POST-RAW carry-corrected candidate

The historical candidate repaired early fusion with explicit raw-mod-switch carry handling and fused at a post-raw boundary. The current candidate does something materially different: it keeps all tagged branches independent through `rawModSwitch`, `newMakeDivisible`, and division by 5, then aggregates the public post-divide pairs immediately before the common affine `recryptEkey` reconstruction. It therefore avoids making an HPS/carry kernel part of the primary mechanism.

That ordering is the genuinely different part of the current construction. Historical POST-RAW correctness, timing, capacity, and native artifacts were treated only as comparator context and were not used as correctness evidence here.

### Comparison with Aung et al., PKC 2025

Aung already discloses the broad goal of avoiding repeated MultKey work on split RMFE ciphertexts. Aung Proposition 3 and its multi-output linear-map treatment also make joint linear recovery/correction a natural consequence once an appropriate packed/restricted state exists. Therefore none of the following is a defensible standalone novelty claim:

- direct-RMFE-MultKey as a high-level objective;
- shared rank-5 linear recovery;
- simultaneous production of correction images;
- a Frobenius/Moore representation of the recovery map.

### Comparison with nearest already-audited packed/restricted-transform work

The durable audits already classify the broad neighboring ideas as prior art: Chen–Han-style packed bootstrap/one common key-dot-product architecture, Halevi–Shoup linearized-polynomial/Frobenius maps, FIMD component-linear folding, Geelen-style binary unpack and sparse coefficient selection, Ma et al. restricted/thin-state transform simplification and fusion, and Peikert–Pepin structured sparse automorphism decompositions.

Consequently, the target-pruned 17-call recovery is best classified as an instance-specific natural specialization/optimization of known linear-transform and binary-unpack machinery. Its `17` count may be useful engineering evidence, but is not itself a paper contribution.

### What remains genuinely new enough to test

The only credible novelty window is the complete obstruction-and-repair package:

```text
Aung repeated-MultKey bottleneck
-> exact failure of naïve early fusion under HElib representative/carry semantics
-> branch identity preserved across every nonlinear preprocessing step
-> aggregation at the first useful affine post-divide boundary
-> one shared reconstruction
-> target-only recovery and exact Aung correction interface
-> material matched latency/Pareto improvement
```

The elementary post-divide distributivity identity and the recovery circuit are individually too weak. Durable value evidence leaves an optimistic window because the declared transform-side count falls from `75` to `23` and reconstruction from `5` to `1`, while five forward/nonlinear preprocessing paths remain. That operation ledger is not a latency prediction. The declared paper-value frontier remains: at least a 10% end-to-end latency gain or a strict secondary Pareto gain under matched key/resource accounting. No current native result establishes either.

## Construction-sufficiency audit

### What is pinned

The durable current-candidate evidence pins:

- modulus `625`, local degree `8192`, and normalization `8192^-1 = 28 mod 625`;
- selected first-slot coordinates `J=[0,1024,7168,2048,6144]`;
- Frobenius exponent labels `4096,2048,1024,512,256,128,64,32,16,8,4,2,1`;
- active-node counts `[1,1,1,1,1,1,1,1,1,1,1,2,4]`, whose sum is 17;
- the five selected rho transports and `182^-1=443 mod 625`;
- label inversion `[2,0,3,1,4] -> [C1,C3,C0,C2,C4]`;
- the symbolic correction formula `L_r=sum_i A_i*phi(e_i)^(5^r)` for `r=0,1,2,3`.

These facts validate a schedule/count oracle and the desired leaf interface. They do not define an executable global circuit.

### Minimum missing mathematical object

The minimum blocker is a **complete two-physical-slot representation of the global recovery operators**, sufficient to evaluate every visited node without direct coordinate access. Any one of these equivalent specifications would close the gap:

1. The exact degree-8192 local quotient-ring polynomial/basis for each physical slot, the chosen identifications of both slots with that basis, and a full formula for `rho(X)` (hence `rho(X^j)` for every `0 <= j < 8192`); or
2. The full `8192 x 8192` monomial/permutation-unit action of rho together with the exact local action of each declared Frobenius key; or
3. A source-faithful node recurrence that explicitly gives, for both slots and every active node, the automorphism map, even/odd masks, `X^(-2^i)` public multiplier as seen in each slot, normalization, child routing, and leaf pairing.

Only five values of rho are supplied:

```text
rho(X^0)    = X^0
rho(X^1024) = 182 X^7168
rho(X^7168) = 182 X^1024
rho(X^2048) = 182 X^6144
rho(X^6144) = 182 X^2048
```

Those values determine the desired final projector targets but do not determine rho on the intermediate public multipliers `X^(-2^i)` or on arbitrary dirty full-ring inputs. Similarly, the listed Frobenius exponents/key labels do not by themselves define their coefficient-vector action in the selected slot bases.

This is decisive because a ciphertext operation is global: one call must act on both physical slots simultaneously. Running two independent coordinate extractors, then pairing slot 0 from one leaf with slot 1 from another leaf, silently assumes a cross-slot operation that the candidate has not defined. It would also fail the user's prohibition on a direct-index/simulated-oracle witness.

### Secondary missing item

The current Turn-5/Turn-6 findings state the `L0..L3` constants symbolically as `phi(e_i)^(1,5,25,125)`. They do not contain a self-contained exact coefficient table tied to the current two-slot basis. Historical RMFE artifacts contain candidate constant tables, but importing them without the missing basis/transport definition would not repair the primary blocker and would risk crossing the mechanism/evidence boundary.

## Why no canary was written or run

No executable recovery source, deterministic input manifest, machine-readable recovery output, or test transcript was created. Doing so would require choosing unpinned ring/automorphism semantics. A test against an oracle sharing that choice would only show internal consistency of an invented model.

Accordingly:

- no naive same-coordinate negative control was fabricated;
- no `PASS` is claimed for 17 calls, two-slot projectors, normalization, branch inversion, or `L0..L3`;
- the static equality `sum(active-node counts)=17` is not upgraded to `EXACT_17_CALLS_VERIFIED`;
- no mod-5-only comparison was performed;
- no native program, HElib KeyGen, benchmark, expensive experiment, web request, or API request was run;
- the progress protocol was not activated because no long native program was created or run.

## Gate assessment

### Correctness

`UNCLEAR / CONSTRUCTION_SPECIFICATION_BLOCKED`. The abstract selected rho-projector identities, inverse label permutation, and symbolic correction-map algebra are consistent. The concrete one-circuit semantics are absent.

### Security

`PENDING / UNCLEAR`. The intended operations are public-linear and the handoff says the 13 exponent labels lie in the inherited FULL Frobenius family, suggesting no new key *type*. Exact key identities/resource parity cannot be verified until the circuit's automorphisms are fully defined. No security failure is established.

### Value

`PENDING`. Static call-count headroom does not kill the candidate, but no matched native latency, remaining-depth, key-byte, or RSS result exists for the current mechanism. The paper-value threshold remains at least a 10% end-to-end gain or a strict Pareto improvement.

### Paper readiness

`NOT_READY`. Recovery correctness is not executable, security/resource parity remains conditional, and value is unmeasured. The novelty story is narrow and depends on the full mechanism plus a material systems result.

## Files changed

Only this new task directory was touched intentionally:

```text
work/BOOT-RMFE-POSTDIVIDE-T7-RECOVERY-WITNESS-20261102/FINAL_REPORT.md
work/BOOT-RMFE-POSTDIVIDE-T7-RECOVERY-WITNESS-20261102/EVIDENCE_SHA256SUMS
work/BOOT-RMFE-POSTDIVIDE-T7-RECOVERY-WITNESS-20261102/SHA256SUMS
```

No orchestrator source, database, memory finding, historical work directory, or binary was modified. The pre-existing worktree had unrelated untracked files; they were left untouched.

## Commands actually executed

All commands were read-only except creation of this task directory. They used local evidence only. The command classes and exact decisive outputs were:

1. `sed`/`wc -l` over the three required findings. Exact line counts:

   ```text
   2041 boot-RMFE-postdivide-turn5-exact-four-output-interface-2026-11-02.md
    879 boot-RMFE-postdivide-turn6-recovery-source-audit-2026-11-02.md
   1097 orchestrator-HANDOFF-crypto-d3bf50a7-d808-41e6-a1d0-b56ad2f0d03c.md
   4017 total
   ```

2. `rg`/`find` searches for current recovery source and the named T16/T17/T22 checkers. Exact decisive result in the workspace and `/mnt/data`: no current executable recovery source was found; each explicitly probed `/mnt/data` artifact returned `MISSING`.

3. `sed`/`rg` over the narrow prior-art/value findings listed in `EVIDENCE_SHA256SUMS` and the predecessor handoff section that records only the exponent labels and active-node ledger. No literature audit was rerun and no web access occurred.

4. `rg`/`jq` inspection of existing historical RMFE constant artifacts, solely to determine whether the current findings were self-contained. This did not supply the missing full rho/two-slot operator semantics and was not used as correctness evidence.

5. `mkdir -p work/BOOT-RMFE-POSTDIVIDE-T7-RECOVERY-WITNESS-20261102`.

6. `shasum -a 256` over the eight evidence files. Exact results are in `EVIDENCE_SHA256SUMS`.

7. `git status --short`. It showed pre-existing unrelated untracked files, including `work/`; none was modified except the new scoped directory reported here.

8. After report creation: `python3 -m unittest discover ...` was **not** run because no implementation exists; final validation consists only of path/scope inspection and SHA-256 hashing.

Some exploratory `rg`/`sed` outputs were intentionally bounded or tool-truncated because the findings and historical JSON arrays are large. No claim relies on omitted output; the exact evidence-file hashes pin the inspected inputs.

## Single credible next action

Provide one durable, source-faithful **full two-slot recovery operator specification**: pin the local quotient rings/bases, full rho action (or an equivalent full monomial matrix), and the exact paired action/key identity for each of the 13 Frobenius labels and each `X^(-2^i)` multiplier. Then implement the 8192-coordinate deterministic canary exactly once against an independently written coefficient oracle. Do not proceed to timing before that canary passes exact mod 625 on both slots and the negative control.

