# SHIP I217 — Doubling N at fixed h,w does NOT meaningfully enlarge windowed sparse-secret space

**Date:** 2026-10-14 Asia/Tokyo. **Track:** independent SHIP evaluation-key memory, following I216. Read before writing: START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, concurrent global STATE.md (vFHE V17, READ ONLY), independent findings/ship-memory-STATE.md I216 SHA `d28506efc750c33060c6b7ce2e1b53754f9cbae7`, and I216 source finding. Do not edit global STATE or source upstream. Scientific parent SHIP EUROCRYPT 2025, ePrint 2025/784; implementation evidence independent third-party Poulpy, NOT author's HEaaN, pinned `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`.

## ONE primary falsifiable hypothesis and ONE cheapest decisive test

**H217:** After the I216 N16384 128-bit-certification failure, simply increasing the illustrative ring degree to **N32768**, keeping SHIP sparse bottom-secret h32/window w256 fixed, increases the *number of possible hidden sparse bottom secrets* by at least **2^16**, making it reasonable to regard generic fixed-HW sparse-ternary security estimates at the larger N as distribution-matched without separately modeling the window constraint.

**Falsifier:** Read pinned `ShipSecretSpec::sample` (not an informal uniform-sparse approximation); compute the exact number of signed *legally supported* sparse secrets for both degrees, considering adjacent support-window overlaps and source duplicate rejection. Check ratio in bits. Distinguish **log2 of support set cardinality** from actual entropy, min-entropy, and concrete RLWE attack security.

## Source [FACT]

- Pinned `poulpy-ckks/src/layouts/ship/secret.rs` blob `e570595f803a4a114c0e4d5a62d0a7af96057e9d`: `ShipSecretSpec::sample` chooses **one** nonzero index `j_k=(k*N/h+δ_k) mod N` per ordered k=0,…,h−1; `δ_k∈[-w,w]`; sign independently ±1; rejects duplicate indices by resampling current position. `ShipSecretSpec::from_support` validates exactly these windowed constraints. The RNG samples offsets via rejection and signs subsequently. Because duplicate rejection can bias the law, our count is the **support set size**, not automatically Shannon or min-entropy.
- Pinned `poulpy-ckks/src/layouts/ship/plan.rs` blob `364f4235253a3c76c70dfacf3ea24c5e69a2c3c2`: `spacing=N/h`, `window=w`, `mux_candidates=ceil((2w+1)/θ)`. With h32,w256, source illustrative choice N16384→spacing512, and suggested N32768→spacing1024. Source `ShipPlan::new` permits both, assuming other params consistent.
- Pinned `poulpy-ckks/src/test_suite/mod.rs` has standard source suite **dense secret fixed ternary HW192**, distinct from h32 regularly spaced encapsulated sparse bottom secret.
- Actual lattice-estimator source `malb/lattice-estimator@main` `estimator/nd.py` `SparseTernary(p,m,n)` (read source): counts globally selected p coefficients +1 and m coefficients -1 via `binomial(n,p)*binomial(n-p,m)` and assumes no per-window position law. It also holds p/m fixed; source `ShipSecretSpec` independently samples signs, so p and m fluctuate. Hence plugging `ND.SparseTernary(16,16,n=32768)` **does not match** SHIP's law. `SparseBinomial(eta=1,hw32,n)` would allow independent signs but still globally uniform nonzero positions, thus not support-windows; the regular-window law needs custom attacker distributions/reduction. **No estimator run**.
- General guidelines from `https://homomorphicencryption.org/security-guidelines/` and 2024 ePrint2024/463 explicitly do not certify h192 sparse fixed-weight nor structured windowed h32 bottom key, so no 128-bit claim follows from table N32768 log2q868.

## [EXECUTED] Exact combinatorial count

At fixed h32,w256 each window has **513 indices** and independent sign ±1, giving universal cardinality upper bound `(2×513)^32=1026^32`, independent of N. In N32768, spacing1024 exceeds window diameter512, so all 32 windows are disjoint; **exact support cardinality** is `|S32768|=1026^32`.

At N16384, spacing512 equals 2w; adjacent cyclic windows share precisely *one endpoint* (right endpoint of window k and left endpoint of k+1); source's duplicate rejection forbids simultaneous selection of those endpoints. Model each window selection category L/interior/R with multiplicity `weights=(1,511,1)`; nearest-window forbidden transition `R→L`, cyclically. Define 3×3 transfer matrix `T_ij=weights[j] * [not(i=R,j=L)]`. **Exact valid unsigned offset assignments = trace(T^32)**; multiply by 2^32 for independent signs. All valid configurations are reachable by source's collision-rejection sampler, though not equiprobable. Verified exact integer matrix exponentiation:
- `log2|S16384|=320.08990507411175`.
- `log2|S32768|=320.0900804994257`.
- `log2(|S32768|/|S16384|)=**0.000175425313955202 bit**` — vastly less than hypothesized 16 bits. No extra entropy guarantee.
- A *globally unconstrained* h32 ±1 support would have `log2(C(N,32)2^32)=362.29303299238` at N16384 and `394.31489167765517` at N32768: apparent increase **32.02185868527516 bits**, showing precisely why **globally uniform sparse ternary model is not source-faithful**.
- Contrast dense fixed-hw192 signed ternary supports `log2(C(N,192)2^192)` grow **1693.944886052657→1886.7569256707725**, +**192.81203961811548 bits** from N doubling. So a real lattice attack hardness gain from higher dimension for **dense key** remains plausible; this result applies only to support space of **windowed bottom key**, not the whole scheme.

Script run in current container (exact Python big ints + math log2, deterministic no randomized sampling, matrix transfer trace):
- `/mnt/data/ship_i217_windowed_secret_space_gate.py`, SHA256 `f907790837822b058a39cd147b7f22163dc08c5bfaefeb993e3898bd51ee1698`.
- `/mnt/data/ship_i217_windowed_secret_space_results.json`, SHA256 `2e9932f7f976b84f57989d011cbd337da362a772d5ef5fe40c28cb7f0239cd33`.
- The script asserts legal support counts and gap under 0.001 bit.

## Security interpretation [NO ATTACK]

**H217 FAIL:** doubling N with h32,w256 does *not* meaningfully increase the structured sparse **bottom secret search-space cardinality**, and standard `ND.SparseTernary` or fixed-p/m law does not model source. This is a source-specific objection to a **shortcut security parameterization**, not an attack, KDM proof, or 128-bit insecurity proof. **320.09 bits is log2 number of support possibilities**, not "320-bit security." Meet-in-middle / lattice hybrid attack complexity, oracle access, public auxiliary-key leakage, effective sample modulus for the bottom key, and correlation with dense secret are **NOT calculated**. There may still be real lattice hardness improvements with larger N even at fixed bottom support entropy; entropy alone cannot prove/deny 128-bit security.
- Sparse bottom key `Distribution::ENCAPSULATED("ship")` is involved in dense→sparse KSK; it is not necessarily a standard `N,q=2^676` plain-LWE instance with unlimited samples under that secret. One **next decisive source audit** is to identify *which publicly exposed ciphertext/key rows encrypt under the bottom sparse secret, at what exact precision*, before attempting a meaningful sparse-key attacker estimator. Do not misassign HMux key's output secret (automorphed dense key) as bottom sparse key.
- Other unresolved constraints: I210 augmented full joint eval-key KDM/circular-security proof unestablished; I207 81.45% IFMA key memory only hypothetical and not security matched; online ~480 extra CT×CT/four serial mux levels unmeasured; no compiled Poulpy. Original SHIP paper and original author HEaaN are not accused of a security flaw. NOVELTY NOT VERIFIED.

## End of iteration

**STATUS:** FAIL H217 N-doubling-meaningful-windowed-secret-space-growth shortcut; **PASS exact source-shaped support cardinality count**; **UNCLEAR** true RLWE/hybrid sparse-secret security and 128-bit strength.
**RESULT:** With exact SHIP window constraints, N16384→N32768 at fixed h32/w256 changes log2 support space by only +0.000175 bit, **not +32 bits** as an unconstrained sparse secret model would predict. Need attack/source distribution match; generic SparseTernary estimator alone cannot certify.
**NEXT_ACTION (ONE primary source audit if PI continues):** Identify precise public **under-sparse-key** ciphertext materials/precision/sample exposure in Poulpy's `ShipKeySet::generate`, and distinguish them from under-automorphed-dense HMux keys, tensor and masks; determine whether h32 windowed bottom key actually faces a high-q RLWE attack surface or only small modulus/other relation. This is the cheapest prerequisite for selecting a realistic concrete estimator input. Then decide conditional continued security parameterization versus PARK, under human PI judgment. Do not start more fabricated LWE bit estimates. **STATE_UPDATE: YES** independent SHIP only, NO vFHE global STATE.
