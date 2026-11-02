# BOOT Research Turn 10/25 — HElib recovery API / metadata / direct-Frobenius realizability gate

Date: 2026-11-02
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Phase: CORRECTNESS_GATE
Candidate: PRE-TAG + POST-DIVIDE LATE AGGREGATION
Pinned HElib: homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1

## Primary hypothesis

Turn 9 supplies a complete exact plaintext-algebra specification for the pruned recovery. The next uncertainty is whether that specification maps source-faithfully to actual pinned HElib Ctxt operations without hidden metadata changes, multi-hop automorphisms, or a different plaintext constant semantics.

Hypothesis:
under HElib FULL Frobenius resources, every one of the 17 required split-node operations can be implemented using existing Ctxt::frobeniusAutomorph, Ctxt addition/subtraction and multByConstant(ZZX), preserving ptxtSpace=625, intFactor, primeSet and key identity as required; each Frobenius is one direct key-switch hop. The only implementation refinement needed is to fold the global normalization 28 into the preceding pure inverse for the production candidate, while a separate x28 is acceptable only for a correctness-only canary.

Falsifier:
- frobeniusAutomorph(j) interprets j differently from p^j;
- FULL addFrbMatrices does not provide direct matrices for the 13 requested j;
- smartAutomorph expands one requested Frobenius into multiple hidden hops even in FULL mode;
- global X^{-s} cannot be represented as a ZZX constant with the correct two-slot action;
- split operations alter ptxtSpace/intFactor/primeSet or trigger BGV factor harmonization;
- the shared reconstructed ciphertext is under a key ID incompatible with the FULL Frobenius matrices.

## Source audit

### 1. Frobenius argument semantics

Pinned src/Ctxt.cpp implements:

Ctxt::frobeniusAutomorph(long j):
- d = context.getOrdP();
- j = j mod d;
- val = p^j mod m;
- smartAutomorph(val).

Thus the Turn-9 labels
[4096,2048,1024,512,256,128,64,32,16,8,4,2,1]
are exactly Frobenius exponents j, not raw Z_m^* automorphism values.

For m=32768,p=5 the corresponding global automorphism values are:
4096->16385
2048->24577
1024->28673
512->30721
256->31745
128->15873
64->7937
32->28545
16->28609
8->30177
4->625
2->25
1->5.

All are distinct because ord_32768(5)=8192.

### 2. FULL Frobenius matrices are direct

Pinned src/keySwitching.cpp:
addFrbMatrices(sKey,keyID)
 -> addSomeFrbMatrices(...,LONG_MAX,...)
 -> add1Dmats4dim(sKey,-1,keyID).

For i=-1 (Frobenius), add1Dmats4dim sets ord=getOrdP(), native=true, then for every j=1,...,ord-1 executes

  GenKeySWmatrix(1, zMStar.genToPow(-1,j), keyID,keyID)

and sets

  KS_strategy(-1)=HELIB_KSS_FULL.

Therefore keyID 0 has a direct key-switch matrix for every nonidentity p^j, including all 13 requested exponents.

Pinned PubKey::setKeySwitchMap performs BFS beginning at node 1. Since every p^j has a direct edge to 1, each p^j is discovered from the root with its direct matrix before any longer path can be assigned.

Pinned Ctxt::smartAutomorph(k) repeatedly calls getNextKSWmatrix(k,keyID), applies its fromXPower automorphism, relinearizes, and updates k <- k/amt. In FULL Frobenius mode, for k=p^j the first matrix has amt=k, so the update immediately gives k=1.

Therefore one call

  ctxt.frobeniusAutomorph(j)

per active node induces exactly one global automorphism + one direct relinearization/key-switch hop under the declared FULL resources.

There is no hidden multi-hop expansion in the canonical resource model.

### 3. Shared reconstructed ciphertext uses key #0

Pinned include/helib/keys.h documents recryptEkey as the bootstrapping key encrypted under key #0.

Pinned SecKey::genRecryptData:
- imports a new recryption secret as recryptKeyID;
- generates the input->recrypt-key switch matrix;
- Encrypt(recryptEkey,keyPoly,p2ePr) under key #0.

The late-aggregation reconstruction begins by assigning out=recryptEkey and then applies public constants. Therefore the post-reconstruction recovery ciphertext is again under key #0.

The ordinary addFrbMatrices(secretKey) FULL matrices with default keyID=0 are therefore the correct matrices for the 17 recovery Frobenius calls.

No new Frobenius matrices for recryptKeyID are required after reconstruction.

### 4. Global odd-child monomial is directly representable

For m=32768,

Phi_m(X)=X^16384+1.

Let N=16384 and s=2^(i-1). In the plaintext ring,

  X^{-s} = -X^(N-s).

Hence the Turn-9 odd-child operation can be represented by the ordinary integer polynomial

  mon_s = -X^(16384-s),

which has degree <16384 and coefficients in {-1,0,1}.

Pinned Ctxt::multByConstant(const NTL::ZZX& poly):
- computes embeddingLargestCoeff(poly) if size is omitted;
- constructs DoubleCRT(poly,context,primeSet);
- multiplies every CtxtPart by that DoubleCRT;
- changes only the tracked noiseBound by the public size factor.

It does not modify ptxtSpace, intFactor or primeSet.

For +/-X^k the canonical embedding magnitude is exactly one, so every retained odd-child global monomial has public multiplier norm one.

This is exactly the global constant semantics required by Turns 8-9; it is not repeated-slot encoding of a local X^{-s}.

### 5. Automorphism and split-add metadata invariants

Pinned Ctxt::automorph(k):
- applies F(X)->F(X^k) to all parts;
- updates the secret-key handle powerOfX;
- does not modify ptxtSpace, intFactor, primeSet or noiseBound.

smartAutomorph then relinearizes back to the same keyID.

For each split node, c and sigma(c) therefore have equal:
- context/pubKey;
- ptxtSpace=625;
- intFactor;
- primeSet;
- keyID after relinearization.

Pinned Ctxt::addCtxt only invokes BGV intFactor harmonization when intFactor differs, and only mod-ups when prime sets differ. Neither condition holds for c +/- sigma(c).

Thus every retained child remains at the same temporary BGV metadata interface. No hidden factor harmonization or prime-set expansion is introduced by the binary tree itself.

### 6. Production normalization placement

Turn 9's exact plaintext canary multiplies each final leaf by 28=8192^{-1} mod625 for semantic clarity.

That is correctness-equivalent but should NOT be the canonical production placement.

Pinned multByConstant(28) would multiply HElib's tracked noiseBound by the canonical size 28. Applying it independently to five leaves would invalidate the inherited public/noise ledger, which already assumes normalization is folded into the preceding pure inverse.

The inherited pure inverse matrix is

  A^{-1}=[[313,91],[313,534]] mod625.

Multiplying by 28 gives

  28*A^{-1}=[[14,48],[14,577]]
            =[[14,48],[14,-48]] centered.

Because 28 is a base-ring scalar fixed by all Frobenius automorphisms and commutes with addition and monomial multiplication, pre-normalizing the pure-inverse output is algebraically identical to applying 28 after all 13 split levels.

Canonical production contract:
- pure inverse includes the factor 28;
- binary tree then returns already-normalized selected leaves;
- no separate x28 leaf multiplication.

Correctness-only debugging may optionally leave the inverse unnormalized and multiply leaves by 28, but such a build must not be used for noise/capacity/performance evidence.

## Exact Ctxt implementation contract

For an active node (residue r, ciphertext c) at level i:

1. tmp = c;
2. tmp.frobeniusAutomorph(8192 / 2^i);
3. even = c; even += tmp;
4. odd = c; odd -= tmp;
5. if odd subtree retained:
     construct ZZX mon with coefficient -1 at exponent 16384-2^(i-1);
     odd.multByConstant(mon);
6. retain even/odd according to target residue metadata.

Production input to the tree must already include the x28 normalization folded into the pure inverse.

Required assertions:
- context p=5,m=32768, ordP=8192;
- ptxtSpace==625 before and after every node;
- common intFactor unchanged across every node;
- same primeSet across parent, automorph copy and retained children;
- keyID==0 after each frobeniusAutomorph;
- getKSStrategy(-1)==HELIB_KSS_FULL for the canonical 17-call count;
- final coordinate order / metadata obey Turn 9;
- no rho_pos+443 post-unpack correction.

## Verdict

PASS_HELIB_RECOVERY_API_REALIZABILITY
PASS_FULL_FROBENIUS_ONE_HOP_CONTRACT
PASS_GLOBAL_MONOMIAL_ZZX_TYPING
PASS_SPLIT_METADATA_INVARIANCE
REFINE_NORMALIZATION_PLACEMENT_PRE_TREE

This closes the source/API feasibility portion of the recovery correctness gate.

It does NOT establish:
- actual ciphertext decryption correctness of an implemented 17-call tree;
- baseline Aung correctness;
- candidate end-to-end correctness;
- numerical noise/capacity/DFR;
- performance.

The next decisive test remains one concrete recovery-only HElib canary using the exact Turn-9 routing and this Turn-10 API contract. It must run correctness before any timing.

NOVELTY_STATUS=PREFLIGHT.
SECURITY_GATE=PENDING.
VALUE_GATE=PENDING.
PAPER_READINESS=NOT_READY.
