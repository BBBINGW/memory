# PVFHE-P14 — Explicit augmented Ring-R1CS matrices and Appendix D private PCS arity

**Date:** 2026-10-15 Asia/Tokyo. **Independent PVFHE-P14 COMPLETED; P15 NOT STARTED.**
**STATUS:** PASS source-shaped 16x16 matrix-level algebra and typed private PCS points; UNCLEAR original author’s printed p28/29 arity, full FHE circuit and real PCS/SNARG/ROM/QROM. Do not claim original-paper bug or actual SNARG execution.

## Read-before-write

Read START_RESEARCH_SESSION.md (SHA 6235e9d376a8b143719a40178132f02a6a41d4f3), RESEARCH_PHILOSOPHY.md (49da3f7fa3e75f5025258cf525482ce4a7ab6867), AGENT.md (b3e73b2c7f852c05aa674dd97b632e9f99ac5f22), global STATE.md (6efa6a27e5b9a13402aa88ef81b8956e5f65d388; independent vFHE V31), P13 findings/pvfhe-P13-appdxD-witness-commitment-linkage-gate.md SHA 7286590014e7480cb8a0559cd36e1084aecc8de1 and P12 SHA bf6f17225b42d8415dd2fcaad74d5de8f1fb8f89. Destination P14 initially absent. No parallel/global state changed.

**Original primary:** Huang, Li, Mao, Zhang, Fully Homomorphic Encryption with Efficient Public Verification, IACR ePrint 2024/1764. Research MCP full 29-page paper SHA256 7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089, VERSION_UNVERIFIED. Inspected physical p12 Definition4.1, p15 Lemma4.4, p17 Theorem4.12, p27 AppendixC.3, pp28–29 AppendixD. Original PDF opened via web as text, but web screenshot of p28–29 FAILED cache miss and container retrieval failed DNS; source version/rendered formula parity unverified.

## One hypothesis / cheapest decisive test

**[HYPOTHESIS P14]** P13’s corrected same-PRIVATE-commitment masked-witness Y and original W/public IO can be compiled as concrete sparse A_new,B_new,C_new Ring-R1CS and multilinear matrix encodings. The mask link Yi=MiWi must be enforced at matrix level, P11 zero anchor uses the same private commitment, and P12 postchallenge private PC.Eval uses correctly typed private-only point coordinates.

**[FALSIFIER]** Explicitly construct a complete tiny square Ring-R1CS and its two-dimensional A/B/C multilinear encodings; verify rank-one constraints and off-Boolean matrix contractions. Set fake Y=0 while keeping nonscalar old W; if fake still satisfies rows, FAIL linkage. Compare input-arity of source p28 step12 vs p29 step13 and independently typed toy PCS; do not declare paper flaw without visual verification.

## Source details

Original Appendix D p28 step1 commits ONLY private tilde_z, while p29 step15 reconstructs full Z(u,t)=(1-u)tilde_z(t)+u public_(io,1)(t). P13 therefore placed added selector b INSIDE private branch; public IO remains in its original outer branch. Original AppendixD preprocesses THREE public matrix commitments CA,CB,CC for A,B,C, which MUST be regenerated for an augmented R1CS; our local SHA256 fingerprints are NOT lattice commitments.

Possible original notational issue: AppendixD p28 step12 prints private polynomial evaluation v=tilde_z(ry[1..]), while p29 step13 appears to call private PC.Eval with entire ry, though p29 step15 again distinguishes full ry[0] from private ry[1..]. Taking the formula literally, private polynomial has one FEWER variables than full interpolation. Could be padding/shorthand/PDF extraction. Rendered authoritative PDF unavailable: CLASSIFY UNCLEAR, not cryptographic source bug.

## Exact source-Q R1CS compilation and executed test

Work over the faithful two-factor CRT subalgebra F_Q×F_Q of the paper’s actual R_Q with Q=2^53+5, N=2048; e=(1,0) is idempotent nonscalar. Let old private W=(5,e,7,0); public IO padded P=(11,1,0,0); public mask M=(0,1,0,0); linked Y=(0,e,0,0), Y0 reserved public zero. Full length16 z=(W0..W3,Y0..Y3,P0..P3,0,0,0,0).

The PRIVATE committed polynomial W_aug(b,t)=(1-b)W(t)+bY(t) has 3 MLE variables (t0,t1,b). Full Z(u,b,t)=(1-u)W_aug(b,t)+u(1-b)P(t) has 4 (t0,t1,b,u), as in original AppendixD private/public LDE shape with one added private bit. Define 16x16 sparse matrices A_new,B_new,C_new. Eleven active 0-indexed rank-one rows (other rows zero):
  0: W0 * P1 = 5P1
  1: W1 * W1 = W1
  2: W2 * P1 = 7P1
  3: W3 * P1 = 0
  4: Y0 * P1 = 0
  5: Y1 * P1 = W1    <- CRITICAL MASK LINK
  6: Y2 * P1 = 0
  7: Y3 * P1 = 0
  8: Y0 * P1 = 0     <- ANCHOR ZERO
  9: P0 * P1 = 11P1
 10: (W0+W2)*P1 = 12P1.
Here P1=1 is the public constant coordinate, so these are genuine Ring-R1CS equations.

For each matrix M=A,B,C construct 8-variate multilinear encoding Mtilde(x,y)=SUM_ij M_ij eq(i,x)eq(j,y); and vector ztilde(y)=SUM_j z_j eq(j,y). Explicitly verify MLE(Mz,x)=SUM_j(SUM_i M_ij eq(i,x))*z_j, including off-Boolean and zero-divisor ring points. The following checks were ACTUALLY RUN with exact integer CRT-pair arithmetic:
- Original public/private split Z=(1-u)W_aug+u P_aug: 256/256 points (u,b,t0,t1 each from 0,1,2,3).
- Matrix A/B/C Boolean row/column coefficient reproduction: 768/768.
- Off-Boolean matrix-vector contractions: 21/21.
- Honest R1CS residuals: every row zero and 7/7 sampled multilinear sum-check weighted residuals zero.
- Fake masked Y_fake=0^4 with same W preserves original old rows and anchor but FAILS exactly row index5 with residual -e=(Q-1,0) !=0.
- Correct PRIVATE PC.Eval accepts 3-variable tail point; supplying FULL 4-variable full-IO challenge to private interpolant FAILS the typed local simulation. This identifies a possible notation mismatch rather than acceptance behavior of real CMNW.

Regenerated deterministic matrix encoding SHA256 fingerprints (NOT cryptographic commitments):
  A d7ccb8098414c583694aba98894be565b0d9d680977d84e8063cb8046eac6980 (12 sparse terms)
  B eb4653fa528ae7c0803fce461d3fbb10f91742a8fd5609b2dac9d960415acbf8 (11)
  C c1b0fe6732c91aa3638318af24ca122a1d28664ec976110678f3621d1e14e8d7 (6).

**Reproducible local artifacts actually created and executed:**
- /mnt/data/pvfhe_p14_matrix_lde_arity_audit.py SHA256 65927b9ba33fbc73908f37c3408d7e3d33a4d9019ff8efa6ee507bed452e2e69
- /mnt/data/pvfhe_p14_matrix_lde_arity_results.json SHA256 6afe46cf8243a3023ed8da78c1477500eb68c3818db1b924fc9e7ba928e184b3
- /mnt/data/PVFHE_P14_Augmented_R1CS_Matrix_LDE_Arity_Audit.md SHA256 72652b8ba7fb2e2d9addec0919231db3912f9b5e18f512271821f2fc0d944b1b

**Scope:** These are source-shaped TOY-SIZED full matrices, NOT a compilation of complete real FHE.EvalGate, actual lattice CA/CB/CC or witness PCS, sum-check proof transcript, SIS security, FS/QROM soundness or author code. End-to-end FHE correctness not proved.

## End of iteration

**STATUS:** PASS source-shaped matrix R1CS/multilinear algebra and privately typed point; FAIL malformed full-point/private-polynomial input in toy type model; UNCLEAR original printed step12–13 intent, actual complete SNARG and ROM/QROM.
**RESULT:** P13’s linkage survives an actual square 16x16 sparse Ring-R1CS and its A/B/C multilinear encodings: unlinked masked zero witnesses are detected by a real rank-one row, public IO is preserved, and the private PCS has correct tail arity. New public matrix commitments must be recomputed.
**NEXT_ACTION P15 only if PI continues:** One full-sized original source FHE witness constraint-count / augmented public-matrix-preprocessing and sum-check dimension feasibility gate, avoiding further CRT toys; or verify p28–29 source typed printed notation using available rendered original PDF. Concrete CMNW adaptive FS and QROM proof are separate OPEN problems.
**STATE_UPDATE:** YES only this independent P14 file; NO changes to concurrent global vFHE/SHIP or P01–P13.