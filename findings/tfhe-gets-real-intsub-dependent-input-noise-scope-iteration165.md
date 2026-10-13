# Iteration 165 — TFHE Gets Real IntSub* independence scope under correlated LWE inputs

**Date:** 2026-10-13. PI said “好的，请继续” after I164 recommendation to PARK p1-only weighting. The PI assent parks 2025/429 p1-only stage; as delegated FHE research agent choose ONE new source-readable unarchived target. Source ePrint 2025/257 `TFHE Gets Real: an Efficient and Flexible Homomorphic Floating-Point Arithmetic`, Bergerat, Chillotti, Ligier, Orfila, Tap, complete Research MCP 59-physical-page mirror SHA256 `8544b4f2a8c0a22ba9d1d8f0a306e81a014243c7e12a8773e2d36cccf1f61ee2`, VERSION_UNVERIFIED. Read-before-write START_RESEARCH_SESSION, RESEARCH_PHILOSOPHY, AGENT, STATE after I164 sha `b86ba6f7b8824b2e3a0e861f461e4cdee056ddc6`, and OPEN_RESEARCH_BRANCHES (old candidate failures checked). No code execution or error probability/attack claim against authors.

## Primary source

§2.4 Algorithm2 `IntSub*` physical pp15–18, Lemma1 and **Lemma2/Proof2** p16, explicitly: each input LWE noise is a **centered Gaussian variance σ_in²**, and the two ciphertext noises are **statistically independent**. At subtraction line6, Proof2 computes variance `2σ_in²`; later uses fresh PBS variances and assumes a criterion `2σ_in² + σ_BR² + σ_KS² + σ_MS² ≤ t²`. This is **correct under paper's explicitly stated independence assumption**. §4.1.1 `AlignMantissa` / Algorithm7 physical pp29–30 line1 calls `IntSub*` on the two **encrypted exponent inputs**; Lemma7 and noise follow-up p32–33 use Lemma2's outputs in CBS and ExtendedCMux. Reading pp29–33 did NOT identify a universal proof that all upstream exponent ciphertext pairs in iterative/feedback pipelines remain noise independent. Absence in inspected pages is not proof of an author theorem that claims arbitrary correlated inputs.

## ONE hypothesis and cheapest test

**[HYPOTHESIS TO FALSIFY]** Merely bounding each of two possibly **correlated** LWE ciphertext input noises by the same variance σ² suffices to retain Algorithm2 line6's `Var(E1−E2)≤2σ²` input to Lemma2, without statistical independence.

**[ONE exact falsifier]** For any valid LWE zero-encryption c with centered noise E of variance σ², use c1=c, c2=−c, both legal encryptions of 0 with marginal centered variance σ², and consider line6 `c1−c2=2c`. Noise pair E1=E, E2=−E, Cov(E1,E2)=−σ², hence
```
Var(E1−E2)=Var(2E)=4σ²
          =2σ²−2Cov(E1,E2) > 2σ².
```
At abstract Gaussian level E∼N(0,σ²), −E has same centered Gaussian marginal, so this violates independence **only**, not Gaussian marginality. Exhaustively checked discrete symmetric toy E∈{−1,+1} as arithmetic sanity check (dependent outputs ±2 variance4 vs independent 4 pairs difference variance2); Gaussian proof is algebraic, no sampling assumption. The counterexample has legitimate LWE linear-negation under a shared secret, and is valid provided decryption noise is considered in the same torus lift range **without wrap/alias**; choose sufficiently small bounded error or analyze unwrapped error variables. The correlated case **lies outside Proof2's explicit statistical independence premise**. It does NOT prove the published Lemma2 false.

**[General covariance boundary]**
```
Var(E1−E2) = Var(E1)+Var(E2)−2Cov(E1,E2).
```
For equal variances σ² and arbitrary dependence, by Cauchy–Schwarz upper bound is 4σ² (attained at E2=−E1). Distinguish input variance from output PBS noise; the precise full KS/PBS failure probability and t noise threshold are NOT analyzed, and the 2x variance bound is a worst-possible dependence penalty, not evidence true author's HFP incurs it.

## Relation to actual floating-point path, important caveats

**[FACT]** Algorithm7 uses `IntSub*` as first step to align encrypted exponents in actual HFP addition/subtraction (pp29–33). Exponents may originate from earlier homomorphic operations, so dependence is conceivable in general compositional programs; however **no actual named upstream HFP program was constructed to produce c,-c as legal, correctly encoded exponent data while satisfying algorithm preconditions**. Author may enforce independent encryptions for relevant input classes or rebootstrap outputs in a way that restores conditions; one must trace a concrete legal HFP operation DAG and noise correlations to substantiate missing composability guarantee. Theoretical HFP arithmetic includes carry/message range and sign conventions that could rule out some toy zero-negation pair usages.

**[NO CLAIM]** Not a correctness defect, parameter attack, IEEE floating failure, numerical precision regression, real noise statistic or publishable gap. Authors explicitly assume independence in proof, and worst-case covariance variance bound is elementary. Distinct future claim would require source-grounded **specific valid iterative Algorithm7 input pair** with covariance surviving prior PBS and a quantified violation of a parameter safety margin (or an inexpensive covariance-aware repair). Otherwise PARK this routine noise-assumption audit.

## End of Iteration 165

**STATUS:** **FAIL** claim that marginal variances alone imply the paper's 2σ² subtraction bound; **PASS** mathematical counterexample and verified genuine Algorithm7 call path; **UNCLEAR** whether source HFP guarantees independence for all claimed use cases or ever suffers an actual failure.
**RESULT:** c,-c legitimate same-secret LWE inputs produce 4σ² subtraction variance vs 2σ² under independence; Paper Lemma2 Proof2 explicitly states statistical independence, so this is **NOT a counterexample within its assumptions**. Algorithm7 AlignMantissa uses IntSub* on encrypted exponents, but no source-grounded legal HFP feedback counterexample established.
**NEXT_ACTION:** **I166 if PI authorizes:** ONE cheapest real-use falsifier: trace a **specific, legal, two-step HFP computation DAG** through Algorithm7's exponent construction/refresh semantics and decide whether two exponents can share a nontrivial correlated pre-IntSub noise under authors' permitted operator API and whether they cross the stated threshold. If all paths reset/independent under scope, PARK. Do not enumerate more abstract covariance toys or claim bug.
**STATE_UPDATE:** YES — independent target and source-bounded dependence frontier after explicit PI assent to park 2025/429 p1-only polynomial work.
