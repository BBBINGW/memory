# Iteration 36 — Gentry–Lee integer matrix encoding: t ≡ 1 (mod 4np) alone is insufficient for composite t

Date: 2026-10-10
Paper: Craig Gentry, Yongwoo Lee, *Fully Homomorphic Encryption for Matrix Arithmetic*, IACR ePrint 2025/1935.
Scope: integer-matrix encoding (§4), not CKKS complex matrix construction, not RLWE security attack.
STATUS: PASS for a precise counterexample to the composite-t reading of the sufficient parameter condition; LOW novelty, likely an easy assumption clarification, NOT a publishable correctness gap.

## Continuity and original source
[FACT] Read current AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md (RIG parked), and MRFHE/GL failure archives before this iteration. No change to those files. Switched from the low-priority joint-packing branch after I35. GL generic BigSwitch was not reopened.

[FACT] Research MCP acquired the original PDF for ePrint 2025/1935 from fixed IACR GitHub mirror, cache READY, 27 physical pages, SHA256 `985173da6bc45f1c89c86769d5b6b16bfcdd98bf07e91476cd424778b8d9ec84`, VERSION_UNVERIFIED. The following passages were read from the parsed full PDF (equations visually unverified; plain modular condition readable):
- §2.1, physical pp.5–6: n is a power of two and p odd, with Z_p^* cyclic for simplicity; underlying rings R=Z[i][X,W]/(X^n-i,Phi_p(W)).
- §2.2 physical p.6: BGV plaintext modulus t satisfies gcd(t,q)=1; no global statement here that t must be prime.
- §4 opening and §4.1 physical p.18: condition **t ≡ 1 (mod 4np)** stated as sufficient to encode 2 φ(p) integer matrices; claims I=√(-1) always exists in Z_t because t ≡1 mod4; assumes X^n−I, Y^n−I and Phi_p(W) split into distinct linear factors and primitive 4n- and p-th roots in Z_t.
- §4.1 Eq.(5), physical p.19: integer encoding σ_int via evaluations at (I, ζ_j, ζ_k, η_l) and (−I, ζ_j^(-1), ζ_k^(-1), η_l^(-1)), yielding two sectors.
- §4.3 Theorem 4.1 physical pp.20–21: integer matrix multiplication relies on that encoding.
In the retrieved passages there is no explicit "t must be prime" requirement. If prime t is an **implicit** unstated convention, the counterexample instead identifies a documentation/scope clarification, not a false intended-domain theorem.

## One predeclared primary hypothesis and minimal decisive test
[HYPOTHESIS — TRUE, narrow] The congruence t≡1 (mod 4np) does not by itself imply that Z_t contains enough primitive roots for §4.1's invertible encoding if composite plaintext moduli t are admitted.
[FAILURE CONDITION] A composite t satisfying the congruence and gcd(t,4np)=1 but lacking I²=−1, an 4n-th root, or a p-th root, establishes the insufficiency.
[MINIMAL TEST] Choose legal n=2, p=3, M=4np=24; exact finite modular enumeration on composite t, with full-rank prime controls. No ciphertext experiment or estimator.

## Exact counterexamples
[DERIVED/EXACT] t=49=7² satisfies t≡1 mod24, but no I in Z_49 with I²≡−1. Any such I would reduce modulo 7 to a solution of X²=−1 in F_7, impossible since 7≡3 (mod4). So even the paper's stated I=√−1 prerequisite fails.

[DERIVED/EXACT] t=25=5² satisfies t≡1 mod24 and does have I∈{7,18}, I²=−1. But |Z_25^×|=φ(25)=20. By Lagrange, no element of multiplicative order 4n=8 or p=3 exists (8∤20 and 3∤20). Exhaustively, for either I=7 or 18, X²=I has no root, and Phi_3(W)=W²+W+1 has no root modulo 25. Thus the full σ_int encoding required by Eq.(5) cannot be constructed over Z_25. This failure exists for an infinite simple family 25^k≡1 (mod24), whose unit groups have order 4·5^(2k−1), still lacking order 8 or 3.

[EXACT POSITIVE CONTROLS] t=73 and 97 are primes ≡1 mod24. Build one primitive 8th root ζ, one primitive 3rd root η, I=ζ², and all 16 evaluation rows across two I=± sectors, n² X/Y coordinates, and φ(3)=2 W coordinates. In each field, the 16×16 evaluation matrix of basis monomials I^a X^b Y^c W^d (a,b,c,d ∈{0,1}) has exact modular rank 16. Exact observed ζ,η,I:
- F_73: (ζ,η,I)=(10,8,27), rank 16/16.
- F_97: (ζ,η,I)=(33,35,22), rank 16/16.
Reproducible: `/mnt/data/iteration36_gl_integer_encoding_modulus_audit.py`; output `/mnt/data/iteration36_gl_integer_encoding_results.txt`.
The CRT composite t=73×97 also has the requisite roots in each prime component, demonstrating composite moduli are not inherently excluded.

## Corrected domain
[DERIVED] A sufficient condition for the complete root-evaluation interpolation with t composite (under gcd(t,4np)=1, n power of two, gcd(4n,p)=1, and relevant Galois ordering) is: every prime divisor ℓ of t satisfies ℓ≡1 (mod 4np). For each prime power ℓ^e, distinct M=4np-th roots of unity lift via Hensel's lemma because ℓ∤M; their pairwise differences stay units since distinct modulo ℓ. CRT combines the evaluations over Z_t, yielding invertible Vandermonde factors. Equivalently one can require t prime with t≡1 (mod 4np). The original congruence on the **product t alone** gives none of those per-prime-factor guarantees.

## Research interpretation and limits
[NEGATIVE] The assertion "t≡1 (mod 4np) alone suffices for *any integer modulus t*" is false. The literal extension to all composite moduli fails at root availability, before ciphertext noise/security analysis.
[CONTEXT] If authors intended **only prime plaintext moduli**, their results may be completely correct as intended; no full general theorem was disproved for those intended parameters.
[PRIOR ART] Composite-ring NTTs requiring suitable roots and invertible root differences are textbook facts, e.g., number theoretic transform discussions; no novel cryptanalysis or optimized algorithm. Merely adding "t prime" or per-factor condition repairs this boundary, so not a publishable research contribution.
[OPEN] Does the authors' implemented integer-matrix scheme use only prime plaintext moduli? The retrieved proof uses roots but code-specific t values were not verified. Not needed to kill the all-composite-t hypothesis. Do not claim actual FHE execution failure for deployed configurations.
NOVELTY NOT VERIFIED; EXPECTED LOW.

## End of Iteration
STATUS: PASS (exact composite-parameter counterexample), but NEGATIVE for a publishable contribution in this form.
RESULT: n=2,p=3,t=49 and t=25 both satisfy t≡1 mod24 yet fail necessary integer-encoding root conditions; t=73 and97 admit a full-rank 16×16 evaluation map. Parameter condition must be strengthened if composite t is in scope.
NEXT_ACTION: Archive this elementary scope correction; for any new GL research idea, test a nontrivial construction property rather than revisiting primitive-root availability. Selection of next FHE research target is reserved to PI.
STATE_UPDATE: NO, since STATE.md holds separate parked RIG-HE state; GL status preserved in dedicated archive.
