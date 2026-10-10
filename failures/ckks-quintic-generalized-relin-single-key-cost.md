# Iteration 47 — Direct degree-5 CKKS relinearization is not a free reuse of the degree-2 key

Date: 2026-10-10
Research area: High-precision CKKS bit cleaning / generalized tensor-then-relinearize
STATUS: FAIL for the **single ordinary s²-key, cubic-like cost** hypothesis. A single final generalized Relin is a candidate cost rearrangement, NOT verified FHE correctness/precision or novelty.

## State and exact source provenance
[FACT] Read AGENT.md, RESEARCH_PHILOSOPHY.md, STATE.md and I46 `failures/ckks-thrifty-quintic-sequential-relin-precision.md` before any edits. User's RIG-HE parked STATE.md remains unchanged.
[FACT] Choe, Kim, Stehlé, Suvanto, *Leveraging Discrete CKKS to Bootstrap in High Precision*, CCS 2025; Research MCP complete 15-page original PDF ePrint 2025/1786, mirror PDF sha256 3d1e2277a4a64de6094094c86a941f95374528be50fea611847927d8a68b4230, VERSION_UNVERIFIED. §4.1 Figure 2 and Theorems 4.1–4.2 physical pp.9–10 give standard thrifty cubic cleaning h1(x)=3x²−2x³, two unrelinearized products with ordinary degree-2 relin for each stage, output scaling Δ² with modulus loss Δ per cleaning; twice increases input scale Δ to Δ⁴, ideal modulus loss Δ³ (up to gaps/rounding).
[FACT] §4.2 physical p.11 proposes general polynomial P(x)=Σ_j α_j x^j through ct_j=Δ^(k−j) Relin(ct^(⊗j)) and notes input ciphertext is regarded as having an exact scaled noisy input plaintext; this is a theoretical high-degree tensor-then-Relin construction, **not** a claim that the stock degree2 RLK is sufficient.
[FACT / IMPLEMENTATION] Verified both the v6.1.1 tag and current public source for tuneinsight/lattigo:
- core/rlwe/evaluator_evaluationkey.go lines ~115–145: `Relinearize` checks `ctIn.Degree()!=2` and returns an error; specifically applies `GadgetProduct` only to `ctIn.Value[2]` with one RLK.
- core/rlwe/keygenerator.go lines ~98–121: `GenRelinearizationKey` computes `sk2 = sk*sk`, then evaluation key under sk; no direct degree3..5 relin API.
- core/rlwe/keys.go lines ~282–295, 537–563: RLK is one `EvaluationKey` encrypting s² under s; generic EvaluationKey is gadget ciphertext.
- core/rlwe/gadgetciphertext.go ~24–43: `NewGadgetCiphertext` stores an RNS decomposition × power-two decomposition matrix of RLWE key ciphertexts; core/rlwe/params.go ~542–549: `BaseRNSDecompositionVectorSize = ceil(lenQ/lenP)` for P present; with no additional base2 decomposition and P present each RNS block has one digit.
Primary GitHub source: https://github.com/tuneinsight/lattigo/tree/v6.1.1/core/rlwe
[SECONDARY CROSS-CHECK] Documentation https://pkg.go.dev/github.com/baahl-nyu/lattigo/v6/core/rlwe describes Relinearize as degree2 only. It is corroboration, not a substitute for source.
[SOURCE LIMIT] HEaaN paper implementation source code for the authors' high-degree generalized operation was not available/inspected; the exact parameterized memory model is for Lattigo-like RNS gadget evaluation keys only. This is NOT a measurement in HEaaN and not a claim that authors used exactly this generalized degree5 operation in their experiments.

## One hypothesis and cheapest decisive test
[HYPOTHESIS — FALSIFIED] For the quintic H(x)=10x³−15x⁴+6x⁵, direct unrelinearized tensor-then-Relin can be executed using only Lattigo's ordinary s² RLK with evaluation-key footprint and number of gadget key-switch operations similar to two thrifty cubic rounds, without new secret-power evaluation keys.
[FAIL CONDITION] Source API rejects ciphertexts of degree>2 or a generic degree5 ciphertext requires independent switching support for secret powers s³,s⁴,s⁵ in addition to s².
[MINIMAL TEST] Source inspection of actual v6.1.1 Relin and gadget-key layout; analytically expand ct^(⊗5) and count needed degree-wise key switches; validate polynomial output under one fixed s using exact integer arithmetic; compute one fixed illustrative key payload, not a parameter sweep or runtime benchmark.

## Exact derivation and costs
[DERIVATION] ct=(c0,c1), `Dec_s(ct)=c0+c1*s`. Tensor power ct^(⊗5) produces degree5 vector (d0,...,d5), decrypts as Σ_i d_i s^i. A straightforward direct switch to degree1 requires independent s^j→s switching material for j=2,3,4,5 in the generic/full-secret case: **4 distinct keys**, **4 gadget products** for ONE degree5 ciphertext. The stock Lattigo `Relinearize` with only s² RLK explicitly rejects this input.

For H(x)=10x³−15x⁴+6x⁵, the paper's §4.2 per-monomial direct recipe uses:
- ct^(⊗3): (s²,s³) terms -> 2 gadget products
- ct^(⊗4): (s²,s³,s⁴) -> 3
- ct^(⊗5): (s²,s³,s⁴,s⁵) -> 4
total **9 nominal gadgets** (not keys: the *set* of secret-power keys is still 4).
For two thrifty cubic rounds, standard Figure2 uses 2 degree2 relins per round; **4 nominal gadgets**, **1 reusable s² key**, two separate final rescale stages.
An alternative elementary lazy scheduling is to form the full unrelinearized degree5 polynomial ciphertext `C_raw=10 Δ² ct^(⊗3) −15 Δ ct^(⊗4)+6 ct^(⊗5)`, then do **one generalized Relin** to a linear ciphertext: **4 gadget products and same 4 higher-power keys** instead of 9. This is algebraically exact at message level, if no modulo wrap and scales align, but remains only a CANDIDATE for real CKKS noise/key decompositions and not established as novel (deferred/lazy relinearization is known).
Two cubics yield fourth-order ideal bit-error suppression; single quintic yields third-order. Their plaintext accuracy, modulus consumption and output scale are DIFFERENT, so the counts are a raw cost tradeoff, NOT a fair matched-precision speedup claim.

## One illustrative exact payload calculation
[DERIVED / MODEL] Take ring N=4096, full 64-bit RNS representations with 8 Q primes and 1 P prime; use LevelQ=7, LevelP=0, base-2 decomposition disabled, **uncompressed** RLWE degree-one gadget ciphertexts, all secret-power keys same level.
RNS gadget count ceil(8/1)=8, each gadget ciphertext pair has 2 polys × (8 Q + 1 P) limbs, each limb N 64-bit words:
  raw_words_per_key=2*8*4096*9=589824 uint64;
  raw_bytes_per_key=4,718,592 bytes=4.5 MiB.
One ordinary s² key => 4.5 MiB; four distinct keys => 18.0 MiB. This is 4x the coefficient payload, excluding serialization metadata/buffers, not HEaaN runtime/key memory. Compressed keys/NTT representation/level-specific evaluation keys may alter actual memory. The keys are NOT security-equivalent without accounting for RLWE parameters, circular security and secret-power evaluation key assumptions. No security claim made.
[EXPERIMENT] Local reproducible `/mnt/data/iteration47_generalized_relin_cost_audit.py` SHA256 cd4c5d81697877ee46ec169fc1b3a1fab3b149d22b06194879623b2afe8574f0, stdout `/mnt/data/iteration47_generalized_relin_cost_results.txt`: 3/3 exact integer polynomial tensor/decryption consistency cases; checks 1/4 secret-power key counts and 4/9/4 gadget counts; computes 4.5/18.0 MiB key payload. NOT encrypted, no runtime, no noise distribution, no RNS key sizes measured.
CAVEAT on lazy single Relin: since raw C_i aggregate Δ powers before gadget decomposition, whether the **actual key-switch noise** preserves the third-order useful CKKS precision and modulus saving has NOT been analyzed. Scale Δ^(5) raw may require larger ambient Q; source Lattigo may not support raw high-degree tensor product with current multiplication API. Do not claim source-ready implementation.

## Outcome and strategic view
[NEGATIVE] The original hypothesis that a single standard quadratic RLK provides direct degree5 relin at comparable memory without changes FAILS. Need ~4 independent secret-power keys under the straightforward generalized structure, and Lattigo's stock degree2 relin cannot accept degree5. Memory overhead is structural.
[POSITIVE / OPEN] Combining raw polynomial terms before ONE generalized Relin reduces nominal gadget products from 9 to 4 without reducing four-key footprint, within the exact source-grounded cost model. Not tested in actual HEaaN nor benchmarked. Need independent novelty check for "deferred/lazy relin" before presenting it as a contribution; a single test of early vs late key-switch error under true RNS parameters could falsify precision viability.
[NOVELTY] Overall novelty unverified / likely LOW: textbook lazy relinearization and high-power key-switching. Avoid further toy expansion unless nontrivial key representation improvement is identified.

## End of Iteration
STATUS: FAIL — degree5 generalized relin is not a no-extra-key drop-in using Lattigo's s² key.
RESULT: Lattigo v6.1.1 only accepts Degree2; direct monomial-wise quintic needs four key types and nine gadget products vs one key / four gadget products for two cubic rounds. A proposed delayed generalized Relin reduces nine to four gadget products but retains four keys; no CKKS correctness/performance claim.
NEXT_ACTION: As a single follow-up, locate in accessible full-text prior art whether **combining unrelinearized polynomial monomials before one generalized relinearization** is already published, and if so archive this scheduling candidate without HEaaN implementation. If not, select one true-RNS gadget-error test to check whether late decomposition preserves the third-order bit-cleaning precision; no broad benchmarking.
STATE_UPDATE: NO — parked RIG-HE STATE.md untouched.
