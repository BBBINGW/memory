# BOOT / B158_OVERALL — Successor Research Turn 19/25
Date: 2026-11-12 Asia/Singapore
TRACK_ID=BOOT
ACTIVE_SUBLINE=B158_OVERALL
Phase=PROBLEM_SELECTION
Candidate=boot-b158-fully-unmerged-branch-per-rail-babybasis-v1
Verdict=FAIL_EXPLICIT_RAIL_FRONTIER_COST / PARKED
Native/Codex=NOT_RUN

## Read-before-write durable provenance
Entering ACTIVE UNKNOWN, BACKUPS none. Independently fetched:
- findings/boot-b158-successor-turn18-two-rail-virtual-axis-single-ct-merge-equivariance-gate-2026-11-12.md, blob e1f95297396266cc0d1e01524d0341e5129a6779, PARKED. Turn18 demands a single ciphertext spatial mux and fails equivariance. THIS candidate changes output interface: it **never merges** branches until the final LUT linear transformation. No reopening of Turn18.
- findings/boot-B158-checkpoint-decoupled-halfbasis-gate-2026-10-28.md blob 49a85b46bf23566b24324e0994b7f2830b136dc5. Authorized B158 historic halfbasis uses masks and normal 1-ciphertext baby basis; it is not the proposed per-branch rails.
- findings/boot-B158-selector-norm-lift-layout-gate-2026-10-28.md blob 17fdf11bffe6044326fa243750d5b3869eb297f7: dyadic masks high noise; H left-row size16384 for older full basis.
- findings/boot-B175-hybrid-selector-pareto-screen-2026-10-29.md blob f12765dd3d2526bf9f9d5ae8771621aa184862c3: B175 count26 ctct through output, projected27 with leading; packed-selector hybrids no all-in value.
B175 actual halfbasis parameter H=8192, checkpoint k0=32, s=8; N=32768, T=65537, L18=19 RNS primes, Q bitlength649; original B175 pointwise required bits664, bitlength Q649, 32767/32768 mismatches. Archive SHA256 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa.
This candidate must not be confused with B158's former H=16384 full-row basis. All quantitative statements below apply to the audited B175 H8192 halfbasis setting.

## Pre-registered high-information paper-level gate
QUESTION: Can B175 avoid all high-norm late stage public selector masks by never re-packing the recursively expanded power branches, instead maintaining one degree-one RLWE ciphertext rail per baby-basis monomial x^(j*k0) and supplying these rails directly to a modified final ParallelLT, while achieving a credible full-system advantage under N32768 and fixed Q?
CURRENT_BELIEF: No, the exact branch-per-rail representation grows from 1 to H/k0=256 explicit rails, with either massive live ciphertext memory or many reassembly operations; the 26 ctct packed baseline will dominate any naive uncompressed route. This is NOT a universal lower bound on all compressed multioutput algorithms.
CHEAPEST_DECISIVE_TEST: Derive the exact monomial count and current ciphertext memory cost, and separately account for streaming versus simultaneous rails, final LT interface mismatch, and the simplest branch-generation cost. No native.
IF_PASS: If a concrete source-compatible compact rail representation produces the complete B175 halfbasis, whole LUT output and zero-root behavior with few ctct and acceptable memory/key/offline costs, retain ACTIVE for exact canary and baseline comparison.
IF_FAIL: If the specified fully UNCOMPRESSED branch-per-rail construction demonstrably violates even optimistic ciphertext memory/count budget, and any streaming alternative gives up the claimed amortization by reintroducing masks or recomputation, PARK without native.
IF_UNCLEAR: Keep compressed rail packing / source-specific streaming DFR UNKNOWN and require a different complete typed construction; do not claim a universal space-time lower bound.
WHICH_PAPER_GATE_CHANGES: exact complete B175 babybasis/LT output semantics (gate1), typed multi-ciphertext ParallelLT interface (gate2), and optimistic full-system time/memory/key/DFR frontier (gate3).
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: Turn18 could not obtain mask-free SINGLE-ct mux. This is its most favorable fully unmerged escape. If 256 separate ciphertexts and full reaggregation costs make the baseline worse before correctness testing, native research of this explicit route is not justified.

## Exact plaintext functionality
At checkpoint k0=32, let z=x^32. Required B175 baby basis at H=8192 contains powers x^0 ... x^8191, or equivalently 256 blocks of 32 powers:
  x^(32j+i), j=0..255, i=0..31.
The proposed branch-per-rail interface stores each block separately, with one rail B_j carrying x^(32j)*[1,x,...,x^31] (or a more optimistic B_j scalar factor z^j if the length32 base rails are freely shared).
The j-blocks are distinct polynomial functions over F_65537: degrees 32j up to8160 (<65537-1), so x^(32j) are linearly independent over F_65537 as functions on ALL field inputs, as a nonzero polynomial of degree <65537 cannot vanish at all 65537 field points. This establishes 256 distinct monomial values for this explicitly unmerged representation; it does NOT exclude an alternative packed/compressed basis.
An exact branch tree with dyadic stage expansion from one interval at k0 doubles number of unmerged branches at each stage. H/k0=8192/32=256=2^8, so eight branch doublings produce 256 rails. This is an EXACT branch count by construction, not a lower bound for arbitrary circuits.
A complete output must compute for each coefficient block f_j(x)=sum_{i=0}^{31} c_{32j+i}x^i the contribution z^j f_j(x), sum over 256 j, and preserve arbitrary input coefficient vector and zero root. If all branch rails are independent full RLWE ciphertexts, original stock ParallelLT expects one packed ciphertext with row/slot layout; source-compatible multi-input LT and final output aggregation have not been constructed. A direct alternative of 256 independent block evaluations plus additions/rotations/merges is a DIFFERENT full-interface cost, not free. A final plaintext mask per rail (spatial packing) would reintroduce some very same norm-cost mechanism that motivated the candidate.

## Optimistic exact resource accounting
One degree-one ciphertext at full N32768, L18 19 moduli and ordinary 64-bit per-RNS-limb storage uses at least
  2 components * 32768 coefficients * 19 limbs * 8 bytes = 9,961,472 bytes =9.5 MiB
for its two coefficient arrays. 256 simultaneous rails would require
  256 * 9,961,472 = 2,550,136,832 bytes = 2.375 GiB
in raw ciphertext polys alone, excluding metadata, temporary ciphertexts, NTT buffers, evaluation keys, basis state, output accumulators, rotations and offline keys. This is an implementation representation cost given Lattigo's 64-bit RNS arrays, not an unconditional information-theoretic storage lower bound for all implementations.
B175 existing eval key serialized BinarySize around 1062.54 MiB, NOT RSS, and is additional to ciphertext polys; claiming it can be removed from the rail scheme is unsupported because rotation/relin for the output remain necessary.
If instead streaming one rail at a time, the 2.375GiB simultaneous-memory example no longer applies. But one must either regenerate/recompute rail values later or immediately feed them to a typed cross-rail LT/accumulator, which entails many operations and/or nonuniform plaintext selector terms. Exact memory-time tradeoff cannot be quantified without a concrete stream schedule and keys; DO NOT claim a general 2.375GiB lower bound.
Under a naive monomial-only rail generation using one initial rail 1 and available z=x^32, producing 256 distinct x^(32j) (j=0..255) requires creating 254 additional nontrivial monomial rails beyond 1,z, with ordinary ct-ct multiplication per newly produced rail in this PARTICULAR grammar. This is an example, not a general arithmetic lower bound; other packed or nonlinear algorithms may reuse data differently.
Against 26 ctct through B175 output and its approximately 1.06GiB serialized key binary size, the straightforward 256-rail representation lacks a plausible frontier gain even with a generous zero-noise assumption. Most importantly, it has no verified fixed-Q DFR or corrected B175 whole output. We cannot infer measured runtime or precision superiority/inferiority from these counts alone; the claim is a failure of this explicit naive construction's optimistic paper-value screen.

## Prior art and novelty
Standard Paterson–Stockmeyer baby/giant decomposition already computes monomial blocks and weights; branch-per-monomial powers are basic uncompressed polynomial evaluation. Existing B158 checkpoint halfbasis and B175 hybrid circuits seek to AMORTIZE many powers via SIMD; unmerging 256 rails discards the exact principal resource benefit. Generic naive uncompressed branch rails have no separately established novelty. The possibility of a new compressed rail layout that changes the tradeoff is NOT precluded, but needs a new typed mechanism rather than merely increasing rail count.

## Final gate disposition
Gate1 conditional plaintext polynomial identity PASS_MATH, but COMPLETE packed LT/extraction typed interface not established. Gate2 stock source cannot be assumed to consume a 256-ciphertext collection in the existing single-input ParallelLT: BLOCKED. Gate3 optimistic VALUE FAIL for the candidate-defined fully materialized explicit branch basis, due 256 live rails / 2.375 GiB raw polys and naive branch generation ≫26 ctct, without guaranteed noise/DFR recovery.
STATUS=PARKED. NEW_MECHANISM=NO_CREDIBLE_NEW_MECHANISM for explicit fully unmerged rail-per-block construction.
REOPEN_CONDITION: Present an actual compact multi-rail representation or source-typed streaming LT that avoids the 256 simultaneous rails AND avoids per-rail recomputation/mask relocation, proves complete arbitrary-message/zero-root polynomial output, source compatibility, positive fixed-Q precision/DFR, security, fair all-in count/memory/keys/offline cost, and independently verified novelty beyond classic PS/SIMD.
ELIMINATED_UNCERTAINTY: Does eliminating all selector masks by explicitly materializing one ciphertext per checkpoint-monomial block plausibly preserve the packed 26-ctct and modest-memory value frontier? No: 256 branch rails and 2.375GiB raw poly storage if simultaneous; alternative streaming is an unconstructed different algorithm.
DECISION_CHANGED=true; research_frontier_exhausted=false; no ACTIVE or BACKUP carried.
