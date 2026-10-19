# BOOT B021 — Boundary-only integer soundness for two linear torus additions

TRACK_ID: BOOT
ITERATION: B021
DATE: 2026-10-19
STATUS: PASS_CONDITIONAL_LINEAR_FUSION / FAIL_ONE_BIT_PARITY / PASS_TWO_BIT_INTEGER_REPAIR / FAIL_NOVELTY_VS_REAL_BASELINE
STATE_UPDATE: YES

## Primary claim and cheapest falsifier
B020 proposed checking 64-bit torus canonical lifts only at nonlinear boundaries. B021 tests ONE precise claim: can two successive q64 torus additions with an unobserved intermediate be replaced by a single Goldilocks field equation and ONE aggregate quotient using B018's one-bit parity, so no full intermediate canonical range/carry check is required? Falsify first with a nonzero even multiple of Goldilocks p as a false output.

## Original and related sources
[FACT; SOURCE CODE INSPECTED] HasteBoots, Liu et al., USENIX Security 2026, official https://www.usenix.org/conference/usenixsecurity26/presentation/liu-fengrun; authors' public repository https://github.com/f7ed/HasteBoots, DEFAULT BRANCH UNPINNED on 2026-10-19:
* vfhe/src/bfhe/parameters.rs lines 25–42: ZAMA_GOLDILOCKS_PARAMETERS ring_modulus=Goldilocks::MODULUS_VALUE, N=1024, gadget basis bits=5. This implementation uses FHE OVER THE NATIVE PROOF FIELD; it does NOT pay the hypothesized q64-to-Goldilocks conversion every addition.
* trace/src/acc_trace.rs lines ~159–201: input_acc_permuted obtained by transforming output_acc and boundary rows; lines 225–269 num_oracles and pack_to_vec include ONLY input_acc and monomial_times_acc, while external_product_input=monomial_times_acc−input_acc and output_acc=input_acc+sum_prod are DERIVED, not independently committed. Source ALREADY exploits linear-derived witness reuse and compact multilinear trace.
* snarks/src/fhe_op/blind_rotation.rs includes exact staged external product, NTT, decomposition, accumulator-iteration proof; rounding/decomposition creates NONLINEAR boundaries requiring proper range/lookup constraints. Do not claim HasteBoots already offers q64 limb sharing; it does not.
[FACT; CLEAR PRIOR ART] arkworks-rs/nonnative https://github.com/arkworks-rs/nonnative explicitly postpones costly modular reduction using mul_without_reduce, adding unreduced intermediates before one reduction. gnark nonnative emulation https://pkg.go.dev/github.com/consensys/gnark/std/math/emulated likewise supports bounded deferred reductions until limb overflow. Thus generic lazy reduction NOT novel.
[OTHER] Zama CCS2025 verifiable TFHE (Tremblay Thibault & Walter, DOI 10.1145/3719027.3765097) modifies proof-friendly modulus and uses recursion; PDF full algorithm unavailable here, so avoid unsupported detailed claims.
[QUALITY] BOOT GitHub Notes read_repo_file returned bare {} in this session, but last B020 and B021 identity were recovered from recent conversation and notes listings. This round does not read full current accepted HasteBoots PDF; original GitHub source code is the key evidence. No native cryptographic/prover experiment, no real security/DFR/PCS-cost measurement.

## One-step functional fusion (conditionally true)
For x,a,b,z canonical integers in [0,q), q=2^64 and y=(x+a) modq, z=(y+b) modq, where intermediate y is neither output, queried nor input to nonlinear operations, the exact combined relation is x+a+b=z+Kq, K=floor((x+a+b)/q) in {0,1,2}. This algebraically removes y and its canonical range witness from a stand-alone integer circuit. Input and output canonical lifts still need to be committed/bound to the same public ciphertext statement.

## Explicit devastating one-parity soundness counterexample
Take q=256, Goldilocks-scaled odd p=251, x=a=b=250, proposed z=248, K=0. Let e=x+a+b−z−Kq=502=2p. Then both field equality e=0(modp) and parity e=0(mod2) PASS with ALL x,a,b,z and K in valid ranges, although true (x+a+b) modq =238 not248. q64 counterpart: q=2^64,p=q−2^32+1, x=a=b=ceil(2p/3), z=3x−2p∈{0,1,2},K=0 gives e=2p and similarly wrong torus sum. Thus B018's parity lemma depended on TIGHT narrow gadget remainder bounds and cannot be blindly transferred to a wider fused linear trace.

## Structural repair: two-bit checksum is sufficient
Let e=x+a+b−z−Kq with x,a,b,z∈[0,q) and K∈{0,1,2}. Then −3q<e<3q, and since p=q−2^32+1 and q=2^64, 3q<4p. If e=0(modp) and e=0(mod4), since p odd and gcd(p,4)=1, e must be a multiple of 4p; boundedness forces e=0 in Z. Because q divisible by4, verifying e mod4 is equivalent to verifying low-two-bit equality x+a+b−z=0 mod4 using the SAME canonically bound integer limbs (not uncommitted, independent low-bit witnesses). K is a single ternary aggregate carry/range witness. This conditional theorem proves exact two-addition integer semantics, not the soundness/cost of a complete PIOP or SNARK.
Generalization: a chain of m canonical unsigned q values yields |e|<(m+1)q when K∈{0,...,m}; any 2^s with 2^s p>(m+1)q and a sound e=0(mod2^s) plus e=0(modp) certifies e=0. This is classical coprime CRT with an integer magnitude bound, not an original number theoretic theorem. No lower bound or optimality of s is claimed.

## Exact independent computation
Use scaled q=256,p=251, K∈{0,1,2} and enumerate by triangular/convolution counts of all 256^3=16,777,216 input triples (x,a,b). For sum S=x+a+b and each possible alias m∈{-3,-2,-1,0,1,2,3}, solve z=S−Kq−mp and count 0<=z<q with multiplicity. Counts by m:
m=-3:680, -2:3,171,656, -1:14,173,091, 0:16,777,216, +1:14,110,090, +2:3,101,200, +3:455.
field-only accepted 51,334,388 witness tuples, of which 34,557,172 are wrong.
field + ONE parity bit accepted 23,050,072, of which 6,272,856 are wrong (even ±2p aliases).
field + TWO low bits accepted 16,777,216, all correct (0 false).
Full q64: 100,000 independent pseudorandom canonical triples and aggregate K checked exact integer, field, mod4, K bounds: 100,000/100,000 honest PASS. Explicit forged q64 example e=2p accepted modp/mod2 and rejected mod4. All calculations use exact integer arithmetic, not FHE/SNARK code.

## Whole-system and novelty gate
[DERIVATION] Stand-alone q64 circuit with NO observed/nonlinear intermediate could eliminate one intermediate canonical q64 range + one local carry check, replacing two q-addition transitions with one ternary K and mod4 check (assuming inputs/endpoints canonically committed). Actual constraint counts/proof costs are UNKNOWN, and an optimized nonnative compiler may already do this. If intermediate feeds nonlinear digit D(y), its canonical q-ring meaning is necessary; cannot simply eliminate that boundary. Across a general PBS, each GSW decomposition is a real nonlinear boundary; the hoped-for arbitrarily long linear run may not exist.
[FACT] HasteBoots (current implementation) uses native Goldilocks ring and already leaves certain linearly-derived accumulators uncommitted. There is NO sourced reduction in its actual carry/range count by introducing our construction. Lazy reduction is public standard prior art. Therefore no publishable novelty or secure/proven performance gain here.
[DECISION] PARK generic q64 carry deferral/Goldilocks checksum scheme as an independent paper direction. Keep B018/B019 lemmas as conditional math, but avoid further low-value parity tweak loops.

## Concrete next hypothesis (not executed)
NEXT_TEST B022: HasteBoots batch blind rotation publicly marks its trace commitment DUPLICATED with the decomposition argument. Paths snarks/src/fhe_batch_op/batch_blind_rotation.rs (~210–215,~455–465) and snarks/src/fhe_op/decomposition.rs (~140–150,196–200) each perform PCS::commit and open on related data. Test ONE exact claim: can ONE canonical commitment and sound MLE-index mapping serve both subproofs and save real PCS work without mixed-oracle/same-witness soundness problems? First read original polynomial generation shapes, evaluation points and challenge order; build a minimum equal-array/different-layout witness counterexample and a cost ledger. Duplicated code may be intentional (different padding/permutation/layout), so DO NOT assert actual savings before proof. Unlike B021 this is a specific source-level inefficiency candidate. BOOT-only.
END: STATUS PASS_CONDITIONAL_LINEAR_FUSION/FAIL_ONE_PARITY/PASS_MOD4_REPAIR/FAIL_NOVEL_CURRENT_BASELINE; NEXT_TEST B022; STATE_UPDATE YES.
