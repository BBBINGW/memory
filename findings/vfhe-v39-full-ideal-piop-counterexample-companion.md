# vFHE V39 Companion — Complete ideal Figure 1 GP transcript for mirror-specific CRT mixed digit

**2026-10-15. COMPANION to AUTHORITATIVE V39** findings/vfhe-v39-remark49-official-edition-source-gate.md. This is NOT V40 and does not advance global FHE I192. Source latest official Feb2026 PDF is SOURCE_VERSION_GATED; this finding only refers to the 52-page inspectable mirror.

## Extra decisive test beyond canonical V39's CRT digit projection

Canonical V39 main already proves that inspected 52-page ePrint2025/286 Appendix E.2 physical p48, after p24 Remark4.9 fieldwise pmin fix, contains false implication: global ring out-of-table digit ⇒ some native field out-of-table. This companion proves more: one actual ring-invalid h and legitimately allowed Rq-valued read_ts, final_cts grand-product witness satisfy **EVERY** Figure1 GP product identity for ALL ring-valued verifier random σ,τ. Constructing four honest-by-definition grand-product trees makes Boolean recurrence and corresponding source sumcheck equations satisfiable without a malicious polynomial-commitment extractor. Thus the exact ideal range PIOP as described in the 52p mirror has a source-shaped false lookup transcript. This is a restatement/strengthening of archival V17–V23, not a novelty claim or a completed malicious Fiat–Shamir SNARK execution.

## Source and edition [FACT]

- Official ePrint landing https://eprint.iacr.org/2025/286 currently says revised **2026-02-16** and explicitly **Fixed a flaw in the proof of Theorem 4.8**. No current official PDF binary with verified SHA. Container official-host DNS failed; web direct PDF returned STALE 50-page indexed edition; See all versions was not fetchable. Screenshot of indexed PDF was attempted and yielded internal error. Hence DO NOT identify accessible 52p mirror with official newest.
- Research MCP source_kind github-mirror, fixed 52pp,836746B,SHA256 **29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19**, VERSION_UNVERIFIED, pp20–24 §4.3 eq21–26 / Figure1 / Theorem4.8, pp46–49 AppendixE.2 (especially p48 invalid CRT projection claim), pp50–52 F.1/F.2; author names Cascudo, Costache, Cozzo, Fiore, Guimarães, Soria-Vazquez.
- Old web-indexed 50pp p45 Appendix E.2 applies Lemma4.6 directly in ring; the 52pp mirror restricts lemma to fields and adds a pmin CRT argument that fails at the diagonal-membership step. Neither edition is proven to be the authentic PDF served today.

## Exact source-format full counterexample [DERIVATION]

Choose N4,d2,Rq=Z377[X]/(X^4+1), prime p13=1+4*3 and p29=1+4*7, two irreducible quadratic factors EACH: F13[x]/(x²-5),F13[x]/(x²-8),F29[x]/(x²-12),F29[x]/(x²-17); 5,8 and12,17 are nonsquares in corresponding prime fields. Let β4, ellstar3, H=2^ellstar=8, so H<13 and β<13 as required by repaired Remark4.9.

Global lookup table is t4={0,1,2,3}⊂Rq. Set all Boolean inputs h(i)=e=261 ∈Rq. Global h(i)∉t4. Yet e mod13=1 in BOTH F13² factors and e mod29=0 in BOTH F29² factors: locally legal but DIFFERENT table indexes.

Submit first round ring oracle read_ts(i)=i∈{0,1,2,3,4,5,6,7} and final_cts(j)=[182,203,0,0] for j=0..3. These CRT-lift respectively to p13 field counts [0,8,0,0] (all reads of digit1), and p29 field counts [8,0,0,0] (all reads of digit0). Figure1 does NOT independently assert each first-round counter lies in a globally diagonal integer subset; arbitrary Rq-valued MLE oracle final_cts is admitted.

Source memory-checking multisets of ring-valued pairs are:
 WSt={(j,0):j=0..3},
 WSh={(e,i+1):i=0..7},
 RS={(e,i):i=0..7},
 S={(j,final_cts(j)):j=0..3}.
Over the original Rq pairs the union WSt∪WSh != RS∪S. But for each native prime/extension field the projected equality is EXACT, not probabilistic: if projected e=u∈{0,1}, projected WSt has (u,0), WSh has (u,1),(u,2),...,(u,8), RS has (u,0),(u,1),...,(u,7), and S has (u,8); all other table entries occur equally on each side. By CRT injectivity, for ALL ring σ,τ (including NONSCALAR extension-field components), the two Figure1 grand-product polynomials are IDENTICALLY equal:

  (∏_{j=0}^3(j−τ)) · (∏_{i=0}^7(e+σ(i+1)−τ))
  = (∏_{i=0}^7(e+σi−τ)) · (∏_{j=0}^3(j+σ final_cts(j)−τ))

in Rq[σ,τ].

Construct all four GP polynomial oracle tables as true partial binary subtree products over Rq for those leaf values; the Boolean grand-product recurrence constraints all hold, and source Figure1 sumchecks have valid zero sums on cube, while the TRUE lookup language Rrange is violated. This holds at ideal oracle/PIOP layer. We have NOT generated Merkle Brakedown native PCS proofs, Fiat–Shamir attack transcripts, proof-composition security analysis, or an exploit of a byte-authenticated current official edition.

## Exact reproduction [EXPERIMENT]

Self-contained standard-library script checks four quadratic factors' irreducibility, source pmin restrictions, CRT counters, every native projected multiset, original ring multiset inequality, and EXHAUSTIVELY all σ,τ constant ring representatives in Z377²: **142129/142129 grand-product equalities hold**. Independent p13² (169) and p29² (841) pairs also pass. Explicit four source binary GP trees at σ5,τ9 satisfy every Boolean recurrence and root identity. The CRT argument above lifts equality to nonconstant ring challenge values without exhaustive enumeration of all such ring elements.

Executed TWICE identically:
 - Python /mnt/data/vfhe_v39_revision_scope_crt_counterexample.py SHA256 d0a3db1c886f0c5798b62a6158fcb9d6c1a23fca4f7ea2da43414179a6bf1fb7
 - JSON /mnt/data/vfhe_v39_revision_scope_crt_counterexample.json SHA256 43e55a76e7dc786f504eeefd37e7033abb81dc2570592257cba0bf7bb5b23ff2
 - Markdown full report /mnt/data/VFHE_V39_Source_Revision_Identity_and_CRT_Counterexample_2026_10_15.md SHA256 7976fdbb03e38b5018c6b792e4ea444fe0f8b832d467c6eb39675eba5b0d778d.

## Status and preservation

**PASS** complete mirror-defined ideal lookup transcript counterexample and explicit failure of revised-looking p48 global-to-field inference. **UNCLEAR/SOURCE_BLOCKED** authentic February2026 full official PDF, final real-world SNARK soundness/security impact; no published erratum or deployed exploit claim. It is SAME V39 source and same mechanism as main V39, not an independently novel second iteration.

**Keep AUTHORITATIVE STATE:** V39 COMPLETED, V40 NOT STARTED, HUMAN_REVIEW/SOURCE_VERSION_GATED. User/PI should supply actual current official PDF unmodified bytes for SHA pin and re-audit of Theorem4.8 Appendix E.2 and Figure1/F.2; or explicitly choose another source-complete research target. Do not spend iterations on speculative large generic BP++ wrappers or contact/disclose to authors autonomously. GLOBAL I192 FROZEN; other research branches untouched.
