# CGS-21 — A real LWE DPRF cannot be locally Gaussian-postprocessed as an unchanged Shamir output

**Date:** 2026-10-15. **Mode:** PI-selected single active FHE research session; `STATE.md` is now the only live task pointer. Research target remains Okada–Takagi ePrint 2025/409 secret-conditioned Gaussian-padding storage problem. **LAST COMPLETED BEFORE THIS: CGS-20**.

**ONE PRIMARY HYPOTHESIS (H-CGS21):** Take a secure noninteractive published LWE DPRF and use its secret-partial evaluations as if they were ordinary Shamir shares. Apply a local nonlinear rounding/inverse-CDF (Gaussian-like) transformation at each participant, without any online MPC; any qualified set should then reconstruct one consistent distributed Gaussian value using the original source Shamir Lagrange coefficients.

**ONE DECISIVE TEST:** Read the published DPRF's actual `PEval / Combine` (not just an abstract) and construct the smallest 2-of-3 Shamir local-rounding candidate with two qualified subsets and two nonce inputs. If either nonce gives different reconstructions, the **direct local-nonlinear-share adaptation** fails before Gaussian distribution/security can be considered. Test targets the proposed *port*, not the actual published DPRF's correctness.

## Exact source interface [FACT / PRIMARY ORIGINAL FULL TEXT]

- **Libert, Stehlé, Titiu**, *Adaptively Secure Distributed PRFs from LWE*, TCC 2018, ePrint **2018/927**, https://eprint.iacr.org/2018/927, retrieved complete 44-physical-page original PDF through GitHub Notes `get_eprint_paper` (mirror SHA256 `9ae0025339690ce80ee701ef6ed987a583fddcd2832f444ffafec93176fe0fdd`, `VERSION_UNVERIFIED`). §4.1 physical **pp18–19**, Lemma 4.1 physical **pp20–21**:
  - Uses **LISS (linear integer secret sharing)** with per-participant *matrices of integer share units*, rather than ordinary original-Okada finite-field Shamir scalar sharing; reconstruction coefficients from `{-1,0,1}`.
  - Each `PEval` produces rounded vectors `Y_j` in `Z_p^{m×d_j}`.
  - `Combine` first linearly combines all participating `Y_j` with LISS reconstruction coefficients to obtain an intermediate `z_tilde∈Z_p^m` with an additive bounded **rounding error**. **Only AFTER** this combination, it rounds again to `Z_u^m` and applies public extractor `π` to output `y=π(round_u(z_tilde))`. Lemma 4.1 justifies equality of these **combined final outputs with overwhelming probability** under source choices `p/u > d·2^{L+λ}` etc. It does NOT establish that locally applying `π`, a Gaussian inverse-CDF, or secret-conditioned sampler on individual `Y_j` yields coherent Shamir shares.
  - LISS share and partial-evaluation sizes and p/u noise margins differ materially from a single field-element `PartDec`. Converting LISS to original Shamir itself needs interface accounting.
- **Okada and Takagi**, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025, ePrint **2025/409**, https://eprint.iacr.org/2025/409, 40pp SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, `VERSION_UNVERIFIED`. Algorithm 6 physical **p26**, Theorem 6.3 physical **p28**: one `ζ^{sid}` of **secret-conditioned** discrete Gaussian law is pre-generated and Shamir-shared for every sid, permitting one local field response and giving a simulatable exposed transcript. Its requirement is strictly stronger/different from a DPRF *combiner* producing a public PRF output.
- A newer **2026/957** Okada–Takagi ACISP 2026 paper exists (source: https://doi.org/10.1007/978-981-92-3015-0_8), with serverless short-share constructions according to the public abstract. The full original PDF remained source-blocked on earlier MCP attempts, so no assertion of originality/absence of this attack or alternative in that source.
- Context: CGS-20 rejected **exact finite-field-linear scalar-output PRFs** (a separate, stronger PRF distinguisher statement under different assumptions); legitimate rounded/group-output DPRFs are not rejected by CGS-20.

## Precise toy falsifier [DERIVATION + EXECUTED TEST]

**Hypothetical Shamir adaptation (NOT the Libert–Stehlé–Titiu construction):**

- Work with original Shamir share field `F_101`. The secret is `s=23`, degree-one sharing `f(X)=23+11X mod101`, giving `x1=34,x2=45,x3=56`.
- Use an LWR-*style*, locally computable map `g_a(x)=round_nearest(17*((a*x) mod101)/101) mod17`. Here `a=1` and `a=3` stand in for two distinct nonce-dependent linear pre-transformations; they are **not** actual `A(X)` parameters sampled by LST18. Perform **exact rational nearest-integer rounding**.
- Reconstruct with integer interpolation coefficients for valid 2-of-3 adjacent subsets: for A={1,2}, `(λ1,λ2)=(2,-1)`; for B={2,3}, `(λ2,λ3)=(3,-2)`. These also happen to reconstruct s in `F_101` and are valid reductions in `F_17`; no inverse or characteristic mismatch is used in this counterexample.

| Nonce multiplier a | `(g_a(34),g_a(45),g_a(56))` | `Recon_{1,2}` | `Recon_{2,3}` | `g_a(s)` |
|---|---|---:|---:|---:|
| 1 | (6,8,9) | `2*6-8=4` | `3*8-2*9=6` | 4 |
| 3 | (0,6,11) | `2*0-6=-6=11 mod17` | `3*6-2*11=-4=13 mod17` | 12 |

Each nonce has inconsistent legitimate subset reconstruction. In nonce a=1, one qualified set even reconstructs the central map by coincidence; the other does not. In nonce a=3, **neither** reproduces the central result.

**Reproducer**: `/mnt/data/cgs21_local_rounding_shamir_gate.py` SHA256 `45aa83cf826059e1c2d9d19e0b8f2524bd888704a3217f619b7e179f55188009`; `/mnt/data/cgs21_local_rounding_shamir_gate.json` SHA256 `01df98af4f18b4d4c6cb2704989e7e6a0c3ffe1dc439f48d857a827cb7ef0dc1`. Exact no-floating calculations and assertions executed; toy arithmetic only, NOT a cryptographic instantiation/benchmark.

### More general same-field obstruction (mathematical lemma, not claimed novel)

For odd **prime** q, suppose a fixed public deterministic `g:F_q→F_q` maps **every** degree-one Shamir triple `(f(1),f(2),f(3))` to another valid degree-one triple, with the same party indices. Writing `f(1)=a`, `f(2)=b`, `f(3)=2b-a`, validity forces `g(2b-a)=2g(b)-g(a)` for all `a,b` (Jensen relation). Set `h(x)=g(x)-g(0)`. Taking a=0 implies `h(2b)=2h(b)`; setting `b=(x+y)/2`, `a=x`, yields `h(y)=2h((x+y)/2)-h(x)`. Hence `h(x+y)=h(x)+h(y)`; over the PRIME field, `h(x)=cx` for some c. Therefore **g is affine**. Any truly nonlinear local single-share map has some 2-of-3 Shamir triple on which fixed-degree consistency fails. For extension fields, F_p-linear (not necessarily F_q-scalar) additive maps also satisfy this relation, so do NOT overgeneralize the affine-scalar conclusion beyond prime fields.

This lemma is separate from the toy's map `F_101→F_17`; toy validity is directly proven by explicit integer arithmetic. A sampler with fresh **correlated randomness**, share-index-dependent nonlinear algorithms, new setup material or interactive MPC is outside this lemma.

## Constructive synthesis / scope

[DERIVED] The actual LST18 DPRF is an example of **avoiding** this error: retain additive structure in partial results, then apply nonlinearity **after** combining. If that combiner exposes the resulting seed/PRF value to a party, it does **not automatically provide a hidden Gaussian Shamir sharing**: those are different functionalities. If the goal requires the secret to stay hidden, nonlinear sampler/extractor must be executed **on secret shared data**, requiring a justified special primitive, interaction or trusted setup. A real candidate must simultaneously account for: source-conditioned sigma(s), complete corrupt-view simulation over adaptive sids, active-set consistency, modulus and rounding bounds, and persistent vs per-session key/storage + online communication.

**Precise conclusion:** A naive **local postprocessing** of an actual DPRF's *partial outputs* is not a safe way to obtain a same-degree Shamir Gaussian generator for Okada–Takagi, even when a real DPRF provides consistent **reconstructed** final PRF outputs. Nothing here attacks LST18 or claims an impossibility of all PRSS/PCF/interactive variants. No publishable new theorem or efficient protocol found.

## Iteration close

- **ITERATION:** CGS-21.
- **STATUS:** FAIL H-CGS21 direct local nonlinear partial-output port; PASS actual §4.1 DPRF interface audit + exact two-subset/two-nonce toy + elementary same-field functional lemma; ORIGINAL CGS OPEN / HUMAN_REVIEW.
- **NEXT_TEST (CGS-22, only PI continuation):** Choose ONE explicit **hidden-output threshold DPRF/PCF functionality** that does not expose the reconstructed PRF seed, and test a minimal source-conditioned *shared Gaussian* conversion with a concrete corrupt-party joint-view distinguisher; immediately cost online rounds, secret setup storage, and Q/precision. If no distinct conversion interface exists in prior art, PARK this DPRF-postprocessing family instead of repeating nonlinear-share examples. First recheck Okada–Takagi 2026/957 full text before claiming innovation.
- **STATE_UPDATE:** YES — update current CGS detailed topic note and root single-task `STATE.md`, re-read both. Existing SHIP/vFHE historical science untouched.
