# BOOT B175 Representation-Mechanism Negative Screen

Date: 2026-10-29 (Asia/Hong_Kong)  
Session: Cryptography 10.0, Research Turn 11/25  
Track: BOOT  
Active subline: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Result

- STATUS: PASS_NEGATIVE_SCREEN / SURVIVORS_UNVALIDATED
- VALIDATED_REDESIGN_CANDIDATE: NONE
- NOVELTY: NOT_ESTABLISHED
- PUBLISHABLE_CONTRIBUTION: NONE
- PENDING_PI_DECISION: BOOT-DECISION-001
- B176: NOT_AUTHORIZED

No existing technique identified in this read-only screen simultaneously preserves fixed `Q`, stays within the current subline, has a sourced mechanism capable of recovering the conditional 16-required-bit deficit, and preserves the current multiplication/key/interface cost case. The result is a negative mechanism screen, not a redesign proposal.

## Fixed necessary-condition gate

For B175:

```text
r_LT8       = 577
r_GROUPED   = 633
delta_SI    = 664 - max(577,633) = 31
r_out       = 664
positive-budget ceiling = 648
required recovery = 16 bits
```

Any fixed-`Q` candidate must satisfy

```text
r_worse' + delta' <= 648.
```

It must therefore change at least one of:

- the coefficient-domain input/output reference geometry;
- ciphertext component centered lifts or `Q`-carry behavior;
- the ciphertext type or encrypted multiplication law;
- the ring, field, or encoding embedding;
- recombination order so that the low-headroom GROUPED ciphertext is not fully materialized before multiplication.

Reducing implementation constants, NTT count, decomposition cost, key-switch noise, or a few local noise bits cannot pass this gate.

## Eliminated as standalone repairs

The following do not independently change the aggregate tensor/reference geometry and are statically eliminated for the B175 correctness deficit:

- full-RNS scaling, CRT basis-extension, and quantization-rounding optimizations;
- key-switch/relinearization decomposition, gadget-base changes, hybrid key switching, and faster decomposition;
- hoisting, double hoisting, lazy or delayed relinearization, and degree-two temporary storage;
- diagonal, BSGS, or hoisted LT scheduling used only to produce the same LT8 ciphertext;
- simple slot permutation, Galois automorphism, bit reversal, Gray ordering, cyclic shift, or row swap;
- standard PS or digit regrouping that reconstructs the same low-headroom GROUPED ciphertext before pointwise multiplication;
- fixed-parameter violations such as increasing `Q`, changing `k0/H/s`, refresh, or another modulus chain.

Turn 10 already bounds quantization below `2^46` and conservative relinearization noise below `2^22`, whereas the measured coefficient residual has bit length 647. Eliminating either or both leaves the same 664-required-bit outcome. Pure LT improvement also cannot help because GROUPED, not LT8, is the worse input.

## Necessary-condition survivors only

Three mechanism families genuinely change geometry but remain unvalidated and cannot be selected without PI direction:

### Delayed recombination / distributed pointwise

Instead of materializing

```text
G = sum_i M_i * Y_i
```

and computing `L * G`, distribute multiplication before recombination:

```text
sum_i ((M_i * L) * Y_i).
```

This avoids materializing the low-headroom GROUPED operand before pointwise multiplication and therefore changes tensor/reference geometry. It survives the necessary-condition gate only. Missing powers, scale alignment, partial-product accumulation, and operation-count growth may erase any benefit. For eight partial products, the coarse sufficient accumulation screen is

```text
max_i(r_i) + ceil(log2(8)) <= 648,
```

or `max_i(r_i) <= 645`.

### External-product representation

GSW/RGSW/NTRU external product or CMux changes ciphertext type, multiplication law, decomposition position, noise expression, and key material. It passes the geometry gate, but direct CMux compilation has very high prior-art risk, high key/memory risk, no established 16-bit recovery, and previously failed novelty review for a direct selector compilation.

### Ring / field / embedding switching

Switching ring or cyclotomic field can change coefficient embedding, ring dimension, convolution factors, and carry behavior. It passes the geometry gate but requires cross-ring keys, packing/interface changes, and new security/noise/cost analysis. No evidence yet shows a 16-bit recovery under the fixed-`Q` target.

## Boundary

Equivalent plaintext semantics do not imply equivalent tensor/reference geometry: different circuits can produce different ciphertext components and `Q` carries. The precise gate is whether the mechanism changes the multiplication-time component geometry or avoids materializing the low-headroom GROUPED operand.

No survivor is a validated candidate, and none is promoted to a contribution or implementation plan.

## Next no-regret task

Build an optimistic static feasibility ceiling for eight-block delayed recombination:

1. write the exact public block-mask and `Y^i` dependency graph;
2. identify which powers are already present in B173/B174 state;
3. count the minimum missing ciphertext-ciphertext multiplications;
4. propagate scale metadata;
5. use existing required-bit traces to bound each partial pointwise optimistically;
6. apply the eight-term accumulation screen;
7. compare the resulting operation count with the current 26 ciphertext-ciphertext operations;
8. determine whether the construction is only known distributive/PS compilation.

This is a read-only feasibility test. It does not authorize Codex, native execution, B176, or a choice of redesign route.
