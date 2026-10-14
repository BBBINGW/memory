# PVFHE-P08 — Classical resettable precommit joint extraction via two-fork binding

**Checkpoint:** 2026-10-14 Asia/Tokyo. **Independent PVFHE P08 COMPLETED, P09 NOT STARTED.**
**STATUS:** **PASS** exact abstract classical interactive joint-extraction-and-forking theorem under explicit interface assumptions, **UNCLEAR/HUMAN_REVIEW** its exact CMNW Ring-PCS instantiation, slack-SIS parameters, runtime, quantum extraction, ROM/QROM FS and complete repaired vFHE. NO real PCS attack, SNARG transcript, implementation or publication claim.

## Read before write / isolation

Read repo START_RESEARCH_SESSION.md (SHA 6235e9d376a8b143719a40178132f02a6a41d4f3), RESEARCH_PHILOSOPHY.md (49da3f7fa3e75f5025258cf525482ce4a7ab6867), AGENT.md (b3e73b2c7f852c05aa674dd97b632e9f99ac5f22), global STATE.md (72cca7c545bb56d956c800251bb1c55bd3bf0554; separate vFHE V27), prior P07 findings/pvfhe-P07-cmnw-joint-extraction-challenge-order-gate.md (4eb5b1a1af088f90166e90c93500ad3b3ed9968e), P06 (f479b7c8f6c6be49cf8aabc294be5d5ccdc3dc99). P07 established binding slack and commitment-before-challenge as necessary conditions. P08 is new; DO NOT EDIT these or independent SHIP/vFHE states.

Original CMNW24b: Valerio Cini, Giulio Malavolta, Ngoc Khanh Nguyen and Hoeteck Wee, *Polynomial Commitments from Lattices: Post-Quantum Security, Fast Verification and Transparent Setup*, CRYPTO 2024 / ePrint **2024/281** (https://eprint.iacr.org/2024/281), source full PDF Research MCP 52 physical pages, GitHub mirror SHA256 a9be7b5c1e9024d2d0c03865978d7f3ea1ed941dce8883f93f9576ae46a73b73, VERSION_UNVERIFIED. Read pp11–13 **Definition3 relaxed binding with slack, Definition6 knowledge soundness against STATEFUL classical adversaries WITH REWINDING and Definition8 single-evaluation commitment relation**, pp15 Theorem4 SIS binding, p22 Theorem2 extraction enlarged norm, p24 multilinear PCS, pp39–42 quantum extraction state repair. The CMNW published theorem does **not** explicitly address our joint statement. The paper itself models evaluation over Z_q and uses ring/lattice constructions; source-level adaptation to PVFHE's R_Q must be audited separately.

Original vFHE source: Huang–Li–Mao–Zhang, *Fully Homomorphic Encryption with Efficient Public Verification*, ePrint **2024/1764**, https://eprint.iacr.org/2024/1764, Research MCP 29pp PDF SHA256 7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089 VERSION_UNVERIFIED, p6 generalized ring Schwartz–Zippel, pp8–9 Ring-PCS abstract interface, p21 Theorem5.7, p27 Ring-R1CS. Source version/visual formula parity not independently established. Web results verified paper identity, but not a published erratum or formal joint-proof theorem.

## ONE primary falsifiable hypothesis + ONE decisive test

**[HYPOTHESIS P08]** For P05's *classical RESETTABLE INTERACTIVE* two-evaluation extension, under same-commitment extracted-slack binding, the two single-PCS CMNW-style knowledge extractors can be coupled on a fixed header, and a TWO-FORK binding argument bounds the acceptance probability of a false Galois-invariance statement **WITHOUT** extracting the committed polynomial before external challenge r.

**[FALSIFIER]** Form a reduction with exact probabilities including the one-evaluation extractor errors, intra-session two-opening collision and cross-fork collision, challenge-order and conditional independence; show via exhaustive finite exact combinatorics how postchallenge changes of extracted f do or do not defeat SZ if commitment binding is available. State any unproven CMNW/QROM composition assumptions explicitly, do NOT conflate source CMNW quantum theorem with our classical abstraction.

## Explicit composed protocol / assumptions

Let R be finite commutative, sigma an involutive automorphism, Y(T) a multilinear polynomial in s variables, E an exceptional set. Assume the following **extension**, NOT original CMNW/vFHE:
(A1) Prover publishes commitment C (and any binding prefix) **BEFORE** verifier samples r uniformly from E^s. After seeing r it publishes BOTH v,v' *BEFORE either internal PCS proof challenges*. Then it sequentially proves claims PC.Eval(C,r,v) and PC.Eval(C,sigma^{-1}(r),v'), using independent **internal PCS verifier coins**, and finally checks v=sigma(v').
(A2) Single-statement knowledge extractor with one-statement knowledge error eps1,eps2, under arbitrary classical auxiliary state, rewind/reset snapshots and sequential simulation of the first proof for the second. The CMNW Definition6 quantifies over stateful classical provers, but the combined transcript/reduction needs this resettable interface. Error-bound coupling must preserve fixed C,r,v,v'.
(A3) Commitment relaxed binding for *TWO extracted* polynomial/opening pairs at slack beta_*; a sufficient norm target for the elementary SIS difference reduction is 2beta_*. CMNW p22 beta_*=(2*r_fold*kappa_fold)^ell beta; §6's published one-statement sufficient hardness bound must not be silently assumed to cover 2beta_*. Need check admissible slack set and expected-time extraction implementations, not claim underlying CMNW is broken.
(A4) The statement is false in the precise sense that there is **no valid sigma-invariant polynomial opening consistent with C and the other public claim constraints**. The twisted polynomial D_f(T)=f(T)-sigma(f(sigma^{-1}(T))) is nonzero for every candidate admissible opening f. For any fixed such f, Pr_r[D_f(r)=0]≤delta=s/|E| by the original ring exceptional-set Schwartz–Zippel.

## Lemma A: coupling two classical single-statement extractors [DERIVATION, conditional]

Condition on fixed joint header C,r,v,v' and resettable prover state immediately before either internal PCS proof. First single-statement reduction interacts with the first proof; second reduction simulates honest first PCS verifier (or uses cloned concrete classical post-first-proof state) and exposes the second proof to its single-statement verifier. Public points being related does not invalidate the per-statement extractor because both public statement tuples are FIXED before the corresponding internal PCS challenges. By the source-style one-proof Definition6, on accepted sessions extraction of invalid openings fails with probability ≤eps1 and ≤eps2 respectively under the induced auxiliary adversaries; coupling the same joint transcript with resettable snapshots yields union bound eps1+eps2. If extracted f1≠f2, both open the same C at extracted slack and yield a binding break with probability eps_B,intra. Consequently the chance of an accepted session without ONE common f satisfying both claimed evaluations is at most
  alpha=eps1+eps2+eps_B,intra.
This is a proof at the CLASSICAL RESETTABLE abstraction, not a completed end-to-end CMNW PCS source implementation/QROM proof. Runtime and security of multiple rewindings must still be validated before asserting it as a concrete CMNW theorem.

## Lemma B: independent FORKS eliminate need for pre-r polynomial extraction [DERIVATION, PASS]

Let tau be the pre-r prefix/prover snapshot, C fixed in tau. Define mu_tau(f) = Pr over fresh r, prover/verifier randomness, and extraction that both proofs ACCEPT and yield the SAME valid f. Set p_tau=Σ_f mu_tau(f).
For EVERY fixed non-invariant admissible f, event extracting f and accepting implies D_f(r)=0, while r is uniform independently of tau. Hence mu_tau(f)≤delta, even though the *selected* f may depend on r.
Run two independent r forks from the same tau, each with independent inner PCS coins/extractors; distinct extracted valid polynomials f≠g yield two relaxed openings of C. The probability of this fork binding collision conditioned tau is exactly
  eps_tau=p_tau^2−Σ_f mu_tau(f)^2.
Average across tau and use relaxed binding:
  E_tau[eps_tau]≤eps_B,fork.
Since μ_f≤delta, Σ_f μ_f²≤delta*p_tau. Thus
  E[p_tau²]≤delta*E[p_tau]+eps_B,fork.
Jensen yields p_good²≤delta*p_good+eps_B,fork, and therefore
  p_good ≤ (delta+sqrt(delta²+4eps_B,fork))/2 ≤delta+sqrt(eps_B,fork).
Add joint-extraction/binding failure:
  Pr[false accept]
   ≤delta+sqrt(eps_B,fork)+eps1+eps2+eps_B,intra.
No need to have pre-extracted r-independent f. This is **one** external SZ challenge; PCS two related openings do NOT provide a second independent SZ trial.

Technical qualifications: both forks must rewind/copy CLASSICAL adversarial pre-r state without giving new C; the binding reduction must operate at extracted polynomial norm/slack; extracted f and st must be valid for the exact committed polynomial class; expected-PPT extractor should be truncated appropriately when converting to a strict PPT SIS adversary, accounting for failure. For actual quantum adversarial state the copying/forking is invalid, and generic Fiat–Shamir/QROM security DOES NOT follow.

## ONE minimal executed exact rational test

Actually executed Python: /mnt/data/pvfhe_p08_classical_forking_lemma.py SHA256 **26e940bee3d91211f96124be0b492de7879bb3a34f09ad95c3aed6c5d9f4c984**.
JSON: /mnt/data/pvfhe_p08_classical_forking_lemma_results.json SHA256 **5c219fc94ed0430f543c2c51305e74b589604a321b5a2431cc8b1c5614d7e539**.
Full Markdown report: /mnt/data/PVFHE_P08_Classical_Precommit_Joint_Extraction.md SHA256 **cafe5eb845e2bf10d9990bfda4a95e799cde2a78b908e336bb28870bf258de31**.

An ABSTRACT exactly enumerable binding-game model with 7 uniformly random challenges and 3 distinct false polynomials, each passing only at one distinct challenge; an adversarial strategy chooses one of 3 extracted polynomials after seeing r or rejects. Enumerated all 4^7=**16,384** deterministic challenge→opening policies using Fraction rational arithmetic. **16,384/16,384** satisfy p²≤(1/7)p+prob(two independently successful forks yield distinct f). Perfect binding (collision0) limits accepted bad statement to p≤**1/7**; without binding, strategy f_r for r0,1,2 achieves p=3/7, binding collision probability6/49, and exact equality (3/7)²=(1/7)(3/7)+6/49. THIS IS NOT A CRYPTOGRAPHIC CMNW EXPERIMENT, NOR AN SIS BREAK. It checks the **quantitative forking lemma's counting argument**, not the source-level extractor.

## End of iteration

**STATUS:** PASS formal conditional classical interactive proof at precise interface A1–A4 and exact finite probability falsification attempt; **UNCLEAR/HUMAN_REVIEW** binding norm and slack instantiate under actual CMNW24b Ring-PCS, rigorous multi-rewind implementation, full PVFHE witness/linkage, concrete prover-verifier costs, quantum/QROM and FS transcript composition.
**RESULT:** Prechallenge COMMITMENT fixation + postchallenge TWO-FORK binding suffices to handle r-dependent extracted polynomials, giving an explicit square-root loss. CMNW source single-statement extractor plus classical resettable auxiliary adversary simulation is plausible and supports an abstract joint extraction lemma, but don't claim fully audited production theorem.
**NEXT_ACTION P09 only on PI continuation:** Source-verify a complete concrete ring-PCS/SIS parameter instantiation and classical-to-FS transcript/domain-separated reduction, OR seek a pre-r extractable commitment lemma removing sqrt(binding) and compare true overhead. Do NOT rerun similar abstract toy games or assert QROM security without separate theorem.
**STATE_UPDATE:** YES standalone P08 record only. NO edits to global STATE.md or concurrent SHIP/vFHE state, or prior P01–P07.