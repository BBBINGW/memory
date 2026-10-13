# Iteration 159 — Uniform HYBRID public key a cancels the symmetric fresh-error *incremental* mean in one-Q/one-P scalar toy

**Date:** 2026-10-13. Human PI explicitly authorized one continued I159 test with “好的，请继续” after I158. Exactly ONE hypothesis, ONE exhaustive deterministic distribution gate, read-before-write. Target: whether the prior **exceptional conditional** bias at fixed public a=P predicts a genuine **unconditional incremental key-error bias**; no parameter sweep, full OpenFHE program, manuscript flaw, or publishable contribution claim.

## Sources and starting state

- Read `START_RESEARCH_SESSION.md` → `RESEARCH_PHILOSOPHY.md` → `AGENT.md` → `STATE.md` (after I158 blob SHA `18a3b5a96281c7e35cda52f5085f31f1d6281d1b`) → `findings/spru-openfhe-two-component-hybrid-ks-rounding-drift-iteration158.md`.
- Original Coron–Köstler, *Low-Latency Bootstrapping for CKKS using Roots of Unity*, ePrint 2025/651 §3.4 Lemma5, physical p11 of Research MCP mirror PDF SHA `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6`, official latest PDF version still VERSION_UNVERIFIED. Lemma5 **norm-bounds** rounded KS error; does **not** claim zero mean or provide a Table2 variance improvement.
- Primary code: OpenFHE upstream **tagged v1.4.2**, `src/pke/lib/keyswitch/keyswitch-hybrid.cpp` blob `552fee8fc52c4ee12176e6b9a2ca279b079b7cbc`, `KeySwitchGenInternal` source Q part `b=-a*sNew+P*sOld+ns*e` and P part `b=-a*sNew+ns*e`; `EvalFastKeySwitchCoreExt` combines digits against (b,a); `EvalFastKeySwitchCore` separately `ApproxModDown`s both resulting QP components. `src/core/include/lattice/hal/default/dcrtpoly-impl.h` blob `0fec66253228c4d6f36526f6f63d62c146fe39ca`, for one P/Q the canonical-residue mapping is `Down(x)=((x modQ)-(x modP))*PInvModQ modQ`. `src/pke/lib/schemerns/rns-pke.cpp` blob `4e46c873112c617713a9b5bb4f70c5fd916b17c8`, `DecryptCore` uses positive ct0+ct1*sNew.
- **I158** archived at `findings/spru-openfhe-two-component-hybrid-ks-rounding-drift-iteration158.md`: conditioning on atypical `a=P`, one-P/one-Q exact scalar relation and e=±1 yields conditional mean −1/2 of the **total decrypted error**. This did not establish mean under actual public-a sampling, and e0 deterministic down-conversion error was not separated.

## ONE hypothesis and falsification condition

**[HYPOTHESIS]** For source-shape **private→private HYBRID KS** with `P=5,Q=17,sOld=sNew=d=1,ns=1`, public `a` **uniform over Z_(P*Q)** independent of the centered symmetric fresh switching-key error `e∈{-1,+1}`, the **incremental decrypted error**
```
  Delta(a,e) = Center_Q(DecNew(a,e) - DecNew(a,0))
```
has **zero unconditional expectation** even though some `a modP` classes have nonzero conditional drift; it is bounded by 1 in absolute value. Here `DecNew(a,e) = Down(P-a+e) + Down(a) modQ`, with each component down-converted separately and then decrypted against `sNew=1`.

**[FALSIFIER / ONE MINIMAL TEST]** Exhaustively enumerate all `a∈{0,...,84}` × `e=±1` (170 pairs), using integer modular arithmetic exact to source single-P/Q down-map. Compute **(a)** conditional `E_e[Delta|a modP]`, **(b)** unconditional E, variance, max|Delta|, **(c)** noiseless `e=0` baseline `DecNew(a,0)-1`. Any nonzero unconditional E kills centeredness hypothesis. Do NOT confuse baseline with incremental error.

## Exact exhaustive results

```
P=5, Q=17, PInvModQ=7, 85 public-a choices × 2 errors = 170 exact assignments.

a modP   count of a   Delta for e=-1   Delta for e=+1   E_e[Delta|a]   baseline(Dec(a,0)-1)
   0         17             -1                  0             -1/2                0
   1         17              0                 +1             +1/2               -1
   2         17              0                  0                0               -1
   3         17              0                  0                0               -1
   4         17              0                  0                0               -1

E_{a,e}[Delta]                     = 0
E_{a,e}[Delta²] = Var(Delta)      = 1/5 = 0.2
E_{a,e}[|Delta|]                 = 1/5 = 0.2
max |Delta|                       = 1
E_a[DecNew(a,0)-1]               = -4/5 = -0.8
```

Executed `functions.exec` exhaustive exact integer arithmetic with 10 explicit checks for sample cardinality, residue uniformity, special conditional biases ±1/2, zero unconditional mean, 1/5 second moment and max1 bound, and nonzero baseline mean; all passed. No Monte Carlo simulation. The original ciphertext `cv=(0,1)` decrypts under old s1 to ideal1, the switching key satisfies `b=-a+P+e` modulo both P and Q for every a,e, and the digit=1 is valid source-extended single Q partition. This is an exact toy instantiation of the source's algebra, not a compiled OpenFHE run.

## Minimal analytical explanation

For `P=5` and centered e=±1, the only input P-residue crossings in `Down(P-a+e)` are:
- `a modP=0`: `b0=P-a` is divisible by P, e=-1 crosses down, yields incremental −1 with probability 1/2, hence E_e Delta=−1/2.
- `a modP=1`: `b0=P-a` ends P-residue P−1, e=+1 crosses up, yields +1 with probability 1/2, hence E_e Delta=+1/2.
- other classes: no crossing with e=±1, increment0.
Both boundary classes have probability1/P under uniform a, giving exact unconditional cancellation. More generally for centered independent integer e with sufficiently small support to avoid **mod-Q difference center-lift aliasing**, averaging the Euclidean quotient increment `floor((u+e)/P)-floor(u/P)` over uniformly random u modP gives **e/P**. Therefore E_e[e]=0 implies unconditional incremental mean0 in this particular uniform-residue model. General larger e, actual discrete Gaussian tails and modulo-Q aliasing need separate justification; this iteration only empirically enumerates e=±1.

The **noiseless baseline** has bias `−(P−1)/P` because `Down(P-a)+Down(a)=1` iff `a≡0 modP`, otherwise 0 (modQ). This is the ordinary deterministic RNS quotient/rounding component and appears even for e=0. Its mean is **not** 0: averaging the **full total error** instead of Delta would confound preexisting rounding with new key-error increments.

## Scientific judgment and strict caveats

**[PASS IN NARROW TOY]** The rare fixed-public-a conditional I158 drift does **not** imply an unconditional *new key-error* mean drift for a uniformly sampled public key; averaged incremental drift exactly cancels. I156's ideal martingale conclusion is not proven for actual source: when conditioning on **public a**, the toy incremental means are nonzero in two residue classes and the baseline deterministic component is biased.

**[NEGATIVE FOR RESEARCH VALUE]** This provides no new FHE algorithm or better precision theorem. It is a standard random-residue rounding-cancellation identity; `Var Delta=1/P` and `|Delta|≤1` are exact for this single scalar toy but not source Table2 RNS/large-N physical variances. An ordinary O(1) coefficient-rounding remainder may be tiny after CKKS scale `Delta` division, but no source-valid amplification/noise budget has been computed, so do **not** quantify impact as negligible for end-to-end SPRU.

**[OPEN]** Multi-prime, actual ternary/Gaussian keygen distribution; full ring coefficient and large-N canonical slot dependence, conditional on public key/ciphertext adaptivity, repeated fixed evaluation keys across bootstraps, 8 HYBRID rotations, subsequent rescale and multiplicative stages. Neither zero-mean source-total error nor SPRU 14-bit precision follows. Current PDF is not latest-official-verified. Original Lemma5 bounded-error result is not challenged by these tests.

**[RECOMMEND / HUMAN_DECISION]** **PARK this microaudit line after I156–I159:** the effect was reduced to conventional modular-rounding residues, and I159 finds no systematic *fresh key-error* drift after averaging public a in the source-shaped minimal model. Resume only if there is an actual source-valid multi-prime/large-N covariance/tail proof with a quantified Table2 improvement, or a genuinely new algorithmic cost frontier—not another small modulus toy. The PI retains the final park/pivot decision. Parent vFHE P1 remains OPEN/SOURCE-GATED and I152–154 integer code repairs PARKED.

## End of Iteration 159

**STATUS:** **PASS** uniform-a cancellation of incremental mean in source-shaped 1P/1Q symmetric-e toy; **FAIL** interpreting previous conditional-on-a I158 drift as generic systematic fresh-error drift; **UNCLEAR** actual OpenFHE HYBRID multi-prime/CKKS runtime precision.
**RESULT:** Exactly 170 assignments: conditional drift ±1/2 in two equal-probability public residue classes, unconditional E Delta=0, Var Delta=1/5, max|Delta|1; importantly e0 baseline total rounding error mean −4/5, so increment must not be conflated with total error.
**NEXT_ACTION:** **HUMAN_REVIEW recommended PARK/PIVOT**. No additional elementary key-switching bias examples; next useful SPRU work requires an actual multistage/multi-prime source-based error bound and a quantified gain, otherwise PI chooses higher-value backlog direction. Do not return to source-blocked vFHE without official PDF or new premise.
**STATE_UPDATE:** **YES** — closes unique source-grounded distribution test and records recommendation to park low-novelty SPRU noise microaudits; active strategy remains PI-controlled.
