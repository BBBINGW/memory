# Turn 20 source audit

Pinned HElib source path for F4 with k=1 evaluates x^3-5x-1 as x*(x^2-6)+(x-1), then multiplies by x^2 and adds x^2+5x.

In the stock Paterson-Stockmeyer code, the temporary for coefficient -6 is created with the default full ctxtPrimes set, then x^2 is added. Pinned Ctxt::addCtxt matches prime sets by mod-UP and, for BGV, harmonizes unequal intFactors before addition. Thus the stock glue can erase the smaller fixed target chosen for x^2 and can add factor-rescaling not represented by the Turn19 first-square proof.

The factor-preserving rewrite z=x2; z.addConstant(-6) is plaintext-equivalent. Pinned addConstant scales the constant using the current intFactor and current modulus residue, without changing the prime set or intFactor. For the scalar -6 the added representative magnitude is at most 1872.

For the next real multiplication, stock multLowLvl would again choose a heuristic commonPrimeSet. A fixed-target multiplication sibling can instead bring both operands to a chosen complete-digit prefix, call the same tensorProduct routine, and then the ordinary reLinearize. Existing key-switch matrices suffice for complete leading digits.

This source audit supports the Turn20 one-step-lookahead selector and shows why the square-only Turn19 policy is not a complete F4 implementation policy.
