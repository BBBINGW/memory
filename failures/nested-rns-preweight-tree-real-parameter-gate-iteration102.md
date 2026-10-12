# Iteration 102 — I101 small-target preweight factoring fails the author's actual nested-RNS parameter gate

Date: 2026-10-12. Active FHE paper Boneh–Kim, *Homomorphic Encryption for Large Integers from Nested Residue Number Systems*, IACR ePrint 2025/346.

STATUS: **FAIL** practical applicability of the I101 **small-centered-CRT-weight sufficient condition** to the pinned nested.go experiment (l=512). **PASS** exact faithful parameter reconstruction and cross-target coefficient witness. Not a no-go for all factorization/rotation optimizations; no new paper correctness flaw, cryptographic security issue, or novelty.

## One hypothesis and cheapest falsifier
Hypothesis: The real experiment uses first-layer moduli p_i and second-layer target r_j satisfying `max_i |center_{r_j}(P/p_i)| < min_i p_i/2`, so the I101 proof allows factorizing target-block-dependent CRT weights into a single SMALL source vector, followed by log2k CKKS rotations. Falsifier: one genuine source setting with a nonuniform source/target CRT-weight table or gross violation of that bound.

## Primary source provenance [FACT]
1. Read live GitHub Notes `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, `STATE.md` (last iteration 101), I101 finding; read IACR ePrint 2025/346 Research MCP primary mirror physical pp25–27 and §3.3 pp15–17 from prior session. PDF: 31 physical pages, SHA256 `7a26e911b00368dace336f4324e8e3f036927a57683cf5fbea1e26ee19777ef5`; source `github-mirror`, original/latest `VERSION_UNVERIFIED`.
2. Paper §6.1 physical p25 Table4: first-layer log(p)≈6 bits, k=16, reported log2(∏p_i)=77.1, second-layer log(r_j)≈15 bits, l=64 *in Table4*, with later experiments varying l to 512 (Table6 p26). Section6 p25 expressly says the implementation uses **unsigned** representatives for Z_m rather than paper's centered representatives. Hence I101 abstract centered lemma is NOT automatically an exact model of Go implementation.
3. Author public GitHub source https://github.com/jaehyungkim0/CRT-FHE pinned HEAD/master commit `a763be8433a71eac7ec93aeadc5b0633871462a1` (2025-06-04). README points to `examples/singleparty/ckks_bootstrapping/slim/nested.go` as main nested CRT experiment. File blob SHA `06009c01637c91d77d7f1f134d546a8f8a31a809`.
   - Lines76–91 `firstKPrimes(k)`, lines95–143 `findClosestPrimes(n,k)` primes near 2^n, lines146–156 `Moduli(n,k)`: start at first k primes, raise each to its *largest prime power ≤n*.
   - `main()` lines~706–720: `n:=64;k:=16;l:=512; mods:=Moduli(uint64(n-2), uint64(k)); primelist:=findClosestPrimes(15,l)`. This pinned Go experiment is the author's *l512* configuration, not necessarily the paper's Table4 l64 baseline.
   - Lines210–224 `HatMod(mods,prime)` computes each `(P/p_j) mod r` in nonnegative representatives with big.Int arithmetic. Lines750–761 construct `hatmod_r[i]=HatMod(mods,primelist[i])`. The `Reduce` closure lines1006–1020 explicitly uses source/target weight `tmp:=hatmod[j%l][jdx] % mods[(jdx+k-i)%k]` and k plaintext-vector multiplications + rotations. All weights are **unsigned**.
4. The existing source p25 Table4 77.1-bit first CRT product is an external consistency check of the reconstructed product below.

## Exact reconstruction and numerical falsification [DERIVED/TEST]
Python port of the pinned Go generator's specific functions, not a cryptographic runtime:
- k=16 first-layer ordered pairwise-coprime `mods = (32,27,25,49,11,13,17,19,23,29,31,37,41,43,47,53)`.
- `P=164249358725037825439200`, `log2(P)=77.12023392028715`, in agreement with paper Table4 77.1 bits.
- `min_i p_i=11`, thus I101 requires `max_j |w_j| < 5.5`.
- First selected target from `findClosestPrimes(15,512)`: **r_0=32771**.
- `w_j=center_{32771}(P/p_j)` for j=0..15:
  `(5945,-2664,-12053,11908,8357,12113,15046,15187,2572,6560,-206,-1944,4640,9759,15901,8536)`.
- `max_j|w_j|=15901`, compared against 5.5, violating the strict condition by a factor **15901/5.5≈2891.09**. Even the smallest nonzero coefficient magnitude (|−206|) exceeds 5.5.
- Original Go unsigned residues `w_j^{unsigned}=(5945,30107,20718,11908,8357,12113,15046,15187,2572,6560,32565,30827,4640,9759,15901,8536)`, also much larger than `min p_i=11` so the even stricter *unsigned* common-coefficient condition fails.
- Concrete **cross-target witness** from source j=0: `(P/p_0) mod r_0 = 5945`. Its actual Go line1010 target weights are `5945 mod 32=25` and `5945 mod 27=5`. Therefore NO common *small* literal integer weight in the original coefficient ranges reproduces the SOURCE-IDENTICAL weighted intermediates across those target blocks. Centered versions are −7 and +5, also different.
- Tested ALL 512 targets of this same pinned experiment as one source-setting gate, not 512 different hypotheses: `r_j` range 30133..35401, and min/max of their `max_i|center_{r_j}(P/p_i)|` are 9795..17523; **0 of 512** satisfy `2 max|w|<11`. Count is only about the I101 sufficient bound, not general homomorphic impossibility.

## Critical scope and potential error traps
[FACT] Paper's centered `[a]_m` and author's Go experiment's UNSIGNED residue choice are not equivalent intermediate integer representations; any derived noise/precision guarantee must track the actual choice.
[DERIVATION] The special-case *source-integer identity* established in I101 does not apply here: `[[P/p_j]_{r}]_{p_d}` depends on target d in the tested code, and is not the same small weight across all d.
[NOT A GENERAL NO-GO] Even when the gate fails, the mathematical full integer `w_j=(P/p_j) mod r` could hypothetically be preweighted **without** target reduction, and after final componentwise Mod_p produce the same residues, provided the MUCH LARGER CKKS intermediate amplitude/noise can be tolerated; no precision bound or performance proof was carried out. Alternative matrix factorization, baby-step giant-step, hoisting, linear-transform scheduling also untested.
[NO IMPLEMENTATION BENCHMARK] Did NOT execute Lattigo/Go or CKKS, and cannot claim original timings improve or degrade, or assert an author bug. The first-layer tiny moduli vs 15-bit r_j suggest potential precision obstruction to an unbounded lift, but it remains speculation. This is a **kill of one narrow practical parameter regime**, not proof that every one-preweight scheme is impossible.
[ORIGINALITY] Standard rotate-and-add is already in paper Algorithm3 lines4–6 and established CKKS linear-transform methods. No novelty claim.

## Reproducibility
Exact Python: `/mnt/data/iteration102_nested_rns_actual_parameter_gate.py`, SHA256 `8683ed4d6a337d06033ff1a37163749f7a9df541e2095350376dc039368668c3`.
JSON: `/mnt/data/iteration102_nested_rns_actual_parameter_gate_results.json`, SHA256 `5f6548e0aa2e410512e97cfd2a805d81b1a929d476a5db2b4fb9664183d29b9e`.
Script reconstructs source n62,k16,l512 and checks pairwise coprime p_i, primality of 512 r_j, exact big integers, finite-source weight nonuniformity. Independent source consistency with paper Table4 first product log77.1.

## End of iteration
STATUS: **FAIL** (I101 small-target real parameter gate); **PASS** (source-pinned actual coefficient witness and 0/512 parameter test); **HUMAN_REVIEW** if further constrained exploration is appropriate.
RESULT: Actual author modulus vector p_i has min=11, and first r0=32771 yields max|center((P/p_i)mod r0)|=15901, ~2891× larger than admissible 5.5. The source explicitly uses unsigned moduli, so previous centered-to-code transposition needs care. This kills the direct small-weight integer-exact factorization as a plausible drop-in technique in the author's published tested setting, NOT every possible rotation optimization.
NEXT_ACTION: PI selects (A) ONE very narrowly scoped large-weight preweight-vs-destination-reduced CKKS error/magnitude analysis for source r0=32771, p_i list above, with a decisive noise/precision budget, or (B, recommended) PARK this parameter-inapplicable standard rotate-and-add branch and pick another independent source-grounded FHE gap. Do not autonomously launch another proposal without PI selection.
STATE_UPDATE: YES. Original vFHE audit retained; PaCo and RIG historical states remain parked. No author contact/email/outreach/public disclosure.
