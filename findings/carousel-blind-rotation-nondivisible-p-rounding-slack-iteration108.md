# Iteration 108 — Carousel generic blind-rotation error threshold omits nearest-integer phase rounding slack when p does not divide N

Date: 2026-10-12. Target Intak Hwang, Seonhong Min, Yongsoo Song, *Carousel: Fully Homomorphic Encryption with Bootstrapping over Automorphism Group*, IACR ePrint **2024/2032**, https://eprint.iacr.org/2024/2032. Research MCP full 34-physical-page primary mirror PDF SHA256 `5ddec99ebbe14b270b413e21ab4923abf0ed5dba8d0f1d053b3fde1c5a35d6c8`, source GitHub mirror revision `a64684fee3625e3f99908d13abe0e065015f52db`, official latest VERSION_UNVERIFIED.
STATUS: **PASS** one exact arithmetic counterexample to a GENERAL sufficient bound stated in the technical overview, and a sharp simple algebraic amendment. **UNCLEAR** novelty / implementation risk / whether a separate unstated convention implicitly restricts p|N. **NOT** verified cryptographic attack or actual parameter failure.

## Read before write / choosing a distinct gap
Read live GitHub Notes `AGENT.md`, `RESEARCH_PHILOSOPHY.md`, `STATE.md` ending I107 and corresponding final finding. PI replied '好的，请继续' to I107 suggested option B to park narrow SIMD ALU scalar audit; snapshot `logs/simd-alu-state-pre-carousel-handoff-iteration108.md` and archive `failures/simd-alu-a2b-cutoff-scalar-microaudit-parked-iteration108.md` separately. Tried candidates ePrint 2025/066 (metadata unavailable due non-padded input) and ePrint 2024/2032, 2020/1549; ONLY new Carousel target 2024/2032 selected for this single technical hypothesis. Original full pages 1–5,6–8,9–16,17–25,26–29 inspected, especially full functional recovery derivation.
[FACT/source] Physical p4, technical overview, after modulus switching to N: `hat b+<hat a,s> = round((N/p)m)+e (mod N)` and states `|e|<N/(2p)`. It sets `v_i=f(round((p/N)i))` for i=0,...,N−1 and asserts `v_[round(Nm/p)+e]_N = f(m)` **regardless of input**, without stating p|N in that passage. Original §3 p12–13 Algorithm1 output extracts `v_[hat b+<hat a,s>]_N` (LUT indexing); §4.2 Theorem4 p23 supplies output expression in terms of rotated LUT and variance rather than separately supplying a general p-nondivisibility rounding slack bound.
[FACT/source] §3.2 physical p14–15 decomposition ring construction uses an odd prime cyclotomic degree M and underlying base prime p0 with order o modulo M, N=(M−1)/o, and plaintext modulus p=p0^r. §5.1 physical p26 author **actual practical experiments** use M=65537, base prime p0=2, N=2048 and plaintext p=2^2,2^3,2^4, so p DIVIDES N in implemented parameters. No claim of breaking these.
[FACT/source] Earlier source passages do not explicitly require p|N universally in the technical overview; however, a complete paper-wide formal assumption audit would be needed before claiming an original theorem false rather than a shorthand that presupposes a divisibility parameter choice.

## One hypothesis / cheapest falsifier
[HYPOTHESIS] The asserted `|e|<N/(2p)` alone suffices to ensure `round((p/N)(round(Nm/p)+e)) ≡ m mod p` for all plaintext m and decomposition-ring-legal parameters, even when p does not divide N.
[FALSIFIER] Find odd prime M with plaintext prime-power p, `o=ord_M(p0)`, `N=(M−1)/o`, N≥p, p∤N, an m, and a strictly-bounded integer e that causes actual LUT lookup index ≠m, with **NO half-integer nearest rounding ambiguity**.

## Small exact parameter-consistent witness [DERIVATION/PASS]
Take cyclotomic degree M=829, which is PRIME; base and plaintext prime p0=p=5; `ord_829(5)=9` (check 5^9≡1 modulo829 and no lower positive exponent), so `N=(829−1)/9=92`. This respects the decomposition-ring automorphism/index algebra and N≥p, though has NO quantified RLWE security.
Take message m=1 and net switched-phase additive integer error e=−9:
- intended ideal phase Nm/p=92/5=18.4 and rounded first phase `round(18.4)=18`, initial rounding discrepancy δ=18−18.4=−2/5.
- stated noise threshold N/(2p)=92/10=46/5=9.2. `|e|=9<9.2`, strictly PASS.
- switched phase modulo N: `[18−9]_{92}=9`. LUT identity function f(j)=j maps it to `round(p·9/N) = round(45/92)=0`, versus required f(m)=1. No tie at either rounding.
Thus a valid input to the exact stated phase/LUT equations satisfying the stated threshold yields INCORRECT OUTPUT at the algebraic phase-recovery level. Note this does **not** construct a malicious RLWE ciphertext or prove the distribution of actual noise e assigns appreciable mass to −9. The net e is treated as the small post-switch error explicitly allowed in the paper's equation.

## Exhaustive check and author parameter control [TEST]
A deterministic Python3 `fractions.Fraction` nearest-half-up test with all plaintext m and all integer e satisfying `2p|e|<N`, for M829,p5,N92:
- 95 valid ordered (m,e) pairs, **3 failures**; two have non-tie final rounding. Examples (m=1,e=−9)→0, (m=4,e=9)→0 (expected4), both tie-free. One other failure uses an exact halfway final rounding and is explicitly NOT required for the decisive result.
- Secondary M127, base prime2, plaintext p8, `ord_127(2)=7` and N18; 24 valid pairs, 6 failures; source-consistent p0=2,r3.
- **ACTUAL AUTHOR PARAM CONTROL** M65537, p0=2, p=16, ord_65537(2)=32, N2048 (p|N). All 2032 possible m/e pairs with `|e|<64` recover exactly, **0 failures**. Important: the ring order uses BASE prime p0=2, not p16, which was fixed in the test harness when initial assertion noticed this; prevents spurious counterexample from wrong N. For p4,p8 same p|N property.
The "exhaustive" claims cover the 1D integer LUT-index model only, not RLWE encrypted evaluation, noise distributions, security/failure probability.

## Tight sufficient correction [DERIVATION]
Let `δ_m=round(Nm/p)−Nm/p`, always |δ_m|≤1/2. The (unwrapped) LUT input argument after inverse scale equals
`p/N [round(Nm/p)+e] = m + (p/N)(δ_m+e)`.
Therefore a simple **message-wise strict sufficient condition** for nearest-round decoding (with circular modN boundary handled modp) is
`|e+δ_m|<N/(2p)`.
Uniform over all m, sufficient
`|e|<N/(2p)−max_(m in Z_p)|δ_m|`.
For M829,p5,N92 the max absolute δ is 2/5, hence uniform bound becomes **44/5=8.8** rather than 46/5=9.2. If p|N, δ_m=0 all m and original threshold is valid. More generally a conservative universal correction is `|e|<N/(2p)−1/2` whenever RHS positive; precise arithmetic can be less restrictive.
This is a condition on **post-modswitch net e**, not a new RLWE correctness theorem; authors must also show their error tail fits whichever strict bound chosen.

## Scientific judgment / novelty gate
[CONFIRMED LIMIT] The technical-overview chain 'small error |e|<N/(2p) => full-domain LUT returns f(m) regardless of m' is **not valid without extra divisibility or rounding slack**. This appears to be a legitimate generic-scope correction, not source code exploit.
[NO AUTHOR PARAM BREAK] Their p2^2,p2^3,p2^4 / N2048 all divide, so no error appears for their measured regimes. This limits practical importance. Theorem4 explicitly expresses rotated LUT output, and source global theorem can remain algebraically correct while introductory f(m) inference needs extra assumption.
[UNKNOWN] Whether certain field/noninteger slot-encoding structural conditions silently force p|N (not obvious in §3.2; the witness M829,p5 supports prime cyclotomic factorization algebra), and how actual LWE error distribution/failure parameters interact with the narrow 0.4 difference. No verified failure at 128-bit parameters or security attack. No novelty or publication significance established.
[RECOMMENDATION] Do not overinvest in a mere rounding correction. One follow-up can check the **actual paper theorem/algorithm assumptions and source parameter generation**: does anything require p|N or reduce e so that the tighter slack automatically holds? If explicitly required, kill "gap" and archive as intended parameter restriction; if not, classify only a technical correctness scope nuance and quantify whether any meaningful parameter set is impacted. PI judges whether worth deeper work.

## Reproducibility
Executed exact script `/mnt/data/iteration108_carousel_rounding_boundary.py` SHA256 `a4c4bd1e3289d13c153c7fbd8b8753f69ae8fd1a6c499cf286994358d0f5ebec`.
JSON results `/mnt/data/iteration108_carousel_rounding_boundary_results.json` SHA256 `026e8107d8563c2af96562df3d67a1524158d64d59e1103b52b78bcd06a7aaaf`.
Script asserts prime M, multiplicative order, N rank, strict bound and tie-free witness; runs exact integer enumeration with Python Fraction. Actual benchmark ring uses base prime2 order32 for p16, corrected in harness after detecting dimension mismatch.

## End
STATUS: **PASS** exact arithmetic counterexample under paper-generally-described parameters; **UNCLEAR** materiality, authors' global formal assumption and implementation impact.
RESULT: Need p|N or additional δ_m rounding margin; original simple noise threshold is not generally sufficient.
NEXT_ACTION (I109): One cheapest source-to-source audit: check §3.1 Algorithm1, §3.2 construction, §4 Theorem4, §5.1 selected parameter restrictions and pinned code `SNUCP/carousel` (if publicly available), for **explicit invariant p|N** or a stricter switched phase noise budget. Avoid another arbitrary sweep / attack claim. If intended assumptions already force it, mark FAIL novelty/scope; else preserve as limited generalization boundary with no source attack.
STATE_UPDATE: YES. No author email/contact/outreach or public disclosure.
