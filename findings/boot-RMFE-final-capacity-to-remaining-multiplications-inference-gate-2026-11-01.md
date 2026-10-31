# BOOT RMFE Final-Capacity to Remaining-Multiplications Inference Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 22/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Pending native task boundary

Authorized native task:

\`BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01\`

remains UNKNOWN / BACKGROUND.

This turn does not:
- inspect or assume its result;
- modify its source/workdir/binary;
- resubmit it;
- start another heavy native task.

## Read-before-write authority

Current durable authority at turn start:

\`BBBINGW/memory main@035010c9d1bda79335ed7210dd8e01f433520993\`.

Relevant durable prerequisites:
- Turn 18: Aung throughput does not subsume remaining multiplicative depth;
- Turn 8: scalar HElib \`noiseBound\` is not a closed state for future key-switch noise because \`breakIntoDigits\` depends on the actual ciphertext part;
- current Turn-4 pending task records final capacity but not Aung-style repeated-squaring depth.

## Primary hypothesis

The final HElib capacity already recorded by the pending throughput task may be sufficient to infer, without another native experiment, the number of Aung-style remaining multiplications (repeated squarings before decryption failure).

Falsifier:
show that two post-bootstrap ciphertext states can share the same scalar capacity/noise metadata while producing different noise evolution after squaring/relinearization, or that Aung's metric depends on actual decryption behavior not encoded by HElib capacity.

## 1. Aung's "Remaining Mults" is an empirical decryption-failure metric

Aung et al. ePrint 2025/350 physical pp23--24 states that, for each bootstrapping workflow, they:
- repeatedly square the bootstrapped ciphertext;
- perform recoding where required;
- continue until decryption fails;
- report the minimum number of successful rounds across ten runs.

Therefore their reported metric is not:

\[
\left\lfloor
\frac{\text{final capacity}}{\text{bits per multiplication}}
\right\rfloor.
\]

It is an empirical repeated-execution/decryption metric.

## 2. HElib capacity is only one scalar metadata ratio

Pinned HElib:

\`homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1\`.

For BGV:

\[
\texttt{totalNoiseBound()}=\texttt{noiseBound}.
\]

HElib defines

\[
\boxed{
\texttt{capacity}
=
\log_2\!\left(
\frac{Q}{\max(\texttt{noiseBound},1)}
\right)
}
\]

where \(Q\) is the product of the current ciphertext primes.

Thus final capacity discards:
- the actual ciphertext polynomial parts;
- their digit decompositions;
- actual decryption-error direction;
- individual evaluation-key error coordinates;
- the exact prime-set identity except through its product;
- any correlation information.

It is a scalar summary, not a complete future-noise state.

## 3. The first square already needs more state than capacity

HElib \`Ctxt::square()\` calls:

\[
\texttt{multiplyBy(*this)}.
\]

For a square:
1. \`multLowLvl\` first chooses \`naturalPrimeSet()\`;
2. the tensor product sets, for BGV,
   \[
   \texttt{noiseBound}_{\rm tensor}
   =
   \texttt{noiseBound}^2;
   \]
3. \`multiplyBy\` then calls
   \[
   \texttt{reLinearize()}.
   \]

The critical step is relinearization.

Pinned \`Ctxt::keySwitchPart\` computes:

\[
\boxed{
\texttt{addedNoise}
=
\texttt{breakIntoDigits(actual\ part)}
\times
W.\texttt{noiseBound}.
}
\]

The first factor is computed from the actual ciphertext part, not from the scalar \`noiseBound\` or \`capacity()\`.

Hence the post-square ledger recurrence is not of the form

\[
C_{t+1}=F(C_t)
\]

for a scalar function \(F\).

## 4. Turn 8 already killed scalar-noiseBound closure

The durable scalar-noiseBound DFR gate established that two valid ciphertext states with the same scalar HElib noise state need not have the same \`breakIntoDigits\` norm.

That result is directly relevant here.

Even if two post-bootstrap ciphertexts have:
- the same context;
- the same plaintext space;
- the same key ID;
- the same scalar \`noiseBound\`;
- the same final capacity,

their next key-switch noise increment can differ because the actual ciphertext parts decompose differently.

Therefore:

\[
\boxed{
\text{final capacity is not a Markov state for repeated squaring}.
}
\]

## 5. naturalPrimeSet does not rescue scalar closure

Before squaring, HElib computes a target modulus interval using:

\[
\log Q-\log(\texttt{noiseBound})
\]

and the modulus-switch added-noise bound.

This part is largely capacity-like.

But after the tensor product, relinearization reads the actual ciphertext digits and injects path-dependent key-switch noise.

So even if the first mod-down decision were identical for two equal-capacity states, the states can diverge immediately during the same square.

The missing information is not merely the selected modulus level.

## 6. HElib isCorrect is still not Aung's actual metric

HElib provides:

\[
\texttt{Ctxt::isCorrect()}
\]

which checks the conservative metadata condition

\[
\texttt{totalNoiseBound}\cdot B_{\rm norm}
\le
0.48Q.
\]

This is a sufficient ledger-style correctness test based on a bound.

Aung's experiment instead actually decrypts after repeated squaring until decryption fails.

Actual decryption depends on the realized error polynomial, while \`noiseBound\` is a bound/estimate.

Therefore even a hypothetical deterministic recurrence for HElib \`isCorrect()\` would not automatically reproduce Aung's "Remaining Mults".

## 7. Actual error carries still more hidden state

For one key-switch matrix, the actual switched error contains

\[
p\sum_j d_j e_j,
\]

where:
- \(d_j\) are the actual decomposition digits of the current ciphertext part;
- \(e_j\) are the fixed sampled evaluation-key error polynomials.

Neither the vector \(d_j\) nor the realized error direction is encoded by final capacity.

Repeated squaring then multiplies and propagates the realized plaintext/error state.

Thus same or similar capacity can coexist with different actual failure margins.

## 8. What final capacity can still be used for

Capacity remains highly useful as:
- Aung's throughput numerator;
- a coarse headroom indicator;
- a comparison metric under the same implementation;
- an input to HElib's own modulus-management heuristics.

It can support statements such as:

> candidate has more/less HElib capacity than comparator.

It cannot support:

> candidate has exactly \(M\) remaining multiplications.

Nor, without an additional proved worst-case recurrence, can it support:

> capacity \(C\) guarantees at least \(M\) Aung-style successful squarings.

No such tight recurrence has been established.

## 9. Published p=5 rows illustrate correlation, not a conversion rule

Aung p=5 reports approximately:

- thin:
  \[
  C=151,\quad M=8;
  \]
- Corr./TnM:
  \[
  C=101,\quad M=5;
  \]
- Corr./BSGS:
  \[
  C=115,\quad M=6;
  \]
- Naive/BSGS:
  \[
  C=58,\quad M=2.
  \]

These values are monotonically suggestive in that table.

But four empirical points do not define a source-valid conversion \(M=f(C)\).

The source mechanics above show why such a universal scalar conversion is not justified.

## 10. Consequence for the pending native artifact

If the pending task Strong-PASSES the throughput gate, its final capacity is not enough to close Turn 18's practical-depth axis.

The safe result remains:

> higher Aung capacity-times-packing throughput under the measured equal-resource configuration.

Do not add:

> and therefore at least as many remaining multiplications.

unless an actual repeated-squaring test is supplied.

## 11. Minimal follow-up if systems value Strong-PASSES

The correct follow-up is very small compared with the current paired benchmark:

For each workflow of interest:
1. obtain a fresh correctly bootstrapped ciphertext;
2. copy it;
3. repeatedly call the same squaring path used by Aung;
4. perform any required recoding exactly as in the source workflow;
5. decrypt/check the expected plaintext after every round;
6. stop at first failure;
7. repeat ten independent runs;
8. report the minimum successful round count, matching Aung's methodology.

For the candidate, the primary question is whether it retains a practically useful depth, not whether capacity predicts it.

This follow-up should only be authorized if the current systems task Strong-PASSES or otherwise leaves publication value alive.

No such task is started in this turn.

## Verdict

\`\`\`text
RESULT:
  FAIL_FINAL_CAPACITY_DETERMINES_REMAINING_MULTIPLICATIONS
  PASS_REMAINING_DEPTH_REQUIRES_SEPARATE_EMPIRICAL_GATE

AUNG_REMAINING_MULTS:
  REPEATED SQUARING UNTIL ACTUAL DECRYPTION FAILURE
  MINIMUM OVER 10 RUNS

HELIB_CAPACITY:
  log2(Q / noiseBound) FOR BGV
  SCALAR METADATA ONLY

FIRST_SQUARE_TENSOR_NOISE:
  noiseBound^2

FIRST_SQUARE_RELINEARIZATION:
  DEPENDS ON actual breakIntoDigits(part)

SCALAR_CAPACITY_MARKOV_CLOSURE:
  FALSE

HELIB_isCorrect:
  CONSERVATIVE BOUND CHECK
  NOT AUNG ACTUAL-DECRYPTION METRIC

EXACT M = f(C):
  NOT JUSTIFIED

NONTRIVIAL GUARANTEED M FROM C ALONE:
  NOT ESTABLISHED

PENDING_TASK_FINAL_CAPACITY:
  USEFUL FOR THROUGHPUT
  INSUFFICIENT FOR DEPTH CLAIM

FOLLOW_UP_IF_STRONG_PASS:
  AUNG-MATCHED 10-RUN REPEATED-SQUARING DEPTH TEST

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  RETAIN PENDING SYSTEMS VALUE

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

Final HElib capacity is not a sufficient state variable for future multiplicative depth.

The source-level obstruction appears immediately at the first post-bootstrap relinearization, whose key-switch noise depends on the actual ciphertext digit decomposition.

Therefore Turn 18's remaining-depth axis cannot be closed by post-processing the pending capacity numbers. A separate, cheap Aung-matched depth test is required only if the systems result survives.
