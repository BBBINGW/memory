# Iteration 181 — An exact BGV q-carry can have full Boolean degree in the secret; linear encrypted corrections do not suffice

**Date:** 2026-10-13. One PI-authorized iteration (“好的，请继续”) after I180. Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` blob `6a2b9f05da637378a6406539f7747069cbacc261`, `findings/dbfv-bgv-public-crt-carry-sidecar-key-recovery-iteration180.md`, and I178–179 findings. One technical hypothesis, one deterministic algebraic degree/circuit-depth falsifier with an all-n constructive family. No novel algorithm, attack on published FHE, or claim of a general BGV lower bound.

## Primary original papers / provenance

- Peikert–Zarchy–Zyskind, *High-Precision Exact FHE Made Simple, General, and Fast*, CRYPTO 2026, ePrint **2025/2321**, https://eprint.iacr.org/2025/2321. Full 43 physical pages, Research MCP GitHub mirror SHA256 `1e41b62004aeee0bf572d0ccca8de8c5827ee9a14fb333a1d3d0f4d2ab483849`, official PDF VERSION_UNVERIFIED. §4.1 physical p19 defines integer digit lattice L; §4.2 p20–21 defines `K[B]/L` as **additive R-module** for dBFV ciphertext; §4.6.1 p27 reduces integer digit representatives. Original p3 footnote acknowledges no known **direct** BGV adaptation. §5.1 p31–32 already implements dBFV bootstrapping via BFV digit-wise rounding and remarks §5.2 p32 about nontrivial **nonlinear** homomorphic rounding. This source does NOT suggest the hypothetical encrypted q-carry shortcut below.
- Alperin-Sheriff–Peikert, *Practical Bootstrapping in Quasilinear Time*, CRYPTO 2013, ePrint **2013/372**, https://eprint.iacr.org/2013/372. Full 28 pages Research MCP GitHub mirror SHA256 `11cd6de60e5aeb89920aa8715bf6fa32e442fe4d8f650bab49ef866858551560`, official version unverified. Appendix A physical p25 gives folklore PUBLIC LSB/MSB ciphertext encoding conversion with factors p,p^{-1} and tracked plaintext units. Appendix B physical pp25–26 gives an actual **nonlinear integer rounding/MSB procedure** for homomorphic evaluation; the authors analyze multiplicative depth `ell−1=log_2(q/2)` for q=2^ell in their particular algorithm, NOT a universal complexity lower bound. Web opened the official PDF https://eprint.iacr.org/2013/372.pdf and attempted a screenshot of physical page26 (web index25); screenshot returned PDF cache-miss. The Research MCP source equations/text remain legible. This prior art establishes that homomorphic carry/rounding is an existing form of *decryption-function evaluation*, not a newly recognized primitive.
- Prior actual negative gates: I178 same-lattice mod-q quotient becomes zero; I179 public coefficientwise dBFV lattice reduction of BGV tuple changes ciphertext plaintext due to secret-dependent centered q carries; I180 publicly exposing exact noiseless modp auxiliary equations can recover secret in units case. All speculative proposals not source bugs.

## ONE primary hypothesis and cheapest falsifier

**[HYPOTHESIS]** To repair I179 while hiding the carry, it suffices to provide encrypted binary secret bits (or a standard linear key-switch hint) and compute the exact q-carry using only a *small fixed degree*, or entirely linear combination, in those encrypted bits, with no substantive nonlinear/bootstrapping-like work. The proposed mechanism would need to work for all valid LWE plaintext/ciphertext phases.

**[FALSIFIER]** Construct one **family** of public LWE coefficients `(a,b,q)` over binary secret dimension n for which centered q-carry is algebraically the Boolean AND of **all n bits**, i.e. unique multilinear polynomial has total degree n. Any universal affine or bounded-degree-in-n carry correction on encrypted secret bits fails for this family. Confirm by exact truth table and Möbius transform for n=4,8,12. The model allows only encrypted secret bits as atomic dependent inputs and ordinary binary (+,×) gates; special evaluation keys pre-encrypting high-degree predicates are excluded and could change bounds.

## General exact construction and restricted degree proof

Take `n≥2`, `q=2n+3` odd, `p=8` (or any p coprime with this q), public LWE coefficients `b=2`, `a_i=1`, secret bits `s_i∈{0,1}`. The *unreduced* phase is
```
 A(s)=2+Σ_{i=1}^n s_i,   2≤A≤n+2.
```
Center modulo q in `{−(q−1)/2,...,(q−1)/2}={−(n+1),...,n+1}`. Thus `A≤n+1` for every secret with at least one zero and needs no q-carry. Only for s=1^n, `A=n+2` wraps to `−(n+1)` with carry +1. Consequently
```
 k(s)=[A(s)−center_q(A(s))]/q = 1_{s=1^n} = Π_{i=1}^n s_i.
```
This equality holds for every binary vector and every n≥2. Note the original c=(a,b) has *different decrypted messages under hypothetical different secrets*; this is nevertheless a valid worst-case function family for any promised all-ciphertext/all-secret generic carry extraction, not a claim on fresh uniform mask distribution. Original-q ciphertext is not claimed to be a secure or typical fresh encryption across all keys.

Every Boolean-cube function has a unique multilinear representation over Z (and over Z_8) by Möbius inversion on subsets: `f(s)=Σ_{S⊆[n]} α_S Π_{i∈S}s_i`, `α_S=Σ_{T⊆S}(−1)^{|S|-|T|} f(1_T)`. In this construction exactly `α_[n]=1` and all others zero. Therefore its **algebraic degree is n**, not bounded degree independent of n. If an arithmetic circuit starts with individually encrypted s_i (each formal degree1), plaintext constants, addition, and fan-in-2 ciphertext multiplication, each multiplication layer at most doubles formal degree, giving `depth_mul≥ceil(log₂ n)` for exact k on all binary secret choices. Known homomorphic rotations/linear transformations alone cannot create this AND, and a *sole public affine key-switch correction* cannot compute it in that model.

**CRITICAL RESTRICTIONS:** This is a restricted Boolean-polynomial degree/depth statement, NOT a universal noise, runtime, security, circuit-size or depth lower bound for BGV bootstrapping or its variants. It does NOT rule out packed or special purpose evaluation keys with pre-encrypted nonlinear functions of s, polynomial evaluation over different rings, nonstandard bootstrapping gates, choosing modulus q to make carry special, or a construction that never explicitly computes k. It is a worst-case (a_i=1) family, not an average-case claim for uniformly sampled RLWE masks. It does NOT show cost relative to dBFV+AP13 in practical parameter regimes. It cannot by itself prove all dBGV implementations impossible.

## One exact test

Executed deterministic integer arithmetic and subset Möbius inversion in `functions.exec` for:
- n=4,q=11,p=8: all16 secrets tested, only `1111` has carry1, polynomial has exactly one nonzero multilinear term `s1 s2 s3 s4`, degree4.
- n=8,q=19,p=8: all256 secrets, only `1^8` has carry1, sole nonzero multilinear coefficient +1 at degree8.
- n=12,q=27,p=8: all4096 secrets, only `1^12` has carry1, sole coefficient +1 at degree12.
- With n=8: weight7 gives unreduced A9 and center9/carry0, weight8 gives A10, center−9/carry1.
- Arithmetic binary depth minimum for this family in the specified model is at least 2,3,4 respectively and balanced AND tree attains it. No cryptosystem executed, no security or timing metric inferred.

## Evaluation versus source and novelty

**[FAIL]** The narrow universal affine/constant-degree encrypted q-carry shortcut hypothesis. Exact carry is a nonlinear threshold function of a hidden LWE phase; a worst-case instance has full degree n in secret bits. This is consistent with AP13 Appendix B's explicit **homomorphic MSB/rounding** arithmetic and original dBFV §5.1/5.2 nonlinear rounding/bootstrapping, and strongly argues the next ordinary carry-correction attempt is **not a free linear representation change**.

**[PASS]** General algebraic construction/proof; exact exhaustive truth tables n4,8,12; restricted depth lower bound.

**[NO NOVELTY]** The observation that homomorphic decryption carry/rounding requires nonlinear operations is foundational FHE knowledge. This source audit is an elimination gate, not a paper flaw, new primitive, attack or high-value contribution. No efficiency/correctness/security proof for a new BGV scheme exists. The unresolved **direct dBFV-to-BGV adaptation** acknowledged by authors remains conceptually open; we have **NO specific new technique** that survives I178–181.

## End of Iteration 181

**STATUS:** **FAIL** general all-ciphertext cheap affine/bounded-degree q-carry-correction hypothesis / **PASS** exact degree-n counterfamily, Möbius verification and restricted `ceil(log₂n)` binary-multiplication depth bound / **UNCLEAR** any new carry representation with genuinely lower costs and full security.
**RESULT:** LWE binary secret dimension n, q=2n+3, public a=(1,...,1), b=2, centered q-carry equals AND(s1,..,sn). This excludes universal affine-only correction, consistent with AP13 homomorphic rounding and original dBFV bootstrapping. It is **not** a general FHE lower bound or practical impossibility.
**NEXT_ACTION:** **HUMAN_REVIEW — recommend PARK I178–181 naive dBGV port branch now** (four successive dead-end mechanisms, no concrete distinct solution). User/PI can reopen ONLY on an explicit source-compatible, secrecy-preserving, costed digit/carry invariant with a genuine benefit over existing dBFV+AP13. On next PI assent, pivot to another source-backed FHE target from `findings/OPEN_RESEARCH_BRANCHES.md` or new recent paper with verified full text; avoid more cheap q/p ring examples or restating known nonlinear rounding. The authors' real general BGV-adaptation open problem is not ruled out.
**STATE_UPDATE:** **YES** — closes cheap encrypted carry candidate and adds precise restricted complexity boundary to dBGV line, recommends archive/pivot while keeping broader mathematical open question explicit.
