# SHIP-I237 — Automorphism-fixed subring rank-2 affine mux: HW/entropy fatal obstruction

2026-10-15. PI-selected active SHIP HMux key-memory branch. This is a FAIL for the proposed *new variant*, NOT an attack on original SHIP. One hypothesis, one decisive exact combinatorial test. We read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, STATE.md, ship-memory-STATE.md and I236 before writing.

## Primary hypothesis H237 / falsification condition

**H237**: The affine onehot fused delta MuxRot of I236 can use a rank-2 rather than rank-3 GGLWE per nonidentity candidate if the encryption secret is fixed by all relevant public Galois rotations. This must also remain compatible with source-shaped **N=16384, dense ternary HW192**, and a plausible >=128bit secret entropy, so that its lower prepared bytes and online VMPs are a legitimate optimization. **Falsify** if even a single mandatory nonidentity rotation's fixed ternary subring cannot contain an HW192 secret or has negligible entropy.

**One cheapest decisive test:** Compute the full-degree signed-monomial Galois orbits for the first group rotation g=5^4 modulo 2N, count allowed ternary coefficient positions, check HW192, then perform only a small exact noiseless RLWE/GGLWE conditional-correctness toy and full-source-shape cost arithmetic. No speculative other variants, no Rust project infrastructure, no false security proof.

## Primary source and provenance

Original Cheon–Hanrot–Kim–Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, EUROCRYPT2025 / IACR ePrint **2025/784**, §4.2, §5.1 Algorithm5 physical pp23–24. Research MCP cached 33pp GitHub PDF mirror SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, VERSION_UNVERIFIED. SHIP original uses X↦X^{5^j} rotation automorphisms.

Independent **third-party** (not authors' HEaaN) pinned `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`:
- `poulpy-ckks/src/layouts/ship/plan.rs` blob `364f4235253a3c76c70dfacf3ea24c5e69a2c3c2`: `theta=4`, mixed radix [4,4,4,3] in the source-shaped illustrative plan; first group nonzero rotation 4.
- `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`: `gal_el=module.galois_element((m-rot)%m)`, source inverse rotation convention, generated `rot=d*weight`; requiring invariant under 5^{-4} is equivalent to invariant under 5^4.
- `poulpy-ckks/src/test_suite/ship.rs` blob `a5e89638c430886e57c036e001093827293bfae0`: fixed ternary generator `glwe_secret_fill_ternary_hw(params.hw)` for dense secret; current illustrative test-suite/source-shape HW192.
- `poulpy-core/src/layouts/prepared/gglwe.rs` blob `80a0d5e63df624cac01a70071da71f735b0b0b61`: prepared PMAT uses N*dnum*rank_in*(rank_out+1)*size*16 bytes in IFMA, N16384 dnum9 size10.
- Prior I236 failure `failures/ship-memory-I236-fused-affine-rank3-keysize-gate.md`: rank3 affine MuxRot mathematically works but online and memory worse.
- Related automorphism-invariant subring method exists for a *different ring/encoding setting*: Hwang–Min–Song *Carousel*, ASIACRYPT2025, ePrint2024/2032. Generic subring/weak-secret concerns precede this candidate. Neither is a novelty claim for a secure SHIP scheme.

## Constructive rank-2 conditional algorithm [DERIVATION]

Use `Dec_s(a,b)=b+a*s=m` over `R_q=Z_q[X]/(X^N+1)`. For a public Galois g:
```
sigma_g(m)-m =
  (sigma_g(b)-b)+sigma_g(a)*sigma_g(s)-a*s.
```
Under restrictive **invariance** `sigma_g(s)=s`, this becomes
```
(sigma_g(a)-a)*s + (sigma_g(b)-b).
```
Thus source-domain rank2 GGSW with gadget input messages `(beta*s,beta)` under same s can consume *two public difference inputs* and produce `Enc_s(beta*(sigma_g(m)-m))` in one GGLWE VMP, with no additional automorphism KSK. Across hidden onehot group `sum beta_d=1` output `ct+sum_{d>0}branch_d` gives exact `sum_d beta_d sigma_gd(m)`. This is a correct fusion **conditional on** secret invariance and exact gadget arithmetic; no KDM/noise/real backend claim.

## Decisive full-degree signed-orbit proof [PASS and FATAL]

Take `N=16384`, `2N=32768`, `theta=4`, generator g=`5^4 mod32768=625`, order `2048`; inverse g has the same fixed space. Signed action on monomials: `sigma_g(X^i)=(-1)^{[625i mod32768>=16384]} X^{625i mod16384}`.

Enumerate all cycles of coefficient indices with cumulative wrap signs. Exact exhaustive result:
- **8 positive-sign cycles, all singletons**, at indices `[0,2048,4096,6144,8192,10240,12288,14336]`.
- **88 negative-sign cycles**, eight cycles of each length `2^j` for j=0,..,10.
To be invariant, coefficients along any negative cycle must satisfy `c=-c`; for ternary c∈{-1,0,1} modulo 2^k (k>=2), c=0. Every permitted nonzero coefficient is therefore at one of those 8 singleton fixed indices:
```
 sigma_625(s)=s => s=∑_{j=0}^7 eps_j X^{2048j}, eps_j∈{-1,0,1}.
 HW(s)<=8, |ternary secret space|<=3^8=6561=2^12.6797.
```
**Source target HW192 has ZERO valid keys** under this constraint, unconditionally. Even abandoning fixed HW192 yields only ~12.68 bits of key entropy (small enumeration), nowhere near 128bit. This is not a probabilistic lattice estimator or security attack on SHIP. Characteristic-2 torsion irrelevant: source coefficients restricted to ternary and modulus>=4. The exact signed-permutation proof avoids falsely counting negative cycles as degrees of freedom.

## Conditional toy and source-shaped resource results (EXECUTED)

Python stdlib reproducible `/mnt/data/ship_i237_subring_obstruction.py`, sha256 `d127a7248337c90decf76eed518ba07545ff6ae5e553a0eccd3548362d1e1208`; JSON `/mnt/data/ship_i237_subring_obstruction.json`, SHA256 `627962f5b6e0f787e837649a608a9ddfbc461f5bf3522da6e65333c7c36137c6`. N64 toy, q2^16, g5^4, invariant secret X^8-X^16+X^24, random full RLWE masks and fresh noiseless rank2 GGLWE rows, four radix16 gadget digits: **48/48 full MuxRot**, **144/144 individual nonidentity branch delta** exact checks passed. Repeating source-family N16384 signed cycles: positive count8, negative count88, HWmax8. No noisy/full actual CKKS test because variant already invalid for HW192.

**Hypothetical costs if the impossible invariant dense secret were allowed:**
- Source original 480 rank2 key objects×90MiB + 2404MiB other prepared = **44.53515625GiB**, baseline 480×36=17280 symbolic ring polynomial-products.
- Conditional rank2 default 352 rank2 key objects×90MiB +2404MiB others = **33.28515625GiB (−25.26094% prepared named bytes)** and 352×36=12672 online VMP ring product slots (**−26.6667%**).
- Matched current-group external raw streaming named max original 2.875GiB, conditional variant 2.7431640625GiB; this is not actual peak RSS, excludes scratch and source plan's input-transform overhead. **None of these is an achievable secure regime for the fixed HW192 secret**.

## Decision

**STATUS:** FAIL H237 secure secret precondition / PASS exact conditional rank2 algebra and signed-orbit bound / PASS arithmetic, no author vulnerability.
**RESULT:** A genuinely lower-cost rank2 affine selector-automorphism fusion is possible only by restricting s to the 8-dimensional fixed subring under g=5^4 in this design. For the source's dense ternary HW192, the proposed secret family is EMPTY; without that HW constraint, the <=6561 candidates are brute-force enumerable. Thus security compatibility, not gadget arithmetic, kills the idea. This is an *assumption-versus-construction* obstruction, NOT a proof all rank2 fused muxes impossible.

**NEXT_TEST / PI:** Do not open I238 just to vary theta, radices, invariant subgroup or tiny parameters. Recommend provisional PARK of SHIP cryptographic HMux key compression; resume only on a clearly different secure secret-independent compressed fused primitive with source-matched cost/novelty evidence, or a defensible real benchmark opportunity. PI controls any strategic pivot to another FHE line.
**STATE_UPDATE:** YES; save this failure and append topic/root state only, verify reread. Other lines unchanged.
