# Turn 21 source audit

Pinned HElib addCtxt first mod-ups mismatched prime sets and then, for BGV, runs an extended-Euclidean search when intFactors differ. That stock path is correct operationally but its chosen scaling coefficients depend on the library noise estimates and are not part of the independent envelope proof.

Pinned mulIntFactor(e) multiplies intFactor by e modulo ptxtSpace, multiplies every ciphertext part by the balanced representative of e, and scales noiseBound by its absolute value. This is exactly the internal operation needed to align two BGV ciphertext factors without changing their plaintext values.

Pinned addConstant on BGV computes the constant injection scale from intFactor and the current prime-set modulus. Thus w=x; w.addConstant(-1) on the already-fixed target keeps primeSet and intFactor unchanged and has an independently bounded representative contribution C1_t<=312.

For the cubic branch the intFactor after x2 and then x*(x2-6) is c_t=a^3*q_t^2 mod625, with a=67. The x-minus-1 branch factor is a. The public alignment multiplier h_t=c_t*a^{-1}=a^2*q_t^2 mod625 is a unit because every ctxt prime is distinct from5. After applying this multiplier to the x-minus-1 branch, both branches have identical primeSet, ptxtSpace and intFactor, so addCtxt performs neither mod-up nor factor harmonization.

This removes the x-minus-1 addition dependency on stock noise-estimate-driven factor harmonization.
