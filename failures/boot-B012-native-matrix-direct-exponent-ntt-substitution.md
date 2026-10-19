# BOOT B012 failure — GL plaintext-linear matrix arithmetic does not directly compute exponent-domain INTT

TRACK_ID: BOOT
ITERATION: B012
DATE: 2026-10-19
STATUS: FAIL_DIRECT_PORT (not a general impossibility theorem)

## Failed hypothesis
Directly replace 2025/696 Algorithm 3 homomorphic_dot_product by a 2025/1935 plaintext–ciphertext native matrix linear operation without converting or re-encrypting its original inputs Zi=GSW(X^{−zhat_i}), and lower encrypted computational cost.

## Decisive algebraic falsifier
For H=[[1,1],[1,-1]] and z=(1,1), desired output of exponent linear butterfly is (X²,1), whereas H applied as ordinary matrix arithmetic to the monomial-encoded inputs (X,X) produces (2X,0). These plaintext polynomials differ with zero encryption noise. For F(a,b)=X^{a+b} in Z_(2^16)[X]/(X^41−1), the mixed finite difference is X^{a+b}(X−1)^2 !=0, for all a,b; a separable affine map of X^a and X^b has zero mixed finite difference. Exact modular reference test: 1681/1681 nonzero mixed differences. This kills ONE direct bridge, not a novel cryptosystem or all possible ciphertext conversions.

## Why this is source-grounded
2025/696 §4.3 Algorithm 3 uses circulant Rtilde_Q-GSW encryptions of X^{-zhat_i} and homomorphic exponent-domain dot product (output X^{-<u,zhat>}). 2025/1935 §3.6 supplies pt-ct matrix arithmetic over already GL-matrix-encoded numerical entries; §4 integer version requires a plaintext root-of-unity congruence. Even t=41, n_mat=2, auxiliary p_aux=5 (satisfying t≡1 mod 40) can coexist arithmetically with 2025/696 incomplete NTT N=8,ell=1, p=41, but their encodings still differ. A full 8×8 GL native matrix under t=41 fails t≡1 mod 4*8*p_aux and the 32nd-root condition. Output reconversion to GSW exponent encoding is unsolved and may outweigh any native matrix savings.

## Decision
FAIL direct plaintext-linear substitution. No source bugs, attacks, FHE DFR, security or concrete performance improvement claimed. No formal lower bound ruling out ct-ct matrix multiplication, nonlinear encoding/re-encoding, regular representation or a different bootstrapping circuit.

Technical evidence: findings/boot-B012-native-matrix-incomplete-ntt-exponent-interface.md.
Source PDFs ePrint 2025/1935 SHA256 985173da6bc45f1c89c86769d5b6b16bfcdd98bf07e91476cd424778b8d9ec84; 2025/696 SHA256 100140416417ad19daf56cc556713ce29d30c68780a9009d7d6234d36f68f85a; versions unverified. Official PDFs HTTP 403, source physical pages inspected through research MCP text.

NEXT_ACTION: B013 evaluate regular-representation bridge z->P^z as one candidate alternative; algebra/size/operation count first, no unjustified claims. Preserve BOOT isolation.
