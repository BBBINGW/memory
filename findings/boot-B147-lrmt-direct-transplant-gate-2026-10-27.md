# BOOT-B147 — Full-source LRMT audit for B145: direct transplant fails the one-FBS objective

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Parent: B145/B146
- Source: supplied ePrint 2026/1264
- Status: FAIL_DIRECT_LRMT_TRANSPLANT / KEEP_AS_STRUCTURAL_HINT
- CODEX_REQUIRED: NO

## Question

Can ePrint 2026/1264 LRMT-FBT be used directly as the LUT backend of B145, so that the exact rank-1 structure of the fourteen 4096-point window functions makes the one-FBS arithmetic A2B concretely cheap?

## Full-source findings

### 1. Rank-1 structure is genuinely supported

1264 proves that if an alpha x beta LUT matrix factors as

    M[i,j] = g(i) h(j),

then its rank is at most one and LRMT evaluation is exact.

For a rank-r LUT, Algorithm 2 uses:
- r(alpha+beta) scalar multiplications,
- r ciphertext multiplications,
- two multiplicative levels.

For balanced P=4096 with alpha=beta=64 and r=1, one LUT-evaluation stage is therefore:
- 128 scalar multiplications,
- 1 ciphertext multiplication,
- 2 levels.

The B145 functions are exactly rank-1 under w=64b+c:
- G(b,c)=H(b);
- S(b,c)=L(c)(P(b)-T(b));
- F_k(b,c)=bit_k(b);
- D_k(b,c)=L(c)(bit_k(b-1)-bit_k(b)).

For K=14 rank-1 outputs on the same selectors, Section 4.3 of 1264 shares the selectors across outputs. The LRMTEval stage alone would therefore use:
- sum ranks = 14;
- 14*(64+64)=1792 scalar multiplications;
- 14 ciphertext multiplications;
- depth still two for the LRMTEval stage.

So the low-rank observation is fully source-backed, not merely an analogy.

### 2. But the full LRMT-FBT front-end is incompatible with B145's main objective

The full LRMT-FBT does not start from one 4096-th root and directly evaluate the low-rank factors.

Instead it retains CMT-FBT's functional digit decomposition (FDD):
- choose a low digit base p;
- let t=ceil(log_p P);
- sequentially extract the radix-p digits;
- each digit extraction invokes SlotsMVB, i.e. a low-precision functional bootstrap;
- after each nonfinal digit, return mod-p to coefficient encoding, subtract it, divide by p, then process the next digit.

For P=2^12=4096, Table 4 chooses p=2^3=8, hence

    t = log_8(4096) = 4.

Therefore a direct LRMT-FBT replacement would use four sequential low-precision MVB/FBS invocations before the low-rank matrix evaluation.

This destroys the central B145 objective of replacing 1869's two sequential FBS calls by one root/FBS stage.

### 3. Source-level parameter evidence

At P=2^12 the 1264 LRMT parameter set is:
- log2 P = 12;
- log2 p = 3;
- matrix 64 x 64;
- N=2^16;
- L=23;
- log2 Delta=48;
- log2 Q_L P =1452 bits;
- 128-bit security, sparse secret h=192.

For ReLU (rank 2) at P=2^12, its measured full LRMT-FBT single-thread latency is 119.91 s; the LUT-evaluation stage itself is only 2.12 s. The dominant cost is the FDD front-end (~107.48 s).

This confirms the structural diagnosis: at 12-bit precision, low-rank LUT evaluation is already cheap; repeated digit-decomposition bootstrapping dominates.

Cross-paper absolute latency must not be compared directly to 2368 because hardware/library differ, but the stage breakdown is decisive for identifying the bottleneck inside LRMT itself.

### 4. Multi-value sharing does not fix the front-end problem

1264 Section 4.3 confirms that K LUTs on the same input share:
- the FDD stage;
- both KProduct calls;
- row/column selectors.

Only the low-rank evaluations branch per output, with total cost proportional to the sum of ranks.

This is excellent for B145's fourteen outputs once row/column selectors already exist, but obtaining those selectors still requires the sequential FDD front-end. Multi-value sharing therefore does not restore the one-root property.

## Decision

Direct use of the complete 1264 LRMT-FBT as B145's backend: FAIL.

Reason: it replaces one 4096-domain LUT problem by four sequential low-precision MVB/FBS digit extractions at P=4096. That is incompatible with B145's core goal and, in the source's own P=2^12 breakdown, FDD dominates total time.

What survives:
- the exact-rank-1 characterization is useful and now fully certified;
- the low-rank decomposition suggests searching for a way to expose the 64x64 row/column factors from the single Root_{4096} output without FDD;
- the multi-value sharing formula gives the correct cost once such factors are available.

## New follow-up hypothesis

Given R = zeta_{B^2}^w with w=Bb+c, one can obtain

    R_c = R^B = zeta_B^c.

A B-point LUT on R_c can evaluate both L(c) and

    q(c) = zeta_{B^2}^{-c}.

Then

    R_b := R * q(c) = zeta_B^b.

Thus a single Root_{B^2} may be sufficient to derive separate B-th roots for c and b without a second root production or FDD. All B145 rank-1 factors then become B-point LUTs on R_b and R_c.

This exact phase-quotient identity is the next cheapest algebraic/performance test. It is not yet a claimed improvement because its depth/noise may exceed the direct B^2 lookup.

NEXT: B148 phase-quotient root splitting gate.
