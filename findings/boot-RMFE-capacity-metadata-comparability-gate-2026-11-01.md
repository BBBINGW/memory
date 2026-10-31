# BOOT RMFE HElib Capacity-Metadata Comparability Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 23/25
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

\`BBBINGW/memory main@caf05547193ca09d2760ea6de4d4c04d0e4d3571\`.

Relevant durable prerequisites:
- Turn 14 source-faithful reconstruction uses the real \`recryptEkey\` and ordinary HElib APIs;
- exact handle gate: fused reconstruction \(\operatorname{Rec}(A,B)\) is CtxtPart-identical to the shifted sum of five stock reconstructions;
- Turn 4/16 use final HElib capacity in the primary throughput metric;
- current candidate recovery uses RM10 plus joint rank-5 Frobenius recovery.

## Primary hypothesis

The candidate's final HElib \`capacity()\` could be spuriously optimistic because aggregate reconstruction with large public integer polynomials \(A,B\) may bypass or understate HElib's noise metadata updates.

Falsifier:
find any candidate-specific reconstruction operation where:
- the actual integer multiplier/addend norm is not included in \`noiseBound\`;
- a default-size heuristic is used instead of the actual \(A,B\) norm;
- coefficient growth reaches the approximate >400-bit norm-scaling branch;
- manual metadata forging/reset is required.

## Pinned source

HElib:

\`homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1\`.

Relevant source:
- \`src/Ctxt.cpp:895-945\`: BGV \`addConstant(DoubleCRT/ZZX)\`;
- \`src/Ctxt.cpp:1830-1882\`: BGV \`multByConstant(DoubleCRT/ZZX)\`;
- \`src/norms.cpp:119-260,443-485\`: \`embeddingLargestCoeff\`;
- \`src/Ctxt.cpp:2949-3048\`: \`rawModSwitch\`;
- \`src/recryption.cpp:69-136\`: \`newMakeDivisible\`;
- \`src/recryption.cpp:1094-1099\`: stock thin reconstruction;
- \`src/powerful.cpp:246-360\`: single-factor powerful-basis identity;
- \`src/matmul.cpp:317-363\`: stock MatMul constant-size bookkeeping.

## 1. Stock thin reconstruction and candidate use the same ZZX overloads

Stock thin recryption reconstructs exactly:

\[
\texttt{ctxt = recryptEkey;}
\]
\[
\texttt{ctxt.multByConstant(zzParts[1]);}
\]
\[
\texttt{ctxt.addConstant(zzParts[0]);}
\]

with \`zzParts[i]\` of type \`NTL::ZZX\`.

Turn 14's source-faithful candidate does the same:

\[
\texttt{ctxt = recryptEkey;}
\]
\[
\texttt{ctxt.multByConstant(B);}
\]
\[
\texttt{ctxt.addConstant(A);}
\]

where \(A,B\) are also \`NTL::ZZX\`.

Therefore reconstruction does **not** fall through the \`DoubleCRT\` default-size heuristic.

## 2. ZZX multiplication computes the actual embedding norm

For BGV:

\[
\texttt{multByConstant(ZZX poly, size=-1)}
\]

first computes

\[
s_B=\texttt{embeddingLargestCoeff(poly)}
\]

and then calls the DCRT overload with this explicit size.

The DCRT overload performs:

\[
\boxed{
\nu \leftarrow \nu\,s_B.
}
\]

Thus for \(B\):

\[
\nu_{E\cdot B}
=
\nu_E\|B\|_{\rm emb,\infty}
\]

up to the numerical norm routine used by HElib itself.

No fixed plaintext-space default is used.

## 3. ZZX constant addition also computes the actual embedding norm

For:

\[
\texttt{addConstant(ZZX A, size=-1)}
\]

HElib first computes

\[
s_A=\texttt{embeddingLargestCoeff(A)}.
\]

The DCRT overload computes the current BGV injection scale

\[
f=
\operatorname{balRem}
\left(
\texttt{intFactor}\cdot Q
\bmod \texttt{ptxtSpace}
\right)
\]

and updates:

\[
\boxed{
\nu \leftarrow \nu+s_A|f|.
}
\]

Therefore the fused reconstruction ledger is:

\[
\boxed{
\nu_{\rm fused}
=
\nu_E\|B\|_{\rm emb}
+
|f|\|A\|_{\rm emb}.
}
\]

This uses the same metadata rule as stock thin reconstruction.

## 4. Fused lower noiseBound is mathematically legitimate

For branch states:

\[
a_i=D(z_{i,0}),
\qquad
b_i=D(z_{i,1}),
\]

and envelope monomial \(Y=X^{1024}\):

\[
A=\sum_{i=0}^4Y^ia_i,
\qquad
B=\sum_{i=0}^4Y^ib_i.
\]

Multiplication by a ring monomial \(Y^i\) has canonical-embedding norm one, because each embedding evaluates \(Y^i\) to a root of unity.

Hence:

\[
\|Y^ia_i\|_{\rm emb}=\|a_i\|_{\rm emb},
\qquad
\|Y^ib_i\|_{\rm emb}=\|b_i\|_{\rm emb}.
\]

By triangle inequality:

\[
\|A\|_{\rm emb}
\le
\sum_i\|a_i\|_{\rm emb},
\]

\[
\|B\|_{\rm emb}
\le
\sum_i\|b_i\|_{\rm emb}.
\]

Five separate stock reconstructions followed by public shifts and summation would have ledger upper bound:

\[
\nu_{\rm sep}
=
\sum_i
\left(
\nu_E\|b_i\|_{\rm emb}
+
|f|\|a_i\|_{\rm emb}
\right).
\]

Therefore:

\[
\boxed{
\nu_{\rm fused}\le\nu_{\rm sep}.
}
\]

So a fused-capacity improvement at the reconstruction boundary is not an artificial metadata reset.

It is exactly what the same HElib norm ledger plus triangle inequality permits.

## 5. Current integer ranges are tiny

For \(p=5,e=4\):

\[
q=p^e+1=626.
\]

Pinned \`rawModSwitch\` explicitly reduces every powerful-basis output coefficient symmetrically modulo \(q\), so:

\[
|x|\le313.
\]

\`newMakeDivisible\` replaces:

\[
x\mapsto x+vq,
\]

with:

\[
|v|\le p^{e'}/2.
\]

After division by \(p^{e'}\):

\[
\left|
\frac{x+vq}{p^{e'}}
\right|
\le
\frac{313}{p^{e'}}+313
\le626.
\]

Thus every post-divisibility branch channel has powerful-basis coefficient magnitude at most 626.

## 6. Powerful basis is exactly the polynomial basis here

Pinned \`PowerfulDCRT\` sets:

\[
\texttt{triv}=(\texttt{mvec.length()==1})
\]

and comments:

> poly and pwfl bases are identical.

Current thin bootstrapping uses the one-factor geometry:

\[
mvec=[32768].
\]

Therefore:

\[
\boxed{
\text{powerful coefficient bound}
=
\text{ZZX coefficient bound}.
}
\]

No hidden basis-conversion blowup occurs.

## 7. Aggregate A,B stay below 12 coefficient bits

Modulo:

\[
\Phi_{32768}(X)=X^{16384}+1,
\]

multiplication by:

\[
Y^i=X^{1024i}
\]

is only a coefficient permutation/sign change after canonical ring reduction.

Five branches therefore give:

\[
|A_j|,|B_j|
\le
5\cdot626
=
3130.
\]

Hence:

\[
\boxed{
\operatorname{MaxBits}(A),\operatorname{MaxBits}(B)<12.
}
\]

Even the crude canonical norm bound:

\[
\|A\|_{\rm emb},\|B\|_{\rm emb}
\le
\phi(m)\cdot3130
<
2^{26}
\]

is tiny.

## 8. The >400-bit norm-scaling path is impossible here

For a \`ZZX\` with coefficient bit-length above 400, HElib's \`embeddingLargestCoeff\` right-shifts coefficients before FFT and rescales afterward.

That approximate scaling path is a potential generic source of tiny truncation error.

But current \(A,B\) are below 12 coefficient bits.

Therefore:

\[
\boxed{
\text{the >400-bit scaling/truncation branch is unreachable for current reconstruction}.
}
\]

The current norm computation uses ordinary double FFT values on exactly representable small integer coefficients.

Floating-point FFT roundoff remains part of HElib's global metric, but there is no candidate-specific large-integer precision hazard.

## 9. Canonical representative requirement

\`embeddingLargestCoeff\` assumes a polynomial representative with degree below \(\phi(m)\).

A naive implementation of:

\[
Y^ia_i=X^{1024i}a_i
\]

that simply shifts polynomial coefficients without reducing modulo:

\[
X^{16384}+1
\]

can produce degree above 16383.

This is not a silent capacity-underestimate path:
the half/quarter FFT norm implementation checks the input length and throws if it exceeds \(m/2=\phi(m)\).

Still, a source-faithful implementation must maintain the canonical ring representative:

\[
\boxed{
A,B\gets A,B\bmod(X^{16384}+1)
}
\]

before reconstruction/norm computation.

Failure to do so is an execution bug.

## 10. Downstream RM10/joint multipliers need the same explicit-size discipline

The reconstruction boundary is safe.

However candidate-specific recovery also performs public ct-pt multiplications.

HElib has two materially different APIs:

### Safe

\[
\texttt{multByConstant(ZZX poly)}
\]

which computes the actual \`embeddingLargestCoeff(poly)\`.

Also safe:

\[
\texttt{multByConstant(DoubleCRT dcrt, explicitSize)}
\]

with:

\[
\texttt{explicitSize}
=
\texttt{embeddingLargestCoeff(original balanced polynomial)}.
\]

### Not sufficient for scientific capacity comparison

\[
\texttt{multByConstant(DoubleCRT dcrt)}
\]

with no explicit size.

That overload uses:

\[
\texttt{context.noiseBoundForMod(ptxtSpace,...)}
\]

a default distributional/plaintext-space estimate, not the actual norm of the custom multiplier.

For arbitrary RM10 or joint-\(\theta\) constants this can differ from the source-specific multiplier norm.

## 11. Stock HElib MatMul already preserves explicit multiplier sizes

Pinned \`matmul.cpp\` stores plaintext multipliers first as balanced polynomial constants.

When upgraded to \`DoubleCRT\`, it explicitly computes:

\[
\texttt{sz = embeddingLargestCoeff(data)}
\]

and stores:

\[
(\texttt{DoubleCRT(data)},\texttt{sz}).
\]

The multiplication then calls:

\[
\texttt{ctxt.multByConstant(data, sz)}.
\]

Thus stock comparator linear maps do not lose their actual constant-size metadata merely because they use cached DCRT multipliers.

Candidate RM10/joint code should follow the same pattern.

## 12. Consequence for the pending native artifact

Final candidate capacity is scientifically comparable **if and only if**:

1. reconstruction uses the real \`recryptEkey\`;
2. \(A,B\) use the \`ZZX\` overloads or explicit actual embedding sizes;
3. \(A,B\) are reduced to canonical degree \(<16384\);
4. every custom RM10/joint DCRT multiplier carries an explicit size computed from its balanced polynomial representative;
5. no manual \`noiseBound\`, \`capacity\`, \`bumpNoiseBound\`, or metadata reset is used to improve the candidate;
6. all workflows use the same HElib capacity definition.

If custom recovery instead uses DCRT constants with implicit default sizes, correctness may still pass but the capacity-based throughput verdict is not scientifically clean.

Use:

\[
\boxed{\texttt{FAIL_CAPACITY_METADATA_CONTRACT}}
\]

for that artifact condition.

## 13. What this turn does and does not prove

Established:

\[
\boxed{
\text{aggregate reconstruction does not create a false HElib-capacity gain}.
}
\]

Established:

\[
\boxed{
\nu_{\rm fused}\le\nu_{\rm sep}
}
\]

under the same HElib reconstruction ledger.

Established:
current \(A,B\) integer range does not trigger large-integer norm approximation.

Not established:
- actual decryption error is bounded pointwise by the ledger;
- DFR;
- remaining multiplications;
- final native capacity value;
- correctness/performance of the pending binary.

## Verdict

\`\`\`text
RESULT:
  PASS_RECONSTRUCTION_CAPACITY_METADATA_COMPARABILITY
  CONDITIONAL_PASS_WHOLE_CANDIDATE_CAPACITY_COMPARABILITY

STOCK_RECONSTRUCTION_API:
  ZZX multByConstant + ZZX addConstant

CANDIDATE_RECONSTRUCTION_API:
  SAME REQUIRED

MULTIPLIER_SIZE_B:
  actual embeddingLargestCoeff(B)

ADDEND_SIZE_A:
  actual embeddingLargestCoeff(A)

FUSED_RECONSTRUCTION_LEDGER:
  nu_E*||B|| + |f|*||A||

SEPARATE_RECONSTRUCTION_LEDGER:
  sum_i [nu_E*||b_i|| + |f|*||a_i||]

FUSED_VS_SEPARATE:
  nu_fused <= nu_separate

RAWMODSWITCH_POWERFUL_COEFF:
  |x| <= 313

POST_DIVISIBILITY_BRANCH_COEFF:
  <= 626

POWERFUL_TO_POLY_BASIS:
  IDENTICAL / mvec.length()==1

AGGREGATE_A_B_COEFF:
  <= 3130

A_B_MAXBITS:
  < 12

EMBEDDING_NORM_400BIT_SCALING_BRANCH:
  UNREACHABLE

CANONICAL_POLY_DEGREE:
  MUST BE < 16384

CUSTOM RM10/JOINT DCRT MULTIPLIERS:
  EXPLICIT embeddingLargestCoeff SIZE REQUIRED

DCRT DEFAULT-SIZE ONLY:
  FAIL_CAPACITY_METADATA_CONTRACT

MANUAL NOISEBOUND RESET/FORGE:
  FORBIDDEN

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  RETAIN PENDING SYSTEMS VALUE

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

The main capacity-fairness risk is not the fused reconstruction.

HElib's stock and fused reconstruction paths use the same actual-polynomial norm bookkeeping, and the fused lower ledger follows from a real triangle-inequality improvement rather than metadata manipulation.

The remaining artifact-level risk is implementation discipline for the custom RM10/joint plaintext multipliers. Their DCRT caches must preserve explicit embedding norms exactly as stock HElib MatMul does.
