# PURE-FHE P0-PRESCOUT-65 — Sparse-Defect A2D Whole-System Value Gate

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
ITERATION: P0-PRESCOUT-65
LATEST_COMPLETED: P0-PRESCOUT-65
NEXT_ITERATION: NOT_STARTED / HUMAN_REVIEW
STATUS: PASS_ALGORITHMIC_FACTORIZATION / FAIL_CURRENT_P384_WHOLE_SYSTEM_PRIORITY / PRESERVE_FACTORIZATION_LEMMA / PARK_H64_IMPLEMENTATION
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO
STATE_UPDATE: YES — isolated PURE-FHE finding only.

## 1. Input from P0-64

P0-64 found a source-specific exact factorization for the general arithmetic-to-digit conversion in supplied ePrint 2026/1869.

For the source P-384 polynomial at b=2 and B=32:
- ell=77 radix blocks;
- only four alpha_j are nonzero: j={0,6,19,25};
- |Lambda|=35;
- source global carry state size |C|=11;
- ordinary alpha=0 blocks need only a 3-state outgoing carry set.

The factorized segmented schedule conservatively reduced carry-relation CMult from

  326095

to about

  18546,

roughly 17.6x, with carry depth reduced from 7 to about 6.

Second-FBS transition/check output count fell from 4620 to about 1378.

P0-65 asks whether this is enough to justify implementation.

## 2. Post-FBS depth / modulus

Source Appendix C.2 gives general A2D post-second-FBS multiplicative depth

  ceil(log2 ell)+ceil(log2 |Lambda|)+3.

For P-384:

  7+6+3=16.

The factorized carry schedule reduces the carry component by one level, so the matched post-FBS bound becomes approximately

  15 levels.

The source B=32 A2B implementation uses:
- 43-bit scale primes;
- ~44-bit bottom modulus;
- a second functional-bootstrap path with about 19 levels before the post-FBS carry stage.

Using this source-shaped level accounting, a P-384 general A2D top context would still be on the order of

  19+15=34 scale levels

after the relevant modulus raise.

A rough Q-only bit budget is therefore

  44 + 43*34
    ~=1506 bits,

before the auxiliary key-switch modulus P.

The source conversion parameters use roughly 400 bits of auxiliary modulus in its implemented setting, giving a source-shaped QP budget around

  1900 bits.

This is not a formal secure parameter instantiation for P-384; it is a level-budget warning.

It is materially above the approximately 1740-bit QP values used by neighboring N=2^16 prime/ALU implementations targeting 128-bit security.

Therefore a concrete P-384 general A2D instantiation may need a larger ring dimension or materially different decomposition parameters.

## 3. Output-memory gate

At 15 retained post-FBS levels, a rough ciphertext modulus is

  44+43*15
    =689 bits.

For N=2^16 and two RLWE components, the coefficient payload of one ciphertext is approximately

  2*N*689/8
    ~=11.3 MB

before implementation/RNS metadata.

Materializing all 1378 proposed second-FBS outputs at once would therefore require roughly

  15--16 GiB

of ciphertext payload alone.

The source baseline 4620 outputs would be over 50 GiB.

### Streaming observation

This is NOT a decisive memory killer.

The source multi-value FBS explicitly shares:
- StC / ModRaise / CtS;
- common Fourier terms;

and combines per-function interpolation coefficients only afterward.

Therefore the lambda-specific defect/check outputs can in principle be generated and consumed in batches while retaining the shared Fourier basis.

A streaming implementation could avoid holding all 1378 outputs simultaneously.

Thus:

  MEMORY_PEAK: PLAUSIBLY MANAGEABLE WITH STREAMING.

But streaming does not remove the total arithmetic work.

## 4. Remaining CMult work is still very large

Even after the 17.6x P0-64 reduction, the conservative carry-stage count is

  ~18546 CMult.

These are full CKKS ciphertext-ciphertext multiplications at N=2^16, across a large modulus chain.

This is not comparable to a small constant-number circuit.

### Neighboring measured proxy: ePrint 2026/1840

Supplied 2026/1840 uses the same N=2^16 scale.

For its 256-bit, base-32 A2B setting:
- carry recovery: 3.63 s;
- its parallel carry algorithm uses about 6 doubling iterations, each with one CMult plus one rotation;
- bit correction: 3.14 s;
- its formula contains 15 CMult for w=5, plus linear work.

These numbers are on a different CPU and a different exact circuit, so they are NOT a direct benchmark.

But they establish the right order of magnitude:
a handful to tens of N=2^16 CMult already costs seconds in a comparable OpenFHE-style CKKS workload.

Even an optimistic extrapolation from the CMult-heavy bit-correction stage makes ~18k CMult a many-minute to hour-scale single-thread workload, not a tens-of-seconds conversion.

This is only a latency proxy, but the gap is too large to justify native work at the current stage.

## 5. Stronger matched alternative: supplied 2026/1836

The prime-modulus ALU paper in supplied 2026/1836 takes a different approach:
- supporting polynomial for an odd prime;
- canonicalization / A2BCLA;
- carry-lookahead and overflow wrapping.

It states existence of a supporting polynomial for arbitrary odd primes and directly targets prime-modulus A2B.

Measured at N=2^16:
- 256-bit prime-modulus A2B: about 72 s single-thread CPU;
- about 0.49 s GPU;
- packing 256 values for the tested 256-bit primes.

P-384 is wider and would not have exactly these timings, so no direct 384-bit runtime is claimed.

However, this is a much stronger baseline than the source 1869 general A2D for a prime modulus:
it is a purpose-built prime conversion whose cost is a small constant number of bootstraps plus O(log n) carry logic, rather than thousands of candidate/state CMult.

Hence the P-384 H64 route is not currently the best target workload.

## 6. Why state/candidate SIMD packing does not rescue the amortized story for free

One could pack:
- carry-state matrix entries;
- lambda candidates;

into additional CKKS slots to reduce the number of ciphertext objects / CMult calls.

But P-384 source packing already uses

  floor(N/384)=170

messages per N=2^16 ciphertext.

Using a large state/candidate axis consumes the same SIMD capacity that currently amortizes work over independent messages.

This can improve single-message latency but does not automatically improve total slot-operation work or amortized throughput.

Therefore this is a systems tradeoff, not a free asymptotic rescue.

## 7. What remains technically valuable

P0-64's algebra should be preserved.

### Sparse-defect factorization lemma

If the general A2D carry maps have the form

  f_{j,lambda}

and a set D of radix positions is the only set on which the maps depend on lambda, then:
- all maximal lambda-independent segment prefix automata can be computed once;
- every candidate lambda only needs to cross the defect automata and apply the shared prefix maps;
- every intermediate carry can still be reconstructed exactly.

This changes candidate-dependent work from "pay lambda at every global scan level" toward work proportional to the number of defects.

The mechanism may matter when:
- |D| is very small;
- the alternative modulus/conversion method is unavailable;
- a composite modulus prevents use of prime-specialized A2B;
- state dimensions are smaller than in P-384;
- an implementation can stream multi-value outputs efficiently.

## 8. Current decision

For P-384 specifically:

  FAIL_CURRENT_P384_WHOLE_SYSTEM_PRIORITY.

Reason:
- ~18.5k CMult remains extremely large;
- output count is still >1000;
- the level/modulus budget is high;
- a stronger prime-specialized neighboring construction already exists.

This is a VALUE kill, not a correctness kill.

Do NOT:
- request Codex implementation;
- run native OpenFHE experiments;
- build a P-384 parameter set;
- optimize GPU kernels for H64.

## End of Iteration

TRACK_ID: PURE-FHE
ITERATION: P0-PRESCOUT-65

STATUS:
PASS_ALGORITHMIC_FACTORIZATION /
FAIL_CURRENT_P384_WHOLE_SYSTEM_PRIORITY /
PRESERVE_FACTORIZATION_LEMMA /
PARK_H64_IMPLEMENTATION /
HUMAN_REVIEW.

RESULT:
- Memory is not the decisive killer because lambda outputs can plausibly be streamed from shared multi-value-FBS Fourier terms.
- The residual ~18.5k CMult work is the decisive practical concern.
- Source-shaped depth still implies a very large modulus budget.
- A prime-specialized A2B route in 2026/1836 is a much stronger baseline for P-384.
- H64 should be archived as a reusable sparse-defect automaton lemma, not implemented for P-384.

NOVELTY:
NOT_ESTABLISHED.

CODEX_REQUIRED:
NO.

NEXT:
Return to PURE-FHE problem-level reselection.
Only reopen H64 if a workload appears with:
- no strong prime-specialized alternative,
- very sparse alpha_j defects,
- materially smaller state/candidate dimensions,
or a new packed/streamed construction that reduces total slot-operation work rather than only ciphertext count.

STATE_UPDATE:
YES — this finding only.
