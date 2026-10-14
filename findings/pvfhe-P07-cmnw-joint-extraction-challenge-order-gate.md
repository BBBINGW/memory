# PVFHE-P07 — CMNW same-commitment joint extraction: norm-slack and challenge-order gate

**Checkpoint:** 2026-10-14 (Asia/Tokyo), independent PVFHE P07 COMPLETED, P08 NOT STARTED.
**STATUS:** **FAIL** automatic implication of a secure same-commitment correlated double evaluation from the **published single-evaluation extractor + honest-shortness binding**; **PASS** exact parameter and challenge-order obstruction witnesses; **UNCLEAR/HUMAN_REVIEW** actual classical multi-statement joint extraction and QROM Fiat–Shamir composition. No CMNW/PVFHE break, no fabricated SNARG proof.

## Read-before-write / provenance / isolation
Read `START_RESEARCH_SESSION.md` SHA `6235e9d376a8b143719a40178132f02a6a41d4f3`, `RESEARCH_PHILOSOPHY.md` SHA `49da3f7fa3e75f5025258cf525482ce4a7ab6867`, `AGENT.md` SHA `b3e73b2c7f852c05aa674dd97b632e9f99ac5f22`, global `STATE.md` SHA `22d3d410ed2107be1a8fa0fde3f2fb9afc6e2a72` (parallel vFHE V26), and earlier `findings/pvfhe-P06-cmnw-correlated-two-opening-soundness-gate.md` SHA `f479b7c8f6c6be49cf8aabc294be5d5ccdc3dc99`, P05 SHA `68cbabb5594b54d496179934d78fb2352512caf0`. P07 target previously absent. **No edits to vFHE, SHIP, global state or other findings**.

**Primary papers:**
- Cini–Malavolta–Nguyen–Wee, *Polynomial Commitments from Lattices: Post-Quantum Security, Fast Verification and Transparent Setup*, CRYPTO 2024, IACR ePrint `2024/281`, https://eprint.iacr.org/2024/281, read via Research MCP full 52pp mirror SHA256 `a9be7b5c1e9024d2d0c03865978d7f3ea1ed941dce8883f93f9576ae46a73b73`, VERSION_UNVERIFIED; p12 Definition6 single-statement knowledge extraction, p13 Definition8 single public evaluation tuple `(C,x,u)`, p15 Theorem4 honest-opening binding, p22 Theorem2 extraction into enlarged relation, pp23–24 §6 multilinear PC and assumptions, pp39–42 Appendix B quantum collapsing/state recovery/rewind structure.
- Huang–Li–Mao–Zhang, *Fully Homomorphic Encryption with Efficient Public Verification*, ePrint `2024/1764`, 29pp mirror SHA256 `7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089`, VERSION_UNVERIFIED; p6 generalized Schwartz–Zippel, pp8–9 Ring-PC interface, p21 Lemma5.6/Theorem5.7 adaptation, p27 R1CS source relation. A web open of 2024/281 official ePrint PDF failed robots check, so primary PDF binary parity is unverified; 2024/1764 web PDF was accessible.

## ONE primary hypothesis / ONE decisive source-contract gate
**[HYPOTHESIS P07]** The published *single-evaluation* knowledge-soundness and SIS binding parameters directly guarantee that two extracted polynomials from the SAME prechallenge commitment under `PC.Eval(C,r,v)` and `PC.Eval(C,σ^{-1}(r),v')` are identical **without strengthening SIS norm bounds, explicit challenge ordering or extraction composition**.

**[FALSIFIER]** Compare exact CMNW extracted norm `β_*` with the SIS bound for TWO differing extracted openings, build a completely explicit small honest-norm vs enlarged-norm binding countermodel, and demonstrate the commitment-before-challenge necessity even with an ideal perfectly binding commitment. If either asserted implication is invalid, reject unqualified joint-security claim and identify minimum sufficient missing lemma (not a fresh toy Galois audit).

## Source facts and derived obstruction
CMNW Theorem2 (physical p22) extracts an opening in enlarged norm relation
```
   β_*=(2rκ)^ℓ β.
```
CMNW Theorem4 (physical p15) binds honest openings at norm β by reduction to SIS norm ≥2β. The §6 multilinear theorem (physical p24) prints a sufficient SIS assumption of the order `β'_source≥(2rλ)^ℓ β` with `κ=λ`. This is a *single-evaluation* theorem and does not explicitly state two related claims on one commitment.

If two extracted opening witnesses each have norm ≤β_*, the elementary difference reduction only guarantees `||f1−f2||≤2β_*`. Thus a clear **sufficient** SIS hardness assumption for the two-extracted-opening collision is
```
  β'_joint ≥2(2rκ)^ℓ β.
```
The displayed §6 threshold alone does not mechanically imply hardness at the factor-2 larger bound. A different extractor or tighter slack/binding argument might avoid it, but was not established. **This is an additional parameter condition for our extension, NOT a flaw in CMNW's published one-statement theorem.** Also source §6 theorem is stated over Z_q multilinear polynomials; PVFHE claims extension to R_Q; this portability is not independently re-proved here.

A genuine joint classical reduction also needs the committed polynomial to be FIXED **before** external identity-test challenge r. Binding of two extracted openings for ONE realized r does not by itself show extraction of an r-independent polynomial; a prechallenge extractor or rewinding/forking across different r values is needed. Original P05 promises commit-before-r, but that promise must be present and bound in the transcript.

## One executed exact countermodel gate
**Toy honest-shortness binding:** ideal deterministic `C=f mod 5`, short `|f|≤1` has unique openings among {-1,0,1}; larger extracted range `|f|≤3` admits distinct `f1=-2,f2=3` that both commit to C=3. This only refutes inference across norm ranges; **not** a CMNW/SIS attack.

**Source-parameter challenge ordering:** faithful idempotent CRT subalgebra `F_Q×F_Q` with Q=2^53+5,N=2048, nontrivial idempotent `e=(1,0)`, sigma factor swap. Take legal scalar exceptional set `E={(i,i):i=0,...,6}` (all pairwise differences units). For coefficient-noninvariant polynomial `Y_t(T)=e(T−t)`, twisted two-point check on r passes iff r=t. With an **ideally perfectly binding** commitment FIXED before r (t=3), test accepts **1/7**; if challenger chooses r first and a malicious prover thereafter commits separately to `Y_r`, it passes **7/7**, with both PC point evaluations individually HONEST. This is not an attack on P05's claimed precommit ordering; it establishes its indispensable soundness condition.

**Illustrative norm substitution:** symbolic (not real security params) `r=2,κ=8,ℓ=3,β=5` gives `β_*=163840` versus sufficient two-extracted SIS bound `327680`. No lattice hardness claim.

Actual executed Python `/mnt/data/pvfhe_p07_joint_extraction_norm_and_order_gate.py`, SHA256 `052cf31f529489fa27b7da6e9c31fecec7e28a08f8ff3a6d708155a72e754839`; exact results `/mnt/data/pvfhe_p07_joint_extraction_norm_and_order_results.json`, SHA256 `f07ffd3a60b12c29a64e83b659addbc2af0992ae44ac52e5f86de28c3411c2ea`; complete report `/mnt/data/PVFHE_P07_CMNW_Joint_Extraction_Challenge_Order_Gate.md`, SHA256 `0717b4cb49491b4a895de055082252360db53316a3deca7ee3ad4efdae853cc9`. No executed CMNW PCS, SIS collision, full R1CS, quantum extractor or FS.

## Proof-status clarification
The conditional *classical resettable* outline is: fix same commitment prefix, use independently sampled INTERNAL CMNW verifier coins to extract valid openings for both related public evaluation statements, use SIS binding at `2β_*` to identify them, and require pre-r fixation (or external-r forking with quantitative loss) before applying source Schwartz–Zippel to `D(T)=Y(T)−σ(Y(σ^{-1}(T)))`. This is a possible proof plan **not a completed quantitative classical joint extractor theorem**. Related public query points do not imply independent polynomial-identity tests. Quantum adversarial state restoration, multi-proof adaptive composition, and ROM/QROM domain-separated FS security are also OPEN; CMNW Appendix B single-protocol proof cannot be invoked twice without justification.

## End of iteration
**STATUS:** FAIL automatic source-theorem extension; PASS exact binding-slack/challenge-order necessary-condition falsifiers; HUMAN_REVIEW/UNCLEAR full joint classical/QROM proof.
**RESULT:** P05 remains a mathematically plausible two-point Ring-PCS extension, but original one-evaluation extraction does not directly close it. For the two-opening binding approach one needs at least a suitably strong SIS assumption through `2β_*`, commitment-before-r, and explicit joint extraction/forking. No source vulnerability or QROM security attack claimed.
**NEXT_ACTION (PVFHE-P08 only on PI continuation):** ONE formal *classical resettable* same-C joint extraction + independent precommit r lemma with quantitative loss, prove or falsify under `2β_*` SIS, then decide if quantum/QROM attempt is worth cost. Do not rerun idempotent/shortness toy checks. If cannot establish the classical lemma, PARK PCS proof integration and hand over exact missing obligation.
**STATE_UPDATE:** YES new independent P07 only; no edits to shared STATE.md, parallel SHIP/vFHE or P01–P06 findings.