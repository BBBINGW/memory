# BOOT RMFE Paired Same-Machine Throughput Native-Gate Contract

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 4/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

Read-before-write authority:
`BBBINGW/memory main@fde6015a165fa3cad9e0da49a1ab532f0df86350`.

Turn 3 established:
- current rank-5 joint recovery can be four physical j=1 KS;
- stock HElib Frobenius strategy materially changes physical-hop counts;
- BSGS+10 direct RM10 matrices gives current recovery 14 physical KS;
- the +10 augmentation has exact +5.555556% Frobenius DCRT payload and <5.557% serialized-PubKey overhead.

Turn 2/R4 supplied a source-faithful local baseline timer decomposition, but the public latency/throughput frontier comes from Aung et al.'s Xeon 8368Q measurements.

This turn asks exactly one experimental-design hypothesis:

> Can the next native gate give a scientifically decisive throughput verdict by timing only the candidate recovery locally and substituting that number into Aung's published absolute-second frontier?

Falsifier:
the candidate timing and published fixed-stage/thin timings are not proven to be on the same hardware/performance basis, so an absolute-second splice is not a valid decisive throughput comparison.

No native task is executed in this turn.

## Result: absolute-second splicing is not decisive

Aung et al. ePrint 2025/350 defines

[
operatorname{throughput}
=
rac{	ext{post-bootstrap capacity}	imes#	ext{slots}}
     {	ext{latency}},
]

with (#	ext{slots}=kell).

For (m=32768,p=5):
- (phi(m)=16384);
- (operatorname{ord}_m(5)=8192);
- hence (ell=2);
- RMFE (k=5) therefore has 10 packed slots;
- vanilla thin has 2 slots.

The published p=5 table uses:
- thin: capacity 151, latency 2.82 s, throughput 107.06;
- Corr./TnM: capacity 101, latency 11.3 s, throughput 89.08;
- Corr./BSGS: capacity 115, latency 15.0 s, throughput 76.48.

The R4 native timing was produced in a different originating runtime; current durable provenance does not prove that it used the same CPU/runtime basis as the paper's Xeon 8368Q measurements.

Therefore a local candidate latency cannot be inserted into

[
T_{m fixed}^{paper}=6.524 {m s}
]

and compared against 107.06 as a rigorous native verdict.

The old (2.909962) s middle budget remains a useful published-hardware design target and sanity reference, but not a local-machine hard pass/fail threshold.

## Paired same-machine comparison

The next decisive gate must measure three workflows on the SAME runtime:

1. **vanilla HElib thin bootstrap**;
2. **source-faithful stock Aung correction/trace-and-merge baseline**;
3. **current carry-compensated post-raw candidate**.

All three must use:
- same pinned HElib source;
- same (m=32768,p=5,r=1,bits=400) context construction;
- single-thread execution;
- same CPU/process affinity policy;
- same warmup/measurement protocol;
- the SAME evaluation-key set.

### Equal-keyset rule

Use BSGS Frobenius matrices plus the ten direct RM10 targets for **all three workflows**.

This prevents the candidate from obtaining an unfair key-set advantage.

It is conservative:
- the stock Corr./TnM trace path also benefits from the added direct (e=4096) matrix;
- vanilla thin may likewise use any relevant added direct matrix through the same key-switch map;
- the candidate still has the established 14 physical-KS recovery path.

Do NOT compare candidate BSGS+10 against a deliberately weaker stock-BSGS baseline.

Also do NOT confuse:
- **HElib Frobenius key-switch strategy BSGS**, an evaluation-key scheduling choice;
with
- **Aung Corr./BSGS**, a different algorithmic recode workflow.

The prior-work comparator for this candidate remains **Corr./TnM**.

## Candidate path under test

The candidate must start from the same logical input as the stock correction/TnM workflow and preserve all unchanged outer stages.

Current modified middle:

[
	ext{branchwise S2C / reLinearize / rawModSwitch}
ightarrow
	ext{typed carry-compensated two-channel aggregation}
ightarrow
	ext{one common recryptEkey reconstruction}
ightarrow
	ext{RM10}
ightarrow
	imes224 {m unit normalization}
ightarrow
	ext{chained rank-5 joint recovery}.
]

The four joint outputs are then passed to the existing correction DigitExtract/final-recode logic.

Do not benchmark:
- obsolete generic rank-16 direct recovery;
- cross-branch hoisting;
- pre-raw fusion;
- one-part dummy reconstruction;
- fresh-thin surrogate states.

## Direct throughput metrics

Let each measured run report final HElib capacity (C) and end-to-end latency (T).

Candidate throughput:

[
oxed{
Theta_{m cand}=rac{10 C_{m cand}}{T_{m cand}}
}
]

Stock Corr./TnM throughput:

[
oxed{
Theta_{m prior}=rac{10 C_{m prior}}{T_{m prior}}
}
]

Thin throughput:

[
oxed{
Theta_{m thin}=rac{2 C_{m thin}}{T_{m thin}}
}
]

Hence the same-machine ratios are

[
oxed{
R_{m prior}
=
rac{Theta_{m cand}}{Theta_{m prior}}
=
rac{C_{m cand}T_{m prior}}
     {C_{m prior}T_{m cand}}
}
]

and

[
oxed{
R_{m thin}
=
rac{Theta_{m cand}}{Theta_{m thin}}
=
5rac{C_{m cand}T_{m thin}}
       {C_{m thin}T_{m cand}}.
}
]

These ratios are the primary performance decision variables. They do not transfer absolute seconds across machines.

## Measurement protocol

Use:
- 5 warmups per workflow;
- 20 measured invocations per workflow;
- single-threaded;
- fresh valid ciphertexts;
- no rescue/retry;
- no parameter sweep;
- fixed code/configuration after measurement begins.

Record per invocation:
- end-to-end latency;
- stage latency:
  SlotsToCtxts / current-or-stock middle / DigitExtract;
- final capacity;
- final plaintext correctness;
- candidate joint-output correctness before DigitExtract;
- physical KS count;
- RM10 target hop count;
- joint j=1 hop count.

Also record once:
- serialized public/evaluation-key bytes;
- key-switch matrix count;
- exact ten RM10 direct targets;
- process RSS if available without changing execution semantics.

### Correctness unit

One candidate bootstrap invocation producing the packed output is ONE correctness/DFR trial.

Do not flatten its ten logical packed values into ten independent Bernoulli trials.

All logical coordinates must nevertheless match for an invocation to count as correct.

This task is a correctness/performance gate, not a statistical DFR proof.

## Decision rule

For each workflow compute:
- Aung-style throughput from mean latency and final capacity;
- median per-run throughput as a robust secondary statistic.

For (R_{m prior}) and (R_{m thin}), compute a deterministic bootstrap 95% CI using the measured invocation arrays.

### Immediate execution failure

Return `FAIL_EXECUTION_CONTRACT` if:
- candidate does not use exactly the intended BSGS+10 direct-target set;
- any RM10 target is not one physical hop;
- chained joint recovery is not four physical j=1 KS;
- source-faithful state boundary is violated.

This is not a scientific latency kill; it means the intended candidate was not measured.

### Correctness failure

If any candidate invocation decrypts incorrectly:

[
oxed{	exttt{FAIL_NATIVE_CORRECTNESS}}
]

and stop performance interpretation for that artifact.

No automatic rescue or parameter change.

### Performance outcomes

**Strong PASS**:

[
operatorname{CI}_{95}^{lower}(R_{m prior})>1
quad	ext{and}quad
operatorname{CI}_{95}^{lower}(R_{m thin})>1.
]

Interpretation:
current candidate establishes same-machine throughput improvement over both the direct prior-work baseline and vanilla thin; proceed to DFR/security/novelty closure.

**Prior-only PASS / thin FAIL**:

[
operatorname{CI}_{95}^{lower}(R_{m prior})>1,
qquad
operatorname{CI}_{95}^{upper}(R_{m thin})le1.
]

Interpretation:
candidate is an engineering improvement over Aung Corr./TnM but does not cross the thin frontier. Because high-level one-linear-phase novelty is already killed, park the branch as low publication value unless a distinct novelty claim survives.

**No prior-work gain**:

[
operatorname{CI}_{95}^{upper}(R_{m prior})le1.
]

Interpretation:
KILL the current candidate on systems value under this fixed parameter regime; do not spend further BOOT turns on DFR optimization for this implementation.

**UNCLEAR**:
otherwise, if either CI straddles 1.

Do not silently convert an UNCLEAR statistical result into PASS.

## Why this gate is higher information than a recovery-only benchmark

A recovery-only timer would still leave:
- hardware normalization;
- final DigitExtract capacity propagation;
- final correctness;
- thin-throughput comparison

unresolved.

The paired gate resolves all four in one bounded experiment while reusing the already-fixed candidate and unchanged DigitExtract.

It remains much smaller than a parameter sweep or a new research branch.

## Authorized task contract

TASK_ID:

`BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01`

Scope:
- fixed (m=32768,p=5,r=1,w=512,k=5,bits=400);
- pinned HElib `acdb264e1a991eaee35fd8b3c31bebe9528c49a1`;
- same BSGS+10 keyset for thin, stock Corr./TnM, and candidate;
- one implementation/configuration;
- 5 warmup + 20 measured each;
- no sweep, rescue, or alternative candidate;
- return raw per-run arrays, correctness, capacity, hop audit, serialized key bytes, provenance, SHA-256 artifact bundle.

The task result must return to Research GPT for independent audit before any PASS/FAIL scientific claim.

## Verdict

```text
RESULT:
  PASS_PAIRED_SAME_MACHINE_NATIVE_GATE_CONTRACT

LOCAL_CANDIDATE_SECONDS_PLUS_PAPER_FIXED_SECONDS:
  INVALID AS DECISIVE NATIVE COMPARISON

PRIMARY_METRIC:
  SAME-MACHINE THROUGHPUT RATIO

COMPARATORS:
  STOCK CORR/TNM
  VANILLA THIN

KEYSET:
  IDENTICAL BSGS+10 FOR ALL WORKFLOWS

CANDIDATE_SLOTS:
  10

THIN_SLOTS:
  2

STRONG_PASS:
  lower95(R_prior)>1 AND lower95(R_thin)>1

HARD_SYSTEMS_KILL:
  upper95(R_prior)<=1

PRIOR_ONLY_THIN_FAIL:
  PARK / LOW PUBLICATION VALUE ABSENT DISTINCT NOVELTY

CURRENT_CANDIDATE:
  READY_FOR_ONE DECISIVE NATIVE GATE

TASK_ID:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01

WHOLE_PIPELINE_DFR:
  NOT ESTABLISHED

PUBLISHABLE_NOVELTY:
  NOT ESTABLISHED

RESEARCH_FRONTIER_EXHAUSTED:
  false
```
