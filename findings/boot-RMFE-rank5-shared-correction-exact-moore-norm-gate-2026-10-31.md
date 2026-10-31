# BOOT RMFE Rank-5 Shared-Correction Exact Moore / Norm Gate

Date: 2026-10-31
Session: 密码学 16.0
Logical Research Turn: 7/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

The authorized native task
\`BOOT-RMFE-POSTRAW-BASELINE-TIMER-DECOMP-20261031-R4-01\`
remains pending. This turn does not modify, rerun, inspect, or assume the result of that task.

This static side-research turn closes the Turn-6 reopening condition:

> For the established deterministic p=5,w=512 RMFE/R8 interface, compute the exact Moore coefficients for the four correction outputs, determine whether any Frobenius term vanishes, and quantify the HElib public-multiplier size tax.

No native execution or heavy local task was started.

## Deterministic algebraic instance

Use the already-established R16 instance:

\[
S=\mathbb Z/625\mathbb Z,
\qquad
G' = S[\xi]/(\xi^{512}+182),
\]

with

\[
\xi=X^{16}
\]

inside the HElib slot ring
\[
GR(625,8192)=S[X]/(X^{8192}+182).
\]

The established R8 generator is

\[
Y=X^{1024}=\xi^{64},
\qquad
Y^8=443\pmod{625}.
\]

Evaluation points are \(0,1,2,3,4\). The exact Lagrange basis polynomials are

\[
\ell_0=[1,50,340,260,599],
\]
\[
\ell_1=[0,4,204,314,104],
\]
\[
\ell_2=[0,622,161,623,469],
\]
\[
\ell_3=[0,418,206,522,104],
\]
\[
\ell_4=[0,156,339,156,599],
\]

so

\[
\phi(e_i)=\ell_i(\xi).
\]

The consecutive adapter maps

\[
J(\phi(e_i))=Y^i,\qquad i=0,\ldots,4.
\]

Thus the active post-R8-C2S submodule is

\[
V=\operatorname{span}_S\{1,Y,Y^2,Y^3,Y^4\}.
\]

## Exact Moore system

For \(0\le i,j<5\), define

\[
M_{i,j}=\sigma^j(Y^i)=Y^{i5^j}.
\]

The correction outputs are

\[
D_t(Y^i)=\phi(e_i)^{5^t}=\ell_i(\xi)^{5^t},
\qquad t=0,1,2,3.
\]

Because \(4\cdot5^3=500<512\), none of the target powers require reduction by the degree-512 polynomial before the Moore solve.

The exact inverse Moore matrix over
\[
E_8=S[Y]/(Y^8+182)
\]
is:

\[
M^{-1}=
\begin{bmatrix}
111-156Y^4 & -111Y^3-111Y^7 & -202Y^2 & 111Y+202Y^5 & -267-111Y^4\\
111-202Y^4 & 91Y^7 & 312Y^6 & -91Y^5 & 202+111Y^4\\
-111Y^4 & -312Y^7 & 0 & 312Y^5 & 111\\
202+202Y^4 & -91Y^7 & -312Y^6 & 91Y^5 & -202-202Y^4\\
202+267Y^4 & 111Y^3-202Y^7 & 202Y^2 & -111Y+111Y^5 & 156+202Y^4
\end{bmatrix}.
\]

For each \(t,j\),

\[
\theta_{t,j}
=
\sum_{i=0}^{4}(M^{-1})_{j,i}\,\ell_i(\xi)^{5^t}.
\]

Exact basis verification:

\[
D_t(Y^i)
=
\sum_{j=0}^{4}\theta_{t,j}\sigma^j(Y^i)
\]

passes for all \(4\times5=20\) basis-output pairs modulo 625.

## Exact support / norm table

Centered coefficient representatives are in \([-312,312]\).

| t | j | support | Linf | L1 | L2^2 | canonical max | coeff SHA256 |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0 | 0 | 30 | 306 | 5447 | 1207825 | 2175.791889979271 | \`296a68085ff8c67823896cc6d1b5ff8c864e39930949df54b43b928b9130deb6\` |
| 0 | 1 | 22 | 311 | 3135 | 646879 | 1514.998964383204 | \`f817ecf29d0084aad49cb17e902360ab7d563e081626e8cb746be9c6861ef707\` |
| 0 | 2 | 17 | 261 | 2449 | 449117 | 1506.194646264560 | \`ce60a1af69ad8761bf236c5bf03128373a73c174239c60882067a544b0cab710\` |
| 0 | 3 | 20 | 311 | 3132 | 646586 | 2316.970720909149 | \`91aa870fd5ba18b4a8958c123dae7a1af7012c97bce361b190b98d8b9f36c778\` |
| 0 | 4 | 30 | 311 | 5622 | 1321028 | 2332.980991724428 | \`3cf717170df4030c5b5bbcecbadb2638b45cf97f11a9861401341ec2cdf3f641\` |
| 1 | 0 | 122 | 311 | 19829 | 4322255 | 5870.684077363186 | \`276ac727e64ecdc1ef702df77c10c64dc7a4adb1db2ded2483c83737d8dce5cb\` |
| 1 | 1 | 90 | 305 | 13179 | 2630699 | 4091.346287386680 | \`9e40e5bd7106eb6bd3aecddbc776c61d8ee7795e95067d093e6254d98e9689bb\` |
| 1 | 2 | 68 | 310 | 10017 | 1987377 | 3311.512873925176 | \`9c96fbc67d969040698da538e1da4548d2c550db2b00d762d548387037157cf5\` |
| 1 | 3 | 88 | 310 | 13434 | 2752656 | 4828.798350623926 | \`c1be10143bbf8506cdccb01c66f38f9d2c00eec959182d96d077c3c98a2c6dd5\` |
| 1 | 4 | 122 | 311 | 19757 | 4273713 | 6426.475245228198 | \`a71fb1f7f09273c4e85bc318aa1dfa519eccbcab6ebe9f63b390eb786f0ddf3f\` |
| 2 | 0 | 456 | 311 | 71057 | 14607321 | 12791.425802693086 | \`b1b9058aab5fde08cfe1eb4c2c7d7f3c295627bea90a845ba2563e5782470079\` |
| 2 | 1 | 346 | 312 | 49982 | 9961250 | 9488.785197169724 | \`e6793555607b921d7603df6609218bd6257319fa4a467244dbd5bd144cbc720f\` |
| 2 | 2 | 283 | 310 | 50620 | 11140626 | 14043.039804676688 | \`cdab126afcb6cacf83127fad789a6d659fed0de96f630b8e409bc4139f5d0b36\` |
| 2 | 3 | 347 | 310 | 49280 | 9591432 | 7596.673739338627 | \`0a497a491ab72375531f06c9e48ee17e32638a751a239a56f9f73e26d7ee517c\` |
| 2 | 4 | 457 | 311 | 74625 | 15739247 | 10841.789976952006 | \`e088416ab02604069c8c31e718eb76852e65025754064ab4a9b1149daa04d50f\` |
| 3 | 0 | 500 | 311 | 80765 | 16933225 | 9914.943225305207 | \`8bf2adfd8e121d1cde36526b3b05ae84c2e0e228fbd46bd294521c6c505decab\` |
| 3 | 1 | 494 | 310 | 79156 | 16077472 | 11849.301198193392 | \`4f9bb232e9a32e985f3376a0947e247ef2903a77e95a1435bb0bc97a626ac4f4\` |
| 3 | 2 | 458 | 310 | 78544 | 16256420 | 12033.623978919826 | \`1e72a3b1cd681f3faa76d3b7f892dbba5e97b2506707bc48a6158b2c1af37617\` |
| 3 | 3 | 472 | 310 | 79025 | 16534825 | 10120.024582281534 | \`50906b69cca881cc143c6921e4596750a24d96950e94fcdeaa9cccf4f801bca9\` |
| 3 | 4 | 499 | 310 | 82512 | 17424250 | 9993.325319076926 | \`f9843a2976c40181181afacbec360545ef0f0dbaf2ae2a4df0b7c4b08ad2375c\` |

Every \(\theta_{t,j}\) is nonzero.

## Frobenius-support minimality

Because the input lies in \(E_8\), only eight distinct Frobenius restrictions
\[
\sigma^e|_V,\quad e=0,\ldots,7
\]
exist.

Each of those eight restrictions was expressed exactly in the canonical Moore basis
\[
\{\sigma^0,\sigma^1,\sigma^2,\sigma^3,\sigma^4\}|_V.
\]

All subsets of sizes 1,2,3,4 among the eight restrictions were exhaustively tested.

Result:

- for each individual \(D_t\), no subset of fewer than 5 Frobenius restrictions spans \(D_t\);
- for the four outputs jointly, no shared subset of fewer than 5 restrictions spans all four maps;
- every tested subset of size \(m\le5\) has reduction-mod-5 rank exactly \(m\), so the negative result is already visible over the residue field and therefore cannot be repaired by a mod-625 lift.

Hence within the exact linearized-polynomial/Frobenius family:

\[
\boxed{\text{five terms / four nonidentity Frobenius calls are minimal}.}
\]

Turn 6's 4-call schedule is therefore optimal inside this family, not merely an upper bound.

## HElib public-multiplier size

Pinned HElib \`Ctxt::multByConstant(ZZX,size<0)\` uses

\[
\texttt{embeddingLargestCoeff(poly,zMStar)}
\]

as the multiplicative noise-size factor.

For a multiplier
\[
\theta(\xi)=\theta(X^{16}),
\]
with degree below 512, this canonical embedding maximum is computed over primitive \(m=32768\) roots. Since all exponents are multiples of 16, it reduces to evaluating \(\theta(z)\) at the 1024 roots
\[
z=\exp(2\pi i(2h+1)/2048).
\]

The sum of canonical multiplier sizes for each correction output is:

| output | sum canonical size | optimistic public-multiplier tax |
|---:|---:|---:|
| \(L_0\) | 9846.937213260611 | 13.265459 bits |
| \(L_1\) | 24528.816834527166 | 14.582190 bits |
| \(L_2\) | 54761.714520830130 | 15.740880 bits |
| \(L_3\) | 53911.218303776885 | 15.718298 bits |

These are triangle-bound public-multiplier taxes only. They exclude automorphism/key-switch noise and additions beyond the standard sum bound.

Worst correction output:

\[
\boxed{15.740880\text{ bits}}
\]

before Frobenius key-switch noise.

## Comparison with the prior explicit-unpack path

For the conservative old candidate

\[
E_8
\to
8\text{-coordinate standard unpack}
\to
\text{retain 5}
\to
\text{CtxtsToSlots correction recombination},
\]

the exact rank-8 Moore unpack gives coordinate public-multiplier sum factors

\[
U=[624,1028,1028,1028,1432]
\]

for the five retained coordinates.

Let
\[
v_{i,t}=\ell_i(\xi)^{5^t}.
\]

A conservative factorized triangle bound is

\[
F_t^{\rm old}
=
\sum_{i=0}^{4}
U_i\,\|v_{i,t}\|_{\rm can}.
\]

Direct rank-5 fusion uses

\[
F_t^{\rm direct}
=
\sum_{j=0}^{4}
\|\theta_{t,j}\|_{\rm can}.
\]

Exact comparison:

| t | direct factor | direct tax | old factorized upper factor | old tax | optimistic tax saving |
|---:|---:|---:|---:|---:|---:|
| 0 | 9846.937213 | 13.265459 | 2875954.137746 | 21.455609 | 8.190150 bits |
| 1 | 24528.816835 | 14.582190 | 7820940.217872 | 22.898911 | 8.316721 bits |
| 2 | 54761.714521 | 15.740880 | 25144507.643861 | 24.583740 | 8.842860 bits |
| 3 | 53911.218304 | 15.718298 | 97255315.139962 | 26.535274 | 10.816976 bits |

This is a comparison of conservative public-multiplier triangle bounds, not a native capacity measurement.

The direct map benefits from algebraic cancellation that is lost when unpack and RMFE recombination are bounded as two separate linear stages.

## Impact on the candidate

Previous conservative candidate transform count:

\[
75\to25
\]

remains unchanged.

This turn strengthens the recovery route in two ways:

1. four nonidentity Frobenius calls are proven minimal inside the E8 linearized-polynomial family;
2. the direct rank-5 correction map does not pay a larger public-multiplier ledger than the explicit factorized route under the same conservative norm model; it is substantially smaller by 8.19--10.82 bits depending on the correction output.

The existing exact R8 C2S optimistic public-multiplier tax is 14.150203 bits. Therefore the worst sequential public-multiplier-only tax for

\[
\text{R8 C2S}
\to
\text{rank-5 shared correction}
\]

is approximately

\[
14.150203+15.740880
=
29.891083\text{ bits},
\]

before automorphism/key-switch noise.

This remains a nontrivial capacity cost and does not establish whole-pipeline capacity.

## Verdict

\`\`\`text
RESULT:
  PASS_EXACT_RANK5_MOORE_AND_NORM_GATE

EXACT_MOORE_BASIS_CHECKS:
  20/20 PASS

THETA_COUNT:
  20

ZERO_THETA:
  0

MIN_SHARED_FROBENIUS_TERMS:
  5

MIN_NONIDENTITY_FROBENIUS_CALLS:
  4

FOUR_CALL_SCHEDULE:
  OPTIMAL_WITHIN_E8_FROBENIUS_LINEARIZED_FAMILY

WORST_DIRECT_PUBLIC_MULTIPLIER_TAX:
  15.740880 bits

DIRECT_VS_FACTORIZED_PUBLIC_MULTIPLIER_BOUND:
  DIRECT BETTER by 8.19--10.82 bits

R8_C2S_PLUS_DIRECT_CORRECTION_PUBLIC_MULTIPLIER_TAX:
  ~29.891083 bits worst case, excluding key-switch noise

NATIVE_LATENCY:
  NOT ESTABLISHED

WHOLE_PIPELINE_CAPACITY:
  NOT ESTABLISHED

NOVELTY:
  NOT ESTABLISHED
\`\`\`

## Pending task interaction

The running baseline timer task remains untouched and retains priority when its result is returned.

Its hard-kill threshold remains a sufficient condition because the new recovery cost is positive.

No additional native task should be started while that slot is occupied.

## Next independent side-research candidate

If the baseline timer remains pending, the next highest-value static question is whether the existing R8 C2S and rank-5 correction map can be **jointly synthesized on the rank-5 image** with fewer than the current 6+4=10 automorphism/key-switch calls without reopening the generic rank-16 failure.

That question should be tested first by an exact rank/support lower bound, not by implementation.

AI_PROVISIONAL_CHOICE:
  RETAIN_POST_RAW_FUSION
  PROMOTE_RANK5_SHARED_CORRECTION_OVER_EXPLICIT_UNPACK
  KEEP_PENDING_BASELINE_TIMER_AS_DECISIVE_LATENCY_GATE

INDEPENDENT_RESEARCH_AVAILABLE: true
RESEARCH_FRONTIER_EXHAUSTED: false
