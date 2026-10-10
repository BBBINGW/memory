# Iteration 49 — Switching Grafting rescale before relinearization introduces an extra s² rounding term

Date: 2026-10-10
Status: FAIL for naive noise-neutral operation reordering. Original paper already uses safe order; no correctness error alleged.

## Continuity
[FACT] Before working read GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md and I48 `failures/ckks-quintic-delayed-generalized-relin-prior-art.md`. I46–I48 generalised lazy relinearization archived, not reopened. RIG-HE is a distinct parked project, leave STATE.md untouched.

## Sources and provenance
[FACT / PRIMARY FULL TEXT] Cheon et al., *Grafting: Decoupled Scale Factors and Modulus in RNS-CKKS*, IACR ePrint 2024/1014. Research MCP acquired full original 20 physical pages, GitHub mirror SHA256 `f50de6671019f6f71c69f24f7686f21a21ab1cb5dd70bb2f66cb12a96da1ce4c`, VERSION_UNVERIFIED.
- §3.1, Definition3.1 and Theorem3.2 physical p.7: rational rescale uses Inv-RS and RS/ModDown, and for a standard degree-one (2 component) ciphertext the bound is proportional to (1+||s||_1)/2 times the number of eliminated RNS blocks.
- §3.1 Algorithm1 physical p.7: Tensor -> KeySwitch -> Rational Rescale. Authors already use the order that avoids direct degree-two-component rescale.
- §3.1 Algorithm2, Lemma3.3 physical p.8: modulus adjustment explicitly tracks integer-rounding perturbations; do not assume rounding is zero.
- §3.2 Algorithm4 physical p.10: key switching for grafted ciphertext moduli. The temptation motivating this test is to perform it at the smaller output modulus to reduce RNS arithmetic.
- §3.3 Algorithms5–6 physical p.10 address power-of-two sprout arithmetic, not needed for this test.
[EXTERNAL CHECK] Seoul National University peer-reviewed proceedings record, https://snu.elsevierpure.com/en/publications/grafting-decoupled-scale-factors-and-modulus-in-rns-ckks/; note available 2024 ePrint mirror version is unverified against proceedings.
[TEXT QUALITY] Exact equations from parsed PDF can have broken superscripts; derivation independently verified from polynomials, no dependence on potentially garbled long displayed lines.

## Single primary hypothesis / cheapest decisive test
[HYPOTHESIS — FALSIFIED] Switch the order in Grafting Algorithm1 to Tensor -> Rational Rescale -> KeySwitch, so switching happens over fewer RNS limbs, **without increasing the two-component rescale noise envelope** or requiring additional precision margin, when rescale is applied independently to the three tensor components.
[DECISIVE FALSIFIER] Construct one valid tensor ciphertext and sparse ternary secret for which the rounding error of the three-component rescale exceeds the norm envelope obtained if one ideal-relinearizes first and then rescales the resulting two-component ciphertext.
[TEST] A single exact integer nearest-rounding / negacyclic multiplication witness. Do not run encryption/benchmarks or parameter scans.

## Proof-level calculation
[DERIVED] In the standard negacyclic ring R, three-component tensor ciphertext C=(c0,c1,c2) decrypts as D(C)=c0+c1*s+c2*s². For coefficientwise integer rescale by R, let rho_j=round(c_j/R)-c_j/R, |rho_j|∞≤1/2.
- Paper's order: key-switch to degree1 first; then rescale a pair, with coefficientwise noise E_after=rho_0'+rho_1'*s and bound ||E_after||∞≤(1+||s||_1)/2, apart from relin noise, which is attenuated by the later rescale.
- Hypothetical swapped order: rescale all three coefficients first; then even a **perfect, noiseless** reduction to degree1 leaves E_before=rho_0+rho_1*s+rho_2*s² and bound ≤(1+||s||_1+||s²||_1)/2. Rescale-after-KS errors contain no rho_2*s² term.
For sparse ternary key weight h, ||s²||_1≤h². For contiguous s=Σ_{j=0}^{h-1}X^j, with N>2h−2, equality ||s²||_1=h² is attained. This is worst-case not average-case; correlations, wrapping, and concrete gadget errors matter for real CKKS.

## One exact counterexample
[EXPERIMENT] Local script `/mnt/data/iteration49_grafting_relin_rescale_order_audit.py`, SHA256 `e1b6d52afc01cfebd588b927ce619ed39b21dd4af01706fd5ecaaba70e4c67bb`; verified output `/mnt/data/iteration49_grafting_relin_rescale_order_results.txt`, SHA256 `d2b5719acfd5623b5672cf0ecc010538d39e0fc5582ccc199b519a31d3cc3ef4`.
R=Z[X]/(X^16+1), h=4, s=1+X+X²+X³, s²=1+2X+3X²+4X³+3X⁴+2X⁵+X⁶, ||s||_1=4 and ||s²||_1=16. Input c0,c1,c2 small integer polynomials with coefficients in {-1,0,1} selected so each independent coefficientwise divide-by-3 rounding residual aligns positively at output coefficient index0 after multiplication by its corresponding key power. Uses Python Fraction for exact arithmetic, no modulo wrap (can embed in sufficiently large divisible-by-3 ciphertext modulus).
- Pre-relinearization RS: decrypted max coefficient rounding error 7, coefficient0 error 7.
- Post-relinearization RS: decrypted max coefficient rounding error 1, coefficient0 error 1.
For the baseline, `(c0+c2*s²,c1)` stands in algebraically for a perfect relinearization; it uses s symbolically and is NOT a publicly computable HE key-switch routine. Crucially, even if key switching introduced ZERO noise, the reordering already gives a 7× worse noise magnitude for this exact input. Ordinary integer factor3 rescale is a special case encompassed by Grafting rational-rescale notation: failing this class rules out universal drop-in ordering, not every parameter choice.
Worst-case 1/2 norm envelopes here: (1+h)/2=2.5 vs (1+h+h²)/2=10.5. Observed exact errors 1 and 7. Security, NTT/RNS implementation, gadget decomposition, and real runtime NOT modeled.

## Research judgment
[NEGATIVE] Plainly swapping KS and RS changes the ciphertext degree during independent component rounding and may introduce an s²-amplified precision loss. Original paper Algorithm1 is not incorrect; in fact its order prevents this simple obstruction.
[OPEN] Specialized correlated high-degree rescale, different key encoding, or an accepted precision budget may mitigate the cost, but no new concrete mechanism or improvement verified. Key switching after RS injects its noise later without attenuation, another non-free effect.
[NOVELTY] Low; routine extension of two-component rescale error analysis to degree2 ciphertexts, useful for avoiding a bad optimization but not a publishable result.

## End of iteration
STATUS: FAIL — naive rescale-before-relinearize does not inherit the two-component error bound.
RESULT: Exact negacyclic h4/N16 divisor3 witness: noise 7 with early rescale vs 1 with late rescale; obstruction is rho_2*s². No Grafting theorem contradiction.
NEXT_ACTION: Archive this ordering variant. In the next distinct iteration, inspect one concrete §3.2 Algorithm3/4 *cost-relevant* boundary, first reading its stated assumptions; do not repeat noise experiments for this ordering without a genuinely different rescale method.
STATE_UPDATE: NO — unrelated parked RIG-HE state unchanged.
