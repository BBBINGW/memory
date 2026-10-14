# Iteration 184 — Independent per-party PRF padding cannot replace Shamir-shared noise for arbitrary threshold active sets

**Date:** 2026-10-14 (local). Authorized by PI "好的，请继续" following I183. Research protocol read START_RESEARCH_SESSION.md → RESEARCH_PHILOSOPHY.md → AGENT.md → STATE.md (I183 sha `584c820b553def3eb5cee94171fe045e4439c2a2`) → findings/OPEN_RESEARCH_BRANCHES.md → I183 finding. One **new parent gap** with ONE primary proposed repair and ONE small-threshold **source invariant** feasibility test; the variance system and finite-field consistency check are two lenses on the same test, not two unrelated hypotheses.

## Original paper (source-grounded, version caveat)

Hiroki Okada and Tsuyoshi Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025, IACR ePrint **2025/409**, https://eprint.iacr.org/2025/409. Read complete current Research MCP **40 physical-page** `github-mirror` PDF SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, official latest PDF **VERSION_UNVERIFIED** (mirror revised full proceedings-looking paper, updated §1.3); web indexed *older distinct 36pp* PDF and web screenshot failed cache miss, so equations/page numbers below refer specifically to Research MCP's 40pp mirror, not that old web version.

**[FACT]** §1.2 physical pp4–5 authors explicitly identify the issue **bounded number of decryption queries** `LDec` for their STANDARD (M)LWE scheme: pre-distribute fresh padding Gaussian noise for EACH decryption session, causing `O(LDec)` stored secret material per party; removing LDec bound is open. Also author assumes an uncorrupted noncolluding semi-honest Server in §1.2; this iteration does NOT address server removal. §5 knLWE version can have unbounded LDec under stronger known-norm assumption (not a direct substitute for standard MLWE). Theorem 6.2/6.3 pp27–28 proves standard-LWE correctness/simulation security assuming fresh padding per permitted session, and Theorem7.4/7.5 pp32 for MLWE.
- **Algorithm6 physical p26** in scalar LWE case: at setup sample `ζ^(1),...,ζ^(LDec) ← D_(Z,σ0√(Bpub²−||s||²))^LDec`. Shamir-share `(s,ζ^(1),...,ζ^(LDec))` at threshold T across all N parties; party i receives `(s_i,ζ_i^(1),...,ζ_i^(LDec))` plus a separate independently generated PRF seed `seed_i`. For active set S and session sid, partial dec `pd_i=λ_(S,i)(a^T s_i+ζ_i^(sid))+m_i (modq)`, `m_i=PRF(seed_i,sid)`. Shamir reconstructs `Σ_(i∈S)λ_(S,i) ζ_i^(sid)=ζ^(sid)` for **every legitimate S**, source Eq(24) p27; PRF masks m_i are separate unweighted pads and cancel via ServerDec in FinDec, so they are NOT Gaussian ζ replacements.
- **Algorithm7 physical p29** uses covariance `Σ_s=Σ_i Gram(s_i)` and sampled multivariate `ζ∼D_(Z^n,σ0√(Bpub²I−Σ_s))`, also Shamir-sharing each session. The scalar-LWE counterexample below is sufficient to refute a universal direct simple repair; DOES NOT analyze MLWE covariance distribution on its own.

## ONE primary falsifiable claim

**[HYPOTHESIS to KILL]** To remove pre-distributed `O(LDec)` Shamir Gaussian padding in Algorithms 6–7 **without any new correlated preprocessing/coordination**, reuse each participant's existing independent `seed_i` and locally compute small zero-mean padding `Z_i(sid)=PRF-Gaussian(seed_i,sid)`. Replacing `ζ_i^(sid)` by `Z_i(sid)` preserves the source's (i) globally shared per-session scalar Shamir reconstruction `Σ_(i∈S)λ_(S,i)Z_i(sid)=ζ(sid)` for ANY eligible S, or at least (ii) the SAME secret-norm-independent target narrow Gaussian padding distribution for every eligible S, so one may reuse Theorem6.2/6.3 without changing security/correctness.

**[CHEAP decisive falsifier]** Instantiate only **3 parties, threshold T=2**, Shamir share indices x_i=i∈{1,2,3} over prime field `F_q` with odd q. Compute λ at zero for S12,S13,S23, compare consistency of one per-session global pad and (in generous real/no-modular-wrap approximation) conditional noise variance as sum of independent per-party contributions for all S. If impossible already here, the no-new-correlation PRF patch cannot work for arbitrary T-out-of-N.

## Exact check A — one global Shamir pad is necessarily correlated (finite field, exact)

Lagrange coefficients at zero:
```
 S12: (λ1,λ2) = (2, −1)
 S13: (λ1,λ3) = (3/2, −1/2)     (interpret inverses in Fq)
 S23: (λ2,λ3) = (3, −2).
```
For the same `sid`, all sets reconstruct one global ζ iff the `Z_i` are evaluations of a **single degree≤1 polynomial**; equivalently `Z3=2Z2−Z1 (modq)`. Three *independent uniform* PRF field outputs satisfy this with probability exactly `1/q`, since given Z1,Z2 only one Z3 qualifies; they do **not** form Shamir shares. Enumerated every (Z1,Z2,Z3)∈F7³: 49 of343 triples reconstruct the same ζ via all3 subsets, probability exactly1/7. This refutes directly replacing SOURCE's Shamir padding shares by 3 independent outputs while claiming to preserve the original reconstruction invariant. Note if one chooses active set only once per sid and redesigns the construction to permit set-dependent pads, the global equality may be dispensable; hence the second distribution check.

## Exact check B — even a generous narrow centered independent Gaussian model cannot be active-set invariant

Assume independent centered real-valued small padding `Z_i`, with variance `v_i≥0`, and a regime in which modular wrap is absent and finite-field interpolation coefficients may be interpreted as their natural rational Lagrange values. In this best-case **relaxed/no-wrap model** the combined pad variances equal
```
 S12: 4v1+v2
 S13: (9/4)v1+(1/4)v3
 S23: 9v2+4v3.
```
To simulate **one** target Gaussian padding variance `V>0` for any S (as required for the source security simulation when the active set is adversarially chosen), these must all equal V. Exact linear solve has **unique** candidate
```
 v1=V/3,   v2=−V/3,   v3=V.
```
This violates nonnegative variance `v2≥0`. For V=120 the computation yields `(40,−40,120)`; all three formal equations evaluate exactly to120, proving no nonnegative solution. The actual Shamir protocol computes over Zq; **do not present this Gaussian real-lift negative-variance fact as a universal theorem about all mod-q local PRSS samplers**, since modq wrap and non-Gaussian distributions can change the model. It rigorously kills the proposed "just sample independent narrow local Gaussians and interpolate normally without modulus issues" shortcut and motivates use of correlated randomness.

## FHE/MPC implications, sources of novelty and caveats

**[FAIL]** Simply reusing the per-party PRF seeds for INDEPENDENT padding samples does not preserve the source's exact per-session Shamir pad invariant. Nor can it match all 2-out-of-3 target variances in the natural small-Gaussian/no-wrap simplification. Current Algorithm6 remains intact and secure under its own assumptions; this is NOT an attack on Okada–Takagi or a proof error.

**[FACT/BOUNDARY]** The author's PRF already pads **partial decryption shares** but those masks are canceled in FinDec; padding `ζ` instead adjusts the decryption-noise distribution so the secret-key norm/covariance is hidden. Those are separate tasks. In MLWE the needed noise padding covariance depends on `Σ_s`, not merely scalar norm; generating correct fresh jointly distributed `ζ` is at least as delicate. Per-session correlated seeds / PRSS / distributed Gaussian sampling **might** be a real way to compress storage, but require compatible threshold subset reconstruction, secret-dependent covariance, simulation security with corrupted parties/possibly adaptive act, and verified sampling (computational vs statistical closeness). No scheme constructed or proved.

**[Novelty]** Need prior-art review of PRSS, pseudorandom *correlated* sampling and threshold Gaussian generation before claiming anything. The no-go for independent PRF is elementary Shamir correlation algebra, not a publishable crypto contribution. The **positive parent gap**—unbounded decryption count with O(1) per-party *stored* secret material under standard MLWE, preserving low communication and sim-security—is explicitly open in source §1.2 and aligns FHE+MPC practical multi-session workflows, but current evidence does not establish a solution or nontrivial new primitive.

## End of Iteration 184

**STATUS:** **FAIL** independent-local-PRF Gaussian replacement for source Shamir padding / **PASS** exact F7 Shamir-consistency enumeration (49/343) and conditional independent no-wrap Gaussian variance impossibility for N3 T2 / **UNCLEAR** any viable correlated seed / PRSS scheme, fresh secret-covariance Gaussian and costs/security at realistic FHE parameters.
**RESULT:** In 2-out-of-3, exact Shamir shares require `Z3=2Z2−Z1 (modq)`; independent local PRF samples do not satisfy. Even if abandoning globally identical padding and only requiring set-independent variance under a favorable narrow no-wrap real-noise model, interpolation constraints force impossible variance v2=−V/3. This specifically excludes a no-coordination seed-only drop-in for author's Algorithm6; not every PRSS or finite-field correlated construction.
**NEXT_ACTION:** **I185 only on human continuation:** ONE prior-art and feasibility gate for **correlated pseudorandom secret sharing of secret-dependent discrete Gaussian padding**, contrasting source's O(LDec) setup shares with established PRSS and distributed Gaussian literature. Require a concrete 2-out-of-3 scheme or sharp formal incompatibility with MLWE covariance `Bpub²I−Σ_s`, preserving adaptive active sets and source simulator; if only generic PRSS and no secure norm/covariance sampler, PARK naive seed-compression and seek another target. Avoid redoing independent Gaussian variance matrices.
**STATE_UPDATE:** **YES**, new explicit unbounded LDec open source target, decisive no-go on naive per-party PRF repair, pinpointed distinct correlation/security obstacle and next prior-art gate.
