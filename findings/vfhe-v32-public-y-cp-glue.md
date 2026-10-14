# vFHE V32 — Original F.2 public native y as a separately provable cross-CRT bit-commitment input

Date 2026-10-15. INDEPENDENT V32; GLOBAL FHE I192 FROZEN.

**ONE falsifiable hypothesis:** Unlike V29's expensive attempt to reproduce native SHA/Merkle authentication INSIDE a third-field hiding proof, the original vFHE Appendix F.2 verifier already checks a PUBLIC native evaluation y=<q1Uf,q2> against an original Merkle/RS coded-matrix commitment. Can a separately implemented small-integer-bit CP use EXACTLY THAT authenticated public y and one precommitted global bit vector as public/witness inputs, proving native-to-integer quotient equality WITHOUT an in-circuit Merkle authentication gadget? Falsifier: test native F.2 and explicit bit-commitment Sigma OR and Schnorr aggregate checks on the earlier CRT261 malicious family, with exact no-wrap bounds, rather than relying on an IDEAL CP black box.

**STATUS:** PASS a fully executable SMALL INSECURE GROUP toy that performs two original-source-shaped native F.2 Merkle/RS checks, 36 bit-OR Sigma proofs, and four aggregate Schnorr equality proofs; both honest primes accept and CRT261 cheat is rejected at the mismatching prime. **UNCLEAR/NOT ESTABLISHED:** actual 128bit knowledge soundness, source F.2 PC extractor or FS composition theorem, real ZK/privacy, successful fully compiled source SNARK patch and source official Feb2026 PDF parity. FAIL a direct naive per-bit CP as a competitive H=2^24 patch: ~7GiB messages/bit-commitments before original F.2.

## Primary source vs prior art [FACT]

Cascudo et al., "Verifiable Computation for Approximate Homomorphic Encryption Schemes", CRYPTO2025 / IACR ePrint2025/286, 52 physical page GitHub Research MCP mirror SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19, latest official 2026-02-16 revision VERSION_UNVERIFIED. §3.1 p10: p_i=1+(2N/d)*odd, k=N/d degree-d CRT field factors/p; §4.3 pp20–24 scalar digit table; F.1 p50 decomposes polynomial commitments by native CRT factors; F.2 physical p51 PUBLICLY sends native v=rtest Uf for testing and v'=q1Uf, verifies Merkle-authenticated sampled columns, Enc(v')|Q'=q1 Uhat|Q', and PUBLIC y=<v',q2>. F.3 p51 allows piecewise [N/2,m/tau] RS. The cross-char CP below is OUR candidate; source does not claim it.

Prior-art primitive: Ronald Cramer, Ivan Damgård, Berry Schoenmakers, "Proofs of Partial Knowledge and Simplified Design of Witness Hiding Protocols", CRYPTO1994, DOI 10.1007/3-540-48658-5_19, https://ir.cwi.nl/pub/1456/ . Basic Pedersen commitments, Schnorr Sigma proof of a discrete log and 2-way Schnorr OR membership are all known techniques. No new cryptographic primitive is claimed.

## Concrete, non-ideal arithmetic circuit [DERIVATION]

Bind ONE canonical vector a=(a_b)_b in [0,beta−1]^H prior to native challenge, beta4 here; a_b=b_(b,0)+2b_(b,1) with bits in{0,1}. Publish group commitments C_(b,l)=g^{b_(b,l)}h^{rho_(b,l)}; for each C use the 2-way Schnorr OR proof that prover KNOWS log_h(C) (value0) OR log_h(C/g) (value1). Unlike testing fieldwise t_beta independently, the SAME global C components feed every RNS prime.

For each representative native field K_i=F_(p_i^d), the ORIGINAL source native F.2 verifier first accepts public y_i at public post-commit full-extension r_i from Merkle source cm_i. In native basis θ, write χ_b(r_i)=Σ_(t=0)^(d−1)c_(i,b,t) θ^t and y_i=Σ_t y_(i,t)θ^t; canonically lift cbar∈[0,p_i−1], ybar∈[0,p_i−1]. Prover separately bit-commits quotient k_(i,t)=Σ_u 2^u kbit_(i,t,u) and supplies bitness OR proofs. In third group prove knowledge of log_h(V_(i,t)) for
 V_(i,t)=[ Π_(b,l) C_(b,l)^{cbar_(i,b,t) 2^l} ] / [ g^{ybar_(i,t)} (Π_u D_(i,t,u)^{2^u})^{p_i} ].
Correctly extracted bit witnesses imply integer congruence Σ cbar a =ybar+p_i k mod group order r. Enforce BOTH side integer bounds strictly below r, converting mod-r equality into exact INTEGERS. This relation also needs the original native accepted y as its EXACT public input; the original Merkle and RS verification remains OUTSIDE the new CP but not optional.

**Security scope:** This is standard Sigma/Fiat-Shamir-style arithmetic with toy checks. A formal joint proof of knowledge extraction, FS transcript-order compliance, malicious multi-session security, actual native F.2 soundness, and witness privacy is NOT provided. Original F.2 already PUBLICLY exposes y and entire field vectors; this CP alone does not make the full scheme zero knowledge.

## ONE executable deterministic toy [EXPERIMENT]

Source-form N4,d2,beta4,ellstar3,H8, representative primes p13=1+4·3 and p29=1+4·7; fields K13=F13[u]/(u²−5), K29=F29[u]/(u²−12). Honest shared a=(0,1,2,3,0,1,2,3). Embed each 3-variate MLE into a 4-variate F.2 4×4 matrix Uf (dummy fourth bit), encode each row with four genuine source F.3 [2,1] repetition RS blocks -> 8 encoded columns, each Merkle leaf hashes ENTIRE 4-field-element column with SHA256. Both testing and evaluation source-shaped F.2 checks authenticate 3 Merkle columns each. PUBLIC native y matches claimed table MLE.

Proof group: multiplicative subgroup of F10091* of prime order r1009, generators g4903,h8557, **intentionally completely INSECURE cryptographically** (discrete logs easy by brute force). Implements bit-commit OR Sigma with seeded domain-separated hash challenge and Schnorr log_h(V) for four native base-coordinate equalities. Global bit commitments: 16; quotient bit commitments: 20; 36 actual OR proofs plus 4 aggregate equality Schnorr proofs, all verified.

Native p13: y=(10,0), integer S=(88,104), quotient k=(6,8), exactly S=y+13k.
Native p29: y=(10,13), S=(242,187), k=(8,6), exactly S=y+29k.
Per-prime native Merkle+RS checks accept; per-prime external bit commitment and aggregate equality checks accept. Tamper public y by +1 -> external CP rejects; tamper OR response -> OR verifier rejects. No-wrap: Smax=H*(beta−1)*(p29−1)=672<r1009, max RHS y+p(2^5−1) at p29 =28+29*31=927<1009.

Decisive BAD full ring digit e=261 mod377: native h13≡1 and h29≡0, with shared committed a=(0,...,0). The two native F.2 authentic evals each ACCEPT; p13 native y=(1,0) disagrees with shared a0 and CP prover cannot produce a correct bounded quotient (toy returns NO PROOF/REJECT); p29 native y=(0,0) agrees with global a0 and CP ACCEPTS. Thus conjunction rejects the original cross-prime non-diagonal witness without moving Merkle into third-field circuit. This is a TOY arithmetic interface test, not adversarial simulation against 128bit Pedersen binding.

Deterministic standard Python executed twice with identical hashes. Local script /mnt/data/vfhe_v32_public_y_cp_glue_gate.py SHA256 071243936179dc9e0ffa2c6141fac69c72a721fc9e0bfc51ba311ac41f1b02c5; JSON /mnt/data/vfhe_v32_public_y_cp_glue_results.json SHA256 0f58649b841f50cabd2cb9d8868346208550995ee03ff6ea65c9466db1e46ca7; full Markdown /mnt/data/VFHE_V32_Public_Y_Bit_CP_Interface_Gate_2026_10_15.md SHA256 db29e7b5c0aca831adc85fd244fb46b7fc4312bceb366ebf1a664a99651e0f0d.

## Direct size gate, no invented runtime

At illustrative H=2^24,beta4, naive per-bit variant requires 2H=33,554,432 global bit commitments (32bytes each, **1GiB** raw group elements) and the explicit OR proof transcript in THIS toy has 2 group elements+4 scalars per bit (192bytes/bit at standard 32-byte encoding), **6GiB** of standalone bit proof transcript before quotient proofs, native F.2 and group multiexponentiations. Nothing here proves that all protocols must have this cost: aggregate range proofs, vector commitments, folding and succinct arguments are known options and require their own soundness/source binding checks. The bitwise CP does NOT add SHA Merkle path hashing *inside* the new proof; original native verifier still performs F.2 SHA authentication of huge columns. Source-scale H2^24 is an illustrative previously studied gate, not automatically real deployment parameters. No 128bit prover timings or proof bytes benchmark exists.

## Research decision

**PASS** *toy* source-F.2-public-y-to-Pedersen-bit-CP link with correct canonical integer quotients and CRT261 rejection, without in-circuit Merkle. **FAIL** economically competitive naive bit-by-bit proof at H2^24; formal knowledge soundness, current latest publication parity, CKKS compute relation, multi-round FS composition and native real prover remain OPEN. This removes a specific V29 architectural obstacle (duplicated Merkle inside CP) but is NOT completed cryptographic repair. Reuse V30 within-prime native alignment and V31 one representative CP per RNS prime CONDITIONALLY; don't imply 4096x system speedup. No author contact without PI decision.

**NEXT_ACTION V33 only if PI continues:** one published aggregate bit range / vector commitment + succinct linear functional proof, retaining same F.2 public-y and canonical quotient constraints, with exact proof size and honest source binding OR HUMAN_REVIEW if no cost advantage. DO NOT resume the parked hidden GP root branch; obtain official Feb2026 ePrint PDF to authenticate any source version claim. Global I192 frozen.

**End:** STATUS PASS executable toy / FAIL naive large-scale efficiency / UNCLEAR secure complete protocol. RESULT actual commitments/OR/Schnorr transcript + Merkle external native authentication; NEXT_TEST V33 aggregation, STATE_UPDATE YES independent V32; GLOBAL I192 FROZEN.
