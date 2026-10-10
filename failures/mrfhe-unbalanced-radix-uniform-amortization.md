# MRFHE fixed n1-batch: uniform constant-cost claim fails for W-heavy radices

Date: 2026-10-10
Iteration: 31
Status: NEGATIVE for a **uniform-over-all-radices** O(1) assertion concerning **unchanged Algorithm 2**. No claim of a correctness bug or false published theorem.

## Question and minimal falsification
[HYPOTHESIS / REJECTED] The precise amortized key-switching cost of MRFHE Algorithm 2 remains O(1) per original R^(i) ciphertext along all admissible mixed-radix sequences (w2 >= 3, w3 >= 0), even when the tensor axes become arbitrarily unbalanced.

[TEST] Analyze the original paper's *own cost formula*, rather than launching benchmark or lattice estimator.

## Primary original-paper evidence
[FACT] Cheon, Hong, Kang, Kim, Kim, Lee, Lee, "MRFHE: Mixed-Radix Fully Homomorphic Encryption with Better Batch Bootstrapping", ePrint 2026/853. Read original 18-physical-page full text **from the user's ChatGPT Library** (file named `2026-853.pdf`, 844,699 bytes), not a successful GitHub Notes ePrint acquisition.
- §2.1 physical p.4: N=2^w2 3^w3, n1=2^(w2-2), n2=2·3^w3.
- §5.2 Theorem 5.6 / Proposition 5.7, physical p.10: right W-axis multiplication converted into auxiliary-ring n2/2-dimensional PCMM; source n1 coefficient ciphertexts regrouped in L=ceil(2n1/n2) blocks. The paragraph explicitly identifies each target block as of size n2/2 and the same secret across representations.
- Algorithm 2 and §5 "Cost Analysis", physical p.11: for **one n1-batch**, 3 switches over S^(i) (rank ratio n1 per R^(i)) plus 4L switches over S^(omega) (rank ratio n2/2 per R^(i)). The resulting amortized cost, in units of base-ring switches and under assumed linear-in-Z-rank switching, is
  C=(3n1+4L(n2/2))/n1 = 3+2(n2/n1) ceil(2n1/n2).
- §1.1 physical p.2 expressly states **with an appropriate choice of the two radices** both transform factors are O(sqrt N); §6.3 physical p.12 says batch experiments focus on aligned parameter sets, and each batch contains n1 ciphertexts. Thus **no demonstrated overclaim** that all legal parameter families have O(1) amortization.
- Table 5 physical p.18 and Table 4 physical p.12 list experimental parameter families and their tested batch regimes.

PDF note: PDF text was parsed through Library files.read. The exact cost formula was legible; original PDF page images were not independently inspected this turn.

## Exact algebraic result
[DERIVED] Put r=n2/n1>0. Then C(r)=3+2r ceil(2/r).
- If r<=2, 7<=C(r)<7+2r<=11. Thus strong **U-heavy** imbalance n1>>n2 still has constant amortized *switch-equivalent* cost.
- If r>2, ceil(2/r)=1, and C(r)=3+2r, unbounded as r increases.
- Consequently, for varying admissible w2,w3 and this **specific** cost model/algorithm, C=O(1) iff n2=O(n1). As N=2n1n2, this is equivalently n1=Omega(sqrt N). Balance n1=Theta(n2) is sufficient but NOT necessary.
- Fix w2=3 and send w3->infinity: n1=2, n2=2·3^w3, N=8·3^w3, C=3+2·3^w3=3+N/4. Valid algebraic asymptotic counterexample; **not** a practical-security parameter claim.
- For r>2, an S^(omega) block of n2/2 coefficient positions holds only n1 source coordinates in the fixed one-batch format: utilized fraction 2n1/n2=2/r. This packing under-utilization is the exact source of the extra ratio, not an inherent lower bound for all possible FHE constructions.

## Exact parameter checks (rational arithmetic)
Name                  n1    n2    L    C
FHE(8,4)-D             64   162    1    129/16  = 8.0625
FHE(10,3)-D           256    54   10    231/32  = 7.21875
FHE(9,4)-S            128   162    2    129/16  = 8.0625
FHE(8,5)               64   486    1    291/16  = 18.1875
Synthetic w2=15,w3=1 8192     6 2731    14337/2048 = 7.00048828125
Synthetic w2=8,w3=8    64 13122    1    6609/16 = 413.0625

The first four are parameter shapes in paper Table 5, **not** measured timings. FHE(8,5) is not among Table 4's reported batch bootstrapping benchmarks. Synthetic cases are algebraic admissible shapes, not security-matched deployment parameters.

## Limits / research interpretation
[NEGATIVE] Uniform O(1) across *all* mixed-radix exponents fails in the paper's own cost model for unchanged Algorithm 2.
[FACT/CONTEXT] The paper already narrows its algorithmic ambitions to appropriately chosen, reasonably balanced/beneficial batching dimensions, so do not advertise this observation as a novel correction to the authors.
[OPEN] U-heavy shapes preserve the key-switch **count per input** but require n1 (possibly enormous) independent input ciphertexts, and auxiliary-ring switching keys of Z-rank n1 times the base. Latency, memory, required batch size, gadget decomposition, and security parameter feasibility are not controlled by C alone.
[OPEN / different future hypothesis] In W-heavy regime n2>>n1, one could consider packing several *independent* S^(i) batches into the unused target S^(omega) block. Before claiming a gain, test whether Theorem 5.6's D2' **dense row mixing** preserves batch independence, or instead mixes unrelated batches and invalidates unpacking. This idea has NOT been proved or tested in this iteration.

## Final
STATUS: FAIL (uniform-over-all-radices claim)
RESULT: Exact one-sided criterion C=O(1) iff n2=O(n1) under the paper's cost model; one-sided underfilling obstruction for W-heavy shapes; no published flaw shown.
NEXT_ACTION: PI selects whether the underfilled S^(omega) batching regime is worth a separate, minimal block-independence test. Do not auto-run.
STATE_UPDATE: NO; STATE.md holds distinct parked RIG-HE branch.
