# I95 — PaCo negacyclic wrap demands conjugation; source Algorithm 4 already supplies it
Date: 2026-10-12. New separate FHE target after PI-approved archive of high-cost vFHE public-A/Brakedown repair branch.
Paper: Jean-Sébastien Coron, Tim Seuré, PaCo: Bootstrapping for CKKS via Partial CoeffToSlot, ePrint 2025/886 (ASIACRYPT 2025).
Research MCP full cached 35pp PDF SHA256 ee427d006097fabdbd30a0a4dc36ed09df5ffea68df30a0511cc154b303a936a; GitHub mirror VERSION_UNVERIFIED against official latest; mathematical PDF text overlines may drop in extraction. Original official ePrint landing https://eprint.iacr.org/2025/886.

## One hypothesis (FALSIFIED) and smallest test
Candidate correctness gap: If PaCo maps a coefficient array a in Z_q[Y]/(Y^C+1) to circle group psi(a)=exp(2pi*i*a/q), then performs a secret monomial blind rotation Y^u by ordinary Z^u multiplication and reconstructs wrapped coefficients as b_i+b_{i+C} without conjugation, the negative sign of negacyclic wrap will be lost.
Falsification condition: source algorithm already conjugates the rotated upper-half coefficients before combining them; then there is no bug of this type.

## Evidence
[FACT] Primary pp6–8 introduces Y^B+1 negacyclic blind-rotation and Fig3, pp18–20 §5.2–5.3 eq9–10 explicitly move to Y^C+1 and circle embedding; extracted PDF formula may lose complex overbars, so don't infer missing conjugation from text extraction.
[FACT] Primary Algorithm4 physical p24, line 8, explicitly sets ct'=Conj(Rot_C(ct)), with comment that one homomorphic operation can fuse conjugation and rotation; line 9 adds ct+ct'. Thus the candidate omission is actually addressed in source.
[DERIVATION] a'(Y)=Y^u sum_{j=0}^{C-1}a_jY^j mod(Y^C+1) has for i<u coefficient -a_{C-u+i}, for i>=u coefficient a_{i-u}. Map psi(-a)=conj(psi(a)). If b_i = psi(a_{i-u}) for u<=i<u+C, else 0 (b vector length 2C), then psi(a'_i)=b_i+conj(b_{i+C}), not b_i+b_{i+C} for i<u. Bit reversal and masks commute in prescribed source operations; source line8 corrects sign.
[MINIMAL COUNTEREXAMPLE to naive shortcut] C4, u2, a=(1,2,3,4). True negacyclic coefficients=(-3,-4,1,2). Without conjugation circular split gives (psi(3),psi(4),psi(1),psi(2)), wrong for q>8; with conjugation matches.
[EXACT TOY] Real circle-group identities validated algebraically using primitive 17th roots of unity in F_103 (omega=64), no floating-point rounding. Exhaustive C2 75 cases: naive wrong44, corrected wrong0; exhaustive C4 3125: naive wrong2344, corrected wrong0; deterministic random C8 5000: naive wrong4444, corrected wrong0; all combined 8200 pass corrected. It models sign/conjugation only, not actual encrypted approximate arithmetic or parameter security.
Script: /mnt/data/iteration95_paco_negacyclic_wrap_conjugation.py sha256 8328f00b362f44c5ba37b92084c5a4ac3e5d01f213fceaa25b9fec34cbd33cba.
JSON: /mnt/data/iteration95_paco_negacyclic_wrap_conjugation_results.json sha256 d8edab01fda16a463835e625b3ca8901d68ab8b7e0032cf4c646e51e48b976c0.

## Prior art and scope
Source Algorithm4 explicitly fixes sign, and existing independent PaCo-inspired implementation published on docs.rs/poulpy-ckks confirms a conjugate-rotate Psi tail. Not a correctness defect, publishable contribution, or security break. Novelty: NONE for this elementary identity.
Earlier alternative 2026 candidate full texts ePrint 2026/975 and 2026/956 were RETRIEVAL_BLOCKED via Research MCP (official403, missing fixed mirror); no technical claims made on abstracts. PaCo was read in full text from verified mirror.

## End
STATUS: **FAIL** candidate omission / PASS exact source-aware consistency test.
RESULT: The required complex conjugation is ALREADY present in PaCo Algorithm4 line8, preventing a false-positive audit based on lossy PDF equation extraction.
NEXT_ACTION (I96): One new distinct PaCo numeric correctness-boundary test: derive the ideal small-angle approximation error for (q/(2π))*sin(2π m/q) at |m|<=p using published §7.2 Table4 parameters I (log q29,log p22), II (log q44,log p32), and compare derived guaranteed worst-case precision with reported 12/22 retained bits. This is an ideal numerical bound, not a claim that paper omitted it; test the hypothesis whether this analytic approximation alone already sets most of the reported precision ceiling. Search existing literature claims before suggesting a technique.
STATE_UPDATE: YES — archived previous branch with PI approval, selected PaCo paper as new current target, and completed one falsifiable algebraic check. No author contact/outreach/public disclosure.