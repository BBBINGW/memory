# CGS-19 — Published secure rounding is not an unchanged low-communication, zero-prestorage drop-in

Date: 2026-10-15. TRACK_ID=CGS. PI directly said continue this conversation's CGS research. Previous authoritative CGS-18; independent CGS-19, no SHIP/VFHE/global edits.

**STATUS:** FAIL **named direct substitution achieving both source-like online communication AND eliminating O(LDec) stored precomputed tables**. PASS source-specific exact accounting and source interface audit. UNCLEAR fundamentally redesigned cheap online MPC comparator or an actual secret-conditioned Gaussian PCF. **HUMAN_REVIEW/PARK this particular direct-port mechanism.** No actual secure MPC protocol implementation or impossibility theorem.

## One primary hypothesis and one cheapest decisive test

H-CGS19: The published CCS 2025 low-online-cost UC MPC rounding as-is, optionally generated on demand, can replace the secret-conditioned Gaussian in Okada–Takagi 2025/409 Algorithm 6 **without sacrificing its existing one-message/party PartDec online behavior and while eliminating LDec-proportional per-party prestorage** in a fixed N=4,T=2 example with one corrupt active participant and an honest/noncolluding semi-trusted Server.

Falsifier: audit source communication/round/preprocessing interfaces and compute exact per-session storage under a published, explicitly fixed scheme parameter set. If low-online-cost variant *consumes per-session preprocessed gates* and interactive variant requires new online MPC preparation and openings, the above *unchanged-drop-in* claim fails even if secret Gaussian sampling is sidestepped.

## Source-grounded exact interfaces [FACT]

- Okada and Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025/ePrint 2025/409, cached complete 40 physical pages SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301, VERSION_UNVERIFIED. Physical pp17–20, Definition 4.2, Algorithm 3, and p26 Algorithm 6: the honest noncolluding semi-trusted Server runs a ciphertext-sanitizing ServerDec and provides c_dec and sid; each active Pi then computes pdi = lambda_(act,i) (a^T s_i + zeta_i^(sid)) + PRF(seed_i,sid) mod q, a single local output in Z_q. Any T out of N active parties reconstruct using Shamir. As per pp4,26, one fresh distributed scalar Gaussian pad and one Shamir field share per sid are precreated for LDec sessions. The Server must not receive parties' PartDec shares under the original noncollusion assumption. Source Def5.4/Thm6.3 simulation security includes the exposed partial decryptions, not just plaintext correctness. Server's sanitization / simulation assumptions remain in place if we change only PartDec.
- Zyskind, Zarchy, Leibovich, Peikert, *High-Throughput Universally Composable Threshold FHE Decryption*, ACM CCS 2025/ePrint 2025/1781, complete mirror 15pp SHA256 021598c3e42400aca7ecfae83889925027f98a4b0c0cae823168cf68beba22e9, VERSION_UNVERIFIED; §3.3 pp6–7, §3.4 p8 Eq(5). Their `F_ABB`/SPDZ2^k example already solves secret secure comparison via preprocessed Sign and ModLTZ gates. Published normal online protocol has **three sequential ABB opens** (possible pipelining changes network broadcast rounds) and specified total online open payload **656 bits per party excluding commitments**; it spends fresh **consumed** preprocessing per decryption. It is not one local message per party. Their own UC theorem belongs to their security model/ABB realization, not immediately to this server-mediated Alg6 relation or transformed prime q.
- Hu et al., *Ajax: Fast Threshold Fully Homomorphic Encryption without Noise Flooding*, USENIX Security 2026/ePrint 2025/1834, complete mirror 51pp SHA256 945802ad74006fb3890b567c527310baf8e5b109b5af670acd43259859fd69be, VERSION_UNVERIFIED; pp5–6,16–18; cross-ring `FDoubleRings` mask-then-open needs offline per-decryption double sharings, an additional interactive opening, and (in its native protocol) a negligible-wrap correctness condition rather than CGS18's ideal private carry. Ajax targets a different active-party/security functionality; not a drop-in.
- Okada–Takagi *Threshold FHE with Short Decryption Shares Without a Semi-trusted Server*, ACISP 2026/ePrint 2026/957 has verified publication/title/abstract online (ACISP pp166–193) but Research MCP original full-text retrieval BLOCKED (ePrint HTTP403 + fixed mirror missing). Do NOT assert novel relation or lack of similar technology until original §protocol is read.

## One exact numerical / round-interface gate [DERIVATION]

Fix **N=4, T=2**, so any two may be active and corruption of one active participant is a dishonest majority among the active. Original model additionally assumes honest noncolluding semi-trusted Server. This is a boundary case useful for testing; security equivalence with CCS malicious ABB is NOT established.

For the precise published CCS 2025 `k=64, message_bits m=1, ell=63, b=8, d=ceil(ell/b)=8, b'=7, MAC s=64`:
- Sign gates have `(d-1)2^b + 2^b' = 7*256+128 = 1920` table entries, ModLTZ `2^(d+1)=512`; **2432** per-decryption entries.
- Unauthenticated gate table bits `(d+1)*1920 + m*512 = 17792`.
- Including authenticated value and MAC shares under *this exact SPDZ2^k cost model*, Eq(5) gives `2*((d+1+s)*1920+(m+s)*512) = 346880 bits = 43360 bytes = 42.34375 KiB PER PARTY PER SESSION`. The paper says it is CONSUMED on each Decrypt.
- Online opened payload `2*(ell+(d+1)+k+3*s)=2*(63+9+64+192)=656 bits per party EXCLUDING commitments and any interactive prep.
- To have all these tables pre-generated for `LDec=1e6`, per-party gate payload is **43,360,000,000 bytes**, approx **40.381 GiB**, before uncounted protocol buffers/keys.
- In original Algorithm 6, per-party padding secret-share storage is `LDec*ceil(log2(q)/8)` bytes (plus secret/key/setup and nonpadding effects). FOR ILLUSTRATION ONLY assuming `ceil(log2(q))=64/128/256` bits, baseline padding share bytes are `8/16/32 MB` for LDec=1e6, so fixed-source CCS gate-data ratios are `5420/2710/1355` respectively. These q widths are not claimed to be proven 128-bit-secure Okada instantiations.
- Source-original `PartDec` sends ONE q-element share (nominal bq bits) after ServerDec; source CCS protocol needs 3 ABB opens and 656bits/party not counting commitments. At illustrative q width 64 bits, that is 10.25x the basic per-party payload of one 64-bit share, but **not apples-to-apples**: distinct cryptosystem moduli, threat/verification/ServerDec models, session coordination and cryptographic setup.
- On-demand generation removes **persistent session-table storage** only if an online MPC/OT engine creates fresh tables when needed. That necessarily invokes extra online steps for THIS concrete CCS gate-generation protocol; no mechanism/proof is supplied that all those entries arise from small standalone seeds without interparty communication. It might be acceptable under another functionality, but then not a direct drop-in preserving source's one-message PartDec.

Reproducible exact integer cost script: `/mnt/data/cgs19_gate_check.py` SHA256 `7e2fa46ed69778601cfa59b5a69bbffcd4fa4345a1ec0e7e3d56a84a58849340`; JSON `/mnt/data/cgs19_cost_gate.json` SHA256 `5b993bd1c4baea6146917eb15720cd3e52293370f2e38bd02df3fb1e5da3012f`. Formula checked via assertions against published 17792,346880,656.

## Synthesis gate and next target

**What was killed:** naive belief that published MPC-rounding removes the CGS LDec dependence *and retains original small-online single-response interface for free*. We did NOT rule out:
(a) lower-cost on-demand secure comparison under a different latency/communication budget;
(b) dynamic online PCG/OT with O(1) long-term key state but per-query communication;
(c) a new truly noninteractive, secret-conditioned seed correlation that retains the original interface;
(d) a stronger theorem for amortized/batched decryption.

**Research conclusion:** Known primitives solve the *noise removal* functionality if interactions and fresh MPC correlations are allowed, but they do not solve the **original** low-communication O(LDec)-free objective. Treat fixed published gate port as **PARK** pending an explicit new lower-cost mechanism. It is not a new contribution and source security/parameter upgrades cannot be assumed.

**Suggested CGS-20 (ONLY with PI continuation):** One *new* source-grounded architectural hypothesis, rather than another generic rounder: can a strictly compact reusable correlation key plus ONE source-compatible PartDec response realize the **jointly simulatable secret-conditioned residual law** without offline per-session padding? Explicitly give the transcript functionality and a minimal two-secret/two-session attack/proof test, and check recent original author 2026/957 text first if available; otherwise source-gate originality. This is an independent new primitive attempt, not an automatic claim it exists.

**END:** STATUS FAIL direct-port dual-objective / PASS exact source cost/round falsifier / UNCLEAR lower-cost new mechanisms / HUMAN_REVIEW. RESULT published same-bits comparator is a complexity/functionality tradeoff, not a cost-free source repair. NEXT_TEST pick one new reusable-key correlation hypothesis with explicit simulator/interface or first obtain 2026/957. STATE_UPDATE YES only CGS.