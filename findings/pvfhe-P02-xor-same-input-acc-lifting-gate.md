# PVFHE-P02 — XOR(ct,ct) carries the P01 XPow alias to a different public output in a special ideal source-shaped EvalGate

**Date:** 2026-10-14 (Asia/Tokyo). **Independent FHE+proof-systems track:** PVFHE-P02 COMPLETED, P03 NOT STARTED. PI said "好的，请继续" after P01.
**STATUS:** **PASS conditional exact algebraic propagation through ACC.Update/Extract and final modulus switch with an ideal zero-noise evaluator**, **UNCLEAR** complete source Rust/C++ RGSW key and generated-key probability, full compiled Ring-R1CS A/B/C satisfaction, concrete SNARG proof/verifier, security exploit against ordinary random keys, and corrected/latest-paper-version parity. No claimed SNARG forgery.

## Read before write / archival isolation

Read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md; current global STATE.md SHA `741f12ace1d5c5088423a6507764796361881732` which is separate vFHE V19; prior `findings/pvfhe-P01-ring-r1cs-bitdecomp-xpow-source-parameter-counterexample.md` SHA `83ac7399bd0f12b9b6873a814d7b35e3625ebfdc`. Target P02 file absent. No edits to global STATE.md, concurrent SHIP research, old PVFHE-P01 or shared backlog.

Primary source: Huang, Li, Mao, Zhang, *Fully Homomorphic Encryption with Efficient Public Verification*, IACR ePrint **2024/1764**, cached full 29-physical-page PDF SHA256 `7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089`, `VERSION_UNVERIFIED`, primary p12 Section4.1 ring setup, p13 Figure2 accumulator, p14 Algorithm2 EvalGate, p15 Lemma4.5/Claim4.6, p16 Lemma4.10 XPow, p17 Thm4.12, p26 AppendixB N/Q/q and C.1, p27 AppendixC.3, p11 vFHE construction. Independent FHEW function-table provenance: Micciancio–Polyakov, *Bootstrapping in FHEW-like Cryptosystems*, ePrint **2020/086**, physical p15 Table1 XOR sign LUT. Web PDF text accessible but BOTH requested PDF screenshots returned cache miss: the exact rendered formula/authenticated newest version are **unverified**. Source §4.1 says WLOG N=q/2, while AppendixB has N2048/q1024 (N is multiple of q/2); this inconsistency matters when extrapolating beyond literal Figure2 arithmetic and is NOT resolved here.

## ONE primary falsifiable hypothesis + ONE decisive source-shaped gate

**[HYPOTHESIS P02]** The P01 noncanonical bit witness for `XPow(0)=X^5 ≠1` is always killed by downstream fixed public inputs, ACC.Extract/KeySwitch/ModSwitch, or other FHE.EvalGate arithmetic when the input is a **legitimate repeated ciphertext** `XOR(ct,ct)`; therefore it cannot induce a different public final LWE output even in an ideal exact selector model.

**[DECISIVE TEST]** Follow source Algorithm2's `c=2(c1−c2)`, Figure2's `ACC.Update` with the ACTUAL source Q,N,q and a valid negacyclic XOR lookup function satisfying f(v+q/2)=−f(v). Inject P01's `alpha=Q ≡0 modQ` bit assignment at a fixed 20 target updates, for both plus and minus XPow branches. Use ideal zero-noise, zero-random-mask RGSW selector semantics, exact negacyclic ring arithmetic and source-shape final integer rounding; check for a distinct **public output ciphertext** and that later normalization uses ordinary canonical bits. The hypothesis is falsified if one concrete ideal evaluator with source-consistent zero/noiseless selectors gives a wrong public output. This DOES NOT imply the ordinary SNARG real-key attack probability is nonnegligible.

## Pinned original algorithm and public-input choice [FACT]

- Figure2 p13: `ACC.Init(b)=(0,m)`, `m(X)=Σ_{i=0}^{N−1}f(b−i)X^i` and
```
ACC.Update(alpha,(C1,C2)):
  c <- c + (X^alpha−1)*(c⋄C1);
  c <- c + (X^(−alpha)−1)*(c⋄C2).
```
For an encrypted ternary s_i, `C1` contains selector mu1 and `C2` selector mu2 with s_i=mu1−mu2.
- Algorithm2 p14: XOR/XNOR computes `c=2(c1−c2)`; parsing this c=(a,b), each of n updates takes `alpha_i=−a_i mod q`; extraction of accumulator, key-switching and modulus switching gives PUBLIC c'.
- Let **c1=c2=ct**, including an ordinarily randomized and valid input LWE ciphertext. Then `2(ct−ct)=0` exactly. So `a_i=0`, `b=0` for every i, regardless of input ciphertext randomness/secret. Correct EvalGate never changes the initialized accumulator because `X^0−1=0`.
- AppendixB source parameters `Q=2^53+5, N=2048, q=1024`. Lemma4.5 includes binary indices 0,...,53. P01 source-legal bits `x0=x2=x53=1` give sum `2^53+4+1=Q=0 modQ`, but `X^Q=X^5` because `X^4096=1` and `Q mod4096=5`. Assign this same noncanonical satisfying bit witness **independently** to both `XPow(+0)` and `XPow(−0)` at the first 20 `ACC.Update` instances only; all other zero-alpha calls use canonical zero bits.
- FHEW/MP21 XOR sign mapping Table1: f(v)=+A for residues v∈[q/8,5q/8)=[128,640), and f(v)=−A otherwise, where A≈Q/8. We use exact integer A=2^50 (nearest integer to Q/8). This function satisfies f(v+512)=−f(v); for each t0..20, f(5t)=−A, and f(0)=−A. The source p13 function-condition and author-cited MP21 Table1 both agree on this pattern. Its final q/8 **recentering** is described in MP21 but NOT explicit in paper's Algorithm2; output difference is tested before this optional correction.

## Algebraic full-path *conditional* witness [DERIVATION]

Choose the source-compatible **special ideal evaluator**: target GSW encryption of ternary s_i is an exact selector with zero randomness/noise, so `c⋄C1=mu1 c`, `c⋄C2=mu2 c`; choose z=0 and zero-mask/no-noise switching keys so source KeySwitch passes an input `(a=0,b_0)` to `(0,b_0)`. These are **degenerate** keys with negligible probability of being generated, NOT typical parameters, NOT a sampled keyset benchmark and NOT an implemented RGSW key matrix. Normal source KeyGen's s_i values are independent uniform ternary.

For each selected update with `s_i=+1` or `−1`, exactly one of mu1,mu2 equals1, and both fake XPow outputs are X^5, so:
```
c <- c+(X^5−1)c=X^5 c.
```
For s_i=0, both selectors zero and update is unchanged. Let t be the number of nonzero s_i among the first 20, 0≤t≤20. Correct accumulator body `m(X)=Σ_{i=0}^{2047} f(−i)X^i`; fake body `X^(5t)m(X)` for t>0.

For t>0, 0<5t≤100<2048=N. Negacyclic reduction says
```
   coeff_0(X^(5t)m) = −m_{N−5t}
                     = −f(−(N−5t)) = −f(5t) = +A,
```
because N=2048 divisible by q1024, and f(5t)=−A. In contrast `coeff_0(m)=f(0)=−A`. For t=0 fake==honest.

After ideal zero-mask KeySwitch, source AppendixB `floor(xq/2^53)` integer rounding (with centered or canonical final representation modq) gives:
```
 honest public body = floor((Q−A)/2^43) mod1024 = 896,
 fake for t=1..20 = floor(A/2^43) mod1024 = 128.
```
Both later output-bit `BitDecomp` and `Rounding` CAN use genuine **canonical** representations within [0,Q−1], each of whose bit equations holds exactly; no further noncanonicality is needed downstream. If the conventional public MP21 q/8=128 recenter were applied after the source's end, results become **0 versus 256** (distinct usual XOR output encodings). The source itself does not explicitly include this recenter, so do NOT treat it as performed by Algorithm2. Wrong public ciphertext `(0,128)` differs from honest `(0,896)` independently of optional recenter.

For independent source ternary s_i uniform {-1,0,1}, the 20-target selector subset has `Pr[t=0]=3^{−20}=1/3486784401`; hence **Pr[t>0]=1−3^{−20}**. **WARNING:** This is ONLY the probability that a nonzero selector is present; it is NOT a provable successful forged SNARG/IND-SA attack probability. Actual GSW noise, accumulator/subsequent operations, public evaluation keys and verifier proof generation have NOT been checked.

**Caveat on N:** This exact one-to-20-update sign flip uses literal Figure2 m(X) length N2048 and AppendixB q1024. Section4.1 also states 'WLOG assume N=q/2' for presentation; modifying the accumulator embedding for N>q/2 may change the shift-to-constant map. The standard N=q/2 case can require different numbers of malicious updates to cross an LUT boundary. We do NOT assert verified exact source production implementation from the displayed formulas.

## ONE executed exact source-shaped falsification

**Script actually executed:** `/mnt/data/pvfhe_p02_xor_same_input_gate.py`, SHA256 `31e3988b2bb611264328619b0c3baf6d8b9f0fc602dddabe5b16633d098e0e81`.
**JSON actually produced:** `/mnt/data/pvfhe_p02_xor_same_input_results.json`, SHA256 `a49c271ed1b4971242a3ea6a00cc268c2b7d4b62e404fb96dce5162e6b0e7c0a`.
All t∈[0,20] checked: 21/21 exact coefficient-0 computations and modulo-q output comparisons match formulas; f negacyclic identity checked over all 1024 residues; final coefficient bits and `Rounding` reconstruction checked with true canonical bit arrays, not fake bits; exact secret selector event evaluated as `1−3^-20`.
The script substitutes ideal GSW multiplication/key-switch identity rather than implementing full RGSW matrices, actual noise, 128-bit crypto security, Fiat-Shamir, full R1CS A/B/C or live proof generation. No measured ciphertext decryption. **Therefore no completed full SNARG attack.**

## Interpretation and next steps

**[PASS limited]** This disproves the P02 blanket barrier that a false XPow identity must be caught downstream: an ideal source-shaped one-gate accumulator's **PUBLIC output** can change when erroneous bits are used; the down-stream coefficient extraction, source-style rounded modulus switch and canonical bit witnesses do NOT supply automatic rejection. Unlike P01's stand-alone local lemma, it reaches the public-output arithmetic interface under transparent special assumptions.

**[OPEN]** The actual source Theorem4.12 `Ring R1CS SAT iff FHE.Eval outputs ct` is not yet falsified by an independently checked complete source-generated `A,B,C` matrix and full witness; exact native RGSW KeyGen sampling may alter even this source-shaped test. The real per-key wrong-output distribution and a valid published-SNARG proof/verification transcript are **unverified**. Authors' published version or erratum may differ. Distinguish relation encoding failures from breaking an otherwise sound SNARG and never claim IND-SA cryptanalysis without a real executable/proof.

**STATUS:** **PASS** one conditional symbolic full-path propagation test and 21 exact tests; **UNCLEAR / HUMAN_REVIEW** real Ring-R1CS full-witness acceptance and full cryptographic security. No verified paper exploit.
**RESULT:** `XOR(ct,ct)` forces public alpha=0 even on a randomized LWE ciphertext, and fake XPow(0)=X5 for 20 updates can change accumulator output from -Q/8 to +Q/8 in a special source-parameter ideal selector model. This motivates a genuine relation-soundness integration test rather than toy idempotent rechecking.
**NEXT_ACTION (PVFHE-P03 only after PI continuation):** ONE **real Ring-R1CS integration/satisfiability gate**. Recover/generate the exact constraints of source Lemmas4.5/4.8/4.10/4.11 and Theorem4.12 for one public XOR(ct,ct), use source-compatible GSW matrices (not ideal selector oracle), generate all intermediate witness wires including key switch and modulus switch, and independently evaluate each equality for the fake/true outputs with identical public ek. First test with noise0 nontrivial masks; only if PASS extend to ordinary random generated keys and proof commitment/verifier. If source implementation / exact constraint generator absent, label SOURCE_BLOCKED rather than assert actual forgery. Independently check newest authenticated paper version and potential correction before any author-impacting claim; **no unsolicited author contact**.
**STATE_UPDATE:** YES standalone PVFHE-P02 finding only. Do not edit global vFHE STATE.md, SHIP series or PVFHE P01.
