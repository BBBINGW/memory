# HLUT-H02 — Benchmark returns encoded output and does not run optional canonical output PBS



Date 2026-10-14 (Asia/Tokyo). Standalone one-hypothesis follow-up to H-HLUT-01; human PI replied 'continue'. Read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, global STATE.md (frozen I192, independent vFHE now V27; READ ONLY), and H01. No global/vFHE/SHIP/HERDS state changes or upstream code modification.



## ONE primary falsifiable hypothesis and cheapest decisive source + original-artifact data test



**H-HLUT-02:** The TCHES 2026 HLUT Rust evaluation benchmark includes the (at most one) extra small-field PBS that §5.2 says can transform **noncanonical encoded final outputs** back to the original/standard plaintext encoding, so its `lambda+2Σt_i` PBS count always includes complete server-side canonical-format conversion even when the decomposition uses encoding switching.



**Falsifier:** Inspect the source's published encoding-restoration statement and `bench/HLUT-rs/src/decomposition.rs` return/caller, fetch actual saved decompositions and encoding map for one cited benchmark size, evaluate the published plaintext program exhaustively to test whether any real input returns a noncanonical Fp field element, and compare conditional PBS call counts. If no noncanonical mapping is ever used, the absence of a conversion PBS is immaterial. Do NOT confuse output **client-side decoding** with server-side **homomorphic normalization**.



## Original source and pin [FACT]



- Sonia Belaid, Nicolas Bon, Matthieu Rivain, *Decomposition of Large Look-Up Tables for Fast Homomorphic Evaluation*, TCHES 2026 Volume 3, ePrint **2026/724**, https://eprint.iacr.org/2026/724. Full 32-page Research MCP mirror obtained; PDF SHA256 **cc45b49e20958f5c3fc1e327d84d1549d7fef08bdb4ba973dac75fd3a67efeb4**, source_revision **108e41a7dc5788eb2d61023f9aecbcb72889d1d9**, **VERSION_UNVERIFIED** vs official publication.

- Original physical p18 §4.3 single-output cost is `lambda+2t` PBS without explicit §5.2 output conversion. p19–20 multi-output cost `lambda+2 sum_i t_i`. Physical p24 §5.2 **explicitly states** an altered `E_out` may be converted back to original encoding with **one small-field PBS**; this is conditional on needing a **homomorphically canonical ciphertext**, not mandatory if only the final client decodes under the saved encoding.

- Authors' public reproduction https://github.com/CryptoExperts/artifact-HLUT-TCHES at commit **088029cb4cd3a6b33ac10e0c78ea193b1835216d**, dated 2026-07-02. `bench/HLUT-rs/src/decomposition.rs` blob **dc995a1fc1f827214484701df87b2acbacfd1521**: `load_decomposition` loads public per-output `encodings`, but `partial_lut_evaluation` computes each `bit_out = server_key.simple_sum(&products)` and appends it to returned `Vec<Ciphertext>` **without any output `E_out^{-1}` PBS**, and `compute_theoretical_cost` counts `self.l + 2 * sum(self.t_is)` excluding canonicalization. Extra `encodings` metadata is available through `pub encodings` in the `Decomposition` object; a caller may intentionally decode final outputs in this noncanonical representation, so this is **not intrinsically a correctness bug**.

- `bench/HLUT-rs/src/main.rs` blob **a4f0f12ef6545bb28be766d0552dbc385bfb1159**: `perf_measurement` times ONLY `decomposition.partial_lut_evaluation(...)` for `input=0..n_tests-1`, with `n_tests=5` in all published-size loops; it does **not** execute a canonicalization PBS, output decrypt/decode, or post-evaluation correctness check inside the timed interval. It returns elapsed integer milliseconds. Hence compared wall-clock totals are **encoded-output evaluation** not necessarily canonical-field output normalization.

- Source paper's released `decompositions/paper/encodings_3_n` for n4..14, `encodings_5_n` for n2..7, `encodings_17_n` for n2..3 were each fetched from the PINNED git commit and checked by parsing all output encoding blocks. Out of 19 **available** published decomposition sets, ONLY `encodings_5_4` has a nontrivial output encoding (the first output, `2 : 2 4`). `encodings_17_4` does NOT exist in this artifact, so do not include in count. This limits any measured PBS-count discrepancy to the particular available published benchmark(s) with actual encoding switching, instead of implying every HLUT result undercounts cost.



## Exact one original-artifact plaintext-program exhaustive test [COMPUTED]



One selected case `s=4,p=5,n=4`: Source `decompositions/paper/parameters_5_4` sets `lambda=27`, `t_is=[8,6,5,5]`; first output has 8 products, so `27+2*(8+6+5+5)=75` PBS in the source program. Files fetched at the same commit: `new_phis_5_4`, `d_5_4`, `betas_5_4`, `sbox_5_4`, `parameters_5_4`, `encodings_5_4` (saved 256-output S-box). The first output's actual mapping is `{0:[0],1:[1],2:[2,4],3:[3]}`. The first output's original U,D,beta program has L=n+lambda=31, d-matrix length 8*31=248 and beta length 9*31=279, all inputs/operations in F5. Evaluated **every one of 4^4=256 possible inputs**, using the 27 source-recorded nonlinear atomic functions and original β,D coefficients, and confirmed every computed F5 output belongs to the correct plaintext class of the recorded output map (0 incorrect under `E_out^{-1}`).



**ONE exact witness:** Input index **245** = base4 digit vector `(x0,x1,x2,x3)=(1,1,3,3)` under author's little-endian SBox index convention. The S-box first chunk is `2`, but the source's polynomial/PBS-level arithmetic program (plaintext idealization, no noise) outputs `4` in F5. The mapping includes `4` in `E_out(2)` so this is correct **noncanonical encoding**. Exactly **ONE** of 256 first-output samples is noncanonical; canonical-field interpretation on this input would be incorrect. All other output encoding blocks for this case are canonical. The benchmark loops only over input indices **0..4** (n_tests=5), so it does not exercise this exceptional input in normal timing; runtime path is nevertheless structurally identical (this fact is NOT evidence the encrypted evaluation actually fails at 245).



**Cost [DERIVATION]:** In this CASE, if the online FHE API promises four **canonical ciphertext outputs suitable for composition** rather than encoded final answers, at least one extra PBS to implement `E_out^{-1}` (e.g. LUT 4→2, other possible values unchanged) is sufficient: **75→76 PBS calls**, a 1.3333% logical call-count increase, not a certified 1.3333% latency increase (different parameterizations/overheads). If outputs are FINAL and client knows encoding metadata, decoder can directly map decrypted F5=4 to plaintext Z4=2 with **zero server-side extra PBS**, consistent with the authors' design. In the p3 and other inspected p5/p17 decompositions with canonical output encodings, this specific overhead is zero.



**Precise claim boundary:** This is a source-supported **interface/cost-model qualification for canonical output**; not proof the paper falsely reports its explicitly measured noncanonical/terminal-result timings, and NOT an inherent ciphertext correctness failure. The paper explicitly admits one possible conversion PBS; so we are not discovering an unmentioned primitive or a general FHE attack. It also does NOT challenge TFHE-rs key security, DFR or code-level multiplication for noncanonical outputs (all actual encryption effects excluded). A more explicit API or benchmark reporting whether canonical server output is required could improve reproducibility, but the identified 1-PBS case alone is not a publishable algorithmic contribution.



## Reproduction & verification



Full arithmetic was executed via a direct JS evaluator over ORIGINAL six checked-out GitHub-file contents returned by connected GitHub API (not through a compiled author backend), asserting dimensions, all 256 mapping memberships, and the single anomalous index 245. A portable standard-Python equivalent standalone script was saved to `/mnt/data/hlut_H02_output_encoding_cost_gate.py`, SHA256 **4a6831222c27f9c2e5163a3baa9fa879a8488d010f95258b045b0070fe0edfde**, requiring a local checkout of the above pinned GitHub repo because this environment cannot fetch arbitrary code within Python. The script syntax was compiled with `py_compile` but **was not run end-to-end against a local checkout**; use the independent JS original-file audit as executed evidence. JSON exact source-check summary `/mnt/data/hlut_H02_output_encoding_cost_results.json`, SHA256 **41bb5d44b0956e9cfabf237dbf4bdc0a011fb8779b5b0ec504297f7f521430e5**. There is NO TFHE ciphertext run, cryptographic security analysis or runtime benchmark.



## End



**STATUS: FAIL H-HLUT-02** assertion that the canonical restoration PBS is always included; **PASS** source-to-artifact encoded-output witness + exact conditional PBS counts. **PARK/HUMAN_REVIEW** this limited interface/cost distinction. **NOVELTY NOT VERIFIED.**

**RESULT:** One actually published decomposition requires `E_out(2)={2,4}` and for x=(1,1,3,3) yields F5=4 for logical output2; the code returns that ciphertext unchanged, so canonical server output would need an additional PBS (75→76 calls in this case). The original paper explicitly mentions this conversion; final-client decoding can avoid the extra PBS legitimately. This is a 1.33%-call interface budget in the only noncanonical-output benchmark case inspected, not a claimed flaw in the paper's measured end-to-end conditions.

**NEXT_ACTION:** Recommend **PARK** H-HLUT-01/02 microaudits. Only reopen if the user PI selects a **substantial mechanism** with published-source-comparable ≥material effect on total PBS count, matched DFR/noise or decomposition success (e.g. a structurally different chain-search method demonstrated on the code's full-rank matrix, not a trivial extra PBS). Otherwise use PI-selected main vFHE workstream, or screen a distinct original-source FHE problem. Do not change global vFHE priorities or contact authors without permission.

**STATE_UPDATE: YES**, this independent finding only; global STATE.md, vFHE, ship-memory-state, HERDS, open backlog left unchanged.