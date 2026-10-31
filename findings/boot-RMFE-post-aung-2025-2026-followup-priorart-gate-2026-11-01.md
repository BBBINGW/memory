# BOOT RMFE Post-Aung 2025–2026 Follow-Up Prior-Art Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 15/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Pending native task boundary

Authorized native task:

\`BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01\`

remains UNKNOWN / BACKGROUND.

This turn does not:
- inspect or assume its result;
- modify its source/workdir/binary;
- resubmit it;
- start another heavy native task.

## Read-before-write authority

Current durable authority at turn start:

\`BBBINGW/memory main@bba1b8f80332198a855e2ae4187823483931e334\`.

Relevant durable prerequisites:
- high-level direct-RMFE-MultKey novelty already killed by Aung 2025 future work;
- joint rank-5 recovery novelty capped by Aung Proposition 3;
- surviving candidate novelty narrowed to obstruction-aware post-raw delayed fusion + one common reconstruction;
- Turn 12 established odd-prime family generality;
- Turn 14 established source-faithful internal implementability.

## Primary hypothesis

A public 2025–2026 follow-up may already have solved Aung's stated future-work problem or an equivalent mechanism:

\[
\text{direct RMFE-packed MultKey}
\]

or, more specifically,

\[
\text{branchwise nonlinear rounding}
\to
\text{post-rounding merge}
\to
\text{one common boot-key reconstruction}.
\]

Falsifier:
find a public post-Aung work that implements or derives the same semantic ordering, even under different terminology.

## Search scope

Fresh public-web search was performed through 2026-11-01 across:
- exact Aung title and citation searches;
- RMFE / reverse multiplication-friendly embedding / FIMD + bootstrapping;
- direct/packed MultKey;
- after/post modulus-switch merge;
- common bootstrapping-key merge;
- rawModSwitch / recryptEkey phrase searches;
- 2025 and 2026 IACR ePrint title indices;
- visible 2026 works of the Aung coauthor cluster;
- a 2026 general FHE-bootstrapping survey.

This is a targeted collision search, not a proof that no unpublished, non-indexed, differently-termed, or private work exists.

## 1. Aung remains the direct source of the open problem

Aung et al., PKC 2025 / ePrint 2025/350, concludes that it remains to be seen whether the MultKey portion can be performed directly on the RMFE-packed ciphertext to avoid executing MultKey multiple times on split ciphertexts.

Thus the high-level research problem is still prior-disclosed.

The current novelty question is only whether a later work closed it in the same way.

## 2. 2026 IACR ePrint title index has no RMFE/FIMD follow-up title

The complete public 2026 ePrint title index, as crawled on 2026-11-01, contains no title match for:
- \`RMFE\`;
- \`Reverse Multiplication\`;
- \`FIMD\`.

This is useful negative evidence but weak:
a paper can use RMFE without putting the term in its title.

The 2025 title index contains:
- Aung 2025/350, \`Bootstrapping with RMFE for Fully Homomorphic Encryption\`;
- 2025/1538, \`Evaluating Ascon in Secure Multi-Party Computation using Reverse Multiplication-Friendly Embeddings\`, which is MPC/symmetric-circuit evaluation rather than FHE bootstrapping.

No later 2025 title collision with direct RMFE bootstrap was identified.

## 3. Visible citation-forward results do not collide

ResearchGate currently surfaces two citing works for the PKC 2025 chapter.

### Anti-MT selective refresh, 2026

\`AsFHEP-Anti-MT Bootstrapping: A Selective Ciphertext Refresh ...\`

Its stated contribution is deciding which ciphertext segments to refresh and recording audit metadata.

It explicitly does not redesign/accelerate the underlying bootstrapping primitive.

No collision with RMFE packed MultKey or post-rounding branch fusion.

### Better GBFV Bootstrapping, Geelen–Vercauteren

Public 2025/1104 / 2026 CiC work:
\`Better GBFV Bootstrapping and Faster Encrypted Edit Distance Computation\`.

Its mechanism converts GBFV encoding toward regular BFV and moves SlotToCoeff work into the GBFV domain.

The public abstract/poster describes:
- GBFV-to-BFV encoding conversion;
- ModUp/Permute/Trace stages;
- improved GBFV SlotToCoeff.

It does not describe:
- RMFE split branches;
- branchwise rawModSwitch;
- carry-compensated merging;
- common recryptEkey reconstruction.

So it is adjacent BGV/BFV bootstrapping prior art but not a direct collision.

## 4. Visible 2026 work by overlapping Aung coauthors does not expose the same mechanism

### Fully Homomorphic Encryption on the Ring of Gaussian Periods

He, Ling, Shi, Tan, Wang, Yang, CT-RSAC 2026 / ePrint 2026/927.

Public abstract:
- starts from GBFV/subring methods;
- changes the plaintext-ring/subring construction using decomposition rings / Gaussian periods;
- targets dimension and parameter flexibility.

No public abstract/search evidence of RMFE-packed MultKey, branchwise rounding fusion, or HElib recryptEkey merging.

### Laurent Polynomial-Based Linear Transformations for Improved Functional Bootstrapping

Ling, Tan, Wang, Yang, ACISP 2026 / ePrint 2025/957.

Public abstract/indexed text:
- targets BFV-based functional bootstrapping;
- uses Laurent-polynomial encoding;
- optimizes a linear transformation / inner-product stage;
- generalizes to prime-power plaintext moduli;
- supports multi-valued functional bootstrapping.

Searches combining this title with RMFE / MultKey did not expose a collision with the current mechanism.

This is important adjacent prior art for "merge/fuse linear phases", but not for the current nonlinear raw-rounding boundary.

## 5. 2026 RMFE activity found outside this FHE-bootstrap problem is non-colliding

A 2026 AAAI work:
\`Scalable Privacy-Preserving Neural Network Training over Z_{2^k} via RMFE-Based Packing and Mixed-Circuit Computation\`

uses RMFE for secret-sharing/MPC packing over Galois rings.

It is not an FHE bootstrapping construction and does not close Aung's direct-MultKey problem.

Likewise, 2025/1538 uses RMFE for MPC evaluation of Ascon, not BGV/FHE bootstrapping.

These results show that RMFE remains active in secure-computation literature, but they do not collide with delayed fusion.

## 6. 2026 general bootstrapping survey gives no direct collision signal

A 2026 open-access survey,
\`A survey of optimization techniques for bootstrapping algorithms in FHE\`,
contains no searchable HTML match for:
- RMFE;
- FIMD;
- Aung.

This does **not** prove novelty.

It only shows that the Aung RMFE bootstrapping line is still niche enough not to appear in that survey's indexed treatment, so one should not rely on general survey coverage to close prior art.

## 7. Mechanism-level phrase searches

Targeted searches for combinations such as:
- "after modulus switching" + bootstrapping key + packed;
- "post modulus switching" + bootstrapping key;
- "common bootstrapping key" + BGV packed;
- "packed MultKey";
- "direct MultKey" + RMFE;
- "merge" + rawModSwitch;
- "rounding" + recryptEkey;
- "modulus switching" + RMFE + bootstrapping

did not surface a public source implementing the current exact ordering:

\[
\boxed{
\text{independent branch raw rounding}
\to
\text{public carry-aware merge}
\to
\text{one common encrypted-key reconstruction}.
}
\]

The searches mostly returned:
- generic TFHE modulus-switch/blind-rotation material;
- generic FHE bootstrapping surveys;
- Aung itself;
- unrelated functional/GBFV bootstrapping.

## 8. Current collision matrix after fresh 2026 search

\`\`\`text
AUNG HIGH-LEVEL DIRECT RMFE MULTKEY OPEN PROBLEM:
  PRIOR-DISCLOSED / NOT OUR NOVELTY

AUNG PROP3 SHARED RANK-k RECOVERY:
  PRIOR ART / NATURAL COROLLARY

2026 DIRECT RMFE-PACKED MULTKEY IMPLEMENTATION:
  NO PUBLIC COLLISION FOUND

2026 POST-ROUNDING RMFE BRANCH MERGE:
  NO PUBLIC COLLISION FOUND

2026 COMMON RECRYPTEKEY MERGE AFTER BRANCH RAWMODSWITCH:
  NO PUBLIC COLLISION FOUND

BETTER GBFV BOOTSTRAPPING 2026:
  ADJACENT / DIFFERENT ENCODING-CONVERSION MECHANISM

LAURENT POLYNOMIAL FUNCTIONAL BOOTSTRAPPING 2026:
  ADJACENT LINEAR-PHASE PRIOR ART
  NO RMFE DELAYED-FUSION COLLISION FOUND

GAUSSIAN-PERIOD FHE 2026:
  ADJACENT RING/SUBRING WORK
  NO RMFE DELAYED-FUSION COLLISION FOUND

RMFE MPC 2025-2026:
  DIFFERENT DOMAIN

POST-AUNG NARROW NOVELTY STATUS:
  SURVIVES TARGETED PUBLIC SEARCH
  NOT PROVEN NOVEL
\`\`\`

## 9. Claim boundary

The fresh search strengthens only the following statement:

> As of 2026-11-01, no public source found in a targeted post-Aung search closes Aung's direct-MultKey future-work problem using the same obstruction-aware post-raw delayed-fusion ordering.

It does **not** justify:

> "we are the first to do direct RMFE-packed MultKey."

That broader claim remains false/unsafe because:
- Aung already disclosed the objective;
- Chen-Han and other packed-bootstrapping work cover broad packed-one-inner-product architectures;
- search absence is not novelty proof.

The only plausible first/new claim remains mechanism-specific:

\[
\boxed{
\text{identify the branch-rounding obstruction}
+
\text{move fusion to the earliest exact post-raw boundary}
+
\text{carry-correct the divisibility defect}
+
\text{reuse one common reconstruction}.
}
\]

## 10. Reopening condition

If the pending native task STRONG-PASSES, a publication-grade novelty closure should next include:
- manual citation-forward review of Aung in Google Scholar/Semantic Scholar if available;
- full-text review of any new citing FHE paper, not just titles/abstracts;
- author-page / talk / thesis search for unpublished follow-up by the Aung group;
- patent/prior-art review only if preparing an explicit "first" claim.

If the native task fails systems value, this deeper novelty closure is not worth the cost.

## Verdict

\`\`\`text
RESULT:
  PASS_POST_AUNG_TARGETED_PUBLIC_COLLISION_SEARCH

DIRECT_POST_AUNG_COLLISION_FOUND:
  NO

HIGH_LEVEL_DIRECT_MULTKEY_NOVELTY:
  STILL KILLED / AUNG FUTURE WORK

NARROW_POST_RAW_DELAYED_FUSION:
  SURVIVES 2025-2026 TARGETED PUBLIC SEARCH

NOVELTY_PROVEN:
  NO

2026_EPRINT_TITLE_RMFE_FIMD_MATCH:
  NONE

VISIBLE_AUNG_CITATIONS_COLLIDING:
  NONE

ADJACENT_2026_FHE_WORK:
  BETTER GBFV BOOTSTRAPPING
  GAUSSIAN-PERIOD FHE
  LAURENT-POLYNOMIAL FUNCTIONAL BOOTSTRAPPING
  NO DIRECT MECHANISM COLLISION FOUND

PUBLICATION_GRADE_CITATION_CLOSURE:
  DEFER UNTIL NATIVE STRONG PASS

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  RETAIN PENDING SYSTEMS VALUE

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

The fresh 2026 literature does not currently kill the surviving mechanism.

This is a meaningful positive update because the candidate's novelty has already been narrowed heavily: if a post-Aung direct-MultKey follow-up existed, the branch would likely lose publication value even under strong native performance.

No such public collision was found.

Do not broaden the claim beyond the post-raw obstruction-and-repair mechanism.
