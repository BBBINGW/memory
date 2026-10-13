# Iteration 169 — Public two-basis synthesis of GHS-type LCR+AKS keys is algebraically feasible, with additive rounding and increased key noise

**Date:** 2026-10-13. Human PI approved with “好的，请继续” after I168. ONE primary falsifiable claim and ONE source-faithful key-equation minimal test. Do not infer an actual dynamic-transform acceleration from ordinary RLWE linearity; distinguish exact key-object equality from valid approximate encrypted message, security/precision and performance.

## Read-before-write / source

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` I168 blob `d014d9e10f56136cfceb1e430fa73e4dba4c03c7`, and `findings/ckks-lcr-aks-plaintext-bound-rotation-key-reuse-iteration168.md`. Full source paper: Yan, Zeng, Cao, Song, Wang, *Faster Bootstrapping for CKKS with Less Modulus Consumption*, PKC 2026, ePrint **2025/1403**; Research MCP full **51 physical pages** GitHub mirror SHA256 `784db16f5a3f7c79c68c52f0a99e03c8ca7ce3e4c06824736f5fd4dfff1f5c29`, official latest version still **VERSION_UNVERIFIED**. Relevant original §4.2 physical pp19–22 (aggregated key switching, generic hybrid construction), §5.1 physical p23 (special level-conserving GHS key Eq.(5)), Appendix B.2 pp38–39 (key precomputation, rescaling-like and ModUp). Original paper's practical *fixed* bootstrapping DFT matrix is static. Web PDF fetch was also attempted on official ePrint PDF and raw public GitHub mirror PDF for formula screenshot/visual validation, but both failed (UnexpectedStatusCode / cache miss); therefore rely on legible Research MCP extract plus **pinned actual keygen code**, and keep original complex glyph parity warning.

Public author code `Fainabi/Lattigo-LCR-AKS`, pinned commit `3fbe5c8eeeea9ee127d074915d909a18c2a0f9d4`, branch `lcr`; `circuits/ckks/bootstrapping/keys.go` blob `51e432b47c2c6ce8c398b3d81527113f9572aebb` lines176–306; `core/rlwe/keygenerator.go` blob `3b1ffc4553e1ad142cd3fd9833d9d34f43a3` lines~375–500, specifically `GenAggregatedLevelConservedKeyNew`. The latter computes `(skIn*matrix)` in the Q ring, centers coefficient representatives, multiplies by `P`, rounds divided by `q_L` (nearest centered residual), maps the coefficient message to RNS QP, generates an **RLWE EncryptZero under skOut** with fresh randomness, and adds the message into its first ciphertext component. The second AKS key constructor `GenAggregatedGaloisKeysNew` uses its own `genAggregatedEvaluationKey` construction with similar P*m*sk/q, **but this iteration's exact centered coefficient rounding test is anchored to the former first-layer GHS-type key**. Do not infer identical detailed rounding from the two constructors without independent verification.

## ONE hypothesis / falsifier

**[HYPOTHESIS]** Given **two independently randomized, source-congruent AKS evaluation keys** for public encoded plaintext diagonals `m0,m1` under the SAME fixed source/target secrets, same rotation, same ciphertext level and modulus `QP`, their public componentwise sum is **exactly equivalent to a fresh source-generated AKS key** for `m0+m1` in both embedded message and fresh-key noise budget. Thus a dynamic matrix update is free of any extra approximation/noise cost.

**[MINIMAL TEST]** Derive the decryption relation of componentwise sum; compare its key-message against source's rounded target, including one explicit coefficient example where nearest-integer roundoff is not additive. Count random error variance for two independent input evaluation-key zero encryptions. Source key-gen's exact noise and rounding should separately appear. Failure of exact equality or same-noise-budget kills strong hypothesis; success as approximate key alone is weaker.

## Algebra / exact findings

Suppress automorphism, gadget and RNS limbs **only for one common key context**, not for a cryptographically complete algorithm. For source's level-conserving GHS precomputed `m` (already an encoded ring polynomial), let for one centered integer coefficient in a **no-wrap** representation:
```
 t_i = P * (m_i*sIn)_coeff / q_L
 μ(m_i) = Round(t_i)
 K_i = (b_i,a_i),  b_i + a_i*sOut = μ(m_i) + e_i   (mod PQ).
```
The key is a public RLWE encryption of the fixed key-message `μ(m_i)`, with a uniform `a_i` and fresh RLWE noise `e_i`. Add the FULL two ciphertext components in R_QP, not just b:
```
 K_syn := (b0+b1, a0+a1);
 b_syn+a_syn*sOut
    = μ(m0)+μ(m1)+e0+e1
    = μ(m0+m1)+δ+(e0+e1)   mod PQ,
 δ:=Round(t0)+Round(t1)−Round(t0+t1).
```
For independent real/integer `t0,t1` with same deterministic nearest rounding convention, `δ∈{−1,0,1}` per coefficient; absolute residual vs the **exact unrounded target** `|Round(t0)+Round(t1)−(t0+t1)|≤1`. Fresh `K_{m0+m1}` has residual ≤0.5 from the exact target per coefficient. Thus synthesized key is **a valid approximate encryption if the downstream algorithm tolerates the extra error** but is **NOT generally equal** to a source-generated exact rounded-message key or equally distributed fresh evaluation key.

If `e_i` are independent conditional on same fixed secret, centered with coefficientwise variance `σ²`, then `E[e_syn]=0, Var[e_syn]=2σ²`; combining one directly generated key would have fresh variance `σ²` under same simplistic noise model. At the *key-message level*, new deterministic `δ` plus `e0+e1` yields mean `δ` and variance `2σ²`; **not** a claim that the *CKKS output* variance doubles, because key-switching multiplies errors by input decomposition digits, automorphisms, ModDown, and rounding/correlation may alter it. `a0+a1` is uniformly distributed mod QP if `a0,a1` are sampled independent uniform and QP shape matches, so the sum remains structurally an RLWE ciphertext, but its noise distribution is convolved (not the keygen's original χ_err). Formal adaptive correlated-key security is NOT established by this observation.

**Exact scalar no-wrap test (one deliberately chosen coefficient):**
```
 P=101, q_L=7, sIn=1, m0=1, m1=3;
 t0=101/7=14.428571...,   μ0=14;
 t1=303/7=43.285714...,  μ1=43;
 target t=404/7=57.714285..., μ_target=58;
 μ_syn=57; δ=−1;
 |μ_syn − t|≈0.7142857 while fresh |μ_target−t|≈0.2857143.
```
For independent Rademacher errors e0,e1∈{−1,+1} (illustrative sanity check only), exhaustive four combinations yield e_syn∈{−2,0,0,+2}, mean0, variance2 versus independent fresh ±1 variance1. The composed key encrypts the target rounded key-message shifted by `−1` plus summed error. A **single combined test** verified math exactly in `functions.exec`, and also checked max absolute nearest-rounding mismatch ≤1 for 3969 integer pairs x,y∈[−31,31] /q7. Toy P101/q7 is insecure and not source Table3 RNS parameters, but proof of nonadditivity of scalar `Round` is exact independently of that toy.

**Critical condition on coefficient lifting:** The author's code computes `skIn*matrix` **mod Q** then centers the coefficients; it rounds `P*(centered residue)/q_L`. The simple `μ(m0+m1)` linear addition identity for **unwrapped integer values** assumes `centered(sk*(m0+m1)) = centered(sk*m0)+centered(sk*m1)`, which can fail due to Q-representative wrap. In full RNS, `δ` can include modulus-wrap terms not bounded by a constant unless source's small-coefficient/no-wrap assumption is maintained **for each basis AND their sum**. This is not a flaw in source's fixed first-DTF use, but a necessary restriction on arbitrary public linear key synthesis. For a large integer combination `∑ α_i m_i`, the worst local roundoff scales as O(∑|α_i|), random key noise variance as `σ²∑α_i²` only under conditional independent centered key errors, and coefficient wrap/overflow may invalidate the approximation entirely. No full number-theoretic convolution bound or CKKS precision proof attempted.

## Value-of-contribution / applicability

**[PASS limited feasibility]** Public componentwise addition of two same-context RLWE evaluation keys produces a valid encryption of sum of their embedded messages; for **small**, **no-wrap** public coefficient combinations, this is approximately the evaluation key for the sum matrix within a *larger* error budget. This is plain RLWE additivity, not a novel AKS primitive.

**[FAIL strong hypothesis]** Exact source-defined rounded message and fresh-key error budget are **not preserved**: δ can equal ±1 per coefficient, variance doubles for two independent basis keys, nontrivial weight coefficients further amplify errors. Some derived keys may remain usable if `P` and source parameters provide sufficient noise slack, but **actual I168 author proof's parameter margin has not been applied**; cannot claim a valid full CKKS new evaluation key or measured output accuracy.

**[No free performance result]** Supporting a basis of b public diagonals for each needed rotation/level requires ~b times the corresponding evaluation-key material versus one fixed-transform key, plus at least O(b S) online public ring work to produce a full-size combined key of size S; a static matrix needs no recomputation. For general independent model weights/diagonals, a two-dimensional span is very restrictive; using an arbitrary-basis description generally scales b with plaintext dimension, so storage can become prohibitive. Conventional ordinary rotation key is already m-independent and supports online plaintext multiplication at a known extra cost. Without a quantified workload with low-dimensional structured update family, adaptation frequency and repeated ciphertext evaluations, a gain is **not established**, and a key synthesis itself is just a public linear combination of ciphertexts. Security under multiple derived related keys, format correctness of the concrete Lattigo API, full RNS ModDown/noise and level/precision remain OPEN.

## End of Iteration 169

**STATUS:** **FAIL** exact source-key equivalence / same fresh-noise-budget hypothesis; **PASS** bounded algebraic *approximate* key-message synthesis under no-wrap/common-key-context; **UNCLEAR** full RNS-CKKS correctness/security and practical advantage.
**RESULT:** `K0+K1` encrypts `μ(m0+m1)+δ+e0+e1`, with coefficient δ∈{−1,0,1} for no-wrap nearest rounding. Example P101/q7/m0=1,m1=3 gives μ_syn57 vs μ_target58, δ−1; independently drawn noise variance2σ² versus σ² fresh. Public sum is not a re-randomized fresh key, and dynamic matrix family would need basis keys and online combining, not free rotation-key reuse.
**NEXT_ACTION:** **HUMAN_REVIEW / recommend PARK generic AKS public-basis linear synthesis** as elementary RLWE linearity and weak cost model. Continue only with one concrete source-realistic low-dimensional update family, exact RNS+noise budget, quantified break-even against ordinary Galois key plus online plaintext multiplication, and a plausible genuinely new technique; do not repeat m0≠m1 or small rounding toy loops. Fixed-DFT author results unaffected.
**STATE_UPDATE:** **YES** — closes I168 two-basis source-equation test and changes priority of dynamic AKS basis-key line to PARK recommendation; preserve source full PDF and pinned implementation. vFHE P1 source-gated and older parks unchanged.
