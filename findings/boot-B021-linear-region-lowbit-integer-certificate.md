# BOOT B021 — Shared torus-lift certificate across two linear steps: modulus-alias gate and 2-adic repair

TRACK_ID: BOOT
ITERATION: B021
DATE: 2026-10-19
STATUS: FAIL_ONE_PARITY_BATCH_CERTIFICATE / PASS_TWO_BIT_LINK_REPAIR / FAIL_DIRECT_HASTEBOOTS_COST_CLAIM / NOVELTY_UNCLEAR_LOW
STATE_UPDATE: YES

## One primary falsifiable hypothesis
[HYPOTHESIS] Given *the same committed canonical unsigned torus integers* x,a,b,y in [0,q), and one bounded aggregate carry k∈{0,1,2}, can two successive q=2^64 linear additions be verified by ONE equation over Goldilocks p=q−2^32+1 PLUS the existing B018 single parity check, avoiding intermediate canonical torus range/carry checks?
[CHEAPEST KILL TEST] Substitute the source-compatible aggregated integer residual e=x+a+b−y−kq, bound its absolute value, find a legal e=2p forged pair. If falsified, check whether a small low-bit integer checksum yields a source-faithful repair and what its real cost/source novelty is. Exactly ONE main aggregate-check hypothesis and a minimal correction, not a new full protocol.

## Source/provenance (read before write)
[FACT; exact connected GitHub source] HasteBoots official f7ed/HasteBoots default-branch source, source versions represented by file blob SHAs (not an immutable repository commit):
- vfhe/src/bfhe/parameters.rs blob e5a34e76bcecce573ca2247cc7cdbcc114a6a062, rows 30–85: ZAMA_GOLDILOCKS_PARAMETERS and GOLDILOCKS_BINARY_128_BITS_PARAMETERS use **Goldilocks itself as the ciphertext ring modulus**. Thus there is NO native 2^64 torus carried between stages and no 2^64 carry-range overhead to remove in that system. The earlier attempt to compare q64 carry amortization against HasteBoots directly is the wrong baseline.
- trace/src/acc_trace.rs blob 70f947fd9f685dc114f68be7b95e0e186407bf88, rows 17–50: input_acc, output_acc, initial_acc, final_acc, a row-permutation link across rounds, monomial_times_acc, and external_product_input; it explicitly notes external_product_input can be omitted in practice.
- snarks/src/fhe_op/acc_iteration.rs blob 4d54fed94858cd144ec885826075be1bc7250132, rows 150–184: batched permutation plus indexed LogUp verifies equality of each round's input accumulator with previous output, and endpoints.
- snarks/src/fhe_op/blind_rotation.rs blob 40ff364a68fde34e46b6430725a91effae38e733, rows 239–292: commits entire packed trace BEFORE sampling Fiat–Shamir challenges, batches Hadamard instances into one sumcheck.
- snarks/src/fhe_op/decomposition.rs blob 1964d4632e6be93a7eaf3f3710d83632ade10e78, rows 139–175: separate decompositions use their own oracle commitment and indexed range lookups; logs note duplication of some oracle commitments. This does not imply a lack of any currently implemented trace sharing.
Public final HasteBoots paper USENIX Security 2026 official https://www.usenix.org/conference/usenixsecurity26/presentation/liu-fengrun; source claims sec-scale proving and batched 16 operations. The full official PDF was not visually inspected in this B021 source pass; GitHub code statements and official webpage suffice for the particular type/dataflow facts. The GitHub default branch may change; pin actual repository commit before implementation/benchmark.
[PRIOR ART] Tremblay Thibault–Walter CCS 2025 DOI 10.1145/3719027.3765097 already adapts TFHE for proof-native field/modulus and uses recursive proof trace; ordinary canonical carry certificates and integer-linear-region folding are standard arithmetic circuit techniques. No firstness or novelty claimed.

## Mathematical falsifier at real source q
Let q=2^64, D=2^32−1, p=q−D (an odd prime).
A canonical two-step torus chain is:
  u=(x+a) mod q,  y=(u+b) mod q.
If the intermediate u is NOT externally observed/consumed, these operations can be algebraically fused to the exact integer relation:
  x+a+b=y+kq, with 0<=x,a,b,y<q, k∈{0,1,2}.
Set e=x+a+b−y−kq. From the ranges:
  −3q<e<3q<4p.
A proposed one-field/one-parity proof checks e≡0(modp), e≡0(mod2). But choose x=a=p, b=0, y=0, k=0. All witnesses canonical and bound-consistent, field e=2p=0(modp), parity e=0(mod2), while actual output is y_true=2p modq=q−2D ≠0. No mixed-witness issue; it exploits even prime multiple newly admitted by the wider aggregate error interval. Thus reusing the B018 one-bit parity lemma outside its original narrower bound is WRONG.

## Minimal positive repair, and general lemma
[DERIVATION] Require ONE additional low bit, namely:
   e ≡0 (mod p) and e≡0 (mod 4),
with all canonical integer ranges and same-witness binding as above. Since p is odd and gcd(p,4)=1, e=tp where t≡0(mod4); |e|<4p forces t=0, so e=0 in Z and the genuine two-addition modulo-q relation follows. As 4|q, the low-bit check simplifies to x+a+b≡y (mod4); k does not enter this low-bit equation. This does not prove the 2bit check has zero SNARK cost: low bits must be extracted from the SAME canonically bound integers, and the quotient/carry bound k∈{0,1,2} is necessary.

[GENERALIZED DERIVATION] For m successive additions of m+1 canonical unsigned q-words x_0..x_m, claimed final y∈[0,q), and k∈{0,..,m}, define e=sum_i x_i−y−kq. Then |e|<(m+1)q. If p is odd and t≥1 with 2^t p>(m+1)q, the pair of checks e≡0(mod p) and e≡0(mod 2^t) guarantees e=0, because e must be a multiple of lcm(p,2^t)=2^t p while lying in the open bound. For Goldilocks q/p≈1, the checksum needs Θ(log m) low bits. It cannot remain the single parity bit from B018 as m grows. This is elementary CRT/size-bound arithmetic, not a new cryptographic theorem or proof system.

## Cheap decisive independent exact reference verification
[EXHAUSTIVE] Use small q=16, odd prime p=13, two additions m=2. Exhaustively enumerate 16^4 * 3=196,608 tuples (x,a,b,y,k), with each word in 0..15 and k∈{0,1,2}. Counts:
   4,096 true exact integer witnesses (exactly one y,k for each x,a,b);
   11,036 additional WRONG witnesses satisfy field condition e%13=0;
   3,336 additional WRONG witnesses satisfy field AND single parity e%2=0;
   ZERO additional WRONG witnesses satisfy field AND two-bit condition e%4=0.
This exhaustively falsifies 1bit certificate and validates 2bit certificate in toy configuration; the general theorem is the source of full-size soundness.
[FULL q64 random/boundary] Independently evaluated 200,000 pseudo-random triples of canonical uint64 x,a,b, true y=sum%q and k=sum//q; every honest witness passes exact integer equality, field, and mod4 checks. Exact q64 forged witness x=a=p, b=y=k=0 has e=2p and passes field+parity but fails mod4 (2p≡2 mod4). No native FHE/SNARK proof was generated, and RNG details are not a cryptographic security statement.

## Application/cost/source compatibility gate
[DERIVATION] In an adapted NONNATIVE-q64 verification circuit, folding a *maximal purely linear segment with no external intermediate consumers* may remove an intermediate canonical-lift witness; but a sound terminal certificate still must bind all input q-word representations, the final q-word, the aggregate k range, and t low-bit checks. If some intermediate u feeds a gadget decomposition/CMUX/branch/witness lookup or is externally committed as a public output, it cannot be discarded without checking its relationship to the shared trace. Endpoints-only checking then proves a different computation.
[FACT] HasteBoots itself already runs ciphertext arithmetic modulo Goldilocks p; it verifies accumulator round links with packed trace, batch sumcheck, and row permutation, and uses lookup at nonlinear boundaries. There is NO repeated q64 carry check baseline to beat. Moreover some intermediate external_product_input is already omitted/recomputed in the trace, demonstrating awareness of linear dataflow simplification. Therefore no justified comparative performance gain over HasteBoots from our q64 folding lemma.
[COST_LEDGER] A two-add boundary certificate needs one k in [0,2], 2bit checksum tied to canonical x,a,b,y, and one F_p polynomial relation; a stepwise circuit would use two Boolean carries, two native/non-native modular relations and an intermediate u bound when that u is not already reused. The exact count of range lookup columns, commitments and native mod-p reductions depends on the representation and optimizer; the above is NOT a proven time/memory saving. For large m the checksum is only logarithmic width, but all input q64 canonicality checks still exist. Source HasteBoots and CCS25 choose prime-field arithmetic and avoid the entire nonnative issue; any new q64-specific implementation requires full correctness/security/DFR re-evaluation.

## Repair synthesis and honest status
[REPAIR] Replace one-bit low-check by t-bit check sized to the EXACT aggregate error bound; commit to the same limbs for range and low-bit checks. This repairs modular aliasing for the terminal linear relation but does not add an actual full verifiable bootstrapping protocol.
[NOVELTY_GATE] LOW in existing proof-native field systems; simple CRT+linear folding is classical. Potential adapted q64 proof is speculative, not source-supported end-to-end.
[RESULT] FAIL B021 hypothesis that a single parity check can amortize proof of two q64 additions. PASS precise two-bit repair and general low-bit-vs-bound lemma, but NO native HasteBoots cost advantage. Under BOOT stagnation rule, stop repeatedly tweaking Goldilocks/parity/q64 constraints unless a new source-specific bottleneck and substantive efficiency improvement are identified. Retain B018's narrower local lemma as valid.
[NEXT_TEST B022] Pivot to a genuinely different, source-grounded BOOT problem rather than another generic modulus-check optimization. Primary candidate to test: in 2026 BatchBoot/2025/686 REAL source, identify a multi-stage repeated computation across native FHE PBS rounds that dominates end-to-end runtime but cannot be shared by existing BatchBoot FFT-hoisting, and propose ONE new algorithmic invariant or scheduling modification. Cheapest test should be a quantified operation/dataflow lower bound or a source-level performance profile, not another arbitrary primitive replacement. Search other contemporary techniques freely, and check strongest 2026 prior art. If no well-specified bottleneck, report UNCLEAR and HUMAN_REVIEW rather than invent new progress. BOOT-only writes.
END: STATUS FAIL_ONE_PARITY_BATCH_CERTIFICATE / PASS_TWO_BIT_LINK_REPAIR / FAIL_DIRECT_HASTEBOOTS_COST_CLAIM; STATE_UPDATE YES.
