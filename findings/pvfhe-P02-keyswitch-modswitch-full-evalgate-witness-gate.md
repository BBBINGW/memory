# PVFHE-P02 — BitDecomp ambiguity lifts to a different public EvalGate ciphertext via KeySwitch

**2026-10-14, independent PVFHE stream. P02 COMPLETED; P03 NOT STARTED.**
**STATUS: PASS source-level exact false-output relation witness, UNCLEAR compiled full R1CS/SNARG acceptance, real-key advantage or plaintext corruption.**

## Read before write
Read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md; separate global STATE.md SHA 03463f39c7c8440e1782d8c0bef87ab11472e1f5 (vFHE V21); parallel SHIP state SHA 3bd92057db7d421e692814c68de84dcf45e1fe72 (I226); and findings/pvfhe-P01-ring-r1cs-bitdecomp-xpow-source-parameter-counterexample.md SHA 83ac7399bd0f12b9b6873a814d7b35e3625ebfdc. Destination absent, and no shared states or prior findings altered. P01 established a local wrong XPow and nontrivial idempotent. P02 selects the **cheapest full-relation propagation of the SAME noncanonical BitDecomp root cause**, through final KeySwitch, rather than pretending to have lifted XPow through noisy GSW.

**Primary source:** Huang, Li, Mao, Zhang, *Fully Homomorphic Encryption with Efficient Public Verification*, ePrint 2024/1764. 29-page full mirror PDF SHA256 7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089, VERSION_UNVERIFIED. Research MCP read physical pp12–16, 26–27. Public IACR PDF web text cross-checked, but rendered screenshot on original pp14–16 and27 FAILED cache miss, so latest original binary parity unverified.

## ONE hypothesis and one decisive test

**[HYPOTHESIS P02]** Other conditions in source Algorithm2 / Theorem4.12 force its compiled per-operation constraints to have a **unique correct public output ciphertext**, despite P01 BitDecomp noncanonicity. Can an alternate satisfying final KeySwitch bit decomposition produce a different public EvalGate output?

**[DECISIVE FALSIFIER]** Hold ALL ACC.Update/Extract and every other operation honest. Modify only the final KeySwitch bit witness for one extracted coefficient, check source BitDecomp Booleanity and modular reconstruction, literal Index, KeySwitchGen public key algebra, final ModSwitch. If a distinct public ciphertext results with all displayed constraints satisfied, Theorem4.12's exact iff claim is false *at the composed algorithmic-constraint level*. Do not claim a forged SNARG proof or wrong decrypted message.

## Primary paper interfaces [FACT]

Physical p13: KeySwitchGen publishes K_(i,j,v)=(a_(i,j,v), <s,a_(i,j,v)>+e_(i,j,v)+v*z_i*2^j) modulo Q with uniform a and Gaussian e; KeySwitch selects one of v0/v1 keys per decomposed bit and subtracts their sum from (0,b). Physical p14 Algorithm2 for NAND first sums two input ciphertexts, initializes ACC with their body, updates with alpha_i=-a_i modq, Extracts an LWE ciphertext, KeySwitches, then ModSwitches. Figure2 p13 ACC.Update terms multiply (X^alpha-1) or (X^-alpha-1), hence alpha0 makes it exact identity regardless of noise in accumulator keys. Physical p15 Lemma4.5 uses x0..x_ell INCLUSIVE with x_j^2=x_j and a=SUM 2^j x_j in R_Q, no explicit integer range <Q. Lemma4.7 Index selects by scalar bits. Physical p16 Lemma4.8/Remark4.9 implements near-power-two modulus switch through truncation. Physical pp17,27 Theorem4.12 / C.3 claim satisfaction iff **exact FHE.Eval output ciphertext**. AppendixB p26 gives Q=2^53+5, N=2048, n=1024, q=1024, ell=53.

## Explicit satisfying-path counterexample [DERIVATION & EXACT TEST]

Select a valid *support* outcome for source KeyGen: ternary LWE secret s=(0,...,0), ring-key coefficient vector z=(1,0,...,0), all key-switch errors 0. For all public K_(i,j,v), masks are 0 EXCEPT K_(0,0,1), whose first mask component is A=2^43; all bodies equal v*z_i*2^j modulo Q as KeySwitchGen requires for s=e=0. Every indicated uniformly sampled a and discrete-Gaussian value lies in its source distribution's support (the overall chosen key is astronomically rare; no normal-key exploitation probability measured). ACC RGSW keys encrypt each s_i=0 but may be any valid randomized ciphertext.

Valid LWE source inputs c1=c2=(0^n,0) and op=NAND give c=(0^n,0). Every alpha_i=0, so each honest ACC.Update is exact identity, ACC.Extract gives (0^N,b), b=f_NAND(0), without needing its numeric value. Honest final KeySwitch represents every extracted a_i0 with all-zero bits, selects K_(i,j,0)=0 and gives raw output (0^n,b); final first mask component0.

**Adversarial witness differs at ONE final coefficient:** For extracted a_0=0 use scalar Boolean x0=x2=x53=1 and all other bits0, so the bit integer is 1+4+2^53=Q and it is 0 MOD Q, exactly the source Ring-R1CS equality. All x_j satisfy x_j²=x_j and all corresponding Index values are faithfully assigned. Other extracted a_i use canonical all-zero bits. Fake public selected keys' total first mask is A; their total body is z0*Q=0 modQ. Therefore fake raw KeySwitch output is (-A first-mask,b) modQ while honest is (0,b).

Since Q-A=2^53-2^43+5, final source near-power-of-two ModSwitch gives floor((Q-A)/2^43) mod1024 = 1023, whereas honest first mask stays0. Signed-center nearest q/Q rounding agrees: -A maps to -1 mod1024. Thus for the SAME public ek,c1,c2,op, all displayed operation constraints admit public ciphertexts differing in the first mask coordinate **0 vs1023**, identical other mask and body. Under s=0 both decrypt to same plaintext: this is an **exact output-CIPHERTEXT relation counterexample**, not a false-plaintext proof.

The satisfying assignments for other ACC/Extract operations are honest ones. The local Ring-R1CS indexing and BitDecomp gadget assigns every key selection as written; Lemma4.4 compiles those arithmetic equalities into R1CS. We have NOT produced the author's fully materialized A/B/C matrices or an actual PC/SNARG acceptance transcript. No additional secret global integer-range check occurs in the displayed local constraints; an unpublished implementation might differ.

**Generality of bit ambiguity:** 54-bit max 2^54-1. For every canonical a from 0 through 2^54-1-Q = 2^53-6, distinct integers a and a+Q both fit 54 bits and represent the same ring value, so **Q-10 out of Q residues** have this duplicated Boolean encoding. This does not independently establish that any normal random ek yields a noticeable attack probability; however the original theorem states a for-all-ek exact iff relation.

## Executed falsification evidence

Actual source-shaped exact arithmetic script /mnt/data/pvfhe_p02_keyswitch_full_relation_gate.py, SHA256 **66ff788d52ea90b3771665d97271bb4c405c58ccb75d6dd6f03fc7c3037c5d9e**.
Actual JSON /mnt/data/pvfhe_p02_keyswitch_full_relation_results.json, SHA256 **ea9499b40a1ba44b29bf2f94de027c438a0c07ab6c85038896e0a05912cad044**.
Full local report /mnt/data/PVFHE_P02_Full_EvalGate_KeySwitch_BitDecomp_Gate.md, SHA256 **56b29ec0c4d51aa44a8d35753e65876f75647c24cfd5deed7541343d54ba6813**.
Ran all N*54 coefficient/bit choices lazily using valid KeySwitchGen symbolic algebra; 5/5 independent f-body test values produce first public mask 0 vs1023, body unchanged; 11 boundary checks confirm exactly ten nonambiguous residues. No actual RGSW encryption binary/full R1CS matrix/PCS/Fiat-Shamir proof, no decryption fraud or IND-SA break verified.

## Research judgment / end of iteration

**STATUS:** PASS exact local-to-Algorithm2 false-public-ciphertext compositional witness (conditional on source-stated constraints); UNCLEAR full SNARG proof acceptance, usual sampled-key advantage, plaintext malleability and authenticated newest edition.
**RESULT:** Same underlying noncanonical BitDecomp as P01 produces wrong final KeySwitch and visibly different ModSwitch ciphertext, independently of the particular f and without changing any honest ACC updates. This materially strengthens the earlier local Lemma4.10 concern as a failure of Theorem4.12's **exact algorithm-to-constraint correspondence**, not of FHE decryption correctness.
**NEXT_ACTION — PVFHE-P03 only if PI continues:** ONE minimal canonical/scalar-bit repair and cost gate. Test a source-shaped O(log Q) integer comparison enforcing SUM 2^j x_j<Q for Q=2^53+5, and a separate valid scalar-bit condition because Claim4.6 fails in reducible R_Q. Alternatively materialize full original A/B/C and verifier transcript only upon available authentic code, to settle security-level exploit. No public allegations/contact without PI approval.
**STATE_UPDATE:** YES new independent P02 finding ONLY; no modifications to global STATE.md, SHIP, vFHE, P01 or backlog.
