# BOOT / B158 — Research Turn 23/25 — final first-F4 branch factor alignment and uniform prime-prefix gate

**2026-11-03 Asia/Singapore.** Same logical Research Turn 23; Turns 1–22 final and untouched. TRACK_ID=BOOT; ACTIVE_SUBLINE=B158_CHECKPOINT_DECOUPLED_HALF_BASIS; candidate=legacy-484479fe4613 (PRE-TAG + POST-DIVIDE); phase=CORRECTNESS_GATE; first polynomial F4(x)=x^5−5x^3+5x. **No Native/Codex execution.**

## Authority / read-before-write
Verified `BBBINGW/memory` main HEAD `2ceef0d6205bf032b90af4e3487571d589a11196`. Prior-artifacts read without modification:
- `findings/boot-RMFE-postdivide-turn22-first-F4-outer-mul-prime-prefix-window-gate-2026-11-03.md` blob `cd158091eae6036a2d63f5942b9b1626bae9ee7c`.
- `findings/turn22-outer-f4-prime-prefix-window-derivation.md` blob `01381a2a7098e94eace04582f7a14d90505bde8d`.
- `findings/turn22-outer-f4-prime-prefix-source-audit.md` blob `7696a17405337610038da25a405e7172e9661720`.
- `findings/turn21-xminus1-factor-alignment-derivation.md` blob `6d10eae4307bee92831d5e6e71a85d3d7df52c42`.
- `findings/turn21-xminus1-factor-alignment-source-audit.md` blob `7acc0261fbb8996911b857012519526b23842e31`.
- Pinned HElib `homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1` `src/Ctxt.cpp` blob `b346fcd52ddf6bd5c778a918865cc6bb5143787f`; `include/helib/Ctxt.h` blob `da4be8176cc074a409afbace647b16fac47642c8`.

This target was checked absent (404 and directory-listing negative) before write. Dedicated Notes reads returned empty objects even for known existing text, so prerequisite recovery used the direct connected GitHub read API. Direct GitHub write connector rejected file creation with HTTP403; the dedicated Notes writer is being used. Do not infer successful persistence until a remote read verifies this exact content.

## One hypothesis / falsifier
At the Turn22 source-guaranteed ordered ctxt-prime prefix `P` with `q=product(P)` and `183<=log2(q)<247`, can the final sibling `x²+5x` be constructed entirely at P, explicitly aligned with outer product factor `d=a^5*q^4 mod625` without noise-estimator-driven harmonization, and can the completed F4 independent coefficient-L1 envelope be proved <0.48q uniformly for **every** q in the window? Fail if exact BGV scalar-5 metadata changes, aligner is nonunit, an addition requires implicit coordination, or the conservative final strict inequality fails.

## Exact polynomial and BGV factor ledger
Set `a=67`, ptxtSpace=625, and input ciphertext `X` fixed on `P` with intFactor `a`. Reuse `X2=X²` (factor `b=a²q mod625`). Existing Turn21 left branch `U=X*(X2-6)+(X-1)=x³−5x−1` has `c=a³q² mod625`. Existing Turn22 outer product `T=U*X2=x⁵−5x³−x²` has `d=c*b*q=a⁵q⁴ mod625`. Do **not** repeat the Turn22 outer-product source audit.

NEW sibling `S=x²+5x`:
1. `V=copy(X)`; invoke the integer-scalar BGV **`V.multByConstant(5L)`**, not `mulIntFactor(5)` and not a float overload. Pinned `Ctxt::multByConstant(const NTL::ZZ&)` computes `c0=5`, `gcd(c0,625)=5`, `c1=1`, `c1_inv=1`: multiplies each ciphertext part by exactly 5 and **keeps intFactor a and ptxtSpace625**. Thus `E_V<=5A`.
2. `h1 = (b*inv(a)) mod625 = a*q mod625`. Apply private/internal `V.mulIntFactor(h1)`: factor becomes `a*h1=b`, plaintext remains `5x`, envelope `<=5*U1*A` where `U1=abs(balRem(h1,625))<=312`.
3. `S=X2+V`: same key, same ordered prefix P, same ptxtSpace625, exact equal intFactor b. `Ctxt::addCtxt` has no set difference to mod-up and no factor-harmonization branch; `intFactor(S)=b`, `E_S<=E2+5*U1*A`.
4. `h2=(d*inv(b)) mod625 = a³*q³ mod625`. Apply `S.mulIntFactor(h2)`. Its plaintext stays `x²+5x`, factor becomes `b*h2=d`, envelope `<=U2*(E2+5U1A)`, `U2=abs(balRem(h2,625))<=312`.
5. Add `F=T+S` at matching P, ptxtSpace625 and intFactor d. Then `F=(x³−5x−1)x²+(x²+5x)=x⁵−5x³+5x`. No stock implicit factor harmonization at either add.

Every ctxt-prime is coprime to p=5, hence q, a=67, and both h1,h2 are units mod625. The pinned `mulIntFactor` is a **private Ctxt member** in Ctxt.h, so a minimal internal Ctxt sibling/helper is required; a public-only unmodified API promise would be false. This is an implementation-contract requirement, NOT an algorithmic obstruction. No secret data/new evaluation keys/new digit partition is introduced. The orientation (scale the small sibling to d rather than the outer product to b) avoids an unnecessary potential factor312 multiplier on the leading E_T bound.

Source anchors (pinned commit): `src/Ctxt.cpp` lines ~2033–2068 for integer-scalar multByConstant; ~330–340 for mulIntFactor; ~1445–1457,1475–1535 for addCtxt set/factor coordination; ~1563 onward for BGV tensorProduct factor `f1*f2*q`.

## Complete first-F4 independent L1 bound
Retain **exactly** Turn21–22 bounding vocabulary, no HElib heuristic noiseBound:
```
A(q) = (q/Q0)*E0 + R
E2(q) = A(q)^2 + K(q)
E3(q) = A(q)*(E2(q)+1872) + K(q)
C1(q) = abs(balRem(a*q,625)) <= 312
H(q)  = abs(balRem(a^2*q^2,625)) <= 312
E4(q) = E3(q) + H(q)*(A(q)+C1(q))
U1(q) = abs(balRem(a*q,625)) <= 312
U2(q) = abs(balRem(a^3*q^3,625)) <= 312
E_T(q) <= E4(q)*E2(q)+K(q)
E_S(q) <= E2(q)+5*U1(q)*A(q)
E_F4(q) <= E4(q)*E2(q)+K(q)+U2(q)*(E2(q)+5*U1(q)*A(q))
```
Correlated reuse of X and X² does not invalidate L1 triangle/submultiplicativity. No K is added for plaintext scalar5 or ciphertext addition; K is already charged for each actual relin multiplication.

Preflight assumptions (not newly established here):
`E0<=1.1433532886831608e35 <2^117`; `Q0>=2^399.5>2^399`; `R<=83891200000`; `K(q)<=K_full<=401679183790908.6`; `183<=log2(q)<247` (Turn22 exact first-crossing prefix, possibly partial final digit); valid prior coefficient-L1 and mod-down/relinearization contracts.

For all such q:
`(q/Q0)*E0 < 2^(247-399+117) = 2^-35 < 1`.
Thus `A(q)<Ahat=83891200001`, `K(q)<Khat=401679183790909`. Use all balanced residues bounded by312. Pure integer domination certificate:
```
Ahat=83891200001
Khat=401679183790909
E2hat=Ahat^2+Khat
     =7037733839286966190910
E3hat=Ahat*(E2hat+1872)+Khat
     =590403937065428472512879468383691
E4hat=E3hat+312*(Ahat+312)
     =590403937065428472539053522881347
EThat=E4hat*E2hat+Khat
     =4155105766733618287140112599225808289479411355663746679
EShat=E2hat+5*312*Ahat
     =7037733970157238192470
EFhat=EThat+312*EShat
     =4155105766733618287140112599228004062478100413979797319
100*EFhat
     =415510576673361828714011259922800406247810041397979731900
48*(2^183)
     =588478287692501321609605258425718726509595822918503235584
```
The strict integer inequality `100*EFhat < 48*2^183` proves `E_F4(q)<EFhat<0.48*2^183<=0.48*q` for **the entire** guaranteed prefix window. Ratio `EFhat/(0.48*2^183) ~=0.7060763079342008`; margin `~0.5021039863` bits. No runtime q, noiseBound, capacity, naturalPrimeSet, or stock harmonization is assumed.

Independent finite integer verification enumerated all `phi(625)=500` unit residues q mod625: in every case `a*h1=b`, `b*h2=d`, `c*b*q=d` modulo625; h1,h2 are units and the maximal absolute balanced representative is312. This is a purely algebraic check, **not** a Native/ciphertext experiment. Minimal reproducer:
```python
from math import gcd
p=625; a=67; count=0
for q in range(p):
    if gcd(q,p)!=1: continue
    b=a*a*q%p; c=a**3*q*q%p; d=a**5*pow(q,4,p)%p
    h1=a*q%p; h2=a**3*pow(q,3,p)%p
    assert a*h1%p==b and b*h2%p==d and c*b*q%p==d
    assert gcd(h1,p)==gcd(h2,p)==1
    count+=1
assert count==500
A=83891200001; K=401679183790909
E2=A*A+K; E3=A*(E2+1872)+K
E4=E3+312*(A+312); ET=E4*E2+K; ES=E2+5*312*A
EF=ET+312*ES
assert EF==4155105766733618287140112599228004062478100413979797319
assert 100*EF<48*(2**183)
```

## Verdict, limitation, next decisive test
**PASS_FIRST_F4_FINAL_SIBLING_EXPLICIT_FACTOR_ALIGNMENT. PASS_FIRST_F4_UNIFORM_PREFIX_L1_GATE.**
**Overall BOOT candidate correctness: UNCLEAR; CORRECTNESS_GATE=BLOCKED.**

Paper-level uncertainty removed: before Turn23, Turn22 only guaranteed a safe fixed-prefix outer first-F4 multiplication; construction and uniform noise bounds for the **final sibling addition** were unresolved. After Turn23, **the entire first degree-5 F4** is statically constructible with exact explicit BGV factor alignment and a q-independent strictly safe envelope across every Turn22 guaranteed prefix.

No local construction failure or intrinsic algebraic no-go was identified; `mulIntFactor`'s private access is a patch constraint. This is **not** complete Algorithm4 or end-to-end bootstrapping correctness. Mandatory recovery canary remains NOT_EXECUTED; no native context, real ciphertext, actual prime instance, full DFR, later F_e evaluation, full p-adic ladder, baseline, security, value, or independent paper audit has passed.

**Next one paper-first correctness test (NO Native):** prove or falsify the *immediate first post-F4 Algorithm4 subtraction and divideByP boundary*: exact 5-divisibility over Z625, typed metadata and factor through ptxtSpace625→125, fixed-prefix prime-set behavior and independently bounded L1 noise, using the present EFhat. If this fails, identify exact construction/interface failure versus inherent p-adic obstruction. The frozen recovery-only canary remains first future **native** action, not authorized by this turn.

Candidate synchronized state unchanged except the named first-F4 subgate closes: ACTIVE / CORRECTNESS_GATE, Novelty=PREFLIGHT, Security=PENDING, Value=PENDING, Baseline=PENDING, Audit=PENDING, Paper=NOT_READY. No ORCHESTRATOR_CONTROL.
