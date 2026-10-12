# FHE Research State — 2026-10-12

ACTIVE: **Carousel generic full-domain bootstrapping algebra / parameter-scope audit**.
Target: Intak Hwang, Seonhong Min, Yongsoo Song, *Carousel: Fully Homomorphic Encryption with Bootstrapping over Automorphism Group*, IACR ePrint **2024/2032**, https://eprint.iacr.org/2024/2032.
Full primary paper obtained through Research MCP: 34 physical pages, GitHub mirror PDF SHA256 `5ddec99ebbe14b270b413e21ab4923abf0ed5dba8d0f1d053b3fde1c5a35d6c8`, source revision `a64684fee3625e3f99908d13abe0e065015f52db`, official latest VERSION_UNVERIFIED.

LAST COMPLETED ITERATION: **108 (2026-10-12)**.

## PROTOCOL / PI–AGENT BOUNDARY
Read `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, last `STATE.md` and relevant prior finding before updates; **one primary falsifiable technical claim and one cheapest decisive test**, [FACT]/[DERIVATION]/[SPECULATION], exact source page / theorem / algorithm; separate archive and state commits/readback. PI judges novelty, risk, strategic pivot, publication, author contacts. No author email/contact/outreach or public disclosure without explicit PI approval.

## I108 — ONE FALSIFIED SOURCE-CLAIM IMPLICATION
[FACT] Paper 2024/2032 physical p4 technical overview: `hat phase = round((N/p)m)+e (mod N)`, assumes `|e|<N/(2p)` and LUT `v_i=f(round((p/N)i))`, then writes returned value f(m) **regardless of input**. §3.1 physical pp12–13 Algorithm1 implements rotated LUT, §3.2 physical pp14–16 prime cyclotomic M, prime p0, N=(M−1)/ord_M(p0), allowed plaintext prime power p=p0^r; §4.2 Theorem4 pp23–24 states output as rotated lookup vector/variance, rather than explicitly proving generic index recovery for p∤N. §5.1 p26 experiments M65537, base prime2 and p4,p8,p16 → N2048, hence p|N in actual tests. The original overview does not in that passage explicitly impose p|N.
[HYPOTHESIS FAIL: SIMPLE THRESHOLD SUFFICIENCY] In general if p∤N, original `|e|<N/(2p)` **alone** does not imply `round((p/N)(round(Nm/p)+e))≡m (modp)` for all plaintext messages. First rounding bias δ_m matters.
[DECISIVE PARAMETER-COMPATIBLE COUNTEREXAMPLE] Take prime cyclotomic M829, base prime/plaintext p0=p5; ord_829(5)=9, N=(M−1)/9=92. m1, e−9, |e|9<92/10=9.2. First `round(92/5)=18`, then switched phase 18−9=9, LUT `round(5·9/92)=round(45/92)=0` ≠m1. No tie ambiguities. Exact exhaustive integer nearest-grid check among 95 valid (m,e) pairs yields **3 failures**, 2 tie-free (other m4,e9); M127, p0=2,p8,N18 gives additional 6/24 failures. This counterexample only concerns the source-stated modular phase/lookup arithmetic, NOT ciphertext generation, 128-bit security, or actual false-decryption probability.
[REAL-PARAM NEGATIVE CONTROL] In the author-chosen source-param M65537, p0=2 has order32, N2048, p16 divides N, δ_m=0. All **2032** valid (m,e) cases with |e|<64 recover identity correctly; p4/p8 likewise divide N. Therefore **NO demonstrated break of author's advertised experiments or original security correctness**.
[DERIVED CORRECTION] δ_m=round(Nm/p)−Nm/p, |δ_m|≤1/2. The correct **message-wise sufficient** small-error condition is |e+δ_m|<N/(2p), and message-uniform sufficient |e|<N/(2p)−max_m|δ_m|. For M829,p5,N92 max|δ|=2/5, hence requires |e|<44/5=8.8 rather than 46/5=9.2. p|N gives δ≡0. A conservative all-parameter bound |e|<N/(2p)−1/2 suffices when positive. This is a potential **generic proof-scope correction**, not verified novelty/impact.
[UNCERTAINTY] Need check whether **full paper or author code already restricts** p|N, or a different post-switch error convention absorbs δ into a smaller e bound; general algebraic numerical counterexample is real for the displayed statement but not necessarily a gap in final formal Theorem4. No author's actual LWE noise-distribution attack. No public disclosure/contact.
Archive: `findings/carousel-blind-rotation-nondivisible-p-rounding-slack-iteration108.md`.
Executed exact reproducer `/mnt/data/iteration108_carousel_rounding_boundary.py` SHA256 `a4c4bd1e3289d13c153c7fbd8b8753f69ae8fd1a6c499cf286994358d0f5ebec`; JSON `/mnt/data/iteration108_carousel_rounding_boundary_results.json` SHA256 `026e8107d8563c2af96562df3d67a1524158d64d59e1103b52b78bcd06a7aaaf`.

## NEXT_ACTION — ONE MINIMAL TEST (I109)
One targeted **scope check**, NOT another numeric parameter sweep: read original source §§3.1–3.2 and formal Theorem4 pp12–16,23–24 and fixed author code `SNUCP/carousel` if available. Determine if **p|N** is imposed by actual encoding/decoding or a stronger modulus-switching phase inequality is used than the p4 overview statement. If yes, original discrepancy is paper-acknowledged/implicitly parameter excluded; archive as FAIL contribution. If not, retain as bounded generic scope clarification; consider real parameter materiality only on PI's instruction. Keep one hypothesis/test.

## PARKED / PRESERVED BRANCHES
- **PARKED Gao–Zheng SIMD ALU single-coordinate cutoff/LUT micro-audit I103–107**, not the full paper. Archive `failures/simd-alu-a2b-cutoff-scalar-microaudit-parked-iteration108.md`; full exact prior STATE snapshot `logs/simd-alu-state-pre-carousel-handoff-iteration108.md` (all complete I103–107 details). Last I107 condition: ideal scalar three-lag contraction uniform if normalized fresh per-stage η≤1.42317e−7, actual CKKS η UNVERIFIED, no paper defect.
- **PARKED only Nested-RNS primitive rotation/weight factoring I99–102**; archive `failures/nested-rns-small-weight-rotation-optimization-parked-iteration103.md`, full state `logs/nested-rns-state-2026-10-12-pre-simd-alu-handoff.md`.
- **PARKED PaCo scalar precision audit I95–98**; `findings/paco-precision-microaudit-parked-iteration99.md`, full state `logs/paco-state-pre-nested-rns-handoff-iteration99.md`.
- **PARKED RIG-HE** `logs/rig-state-2026-10-12-pre-vfhe-handoff.md`.
- **ARCHIVED GL generic BigSwitch** `failures/gl-generic-bigswitch-structure.md`.
- **ARCHIVED only expensive vFHE bounded-public-A + native Brakedown repair**, `failures/vfhe-bounded-public-A-direct-brakedown-repair-archived-iteration95.md`. **PRESERVE original vFHE CRT lookup soundness/correctness ideal-IOP gap** from ePrint 2025/286, in findings and full prior snapshot `logs/vfhe-state-2026-10-12-pre-paco-handoff.md`; not proven compiled SNARK forgery, not deleted.

STATUS: **ACTIVE Carousel I108 exact generic LUT rounding-threshold sufficiency counterexample PASS; I109 source scope check NEXT.** This may be a small missing assumption, NOT an attack or publishable correction yet.
