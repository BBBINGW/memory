# FHE Research State — After Iteration 183

**Checkpoint:** 2026-10-14 · `main` · **I183 COMPLETED; I184 NOT STARTED**.
**Authority:** `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → `STATE.md`; one falsifiable technical claim, one decisive test, read-before-write, evidence provenance. Human PI chooses final research direction and contribution. Latest archival index `findings/OPEN_RESEARCH_BRANCHES.md`.

## LATEST — Iteration 183 GBFV few-slot automorphism compatibility

**STATUS: FAIL** simple public masking followed by the unmodified GBFV.Auto to bypass the paper's temporary BFV-domain operation; **PASS** exact source-compatible root/divisibility test; **UNCLEAR** a newly designed scaling-compensated masked automorphism and performance. **I183 COMPLETED, I184 NOT STARTED.**

**Primary source:** Geelen–Vercauteren, *Better GBFV Bootstrapping and Faster Encrypted Edit Distance Computation*, ePrint **2025/1104**, full 22pp GitHub mirror PDF SHA256 `2128d7f5e568b6d66f71f6ad5f913baf34847103ef694246348d27d89ca0956f`, VERSION_UNVERIFIED. §3.2.1 pp7–8 **already explicitly notes** that in few-slot SubConvert some automorphisms do not stabilize the plaintext modulus and must be temporarily performed in BFV domain. Original generalized BFV paper Geelen–Vercauteren ePrint **2024/1587**, full 32pp mirror SHA256 `3158eb77d6aebe92d34479ed6163af34fde7b9f2fc7d82cb85ca7d50151ea4de`, §3.3 p11 ordinary GBFV automorphism requires `σ(t)∈tR` and scale correction `σ(t)/t` since ciphertext scale is `q/t`.

**One exact falsifier:** Ring `R=Z[X]/(X^64+1)`, source-valid binomial `t0=X^4−2`, characteristic prime `p=65537`, ℓ=4 slots, target subring dimension n''=4, hence ℓ=4 < n'/n''=16. Source first iteration g=77=5^-1 mod128, `t1=(X⁴−2)(X⁵²−2)`; `σ77(t1)=(X⁵²−2)(X³⁶−2)`. Mod-p root `r=4938` obeys `r^64=−1`, `t1(r)=0`, but `σ77(t1)(r)=48069≠0`. Hence `σ77(t1)` is not a t1-multiple in R and existing native GBFV.Auto cannot be invoked *unchanged* just by masking. Contrast borderline n'=16,n''=4,ℓ=4,b=4,p257,g13: `t1=16−X⁸`, `σ13(t1)=t1` exactly. The strict few-slot constraint corresponds to a genuine source scaling/integrality distinction.

**Scientific judgment:** The authors already document the restriction, so this is an architectural falsifier of a naive optimization, **not a discovered paper bug, cryptographic attack, or publishable contribution**. Masked compensated operator could in principle exist but would need an explicit lift-independent plaintext map, a valid encrypted scale correction, matched noise/security and smaller measured cost than existing BFV detour; no such construction or benchmark currently exists. Recommend PARK the simple bypass and pivot. Full derivation `findings/gbfv-few-slot-invalid-automorphism-scaling-gate-iteration183.md`, blob `b797b17673d260332577763562128a10c628f88a`, commit `4c1b4b5e2dcf2d2065c86640d2e0b328d8124c82`.

**End:** STATUS FAIL/PASS limited; RESULT exact root+scaling incompatibility; NEXT_ACTION: I184 NOT STARTED, one new distinct source-based hypothesis on next PI continuation, or only revisit with a substantive compensated scheme; STATE_UPDATE YES. Earlier I182 notes and archives below are HISTORICAL, not an active research target.

## HISTORICAL I182 TARGET / LATEST ITERATION

**GBFV→CKKS source-based Theorem 9 digit-modular-reduction correctness boundary (I182) — CLOSED / recommend PARK simple no-wrap audit.** The primary Jaehyung Kim *Bootstrapping GBFV with CKKS*, IACR ePrint **2025/888**, full22pp Research MCP github-mirror PDF SHA256 `604a22c3abe24fe0c91f1fccf9b09c0599156b6d9e759a9f352f03262e14a8e3`, official latest `VERSION_UNVERIFIED`. Original §4.1 pp10–14 (Theorems5–8/Corollary3) bounds `Phi=Flatten(m)+(X^k−b)I` coefficients `≤3(|b|+1)/2` and degree `<k(ell+2)` under small-error and message-range conditions. §4.2 pp15–18 (Lemmas3–4, Algorithm3, Theorem9) computes approximate modulus u via centered digit residues `r_j=[b^j]_u`, for `|b|=B≥2,u<B^ell,ell<N/k−4,p=B^(N/k)+1`. I182 attempted to falsify post-linear-transform integer representability: might y_i=Σ_{j≤ell+1}phi_{kj+i}r_j exceed p/2, causing modp wrap that disrupts mod-u arithmetic. **FAIL hypothesized missing condition.** Exact uniform inequality

`|y_i|≤3(B+1)/2·Σ_{j=0}^{ell+1} min(B^j,u/2) < 3(B+1)/2·(2+1/(B²(B−1)))B^ell < B^(ell+5)/2≤B^(N/k)/2 < p/2`.

Last four digit residues use ≤u/2 and earlier ones a geometric series; direct ell0,1 cases smaller. Numeric sanity B=2 gives `3(B+1)(2+1/(B²(B−1)))=20.25<32=B^5`. An exhaustive coefficient-level fixed source toy `N16,k1,b2,ell11,p65537` over **8,382,462** (m,u) pairs with `I=0` yielded no wrap or modulo-u failures (max |y|=1536); accounting for independent sign-compatible `I_j∈{−1,0,1}` allowed by per-coefficient `|e_j|/q<1/4` gives max |y|3633, also safely below32768.5. **PASS** exact conditional integer no-wrap bound, NOT a complete proof of CKKS-to-GBFV noise/security/precision. No paper flaw or new FHE method. Artifact `findings/gbfv-ckks-modular-reduction-integer-nowrap-bound-iteration182.md` blob **`3394534ac41d6ed365e958fa8c9d6799ec80312e`**, commit `539c0de69047f643a97966b45712b48af679444e`.

**Related primary paper** Geelen–Vercauteren *Better GBFV Bootstrapping and Faster Encrypted Edit Distance Computation*, ePrint **2025/1104**, full22pp mirror SHA256 `2128d7f5e568b6d66f71f6ad5f913baf34847103ef694246348d27d89ca0956f` VERSION_UNVERIFIED; §3.2 explicitly handles few-slot invalid GBFV automorphism via temporary BFV domain, and §5 tables emphasize low vs high plaintext precision/latency tradeoff. No standalone novel claim from merely comparing papers or an already admitted boundary. Third-party/current ePrint2026/2310 (TFHE multi-value bootstrapping) and ePrint2026/1604 (coefficient-wise trace) full sources inaccessible (Research MCP RETRIEVAL_BLOCKED); not audited.

**I182 status:** FAIL hypothetical post-LinTrans wrap counterexample under source's assumptions, PASS rigorous small-representative bound and exhaustive toy, UNCLEAR all other source correctness/security and whether any deeper research question merits reopening. **NEXT_ACTION:** I183 NOT STARTED. Human PI continuation may choose different source-backed high-impact research claim; avoid repeated elementary coefficient-size proofs. **STATE_UPDATE:** YES.

## PREVIOUS ARCHIVES / DO NOT REPEAT

- **I177** TFHE exact-known-Hamming-weight public mask shift, n834 uniform mask residual variance gain ~4.21% only, distribution/security and novelty unclear; PARK.
- **I175–I176** Park C-MT lightweight binary jump reuses known LLKN23 ePrint2022/532 RotToRot, p-ary master generation, spanning tree; novelty FAIL, PARK.
- **I171–I174** SHIP 2025/784 independent Poulpy full masked-selector storage, generic seeded compression halves persistent data but NOT prepared full operands, hybrid fused masks sum to secret one-hot per column; simple memory tricks PARK.
- **I170** BGV Hom-NTT 2024/164 complete layer-collapse density known and in source §4.1; PARK.
- **I168–169** AKS basis-key public linear sum and its extra noise/rounding; PARK.
- **I167** unpacked AHE notation, I165–166 HFP covariance, I160–164 CKKS first-stage weighting, I156–159 SPRU toy error are PARKED. Older MRFHE/GL failures likewise archived.
- **vFHE ePrint2025/286 P1** CRT scalar lookup soundness question remains **OPEN/SOURCE-GATED** pending correct latest official Feb2026 full PDF; no current-edition proof bug asserted.
- Other older targets and source gates indexed in `findings/OPEN_RESEARCH_BRANCHES.md`; missing or source-blocked full papers tracked `MISSING_SOURCES.md`. ePrint2026/2310 PDF currently source-blocked; do not reason from abstract.

## HISTORICAL I182 NEXT_ACTION (SUPERSEDED)

**No primary hypothesis active.** On next “继续”, interpret assent to PARK the **naive dBGV I178–181 exploration**, without claiming authors' general problem solved/impossible, then select ONE **genuinely new high-value source-available** FHE correctness/security/noise/cost target from real primary literature and archival index. Verify source version, strongest paper's own baseline/limitations and prior art BEFORE algebra toys, and specify one sharp falsification test with substantive practical/theoretical value. Do not relabel obvious modular arithmetic or known bootstrapping nonlinear rounding as a publication result. PI decides scientific contribution/pivots.


## HISTORICAL I183 NEXT_ACTION — SUPERSEDED

No active primary hypothesis after I182. Recommend PARK Theorem9 integer no-wrap boundary as resolved; on next “继续”, use original paper source plus prior-art to specify ONE genuinely new falsifiable correctness/noise/security/cost hypothesis with real practical importance before calculations. Preserve previous dBFV→BGV I178–181 PARK recommendations, vFHE latest-edition SOURCE-GATED and all other archives. PI final decision.
