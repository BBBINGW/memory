# Iteration 100 — Removing CRT weights in Boneh–Kim Algorithm 3 breaks lazy base conversion

Date: 2026-10-12. Active source Boneh–Kim, *Homomorphic Encryption for Large Integers from Nested Residue Number Systems*, ePrint 2025/346, 31-physical-page Research MCP GitHub mirror PDF SHA256 `7a26e911b00368dace336f4324e8e3f036927a57683cf5fbea1e26ee19777ef5`; latest official VERSION_UNVERIFIED.

STATUS: **FAIL** optimization claim "remove all p_i-specific source CRT weights before inner-rotation aggregation"; **PASS** a source-consistent exact CRT algebra test. NOT a flaw/attack on the published Boneh–Kim method. No novelty claimed.

## ONE primary hypothesis / smallest decisive falsifier
HYPOTHESIS: In Algorithm 3 `IMod_r`, once input CRT residues `y_i` have been computed and inner rotations collect slots, the plaintext diagonal weights `[[P/p_i]_r]_{p_{j-i}}` in line 9 are redundant; replace by 1 and retain correction `v [P]_r` and the final `Mod_p`.
FALSIFIER: small centered CRT x with correct weighted output congruent x mod r, but unweighted inner-rotation aggregate not congruent x mod r, even after final `Mod_p`.

## Source FACT / assumptions
Primary §2 p7: `Z_t` is identified with centered integer representatives `[-t/2,t/2)` (not all-nonnegative CRT representatives).
Primary §3.3 physical p15 Theorem 2: `P=∏p_i`, `hatp_i=P/p_i`, `y_i=[[x]_{p_i}hatp_i^{-1}]_{p_i}`, `v=nearest_integer(Σ_i y_i/p_i)`, and exact original centered `x=Σ_i y_i hatp_i-vP` for |x|<P/2. Lazy base-conversion computes `x'=Σ_i y_i [hatp_i]_r -v[P]_r = [x]_r + r e` for some integer e; **x' need NOT be canonical [x]_r**.
Primary §3.3 physical p16 Algorithm 3 lines8–14 uses k inner rotations, `cty` multiplied by source/target CRT-weight arrays depending on j,i, subtracts `v[P]_r` and finally `Mod_p`. Thus *author already explicitly preserves the weights*; testing necessity is a test of a proposed optimization, not uncovering an author omission.
Primary §3.3 physical p17 Theorem 3: approximate CKKS correctness needs message |x| `≪ min_i hatp_i`. With tiny p_i=(5,7), even x=2 is not rigorously asymptotically in `≪` regime; results here are ONLY exact integer/CRT skeleton, NOT proof of approximate homomorphic realization.

## One decisive two-prime counterexample [DERIVATION]
Let (p0,p1)=(5,7), P=35, target r=3 (coprime to P, 3<√35), x=2.
- `hatp=(7,5)`, inverses modulo (5,7) respectively (3,3), so centered `y=(1,-1)`.
- `Σy_i/p_i=1/5−1/7=2/35` so `v=0`.
- **Centered** weights `([hatp0]_3,[hatp1]_3)=(1,-1)`. Weighted input `(1,-1)⊙(1,-1)=(1,1)`. For k=2, line8–12 sums identity and one circular inner rotation, giving slots (2,2). Subtract `v[P]_r=0`; last `Mod_p` leaves `(2 mod5,2 mod7)`, CRT decode centered 2. This obeys 2≡x (mod3); source's lazy output 2 equals [2]_3 +3, with [2]_3=-1, e=1.
- Removing only weights gives `(1,-1)+(-1,1)=(0,0)`; after same subtraction and `Mod_p`, CRT gives 0, **not** congruent x=2 modulo3.
This rules out deleting line9's prime-specific factors while otherwise retaining the algorithm, not alternative genuinely different circuits.

## Explicit role of v [CHECK of SAME source identity, no second hypothesis]
For x=6 (outside theorem3 smallness), centered y=(-2,-3), sum y/pi=-29/35, v=-1. Weighted sum `(-2)*1+(-3)*(-1)=1`, while `[P]_3=[35]_3=-1`, so subtracting `v[P]_3=(-1)*(-1)=1` yields 0, congruent 6 modulo3. Without that correction output 1, which is wrong. Auxiliary illustrates why source keeps the correction; **not** an additional claimed optimization test and not validation of security/precision.

## Exhaustive arithmetic [TEST]
Evaluated each of the 35 unique centered messages x∈[-17,17] exactly with Python `fractions.Fraction`, modular inversion, nearest rational rounding, both k=2 rotations modeled as pairwise source-weight sum, final reduction componentwise by p_i, AND centered CRT reassembly into Z_P.
- Correct source-style weighted CRT skeleton: **35/35** outputs congruent to x modulo r.
- Delete source weights while keeping v correction: **20/35** outputs NOT congruent to x mod r, including x=2. 15/35 pass incidentally.
- Initial test incorrectly compared nonnegative CRT x∈[0,P) to centered x (a representation mismatch), caught by assertions and fixed to compare centered Z_P representatives. Never infer an algorithm flaw from this mismatch.
- No actual encrypted CKKS operations, noise, lazy-reduction error size on realistic moduli, or implementation throughput estimated.
Script verified active path `/mnt/data/iteration100_nested_rns_weighted_baseconv.py`, SHA256 `7bf68ebeee7c4b49b90b92d4b2dda0adb2a20c39e2ca74ddccfa27cf14748e11`. JSON `/mnt/data/iteration100_nested_rns_weighted_baseconv_results.json`, SHA256 `75e89b5e07f446a88c8270abd11ad828071a7a7fb64fd3a66ba6239a02fe9e93`.

## Implication and limits
[FAIL] A drop-in CKKS rotation-only base-conversion shortcut ignoring `[hatp_i]_r` cannot correctly implement arithmetic for arbitrary CRT inputs. Authors are already following correct weighted HPS-style conversion. No novel repair or attack.
[IDEA / NOT YET TESTED] More interesting narrower hypothesis: **under a sufficiently small target r so that all `[hatp_i]_r` have a common small integer representation across all source/target p_j**, could ONE pre-weighting plus logarithmic tree rotations substitute Algorithm 3's k separately weighted rotations? Check whether source's target-dependent modulo coefficients can be factored before rotation without precision overflow and whether BSGS/log rotations are prior art. Neither equality under realistic parameters nor meaningful concrete saving has been established.

## End
STATUS: **FAIL** weight-deletion optimization; **PASS** counterexample and full centered small-ring exhaustive exact test.
RESULT: Source's p_i-specific CRT weights are algebraically necessary to compute `[x]_r + re` in general; x=2 yields correct 2 versus unweighted 0. Original algorithm not challenged.
NEXT_ACTION (I101): ONE toy-level equivalent-transform and feasibility test: under explicit bound `max_i|[hatp_i]_r|<min_j p_j/2`, can weighted inner rotations in Algorithm3 be replaced by pre-weight once and binary rotation-sum, without additional `Mod_p` and without changing ciphertext-slot integer output? Check an explicit k=4 CRT array and paper's centered coefficient indexing, then count baseline k rotations vs log2(k); if source/prescribed plaintext modulus makes bound unusable or prior art covers it, kill it. No performance/novelty claim before proof.
STATE_UPDATE: YES. No author contact/email/outreach or public disclosure.
