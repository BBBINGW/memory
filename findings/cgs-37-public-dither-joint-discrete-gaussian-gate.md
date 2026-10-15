# CGS-37 — Public residue dither fixes Gaussian support but fails marginal and joint-law gates

**Date:** 2026-10-15. **One active FHE PI task:** CGS, root STATE latest override CGS-36; NEXT was CGS-37. **One primary hypothesis plus one decisive exact finite-distribution test.** This is NOT an attack on unchanged Okada–Takagi threshold FHE or a new Gaussian primitive.

## Primary hypothesis H-CGS37

The static Shamir-shared Gaussian *factor* approach of CGS-36 fails because `dG` lies on the sublattice `dZ`. Repair its support *without any nonlinear per-party MPC or extra online rounds* by adding a PUBLIC independent residue dither U to each local output share:
```
L_s=2 (favorable integer scalar model), G_sid ~ D_(Z,2),
U_sid ∈ {-1,0,+1}, with Pr[U=0]=1/2 and Pr[U=±1]=1/4,
ζ_i = L_i G_sid + U_sid  (mod q),
ζ = Σ_(i∈act) λ_(act,i) ζ_i = 2G_sid+U_sid.
```
Hypothesis: Full integer support + correct Gaussian variance scale + exact T-out-of-N reconstruction makes output close enough to source-required `D_(Z,4)`, INCLUDING the public U joint law in an adversarially observable residual, with fixed long-term Shamir shares and zero extra online rounds.

**One cheapest decisive test:** Calculate EXACT probability mass functions of (i) ζ alone and (ii) (U,ζ) against the original distribution plus an INDEPENDENT newly published U. Use an elementary observable event `ζ mod2 = U mod2`, and compute rigorous distributional separation. Independently sanity-check any-T reconstruction with the public dither. If failure is constant TV, reject this particular sampler before full FHE security/cost.

## Original and closely related prior art [FACT]

1. **Okada–Takagi**, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025, IACR ePrint **2025/409**, https://eprint.iacr.org/2025/409, 40 physical-page Research MCP mirror SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, VERSION_UNVERIFIED. **Algorithm7 physical p29**, setup KeyGen requires INTEGER discrete Gaussian `ζ^(sid)←R(D_(Z^n,σ0 sqrt(Bpub²I−Σ_s)))`, Shamir shares `ζ_i`; **Algorithm5 physical p23** adversarial ODec makes `ctdec` and all `pdi` visible; **Lemma7.1 p30 Eqs25–26** provides statistical simulation for **aggregate** secret-independent latent noise, which ALSO contains independent Server flooding. An output-only TV test of raw ζ is an exact *sampler substitution* check, NOT automatically a full transcript distinguisher after flooding/rounding.
2. **Raymond K. Zhao, Ron Steinfeld, Amin Sakzad**, *COSAC: COmpact and Scalable Arbitrary-Centered Discrete Gaussian Sampling over Integers*, ePrint **2019/1011**, PQCrypto 2020, https://eprint.iacr.org/2019/1011. Full 19pp original via Research MCP, PDF SHA256 `b70811ed22fd3978a5a613614255d9044f9c9b69ed5cf681f8cfd16c5318a0a8`, VERSION_UNVERIFIED; **Algorithm 3 physical p8, Theorem 3 physical p6**: a correctly parameterized *single-party* discrete Gaussian sampler based on continuous normals + rejection/acceptance tests. It is NOT a noninteractive Shamir-threshold protocol. Source text p6–8 contains glyph extraction errors; web PDF screenshot was attempted but 403/cache miss. Rely on unambiguous rejection/acceptance structure and original theorem attribution only, not a fragile transcribed formula.
3. **Olive Franzese et al.**, *Secure Noise Sampling for Differentially Private Collaborative Learning*, ePrint **2025/1025**, https://eprint.iacr.org/2025/1025. Read ORIGINAL 38pp via Research MCP, mirror PDF SHA256 `ea7f3a14ddbff6214bad0a1550b2d42e2a81b9a4d01051e41841d6b0ac575d4f`, VERSION_UNVERIFIED. §4 physical p6 and Fig1 p3: approximates discrete noise distribution using private MPC table lookups. **Table 1 physical p2** reports positive per-sample online communication (e.g., 0.72MB for 2 parties, 1.91MB for 4 parties in their DP setting and parameterization), so this actual robust MPC primitive is NOT a drop-in 2-round/no-online-communication ThFHE sampler; those MB values are not transferable ThFHE benchmark estimates. It is a grounded next direction, not a claim about universal impossibility.
4. CGS-21 original LWE DPRF Shamir pointwise nonlinear rounding failed same-degree/all-active-set consistency; CGS-36 factor-only output `2 D_Z,2` has TV `0.4999965126576` from source target `D_Z,4`. This iteration tests DIFFERENT attempted repair: public full-residue dither `U`.

## Shamir correctness [DERIVED + TESTED]

Over odd prime `q=65537`, trusted KeyGen shares `L_s=2` with degree-1 polynomial `P(t)=2+r t`, giving each party `L_i=P(i)`. For each public `G` and `U`, output local padding shares `ζ_i=L_i G+U`. The interpolation polynomial `P(t)G+U` keeps degree 1 and its constant coefficient is `2G+U`. For ANY legal active set S size ≥T=2:
```
Σ_(i∈S) λ_(S,i) ζ_i = (Σ λ_i L_i)G + (Σ λ_i)U = 2G+U.
```
Exactly 492 enumerated algebraic reconstructions (every authorized subset among N3, 41 integer G candidates in [-20,20], and 3 U possibilities) passed. This establishes only algebraic integrity and no additional communication; not privacy or actual source gaussian law.

## Exact public-dither support and statistical tests [DERIVED]

Let `p_G(g) = exp(−πg²/4)/Z_2`, `p_H(z)=exp(−πz²/16)/Z_4` where `H~D_(Z,4)`. Let `P_U(0)=1/2`, `P_U(±1)=1/4`. Candidate output is `ζ=2G+U`.

- **Output support:** ζ spans ALL integers (previous n=1 parity support obstruction removed). Both ζ and H have roughly centered/similar continuous scale; U has mean zero.
- **Exact marginal TV:** compare `Q(z)=Σ_u P_U(u) · 1[z≡u (mod2)] · p_G((z−u)/2)` with `p_H(z)`. Executed precision-85 series gives
```
TV(Q,H)=0.046883973077439879525764258669091421...
```
which is constant ~4.69%, much smaller than CGS36 ~50% but still NOT negligible for exact source discrete-Gaussian substitution.
- **Exact public joint law:** The new PUBLIC U is independently sampled. For the unchanged source to be augmented with the same independent public information, target/reference is `(U,H)` where H is independent `D_Z,4`. Candidate is `(U,2G+U)`. The event
```
A(U,z) := [ z mod 2 = U mod 2 ]
```
holds with probability ONE in candidate, while under reference it holds with probability
```
(1/2)·Pr[H even] + (1/2)·Pr[H odd] = 1/2.
```
Thus JOINT `TV((U,ζ),(U,H))≥1/2` **EXACTLY**, regardless of base G law. Full finite-Gaussian pmf evaluation produces even larger
```
TV((U,ζ),(U,H)) = 0.51126637352153953703144881075376121...
```
This is the decisive **public-randomness joint-law** gate, not merely an output parity repair. For d residue classes with public uniformly distributed residue U mod d and a candidate output with ζ mod d=U, exact analogous bound `TV≥1−1/d` against independent target.
- **Distinguishing scope:** This proves a raw-joint sampler limitation if ζ (or its residue) is observable along with U. Original source actual reveal is `ctdec,{pdi}` and resulting residual after adding independent secret-aware r^Ts and flooding and final mod q rounding. Those transformations may statistically wash out the parity. We DO NOT claim an attack on the actual source or that this TV lower bound transfers automatically through postprocessing. The candidate nevertheless fails its own exact Gaussian pad distribution requirement and cannot reuse source Lemma7.1/Thm7.5 without NEW convolution/masking proof.

## One executed test [EXECUTED]

`/mnt/data/cgs37_public_dither_joint_gaussian_gate.py` SHA256 **2c053d68793ed1304f55e8322f77186ec00034bfb1fa47a232a4fee6d5ab56b8**; JSON `/mnt/data/cgs37_public_dither_joint_gaussian_results.json` SHA256 **89121b8f7b7abf60a4fe9c4e075f6d113eb3286b86e4e58f4d34f0cac96d8689**. Directly executed in this session, all assertions PASS. Used mpmath 85 decimal digits, Gaussian sums g=-80..80 and z=-161..161; conservative mathematical Gaussian omitted two-sided normalized tail estimates <`2.42e-2238` per base and target tail. Script computes marginal/joint TV and parity predicate probabilities independently.

## Synthesis / boundaries / novelty

**PASS** output full integer support, mean-zero dither, linear Shamir threshold consistency, fixed long-term shares, no additional rounds. 
**FAIL** correct output law: TV~0.04688 despite full support. **FAIL** unmasked public U+ζ joint simulation: TV~0.51127, parity event advantage≥0.5.
**UNCLEAR** actual source-adversarial transcript effect because independent E (original Server noise) + secret rounding may hide the raw residue; a new proof would have to start from full Algorithm5 joint view, not the isolated sampler. Exact discrete Gaussian can be sampled via known COSAC rejection/acceptance mechanisms, but porting it into local Shamir shares is nonlinear, and a generic MPC secret table lookup has documented positive online communication. No known support for retaining arbitrary T,N and source O(1)-in-N online broadcast without added setup or interactions.
**NOT NOVEL:** Dither/trivial parity conditioning and rejection sampling are old. No new attack on source original 2025/409, no completed secure ThFHE, no publishable primitive claimed.

### End-of-iteration
- ITERATION: CGS-37.
- STATUS: **FAIL** explicit public-dither raw source-Gaussian distribution and public joint-law; **PASS** algebraic any-T consistency and exact TV calculations; **HUMAN_REVIEW** parent secret-conditioned Gaussian O(LDec) question OPEN.
- RESULT: `TV(marginal,dZ4)=0.04688397`, `TV((U,ζ),(U,dZ4 independent))=0.51126637`, public parity test advantage exactly 0.5, 492 all-subset reconstructions PASS.
- NEXT_TEST CGS-38 (only if PI next "继续"): ONE concrete existing MPC **private lookup discrete Gaussian sampling** primitive (e.g., Franzese et al. 2025/1025) and an exact source-cost/round falsifier for ANY T-of-N. Test whether it can run in source's online TWO rounds and preserve O(1)-in-N Server broadcast without O(LDec) preprocessing, when sampler target variance is itself SECRET correlated with s. First distinguish prior-art's PUBLIC distribution sampler from our SECRET parameter/hidden covariance requirement. If no mechanism meets necessary constraints, present clear PI HUMAN_REVIEW/pivot rather than repeating trivial dither variants.
- STATE_UPDATE: YES; one CGS finding, topic addendum, root checkpoint, no unrelated modifications.