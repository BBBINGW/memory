# BOOT B031 — Source-driven incomplete-NTT automorphism-keyset audit: full dynamic reachability, free identities and hybrid key-memory repair

TRACK_ID: BOOT
ITERATION: B031
DATE: 2026-10-19
STATUS: FAIL_STATIC_SUBGROUP_ONLY_KEY_PRUNING / PASS_FREE_IDENTITY_BYPASS / PASS_ALGEBRAIC_HYBRID_KEYSET_TRADEOFF / NO_PUBLISHABLE_NEW_PRIMITIVE_YET
STATE_UPDATE: YES

## PI scope and one falsifiable primary hypothesis
The PI explicitly approved a conditional methodological pivot **within ordinary FHE BOOTSTRAPPING research** after long B001–B030 original-paper-inspired construction attempts, to a source-grounded search for hidden limitations, correctness/security traps, inefficient operations, and substantial end-to-end repairs. NOT a shift to ZK, VFHE, SHIP, etc.
Choose one paper with FULL title-verified PDF and public code: Paiva–De Micheli–Hafiz–Simplicio Jr.–Yildiz, "Faster amortized bootstrapping using the incomplete NTT for free," ePrint 2025/696, TCHES2025/4, and authors' https://github.com/thalespaiva/incomplete_ntt_amortized_bt .
PRIMARY HYPOTHESIS: The two-part incomplete inverse NTT calls automorphisms only on a small fixed group of twiddle ratios, so a **direct subset of the FULL automorphism keyset**, with NO extra key switching, may support arbitrary PBS inputs. This would cut evaluation-key bytes and preserve online noise/runtime. Cheapest falsification: from source matrix construction, derive the actually generated keys in the INPUT-DEPENDENT first half and INPUT-INDEPENDENT second half; exhibit arbitrary reachable generator for a legitimate public mask, or count all used generators. Repair search after falsification: identity fast path, and a reduced-generator keyset time/memory strategy, costed and novelty-gated.

## Exact source provenance, what was actually inspected
[FACT] ePrint 2025/696 title-verified research-MCP mirror PDF, 24 physical pages, SHA256 100140416417ad19daf56cc556713ce29d30c68780a9009d7d6234d36f68f85a, VERSION_UNVERIFIED. Source is GitHub ePrint mirror artifact revision 9e3c7187693fe7e51fd0e1ee969d32bb8a047773, not a certified original published version. Physical pp11–15 Section4 defines ℓ-incomplete NTT, two-part inverse INTT, linear-algebra embedding of base multiplication in first half; p18–20 Section5 and Table2 use examples N=1024, p=7681, alpha=6, incomplete level ell<=4, and acknowledge automorphism key memory cost. Also reviewed current related 2025/2214 sorted TFHE and 2026 BatchBoot in preliminary prior-art discovery, but neither source determines this focused test.
[FACT] Direct author GitHub file blob SHAs (individual files from default branch; the WHOLE REPOSITORY commit is NOT pinned):
* src/amortized_bootstrap_general.cpp blob 0368714b416df3c342e2dc8421bfc18e891f6ffe
  - lines24–30 #ifdef USE_DECOMP_AUTOMORPHISM provides decomposed key option; default macros always use aut_ksk[GEN].
  - lines56–109 rns_gsw_dot_product enumerates nonzero plaintext coefficients, computes each modular inverse, and makes first automorphism with ratio a_first/a_second, then consecutive a_j/a_(j+1), final a_last/1, through MACRO_hgsw_automorphism. NO gen==1 skipping in macro.
  - lines113–160 rnsc_rlwe_dot_product similarly applies first 1/a_first and consecutive ratios; full generic group may also occur here.
  - lines163–191 get_middle_intt_matrix_column and get_part2_intt_matrix_column: the former is the first PART, mixed with input a_hat; the latter fixed.
  - lines220–280 intt_negacyclic_part1_quadratic builds first matrix, then public base-multiplication coefficients in_const derived from INPUT LWE mask, and calls rns_gsw_dot_product for each row. For incomplete block dimension 2^ell, the first block with row0=64 at column0 yields the full 2^ell-length cyclic base multiplication. lines290–324 part2 depends ONLY on fixed transformation coefficients. lines454–465 modulus switches public input mask from Q2 to p and applies incomplete NTT; lines484–486 generate all automorphism keys via rlwe_new_RNS_automorphism_keyset.
* src/rlwe.cpp blob 2ec73abdfa64f4254730ce5478b6d3f3968684a3:
  - lines468–475 rlwe_automorphism_RNSc ALWAYS allocates tmp, permutes polynomial and calls rlwe_RNSc_keyswitch, even for gen==1, then frees tmp. No early-return.
  - lines612–623 rlwe_new_RNS_automorphism_keyset allocates Q pointer array and generates fresh KS key for every 1<=gen<Q; Q here is cyclic ring degree p, not the large RNS ciphertext modulus. At p=7681 this stores 7680 keys INCLUDING an unneeded key for gen1.
  - lines626–636 ALREADY contain decomposed automorphism keyset using O(log p) generator powers, and src/amortized_bootstrap_general.cpp has a macro for optional decomposed use. This is fundamental prior art in the SAME repository.
* src/gsw.cpp blob [inspected via GitHub fetch this turn; extract exact SHA before software patch], lines262–267 gsw_automorphism_RNSc_half_gsw applies rlwe_automorphism_RNSc once for each half-GSW limb l. Skipping identity at GSW level must be an in-place no-op (or copy if out!=in), not skip the preceding required GSW multiplication.
* src/forward_ntt.cpp blob 1bcb6ea869c3d941d21a8d6c4c34af72b05da5c1, lines109–147 and160–207: source’s incomplete forward/inverse butterfly layers; they are invertible over F_p for odd p and unit roots (determinants ±2*phi).
[FACT] Authors' README documents exact CLI parameters, stored benchmarks, and GitHub repo publication; actual code is available, NOT executed on native C++ CPU host in B031. Dynamic output from author's compiled program and physical byte sizes not benchmarked.
[KNOWN PRIOR ART] BSGS is classical group arithmetic. Poulpy currently describes baby-step/giant-step automorphism-key schedules and free identity rotations in its public docs https://github.com/poulpy-fhe/poulpy/blob/main/docs/linear_transformation.md ; the schemes/linear-transform workloads DIFFER, so this is conceptual prior art not identical source-algorithm code. Original GPVL 2023 already discusses GSW automorphisms and variable time/space; no claim that B031 BSGS is cryptographically novel.

## Exact falsifier: first-half mask-dependent ratios reach all p−1 generators
Focus on ACTUAL example p=7681 prime, N=1024, incomplete ell=4, split alpha=6. Since (2N)>>ell=128 divides p−1=7680, choose any primitive 128th root; source-compatible example root omega128=202 mod p.

Port to exact Python integers the source's:
 get_middle_intt_matrix_column(j)
 = nc_ntt_forward_leveled(
       nc_ntt_inverse_leveled(e_j, ell=4),
       incompleteness=log2(N)-alpha=4).
Use the SAME inverse butterfly ordering and lack of 1/2 normalization as forward_ntt.cpp. For first row, first base-multiplication 16-column block, exact result:
 M_A[0,0:16] = (64,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0) over F_7681.
The get_twiddles_for_basemul code's first block produces nonzero omega=202 for the chosen primitive root. Its public base-multiplication forms for first two output coefficients:
  c_0=64*u_0
  c_1=64*omega*u_15
if all other a_hat/input coefficients in that block are zero. Since the public incomplete NTT is invertible, arbitrary target u_0,u_15 can be reached by suitable public incoming coefficient mask (assuming standard full-support input mask modulus switched onto p). Choosing u_0=g*omega, u_15=1 for arbitrary nonzero g∈F_p makes c_0/c_1=g, exactly the first ratio passed as automorphism GEN in rns_gsw_dot_product lines94–98.
EXHAUSTIVE group enumeration: for ALL g=1..7680, compute these two coefficients and their ratio modulo7681, obtains all 7680 distinct nonzero generators; no zero denominator or mismatches. Thus direct one-step group-automorphism keyset CANNOT be pruned down to fixed INTT twiddles while accepting all publicly possible LWE masks, under the SAME input representation. The paper's fixed second-half matrix cannot justify pruning keys needed by variable first-half input.
[CONDITIONALITY] The proof is for algebraically full public mask support modulo p. Source array_mod_switch from larger Q2 to p and invertible incomplete NTT support this for the intended uniform-mask domain; an unusual artificially restricted set of input ciphertexts might not. This does NOT prove every private key leaks or every key is security-necessary; it proves the simple universal one-key-switch direct-subset implementation is algebraically inadequate.

## POSITIVE source implementation repair: free identity automorphisms
[DERIVATION] Ring automorphism ψ_g maps X↦X^g in cyclic ring F_q[X]/(X^p−1). For g=1, ψ_1=identity. The ciphertext is already under the desired original ring secret, so running an extra RLWE key switch to the SAME ring secret is mathematically unnecessary in the ordinary correctness/IND-CPA bootstrapping interface and adds fresh key-switching noise. In-place bypass if g==1 returns without action; out!=in copy input ciphertext; do not suppress any preceding ciphertext product.
[EXACT SOURCE MATRIX COUNT] Construct all 1024 rows of part2 INTT matrix via source-identical inverse butterfly, modulus p7681, N1024, ell4, alpha6. Every row has 64 nonzero coefficients, hence 1024*64=65,536 source calls to GSW automorphism from rns_gsw_dot_product, before any other operations. Compute exact GEN for each adjacent nonzero pair and final last-to-one ratio, counting histogram:
  generators used =96 distinct values, ALL lie in 128th-root subgroup, 1 is present.
  calls with GEN=1:21,856 /65,536 =33.35%.
  calls with GEN=-1 modp=7680:21,840 (NOT safe to bypass, generally changes ciphertext secret).
  calls with other generators:21,840.
At real RNS half-GSW level l=3, the identity case invokes rlwe_automorphism_RNSc l times per high-level operation in source, thus nom. 65,568 redundant RLWE automorphism-key-switch invocations in part2 alone per complete transformation, before considering other code paths. This is an OPERATION COUNT, NOT measured time savings, full-batch acceleration, or source security bug. Do not call dropping GEN=-1 safe: ψ_-1 transforms secret and requires switching without an alternative invariant.
[FAST PATH CODE INTENT]
if (gen == 1) {
    if (out != in) copy_entire_RNSc_half_GSW(out,in);
    return;
}
gsw_automorphism_RNSc_half_gsw(out,in,gen,ksk);
Must use the repo's correct copy APIs and aliasing rules; no native patch attempted. Need check whether downstream circuit-privacy/nontrivial randomized evaluation requirements mandate extra re-randomization, although source bootstrapping does not present such as prerequisite.
[REPEATED USE] Part2 matrix is fixed across bootstrapping instances; its inverse coefficients and GEN ratios can also be precomputed instead of calling InverseMod at runtime. This may be engineering optimization, not a cryptographic invention. Do not expand this B031 hypothesis into multiple unrelated tests.

## Nontrivial repair after failed subset prune: hybrid fixed-hot key + 2-step decomposition
[DERIVATION] Multiplicative F_p^* cyclic group order 7680, generator g0=17 confirmed primitive. For any requested generator u=g0^e, 0<=e<7680, choose split base m=ceil(sqrt(7680))=88, e=a+88b, 0<=a<88, 0<=b<=87. Then automorphism ψ_u=ψ_(g0^a)○ψ_(g0^(88b)) and a single automorphism's message effect is exactly correct after TWO key-switched automorphisms (each bound to original ring key). Precompute nontrivial baby keys g0^1..g0^87 (87) and giant keys g0^88,..,g0^(88*87) (87): total174 compared to7680 direct keys (44.14x fewer keys, disregarding per-key variable sizing). Verified ALL 7680 field-group elements by exact modular exponentiation: 7680/7680 group factorization PASS, algebraic ciphertext correctness of automorphism composition follows ψ_u ψ_v=ψ_uv.
On uniformly random u over F_p^*, number of nontrivial switched factors is average 1.9770833 (one or two vs baseline1, with u1 zero); actual dynamic GEN distribution not assumed uniform, and GSW/RNS noise can increase by two KS calls and their correlations; NO native noise/DFR proof.
HOT-HYBRID: Keep first-stage 174 BSGS keys and ALSO direct keys for every non-identity part2-used generator (95). Exact sets overlap5, so keyset union needs264 distinct keys; p7681 full set7680 => 29.09x reduction of AUTO-KS key count, while retaining SINGLE-step automorphism for all part2 non-identity calls (43,680) and eliminating part2 identities (21,856). Variable first-half dynamic GEN would require one or two sequential KS, instead of one, and need precompute public discrete-log exponent lookup 7681 slots. An actual hybrid must prove correct for GSW half-accumulators, and noise/precision/security+memory vs latency/CRT cost, rather than just pointwise automorphism exponent group identity. RAM SAVING is only a KEYSET COMPONENT, NOT 29x full bootstrapping memory.
IMPORTANT NOVELTY FILTER: The repository itself already implements/declaratively supports a log-sized decomposed automorphism alternative, and known BSGS/rotation-cache ideas and free identity skips are textbook. Hybrid is a mathematically valid Pareto example but no novel BOOT algorithm or speedup / DFR claim yet. It could have a RAM-constrained practical engineering use if native profiling shows an unaddressed regime; absent evidence, DO NOT label publishable.

## Exact reproduction recipe
1. Source parameters p=7681,N=1024,ell=4,alpha=6, root128=202; reconstruct source bit-reversal butterfly NTT matrix from source forwards and inverses over F_p, no floating point.
2. For part1 row0 apply inverse incomplete NTT then forward leveled at incompleteness4 to unit columns 0..15; verify M[0,0:16]=(64,0,...,0). Extract first base-mul omega=202 from get_twiddles_for_basemul and verify c0/c1 sweeps exactly 1..7680.
3. For part2 matrix apply source inverse incomplete NTT to 1024 identity basis vectors (NumPy signed 64-bit safe for arithmetic with p7681), extract nonzero entries for each of 1024 rows; for each row compute first nonzero/next, next/next, ... and last/1; count 65536, GEN1 21856, GEN(-1)21840, unique gens96 all satisfy gen^128=1 mod7681.
4. Primitive generator17 checked via factors of p−1 (2,3,5); enumerate exponent table g0^e,e=0..7679, verify BSGS e=a+88b; set union of baby, giant and fixed-hot gens has size264.
All arithmetic deterministic exact small-field/large-parameter *linear-transform layer*, NOT real fully encrypted CPU execution, no actual bootstrapping noise/DFR/security or latency benchmark in this iteration.
CHECKS: PART1 7680/7680 generators reachable; PART2 65536 calls exact; BSGS 7680/7680 factorization.

## End-of-iteration judgment, primary hypothesis versus repair
STATUS: FAIL_STATIC_GALOIS_KEY_PRUNING / PASS_FREE_IDENTITY_AUTOMORPHISM / PASS_CONDITIONAL_HYBRID_264KEY_TRADEOFF / LOW_PAPER_NOVELTY.
PRIMARY RESULT: First-stage public mask support makes all automorphism generators necessary if one wants direct one-switch-one-generator evaluation; fixed twiddle-only subset is not sound for unrestricted inputs. But source has tangible redundant identity keyswitching (~33.35% of part2 auto calls) and a known-group-based key memory/online noise-time Pareto option. This exemplifies PI's source-first repair methodology, NOT a successful new FHE bootstrapping paper.
NO BUG CLAIM AGAINST PUBLISHED SCHEME: The original authors' algorithm is correct in principle; our identity finding is redundant work in current implementation, not a correctness/security flaw, and decomposed automorphism already exists in their code. Version unverified original paper, no native binary runtime measurements.
NOVELTY: Primitive generator decomposition and no-op identity are existing concepts. No verified end-to-end new protocol, asymptotic improvement beyond prior art, DFR/KS key noise analysis, or hardware speedup. Do not claim publication contribution.
NEXT_TEST B032: Continue PROBLEM-FIRST BOOT source audit. Before investing in this 2025/696 hybrid, perform a minimal genuine author-code native benchmark of identity skip (if compatible environment) and compare automation of group generator hot frequency / available decomposed-automorphism keyset; decide whether it has a meaningful unique cost frontier or is only standard engineering. Alternatively target a distinct full-source newer bootstrapping paper such as ePrint 2025/2214 sorted PBS or ASIACRYPT25 dense-key automorphism traversal if both PDF and implementation can be verified. Select one PRIMARY new bottleneck/repair test; do not keep adjusting BSGS width without evidence. PI retains direction decision. B032 NOT STARTED. BOOT-only files.
STATE_UPDATE YES.

## Source SHA follow-up verification
[FACT] src/gsw.cpp Git blob SHA-1 = 7eac24cf2eff32661c1fde6a8f7cae6dfd95da63 (default branch fetched in this iteration). Its gsw_automorphism_RNSc_half_gsw lines262–267 invokes rlwe_automorphism_RNSc for every half-GSW RNS level. This resolves the pending source-hash placeholder above; no native source-code patch was attempted.
