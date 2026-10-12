# Iteration 114 — LFBS PRCA packing O(log N) shorthand is not uniform in variable B

Date 2026-10-12. Research student, PI controls pivots/novelty. One hypothesis/test.

## Sources and provenance
[FACT] Primary full public 35-physical-page PDF: Zhihao Li, Xuan Shen, Xianhui Lu, Ruida Wang, Yuan Zhao, Zhiwei Wang, Benqiang Wei, *Leveled Functional Bootstrapping via External Product Tree*, ePrint 2025/022, https://eprint.iacr.org/2025/022.pdf . Obtained via ordinary public PDF fetch (web source `turn485557view0`, 35pp); Research MCP `get_eprint_paper("2025/022")` failed with metadata SOURCE_UNAVAILABLE because it rewrote 022 as /2025/22. Therefore no Research-MCP source SHA or cached-version verification. Web PDF screenshot tool was invoked for pp4,17 but errored, so no independent rendered-formula glyph verification; pdf extracted text was sufficient for clear operation counts but source may have text extraction risks.
[FACT] Technical overview physical p4–5 near lines147–159 says RLWE packing "requires only O(log N) gadget products" after claiming "B automorphisms" in preceding sentence. §4.2 PRCA physical pp16–17 (source lines921–985) states exactly **B/2+B/4+...+1 + log(N/B) = B−1+log(N/B)** RLWE key switchings, and Algorithm5 physical p17 (lines986–1019) indeed performs B/2^i homomorphic automorphisms each of log B combine levels, followed by trace log(N/B). Formal Table3 physical p19 compares all LFBS costs, but B is usually fixed small base in benchmark parameters. Do NOT conflate gadget products and total end-to-end operations; one RLWE automorphism with key switch is the relevant primitive in the paper's cost model.
[FACT] Other central paper contributions LWE→RGSW cyclic encoding, external-product tree multi-input LUT, PRCA packing, BFV scheme switching; real experimental 12/16-bit LUT gains over TFBS reported. This iteration only audits the asymptotic phrasing of PRCA step, not total LFBS performance.

## ONE hypothesis / smallest falsifier
Hypothesis: The informal "PRCA needs only O(log N) gadgets/keyswitching" is uniform for a growing number B of input RLWE ciphertexts.
Falsifier: Compare with paper's **own exact Algorithm5** key-switch count as B varies subject to B power-of-two, B<=N.

[DERIVATION] For N=1024 and B∈{4,16,64,256}, cost B−1+log2(N/B) gives 11,21,67,257. The combine tree alone costs B−1. For B=Θ(N^a), a>0, C=Ω(N^a), not O(log N); in general C=Θ(B+log(N/B)) under N,B≥2 powers of two.
[RESULT] **FAIL uniform O(log N) shorthand for variable B**. Source **already states correct exact formula** so this is NOT an erroneous Algorithm5, proof hole, implementation bug, nor novel optimization. With B fixed at application base (e.g. B=4/16) O(log N) is appropriate as an asymptotic in N alone. Does NOT refute speed/size benchmarks or composite total costs.
[RECOMMENDATION] Park narrow PRCA notation/computation-count quibble immediately as low novelty; next target must contain a genuine uncovered regime or nontrivial tradeoff rather than paper-internal shorthand. Do NOT message authors.

## End of iteration
STATUS: FAIL overly broad interpretation / PASS paper-internal exact-operation-count check / LOW NOVELTY.
RESULT: B-1+log2(N/B) exact PRCA key-switch count; only O(log N) for fixed B.
NEXT_ACTION (I115): Choose a new high-value technical issue from source full text, ideally **algorithmic noise or key memory trade-off at specified real use case**. Continue with ONE hypothesis and one falsification, avoid another notation-only gap. If returning to this same LFBS paper, select an actual unresolved correctness or practical cost issue, not PRCA count.
STATE_UPDATE: YES. No author outreach or public release.
