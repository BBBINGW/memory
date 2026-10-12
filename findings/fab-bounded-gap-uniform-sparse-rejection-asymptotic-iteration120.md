# Iteration 120 — Constant-factor bounded gaps make uniform sparse-key rejection sampling asymptotically exponential

Date: 2026-10-12. Human/PI explicitly authorized research continuation and agent paper selection; one new target, ONE primary hypothesis and ONE cheapest decisive combinatorial test. This finding concerns asymptotic KEY GENERATION and security-reduction regime, NOT bootstrapping arithmetic correctness, concrete reported latency, or an attack.

## Sources / read-before-write
- Antonio Guimarães and Hilder V. L. Pereira, *Fast amortized bootstrapping with small keys and polynomial noise overhead*, CCS 2025, IACR ePrint **2025/686**, https://eprint.iacr.org/2025/686.
- Full Research MCP PDF 34 physical pages, GitHub ePrint mirror `github-mirror`, SHA256 `84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335`, mirror revision `29f9da07b541e562a94af168cef80c29a8b3fb2d`, official latest `VERSION_UNVERIFIED`.
- Original paper §1.2 physical p6 asserts high-probability `B=O(n/h)` for consecutive secret indices, hence `O(h n log(n/h))` SAB operations; §6.1 p21-22 claims `O(h log(n/h))` amortized per-message and `O(h)` if n,h=O(λ), and §6.2 p22 explicitly uses rejection sampling to accept only keys whose adjacent index differences are < B. Appendix C pp33–34 estimates acceptance by 100,000 uniformly sampled sparse keys and adjusts security by δ=-log₂ P(accept); Tables 4–5 pp24–25 provide finite concrete parameters and timings.
- Author-maintained implementation is public at https://github.com/antoniocgj/Fast-Amortized-Bootstrapping but was NOT executed or audited in this one analytical iteration.

## ONE technical hypothesis and falsifier
[HYPOTHESIS] For uniformly sampled fixed-Hamming-weight secret positions, the paper's rejection-sampling route to `B=Θ(n/h)` admits expected polynomial-time key generation throughout the advertised asymptotic linear-sparsity regime `n=Θ(λ),h=Θ(λ)`.

[FALSIFIER / ONE MINIMAL TEST] Exhibit a valid asymptotic parameter family with `n=Θ(λ)`, `h=Θ(λ)`, `B=Θ(n/h)`, where the acceptance probability `Pr(max interior consecutive index gap < B)` is exponentially small. Use a rigorous combinatorial probability bound, not a concrete-parameter benchmark.

## Derived combinatorial result (rigorous under stated uniform-support model)
Take integer `t≥1`, `n=128t`, `h=8t=n/16`, and `B=32=2n/h`. Let A be the event that every gap between consecutive nonzero positions of a uniformly drawn size-h subset of `{0,...,n−1}` is **strictly less than 32** (exactly the interior condition of §6.2). Let `p=h/n=1/16`.

Instead sample `n` independent Bernoulli(p) bits and condition on their total H=h. This conditional distribution is **exactly** uniform among all size-h subsets. Partition the index interval into a left quarter, a central half, and a right quarter; subdivide the central half into `m=n/64=2t=h/4` disjoint length-32 blocks.

Whenever there is at least one selected index in EACH outer quarter and ANY length-32 central block is empty, some two consecutive selected indices must differ by at least 33, violating A. Thus A implies at least one of:
(i) left quarter has no 1, (ii) right quarter has no 1, or (iii) all m central blocks contain a 1.

The Bernoulli variables on disjoint central blocks are independent. Put `z=(1-p)^32=(15/16)^32≈0.1267887864`. Then, by union bound,
```
Pr_Ber(A) ≤ (1-z)^(n/64) + 2(1-p)^(n/4).
```
Since H=h is a mode of Binomial(n,p), `Pr_Ber(H=h) ≥ 1/(n+1)` (a maximum among n+1 probabilities). Hence conditioning gives the explicit upper bound:
```
Pr_uniform_h(A)
  = Pr_Ber(A|H=h)
  ≤ (n+1)[(1-(15/16)^32)^(n/64) + 2(15/16)^(n/4)]
  = exp(-Ω(n)) · poly(n)
  = exp(-Ω(h)) · poly(h).
```
Numerically the first exponential term is `exp(-0.03389445 h)`; the other term decays faster. Therefore the expected number of independent uniform sparse-key draws before acceptance is **at least** `exp(Ω(h))/poly(h)`, which is superpolynomial for h=Θ(λ).

This is ONE explicit asymptotic counterfamily. It does NOT claim that fixed Table-4 choices with h around 25–42 are infeasible; those finite probabilities are measured and explicitly accounted for in the paper.

## Scientific distinction and practical relevance
[NEGATIVE] The hypothesis that **uniform sparse-secret rejection sampling** always realizes the claimed `B=Θ(n/h)` with polynomial expected key-generation time in the linear-h regime is FALSE.

[DERIVED] This exposes an unaccounted regime boundary if the `O(h)` amortized bootstrapping expression is interpreted as an efficient end-to-end cryptographic family **under the original uniformly sparse-secret distribution**: constant-factor mean spacing does not make the maximum spacing bounded with nonnegligible probability as h→∞. The paper's concrete finite benchmarks and their reported δ deductions are not refuted; the paper explicitly discloses rejection sampling and does NOT make a blanket explicit uniform polynomial expected KeyGen theorem.

[OPEN] Potential routes need separate prior art/security scrutiny: (1) choose a larger spacing budget on the order of `(n/h) log h` (incurs `log B` cost); or (2) directly sample a structured/conditioned bounded-gap key (which can avoid rejection overhead but needs appropriate security justification/reduction). Sparse block secrets and related techniques exist in prior FHE work, so this is NOT a novel construction claim. The exact asymptotic security-loss tradeoff and whether it yields a worthwhile FHE contribution are unverified. NOVELTY NOT VERIFIED.

## End
STATUS: **FAIL primary hypothesis / PASS precise asymptotic rejection-sampling obstruction / HUMAN_REVIEW for contribution direction**.
RESULT: A rigorous conditional-Bernoulli counting proof shows exponentially small acceptance for a valid `n=128t,h=8t,B=32=2n/h` family. This is a keygen/security-reduction barrier, NOT a correctness/benchmark attack.
NEXT_ACTION: PI decides whether to authorize a distinct I121 hypothesis assessing **one** implementable, security-preserving remedy for the bounded-gap key distribution, or PARK this asymptotic audit and select another FHE target. Start with strongest prior-art/assumption falsifier rather than implementation.
STATE_UPDATE: YES. No author contact, public issues, or disclosure.
