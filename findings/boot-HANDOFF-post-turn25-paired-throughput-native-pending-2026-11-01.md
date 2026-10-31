# BOOT Session Handoff — post Research Turn 25/25, paired-throughput native task still pending

Date: 2026-11-01
Session completed: 密码学 17.0
Turn 26 classification: HANDOFF ONLY
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Session accounting

Research Turns 1--25 are complete.

Turn 26 performs only state transfer. It does not:
- introduce a new hypothesis;
- start an experiment;
- alter the candidate;
- reinterpret the pending native task as complete.

The latest substantive result is:

\`Research Turn 25/25 — end-to-end static semantic-equivalence gate\`.

## Durable authority at handoff construction

Latest substantive commit before this handoff:

\`BBBINGW/memory main@56597dfabaf7047a9be26b94172451a29ad356f2\`

Latest Turn-25 finding:

\`findings/boot-RMFE-end-to-end-static-semantic-equivalence-gate-2026-11-01.md\`

Turn-25 finding blob:

\`02babe02f02658fab426fb21938fc7713a01c49a\`

## Pending native task — preserve exactly

Task ID:

\`BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01\`

Status at handoff:

\`UNKNOWN / BACKGROUND\`

The task may cross Research GPT session boundaries.

Do not:
- treat its result as known;
- modify its source/work directory/binary;
- resubmit it;
- start another heavy local native task while this slot remains occupied.

If the result becomes available, it preempts the next free substantive turn in the successor session for independent audit.

## Current candidate

Current surviving mechanism:

\[
\text{Aung SlotsToCtxts}
\to
5\times
\big(
\text{thin SlotsToCoeff}
\to
\text{reLinearize}(s_R)
\to
\text{rawModSwitch}
\big)
\]

then:

\[
\text{two typed raw-channel aggregation}
\to
\text{public carry correction}
\to
\text{one divisibility-lift/divide per aggregate channel}
\]

then:

\[
\text{one real recryptEkey reconstruction}
\to
\mathrm{RM10}
\to
\times224
\to
\text{joint rank-5 recovery}
\]

then the four outputs:

\[
L_0(z)=z,\ L_1(z),\ L_2(z),\ L_3(z)
\]

are passed into the stock Aung correction DigitExtract / final-recode logic.

## Static semantic status

Turn 25 established:

\`PASS_STATIC_END_TO_END_PLAINTEXT_SEMANTIC_EQUIVALENCE\`.

Under the explicit implementation/type assertions already persisted:
- branch prefix through rawModSwitch is source-identical;
- post-raw carry/divisibility fusion is exact;
- the two raw channels remain typed and are not cross-mixed;
- single \`recryptEkey\` reconstruction is CtxtPart-exact to the shifted sum of five stock reconstructions;
- RM10 + 224 is the exact normalized projector onto the R8 envelope subring;
- the post-RM10 state lies in the established rank-5 active domain;
- joint recovery outputs exactly \(z,L_1(z),L_2(z),L_3(z)\);
- temporary plaintext space is 625;
- temporary post-224 intFactor 399 is valid;
- downstream correction DigitExtract is well-typed;
- final input intFactor restoration is multiplicative, as in stock HElib;
- Aung Algorithm-4 precondition \(\eta=125=5^{e-1}\) holds.

This is plaintext/BGV semantic equivalence.

Do NOT upgrade it to exact post-map ciphertext/noise equality.

Native correctness, capacity, DFR, latency, throughput, remaining multiplications, and RSS remain empirical/unresolved.

## Current exact structural cost facts

### Recovery term / physical-KS structure

With the common BSGS+10 evaluation-key resource:
- candidate RM10 = 10 direct physical KS;
- joint rank-5 recovery = 4 direct chained \(j=1\) KS;
- candidate recovery = 14 physical KS.

Equal-resource Corr./TnM recovery:
- exact BSGS+10 recovery-side count = 95 physical KS.

Term-count shorthand \(70\to14\) is valid only as the older FULL/transform-term perspective; use \(95\to14\) for the current equal-resource BSGS+10 physical comparison.

### RM10 optimality

Turn 24 established:
- RM10 is the normalized 1024-element relative-trace/Reynolds projector onto the rank-16 R8 subring;
- its unique automorphism support has 1024 nonzero labels;
- a \(t\)-automorphism linear circuit can expose at most \(2^t\) labels;
- therefore \(t\ge10\);
- current RM10 uses exactly 10.

Do not search for a 9-call exact RM10 inside the same standard linear automorphism-multiplier model.

### Joint recovery optimality

The exact four-output joint map requires five automorphism terms, including identity.

Therefore four nonidentity calls are support-minimal inside the established R8 automorphism-multiplier interface.

## Equal-keyset comparator interpretation

The Turn-4 benchmark intentionally gives thin, Corr./TnM, and candidate the same BSGS+10 keyset.

HElib recomputes the global BFS \`keySwitchMap\`, so comparators are:

> source-faithful algorithms under an augmented equal-resource BSGS+10 key budget,

not operationally identical stock-keyset executions.

This is intentional and conservative.

Turn 20 bounded comparator strengthening:
- thin transform physical KS: \(21\to20\);
- Corr./TnM five branch transform count: \(105\to100\);
- Corr./TnM CoeffToSlots/recovery count: \(100\to95\);
- possible extra Method-1 strengthening is 0 or 5 per k=5 map only if the unpublished RMFE \(s=16\);
- source-implied likely p=5,w=512 choice is \(s=1\), but \(s\) is not explicitly published.

A candidate Strong PASS under this equal-resource configuration is a robust algorithmic win.

A negative prior result should be labelled:

\`NO_EQUAL_RESOURCE_PRIOR_GAIN\`

rather than a literal claim about Aung's original stock-keyset execution.

## Throughput decision contract

Aung-compatible workflow statistic:

\[
\Theta_w
=
S_w\frac{\bar C_w}{\bar T_w}.
\]

Slots:
- candidate \(S_c=10\);
- prior Corr./TnM \(S_p=10\);
- thin \(S_t=2\).

Primary ratios:

\[
R_{\rm prior}
=
\frac{\bar C_c\bar T_p}
     {\bar C_p\bar T_c},
\]

\[
R_{\rm thin}
=
5\frac{\bar C_c\bar T_t}
       {\bar C_t\bar T_c}.
\]

Point-estimate frontier:

\[
\bar T_c
<
\bar C_c
\min
\left(
\frac{\bar T_p}{\bar C_p},
5\frac{\bar T_t}{\bar C_t}
\right).
\]

Strong scientific PASS still requires:

\[
CI^{lower}_{95}(R_{\rm prior})>1
\]

and

\[
CI^{lower}_{95}(R_{\rm thin})>1.
\]

Bootstrap contract:
- resample joint \((C_i,T_i)\) observations;
- pair workflows only if actual matched trial blocks exist;
- otherwise bootstrap workflows independently;
- \(B=100000\);
- deterministic seed \`20261101\`;
- percentile 95% CI primary;
- BCa sensitivity if well-defined;
- percentile/BCa threshold disagreement => UNCLEAR;
- missing raw arrays => no scientific CI PASS.

Fixed-keyset CI is conditional on the measured keyset, not fresh-KeyGen averaged.

## Capacity metadata contract

Turn 23 established fused reconstruction capacity bookkeeping is legitimate.

For the reconstruction:

\[
\nu_{\rm fused}
=
\nu_E\|B\|_{\rm emb}
+
|f|\|A\|_{\rm emb}
\le
\nu_{\rm separate}.
\]

Current aggregate coefficients satisfy:
- branch post-divisibility coefficient magnitude \(\le626\);
- aggregate \(A,B\) coefficient magnitude \(\le3130\);
- \(<12\) coefficient bits;
- HElib's >400-bit scaled-FFT norm branch is unreachable.

Artifact acceptance requires:
- real \`recryptEkey\`;
- canonical \(A,B\bmod(X^{16384}+1)\);
- ZZX overloads or explicit actual \`embeddingLargestCoeff\` size;
- custom RM10/joint DCRT multipliers carry explicit actual sizes;
- no manual noiseBound/capacity reset/forging.

If custom DCRT multipliers use implicit default size, classify:

\`FAIL_CAPACITY_METADATA_CONTRACT\`.

## Remaining-depth boundary

Final HElib capacity does not determine Aung "Remaining Mults".

Reason:
- first post-bootstrap square already relinearizes;
- KeySwitch added-noise bookkeeping depends on actual \`breakIntoDigits(part)\`;
- final capacity/noiseBound is not a sufficient Markov state;
- Aung measures actual repeated squaring until actual decryption failure.

If the systems gate survives, remaining depth requires a separate Aung-matched ten-run repeated-squaring test.

Do not infer discrete remaining multiplications from final capacity.

## Security claim boundary

The ten added RM10 automorphism hints:
- encode linear/affine functions \(\sigma_u(s)=A_us\);
- do not enlarge the broad affine-KDM function class;
- add ten concrete matrices / \(10D\) rows;
- remain in the same polynomial-query regime;
- do not add a new key-dependency cycle.

Safe posture:

> same HElib/Aung evaluation-key / circular-KDM posture, with ten additional standard same-key automorphism hints.

Do not claim:
- a formal ACPS09-to-HElib reduction;
- unchanged standard-RLWE security;
- exactly zero concrete-security effect;
- a 5.56% security-bit loss.

The +5.555556% figure is row/payload growth, not a security loss percentage.

## Publication-claim boundary

A Strong Turn-4/16 PASS establishes:

> statistically higher Aung-style capacity-times-packing throughput under the same-machine equal-resource configuration.

Preferred language:

> crosses the Aung throughput frontier.

It does NOT by itself establish:
- lower latency than thin;
- higher capacity than thin;
- higher remaining multiplicative depth;
- smaller evaluation key;
- lower RSS;
- strict all-axis Pareto dominance.

Likely interpretation after Strong PASS:
- a new non-dominated tradeoff point,
- with bounded extra evaluation-key cost,
- conditional on practical remaining depth.

High-level "direct RMFE-packed MultKey / one linear phase" novelty remains killed by Aung's own future-work statement and prior-art context.

Joint rank-5 recovery is not standalone novelty; it is a natural specialization/corollary of Aung Proposition 3.

Potential mechanism-specific contribution remains:
- branch-local raw-rounding obstruction;
- earliest exact post-raw fusion;
- explicit public carry compensation;
- one common reconstruction;
- restricted recovery;
- measured frontier movement.

## Native-result audit — must preempt successor research

When the pending result becomes available, audit before accepting any scientific PASS.

### Provenance / binary

Verify:
- upstream HElib base
  \`acdb264e1a991eaee35fd8b3c31bebe9528c49a1\`;
- candidate patch commit/diff;
- exact changed files/functions;
- same patched tree/binary for all three workflows;
- no fresh recryptEkey surrogate;
- no secret-key evaluator operation;
- no dummy one-part reconstruction;
- stock rawModSwitch semantics unchanged.

### Shared keyset

Verify:
- standard BSGS Frobenius matrices generated;
- exact ten RM10 direct matrices added;
- global \`keySwitchMap\` recomputed;
- all workflows use the same resulting key object / byte-identical serialized key material.

Ten RM10 target automorphisms:

\[
16385,8193,4097,2049,1025,513,257,129,65,33.
\]

Expected:
- candidate RM10: ten one-hop calls;
- candidate joint recovery: four direct \(j=1\) calls;
- Corr./TnM recovery: 95 physical KS under BSGS+10.

### Candidate semantic assertions

Verify all Turn-25 implementation assertions:
1. stock SlotsToCtxts branch semantics;
2. source-identical thin SlotsToCoeff;
3. branch \`inCanonicalForm(recryptKeyID)\`;
4. exactly two raw channels;
5. branchwise rawModSwitch unchanged;
6. typed carry channel 0 / channel 1;
7. \(Y^i\) implemented as public monomial multiplication, never automorphism;
8. canonical \(A,B\bmod(X^{16384}+1)\);
9. actual shared \`recryptEkey\`;
10. \`ptxtSpace==625\`;
11. exact RM10 targets + one \(\times224\);
12. established rank-5 active-domain layout;
13. exact joint \(\theta\) maps;
14. output ordering \(L_0,L_1,L_2,L_3\);
15. multiplicative stock final intFactor restoration.

### Capacity bookkeeping

Verify:
- reconstruction uses actual ZZX/explicit norm sizes;
- all custom RM10/joint DCRT constants use explicit actual \`embeddingLargestCoeff\`;
- no manual favorable metadata reset.

### Measurement

Verify:
- 5 warmups + 20 measured invocations/workflow;
- single-thread;
- CPU/process affinity policy;
- fresh valid ciphertexts;
- no retry/rescue;
- per-invocation correctness;
- raw \(C_i,T_i\) arrays;
- exact workflow execution order;
- trial matching / input-copy relationship;
- keyset hash/ID;
- stage timings;
- physical KS counts/hops;
- serialized key bytes;
- RSS if recorded.

### Statistics

Use Turn-16 estimator:
- throughput from ratio of means;
- joint C/T bootstrap;
- paired only for true matched trials;
- fixed-keyset inference only;
- seed 20261101;
- B=100000;
- percentile + BCa sensitivity.

### Interpretation

Do not infer:
- DFR proof from 20 zero failures;
- remaining multiplications from capacity;
- strict Pareto dominance from throughput;
- new security theorem from the added keys.

## Successor-session control

If the pending native result is ready:
- first substantive successor turn = independent audit of
  \`BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01\`.

If it is still pending:
- resume independent BOOT research in a new session-local turn budget;
- do not rerun or replace the occupied native task;
- retain TRACK_ID / ACTIVE_SUBLINE;
- continue one-hypothesis / cheapest-decisive-test discipline.

No additional substantive research was performed in Turn 26.
