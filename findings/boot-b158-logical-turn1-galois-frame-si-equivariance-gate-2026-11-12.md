# BOOT / B158_OVERALL — logical Research Turn 1/25 (UI identity recovery)
Date: 2026-11-12 Asia/Singapore
Phase: PROBLEM_SELECTION
Candidate: boot-b158-galois-frame-conjugated-final-si-v1
Status: PARKED; FAIL_IDEAL_EQUIVARIANCE / FAIL_VALUE_MECHANISM
This is logical Turn 1; the immediately preceding assistant-produced turn was expressly invalidated by the PI's UI identity recovery instruction and must not be counted or interpreted as evidence for this turn.
No native/Codex task launched or resumed.

## Question and registered decisions
QUESTION: Can applying the same nontrivial cyclotomic Galois automorphism to BOTH B175 input ciphertexts, multiplying with stock BGV MulRelinScaleInvariant, and then applying the inverse automorphism give a provable coefficient-geometry reduction sufficient to repair the fixed-Q ~16 required-bit deficit while preserving the whole 32768-slot product?
CURRENT_BELIEF: No. An automorphism X -> X^g (g odd mod 2N) is a signed permutation of degree-N coefficient vectors and a ring automorphism; the raw tensor and coefficientwise centered nearest-integer SI rounding are equivariant, leaving the ideal dominant residual's coefficient max norm invariant. Actual Galois evaluation adds key-switch noise and keys/operations, not a designed contraction.
CHEAPEST_DECISIVE_TEST: Derive ideal automorphism-equivariance of the complete tensor + centered scaling/quantization path with exact half-tie conditions; then examine stock rotation interface and optimistic value. No native test.
IF_PASS: If a source-supported non-equivariant step gives a provable useful >=16-bit contraction of the complete B175 tensor/reference residual family with exact output semantics, admit ACTIVE for constructive source/parameter/key specification.
IF_FAIL: If the ideal transformation is exactly conjugate and norm preserving, PARK this candidate with no native run.
IF_UNCLEAR: Resolve only exact rounding and Galois-key-switch interface; do not claim improvement from instance-specific cancellation.
WHICH_PAPER_GATE_CHANGES: killer gate 1 (whole-output and carry), gate 2 (key/interface), gate 3 (full-system value).
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: The purported gain requires reshaping the dominant coefficient residual; exact signed-permutation equivariance gives zero ideal gain regardless of which automorphism is chosen.

## Baseline and sources
B175 original N=32768, T=65537, fixed Q_L18, LT8 required bits 577, GROUPED 633, POINTWISE 664, log2 Q ceiling 649; allowed required bits <=648, conditional necessary recovery >=16 bits, per findings/boot-B175-static-noise-attribution-audit-2026-10-29.md (source blob e31ec2cbee6886ca61b6bc721920938d2a8a072b) and findings/boot-B175-source-level-si-error-bounds-2026-10-29.md (source blob c75aa60e080b28b688de7ee8859c5df4d1951c02).
Pinned source: tuneinsight/lattigo v6.2.0, schemes/bgv/evaluator.go blob 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f. Public v6.2.0 API: https://pkg.go.dev/github.com/baahl-nyu/lattigo/v6@v6.2.0/schemes/bgv documents RotateColumns requiring Galois keys and degree-one ciphertext, MulRelinScaleInvariant, and GaloisElementForColRotation X->X^{5^k mod 2N}. No claim of full source re-audit in this turn.
Closest prior art is ordinary cyclotomic Galois automorphism/slot rotation in BGV and the stock rotation + SI tensor APIs. Proposed delta is to conjugate one complete final SI product by the SAME Galois transform on both inputs, instead of rotating slots as a computational primitive; novelty is PREFLIGHT, with obvious construction-level collision with already-known algebraic symmetry.

## Exact ideal semantic/carry oracle
Let R_A=Z_A[X]/(X^N+1), A odd, N=32768, and let g be any odd unit mod 2N. Define phi_g(f(X))=f(X^g) mod X^N+1, over any coefficient ring. Because g is odd and invertible mod 2N, phi_g maps the standard basis {X^i}_{i=0}^{N-1} bijectively to {+/- X^{pi(i)}}, a signed permutation P_g. Consequently ||center_A(phi_g(f))||_infty=||center_A(f)||_infty (including mod-A centered coeffs). Also phi_g(fh)=phi_g(f)phi_g(h) in every R_A; phi_{g^{-1}}phi_g=id.

For componentwise centered exact Q->QMul basis extension, phi_g commutes with lift, since both lift and phi are compatible with a coefficient signed permutation (odd Q and QMul eliminate nonzero signed representatives at exact ties). For exact coefficientwise SI integer scaling q_{Q,T}(z)=nearest_integer(T*z/Q) with consistent odd symmetry and z centered, phi_g q = q phi_g. Here Q odd and T odd: T*z/Q cannot land on a half-integer unless 2Tz=(2k+1)Q; since Q is odd this has no nonzero half-tie for integer z when interpreted with the chosen centered rational representative; more generally use a tie convention symmetric under negation. The exact Lattigo quantizer has not been re-proven from byte-level source for all edge conventions, so this is an ideal/source-structured statement, NOT full native correctness.

For degree-one input C=(c0,c1), D=(d0,d1), prequantized tensor U=(c0d0,c0d1+c1d0,c1d1). Since phi is multiplicative and additive, U(phi C,phi D)=phi U(C,D); centered lifts and ideal SI quantization preserve equality componentwise. Decryption after the automorphism uses secret phi(s), or after key-switch to original s has extra switching noise. The expected plaintext/reference is phi(m_C m_D) before inverse phi, so carry/reference corrections transform the same way under ideal coefficientwise embedding. Therefore the ideal completed residual satisfies e_ideal(phi C,phi D;phi s)=phi(e_ideal(C,D;s)), and ||e'_ideal||_infty=||e_ideal||_infty. Applying inverse phi restores the same plaintext and error coefficient norm, not a contraction. All 32768 slots are permuted before multiplication and exactly restored afterward.

## Stock feasibility and value
Stock RotateColumns/RotateRows performs automorphism with secret-key switching; each requires generated Galois keys. Applying g to BOTH input ciphertexts and g^{-1} to output costs >=3 automorphism/key-switch operations and potentially additional Galois-key memory, without reducing the 1 failing ciphertext-ciphertext SI product, Q-limbs, or multiplicative depth. The ideal tensor/reference residual is unchanged up to signed permutation; any real differences arise from extra key-switch errors or implementation particulars, for which no deterministic or useful probabilistic >=16-bit noise recovery has been derived. Such errors may accidentally cancel a specific trace, and this finding does not claim impossibility for all stochastic noise coincidences.
Killer gate 1: PASS for ideal whole-output semantic identity, but no exact stock key-switched residual guarantee.
Killer gate 2: stock rotations exist with Galois keys; no distinct source-level coefficient-shaping primitive.
Killer gate 3: FAIL optimistic mechanism/value as exact ideal norm recovery is 0 bits and extra rotations/keys have nonnegative cost. (Not a measured runtime claim.)
NO_CREDIBLE_NEW_MECHANISM for this candidate. PARK; no active paper candidate admitted.
Precise obstruction: fixed common Galois conjugation is an isometry of the exact ring tensor/reference geometry, not a tensor-component balancing mechanism.
Reopen only with source-backed non-equivariant transformation, provably useful B175 full residual/DFR reduction under exact whole-output semantics, and comprehensive key/noise/offline/memory/runtime ceiling. Plain rotations and relying on accidental cancellation do not qualify.
ELIMINATED_UNCERTAINTY: Can ideal common Galois-frame conjugation shrink the norm of B175 dominant tensor/reference error? No, exactly invariant under signed permutation.
DECISION_CHANGED: true from untested distinct hypothesis to PARKED after algebraic falsification.
EVIDENCE_REFS: this finding path and verified commit/blob; pinned source URLs and blobs above; the signed permutation derivation in this finding.
NOVELTY_STATUS: PREFLIGHT; PAPER_READINESS: NOT_READY.
