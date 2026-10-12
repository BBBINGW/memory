# Iteration 109 — Carousel paper generic rounding bound vs public Go parameter and LUT conventions

Date: 2026-10-12. Primary source Hwang–Min–Song, *Carousel: Fully Homomorphic Encryption with Bootstrapping over Automorphism Group*, ePrint 2024/2032; Research MCP 34pp mirror PDF SHA256 5ddec99ebbe14b270b413e21ab4923abf0ed5dba8d0f1d053b3fde1c5a35d6c8; official VERSION_UNVERIFIED. Fixed author repo SNUCP/carousel commit 21d5800462920d63afcc58873446455642588297.
STATUS: **PASS** general algebraic bound needs divisibility or correct rounding margin; **FAIL** inference that I108 message-specific counterexample directly occurs in the real Go LUT or affects published implemented parameters. No cryptographic attack, implementation correctness flaw, or research novelty established.

## One hypothesis / decisive source-scope test
HYPOTHESIS: Source §3.1–3.2 and actual parameters impose p|N, or a distinct stronger phase-LUT rule, thereby resolving I108 counterexample within the truly claimed implementation scope. Check original pp4,12–16,23–26 and **pinned** Go's compile gate, LUT generator and modulus-switch code; verify exactly one small non-divisible parameter with source LUT semantics and an actual parameter control. No CKKS/HE ciphertext experiment.

## FACTS: paper
- p4 technical overview uses phase round(Nm/p)+e and LUT v_i=f(round(p i/N)) with |e|<N/(2p), asserting f(m) for all m. This algebra is NOT universally valid if p∤N; cf I108 exact tie-free counterexample M829,p5,N92,m1,e−9. 
- §3.1 pp12–13 Algorithm1 only asserts output equals v_(phase modulo N). That assertion is true as a *LUT-index property* independently of message recovery; it does NOT independently claim v_(phase)=f(m) for arbitrary error e.
- §3.2 pp14–16 gives prime cyclotomic M, base prime p0, o=ord_M(p0), N=(M−1)/o, plaintext p=p0^r and CRT/coeff encoding; does not universally assert p|N. The source additionally says it considers conjugate-invariant base rings (footnote physical p11), so I108 M829,p5,o9 **fails that symmetry property** and should not be advertised as slot-mode complete assumption-satisfying example.
- A corrected smallest illustrative algebraic ring-compatible witness that also satisfies even o and N a power of two is **M=449 prime, p0=p5, o=ord_449(5)=14, N=32**; p5∤32. For paper's p4 LUT formula x=m1,e−3: round(32/5)=6, phase3, round(5*3/32)=0≠1 although |e|3<3.2. This is again a mathematical post-modswitch integer phase only, with unquantified RLWE-security/noise distribution.
- §4.2 Theorem4 physical pp23–24 explicitly describes output as rotated lookup message, accompanied by variance bound; Theorem4 is not itself disproved by the generic p4 indexing counterexample. §5.1 p26 Table3 specifies N2048 and p4,p8,p16, all satisfying p|N.

## FACTS: pinned public code
- Repo README publicly describes **under construction**.
- `carousel/params.go` blob SHA 05fbbc8edf0a08e52e28d06ad5ecfa3cb1a0513b, `ParametersLiteral.Compile()` lines228–249: requires `PolyDegree` and `MessageModulus` both powers of two; compiler does not explicitly check p≤N, but supplied presets do, so p|N for those intended p≤N configurations. An arbitrary invalid modulus p5 cannot be loaded into this code by only changing a literal. Warning in code says compiling is not guarantee of security/correctness.
- `carousel/params_list.go` blob SHA 8fd34601da8fd5d0109790800ee55c58b759ba73 defines six presets, N2048, p4,p8,p16, coeff and slot variants.
- `math/poly/evaluator_params.go` blob SHA fbcca9da7b4b296861c63e98f7da24ecc2479380 requires N power-of-two and creates prime cyclotomic M with cyclic automorphism; `NewEvaluatorParametersForPacking` uses base prime2.
- `carousel/bootstrap_lut.go` blob SHA 71acac44c868cc15d408edebad8b35d0c9dae037 lines113–131: constructs LUT via intervals `start=DivRound(x*N,p)`, `end=DivRound((x+1)*N,p)`, then circularly rotates full LUT by `-DivRound(N,2p)` before packing. This is **not identical** to p4's pointwise rounded LUT under non-divisible N,p.
- `carousel/bootstrap.go` blob SHA 53111c68a004cfb36c5f6f368e38a2ccffd6cfae lines35–37 uses Go `math.Round(modSwitchConstant*float64(x)) % lookUpTableSize`. No explicit extra δ_m correction; phase/LUT alignment is through tables and parameter choices.
- Correct rotation interpretation for `RotateInPlace(...,-offset)` is used as `v[i]=raw[(i+offset)%N]` (verified also by N2048,p16 zero-failure control). Note this simulation is exact integer LUT construction, not Go execution nor crypto.

## One exact source-style LUT arithmetic test [DERIVATION/TEST]
Python integer `half_up` corresponds to nonnegative source `DivRound` arguments (no halfway necessary for decisive cases) and source interval fill; offset `round(N/2p)`; LUT lookup at `[round(Nm/p)+e]_N`.
- Non-divisible paper-algebra witness corrected to M449,p5,o14,N32 (prime order and even o); p5 does not divide N32.
- At N32,p5, all 35 pairs (m,e) with strict |e|<N/(2p) checked. **3 fail** in code-style LUT: (m0,e+3)→1, (m2,e+3)→3, (m4,e+3)→0; I108 m1,e−3 becomes CORRECT under source-style LUT, so must not call it an actual code counterexample.
- At N92,p5, 3/95 fail with code-style LUT (different pairs from p4 ideal LUT).
- At author's actual N2048,p16, 0/2032 fail.
- This is NOT a valid invocation of author's compiled binary on N32,p5 (compiler explicitly disallows p5), nor proof of an available 128-bit-secure setting. Exact source-inspired model has no LWE encryption/decryption, key generation, noise tails, key switching, or actual blind rotation.
- I108 old M829 example has odd o9, incompatible with paper's conjugate-invariant context; retain as general coefficient-rotation algebra only, do not reuse to allege complete slot-encoding failure.

## Conclusion and limitation
[PASS] The overview condition |e|<N/(2p) is insufficient in a broader mathematically permissible p∤N ring regime; the corrected even-order M449 example demonstrates this.
[NEGATIVE EVIDENCE] The public **implementation deliberately supports only power-of-two p and N**, with presets p≤N; no implemented parameter failure. Source's actual LUT offset changes the test witnesses, but cannot guarantee original |e| bound for arbitrary nondivisible p.
[NOT PROVED] No cryptographic exploit, no formal theorem proof gap independent of overview, no security parameter materiality, no novel repair. Since elementary missing rounding slack is well-known and no practice affected, recommendation is to PARK this generic p∤N scope clarification pending PI decision and seek a deeper technical gap.
Next I110 recommended: archive/park Carousel p∤N generic rounding-bound microaudit as low technical novelty, then choose ONE new source-grounded FHE hypothesis. If PI prefers scope-repair memo, write it only on explicit request. No authors contacted.
STATUS: PASS scope classification / FAIL actual implementation break hypothesis; STATE_UPDATE YES.

Reproduction: `/mnt/data/iteration109_carousel_source_scope.py`, SHA256 c32bdb286ebeb188cc554f81fbc2540eb874d411f66c6073bd5652aaf251eaeb; `/mnt/data/iteration109_carousel_source_scope_results.json`, SHA256 380e0d95f3e6c4abe1dce6cc932a0990de307f0130c350b9c1040480b52a8550.
