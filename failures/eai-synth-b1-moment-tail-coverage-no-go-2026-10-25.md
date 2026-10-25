# EAI Synthetic B1 — first two moments cannot identify a 1% rare mode (2026-10-25)

**Only tested claim:** Is `T(P)=(sum P, E[X], E[X²])` sufficient to certify whether `P[X=3]>0` for unknown `P` on `{0,1,2,3}` when a verifier receives no further distribution-dependent data? `FAIL`. This is a single easy algebra falsifier, not a synthetic LLM training experiment, not a new mathematical discovery or an attack on existing OT methods.

## Exact toy with fractions (no statistical or floating error)

On `x=0,1,2,3`, choose:

| x | P_A(x) | P_B(x) |
|---|---:|---:|
| 0 | 70/100 | 71/100 |
| 1 | 20/100 | 17/100 |
| 2 | 9/100 | 12/100 |
| 3 | 1/100 | 0 |

In both worlds:
- `sum_i p_i=1`
- `E_A[X]=E_B[X]=41/100`
- `E_A[X²]=E_B[X²]=65/100=13/20`
- `Var_A(X)=Var_B(X)=65/100-(41/100)^2=4819/10000`.

Yet **`P_A[X=3]=0.01`** whereas **`P_B[X=3]=0`**; these require opposite decisions for the binary true-distribution-tail-exists predicate. The candidate synthetic pool and verifier's public inputs are fixed identically across worlds, and each private silo is restricted to the same exact moment summary; the transcript is identical.

**Nullspace derivation:** `P_B=P_A+(1/100)(1,-3,3,-1)`; `sum_{i=0}^{3}i^k (1,-3,3,-1)_i=0` for `k=0,1,2`, by the third finite difference. Consequently T maps both worlds to same result. Any deterministic decision makes an error in one world; for randomized decision with probability p of 'tail exists' on the common transcript, the A-error is 1-p, B-error p, so maximum >=1/2. This does not rely on DP randomness or a privacy lower bound: the exact noiseless summary already loses the signal.

**Reproducer (standalone Python, exact rational):**
```python
from fractions import Fraction as F
a = [F(70,100), F(20,100), F(9,100), F(1,100)]
b = [F(71,100), F(17,100), F(12,100), F(0)]
for k in (0,1,2):
    assert sum((i**k)*a[i] for i in range(4)) == sum((i**k)*b[i] for i in range(4))
assert sum(a)==sum(b)==1
assert a[3]==F(1,100) and b[3]==0
```
Executed in this assistant's Python scratch session with exact rational arithmetic; sums and moments matched. No model/GPU runs.

## Scope and prior art limitation

- This only invalidates an **unconditional moment-only certificate**. It does **NOT** refute a verifier that receives `P[X=3]` via a tail-mass query, DP histogram, secure-aggregate indicator count, higher moments, or an OT proxy that distinguishes the worlds. In particular **`W_1(P_A,P_B)>0`**; `W_1=|-.01|+|.02|+|-.01|=0.04` for the unit-spaced four-point 1D support. Qiao ICML2026 [full original](https://arxiv.org/html/2606.13732) §§4.3–4.4 shares Wasserstein interpolations/barycenters, and appendix §C.6 analyzes DP OT, not just (mean,var) aggregates.
- The nullspace example is a classic **truncated moment nonidentifiability** toy, **`NOVELTY_FAIL`** for a paper contribution.
- Even though P_A has 1% mass, the toy is population-level; at finite sample size, seeing at least one tail record in P_A is stochastic. This test says nothing about actual sample draws, downstream task quality, or recursive model collapse guarantees.
- A privacy-preserving multilateral protocol may still distinguish the two worlds by adding an **appropriate statistic**; its privacy, cost and utility must be separately evaluated.

## End of iteration

**STATUS:** `FAIL_B1_MOMENT_ONLY_TAIL_IDENTIFIABILITY / PASS_EXACT_4_POINT_TWO_WORLD_PROOF`.
**RESULT:** `T=(n,mean,second_moment)` identical; rare mode probability 1% vs 0. No universally correct tail-presence rule under only these public statistics.
**NEXT_TEST:** `B2_SOURCE_FIRST_ADAPTIVE_PRIVATE_TAIL_QUERY_IDENTIFIABILITY_AND_COST` only upon PI continuation: check existing DP histograms/tail counts/secure aggregation and Qiao §C.6 before new protocol ideas, then one minimal test of a more specific gap. Do not assume there is one.
**STATE_UPDATE:** `YES` only after GitHub commit/readback.
