# PURE-FHE P0-PRESCOUT-56 — Dense PhaseDecomp Matched Security / Noise / Cost Gate

Date: 2026-10-27, Asia/Singapore
TRACK_ID: PURE-FHE
ACTIVE_SUBLINE: INDEPENDENT_CORE_FHE_ALGORITHM_SCREEN
ITERATION: P0-PRESCOUT-56
STATUS: PASS_MATCHED_TOTAL_WORK_GATE / PASS_SECRET_DISTRIBUTION_SANITY / PASS_RESTART_STRUCTURAL_NOISE_GATE / EXACT_128BIT_SECURITY_AND_DFR_UNRESOLVED
LATEST_COMPLETED: P0-PRESCOUT-56
NEXT_ITERATION: P0-PRESCOUT-57 NOT_STARTED
NOVELTY: NOT_ESTABLISHED
CODEX_REQUIRED: NO
STATE_UPDATE: YES — isolated PURE-FHE finding only.

## Purpose

P0-55 established a rigorous all-digit probabilistic phase-width certificate and a source-shaped dense fixed-weight point:
- N=2048
- n=1800
- q=2^64
- fixed binary weight beta=900
- alpha=4, l=32
- all-digit phase-overflow <=2^-128 with certified width 907<N.

P0-56 performs the promised matched feasibility gate:
1. central fixed-weight secret security sanity;
2. Theorem-4 accumulator-noise/restart implications;
3. matched total analytical work against the paper's dense-key fallback, correcting P0-55's raw blind-rotation-call comparison.

No native execution or Codex.

## Sources

Primary source:
Leonard Schild, Aysajan Abidin, Bart Preneel,
"On Phase Decompositions with Applications to Digit Decomposition,"
ePrint 2026/537, revision 2026-10-25.
Verified eprint.iacr.asia PDF, 17 pages.

Source facts used:
- Theorem 3, p.6: HomTruncTrace output variance
    sigma_Trunc^2 <= alpha sigma^2 + (N/alpha) sigma_Trace^2,
  and truncation uses
    log2(alpha)+N/alpha-1
  automorphism evaluations.
- Algorithm 3 / Theorem 4, p.9:
    sigma_i^2 <= alpha sigma_{i-1}^2 + (N/alpha)sigma_Trace^2 + sigma_br^2
  and
    sigma_out,i^2 <= N(alpha^2+2)/12 * sigma_i^2.
- Section IV-A(a), p.12: restart costs one additional blind rotation and one key switch; restart failure occurs if carry-extraction noise exceeds Delta_h/2.
- Section IV-A(c), p.13: dense fallback partitions [1,n] into Gamma public index blocks, performs Gamma independent decompositions, then homomorphically adds their digit vectors. For an unrestricted uniform binary key, blocks of size beta guarantee the bound and
    Gamma=ceil(n/beta).
  Source cost:
    about Gamma*l blind rotations
    + Gamma(l-1) truncations
    + (Gamma-1)l*c_f encrypted digit-function evaluations
    + O(l*c_f) final conversion,
  plus key/modulus switching before the adder.
  The paper states c_f is about two blind rotations using [8].
- Section IV-A(d), p.13: probabilistic phase bounds are source prior art in spirit; high digits are heuristic in the paper.
- Table II / p.14: truncation cost for N=2048,n=1800 is reported at about 7% of one blind rotation for alpha=16 and 4% for alpha=32; output conversion may require one KS+MS per digit and possibly refreshing bootstrap.

Secondary security sanity:
- current lattice-estimator scheme catalog includes a TFHE-rs LWE instance with n=918,q=2^64,binary secret,TUniform(45);
- Zama TFHE-rs documentation states its parameter sets provide at least 128-bit security according to lattice-estimator.
This is only a sanity baseline, not a matched estimator run.

## 1. Fixed-weight beta=900 security sanity

The proposed key distribution is uniform over

  S={s in {0,1}^1800 : wt(s)=900}.

Its exact entropy is

  log2 binom(1800,900)
    = 1794.267160965... bits.

Compared with iid uniform binary secret entropy 1800 bits, conditioning on exact central weight loses only

  5.732839034... bits.

Equivalently,

  Pr_{s<-{0,1}^1800}[wt(s)=900]
    = 2^-5.732839... .

Thus the fixed-weight distribution is the central slice of ordinary binary secrets, not a sparse-secret regime.

Marginals remain
  Pr[s_i=1]=1/2,
  Var(s_i)=1/4,

with only weak negative pairwise covariance
  Cov(s_i,s_j)=-1/(4(1799)) ≈ -1.3897e-4.

A generic conditioning argument says that an attack specialized to the exact central-weight distribution translates to an attack on ordinary binary-secret instances with only the central-slice probability loss (~5.73 bits in success probability). This is a useful sanity bound, not a substitute for a concrete LWE estimator run.

Importantly, beta=900 is not "sparse" in the sense exploited by sparse-secret hybrid attacks.

### Decision on security

PASS_NO_IMMEDIATE_SECRET_DISTRIBUTION_BLOCKER.

But exact >=128-bit security is NOT CERTIFIED because:
- the source paper is generic and does not pin one input-LWE error distribution for our q=2^64 point;
- current lattice-estimator does not directly model this exact fixed-weight binary distribution as iid Binary;
- no matched estimator run was executed.

Before native implementation, instantiate a concrete input error distribution and run a pinned current estimator.

## 2. Corrected dense fallback block count

P0-55 compared beta_total=900 to beta_block<=127 and wrote Gamma>=ceil(900/127)=8.

That is NOT the published dense fallback guarantee.

The paper partitions PUBLIC INDICES into blocks. For an arbitrary/unrestricted binary key, a block of size at most beta_block guarantees its Hamming weight is <=beta_block. Therefore with

  alpha_base=16,
  N=2048,

the deterministic condition gives

  16(beta_block+1)<=2048
  => beta_block<=127,

and the source fallback needs

  Gamma=ceil(1800/127)=15.

P0-55's Gamma=8 statement is withdrawn.

### Could fixed global weight beta=900 probabilistically reduce Gamma?

For a fixed public block of size m, under a uniformly random global fixed-weight-900 secret, the block weight is Hypergeometric(1800,900,m).

Requiring, by union bound over all blocks,

  Pr[any block weight >=128] <=2^-128

does not materially relax the source partition:
- m=128 with Gamma=15 gives union failure about 2^-131.11;
- m=140 gives only about 2^-85.95;
- m=160 gives about 2^-48.21;
- m=225 (Gamma=8) gives only about 2^-2.95.

The largest tested equal-size block satisfying the 2^-128 global target is m=128, still Gamma=15.

Thus under the same very strong failure target, fixed global weight does NOT justify the optimistic Gamma=8 source fallback.

One could impose a stronger balanced-per-block secret distribution at key generation, but that is a different structured secret distribution and is not the source baseline.

## 3. Matched blind-rotation core work

This is the most important correction to P0-55.

A dense-fallback blind rotation on one block does not necessarily cost a full n=1800 blind rotation; the core external-product work scales with the block's LWE dimension.

### Candidate: single-chain alpha=4

  l=32.

Blind-rotation external-product count, in n-normalized units:

  32 * 1800 = 57,600 EPs.

### Source dense fallback: alpha=16, Gamma=15 blocks

Across all blocks, dimensions sum to n=1800. Therefore per digit the TOTAL block blind-rotation EP work is about one full-n blind rotation, not Gamma full-n rotations.

Over l=16 digits:

  16 * 1800 = 28,800 EPs.

So on the blind-rotation core ALONE:

  candidate / fallback = 2.

The alpha=4 candidate is about 2x MORE expensive in BR-core EP count.

Therefore the P0-55 "128 vs 32 blind rotations => 4x" performance interpretation is invalid and withdrawn.

## 4. Matched truncation work

Theorem 3 gives exact automorphism-evaluation count per truncation

  T(alpha)=log2(alpha)+N/alpha-1.

For N=2048:

Candidate alpha=4:
  T(4)=2+512-1=513.
  31 truncations:
  31*513=15,903 automorphism evaluations.

Fallback alpha=16:
  T(16)=4+128-1=131.
  Gamma*(l-1)=15*15=225 truncations:
  225*131=29,475 automorphism evaluations.

Thus the candidate uses:
- 2x more BR-core EP work,
- but only about 54% as many truncation automorphism evaluations.

Using the paper's empirical statement that one alpha=16 truncation is about 7% of a full n=1800 blind rotation, scaling by T(4)/T(16)=513/131 gives a rough alpha=4 truncation cost of about 27.4% of a full-n BR.

This yields only a rough BR-equivalent decomposition cost:
- candidate: 32 + 31*0.274 ~= 40.5 full-n BR equivalents;
- fallback decomposition before digit addition: 16 + 225*0.07 ~=31.75 full-n BR equivalents.

So the source fallback is still cheaper at the decomposition-only stage.

## 5. Dense fallback adder is the decisive total-work term

The source dense fallback must homomorphically add Gamma independent base-alpha digit vectors.

For Gamma=15,l=16 it requires

  (Gamma-1)l
   = 14*16
   = 224

encrypted digit function evaluations, plus final conversion.

The paper states one such function evaluation c_f costs about TWO blind rotations with [8].

It also requires each block digit to be key- and modulus-switched before entering the adder:
  Gamma*l = 240 intermediate digit conversions,
before final conversion.

The P0-55 single-chain candidate has no cross-block encrypted digit adder at all.

Even ignoring:
- the source's O(l*c_f) final conversion,
- all intermediate KS/MS cost,
- fallback restart costs,

the adder contributes roughly

  224*c_f.

At the source's c_f≈2 BR, this dwarfs the 8.75-BR-equivalent decomposition-stage advantage of the fallback.

A robust break-even calculation is stronger:
Even if the candidate restarted after EVERY digit, adding at most 31 extra BRs, its rough cost becomes

  40.5 +31 =71.5 BR-equivalents
  plus 31 restart key switches.

The source fallback decomposition is ~31.75 BR-equivalents before the adder.

Therefore the candidate still wins total work whenever

  c_f > (71.5-31.75)/224
      ≈0.1775 full-n BR.

The source says c_f is about 2 BR, more than an order of magnitude above this break-even.

Hence the matched TOTAL-WORK advantage survives very conservatively.

Using the source's own c_f≈2 BR and ignoring dimension differences/final conversion gives a rough lower comparison:
- candidate decomposition, no restarts: ~40.5 BR-equivalent;
- candidate with restart after every digit: ~71.5 BR-equivalent + KS;
- fallback decomposition + adder: ~31.75 +448 ~=479.75 BR-equivalent,
  before final conversion and 240 intermediate KS/MS.

Do NOT treat these as measured runtimes.

## 6. Latency is a different story

The source's Gamma block decompositions are independent and can be done in parallel.

With enough parallelism:
- fallback decomposition depth is ~16 digit iterations, not 15*16;
- digit addition can use a binary tree of depth ceil(log2 15)=4;
- each c_f costs about two blind rotations, so adder depth is roughly another ~8 BR-like serial steps, with digits parallelized.

Thus a rough source latency shape is on the order of
  16 decomposition steps + 8 adder-BR steps
before conversions/restarts.

The candidate has 32 sequential digit iterations.

Therefore:
- TOTAL WORK: candidate strongly favored;
- LATENCY under abundant parallelism: candidate may be worse.

No latency-speedup claim is allowed.

## 7. Theorem-4 noise and restart gate

Theorem 4 gives

  sigma_i^2
   <= alpha sigma_{i-1}^2
      +(N/alpha)sigma_Trace^2
      +sigma_br^2.

Without restart, the geometric term is roughly alpha^i.

Across a complete radix decomposition of q=2^64:
- alpha=4,l=32 => alpha^l=2^64;
- alpha=16,l=16 => alpha^l=2^64.

Thus the gross multiplicative variance growth over the full bitlength is not fundamentally worse for alpha=4; it is redistributed over more, smaller-radix iterations.

For a variance-growth cap F, a segment can have approximately

  rho_alpha ~= log_alpha(F)

digits before restart.
The number of restart segments is

  l/rho_alpha
   ~= log(q)/log(F),

approximately radix-independent.

This is only a structural observation; additive sigma_Trace and sigma_br terms matter in concrete parameters.

### Output extraction scaling

Theorem 4 multiplies accumulator variance by

  C_out(alpha)=N(alpha^2+2)/12.

For N=2048:
- C_out(4)=3072;
- C_out(16)=44032.

So for the same accumulator variance, alpha=4's digit output variance multiplier is about

  44032/3072 =14.333...

times SMALLER.

This partially compensates the longer chain.

### Restart cost

Section IV-A(a) states each restart costs:
- one additional blind rotation;
- one key switch;
and introduces a carry-extraction failure event if noise exceeds Delta_h/2.

Even the extreme upper bound of restarting after every one of the remaining 31 alpha=4 digits does not erase the candidate's total-work advantage over the published dense fallback adder, as shown above.

Therefore Theorem-4 growth is NOT a structural cost killer.

However exact full DFR is still unresolved because we do not yet have a matched numerical tuple for
  sigma_br,
  sigma_Trace,
  Delta_h,
  Q,
restart schedule,
output KS/MS noise,
and all union-bounded failure events.

## 8. Security sanity against current TFHE practice

Current lattice-estimator source includes a TFHE-rs LWE instance
  n=918,
  q=2^64,
  Xs=Binary,
  Xe=TUniform(45).

Zama documentation states its parameter sets target at least 128-bit security according to lattice-estimator.

Our candidate's n=1800 central fixed-weight binary secret is much denser than any sparse-secret regime and has only a 5.73-bit conditioning loss relative to ordinary Binary(1/2)^1800.

This strongly suggests the SECRET DISTRIBUTION itself is unlikely to be the limiting security issue when paired with a standard TFHE-scale error distribution.

But no monotonic "n=1800 therefore >128 bits" theorem is claimed.
A pinned current estimator run with the final chosen error distribution remains mandatory.

## Decision

STATUS:
PASS_MATCHED_TOTAL_WORK_GATE /
PASS_SECRET_DISTRIBUTION_SANITY /
PASS_RESTART_STRUCTURAL_NOISE_GATE /
FAIL_RAW_BR_SPEEDUP_CLAIM /
UNCLEAR_LATENCY /
EXACT_128BIT_SECURITY_AND_DFR_UNRESOLVED.

RESULT:
1. P0-55's raw 4x BR-call argument was not a fair cost comparison and is withdrawn.
2. After accounting for block dimensions, the alpha=4 candidate has ~2x MORE blind-rotation EP core work than the alpha=16 dense fallback.
3. The candidate uses fewer truncation automorphisms.
4. The source fallback's required encrypted digit addition is enormous in total work: 224 c_f calls for Gamma=15,l=16, with c_f≈2 BR, plus 240 intermediate KS/MS.
5. Eliminating this adder keeps the candidate strongly ahead in TOTAL WORK even under the extreme assumption of one restart after every digit.
6. The candidate does NOT yet have a latency advantage and may have worse latency under abundant parallelism.
7. Theorem-4 noise growth does not structurally kill alpha=4; exact DFR still needs concrete parameters.
8. Fixed-weight beta=900 is not a sparse-security regime; exact 128-bit security still needs a matched estimator run.

NOVELTY:
NOT_ESTABLISHED.

COMPLETE SPEED:
NO measured speed claim.
Analytical total-work advantage survives; latency unclear.

CODEX_REQUIRED:
NO.

NEXT_TEST P0-57:
Do one full parameter/DFR closure, still without native implementation:
- choose one concrete current TFHE-compatible input error distribution at q=2^64;
- choose accumulator Q and evaluation-key noise;
- compute sigma_br and sigma_Trace from a pinned source/implementation parameter set;
- optimize a restart schedule rho;
- allocate a total failure budget across:
  phase-overflow,
  restart carry failures,
  output digit noise,
  KS/MS conversion;
- run a pinned current lattice-estimator (or document precise blocker) for the fixed-weight secret;
- compare resulting TOTAL WORK and LATENCY against the paper's Gamma=15 dense fallback under the same failure target.

If no concrete parameter set closes at >=128-bit security and <=2^-128 total failure without destroying the work advantage, KILL.
If it closes, candidate is ready for PI decision on native implementation.

STATE_UPDATE: YES — this finding only.
