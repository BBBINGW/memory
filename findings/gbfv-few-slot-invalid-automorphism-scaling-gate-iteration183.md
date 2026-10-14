# Iteration 183 — Few-slot GBFV SubConvert: bare masked rotation cannot reuse ordinary GBFV.Auto under non-stabilizing plaintext modulus

**Date:** 2026-10-14 (JST). One PI-authorized iteration (“好的，请继续”). Followed `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → `STATE.md` after I182 (blob `0731d060a597b2b180d1b1cd0399df525c4d21ba`); read `findings/OPEN_RESEARCH_BRANCHES.md`, I182 archive. ONE primary **source-defined GBFV.Auto compatibility** hypothesis + ONE exact two-parameter stabilizer witness test. This is not a new scheme, source-paper bug or security attack.

## Original papers and precise primary-source claims

1. **[FACT]** Robin Geelen and Frederik Vercauteren, *Better GBFV Bootstrapping and Faster Encrypted Edit Distance Computation*, IACR ePrint **2025/1104**, https://eprint.iacr.org/2025/1104, full **22 physical pages** Research MCP `github-mirror` PDF SHA256 **`2128d7f5e568b6d66f71f6ad5f913baf34847103ef694246348d27d89ca0956f`**, latest official PDF **VERSION_UNVERIFIED**. Original §2 physical p3 lists `GBFV.Auto(ct,σ)` only for automorphisms satisfying σ(t)=t (footnote permits σ(tR)=tR), and ModUp/ModDown requirements. §3.2 pp7–10 gives Algorithm1 `GBFV.SubConvert`, intermediate `t_i=t_{i−1}·σ_{g_i}(t_{i−1})`, and masking sub-operation `SubPermute_i(µ)=a_iµ+σ_{g_i}((1−a_i)µ)`; conversion iterates `L=min(log₂ ℓ,log₂(n'/n''))`; for **few slots** ℓ≤n'/n'' §3.2.1 p8 explicitly states **σ_{g_i}(t_i) ≠ t_i**, so automorphism is generally invalid on the native GBFV plaintext modulus and `can be implemented temporarily in BFV domain` (footnote4 says output forced to be multiple of t_{i−1}). Source author already knows and accounts for the constraint; not a discovered flaw. Original §3.5 p12 stage count and §5.1 Tables2–4 pp17–18 compare costs. Do NOT claim source performance tables omit overhead without checking code/benchmark.
2. **[FACT]** Geelen and Vercauteren, *Fully Homomorphic Encryption for Cyclotomic Prime Moduli*, EUROCRYPT2025, ePrint **2024/1587**, https://eprint.iacr.org/2024/1587. Full **32 physical-page** Research MCP github-mirror SHA256 **`3158eb77d6aebe92d34479ed6163af34fde7b9f2fc7d82cb85ca7d50151ea4de`**, version unverified. **§3.3 physical p11** defines GBFV automorphism algorithm for `σ∈G={σ:σ(t)∈tR}` with ciphertext-phase scaling correction factor **`σ(t)/t`**. Unlike normal BFV, GBFV MSB fractional scaling is `∆=q/t` and automorphism maps it to `q/σ(t)`; without a valid and applied correction, mere plaintext-slot permutation does **not** imply GBFV ciphertext correctness. The ring-divisibility condition is explicitly imposed by source, and authors discuss only those auto actions. This is **prior art** for necessity of checking t stabilization.

## ONE primary hypothesis and decisive falsifier

**[HYPOTHESIS to falsify]** In the few-slot branch of `2025/1104` Algorithm1, after ordinary public slot masking, the ordinary GBFV `Automorphism` primitive of `2024/1587` can simply be reused for `σ_{g_i}` with **no BFV detour and no new compensating scaling/encoding operation**, because the required permutation is correct on the occupied slots.

**[FALSIFIER]** Test, for a paper-compatible binomial t with ℓ < n'/n'', whether source's derived intermediate plaintext modulus `t_i` satisfies **`σ_{g_i}(t_i)∈t_i R`**, a necessary precondition of the ACTUAL pre-existing GBFV.Auto primitive. Exhibit an explicit prime-field root `r` of both `X^{n'}+1` and `t_i` with `σ_{g_i}(t_i)(r)≠0`. Such a root disproves divisibility and hence the proposed direct reuse; compare a many-slot boundary parameter where divisibility holds. Do not claim this rules out **new specialized, compensated masked** operators.

## Exact source-compatible algebraic test

Take `R'=Z[X]/(X^{n'}+1)`; `R''` the subring of dimension `n''=4`, `t_0=X^4−b`; plaintext characteristic `p=b^{n'/4}+1` is prime, and 2n' divides p−1, so `t_0` has exactly **ℓ=4 distinct F_p-root slots** in R'. Choose source's first-stage `g_1=5^{−1} mod 2n'` when L=min(log₂ℓ, log₂(n'/n''))=2.

**A — boundary many-slot source-valid control:** `n'=16,n''=4,b=4,p=4^4+1=257`. `ℓ=4=n'/n''`; `g_1=13=5^{−1} mod32`. In R', `σ_13(t_0)=X^{52}−4=−X^4−4`, so
```
t_1 = (X⁴−4)(−X⁴−4)=16−X⁸,
σ_13(t_1)=16−X^(8·13)=16−X⁸=t_1   in R'=Z[X]/(X^16+1).
```
Thus automorphism **stabilizes** t1 here. One F_p root r=60 has r^4=4 and r^16=−1; exact ring/power checks PASS.

**B — strict few-slot source-valid candidate:** `n'=64,n''=4,b=2,p=2^16+1=65537`; `ℓ=4<n'/n''=16`, `g_1=77=5^{-1} mod128`. In `Z[X]/(X^64+1)`, source's stage1 plaintext modulus is
```
t_1=(X⁴−2)(X⁵²−2);
σ_77(t_1)=(X⁵²−2)(X³⁶−2).
```
Proof by evaluating modulo 65537 at exact `r=4938`:
```
r⁴≡2 (mod65537), r⁶⁴≡−1 (mod65537),    t_1(r)=0,
σ_77(t_1)(r)=48069 (mod65537) ≠0.
```
All values verified by exact modular exponentiation in isolated JS (no floating point). Hence `t_1∤σ_77(t_1)` in `R'`, since any t1 multiple must vanish at every valid ring/t1 root; **`σ_77(t_1)/t_1∉R'`**. Root-set count also verified by enumerating primitive128-th roots mod65537: `t_0` has4 roots, `t_1` has8, `σ_77(t_1)` has8, with only4 shared; there are4 roots of t1 missing from σ_77(t1). This is a genuine source-allowed *few-slot* instability, not an artefact of random invalid root choice. Compare the boundary-many-slot case where σ13(t1)=t1.

**Core scaling obstruction:** GBFV encrypts as `c(s)=⌊(q/t_i)m⌉+e` (modq). Applying σ_g to c gives leading term `q/σ_g(t_i)·σ_g(m)`. The native GBFV.Auto algorithm §3.3 of ePrint2024/1587 multiplies by `σ_g(t_i)/t_i` to restore target scale `q/t_i`, and requires `σ_g(t_i)∈t_iR` to define the resulting integral plaintext automorphism. The concrete strict-few-slot example violates the precondition. A mask defined only on occupied plaintext slots does NOT automatically turn the ordinary **unchanged** GBFV.Auto into a legal call or correct the scaling. This falsifies only **bare call reuse without additional mechanism**: it DOES NOT establish any impossibility for a new carefully compensated masked automorphism or a different RNS ciphertext conversion; public BFV detour is the explicitly existing source solution.

**Important caveat:** Full actual key-switching/gadget/SEAL implementation was NOT executed; no measured extra BFV cost and no source-paper performance issue proven. The example validates the exact absence of a native **unmodified** GBFV.Auto operation. The case choices satisfy binomial plaintext modulus, source's prime splitting/p≡1 mod2n', and n'≥n''. Any future idea must prove a compensating masked operator is well-defined on quotient lifts AND maintains encrypted fractional scale/noise at matched security and cost. Simply adding a mask does not prove these.

## Novelty and value gate

The source **explicitly acknowledges** invalid few-slot automorphisms and BFV workaround (ePrint2025/1104 §3.2.1 footnote4), and the original GBFV implementation (§3.3 ePrint2024/1587) already formalizes the exact scaling factor issue. Therefore there is **NO independent novelty** in discovering this boundary or giving an illustrative small root. A possible future distinct contribution would be a genuinely **new native masked/supported automorphism with demonstrably lower noise/runtime** than temporary BFV conversion. No such operator or proof/benchmark currently exists. This is primarily a **negative architectural compatibility gate**, not a publishable result.

## End of Iteration 183

**STATUS:** **FAIL** bare masking + ordinary GBFV.Auto bypass of the documented BFV detour; **PASS** exact source-valid ring/prime/root divisibility witness and boundary control; **UNCLEAR** whether an independently new compensated masked rotation has real benefit.
**RESULT:** n'=64, n''=4, ℓ4, t0=X⁴−2, p65537, g77, t1=(X⁴−2)(X⁵²−2); r4938 satisfies t1(r)=0 but σ77(t1)(r)=48069≠0, so `σ77(t1)/t1` not integral, cannot use source's native GBFV Auto. Contrast n'16,n''4,b4,p257,g13 stage t1=16−X⁸ which is stabilized. Source already acknowledges invalid automorphism; no author error.
**NEXT_ACTION:** **HUMAN_REVIEW / recommend PARK** simple mask-only elimination of few-slot temporary BFV step. Reopen only with a source-compatible **compensated masked automorphism** definition that is independent of ciphertext plaintext lifts, fixes scaling by an implementable public operator, and beats source BFV detour in noise/key bytes/latency at matched security. On PI next “继续”, pivot to another parent gap with clear novelty/importance before more tiny roots or known ring-stability conditions.
**STATE_UPDATE:** **YES** — new full-source GBFV architecture branch independently falsified with exact representative, source acknowledgement explicit, preserving distinction from older I182 modular-u no-wrap audit and all previous PARKED lines.
