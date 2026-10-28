# BOOT — IND-CPA-D / reactive-correctness local-randomization gate

Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER_LEVEL_ONLY
CODEX: NOT_USED
NATIVE: NOT_RUN

## Authoritative BOOT state

LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE_GATE: B163_CORRECTED_B160_NOSCALE_SELECTOR_GATE
B163_STATUS: PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
DO_NOT_AUTO_RUN_CODEX: YES

B158_ALGEBRA: PASS
B158_CTCT_MULT_COUNT: OPTIMAL
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B158_NATIVE_FEASIBILITY: UNRESOLVED
B163: NOT_RUN

## Security trigger: new BFV/BGV IND-CPA-D attacks

Hyeongmin Choe, Minsik Kang, Damien Stehle,
"New IND-CPA-D Attacks on BFV and BGV",
IACR ePrint 2026/2546; accepted at ACM CCS 2026.

The public abstract states that the paper gives three new attacks on BFV/BGV instantiated using common heuristic correctness assumptions:

1. bootstrapping-failure attacks extending prior exact-FHE / CKKS-style failure attacks to BFV and BGV, with focus on BGV powerful-basis representation;
2. a BFV secret-key-recovery attack that skews ciphertext noise using crafted plaintexts so plaintext-ciphertext multiplication exceeds heuristic noise bounds;
3. an IND-CPA-D attack that skews the ciphertext mask by adding a selected encryption of zero so the mask norm outpaces heuristic ciphertext-ciphertext multiplication noise assumptions.

Public sources:
https://eprint.iacr.org/2026/2546
https://www.sigsac.org/ccs/CCS2026/program/accepted-papers.html

The full 2546 paper was NOT acquired in this round. Exact attack transcripts, oracle access, parameters, and repair discussion are source-gated.

## Prior security framework

Nigel Smart and Michael Walter,
"Reactive Correctness, sIND-CPA-D-Security and Deterministic Evaluation for TFHE",
IACR Communications in Cryptology 3(1), 2026.

The paper establishes:
- computational/reactive ACER correctness + IND-CPA implies sIND-CPA-D;
- their generic randomized evaluation rerandomizes every input ciphertext BEFORE FHE.Eval by adding a fresh encryption of zero;
- their TFHE proof focuses strongly on adversarially visible ciphertext masks;
- randomized masks turn adversarial inputs into average-case-looking masks under their assumptions;
- a ROM construction derandomizes evaluation while preserving the security argument.

Primary open full text:
DOI 10.62056/aksdkmol
Public full text also available through ResearchGate under CC BY 4.0.

## Theorem 1 — post-evaluation rerandomization cannot erase a known-output failure oracle

Let Eval(c,F) produce c_out and let the adversary know the correct semantic result y=F(m).

Define the failure bit

    fail(c_out,y) = 1[ Dec_sk(c_out) != y ].

Let T be ANY post-processing transformation satisfying plaintext preservation pointwise:

    Dec_sk(T(c)) = Dec_sk(c)

for every ciphertext c in its domain.

Then

    fail(T(c_out),y)
      = 1[ Dec_sk(T(c_out)) != y ]
      = 1[ Dec_sk(c_out) != y ]
      = fail(c_out,y).

Therefore any post-evaluation transformation that preserves the decrypted result exactly leaves the known-output failure oracle unchanged.

Examples covered by the theorem include, when message-preserving:
- output rerandomization;
- key switching;
- modulus switching;
- representation conversion;
- semantic re-encoding.

Status:

    POST_EVAL_RERANDOMIZATION_AS_FAILURE_ORACLE_FIX = FAIL EXACTLY.

The repair must act before the failure-sensitive evaluation, alter the failure distribution itself, correct the result, or prevent the relevant success/failure observation.

## Local-randomization sufficiency criterion

Consider a failure-sensitive stage B in an evaluation pipeline.

Let z be the full stage input and let m=Sem(z) be its semantic plaintext state.
Let R be a randomized local preprocessor and let Fail(B(R(z;r))) be the stage/event failure indicator.

A strong sufficient condition for adversarial-input correctness is:

There exists a canonical distribution D_m depending only on m such that, uniformly for every adversarial z with Sem(z)=m,

    R(z; r) ≈ D_m

(statistically or computationally, according to the target correctness/security notion),

and

    Pr_{w <- D_m}[ Fail(B(w)) = 1 ]

is negligible uniformly over allowed semantic messages/functions.

Then the adversary cannot increase the failure probability through any representation-level feature erased by R, up to the indistinguishability error.

This is a simple data-processing/canonicalization criterion, not a new cryptographic construction.

### Fiberwise form

If R leaves some invariant h(z) unchanged, the relevant condition is instead uniform over each surviving fiber:

    sup_{z: Sem(z)=m, h(z)=h}
        Pr_r[ Fail(B(R(z;r)))=1 ]

must be negligible for every adversarially reachable h.

Therefore local rerandomization cannot establish ACER correctness when the adversary can bias a failure-relevant invariant that R does not randomize.

This provides a cheap kill test for any proposed partial sanitizer.

## Smart–Walter TFHE randomization is PRE-evaluation and mask-oriented

Their generic FHE.ReRand computes a fresh encryption of zero and adds it to every ciphertext before Eval.

For TFHE they instantiate this by:
- generating a zero encryption with TFHE.Enc-Sub;
- DimensionSwitching it to the relevant input ciphertext type;
- adding it to the input ciphertext.

In their Section 8 analysis, they explicitly state that the randomizers statistically rerandomize the ciphertext masks; the remaining gap to their average-case correctness game lies in noise terms.

They make an Assumption 3 concerning those noise terms, and explicitly say this assumption can be avoided using sanitization techniques [BI22, SW25].

Thus:
    TFHE_FULL_PRE_EVAL_RERANDOMIZATION_FOR_ACER = DIRECT PRIOR ART.
    MASK_RANDOMIZATION_AS_CORE_ACER_MECHANISM = DIRECT PRIOR ART.

Sources:
Smart–Walter 2026, Sections 6.1, 7.3, 8.1–8.3.

## Stage-local sanitization is ALSO existing TFHE prior art

Nigel Smart and Michael Walter,
"Error-Simulatable Sanitization for TFHE and Applications",
ePrint 2025/275.

Research MCP recovered the full 40-page paper:
SHA256
83d3054c46fcd0fe6eaa6569551cc5707efe71915b358f4d44af3f5e274775cf
(version status VERSION_UNVERIFIED).

The construction replaces deterministic gadget decomposition G^{-1} inside blind rotation with a randomized lattice-coset decomposition G^{-1}_r.

Its Sanitized-BR then adds a fresh/pseudofresh GLWE zero sample.

Theorem 1 gives an output distribution of the form

    (u, u*s_tilde + e0 + t * X^{-b + sum_i a_i s_i})

with u uniform and e0 close to a prescribed Gaussian-type distribution under the stated assumptions.

Therefore it randomizes/sanitizes the representation-level mask/error while preserving the input phase-dependent rotation exponent.

This distinction is essential:

    representation randomness is sanitized,
    but the semantic/phase state -b + sum_i a_i s_i is intentionally preserved.

The paper targets error-simulatable sanitization, funcCPA, and threshold-decryption applications, not the 2026 BFV/BGV ACER attacks.

However, Smart–Walter 2026 explicitly cites this sanitization line as a way to remove their TFHE noise-distribution assumption.

Therefore:

    GENERIC_STAGE_LOCAL_SANITIZER_TO_TFHE_ACER = PRIOR-ART-ANTICIPATED / NOT A CLEAN NOVELTY CLAIM.

## Why sanitization is not automatically an ACER repair

Output simulation and correctness are different properties.

A sanitizer may ensure that, conditioned on a phase/message, the output mask and fresh error look canonical. That alone does not establish that the preceding or internal evaluation never crosses a correctness boundary.

In particular, if a failure event depends on a stage input invariant that survives the sanitizer — such as:
- semantic plaintext/function coefficients;
- an already-rounded phase;
- a phase drift not erased by the randomization;
- a pre-sanitization modulus-switch failure;

then output sanitization does not by itself bound that failure probability.

The correct requirement is the local-randomization sufficiency criterion above.

## Implication for the three public 2546 attack classes

Because the full paper is unavailable, these are conservative abstract-level classifications only.

### Attack class A — bootstrapping failure

Potentially relevant to local rerandomization, but exact failure variable is UNKNOWN.

Need the full source to identify whether the attack biases:
- a public ciphertext mask;
- input noise/drift;
- a modulus-switch/rounding residue;
- powerful-basis coefficient geometry;
- or a later bootstrap stage.

Status:
    LOCAL_FIX_POSSIBLE = UNKNOWN / SOURCE-GATED.

### Attack class B — crafted plaintext skews BFV multiplication noise

A ciphertext-only rerandomizer does not change the adversarially chosen plaintext multiplier/function.

Therefore fresh mask randomization alone cannot remove the deterministic plaintext-dependent amplification mechanism.

It may change the input noise distribution, but a proof still needs correctness uniformly over the allowed plaintext multiplier.

Status:
    MASK_ONLY_RERANDOMIZATION_AS_GENERIC_FIX = FAIL CONCEPTUALLY.

### Attack class C — ciphertext-mask skew via selected encryption of zero

This is the attack class most naturally aligned with pre-evaluation mask rerandomization.

If a public-key rerandomizer makes the resulting mask statistically/computationally close to the honest mask distribution independently of the attacker's chosen zero encryption, the direct mask-skew channel may be removed.

However:
- exact 2546 attack details are missing;
- added rerandomization noise may create another failure surface;
- reactive repeated-query security needs a formal correctness game.

Status:
    MASK_CANONICALIZATION_FIX = PLAUSIBLE / NOT ESTABLISHED.


## Stronger closure: drift-aware ModSwitch and randomized ModSwitch are already general defenses

Two prior works substantially narrow the remaining BOOT-security space.

### Bernard–Joye–Smart–Walter, ePrint 2024/1718 / EUROCRYPT 2025

"Drifting Towards Better Error Probabilities in Fully Homomorphic Encryption Schemes"

For modulus switching, write the public rounding/drift vector as
    (alpha_1,...,alpha_n,beta)
and the secret-dependent drift as
    e_drift = beta - sum_j alpha_j s_j.

The paper:
- identifies modulus switching drift as the main correctness/IND-CPA-D gap in FHEW/TFHE/FINAL;
- transforms a ciphertext to another encryption of the same message, including by adding encryptions of zero, to change the drift vector;
- applies a PUBLIC quality test before accepting the transformed ciphertext;
- gives both probabilistic mean/variance tests and an exact worst-case bounded-secret test;
- retries the transform until the candidate drift vector passes.

Hence:
    GENERIC_PRE_MODSWITCH_RERANDOMIZE_AND_PUBLIC_DRIFT_TEST = PRIOR ART.

This is stronger than merely saying "add fresh noise": the prior work explicitly exposes a public failure-relevant statistic and rejects bad candidates before ModSwitch.

Primary source:
ePrint 2024/1718; EUROCRYPT 2025.

### Liu–Wang–Fisch, ePrint 2025/1627 / CCS 2025

"IND-CPA-D of Relaxed Functional Bootstrapping: A New Attack, A General Fix, and A Stronger Model"

Research MCP recovered the full PDF:
SHA256
29ee6aeb6263f576e9b976c4b3f6a25813308d98789ba68a4ab5cd2718a5385a
(version status VERSION_UNVERIFIED).

Section 5 defines

    ModSwitch'(pk, ct; r)
      = round( (q'/q) * (ct + Enc_pk(0;r)) ).

The paper's Lemma 5.1 proves the intended IND-CPA-D hiding property under its fixed-Hamming-weight secret setup and modulus/error conditions.

The authors state that this randomized procedure:
- has essentially no overhead relative to bootstrapping;
- prevents their modulus-switching-error inequality hints;
- applies as a general mitigation to existing modulus-switching-error-based exact-FHE bootstrapping attacks as well.

The paper also explains a critical limitation:
in the stronger IND-CPA-DR model, where the adversary observes evaluation randomness, the fix fails because the adversary can recover/subtract the zero-encryption mask and reconstruct the hint.

Therefore:

    GENERIC_HIDDEN_RANDOMNESS_MODSWITCH_ERROR_FIX = DIRECT PRIOR ART.
    "ZERO-OVERHEAD" RANDOMIZED MODSWITCH AS IND-CPA-D REPAIR = DIRECT PRIOR ART.
    IND_CPA_DR_SECURE_VARIANT = NOT SOLVED BY THIS FIX.

### Combined implication for ePrint 2026/2546

The public abstract of 2026/2546 contains three attacks.

Only its first attack class is directly BOOT-specific: extension of bootstrapping-failure attacks to BFV/BGV, with special focus on BGV powerful-basis representation.

The second and third attacks target BFV plaintext-ciphertext and ciphertext-ciphertext multiplication heuristic noise bounds. They are important FHE security results but are not themselves bootstrapping optimizations and should not pull this BOOT track into a generic BFV-noise-security subproject.

For the BOOT-specific first attack, a positive repair is interesting ONLY if the exact 2546 failure variable is not already reducible to:
- the public linear drift-quality model of 2024/1718; or
- a modulus-switching-error hint hidden by 2025/1627's randomized ModSwitch.

If the powerful-basis attack is just a representation-specific instance of such a modulus-switching/drift hint, then:
    NEW_REPAIR_NOVELTY = FAIL.

A surviving target must identify a failure-critical variable that remains visible/correlated even after both defenses.

## Priority update

BOOT_SECURITY_2546:
    DOWNGRADE TO SOURCE-GATED NARROW CHECK.

Reason:
- full-input ACER rerandomization: prior art;
- TFHE stage-local sanitization: prior art;
- public drift-vector candidate testing: prior art;
- randomized zero-encryption ModSwitch with general mod-switch-error hiding claim: prior art.

Only:
    BGV_POWERFUL_BASIS_NON_MODSWITCH_FAILURE_SURFACE
may remain interesting, and this cannot be established from the public abstract.

The exact 2546 PDF is now the only justified next step on this security branch.

Do not spend Codex/native effort on defenses before that source is available.

## Research decision

POST_EVAL_RERANDOMIZATION:
    FAIL EXACTLY.

GENERIC_FULL_PRE_EVAL_RERANDOMIZATION:
    PRIOR ART (BJSW25 / Smart–Walter 2026).

GENERIC_TFHE_STAGE_LOCAL_SANITIZATION:
    PRIOR ART / EXPLICITLY CONNECTED BY SMART–WALTER 2026.

BFV_CRAFTED_PLAINTEXT_ATTACK_FIXED_BY_MASK_RERAND:
    NO, NOT GENERICALLY.

BFV/BGV_MASK_SKEW_LOCAL_FIX:
    PLAUSIBLE BUT SOURCE-GATED.

BFV/BGV_BOOTSTRAP_FAILURE_LOCAL_FIX:
    UNKNOWN / SOURCE-GATED; generic ModSwitch/drift repairs are already prior art.

NOVELTY:
    NOT ESTABLISHED; generic rerandomization/ModSwitch repair is prior art.

CCF_A_B_READINESS:
    NO.

CODEX/NATIVE:
    NOT REQUIRED NOW.

## Positive direction that survives

The only worthwhile security question is narrow and scheme-specific:

    Can one construct a minimal BFV/BGV pre-evaluation canonicalizer
    that randomizes exactly the public/adversarial state exploited by 2026/2546,
    while adding substantially less cost/noise than full ciphertext rerandomization
    and proving reactive correctness for the repaired operation?

This is NOT the same as generic rerandomization.

A CCF-A/B contribution would need:
1. exact reconstruction of one 2546 attack oracle;
2. identification of the minimal failure-critical public statistic;
3. a local canonicalizer that erases that statistic;
4. a reactive correctness / IND-CPA-D proof;
5. proof that other surviving invariants cannot recreate the failure oracle;
6. concrete overhead materially below generic full rerandomization or worst-case-safe parameters.

If the attack-critical statistic is the full ciphertext randomness, or if the cheapest safe repair is simply standard full rerandomization, PARK.

## Next minimum verification

Acquire/read current ePrint 2026/2546.

For EACH attack:
1. write the exact adversarial state variable;
2. write the observable failure predicate;
3. identify which variables are preserved by fresh-zero rerandomization;
4. apply the fiberwise criterion;
5. keep only a repair that canonicalizes all failure-critical public variables;
6. check whether the paper itself already proposes the same repair.

No native experiment is authorized until this paper-level gate survives.

B163 remains the highest native gate when Codex quota returns.
