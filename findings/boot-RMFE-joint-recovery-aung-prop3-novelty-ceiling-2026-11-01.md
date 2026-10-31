# BOOT RMFE Joint-Recovery Novelty Ceiling from Aung Proposition 3

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 11/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Pending native task boundary

Authorized native task:

\`BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01\`

remains UNKNOWN / BACKGROUND.

This turn does not:
- inspect or assume its result;
- modify its source/workdir/binary;
- resubmit it;
- start another heavy native task.

## Read-before-write authority

Current durable authority at turn start:

\`BBBINGW/memory main@e394025b62bb55a365d410c60f34b1a8b2e47931\`.

Relevant durable context:
- post-rounding delayed-fusion novelty collision gate;
- citation closure;
- Turn 5 structural maximal-fusion lemma;
- exact rank-5 joint C2S/correction synthesis;
- exact Moore/norm gate.

## Primary hypothesis

The current four-output joint C2S/correction recovery may constitute an independent structural novelty beyond Aung et al.'s RMFE linear-map framework.

Falsifier:
show that Aung Proposition 3, plus their explicit multi-output automorphism sharing and linear-map functionality, already implies the existence and shared-Frobenius execution of our joint map once the post-MultKey state is recognized as a free rank-5 module.

## Source provenance

Primary source:
Khin Mi Mi Aung, Enhui Lim, Jun Jie Sim, Benjamin Hong Meng Tan, Huaxiong Wang,
*Bootstrapping with RMFE for Fully Homomorphic Encryption*,
ePrint 2025/350 / PKC 2025.

Connected ePrint mirror:
- source kind: GitHub mirror;
- version status: VERSION_UNVERIFIED;
- SHA256:
  \`922c860a838fd8c9a8a5853489ac8ac7706fc3332e2083075540ad5f422bde82\`;
- 30 physical pages.

Web-indexed official ePrint PDF was also inspected textually. A developer-required screenshot attempt for the PDF failed with HTTP 403, so no visual-byte equivalence claim is made.

Springer metadata confirms a PKC 2025 chapter with the same title/authors, DOI
\`10.1007/978-3-031-91832-2_3\`,
pages 71--101. The exact published chapter bytes were not compared with the ePrint mirror in this turn.

## 1. Aung Proposition 3 is already general enough

Aung Proposition 3 states:

Let

\[
G=\operatorname{GR}(p^r,s)
\]

and let \(G'\) be an extension of \(G\). If

\[
f:V\to G'
\]

is \(G\)-linear and \(V\subseteq G'\) is a free rank-\(k\) \(G\)-submodule, then there exist unique

\[
\theta_0,\ldots,\theta_{k-1}\in G'
\]

such that

\[
\boxed{
f(x)=\sum_{j=0}^{k-1}\theta_j\sigma^{sj}(x)
}
\]

for every \(x\in V\).

This is not restricted to:
- the RMFE recode map;
- projection maps;
- the full slot algebra.

It applies to **any** \(G\)-linear map on a free rank-\(k\) submodule.

The proof explicitly solves a \(k\times k\) Moore system.

## 2. Aung already states the multi-output sharing pattern

In their SlotsToCtxts Method 2, Aung uses \(k\) projection maps

\[
\tau'_1,\ldots,\tau'_k
\]

on the same RMFE image submodule.

They explicitly state that, by Proposition 3, evaluating **all** projection maps only requires the **same \(k\)-many automorphisms on the input**.

Thus the following execution principle is already explicit prior art:

\[
\boxed{
\text{many linear outputs on one rank-}k\text{ input}
\Rightarrow
\text{compute one shared Frobenius orbit and reuse it}.
}
\]

Aung further states that CtxtsToSlots may compute other linear maps

\[
L:\operatorname{im}\phi\to G'
\]

by using precomputed basis images.

In their implementation description for the correction workflow, CtxtsToSlots is already used to compute:
- the ciphertext entering DigitExtract;
- images under the correction maps.

Therefore:
- multi-output linear recovery;
- correction-map outputs;
- shared linear processing

are not new conceptual axes.

## 3. Our joint map is a direct specialization once the rank-5 domain is exposed

Current exact interface:

\[
S=\mathbb Z/625\mathbb Z.
\]

Per E8 slot, the post-RM10 active state has free rank 5:

\[
V_{\rm act}
=
\operatorname{span}_S\{u_0,u_1,u_2,u_3,u_4\}.
\]

Let \(L\) denote the established C2S isomorphism on that slot representation.

The actual pre-C2S restricted domain is

\[
U=L^{-1}(V_{\rm act}).
\]

For correction output \(t\in\{0,1,2,3\}\), let

\[
D_t:V_{\rm act}\to E_8
\]

be Aung's required \(S\)-linear correction/recovery map.

Then

\[
f_t
=
D_t\circ L|_U
\]

is an \(S\)-linear map on a free rank-5 module.

After the standard identification of the one-slot coefficient representation with the extension-ring representation, Proposition 3 applies directly:

\[
\boxed{
f_t(x)
=
\sum_{j=0}^{4}
\theta_{t,j}\sigma^j(x).
}
\]

Critically, the automorphism support

\[
\{\sigma^0,\sigma^1,\sigma^2,\sigma^3,\sigma^4\}
\]

depends on the rank, not on \(t\).

So for all four outputs one computes:

\[
x,\sigma(x),\sigma^2(x),\sigma^3(x),\sigma^4(x)
\]

once and only changes the public coefficients \(\theta_{t,j}\).

Therefore the existence of a schedule with exactly four nonidentity Frobenius calls shared across all four outputs is not a new theorem once the rank-5 domain is known.

## 4. Why "joint C2S + correction" itself is also not a new linear-map principle

The separate C2S stage and each correction map are linear.

On the restricted domain,

\[
D_t\circ \mathrm{C2S}
\]

is therefore one linear map.

Aung Proposition 3 does not require the map to be factored according to the original algorithm.

Hence replacing

\[
\mathrm{C2S}
\to
D_t
\]

with one linearized-polynomial representation of the composition is a direct application of:
- composition of linear maps;
- Proposition 3.

The current exact 40/40 basis verification is still scientifically useful because it:
- validates the concrete HElib/R8 identification;
- confirms the stored \(\theta_{t,j}\);
- catches representation/axis mistakes.

But it does not create an independent novelty claim.

## 5. What our support-minimality result does add

Our earlier exhaustive result proved:
- every support of size 1--4 among the available automorphism restrictions fails;
- size 5 is first feasible;
- therefore four nonidentity automorphisms are minimal within the exact automorphism-multiplier family.

Aung Proposition 3 gives a canonical \(k\)-term representation and uniqueness in its Moore basis, but does not, from the source passages inspected here, explicitly prove our instance-specific global support lower bound over the larger tested automorphism set.

Thus:

\[
\boxed{
\text{our 4-call optimality certificate is an additional instance-specific result}.
}
\]

However, this is best viewed as:
- implementation optimality evidence;
- a supporting lemma;

not a strong standalone contribution.

## 6. Relation to Aung's direct-MultKey future work

Aung's conclusion explicitly says it remains to be seen whether the MultKey portion can be performed directly on RMFE-packed ciphertext, avoiding repeated MultKey on the split ciphertexts.

This has an important novelty consequence.

Once a future construction succeeds in preserving a suitable rank-\(k\) packed state through MultKey, Proposition 3 already supplies a generic route for subsequent linear recovery.

So the conceptual sequence

\[
\text{direct packed MultKey}
\to
\text{rank-}k\text{ linear recovery}
\]

is strongly suggested by Aung's own toolkit.

What their source does **not** provide is our current obstruction-aware method for actually reaching that state under HElib branch semantics:

\[
\boxed{
\text{branchwise rawModSwitch}
\to
\text{carry-corrected post-raw fusion}
\to
\text{one common reconstruction}.
}
\]

That remains the material mechanism distinction.

## 7. Revised novelty allocation

The candidate should now be decomposed as follows.

### Prior-art / natural-corollary layer

Do not claim independent novelty for:
- rank-5 Moore/Frobenius representation;
- sharing the same Frobenius orbit across four correction outputs;
- composing C2S with correction maps;
- four-call shared recovery existence;
- computing correction images during a linear recovery phase.

These are either explicitly present in Aung or direct applications of Proposition 3 once the restricted rank-5 domain is exposed.

### Supporting original analysis

Potentially useful but secondary:
- exact HElib/R8 identification of the restricted domain;
- 40/40 basis verification;
- exhaustive proof that 5 terms / 4 nonidentity calls are minimal in the tested automorphism family;
- exact \(\theta\) norm/capacity audit.

### Surviving mechanism-level novelty candidate

The only remaining central mechanism is:

\[
\boxed{
\text{obstruction-aware post-raw delayed fusion}.
}
\]

Specifically:
1. the obvious pre-rounding packed route is not source-equivalent because rawModSwitch representative selection is non-additive;
2. the later divisibility defect is an explicit public carry;
3. after preserving branchwise raw decisions, the two typed channels can be merged;
4. one common boot-key reconstruction produces a rank-5 state;
5. known linear-map machinery can then recover outputs efficiently.

Thus joint recovery should be presented as the **enabling completion after the repair**, not as the repair itself.

## 8. Publication-value consequence

If the pending paired native gate STRONG-PASSES, the plausible paper story is narrower but cleaner:

\[
\text{natural direct-packed attempt}
\;\xrightarrow{\text{fails at branch rounding}}\;
\text{identify maximal exact fusion boundary}
\;\xrightarrow{\text{carry-corrected delayed fusion}}\;
\text{one reconstruction}
\;\xrightarrow{\text{prior-art linear-map machinery}}\;
\text{efficient recovery}.
\]

The intellectual contribution is the obstruction and exact repair ordering.

If the systems gate fails, the instance-specific optimal recovery proof does not by itself justify continuing the branch.

## Verdict

\`\`\`text
RESULT:
  FAIL_JOINT_RECOVERY_STANDALONE_NOVELTY
  PASS_AUNG_PROP3_NATURAL_COROLLARY_CLASSIFICATION

AUNG_PROP3:
  ANY G-LINEAR MAP ON FREE RANK-k SUBMODULE
  -> k FROBENIUS TERMS

AUNG_MULTI_OUTPUT_SHARING:
  EXPLICIT
  SAME k AUTOMORPHISMS REUSED FOR ALL PROJECTION MAPS

AUNG_CORRECTION_LINEAR_OUTPUTS:
  EXPLICIT VIA CTXTSTOSLOTS / PRECOMPUTED BASIS IMAGES

CURRENT_JOINT_MAP:
  D_t o C2S ON RANK-5 DOMAIN
  DIRECT PROP3 SPECIALIZATION

FOUR_SHARED_NONIDENTITY_FROBENIUS_CALLS:
  NATURAL COROLLARY ONCE RANK-5 DOMAIN IS KNOWN

OUR_4_CALL_MINIMALITY_CERTIFICATE:
  ADDITIONAL INSTANCE-SPECIFIC SUPPORTING RESULT
  NOT PRIMARY NOVELTY

HIGH_LEVEL_DIRECT_MULTKEY:
  PRIOR-DISCLOSED AS AUNG FUTURE WORK

SURVIVING_PRIMARY_MECHANISM:
  POST-RAW / CARRY-PRESERVING DELAYED FUSION
  + SINGLE COMMON RECONSTRUCTION

PUBLISHABLE_NOVELTY:
  STILL CONDITIONAL ON NATIVE FRONTIER MOVEMENT
  CLAIM MUST BE NARROW

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  RETAIN PENDING SYSTEMS VALUE

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

Do not spend future turns trying to promote the joint rank-5 recovery itself into an independent paper contribution.

Its role is now settled:
- technically necessary;
- exactly validated;
- operation-count optimal in our tested family;
- but conceptually a natural application of Aung's general linear-map theorem.

Novelty effort should remain centered on the nonlinear branch-rounding obstruction and delayed-fusion repair.
