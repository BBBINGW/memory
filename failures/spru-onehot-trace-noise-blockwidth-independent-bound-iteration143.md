# I143 — SPRU one-hot plaintext does not yield block-width-independent worst-case Trace noise

**2026-10-13, after I142.** PI authorized exactly one next round with “好的，请继续”. One hypothesis + one minimal exact linear Trace falsifier, not a compiled OpenFHE cryptographic run.

## Sources and read-before-write

- Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` after I142 sha `4fbc9ec2b799d221efc5cb97f7741489df5693cc`, long-term `findings/OPEN_RESEARCH_BRANCHES.md`, SPRU I119 and I142 findings.
- Primary Coron and Köstler, *Low-Latency Bootstrapping for CKKS using Roots of Unity*, ePrint **2025/651**, https://eprint.iacr.org/2025/651. Read full parsed original §3.5 **physical pp11–12**, §4.3–4.4 pp15–16, §6.1/Table2 p24, plus I142 prior Appendix E pp40–41. Exact 42pp cached GitHub-mirror PDF sha256 `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6`; latest official edition VERSION_UNVERIFIED.
- **Source §3.5:** `Tr_(N/2→a)=(id+Psi_a)∘(id+Psi_(2a))∘...∘(id+Psi_(N/4))`, *unnormalized*. It computes `t_k=Σ_{j=0}^{N/(2a)−1} z_(k+j a)`, repeating the a outputs. `Psi_r` ring automorphism is slot rotation by r after a key switch. `Tr` consumes no multiplicative levels, but uses `log₂(N/(2a))` rotations/key switches. §4.3 states *plaintext* exactly one active selector per B=N/h positions; §4.4 splits two half-block encodings, applies `Tr_(N/2→h)` then `Pr_(h→1)`. Table2 N=2¹⁵, h64, so B=512 and trace multiplicity `L=N/(2h)=256`.
- Author's actual public code `coron/spru_boot` verified with CONNECTED GitHub: `src/single_slot.cpp` blob `38d9fda8023ca0a06c5f4c9632802c83e4762c22` lines ~76–85: `irot=N/4`, `nB=round(log₂(B))`, and for `k=0..nB−2`, `cadd=cadd+cc->EvalRotate(cadd,irot); irot/=2`. For B512 this yields exactly 8 shifts [8192,4096,2048,1024,512,256,128,64]. `src/multiple_slot.cpp` SHA `7ffb1fff5d99dc8e0f947ae77083455d163afa64` lines ~116–126 uses analogous unnormalized trace in multislots with multiplicity `B/(2n)`, after EvalMult and EvalAdd across packed key ciphertexts. This is not a new source bug; source implements the published operator.
- I119 and I142 had found the unoptimized Appendix E sufficient noise proof does not directly certify the *different* optimized Table2 circuit, and a depth-only transplant still demands log₂Δ≥62.55 vs ≈49. We **do not** re-test the same bound or claim hardware precision failure.

## ONE hypothesis and ONE falsifier

**[HYPOTHESIS]** Given plaintext exactly-one-per-block selectors in SPRU optimized Eq.(9), the homomorphic trace stage `Tr_(N/2→h)` has a **deterministic** post-Trace additive ciphertext noise bound `||E_out||∞ ≤ C ||E_in||∞` with a constant C independent of the half-block width `L=B/2=N/(2h)`; only h selector-related terms, rather than L potential noise summands, contribute. This is a proposed PROOF shortcut, not a claim made by the authors.

**[FALSIFIER]** Provide one source-compatible input plaintext with exactly one selector in each original B block and one admissible *small ring plaintext-decryption error* e(X) of coefficient infinity norm1, such that ideal homomorphic Trace (zero additional rotation-keyswitch noise solely to isolate initial-error propagation) amplifies e by L. Test exact source rotations on a 16-slot toy and on Table2 actual 16384 slots, not the full bootstrapping or a security claim.

## Exact mathematics

For any e(X) in real integer negacyclic ring R=Z[X]/(X^N+1), each automorphism Ψ_r permutes ring power-basis coefficients with signs, so `||Ψ_r(e)||_coeff∞ = ||e||_coeff∞`. The ideal unnormalized trace adds precisely `L=2^k` such automorphically transformed terms. By triangle inequality,
```
 ||Tr_(N/2→h)(e)||_coeff∞ ≤ L ||e||_coeff∞,     L=N/(2h).
```
**This bound is exact (attained):** let **e(X)=1**. Every Ψ_r fixes the constant polynomial, so each `id+Ψ_r` maps 1→2; after k rotations `Tr(1)=2^k=L` **as an integer constant polynomial**. Hence `||Tr(e)||_coeff∞ / ||e||_coeff∞ = L`. In CKKS canonical evaluation slots, e(X)=1 also evaluates to 1 in **all** N/2 slots, and Trace gives L in every slot. This input error is within coefficient bounded unit errors; an actual centered-small error distribution assigns some positive, potentially tiny, probability, and it is NOT presented as typical sampling.

Exactly-one-per-block only constrains the underlying packed plaintext selector. For n=1, choose in each B block the one selector in the **first position of the first half-block**, so packed first-half selection is 1 at slot indices 0,…,h−1, all other slots0, and the second-half selection ciphertext plaintext is 0. For k=0,…,h−1, `Tr(s)_k=Σ_{j=0}^{L−1}s_(k+jh)=1`. Independently superpose the legal additive decryption error e(X)=1 (slot-wise all ones) on **one ciphertext just before trace**. Plaintext output remains1 per k, but decryption error output becomes L, irrespective of the onehot sparsity. Fresh nonzero rotation-key-switch errors can contribute additional terms; they are deliberately set to zero in this isolated deterministic counterexample and not claimed typically zero.

For source Table2 N32768, h64, B512, L256, Trace consists of eight `id+Ψ` stages and `Tr(1)=256`. **This is 8-bit max amplification for an input with perfectly coherent unit slot error, not proof of actual loss of 8 CKKS precision bits** or a bound on the full optimized circuit. The post-Trace code uses a product tree, imaginary extraction, scaling δ and eventual rescale/S2C, not modeled.

## ONE exact reproducible test

Saved standalone offline Python `/mnt/data/i143_spru_trace_error_gate.py`, SHA256 `67f39319c15d8ba77a8a05a02fc7cdcf15894786439c41f38488dd8acb45e5b9`; contains just 48 lines pure integer slot rotations/additions; uses source positive rotation indices and exact onehot packed plaintext + coherent ring e=1. Executed and output:
```
N=32, h=2, B=16, input_slots=16, rotation_shifts=[8,4,2],
 selector_out=1, additive_error_in=1, additive_error_out=8, ratio=8x

N=32768, h=64, B=512, input_slots=16384,
 rotation_shifts=[8192,4096,2048,1024,512,256,128,64],
 selector_out=1, additive_error_in=1, additive_error_out=256, ratio=256x
```
Assertions verified: all slots of selector Trace output=1, all additive error Trace slots=L, superposed ciphertext slot semantics 1+L. One test generalizes a single coherent unit-error witness to source actual shape. **No OpenFHE compilation; not a Gaussian sampler, LWE security/probability/precision estimate, full key switching, or new full precision theorem.**

## Judgment

- **[FAIL]** the *deterministic block-width-independent Trace-noise bound based only on plaintext one-hot structure*. The ideal trace operator's coefficient/slot \(\ell_\infty\) norm is exactly L=B/2. Arbitrary ciphertext decryption noise is NOT a onehot sparse vector simply because plaintext selectors are.
- **[PASS]** source implementation and paper operator agree; exact coefficient argument and small+original-dimension integer tests verify worst-case noise sensitivity. No source flaw, no new cryptographic result, no universal implementation precision failure.
- **[OPEN]** Real optimised SPRU Table2 ≈14-bit measured precision may admit a **probabilistic** trace-error analysis if actual fresh/rotation-key noise distributions and their correlations imply cancellation/√L scaling, but applying such an argument rigorously to these ring automorphisms plus key switching requires new assumptions and potentially code-driven data. Onehot plaintext by itself cannot justify it. The entire subsequent product tree, δ and SlotToCoeff also matter. Novelty and importance of a full optimized noise theorem unknown.
- **[DIRECTION]** The idea of simple onehot→small noise is classical and fails. Recommend **PARK this deterministic SPRU proof shortcut**. If PI wants another SPRU iteration, only a genuinely distinct distribution-aware joint rotation-noise invariant with a falsifiable source-derived covariance bound and actual OpenFHE code sample should be considered; otherwise pivot to higher-value backlog candidates instead of micro-audits.

## End of iteration

**STATUS:** **FAIL onehot-based blockwidth-independent deterministic Trace noise / PASS exact source operator norm counterexample / HUMAN_REVIEW optimized circuit precision proof**.
**RESULT:** `Tr_(N/2→h)(1)=N/(2h)` exactly. For Table2 N32768,h64, small unit additive decryption error (ring 1) becomes 256 despite exactly-one-per-block message. Exact source code unnormalized rotations and exact 16-/16384-slot simulation agree. No actual runtime/precision anomaly or theorem breach.
**NEXT_ACTION:** I144 ONLY with PI authorization. Recommend PARK cheap SPRU bound-transplant/sparse-plaintext noise assumption. New material hypothesis would need a correlated/probabilistic error distribution **from real OpenFHE trace/key switching** and a specific trace bound substantially sharper than L in the source parameter regime, before attempting any full theorem; else pivot to vFHE CRT new PCS/other independent algorithmic gap. Do not repeat I119/I142 or call onehot plaintext a noise cancellation proof.
**STATE_UPDATE:** YES — disproves a distinct attractive cheap proof shortcut and sets a concrete necessary test for later trace-aware noise analysis.
