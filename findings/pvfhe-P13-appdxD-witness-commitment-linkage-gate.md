# PVFHE-P13 — Appendix D source witness commitment linkage gate

**2026-10-15 Asia/Tokyo. P13 COMPLETED; P14 NOT STARTED.**
**STATUS:** PASS conditional source-interface repaired embedding; FAIL naive reuse of the public selector and any unlinked masked-value scheme; UNCLEAR actual compiled SNARG/PCS, current original PDF equation rendering and ROM/QROM security.

## Read-before-write

Read START_RESEARCH_SESSION.md SHA 6235e9d376a8b143719a40178132f02a6a41d4f3, RESEARCH_PHILOSOPHY.md SHA 49da3f7fa3e75f502525482ce4a7ab6867, AGENT.md SHA b3e73b2c7f852c05aa674dd97b632e9f99ac5f22, global STATE.md SHA 6efa6a27e5b9a13402aa88ef81b8956e5f65d388 (separate concurrent vFHE V31), P12 SHA bf6f17225b42d8415dd2fcaad74d5de8f1fb8f89, P11 SHA 165dfc36f7ba9914561ebe93ef5ff113316b083c and P05 SHA 68cbabb5594b54d496179934d78fb2352512caf0. Destination absent. NO edits to shared state or other research branches.

**Primary source:** Huang–Li–Mao–Zhang, Fully Homomorphic Encryption with Efficient Public Verification, ePrint 2024/1764, full 29-page Research MCP PDF SHA256 7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089, VERSION_UNVERIFIED. Inspected physical p12 Definition4.1, p15 Lemma4.4/4.5, p16 Lemma4.11, p17 Theorem4.12, pp27–29 AppendixC.3/D. Cross-checked PDF via web open/text and attempted screenshots physical pp12,28,29; screenshots failed CACHE MISS. Apparent PDF text/arity discrepancy unverified visually.

## ONE primary falsifiable hypothesis and ONE decisive check

**[HYPOTHESIS P13]** Original AppendixD's commitment to PRIVATE witness polynomial tilde_z and verifier-computed PUBLIC io branch can accommodate one augmented private witness containing BOTH old FHE witness W and Galois masked reconstruction values Y, with exact ordinary Ring-R1CS linkage and a public-zero prechallenge anchor, without a distinct unlinked commitment or corrupting io.

**[FALSIFIER]** Inspect which polynomial source actually commits and the source public/private interpolation, then perform source-shaped MLE + mask-copy R1CS check. If Y can be faked as zero and pass added rows, or if Y must occupy the pre-existing public selector, the design fails.

## Source facts and necessary correction [FACT/DERIVATION]

Definition4.1's full R1CS z=(io,1,w) is reordered by source AppendixD into an interpolated PRIVATE part tilde_z and verifier-known PUBLIC part (io,1). AppendixD physical p28 step1 commits C=PC.Commit(pp,tilde_z), NOT a full private/public vector. Physical p29 step15 computes:
   Z(u,t)=(1-u)*tilde_z(t)+u*public_(io,1)(t).
Thus outer u=1 is already PUBLIC IO. Earlier P05 informal use of Z_aug(1,r)=Y(r) is invalid IF this is the same outer selector; it would overwrite public IO. That is a defect in our original integration sketch, NOT an original-paper flaw.

**Repaired ONE-private-commitment layout:** add an INNER private selector b. Let W(t) be old private interpolation; Y(t) new mask values, P(t) original public (io,1). Define:
   W_aug(b,t)=(1-b)*W(t)+b*Y(t)
   P_aug(b,t)=(1-b)*P(t)+b*0
   Z_new(u,b,t)=(1-u)*W_aug(b,t)+u*P_aug(b,t).
Only W_aug is privately committed under ONE C; source public/private interpolation remains exactly the same form after one extra coordinate. Use power-of-two padding and a reserved Y_0=0.

**Actual constraint linkage, not trust:** choose public selector coefficients M_i in {0,1} for actual original private BitDecomp reconstruction variable positions (and reindex if necessary). For each i append sparse Ring-R1CS row
   (Y_i)*(1)=M_i*(W_i).
Append fixed zero row (Y_0)*1=0. This is source Lemma4.4-valid ring arithmetic. Original computation constraints must stay in the instance with every old W and public IO wire reindexed; new rows increase witness/constraints by O(m) and must enter the same R1CS sum-check. Original AppendixD also uses PUBLIC preprocessing commitments CA, CB, CC for the matrices' multilinear encodings, so all three must be REBUILT for A_new/B_new/C_new. This is essential and not simulated by merely appending C.

**PCS interfaces:** P11 prechallenge full-opening anchor uses point (b=1,t=0) in private W_aug commitment, value 0; P12 postchallenge one PC.Eval(C,(b=1,t=r),v) uses r in its large sigma-fixed exceptional set and verifier checks v=sigma(v). Neither requires a second independent witness C.

**UNCLEAR printed source type mismatch:** AppendixD p28 step12 prints v=tilde_z(ry[1..]), but physical p29 step13 prints PC.Eval(C,ry,v,mu2), with full ry of dimension log m rather than tail ry[1..] of private interpolant. Research MCP extraction and original PDF web text agree; rendered screenshot unavailable. The natural typed call uses private tail ry[1..]. This is a possible notational typo/reading ambiguity, NOT a confirmed author proof error or attack. P14 must settle from rendered authoritative source before adverse claims.

## ONE minimal exact executed source-Q algebraic compiler gate [VERIFIED]

Used actual Q=2^53+5 and faithful CRT subalgebra F_Q × F_Q within R_Q=F_Q[X]/(X^2048+1); sigma exchanges factors. Let e=(1,0) be nonscalar idempotent. Original W=[5,e,7,0], public P=[11,1,0,0], public selector M=[0,1,0,0], linked Y=[0,e,0,0]. New privately committed polynomial coefficient vector W_aug=W||Y length8, public P_aug=P||0^4 length8, full Z_new length16. All 4 link rows Y_i*1=M_iW_i PASS; zero anchor in masked branch PASS; original private and original PUBLIC selector branches preserved exactly at all Boolean coordinates. For ALL 4^4=256 challenge quadruples u,b,t0,t1∈{0,1,2,3}, exact modulo-Q multilinear interpolation obeys Z_new=(1-u)W_aug+u P_aug.

**Decisive negative control:** If no mask-link rows are added, prover can set Y_fake=0^4 even though W contains nonfixed e. Then anchor and EVERY sigma test PASS, demonstrating the unsoundness of an UNLINKED auxiliary commitment. With explicit row i=1, the fake fails 0≠e. Honest Y's nonscalar e correctly fails sigma check at target vertex; for tiny scalar E={0,1,2}^2 the one-point test passes 5/9, consistent with generalized degree2/|E| error, NOT a security parameter.

Private PCS arity is 3 (b,t0,t1), while source full interpolation arity is 4 (u,b,t0,t1). This directly illustrates source AppendixD step12/13 possible mismatch. All algebra checked exactly. NO real CMNW implementation, fully materialized FHE R1CS matrix, sum-check/SNARG proof transcript, SIS estimation, or ROM/QROM extraction was run.

**Actual artifacts**:
- /mnt/data/pvfhe_p13_appendix_d_witness_link_gate.py, SHA256 e24cef8d32066688ec576bbe23793398384a8f8eee17e204b8bec0e68b2ef98b.
- /mnt/data/pvfhe_p13_appendix_d_witness_link_results.json, SHA256 48d51829c48a5d3d77ec3f1b552a601ab255157f780a840896523c4385d5076d.
- /mnt/data/PVFHE_P13_AppendixD_Witness_Commitment_Linkage_Gate.md, SHA256 b82b8964bf3a2777253ea2173e31df5b52ac3c476e06bcbbe4a99c6a650e13c1.

## End of iteration

**STATUS:** PASS corrected private-only shared PCS witness/mask/anchor algebra; FAIL naive P05 outer selector replacement and unlinked Y; UNCLEAR source printed PCS evaluation-point arity, full transformed matrices and commitments, real security.
**RESULT:** One extra selector WITHIN source private witness and source-compatible explicit Y_i=M_iW_i rows bind masked values to original computation witness, preserving the original public IO. Public A/B/C matrix-encoding commitments MUST be regenerated. Algebraic integration possible with one private commitment; not an actual verified SNARG yet.
**NEXT_ACTION PVFHE-P14 only upon PI continuation:** ONE complete source-typed A_new/B_new/C_new matrix and AppendixD low-degree interpolation gate, with source step12/13 private arity audit and authoritative rendered PDF verification. If visual edition unavailable, keep printed arity issue UNCLEAR, not a declared paper bug. Classical ROM/QROM and SIS security remain separate open obligations.
**STATE_UPDATE:** YES this independent P13 file only; no edits to global or parallel SHIP/vFHE STATE.md, or P01–P12.
