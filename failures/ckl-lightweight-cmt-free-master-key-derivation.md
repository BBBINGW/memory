# Iteration 39 — CKL lightweight CMT: one stored master key does not imply free derived keys

Date: 2026-10-10
Research focus: CKL 2025/1957 §5.3 hierarchical rotation-key generation.
Status: FAIL for the *free key derivation / unchanged key error* hypothesis. This does NOT allege an author overclaim or an incorrect CKL lightweight CMT construction.

## Provenance and previous state
[FACT] Read AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md and Iteration 38 failure plus earlier archived MRFHE CKL composition. No GL BigSwitch or MRFHE joint packing branch reopened. STATE.md remains parked on distinct RIG-HE.
[FACT: PRIMARY] Jung Hee Cheon, Minsik Kang and Junho Lee, *Fast Batch Matrix Multiplication in Ciphertexts*, ePrint 2025/1957, Research MCP cached 32 physical pages (GitHub ePrint mirror, SHA256 ab063dd495542ebee0004bf0211cabd3e7af978ae71dc95995973dba45c7aa9a; VERSION_UNVERIFIED).
- §5.1 Algorithm 3 physical p.20: CMT invokes d homomorphic Auto(key switching) operations and TWEAK permutations. Not one online rotation.
- §5.3 physical p.21: subgroup H={2ki+1 : i=0..d−1}=⟨5^(k/2)⟩ modulo 2N (for power-of-two N=dk and k even). A single higher-modulus master automorphism key and trivial (0,p) starting ciphertext generate rotation keys; d online automorphisms still required for CMT.
- §7 Table 1 and Table 2, physical pp.26–27: explicitly distinguishes d rotation operations from key count, and gives *lightweight* key storage in parentheses; for d=64 CCMM, 41.9 MB normal versus 0.79 MB lightweight, reported by authors, not reproduced here.
[FACT: PRIOR ART] Joon-Woo Lee et al., *Rotation Key Reduction for Client-Server Systems of Deep Neural Network on Fully Homomorphic Encryption*, ASIACRYPT 2023, ePrint 2022/532, Research MCP acquired original full text (45 physical pages, PDF SHA256 1cd4c9b632ba19fb4c27fec549bac84d85d0a988d84db93212971d86630c936f, VERSION_UNVERIFIED). Its §3.2 Algorithm 2 RotToRot physical pp.14–16, Theorem 1 proof physical p.41, expressly performs homomorphic automorphism followed by higher-level key switching to derive lower-level keys, with new error. §3.1/§3.2 physical pp.13–17 and Appendix C pp.42–43 require appropriate modulus hierarchy and show ModDown noise; §4 physical pp.18–22 covers bundling/hoisting/key-generation order. Therefore *extra derivation time and noise are already known*, not a new research insight.
[SOURCE QUALITY] PDF text parsed from Research MCP, not an image verification. Text extraction may garble subscripts and powers. Key equations here are independently established in a standard toy model; do not claim exact runtime or CKL production noise bound.

## Primary hypothesis and cheapest falsifier
[HYPOTHESIS — FALSIFIED] Starting from the one master rotation key in §5.3, derive all d keys with just Galois coefficient permutations, without *additional* key-switch operations or additive evaluation-key noise; thereby preserve the noise distribution of direct key generation at equal modulus.
[FAILURE CONDITION] The newly transformed evaluation-key ciphertext is encrypted under σ(s), not s, requiring key switch; show explicit nonzero inherited error when applying master key.

## Algebra / derivation
[DERIVED] In a negacyclic ring R_q = Z_q[X]/(X^N+1), let σ(f(X))=f(X^g), g=5^(k/2) mod 2N. For c_j=(B_j,A_j) under s satisfying B_j+A_j s=P σ^j(s)+e_j, σ(c_j) decrypts under σ(s) to P σ^(j+1)(s)+σ(e_j). Thus to continue under s:
  c_(j+1) := KS_(σ(s)→s)(σ(c_j)).
Under standard gadget key switching, if key encryptions satisfy B_l+A_l s=G^l σ(s)+ε_l and a=∑_l D_l(a)G^l, then the additional noise is ∑_l D_l(σ(A_j)) ε_l (and RNS schemes also incur ModDown/rounding noise). Consequently
  e_(j+1)=σ(e_j)+ε_KS,j.
Coefficient norm of σ(e) is unchanged (signed permutation) for the power-of-two cyclotomic ring, so if each per-stage error has infinity norm ≤B, then ||e_j||∞≤||e_0||∞+j B (conservative, conditional model). **Not** a lower bound nor a real CKL noise estimate.

A stored single master key is not the same as a single online switch: CMT Algorithm 3 still invokes d switches. Derivation from the trivial key to all d−1 others via the straightforward sequential RotToRot chain has (d−1)*L *offline ciphertext* key-switching operations if an evaluation key contains L gadget ciphertexts. This is not a universal operation lower bound: RNS/hoisting/efficient generation strategies may reduce costs. If derived keys are cached all at once, transient storage scales with d; if regenerated on demand, memory can remain low at the price of additional runtime.

## Exact toy decisive verification
[EXPERIMENT] Script /mnt/data/iteration39_ckl_master_key_derivation.py, fixed seed 20261039. R=Z_65537[X]/(X^8+1), g=5 with order d=4 modulo 16 (powers 1,5,9,13), k=2, gadget G=16 with L=5 balanced digits. Common ternary secret. Master KSK encrypts G^l σ(s) with noise coefficients in {-1,0,1}. Starts with trivial encrypted vector (0,G^l) for all gadget levels. For every j, executes σ and full standard polynomial gadget key switch to obtain encryptions of G^l σ^j(s), all under the original s; exact coefficient decryption relations asserted mod q.

Observed per-key max centered errors for indices 0..3: 0, 1, 46, 63. Cumulative derived *ciphertext* switches: 0, 5, 10, 15. In 32 independent seeds, index-2 derived error nonzero 32/32, and index-3 total squared error exceeded index-2 32/32. All observed errors stayed well within q/2. These are toy observations, NOT universal monotonicity or security/CKKS precision claims. The toy does not instantiate CKL's special-modulus P,P' hierarchy, RNS base extension, or ModDown. In actual hierarchical key systems the master key generally uses higher modulus than a derived key; modulus and rounding constraints must be analyzed separately.

## Conclusion and novelty
[NEGATIVE] Mere automorphism cannot move a key back under s; KS adds cost and potentially noise, and one-master storage does not lower online CMT's d automorphism count. Free derivation claim FAILS.
[SURVIVES] CKL lightweight CMT is algebraically compatible with established hierarchical rotation-key derivation; one-master-key design may be valuable for transmission or persistent storage, and the authors have explicitly identified this use case.
[PRIOR ART] Extra server-side key generation, modulus hierarchy, and noise are already addressed by Lee et al. ASIACRYPT 2023. No new flaw/optimization established; NOVELTY NOT VERIFIED, expected LOW. Do not return to this as a new contribution absent a genuinely different mechanism.

## End of iteration
STATUS: FAIL (free/noiseless master-key expansion).
RESULT: A precise σ(s)→s conversion and inherited key-switch noise term are unavoidable in standard on-the-fly key derivation; q=65537 exact toy confirms nonzero derived-key noise, while original CKL CMT still requires d online automorphisms.
NEXT_ACTION: Archive this branch. If PI authorizes a distinctly new target, first inspect the full primary text of a newer CKKS bootstrapping or programmable-bootstrapping method and isolate one unaddressed **concrete** dominant cost; do not continue lightweight-CMT key-chain noise sweeps.
STATE_UPDATE: NO (RIG-HE parked STATE.md preserved).
