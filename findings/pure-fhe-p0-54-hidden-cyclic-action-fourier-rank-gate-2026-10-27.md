# PURE-FHE — P0-PRESCOUT-54: Hidden Cyclic-Action Fourier / Operator-Rank Gate

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
PREVIOUS: P0-PRESCOUT-53 plus post-P0-53 hidden multi-bit action HUMAN_REVIEW
LATEST_COMPLETED: P0-PRESCOUT-54
NEXT_ITERATION: P0-PRESCOUT-55 NOT_STARTED
STATUS: FAIL_NATIVE_FOURIER_HIDDEN_SHIFT / PASS_ONE_STAGE_OPERATOR_RANK_LOWER_BOUND / FAIL_PRIVATE_FKS_BYPASS / NOVELTY_NOT_ESTABLISHED
CODEX_REQUIRED: NO
STATE_UPDATE: YES — isolated PURE-FHE finding only; root STATE.md and other tracks unchanged.

## Primary hypothesis H54

Can the exact P0-52 two-sheet secret cyclic/semilinear shift be transformed into a Fourier/group-algebra basis so that one compact secret-dependent phase key represents a hidden gap d in [0,B), and the online action costs about O(n) base-ring EP-equivalents rather than O(n log B), while retaining the arbitrary negacyclic LUT path?

The intended construction was:

1. Let L = 2n and P be the exact two-sheet cyclic-shift operator from P0-52, so hidden gap d acts as P^d.
2. Apply a public character/Fourier transform F over the list index:
      F P^d F^{-1} = diag(zeta^{0d}, zeta^{1d}, ..., zeta^{(L-1)d}).
3. Try to encode d compactly in one or polylogarithmically many RGSW/GGSW-style keys and apply the diagonal action with O(L) mode-wise work.
4. Invert F or use an equivalent public linear readout.

Cheapest decisive tests:
- Is an exact invertible character basis available under the source's native modulus q = 2^64?
- Even if the modulus is changed so a DFT exists, can B distinct hidden shifts be represented in one scalar-gadget layer using o(B) independent secret-dependent operator coefficients?
- Does private/functional key switching hide the secret permutation/index without reintroducing the same operator basis?

## Primary sources / nearest mechanisms

### [FACT] CCS 2025 AmortBoot source parameters
Guimarães–Pereira, *Fast amortized bootstrapping with small keys and polynomial noise overhead*, ePrint 2025/686.
GitHub Notes cached PDF SHA256:
84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335
VERSION_UNVERIFIED.

- Algorithm 1 MPmul uses log B encrypted gap bits and n external products per bit stage.
- Lemma 4.1 / Algorithm 2 gives O(h n log B) EP for binary sparse SAB.
- Concrete parameter Tables 3–4 use q = 2^64.

### [FACT] BootMMPM source
Duan–Li–Liu–Ma, *Large-Plaintext Functional Bootstrapping in FHE with Small Bootstrapping Keys*, ePrint 2025/1717 / TCC 2025.
GitHub Notes PDF SHA256:
26b1e326351f6feffac72de8a3223bfe218a7e707fb79d585f8437c9a8e427f2
VERSION_UNVERIFIED.

Physical pp.14–20 were inspected in the prior post-P0-53 gate.
BootMMPM uses public monic-monomial permutation matrices Phi(a) and scalar encrypted controls RGSW(s_k^+), RGSW(s_k^-); it does not give a compact Enc(Phi(d)) for a hidden multi-bit d.

### [FACT] Carousel source
Hwang–Min–Song, *Carousel: Fully Homomorphic Encryption with Bootstrapping over Automorphism Group*, ePrint 2024/2032.
GitHub Notes PDF SHA256:
5ddec99ebbe14b270b413e21ab4923abf0ed5dba8d0f1d053b3fde1c5a35d6c8
VERSION_UNVERIFIED.

Physical pp.24–25 explicitly state a space/time trade-off for automorphism keys:
- all N-1 automorphism keys allow direct automorphisms;
- only O(log N) keys can be stored and arbitrary automorphisms composed from binary powers, increasing time by O(log N);
- this generalizes to b-ary representation using b log_b N keys.

This is direct prior-art evidence that compact generator sets versus composition depth are already an explicit FHE trade-off.

### [FACT] Private functional key switching check
Kim–Park–Sung, *Private Information Retrieval based on Homomorphic Encryption, Revisited*, ePrint 2025/729.
GitHub Notes PDF SHA256:
f5ece25e405b8a7f69c1f0df937371770e7aee0fc3e1c309f0992f272ecdd87c
VERSION_UNVERIFIED.

Physical pp.8–9 / Algorithm 1 "PrivKeySwitch" were inspected.
The algorithm receives the coefficient index k as a PUBLIC input, performs SampleExtract(c,k), and uses a KSK encrypting secret-key coefficients. It does not supply a hidden runtime coefficient/permutation index encoded only in the key. Therefore this particular private functional KS does not bypass H54's hidden-action problem.

## [DERIVATION] Killer 1: native q=2^64 does not admit the desired invertible DFT basis

Let L = 2n, with n a power-of-two source dimension, and let A = Z/(2^64)Z.

The ordinary character diagonalization of the L-cycle uses an L-th root of unity zeta and a DFT matrix F whose inverse contains the factor 1/L. But L is even, hence L is not a unit in A. Therefore the standard L-point DFT cannot be an invertible A-linear change of basis.

A stronger reduction argument gives the same obstruction. Let P be the L-cycle permutation matrix. Reducing modulo 2:
  x^L - 1 = (x - 1)^L
in characteristic two for power-of-two L.
The cyclic permutation matrix has minimal polynomial x^L - 1, hence after mod-2 reduction its minimal polynomial has a repeated root of multiplicity L and is not square-free. Thus P mod 2 is not diagonalizable over any field extension of F_2.

If P had an exact invertible diagonalization over an integral 2-adic / Z_(2^64)-compatible extension whose change-of-basis matrix remained invertible modulo 2, reducing that diagonalization mod 2 would diagonalize P mod 2, contradiction.

Therefore the proposed exact native-torus character basis is not available. This does not rule out changing ciphertext modulus/ring, approximate transforms, non-semisimple/Jordan representations, or a different FHE scheme.

### Useful interpretation
In characteristic 2, the shift representation is unipotent rather than semisimple. Mod 2 one may write P = I + N with N nilpotent, and
  P^d = product_i (I + b_i N^(2^i))
for the binary bits b_i of d.
This mirrors the source's binary staged MPmul rather than collapsing it into independent characters. This is an algebraic explanation, not a universal lower bound on every encrypted cyclic-shift circuit.

## [DERIVATION] Killer 2: one-shot scalar-gadget hidden shift needs B operator basis elements

This result is independent of the modulus and survives an odd-modulus redesign.

Let A be any commutative coefficient ring and P the exact L-cycle operator on A^L. For 0 <= d < B <= L, the operators
  I, P, P^2, ..., P^(B-1)
are A-linearly independent.

Proof:
Assume sum_{d=0}^{B-1} a_d P^d = 0.
Apply this operator to the first standard basis vector e_0. Since P^d e_0 = e_d for d < B <= L,
  sum_d a_d e_d = 0.
The standard basis is free, so every a_d = 0.

Now consider any ONE-STAGE scalar-controller construction whose plaintext action has the form
  T_d = A_0 + sum_{j=1}^r f_j(d) A_j,
where:
- A_j are fixed public A-linear operators on the state;
- f_j(d) are arbitrary secret-dependent scalar functions supplied through scalar RGSW/GGSW-like controls;
- online evaluation is linear in those controller plaintexts (public transforms + external/gadget products + additions), with no nonlinear composition among the controller ciphertexts before applying the state.

Then all T_d lie in span_A{A_0,...,A_r}, which has rank at most r+1. To realize T_d=P^d for every d in [0,B), whose span rank is B, necessarily
  r + 1 >= B,
so
  r >= B - 1.

Therefore a one-shot linear scalar-controller hidden shift cannot use O(log B) independent selector payloads. It needs B-scale operator basis material. The ordinary one-hot/q-ary construction meets exactly this qualitative requirement.

This is a model-specific lower bound:
- it does NOT rule out nonlinear composition of encrypted controls;
- it does NOT rule out an encrypted vector/matrix/tensor controller;
- it does NOT rule out changing the state representation;
- it does NOT prove an unconditional lower bound for arbitrary FHE circuits.

But it kills the concrete hoped-for "one compact scalar phase key + one linear gadget layer" construction.

## [DERIVATION] Odd-modulus Fourier redesign still hits the same rank wall

Suppose we replace q=2^64 by an odd NTT-friendly q' with L | (q'-1), so an exact DFT exists:
  P^d = F^{-1} D_d F,
  D_d = diag(zeta^(0d), ..., zeta^((L-1)d)).

Because conjugation by invertible F preserves linear independence, the diagonal operators D_0,...,D_(B-1) also span a B-dimensional operator space.

Hence if the diagonal action is realized in one scalar-gadget layer from fixed public diagonal bases and secret scalar coefficients, the same r >= B-1 lower bound applies.

A single RGSW(zeta^d) does not itself provide all mode multipliers zeta^(kd):
- deriving them by repeated GSW×GSW powers introduces nonlinear ciphertext-ciphertext synthesis and depth/noise;
- storing fresh RGSW(zeta^(kd)) for all k gives rank-sized key material;
- deriving them through automorphisms requires applicable plaintext automorphisms and key-switching/composition, and only moves into the known key/time trade-off;
- packing the entire secret diagonal operator in a vector/module GSW returns to the P0-52 tensor/module representation class.

Therefore merely switching to an odd modulus makes the DFT mathematically available but does not give the missing compact hidden-action operator.

## [FACT + DERIVATION] Relation to known space/time trade-offs

Carousel pp.24–25 gives an explicit nearby example:
- N-1 automorphism keys: direct action;
- O(log N) generator keys: compose O(log N) automorphisms;
- b-ary: b log_b N keys.

This is not a proof that every hidden shift must obey exactly the same formula, but it supports the mechanism-level interpretation of H54:
  fewer stored action basis elements -> more online composition,
while direct high-arity action requires more key material.

The H54 rank proof explains why a one-stage scalar-controller endpoint needs B-scale basis material; the source binary MPmul occupies the opposite endpoint with O(log B) selector material and O(log B) stages.

## Private functional KS bypass: FAIL for inspected mechanism

The 2025/729 PrivKeySwitch does not hide index k. It uses a public k to select the sample-extracted coefficient and then applies a KSK independent of k. Therefore it cannot directly implement "secretly choose one of B cyclic shifts of an arbitrary runtime ciphertext list".

More generally, if a functional-KS candidate keeps the online transform linear in arbitrary input state while the secret function only enters through a bounded number of scalar encrypted coefficients, the operator-rank argument above still applies. A different functional key with operator-valued ciphertext payloads would have to be costed as a new matrix/module/tensor representation rather than treated as free.

## Contribution / novelty decision

H54 FAILS as a construction.

What was learned is stronger than another toy counterexample:

1. Native q=2^64 blocks the intended exact Fourier diagonalization at the algebraic level.
2. Even if an odd modulus repairs the DFT, the B hidden cyclic shifts have operator span rank B, so a one-stage scalar-gadget realization requires B-scale independent controller basis.
3. Private functional key switching, in the inspected TFHE/PIR form, uses a public extraction index and does not supply a hidden permutation primitive.
4. The remaining alternatives are exactly the categories already identified:
   - nonlinear composition/windowing -> time/key trade-off;
   - B-way selectors -> B-scale key/work;
   - vector/matrix/tensor operator ciphertext -> representation blow-up;
   - a genuinely new non-linear compact operator representation -> still missing.

The operator-rank lemma is elementary linear algebra and is NOT claimed as a publication contribution by itself. Its value is to close a large class of superficially promising P0-55 variants before more work.

## End of Iteration

TRACK_ID: PURE-FHE
ITERATION: P0-PRESCOUT-54
STATUS: FAIL_NATIVE_FOURIER_HIDDEN_SHIFT / PASS_MODEL_SPECIFIC_OPERATOR_RANK_LOWER_BOUND / HUMAN_REVIEW
PRIMARY_HYPOTHESIS: compact Fourier/group-algebra hidden shift can reduce MPmul n log B -> O(n) with compact scalar action key.
SMALLEST_TEST: native-modulus DFT invertibility + one-stage operator-span rank.
EVIDENCE_LEVEL: DERIVED + primary-source audit; NO native experiment.
SECURITY/DFR: NOT_REACHED because representation gate fails first.
NOVELTY: NOT_ESTABLISHED.
COMPLETE_SPEED/KEY/RAM_HEADROOM: candidate not viable; no performance claim.
DECISION: KILL one-shot Fourier/scalar-controller route. Do not implement.
NEXT_TEST: NONE automatically. Before P0-55, require a concrete mechanism that escapes the one-stage scalar-controller model without merely becoming (a) known b-ary/windowed composition or (b) matrix/module/tensor GSW. Otherwise issue HUMAN_REVIEW and pivot away from MPmul.
STATE_UPDATE: YES — this finding only.
CODEX_REQUIRED: NO.
