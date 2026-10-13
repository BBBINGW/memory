# Iteration 179 — dBFV-to-BGV mixed-modulus digit tuple: public per-component short L-reduction fails from secret-dependent q carry

**Date:** 2026-10-13 (JST). Human PI authorized I179 with “好的，请继续”, following I178's direct finite mod-q digit quotient collapse. Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` I178 blob `ef403349f6547a75510fca4573d1c812289464aa`, `findings/dbfv-to-bgv-modq-digit-quotient-collapse-iteration178.md`, and `findings/OPEN_RESEARCH_BRANCHES.md`. ONE primary hypothesis, ONE decisive exact correctness counterexample; necessary prior-art lookup AP13 is part of the hypothesis gate, not a second research idea. No code execution of encrypted schemes or security/noise/speed benchmarks. PI controls final park/pivot.

## Primary original sources (not snippets or unverified claims)

1. **[FACT]** Peikert, Zarchy, Zyskind, *High-Precision Exact FHE Made Simple, General, and Fast*, CRYPTO2026, ePrint **2025/2321**, https://eprint.iacr.org/2025/2321. Full Research MCP **43 physical pp**, `github-mirror` SHA256 `1e41b62004aeee0bf572d0ccca8de8c5827ee9a14fb333a1d3d0f4d2ab483849`, latest official **VERSION_UNVERIFIED**. Original p3 footnote1 explicitly says authors do not know a **direct** adaptation to BGV. Original §4.1 physical p19 Equation(4.1) digit lattice `L=ker(ev_b:R[B]→R/p)`, §4.2 physical p20 Definition4.3 **additive R-module** `K[B]/L` ciphertext and digit-error polynomial; §4.6.1 physical p27 nearest-plane for p=b^d: for each coefficient a_i of lifted polynomial write `a_i=q_i b+r_i`, retain centered mod-b `r_i`, carry `q_i` to the NEXT digit and discard last carry. This reduction maps any integer polynomial already in L to canonical zero, e.g. constant `−p` under p=b^d.
2. **[FACT]** Alperin-Sheriff, Peikert, *Practical Bootstrapping in Quasilinear Time*, CRYPTO2013 (AP13), ePrint **2013/372**, https://eprint.iacr.org/2013/372. Acquired *full original 28 physical pp* via Research MCP `github-mirror` SHA256 `11cd6de60e5aeb89920aa8715bf6fa32e442fe4d8f650bab49ef866858551560`, latest official **VERSION_UNVERIFIED**. Original §2.2 physical pp10–11 defines MSB ciphertext phase `(q/p)μ+e (modq)` and distinguishes LSB `μ+p e (modq)`; original **Appendix A physical p25** rigorously describes public transformation between LSB and MSB ciphertext encodings for coprime p,q by multiplying all ciphertext coefficients with `p^{-1} modq` (LSB→MSB) or `p modq` (MSB→LSB); transformed plaintext value is respectively `−q^{-1} μ (modp)` or `−q μ (modp)`, and known scale factor must be tracked unless `q≡−1 (modp)`. This is an **established public encoding change**, **not** a novel BGV implementation of dBFV's native digit lattice reduction or a proof that noise/security profile is identical through whole circuit. Research MCP original formula readable; attempted web screenshot of original PDF p25 (zero-index p24) gave *PDF cache miss*, so exact visual glyph parity is not independently screenshot-checked.
3. **[Prior I178]** Naive module transplant `(R/qR)[B]/image(L)` is zero for gcd(p,q)=1 because p∈L is invertible modq; `K[B]/L` stays meaningful as additive quotient not K-algebra. This iteration avoids THAT collapse by keeping independent BGV ciphertext components and an external integer digit lattice.

## ONE primary falsifiable hypothesis

**[HYPOTHESIS]** A natural alternative mixed-modulus dBGV wrapper can keep `d` ordinary *LSB/BGV* encrypted digit components `(c_{0,i},c_{1,i})∈Z_q²` encrypting `μ_i∈Z_p`, and after homomorphic arithmetic publicly lift each *ciphertext component polynomial* `c_j(B)` to an integer representative, separately apply the SAME short lattice representative reduction `Reduce_L` from dBFV §4.6.1, then re-encode modulo q. The resulting ciphertext tuple would preserve the combined plaintext `μ=Σ_i μ_i b^i modp` without extra encrypted carry metadata, while enabling the low-error-growth trick.

**[CHEAP FALSIFIER]** Find ONE legal noise-zero scalar BGV-LSB ciphertext where decryption must center modulo q before reading μ modp, with *nonzero secret-dependent q carry* in the chosen integer lifts; apply actual source §4.6.1 p=b^d nearest-plane to each public ciphertext component; compare the exact decrypted combined message before vs after. If different, the proposed unconditional public reduction is not a correct ciphertext operation, irrespective of cost/novelty. AP13's public conversion is checked as baseline prior art and to avoid conflating an LSB/MSB representation switch with a BGV-native L-reduction algorithm.

## Exact scalar integer counterexample: SUCCESSFULLY FALSIFIES

Set **p=8, q=17, b=2, d=3, s=1** (scalar version R=Z; valid algebraic BGV-LSB, not security parameters). Digit lattice `L=ker(ev_{B=2}:Z[B]→Z_8)=(8,B−2)`. Ciphertext two component polynomials are both the **constant** `c0(B)=−8`, `c1(B)=−8` (centered residues modulo17). Each is legitimate mod17; for secret s=1, the *mod-q LSB decryption phase* is `[c0+s c1]_{17}=[−16]_{17}=1`. Therefore first digit decrypts `μ_0=1 mod8`, other two digits 0, **combined original plaintext μ=1 with zero noise**. Such a ciphertext can arise from a chosen uniformly sampled mask a at this toy modulus and a zero encryption error, with a fresh-encryption sign convention; no security claim or random sampling rate is involved.

Source §4.6.1's `p=b^d` reduction of each public *integer* coefficient polynomial separately maps **−8∈L to zero**. Concretely `−8` has quotient digits:
```
digit0: −8 = (−4)*2 + 0  → forward −4
digit1: −4 = (−2)*2 + 0  → forward −2
digit2: −2 = (−1)*2 + 0  → discard final carry
=> Reduce_L(−8)=0.
```
Thus after separately reducing `c0,c1`, resulting ciphertext is `(0,0)`, whose LSB plaintext is `0`, **NOT 1**. Both before and after have zero cryptographic noise at scalar decode. The failure is algebraic, not due to approximate FFT or invalid large noise.

**Underlying obstruction, general identity:** Let `\tilde c0(B),\tilde c1(B)∈Z[B]` be integer lifts of mod-q encrypted digit component vectors. Write
```
\tilde c0(B)+s\tilde c1(B) = μ(B)+p e(B)+q k(B)
```
for a chosen centered decoded digit polynomial `μ(B)+pe(B)`. The carry polynomial `k(B)` is generally **secret-dependent** and cannot be assumed to be in the digit lattice `L`. If we subtract public `L` members `ℓ_0,ℓ_1` separately, the integer lift becomes
```
 μ(B)+p e(B)+q k(B) − ℓ_0(B)−sℓ_1(B).
```
Although `ℓ_0+sℓ_1∈L`, `q k(B)` need not lie in L when gcd(p,q)=1. Decryption of the re-encoded modq result may choose a *different* centered modq carry `k'(B)`; evaluating at b modulo p may then change plaintext by `q(k−k')(b) modp`. This is why publicly reducing integer coefficient lifts mod L is not an operation well-defined on mod-q BGV ciphertext **classes with maintained decoding**, unless some additional mechanism tracks/corrects quotient carries (or imposes restrictive safe ranges).

For the counterexample `\tilde c0+s\tilde c1=−16 = 1 −17`, initial decoded `μ(B)=1` and `k=−1`; after reduction ciphertext 0 has `k'=0, μ'=0`. Difference `q(k−k')=−17≡−1(mod8)`, taking plaintext1 to 0. The previous I178 zero-ring collapse and this I179 hidden-q-carry failure are **different obstructions**.

**Baseline AP13 numeric sanity check:** For p8,q17, `p^{-1} mod17=15`; LSB scalar v=1 encrypts μ=1, convert to MSB `w=15 mod17` whose centered representative is −2 and MSB rounding `round((8/17)*−2)=−1≡7(mod8)`; `−q^{-1} μ=−1≡7(mod8)` agrees with AP13. Converting w back by p gives v=1 and plaintext `−q*7 ≡1(mod8)`. This checks *known* transform; it does not remove secret-dependent per-digit q carry or create new evaluation semantics.

**Limits:** This fails only a **particular algorithm** (independent public `Reduce_L` of each modq ciphertext component and modq re-encoding, without encrypted carry corrections). It **does not prove** that a BGV-flavored dBFV scheme is impossible, that a public LSB↔MSB conversion cannot implement dBFV internally, that secure parameter choices are attacked, or that original dBFV authors overlooked a bug. A genuine candidate would require a coherent invariant for q-lifts and p-digit lattice, noise analysis across multiplication/relinearization/modswitch, plus a demonstrably superior 128-bit security matched application compared with dBFV+AP13 conversion. The counterexample is one elementary obstruction, not publishable by itself.

## End of Iteration 179

**STATUS:** **FAIL** unconditional correctness of naive mixed modq-BGV ciphertext tuple + per-component dBFV short-lattice reduction; **PASS** original AP13 Appendix A prior-art comparison and exact zero-noise q-carry counterexample; **UNCLEAR** any native coherent efficient dBGV with encrypted carry management or nontrivial gain over dBFV plus AP13.
**RESULT:** p8,q17,b2,d3,s1,c0=c1=−8 constant polynomials are a valid BGV-LSB zero-error encrypt of digit1, but independent `Reduce_L` sends both to0, changing decrypted digit1→0. General obstruction from `q k(B)` not in L; q-carry depends on secret s. AP13 only gives public coefficient scaling p,p^-1 with known plaintext scaling -q,-q^-1, not an error-free digit-lattice reduction.
**NEXT_ACTION:** **HUMAN_REVIEW; recommend PARK naive mixed tuple reduction**. A follow-up I180 *only on PI assent* should first seek a **concrete distinct public/encrypted q-carry-correction mechanism** or source-compatible BGV level invariant with one explicit output correctness lemma; if all variants merely wrap dBFV+AP13 or require full expensive homomorphic carry/rounding, PARK broader dBGV direct-transfer idea promptly. Do not repeat the toy, zero-ring argument, or claim a new proof gap in original dBFV.
**STATE_UPDATE:** **YES** — source-backed AP13 prior art, a new distinct exact q-lift carry obstruction, explicit dead-end and remaining nontrivial technical requirement.
