# Turn 22 source audit

Pinned HElib source facts supporting the prime-prefix rescue:

1. Context::addCtxtPrimes constructs the ciphertext-prime chain by repeatedly adding primes generated at a target bit size not exceeding HELIB_SP_NBITS.

2. Pinned CMake limits a user override HELIB_SP_NBITS to at most64. The default is NTL_SP_NBITS or49 under Intel HEXL. Thus every individual ctxt prime contributes strictly less than64 bits to log2 of a prefix product.

3. Pinned DoubleCRT::breakIntoDigits starts from the current ciphertext prime set. For each context digit it intersects that digit with the remaining current primes before forming the corresponding decomposition component. Therefore an ordered prime prefix ending inside a context digit produces a legitimate partial final digit.

4. keySwitchDigits iterates only over the decomposition components actually returned and indexes the existing switching-matrix rows W.b[i]. The full matrix is generated for the complete Context digit count, so a partial final digit in the final used row does not require a new key family.

5. For the outer multiplication both operands are already reduced to the same chosen prefix P. A fixed-target multiplication sibling therefore needs no adaptive commonPrimeSet selection: it can use stock tensorProduct followed by stock reLinearize. The BGV product intFactor is d=a^5*q^4 mod625.

Conclusion: partial-final-digit prime prefixes are a pinned-source-supported mechanism and are required to obtain a source-guaranteed safe modulus for the outer first-F4 multiplication independently of the unknown Aung digit partition.
