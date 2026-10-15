# CGS-18 — Cross-ring masked carry correction as an on-demand alternative to Gaussian padding

**Date:** 2026-10-15; **TRACK_ID: CGS only**. Last complete before this: CGS-17. No unrelated states/global metadata modified.
**STATUS:** PASS **algebraic toy and perfect public-mask marginal**; **KNOWN PRIOR ART** (Ajax / Zyskind et al.); full Okada–Takagi security, arbitrary-threshold efficiency, unbounded-session storage and novel advantage **UNCLEAR / HUMAN_REVIEW**.
**No claim** of a new primitive, complete working ThFHE, proof of original source flaw, or an implementation benchmark.

## Primary hypothesis and one decisive test

**H-CGS18 (narrow algebraic PASS):** In the ideal secret-sharing / private-comparison setting, if an LWE decryption residual is shared as `u = Phi*m + e (mod eta)`, where `eta = Phi*P` and the centered integer noise satisfies `|e| < Phi/2`, then a **fresh uniformly masked low-residue opening** plus a **private carry-comparison bit** removes `e` exactly without generating a secret-conditioned Gaussian pad and without a negligible-wrap requirement on `Phi`. The opened masked residue is uniform independently of `e,m`.

**ONE cheapest decisive test:** Exhaustively enumerate a toy `eta=64, P=4, Phi=16, m=0..3, e=-7..7, r=0..15`, verify the corrected integer lift and reconstructed plaintext for all cases, and check uniformity of the masked opened residue. This is NOT a protocol security test.

## Source-level prior art and interfaces [FACT]

1. **Okada–Takagi**, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025, ePrint **2025/409**, primary cached full 40 physical pages, PDF SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`, VERSION_UNVERIFIED. Algorithm 6 physical **p26** precomputes `LDec` many `zeta(sid) ~ D_{Z, sigma0 sqrt(Bpub^2-||s||^2)}` and Shamir-shares them; `PartDec` p26 is locally computable per active party using `lambda_act,i (a^T s_i + zeta_i(sid)) + PRF_i(sid)`. Lemma 6.1 p26 and Theorem 6.2 p27 establish source-dependent distribution/correctness. Removing `zeta` invalidates its original proof, not the validity of any other protocol's proof.
2. **Hu et al.**, *Ajax: Fast Threshold Fully Homomorphic Encryption without Noise Flooding*, USENIX Security 2026 / ePrint **2025/1834**, full original-source mirror 51 pages, PDF SHA256 `945802ad74006fb3890b567c527310baf8e5b109b5af670acd43259859fd69be`, VERSION_UNVERIFIED. Physical pp**5–6**, section 4.3 / Figures 10–12 pp**16–18**: double additive shares of a random value `r` over rings with `Phi | eta`, mask `e` modulo `Phi`, publicly open, re-lift using the `eta` sharing. Explicit probability of uncorrected wrap `|e|/Phi`; uses offline per-session double sharings. Baseline original q may be prime: Ajax uses an additional modulus-switch to divisible eta and analyzes introduced noise, NOT a cost-free syntactic drop-in.
3. **Zyskind–Zarchy–Leibovich–Peikert**, *High-Throughput Universally Composable Threshold FHE Decryption*, ACM CCS 2025 / ePrint **2025/1781**, mirror PDF 15 physical pages, SHA256 `021598c3e42400aca7ecfae83889925027f98a4b0c0cae823168cf68beba22e9`, VERSION_UNVERIFIED. Physical pp**3,5–8**, especially §3.3 **p7**: masked opening and secret secure comparator `u = (z' < r)` enable exact MPC rounding without flooding. §3.4 **p8** discloses one-time preprocessed Sign/ModLTZ gates: for their example, **346880 bits (~42.34 KiB) of party-local gate storage PER DECRYPTION**, not 346880 bytes; gates are consumed. The paper has a UC-security claim for its own MPC functionality/model, not for a composed version of source Okada–Takagi.
4. **Same authors' 2026 ePrint 2026/957** (Short Decryption Shares without a Semi-trusted Server) identified, but reliable full original text retrieval remained SOURCE_BLOCKED (IACR 403 and no mirror). No claim on whether this follow-up solves the present LDec issue. Research may need PI supplied source before a claimed novelty result.

## Exact masking and carry identity [DERIVATION]

Let `P` denote plaintext modulus to avoid overloading source auxiliary primes. Work in `Z_eta`, `eta=Phi*P`; `m in Z_P`; `u=Phi*m+e mod eta`, with `|e|<Phi/2`. A qualified active subset must hold a **secure additive sharing** `[u]_eta`; ability to convert existing Shamir shares securely is assumed, not proved.

- Generate fresh secret-shared `r` **uniform over `{0,...,Phi-1}`** with consistent representations `[r]_Phi,[r]_eta` (Ajax's *double sharing*). No party adversary may know the full `r`.
- Open `v=(u mod Phi+r) mod Phi = (e+r) mod Phi`. Because r is uniform and independent, `v` is uniform over `Z_Phi` for every fixed `e,m`. This is unconditional for the opened scalar alone, not a corrupted-party/full-transcript proof.
- Privately compute `d=v-r` as an INTEGER using shares of `r` and public `v`. Then set the shared correction `c = 1{d < -Phi/2} - 1{d > Phi/2}`. The assumption `|e|<Phi/2` makes the desired centered residue unique. Consequently **`e=d+c*Phi` exactly** even when the original mask addition wrapped.
- Reconstruct shares `[e]_eta = v - [r]_eta + Phi*[c]_eta` and `[Phi*m]_eta=[u]_eta-[e]_eta`. Only the plaintext is released to the authorized receiver. Computing `c` privately requires a **real secure comparison / MPC**, not a locally linear function of Shamir shares.
- Without `c`, Ajax's direct centered-lift mismatch probability is `|e|/Phi` for uniform r when `|e|<Phi/2`; polynomial Phi does not yield negligible 2^-lambda error for `|e|>=1`. The additional private comparator removes THIS arithmetic wrap failure, not errors from previous source modulus switching or excessive FHE noise.

**Toy proof-of-concept:** `/mnt/data/cgs18_masked_carry_toy.py` SHA256 `c519b17797504d5add04e0fbf2eab5be9690b7f63db7e08a3820ab92eb3b855b`; JSON `/mnt/data/cgs18_masked_carry_results.json` SHA256 `2a00caa4ccb63daf7feace532798da634ac92a8ae9f050cb48e3946d880c4186`. Exhaustive **960/960 corrected pairs PASS**, **224/960 naive no-carry failures**, and public `v` exact uniformity for all 60 (m,e) pairs (**0 nonuniform cases**). This is a tiny integer arithmetic witness only: it tests no Shamir/MPC/corruption security or modulus-switching precision.

## Constructive synthesis / barriers [DERIVED + OPEN]

This line changes the functionality from sampling key-conditioned Gaussian to removing error *before opening*; it thereby avoids having to solve the Gaussian PCF problem in the **modified, interactive protocol model**. This does **NOT** supply a nonce-only substitute for original Algorithm 6, whose part-decryption is ONE local share message, has a semi-trusted noncolluding Server interface and a specific adaptive simulator.

At least four unresolved interfaces:

1. **Round / functionality mismatch.** A secure comparison requires interparty MPC beyond original `PartDec`; source supports arbitrary qualified T-of-N sets with active-set Lagrange weights. Need instantiate secure comparisons for worst-case T-1 corrupt within selected subset and check server-collusion/noncollusion, session scheduling, output-to-receiver, and adaptive repeated queries. CCS2025 security proof can help but is NOT automatically portable.
2. **Preprocessing merely moved, not eliminated.** Ajax fresh double sharings and CCS 2025 Sign/ModLTZ tables are consumed per decryption. They do not eliminate O(LDec) *precomputed material* if kept offline. Online on-demand PCG/OT/MPC might achieve persistent setup keys independent of LDec but adds interaction/communication; this is **conditional generic MPC feasibility, not new PCF/construction or established complexity win**.
3. **Modulus/representation mismatch.** Original Alg6 uses prime q and sanitized ServerDec ciphertext; `Phi|eta` ring adjustment/rounding must preserve original correctness and standard LWE-based security. No exact Okada Algorithm6 end-to-end parameters or simulator demonstrated.
4. **Prior art/novelty.** Mask-and-open, double-ring sharing, private comparator, and generic MPC rounding are known (Ajax, CCS2025). Any paper must identify a genuinely **new FHE-specific interface, algorithmic optimization, lower-cost on-demand comparison or theorem** beyond these sources and beyond 2026/957 once accessible.

## Scientific interpretation and suggested one next decisive gate

**CGS-18 STATUS: PASS narrow arithmetic; FAIL novelty of a bare masked-carry primitive; UNCLEAR actual ThFHE and O(LDec)-free low-communication improvement; HUMAN_REVIEW**. The Gaussian-correlation generation open problem itself remains unsolved; this is an **alternative design branch**, not a cryptographic repair of the published 2025/409 protocol.

**NEXT_ACTION CGS-19 (only on PI continuation):** Fix one **T,N, threat model and original Algorithm6 ServerDec/PartDec interface**, and compare (a) ORIGINAL one-message/party Gaussian pre-sharing, (b) published CCS2025 preprocessed rounding, (c) an **on-demand no-prestored-table secure comparator** with fresh correlation generation. Test ONE precise end-to-end online communication/round and storage inequality; include setup/OT assumptions and full memory-vs-communication accounting. Kill the branch if generic published MPC dominates or original low-communication requirement cannot be retained. Do not claim novelty on the strength of this CGS18 algebraic PASS or launch unrelated SHIP/VFHE tasks.

**STATE_UPDATE:** YES, CGS-only. **Novelty:** NOT VERIFIED for any hybrid; constituent method PRIOR ART.
