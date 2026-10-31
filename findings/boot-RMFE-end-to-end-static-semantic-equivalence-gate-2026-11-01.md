# BOOT RMFE End-to-End Static Semantic-Equivalence Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 25/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Pending native task boundary

Authorized native task:

\`BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01\`

remains UNKNOWN / BACKGROUND at the start and end of this substantive turn.

This turn does not:
- inspect or assume its result;
- modify its source/workdir/binary;
- resubmit it;
- start another heavy native task.

## Read-before-write authority

Current durable authority at turn start:

\`BBBINGW/memory main@3b3ae165d875dd62f398715a63c7bfc21a1390a0\`.

This turn composes, but does not weaken, the already-established static gates:
- branchwise rawModSwitch is the earliest exact aggregate-only fusion boundary;
- post-raw divisibility-lift nonlinearity has an exact public carry correction;
- both raw channels share the same recryption-key handle basis;
- one common \`recryptEkey\` reconstruction is exact at CtxtPart level;
- RM10 is the normalized projector onto the embedded R8 subring;
- joint rank-5 recovery exactly synthesizes C2S plus the four correction outputs on the actual active post-RM10 domain;
- RM10 unit normalization and downstream \`intFactor\` semantics are valid;
- Aung Algorithm 4 is correct on RMFE inputs with \(\eta\ge p^{e-1}\).

## Primary hypothesis

All surviving static identities compose into one source-faithful theorem:

> for the current p=5,w=512,k=5 correction-style instance, the carry-compensated post-raw fused candidate produces exactly the same four plaintext semantic inputs required by Aung correction DigitExtract as the five-branch stock Algorithm-2 path, provided all homomorphic operations remain within their correctness/noise regime.

Falsifier:
any interface mismatch among:
- branch raw representative semantics;
- two-channel carry typing;
- recryption-key handle basis;
- R8 envelope placement;
- RM10 normalization;
- joint-map restricted domain;
- plaintext space / intFactor;
- correction-map ordering.

## 1. Source target semantics

Aung Algorithm 2 takes one RMFE-packed ciphertext \(c\), splits it into \(k\) thin ciphertexts, performs the MultKey block on each branch, recombines them, and then invokes RMFE DigitExtract.

For p=5 correction style:

\[
e=4,\qquad
\eta=p^{e-1}=125,\qquad
k=5.
\]

Aung Algorithm 4 requires, for one RMFE-packed value \(z\in\operatorname{im}\phi\), the four correction inputs:

\[
L_0(z)=z,\qquad
L_1(z),\qquad
L_2(z),\qquad
L_3(z).
\]

Aung §5.1 explicitly says \`CtxtsToSlots\` can compute these linear maps by constant-multiplying each split branch by precomputed images of the RMFE basis and summing.

Thus the candidate's exact semantic target is not merely reconstruction of \(z\); it is the ordered four-tuple

\[
\boxed{
(z,L_1(z),L_2(z),L_3(z)).
}
\]

## 2. Branch-local prefix is exactly preserved

Let Aung \`SlotsToCtxts\` produce five thin branches

\[
c_0,\ldots,c_4.
\]

For each branch, the candidate preserves the same source prefix through:

\[
\text{thin SlotsToCoeff}
\to
\texttt{reLinearize(recryptKeyID)}
\to
\texttt{rawModSwitch}.
\]

After relinearization, every branch is in the same two-handle basis:

\[
(1,s_R),
\]

where \(s_R\) is the recryption secret.

Write the raw integer-polynomial pair for branch \(i\) as:

\[
(z_{i,0},z_{i,1}).
\]

Its exact secret linear form is:

\[
z_{i,0}+s_R z_{i,1}.
\]

No branch-specific \(\sigma(s_R)\) handle remains.

## 3. Post-raw divisibility fusion is exactly branch-equivalent

Let

\[
P=p^{e'}
\]

and

\[
q=p^e+1.
\]

For odd \(p=5\), HElib \`newMakeDivisible\` followed by division is exactly the coefficientwise map

\[
D(z)
=
\frac{z-q\rho_P(z)}{P},
\]

with unique centered residue section \(\rho_P\).

For one signed aggregation row, the exact carry identity is:

\[
D\left(\sum_i a_i z_i\right)
-
\sum_i a_iD(z_i)
=
q\kappa_a,
\]

where the integer carry \(\kappa_a\) is publicly computable after branch raw outputs are known.

The current envelope uses:

\[
Y=X^{1024}
\]

and signed coefficient-permutation shifts \(Y^i\).

Apply the carry correction separately to the two raw channels.

Define the exact branchwise post-divisibility values:

\[
a_i=D(z_{i,0}),\qquad
b_i=D(z_{i,1}).
\]

The candidate's aggregate procedure is required to produce exactly:

\[
A=\sum_{i=0}^4Y^i a_i,
\qquad
B=\sum_{i=0}^4Y^i b_i.
\]

Hence, after carry correction:

\[
\boxed{
(A,B)
=
\left(
\sum_iY^iD(z_{i,0}),
\sum_iY^iD(z_{i,1})
\right).
}
\]

This is an exact integer-polynomial equality, not a probabilistic approximation.

## 4. One common boot-key reconstruction is CtxtPart-exact

Let the actual stock \`recryptEkey\` ciphertext be:

\[
E=(E_0,E_1)
\]

under the main key \(s_0\).

For any public pair \((a,b)\), stock reconstruction is:

\[
\operatorname{Rec}(a,b)
=
(bE_0+fa,\ bE_1),
\]

where \(f\) is the common BGV constant-injection scale for that state.

The candidate reconstructs:

\[
C_{\rm fus}
=
\operatorname{Rec}(A,B).
\]

By ring linearity:

\[
\begin{aligned}
\operatorname{Rec}(A,B)
&=
\operatorname{Rec}\left(
\sum_iY^ia_i,\sum_iY^ib_i
\right)
\\
&=
\sum_iY^i\operatorname{Rec}(a_i,b_i).
\end{aligned}
\]

Therefore:

\[
\boxed{
C_{\rm fus}
=
\sum_iY^i C_i^{\rm stock,preC2S}
}
\]

as an exact HElib CtxtPart/handle identity.

This is the strongest exact equality in the composed proof.

The output handle basis is exactly:

\[
(1,s_0).
\]

## 5. RM10 + 224 is the exact projector onto the envelope subring

The embedded subring is:

\[
R_8=S[Y]/(Y^{16}+1),
\qquad
S=\mathbb Z/625\mathbb Z.
\]

Turn 24 established:

\[
\mathrm{RM10}
=
\sum_{h\in H}\sigma_h
\]

for the 1024-element subgroup fixing \(Y\).

The source chain is therefore the relative trace:

\[
\operatorname{Tr}_{R/R_8}.
\]

The source trace acts as multiplication by 1024 on \(R_8\).

Since:

\[
1024^{-1}\bmod625=224,
\]

the candidate applies one unit normalization:

\[
P_H
=
224\cdot\mathrm{RM10}.
\]

Hence \(P_H\) is the exact Reynolds projector:

\[
\boxed{
P_H(x)=x
\quad
\text{for every }x\in R_8.
}
\]

Applied to the fused envelope state, it deletes components outside the embedded \(Y\)-subring while preserving the five active envelope coordinates exactly in plaintext semantics.

## 6. Exact active-domain condition is satisfied by construction

The R8 C2S interface has two E8 slots.

The candidate envelope places the five branch coordinates into the first five power-basis coordinates in each slot and pads the remaining three coordinates with zero.

Thus after normalized RM10, the slot-space image lies in:

\[
V_{\rm act}
=
\operatorname{span}_S
\{e_0,\ldots,e_4,e_8,\ldots,e_{12}\}.
\]

Let \(L\) be the exact R8 coefficient-to-slot map and:

\[
U=L^{-1}V_{\rm act}.
\]

The post-RM10 coefficient state is therefore in exactly the restricted domain:

\[
\boxed{
U
}
\]

used by the joint-recovery synthesis gate.

This closes the domain-interface condition; the joint map is not being applied to an arbitrary rank-16 ciphertext.

## 7. Joint rank-5 recovery outputs exactly the Aung correction tuple

For the selected Frobenius support:

\[
\{1,5,25,29,17\}
=
\{5^0,5^1,5^2,5^3,5^4\}
\pmod{32},
\]

the exact joint map uses coefficients \(\theta_{t,j}\) satisfying:

\[
(D_t\circ\mathrm{C2S})(x)
=
\sum_{j=0}^4
\theta_{t,j}\sigma^j(x)
\]

for every \(x\in U\), for:

\[
t=0,1,2,3.
\]

The prior exact basis audit verified all:

\[
2\text{ slots}\times5\text{ active coordinates}\times4\text{ outputs}
=
40
\]

basis-output equations modulo 625.

These four outputs are exactly:

\[
\boxed{
z,\quad
L_1(z),\quad
L_2(z),\quad
L_3(z)
}
\]

that stock Aung \`CoeffToSlots + CtxtsToSlots\` would supply to correction DigitExtract.

Therefore the separate five branch CoeffToSlots operations and the explicit CtxtsToSlots/correction assembly are semantically replaced by one normalized RM10 plus one joint rank-5 map.

## 8. Plaintext-space and intFactor interface is valid

The joint coefficients were constructed over:

\[
S=\mathbb Z/625\mathbb Z.
\]

Therefore the required temporary interface assertion is:

\[
\boxed{
\texttt{ptxtSpace}=625
}
\]

through reconstruction, RM10, and joint recovery.

The common reconstruction starts from the stock \`recryptEkey\` temporary factor:

\[
\texttt{intFactor}=1.
\]

The unit normalization \(\times224\) changes HElib metadata to:

\[
\texttt{intFactor}=224^{-1}=399
\pmod{625}
\]

while preserving the exact BGV invariant.

All four joint outputs inherit the same factor 399.

HElib DigitExtract operations are valid for arbitrary invertible intFactor values; they update the factor and plaintext space through ordinary BGV arithmetic.

After the final application plaintext space is reached, the original input factor \(f_{\rm in}\) must be restored exactly as stock HElib does:

\[
\boxed{
\texttt{intFactor}
\leftarrow
\texttt{intFactor}\cdot f_{\rm in}
\bmod p^r.
}
\]

No extra compensation for 399 is required.

## 9. Aung Algorithm-4 correctness theorem now applies

Aung proves correction DigitExtract for RMFE inputs when:

\[
\eta\ge p^{e-1}.
\]

For the current correction instance:

\[
\eta=125=5^3,
\qquad
e=4.
\]

The candidate supplies exactly the required correction tuple:

\[
(z,L_1(z),L_2(z),L_3(z))
\]

over the correct \(625\)-ring interface.

Therefore, conditional on the homomorphic ciphertext operations remaining correct/noise-safe, Aung Algorithm 4 returns the same RMFE plaintext as stock correction-style bootstrapping.

The resulting semantic statement is:

\[
\boxed{
\operatorname{Dec}
\left(
\Pi_{\rm cand}(c)
\right)
=
\operatorname{Dec}
\left(
\Pi_{\rm Aung,Corr/TnM}(c)
\right)
=
m
}
\]

for every input in the established RMFE message domain, under the same BGV/RMFE correctness assumptions and the candidate's explicit runtime assertions.

## 10. What equality is and is not established

### Exact integer/ciphertext-part equality established up to reconstruction

The following is exact:

\[
\operatorname{Rec}(A,B)
=
\sum_iY^i\operatorname{Rec}(a_i,b_i).
\]

### Exact plaintext-linear-map equality established after reconstruction

Normalized RM10 + joint recovery computes exactly the same desired plaintext linear outputs as the stock branchwise C2S + CtxtsToSlots/correction assembly.

### Exact ciphertext transcript equality is NOT established

The candidate and stock use different:
- automorphism sequences;
- physical KeySwitch paths;
- evaluation-key error polynomials;
- modulus-management timing;
- addition/multiplier schedule.

Therefore actual ciphertext parts after the differing linear maps need not be equal.

Likewise:

\[
\boxed{
\text{semantic equivalence}
\not\Rightarrow
\text{equal noise/capacity/DFR}.
}
\]

This is why the pending native gate remains scientifically necessary.

## 11. Complete implementation assertions

A candidate execution is inside the static theorem only if all hold:

1. Aung SlotsToCtxts branch semantics are preserved;
2. each branch uses the source-identical thin SlotsToCoeff;
3. every branch is canonicalized to the same \`recryptKeyID\`;
4. each branch has exactly two rawModSwitch channels;
5. rawModSwitch remains branchwise and source-identical;
6. carry/divisibility correction is computed separately for channel 0 and channel 1;
7. every \(Y^i\) is public ring-monomial multiplication, not a Galois automorphism;
8. \(A,B\) are canonical representatives modulo \(X^{16384}+1\);
9. the actual shared \`recryptEkey\` is used exactly once;
10. \`ptxtSpace==625\` at the joint-map interface;
11. RM10 uses the exact ten targets and normalization 224 exactly once;
12. post-RM10 state is interpreted under the established rank-5 active-domain layout;
13. joint outputs use the exact four \(\theta\)-maps;
14. outputs are passed into the source correction DigitExtract in the order
    \[
    L_0,L_1,L_2,L_3;
    \]
15. the original input intFactor is restored multiplicatively, not overwritten.

Violation of any item invalidates the composed static theorem.

## 12. Remaining scientific uncertainties after static closure

This turn closes the static semantic composition.

It does **not** establish:

- end-to-end native correctness on sampled ciphertexts;
- final capacity;
- actual key-switch error;
- DFR;
- latency;
- throughput;
- remaining multiplications;
- RSS;
- publication-level novelty.

The current decisive systems question therefore cleanly reduces to:

> Does this statically sound candidate survive the exact source-faithful native execution contract and move the same-machine Aung throughput frontier?

That is precisely the pending task.

## Verdict

\`\`\`text
RESULT:
  PASS_STATIC_END_TO_END_PLAINTEXT_SEMANTIC_EQUIVALENCE

SOURCE_TARGET:
  AUNG CORRECTION/TNM P=5 W=512 K=5

AUNG_CORRECTION_OUTPUTS:
  L0,L1,L2,L3

BRANCH PREFIX THROUGH RAWMODSWITCH:
  SOURCE-IDENTICAL

POST_RAW CARRY/DIVISIBILITY:
  EXACT BRANCH-EQUIVALENT

TWO RAW CHANNELS:
  TYPED / NO CROSS-MIX

SINGLE RECRYPTEKEY RECONSTRUCTION:
  EXACT CtxtPart EQUALITY TO SHIFTED SUM OF FIVE STOCK RECONSTRUCTIONS

RM10_PLUS_224:
  EXACT NORMALIZED PROJECTOR ONTO R8

POST_RM10 DOMAIN:
  EXACTLY THE ESTABLISHED RANK-5 ACTIVE DOMAIN

JOINT RECOVERY:
  EXACTLY PRODUCES z,L1(z),L2(z),L3(z)
  40/40 BASIS CHECKS FROM PRIOR GATE

PTXTSPACE:
  625 REQUIRED / TYPE-CLOSED

TEMPORARY INTFACTOR AFTER 224:
  399 / VALID UNIT

DOWNSTREAM DIGITEXTRACT:
  WELL-TYPED FOR UNIT INTFACTOR

FINAL INPUT INTFACTOR RESTORE:
  MULTIPLICATIVE / STOCK RULE

AUNG ALGORITHM4 PRECONDITION:
  eta=125=p^(e-1) / SATISFIED

STATIC PLAINTEXT CORRECTNESS BLOCKER:
  NONE FOUND

EXACT POST-MAP CIPHERTEXT/NOISE EQUALITY:
  NOT CLAIMED

NATIVE CORRECTNESS:
  NOT ESTABLISHED

CAPACITY / DFR / LATENCY / THROUGHPUT:
  NOT ESTABLISHED

PUBLISHABLE NOVELTY:
  CONDITIONAL / NOT ESTABLISHED

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  RETAIN PENDING SYSTEMS VALUE

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

The current candidate is no longer a collection of disconnected local identities.

Under the explicit implementation/type assertions above, the entire modified middle composes to the same RMFE correction-DigitExtract plaintext interface as stock Aung Corr./TnM.

The remaining uncertainty is operational rather than algebraic: actual HElib key-switch noise, capacity, correctness failures, and throughput.
