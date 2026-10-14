# PVFHE-P12 — One sigma-fixed-subfield challenge replaces two Galois PCS openings

**Date:** 2026-10-15 Asia/Tokyo. Independent PVFHE P12 COMPLETED, P13 NOT STARTED.
**STATUS:** PASS actual-source-ring field factorization, large sparse exceptional set and one-opening algebraic correctness; UNCLEAR actual CMNW adaptive PCS/FIat–Shamir/QROM security, source full Ring-R1CS witness linkage, concrete lattice parameters/implementation and novelty.

## Read-before-write, source and workstream provenance

Read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md; separate global STATE.md SHA `aaa1a1f299c66d2d665e558ef51885efb585d13f` (concurrent vFHE), P11 `findings/pvfhe-P11-binding-sqrt-loss-precommit-extraction-gate.md` SHA `165dfc36f7ba9914561ebe93ef5ff113316b083c`, P05 SHA `68cbabb5594b54d496179934d78fb2352512caf0`. P12 target absent before write. DO NOT update parallel SHIP/vFHE/global state or overwrite P01–P11.

**Primary source FACTS:**
- Huang–Li–Mao–Zhang, *Fully Homomorphic Encryption with Efficient Public Verification*, ePrint **2024/1764**, 29 physical pp, Research MCP full PDF SHA256 `7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089` VERSION_UNVERIFIED. Physical pp5–6 Definition2.1 (E pairwise unit differences), Remark2.2 and Lemma2.3 generalized Schwartz–Zippel for E; p21 Lemma5.6 PCS evaluates ring multivariate polynomials at arbitrary ring points; p26 AppendixB source Q=2^53+5, N=2^11. This NEW fixed-subfield design is NOT in source.
- CMNW, CRYPTO24/ePrint **2024/281**, 52pp Research MCP full mirror PDF SHA256 `a9be7b5c1e9024d2d0c03865978d7f3ea1ed941dce8883f93f9576ae46a73b73` VERSION_UNVERIFIED. Physical p13 Definition8 PCS full-opening witness and p24 multi-linear PCS; original source does not establish the added sigma protocol's composed security. Web PDF screenshot retrieval gave cache miss; latest edition parity remains unverified.

## One primary falsifiable claim; one decisive exact test

**[HYPOTHESIS P12]** The source actual ring R_Q=F_Q[X]/(X^2048+1), Q=2^53+5, contains an efficiently samplable sigma-invariant exceptional set of cardinality >=2^200, where sigma(X)=X^-1. Hence the P11 NEW masked-witness Galois repair can replace P05's TWO postchallenge evaluations at r and sigma^-1(r) with ONE authentic PC.Eval at r and a verifier-side check z=sigma(z), retaining source generalized Schwartz–Zippel and P11 prechallenge anchor.

**[DECISIVE FALSIFIER]** Derive actual cyclotomic factor degrees and inversion action. If Fix(sigma) is not a field or if a nonzero difference in proposed E is a zero-divisor, the construction FAILS. Verify four-vector independence, fixedness, units and small-ring full enumeration; test honest and malicious one-opening polynomial behavior. Do not conflate source algebraic results with actual PCS/FS proof.

## Exact algebra [DERIVATION / PASS]

The source Q=9007199254740997 is PRIME; Q mod4096=5, ord_4096(Q)=1024. For Phi_4096=X^2048+1, there are EXACTLY two irreducible factors of degree1024 over F_Q, and inversion sends a primitive root zeta to zeta^-1. The element -1 is not in the Frobenius powers <Q> mod4096 since all Q^j≡1 mod4, while -1≡3 mod4. Therefore inversion SWAPS the two factors:
  R_Q ≅ F_{Q^1024} × F_{Q^1024},
  K=Fix(sigma) ≅ F_{Q^1024}.
Every nonzero a∈K has nonzero coordinates in BOTH CRT fields and hence is a UNIT in R_Q. Therefore any subset E⊂K is exceptional per original Definition2.1.

**Sparse E_4:** v=X+X^-1=X−X^2047 is fixed under sigma. Define
  E_4={a0+a1*v+a2*v²+a3*v³ : a_i∈F_Q}.
1,v,v²,v³ are F_Q-linearly independent: coefficient of X^k in v^k is 1 and lower powers lack X^k, k=0..3, because N=2048>6. Thus
  |E_4|=Q^4 > 2^212 >2^200.
Uniformly sample FOUR F_Q coefficients; the map is injective so r is uniformly distributed in E_4. Different E_4 elements differ by a nonzero K-element, hence their difference is a unit in R_Q; this is the original paper's required exceptional-set property. Source-form 54-bit coefficient encoding costs 216bits≈27bytes/challenge excluding domain/metadata. Implement unbiased F_Q sampling by rejection rather than modulo reduction. Elements have at most 7 occupied X^j coefficients in standard representation.

For additional explicit algebra, (X+X^-1)^-1 = (X/2) Σ_{k=0}^{1023}(-1)^k X^{2k} in R_Q: multiplying by X^-1(1+X²) gives (1−X^2048)/2=1. Exact 2048-dimensional sparse product verified.

**One PCS postchallenge evaluation:** Let Y(T)=Σ_I y_I T^I be the committed masked multilinear witness slice. r←E_4^s satisfies sigma^-1(r)=r. So original P05
  Y(r)=sigma(Y(sigma^-1(r)))
is EQUIVALENT to
  z=Y(r) from ONE authentic PC.Eval(C,(1,r),z); verifier checks z=sigma(z).
Define D(T)=Σ_I(y_I−sigma(y_I))T^I. If any y_I is not sigma-fixed, D is a nonzero polynomial of total degree<=s in R_Q[T]. Source generalized Schwartz–Zippel gives
  Pr_r[ z=sigma(z) ] ≤ s/|E_4| = s/Q^4.
Nonzero anti-fixed coefficients are also units because sigma swaps CRT fields. The check is therefore semantically sensitive to every non-invariant coefficient, not just to one ring component. The result is CONDITIONAL on honest PCS evaluations representing the SAME masked and anchored commitment; mask-link Ring-R1CS and adaptive classical/ROM/QROM knowledge soundness NOT independently established.

## One executed exact test [VERIFIED]

Actual executable `/mnt/data/pvfhe_p12_fixed_subring_one_opening.py`, SHA256 `dcde08f8c361b2c1027dad680c3e6afb06877b1aa8ecf326ec4d7e1e6d0aed36`.
Actual JSON `/mnt/data/pvfhe_p12_fixed_subring_one_opening_results.json`, SHA256 `d4442f2c23ab36e18ddc67ad14c235ffbe811bdcfe2859fcbca59ff1198b3c8f`.
Complete local report `/mnt/data/PVFHE_P12_Fixed_Subring_Single_Opening_Gate.md`, SHA256 `8cbfa3be358b380b9f9b059b0f3bad126318996bd4215939ff9bbe23515be286`.

For original source Q,N: primality, ord_4096, v^0..v³, sigma-invariance, four-basis coefficient independence and explicit inverse of v all PASS. Reconstructed nonconstant idempotent e=(1+iX^1024)/2, i²=-1, checked e²=e, sigma(e)=1−e. Malicious Y(T)=eT gives Y(r)−sigma(Y(r))=(2e−1)r with (2e−1)²=1, hence pass iff r=0 when r∈K. Exact sparse ring computations confirm selected zero/nonzero source r.

Exhaustive independent analogue q=37,N=4: fixed subring F_37[v]/(v²−2) is field F_1369; every r=a+bv has inverse (a−bv)/(a²−2b²) unless r=0 because 2 nonsquare. Enumerated ALL 1369 fixed r; **1368/1368 nonzero unit witnesses PASS**; malicious Y(T)=eT accepts **only 1/1369 (r=0)**; honest Y(T)=T accepts **1369/1369**. This is exact algebra and NOT CMNW PCS/SNARG cryptographic execution.

For illustrative external ROM challenge budget q_H=2^64, s=32:
  (q_H+1)*s/Q^4 ≈ 8.96831017e−44 <2^-128.
This is ONLY identity-test loss; exclude extractor errors, SIS binding, FS/QROM and other Ring-R1CS soundness. E_4 meets P11's >=2^202 conditional challenge budget with margin.

## Efficiency, boundaries and decision

P05 (no anchor): TWO postchallenge PCS openings. P11: ONE prechallenge anchor plus TWO postchallenge = THREE. **P12: ONE prechallenge anchor plus ONE postchallenge = TWO total** and verifier locally applies ONE sigma automorphism to claimed ring value. Saves one PCS point proof vs P11 at source asymptotic prover O(2^s poly(lambda)), opening O(s²poly(lambda)), verifier O(s poly(lambda)) per removed PCS evaluation; no real timing measured. Four F_Q coefficients suffice per external challenge; computing sigma on ring value costs O(N) coefficient operations, not zero.

**STATUS:** PASS source-parameter field-theoretic fixed E4 and one-point SZ test; UNCLEAR full actual PCS adaptive knowledge extractor/FS/QROM, lattice hardness and cost, complete mask and zero-anchor Ring-R1CS compilation, latest PDF edition and originality.
**RESULT:** The original ring's Galois-fixed field K=F_{Q^1024} contains sparse easily sampled E_4 of size Q^4>2^212, permitting ONE postchallenge PC.Eval instead of TWO without weakening the algebraic identity-test error.
**NEXT_ACTION (PVFHE-P13 only after PI continues):** ONE actual AppendixD/Section5 witness-compilation integration audit: verify public masked values and preanchor zero coordinate are connected to SAME committed witness as the source R1CS, and single-point input (1,r) is supported; if not identify a minimal genuine obstruction. Keep FS/QROM, SIS security and novelty separate/open. Do not repeat source-ring toy checks.
**STATE_UPDATE:** YES only this NEW independent P12 file; do not modify parallel vFHE/SHIP state or prior P01–P11.