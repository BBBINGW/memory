# BOOT — KSK elimination via public linear secret embedding: algebra PASS, value FAIL

Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER_LEVEL_ONLY
CODEX: NOT_USED
NATIVE: NOT_RUN

## Authoritative BOOT state (unchanged)

LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE_GATE: B163_CORRECTED_B160_NOSCALE_SELECTOR_GATE
B163_STATUS: PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
DO_NOT_AUTO_RUN_CODEX: YES

B145+B152: PARK / FAIL_NATIVE_VALUE
B158_ALGEBRA: PASS
B158_CTCT_MULT_COUNT: OPTIMAL
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B158_NATIVE_FEASIBILITY: UNRESOLVED
B162_B161_HYBRID: VALID_FAIL_AT_K1024
B163: NOT_RUN

## Motivation: KSK once dominated modern NTRU/FHEW bootstrap keys

CRYPTO 2023 Xiang et al., "Fast Blind Rotation for Bootstrapping FHEs" reports parameter sets where the blind-rotation EVK is much smaller than the final LWE key-switching key. In P128G the EVK is about 17.90 MB while the KSK is about 203.44 MB; in the updated NewP128G appendix the EVK is about 7.54 MB while KSK is about 65.97 MB.

So an initial structural question was whether the final key-return family could be eliminated entirely rather than compressed.

Primary source:
https://eprint.iacr.org/2023/1564.pdf

## Algebraic public-mask-projection lemma

Let the first-layer LWE secret be s in Z_q^n.
Let the coefficient vector of the second-layer ring/NTRU secret be a public linear image
    t = T s in Z_q^N
for public T in Z_q^{N x n}.

Suppose sample extraction yields an LWE ciphertext (a,b) under t whose phase is
    b - a^T t = m + e.

Define publicly
    a' = T^T a.

Then
    b - (a')^T s
      = b - a^T T s
      = b - a^T t
      = m + e.

Therefore the map (a,b) -> (T^T a,b) returns the ciphertext to secret s with no encrypted key-switching key, no added noise, and no approximation.

Status:
    PUBLIC_MASK_PROJECTION_ALGEBRA = PASS.

For a zero-padding embedding, this is simply dropping mask coordinates paired with known-zero secret coefficients.

## Prior art boundary

### Micciancio–Sorrell 2018: same-secret special case

"Ring Packing and Amortized FHEW Bootstrapping" already states that if the ring-register secret z is chosen so that its coefficient vector equals the original LWE secret s, then the intermediate LWE after extraction is already under the desired secret and the usual final key switch can be omitted.

This is the identity-map / n=N special case.

Source:
https://eprint.iacr.org/2018/532.pdf

Therefore:
    SAME_SECRET_KSK_ELIMINATION = OLD PRIOR ART.

### Wang–Xiang–Zhang–Deng–Feng 2025: zero-padded target secret and NTRU-domain key return

"Improved FHE Bootstrapping and Its Applications in Discretized Neural Networks" gives a stronger current value baseline.

The paper:
1. samples the first-layer LWE secret s;
2. pads s with N-n zeros to form an N-dimensional coefficient-vector/ring-secret target;
3. resamples until that target polynomial is invertible;
4. performs the key switch while the ciphertext is still in the NTRU layer;
5. extracts only after switching to this padded target.

Thus the natural zero-padding embedding is already explicit in current prior art, although they retain an independent blind-rotation secret f and use a compact NTRU key switch from f to the padded s-target.

The paper bases the modified key generation on a Hint-NTRU assumption and explicitly discusses the related-secret setting.

Primary open-access source:
https://doi.org/10.1049/ise2/7097351

## Decisive current value comparison

The 2025 paper reports in its DiNN comparison:
- old KSK: 80.10 MB;
- new KSK: 0.00525 MB;
- new BRK: 3.45 MB.

Therefore the remaining KSK is only about
    0.00525 / (3.45 + 0.00525) = 0.001519,
or roughly 0.152% of the new bootstrap-key bytes.

Deleting the KSK completely could reduce the reported key bytes by only about 0.15%, before accounting for any parameter/security cost.

The paper also states that the primary computational and storage costs now arise from blind rotation.

Hence the original KSK-dominance motivation from the CRYPTO 2023 baseline is no longer current after this 2025 construction.

## What would be required to remove even this tiny KSK

The only remaining distinction would be to set the blind-rotation secret itself to
    f = T s
rather than keep f independent and key-switch to the T s target.

Correctness is immediate from the public-mask-projection lemma, but security becomes materially harder.

For the NTRU blind-rotation construction, evaluation keys encrypt functions of first-layer secret coefficients under f. If f=T s, those messages are now functions of the same underlying secret used in the NTRU denominator/key. This creates a stronger related-secret/KDM setting than the ordinary independent-layer formulation.

Moreover, f lies in the publicly known low-dimensional subspace Im(T). For zero-padding, N-n secret coefficients are known to be zero. Standard NTRU/RLWE hardness cannot simply be cited as if f were sampled from the full ring-secret distribution.

Relevant security literature:
- Order-LWE and the Hardness of Ring-LWE with Entropic Secrets, ePrint 2018/494.
- Current structured/sparse MLWE/RLWE attack literature further cautions against equating ring-structured small-secret security with generic LWE estimates.

This does NOT prove the proposed correlated secret insecure. It shows that a standard full-ring NTRU/RLWE security claim would be unjustified without a dedicated assumption/reduction and concrete estimate.

## Research decision

LINEAR_SECRET_PUBLIC_RETURN = PASS algebraically.

But after the 2025 state of the art:
- MEMORY_VALUE = FAIL: removable KSK is already about 0.15% of reported key bytes.
- LATENCY_VALUE = LOW / NOT_ESTABLISHED: the remaining ring-domain key return is compact while blind rotation dominates.
- NOVELTY = WEAK: identity-map omission is known since 2018 and zero-padded secret alignment is explicit in Wang et al. 2025.
- SECURITY = HARDER / UNRESOLVED: setting the blind-rotation secret itself to T s creates a public low-dimensional related-secret/KDM setting.

CCF_A_B_VALUE = FAIL_CURRENTLY.

## Gate decision

PUBLIC_MASK_PROJECTION_ALGEBRA: PASS
SAME_SECRET_IDENTITY_MAP: PRIOR_ART
ZERO_PADDED_TARGET: PRIOR_ART
FULL_KSK_ELIMINATION_BY_SETTING_BLIND_ROTATION_SECRET_TO_Ts: PARK
VALUE: FAIL_CURRENT_BASELINE
SECURITY: UNRESOLVED / STRONGER_ASSUMPTION
NATIVE_REQUIRED: NO

Do not spend Codex/native cycles on this candidate.

## New structural target

The 2025 baseline changes the bottleneck:
- KSK has become negligible;
- BRK remains approximately 3.45 MB and dominates key storage.

Therefore the next useful BOOT scout should target the n-dependent blind-rotation evaluation-key family itself, not the final KSK.

Audit this against:
- sparse-secret bootstrapping / CRYPTO 2026 ePrint 2026/1730;
- later sparse-key compiler work;
- key-compression / seeded evaluation-key prior art;
- grouped-inner-product / one-hot / Cuckoo representations that may already reduce n secret-dependent objects.
