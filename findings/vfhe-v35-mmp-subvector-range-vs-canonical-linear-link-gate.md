# vFHE V35 — Published one-vector ZK range proof does not directly open native canonical-lifted MLE weights

Date 2026-10-15 Asia/Tokyo. Human PI authorized continue. Independent V35; global general I192 FROZEN, independent SHIP I226 unchanged. Read-before-write START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, STATE.md (V34 done/V35 next), findings/vfhe-cross-crt-state.md and V34 failure. One hypothesis, one minimal source-shaped exact test.

## H-V35: one primary falsifiable assertion

The ORIGINAL unmodified AoKagg method, published in Yang et al. ePrint2024/827 Section4 on ONE Pedersen subvector commitment, both (A) aggregates a range proof of all beta4 digits of a common vector a AND (B) DIRECTLY proves any native vFHE F.2 public-y/canonical-integer-lift weighted vector functional, including the cross-prime quotient checks, without needing a distinct generalized IPA/VC protocol.

Falsifier: Compare the exact supported AoKagg coefficient family to an explicit source-form native full-extension MLE challenge's canonically lifted Fp basis weights. A legal row outside that family kills direct AoKagg composition, regardless of its sound published range-proof performance.

## Actual original sources [FACT]

- Xiao Yang, Chengru Zhang, Mark Ryan, Gao Meng, Multivariate Multi-Polynomial Commitment and its Applications, ePrint 2024/827, https://eprint.iacr.org/2024/827, full original Research MCP 40 physical pages, PDF SHA256 ae0baa1357ef38a40e8203b291162818a423a157940cc182264a22d954ae887e, mirror source revision f36846bd4bd55a8434eb0b07c56060b7e8a83376, VERSION_UNVERIFIED relative to official. Source pp19–22 Section4, Fig6, Table1: ONE Pedersen subvector commitment c_v=product_j g_j^(v_j) g^omega, plus batched ZK range protocol for v_j in [0,2^l-1]. AoKagg authenticates a geometric aggregation sum_(j in S) z^(sigma(j)+1)*v_j, with its original pairing and Schnorr protocol. It is NOT stated to authenticate an arbitrary public coefficient vector chosen independently of z. Proof sizes and arithmetic operation counts at physical p22 Table1 used verbatim below.
- Cascudo et al. Verifiable Computation for Approximate Homomorphic Encryption Schemes, CRYPTO2025, ePrint 2025/286, https://eprint.iacr.org/2025/286; complete 52pp original Research MCP mirror PDF SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19, VERSION_UNVERIFIED vs revised source. Section3.1 p10 RNS native extension fields; Section4.3 pp20–23 ring digit scalar lookup; Appendix F.1/F.2 p50–51 independent native Merkle/RS polynomial commitments with publicly authenticated field evaluation y. The proposed external CP must prove that the SAME precommitted a has canonical integer coordinate weighted sums equal to the publicly authenticated native y plus p_i times bounded integer quotients.
- V31/32 provided conditional one-representative link theorem and an insecure but executable precommitted-a Pedersen/Schnorr+native-F.2 toy. V33 showed stock aggregated Bulletproofs range proof STILL needs H public value commitments; V34 showed late-selected postchallenge a is insufficient. We do not question the original papers' claimed correct functionality.

## Source-shaped exact test [DERIVATION + EXECUTED]

Pick valid N4,d2,prime p13=1+4*3, beta4, ellstar3, H8; irreducible u^2-5 over F13. Full extension native r=(2+u,3+2u,4+3u). Lexicographic b from 000 through 111. Direct F13^2 multiplication gives 8 canonical Boolean MLE weights chi_b(r):

(8,4), (4,0), (10,2), (3,6), (2,8), (10,12), (3,9), (0,11).

The two canonical integer Fp-coordinate rows are c0=(8,4,10,3,2,10,3,0) and c1=(4,0,2,6,8,12,9,11). Any geometric functional even with common scalar, c_j=gamma*z^(j+1), satisfies c[0]*c[2]=c[1]^2 in an external prime-order proof field (e.g. F1009). But coordinate0: 8*10=80 !=4^2=16, coordinate1: 4*2=8 !=0^2=0. Both rows lie OUTSIDE the unmodified full-index AoKagg geometrically weighted family. Hence no *direct* AoKagg call can certify the needed arbitrary original-native MLE coordinate functional with that exact method. Does NOT prove a generalized arbitrary-linear IPA impossible, or reject multiple proof calls, modified encodings or other VCs.

Honest cross-characteristic equation sanity: a=(0,1,2,3,0,1,2,3), literal integer sums S=(49,85), actual native evaluated y=(10,7) and quotient k=(3,6); S=y+13*k exactly. So original proposed quotient relation IS satisfiable, but its coefficient row cannot be passed unchanged as a published AoKagg z-power aggregation.

EXACT runnable Python standard-library finite field checker /mnt/data/vfhe_v35_mmp_aokagg_geometric_link_gate.py SHA256 b2a227cf27bbf1ea8e48ec41117f1a9c731c0eebd4985ab571cf209591d70b70. Exact JSON /mnt/data/vfhe_v35_mmp_aokagg_geometric_gate_results.json SHA256 329eb0fb92ac84299a9c40cae91b76ae5faab689289adbf17da267e34a17c1c9. Both files ACTUALLY CREATED and script EXECUTED. No source cryptographic pairing proof nor end-to-end SNARK/F.2 run.

## Concrete published symbolic range-proof costs [DERIVATION not benchmark]

At H=n=2^24=16,777,216 digits, l=2 bits per digit, log2(n*l)=25: one Pedersen subvector commitment c_v and ZKRP optimized range proof body (2log(nl)+7)G+(9+2log(nl))Zp = 57 group +59 scalar objects, 3712 bytes if all 32B. Source Table1 prover symbolic group work (10*n*l+4log(nl)+2n+13)G =369,098,865 group operations. Optimized verifier (8log(nl)+n+11)G+3P =16,777,427 group operations +3 pairings. Indexed SRS/commitment creation costs NOT INCLUDED, and this is NOT proof all large-scale instances are implementable at acceptable parameters. Even if range worked with one commitment, missing two primes x d4 =8 weighted canonical-quotient equalities, 8H=134,217,728 linear coefficient terms by dense direct algorithm (not necessarily multiplication gates).

## Conclusion and next gate

STATUS FAIL H-V35: unmodified published AoKagg range protocol does not DIRECTLY prove arbitrary vFHE canonical-lifted native MLE functional nor quotient link. PASS identified an EXISTING single-vector prechallenge ZK range argument (so V33 per-digit Pedersen commitments need not be intrinsic to the range task), verified nongeometric weight counterexample and source Table1 symbolic cost. UNCLEAR robust 128-bit pairing security, setup footprint, practical prover time, full source F.2 integration, other VC/IPA generalized linear openings, ZK/Fiat-Shamir cross-transcript composition and publishability. NOVELTY NOT VERIFIED.

NEXT_ACTION V36 ONLY if PI continues: source-audit a PUBLISHED arbitrary-linear-functional proof using the SAME single-vector commitment, prebound before native F.2 r; test one concrete canonical-lift row and entire quotient y relation, include setup/prover/verifier work and possibility of no-wrap. If unavailable or cost uncompetitive, HUMAN_REVIEW/PARK this class rather than stack more toy range proofs.

STATE_UPDATE YES independent V35 finding/state pointer only; global I192 FROZEN, SHIP I226 and all other branches unchanged.