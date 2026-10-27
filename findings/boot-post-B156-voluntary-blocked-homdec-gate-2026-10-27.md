# BOOT post-B156 — voluntary blocked homomorphic decryption gate

Date: 2026-10-27
TRACK_ID: BOOT

State impact: NONE.
- LATEST_COMPLETED remains B156_AUDIT.
- B157 remains PENDING_CODEX_QUOTA.
- B145+B152 remains MAIN_POSITIVE_CANDIDATE.
- No Codex / GPU / remote native execution was used.

## Source target

Primary target:
- ePrint 2026/975, *Functional Bootstrapping for a Single LWE Ciphertext with O~(1) Polynomial Multiplications* (Zheng, Li, Wang).
- Author repository inspected: xiaopeng-stu/bfv-functional-bootstrapping (current HEAD, not treated as a pinned paper artifact).

Closest ancestor:
- ePrint 2023/910 / ASIACRYPT 2023, Liu–Wang, *Amortized Functional Bootstrapping in Less than 7 ms, with O~(1) Polynomial Multiplications*.

Collision source still unavailable:
- ePrint 2026/1401, *A New Framework for Efficient Multivariate Functional Bootstrapping*.
  Full text could not be acquired through the configured ePrint/mirror path. Novelty therefore remains unresolved.

## 1. Exact source fact from 2026/975

Let m be batch size and r=N/m.

The paper's Step 1 uses:
- if r >= n: exactly one BFV ciphertext encrypting repeated LWE secret s, one pt×ct multiplication with public -a, then rotate-and-sum over n positions;
- if n > r: capacity-forced blocking t=n/r, with one BFV encryption per secret block, one pt×ct per block, sum blocks, then one rotate-and-sum over r positions.

The paper states Step-1 complexity:
  ceil(n/r) plaintext-ciphertext multiplications
  + log2(min{r,n}) rotations.

Thus the paper always uses the largest capacity-allowed block width. It does not expose deliberate blocking when r >= n as an optimization variable.

The paper also counts BFV encryptions of the LWE secret as part of the bootstrapping-key size.

## 2. Candidate: VOLUNTARY_BLOCKED_HOMDEC

For r >= n, deliberately choose a block width b < n, with b | n and b | r (power-of-two case first).

Define:
  k = n/b.

Offline:
- create k BFV/RLWE ciphertexts C_0,...,C_{k-1};
- C_q encrypts secret block s[qb:(q+1)b], periodically repeated/aligned to the same b local coordinates in every row.

Online for each public LWE mask a:
- construct public plaintext masks P_q with entries -a[qb+j] aligned to local coordinate j;
- compute
    H = sum_q C_q ⊙ P_q;
- apply rotate-and-sum only over the b local positions;
- add public b-coordinate.

The resulting replicated plaintext is exactly:
  b_LWE - <a,s> mod T.

Cost:
  k pt×ct multiplications
  + log2 b rotations,
i.e.
  k P + log2(n/k) R.

## 3. Algebra gate

Exact modular falsification was performed over 120 valid tuples spanning:
- n from 16 through 2048,
- m in {1,2,4,8},
- k in powers of two subject to divisibility/layout constraints.

No counterexample was found.

The construction is algebraically exact; no approximation or new decryption assumption is introduced.

## 4. Restricted-model lower bound / Pareto frontier

Model:
- k offline ciphertexts encode public fixed layouts of the secret;
- public input a enters online only through diagonal plaintext-ciphertext multiplication;
- online linear aggregation is by additions and automorphism/rotation steps;
- no ciphertext-ciphertext multiplication is used in Step 1.

After t binary rotate/add aggregation layers, one target slot can depend on at most k*2^t independently weighted public coordinates.

For arbitrary n-dimensional inner product, necessity:
  k * 2^t >= n.

Therefore:
  t >= ceil(log2(n/k)).

For power-of-two n,k, VOLUNTARY_BLOCKED_HOMDEC attains equality.

This explains the candidate as a storage/rotation Pareto frontier in this restricted Step-1 model, rather than an arbitrary block tuning.

## 5. Key-memory model

Let:
- C = bytes of one full-level ordinary BFV ciphertext encrypting a secret block;
- G = bytes of one required full-level Galois/rotation key.

Relevant Step-1 key material:
  K(k) ≈ k C + log2(n/k) G.

Continuous optimum:
  k_mem* = G / (C ln 2),
clamped to [1,n] and rounded to legal powers of two.

For current 9-bit m=1 author-repo parameters:
- n=2048;
- 11 full-level Galois keys at L19/logQ~679 total 660.02 MiB, about 60 MiB/key;
- one full-level degree-1 BFV ciphertext is about 10 MiB at N=32768 and 20 Q limbs.

Thus G/C ≈ 6 and:
  k_mem* ≈ 8.7.

Nearest power-of-two candidate k=8:
- baseline relevant material ≈ 1*10 + 11*60 = 670 MiB;
- k=8 candidate ≈ 8*10 + 8*60 = 560 MiB;
- net saving ≈ 110 MiB.

Against the current ~0.73 GiB total reported BSK scale, this is roughly a 15% whole-key-size opportunity before exact serialization accounting.

Important: this is a source-derived model, not a native measured candidate result.

## 6. Online-latency model

Online:
  L(k) ≈ k P + log2(n/k) R,
where P is one full-level no-rescale pt×ct and R one full-level rotation.

Continuous optimum:
  k_lat* = R / (P ln 2).

Current source does not isolate P and R enough to certify k_lat*.

A rough cross-configuration decomposition using current 9-bit Step-1 times:
- m=1: ~0.6934 s for 1 block + 11 rotations + one online secret encryption;
- m=128: ~0.8376 s for 8 blocks + 8 rotations + eight online secret encryptions.

Ignoring parameter/overhead differences and writing X=Encrypt+P gives:
  R ≈ 58.9 ms,
  X ≈ 45.8 ms.

This is only a plausibility check. No speedup claim is made without a matched native benchmark and offline-secret-key preprocessing.

## 7. Current-repo online/offline accounting issue

The current author repository's timed Step-1 path calls EncryptNew(ptSk) for each secret block inside each online invocation.

The same program:
- counts these encrypted-secret ciphertexts as bootstrapping-key material in its BSK-size summary;
- also contains a separate preprocessEncryptedSecretBlocks function and an alternative packing path accepting pre-encrypted secret blocks.

Therefore the current HEAD's Step-1 timing includes regeneration of static BSK material. This should be corrected in any future matched comparison:
- pre-encrypt secret blocks offline for BOTH baseline and candidate;
- do not count EncryptNew in online latency.

Do not infer that the published paper's original 3.15 s number necessarily used this current-HEAD accounting; the repository is not pinned to the paper artifact here.

## 8. Noise gate

No paper-level blocker found.

Proxy model:
Let V0 be the masked fresh-secret-ciphertext error variance contribution for the baseline, and VR a rotation/key-switch error contribution.

Deliberate k-blocking:
- creates roughly k independent masked fresh-encryption contributions initially;
- reduces rotate/sum width from n to n/k.

Under the standard isotropic/isometric approximation:
- inherited fresh-encryption term:
    baseline ~ n V0;
    candidate ~ (n/k)*(k V0) = n V0;
  so the main fresh-encryption contribution is approximately conserved.
- rotation/key-switch term:
    baseline ~ (n-1) VR;
    candidate ~ (n/k - 1) VR;
  so this term decreases with k.

This is not a formal worst-case BFV error proof; full covariance/plaintext-multiplication effects remain to be checked before native promotion.

Source-level empirical support:
the current 9-bit m=128 configuration is already capacity-forced into 8 secret blocks + 8 rotations and reports output noise sigma_res ~6.5792, versus ~6.4474 for m=1. The ratio is only ~1.0204, despite different downstream packing/evaluation. This does NOT isolate Step 1, but strongly argues against catastrophic noise growth from eight blocks.

## 9. Security gate

No new security assumption identified.

The LWE secret s_LWE is independent of the BFV/RLWE secret s_BFV.

The baseline already publishes BFV.Enc_{s_BFV}(s_LWE-layout) as bootstrapping-key material. The candidate publishes k encryptions of correlated/publicly partitioned functions of the same s_LWE.

By multi-message IND-CPA/semantic security of BFV with an independent encryption key, this does not introduce a new circular/KDM relation.

The candidate also removes some Galois keys rather than adding new ones.

This matches the Liu–Wang 2023 security argument for BFV encryptions of the LWE secret under an independent BFV key.

## 10. Prior-art gate

Important adjacent collision:
Liu–Wang 2023 explicitly precomputes rotations of BFV.Enc(s_LWE) during bootstrapping-key generation and stores the rotated ciphertexts in btk, saving those rotations online. They also use level-specific rotation keys to reduce BSK size.

Therefore the broad idea:
  "store more secret-related BFV ciphertext material to save online rotations"
is PRIOR ART and is NOT novel.

However, no direct collision was found for the narrower construction:
  deliberately decompose the secret into more aligned blocks than capacity requires,
  thereby replacing expensive full-level rotation keys with much smaller ordinary encrypted-secret ciphertexts,
  while preserving a logarithmic rotate-and-sum and potentially improving BOTH online latency and BSK memory.

Liu–Wang's cached-rotation / BSGS technique does not directly dominate this structured m=1/small-batch inner-product tradeoff: eliminating rotations by caching rotated secret copies generally increases the number of pt×ct products substantially, whereas blocked homomorphic decryption retains t=log2(n/k) aggregation and attains k*2^t=n.

Still unresolved:
- ePrint 2026/1401 full text is unavailable and must be checked before novelty can be upgraded.

## 11. Decision

Status:
- ALGEBRA: PASS
- RESTRICTED-MODEL PARETO LOWER BOUND: PASS
- SECURITY: NO_NEW_BLOCKER
- NOISE: PLAUSIBLE / FORMAL_BOUND_PENDING
- MEMORY_VALUE: PROMISING (~110 MiB / ~15% modeled at 9-bit m=1, k=8)
- LATENCY_VALUE: PLAUSIBLE_NOT_MEASURED
- DIRECT_PRIOR_COLLISION: NOT_FOUND
- ADJACENT_PRIOR_ART: STRONG (Liu–Wang pre-rotated secret ciphertexts)
- 2026/1401 COLLISION CHECK: SOURCE_REQUIRED
- NOVELTY: PROMISING_SECONDARY / NOT_ESTABLISHED

Do NOT promote above B145+B152.

## 12. Future decisive test (do not run while Codex unavailable)

When experimental quota exists, a cheap matched micro-gate should precede any full bootstrapping benchmark.

Use the same 9-bit m=1 2026/975 current implementation/parameters.

Baseline:
- precompute the single encrypted-secret ciphertext offline;
- k=1,b=2048;
- 1 no-rescale pt×ct;
- 11 high-level rotations.

Candidates:
- k in {2,4,8,16};
- b=2048/k;
- precompute all encrypted-secret block ciphertexts offline;
- k no-rescale pt×ct;
- log2 b high-level rotations.

Measure ONLY Step 1 first:
- exact plaintext parity;
- online latency;
- isolated pt×ct and rotation time;
- output BFV noise before Step 2 if available;
- serialized secret-block ciphertext bytes;
- serialized retained Galois-key bytes;
- peak memory.

Kill criterion:
- if no k improves BOTH Step-1 online latency and Step-1 key material after fair offline preprocessing, PARK immediately.

If k=8 (or another k) passes, only then run end-to-end FBS.

This future micro-gate is separate from B157 and must not replace/reschedule B157.
