# Iteration 71 — CKKS rescaling computation-level soundness counterexample caused by rectangular CRT range checks

Date: 2026-10-11
Research target: Cascudo, Costache, Cozzo, Fiore, Guimarães, Soria-Vazquez, *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, IACR ePrint 2025/286, CRYPTO 2025; audit of §3.1–§3.4 and §4.1, especially Eq. (6), (7), (11), (13)–(15), the explicit Pi_CKKS composition, and §4.3's Pi_range.
STATUS: **PASS — explicit false CKKS arithmetic-computation statement satisfies source Eq(11)/(13) and the actually justified RECTANGULAR range predicates at PIOP algebraic relation level.** NO compiled SNARK/Fiat–Shamir proof forged and no real deployment attacked. This is stronger than I59–I61 standalone range-lookup examples: real CKKS zero×zero then rescale should give (0,0), while the admitted witness claims (22294,0).
Source limitation: complete 52pp revised-looking PDF was accessed via Research MCP, sha256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19, Git blob a549654c5dffa3484e95e8244056f4a27c48c3e6, mirror snapshot pinned 2026-04-28 (I69); source metadata still VERSION_UNVERIFIED versus current official IACR bytes. Official revision dated 2026-02-16 with prior Theorem4.8 fix; do not claim current official PDF bitwise authentication.
No author contact, disclosure, public issue or broad exploitation claims.

## Read-before-write, one primary hypothesis, cheapest decisive test
[FACT] Read AGENT.md, RESEARCH_PHILOSOPHY.md, separate parked RIG-HE STATE.md, and I70 `findings/vfhe-theorem48-actually-sound-rectangular-relation.md` before audit. Read primary §3/§4 physical pp10–17 and §4.3 pp20–24 via Research MCP. GitHub Notes RIG-HE STATE.md must remain unchanged.
[HYPOTHESIS — PASS at algebraic PIOP-relation level] The soundness degradation from the original coefficient-range T_B to its CRT rectangular closure T_B^rect is sufficient to make the CKKS rescaling system Eq(11),Eq(13) plus its range checks accept a FALSE full-computation input/output statement; other algebraic wiring constraints do not restore soundness.
[FALSIFIER] A hidden source check prevents a noncanonical remainder e_0 whose dropped-prime residue equals the correct remainder, OR output cannot satisfy the true embedded quotient ideal/range-relaxed oracle conditions, OR parameters cannot meet revised Theorem4.8. Test ONE minimal depth D=1 width W=1, two-prime, N8,d4 zero×zero computation. No new encoder/noisy security-parameter experiments.
[CHEAPEST TEST] Exact integer CRT and polynomial-factorization arithmetic + explicit base-β digit MLE Boolean-grid values and arbitrary bound transformations. No packaged SNARK implementation available or claimed.

## Key new universal theorem: the rounded upper bound becomes RECTANGULAR-VACUOUS
Let R_q=Z_q[X]/(X^N+1)≅∏_k F_k with F_k=F_(p_i)[X]/(f_k), f_k degree d, q=∏p_i. For B≥max_i p_i, original coefficient table
 T_B={Σ_(j=0..N−1)a_jX^j: 0≤a_j<B}
maps SURJECTIVELY to every field F_k: every field element has a degree-<d polynomial representative with coefficients in F_(p_i), each admitting integer lift in [0,p_i−1]⊂[0,B−1]. (d≤N.)
Hence the actually justified rectangular closure from I70,
 T_B^rect=Phi^−1(∏_k Phi_k(T_B)),
equals **ALL R_q** whenever B≥max p_i.
This is not true for original diagonal table T_B (unless B sufficiently huge to span Z_q digits, which is not the case here). The paper §4.1 explicitly optimizes key-switching and remainder ranges by rounding each p_i up to one shared B=2^u, with 2^(u−1)<p_i<2^u and the common u for selected RNS primes. Such checks become **completely vacuous in the rectangular language** even though β=2^(b/c)<p_min and 2^ell*<p_min can still hold.

## Original paper's full computation constraints (source anchors)
[FACT, §3.2 physical p11] q_0=∏_(i=0..L)p_i; z_l=CRT(1,...,1,0,...,0); at first top layer L=1, z_L=1.
[FACT, §3.3 physical p12 Eq(6)] rescale on c'_b uses reduction modulo dropped RNS prime p_l and inverse p_l^−1 in surviving modulus times z_l. Therefore Rescale of c'=(0,0) is exactly (0,0).
[FACT, §4.1 p13–14] Eq(11) checks d2−∑_i PW_ωl(1)[i] w_ks,i=0; Eq(13) checks algebraic quotient/remainder rescale relation using p_l^−1; Eq(14) requires quotient/output coefficients <q/p_l; Eq(15) requires remainder coefficients <p_l. Paper explicitly says correct computation is characterized by Eq(11), Eq(13) PLUS Eq(9),Eq(14),Eq(15) ranges.
[FACT, §4.1 p14–15] Optimization rounds all p_i remainder/decomposition bounds to 2^u for one batched range proof; §4.1 defines R_CKKS=C(x,w,y)=0 AND appropriate range predicate(s), and Pi_CKKS runs Pi_AC for C and Pi_range on batched w_2u, intermediate quotient values, and output y. §4.3 physical p24 gives arbitrary bound B∉2^Z by checking range [0,2^u) of both x and x−B+2^u. This transformation only holds with true integer coefficient membership; the two checks remain RECTANGULAR-VACUOUS when 2^u exceeds every RNS prime.
[CALCULATION PARENTHESIS] Page14 PDF math text extraction can make placement of p_l^−1 appear ambiguous (multiply entire rescaling difference vs only w_rem term). The constructed example sets c'_0=c'_1=0, so both parenthesizations yield the SAME y=−w_rem*p_l^−1. This removes that source-parsing ambiguity. Physical-page screenshots from stale official 50pp web cache failed; no false claim to visual source inspection.

## One legal exact toy parameter point and false CKKS result
Choose N=8, extension degree d=4, L=1 (two RNS primes), p0=149=4·37+1 and p1=157=4·39+1 (a odd as required by §3.1). Both 5 mod8. q0=23393 and R_q0=Z_23393[X]/(X^8+1).
Over p0, X8+1=(X4+44)(X4−44); over p1, X8+1=(X4+28)(X4−28), four irreducible degree4 field factors in total. All verified by sympy exact finite-field factorization; toy N8 is NOT a 128-bit secure CKKS parameter set, but satisfies source algebraic format.
Take common upper bound B=2^u=256, u=8 (128<149,157<256). Choose c=2=2^gamma, b=8, beta=B^(1/c)=16. Batched w_2u vector has 4 ring entries in one D1,W1 layer (two wks entries and two remainder entries) so ell=2, nu=log2 N=3, gamma=1, ell*=6, 2^ell*=64<min p149; beta16<149. Output vector of two ring elements has ell=1, ell*=5, 2^ell*=32<149. All revised Thm4.8 inequalities apply.
Use two **zero ciphertexts** input (0,0)×(0,0), so pre-multiplication yields d0=d1=d2=0, and set wks0=wks1=0; all original Eq(7)/Eq(11) inputs/gates honest. Legitimate eval-key values irrelevant because multiplied by wks=0. Thus c'_0=c'_1=0, and the TRUE CKKS rescale output is (0,0).
Define orthogonal scalar RNS CRT idempotents:
 e0=8792 ≡1(mod149), ≡0(mod157)
 e1=14602 ≡0(mod149), ≡1(mod157),
 e0²=e0, e0e1=0 mod q0.
Under first top-level rescale the dropped prime is p1=157 and the surviving prime p0=149. Inverse p1 modp0 is 56 since 157*56≡1 mod149, and z_L=1. Therefore p_l^−1 is represented by scalar 56 in R_q0 (as in paper Eq(6)).
Choose malicious remainder witness w_rmd,0=e0=8792, w_rmd,1=0. Although w_rmd,0 mod p1=0 equals the honest dropped-prime remainder of c'_0=0, its canonical coefficient 8792 is **not** <p1 or <rounded B256. Now supply public claimed output
 y0=−56e0 mod23393=22294, y1=0.
Then the rescaling algebraic equality (Eq13) holds identically for c'=(0,0) and this w_rmd, whereas true CKKS Eval/Rescale on zero is ytrue=(0,0). y0 mod149=93 and y0 mod157=0, so y is even supported on the surviving RNS ideal z_(L−1)=e0 (no hidden zeroed-RNS-component obstruction). Canonical integer y0=22294 exceeds BOTH candidate bounds q/p1=149 and q/p0=157; paper's Eq14 and final Eq15 range conditions reject it under TRUE coefficient range.
But with B256>max primes, Pi_range proves only T256^rect=R_q0: all necessary rounded checks accept in the ideal ring PIOP.
For paper arbitrary bounds B=149 or157, the two check transformations use x in T256 and (x−B+256) in T256. Each is rectangular-vacuous, so both accept, including for output y0 and remainder e0. No sumcheck or GKR arithmetic gate can reject because its enforced equations really hold for the malicious witness, by definition.
It follows that the actual *algebraic relation checked by the composite* (Pi_AC + fieldwise Pi_range) accepts a false R_CKKS statement at the ideal PIOP level. This is not merely existence of a false-range element.

## Explicit CRT-glued base-16 range proof witnesses (no handwaving)
For any scalar x∈Z_q, compute a=x mod149, b=x mod157. Since each residue is <256=16², form base16 pairs (a0,a1)=(a%16,a//16), (b0,b1) analogously. Set h_low=(a0e0+b0e1) modq, h_high=(a1e0+b1e1) modq, so every field projection of h_low,h_high is in table {0,...,15} and h_low+16 h_high=x in R_q.
 - Malicious w_rem,0=8792 => residues (1,0), digits (1,0) and (0,0), ring h=(e0,0).
 - Malicious y0=22294 => residues (93,0), base16 pairs (13,5) and (0,0), ring h=(13e0 modq, 5e0 modq), recomposition yields y0.
 - Output with arbitrary bound149 shift +107: y0+107 modq=22401, residues (51,107), base16 pairs (3,3) and (11,6), all valid field digits.
 - Remainder with true bound157 shift +99: e0+99 modq=8891, residues (100,99), base16 pairs (4,6) and (3,6).
 - All other remainder, key-switch and output entries are zero; the true `Pi_decomp` equations reconstruct each common ring witness exactly. Each field projection has honest integer lookup memory traces for these digits; by I59–I60 CRT-gluing the ring `Pi_beta_range` oracle products, first-round memory witnesses, root equalities and sumchecks all admit acceptance. We computed the explicit digit witnesses for entire batched vector, both output/shift bounds, and shifted remainder programmatically.
This is enough to construct honest field-projected PIOP algebraic proof messages and CRT-compose them; the actual full compiler transcript with polynomial commitment and Fiat–Shamir was not built.

## Reproducibility
Executed exact Python source:
 `/mnt/data/iteration71_vfhe_ckks_zero_rescale_rectangular_attack.py`
 SHA256 `5ddacb26bfec11894872ce3bdedd26f19093c0381258b7a1331d3ed06c4e2d67`.
JSON result:
 `/mnt/data/iteration71_vfhe_ckks_zero_rescale_rectangular_results.json`
 SHA256 `97ad3884aa48095a103f185d6f52b4c6567cdf99f814cb8ec96baf9868ed4b1c`.
Passes exact factorization, theorem parameters, CRT idempotents and valid RNS ideal support; validates false CKKS output, Eq11/Eq13, all original-range violations, fieldwise/CRT base16 witness decompositions and both arbitrary-bound shifts. No timing/noise experiments; SymPy emits only a modular-polynomial ordering deprecation warning.

## Impact, what is and is not established
[PASS] There is a concrete full computation-level **algebraic witness** falsifying original R_CKKS relation while satisfying actual PIOP-checkable equations and rectangular range relation; original paper's rounded ranges become completely vacuous in this setting. This is a substantive connection of I59–70 gap to CKKS Rescale, not another random coding variant.
[NOT CLAIMED] Practical IND-CPA/FHE confidentiality break, exploitation of an existing deployed verifier, fully serialized Fiat–Shamir SNARK forgery, statistical security at toy N8, or formal independent proof of the entire Pi_AC/GKR PIOP compiler. The intended vFHE soundness issue remains conditional on the inspected version and absence of extra checks not described in primary §4.1–5.
[PARAMETER SCOPE] Toy p149,157,N8 satisfy paper's exact algebraic format and Theorem4.8, but are not deployment security parameters. **Universal vacuity lemma** for B≥max p_i holds for arbitrary extension degree d and large p_i; source §4.1 applies 2^u rounding to clustered primes, so this is not an extreme-only situation.
[VERSION] Pinned mirror exists 2026-04-28 after official 2026-02-16 Theorem4.8 revision, yet exact newest official IACR PDF SHA still unavailable. Must retain VERSION_UNVERIFIED and privately verify with authors before public statements.
[DISCLOSURE] No author email/issue/release. PI decides contact.

## Next narrow decisive action
STATUS: PASS at ideal PIOP arithmetic relation/computation semantics; HUMAN_REVIEW as impact materially increased.
RESULT: True Eval(zero×zero)=zero but false y=(22294,0) is admitted by algebraic Eq11/Eq13 plus rectangular range checks. Rounded 2^u bounds become T_B^rect=entire R_q when B>max RNS primes. Explicit fieldwise base16 digit witnesses and arbitrary-bound shifts pass.
NEXT_ACTION: Independently audit *all* Pi_CKKS public interface/witness-binding, ideal-oracle Pi_AC and Pi_range composition for the exact D1/W1 zero-input-to-false-output trace. Specifically check if the output oracle Jy is tied to a public y with an extra check outside Eq11/13 + range, and whether a separate z_l ideal or positivity condition can forbid y=22294. If none, present PI a carefully qualified confidential author contact decision package with proof artifacts. This is one next technical test, not another coding branch.
STATE_UPDATE: NO — unrelated parked RIG-HE STATE.md untouched.
