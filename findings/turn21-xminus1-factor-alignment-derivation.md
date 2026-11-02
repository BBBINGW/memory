# Turn 21 derivation

Let a=67 be the Algorithm4-entry intFactor and let P_t be a complete leading Context-digit target with modulus q_t. After real mod-down, the x branch keeps factor a. The fixed-target square has factor b_t=a^2*q_t mod625. The factor-preserving z=x2; z.addConstant(-6) keeps b_t. The fixed-target product x*z therefore has factor c_t=a*b_t*q_t=a^3*q_t^2 mod625.

Construct w=x on the same P_t and call w.addConstant(-1). This keeps factor a and adds a centered representative of exact magnitude C1_t=abs(balRem(a*q_t,625))<=312.

Define h_t=c_t*a^{-1}=a^2*q_t^2 mod625. Since q_t is a product of at least 30-bit ctxt primes and p=5, q_t is a unit modulo625, so h_t is a unit. Apply the internal public-unit factor update corresponding to Ctxt::mulIntFactor(h_t) to w. This multiplies both ciphertext parts and intFactor by the balanced representative of h_t and preserves plaintext semantics. Let H_t=abs(balRem(h_t,625))<=312.

After this update both branches have the same prime set P_t, ptxtSpace625 and intFactor c_t. A subsequent addCtxt therefore performs neither mod-up nor factor harmonization.

With Turn20 notation A_t=(q_t/Q0)E0+R, E2_t<=A_t^2+K_t and E3_t<=A_t*(E2_t+1872)+K_t. The x-minus-1 branch has Ew_t<=A_t+C1_t before alignment and <=H_t*(A_t+C1_t) after alignment. Hence

E4_t <= A_t*(A_t^2+K_t+1872)+K_t + H_t*(A_t+C1_t).

The authoritative selector should therefore choose the shortest complete-digit prefix satisfying E4_t<0.48*q_t. This condition subsumes the Turn20 cubic-only lookahead.

Using the conservative H_t<=312 and C1_t<=312 bounds, the full ctxt-prime set still has 49.0588425804811 bits of margin. The simple guard log2(q)>=110 remains sufficient under the current global maxima.
