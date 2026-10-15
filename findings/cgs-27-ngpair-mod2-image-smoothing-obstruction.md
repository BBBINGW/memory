# CGS-27 — Fixed Gram is not a discrete-lattice smoothing theorem: universal mod-2 image obstruction

**Date:** 2026-10-15. **Single active workflow:** FHE PI selected CGS; root `STATE.md` last CGS-26. One primary falsifiable hypothesis + one exact minimum test. The NG secret-covariance detour CGS-22–26 is being assessed for sufficiency; original Okada–Takagi 2025/409 conditional Gaussian / O(LDec) storage remains OPEN.

## ONE primary hypothesis, exactly scoped

**H-CGS27 [FAIL for the named shortcut]:** For rank-two binary ±1 negaperiodic Golay (NG) keys `(a,b)` with exact public covariance
`C C^T=mat(a)mat(a)^T+mat(b)mat(b)^T=2n I_n`, the **unflooded integer convolution**
`y=mat(a)r_1+mat(b)r_2` for independent sufficiently wide integer-discrete Gaussians `r_i` can be treated as close to a full-support isotropic integer Gaussian on `Z^n` merely from this stacked **real Gram** identity. Thus source Lemma 7.1's individual lattice-smoothing/spectral conditions could be replaced by the stacked real singular-value `√(2n)` *without extra lattice-congruence checks*.

**ONE decisive test:** Determine `rank_{ᵓ_2}([mat(a)|mat(b)] mod2)` for any dense ±1 keys and the exact support of `y mod2`. If rank is far below n, there is an information-theoretic separation from a full-support discrete Gaussian whose parity is nearly uniform. This test is **deliberately before the source's independent flooding E**: it does not claim a break of the full source Eq.(25).

## Primary-source anchor and prior art [FACT]

- **Okada–Takagi**, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025, ePrint **2025/409**, https://eprint.iacr.org/2025/409, full original mirror 40 physical pages SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, VERSION_UNVERIFIED. **Algorithm 7 physical p29** samples `ζ^{sid}` from hidden-shape discrete Gaussian and Shamir-shares it. **Lemma 7.1 physical pp30–31 Eqs(25),(26)** analyses `r^T s + E`: rounding errors `r_i` induce coset discrete Gaussians, secret matrices `S_i=mat(s_i)` map those cosets, and crucially **E is an INDEPENDENT flooding Gaussian on a half-integer lattice**, chosen large for smudging and smoothing. The proof invokes generalized convolution/smoothing Lemma 7.3 physical p32 with individual singular-value assumptions. A covariance-only check cannot be substituted for these proof interfaces. **Theorem 7.5 p32** uses original `χ_mlwe` secret distribution and MLWE security, NOT a globally structured NG-pair family.
- **Balonin–Đoković**, *Negaperiodic Golay pairs and Hadamard matrices*, 2015, arXiv **1508.00640**, https://arxiv.org/abs/1508.00640. Defines signed negacyclic correlation and NGP, making `Σ_s=2nI` for the binary two-polynomial pair. Well-known mathematical sequences; no new sequence construction claimed.
- Prior CGS-24/25 rigorously established the fixed-Gram pair and recursive 129-bit **KEYSPACE** only at n32768; CGS-26 rejected literal removal of source padding at unchanged `Bpub`. No original author-paper flaw or novel full ThFHE primitive is asserted.

## Theorem: parity rank-one obstruction [DERIVED]

Let `n≥2` (including n=32768), `R=Z[X]/(X^n+1)`, `a,b∈R` with **every coefficient odd** (in particular binary ±1), and define `H(X)=Σ_(j=0)^(n−1) X^j`.

Modulo2, `a(X)≡b(X)≡H(X)`. In `F_2[X]/(X^n+1)=F_2[X]/(X^n−1)`,

```
X H(X) = H(X) + X^n−1 = H(X)  (mod 2, X^n+1).
```

Therefore `H(X)u(X) = u(1) H(X)` for every `u∈R` after reducing modulo2. In matrix form every column of `mat(a) mod2` and `mat(b) mod2` is the same **all-ones vector** `1_n`:

```
C=[mat(a) | mat(b)]     ∈ Z^{n×2n},
C (mod 2) = 1_n · 1_(2n)^T,
rank_F2(C mod 2) = 1.
```

For ALL integer input vectors `r_1,r_2∈Z^n` the parity of `y=mat(a)r_1+mat(b)r_2` is either `0_n` or `1_n`; no other parity strings occur. Hence the full-rank integer image lattice `Λ=C Z^{2n}⊂ Z^n` is contained in the index-`2^{n−1}` parity-constant sublattice

```
Λ⊂{y∈Z^n: y_i≡y_0 (mod2) for all i};
[Z^n:Λ]≥2^{n−1}.
```

For `U∼U(F_2^n)` the predicate `P(y):=[all n parities equal]` accepts with probability `2^{1−n}`, versus probability **1** on ANY `C r`. Thus the **exact** distinguishing advantage of P for those two parity distributions is `1−2^{1−n}`. This is a mod2 support theorem **regardless of how large the integer Gaussians r_i are**. For a full-lattice broad product discrete Gaussian `D_{Z^n,σ}` with nearly fair parity bits, the target acceptance is approximately `2^{1−n}`, not exactly; do not confuse this approximation with the exact uniform-parity case.

For n32768 the lower bound on parity-index is `2^{32767}`; this is not a claim about ciphertext size or an actual attack when independent E is present.

**Key conceptual distinction:** `C C^T=2nI` and `rank_R(C)=n` (good *continuous* covariance) coexist with `rank_F2(C)=1` (terrible *integer-lattice* surjectivity). Hence **full row real Gram alone cannot imply a full-lattice statistical-Gaussian convolution theorem**.

## One exact numerical gate / checks [EXPERIMENT]

Local code `/mnt/data/cgs27_ngpair_lattice_image_gate.py`, SHA256 `3ed5bbaa29911c1389d0ea32b9365a6ecc5ec63a68fde020483c88ee8dac3d4e`; JSON `/mnt/data/cgs27_ngpair_lattice_image_gate.json`, SHA256 `db4aa2d98dc3c883740b9c36d02cb42aff28875a41e17d779ffbf342a40771e1`.

Found an actual signed ±1 NG pair by **exact autocorrelation** at each n=2,4,8,16. Checked `mat(a)mat(a)^T+mat(b)mat(b)^T=2nI` over integer matrices. Checked each `rank_F2(mat(a))`, `rank_F2(mat(b))`, `rank_F2([mat(a)|mat(b)])` equals 1. Exhaustively tested **all 2^(2n) binary input pairs for n=2,4**; at n8/16 checked zero and each standard input basis spanning the whole mod2 map. For every n, image mod2 has exactly 2 elements. For a product lattice Gaussian with D_Z,4 convention weight `exp(-πx²/4²)`, calculated one-coordinate even-parity probability `0.5000034873423562`; at n16 the parity-constant predicate accepts with probability `~3.0517578303e−5`, compared with 1 for the unflooded NG convolution, a **toy near-maximal discrepancy**. Floating Gaussian truncation/approximation is not the basis of the rank theorem.

## Auxiliary norm-based spectral certificate [DERIVATION; caution]

For n a power of 2, `X^n+1=Φ_(2n)(X)` is cyclotomic irreducible over Q. Any nonzero signed ±1 polynomial a of degree<n has nonzero algebraic integer field norm `|N(a(ζ))|≥1`; pair complementarity implies `|a(ζ_j)|≤sqrt(2n)` at each n negacyclic spectral root. Thus

```
σ_min(mat(a))=min_j |a(ζ_j)| ≥ (2n)^(-(n−1)/2)
```

(and identically for b). At n32768 this uniform **generic** certificate is merely `2^(−262136)`, an astronomically weak bound; it does **not** show actual recursively generated keys reach that minimum, nor that no useful filtered high-entropy family exists. It is insufficient as a realistic source smoothing parameter unless a much sharper construction-dependent estimate is proved. This is a mathematical lower bound, NOT a spectral attack.

## Critical caveat: source flooding fixes the support gap [FACT / DERIVED]

**Do not misreport this as a flaw or distinguisher for Algorithm 7.** Eq(25) is a statement about `r^T s + E` with an **independent flooding** `E`, not the isolated `r^T s`. The E support is a sufficiently wide *half-integer* lattice in source units, and convolution with E can smooth away parity restrictions. In a simpler **integer lattice** toy, adding independent uniform parity bits to each coordinate makes the mod2 output uniform regardless of the original rank-one image. A sufficiently wide independent discrete Gaussian makes parity nearly uniform too. Thus our isolated-mod2 distinguisher does not extend to source's smoothed output without checking the source's actual E and rounding. The full source's Eq25 proof may still be valid even if an alternative joint smoothing proof were found. The point is that one cannot replace the whole smoothing argument by `Σ=2nI` alone.

Neither this obstruction nor the tiny norm-based c bound proves structured-NG MLWE secret *insecurity*. The user seeks efficient secure threshold FHE, not a generic unpadded convolution toy. Prior CGS-23–26 leave native key distribution + FHE evaluation security unproved, with no actual standard-MLWE reduction, and the cheap 128-bit minimum support occurs only at n32768. This branch currently lacks a competitive complete construction.

## Constructive-synthesis gate and disposition

Positive components: explicit native k2 covariance-flat NG secret family; known support ≈2^129 at n32768; original Eq25 without extra ζ has public **covariance** if a modified KeyGen and simulator could be proved.

Missing necessary components: source-compatible (M)LWE hardness for recursively globally correlated secrets, a **usable individual σmin** certificate or a new rigorous flooded convolution lemma sensitive to image lattices, adaptive multi-sid decryption transcript simulation, FHE evaluation keys/security, and cost relative to original `O(LDec)`. The mod2 image theorem demonstrates why **a real Gram-only shortcut is insufficient**, but does NOT rule out the existing high-`σflood` route. Additional generic NGP identities without closing these interfaces are unlikely to make progress.

**Recommendation:** **PARK the covariance/NGP secret-replacement subbranch now**, retaining it as documented speculative math, not a publishable ThFHE candidate. Keep parent CGS conditioning/open question active. Next iteration should return to a SINGLE new, source-respecting conditional-Gaussian sampler or alternate source-compatible tradeoff, not another small-family Golay enumeration.

## End-of-iteration

- **ITERATION:** CGS-27.
- **PRIMARY HYPOTHESIS:** fixed Gram plus stacked real singular value alone suffices to infer full-lattice discrete Gaussian for **unflooded** NG rounding convolution, bypassing independent smoothing requirements.
- **STATUS:** **FAIL** that direct inference; **PASS** exact parity rank theorem, spectral general-certificate bound, executed toy; **UNCLEAR** any redesigned fully flooded no-pad structured-key protocol; **HUMAN_REVIEW/PARK recommended** for NG secret branch. Parent CGS O(LDec) OPEN.
- **RESULT:** for all dense ±1 keys, `rank_F2 C=1`, output lattice index≥2^(n−1), uniform-parity distinguisher 1−2^(1−n) **when independent E is excluded**. Full source E may erase it. Generic norm-based individual σmin certificate ~2^−262136 at n32768 offers no usable security/smoothing guarantee.
- **NEXT_TEST CGS-28 (only with PI next "继续"):** Return to ORIGINAL source's already-existing standard-LWE/MLWE secret distribution. Choose one concrete **external-secret-linked reusable correlation / covariance-hiding mechanism** (not simply plain PRSS/PCF ports previously failed), define the complete source adversarial observable transcript, and run the single cheapest simulator/privacy or cost falsifier. If no viable new primitive, recommend PI pivot/stop rather than endlessly accumulating conditional lemmas.
- **STATE_UPDATE:** YES, CGS technical state + root one-active-task STATE + this finding only.
