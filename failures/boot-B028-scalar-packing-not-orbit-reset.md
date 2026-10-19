# BOOT B028 FAILURE — Published scalar Packing KS does not reset a list of orbit-mask RLWE states

TRACK_ID: BOOT
ITERATION: B028
DATE: 2026-10-19
STATUS: FAIL_DIRECT_PACKING_KS_RESET / FAIL_SIMPLE_PERIODIC_PER_CT_RESET
STATE_UPDATE: YES

Target: repair B027 key-switch-free automorphism rank-2 orbit-mask MPmul by amortized packing key switching across n intermediate monomial RLWE states at each repeated MPmul boundary.

SOURCE TYPE: ePrint 2025/686 Section5 Algorithm5 inputs n SCALAR LWE ciphertexts, outputs ONE RLWE encryption of SUM m_i X^i; Algorithm1 and code src/sparse_amortized_bootstrap.c (blob b86d4d7f8f578665196a94dd6a2c9ca155f8bde7 lines227–245) NEXT MPmul requires n INDIVIDUALLY addressable RLWE encryptions of X^{u_i}. Author implementation runs end-stage trlwe_extract_tlwe(...,0) on each output only after complete SAB and trlwe_full_packing_keyswitch to assemble ONE RLWE (lines359–391), not reset MPmul states mid-loop. Their sparse Packing KS variant is explicitly described as theoretical but currently limited practically by increased multiplications (paper p19).

ZERO-NOISE INVERSION COUNTEREXAMPLE: ring R=Z_q[X]/(X^4+1), natural "pack 2 ring monomial ciphertext messages" P(m0,m1)=m0+X*m1. Inputs (1,X) and (X²,X^7) produce identical 1+X² because X^8=1, yet require distinct next-stage MPmul outputs. Exhaustive all monomial pairs exponent u0,u1 in Z8 gives 64 inputs but only 33 images (31 collisions); N8 256 inputs/129 images (127 collisions). The original scalar-input Packing KS does NOT suffer this problem: it packs scalar messages, not ring elements. An alternative larger tensor ring might store them separately but is not Alg5 and requires new end-to-end format/security/cost analysis.

ALTERNATIVE NAIVE REPAIR FAIL: Extracting one scalar coefficient per RLWE input loses encrypted exponent (X vs X² both coefficient0=0). Extracting all N coefficients of n RLWE intermediates produces nN scalar LWE samples. One output coefficient-encoded packed RLWE would need N'≥nN; n=N2048 yields 4,194,304 slots, ×2048 degree vs native, with huge keys/unpacking; this is NOT a universal compression lower bound for monomial-specific nonlinear encodings.

CHECKPOINT COST: B1-source-compatible n=N2048,h39,B128,L7,M40 MPmul. Original uses M(B−1)=5080 automorphism KSK. B027 pessimistic dense-support propagation t_next=min(n,t+2^i), reset after t full MPmuls. Exact integer recurrence:
period1 9880 dual CMUX +4953 KSK boundary => saves only127 original KSK;
period2 27660 +4826 => saves254;
period4 63220+4572 => saves508;
period8 134340+4064 => saves1016;
period40(no reset) 454658+0 => saves5080.
At +2 ring products/dual CMUX B027 abstract cost, break-even KS would have to exceed 155.6 products with t1 or 179.0 products with no reset, even ignoring extra FFT/memory/noise. This is a proxy for full dense intermediate RLWE states, not native timings or worst-case impossibility theorem. B027 earlier n512 illustrative no-reset135342 duals; source n2048 worsens to454658, don't confuse.

CONCLUSION: No actual cheap source-compatible batched orbit->single-mask conversion found; published Packing KS input/output does not match, and simple boundary checkpoint buys little. B027 local orbit automorphism algebra remains mathematically valid but currently noncompetitive for complete MPmul/SAB. Distinct specialized scheme might exploit ciphertext correlations, but requires substantial new packed layout and full noise/security proof, not just Alg5 invocation.

DETAILS & ORIGINAL EVIDENCE: findings/boot-B028-orbit-mask-batch-reset-packing-type-and-cost-gate.md, including author code SHAs and exact enumeration.
NEXT B029: remain BOOT Priority1 but exit orbit-mask subbranch. Seek source-specific new structural computation around scale-based Mat-MGSW rounding/noise and amortized MPmul dataflow with hetero gadget performance from 2025/1711, 2025/1892 and 2025/686, not a trivial gadget replacement. Ask PI HUMAN_REVIEW only after appropriate stagnation analysis; no automatic topic switch. BOOT-only.
