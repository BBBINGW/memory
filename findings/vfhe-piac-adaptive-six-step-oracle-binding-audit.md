# Iteration 76 — Adaptive six-step Pi_AC public-coin transcript: fixed false CKKS rescale witness

Date: 2026-10-12
Paper: Cascudo, Costache, Cozzo, Fiore, Guimarães, Soria-Vazquez, *Verifiable Computation for Approximate Homomorphic Encryption Schemes* (CRYPTO 2025), ePrint 2025/286.
**STATUS: PASS** at algebraically source-equivalent ideal PIOP public-coin transcript layer. **UNCLEAR** at authors' exact optimized variable-packing/byte-format layer or compiled polynomial-commitment/Fiat–Shamir SNARK implementation layer.
**NO MAIL:** User explicitly instructed NOT to email authors and to continue research. Absolutely NO outgoing author contact, Gmail draft, public issue, disclosure, etc. No user-authorization inferred from prior "continue".
**STATE_UPDATE: NO** — separate parked RIG-HE STATE.md unchanged.

## Read before write and source provenance
Read connected Research MCP AGENT.md, RESEARCH_PHILOSOPHY.md, parked STATE.md, I73 `findings/vfhe-piac-gkr-eq16-20-source-wiring-transcript-audit.md`, I72 `findings/vfhe-ckks-public-output-binding-robust-rescale-counterexample.md`; source primary original PDF through Research MCP, especially §4.2 pp17–19 and Appendix E.1 pp44–46. 52-page revised-looking mirror PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19` was pinned in I69 to 2026-04-28 mirror history postdating official 2026-02-16 proof fix. **VERSION_UNVERIFIED** for strict byte match to official currently served PDF. The source page45 specifies six steps: initial Eq16 sumcheck (r0), Eq17 sumcheck (r1), random linear-combination Eq19 (s01,s2), Eq18 sumcheck (s), Eq20 sumcheck (squot,squot',sBD,sIP), final input/output/aux ideal oracle queries. D=1 eliminates intermediate quotient-oracle levels.
[HYPOTHESIS] Once sample challenges and all claimed intermediate points are linked across the original six steps, the fixed I72 zero-input / false public output witness can no longer pass because the genuine challenge sequence or final oracle openings impose a hidden independent restriction beyond checked polynomial identities.
[FALSIFIER] Produce ONE continuous adaptive public-coin verifier record with all five Eq16→17→19→18→20 sumchecks followed by exact source-bound oracle openings, all consistent with the SAME public y=173 and aux r=4,017,060. Include negative controls mutating either oracle while holding original prover messages, verifying that binding checks are active.
[RESULT — HYPOTHESIS FAIL] Built complete six-step source-equivalent adaptive ideal-oracle transcript; all pass. No hidden independent check appeared in the specified Appendix E.1 step sequence. We do not claim authors' exact internal packaging/serialization.

## The SAME fixed small admissible computation
N=8, d=4, D=W=1, RNS primes 149,157,173, q=4,046,989, dropped p_l=173, surviving q'=23,393.
Both input CKKS ciphertexts are (0,0); legit pre-multiplication d0=d1=d2=0 and BD/wks three wires=0, key-switch c'_0=c'_1=0; true rescale output=(0,0).
Public claimed output Vout=[173,0], **inside actual true output coefficient bound 173<23393**, and also y0%173=0 (natural surviving ideal).
Malicious auxiliary remainder Vaux index 3 is r=4,017,060; intended global coefficient bound [0,256) violated. Exact Eq16 stronger rescale gate:
 `0 - 4017060 - 173*173 = -4046989 = -q ≡0 modq.`
Source §4.1's rounded B256 >max RNS prime173 causes CRT-rectangular closure T_256^rect = Rq. Prior I72 verified all 128 base16 CRT-glued lookup digits and per-field memory grand-product multisets: beta=16<149, ell*=7, 2^ell*=128<149. In I76 only Π_AC is replayed; the Π_range evidence is not reimplemented anew.

## Exactly one adaptive challenge chain, accurate domain dimensions
Build explicit MLEs for source sets:
 `Vin=[0,0,0,0]`, `V1=[0,0]`, `V2=[0,0,0,0]`, `V2_d01=[0,0]`, `V2_d2=[0,0]`;
 `V3BD=[0,0,0,0]`, `V3quot=[173,0]`, `V3IP=[0,0,0,4017060,0,173,0,0]`, `Vaux=[0,0,0,4017060,0,0,0,0]`, `Vout=[173,0]`.
All ring element values here are constant polynomials in X; ideal-oracle checks are exact arithmetic modulo q. Pad unused index slots with zeros.
Original source sums in Eq16/Eq17/Eq18/Eq20 run over DIFFERENT Boolean dimensions. Instead of I73's heuristic merge, define a single product-domain sum and use multilinear χ_zero selectors for unused coordinates, so each term sums to exactly its original source-domain sum. The verifier also knows these selector factors. This preserves individual source-domain dimensions and all challenge links, but MAY DIFFER from the authors' optimized internal index encoding or message bytes, which Appendix E.1 does not fully specify.
Six protocol steps:
1. V samples r0∈S^2, sum-check Eq16 over V1(1 bit), V2d2(1 bit), V3IP(3 bits), **5 rounds**, extract `r1,r2,rIP`; initial sum 0; final nonzero evaluation with original RHS source oracles and predictors matches. Nontrivial cancellation uses r=4,017,060 and y=173. Rescon weights are coefficient −1 for remainder and −p_l for quotient; BD uses genuine CRT PW idempotents.
2. With same `r1`, sum-check Eq17 over d01(1bit), BD(2bits), **3 rounds**. Both source arrays zero; any legitimate eval key coefficients work since BD=0. Transcript uses arbitrary fixed evk coefficients for deterministic simulator only, NOT asserts they came from genuine CKKS keygen. Claim V1(r1)=0, final zero.
3. V samples `s01,s2`, sum-check Eq19 over full V2(2bits), **2 rounds**, obtains `s`; Eq19 subset incidence maps d01,d2 to full V2. All zero.
4. Using SAME `s`, sum-check Eq18 over input left(2bits), input right(2bits), prior quotient left(1bit), right(1bit), **6 rounds**; D1 means no prior-layer quotient factors in multiplication; input polynomials are zero. Claims `Vin(rin),Vin(rin'),V3quot(rquot),V3quot(rquot')` are extracted under SAME challenges. V3quot may evaluate nonzero but Xmult previous-quot terms vanish by no previous layer, and source zero-input multiplication gate passes.
5. V samples four aggregation challenges `sq,sq',sBD,sIP`, sum-check Eq20 over aux(3bits) × public out(1bit), **4 rounds**; index predicates map BD indices0..2 and IP indices0..4 to Vaux; map V3quot 0,1 and IP indices5,6 to SAME public Vout. Initial claim **3312777** mod q, final nonzero claim; root sum exactly Eq20 and final original source oracle product equals prover claim. Extract `raux,rout`.
6. Final verifier independently queries fixed input, public output and aux oracle MLEs at all derived points; obtained:
 `Vin(rin=(30,52))=0`, `Vin(rin'=(8,23))=0`, `Vout(rout=(117))=4026921`, `Vaux(raux=(11,79,71))=3483009`.
 All match exact Step5 claimed oracle evaluations. y public is 173 on the Boolean output wire even though its multilinear evaluation at 117 is 4026921 modulo q; no equivocating allowed.
Total **20 adaptive sumcheck rounds** (5+3+2+6+4), all individual polynomial degree <=2 verified at off-interpolation points 3 and 5; all sumcheck recurrences g_j(0)+g_j(1)=prior and final g_last(r)=direct source-oracle expression hold modulo q.
S chosen as diagonal scalar integers [0,148] (each difference of distinct elements is invertible mod149·157·173); concrete deterministic challenges sampled in 2..127. Toy security |S|=149 alone is NOT adequate for cryptographic negligible bounds, but identities/acceptance are exact at this challenge schedule and construction is algebraically valid for arbitrary challenges in the source model.

## Negative tamper controls to validate the verifier is binding
Replace just published Vout by [0,0] while leaving prover transcript and internal quotient [173,0] unchanged: Eq20 claim mismatch = **3308106** modulo q and final output opening mismatches. REJECT.
Replace just committed Vaux by zeros while leaving internal IP remainder 4017060: Eq20 claim mismatch = **1473095** modulo q and final aux opening mismatches. REJECT.
The original malicious consistent pair Vout173 and Vaux4,017,060: ACCEPT in constructed ideal oracle transcript.

## Exact independently executed artifacts
- Python: `/mnt/data/iteration76_vfhe_piac_six_step_public_coin.py` SHA-256 `108e11436fc1fc5d068cb14b24725809d36799cac889b94c92265866a986b0c1`.
- JSON: `/mnt/data/iteration76_vfhe_piac_six_step_transcript.json` SHA-256 `bd12dc94adadcc58922b4a765c282e6732a4d3a51cfdc263f4a92f913b67c7f8`, 9467 bytes. Contains verifier coin schedule, each g_j polynomial [constant,linear,quadratic], final oracle values, explicit openings and mutation controls.
Both generated in the active container; the script executed PASS. Note original I73 script's 32 stochastic Eq20 trials not used in this single main test.

## Boundaries and research decision
The source describes Eq16–20 and Appendix E.1 six-step sequencing but not one fixed internal variable packing. Our choice is an explicit **equivalent product-domain padding** (all sum identities mathematically exact), not authors' original optimized transcript serialization. There is NO polynomial commitment key, actual evaluation proof, Fiat–Shamir transform or deployed verifier. No claim of complete compiled SNARK forgery; output y=173 is small and legal, but parameters N8 are not real cryptographic security parameters. Official newest ePrint PDF byte authenticity remains VERSION_UNVERIFIED; 52pp mirrored revision was pinned after the official proof-update note. Do not contact authors without a future explicit user approval, and user CURRENTLY specifically said do not send.
The scientific result is that every stated Π_AC relation-level check and adaptively chained verifier event is satisfiable with the malicious auxiliary value; the structural fault is in Π_range's failure to prove global scalar table membership. Merely binding output, auxiliary and input oracles cannot repair that relation mismatch.

## End of Iteration 76
STATUS: PASS — fully chained source-equivalent ideal Π_AC six-step adaptive transcript with negative binding controls; UNCLEAR — byte-for-byte optimized Π_AC/complete compiled SNARK.
RESULT: Fixed false y173 and remainder4017060 pass 20 round checks and final separate oracle queries. Both intentionally tampered oracle datasets are rejected, showing binding tests active. No new CKKS parameter variants, no outreach.
NEXT_ACTION: Start one minimal technical repair test: Can **one globally shared auxiliary index/bit witness outside Rq** be cryptographically bound to all CRT field-components without linear per-index overhead? Pin a concrete two-component statement (single Boolean digit) and kill the naive proposal by testing whether any verifier commitment/check actually forces the SAME index across components. Only if it survives that toy falsification should analyze protocol cost. Keep focus on source soundness gap and skip unrelated encoder sweeps.
STATE_UPDATE: NO — parked RIG-HE STATE.md untouched.
