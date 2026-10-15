# CGS-20 — An exact scalar-field key-homomorphic PRF cannot supply compact noninteractive Shamir randomness

**Date:** 2026-10-15. **TRACK_ID:** CGS. **Prior:** CGS-19 (interactive MPC rounding cost gate), authorizing PI message “继续”. No change to SHIP, VFHE, EXPLORE, root/global state. This is ONE hypothesis and ONE minimal decisive test.

**STATUS:** **FAIL** the direct exact `F_q`-linear keyed-PRF construction; **PASS** a general unconditional distinguishing lemma and reproducible finite-field test. **UNCLEAR/HUMAN_REVIEW** the original Gaussian padding problem; no new secure primitive, full ThFHE protocol, or publishable result established.

## One primary hypothesis and cheapest decisive test

**H-CGS20 [FALSIFIED]:** Give every party `P_i` a Shamir share `k_i` of a reusable compact seed vector `k in F_q^d`, and let it generate on demand `z_i(sid) = F(k_i,sid) in F_q` **without interaction**. Make the PRF exactly additive in key, `F(k+k',sid)=F(k,sid)+F(k',sid)`, so that the `z_i` shares remain on ONE degree-`T-1` Shamir polynomial for every sid and any qualified T-set reconstructs a common `z(sid)=F(k,sid)`. Hope this `z(sid)` is pseudorandom and suitable for a later share-preserving noise sampler. `d=poly(lambda)` and Eval is public on any explicitly supplied key.

**Decisive test:** Determine if an exact scalar-field output and exact key-linearity can coexist with a standard PRF indistinguishability game for polynomial-size vector keys. One linear-algebra lemma falsifies it without needing full noisy decryption simulations. Only this restricted candidate is tested (not general DPRFs).

## Source interface and relevant prior art [FACT]

- Okada–Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025/ePrint **2025/409**, original full cached 40 physical pages, PDF SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, version unverified. §2.4 physical pp10–11 and Algorithm 6 p26: `zeta^(sid)` drawn from secret-norm-conditioned discrete Gaussian for EACH `sid`, Shamir-shared to parties, `PartDec` returns ONE locally evaluated field share. Theorem 6.3 p28 requires joint simulation of corrupted parties' views and their exposed decryptions; a marginal PRF test would be insufficient. Module case Algorithm 7 p29 uses secret-dependent `Bpub^2 I-Sigma_s`. Original O(LDec) preprocessing/storage remains open.
- Boneh, Lewi, Montgomery, Raghunathan, *Key Homomorphic PRFs and Their Applications*, CRYPTO 2013 (author page https://cs.stanford.edu/people/dabo/pubs/abstracts/homprf.html): key homomorphic PRFs give distributed PRFs; existing secure constructions do NOT imply ordinary exactly linear scalar-field keys/outputs with efficient public basis evaluation. Their lattice variants employ (almost) key homomorphism/rounding.
- Libert, Stehlé, Titiu, *Adaptively Secure Distributed PRFs from LWE*, TCC 2018/ePrint **2018/927**, original cached 44 physical pages SHA256 `9ae0025339690ce80ee701ef6ed987a583fddcd2832f444ffafec93176fe0fdd`, version unverified. Physical pp1–4 define actual noninteractive DPRFs and discuss **approximate** key homomorphism and LWR rounding, adaptive security, lossy/injective tools and special LISS reconstruction coefficients rather than directly claiming `F_q`-linear scalar outputs from ordinary Shamir shares. Their group/rounded/output decoding/security interfaces cannot be silently transplanted.
- Sam Kim, *Key-Homomorphic Pseudorandom Functions from LWE with a Small Modulus*, ePrint **2020/233**, cached 45pp, original PDF SHA256 `58f3827f102864cde9c7f8ec97d8265314d11189e651e4c032fd10d28c79c3d6`, version unverified; §1 pp1–3 details key homomorphism and lattice modulus/security tradeoffs. **This CGS20 elementary lemma is NOT claimed new folklore prior-art technique.**
- Same target authors' 2026/957 newer paper full source was not acquired during CGS19; novelty/source comparisons may be incomplete. No claim about its technical content.

## General mathematical obstruction [DERIVATION, precise]

**Theorem (scalar exact linear key PRF distinguishing).** Let `q` be prime, `K=F_q^d` with `d=poly(lambda)`, and let `F: K × X -> F_q` have a public efficient evaluation algorithm on EVERY supplied key and satisfy `F(k+k',x)=F(k,x)+F(k',x)` for all keys and inputs. Assume `|X|>=d+1`, with distinct efficiently chosen `x_1,...,x_(d+1)`. Then a PPT oracle distinguisher separates `F(k,.)` for any secret `k` from a truly random function `R:X->F_q` with advantage EXACTLY `1-1/q` in `d+1` oracle queries (ignoring merely the polynomial-time precomputation needed to evaluate the public algorithm `d(d+1)` times).

**Proof.** For standard basis `e_j` of `F_q^d`, publicly compute `A_(i,j)=F(e_j,x_i)`. Additivity implies `F(k,x_i)=sum_j A_(i,j)k_j`. Since `A` has `d+1` rows and `d` columns, compute any nonzero `alpha in ker(A^T)` using Gaussian elimination over `F_q`. Thus `sum_i alpha_i F(k,x_i)=alpha^T A k=0` for EVERY secret `k`. For independent uniform random `R(x_i)`, the nonzero linear functional `sum_i alpha_i R(x_i)` is uniform in `F_q`, zero with probability exactly `1/q`. Distinguisher outputs REAL iff this sum vanishes. Its distinguishing advantage is `1-1/q`. QED.

**Consequences (narrow):** A generic simple exact additively key-homomorphic PRF **whose native output is an ordinary field element** cannot support both threshold-Shamir preservation and pseudorandomness. If the output group is represented so that obtaining its discrete-log coordinates is hard, computing `alpha` above from arbitrary key-basis evaluations cannot be transplanted in the same way. Rounding-based lattice KHPRFs break exact scalar field linearity. DPRF and PRSS interfaces are distinct. This lemma does NOT prove that any CGS simulation-secure noninteractive threshold sampler is impossible, and it does not establish a lower bound for nonlinear secret-conditioned Gaussian samplers.

## ONE exact minimal computation [EXPERIMENT]

Local reproducible artifact `/mnt/data/cgs20_exact_scalar_khprf_linear_attack.py`, SHA256 `3d47be2657a25984d9b07d128ed6f86604a9ecb62e437d304beefea6fc52691d`; results `/mnt/data/cgs20_exact_scalar_khprf_results.json`, SHA256 `0cbc89685a09814cd01eadc914c7f7610e11e90c7a4e4db603ef1a250b9993c9`. Toy `q=101,d=3`, domain points `sid:0,...,sid:3`, publicly keyed basis functions formed via SHA256 deterministic coefficients (not claimed cryptographically secure). The computed 4-by-3 public coefficient matrix:

```
A=[[66,36,68],[99,3,47],[21,43,84],[60,94,18]]
alpha=(22,20,79,1) mod101; alpha^T A=0.
```

For 10,000 independently sampled secret vectors, ALWAYS `alpha·(A k)=0`. For 10,000 independent truly random field-function outputs, the same relation held in 105 cases, consistent with exact chance `1/101`. The theorem, not the sampled frequency or SHA toy coefficients, supplies the unconditional 1-1/q distinguishing guarantee.

## Constructive synthesis: genuinely missing interface

We now know the following four wishes cannot be obtained by the tested *exact-scalar-linear-PRF* shortcut alone:

1. Reusable compact setup key + on-demand fresh samples across arbitrary polynomially many sids.
2. Common Shamir reconstruction for any qualified `T` active participants, with one local reply and no online interaction.
3. Secret-dependent **joint** conditional Gaussian distribution, including entire corrupted-party multi-session view and simulator.
4. Cheap explicit security/noise/precision, overhead and source-party/Server consistency.

**Promising but not yet built alternative [SPECULATION]:** use a published group-valued or rounded almost-key-homomorphic DPRF, then find a *new*, efficient, share-preserving randomized Gaussian/secret-covariance link whose rounding defects and threshold reconstruction are provably bounded, or relax interaction/cost. The conversion from group/rounded PRF output to an INTEGER Gaussian shared using original Shamir without interaction is precisely the open gap. Prior CGS-17 excluded exponential subset-PRSS as the naive solution; CGS-19 excluded unmodified MPC-rounding with both zero-prestorage and one-response online properties. Avoid repeating those negatives.

**END OF ITERATION**
- `TRACK_ID: CGS`, `ITERATION_ID: CGS-20`
- `STATUS: FAIL` for H-CGS20 direct primitive / `PASS` exact algebraic distinguisher / `UNCLEAR` general source-compliant sampler, `HUMAN_REVIEW` novel route.
- `RESULT:` Unconditional d+1-query attack with advantage 1-1/q; key-homomorphic PRF title/intent does not justify exact scalar Shamir homomorphism.
- `NEXT_TEST (CGS-21, PI continuation ONLY):` Choose ONE actual published approximate/group-valued DPRF with full original theorem, identify a concrete output-to-Shamir-Gaussian conversion candidate and its transcript; first minimal exact two-active-set/two-session degree/rounding test plus real security/size boundary. If no concrete conversion exists, PARK KHPRF-direct branch. Require source-current 2026/957 before claiming novelty.
- `STATE_UPDATE: YES` CGS files only. General root, SHIP, VFHE, EXPLORE unaffected.
