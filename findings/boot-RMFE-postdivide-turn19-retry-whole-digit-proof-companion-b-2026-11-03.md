# Turn19 retry companion B

Source audit for pinned HElib acdb264e1a991eaee35fd8b3c31bebe9528c49a1:

1. Context::addSpecialPrimes builds ordered disjoint digit blocks by taking leading primes from the remaining ctxtPrimes; the last block receives the remainder. Therefore a union of the first t blocks is an ordinary ctxt-prime prefix.

2. Stock square performs adaptive set selection before tensorProduct. A fixed-target sibling can instead reduce to a chosen prefix, invoke the same private tensorProduct routine, then invoke the ordinary reLinearize routine.

3. Real BGV modDownToSet scales to the chosen target and leaves intFactor unchanged; tensorProduct then applies the same q-mod-ptxtSpace factor rule used by stock multiplication.

4. If the target contains only ctxtPrimes, the initial dropSmallAndSpecialPrimes inside reLinearize reduces to modDownToSet(ctxtPrimes), which is a no-op for that target. Therefore no second adaptive set choice occurs before switching.

5. A target formed from complete leading Context digit blocks makes breakIntoDigits return only complete blocks; the ordinary existing matrix rows suffice and no partial-block argument is needed.

Conclusion: the first F4 square can use a proof-driven complete-digit prefix without changing its plaintext arithmetic semantics.
