# vFHE V43 — October 2026 revised range PIOP blocks archived Cross-CRT witness

**Research date:** 2026-10-15. **Independent V-series; general I192 stays frozen.**
**STATUS: FAIL (old counterexample transfer); PASS (source recovered and new gate excludes the exact witness); HUMAN_REVIEW for future scope.**

## Original primary source and version boundary [FACT]

- IACR ePrint 2025/286, *Verifiable Computation for Approximate Homomorphic Encryption Schemes* (Cascudo et al.), official landing https://eprint.iacr.org/2025/286 displays **2026-10-01, last of 2 revisions** and notes **"Fixed a flaw in the protocol for range checks of Section 4.3. Minor editorial improvements."**
- Human-supplied GitHub file: `papers/supplied/eprint-2025-286-official-2026-revision.pdf`, main, Git blob SHA `3431dd8acbac7141cad2592d45eb13c38510b1e4`, **902276 bytes, 58 physical pages**, inspected with Research MCP `read_repo_pdf` (pp1–2, 22–29, 52–57). Prior Feb-2026-looking GitHub mirror has **836746 bytes, 52 pp**, SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`: not same PDF.
- **Provenance limit:** user identifies supplied bytes as recently downloaded official PDF; live official landing date and the new text agree with Oct 2026 revision. We did **not** independently download official raw bytes (web official PDF request returned HTTP 403), compute supplied file's PDF SHA256, or authenticate exact official-origin byte equality. Git SHA is a blob ID, not PDF SHA256. Do not equate the filename to cryptographic provenance. However the required *new theorem/protocol text* is accessible and usable with this provenance qualifier.
- The new PDF §4.3 physical p22–24 and Theorem 4.8 p24 now state a **field** range PIOP `Pi^F,beta_range` over F=Z_p, not the old directly ring-instantiated theorem. New Prop. 4.9 p24 integer lift, constraints (27)–(29) and Lemma 4.10 p25, **Figure 2 p26** cross-modulus consistency and Theorem 4.11 pp25,54–56 are new decisive source evidence.
- **Remark 4.12 p26 explicitly acknowledges** older R_q lookup PIOP ensured only independently bounded CRT digits and did *not* imply global ring-scalar membership; thanks Yuanju Wei, cites `[WZZ+26]` = Wei et al. **GlueLUT: Efficient Lookup Table Arguments over Residue Rings**, ePrint 2026/494 (reference p38). Do NOT assert unrecognized novelty or a live-Oct-2026 security bug.

## One falsifiable H-V43

**H-V43 (falsified):** The archived V17–V19 native CRT-idempotent invalid scalar digit `e=(1,0)` can still yield an accepting *honest-consistent-oracle* Figure 2 revised range proof by supplying separate digit witnesses for the native CRT components, as in the former source Figure 1 proof.

**Cheapest decisive test:** instantiate the EXACT archived counterexample against the new Figure 2 step-2 equality check, assuming correct polynomial-evaluation oracles and successful auxiliary *field* range proof. If it cannot satisfy the explicit new check, old Figure 1 transcripts do not carry over.

## Exact algebraic test [DERIVED/EXPERIMENT]

Take `R=F_13[X]/(X^4+1)`, `N=4,d=2`, `beta=2`, `t_beta={0,1}`, and `e=7+4X^2`.

- CRT factorization: `X^4+1=(X^2-5)(X^2+5)` mod13. `e mod (X^2-5)=7+4*5=1`; `e mod (X^2+5)=7-4*5=0` mod13.
- `e^2=e` in R; yet `e !=0`, `e !=1`. This witnesses the *old* soundness problem and fits the archived legal native factors.
- Let the ring oracle `h(T) = e` be constant and invalid. Figure 2 requires a **single** polynomial `h'(T)` over one auxiliary `F=F_p`, checked with `Pi^F,beta_range`. Conditioned on the field range proof being sound, `h'(0),h'(1) in {0,1}`, so `iota(h'(r)) in {0,1}` at `r=0,1`.
- Choose toy `ell*=1,m=1,theta=2,kappa=10,p=101`, `q=13`. Then `theta<=pmin=13`, `p>2*beta*(2theta)^m=16`, `(m/theta)^kappa=2^-10`, and `2^(ell*-m)=1`. These are **toy source-shape parameters, NOT security-strength parameters**.
- For every such r, the new Figure 2 p26 Step 2 requires `y(r) mod 13 = iota(y'(r)) mod 13`. Correct source oracles give `y(r)=e`, while the right is constant ring-scalar 0 or 1. In CRT coordinates LHS `(1,0)`; RHS `(0,0)` or `(1,1)`. **NEITHER equals LHS**, so the verifier's explicit all-prime, all-remaining-Boolean-coordinate check rejects deterministically, excluding cheating in the separate oracle-evaluation proofs and in `Pi^F,beta_range`.
- For general valid field digits, Theorem 4.11's source argument defines `h''` as the common integer lift of the auxiliary field oracle, `f=h-pi_q(h'')`, uses the ring exceptional-set Schwarz–Zippel bound `(m/theta)^kappa`, bounded-integer no-overflow Prop4.9/Lemma4.10, and a final native-prime check to detect nonzero f. This repairs the *interface that was absent before*. We independently checked only the exact old e witness; this is **not** a formal independent proof of every bound in Theorem 4.11 or full Fiat–Shamir/PCS security.
- Tiny independent polynomial-ring multiplication verified `e^2=e` and native CRT images; scalar candidate 0/1 both failed the new congruence comparison (performed in this session, reproducible from the displayed equations).

## Cost and research implications

[FACT] New §4.3 p27 states prover work `O(kappa*2^(ell+nu+gamma) + 2^(b/c))` and verifier work `O(ell+nu+gamma+b/c+kappa*2^(ell+nu+gamma-m))`; it sends `kappa*2^(ell+nu+gamma-m)` clear elements **in each of** Z_q and F, besides committed oracle material (see p27). This is an explicit new overhead/interoperability issue, **not itself a new optimization proposal**. A meaningful follow-up would compare the new protocol to GlueLUT 2026/494 and assess source parameters, security and end-to-end cost, but requires PI choice and a genuinely novel nontrivial technique.

**Result:** The exact archived counterexample is a **confirmed historical flaw for the older construction and author-recognized in Remark4.12**, not a surviving counterexample to the supplied October revision's Figure 2. No independently verified latest-version vulnerability, exploit or distinct novel repair has been established.

**STATUS:** FAIL H-V43; PASS exact new-consistency-gate falsification of old attack; no new live vulnerability. **NEXT_ACTION:** HUMAN_REVIEW — PI chooses whether to PARK the historic vFHE bug-hunt and prioritize new source-complete FHE optimization-composition research (current strategic priority), or to authorize ONE precisely defined fresh audit of revised Theorem4.11 efficiency/cross-modulus assumptions against GlueLUT. Do not automatically continue another V-round. **STATE_UPDATE:** YES, source gate materially resolved for document text, provenance caveat retained. SHIP I226 and CGS-17 remain independent and untouched.
