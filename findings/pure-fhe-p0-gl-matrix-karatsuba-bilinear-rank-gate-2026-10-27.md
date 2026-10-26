# PURE-FHE · P0-PRESCOUT-40 — Gentry–Lee Matrix-FHE: four tagged products vs naive Karatsuba

Date: 2026-10-27 (Asia/Singapore)
TRACK_ID: PURE-FHE
ACTIVE_TOPIC: MATRIX_FHE_MIXED_OPERATOR_NOVELTY_GATE
PREVIOUS: P0-PRESCOUT-39, findings/pure-fhe-p0-batchboot-key-onehot-autotag-ram-gate-2026-10-27.md, commit 567d0af24da88945259ade0670679841173a8f5e
LATEST_COMPLETED: P0-PRESCOUT-40
NEXT_ITERATION: P0-PRESCOUT-41 NOT_STARTED
STATUS: PASS_SOURCE_TAGGED_BILINEAR_RANK_GATING / FAIL_SCALAR_KARATSUBA_4_TO_3 / UNCLEAR_NEW_TYPED_FUSION
NOVELTY: NOT_ESTABLISHED; elementary rank bound on narrow operation model, not a new FHE construction
CODEX_REQUIRED: NO. No native execution, GPU, remote setup, or shared STATE edit.
STATE_UPDATE: YES, one isolated PURE-FHE finding. Other research tracks untouched.

## One primary hypothesis H40 and minimal decisive test

Does original Gentry–Lee ePrint 2025/1935 ct–ct matrix multiplication admit a **Karatsuba-style four→three** reduction of its four independent intermediate tagged component products, using exactly three calls to source-style bilinear matrix multiplication of public-scalar-linear mixtures of ciphertext components followed by only public scalar linear work, while preserving the full four-component intermediate representation, WITHOUT special key-switching/repacking/new tags?

Cheapest decisive test: read primary Section3.4–3.6 full original with ciphertext secret tags; restrict bilinear operation to one scalar output channel; compute symbolic tensor rank of the four required b/a cross monomials. Then screen source-matched whole-workload operation-time envelope for whether an allegedly perfect 4→3 change could be important.

## [FACT] Primary sources checked directly

1. Gentry & Yongwoo Lee, *Fully Homomorphic Encryption for Matrix Arithmetic*, CRYPTO2026, ePrint 2025/1935 (https://eprint.iacr.org/2025/1935), mirror PDF 27 physical pages, SHA256 985173da6bc45f1c89c86769d5b6b16bfcdd98bf07e91476cd424778b8d9ec84, VERSION_UNVERIFIED. Physical p15 Theorem3.12, p16 §3.5 relinearization and §3.6 Hadamard, p22 Tables1–2, p23 Table3 directly reread. Original ct–ct matrix multiplication produces
 d0=bu ⊛ bv,
 d1=bu ⊛ av,
 d2=au ⊛ bv,
 d3=au ⊛ av.
Decryption uses 1, s(X,W), s(Y^{-1},W^{-1}), s(X,W)s(Y^{-1},W^{-1}). The two cross terms have DIFFERENT secret tags. Ordinary ring Karatsuba's single cross-sum d1+d2 is NOT sufficient to represent these separate terms under their respective secrets. Source relin uses two key switches to return to 2-component ciphertext; p16 §3.6 already provides native Hadamard product by one ordinary ring product plus Switchsmall under secret s(X,W), and a distinct key type. This already defeats novelty of generic "native matrix multiply AND Hadamard".
2. Cheon/Kang/Junho Lee, *Fast Batch Matrix Multiplication in Ciphertexts*, CRYPTO2026, ePrint2025/1957 (https://eprint.iacr.org/2025/1957), 32-page mirror SHA256 ab063dd495542ebee0004bf0211cabd3e7af978ae71dc95995973dba45c7aa9a, VERSION_UNVERIFIED. §3.1–3.2 pp12–14 provides SinC and SinCBoot directional conversion SinC→slot; §7 p25–27 with N8192, 128 batch d64 CPMM0.199s CCMM0.912s ~15.7 accuracy bits under different environment. P0-06/07 already proved plain SinC ring product is NOT rowwise Hadamard and source itself has original SinC→slot and slot→SinC conversions. Do not redo those old toy tests.
3. Crockett/Gentry/Kim/Lee/Lee *Efficient Bootstrapping in Fully Homomorphic Encryption for Matrix Arithmetic*, CRYPTO2026, ePrint2026/956 (https://eprint.iacr.org/2026/956), first-party published abstract confirms CtS/StC as native ciphertext–plaintext matrix products. FULL PDF READ BLOCKED by ePrint403 and research MCP; no unverified noise/cost theorem claimed.
4. Cheon/Kang/Lee *Fast Batch Bootstrapping in CKKS*, ASIACRYPT2026 to appear, recent author publication listing https://mskang0503.github.io/publications/ (web search indexed current listing). No full PDF/algorithm retrieved, so its handling of SinC interoperability is UNKNOWN and blocks absolute novelty claims.

## [DERIVATION] Narrow bilinear rank 4 obstruction

Introduce independent scalar variables bu,au,bv,av in a characteristic-zero field, and study target output vector
  F=(bu*bv,bu*av,au*bv,au*av).
The four basis monomials are linearly independent as bilinear forms in left inputs (bu,au), right inputs (bv,av); equivalently coefficient vector of F is the 4×4 identity in monomial basis. Each call (α bu+β au)*(γ bv+δ av) produces one rank-1 bilinear scalar form. Any three such calls followed only by public scalar linear combinations span dimension≤3, so cannot recover the four outputs (rank=4). Thus original all-four component tensor requires ≥4 such products in this narrow input/output and scalar-mixing model.

Ordinary Karatsuba derives K=(bu+au)*(bv+av)−bu*bv−au*av=bu*av+au*bv=d1+d2, not d1 and d2 separately; and their GL decryption tags are s(X,W) and s(Y^-1,W^-1), respectively. Even the sum is not a valid replacement for both unless additional tagged key switching/secret algebra is performed or tags coincide under a restricted secret (not assumed).
This argument is NOT a general lower bound for arbitrary matrix-valued product packing, SIMD recombination that embeds different bilinear forms into different matrix coordinates, different output encodings, secret-dependent early key switching, or changed protocol. Those could invalidate the narrow scalar argument; no claims of impossible 3-call FHE matrix multiplication in every conceivable scheme.

[TOY_EXECUTED] SymPy on four formal input variables verified coefficient-space rank 4 and expanded Karatsuba cross product to d1+d2. No native FHE run, no concrete FHE security or noise proof.

## [FACT + DERIVATION] Source-matched latency headroom in current GL, not cross-scheme claims

Author's SAME CPU/parameter table p22, single-thread i9-11900K, n256,p17 batch16 complex matrices, says ct–ct matrix mult:
  normal 11.582s; of which 7.407s matrix multiplication over Zq, and 3.343s key switching.
  WITH FLINT 7.237s; of which 3.042s matrix multiplication over Zq, 3.317s key switching.
  Native Hadamard product 2.779s including 1.169s KS and 1.610s others.
The paper reports these as isolated operations, not a sequential mixed-workload benchmark and not at SinC's N8192 parameter set.

For a *counterfactual* fixed 2×ct–ct matrix multiply +1×Hadamard (square), ignoring additional bootstrap/scale/level feasibility:
  T_basic=2*11.582+2.779=25.943s, H share 10.712%, perfectly eliminating Hadamard at no cost gives upper speedup only 25.943/(2*11.582)=1.119971x;
  T_FLINT=2*7.237+2.779=17.253s, H share 16.107%, ideal deletion upper gain17.253/(2*7.237)=1.191999x.
Including any positive bootstrap overhead without optimizing it reduces this particular optimistic speedup envelope. These are conditional Amdahl-style bounds, not an actual end-to-end timing or a reason to assume Hadamard can disappear without computing a different function.
Even if perfect 4→3 component multiplication reduced p22 source's matrix-arithmetic portion by one quarter, keeping all other costs at same value, the 2MM+H proxy would improve at most 25.943/(25.943−2*7.407/4)=1.16653x (normal) or 17.253/(17.253−2*3.042/4)=1.09668x (FLINT). Since H40 fails as a representation-preserving 3-product Karatsuba, these are headroom-only counterfactuals, not achieved gains.
Do NOT compare SinC 0.912s and GL 7.237s as if same matrices/batch/precision/N/hardware. Do NOT infer bootstrapping latency for GL from 2026/956 public abstract. Full pipeline has additional CKKS scale, modulus consumption, noise, key memory and security constraints.

## Decision / contribution threshold

H40 FAILS specifically for preserving all four independent secret-tagged source ciphertext components under three scalar-linear Karatsuba matrix-product calls. A broader early-relin / multi-product packing / new tensor-bilinear algorithm might be possible and is NOT ruled out; but it must pay for representation, key switching, noise/security, output bandwidth and support original n×n and batch dimension. The author already has native Hadamard and new matrix bootstrapping work; no novel contribution established.
The native GL bottleneck is more dominated by ciphertext-component matrix products and key switching than Hadamard in author's tested batch, so a simple "Hadamard bridge" is low leverage in that setting. Main original bottleneck in SinC is still a distinct unmatched representation choice, not comparable by existing rows.

Recommendation: PARK naive Karatsuba and generic conversion-free matrix nonlinearities as independent PURE-FHE publication directions. Only re-enter if a source-complete new typed key/dataflow representation that simultaneously changes dominant matrix multiplication work and key overhead while preserving end-to-end accuracy/security survives comparison to 2026/956 and ASIACRYPT 2026 batch CKKS paper. Otherwise next PI-approved P0 iteration should pivot to a genuinely new, source-complete core cost problem, or state the current portfolio lacks build-ready crypto mechanisms; don't repeat more pairwise toy matrix algebra.

END_OF_ITERATION:
STATUS: FAIL_NAIVE_4_TO_3_KARATSUBA / PASS_TYPED_BILINEAR_RANK_AND_COST_SCREEN / NOVELTY_NOT_ESTABLISHED.
RESULT: GL four distinct secret-tagged intermediate products cannot be recovered by 3 public-scalar mixed products and public linear recon; Karatsuba produces d1+d2 only; source GL 2×MM+Hadamard ideal removal ceiling 1.120–1.192× excluding bootstrap.
NOVELTY: NOT_ESTABLISHED.
NEXT_TEST: nearest-full-source for 2026/956 and Fast Batch Bootstrapping in CKKS, or source-backed different FHE key/dataflow method; no unbounded more toy variants. If user PI explicitly prioritizes generic FHE systems rather than cryptographic construction, native mixed workload benchmarks may be considered but not now.
STATE_UPDATE: YES one isolated PURE-FHE finding only; global STATE.md/other tracks untouched.
CODEX_REQUIRED: NO. Any implementation or GPU/remote step remains pending explicit PI approval.