# PVFHE-P23 — Ordinary KeySwitchGen masks do not eliminate noncanonical BitDecomp public-output ambiguity

**Checkpoint:** 2026-10-15 Asia/Tokyo. **P23 COMPLETE; P24 NOT STARTED.**
**STATUS:** PASS source-conditional generic-key local public ciphertext-mask nonuniqueness; UNCLEAR actual full SNARG proof acceptance, full ACC.Extract coefficient distribution/independence and current published binary version. P05–P22 nested PCS/FS security integration stays PARK/HUMAN_REVIEW, not reopened.

## Read before write
Read START_RESEARCH_SESSION.md SHA 6235e9d376a8b143719a40178132f02a6a41d4f3; RESEARCH_PHILOSOPHY.md SHA 49da3f7fa3e75f5025258cf525482ce4a7ab6867; AGENT.md SHA b3e73b2c7f852c05aa674dd97b632e9f99ac5f22; separate STATE.md SHA 653fb73ad18d13ab27e1d4b0067247e35fcb8670 (independent vFHE V40); P22 SHA b3e3fc6683b73ab1e116f9d0979f29548c77b534, P01 SHA 83ac7399bd0f12b9b6873a814d7b35e3625ebfdc, P02 SHA 9b09262066c61778ce581abbba4dbd5098ee5483, P04 SHA 004f4e3904e3e65c2c46cd194b64a56670cdf3fd. Listed findings, failures and opportunity backlog. No modifications to shared STATE, P01–P22 or parallel SHIP/vFHE.

**Original primary source:** Huang, Li, Mao and Zhang, Fully Homomorphic Encryption with Efficient Public Verification, ePrint 2024/1764, full 29-physical-page Research MCP mirror PDF SHA256 7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089, VERSION_UNVERIFIED. Read pp12–16 and 26–27. p13 KeySwitchGen fresh a uniform in Z_Q^n for every (i,j,v), public ciphertext body <s,a>+e+v*z_i*2^j; p14 KeySwitch, Algorithm2 and ModSwitch; p15 Lemma4.5 inclusive 54 bit variables j=0..ell with modulo-Q reconstruction, NO integer canonical range; p16 Remark4.9 near-power-two truncation; p26 AppendixB Q=2^53+5, n=q=1024; p27 Theorem C.3 exact compiled-circuit iff. No latest official PDF parity authentication or original complete Ring-R1CS prover execution.

## ONE smallest falsifiable hypothesis and decisive test

**HYPOTHESIS P23:** The P02 false-public-KeySwitch-output witness is an exceptional secret=0/error=0 key generation outcome; under ordinary independently random public switching-key masks both allowed bit decompositions yield the SAME public ModSwitch ciphertext with high probability.

**FALSIFIER:** For ANY fixed intermediate coefficient a admitting an alternative 54-bit representative mod Q and independent of fresh KeySwitchGen masks, couple the two selected branches on identical other source inputs. Compute the conditional probability that their entire n-dimensional public mask vectors agree after the source near-power-two modulus switch. Check bit boundary and a small exact rounding-collision table. Do not assume a uniform ACC.Extract distribution or claim a real SNARG forgery.

## Source-Q alias theorem [DERIVATION, EXACT]

Q=2^53+5, ell=53, binary witness has 54 bits, integer range [0,2^54−1]. For canonical scalar a in [0,Q−1], distinct a+Q is available iff a+Q<2^54, i.e. 0<=a<=Q−11. Exactly Q−10=9007199254740987 of the Q canonical coefficient values have TWO allowed bit witnesses. This is a cardinality fraction 1−10/Q, NOT a probability for actually generated ACC.Extract outputs. Example a=0 vs integer representative Q: bits {0,2,53} and all-zero bits both satisfy x_j²=x_j and reconstruction in R_Q. This phenomenon uses plain scalar bit values, no CRT idempotents.

## Normal switching-key distribution [DERIVATION, PASS conditional]

For fixed aliasable a, two bit strings b,b' differ at one or more j. Choose any differing (i,j). Source KeySwitchGen independently samples vectors U=a_(i,j,0), V=a_(i,j,1), both uniform Z_Q^n. Condition on all other switching-key masks and the fixed extracted coefficient. The selected canonical and alternate switching-output mask vectors are CONST−U and CONST'−V. Thus they are INDEPENDENT uniform Z_Q^n for arbitrary normal/exceptional ternary secret keys, ring keys and Gaussian errors. No P02 rare key-event needed.

For the published 2^ell-denominator floor ModSwitch variant, map canonical representative x∈[0,Q−1] to floor(q*x/2^ell) modq, ell=53, q=1024. Put w=2^ell/q=2^43 and Q=2^ell+5. Its exact residue-bin sizes are w+5 at residue0 and w at every other residue. For independent uniform mask coordinates U,V:

  p_one=((w+5)^2+(q−1)*w^2)/Q^2.

Independently sampled n=1024 vector coordinates yield identical modulus-switched PUBLIC mask probability p_one^1024, approximately 2^(−10240). Thus two locally satisfying KeySwitch bit-witness paths almost certainly produce different public ciphertext masks over KeySwitchGen masks conditioned on the aliasable input. No need to inspect ciphertext body for nonuniqueness. A different nearest-rounding convention changes exact bin sizes slightly and needs separate count, not the basic near-1/q collision conclusion.

**Critical boundaries:** The statement is CONDITIONAL ON a fixed aliasable coefficient independent of the KSK masks; source has not shown real ACC.Extract coefficients are uniform. Probability over fresh KSK samples, not conditioned on a specific disclosed evaluation key. Proof checks source local KeySwitch semantics, not full original A/B/C SNARG prover/verifier or false plaintext decryption. It is NOT an original paper security break or public published-version erratum.

## ONE actually executed test

Actual run: /mnt/data/pvfhe_p23_generic_keyswitch_alias_test.py SHA256 df4bf6d84840208eb8cef4b2e129a89ff768f0d77dd6612e73a27553aaa67e79
JSON: /mnt/data/pvfhe_p23_generic_keyswitch_alias_results.json SHA256 077e7fa540b0902049960e1d968899d8b15662b8d28d41c79402fdfa9fcd5a63
Full source-backed report: /mnt/data/PVFHE_P23_Generic_Keyswitch_Alias_Distribution_Gate.md SHA256 feec56113e6b006b1daaa9e7b1213790743b4009d69fa28d2e177a5418af0e15.

Source-Q bit support {0,2,53} PASS, last aliasable Q−11, first nonaliasable Q−10. Exhaustively checked ALL 1369 ordered pairs of toy Q=37, ell=5, q=8 random mask coordinates under exact same floor+modq map: bin sizes [8,5,4,4,4,4,4,4], exactly 185/1369 pairs collide. Validates counting, NOT actual LWE, Ring-R1CS or SNARG execution.

## End of iteration

**STATUS:** PASS local normal-KeySwitchGen mask divergence conditional on aliasable independent ACC coefficient; FAIL claim that rare zero-secret/key-error support is necessary; UNCLEAR full compiled SNARG accept, coefficient distribution, message impact/current publisher version.
**RESULT:** P02 local Ring-R1CS output ambiguity persists under generic independently uniform KSK masks and is not limited to negligibly sampled zero keys/errors. This improves impact evidence but is not sufficient for a verifiable-FHE security attack.
**NEXT_ACTION P24 only upon PI continuation:** One full original-source ACC.Extract-vs-KSK randomness independence and hidden canonicality constraint audit, using original gate interfaces. No repeat of mask collision toys. If author compiler/latest official PDF still unavailable, maintain HUMAN_REVIEW, not a forged-SNARG claim.
**STATE_UPDATE:** YES this independent P23 standalone note only; leave global STATE and concurrent vFHE/SHIP unchanged, P05–P22 PCS integration remains PARK.
