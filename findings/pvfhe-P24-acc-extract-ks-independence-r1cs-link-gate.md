# PVFHE-P24 — Deterministic honest self-XOR ACC zero-mask defeats input-distribution objection

**Date:** 2026-10-15 Asia/Tokyo. Independent PVFHE-P24 COMPLETED; P25 NOT STARTED.
**STATUS:** PASS exact source-algorithm self-XOR ACC zero-mask trigger and conditional ordinary independent KSK-mask divergent public ciphertext computation. UNCLEAR complete compiled Ring-R1CS/SNARG proof and source-version parity; NO wrong-plaintext/security attack established. P05–P22 PCS/FS integration stays PARK/HUMAN_REVIEW.

## Read-before-write and primary-source provenance
Read START_RESEARCH_SESSION.md SHA 6235e9d376a8b143719a40178132f02a6a41d4f3, RESEARCH_PHILOSOPHY.md SHA 49da3f7fa3e75f502525482ce4a7ab6867, AGENT.md SHA b3e73b2c7f852c05aa674dd97b632e9f99ac5f22, global STATE.md SHA 848893be120937b2268e8ce33aa261fde6e1ad1f (other independent vFHE V41, **NOT edited**), previous P23 SHA 8c74c73f761571dbced8ed32391985a982c0aede, and P02 SHA 9b09262066c61778ce581abbba4dbd5098ee5483. Target P24 did not exist; no old findings or global state changes.

Primary source: Huang–Li–Mao–Zhang, *Fully Homomorphic Encryption with Efficient Public Verification*, ePrint 2024/1764, full Research MCP PDF, 29 physical pp, SHA256 7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089, VERSION_UNVERIFIED; physical p13 Figure2 ACC.Init/Update/Extract and KeySwitchGen, p14 Figure3 and Algorithm2, p15 Lemma4.5 BitDecomp and Lemma4.7 Index, p16 Rounding Lemma4.8 and Remark4.9, p17 Theorem4.12, p26 source concrete Q=2^53+5,N=2048,n=q=1024, p27 proof TheoremC.3. Equation glyph/column warnings, no authenticated latest original PDF screenshot/full original compiler.

## ONE falsifiable hypothesis / ONE decisive test
**HYPOTHESIS P24:** P23's source-conditional generic KSK mask divergence requires an unrealistically rare/unknown ACC.Extract coefficient-distribution event or breaks due to common KeyGen secrets; therefore it cannot be triggered by any normal valid FHE.EvalGate input without extra hidden canonicality constraints.
**FALSIFIER:** Feed the SAME properly formed LWE ciphertext twice to source Algorithm2 with op=XOR; symbolically propagate ALL ACC updates for any ek, prove exact extracted zero mask; then demonstrate, in one exact source Q,n key-switch terminal-gadget test with nonzero secrets/errors and fresh independent normal KSK masks, that two BitDecomp branches satisfy the printed BitDecomp/Index/Rounding relations while yielding different public ciphertext masks. Inspect source AppendixC.3 for additional range constraints; never claim running its actual compiled SNARG.

## Decisive new deterministic theorem [SOURCE+DERIVATION]
Algorithm2 p14 for XOR uses c_tmp=2(c1-c2). For any *one* valid LWE ciphertext c, c1=c2=c => c_tmp=(0^n,0). Thus every alpha_i=-a_i modq is 0. Figure2 p13 ACC.Init sets accumulator RLWE mask polynomial to 0; each ACC.Update adds
 (X^alpha_i-1)*(c diamond C1)+(X^-alpha_i-1)*(c diamond C2).
Both factors vanish identically for alpha_i=0; no ACC.Enc ciphertext, KSK, secret, error or randomness can change the zero mask. ACC.Extract therefore returns **all-zero LWE mask coefficients** for every evaluation key and the honest operation XOR(c,c). The unknown body f_XOR(0) is irrelevant to this coefficient claim.

For Q=2^53+5 and 54 source BitDecomp bits j=0..53:
 - canonical bits all zero => reconstructed 0;
 - noncanonical scalar Boolean bit set {0,2,53} => reconstructed 1+4+2^53=Q≡0 modQ.
Both satisfy every printed Booleanity and modular reconstruction equation, including their obvious prefix-sum implementation witnesses. The source p15 Index selects K_(i,j,0) or K_(i,j,1) via the bit; three positions differ at the zero coefficient. All other computation and coeff extraction can be held honest. A full original A/B/C compiled witness still needs independent verification.

KeyGen p14 first samples secret (s,z), KeySwitchGen independently samples mask A_(i,j,v) uniformly from Z_Q^n, and only then generates ACC.Enc(z,s_i) with fresh encryption randomness. Shared secrets affect KSK BODIES but do NOT invalidate fresh MASK independence. Even stronger, self-XOR gives extracted coefficient zero as a constant for ANY ek and ANY shared public ciphertext c: it does not require an ACC coefficient distribution or even c independent of the evaluation key.

Fix all other KSK vectors and one j where bits differ. The two chosen KSK public masks are independent uniform vectors; hence canonical and noncanonical switched output masks are independent uniform affine shifts. Using the source's adopted floor(q*x/2^53) modulo q, one-coordinate rounded collision
 p=(((w+5)^2)+(q-1)w^2)/Q^2, w=2^43,q=1024,
and all n=1024 mask-coordinates match with probability p^n≈2^-10240. This is an ordinary KeySwitchGen randomness result, NOT a SNARG soundness bound.
**Rounding boundary caveat:** Source p16 canonical bit truncate outputs q rather than 0 for raw residue x∈[2^53,Q-1] (5 points); if insisting that the public output is the canonical Z_q representative, condition the two raw n+1-vectors on having no such coordinates. Union bound for this good event at least 1−10(n+1)/Q; actual one-sample gate test satisfies it. This separate top-five issue was NOT studied as a new hypothesis.

**Critical semantic limitation:** KeySwitch ciphertext phase is
 B_out−<s,A_out> = B_ACC − Σ selected e_(i,j,b_j) − z_i Σ_j 2^j b_j (modQ).
The two reconstructed integer sums differ by Q, so secret-dependent terms are IDENTICAL modulo Q. Phase difference is solely the change in KSK errors. This is **exact output ciphertext ambiguity**, NOT a demonstrated different plaintext, IND-CPA break, or real complete proof forgery.

## ONE actually executed exact test
Tested Q=2^53+5,n=q=1024,N=2048. Used a reused zero-plaintext LWE-shaped source input with an ordinary uniform Z_q^1024 mask, ternary secret containing 331 negatives/309 zero/384 positives, small nonzero encryption error, and nonzero ring coefficient z_i=3. Source c_tmp and all alpha_i are exactly zero; ACC ring mask forced zero algebraically. For one extracted zero coefficient, generated BOTH j=0..53 KSK branch masks as independent uniform vectors in Z_Q^1024, with valid nonzero small Gaussian-support errors. Unchanged other key selections represented by one fixed common aggregate, **not a full 2048-coefficient KSK materialization**. Verified ALL scalar BitDecomp Boolean/mod reconstruction, 54 Index branch choices, selected KSK body linear equalities, all 1025 output canonical Rounding reconstruction witnesses in each execution path. Used representative symbolic accumulator body 42 merely for an arithmetic example; no actual f_XOR(0) or RGSW evaluated. Different public output mask coordinates: **1024/1024**. Public bodies in this representative test 72 vs503. Raw phases 43 vs39, fully explained by selected KSK error sums −1 vs3. No top-five exception hit. The actual FHE.EvalGate complete matrix and PCS were NOT executed.

Reproducible local files successfully created and executed:
- /mnt/data/pvfhe_p24_self_xor_keygen_gadget_gate.py SHA256 b4d05ce8b0c7890f7bd287dea0c4bb1662d52d1b409225e9fa2b5e627c28fbb8.
- /mnt/data/pvfhe_p24_self_xor_keygen_gadget_results.json SHA256 7196e3af76c45c7466a44af6d651752373da7acd43353911efc1187ad1b6acbc.
- /mnt/data/PVFHE_P24_Self_XOR_ACC_ZeroMask_Generic_Keyswitch_Gate.md SHA256 fdb4f6ac0a25e9bc59d00d70a2a4518d92c72fa2ec4fe1f579135dcb4bf9fe48.

## End of iteration
**STATUS:** PASS honest, deterministic self-XOR ACC-trigger with independent ordinary KSK masks and a complete one-coefficient terminal gadget chain; FAIL P24 suspicion that alias event must be sampled rarely; UNCLEAR complete A/B/C compilation, actual Fiat–Shamir/PCS/SNARG proof, latest PDF, wrong plaintext and practical security effect.
**RESULT:** P23's remaining ACC output-distribution premise can be removed by a source-native c1=c2 XOR call, which fixes every extracted coefficient to zero for any ek. Three noncanonical source-valid bits can force a different deterministic public ciphertext output with overwhelming probability over original fresh uniform KSK masks. The ciphertext secret phase differs only through switching-key errors.
**NEXT_ACTION (P25 only on PI continuation):** ONE source-faithful final compilation/public-output binding gate: audit Appendix C.3 merge-of-identical-variable policy, Coeff-vs-KeySwitch BitDecomp wire sharing, final public-IO constraints and actual A/B/C/SNARG instantiation if source material available. If author compiler remains missing, classify complete SNARG acceptance HUMAN_REVIEW instead of asserting a forgery. Do not repeat mask-collision experiments; nested PCS proof remains PARK.
**STATE_UPDATE:** YES only new independent P24 file; NO edits to global STATE.md, parallel SHIP/vFHE or P01–P23.