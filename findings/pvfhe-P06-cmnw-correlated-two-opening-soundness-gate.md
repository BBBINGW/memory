# PVFHE-P06 — CMNW24b correlated two-opening knowledge-soundness gate

**2026-10-14 (Asia/Tokyo). Independent P-series: P06 COMPLETED; P07 NOT STARTED.**
**STATUS:** **UNCLEAR/HUMAN_REVIEW** sound composition of the P05 two-point extension in the quantum/Fiat–Shamir model; **PASS** precise *conditional* classical binding/extraction → identity-test argument; **FAIL** treating two related evaluations as independent SZ tests or treating original single-instance quantum theorem as already proving joint security. NOT a full SNARG attack or secure repaired system.

## Read before write and sources

Read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md and independent global STATE.md (SHA f9bd09a0b1e03deed668b3c57e877c32cdb15727; concurrent vFHE, DO NOT EDIT); previous findings/pvfhe-P05-ring-pcs-galois-inversion-proof-gate.md SHA 68cbabb5594b54d496179934d78fb2352512caf0 (P05 is math/source-interface-only, not production secure), and P04 SHA 004f4e3904e3e65c2c46cd194b64a56670cdf3fd.

**Actual primary papers checked:**
1. Huang–Li–Mao–Zhang, *Fully Homomorphic Encryption with Efficient Public Verification*, IACR ePrint **2024/1764**, 29pp Research MCP full mirror SHA256 **7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089**, **VERSION_UNVERIFIED**; pp8–9 Definition2.5 (Ring-PC commit/open/eval), p6 Lemma2.3 generalized SZ, p21 Lemma5.6/Theorem5.7 (adapt CMNW24b to ring R1CS).
2. **Correct identified source [CMNW24b]:** Valerio Cini, Giulio Malavolta, Ngoc Khanh Nguyen, Hoeteck Wee, *Polynomial Commitments from Lattices: Post-Quantum Security, Fast Verification and Transparent Setup*, CRYPTO 2024, IACR ePrint **2024/281** https://eprint.iacr.org/2024/281; acquired **all 52 physical pages** via Research MCP, mirror PDF SHA256 **a9be7b5c1e9024d2d0c03865978d7f3ea1ed941dce8883f93f9576ae46a73b73**, **VERSION_UNVERIFIED**. Read physical pp12–13 Definition6 (knowledge soundness) / Definition8 (per evaluation statement), p15 Theorem4 (SIS-based binding), p22 Theorem2 (per-instance extraction with enlarged norm and error), pp23–24 §6/Theorem4 (multilinear polynomial evaluation), pp29–31 explicit protocol (already uses sigma^{-1} for coefficient-inner-product conversion), pp39–42 AppendixB (single-protocol quantum extraction, collapsing, state restoration; B.3 says some lifting arguments require non-adaptive extractor challenge queries). Official ePrint PDF web URL is robots-denied, mirror URL cache miss for screenshot; **rendered/latest edition has not been verified**. The external CRYPTO 2024 bibliographic listing confirms the 2024/281 paper identity.

## ONE primary falsifiable hypothesis + minimum gate

**[HYPOTHESIS P06]** Original CMNW24b Theorem2/Definition8 for a **SINGLE** point evaluation automatically implies P05's *same-commitment, adaptively related TWO point queries* \`Y(r)\` and \`Y(σ^{-1}(r))\` are **composably knowledge-sound including quantum Fiat–Shamir**, with no new joint extraction/composition theorem, and two evaluation openings can be counted as two independent polynomial-identity tests.

**[FALSIFIER]** Read CMNW source's precise single-statement knowledge extraction relation, binding/extraction parameter slack, adaptive/quantum assumptions and its actual §6 multilinear PC. Construct minimal exact source-ring CRT challenge instance distinguishing two correct evaluations from two independent identity tests. Determine exactly what theorem would still need to be proved before saying P05 is a secure extension.

## Primary facts from the two papers [FACT]

- CMNW24b Definition8 p13 proves knowledge for **one** tuple \`(ppCM,C,x,u)\` and a witness \`(f,st)\` satisfying \`Open(ppCM,C,f,st)=1 ∧ f(x)=u\`. Definition6 p12 extracts for one public statement from a stateful prover.
- CMNW p15 Theorem4 gives computational commitment binding under SIS; p22 Theorem2 extracts an opening with **enlarged norm/slack** and nonzero knowledge error. For joint claims binding must hold at the resulting extracted norm, not merely honest norm.
- CMNW §6 p23–24 explicitly handles multilinear polynomial evaluation with arbitrary public ring evaluation coordinates (supports both \`r\` and \`σ(r)\` individually); available as a per-evaluation interface. Their protocol p31 internally employs sigma^{-1}, proving automorphism arithmetic is familiar to underlying PCS implementation; **this is NOT a proof of the proposed pair relation**.
- Appendix B p39–42 quantum knowledge extraction uses last-round collapsing, state repair and non-adaptive internal query structure; the published statement does **not** explicitly prove same-commitment joint extraction for two related *public evaluation statements*, nor P05's QROM FS composition. Distinguish public correlated points from the independently sampled **internal PCS verification coins**.
- Upstream PVFHE §2.4/§5.3 merely instantiates these PC capabilities in ordinary Ring-R1CS, not a built-in cross-CRT Galois relation. No implementation/security theorem for this extra check found.

## Conditional construction and binding reduction [DERIVATION]

P05 commits to one augmented witness multilinear polynomial \`Y(T)=Σ_I y_I T^I\` **BEFORE** sampling \`r←E^s\`. Its two claimed evaluations are on the **same** C:
\`\`\`
 v = Y(r),        v' = Y(σ^{-1}(r)),
 test v = σ(v').
\`\`\`
Define \`D(T)=Y(T)-σ(Y(σ^{-1}(T)))=Σ_I(y_I−σ(y_I))T^I\`. If a y_I is not σ-invariant then D≠0 with degree≤s; exceptional-set Schwartz–Zippel yields \`Pr[D(r)=0]≤s/|E|\`.

A **conditional classical composition** would proceed: jointly extract valid openings \`(f1,st1)\`, \`(f2,st2)\` for the two accepted statements. Because both open SAME C, an SIS binding reduction forces \`f1=f2=f\` except negligible (assuming the enlarged extraction slack is explicitly covered). Hence both v,v' are genuine evaluations of ONE f, and residual false accept is governed by D_f(r). With actual joint extraction security this gives
\`\`\`
 Pr[false relation accepted] ≤ s/|E| + ε_joint-extract + ε_binding.
\`\`\`
One cannot simply replace \`ε_joint-extract\` with \`2ε_single\` or infer post-quantum QROM security from the per-instance CMNW theorem WITHOUT a composition proof: extraction may require rewinding stateful adversaries, different transcript scheduling, and a carefully chosen post-commit random point r. Domain separation for the two Fiat–Shamir subprotocols and transcript binding to C/r/the relation are additional obligations. This is an **unproven conditional reduction**, not claimed as a full theorem for the actual CMNW protocol.

## ONE actually executed minimal correlation gate

Working in the **faithful two CRT factor subalgebra of actual Q,N** (Q=2^53+5,N2048): represent e=(1,0), sigma swaps factors. The tiny set \`E={(0,0),(1,1),(2,3)}\` is a valid exceptional set (all pairwise differences units). Choose honestly committed multilinear polynomial \`Y(T)=eT\` with invalid Galois-invariant coefficient \`σ(e)≠e\`.
- r=(0,0): \`Y(r)=σ(Y(σ^{-1}(r)))\` TRUE.
- r=(1,1) or (2,3): FALSE.
- All evaluations are honest; nonetheless false relation accepted **1/3**, the one-variable \`1/|E|\` bound. It is WRONG to treat two correlated point openings as two independent identity trials and claim \`(1/3)^2=1/9\`. The second query point may not be in E; PCS interface accepts arbitrary ring points while the **single random challenge** comes from E.

**Actually executed Python:** \`/mnt/data/pvfhe_p06_correlated_eval_security_gate.py\`, SHA256 \`ffee5245a212308d7086b59c1d34b94b21f109b80520dbaeb3c15449f18817d8\`.
**JSON:** \`/mnt/data/pvfhe_p06_correlated_eval_security_results.json\`, SHA256 \`a76e64024ee44ea5832e5c9dd956e540e7c417b29a1e1c325898fab324438ed0\`.
**Full readable report:** \`/mnt/data/PVFHE_P06_CMNV_Two_Point_Knowledge_Soundness_Audit.md\`, SHA256 \`6635e391ba8b974eb4ba134b107fc91b801886a46f1a25b2c3112e8565af6845\`.
Test is exact ring arithmetic for point-correlation ONLY: **no executed CMNW PCS, SIS instance, quantum extraction, full augmented witness SNARG nor Fiat–Shamir transcript**. Tiny E does not claim production security.

## Research judgment / end of iteration

**STATUS:** **UNCLEAR/HUMAN_REVIEW** real correlated joint-proof security/QROM composition; **PASS** math + conditional classical extract-both/binding mechanism; **FAIL** alleged automatic coverage by CMNW single-evaluation security and independence-squared soundness shortcut.
**RESULT:** P05's twisted proof extension is still plausible with existing CMNW interface, but its **cryptographic missing lemma is specific**: composable *joint* extraction on same commitment for adaptively related public points with correct SIS slack and non-interactive transcript domain separation. CMNW's built-in Galois arithmetic does not provide that theorem.
**NEXT_ACTION — P07 ONLY on PI continuation:** Prove or falsify ONE **two-statement joint extraction lemma** for CMNW24b from its concrete proof extractor (first classical resettable, then quantum/QROM only if sound). Explicitly settle transcript order, challenge independence INSIDE PCS, public-point correlation and β*/binding parameter. If the proof cannot be established, PARK P05 as an unverified algebraic repair; do not assert publishable secure vFHE yet.
**STATE_UPDATE:** YES ONLY new standalone P06 note, NO modifications to shared vFHE/SHIP global STATE.md, prior P01–P05 or backlog.