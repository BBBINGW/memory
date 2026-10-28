# BOOT — B158 residual structural rescue scout after B163

Date: 2026-10-28
TRACK_ID: BOOT
Native authoritative state remains:
- LATEST_COMPLETED: B163_AUDIT
- B163_STATUS: FAIL_B163_NATIVE_NOISE
- B158_PRACTICAL_LINE: PARK unless a materially different noise mechanism is found.

## New trace-level observation

B163 keeps logQ=649 and performs no selector Rescale.

Late-stage trace:
- state k=2048: required_logQ=571, budget=78
- selector M_k*RowRotation(S_k) for target 4096: required=591 (about +20 bits)
- fused output k=4096: required=620 (another +29 bits)
- state k=4096: required=620, budget=29
- selector M_k*RowRotation(S_k) for target 8192: required=646 (about +26 bits), still exact with budget=3
- fused output k=8192: required=665 (another +19 bits), then failure.

Thus the late failure is not attributable only to the ct-ct tensoring. The public 0/1 selector plaintext multiplication is a major noise amplifier, consuming about 16-26 required-logQ bits per late stage in the observed trace.

## Current-layout mask-free no-go

For k>=2 the B158 state is
  S_k = [P_k repeated H/k | x^k repeated H].
After row swap, the left row containing x^k is constant across all H positions.

The desired factor requires on the left row
  [1^k, (x^k)^k] repeated,
equivalently selecting x^k by the nonconstant periodic public mask M_k.

Within the current power-of-two batching layout, row-preserving slot automorphisms/rotations only permute the constant x^k row. Any public linear combination of such permutations remains constant in that row. Row swap only exchanges the two rows. Therefore the nonconstant M_k*x^k pattern cannot be synthesized from the current layout using only automorphisms, additions and public scalars.

Conclusion:
  SIMPLE_MASK_TO_ROTATION_REPLACEMENT = FAIL in the current layout.
A rescue must change either the selector representation/lift or the state/slot layout.

## Highest-priority residual candidate: noise-aware selector representation

The masks M_k are public plaintexts in R_T. Their multiplication amplifies coefficient noise substantially. The same plaintext semantics may admit different integer/RNS representatives or a different logical slot layout, with different multiplication-operator norms.

Candidate question:
Can the fixed family of B158 stage masks be represented or laid out so that ct-pt selector multiplication has materially smaller noise amplification, without adding ct-ct depth or changing security parameters?

Cheapest gates:
1. recover the exact encoded polynomial coefficients/canonical multiplication norm of each B158 selector at T=65537, N=32768;
2. correlate those norms with the measured +16..+26 bit selector noise increments;
3. test whether equivalent lifts / allowed slot permutations can reduce the relevant operator norm while preserving exact plaintext semantics;
4. reject immediately if the centered standard representative is already optimal for the relevant norm, or if the alternative lift creates comparable message-dependent noise;
5. only then consider a native patch.

This is motivated by general plaintext-lifting literature, but direct novelty for B158 is NOT established.

## Second structural candidate: automorphism-rich / higher-dimensional hypercube layout

Power-of-two cyclotomic batching exposes essentially a 2 x H slot geometry. B158 needs a hierarchy of stage-dependent binary selectors M_k. General BGV/BFV cyclotomics can expose multi-dimensional slot hypercubes, where rotations along good dimensions are single automorphisms.

Hypothesis:
choose a plaintext/cyclotomic layout where more of the exponent-doubling selector bits correspond to hypercube dimensions, so stage selection can be implemented by automorphisms/permutations rather than high-norm plaintext masks.

This is a representation change, not a drop-in tweak. It has substantial prior art risk because hypercube slot layouts and good/bad dimensions are classical HElib/BGV machinery. Novelty would require a specific theorem tying the power-basis recurrence to a selector-noise reduction or operation/noise bound.

Status: HIGH-RISK / PAPER-LEVEL ONLY.

## Lower-priority candidates

### Deferred/less frequent relinearization
The late fused ct-ct step adds roughly 19-29 required-logQ bits beyond the factor in the observed stages. Lattigo scale-invariant tensoring includes quantization and relinearization. A diagnostic separating pre-relinearization vs post-relinearization noise could determine whether key-switch noise is a large share.

Do not implement before a source-level cost/noise gate; higher-degree ciphertexts and extra relinearization keys can erase the value.

### Selective refresh / component-wise re-encoding
Recent CKKS/GCKKS work (ePrint 2026/2600) reports useful-slot-preserving conversion and resetting unused slots through component-wise re-encoding. This is conceptual inspiration only: B158 needs exact BFV/BGV semantics and both halves are useful. A full or recursive bootstrap inside B158 is likely value-negative.

### Separate clean power chain
Reintroducing a clean x^(2^i) chain restores noise independence but also restores almost all multiplications eliminated by B158. Unless a genuinely cheaper squaring mechanism exists, this collapses back toward the 28-multiplication baseline and is not publication-worthy.

## Priority after this scout

1. B158 selector-noise / equivalent-representation gate.
2. If that fails, paper-level hypercube-layout feasibility theorem.
3. Only if either is promising, measure relinearization contribution.
4. Otherwise keep B158 practical line PARKED and return to 2026/1779 / 2026/2630.

No native experiment, Codex run, parameter change, or other research-track modification was performed.
