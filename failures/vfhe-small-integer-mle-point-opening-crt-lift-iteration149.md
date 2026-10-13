# Iteration 149 — A native h~(r) opening at a small non-Boolean integer point need NOT have a no-wrap common integer lift

Date: 2026-10-13. Human PI's "好的，请继续" authorizes one iteration I149 after I148. One primary source-specific hypothesis and one exact constructed diagonal-digit MLE falsifier, not a vFHE protocol attack or PCS lower bound.

## Evidence and prior work read first

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` after I148 (SHA `2a5dc0fcee5bff0833db69c922565e922b2277a3`), opportunity index `findings/OPEN_RESEARCH_BRANCHES.md`, I59/60 CRT witness/PIOP results, I63 ring-only local no-go, I77/78 external common integer link vs CRT fake aggregation, I83–85 privacy/witness range, **I86 `findings/vfhe-public-aggregate-vs-mle-evaluation-rank-obstruction-iteration86.md`** (rejects arbitrary mask as ONE original MLE opening, DIFFERENT question), I87/88/90/91/94, I95 archived bounded-public-A + source Brakedown repair, and I136–138 simple PCS batching failures; I148 `findings/vfhe-bounded-alphabet-rankone-mask-soundness-cost-iteration148.md` verified 39 bounded weighted masks but no material PCS savings. Do not reopen old routes or claim novelty for interpolation algebra.

Primary paper Cascudo, Costache, Cozzo, Fiore, Guimarães, Soria-Vazquez, *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint **2025/286** https://eprint.iacr.org/2025/286. Research MCP full **52 physical pages** GitHub-mirror PDF SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, compared to current official PDF **VERSION_UNVERIFIED**, original official revision dated 2026-02-16 reported fixes to Theorem4.8. Re-read source primary §4.3 physical pp20–23 Eq(22)–(23): `h~` MLE values at Boolean grid in diagonal scalar table `t_beta={0,...,beta−1}`; §5 pp25–26: source Ring PC commits per CRT finite field, evaluation proof opens `h~(r)` and its projections; §6.3 p29: Medium circuit `N8192,L3,c5`, 20bit table, Πrange maximum input286720 ring elements, 49bit RNS primes. I90's **pessimistic conditional envelope** `m=2^19, ell=19, beta≤2^20` is NOT a verified exact author's h digit oracle, especially the formal c=2^gamma versus application c5 discrepancy. Use **beta=2^20** merely as the extremal allowed assumption to test a universal repair guarantee, not a source-measured actual beta.

## ONE new hypothesis and falsifier

**[HYPOTHESIS]** Without introducing new original-h PCS evaluation-phase openings or a masked sumcheck, replace source random challenges for an already-opened h~(r) by a common **ordinary integer coordinate** set `S⊂Z`, `|S|≥3`, and ask the verifier to reconstruct/compare **one canonical ordinary integer** `A=h~(r)` in `[0,p_min)` (or a similarly narrow single-prime no-wrap interval) against every independently proven CRT projection. Since **all honest Boolean h(b) are bounded scalar digits**, hope every honest non-Boolean evaluation h~(r) also has a unique canonical *single-prime* integer lift. This would turn a pre-existing source h point opening into a free globally coupling check with no new Brakedown evaluation phase, unlike I86's *arbitrary Boolean mask* rank obstruction.

**[FALSIFIER / one cheapest test]** Construct one **perfectly honest diagonal scalar digit** h :{0,1}^ell→[0,beta−1] with some eligible non-Boolean **integer** r∈S^ell such that its exact Z-valued MLE h~(r) lies outside any 49-bit prime's [0,p) range. Toy check with two small legal CRT primes and exact integer MLE then source-envelope integer inequality. If such an honest proof cannot be parsed as one bounded A, the proposed no-new-proof common-small-integer check fails **completeness**, without even needing to design a malicious CRT transcript.

## Exact MLE extremal identity

For Boolean b∈{0,1}^ell, `χ_b(r)=∏_{j=1}^ell (r_j if b_j=1 else 1−r_j)`. The integer multilinear extension `h~(r)=Σ_b h(b)χ_b(r)`. At homogeneous integer point r=(t,...,t):
```
 Σ_b χ_b(r) = (t+(1−t))^ell = 1.
 Σ_b |χ_b(r)| = (|t|+|1−t|)^ell =: H_t^ell.
```
Choose honest digit table `h(b)=beta−1` if `χ_b(r)>0`, otherwise0. Then `h(b)∈t_beta` for EVERY Boolean b, yet
```
  h~(r) = (beta−1) Σ_{χ_b(r)>0} χ_b(r)
        = (beta−1) (H_t^ell+1)/2.
```
For an INTEGER t not in {0,1}, `H_t=|t|+|1−t|≥3`. Every integer S with ≥3 distinct members contains at least one such t. Thus
```
 h~(t,...,t) ≥(beta−1)(3^ell+1)/2.
```
For the conservative Medium envelope `ell=19,beta=2^20`, RHS is EXACTLY `609359159404050` when t=2 or t=−1, and greater for |t| further from {0,1}. In particular
```
  (2^20−1)(3^19+1)/2
   =609359159404050
   >2^49=562949953421312
   >p for EVERY 49bit RNS prime p.
```
So **no choice of an ordinary scalar integer challenge alphabet S with |S|≥3** can guarantee every honest bounded digit MLE evaluation lies in a single-prime `[0,p_min)` under this parameter envelope. It is a **completeness counterexample to THAT simple normalization**, NOT to original source PIOP or a general impossibility for CRT-wide integer lifts (modulus Q≫p_min), BIGNUM arithmetic, larger primes, small actual beta, or new PCS with authenticated canonical representation.

Even taking S={0,1} to keep every h~(r) itself a legal Boolean digit yields |S|2, making source ring Sumcheck's ordinary `degree×#variables / |S|` soundness estimates vacuous for ~19 variables. One can also choose challenges with sparse non-Boolean positions to reduce integer magnitude, but the strict all-S^ell/ordinary Sumcheck challenge set and its source soundness proof then change. Do not claim a universal lower bound on ALL altered protocols.

## ONE exact independent sanity test and deterministic reproduction

Executed `/mnt/data/i149_vfhe_scalar_mle_nosmall_lift.py`, SHA256 `b49690e1fa65470f27ebfa318445482797128c1777b516782a8e41b80c4e76d0`. It directly computes ALL 2^3 multilinear basis terms at t=2 and t=−1 with ell3, beta4 and valid Boolean digit table chosen based on coefficient signs. Both cases give
```
h~(t,t,t)=42;
t=2:  h in lex-index bit order [0,3,3,0,3,0,0,3]
t=-1: h in lex-index bit order [3,0,0,3,0,3,3,0]
mod 29 =13; mod37 =5.
```
Thus although digits all in [0,3], **NO canonical integer A in [0,29) can equal the two field evaluations simultaneously** (over integers 13≠5). No sound protocol should reject honest h, hence this narrow lift semantics fails. Source-envelope exact computation gives `h~(2^19)=609359159404050>2^49` (precise argument is r=(2,...,2), not the integer base 2^19 itself) and ratio to 2^49≈1.08244; no cryptographic sampling or full SNARK run.

## Evaluation / scientific judgment

**[FAIL narrow free-reuse hypothesis]** Bounded scalar digits on Boolean points do NOT imply a bounded ordinary single-prime lift of h~(r) at non-Boolean scalar integer challenges. A comparison of CRT projections after lifting each residue into the same small `[0,p_min)` integer interval would lose perfect completeness for some legal h, even with **just r_i=2**. With only binary coordinate challenges, source Sumcheck's security estimate becomes too weak. Thus this plausible way to avoid I95/I136–138 extra field PCS openings is not source-viable without a different integer-lift/proof architecture.

**[NOT established]** This is NOT the I86 tensor rank argument, NOR an attack on source PIOP, nor a general no-go against a **full-product Q CRT lifted** value, an interval with signed values >p_min, multi-point clever sampling, special digit shape/β≪2^20, or transparent hash/commit-and-prove coupling. In full Q, honest value 609e12 could have an exact canonical lift, but then an ill-formed componentwise CRT tuple also has *some* lift; additional smallness/binding and challenge soundness are nontrivial. A shared canonical lift protocol would need a source-costed proof and independent randomness; no cheap answer obtained. This is elementary Lagrange/MLE coefficient growth and likely zero publication novelty alone.

**[DIRECTION]** I148 I87-mask improvements and I149 native-opening canonical small-lift both insufficient to solve core vFHE CRT global digit index binding. Recommend PARK this single-prime integer-lift shortcut, do not falsely revive I95. A genuinely different prospective direction is a *whole CRT modulus Q bounded lift with quantified soundness and cheap certified range*, or an external integer commitment built into a new PCS, each requiring a new hypothesis/security/cost test and no claim of 10× yet. Otherwise PI may pivot to another higher-value FHE branch. Do NOT contact authors without separate PI authorization, as original issue is confidential and full official current PDF binary still unverified.

## End

**STATUS:** **FAIL_NATIVE_EXISTING_MLE_OPENING_SMALL_INTEGER_LIFT_COMPLETENESS / PASS_EXACT_HONEST_DIGIT_MLE_OVERFLOW_COUNTEREXAMPLE / HUMAN_REVIEW / NO_ACTIVE_HYPOTHESIS**.
**RESULT:** Under conditional ell19,beta2^20 and 49bit prime regime, an honest h with all Boolean digits0/β−1 has integer MLE at r=(2,...,2) equal609359159404050>2^49. Any integer coordinate challenge alphabet with ≥3 elements contains a t outside {0,1} yielding as much growth. Tiny ell3,beta4 h evaluation42 maps to CRT residues13 and5 for primes29,37, no shared A∈[0,29) for the honest witness. No original vFHE attack or PCS lower bound.
**NEXT_ACTION:** I150 only with PI authorization. Do not retry S={0,1} or invoke a cheap normalization to single-prime A from existing h point openings. If continuing vFHE, state ONE source- and proof-cost-specific **whole-product Q canonical short-integer lift check** hypothesis with a precise completeness/soundness/no-wrap falsifier and estimate whether any new PCS is saved, or pivot to a higher-potential FHE branch. Current latest official paper version **VERSION_UNVERIFIED**, no public security disclosure.
**STATE_UPDATE:** YES — a distinct, source-parameter-conditional completeness blocker to new zero-extra-PCS candidate, not a revival of archived direct scalar masked sumcheck repair.
