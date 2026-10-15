# CGS-52 — Adaptive shifted-Gram hints recover the exact MLWE secret: a computational-hybrid leakage-composition gate

Date: 2026-10-15. PI-selected SINGLE ACTIVE CGS research; prior root checkpoint CGS51. ONE hypothesis and ONE decisive polynomial-time exact algebra/recovery/decision experiment. The original two-round standard-MLWE threshold-FHE secret-conditioned Gaussian O(LDec) removal remains OPEN. No original Okada–Takagi attack or novel primitive is claimed.

## ONE primary hypothesis and target game

H-CGS52 [FAIL in the stronger multi-hint game]: A standard decision-MLWE challenge (A,b=A s+e) can be publicly shifted to (A,b+A r) with hidden key s+r, and a computational known-covariance proof might harmlessly expose the corresponding shifted Gram hints for several related keys sharing the same secret s while reasoning about their security. Test only TWO explicit nontrivial shifts r=1 and r=X, plus base h(s), in the native even negacyclic ring Rq=Zq[X]/(X^n+1), odd q. If these three hints permit polynomial-time recovery of s, the multi-shift-key-hint proof interface is unsound regardless of computational LWE hardness. This is an explicit STRONGER challenge interface and not the normal one-hint known-covariance security game.

## Primary original-paper provenance and existing results

1. Okada–Takagi, Low Communication Threshold FHE from Standard (Module-)LWE, ASIACRYPT 2025, ePrint 2025/409, https://eprint.iacr.org/2025/409. Actual newer 40 physical-page Research MCP original PDF SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301, VERSION_UNVERIFIED. Section2.2 physical p8 explicitly distinguishes known-norm LWE from known-covariance RLWE; Algorithm7 p29 computes SECRET Sigma_s=sum_i Gram(s_i) to generate correlated Gaussian pads, DOES NOT RELEASE the three shifted hints, and requires per-sid pre-sharing. Any public Gram is hypothetical replacement assumption, not source ciphertext leakage. Shifting MLWE key also changes small-secret KeyGen distribution.
2. Micciancio–Suhl, Simulation-Secure Threshold PKE from LWE with Polynomial Modulus, ePrint 2023/1728 https://eprint.iacr.org/2023/1728, full original 29-page Research MCP PDF SHA256 f72c3839f31b234a94d47d2af3a7fd259167c45595f41a2ec8e021d96f5599e0, VERSION_UNVERIFIED. Section5.3.2 pp16–17 defines known-covariance RLWE with SECRET-AND-ERROR autocorrelation hint. It notes that standard ring equivalence/security was unresolved; no triple same-key shifted oracle is claimed. The difference-of-hints identity ALSO cancels any UNCHANGED error Gram contributions, but that does not make such correlated oracle available in the published experiment.
3. Boudgoust–Jeudy–Tairi–Wen, Hardness of M-LWE with General Distributions and Applications to Leaky Variants, PKC2026 / ePrint2025/1472 https://eprint.iacr.org/2025/1472, full original 35pp MCP PDF SHA256 63d6367243af89b4f495ed9a720c64f424a54221cbb71e6f82d627c8a4a417cb, VERSION_UNVERIFIED; Section6.2.2 pp25–26 considers HNF x*x secret+error hint and says single known-norm leakage can be guessed but full ring known-covariance cannot. Theorem4.1 is SEARCH, not directly low-rank DECISION. No same-key shift composition theorem applies automatically.
4. CGS47–51 previously ruled out straightforward full-ring statistical entropy/hint reduction from small-support native distribution; CGS52 instead falsifies ONE computational rekeying/shift-hint hybrid that might be tried in a reduction. Elementary polarization/shifted-quadratic-query secret extraction is not independently publishable as new cryptography.

## Exact reconstruction lemma [DERIVED]

Let n even, q odd (composite odd q ALLOWED), Rq=Zq[X]/(X^n+1), star involution f*(X)=f(X^-1), Gram ring hint h(s)=s s*.

Suppose the same UNKNOWN s gives three PUBLIC correlated hints:
  h0=h(s);
  h1=h(s+1);
  hX=h(s+X).

All computations below are over Rq. Because 1*=1 and X X*=1,

  u=h1−h0−1=s+s*,
  v=hX−h0−1=s X^-1+X s*.

Multiplying v by X and subtracting u gives
  X v−u=(X²−1)s*.

Now n even and X^n=−1 imply
  (X²−1) [sum_(j=0)^(n/2−1)X^(2j)]=X^n−1=−2.
Because q is ODD, 2 is invertible modulo q, so
  (X²−1)^−1=−(1/2)sum_(j=0)^(n/2−1)X^(2j).

Thus the public three-hint recovery algorithm is

  s*=(X²−1)^−1 (Xv−u);      s=u−s*.

No lattice algorithm, exhaustive search, CRT split or floating approximation is involved. For even n, the fixed inverse and polynomial operations are efficient (polynomial in n log q, O(n²) naive). The result is true modulo q; for a bounded secret with q larger than its coefficient range it reveals the original centered integer coefficients exactly.

**Module rank d**: Let H(s1,...,sd)=sum_i s_i s_i*. To recover a selected component si, keep all other components UNCHANGED and obtain base H0 plus two shifted hints H_(i,+1), H_(i,+X). Contributions from other components cancel in the difference, giving the same u and v for si. With one base hint and 2d suitably component-specific shifted hints, recover the ENTIRE secret module vector. The shifts are public and correlated with the SAME underlying hidden key; independent fresh KeyGen secrets do not satisfy the lemma.

## Computational decision distinguisher in a STRICTLY STRONGER game [DERIVED]

Given a standard sample (A,b=As+e) and the triple of related hints for the SAME hidden secret s, an adversary reconstructs s as above and computes e=b−As in Rq. For coefficientwise error supported on {-1,0,1}, test whether each centered coefficient of e is in that set. For TRUE output the test accepts with probability one. For uniform decision challenge b independent of s,A,h, computed b−As is uniformly distributed over Rq, hence test accepts with probability exactly (3/q)^n for q>3 (regardless of A). Advantage is 1−(3/q)^n. With a module vector the same works given base+2d component-specific hints. **This does NOT apply to a public SINGLE h(s)** or original Algorithm7, so do not call it a known-covariance MLWE break. It also assumes exact finite-support errors; unbounded Gaussian needs a probabilistic acceptance range and tail analysis.

The publicly computable secret shift itself is easy: if b=As+e, then b'=b+A r=A(s+r)+e. But publishing a CONSISTENT hint h(s+r) is not a public linear operation on (A,b); h(s+r)−h(s)=sr*+rs*+rr* contains UNKNOWN mixed terms. More importantly, shifts s+r generally no longer follow the same iid secret χ required by a standard decision-MLWE challenge. Thus this exact three-hint counterexample falsifies only one particular correlated-rekeying/hint-composition proof path, **NOT ALL possible computational reductions**.

## ONE executed minimal gate and exact validation

Script /mnt/data/cgs52_shifted_gram_recovery_gate.py SHA256 b73c5039ed686f0721b2972ad1233c7a49b9644d6539e5dc0142ce2c5a1beed9;
JSON /mnt/data/cgs52_shifted_gram_recovery_results.json SHA256 a1d9baabba3b2049f079a96580abc8fbbee39b4c1812f38429304a0d98238b93.
Executed using ONLY Python integer negacyclic polynomial multiplication and star, exhaustive small support and seeded module tests:
- Complete ternary secret enumeration n2/q17:9; n4/q17 and q97:81 each; n8/q17,q97,q15:6561 each. All base, +1, +X Gram recovery exact PASS, including composite odd q=15.
- Module rank2 cases n8/q97, n16/q97, n8/q15: 512 secret vectors each, both component shifts recovered exact, real b−As equals chosen ternary error in each case. All PASS.
- A tiny complete DECISION game n2,q5,d1 exhausts ALL ternary secrets, 25 public A, all 9 ternary error vectors and all 25 uniform b vectors: real hits 2025/2025, uniform hits 2025/5625, exactly 0.36 uniform accept and advantage 0.64=1−(3/5)^2. This is a new triple-hint game, not source standard decision.
- Separate readable toy n4,q17,s=1−X+X³: h(s)=[3,15,0,2], h(s+1)=[6,13,0,4], h(s+X)=[2,16,0,1]; reconstruct s coefficients mod17 as [1,16,0,1] exactly.

## Scientific assessment and next step

**STATUS CGS52: PASS exact shifted-Gram key-recovery formula and complete algebra/decision-hint toy; FAIL attempt to treat MULTIPLE correlated shifted Gram disclosures as innocuous in a computational reduction; UNCLEAR single-hint decision known-covariance MLWE security, actual FHE public/eval-key game and main two-round no-O(LDec) problem.**

**Novelty / prior art:** polarization of a quadratic oracle is elementary, and shifted leakage reconstruction is well-known conceptually. No research novelty or source-paper error claimed. The value is formally delimiting a concrete security-hybrid interface that CANNOT be used without protecting the covariance hints from composition. Source/PKC2026 only require a single hint per underlying secret and their assumptions are not contradicted.

**NEXT ACTION HUMAN_REVIEW:** Recommend PARK naive public-shift proof strategy and further toy entropy statistics. A legitimate continuation on strict CGS needs a NAMED COMPUTATIONAL DECISION reduction where the reducer can efficiently generate ONE correct h(s) jointly with standard challenge (A,As+e) WITHOUT knowing s, preserve actual χ distribution and simulate source pk/evk/ODec, or a new provable primitive/assumption. If no such candidate, advise PI to pivot to another original FHE correctness/efficiency gap. CGS-53 NOT STARTED; user PI retains final decision. STATE_UPDATE YES own finding, cumulative CGS, authoritative root only.