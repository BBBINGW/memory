# Iteration 180 — Public noiseless mod-p CRT carry sidecar for BGV exposes RLWE secret

**Date:** 2026-10-13. PI authorized by “好的，请继续” after I179. Followed `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → `STATE.md` after I179 blob `412124615a4a9ebd0c25549c9275ca08036d1270`; read I179 and I178 finding. Exactly ONE primary security hypothesis and ONE decisive exact algebraic small-RLWE test. Not an attack against an actual deployed BGV, dBFV, authors' CRYPTO2026 scheme, or known AP13 ciphertext conversion.

## Source basis and scope

- **[FACT, cited original]** Peikert–Zarchy–Zyskind, *High-Precision Exact FHE Made Simple, General, and Fast*, CRYPTO2026, ePrint **2025/2321** https://eprint.iacr.org/2025/2321, complete Research MCP GitHub mirror 43 physical pages SHA256 `1e41b62004aeee0bf572d0ccca8de8c5827ee9a14fb333a1d3d0f4d2ab483849`, official latest binary VERSION_UNVERIFIED. Physical p3 fn1 states no known *direct* BGV port. Original §4.1 p19 defines `L=ker(ev_b:R[B]→R/p)`, §4.2 pp20–21 formal dBFV ciphertext `c(B,s)=μ(B)+e(B) (mod L)` in additive `K[B]/L`, and §4.6.1 p27 constructs short lattice reps for `p=b^d`. This paper **does not propose** our insecure public mod-p auxiliary sidecar.
- **[FACT prior art]** Alperin-Sheriff–Peikert CRYPTO2013 *Practical Bootstrapping in Quasilinear Time*, ePrint **2013/372**, full 28 physical pp GitHub mirror SHA256 `11cd6de60e5aeb89920aa8715bf6fa32e442fe4d8f650bab49ef866858551560`, VERSION_UNVERIFIED. Appendix A physical p25 offers **public** LSB/MSB ciphertext encoding transforms multiplying by `p,p^{-1} modq` and tracking plaintext factor `−q,−q^{-1} modp`; it does NOT attach an exact public modp decryption equation or expose s.
- **[Previously archived]** I178 naïve quotient `(R/qR)[B]/image L` zero for coprime p,q; I179 separately short-reducing public integer coefficient lifts of BGV ciphertext tuple changes plaintext via secret-dependent q-carry `qk(B)`. They do not prove no carry-aware alternatives exist.

## ONE primary hypothesis and decisive falsifier

**[HYPOTHESIS to KILL]** We can repair I179's secret-dependent `qk(B)` by publicly exposing a CRT sidecar of the ciphertext **component residues modulo p**, maintained under evaluation with the exact noiseless invariant
```
 b_p + a_p s = μ    (mod p)         [source sign convention +]
```
for each ciphertext. The sidecar is intended to be a public/no-online-FHE-carry method that allows digit-L reduction using an exact plaintext-mod-p congruence, independent of the mod-q primary ciphertext, while staying semantically secure.

**[FALSIFIER]** For a publicly known encryption of μ=0, find an invertible sidecar mask `a_p∈R_p^×`. The advertised exact congruence implies `s=−a_p^{-1}b_p modp`, recovering binary/small secret. Produce a completely consistent CRT lift with an ordinary valid mod-q BGV ciphertext and check all computations over an actual power-of-two negacyclic polynomial ring, not just scalar.

## Exact source-compatible RLWE ring test and general proof

Set `N=4`, `R=Z[X]/(X^4+1)`, `p=8`, `q=17`, coprime. Take small **binary secret** `s(X)=1+X²+X³` = coefficients `[1,0,1,1]`. Construct standard **noise-zero BGV LSB zero encryption** with q-mask `a_q=[2,3,4,5]` and q-body `b_q=−a_q*s (mod 17)=[5,6,16,7]`. Thus `b_q+a_q s=0 (mod17)`, encrypts known zero at zero noise (not a cryptographic-secure parameter size, but valid zero-noise correctness instance).

**Proposed PUBLIC exact CRT sidecar** modp: `a_p=[1,1,1,0]`, `b_p=−a_p*s (mod8)=[1,0,6,6]`, so `b_p+a_p s=0 (mod8)`. Using CRT coefficientwise modulo `pq=136` produces fully consistent **public** integer-lift polynomials:
```
 a_lift=[121,105,89,56],  b_lift=[73,40,118,126] (mod136),
 a_lift mod17=[2,3,4,5], b_lift mod17=[5,6,16,7],
 a_lift mod8 =[1,1,1,0], b_lift mod8 =[1,0,6,6].
```
Both `q` original phase and `p` sidecar phase were independently checked identically zero by exact modular negacyclic polynomial multiplication in a V8 isolated JS test.

Over `R_p=Z_8[X]/(X^4+1)`, `a_p(X)=1+X+X²` has exact polynomial inverse `a_p^{-1}(X)=1+7X²+X³`:
```
 (1+X+X²)(1+7X²+X³)=1 (mod8, X⁴+1).
```
The adversary, given only the public sidecar and known plaintext μ0, computes
```
 s=−a_p^{-1} b_p (mod8) = [1,0,1,1].
```
ALL exact arithmetic checked; brute force of all 16 binary length-4 secret candidates yields precisely one satisfying sidecar relation. Thus a single known-zero encryption with unit `a_p` **fully RECOVERS** binary s. No secret is input into the attack beyond choice of known plaintext and published sidecar. The CRT-lift construction itself would require encryptor to create this inconsistent-with-secure sidecar, but if a proposed secure scheme managed to publish it, it fails by the argument.

**[General probability, not just toy]** For any `N=2^r`, `p=2^k`, modulo2
```
 X^N+1=(X+1)^N (mod2).
```
Hence `F_2[X]/(X^N+1)` is local with sole residue field F2 at X=1. `a(X)∈Z_{2^k}[X]/(X^N+1)` is a **unit iff a(1) mod2=1** (units lift across nilpotent mod2 reduction kernel). For uniform public `a_p`, this occurs with **probability exactly 1/2**, independently of ring dimension. If a_p is uniform and independently sampled across m known-plaintext zero ciphertexts, probability at least one unit is `1−2^{-m}`; with one unit recover binary secret as above. This is **conditional** on the candidate scheme's a_p being uniform, not a universal bound for deliberately restricted sidecars. If a_p is forced nonunit, specific attacks/privacy/security need further analysis; no blanket impossibility of all metadata claimed.

**[Security versus correctness dilemma]** Exposing an exact noise-free *linear* secret-key equation mod p is incompatible with the standard RLWE goal of keeping s secret when masks may be units and known plaintext is available. To avoid the attack, one must NOT publish such exact unblinded modp component equations; options may include encrypting the carry/auxiliary info, randomizing it by hidden modp noise, restricting sidecar masks, using higher-level gadgets or proving a distinct security assumption. These alter the functional/cost/noise conditions and were NOT implemented or proved viable here. Ordinary BGV does not reveal this extra exact equation, even when its normal modq ciphertext is public; the attack is NOT against BGV.

**[Novelty]** Solving a noiseless linear equation over a ring using an invertible coefficient is standard elementary cryptanalysis; this is not new cryptographic technique or an original paper bug. Its role is a **decisive negative feasibility gate** for a plausible direct dBGV repair; no publishable contribution, runtime gain, or vulnerability in a deployed scheme.

## End of Iteration 180

**STATUS:** **FAIL** semantic-security/secret-hiding premise of publicly exposing an exact noiseless modp CRT carry sidecar under standard unit-mask distribution; **PASS** complete q17/p8 CRT-compliant RLWE toy and exact inverse key recovery, plus uniform unit-mask probability 1/2; **UNCLEAR** viability of encrypted carry, noisy/hidden sidecar, native dBGV and cost versus known dBFV+AP13.
**RESULT:** One known-plaintext-zero sidecar reveals s in `R_8` whenever a_p unit; exact example s=[1,0,1,1], a_p=[1,1,1,0], b_p=[1,0,6,6], inverse a_p=[1,0,7,1]. CRT lifts q17/p8 form a legitimate q ciphertext and the insecure p sidecar. General uniform mask invertibility probability1/2 for N power2,p power2. No actual BGV attack.
**NEXT_ACTION:** **HUMAN_REVIEW / recommend PARK the entire class of trivial public q-carry sidecars**. At I181 upon PI assent, do NOT assume the absence of native dBGV follows from I178–180. Decide whether a genuinely nontrivial **encrypted carry correction** can be specified with one credible, source-compatible correctness/noise/complexity lemma that improves on dBFV plus AP13; if no concrete candidate, recommend PARK broader dBGV direct-port exploration and choose a distinct fresh source-backed FHE contribution opportunity. Do not iterate more trivial q/p toy rings without a new security/algorithmic mechanism.
**STATE_UPDATE:** **YES**, material new SECURITY obstruction to no-cost exact public CRT auxiliary sidecar; the previous two distinct algebraic/correctness obstructions and AP13 prior art remain archived.
