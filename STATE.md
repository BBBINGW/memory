# FHE Research State — After Iteration 171

**Checkpoint:** 2026-10-13; `main`; **I171 COMPLETED, I172 NOT STARTED**.
**Research authority:** Human is PI and decides research direction, contribution, final pivot/park. Agent follows `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md`; exactly ONE smallest falsifiable technical hypothesis, ONE cheapest decisive test, classify evidence, record END OF ITERATION, then stop. Historical full project record `logs/state-pre-session-handoff-2026-10-13-iteration151.md` and `findings/OPEN_RESEARCH_BRANCHES.md`; current concise state does NOT erase archived iterations.

## CURRENT TARGET

**SHIP CKKS bootstrapping selector-key memory vs throughput/latency frontier — OPEN / HUMAN_REVIEW after I171.** Authors Jung Hee Cheon, Guillaume Hanrot, Jongmin Kim, Damien Stehlé, *SHIP: A Shallow and Highly Parallelizable CKKS Bootstrapping Algorithm*, IACR ePrint **2025/784**, https://eprint.iacr.org/2025/784, Research MCP complete **33-physical-page GitHub mirror** SHA256 `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742`, official version **VERSION_UNVERIFIED**. Original source §3.3 pp16–17; §§4.1,4.4 pp17–18,21–22; §5.2 Table2 p24–25; §5.4 Table3 pp25–26. **I171 calculates explicit literal high-modulus full RLWE mask selector storage**, not measured author HEaaN RAM, no security or correctness flaw, no memory-saving algorithm yet. The source explicitly mentions memory optimization via four-mask algebraic sums, and text Algorithm4 describes opposite split direction from implementation, so distinguish true θ from N/θ.

**Previously closed/parked on PI assent:** I170 ePrint **2024/164** BGV Hom-NTT no-free-depth-collapse (source §4.1 already addresses sparse-vs-depth); I168–I169 Yan et al. **2025/1403** dynamic AKS public basis-key linearity (ordinary RLWE linear sum extra noise/rounding, no measured win); I167 unpacked AHE 2025/711 Alg3 notation (source code correct); I165–I166 TFHE HFP 2025/257 generic covariance (author expressly assumes independence, no real harmful DAG); I160–I164 Min et al. CKKS 2025/429 p1-only weighting (only 3.5% ideal d53/d25 source-shape sampled error improvement); I156–I159 SPRU CKKS 2025/651 key-switching rounding (zero unconditional new incremental bias in 1P/1Q toy). All older failures remain as indexed.

**Older OPEN / SOURCE-GATED:** Cascudo et al. vFHE ePrint **2025/286** P1 ideal PIOP CRT scalar digit equality finding I59–I60 remains *HUMAN_REVIEW/SOURCE-GATED*, latest official revised Feb2026 full PDF bytes unavailable; no present-edition bug or compiled exploit proven. MRFHE 2026/853 source experiment blocked by non-power-of-two custom Lattigo fork; old alternative repairs archived; missing details in `MISSING_SOURCES.md`. No author outreach or public disclosure without PI.

## LAST COMPLETED ITERATION

**I171, 2026-10-13; I172 NOT STARTED.** Finding `findings/ship-ckks-column-selector-key-material-envelope-iteration171.md` blob `8fe892b3a9ee72a82cfa051d26cad4553a6114bd`. ONE SOURCE PARAMETER-BASED KEY-MATERIAL GATE. In actual source §4.4 Algorithm4 four masked-selector ciphertexts per column candidate per sparse-secret position, implementation uses reversed stage order compared to text (noted by authors p22), so `column width θ` from Table2 (p25) rather than mux width `ℓ0/θ`. With h=31 (p24), literal `4hθ` full-level encrypted RLWE ciphertexts and source `log2PQ`, modulus prime-tower count, `N`:
- **LL13**: N8192, logPQ218, θ6, 9 primes →744 ciphertexts; independent densely-bit-packed RLWE payload **0.3094GiB** or 64-bit-RNS 9-tower payload **0.8174GiB**; authors’ actual precision4.45bit, 32-core latency215ms.
- **LL14**: N16384, logPQ437, θ9,10 primes →1116 ciphertexts; bitpacked **1.8604GiB**, RNS **2.7246GiB**; authors’ actual precision16.9bit, latency333ms.
- **HT14**: N16384, logPQ438, θ9,18 primes →1116; bitpacked **1.8647GiB**, RNS **4.9043GiB**; authors precision4.55bit, latency1.09sec.
- **HT15**: N32768, logPQ881, θ17,20 primes →2108; bitpacked **14.1689GiB**, RNS **20.5859GiB**; authors precision18.1bit, latency1.63sec.
Formulas: `count=4hθ`, `bitpacked_bytes = count*2*N*log2PQ/8`, `RNS64_bytes=count*2*N*(# full prime limbs)*8`. ALL these numbers are **conditional RAW DATA ENVELOPES for independently stored, dense, highest-PQ RLWE ciphertexts**, not measured memory, not information-theoretic compression lower bounds; may shrink through authors' acknowledged mask sum relations, seeded first components, level-specific key parameters, streaming/on-demand, different implementation. Do NOT infer actual HEaaN peak memory or claim authors ignored storage. No evaluation of security / performance; no source-code execution.

**Status:** **FAIL** hypothesis that literal full-PQ high-precision LL14/HT15 selector payload fits under 1GiB; **PASS** exact paper-parameter conditional cost calculation; **UNCLEAR** actual original implementation key size, true memory bottleneck and novel compression. Distinguish author's original performance as *source-reported*, not measured in this iteration.

## CURRENT QUESTION

Do the SHIP **actually implemented** masked-selector keys at LL14/HT15 retain multi-GiB uncompressed equivalent payload after authors’ mask sharing / actual prime levels / possible seeded data structures, and, if so, can a nontrivial compression improve key storage at **fixed** CKKS correctness, noise, security, depth, latency? No such scheme established, **no active technical hypothesis after I171**.

## PRIMARY HYPOTHESIS

**NONE ACTIVE.** I171 only ruled out sub-1GiB high-precision selector component for literal full-PQ independently stored dense key layout. Not a claim of universal minimum or actual author-code memory. New claim must be grounded to code or explicit algebraic key object and test an actual source-equivalent bottleneck.

## CURRENT EVIDENCE

- **[FACT original source]** SHIP ePrint 2025/784 §3.3 four masks, sum relation explicitly noted as storage-saving; §4.4 Algorithm4 keys `M^{(k)}(j)`, four per candidate j' and sparse secret position; the authors' implementation reverses written hybrid order, so Table2 θ counts **column**, not mux size; §5.2/5.4 source N/PQ/h/precision and runtime. 33pp mirror SHA `3e8deccd8bd5f3845a82baa56c90fbe03fbbe8a7e96844092d4d0f57cba80742` version unverified. No author HEaaN source artifact inspected.
- **[DERIVED I171]** Exact integer key count / bitpacked and native 64-bit RNS payload for LL13/LL14/HT14/HT15 under independent full-PQ storage as above; high precision LL14 and HT15 exceed 1GiB. This is a meaningful possible key-memory resource challenge, not a new algorithm.
- **[FACT prior source gates]** See I170 `findings/bgv-hom-ntt-full-layer-collapse-diagonal-fillin-iteration170.md` for exact 16×16 dense CRT; source treated level-depth tradeoff. I169 `findings/ckks-lcr-aks-public-basis-key-synthesis-roundoff-noise-iteration169.md` public basis eval-key addition only approximate with rounding/noise; parked. I164 `findings/ckks-generalized-composite-source-shaped-p2-dominance-iteration164.md` weak source-shape p1-only benefit; parked. I166, I159 source-specific archives intact. vFHE and MRFHE P1 blocked as above.

## MAIN OBSTRUCTION

Source key layout may be compressed/hoisted, and Table2 “log PQ” need not coincide with storage modulus of every individual selector in optimized implementation. Independent full ciphertext bitpacking is a **conditional resource floor only for that literal layout**. Authors explicitly acknowledge mask memory reduction; ordinary seeded ciphertext compression may halve stored RLWE material, but no new scheme or verified HEaaN RAM size exists. At least one actual key format/source code or concrete raw-key export is needed before claiming a resource bottleneck or proposing published improvement. Generic 4hθ arithmetic alone is elementary.

## OPEN UNCERTAINTY

Actual SHIP vs Poulpy implementation equivalence, per-key RNS levels, initialized selector-mask sharing, number of ciphertexts resident vs streamed, seeded first components, memory bandwidth vs computation, frequency of bootstrap calls, whether material savings have independent novel structural basis, error/precision and latency after compression. Source official version unverified.

## NEXT_ACTION — UNIQUE GATE FOR NEXT ITERATION

**I172 ONLY upon PI “继续”: one real key-layout falsifier.** Look for available **pinned, verifiable implementation** of SHIP masks / selector keys (author HEaaN if accessible, otherwise third-party `Poulpy CKKS SHIP` clearly marked independent) and inspect *exact* stored selectors count, per-key actual modulus limbs / key format, memory allocation and/or emitted size. Compare source-derived `4hθ` raw envelopes. If masked key storage is already compressed enough to kill concern, PARK quickly; if it persists, identify ONE source-compatible compression candidate with measured or provable key bytes and no more online time/noise/depth. **Do not conflate third-party SHIP with original author's measured 215ms/333ms/1.63s, or invent author private code.** If no actual source can be verified, record SOURCE GATE instead of further toy param sweeps. No more BGV dense FFT / AKS textbook RLWE sums / HFP covariance or old archived variants.

## RELEVANT FILES — NEW CHAT READ ORDER

1. `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → `STATE.md`.
2. `findings/ship-ckks-column-selector-key-material-envelope-iteration171.md` — active resource envelope and formula.
3. Original ePrint2025/784 §3.3–§5.4 pp16–27, Table2 and Algorithm4 as needed.
4. `findings/OPEN_RESEARCH_BRANCHES.md` — opportunity index, not authority. Older failures and `MISSING_SOURCES.md` only if sources actually needed.
5. I170, I169, I164 archives only when explaining why parked.

## STATUS

**I171 CLOSED: FAIL under-1GiB high-precision SHIP literal selector-layout hypothesis / PASS source-level exact conditional raw key-memory envelope / UNCLEAR actual author HEaaN memory and publishable improvement. I172 NOT STARTED.** Prior BGV HomNTT free-collapse I170 now PARKED by PI assent. Other listed archives remain parked; vFHE P1 OPEN/SOURCE-GATED. No claims of author bug or practical key-memory superiority.
