# Iteration 37 — GL Gaussian inversion requires conjugating the coefficient i

Date: 2026-10-10.
STATUS: FAIL for the naive fixed-i variable-only inversion model, not an established error in the published construction.
NOVELTY NOT VERIFIED; elementary cyclotomic involution.

## Source and state
Read current GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md, GL integer composite-modulus archive, and GL generic BigSwitch archive. Did not reopen BigSwitch. No change to parked RIG-HE state.
[FACT] Original source: Craig Gentry and Yongwoo Lee, Fully Homomorphic Encryption for Matrix Arithmetic, ePrint 2025/1935; Research MCP cached the full 27-page PDF, SHA256 985173da6bc45f1c89c86769d5b6b16bfcdd98bf07e91476cd424778b8d9ec84, VERSION_UNVERIFIED.
Exact passages read:
- Section 2.1 physical pp.5–6: R' = Z[i][X,Y,W] / (X^n-i, Y^n-i, Phi_p(W)).
- Section 3.4 Observation 3.1 and Observation 3.2 physical p.11: complex conjugation and conjugate transpose under inverse-variable notation.
- Section 3.4 Theorem 3.5 physical p.12; Observation 3.7, Theorem 3.8 physical pp.13–14: trace product is intended to decode (1/n) A B^*.
- Section 3.5 Theorem 3.12 physical p.15, Section 3.6 Conjugation physical p.17: ciphertext trace operation and explicit automorphism (I,X,Y,W) -> (I^-1,X^-1,Y^-1,W^-1).
- Section 5.1 physical p.22: Z_q[i] splits into two field components when -1 is a square modulo q.
Source caution: extracted PDF text may omit bars over symbols. Cached PDF page images and latest 2026 CRYPTO version were not visually inspected. Do NOT claim a missing printed overbar or publication correctness error. Web search verifies 2026 CRYPTO appearance, but not text comparison.

## One primary hypothesis and decisive test
[HYPOTHESIS — FALSE] Fixed-i, variable-only inverse substitution b(Y^-1,Z^-1,W^-1) is a Z[i]-linear, well-defined operation computing the AB^* semantics in GL.
[FALSIFICATION CONDITION] Show a legal Gaussian polynomial where literal variable-only substitution differs from conjugate transpose, or show that it violates X^n=i.

[DERIVATION / EXACT] n=2,p=1, a=1,b=i. The decoded matrices are A=2x2 all ones and B=2x2 all i, so AB^* has all entries -2i, requiring normalized c=-i. Literal substitution that keeps i fixed gives Tr_Z(1*i)=+i. The correct involution sends i -> -i and gives the expected -i.

For X^n=i, any inversion tau(X)=X^-1 must satisfy tau(i)=tau(X^n)=X^-n=i^-1=-i. Thus tau(i)=i is incompatible with the quotient relation (when characteristic is not 2). The correct map is conjugate-semilinear on Gaussian coefficients: tau(i*a)=-i*tau(a). Consequently a Z[i]-linear implementation of Gaussian conjugate transpose is not possible in this representation.

[EXACT TOY CHECK] /mnt/data/iteration37_gaussian_involution_audit.py executes exact Gaussian integer pair arithmetic for b in {1,i,1+i,-2+3i}; normalized AB* matches conjugate(b) in each case, not literal b for imaginary coefficients. It verifies semilinearity. The q=17 split-CRT test with sqrt(-1)=4 shows b=i maps to (4,13), while conjugate(b) maps to (13,4); the two CRT components swap on conjugation.

## Interpretation
[NEGATIVE] No-conjugation fixed-i substitution fails algebraically and yields an incorrect matrix operation.
[SURVIVES] Original GL Section 3.6 explicitly names I -> I^-1, and thus already covers the missing coefficient action. The issue is a possible notation / implementation-interface trap, not a newly verified theorem error, security break, or publishable optimization.
[OPEN] Whether any particular source-code kernel or exact 2026 publication text omitted the coefficient swap was not checked. No claim that it did.
[PRIOR ART] Involution and CRT component swaps are standard. NOVELTY NOT VERIFIED. Keep this archive narrow and do not revisit this interpretation without new evidence.

## End of iteration
STATUS: FAIL (naive fixed-i conjugation hypothesis).
RESULT: Exact constant-polynomial counterexample and ring-relation proof require Gaussian coefficient conjugation i -> -i; the original paper Section 3.6 states the full map.
NEXT_ACTION: Archive this failed interpretation and choose another concrete construction-level research hypothesis grounded in an available primary source and distinct from prior archived GL BigSwitch branches.
STATE_UPDATE: NO — unrelated RIG-HE parked STATE.md unchanged.
