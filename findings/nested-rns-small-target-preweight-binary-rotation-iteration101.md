# Iteration 101 — Conditional factorization of Algorithm 3 CRT target weights into one plaintext preweight and binary rotate-sum

Date: 2026-10-12. Target Boneh–Kim, *Homomorphic Encryption for Large Integers from Nested Residue Number Systems*, CRYPTO 2025, ePrint 2025/346. Research MCP primary 31pp PDF SHA256 7a26e911b00368dace336f4324e8e3f036927a57683cf5fbea1e26ee19777ef5, GitHub mirror revision edfb5603b09e7608360f41b276e1389857051f5b, **VERSION_UNVERIFIED** against official latest.

## One falsifiable hypothesis + cheapest decisive test
[HYPOTHESIS] In the special-case parameter regime `max_j|[P/p_j]_r| < min_i(p_i)/2`, the target-block-specific centered weights `[[P/p_j]_r]_{p_(j-i)}` in Algorithm 3, line9, all collapse to the same integer for each source j. Thus we can factor all k plaintext weights into one multiplication before rotating and reduce the k-source rotation aggregation to a binary rotate-and-add fold with log2 k rotations, without extra Mod_p. Need prove exact integer equality and test source indexing k4.
[FALSIFIER] Source line9 coefficient depends nontrivially on target modulus even under bound; or exact integer sums/CRT reconstruction differ for some centered x.

## Source and prior art [FACT]
Read live AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md I100, failure I100 before source/write. Research MCP read original §3.3 Theorem2 physical p15, Eq(3), and Algorithm3 physical p16, Theorem3 p17.
- `hatp_j=P/p_j`, `y_j=[[x]_(p_j) hatp_j^-1]_(p_j)`, `w_j=[hatp_j]_r` centered. For source rotation index i, source position j's plaintext coefficient is `w_j^(i)=[w_j]_(p_(j-i mod k))` (Algorithm3 line9). Source output target-block d receives `sum_j y_j [w_j]_(p_d)`, then `-v[P]_r` (line12–13), and `Mod_p` (line14); output is LAZY `[x]_r+re`.
- §3.3 p16 ALREADY uses the standard doubling rotate-and-add fold to compute v in Algorithm3 lines4–6, and calls other aggregation 'a proper rotation-sum' in prose. Thus logarithmic fold itself is OBVIOUS KNOWN PRACTICE, not a new algorithmic primitive. OpenFHE documentation/public source also implements `EvalPartialSumInPlace` using doubling rotations (https://openfhe-development.readthedocs.io/en/latest/api/classlbcrypto_1_1FHECKKSRNS.html). No demonstration authors lack similar implementation optimization in practice.
- The source's target r is generally intended for **large prescribed modular arithmetic**, whereas the sufficient hypothesis requires w_j small relative to every p_i and is trivially true if r<min_i p_i. That regime may be irrelevant for claimed high-precision target sizes; check practical inputs before pursuing.

## Exact factoring lemma [DERIVATION, CONDITIONAL PASS]
Let `center_m(a)` be the unique integer congruent to a modulo m in [-m/2,m/2). Let p_i pairwise coprime, k a power of two, r coprime to P, and `w_j=center_r(P/p_j)`. Suppose `2 max_j |w_j|<min_i p_i`. Then for all target d and source j,
`center_(p_d)(w_j)=w_j`, hence `w_j^(i)=w_j` independently of rotation i.
Therefore the source uncorrected vector satisfies
`O = sum_(i=0)^(k-1) Rot_i(y ◦ w) = (S,...,S)` with `S=sum_j y_j w_j`.
Define `a^(0)=y◦w` and `a^(t+1)=a^(t)+Rot_(2^t)(a^(t))` for t=0..log2 k−1. Induction yields
`a^(t)=sum_(i=0)^(2^t−1) Rot_i(y◦w)`, so final `a^(log2k)=O` **exactly as integers BEFORE final Mod_p**, not just modulo each p_i.
Subtract source `v[P]_r` and apply same final Mod_p. The mathematical output and lazy `x mod r` correctness coincide. No extra LUT/Mod_p is needed as algebraic identity.
- Conditional source-body cost, k power2: original pseudocode lines8–11 performs k plaintext-weighted slotwise multiplications and at most k−1 **nonidentity** rotations, while this factoring uses 1 slotwise plaintext multiplication + log2k nonidentity rotations. Same correction and post-Mod_p. PLUS original v computation already log2k rotations and remains untouched.
- This is a **pseudocode operation count**, NOT runtime or mandatory count in optimized implementation: authors can hoist, share key switching, and use identity rotations and plaintext encoding efficiently.
- Integer upper bound on any fold partial sum at a slot ≤∑_j |y_j w_j| also bounds the sequential source partial sums. This is NOT a CKKS key-switch/noise/precision guarantee; different evaluation order can differ in noise.

## One exact k=4 test and exhaustive toy [TEST PASS]
Choose p=(11,13,17,19), P=46189, r=7; hatp=(4199,3553,2717,2431); centered weights w=(-1,-3,1,2), max |w|=3<11/2. Thus all FOUR line9 target-source centered plaintext weight arrays are the same w.
For x=2: centered y=(3,-6,5,-2), v=nearest(∑y_j/p_j)=0, initial preweighted a=(-3,18,5,-4); a+Rot1(a)=(15,23,1,-7); plus Rot2(that)=(16,16,16,16). Original Algorithm3 exactly likewise gives (16,16,16,16). After source post Mod_p: (5,3,-1,-3), centered CRT decode 16≡2 (mod7), legal lazy output.
Python exact Fractions, modular inversion, all 46,189 unique centered x∈[-23094,23094]: original and binary versions agree **as integer k-vectors** for all 46,189; both modulo-p reduction then CRT decoding yield integer congruent to x modulo r for all 46,189. Maximum absolute intermediate source and tree 49, and 0 of 46,189 toy inputs showed larger tree intermediate peak. v nonzero for 18,476 examples.
IMPORTANT: the full exhaustive set includes x outside Theorem3 `|x|≪ min hatp` (here min hatp=2431), so 46,189 equality tests verify only exact algebra, NOT correctness of actual FHE approximate IntMod. Only x=2 is qualitatively small relative to hatp, yet no noise calculation.
At k4: source loop 4 plaintext weightings & 3 nonidentity rotations vs one weighting & 2; already present separate v fold 2 rotations so modeled totals 5→4. For realistic k, nominal body difference k−1→log2k, but no verified exact speedup or new Galois key requirements.

Reproducible local verified file `/mnt/data/iteration101_nested_rns_preweight_tree_test.py` SHA256 `89798251c973205c620a033b6fae2390644a71fb60d75bda91a1fb5c9d8717c8`; JSON `/mnt/data/iteration101_nested_rns_preweight_tree_results.json` SHA256 `a733e5e7f674860ab8ab8a45005240b40041216d4b40f3c185a758678819fc3a`. Both exact container files created, not merely repo paths. No actual CKKS ciphertext, empirical noise, key setup, timings or security.

## Result and follow-up gate
STATUS: **PASS** narrow exact factoring lemma and full toy validation; **UNCLEAR** practical cryptographic regime, performance and novelty. No source error or exploitable cryptographic attack.
KEY OBSTRUCTION: r<min_i p_i is a sufficient easy regime, but original work is designed to support prescribed LARGE moduli, with tiny p_i in discrete-CKKS CRT base. The *general* r can be bigger; then original destination-specific centered w_j differ by multiples p_dest from common w_j. They remain equal after final mod_p in exact algebra but may cause huge intermediate values exceeding CKKS precision/noise assumptions if preweighted directly. No general cost saving has been established.
NEXT_ACTION (I102): Read source §6 physical pp25–27 + pinned author repo `jaehyungkim0/CRT-FHE` param settings for actual p_i and the Algorithm3 IMod_r target r; check **one concrete parameter instance** whether `max_j|[P/p_j]_r|<min_i p_i/2` (or a comparably tight precision-safe bound). If not, FAIL practical relevance, park this small-target factorization; do not invent noise margins. Also check whether authors already call generic fast partial summation; require proof before claiming performance originality.
STATE_UPDATE: YES — conditional positive with sharp parameter gate, source precise, real experimental applicability still unknown. No author contact, email, outreach or public release.
