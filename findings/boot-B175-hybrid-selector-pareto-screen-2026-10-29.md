# BOOT B175 Hybrid-Selector Pareto Screen

Date: 2026-10-29 (Asia/Hong_Kong)  
Session: Cryptography 10.0, Research Turn 13/25  
Track: BOOT  
Active subline: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Result

- PRIMARY_HYPOTHESIS: PASS_ALGEBRAIC_EXISTENCE / UNCLEAR_CRYPTOGRAPHIC_FEASIBILITY
- STATIC_STATUS: SURVIVORS_UNCLEAR
- ENUMERATED_WEIGHTED_NONISOMORPHIC_CIRCUITS: 43
- OPTIMISTIC_SURVIVORS_BEFORE_DOMINANCE: 20
- MINIMAL_PARETO_FRONTIER: 2 mechanism classes
- VALIDATED_REDESIGN_CANDIDATE: NONE
- NOVELTY: NOT_ESTABLISHED
- PENDING_PI_DECISION: BOOT-DECISION-001
- B176: NOT_AUTHORIZED

Within the audited selector-subcube grammar, two hybrid mechanism classes satisfy the structural conditions `count < 34`, selector-endpoint serial SI depth below three, and no complete GROUPED materialization before pointwise multiplication. Both retain 26 ciphertext-ciphertext operations and selector-endpoint depth two.

They survive only an extreme optimistic model: every unmeasured SI multiplication adds 29 required bits, public masks add zero bits, component-lift/carry adds nothing, and only exact public scale alignment plus addition fan-in are charged. Their remaining slack is only three to four required-bit units. They are not validated candidates.

## Enumeration boundary

The grammar uses the existing selector factors

```text
F0 = d0 + c0*Y
F1 = d1 + c1*Y^2
F2 = d2 + c2*Y^4,
```

public subcube expansions over selector-bit subsets, SI multiplication only across disjoint selector-bit sets, and selector-endpoint depth at most two. Each selector bit is used exactly once, and circuits that first materialize the full three-bit GROUPED selector and then multiply by LT8 are forbidden.

Enumeration removes operand swaps and public-addition reorderings but retains selector-bit labels because `Y`, `Y^2`, and `Y^4` have different measured scales and residuals. The 43 circuits are complete only for this weighted selector-subcube grammar, not for arbitrary FHE arithmetic circuits.

The common prefix already costs 23 ciphertext-ciphertext operations: 21 checkpoint/basis operations plus existing `Y^2` and `Y^4`. The grammar-level count-depth frontier is

```text
(26 ct-ct, selector endpoint depth 2)
(34 ct-ct, selector endpoint depth 1).
```

Both count-26 survivors retain full SI dependency depth four, equal to the current path. They reduce only selector-endpoint depth.

## Frontier A: explicit lower-two-bit selector

```text
Y^3   = SI(Y,Y^2)
G01^E = M0 + M1*Y + M2*Y^2 + M3*Y^3
H     = SI(L,G01^E)
OUT   = SI(H,F2).
```

Aligning the nonconstant terms to target scale 22359 uses centered multipliers

```text
Y: 256
Y^2: -16
Y^3: 1.
```

The modeled selector scale becomes 22359, `H` scale 35478, and final scale 30059, matching the B175 pointwise target.

Under the optimistic 29-bit recurrence:

```text
r(Y^3)  = 584
r(G01^E)= 586
r(H)    = 615
r(OUT)  = 644.
```

The total remains 26 ciphertext-ciphertext operations; selector-endpoint depth is two and full depth is four. The sufficient fragility condition is

```text
557 + delta_3 + delta_H + delta_OUT + mu <= 648,
```

where `mu` aggregates all omitted mask, public-combination, component-lift, and carry costs. At `(29,29,29)`, only `mu <= 4` is allowed. Three 31-bit increments fail even with `mu=0`.

## Frontier B: high-bit distributed balanced split

A representative is

```text
ACC1  = SI(F0,F1)
A2(L) = d2*L + c2*SI(L,Y^4)
OUT   = SI(ACC1,A2(L)).
```

The two branches of `A2(L)` have scales 43352 and 22185. Target scale 22185 aligns them with multipliers `-1` and `1`, avoiding a large public multiplier. The final scale again becomes 30059.

Under the optimistic recurrence:

```text
r(ACC1) = 602      measured input trace
r(L*Y^4)= 615      optimistic model
r(A2(L))= 616
r(OUT)  = 645.
```

The total is 26 ciphertext-ciphertext operations; selector-endpoint depth is two and full depth four. Only three required-bit units remain for all omitted increment and mask/carry costs. Two 31-bit increments fail even when public-mask cost is assumed zero.

## Dominance and boundaries

Frontier A has one modeled bit less output noise. Frontier B needs no new power, has lighter scale alignment, and has fewer unmeasured masked terms. Neither fully dominates the other.

Other families are dominated:

- direct balanced reassociation reaches an optimistic 661 required bits;
- expanded two-bit operators use at least 28 operations with no better score;
- other explicit two-bit subsets require deeper/noisier powers and score at least 646;
- the improved full eight-branch endpoint still costs 34 and scores 653.

The two frontier circuits are distributive/binary-selector/PS scheduling variants. Their plaintext functions are not new; any possible distinction lies only in ciphertext component-lift and `Q`-carry geometry. No novelty or correctness claim is established.

Historical B174 mask multiplication adds about 16--17 required bits, far above the current three-to-four-bit slack. This is not a formal lower bound for the new operands, but it makes both survivors too fragile to promote without stronger static evidence.

## Next no-regret task

Use the saved B175 coefficient-residual arrays and exact Lattigo public-mask encoding to screen both frontiers:

1. reconstruct coefficient polynomials for `c2,d2` and `M0..M3`;
2. compute exact `l1`/`l_infinity` norms and scale multipliers;
3. where existing residual arrays suffice, compute the actual negacyclic convolution of each public mask with the saved residual;
4. compare the resulting deterministic mask contribution with Frontier A's four-bit and Frontier B's three-bit slack;
5. retain `UNCLEAR` for every term requiring missing component-lift data.

This remains read-only and does not authorize native execution, Codex, B176, or route selection.
