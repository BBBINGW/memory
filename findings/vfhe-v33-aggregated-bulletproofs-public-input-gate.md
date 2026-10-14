# vFHE V33 Companion — Executed public-native-y / value-commitment weighted link and omitted-range counterexample

**2026-10-15. COMPANION to authoritative V33 main finding `findings/vfhe-v33-bulletproofs-aggregate-value-commitment-interface-gate.md`, NOT another numbered research iteration. Global I192 FROZEN.**

## Primary hypothesis and cheapest decisive test

**Companion subclaim [FAIL for total communication; same V33 parent]:** Replace V32's 2H individually bit-committed Pedersen values and 2H Schnorr-OR bitness proofs with H committed canonical digits V_j=g^a_j h^rho_j and ONE published aggregated Bulletproofs proof for all 0≤a_j<beta=4, while retaining F.2's already-authenticated PUBLIC native y and the same cross-characteristic integer quotient/Schnorr relation. Claim this produces O(log H) communication for the ENTIRE cross-CRT CP proof including its public commitments.

**Decisive source-API check [FACT]:** Bünz et al., *Bulletproofs: Short Proofs for Confidential Transactions and More*, IEEE S&P 2018, ePrint 2017/1066, inspected Research MCP 45pp GitHub mirror SHA256 c79f9c32d061c6814e57d1d4007958efed66923f0194497e8596aa3edd387a53, VERSION_UNVERIFIED. §4.3 physical p21 range proof statement relation (69) has PUBLIC **V∈G^m**, m Pedersen commitments, and verification Eq(72) uses a product of EVERY V_j. §6.1 physical p28 Table1 gives **2(log2(n)+log2(m))+4 group elements and 5 scalar elements** = 2log2(nm)+9 total elements, but only for the range-proof **payload**, excluding the m public value commitments. Published prover/verifier work is linear in nm. The IACR landing for 2017/1066 explicitly notes a revised correction of its Fiat–Shamir section; no stale-version theorem overclaim.

The source vFHE is Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, ePrint2025/286 52pp inspected GitHub mirror SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19, official Feb2026 pdf parity VERSION_UNVERIFIED; original Appendix F.2 physical p51 verifies PUBLIC native y after Merkle authentication of RS-coded MATRIX COLUMNS, with Enc(v')|Q=q1 Uhat|Q and y=<v',q2>. We keep that y as the CP public input. The candidate CP is OUR augmentation; source does not contain it.

## Concrete candidate algebra and exact witness-binding issue

Commit ONE global canonical digit vector a by individual VALUE commitments V_j=g^a_j h^rho_j for j<H (rather than 2H bit commitments). ONE published aggregated Bulletproofs range proof should prove openings a_j∈[0,4). Native per-RNS prime representative F_(p_i^d) polynomial evaluation y_i is publicly authenticated by ORIGINAL source F.2. In native basis t, canonical lifts satisfy an exact bounded integer relation:

    S_(i,t)=∑_j lift(c_(i,j,t)) a_j = lift(y_(i,t)) + p_i k_(i,t).

Commit quotient k_(i,t) with independent Pedersen K_(i,t). The CP prover provides a Schnorr h-only discrete-log proof for group relation

    W_(i,t)=(∏_j V_j^(lift(c_(i,j,t)))) / (g^(lift(y_(i,t))) K_(i,t)^p_i) ∈ <h>,

using the SAME V_j for ALL primes. Correctly extracted openings give equality mod group order r; proving 0≤S<r AND 0≤lift(y)+p_i*k<r via actual range constraints yields INTEGERS equality, avoiding accidental wrap. Both V_j and F.2 source polynomial commitments must be fixed before native challenge r_i and source sampled Q; the F.2 accepted PUBLIC y must be the exact CP public y, and Fiat–Shamir transcripts must be bound.

An independent "short vector commitment only" cannot be substituted for the public list V_j in original published aggregated BP verifier without an additional knowledge-sound vector-opening link. Verifier also needs ∏ V_j^c for Schnorr quotient equality; keeping only a Merkle digest or a third unrelated vector commitment reproduces V12 unlinked-witness weakness. This is a LIMITATION OF THIS DIRECT PUBLISHED API, not an impossibility theorem for alternate cryptographic vector commitments.

## One executable falsifier, NO actual Bulletproofs prover

The local script **reuses V32's real native F.2 toy implementation** (standard Python SHA256 Merkle roots over native RS full-column leaves, source testing/evaluation y and finite F_(p^2) arithmetic) and replaces 2H bit commitments with H Pedersen VALUE commitments. It executes Schnorr proofs for ALL weighted native base-coordinate equalities against the SAME V_j for p13 and p29. Legal source-form N4,d2,ellstar3,H8,beta4, p13=1+4·3 and p29=1+4·7. Honest a=(0,1,2,3,0,1,2,3) yields native F.2 verified y13=(10,0),y29=(10,13) and group Schnorr weighted equality PASS for both primes.

**CRITICAL explicit soundness test — omit global range:** Let ONE shared committed integer digit be 261 at index0, others0, violating a_0<4. Its honest native values are index0=1 mod13 and0 mod29. Query native F.2 at r=(0,0,0): original honest native Merkle/RS evaluations y13=(1,0),y29=(0,0) pass. The SINGLE shared value commitment V_0=Com(261) and weighted Schnorr quotient relation ALSO pass for both prime fields:
  p13: 261=1+13·20;
  p29: 261=0+29·9.
These exact integer equalities have S=261<insecure toy group order1009, so not an alias/wrap attack. An ACTUAL aggregate Bulletproofs range proof of [0,4) would have to reject this witness. Hence range proof binding to THESE VERY SAME V_j is essential, even if the weighted CP has perfect witness knowledge. **NO aggregated Bulletproofs proof is generated/verified in this script**; acceptance/rejection of BP relies on published protocol theorem, not fake simulated proof objects. Tiny multiplicative subgroup order1009 is cryptographically INSECURE, same as V32.

## Source-faithful proof traffic and native work count [EXACT MODEL, NOT BENCHMARK]

H=2^24=16,777,216 canonical digits, beta4 requires n2 bits/digit. Published aggregate BP proof alone: 2log2(nH)+9=59 elements, **1,888 bytes** with a uniform 32-byte group/scalar encoding. BUT published relation still takes H individual Pedersen V_j public inputs: **H*32=536,870,912 bytes=512 MiB**. Thus V_j + BP proof = **536,872,800 bytes**, before original F.2, CP quotient commitments and equality statements. Range-proof PAYLOAD is O(log H); overall CP public statement/transcript for this specific API is Θ(H), not O(log H).

V32 naive β4 baseline: 2H group bit commitments *32=1 GiB; 2H OR Sigma transcript items *192=6 GiB, 7 GiB total before quotients. Thus BP aggregation CAN save nearly all bit-OR proof bytes but retains 512 MiB committed digit vector input. BP proof generator arrays/verify multiexponentiation still scale in nH=2^25 bits; no actual runtime, 128bit security level, peak memory or optimized aggregation batch benchmark performed.

Conditionally using V31 two-prime representative method N=2^14,d4,L2 still processes 8192 native F.2 factor evaluations and 2*d*H=134,217,728 directly weighted integer/group coefficient terms in the cross-char representative layer. Advanced MSM may optimize performance but does not automatically remove dense public input processing. Range on quotients, no-wrap checks, actual SNARK proof, witness privacy and full simulator still MISSING. Native F.2 PUBLIC y and v' are not made zero-knowledge by appending BP.

## Decision

**FAIL:** claiming off-the-shelf aggregated range-proof result makes ENTIRE vFHE cross-prime CP O(log H) communication or cost. **PASS:** the published BP range proof payload is logarithmic AND can use one Pedersen VALUE commitment vector, reused for native authenticated public y and separate Schnorr integer quotient linking. The local arithmetic verification is REAL in an explicitly insecure small group, but the aggregate range prover/verifier and full protocol/Fiat–Shamir soundness are **NOT IMPLEMENTED**. This is standard techniques recombination and not yet evidence of new contribution or efficient deployable repair.

**Keep main V33 NEXT V34 unchanged. If PI continues V34:** One published vector commitment/IPA commitment to a canonical small-integer vector supporting BOTH succinct whole-vector boundedness AND arbitrary postcommit dense linear-functional opening, explicitly linked to same commitment with the F.2 verified PUBLIC native y. Cheapest kill gate: whether published aggregate range proof is actually defined over that compressed vector commitment or still needs all H V_j. If no credible mechanism advantage or latest paper edition source, return HUMAN_REVIEW and park. Do not resume already parked hidden GP-root ZK line. General FHE I192 frozen, no author outreach without PI.

**Reproducibility (local-only, twice deterministic):**
- /mnt/data/vfhe_v33_aggregate_bp_api_gate.py SHA256 51c4842bb23120f3b31fd7e82225b126193d7a34451f8678ae3d5c269725d182;
- /mnt/data/vfhe_v33_aggregated_bp_public_inputs_results.json SHA256 f55b44eb21cfd8d3a81a7d92e7ef1d1738c270db497724e335c12e482c6e14f1;
- /mnt/data/VFHE_V33_Bulletproofs_Aggregated_Range_Public_Input_Gate_2026_10_15.md (full report);
- local script depends on previous V32 source /mnt/data/vfhe_v32_public_y_cp_glue_gate.py SHA256 071243936179dc9e0ffa2c6141fac69c72a721fc9e0bfc51ba311ac41f1b02c5.

**END V33:** STATUS FAIL total-logarithmic communication shortcut, PASS published range theorem/public input cost and toy authenticated native weighted-Schnorr link, no BP proof generated, NEXT_TEST true vector-commitment basis, STATE_UPDATE YES independent vFHE, I192 FROZEN.
