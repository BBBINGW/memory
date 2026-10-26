# PURE-FHE — P0-PRESCOUT-52: Two-sheet cyclic secret-shift and dense tensor-GSW cost gate

Date: 2026-10-27 Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
PREVIOUS: P0-PRESCOUT-51, findings/pure-fhe-p0-51-amortboot-mpmul-automorphism-ep-fusion-main-cost-gate-2026-10-27.md; commit 8fcd018c75d66ea818093f0d65d366d211d1fc06
LATEST_COMPLETED: P0-PRESCOUT-52
NEXT_ITERATION: P0-PRESCOUT-53 NOT_STARTED
STATUS: PASS_EXACT_TWO_SHEET_SHIFT / FAIL_NAIVE_NEGACYCLIC_WRAP / FAIL_DENSE_TENSOR_GSW_KEY_HEADROOM / NOVELTY_NOT_ESTABLISHED
STATE_UPDATE: YES isolated PURE-FHE finding only, no global STATE.md or other research track changes
CODEX_REQUIRED: NO; no native experiment, code, GPU, remote machines, models, deployments

## Single primary H52
Can Guimarães–Pereira's 2025/686 MPmul eliminate n log2(B) per-output gadget external products by one PRE-ENCRYPTED monomial Y^v evaluated with a single packed EP, WITHOUT expanding the evaluation-key/representation by a factor linear in n and while preserving the true negacyclic X↦X^-1 wrap?

Minimal test: exact sign/automorphism semantic check against original Algorithm1, explicit faithful packed ring realization if necessary, then dense RGSW key-byte and FFT arithmetic proxy compared with original source's B~n/h. ONE cost-and-type gate; no native FHE.

## [FACT] Verified primary sources
Guimarães and Pereira, Fast Amortized Bootstrapping with Small Keys and Polynomial Noise Overhead, CCS2025, ePrint https://eprint.iacr.org/2025/686 ; 34-page full PDF via GitHub Notes mirror sha256 84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335, VERSION_UNVERIFIED. Directly reread pp3–6 (§1.1–1.2), pp10–12 (MPmul Algorithm1 and Lemma3.1), pp17–20 and bibliography. Author's GitHub original source https://github.com/antoniocgj/Fast-Amortized-Bootstrapping, main.c blob a55fcfaa78151b71ae3aca1e434e0ec69b8afe27; current source contains sample N_input4096, output RLWE N2048, h~25–34, but source revision is not independently tied to published timing configurations.
Algorithm1 has c_j=RLWE_z(X^{u_j}) (or public LUT times monomials), encrypted bit selectors C_i=GSW_z(v_i), per level i n EP, first 2^i outputs use HomAut_{-1}(c_{n-2^i+j})−c_j, and others use c_{j-2^i}−c_j. Wrap therefore acts on the whole plaintext polynomial by τ:X↦X^-1; this is NOT a scalar sign flip. v is a difference of sparse secret support positions, known to KeyGen. The author proves O(h n log B) with typical/high-prob B=O(n/h), O(h log B) encrypted bit selectors. Original §1.1 pp3–5 explicitly contrasts prior [GPvL23] 63GB evaluation keys (reported source Table1 for 1024 messages 7 bits) and states large GSW/DFT parameter footprint is problematic.
Prior old tensored/packed ideas include Micciancio–Sorrell (ICALP2018), cited directly by 2025/686, and Bonnoron–Ducas–Fillinger, Large FHE Gates from Tensored Homomorphic Accumulator (AFRICACRYPT2018), institutional publication page https://ir.cwi.nl/pub/27652 . No claim these exact old algorithms equal the toy two-sheet construction; no novelty clearance for any doubled ring mechanism.
Current BatchBoot USENIX Security2026 additionally optimizes batched homomorphic polynomial multiplication, so old 2025/686 is not the final speed baseline.

## [DERIVATION] Naive negacyclic Y packing fails
Set R_X=Z_q[X]/(X^N+1), τ(m(X))=m(X^-1). Encode W0(Y)=Σ_{j=0}^{n−1}m_j(X)Y^j in R_X[Y]/(Y^n+1).
On multiplying Y^v with 0≤v<n, wrapped positions j<v equal −m_{n+j−v}, but original Alg1 needs τ(m_{n+j−v}). For m=X, τ(X)=X^-1=−X^{N−1}, generally different from −X. Thus direct n-size negacyclic tensor EP is semantically WRONG.

## [DERIVATION] Exactly correct 2-sheet algebraic cover
Define S=R_X[Y]/(Y^{2n}−1), Lift(m)=Σ_{j=0}^{n−1}[m_j(X)Y^j + τ(m_j(X))Y^{n+j}].
For 0≤v<n, first n Y-coefficients of Y^v Lift(m) equal:
  output_j=m_{j−v} if j≥v;
  output_j=τ(m_{n+j−v}) if j<v.
The other n coefficients are τ of the first n coefficients. This remains true after repeated signed cyclic shifts since τ²=id. General m_j may include test-vector polynomial factors: τ applies to the whole polynomial, as source's HomAut does.
Source Alg2 initially uses public test vectors and public b coefficients, so two sheets may initially be prepared publicly without per-output τ KeySwitch; for arbitrary encrypted input c_j a τ-key-switch or mixed-secret representation would be required. Subsequent public signed X^a per-position exponent corrections can be mirrored across two sheets.

[TOY_EXECUTED] In R_X=Z_257[X]/(X^8+1), n4, a deterministic private Python exact negacyclic polynomial implementation checked 16 randomly sampled exponent vectors with v∈[0,3], requiring exact first-sheet output and second-sheet τ relation: PASS16/16. Another 24 random signed cyclic rotations checked the second-sheet involution: PASS24/24. τ(X)≠−X also checked. No FHE encryption or performance measurement.

## [DERIVATION] Dense S-RGSW key byte and FFT-work cost
One RGSW(Y^v) under a full dense standard gadget over S requires Θ(2nN) coefficients per row, since S has Y length2n and X lengthN, compared to Θ(N) per bit selector C_i in the original R_X ring. It replaces log2 B bit keys per sparse difference by one huge tensor monomial key per difference. Under equal digit count, torus width, GLWE rank, the *standard dense representation* selector-key size ratio is (2n)/(log2 B). THIS IS NOT a universal lower bound on hypothetical compression or module-equivariant structured GSWs.

Illustrative n=4096, target ring N=2048 (NOT an author matched benchmark), B=128 (7 bit stages), h=33, 64-bit torus, k=1, one gadget digit for both mask/body:
- S degree D=2nN=16,777,216 coefficient units, one polynomial ~128MiB;
- one RGSW(Y^v) =2 RLWE rows ×2 polys/row×D×8 bytes=536,870,912B=512MiB;
- 34 such gap keys =17GiB before other keys, working buffers, security changes;
- native selector bits: 34*7=238 RGSWs, each 2×2×2048×8=65,536B=64KiB; 238 keys =14.875MiB;
- ratio ~1170.29x in JUST this toy matched-type selector ledger, NOT actual original Table1 (which includes separate key classes). This also shows why simply converting to a big tensor representation revisits the giant-key regime author explicitly contrasts.
- Online one S-EP instead of n*7 base EPs, but tensor EP itself multiplies polynomials 8192× as long. Under a simplistic O(D log2 D) scalar FFT arithmetic proxy, T_old ~n*7*N*log2N, T_new~2nN*log2(2nN); ratio old/new=(7*11)/(2*24)=77/48=1.60417x potential MPmul arithmetic-only speedup, BEFORE memory/cache, ciphertext preparation, security/DFR, packing, n output extraction, h repetitions, new modulus assumptions and additional lower-level costs. NO native speedup measured and no genuine upper bound for arbitrary compressed forms.
S with Y^{2n}−1 is a reducible quotient, not automatically a normal 2-power cyclotomic RLWE ring. Repeated X-secret z(X) across Y components may be treated as a module of many base-ring encryptions but requires its own exact semantic security/KDM/noise proof before use as FHE. Dense GSW row errors convolved across 2nN coeff can be much larger; no DFR or polynomial-noise proof established. Compression of only pseudo-random masks reduces at most part of dense stored ciphertext and does not close the ~1170x structural ratio.

## Novelty/contribution decision
H52 as stated FAILS: ordinary Y negacyclic packing cannot model τ wrap, while exact doubled sheet forces O(n)-larger standard dense tensor-ring GSW and huge key material, for only conditional modest arithmetic headroom under representative sparse h and B. A radically new COMPACT encrypted monomial-control representation with Θ(N log B) storage and sub-n log B online work would be interesting but NONE has been constructed, and old tensored accumulator/ring-packing prior art is close. The two-sheet cyclic semilinear lift is an algebraic representation trick, not claimed new cryptographic theorem or publication-level mechanism.
Do not open another round merely varying n/B or replacing FFT constants; source-first distinct compressed GSW or different major FHE construction required. Keep P0-53 NOT_STARTED; no Codex tasks without new proof/credible headroom.

END_OF_ITERATION:
STATUS: PASS_TWO_SHEET_SHIFT_ALGEBRA / FAIL_SMALL_KEY_ONE_SHOT_MPMUL / NOVELTY_NOT_ESTABLISHED / STAGNATION_HUMAN_REVIEW
RESULT: 16/16 exact ring tests plus 24/24 signed invariant; n4096,N2048,B128,h33 dense selector key rises ~14.875MiB→17GiB (~1170x) for simplistic 1.60x FFT-work MPmul proxy.
NOVELTY: NOT_ESTABLISHED
NEXT_TEST: no automatic P0-53; needs genuinely new compressed monomial selector proof or pivot core algorithm, with real same-security/DFR/whole-system ledger.
STATE_UPDATE: YES isolated finding only.
CODEX_REQUIRED: NO.