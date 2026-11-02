# Turn19 retry companion A

Let G_0,...,G_{c-1} be the ordered disjoint Context digit blocks whose union is ctxtPrimes. For t=1,...,c set P_t=G_0 union ... union G_{t-1} and q_t=product(P_t).

At the first F4 square use the previously derived bounds log2(Q0)>=399.5, E0<=1.1433532886831608e35 and R<=83,891,200,000. Define K_t=8125*phi^2*(sum_{i<t} product(G_i))/S.

Select the smallest t satisfying ((q_t/Q0)*E0+R)^2+K_t<0.48*q_t. No monotonicity assumption is needed; enumerate the finite list.

Existence: P_c=ctxtPrimes and q_c=Q0. With K_c<=401,679,183,790,908.6, log2((E0+R)^2+K_c)<=232.92150915364357 while log2(0.48*Q0)>=398.44110631094645. Margin >=165.51959715730285 bits.

Hence a complete-digit target always exists under the same Turn14-17 preflight assumptions.
