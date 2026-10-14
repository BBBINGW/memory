# PVFHE-P18 — Nested Fiat–Shamir anchor prefix-extraction gate

**Date:** 2026-10-15 Asia/Tokyo. **Independent PVFHE P18 COMPLETED; P19 NOT STARTED.**
**STATUS:** FAIL automatic upgrade of CMNW interactive knowledge extractor to a prefix-preserving nested FS extractor; PASS explicit minimal transcript-dependency test; UNCLEAR actual classical ROM/QROM composed security, SIS and full Ring-R1CS. PARK unqualified claims that P11/P12 form a fully proven secure noninteractive repair. No original-paper attack claimed.

## Read before write / source provenance

Read START_RESEARCH_SESSION.md SHA 6235e9d376a8b143719a40178132f02a6a41d4f3, RESEARCH_PHILOSOPHY.md SHA 49da3f7fa3e75f5025258cf525482ce4a7ab6867, AGENT.md SHA b3e73b2c7f852c05aa674dd97b632e9f99ac5f22, separate global STATE.md SHA ff53173e3c523841751c3be61ff0610fe2458c2d (independent vFHE V35), P17 findings/pvfhe-P17-real-compiler-occupancy-gate.md SHA c7c1e1ff6ada88f5a41a19c04585a1d18480384f and P11 findings/pvfhe-P11-binding-sqrt-loss-precommit-extraction-gate.md SHA 165dfc36f7ba9914561ebe93ef5ff113316b083c. Target P18 was absent; do NOT overwrite concurrent vFHE/SHIP or prior findings.

Full original CMNW: Cini–Malavolta–Nguyen–Wee, Polynomial Commitments from Lattices: Post-Quantum Security, Fast Verification and Transparent Setup, CRYPTO 2024, ePrint 2024/281, physical 52pp Research MCP mirror PDF SHA256 a9be7b5c1e9024d2d0c03865978d7f3ea1ed941dce8883f93f9576ae46a73b73, VERSION_UNVERIFIED. Inspected Definition6 physical p12, Definition8 p13, Figure6 p17, Lemma3 pp19–21, Theorem2 p22, Theorem4 p24, Appendix A.4 p39 and Appendix B pp39–42. CMNW single-statement INTERACTIVE extractor can rewind a stateful adversary and returns a full polynomial-opening witness; Lemma3 uses multiple DIFFERENT challenge matrices / coordinate-wise special soundness. Appendix A.4 calculates a linear FS random-oracle query penalty for ITS OWN PCS but does NOT prove OUR nested protocol.

Original Huang–Li–Mao–Zhang, Fully Homomorphic Encryption with Efficient Public Verification, ePrint2024/1764, Research MCP full PDF 29pp SHA256 7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089 VERSION_UNVERIFIED, §5.3 pp20–22: Fiat–Shamir of original Ring-R1CS argument, NOT our new anchor. No author flaw inferred.

External distinct reference (do not conflate): Journal of Cryptology, Lattice-Based Polynomial Commitments: Towards Asymptotic and Concrete Efficiency, DOI 10.1007/s00145-024-09511-8, Section8 proves ADAPTIVE FS knowledge extraction for a DIFFERENT lattice-based commitment design and coordinate-wise multi-round protocols. An avenue for P19, not a theorem for CMNW 2024/281 or nested H_outer.

## One primary hypothesis + minimal falsifier

**[HYPOTHESIS P18]** The published CMNW interactive single-evaluation knowledge extractor can be used unchanged as a noninteractive online extractor for an anchor proof pi0 before sampling r=H_outer(statement,C,pi0), while keeping pi0 and the original continuation hash table unchanged, thus directly justifying P11's linear-binding-loss classical ROM bound.

**[FALSIFIER]** Show source extraction requires distinct internal challenges and build one exact valid simple FS PoK where changing the inner challenge necessarily changes the complete proof pi0, and hence its outer RO query input. If so the purported direct transfer of an interactive extractor into an unchanged-prefix online FS extractor FAILS. A new specialized nested-ROM extractor is not ruled out.

## Source-typed protocol dependency [DERIVATION]

Our NEW P11/P12 scheme:
  public statement/selector fixed
  -> SAME private witness commitment C
  -> finished fixed-zero CMNW FS evaluation anchor pi0
  -> r=H_outer(domain,statement,C,pi0) in P12 sigma-fixed exceptional set
  -> one masked-face PC.Eval under SAME C, check v=sigma(v), enforce original Ring-R1CS/mask links.

The desired P11 error <= s/|E| + eps_K0 + eps_K1 + eps_B1 is a CONDITIONAL CLASSICAL INTERACTIVE conclusion: before independent external challenge r, rewind/extract whole polynomial f from pi0; binding identifies later extracted f. The full FS version is not automatically covered.

CMNW Lemma3 physical p19–21 needs multiple accepting continuations with DIFFERENT verification challenges to extract entire polynomial opening. In FS, internal challenge is a HASH of prior proof prefix. A reduction changing an inner challenge usually also changes the response, so complete anchor proof pi0 becomes pi0'. The outer oracle key changes:
  H_outer(statement,C,pi0) versus H_outer(statement,C,pi0').
For distinct oracle INPUT STRINGS, independent ideal outer RO answers are sampled; the original external r and accepted prover continuation cannot be copied unchanged into the fork by simply appealing to interactive knowledge soundness.

**Limit of this falsifier:** A stronger nested-ROM proof may explicitly preserve the MAIN original branch, fork only auxiliary branches, reprogram inner/outer RO consistently and bind recovered f by SIS. We have neither proved such an extractor impossible nor built one. Source Definition6 alone does NOT provide that stronger oracle-consistent online extraction, adaptive outer-query proof, knowledge error or strict-PPT loss. Distinguish proof boundary from actual scheme unsoundness.

## One ACTUALLY EXECUTED exact minimal challenge fork [VERIFIED]

A valid toy Schnorr-style PoK for discrete-log subgroup of F23, prime order11 and generator g=2, has witness x=7, public y=13, first message a=2^k mod23, challenge c, response z=k+c*x mod11 and verification g^z=a*y^c mod23. Complete FS anchor proof is (a,z), c implicit in H_inner(statement,a).

Enumerated ALL 11 k values and 11*10 ordered distinct challenge pairs (c,c'): **1210/1210** both accepting proof transcripts differ; **1210/1210** their OUTER hash input strings differ. Formula z-z'=(c-c')x mod11 nonzero. Ideal outer RO range of size7 has probability 1/7 of an accidental equal OUTPUT at two different input strings; outputs are NOT guaranteed different. Demonstrative SHA256 mod7 produced 168/1210 equal outputs, NOT a cryptographic probability bound and sampled entries are not independent. This model is NOT CMNW lattice PCS, not a false accepting proof/attack, and does not establish impossibility of a better extractor.

Actually executed local files:
- /mnt/data/pvfhe_p18_nested_fs_prefix_gate.py SHA256 00eb19db33541e6e7b3aba6f444c841ae1f846fc921ece351738141e3a33cdb9.
- /mnt/data/pvfhe_p18_nested_fs_prefix_results.json SHA256 1cea36ed12a2c90250994cf6d43ddc7daacdfc51fb2da21fdd4c279b83e6639e.
- /mnt/data/PVFHE_P18_Nested_Fiat_Shamir_Anchor_Gate.md SHA256 abcd8b250b73c229a8842182b490418a2eb301f9c1e18516de977a047c773bb4.

## Exact missing lemma / stop condition

Need source-level theorem for ADAPTIVE NESTED CLASSICAL ROM FULL OPENING extraction on ONE commitment and fixed anchor statement:
1. Extract whole f and opening in norm beta_* under dynamic statements with explicit errors.
2. Compose inner FS rewinding/reprogramming with outer r=H_outer(statement,C,pi0), controlling probability of original accepting execution despite fork transcript changes.
3. Bound q_H, internal query loss, extractor truncation, two-opening difference SIS hardness at 2beta_*, and enforce source Ring-R1CS mask links. Need a separate QROM/quantum security theorem.
Without this, P11's attractive linear-binding loss is a CONDITIONAL INTERACTIVE theorem, and the fully noninteractive PVFHE repair remains HUMAN_REVIEW, not a proved new scheme. Existing algebraic counterexamples P01/P02 and semantic repair P04/P12, source-shaped matrix work P13–P16 remain separately archived with their own scopes. P17's concrete performance optimization remains PARK.

## End of iteration

**STATUS:** FAIL direct interactive extractor -> prefix-preserving nested FS inference; PASS exact structural transcript counterexample; UNCLEAR actual classical ROM/QROM composition.
**RESULT:** CMNW source extractor forks internal challenges, necessarily changes transcripts in a simple valid FS PoK; because our outer r hashes complete pi0, naive extractor continuation is not source-justified. No cryptographic break or impossibility theorem established.
**NEXT_ACTION P19 only on PI continuation:** ONE actual theorem audit of adaptive Fiat–Shamir full-opening extraction (e.g. the separate 2024 Journal of Cryptology PCS Section8), with focus on nested RO branch consistency, full-opening relation and norm slack. If unavailable, PARK complete PCS integration and prepare a PI HUMAN_REVIEW technical-obligation package rather than more toy algebra or speculative costs.
**STATE_UPDATE:** YES only NEW independent P18 note; do not edit global STATE.md, concurrent SHIP/vFHE or P01–P17.
