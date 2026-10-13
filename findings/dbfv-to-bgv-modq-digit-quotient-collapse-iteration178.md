# I178 — Direct finite-modulus BGV transplantation of dBFV's digit-lattice ciphertext quotient collapses to zero

**Date:** 2026-10-13. PI: “好的，请继续” after I177. ONE primary hypothesis + ONE decisive algebraic ideal/finite-ring test. Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` I177 blob `03dc15a642e8732251daa07b14ea729844a0c22b`, `findings/OPEN_RESEARCH_BRANCHES.md` and I177 finding. PI assent parks generic fixed-weight TFHE mask drift after its weak typical-noise gain.

## Primary source and provenance

Chris Peikert, Doron Zarchy, Guy Zyskind, *High-Precision Exact FHE Made Simple, General, and Fast*, IACR ePrint **2025/2321**, https://eprint.iacr.org/2025/2321, CRYPTO 2026. Full Research MCP **43 physical-page** `github-mirror` PDF SHA256 **`1e41b62004aeee0bf572d0ccca8de8c5827ee9a14fb333a1d3d0f4d2ab483849`**; **VERSION_UNVERIFIED** against latest official edition. Original source p3 footnote 1 explicitly notes authors have not found a way to adapt their method **directly to BGV**. Source §3.1–3.4 physical pp14–18 (fraction-field BFV ciphertexts), §4.1 physical p19 Equation(4.1) digit lattice, §4.2 p20 Definition4.3 ciphertext over `K[B]/L`, §4.4 pp23–25 error growth, §4.6.1 pp26–27 lattice degree reduction. Original paper asserts significant reduction of large p error-growth factor from BFV p to `O(d p^{1/d})` using small digit representatives; these are source-reported theoretical results, not independently rederived here. This investigation does not attempt a fresh dBGV scheme or claim original source wrong.

Other topical candidates were checked for source priority but not selected: ePrint2026/2310 and 2026/1836/1840/956 and 2026/1089 lacked verified PDF via Research MCP (RETRIEVAL_BLOCKED); ePrint2026/233 complete, but its single-ciphertext A2B bottleneck had already been addressed by independent 2026/1836 per public context (unverified full new paper). No substantive technical claim about unavailable PDFs.

## ONE primary falsifiable hypothesis

**[HYPOTHESIS]** The most direct dBGV transplant is well-defined: replace dBFV's rational additive ciphertext quotient `K[B]/L` by `R_q[B]/\bar L`, where `R_q=R/qR` is the usual BGV ciphertext coefficient ring and `\bar L` is the reduction modulo q of exactly the same digit lattice `L=\{f∈R[B]: f(b)∈pR\}`. The resulting quotient still contains nonzero digit plaintext information, and one could then apply original short lattice reduction and error argument unchanged.

**[FALSIFIER]** Check ideal generators at scalar `R=Z` with plaintext integer `p`, base `b`, BGV ciphertext modulus `q`. If `p∈L` and p is a unit in `Z_q`, then `1∈\bar L`, so the entire ciphertext quotient is the zero ring. A single valid coprime p,q instance disproves the claimed verbatim transplant for generic standard BGV.

## Mathematical proof and exact toy

**[FACT SOURCE]** Digit lattice `L=L_p^⊥(b)=ker(ev_b:Z[B]→Z_p)`; `p∈L`, and in scalar case `L=(p,B-b)` as ideals of `Z[B]`. Its plaintext quotient `Z[B]/L ≅ Z_p` is meaningful and has p distinct messages. Source dBFV ciphertext quotient `Q[B]/L` is an **additive abelian-group/Z-module quotient**; it is **NOT** a quotient *Q-algebra/ring*, because L is not a Q-subspace (multiplication of an integer lattice element by arbitrary rationals leaves L). Thus p cannot be canceled inside Q[B]/L merely because 1/p exists in Q.

**[DERIVATION, decisive]** In standard co-prime BGV setting `gcd(p,q)=1`, reduce source L coefficientwise into `Z_q[B]`, yielding ideal `\bar L=(\bar p,B-\bar b)`. Bezout gives integers u,v with `up+vq=1`, hence `\bar u\bar p=1` in `Z_q`, i.e. `1∈\bar L`. Therefore
```
   Z_q[B] / bar(L) = {0}.
```
More generally for plaintext integer `p` and ring `R`, if the constant integer p acts invertibly in R/qR (e.g. gcd(p,q)=1), any naïve quotient `(R/qR)[B]/image(L)` collapses. There is NO canonical ring homomorphism `Z_q→Z_p` for coprime p,q: equality modulo q does not preserve equality modulo p. This is the **coefficient-modulus incompatibility**; NOT a proof that BGV itself fails or that dBFV is insecure.

**[Exact arithmetic test executed]** Let p=8, q=17, b=2, d=3. Source digit plaintext ideal `L=(8,B−2)`; `Z[B]/L≅Z_8` and all eight binary expansions `m=m0+2m1+4m2` are distinct. In `Z_17`, `8*15=120=1 (mod17)`, so `1=15·8∈barL`. Therefore for EVERY polynomial `c(B)∈Z_17[B]`, `c=15·8·c∈barL`. Deterministically checked all `17^3=4913` degree<3 coefficient vectors and the exact modular equality `c_i ≡ 8·(15 c_i) mod17`. All reduce to the zero class. The test is symbolic proof with exhaustive tiny verification, NOT any RLWE encrypted simulation, measured precision or security attack.

**[Interpretation / limits]** This FAILS *only* the **naïve same quotient construction over the standard mod-q BGV ciphertext ring**. It does **not** rule out an alternative dBGV based on `(R_q)^d` together with a separate integer digit/carry structure, mixed-modulus lifts, and a BGV-compatible key-switching/decomposition protocol. Those alternatives would need to (1) distinguish the ciphertext mod-q ring from independent digit lattice mod-p, (2) preserve coherent changing digit plaintexts across carries under homomorphic multiplication/relinearization/mod-switch, (3) maintain BGV's `m+p e (modq)` interpretation with representatives, and (4) prove p-independent error growth and security at matched parameters. No such construction is offered or disproved here. In particular the original dBFV's `K[B]/L` is **not** being claimed to collapse; its rational additive quotient is why it stays meaningful.

**[Novelty warning]** An elementary Bezout/unit-ideal collapse is conventional algebra. The original authors *already acknowledge* missing direct BGV construction. This is a precise **reason** one straightforward avenue fails, NOT an independent new FHE primitive or proof of BGV impossibility; no source paper mistake.

## End of Iteration 178

**STATUS:** **FAIL** direct `(R_q[B]/barL)` verbatim-transplant hypothesis / **PASS** exact ideal-unit obstruction and 4913-element polynomial check / **UNCLEAR** any alternative secure efficient dBGV construction.
**RESULT:** Since `p∈L` and gcd(p,q)=1 for standard BGV co-prime moduli, `1∈image(L mod q)`; `(R/qR)[B]/image(L)=0`, unlike source dBFV's nontrivial rational **additive** quotient `K[B]/L`. Toy p8 q17 base2 d3 shows all 4913 degree<3 polynomials vanish in the naïve ciphertext quotient, though plaintext Z8 has 8 values.
**NEXT_ACTION:** **HUMAN_REVIEW / conditional CONTINUE** a **distinct** potential dBGV mechanism if PI agrees. Next ONE source-based feasibility gate: before inventing a new scheme, inspect existing BGV↔BFV switch [AP13 Appendix A], high-precision dBFV claim, and any known decomposition-in-BGV works to determine whether a **mixed-modulus digit lattice / BGV ciphertext tuple with explicit integer lifts/carries** can be meaningful and whether it's already equivalent to known BFV↔BGV switching. Require an actual correctness/error recurrence under p,q, not a vague “could work.” If only trivial conversion dBGV→dBFV→BGV is available without benefits, PARK. Never claim universal impossibility from collapsed naïve quotient.
**STATE_UPDATE:** **YES** — selects a new, source-signaled high-value dBFV-to-BGV gap, exactly falsifies the simplest transplant, records a precise technical boundary and carefully scoped next test.
