# BOOT / B158_OVERALL — Successor Research Turn 5/25
Date: 2026-11-12 Asia/Singapore
Phase: PROBLEM_SELECTION
Candidate: boot-b158-public-l19-phase-preserving-modraise-v1
Status: PARKED / FAIL_SECRET_INDEPENDENT_PHASE_LIFT / FAIL_SOURCE_CONSTRUCTION
Native/Codex: NOT_RUN
TRACK_ID BOOT; ACTIVE_SUBLINE B158_OVERALL

## Durable restoration / distinctness
Input controller state ACTIVE=UNKNOWN, BACKUPS=none. The predecessor Turn4 is findings/boot-b158-successor-turn4-period8-reynolds-output-projector-value-gate-2026-11-12.md, verified Git blob 3494b73d5f353099fbb5b7756575b53957423609, status PARKED. The B175 dominant source term finding is findings/boot-B175-source-level-si-error-bounds-2026-10-29.md blob c75aa60e080b28b688de7ee8859c5df4d1951c02. Native B175 artifact: BOOT-B175-B158-CASE1-SI-POINTWISE-NATIVE-20261028.zip SHA256 1b1e49d07d4bf60a27cde1d67474cfcd9f9f2523c53aac1735ca1e13444796fa. Fixed N=32768, T=65537, Q_L18 bitlength649; LT8 required bits577, GROUPED633, failing SI pointwise664, positive ceiling648. Existing L19 prime above L18 is around 30 bits in the B174 source logQ literal (LogQ=[36,34x18,30]); exact effective Q'_L19/Q_L18=last prime remains subject to source prime-order verification.
Distinct from closed Turn25's transient centered Q->QMul basis-extension identity: this proposal changes the PERSISTENT ciphertext modulus before last SI, leaving ciphertext components in enlarged R_Q', rather than extending components temporarily to QMul for an unchanged-Q tensor. Distinct from Turn2 trace-annihilator because no Galois subgroup trace is used; proposed core is public, phase-preserving level raising without EvalMod or re-encryption. It also does not reopen PK gauge, reciprocal preconditioning, secret switching or rescale-only schedule.

## Pre-registered decisive test
QUESTION: Can the stock public componentwise L18->L19 RNS basis extension preserve the exact centered decrypted phase for all ternary secrets and legal ciphertexts, thereby providing approximately one extra prime of fixed-parameter SI headroom without homomorphic modular reduction, key assistance, or new noise?
CURRENT_BELIEF: No: decryption of individually lifted components includes an s-dependent Q-multiple alias which a source-independent choice of representatives cannot generally remove.
CHEAPEST_DECISIVE_TEST: Construct a scalar constant-coefficient counterexample using three legal ternary secrets -1,0,+1 on the SAME publicly visible ciphertext; solve for the integer Q-multiple adjustments required of any independent publicly fixed component lifts. Use exact integer algebra; no native run.
IF_PASS: If one public componentwise lift preserves all centered phases over the full secret/ciphertext domain, admit ACTIVE for L19 BGV source, exact T/scale carry, noise/DFR and all-in cost.
IF_FAIL: If lifting requires mutually incompatible secret-dependent Q-carry corrections even for constants, PARK; no native execution.
IF_UNCLEAR: Verify source basis-extension representative and secret quantifier, retain UNKNOWN, no native run.
WHICH_PAPER_GATE_CHANGES: Killer gate 1, complete whole-phase correctness, preceding source feasibility and value.
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: The candidate's claimed free extra 30-bit headroom requires the SAME message/decryption phase under the larger modulus; a phase alias invalidates its input to the SI multiplication regardless of possible added Q bits.

## Exact source-shaped scalar counterexample and quantifiers
Take any odd Q>3, Q'=Q*p, p odd >=3 and coprime to Q; Q' is the higher-level ciphertext modulus and p an added NTT-friendly prime. Let h=(Q-1)/2 and public ciphertext pair c0=c1=h in Z_Q. For the three valid scalar ternary secret values s=0,+1,-1, the CENTERED old decrypted phases are:
s=0: rho_Q(h)=h.
s=+1: rho_Q(2h)=rho_Q(Q-1)=-1.
s=-1: rho_Q(0)=0.
Any public per-component basis-extension rule that preserves the residues modulo Q must choose integer lifts of form:
c0'=h+Q*k0; c1'=h+Q*k1.
These k0,k1 may be arbitrary functions of the visible pair and public parameters, but cannot vary with the secret s.

If the enlarged-modulus decryption is required to equal the old centered phase MOD Q' for each s, subtracting gives:
s=0: Q*k0 = 0 (mod Q*p) => k0=0 (mod p).
s=+1: Q*(1+k0+k1)=0 (mod Q*p) => 1+k0+k1=0 (mod p).
s=-1: Q*(k0-k1)=0 (mod Q*p) => k0-k1=0 (mod p).
Combining k0=0 and k1=0 from the first and third forces 1=0 (mod p), contradiction because p>=3.
Therefore NO such secret-independent componentwise representative selector exists, even allowing arbitrary publicly computed k_j per coefficient. This scalar constant-polynomial counterexample embeds in R=Z[X]/(X^N+1) for any power-of-two N, so it is also a full-ring counterexample. Every secret choice belongs to the syntactic ternary-secret support, though the full-constant secrets may be exponentially unlikely under a dense product distribution; the result is a worst-case universal semantic no-go, not a DFR lower bound for sampled secrets.

Stock exact centered componentwise ModUpQtoP (pinned source in predecessor Turn25: Lattigo v6.2.0 ring/basis_extension.go blob fb9f0e877d928984b57b1db9917c03417f2fd211, evaluator.go blob 8203be6e7f13adbad2c08cf7cc1ec2b4ac00b04f) cannot eliminate this cross-component, secret-dependent alias by merely choosing a different centered representative for each component. The actual library ModUpQtoP is used for transient basis extension and is not, alone, a noise-refreshed persistent R_Q' ciphertext conversion.

### Why bare added modulus is not guaranteed extra headroom
For integer lifts c0',c1' of a valid R_Q ciphertext, decrypt:
D' = c0'+c1'*s = D+Q*(k0+k1*s).
Old phase is D mod Q; the unknown carry K=k0+k1*s changes the enlarged-phase by Q*K. This term need not vanish in R_Q' and is not necessarily a small multiple of plaintext encoding. In BGV the message-reference embedding and scale metadata also depend on ciphertext modulus and exact multiplication mode, so simply reusing old references after lifting cannot be presumed correct.
The B175 noise requirement is 16 additional required-bit margin if final SI increment remains 31. The presence of an existing ~30-bit top RNS prime is only nominal potential. It proves neither corrected semantics nor 16-bit gain. Making the legitimate lifted ciphertext correct would require encrypted modular reduction/key assistance/refresh or a wholly new representation/carry invariant; those change scheme/cost and are NOT silently provided by the candidate.
This is not the same no-go as Turn2: a source-compatible custom even-modulus trace might cancel a specific carry but remains outside stock. Nor is this a no-go against full BGV bootstrapping. Relevant public background:
- https://pkg.go.dev/github.com/tuneinsight/lattigo/v6@v6.2.0/ring documents RNS BasisExtender.ModUpQtoP, NOT an automatically refreshed ciphertext.
- https://fhetextbook.github.io/ModulusBootstrapping1.html (BGV modulus-bootstrapping needs extra homomorphic processing to eliminate overflow).
- Survey https://link.springer.com/article/10.1186/s42400-025-00384-3 (CKKS ModRaise phase includes qI and EvalMod removes it).
No claimed independent audit of these external paper versions; source-level history above is pinned.

## Killer gates / research value
Gate1 FULL SEMANTIC: FAIL for the concrete universal phase-preserving public component-lift construction. This prevents admission to ACTIVE.
Gate2 STOCK: a basis extender exists, but it cannot itself supply the secret-dependent phase/carry correction and does not constitute a stock persistent ciphertext refresh. Candidate as specified fails construction feasibility.
Gate3 OPTIMISTIC COMPLETE VALUE: no justified useful noise/DFR margin after accounting for unknown Q alias; any additional corrective protocol incurs nonzero online work, keys, memory, possible security parameter changes. No numerical performance claim, no DFR bound and no baseline-matched candidate result. The precise construction is classical uncorrected modulus raising, with established CKKS/BGV bootstrap overflow handling as closest prior art; novelty PREFLIGHT, not CLEAR.
Verdict: FAIL_SECRET_INDEPENDENT_PHASE_LIFT -> PARKED. NO_CREDIBLE_NEW_MECHANISM in the precise free public-lift candidate. Not a strict no-go for secret-assisted encrypted-carry schemes, certified restricted secret/ciphertext families, or full bootstrapping.
REOPEN_CONDITION: Provide a concrete public or cryptographically evaluated Q-carry correction with exact BGV scale/whole-output preservation for the B175 legal domain, a useful >=16-bit fixed-parameter DFR/noise recovery, stock or specified custom key/interface feasibility, independent prior-art distinction and complete online/offline/security/memory/runtime cost. Replacing centered ModUpQtoP or re-running uncorrected ModRaise does not qualify.
ELIMINATED_UNCERTAINTY: Can the stock per-component public lift L18->L19 guarantee centered-decryption phase preservation for all ternary secrets, so the existing ~30-bit top prime is a free precision rescue? No, exact scalar counterexample.
DECISION_CHANGED=true; no native, no new TASK_ID, frontier not declared exhausted.
