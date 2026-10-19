# BOOT-B019 — One-parity lookup integration for approximate gadget: shared-witness/cost gate

TRACK_ID: BOOT
ITERATION: B019
DATE: 2026-10-19
STATUS: FAIL_FREE_INTEGRATION_INTO_EXISTING_HASTEBOOTS / PASS_PARITY_FOLDED_RANGE_REPAIR / PASS_EXACT_MIXED_WITNESS_FALSIFIER / UNCLEAR_GLOBAL_PROOF_VALUE
STATE_UPDATE: YES

## Exactly one primary hypothesis
Does HasteBoots' EXISTING LogUp gadget decomposition range proof ALREADY contain enough bounded remainder bits and common commitment to verify B018's q=2^64 approximate gadget parity/integer-lift almost for free, without significant new range/PCS witness? Cheapest decisive test: inspect exact source trace/commitment schedule; construct a one-coefficient complete witness layout; falsify weak independent parity binding with a concrete field-valid integer-invalid witness and count required 5-bit range elements.

## Prior-work source provenance and limitations
[FACT] HasteBoots, Liu–Liang–Xie–Yu–Zheng–Hu, USENIX Security 2026, official landing page https://www.usenix.org/conference/usenixsecurity26/presentation/liu-fengrun . HasteBoots official research artifact https://github.com/f7ed/HasteBoots, files:
 - README.md: explicitly states exact *full* gadget decomposition; to match Zama baseline uses B=2^5, ell=13 rather than approximate version. Current implementation does not provide a public preexisting 41-bit approximate remainder proof.
 - snarks/src/fhe_op/external_product.rs lines 1–6: external product verification uses SumHadamardTraceMLE, NTTMatrixEvalPIOP, LogUpPIOP for gadget decomposition.
 - same file lines 218–244: PCS::commit to trace oracle BEFORE Fiat–Shamir lookup challenge; extract_lookup_trace_mle_small_table(params.basis) from committed trace; LogUp witness; separate helper PCS commitment.
 - lines ~251–289: batch Hadamard and lookup into shared sumcheck; lines ~291–352 and 384–505: challenge openings and PCS batch verification. Thus trace-derived lookup columns can be mutually bound *if* the new remainder/parity relation is inserted into this committed trace and actually checked; adding independent parity oracle is unsafe.
 - trace/src/lookup_trace/small_table.rs lines ~93–115,151–180: small-table lookup checks input field values are in {0,..,range−1}, and maintains occurrence multiplicities; it does not by itself reveal or bind an LSB/parity of an input field element in a separate equality constraint.
 - vfhe/examples/zk_nand_op/zk_lookup.rs uses params.blind_rotation_basis().bits() to select lookup table size.
Repository default branch read via linked GitHub connector; commit hash NOT pinned, no code modifications or native benchmark.
[FACT] Tremblay Thibault–Walter, "Towards Verifiable FHE in Practice", CCS 2025, DOI 10.1145/3719027.3765097, general approximate-gadget TFHE SNARK already published; original authors' https://www.zama.org/post/verifiable-fhe-bootstrapping-using-snarks describes changed ciphertext modulus to Plonky2-native Goldilocks rather than mechanically proving the original 2^64 torus. Its exact per-coefficient proof arithmetic and range layout not recovered in this iteration. TFHEprus https://github.com/virtualsecureplatform/TFHEprus already describes approximate gadget bounded reconstruction/range PoC. Do not claim first approx gadget proof.
[FACT] Guimarães–Pereira 2025/686 PDF phys p23 Table3/source polynomial_decompose_i as in B018: q=2^64, FBS1 B=2^23 G=2^41, FBS2 B=2^22 G=2^42; one-level centered rounding. B018 proof: x−Gd−r−qw=0(mod Goldilocks p) plus correctly bounded *same integers* and parity x≡r mod2 implies exact integer equality. No need to repro B018 theorem.

## Concrete bounded witness layout and model-relative costs
Let d'=d+B/2 ∈[0,B), r'=r+G/2∈[0,G), w∈{0,1}, x∈[0,2^64). Their field relation is:
  x−Gd'−r'−q w+(q+G)/2=0 modp .
For a HasteBoots-like lookup table with 5-bit input digits, one simple explicit decomposition proof requires:
 - 23-bit d' -> ceil(23/5)=5 lookup limbs (FBS2 22 bits also five);
 - 41-bit r' -> ceil(41/5)=9 lookup limbs (FBS2 42 bits also nine);
 - w -> one Boolean lookup/check;
 - if x must be a NEW private canonical 64-bit torus lift -> ceil(64/5)=13 further lookup limbs, unless the exact x word/limbs are already public or committed and soundly linked to previous stages.
Hence ~15 small lookup/check objects when x is already canonical-bound, ~28 objects when private x also needs new limb range proof. This is a PARTICULAR natural small-limb layout, not an information-theoretic lower bound on proof costs, not a calibrated PCS/sumcheck runtime benchmark, and is not fully apples-to-apples with the native-field original HasteBoots exact-ell=13 gadget.

## Decisive concrete mixed-witness attack
At scaled q=256,p=251,B=G=16, adversarially supply for the FIELD subproof:
  x=0,d=0,r_field=−5,w=1.
Then e=x−Gd−r_field−qw=−251 ≡0 mod251, all four integer ranges hold, but e ≠0 in Z.
If a separate PARITY subproof uses an UNBOUND r_parity=−4, it accepts x≡r_parity mod2 (both even), so both independent proofs pass although the claimed integer gadget relation is false. The single-committed-witness parity of r_field=−5 correctly rejects (odd versus even).
Furthermore Goldilocks public input represented ONLY as one field element is not enough to identify canonical 64-bit torus x, because p<q and x and x+p can both be canonical; e.g. scaled x=0 and x=251 have same mod251 image but distinct actual gadget residues. A q64 TORUS-INPUT BINDING is necessary; a field-value range check x<q alone is insufficient to distinguish these two lifts. If x is public to verifier as 64-bit bytes, that can anchor it; if x is intermediate, a shared torus-limb commitment or different sound lift mechanism is needed.

## Positive structural repair: parity folded into already-needed lowest-limb lookup
[DERIVATION] Because G/2 is even (b22/23), r and r' have the same parity. If the canonical x low bit b=x mod2 is already PUBLIC/TRUSTED, instead of a conventional 5-bit r'_0∈[0,32) lookup, use:
    r'_0=2u+b, u∈[0,16).
A 4-bit range lookup of u can REPLACE (not supplement) the old 5-bit low-limb lookup of r', provided the integer/field reconstruction of r' from the same committed limbs is soundly checked. Thus the PARITY CHECK itself adds no additional lookup COLUMN in this proposed trace layout and may even use a smaller table. It does not make the *new 41-bit remainder* or torus-input lifting free.
If x is private but canonically decomposed and already committed, write x_0=2v+b and r'_0=2u+b, with u,v∈[0,16) and common Boolean b. This uses two 4-bit range lookups plus a common Boolean check, compared with two independent 5-bit range lookups, potentially modest overhead depending lookup batching and PCS; the same b must be bound into BOTH reconstructions and upstream ciphertext commitments.
[EXHAUSTIVE TOY] With q=256,p=251,B=G=16, radix-4 low-limb layout r'=4h+2u+b where h∈{0,1,2,3}, u∈{0,1}, b=x mod2, enumerate all 256 x×16 shifted digits×4 h×2 u×2 w =65,536 candidate tuples (remainder half space due parity). Among field-valid tuples exactly 256 pass, each with e=0; ZERO false integer lifts. Counterexample above passes unbound-r versions, proving shared-witness necessity.
[REFERENCE] Previously B018 enumerated 131,072 arbitrary bounded (x,d,r,w), finding 266 extra field-only false tuples, all removed by correctly bound parity.

## Critical incomplete links: VFHE lesson
The CONDITIONAL low-limb optimization DOES NOT establish that HasteBoots's existing PCS/LogUp implementation already has an r' trace: it has only exact gadget digits. Need redesign and commit trace for d',r',w,x lift before lookup FS randomness; verify (a) reconstruction in same committed oracle, (b) parity public/shared b from same trace, (c) full torus input/output binding across every step, (d) exact bounds/tie handling, (e) updated NTT/Hadamard trace and source FHE correctness, (f) LWE/RLWE sparse-secret security/DFR and the entire FHE statement. If the trace stores only field x modp, two unsigned torus lifts may be indistinguishable even when the decomposition relation is internally valid. Reusing PCS commitment structure is not equivalent to actual construction or security proof.
Prior-art gate: existing Zama TFHE CCS25 already proves approximate gadget; HasteBoots exact current repo. One-parity lemma may or may not be new; no claims of publishable performance until measured witness/commitment/lookup costs and soundness across the bootstrapping trace.

## Decision
PRIMARY STATUS: FAIL claim of NEAR-ZERO TOTAL MARGINAL COST when attaching approximate gadget to EXISTING HasteBoots: it lacks remainder x-bound witness. PARTIAL PASS: conditional parity check can replace an existing low-limb range lookup, preserving exact integer soundness when all integer bounds and common commitments are already in place. Complete source-grounded proof/benchmark still UNCLEAR, not a finished cryptographic scheme.
NECESSARY_CONSTRAINTS: exact source q64 rounding, signed-canonical digit/remainder/carry, upstream canonical 64-bit input binding, common witness commitments, lookup reconstruction, FS challenge ordering, integral not only field correctness, full security/DFR, cost measured against exact HasteBoots and CCS25 approximate proof.
REPAIR_SEARCH: discovered zero-extra-lookup parity folding (conditional), explicit mixed-witness forgery, and a new source-derived representational obstacle q64>p_gold. Do not archive B018 lemma as incorrect, do not assert zero overall prover overhead.
NEXT_TEST B020: One falsifiable new structural hypothesis inspired by VFHE: because p_gold<q64<2p_gold and p_gold is odd, can a committed Goldilocks field element z together with ONE canonically bound parity bit b provide a UNIQUE torus q64 lift x∈[0,q), eliminating redundant 64-bit limb-range proof across bootstrapping trace transitions? First derive exact two-lift representation, boundary legality and mixed-witness attack; test whether one-step q64 addition/negacyclic transform preserves compact representation without rebuilding all 64-bit limbs or imposing a 32-bit boundary check. Check recent compact nonnative/lookup prior art and choose source-compatible microbenchmark only if the closure/cost gate survives.
END: STATUS FAIL_FREE_EXISTING_LOOKUP / PASS_CONDITIONAL_PARITY_FOLD / FULL_PROTOCOL_UNCLEAR; STATE_UPDATE YES; BOOT files only.
