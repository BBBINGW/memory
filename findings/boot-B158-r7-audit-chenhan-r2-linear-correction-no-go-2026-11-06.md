# BOOT / B158 — R7 audit + Chen–Han r=2 linear-correction boundary

Date: 2026-11-06
Session: 密码学 32.0
Research turn: 1/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Prior durable head supplied by PI: b43d4eb99c8104242e15681cd92aca07719edc9b

## R7 independent source audit (no rerun)

Task: BOOT-B158-R6-STOCK-KEYSET-CONTINUATION-20261105-R7
Pinned HElib: acdb264e1a991eaee35fd8b3c31bebe9528c49a1
Artifact path supplied by PI was not mounted in this Chat runtime, so the artifact bytes/SHA256 could not be independently re-read here. The scientific result therefore remains UNKNOWN / INFRA_BLOCKED / DO_NOT_RERUN.

However, the exact reported exception can be localized independently against the pinned HElib source.

1. `Ctxt::smartAutomorph(k)` checks `pubKey.isReachable(k,keyID)` and, on missing automorphism reachability, throws:
   `no key-switching matrices for k=..., keyID=...`.
2. The exact reported string `No key-switching matrix exists` is thrown instead by `Ctxt::reLinearize` when the current non-canonical `CtxtPart` has no matching direct `KeySwitch` matrix.
3. `addAllMatrices` is automorphism-only: it generates `GenKeySWmatrix(1,i,keyID,keyID)` for every `i in Z_m^*`. Thus an observed stock set of 8192 such matrices does not by itself certify relinearization edges such as `s^2 -> s`.
4. For the reported call `extractDigitsThin(3,1,1)`, HElib does **not** enter the Chen–Han branch because `r=1`; it takes the basic `extractDigits` branch. For p=5, `extractDigits` repeatedly evaluates the degree-5 digit polynomial through `polyEval`, which creates multiplication/relinearization demand.
5. HElib normally creates `s^e -> s` matrices in `SecKey::ImportSecKey` for `2 <= e <= maxDegKswitch`; `GenSecKey` defaults `maxDegKswitch=3`. Therefore the exact missing edge cannot be named from source alone without the R7 key-generation call/handle dump, but the exception class rules out "missing Frobenius/rotation reachability" as the immediate failure and localizes the first repair target to the non-canonical relinearization handle generated during polynomial evaluation.

Audit verdict: INFRA_BLOCKED remains the correct task verdict. Do not reinterpret as candidate failure. Before any repair, inspect/log the failing `CtxtPart.skHandle` at the `reLinearize` assertion and check whether the absent edge is `s^2 -> s` (or another secret-key power/keyID pair). Do not add Frobenius/rotation keys merely in response to this exception string.

## One cheapest decisive Chen–Han r=2 correctness step

Parameters: p=5, e=4, v=2. Let scalar Chen–Han first-step quotient be
[
q_4(x) := (x-G_4(x))/5 pmod{5^3},
]
where `G_4(x)` returns the centered lowest base-5 digit modulo `5^4`.

Aung's correction maps are fixed linear maps of the *original* fresh RMFE encoding. A direct Chen–Han extension would need, at the second outer iteration, a precomputable correction representative for `z_1=q_4(z_0)`. Any such fixed linear map `C_2` from the original encoding would induce a linear decoded map
[
psicirc C_2circphi : (mathbb Z_{5^4})^k 	o (mathbb Z_{5^3})^k.
]
But coordinatewise `q_4` is not additive because of the base-5 carry.

Concrete counterexample in one scalar coordinate:
- centered digit of 2 is 2, so `q_4(2)=(2-2)/5=0`;
- again `q_4(2)=0`;
- centered digit of 4 is -1, so `q_4(4)=(4-(-1))/5=1`.
Hence
[
q_4(2+2)=1 
eq 0+0=q_4(2)+q_4(2)pmod{125}.
]

Therefore **no fixed linear correction map of the original input can supply the exact decoded `z_1` semantics needed by the second Chen–Han iteration for all inputs**. This kills the direct Aung-style strategy "precompute all correction maps linearly in CtxtsToSlots, then run both Chen–Han iterations with one final recode."

Scope: this is not yet a no-go for all nonlinear/carry-aware public corrections of total degree <=45. Such a rescue would have to generate the first quotient's carry-dependent representative nonlinearly during digit extraction, rather than as a linear precomputation from the fresh RMFE input.

Candidate status:
- direct Aung-style linear Chen–Han correction extension: KILLED by carry nonlinearity;
- broader rmfe-chenhan-correction-r2-v1 with nonlinear/carry-aware correction: ACTIVE, correctness unresolved;
- no performance/security/DFR claim.

Next cheapest decisive theorem unit: test whether the degree-45 polynomial data already computed in the first iteration can synthesize an ambient representative of q4(z) whose decoded value is q4(a) and whose residue modulo 5 matches G3(w1), without invoking a recode. Stop at first explicit extension-ring counterexample.
