# Turn 20 derivation

At Algorithm4 entry let Q0 be the full ciphertext modulus and E0 the independent representative envelope. For a complete leading digit prefix P_t with modulus q_t define A_t=(q_t/Q0)E0+R and K_t=8125*phi^2*(sum of products of the included complete digits)/S.

After the first fixed-target square, E2_t <= A_t^2+K_t.

Do not construct x^2-6 by creating a full-modulus constant ciphertext and then adding x^2, because stock addCtxt mod-ups mismatched prime sets and may also harmonize intFactors. Instead set z=x2 and call addConstant(-6) on z. This preserves the current prime set and intFactor. The added centered representative has magnitude at most 6*312=1872, so Ez_t<=E2_t+1872.

Bring a fresh copy of x down to the same P_t and multiply x by z using a fixed-target multiplication sibling that reuses tensorProduct and reLinearize without adaptive commonPrimeSet selection. A sufficient bound is

A_t*(A_t^2+K_t+1872)+K_t < 0.48*q_t.

This one-step-lookahead condition implies the first-square condition because A_t>1. Therefore it supersedes the Turn19 square-only selector for the paper construction.

Using the same conservative full-chain values E0<=1.1433532886831608e35, R<=83891200000, K_full<=401679183790908.6 and log2(Q0)>=399.5, the full set satisfies the x3 condition with margin 49.0588425804811 bits. A scalar sufficient guard using K_full and the 1872 constant bound crosses at log2(q)=109.92229506733422, so log2(q)>=110 is sufficient under these source-sized maxima.
