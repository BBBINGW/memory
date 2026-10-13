# I174 — SHIP mask partition-of-unity does not allow dropping one of four encrypted masks PER hybrid candidate without encrypted onehot

**Date:** 2026-10-13 (JST). PI approved with “好的，请继续”. Read `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → `STATE.md` after I173 blob `e3735d8417b17a49e85f2d7a299ed9bfe61ad414`, then I173 finding. ONE primary source-anchored conjecture; ONE exact reproducible secret-index gating test, with affine-uniqueness cross-check. No new cryptographic construction, software runtime benchmark or unverified author exploit.

## Primary sources and version caveats

**[FACT original paper]** Cheon, Hanrot, Kim, Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, ePrint **2025/784** https://eprint.iacr.org/2025/784. Complete Research MCP `github-mirror` PDF **33 physical pages** SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`; latest official version **VERSION_UNVERIFIED**. Re-read primary §3.3 physical pp16–17, §4.1 pp17–18, §4.4 pp21–22. Lemma1 defines four slot masks for each sparse-secret monomial (sign and support position) with `∑_{k=1}^4 m_{j,δ}^{(k)}=1` for each δ∈{1,2}; paper itself explicitly notes this sum can reduce memory. Eq.(4) writes masked sum of four rotated phase functions `π_k(a)`; **do not assert `π_2=-π_1` or `π_4=-π_3`**: `π_1(a)=ω_1(a)` with `ω_1(a)=(ω^{a_i})`, and `π_2(a)=ω_1(-a)=(ω^{-a_i})`, NOT linear negations. Fused hybrid §4.4 Eq.(7) constructs encrypted masks `M^{(k)}(j)_i = 1_{i=j} * m^{(k)}`, and the Algorithm4 Eq.(8) variant folds an additional pre-rotation into these masks. Paper notes its actual implementation reverses column/mux stage order compared with written Algorithm4.

**[FACT pinned third-party code]** Independent Poulpy repo `poulpy-fhe/poulpy`, pinned `main` commit `250d4392656cd313f92ca66d96d8865702d39ddf` (not author's original HEaaN). `poulpy-ckks/src/encoding/ship/masks.rs` blob `2754eafd1ad24c1eca1382204d37005449f88cca`, `ship_pre_rotated_masks` lines ~9–29, `ship_mask_slot_vectors` lines ~40–75:
```
for c in 0..θ:
  for band k=1..4:
    M[c,k][i] = band_k[(i + 2m - (p+c)) mod m]  if c == u mod θ
                0                             otherwise.
```
The source uses θ secret low-digit column candidates, encrypts all `4θ` key masks at every sparse support, and `poulpy-ckks/src/reference/ship/masking.rs` blob `91ba98e08ea7172b34c492d9fcc69ef18628820d` lines~31–120 accumulates all mask/p_i convolution pairs. Source `keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4` lines225–301 eagerly prepares all into `CnvPVecL`; exact key count previously verified in I172. This is an independently validated paper-based implementation, not reproducibility of original HEaaN.

## ONE primary hypothesis and decisive falsifier

**[HYPOTHESIS]** Since the four original *unfused* masks sum to plaintext `1`, after hybrid column onehot fusion the same identity holds **individually for each candidate c**. Therefore evaluator may drop the fourth encrypted mask of **every** candidate c and replace it using public `1−∑_{k=1}^3 M[c,k]` with no extra encrypted onehot material or costly online calculation: a **25% prepared selector count reduction** for all θ.

**[TEST]** Apply **exactly the source's mask generation**, with a legal θ=4, m=8, j=3, sparse sign s=+1, low-digit secret u=2, public p=0. Enumerate 8 slots for each of the `θ×4=16` plaintext masks. Check separately the four-mask sum at each candidate, and the sum across candidates; compare incorrect local `1−∑_{k≤3}` reconstruction to actual fourth mask.

## Results: the gating changes the identity

**[DERIVATION]** Let `b_k(x)` be the *four unfused slot mask values*, `∑_k b_k(x)=1` pointwise. The source hybrid key embeds
```
 M[c,k](x) = 1_{c=u0} * b_k(rot_c(x)),  u0=u mod θ.
```
Rotation preserves the four-mask partition of unity. Hence the **actual** identities are
```
 ∑_{k=1}^4 M[c,k](x) = 1_{c=u0}        [NOT public 1 per c]
 ∑_{c=0}^{θ−1}∑_{k=1}^4 M[c,k](x) = 1 [public globally].
```
The first RHS is secret-dependent **encrypted onehot** `H_c`; to delete the fourth mask of every column, the formula is `M[c,4]=H_c−∑_{k≤3}M[c,k]` and one must still supply/compute all `H_c` in encrypted form at comparable cost. Replacing each `H_c` with publicly known `1` changes the evaluated function, including for every **unselected** candidate. Thus there is NO cost-free, key-object 25% reduction from this one lemma after fusion.

**[ONE exact test; done with deterministic JS arithmetic reproducing pinned Rust masks]** For θ4,m8,j3,s1,u2,p0: `∑_k M[c,k](x)` is respectively eight 0s for c0, eight 0s for c1, eight 1s for c2, eight 0s for c3. The naive public-one reconstruction `1−∑_{k≤3}M[c,k]` for the fourth mask differs from actual last mask in **all 8 slots of each of the 3 unselected candidates**, 24 false entries; actual global across all four candidate sums is 8 ones. PASS exact source-code-model calculation, **FAIL per-candidate public-one identity**. Repeated affine uniqueness checks below use same original mask data family (not a separate second hypothesis).

**[Derived tighter restricted affine statement]** For fixed θ=4,m8,j3 with allowed s∈{±1}, u∈{0,1,2,3}, and slot x varying, the possible 16-dimensional fused-mask vectors `(M[c,k](x))` contain **each canonical basis vector e_(c,k)**: each secret candidate is selectable; s chooses which two of the four k bands can occur, and x can choose either band. Exact enumeration exhibited source-valid witness `(s,u,x)` for every one of the 16 standard basis vectors. Therefore **any** source-parameter-independent public *affine constant* relation
```
  ∑_{c,k} α_{c,k} M[c,k](x) = β
```
holding for all these legal inputs must have `α_{c,k}=β` for all c,k. Thus, **up to scalar, the single global sum-to-one relation is the only public affine-constant identity in this whole mask family** at the fixed θ4,m8,j3 configuration. With that one relation, at most **one** of the `4θ` prepared selectors per support can be eliminated by a direct affine rewrite with known constant and no other encrypted selector keys; this is **not a general key-material lower bound against alternate cryptographic/compression algorithms, nonlinear relations or new inputs**.

For public test plaintext operands `P_{c,k}`, the full linear masked sum is
```
 F=∑_{c,k} M[c,k] P[c,k].
```
Using the one global identity and a chosen reference index r, one can write the exact **plaintext symbolic identity**
```
 F=P_r +∑_{(c,k)≠r} M[c,k] (P[c,k]−P_r).
```
It suggests saving one prepared mask per support but requires changed public plaintext preprocessing, proper CKKS scale/modulus alignment, and a source noise/security proof for any actual ciphertext implementation. It is not implemented/benchmarked. It is NOT a 25% memory reduction: max by this one affine relation `1/(4θ)`, e.g. source θ9 →2.78%, θ17→1.47% per support; θ4→6.25%. Individual masks of same k remain independently randomized encryptions in pinned Poulpy; a sum of ciphertexts does NOT equal a deterministic plaintext constant at ciphertext level unless explicitly derived/correlated at keygen. Algebraic rewrite avoids requiring exact ciphertext sum equality.

**[CRITICAL caveats]**
- Original SHIP paper already says `∑_k m^{(k)}=1` and that it can save memory, so **this is not a new research technique** and is NOT an overlooked published author's error.
- The exact uniqueness proof pertains to *public, fixed-coefficient affine-constant mask relations* over the specified legal source mask family. It does NOT preclude clever encrypted onehot reuse, nonlinear key encodings, on-the-fly generation, or secret-conditioned key arrangements with different costs.
- The small m8/θ4 toy uses source-compatible selector-mask coding; **not** an implementation of the full CKKS bootstrapping, and no modulus/noise/security/latency gain has been demonstrated.
- Paper source mirror latest version `VERSION_UNVERIFIED`. Pinned Poulpy implementation is independent from original HEaaN, which remains unverified as to actual memory.

## End of Iteration 174

**STATUS:** **FAIL** hypothesis that 4-mask unity gives 25% prepared-key reduction FOR EACH secret-gated hybrid column using free public constant; **PASS** exact counterexample and source-only globally summed identity; **UNCLEAR** a nontrivial secure prepared-key compression in another model.
**RESULT:** Hybrid fusion changes `∑_k M[c,k]=1` to `1_{c=u0}` (SECRET). Only `∑_{c,k}M[c,k]=1` is public; naive per-column drop produces 24 false slot-mask values in a legal θ4,m8 example. For this source family, all 4θ canonical basis vectors occur, so unique public affine-constant relation means at most **one** mask per support is directly eliminable via the one global affine trick, `1/(4θ)` vs 25%. Original paper already flags sum relation and is not contradicted.
**NEXT_ACTION:** **HUMAN_REVIEW / recommend PARK ordinary SHIP 4-mask prepared-key compaction** unless there is a **genuinely new** secret-choice-preserving representation that reduces prepared selector keys substantially while keeping the source's parallel low-latency property. If PI assents to PARK, I175 should choose a DISTINCT source-available, meaningful FHE cost frontier, not revisit basic selector affine identities, seeded serialization or simple ciphertext count estimates. No benchmark or source error claim.
**STATE_UPDATE:** **YES** — material source-specific impossibility of claimed 25% trivial affine per-column prepared-key removal; formalizes exactly which public identity survives hybrid onehot fusion and closes simplistic mask compression avenue.
