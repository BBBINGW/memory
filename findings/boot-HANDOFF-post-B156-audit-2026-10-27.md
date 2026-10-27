# BOOT Session Handoff — Post B156 Audit / B157 Pending

- Date: 2026-10-27
- TRACK_ID: BOOT
- LATEST_COMPLETED: B156-AUDIT
- NEXT_ITERATION: B157 — PENDING_CODEX_QUOTA
- CURRENT_STATUS: ACTIVE_RESEARCH / NATIVE_GATE_REACHED
- NOVELTY: PROMISING_NOT_ESTABLISHED
- CODEX_REQUIRED: YES_FOR_B157, BUT DEFERRED DUE TO QUOTA
- DO_NOT_AUTO_RUN_CODEX: YES

## 1. Research identity

This handoff is authoritative for resuming the independent FHE Bootstrapping research line only.

Strictly isolate BOOT from SHIP, PURE-FHE, CGS, VFHE, EXPLORE, EAI and other tracks.

Research method remains:

smallest falsifiable claim -> cheapest decisive test -> minimal verification -> expand only if warranted

Priority order:
source/prior-art plausibility
-> algebra/counterexample
-> correctness
-> assumptions/security
-> noise/DFR/precision
-> matched native benchmark

Do not launch Codex/GPU/remote/native work without explicit PI authorization.

## 2. Earlier parked branches

Keep previous B121-B141 parked/frozen as already recorded in boot-STATE. Do not repeat:
- sorted bootstrapping/CMS;
- automorphism traversal DP;
- Descent-PBS input-KSK compression;
- phase-decomposition small-alphabet grouping;
- CI-CKKS CtS scheduling/Hermite variants;
- low-rank FBT local optimization;
- packed-key direct consumption;
- conjugate-pair base-table NTT reuse;
- multi-level frequency-basis variants;
- GCKKS local split-clean reorderings.

## 3. B135 source audit

ePrint 2026/2119 full source was supplied and audited.

Important established facts:
- 8.2 ms headline is LL13 complex on RTX PRO 6000;
- N=2^13, measured precision about 5.18 bits, one remaining multiplication level;
- batch64 4.6 ms/ciphertext;
- high-precision LL14 is about 23.1 bits but 44 ms batch1 / 29 ms batch64;
- fair matched SHIP evidence is CPU LL13 speedup about 2.5x real / 3.7x complex;
- one-time evaluation-key reconstruction is excluded from bootstrap latency;
- resident GPU key bytes and stage-by-stage GPU timing are not reported.

## 4. Main active positive candidate: B145

Canonical file:
findings/boot-B145-single-fbs-adjacent-window-a2b-2026-10-27.md

Target:
single-FBS non-amortized Arithmetic-to-Boolean conversion for the power-of-two arithmetic polynomial representation of ePrint 2026/1869.

Core source identity before the first FBS:

    x_j = d_j + U_j - B U_{j+1}.

B145 forms, before any FBS:

    y_j = B x_j + x_{j-1}
        = B d_j + d_{j-1} + U_{j-1} - B^2 U_{j+1}.

Therefore modulo B^2:

    y_j mod B^2 = B d_j + d_{j-1} + U_{j-1}.

This cancels the intermediate overflow U_j before bootstrapping and creates a 2026/2368-style two-digit window directly from the 1869 arithmetic representation.

The goal is:

    two sequential FBS -> one sequential FBS.

For n=256:
- B=64;
- u=ceil(256/6)=43;
- W=B^2=4096.

## 5. Boundary repair and minimum radix

Source-backed refreshed overflow bound from 1869:

    |U| <= 16.

Thus E=16.

The attractive radix B=64 lies at B=4E, while 2368's simplified recurrence assumes B>4E.

B145 derived the exact boundary-corrected affine recurrence:

    G(b)=1[32<=b<64],
    L(c)=1[c<32],
    P(b)=1[b=0],
    T(b)=1[b=32],

    sigma_j
      = G(b_j)
        + L(c_j)(P(b_j)-T(b_j)) sigma_{j-1}.

The slope can be -1, but 2368's affine pair composition supports arbitrary real affine maps.

Randomized exact-integer falsification over n=32,64,128,256 and edge overflow cases passed.

B155 proved a local-window lower bound:
if B<=2E, the same observed window can correspond to two different correct high digits. With E=16, any deterministic one-window construction needs B>32. Among power-of-two radices:

    B_min=64.

Therefore the 4096-point window domain is minimal in the current source-faithful local-window model.

## 6. B151/B152 optimized direct backend

B151 exact identities at B=64,E=16:

    F_k(b)=bit_k(b),
    D_k=L(c)(F_k(b-1)-F_k(b)).

The carry state is already the highest-bit pair:

    G = F5,
    S = D5.

Therefore separate carry LUTs are redundant.

B152 preferred direct backend requests only eight real 4096-point LUT outputs:

    F0,F1,F2,F3,F4,F5,L,D5.

Synthesize D0..D4 homomorphically in parallel with the carry prefix.

Let a_r=1-F_r.

Depth 1:
    p01=a0*a1
    p23=a2*a3

Depth 2:
    Z3=p01*a2
    Z4=p01*p23
    Z1=a0
    Z2=p01

Depth 3:
    A1=L*Z1
    A2=L*Z2
    A3=L*Z3
    A4=L*Z4
    D0=L*(1-2F0)

Depth 4:
    D1=A1*(1-2F1)
    D2=A2*(1-2F2)
    D3=A3*(1-2F3)
    D4=A4*(1-2F4)

Carry prefix:
    sigma_j = F5_j + D5_j sigma_{j-1}

with associative affine prefix scan.

At n=256:
- prefix depth = 6;
- D0..D4 synthesis depth = 4 and runs in parallel;
- final corrections for bits 0..4 add one level;
- bit5 is the prefix intercept;
- critical post-LUT depth = 7.

B152 uses:
- 8 direct LUT branches;
- 13 correction-synthesis CMults;
- 6 prefix CMults;
- 5 final correction CMults.

## 7. Paper-only gates already passed

B153:
- conservative error/depth gate PASS;
- synthesized correction error remains comfortably below 1/2 rounding threshold for source-like 6-8 bit LUT precision;
- no new structural correctness blocker;
- critical depth unchanged.

B154:
- direct prior-art collision not found;
- 2026/233 explicitly leaves non-amortized O(1)-bootstrapping arithmetic->Boolean conversion as an open problem;
- 1836 uses 3 bootstraps for power-of-two A2B;
- 1840 and 1869 use two sequential FBS;
- 2368 gets one-bootstrap decomposition from ordinary real/integer slots but explicitly notes the two-FBS structure of 1840/1869 and does not derive the arithmetic-polynomial pre-FBS cancellation.

Novelty label:
PROMISING / NOT ESTABLISHED.

## 8. Backend audits

B147:
full 2026/1264 LRMT-FBT audit.

B145's required 4096-point functions are exact rank-1 under 64x64 reshape, but the complete LRMT-FBT uses functional digit decomposition. At P=4096 it chooses p=8 and performs four sequential SlotsMVB/FBS digit extractions before the rank-1 evaluator.

Therefore:
FAIL_DIRECT_LRMT_TRANSPLANT.

Keep low-rank structure as a hint only.

B148:
phase-quotient root splitting is algebraically valid but adds about log2(B) extra serial depth and collides with modulus headroom. PARK.

B149:
SWIFT 2026/1163 is not the matched-throughput backend because slot expansion occurs per radix window. For n=256 there are 43 windows/message, producing about 11x-51x packing loss depending on t. PARK as primary backend; small-batch latency variant only.

B150:
joint ordinary Fourier support of six bit LUTs is nearly dense:
union support = 4033/4096.
Sparse-Hermite 2026/1026 remains a supporting source, not a blocker.

## 9. B156 Codex native artifact

Artifact:
BOOT-B156-ONE-FBS-A2B-NATIVE.zip

SHA-256:
7ae78aafe5fd4331a93f5d88653ae04473a47045669b1572ac52d1a547b3936d

Independent audit file:
findings/boot-B156-native-artifact-audit-2026-10-27.md

Baseline native result:
- implementation: source-faithful fhe-simd-alu, pristine import 0482dc2;
- N=65536;
- HEStd_128_classic;
- n=256;
- packing=256 words/ciphertext;
- FBS count=2;
- depth=28;
- log2(QP)=1690;
- correctness=65536/65536 bits;
- failed words=0/256;
- max decoded bit error=0.0011852546;
- total native A2B=62.481726 s;
- core A2B excluding optional output reordering=48.994713 s;
- peak sampled memory=76.8 GiB.

Codex initially returned:
    FAIL_SECURITY_MODULUS

for a packed-output candidate with:
- depth 33;
- packed-output +1 level;
- minimum QP=1760;
- source paper bound about 1746.

This packed variant genuinely fails.

## 10. Independent B156 audit: failure label overruled

Codex treated two conditions as mandatory that should not have been hard failure conditions:

1. optional Boolean output repacking as a mandatory +1 level;
2. baseline HYBRID NumLargeDigits=8 as a required matching parameter.

The original native task explicitly allowed native Boolean output layout and said not to spend effort on cosmetic output repacking.

The source baseline itself reports core A2B before optional output reordering.

The B156 artifact found a surviving parameter point:

    N=65536
    depth=32
    scaleBits=50
    Q towers=33
    Q=1650 bits
    P=60 bits
    QP=1710 bits
    NumLargeDigits=33

and:

    1710 < approximately 1746.

Changing NumLargeDigits changes key-switch performance/key memory, but is not by itself a change in plaintext packing, ring dimension, secret distribution, or security target.

However this point was enumerated with HEStd_NotSet and was NOT instantiated under exact HEStd_128_classic.

Therefore canonical B156 status is:

    FAIL_PACKED_VARIANT_SECURITY
    / UNPACKED_CORE_CANDIDATE_REMAINS_VIABLE
    / REOPEN_NATIVE_GATE

Do NOT call B145 killed.

## 11. B157 — pending due Codex quota

B157 is the next decisive test but MUST NOT be run automatically.

Reason for pause:
Codex quota unavailable.

Exact fixed test when quota returns:

    N=65536
    n=256
    B=64
    W=4096
    scaleBits=50
    depth=32
    NumLargeDigits=33
    HEStd_128_classic
    same source-faithful secret/error setting
    no optional output repacking
    packing target=256 words/ciphertext.

First instantiate this exact point with HEStd_128_classic and source-matched lattice estimator.

If exact point fails:
    FAIL_SECURITY_MODULUS_CONFIRMED.

If security passes:
run the full B145+B152 one-FBS candidate.

Primary fair latency baseline:

    48.99471343 s

not 62.48 s, because both arms should exclude optional cosmetic output reordering.

Measure:
- correctness;
- max/mean decoded bit error;
- minimum rounding margin;
- actual sequential FBS count;
- total core latency and stage breakdown;
- Q/P/QP;
- NumLargeDigits impact;
- KS/key memory;
- peak RSS;
- packing capacity.

Do not reduce scaleBits to 49 yet.
Do not increase N.
Do not force NumLargeDigits back to 8.
Do not add output repacking.

## 12. Source status

Supplied/resolved:
- 2026/2119
- 2026/2368
- 2026/1163
- 2026/1264
- 2026/1869
- 2026/1840
- 2026/1836
- 2026/2531
- 2026/2600

Supporting missing source:
- 2026/1026 Sparse Hermite — useful, not blocking B145.

Separate high-value ring-switching source gate may still remain for:
- 2026/1779
- 2026/1023
unless later supplied.

## 13. Resume rule

When the next GPT session starts:

1. read this handoff first;
2. read findings/boot-STATE.md;
3. read findings/boot-B156-native-artifact-audit-2026-10-27.md;
4. do NOT rerun B145-B156 paper analysis;
5. do NOT launch B157 while Codex quota is unavailable;
6. while B157 is pending, either:
   - do fresh BOOT source scouting for a separate high-value candidate, OR
   - do only paper-level checks that cannot invalidate the pending native experiment;
7. once PI says Codex quota is available, resume B157 exactly from the fixed point above.

Current authoritative state:

TRACK_ID: BOOT
LATEST_COMPLETED: B156_AUDIT
NEXT: B157_PENDING_CODEX_QUOTA
MAIN_POSITIVE_CANDIDATE: B145+B152
B145_STATUS: PROMISING / NATIVE_SECURITY+PERF_UNRESOLVED
CODEX_REQUIRED: YES_FOR_B157
CODEX_AVAILABLE: NO
NOVELTY: PROMISING_NOT_ESTABLISHED
