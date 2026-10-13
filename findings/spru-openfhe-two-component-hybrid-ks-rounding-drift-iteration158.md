# Iteration 158 — Two-component source-consistent HYBRID KeySwitch decryption need not cancel ApproxModDown conditional bias

**Date:** 2026-10-13. PI authorized “好的，请继续” following I157. Exactly ONE precise claim and ONE source-matched two-component exact minimal test. No actual OpenFHE encryption execution, precision/runtime claim, original paper correctness failure, or exploit.

## Read before write and original evidence

Read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md`, `STATE.md` after I157 SHA `b71f51c7ad97579f1f3c9e9ec9a03e1c8bc75cf7`, I157 `findings/spru-openfhe-hybrid-approxmoddown-rounding-conditional-bias-iteration157.md`, and I156. Target paper Coron–Köstler, *Low-Latency Bootstrapping for CKKS using Roots of Unity*, ePrint 2025/651 (previously acquired GitHub-mirror 42pp, PDF SHA256 `2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6`, official version VERSION_UNVERIFIED), §3.4 Lemma5 p11: KS is approximately division by special modulus P with **norm-bounded** (not mean-zero guaranteed) error. No source-paper error claim.

**Tagged, exact OpenFHE v1.4.2 source re-read via GitHub connector:**
- `openfheorg/openfhe-development/src/pke/lib/keyswitch/keyswitch-hybrid.cpp` blob `552fee8fc52c4ee12176e6b9a2ca279b079b7cbc`. `KeySwitchGenInternal(oldPrivateKey,newPrivateKey,ekPrev=null)` Q-part `b=-a*sNew+P*sOld+ns*e`, P-part `b=-a*sNew+ns*e`, congruent modulo P; choose CKKS noise scale `ns=1`. `KeySwitchInPlace` uses `KeySwitchCore→EvalFastKeySwitchCore`; `EvalFastKeySwitchCoreExt` makes `cTilda0=Σ digit*b`, `cTilda1=Σ digit*a`; `EvalFastKeySwitchCore` applies **two separate** `ApproxModDown` calls. `KeySwitchInPlace` preserves/adds input `cv[0]` to output `ba[0]`, and replaces `cv[1]` with `ba[1]` when original cv length 2.
- `openfheorg/openfhe-development/src/core/include/lattice/hal/default/dcrtpoly-impl.h` blob `0fec66253228c4d6f36526f6f63d62c146fe39ca`. `ApproxSwitchCRTBasis` and `ApproxModDown` for one P and one Q, CKKS t0 yield `Down(x)=((x modQ)−((x modP) modQ)) P^{-1} modQ` with **canonical nonnegative P residue**, independent of source Eval format when correctly transformed to coefficients.
- `openfheorg/openfhe-development/src/pke/lib/schemerns/rns-pke.cpp` blob `4e46c873112c617713a9b5bb4f70c5fd916b17c8`, `PKERNS::DecryptCore` about line198: `b=cv[0]+cv[1]*s+...`, so **plus** convention verified directly.

## ONE hypothesis and falsifier

**[HYPOTHESIS TO FALSIFY]** Although I157 single-component `ApproxModDown(P+E)` maps centered `E=±1` to an error with mean `−1/2`, a *complete source-compatible two-component* private-private HYBRID switching key `(b,a)`, both down-converted separately and decrypted as `ct0+sNew*ct1`, automatically cancels this conditional bias.

**[FALSIFIER]** Give ONE valid small pair `(b,a)` satisfying both Q/P congruence equations under chosen secrets, one switching digit corresponding to current ciphertext, and a centered ±1 key error, for which the **post-downconversion decrypted error** has nonzero mean. Check e=0 baseline for correctness; no parameter scans.

## One exact source-equation instance

Work with one Q=17 and P=5, coprime primes (both 1 mod4, so this can be embedded into constant-polynomial sector of a negacyclic `N=2` toy `Z_85[X]/(X²+1)` with 4th roots; actual OpenFHE/author use vastly larger, secure N,Q,P). Choose

```
  sOld=1, sNew=1, P=5, Q=17, ns=1,
  digit d=1, a=5 (nonzero uniform-a possible value mod QP=85),
  E uniform{-1,+1}, b=-a*sNew+P*sOld+E=E,
  original ciphertext (cv0,cv1)=(0,1), decrypts under sOld to 1.
```
At the P tower, P*sOld=0 modP, so source `b_P=-a_P*sNew+E_P` and at Q `b_Q=-a_Q*sNew+(P modQ)*sOld+E_Q` hold simultaneously. `a=5` has residues `a_Q=5,a_P=0` and b is one consistent CRT integer (e=-1 represented as 84 in [0,85)). The input digit d=1 has consistent Q/P representations after the source single-partition approximate basis expansion (the one-Q basis lift of 1 is 1); thus `cTilda0=b`, `cTilda1=a`, no fabricated independent Q and P limbs.

For P5,Q17, inverse(P)=7 mod17. Exact results:

```
 E     b (mod85)   Down(b) mod17 (centered)   Down(a)   DecNew=Down(b)+Down(a)   ideal   error
 -1       84                    -1                1                 0              1       -1
  0        0                     0                1                 1              1        0
 +1        1                     0                1                 1              1        0
```

Code-equivalent identities:
```
   b + a*sNew = P*sOld + E  mod QP;
   Down(-1)=-1, Down(0)=0, Down(+1)=0, Down(P)=1  mod Q;
   DecNew(e=-1)=0, DecNew(e=+1)=1, baseline DecNew(e=0)=1.
   E[DecNew − d*sOld | a=P,sOld=sNew=1,d=1] = (-1+0)/2 = −1/2.
```
Exact test executed with integer modular arithmetic in `functions.exec` (no random sampling). All source congruences, zero-noise baseline, two downconversions, sign-lifted modQ decryption, and nonzero conditional mean were asserted. The same simple algebra `a=P,b=E,d=1,sOld=sNew=1` works for **any coprime odd P,Q** with single-P/one-Q canonical-residue specialization, because `Down(-1)=-1` and `Down(P)=1` modQ. This is not a theorem about the multi-prime implementation's typical distribution. Fixed a=P corresponds to the exceptional zero-P-tower public sample (probability roughly 1/P for uniformly distributed a_P per scalar coefficient); **do not claim typical bias without averaging over true a and actual key-error distribution**.

## Meaning, what survived and what failed

**[NEGATIVE, scoped]** The universal “the second output component automatically cancels the first component's rounding bias” claim is **FALSE** even with a true source key equation and plus-sign decryption, because one source-consistent conditional sample has post-decryption error `−1` or `0` equiprobably with conditional mean `−1/2`.

**[SURVIVED]** I156 remains mathematically true in the pre-rounded conditional independent/centered error model. I157's isolated component drift can **sometimes** survive full decryption. The correct decomposition is still `Z_j=B_j+M_j` with `B_j=E[Z_j|F_previous]` and `E[M_j|F_previous]=0`; this statement alone supplies no quantitative source precision result.

**[CRITICAL LIMIT]** Tiny insecure parameter choice, degenerate but admissible public a=P, extremely artificial centered two-point distribution (source uses actual discrete Gaussian), chosen digit/ciphertext, only single Q/P tower, constant-polynomial specialization. No real OpenFHE algorithm executed, no proof of nonzero *unconditioned* mean over uniform a, no bound on B_j at N32768/h64, no physical Gaussian/CKKS 14-bit noise/precision failure, no contradiction of paper Lemma5 or new publishable technique. Further toy drift examples risk being trivial and low-novelty; do not simply re-run alternate small P/Q values.

## End of Iteration 158

**STATUS:** **FAIL** mandatory full-two-component bias cancellation / **PASS** exact source-consistent conditional survivor / **UNCLEAR** actual high-dimensional HYBRID KS expected error & Table2 precision.
**RESULT:** For a=P5, Q17, sOld=sNew=d1, fresh centered E±1, actual two-component b=-a*sNew+P*sOld+E gives Decrypted Down(b)+sNew Down(a) errors −1,0 with mean−1/2; zero-noise baseline is correct. Conditional survivor does not imply typical source distribution behavior or accuracy significance.
**NEXT_ACTION:** If PI continues: ONE **source-relevant distribution** gate rather than fourth low-value toy: with a uniformly random modulo-P sample, a specified symmetric discrete key-error law and fixed digit, compute averaged post-decryption **incremental** key-error conditional mean relative to the same public a with e=0, distinguishing baseline rounding bias. If mean vanishes or is bounded insignificantly under realistic modulus/scale, PARK noise-bias microaudits. Otherwise quantify an actual Table2-aware conditional bias and noise budget before claiming benefit. Consider HUMAN_REVIEW/pivot if this yields only conventional O(1) rounding.
**STATE_UPDATE:** **YES** — resolves I157's complete-two-component cancellation gate and pins precise full source call/evaluation/decryption formulas. Does NOT revise P1 vFHE source gate.
