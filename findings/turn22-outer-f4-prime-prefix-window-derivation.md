# Turn 22 derivation

Use Turn21 notation on a fixed target P with modulus q. Let A=(q/Q0)E0+R, K=K(P), E2=A^2+K, E3=A*(E2+1872)+K, and E4=E3+H*(A+C1), where H=abs(balRem(a^2*q^2,625)) and C1=abs(balRem(a*q,625)). The Turn21 cubic-plus-xminus1 state therefore has factor c=a^3*q^2 mod625 and envelope E4.

The retained x2 state has factor b=a^2*q mod625 and envelope E2. A fixed-target multiplication of these two states uses the same tensorProduct/reLinearize path as stock multiplication at modulus q. Its output factor is

d = c*b*q = a^5*q^4 mod625,

and a sufficient independent envelope is

E5(P) <= E4*E2 + K(P).

For a source-sized conservative scalar window use K(P)<=K_full=401679183790908.6 and H,C1<=312, with E0<=1.1433532886831608e35, R<=83891200000, Q0>=2^399.5. Solving E5(q)<0.48*q gives the sufficient continuous interval

182.49789601363528 < log2(q) < 353.5343333566185.

At the full chain q=Q0, log2(E5)<=582.3037728841089 while log2(0.48Q0)>=398.44110631094645. Thus the full chain fails this conservative outer-multiplication envelope by 183.86266657316247 bits. This is a proof-method obstruction, not a native correctness counterexample.

Whole-digit boundaries are not source-guaranteed to hit the safe interval because the exact Aung digit count/partition remains unknown.

However an ordinary ctxt-prime prefix is guaranteed to hit it. Pinned HElib CMake permits HELIB_SP_NBITS at most64, and Context::addCtxtPrimes generates ctxt primes with target bit size no larger than HELIB_SP_NBITS. Since Q0 has at least399.5 bits, let Pdagger be the first ordered ctxt-prime prefix with log2(product(Pdagger))>=183. Such a prefix exists. The previous prefix is below183 bits and one added ctxt prime contributes less than64 bits, hence

183 <= log2(qdagger) < 247.

This entire interval lies strictly inside the conservative safe window above. Therefore Pdagger is a source-guaranteed safe target for the outer multiplication under the current preflight bounds.

The exact implementation may instead enumerate all ordered ctxt-prime prefixes and choose the smallest one satisfying the exact E5(P)<0.48*q condition using exact K(P), H(P), and C1(P). The simple first-prefix-crossing-183 rule is a conservative source-level fallback.
