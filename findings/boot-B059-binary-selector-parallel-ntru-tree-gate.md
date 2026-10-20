# BOOT-B059 — Binary-selector NTRU key re-encoding for balanced grouped blind rotation

Date: 2026-10-20
TRACK_ID: BOOT; SHIP: PAUSED.
STATUS: PASS_EXACT_TYPE_AND_TREE_TOY / PASS_TWO_TERM_LEAF_NOISE_IDENTITY / UNCLEAR_FULL_TREE_NOISE_SECURITY_NATIVE_PERFORMANCE_NOVELTY.

## One primary hypothesis
For the 2026 Dai et al. NTRU grouped blind rotation with binary secret s_j, change the group-first normalized BSK from encryption of X^{s_j}/f to encryption of s_j/f and other unnormalized BSKs from X^{s_j} to s_j. Publish one additional normalized NTRU gadget encryption of 1/f per secret f. This permits each public weight w_j to be applied through sparse plaintext polynomial X^{w_j}-1 instead of per-step automorphism key switching, and lets independent unnormalized leaf products form a balanced tree, then multiply with the group's normalized first leaf.

## Sources
[FACT] Dai, Xiang, Deng, Zhang, Accelerating MKFHE bootstrapping via parallel-friendly NTRU-based blind rotation, Cybersecurity 9:136 (2026). https://doi.org/10.1186/s42400-026-00563-w . Physical PDF p.9 Definition 5, p.10 Eq(4), p.11 Algorithm 2, Appendix B proof Lemma 4. Original group g=n/l: g-1 vector multiplications and g automorphisms, reported 2g-1 costly vector-sized operations, with final-group correction BSK_n.
[PRIOR ART] The binary selector identity 1+(X^w-1)s is standard in TFHE/CMux and appears in https://patents.google.com/patent/EP4335073A1/en . Wan et al., Revisiting Multi-Key Blind Rotation, ePrint 2025/1933 physical p.26, explicitly describes binary-secret key unrolling and paired monomial selectors, citing Li et al. TCHES 2024. No claim of standalone novelty for this identity or tree scheduling. https://eprint.iacr.org/2025/1933 .

## Exact typed construction
Let R_Q=Z_Q[X]/(X^N+1), gadget G_i=B^i, invertible secret f. The noiseless normalized and raw (unnormalized) ciphertext gadget limbs are L_f(v)_i=B^i v/f, R_f(v)_i=B^i v. Their noisy forms add g_i/f. Since s∈{0,1}, X^{ws}=1+(X^w-1)s exactly.
For right leaf C_s=R_f(s), public T^R_w(C_s)_i=B^i+(X^w-1)C_{s,i} has plaintext R_f(X^{ws}), noise numerator (X^w-1)g_i. The deterministic gadget (B^i) is *only* valid in raw type.
For normalized first leaf C_s=L_f(s), extra **secret-generated** normalized K_f=L_f(1), T^L_w(C_s,K_f)=K_f+(X^w-1)C_s has plaintext L_f(X^{ws}), noise numerator g^unit_i+(X^w-1)g^bit_i. One K_f may be reused across groups only after security/correlation audit.
For odd w, N even, X^w-1 has exactly two ±1 coefficients. Under IID mean-zero primitive noise, per coefficient right-leaf variance is 2σ² and first normalized leaf 3σ² when unity and bit encryptions have independent noise; this is NOT end-to-end noise.
The exact gadget product EXT(C,D)_i=sum_j h(C_i)_j D_j with sum_j B^j h(C_i)_j=C_i is typed both L*R→L and R*R→R at the noiseless representation level, even though source only formally presents L*R. The exact noisy residual is e_out = v e_left + sum_j h(C_i)_j e_right,j, which may amplify correlated intermediate errors.

## Verified toy tests
[TEST] Independent Python3 script verify_b059_binary_reencoding.py SHA256 434fda432a7ab99045dba327f6bfc78ef83af332e199dc18d443dd7cea6e7f8f; R=F_257[X]/(X^8+1), f=1+X, B=2,d=9, exact finite-ring coefficient gadget digits. All odd weights and binary s: 288/288 type-converted limbs pass; exact noisy decryption relation 288/288 limbs pass; balanced L(root)*R subtree composition for 300 random groups g=2..16 equals normalized monomial X^{sum w_js_j} across all gadget limbs: 300/300 PASS. This is a mathematical toy, NOT native OpenFHE correctness, DFR, security or timing.
[TEST] Ancillary direct-old-key transform S_w=(X^w-1)/(X-1) on R(X^s) is algebraically correct but uses dense public polynomial, with expected single-coefficient noise variance multiplier N/2 for uniform odd w (N1024 -> 512). The bit-encoding construction avoids this *leaf-level* amplification.

## Cost and noise gate
For g factors, source nominal g-1 products plus g automorphism switches. Candidate g-1 vector products plus g public sparse affine transforms, zero group-local automorphism switches, +1 normalized unity key per secret f; conceptual balanced dependency depth ceil(log2 g), if right-type subtree gadget multiplication remains viable. For g32 source 63 nominal costly operations vs candidate 31 products and 5 serial product layers, NOT wall-clock speedup; source skips some identity automorphisms; pre/post processing and hybrid product unchanged.
[NOISE LIMITATION] Replacing sequential accumulation with a balanced tree moves noisy intermediate R ciphertexts to the right operand. Using the source Lemma 4 bound heuristically as V_out<=V_left+γ V_right, with R leaf V=2σ² and leftmost L leaf V=3σ², a g=2^h balanced tree yields an illustrative bound (2(1+γ)^h+1)σ², unlike source's approximate (2g-1)γσ². At g=32 γ=1: 65 vs63; γ=2:487 vs126; γ=4:6251 vs252. This is a **conditional symbolic recurrence**, not a validated noise bound: source's gadget error distributions and correlations for recursively computed R*R are unverified, and real γ has not been established for a matched parameter set. Critical noise risk; may invalidate the balanced-tree advantage.
[SECURITY] Need prove joint security of changed bootstrap key transcript and K_f=L_f(1); original NTRU encryption of bits vs exponent-coded monomials and reuse of K_f may alter assumptions. No attack or IND-CPA reduction completed.
[NOVELTY] Elementary affine binary selector already known; potential novelty would require new securely analyzable NTRU key encoding/tree-noise design with demonstrable performance advantage over prior MKFHE and key-unrolling work.

## End iteration
STATUS: PASS_ALGEBRA / UNCLEAR_FHE_FEASIBILITY_AND_NOVELTY.
RESULT: B058's right-automorphism interface can be bypassed algebraically by changing BSK encoding; no new secret-dependent transform per right leaf required, but balanced gadget tree creates a potentially severe noise recurrence.
NEXT_TEST B060: ONE decisive source-shaped noisy experiment with same N,Q,B,d, secret and noise distribution for exact original serial group vs candidate binary-selector balanced group; test full residue distributions and noise correlation before claiming security/latency. Obtain native author source if accessible, otherwise a deliberately scoped validated simulator. Check K_f key transcript assumptions and ePrint2025/1933/Li 2024 prior art before publication claims.
STATE_UPDATE NO: existing findings/boot-STATE.md read interface remains unavailable (empty object); do not overwrite. Keep B059 as append-only finding. Full local report and scripts in BOOT_B059_handoff.zip.