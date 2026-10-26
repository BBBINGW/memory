# FHE × MPC — Malicious Random-Bit Backend Replacement Gate

Date: 2026-10-26 (Asia/Singapore) | Stage: `PRESCOUT-FHE-MPC-05` (no official BOOT/SHIP/CGS resumption).
PI-authorized focus: examine whether *existing* maliciously secure MPC random bit sharing can replace Hwang's Discrete CKKS `BinBoot + Clean` collaborative-sampling backend. One primary hypothesis and cheapest decisive counterexample; STOP naive iteration.

## Status, strongest conclusions

- `FAIL_NAIVE_NOVELTY`: OT-based random shared bits, malicious arithmetic random bits and Boolean-to-arithmetic bit conversions (daBits/edaBits) are strong established prior art, not new FHE×MPC primitives.
- `FAIL_NAIVE_MODULUS_CONVERSION`: arithmetic bit sharing over Z_(2^k) does NOT automatically become valid Z_(q_out)-bit sharing by local reduction when q_out does not divide 2^k.
- `PERFORMANCE_UNRESOLVED`: no source-equivalent malicious security / arbitrary n, target q_out and same network+preprocessing benchmark versus Hwang's Hwang's `BinBoot+Clean`; cannot claim any native end-to-end speedup. The arithmetic-modulus mismatch is a deployment/cost issue with existing share-conversion solutions, not known new mathematical contribution.
- `DECISION: PARK_GENERIC_MPC_BIT_REPLACEMENT; VALUE_REVIEW; PIVOT_TO_PURE_FHE_PROBLEM_FIRST_SCOUT`. Retain a *possible engineering benchmark*, not a new crypto idea.

## Primary hypothesis / falsifier

Hypothesis: `The output of an existing malicious MPC arithmetic-random-bit protocol over Z_(2^k) can be used as a drop-in realization of the CKKS F_{n-ColSamp} modulo an arbitrary q_out, simply by locally reducing each party share modulo q_out, without any share conversion or distribution/security change.`

Source-independent counterexample: b=1, share r1=6 and r2=3 over Z_8, 6+3=9 ≡ 1 mod8. Reduce each share to Z_5: r1'=1,r2'=3; 1+3=4 ≠ 1 mod5. General identity: if Σ r_i = b + t·2^k as integers, after reduction mod q target Σ(r_i mod q) ≡ b + t·2^k mod q. When q∤2^k and unknown t nonzero, target sum is wrong. Correct cross-domain sharing needs compatible native modulus or explicit carry-aware conversion. **Not** an attack on SPDZ2k or Hwang; only falsifies a naive composition.

Further CRT caveat: independently generating unrelated Bernoulli bits in each CRT factor does not certify a *single* Z_q bit; need equality/coherence of per-prime residues. This is familiar source-compatibility work, not new.

## Primary-source prior-art and relevance

1. PI-supplied **Hwang et al., On the (In)security of Approximate Computation Protocols from CKKS** ePrint 2025/395, `papers/supplied/2025-395.pdf` Git blob `84710edb51998a1c9d50a8c306ec1970d8d389f5`: physical p15 Fig8 ideal `Fn-ColSamp` samples e~D and uniformly additive shares e in R_qout. Physical p16 §4.3 uses k≈log E+lambda shared random bits per coefficient (rounding/inclusive endpoints depend on exact distribution). Physical p17 Fig11 performs discrete CKKS `BinBoot+Clean` then `PRF` zero-share masks and distributed decryption. Single-thread Xeon 8268 benchmark: 2^16 BIT SHARES 33.96 sec, 2^18 135.84 sec, specifically measured only BOOTSTRAPPING+CLEANING. Thus no matched full MPC runtime, no robust conclusions from CPU-only numbers. Physical pp29–30 threshold variant chooses T then uses F_ThColSamp, semi-honest/hybrid security.
2. **Improved Primitives for MPC over Mixed Arithmetic-Binary Circuits**, Escudero, Ghosh, Keller, Rachuri, Scholl, CRYPTO 2020, https://eprint.iacr.org/2020/338 , https://iacr.org/cryptodb/data/paper.php?pubkey=30455 ; established malicious/active edaBits, bit-conversion and malicious preprocessing across thresholds. Not a paper specifically about Hwang's q_out smudging distribution.
3. **BarnOwl: Secure Comparisons using Silent Pseudorandom Correlation Generators**, Sameer Wagh, ePrint 2022/800, https://eprint.iacr.org/2022/800 ; malicious daBit/edaBit generation via silent PCG, **three-party with one corrupted (honest majority)**. It does NOT match arbitrary dishonest majority or same q and full Hwang runtime. PDF fetched as text via web, PDF screenshot cache miss, so rely on author ePrint landing abstract for security/model/performance claims, not visually audited exact per-table numbers.
4. **MP-SPDZ** project code + docs: https://github.com/data61/MP-SPDZ , https://mp-spdz.readthedocs.io/en/latest/readme.html . Available malicious dishonest-majority prime-field MASCOT and ring Z_(2^k) SPDZ2k, honest-majority protocols; docs explicitly discuss malicious edaBit preproc, batch/cost tradeoffs, `-B 3` requires >1 million to minimize amortized cost, plus security/communication tradeoffs. GitHub code search on default commit `113c4e47dd94bca9ecab029d2f0abe649bea5c52` found `Compiler/comparison.py` calls `sint.get_dabit()`, and `Protocols/MascotPrep.hpp` has bits-from-squares code: these are genuine implementation paths. Code search result does NOT establish Hwang-compatibility or exact output view distribution.
5. **Cao–Chatel–Knabenhans**, PI-supplied ePrint 2025/1845 `papers/supplied/2025-1845.pdf`: the actual malicious UC MGHE game involves `IND-CPApD`, `SIM-PDEC`, `Rob` and uncorrupted-server `IND-CIRC`. The above generic random-bit generator alone proves none of these, and malicious MPC `with abort` is NOT automatically `UC-MGHE` secure.

## Exact ideal-interface and cost gates needed for any engineering reopening

Desired for fresh each output: for each coefficient, secret bit b∈{0,1}, shares r_i∈Z_q distributed indistinguishably from `n-1` uniform shares and final balancing share with `Σr_i=b (mod q)`; for k bits, e=Σ 2^j b_j with prescribed D and independent across separate outputs. Simulator must cover corrupt-party auxiliary state (MACs, seeds), malicious bias/abort, required corruption threshold; nonuniform CRT carry and shape of output ring R_q matters.

`TotalCost` must include offline key/setup/PCG/OT-preprocessing + online rounds+bytes, native modulus/share conversion, malicious checks, mask/decryption transcript, memory, and integration in CKKS; equal ring degree N, batch bit count kN, n/t, q_out, lambda and error bound. Hwang's 33.96s vs BarnOwl/MP-SPDZ external results are NOT a head-to-head experiment (different threat model, hardware, output domain and measured scope). Pure HE SIMD trades expensive computation for low communication; generic MPC can reverse this tradeoff. No author-independent speedup figure.

The basic way to avoid modulus problem is *choose arithmetic backend native to q_out* (if q_out prime and supported) or use proven general share conversion; neither is novel by default. Ordinary edaBits are a **sufficient source of candidate shared bits after correct domain/view adaptation**, but not a proof of realizing Hwang's `F_n-ColSamp` with malicious-UC security automatically.

## End of Iteration

`STATUS: FAIL_NAIVE_MODULUS_CONVERSION + FAIL_GENERIC_NOVELTY`
`RESULT: established malicious bit-sharing alternatives exist; direct drop-in and fair cost unproved`
`NEXT_TEST: perform problem-first pure-FHE prior-art/source/cost scout; retain backend replacement as optional engineering benchmark only if PI reopens`
`STATE_UPDATE: THIS FINDING ONLY; NO OFFICIAL RESEARCH SERIES NUMBERING`
`CODEX: NOT_RUN`.
