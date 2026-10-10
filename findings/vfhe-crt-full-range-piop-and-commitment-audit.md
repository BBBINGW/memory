# Iteration 60 — Full Pi_range counterexample survives §5 CRT polynomial commitments

Date: 2026-10-10
Primary target: Cascudo, Costache, Cozzo, Fiore, Guimarães and Soria-Vazquez, *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, IACR ePrint 2025/286.
STATUS: **PASS (independent formal ideal-PIOP / range-decomposition soundness counterexample)**; **HUMAN_REVIEW** for responsible author confirmation and end-to-end/novelty impact. No full Fiat–Shamir SNARK forgery or deployed CKKS exploit is claimed.
NEW OVER I59: independently tested the **entire two-subprotocol composition** Pi_range=Pi_decomp + Pi_beta_range with ONE common false public polynomial v and common malicious h; verified the sum-check relation, product-tree gates, and virtual sumcheck consistency; inspected §5 componentwise polynomial-commitment design and Appendix D.3 compiler for missing cross-component diagonal-table constraints. None present in specified steps.
Impact potentially material: revised Theorem 4.8 and consequent black-box Pi_range knowledge-soundness bound do not hold as stated for CRT-product ring and diagonal scalar-digit table. Research-grade report suitable for confidential author review; no public disclosure or email performed.

## Read-before-write and primary source pin
[FACT] Read GitHub Notes AGENT.md, RESEARCH_PHILOSOPHY.md, unrelated parked RIG-HE STATE.md, and I59 file `findings/vfhe-crt-lookup-cross-component-soundness.md` before setting one primary technical hypothesis. RIG-HE STATE.md remains UNMODIFIED.
[FACT] Research MCP cached a complete 52-physical-page PDF for 2025/286 from immutable GitHub mirror `arturo-kong/IACR-eprint-mirror`, blob revision `a549654c5dffa3484e95e8244056f4a27c48c3e6`; 836746 bytes; SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`; source_kind github-mirror, version status VERSION_UNVERIFIED. Official landing https://eprint.iacr.org/2025/286 notes **2026-02-16 revision** "Fixed a flaw in the proof of Theorem 4.8" and minor editorial improvements. Mirror PDF includes revised Theorem4.8 and Remark4.9, but mirror bytes cannot yet be equated to latest official PDF; currently web-cached ePrint PDF is an older 50pp version and web PDF screenshot cache missed. Do not misattribute ePrint PDF source versions.
[PRIMARY SECTIONS] §3.1 physical p.10 defines proof-friendly ring as CRT product of finite extension fields; §4.3 pp.20–24 Lemma4.3, equations (21)-(23), Pi_decomp, Theorems4.4–4.8, Fig.1 and revised Remark4.9; §5 physical p.25 constructs commitments by committing **independently to each CRT projection**; Appendix D.2-D.3 physical pp.42–44 defines polynomial commitments and compiles sound PIOPs into arguments via commitment+opening+evaluation checks; Appendix E.2 physical pp.47–49 proves revised Theorem4.8 and improperly concludes "if h notin scalar table then some CRT field projection notin scalar table".
[AUTHOR CODE SCOPE] Official referenced GitHub `vfhe/proof-friendly-CKKS`, README blob SHA `60bc2c9bb4935bfc48ab94e70081d134a10bcb81`, describes proof-friendly CKKS, sumcheck and polynomial-commitment performance benchmarks. No deployed compiled end-to-end Pi_range verifier or cross-component check was independently verified in source code.

## One hypothesis / falsifier / cheap test
[HYPOTHESIS — FALSE] While §4.3's ring lookup is vulnerable to CRT componentwise digit-table cheating (I59), either (A) the full range protocol Pi_decomp imposes a scalar-digit constraint, or (B) the §5 polynomial-commitment / Appendix D.3 compiler automatically binds the same scalar table index across CRT fields and restores the original relation's soundness.
[FALSIFIER] Instantiate an *invalid full range statement* v and a **single common** h such that both Pi_decomp and Pi_beta_range receive algebraically true oracle relations; show the §5/D.3 PC only binds this shared h polynomial, without a proof that its Boolean values are diagonal scalar digits.
[TEST] Exact legal tiny ring; verify EVERY element of Pi_decomp sumcheck for all 49×49 initial/final ring challenges, full lookup multiset polynomial identity from I59 and its CRT projections, all product-tree gates plus virtual sumcheck evaluations; read exact primary compilation statements. No CKKS implementation, no noisy arithmetic, no unnecessary parameter sweep.

## Exact small ring / false public statement
Take `R=Z_77[X]/(X^2+1)`, `N=d=2`, `q=7·11`. Both p7 and p11 equal 2*a*N/d+1 for odd a=3,5 and X²+1 is irreducible over both fields, so `R≅F_(7²)×F_(11²)`. Parameters `B=2`, `b=1`, `c=1`, `gamma=0`, `nu=1`, `ell=1`, `ell*=ell+nu+gamma=2`, `beta=2`. Correct revised Theorem4.8 requirements `beta<pmin=7`, `2^ell*=4<pmin=7` are satisfied.
The explicit exceptional challenge set `S={a+bX : 0≤a,b<7}` has size 49 and pairwise unit differences: since -1 nonsquare modulo both7,11, norm `(a−c)^2+(b−d)^2` is a unit for every distinct pair. In scalable analogues with large 3mod4 primes, |S| grows as p_min² while the PIOP accepts with probability1; this is not merely a small-parameter value of a loose asymptotic soundness bound.
Choose false public ring-vector `v(0)=v(1)=56 ∈ R`, each coefficient-vector (56,0) not in the intended `T_B={a+bX: a,b∈{0,1}}`. Let `h(i,j)` indexed i,j∈{0,1} be [56,0,56,0] in lexicographic order.
CRT projection `56=(0 mod7,1 mod11)`, hence every field projection of every h(i,j) is in scalar table {0,1} while h itself is NOT in diagonal scalar table.
The SAME h and v are used by both subprotocols; no switching witnesses between Pi_decomp and Pi_beta_range.

## Pi_decomp: exact honest relation despite false range statement
Eq.(22): `v(i)=h(i,0)+X*h(i,1)=56` for i=0,1. Define multilinear extensions `v~(R)=56` (independent of input challenge R) and `h~(R,Y)=56(1−Y)`; public `p~_(β,N)(Y)=(1−Y)+X Y`.
For every r∈R, the sumcheck claim over Y∈{0,1} is
 `v~(r) = sum_(j∈{0,1}) h~(r,j)*p~(j) =56`,
so the statement fed to Pi_decomp is TRUE and the honest sumcheck prover succeeds (not an exceptional-challenge accident).
Exact univariate sumcheck polynomial:
 `g(Y)=56(1−Y)*((1−Y)+X Y)`
 `=56+(-112+56X)Y+(56−56X)Y²` in R[Y].
 `g(0)+g(1)=56`; after arbitrary verifier challenge t∈R its final value is exactly `h~(r,t)*p~(t)`. Script checks both for **all 49 choices of r and all 49 choices of t** (2401 instances).

## Pi_beta_range: CRT-glued *valid* field memory transcripts
For h=[56,0,56,0]:
 - mod7 honest accesses [0,0,0,0], field read=[0,1,2,3], final counts table (0,1)=[4,0].
 - mod11 honest accesses [1,0,1,0], field read=[0,0,1,1], final counts table (0,1)=[2,2].
CRT idempotents `e7=22`, `e11=56`: `CRT(a,b)=22a+56b mod77`.
Hence `read_ts=[0,22,23,45]` and `final_cts=[46,35]`.
Both are standard R-valued multilinear evaluation tables. The underlying **ring-pair multisets** WS and RS∪S are NOT equal, but their two CRT projections are equal. Therefore the grand-product polynomial identity `G_WS(σ,τ)=G_(RS∪S)(σ,τ)` holds IDENTICALLY in R[σ,τ], independently of challenges. I59 expanded both sides and compared every polynomial coefficient (17 nonzero terms, total degree6).
I60 newly constructs the product tree oracles directly from true ring leaf factors `a+σb−τ`, verifies **24 parent=child0*child1 gates** at fixed nontrivial ring challenges, and checks the honest degree≤3 virtual sumcheck polynomial against **147 ring challenge evaluations** via independent Lagrange interpolation (denominators 1,2,3 all units in Z77). For the table-side tree the virtual sumcheck relation is identically 0. Because these local predicates are valid ring polynomial equalities on Boolean points, honest sumcheck strategies work. Together with I59's identity valid for all σ,τ, this specifies an accepting ideal-PIOP strategy for an invalid public v, not merely a suspicious step of a proof.

## §5 and Appendix D.3: commitments do not constrain diagonal scalar digits
[FACT] §5 physical p.25 explicitly constructs a Ring-Rq commitment as the **vector of field commitments** to each projection `f^(k)=Phi^(k)(f)`. To open an evaluation `f(a)=y`, verifier independently checks `f^(k)(a^(k))=y^(k)`. Under this construction the above malicious R-polynomials have perfectly well-defined commitments and truthful openings. Independent field consistency checks only verify each field's committed function. They do NOT assert `h(i,j)∈{0,1}*1_R` or require a unique common table-index bit shared across all k.
[FACT] Appendix D.3 pp.43–44 (Theorem D.3) replaces oracle messages by commitments and oracle queries by verified openings and explicitly **requires a negligible-soundness PIOP as input** to infer a sound argument for the *same* relation. The compiler supplies **no missing semantic relation check**. Since the standalone Pi_beta_range is unsound, the precondition of its desired application fails. This is not an attack on polynomial-commitment binding: the prover is binding to a truly malicious ring polynomial, not equivoking.
[FACT] §4.3 Theorem4.4 composes Pi_decomp and Pi_beta_range with a SHARED h oracle. Pi_decomp enforces only decomposition equality, which is met. Thus its generic knowledge-soundness conclusion does NOT follow for the original scalar coefficient range relation. This is the stronger finding of iteration 60.

## Source-level proof bug and asymptotic scope
Appendix E.2 physical p.48 wrongly asserts
 `h~ notin diagonal scalar t_beta => exists CRT component k: Phi^(k)(h~) notin projected t_beta`.
For a product ring, the rectangular closure `prod_k Phi^(k)(t_beta)` strictly contains the diagonal table image `{(t,...,t):t∈t_beta}`. Ring idempotent `e=(0,1)` is not Boolean in diagonal scalar sense even though `e(e−1)=0` in ring; ordinary ring-Boolean checks cannot fix this.
This is distinct from the older corrected issue described in Remark4.9 about field-version Lemma4.6 assumptions. It persists in the examined repaired 52pp mirror text.
The absolute upper bound `O((2^ell*+2^(b/c))/|S|)` from Theorem4.8 should vanish in large valid CRT examples. Since the constructed prover's acceptance is 1 for false statement, its proof system in this form cannot satisfy that asymptotic claim. Our tiny |S|49 witness illustrates algebra; family argument with growing valid primes and extension fields is needed for a formal asymptotic lower-bound contradiction.

## Reproduction and source limits
[EXACT NEW SCRIPT] `/mnt/data/iteration60_vfhe_full_range_piop_audit.py`; SHA256 `2bfa13a134a1b3938adf544bdc5955316e78cf6afdd6938dba2aecbb6ede856f`.
[NEW OUTPUT] `/mnt/data/iteration60_vfhe_full_range_piop_results.txt`; SHA256 `5624bee8332ce907f9fd846db758531ffb232f9c1d84ddec1c5df2db46992e78`.
[PREVIOUS SCRIPT] `/mnt/data/iteration59_vfhe_crt_lookup_soundness_audit.py`; SHA256 `8b7f3a03d5fb6e23b896af494d03fe95081171ffe10355fce6408935cebe4826`.
All three files existed and new script was executed successfully in the active container, zero floating-point approximate decisions.
CAVEAT: I60 checks all Pi_decomp sumcheck challenges and explicit instantiated Fig1 algebraic constraints, but does NOT run a byte-for-byte copy of a shipped compiled SNARK verifier or each message of the actual Fiat–Shamir compilation. Independent formal check of the complete interactive transcript should still be performed before public exploit claims.
OFFICIAL VERSION: Official ePrint landing dated 2026-02-16 currently says Theorem4.8 proof fix; the Research MCP cached 52pp PDF includes revised Remark4.9 but is VERSION_UNVERIFIED; official PDF downloadable bytes not acquired in this run. Confirm official revised artifact before contacting authors.
GITHUB CODE: `vfhe/proof-friendly-CKKS` source README documents proof-of-concept CKKS/sumcheck/PC benchmarks, not a fully verified end-to-end compiled lookup SNARK. No specific deployed system attacked.

## Responsible minimal author-review package (UNSENT)
To: corresponding authors of ePrint 2025/286 (not sent).
Subject: Possible remaining CRT cross-component soundness issue in revised Theorem 4.8 / Pi_range.
Key claim: Revised Appendix E.2 assumes a diagonal-digit membership implication that fails in CRT product rings; independently valid per-field memory traces CRT-glue to an accepting ring lookup even though a digit is not a scalar table element.
Paper pages: physical pp.20–25, 43–44, 47–49 in 52pp cached revision; Theorem4.8, Remark4.9, Appendix E.2.
Minimal witness: `R=Z_77[X]/(X²+1)`, `p=(7,11)`, `B=beta=2`, `ell=1, ell*=2`, `h=[56,0,56,0]`, `v=[56,56]`, `read_ts=[0,22,23,45]`, `final_cts=[46,35]`, `S={a+bX: 0<=a,b<7}`. All theorem restrictions hold, decomposition sumcheck true for all challenges; grand-product identity true as a polynomial. Source PDF SHA and both exact Python scripts above.
Question to authors: Is there any separate index/scalar-subring consistency check omitted from §4.3–§5 that forces the *same* lookup-table digit across every CRT component? If so, where is it specified and how does it affect efficiency/soundness? If not, does the revised Theorem4.8 need a new global-diagonal-membership argument, and how does the full SNARK enforce its range constraints?
Before any external communication, human PI should verify revision and approve content. No disclosure performed.

## End of iteration 60
STATUS: **PASS — exact two-subprotocol ideal Pi_range counterexample and absence of extra constraints in the specified §5/D.3 compiler**, subject to official PDF version confirmation. **HUMAN_REVIEW** for security impact and disclosure.
RESULT: Same invalid public v and same h witness pass full Pi_decomp relation and CRT-compatible Pi_beta_range grand products, tree gates and sumcheck checks. §5 per-field commitments bind the malicious polynomial but do not impose diagonal table membership; D.3 compiler assumes, not repairs, PIOP soundness. Stronger than I59's standalone grand-product example; end-to-end deployed forgery not established.
NEXT_ACTION: HUMAN_REVIEW single decision — approve confidential author verification of the pinned minimal counterexample and identify whether an omitted cross-component scalar index binding exists, before initiating a nontrivial repair design or public novelty claim. If authors confirm absence, next minimal technical task is to devise a global table-index relation with *measured* extra proof/verification cost; never substitute naive idempotent Boolean tests.
STATE_UPDATE: NO — unrelated parked RIG-HE STATE.md not changed.
